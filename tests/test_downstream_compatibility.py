"""Run the downstream checker against isolated crates.io consumer fixtures."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check-downstream.sh"
FIXTURES = ROOT / "scripts/tests/validate-downstream.py"


class DownstreamCompatibilityTests(unittest.TestCase):
    def test_fixture_cases(self):
        with tempfile.TemporaryDirectory(prefix="downstream-results-") as results:
            proc = subprocess.run(
                [sys.executable, str(FIXTURES), str(SCRIPT), results],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("All crates.io consumer fixture cases passed", proc.stdout)


if __name__ == "__main__":
    unittest.main()
