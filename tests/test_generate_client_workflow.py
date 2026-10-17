"""Guard the generation workflow's validation and publication boundary."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/generate-client.yml"


class GenerateClientWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)

    def test_manual_runs_default_to_validation_only(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]["inputs"]["publish"]
        self.assertEqual(dispatch["type"], "boolean")
        self.assertEqual(dispatch["default"], "false")
        self.assertEqual(dispatch["required"], "false")

    def test_only_schedule_and_manual_dispatch_can_start_workflow(self):
        self.assertEqual(set(self.workflow["on"]), {"schedule", "pull_request", "workflow_dispatch"})
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        self.assertEqual(self.workflow["on"]["pull_request"]["branches"], ["main"])

    def test_publish_requires_successful_validation_changes_and_trusted_main_event(self):
        publish = self.workflow["jobs"]["publish"]
        self.assertEqual(publish["needs"], "validate")
        condition = publish["if"]
        for requirement in (
            "needs.validate.result == 'success'",
            "needs.validate.outputs.has_changes == 'true'",
            "github.ref == 'refs/heads/main'",
            "github.event_name == 'schedule'",
            "github.event_name == 'workflow_dispatch'",
            "inputs.publish == true",
        ):
            self.assertIn(requirement, condition)

        # A failing validation, no-change result, branch ref, or an opt-out
        # manual run must prevent the privileged job from being eligible.
        scenarios = [
            ("failure", "true", "refs/heads/main", "schedule", True, False),
            ("success", "false", "refs/heads/main", "schedule", True, False),
            ("success", "true", "refs/heads/feature", "workflow_dispatch", True, False),
            ("success", "true", "refs/heads/feature", "workflow_dispatch", False, False),
            ("success", "true", "refs/pull/42/merge", "pull_request", False, False),
            ("success", "true", "refs/heads/main", "workflow_dispatch", False, False),
            ("success", "true", "refs/heads/main", "workflow_dispatch", True, True),
            ("success", "true", "refs/heads/main", "schedule", False, True),
        ]
        for result, changes, ref, event, requested, expected in scenarios:
            with self.subTest(result=result, changes=changes, ref=ref, event=event, requested=requested):
                allowed = (
                    result == "success"
                    and changes == "true"
                    and ref == "refs/heads/main"
                    and (event == "schedule" or (event == "workflow_dispatch" and requested))
                )
                self.assertEqual(allowed, expected)

    def test_write_permissions_and_app_token_are_confined_to_publish_job(self):
        publish = self.workflow["jobs"]["publish"]
        self.assertEqual(
            publish["permissions"],
            {"contents": "write", "pull-requests": "write"},
        )
        self.assertNotIn("permissions", self.workflow["jobs"]["validate"])
        steps = publish["steps"]
        token_index = next(i for i, step in enumerate(steps) if step["name"] == "Create GitHub App token")
        apply_index = next(i for i, step in enumerate(steps) if step["name"] == "Apply validated changes")
        self.assertGreater(token_index, apply_index)
        self.assertFalse(any(step["name"] == "Create GitHub App token" for step in self.workflow["jobs"]["validate"]["steps"]))

    def test_validation_runs_all_checks_before_saving_an_artifact(self):
        steps = self.workflow["jobs"]["validate"]["steps"]
        names = [step["name"] for step in steps]
        artifact_index = names.index("Upload validated changes")
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
        self.assertEqual(keepalive["permissions"]["actions"], "write")


if __name__ == "__main__":
    unittest.main()
