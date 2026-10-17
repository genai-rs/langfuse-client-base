"""Execute and guard the generation workflow's publication boundaries."""

import ast
from itertools import product
from pathlib import Path
import re
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
