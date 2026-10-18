"""Exercise the downstream gate against isolated Cargo and Git fixtures."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-downstream.sh"


class DownstreamCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.clean_home = self.root / "clean-home"
        self.clean_home.mkdir()
        self.empty_cargo_home = self.root / "empty-cargo-home"
        self.empty_cargo_home.mkdir()
        self.git_env = os.environ.copy()
        self.git_env.update(
            HOME=str(self.clean_home),
            GIT_CONFIG_GLOBAL="/dev/null",
            GIT_CONFIG_NOSYSTEM="1",
        )
        for key in (
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL",
        ):
            self.git_env.pop(key, None)
        self.base = self.root / "base"
        self.wrapper = self.root / "wrapper"
        self.base.mkdir()
        self.wrapper.mkdir()
        self.git(self.base, "init", "--quiet")
        self.git(self.base, "config", "user.name", "Fixture")
        self.git(self.base, "config", "user.email", "fixture@example.invalid")
        self.write_base()
        self.git(self.base, "add", ".")
        self.git(self.base, "commit", "--quiet", "-m", "baseline")
        self.baseline = self.git(self.base, "rev-parse", "HEAD")
        self.git(self.wrapper, "init", "--quiet")
        self.git(self.wrapper, "config", "user.name", "Fixture")
        self.git(self.wrapper, "config", "user.email", "fixture@example.invalid")
        self.write_wrapper()
        self.git(self.wrapper, "add", ".")
        self.git(self.wrapper, "commit", "--quiet", "-m", "pinned wrapper")
        self.wrapper_sha = self.git(self.wrapper, "rev-parse", "HEAD")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, cwd, *args):
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            env=self.git_env,
        ).stdout.strip()

    def write_base(self, ingestion=True, addition=False):
        (self.base / "Cargo.toml").write_text(
            '[package]\nname = "langfuse-client-base"\nversion = "0.15.0"\nedition = "2021"\n'
        )
        src = self.base / "src"
        src.mkdir(exist_ok=True)
        lines = []
        if ingestion:
            lines.append("pub mod apis { pub mod ingestion_api { pub fn ingestion_batch() {} } }")
        if addition:
            lines.append("pub mod added_api { pub fn new_operation() {} }")
        (src / "lib.rs").write_text("\n".join(lines) + "\n")

    def write_wrapper(self, unrelated_failure=False):
        (self.wrapper / "Cargo.toml").write_text(
            '[package]\nname = "pinned-wrapper"\nversion = "0.1.0"\nedition = "2021"\n'
            '[dependencies]\nlangfuse-client-base = "^0.15.0"\n'
        )
        tests = self.wrapper / "tests"
        tests.mkdir(exist_ok=True)
        source = "#[test] fn ingestion_contract() { let _ = langfuse_client_base::apis::ingestion_api::ingestion_batch; }\n"
        if unrelated_failure:
            source += '#[test] fn unrelated_wrapper_failure() { panic!("fixture failure"); }\n'
        (tests / "api.rs").write_text(source)

    def run_gate(self, candidate_mutation=None, default_remote=False, extra_env=None):
        if candidate_mutation:
            candidate_mutation()
        self.git(self.base, "add", ".")
        tree = self.git(self.base, "write-tree")
        report = self.root / "report.json"
        env = self.git_env.copy()
        env.update(
            WRAPPER_REPOSITORY=str(self.wrapper),
            WRAPPER_REVISION=self.wrapper_sha,
            BASELINE_SHA=self.baseline,
            CANDIDATE_TREE_SHA=tree,
            REPORT_PATH=str(report),
            CARGO_TARGET_DIR=str(self.root / "unused-target"),
            CARGO_HOME=str(self.empty_cargo_home),
            RUSTUP_HOME=os.environ.get("RUSTUP_HOME", str(Path.home() / ".rustup")),
        )
        if default_remote:
            real_git = shutil.which("git")
            self.assertIsNotNone(real_git)
            proxy_bin = self.root / "proxy-bin"
            proxy_bin.mkdir()
            proxy_log = self.root / "git-fetch.log"
            proxy = proxy_bin / "git"
            proxy.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = -C ] && [ \"$3\" = fetch ] && [ \"$6\" = https://github.com/genai-rs/langfuse-ergonomic.git ]; then\n"
                "  printf '%s %s\\n' \"$6\" \"$7\" >> \"$GIT_PROXY_LOG\"\n"
                "  set -- \"$1\" \"$2\" \"$3\" \"$4\" \"$5\" \"$LOCAL_WRAPPER\" \"$7\"\n"
                "fi\n"
                f"exec {real_git} \"$@\"\n",
                encoding="utf-8",
            )
            proxy.chmod(0o755)
            env.pop("WRAPPER_REPOSITORY")
            env["GIT_PROXY_LOG"] = str(proxy_log)
            env["LOCAL_WRAPPER"] = str(self.wrapper)
            env["PATH"] = f"{proxy_bin}{os.pathsep}{env['PATH']}"
        if extra_env:
            env.update(extra_env)
        proc = subprocess.run(
            [str(SCRIPT)], cwd=self.base, env=env, capture_output=True, text=True
        )
        if not report.exists():
            raise AssertionError(f"gate did not produce report\nstdout: {proc.stdout}\nstderr: {proc.stderr}")
        return proc, json.loads(report.read_text()), proxy_log if default_remote else None

    def test_both_fixture_repositories_have_local_identity_under_clean_home(self):
        self.assertEqual(
            self.git(self.base, "config", "--local", "user.email"),
            "fixture@example.invalid",
        )
        self.assertEqual(
            self.git(self.wrapper, "config", "--local", "user.email"),
            "fixture@example.invalid",
        )
        self.assertFalse((self.clean_home / ".gitconfig").exists())

    def test_compatible_candidate_passes_against_exact_patched_source(self):
        proc, report, _ = self.run_gate()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(report["wrapper_commit"], self.wrapper_sha)
        self.assertEqual(report["baseline"]["status"], "passed")
        self.assertEqual(report["candidate"]["status"], "passed")
        self.assertEqual(Path(report["candidate"]["resolved_manifest"]).parent.name, "candidate")

    def test_removing_ingestion_api_fails_as_candidate_regression(self):
        proc, report, _ = self.run_gate(lambda: self.write_base(ingestion=False))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("candidate fails pinned wrapper compatibility", proc.stderr)
        self.assertEqual(report["baseline"]["status"], "passed")
        self.assertEqual(report["candidate"]["status"], "failed")

    def test_compatible_addition_passes(self):
        proc, report, _ = self.run_gate(lambda: self.write_base(addition=True))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(report["candidate"]["status"], "passed")

    def test_unrelated_baseline_failure_is_reported_and_never_accepted(self):
        self.write_wrapper(unrelated_failure=True)
        self.git(self.wrapper, "add", ".")
        self.git(self.wrapper, "commit", "--quiet", "-m", "fixture failure")
        self.wrapper_sha = self.git(self.wrapper, "rev-parse", "HEAD")
        proc, report, _ = self.run_gate()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("baseline failed", proc.stderr)
        self.assertNotIn("candidate fails pinned wrapper compatibility", proc.stderr)
        self.assertEqual(report["baseline"]["status"], "failed")
        self.assertEqual(report["candidate"]["status"], "failed")

    def test_default_remote_path_fetches_the_real_wrapper_repository(self):
        proc, report, proxy_log = self.run_gate(default_remote=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            proxy_log.read_text().strip(),
            f"https://github.com/genai-rs/langfuse-ergonomic.git {self.wrapper_sha}",
        )
        self.assertEqual(report["wrapper_commit"], self.wrapper_sha)

    def test_source_override_cannot_claim_the_pinned_wrapper_identity(self):
        untrusted_wrapper = self.root / "untrusted-wrapper"
        untrusted_wrapper.mkdir()
        (untrusted_wrapper / "Cargo.toml").write_text(
            '[package]\nname = "pinned-wrapper"\nversion = "0.1.0"\nedition = "2021"\n'
            '[dependencies]\nlangfuse-client-base = "^0.15.0"\n'
        )
        (untrusted_wrapper / "src").mkdir()
        (untrusted_wrapper / "src/lib.rs").write_text("")
        (untrusted_wrapper / "tests").mkdir()
        (untrusted_wrapper / "tests/api.rs").write_text("#[test] fn empty_test() {}\n")
        proc, report, _ = self.run_gate(
            candidate_mutation=lambda: self.write_base(ingestion=False),
            extra_env={
                "WRAPPER_SOURCE": str(untrusted_wrapper),
                "WRAPPER_ACTUAL_SHA": self.wrapper_sha,
            }
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("candidate fails pinned wrapper compatibility", proc.stderr)
        self.assertEqual(report["wrapper_commit"], self.wrapper_sha)
        self.assertEqual(report["candidate"]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
