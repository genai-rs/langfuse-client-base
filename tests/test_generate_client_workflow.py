"""Execute and guard the generation workflow's publication boundaries."""

import ast
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from itertools import product
import os
from pathlib import Path
import re
import subprocess
import tempfile
from threading import Thread
from types import SimpleNamespace
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/generate-client.yml"
ALLOWED_EXPRESSION_NODES = {
    ast.Expression,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Compare,
    ast.Eq,
    ast.Name,
    ast.Attribute,
    ast.Constant,
    ast.Load,
}


def evaluate_actions_expression(expression, context):
    """Evaluate the workflow's boolean expression subset, not a copied gate."""
    python_expression = expression.replace("&&", " and ").replace("||", " or ")
    python_expression = re.sub(r"(?<!['\"])\btrue\b(?!['\"])", "True", python_expression)
    tree = ast.parse(python_expression, mode="eval")
    if any(type(node) not in ALLOWED_EXPRESSION_NODES for node in ast.walk(tree)):
        raise AssertionError("unexpected syntax in the workflow expression")

    def namespace(value):
        if isinstance(value, dict):
            return SimpleNamespace(**{key: namespace(item) for key, item in value.items()})
        return value

    return eval(
        compile(tree, str(WORKFLOW), "eval"),
        {"__builtins__": {}},
        {key: namespace(value) for key, value in context.items()},
    )


def render_group(template, context):
    return re.sub(
        r"\$\{\{\s*(.*?)\s*\}\}",
        lambda match: str(evaluate_actions_expression(match.group(1), context)),
        template,
    )


def step_named(steps, name):
    return next(step for step in steps if step["name"] == name)


class GenerateClientWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)

    def test_manual_runs_default_to_validation_only(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]["inputs"]["publish"]
        self.assertEqual(dispatch["type"], "boolean")
        self.assertEqual(dispatch["default"], "false")
        self.assertEqual(dispatch["required"], "false")

    def test_only_schedule_pull_request_and_manual_dispatch_start_workflow(self):
        self.assertEqual(set(self.workflow["on"]), {"schedule", "pull_request", "workflow_dispatch"})
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        self.assertEqual(
            self.workflow["on"]["pull_request"]["branches"],
            ["main", "feat/generation-provenance"],
        )

    def test_actual_publish_expression_allows_only_successful_main_publications(self):
        expression = self.workflow["jobs"]["publish"]["if"]
        scenarios = product(
            ("success", "failure", "cancelled", "skipped"),
            ("true", "false"),
            ("refs/heads/main", "refs/heads/feature", "refs/pull/42/merge"),
            ("schedule", "workflow_dispatch", "pull_request"),
            (True, False),
        )
        for result, has_changes, ref, event, publish_input in scenarios:
            with self.subTest(
                result=result,
                has_changes=has_changes,
                ref=ref,
                event=event,
                publish_input=publish_input,
            ):
                actual = evaluate_actions_expression(
                    expression,
                    {
                        "needs": {
                            "validate": {
                                "result": result,
                                "outputs": {"has_changes": has_changes},
                            }
                        },
                        "github": {"ref": ref, "event_name": event},
                        "inputs": {"publish": publish_input},
                    },
                )
                expected = (
                    result == "success"
                    and has_changes == "true"
                    and ref == "refs/heads/main"
                    and (event == "schedule" or (event == "workflow_dispatch" and publish_input))
                )
                self.assertEqual(actual, expected)

    def test_pr_validation_cannot_cancel_or_join_trusted_publication_group(self):
        jobs = self.workflow["jobs"]
        validation_group = jobs["validate"]["concurrency"]["group"]
        publish_group = jobs["publish"]["concurrency"]["group"]
        keepalive_group = jobs["keepalive"]["concurrency"]["group"]
        self.assertEqual(jobs["validate"]["concurrency"]["cancel-in-progress"], "true")
        self.assertEqual(jobs["publish"]["concurrency"]["cancel-in-progress"], "false")
        self.assertNotIn("concurrency", self.workflow)

        scheduled_main = {"github": {"event_name": "schedule", "ref": "refs/heads/main"}}
        pull_request = {"github": {"event_name": "pull_request", "ref": "refs/pull/42/merge"}}
        self.assertNotEqual(
            render_group(validation_group, scheduled_main),
            render_group(validation_group, pull_request),
        )
        self.assertNotEqual(publish_group, keepalive_group)
        self.assertNotEqual(render_group(validation_group, scheduled_main), publish_group)

    def test_validated_base_and_candidate_tree_are_artifact_outputs(self):
        validate = self.workflow["jobs"]["validate"]
        self.assertIn("steps.changes.outputs.base_sha", validate["outputs"]["validated_base_sha"])
        self.assertIn("steps.changes.outputs.tree_sha", validate["outputs"]["validated_tree_sha"])
        save = step_named(validate["steps"], "Save validated changes")["run"]
        for required in (
            "git rev-parse HEAD",
            "git add -- src/ Cargo.toml docs/ openapi.yml",
            "git write-tree",
            "git diff --cached --binary HEAD > validated.patch",
            "validated-base.sha",
            "validated-tree.sha",
        ):
            self.assertIn(required, save)

        publish = self.workflow["jobs"]["publish"]
        checkout = step_named(publish["steps"], "Checkout validated base")
        self.assertEqual(
            checkout["with"]["ref"],
            "${{ needs.validate.outputs.validated_base_sha }}",
        )
        verify = step_named(publish["steps"], "Verify validated base and candidate tree")["run"]
        for required in (
            "git rev-parse HEAD",
            "validated-base.sha",
            "git apply --index --binary validated.patch",
            "git write-tree",
            "validated-tree.sha",
        ):
            self.assertIn(required, verify)

    def test_publish_applies_only_the_artifact_for_its_validated_base_and_tree(self):
        publish_steps = self.workflow["jobs"]["publish"]["steps"]
        verify = step_named(
            publish_steps, "Verify validated base and candidate tree"
        )["run"]

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)

            def git(*args):
                return subprocess.run(
                    ["git", *args],
                    cwd=repo,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            git("init", "--quiet")
            git("config", "user.name", "Workflow test")
            git("config", "user.email", "workflow-test@example.invalid")
            source = repo / "src.txt"
            source.write_text("validated base\n", encoding="utf-8")
            git("add", "src.txt")
            git("commit", "--quiet", "-m", "base")
            base_sha = git("rev-parse", "HEAD")

            source.write_text("validated candidate\n", encoding="utf-8")
            patch_file = repo / "validated.patch"
            patch_file.write_text(
                git("diff", "--binary", "HEAD") + "\n", encoding="utf-8"
            )
            git("add", "src.txt")
            tree_sha = git("write-tree")
            git("reset", "--hard", "HEAD")
            (repo / "validated-base.sha").write_text(base_sha + "\n", encoding="utf-8")
            (repo / "validated-tree.sha").write_text(tree_sha + "\n", encoding="utf-8")

            command = (
                verify.replace(
                    "${{ needs.validate.outputs.validated_base_sha }}", base_sha
                )
                .replace("${{ needs.validate.outputs.validated_tree_sha }}", tree_sha)
            )
            accepted = subprocess.run(
                ["bash", "-e", "-c", command],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(git("write-tree"), tree_sha)

            git("reset", "--hard", "HEAD")
            wrong_base = "0" * 40
            wrong_base_command = command.replace(base_sha, wrong_base)
            rejected_base = subprocess.run(
                ["bash", "-e", "-c", wrong_base_command],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(rejected_base.returncode, 0)

            wrong_tree = "0" * 40
            (repo / "validated-tree.sha").write_text(wrong_tree + "\n", encoding="utf-8")
            wrong_candidate = command.replace(tree_sha, wrong_tree)
            rejected = subprocess.run(
                ["bash", "-e", "-c", wrong_candidate],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(rejected.returncode, 0)

    def test_candidate_is_never_rebased_or_mutated_after_validation(self):
        publish = self.workflow["jobs"]["publish"]
        step_names = [step["name"] for step in publish["steps"]]
        self.assertIn("Push the exact validated tree", step_names)
        self.assertIn("Create PR for the validated candidate", step_names)
        self.assertLess(
            step_names.index("Verify validated base and candidate tree"),
            step_names.index("Create GitHub App token"),
        )
        self.assertLess(
            step_names.index("Create GitHub App token"),
            step_names.index("Push the exact validated tree"),
        )
        self.assertLess(
            step_names.index("Push the exact validated tree"),
            step_names.index("Create PR for the validated candidate"),
        )
        serialized = "\n".join(str(step) for step in publish["steps"])
        self.assertNotIn("updateBranch", serialized)
        self.assertNotIn("--auto", serialized)
        self.assertNotIn("peter-evans/create-pull-request", serialized)

        preflight = step_named(publish["steps"], "Check main and existing generated PR")["run"]
        self.assertIn("validated_base_sha", preflight)
        self.assertIn("main_sha", preflight)
        self.assertIn("skip=true", preflight)
        commit = step_named(publish["steps"], "Push the exact validated tree")["run"]
        self.assertIn("git rev-parse 'HEAD^{tree}'", commit)
        self.assertIn("VALIDATED_TREE_SHA", commit)
        create_pr = step_named(publish["steps"], "Create PR for the validated candidate")["run"]
        self.assertIn("git push origin --delete", create_pr)
        self.assertIn("VALIDATED_BASE_SHA", create_pr)
        for name in ("Push the exact validated tree", "Create PR for the validated candidate"):
            step = step_named(publish["steps"], name)
            self.assertIn("GH_TOKEN", step["env"])

    def test_raw_git_push_uses_temporary_auth_and_rejected_transport_fails_closed(self):
        publish_steps = self.workflow["jobs"]["publish"]["steps"]
        configure = step_named(publish_steps, "Configure temporary Git authentication")
        push = step_named(publish_steps, "Push the exact validated tree")
        cleanup = step_named(publish_steps, "Remove temporary Git authentication helper")
        self.assertLess(
            publish_steps.index(configure),
            publish_steps.index(push),
        )
        self.assertLess(
            publish_steps.index(step_named(publish_steps, "Create GitHub App token")),
            publish_steps.index(configure),
        )
        self.assertIn("GH_TOKEN", configure["env"])
        self.assertIn("always()", cleanup["if"])

        token = "workflow-test-token"
        auth_header = "Basic " + base64.b64encode(
            f"x-access-token:{token}".encode("ascii")
        ).decode("ascii")

        class RejectingGitHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.server.auth_headers.append(self.headers.get("Authorization"))
                if self.headers.get("Authorization") == auth_header:
                    self.send_response(403)
                else:
                    self.send_response(401)
                    self.send_header("WWW-Authenticate", 'Basic realm="mock git"')
                self.send_header("Content-Length", "0")
                self.end_headers()

            def do_POST(self):
                self.server.post_requests += 1
                self.send_response(403)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, _format, *_args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), RejectingGitHandler)
        server.auth_headers = []
        server.post_requests = 0
        server_thread = Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                repo = Path(temp_dir)
                runner_temp = repo / "runner-temp"
                runner_temp.mkdir()
                output_file = repo / "github-output"
                mock_bin = repo / "mock-bin"
                mock_bin.mkdir()
                gh = mock_bin / "gh"
                gh.write_text(
                    "#!/bin/sh\nprintf '%s\\n' \"$VALIDATED_BASE_SHA\"\n",
                    encoding="utf-8",
                )
                gh.chmod(0o700)

                def git(*args):
                    return subprocess.run(
                        ["git", *args],
                        cwd=repo,
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout.strip()

                git("init", "--quiet")
                git("config", "user.name", "Workflow test")
                git("config", "user.email", "workflow-test@example.invalid")
                source = repo / "src.txt"
                source.write_text("validated base\n", encoding="utf-8")
                git("add", "src.txt")
                git("commit", "--quiet", "-m", "base")
                base_sha = git("rev-parse", "HEAD")
                source.write_text("validated candidate\n", encoding="utf-8")
                git("add", "src.txt")
                tree_sha = git("write-tree")
                git("remote", "add", "origin", f"http://127.0.0.1:{server.server_port}/repo.git")

                env = os.environ.copy()
                env.update(
                    {
                        "GH_TOKEN": token,
                        "GITHUB_SERVER_URL": f"http://127.0.0.1:{server.server_port}",
                        "GITHUB_REPOSITORY": "genai-rs/langfuse-client-base",
                        "GITHUB_OUTPUT": str(output_file),
                        "RUNNER_TEMP": str(runner_temp),
                        "VALIDATED_BASE_SHA": base_sha,
                        "VALIDATED_TREE_SHA": tree_sha,
                        "RUN_ID": "123",
                        "RUN_ATTEMPT": "1",
                        "PATH": f"{mock_bin}{os.pathsep}{env['PATH']}",
                        "GIT_TERMINAL_PROMPT": "0",
                    }
                )
                configured = subprocess.run(
                    ["bash", "-e", "-c", configure["run"]],
                    cwd=repo,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(configured.returncode, 0, configured.stderr)
                auth_dir = Path(
                    next(
                        line.split("=", 1)[1]
                        for line in output_file.read_text(encoding="utf-8").splitlines()
                        if line.startswith("auth_dir=")
                    )
                )
                helper = auth_dir / "credential-helper"
                self.assertTrue(helper.is_file())
                self.assertNotIn(token, helper.read_text(encoding="utf-8"))
                self.assertNotIn(token, git("config", "--local", "--get", "credential.helper"))

                pushed = subprocess.run(
                    ["bash", "-e", "-c", push["run"]],
                    cwd=repo,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(pushed.returncode, 0)
                self.assertIn(auth_header, server.auth_headers)
                self.assertEqual(server.post_requests, 0)
                branch = "automated/generate-client-123-1"
                self.assertEqual(git("rev-parse", f"refs/heads/{branch}^{{tree}}"), tree_sha)

                cleanup_env = env.copy()
                cleanup_env["AUTH_DIR"] = str(auth_dir)
                cleaned = subprocess.run(
                    ["bash", "-e", "-c", cleanup["run"]],
                    cwd=repo,
                    env=cleanup_env,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(cleaned.returncode, 0, cleaned.stderr)
                self.assertFalse(auth_dir.exists())
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=2)

    def test_pr_body_keeps_manifest_filename_literal_in_expanding_heredoc(self):
        publish_steps = self.workflow["jobs"]["publish"]["steps"]
        create_pr = step_named(publish_steps, "Create PR for the validated candidate")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            mock_bin = root / "mock-bin"
            mock_bin.mkdir()
            body_path = root / "captured-pr-body.md"
            gh = mock_bin / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = api ]; then printf '%s\\n' \"$VALIDATED_BASE_SHA\"; exit 0; fi\n"
                "if [ \"$1\" = pr ] && [ \"$2\" = create ]; then\n"
                "  shift 2\n"
                "  while [ \"$#\" -gt 0 ]; do\n"
                "    if [ \"$1\" = --body-file ]; then cp \"$2\" \"$PR_BODY_CAPTURE\"; exit 0; fi\n"
                "    shift\n"
                "  done\n"
                "fi\nexit 1\n",
                encoding="utf-8",
            )
            gh.chmod(0o700)
            env = os.environ.copy()
            env.update(
                {
                    "PATH": f"{mock_bin}{os.pathsep}{env['PATH']}",
                    "PR_BODY_CAPTURE": str(body_path),
                    "VALIDATED_BASE_SHA": "base-sha",
                    "VALIDATED_TREE_SHA": "tree-sha",
                    "VALIDATED_BRANCH": "candidate-branch",
                    "GITHUB_SERVER_URL": "https://github.com",
                    "GITHUB_REPOSITORY": "genai-rs/langfuse-client-base",
                    "GITHUB_RUN_ID": "123",
                    "GIT_TERMINAL_PROMPT": "0",
                }
            )
            result = subprocess.run(
                ["bash", "-e", "-c", create_pr["run"]],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            body = body_path.read_text(encoding="utf-8")
            self.assertIn("`generation-manifest.json` artifact", body)
            self.assertNotIn("command not found", result.stderr)

    def test_app_token_and_writes_follow_read_only_preflight(self):
        publish = self.workflow["jobs"]["publish"]
        self.assertEqual(publish["permissions"], {"contents": "read", "pull-requests": "read"})
        steps = publish["steps"]
        preflight_index = next(i for i, step in enumerate(steps) if step["name"] == "Check main and existing generated PR")
        token_index = next(i for i, step in enumerate(steps) if step["name"] == "Create GitHub App token")
        self.assertGreater(token_index, preflight_index)
        token = steps[token_index]
        self.assertEqual(token["with"]["permission-contents"], "write")
        self.assertEqual(token["with"]["permission-pull-requests"], "write")
        self.assertFalse(any(step["name"] == "Create GitHub App token" for step in self.workflow["jobs"]["validate"]["steps"]))

    def test_manifest_is_required_and_copied_to_visible_artifact_path(self):
        validate = self.workflow["jobs"]["validate"]
        save = step_named(validate["steps"], "Save validated changes")["run"]
        self.assertIn(".openapi-generator/generation-manifest.json", save)
        self.assertIn("test -f", save)
        self.assertIn("cp .openapi-generator/generation-manifest.json", save)
        self.assertIn("validation-output/generation-manifest.json", save)

        upload = step_named(validate["steps"], "Upload validated changes and generation provenance")
        self.assertEqual(upload["uses"], "actions/upload-artifact@v4")
        self.assertEqual(upload["with"]["retention-days"], "30")
        self.assertEqual(upload["with"]["if-no-files-found"], "error")
        self.assertIn("validation-output/generation-manifest.json", upload["with"]["path"])
        self.assertNotIn("include-hidden-files", upload["with"])

    def test_pinned_downstream_check_runs_after_candidate_tree_is_saved(self):
        steps = self.workflow["jobs"]["validate"]["steps"]
        names = [step["name"] for step in steps]
        save_index = names.index("Save validated changes")
        downstream_index = names.index("Check pinned downstream wrapper compatibility")
        upload_index = names.index("Upload validated changes and generation provenance")
        self.assertLess(save_index, downstream_index)
        self.assertLess(downstream_index, upload_index)
        downstream = steps[downstream_index]
        self.assertEqual(downstream["run"], "./scripts/check-downstream.sh")
        self.assertIn("github.event.pull_request.base.sha", downstream["env"]["BASELINE_SHA"])
        self.assertIn("steps.changes.outputs.tree_sha", downstream["env"]["CANDIDATE_TREE_SHA"])
        self.assertIn("validation-output/downstream-compatibility.json", steps[upload_index]["with"]["path"])
        report_upload = step_named(steps, "Upload downstream compatibility report")
        self.assertIn("always()", report_upload["if"])
        self.assertEqual(report_upload["with"]["name"], "downstream-compatibility")

    def test_downstream_gate_pins_accepted_wrapper_and_keeps_cases_offline(self):
        script = (ROOT / "scripts/check-downstream.sh").read_text()
        self.assertIn("dd57b2c10d387fdcbd180953a79f04e21ed2017d", script)
        self.assertIn("cargo test --all-targets --all-features --offline --locked", script)
        self.assertIn("CARGO_BUILD_JOBS=2", script)
        self.assertIn("baseline failed", script)

    def test_validation_runs_all_checks_before_saving_an_artifact(self):
        steps = self.workflow["jobs"]["validate"]["steps"]
        names = [step["name"] for step in steps]
        artifact_index = names.index("Upload validated changes and generation provenance")
        required = [
            "Test generation compatibility rules",
            "Generate client",
            "Build all features",
            "Run tests and doctests",
            "Check formatting",
            "Run Clippy",
        ]
        for name in required:
            self.assertLess(names.index(name), artifact_index)

    def test_keepalive_write_permission_is_limited_to_scheduled_main(self):
        keepalive = self.workflow["jobs"]["keepalive"]
        self.assertIn("github.event_name == 'schedule'", keepalive["if"])
        self.assertIn("github.ref == 'refs/heads/main'", keepalive["if"])
        self.assertEqual(keepalive["permissions"], {"actions": "write", "contents": "read"})


if __name__ == "__main__":
    unittest.main()
