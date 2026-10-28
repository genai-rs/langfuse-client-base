import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "prepare_compatible_spec", ROOT / "scripts/prepare_compatible_spec.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompatibleSpecTests(unittest.TestCase):
    def setUp(self):
        self.upstream = yaml.safe_load((ROOT / "openapi.yml").read_text())
        self.compatibility = json.loads(MODULE.COMPATIBILITY_FILE.read_text())
        self.result = MODULE.prepare_spec(self.upstream, self.compatibility)

    def test_legacy_operations_keep_their_published_module_and_function(self):
        for path, methods in self.compatibility["paths"].items():
            for method, legacy in methods.items():
                with self.subTest(path=path, method=method):
                    actual = self.result["paths"][path][method]
                    self.assertEqual(actual["operationId"], legacy["operationId"])
                    self.assertEqual(actual["tags"], legacy["tags"])

    def test_every_local_reference_resolves(self):
        def visit(value):
            if isinstance(value, dict):
                if "$ref" in value and value["$ref"].startswith("#/"):
                    target = self.result
                    for part in value["$ref"][2:].split("/"):
                        target = target[part.replace("~1", "/").replace("~0", "~")]
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(self.result)

    def test_upstream_endpoints_and_model_additions_are_preserved(self):
        path = "/api/public/llm-connections"
        self.assertEqual(self.result["paths"][path], self.upstream["paths"][path])
        self.assertEqual(
            self.result["components"]["schemas"]["CreateScoreRequest"],
            self.upstream["components"]["schemas"]["CreateScoreRequest"],
        )

    def test_current_wire_changes_on_renamed_operations_are_preserved(self):
        path = "/api/public/v3/scores"
        self.upstream["paths"][path]["get"]["description"] = "New upstream docs"
        result = MODULE.prepare_spec(self.upstream, self.compatibility)
        self.assertEqual(result["paths"][path]["get"]["description"], "New upstream docs")

    def test_single_score_request_and_response_variants_survive(self):
        schemas = self.result["components"]["schemas"]
        self.assertIn({"$ref": "#/components/schemas/CreateScoreRequest"},
                      schemas["CreateScoresRequest"]["oneOf"])
        self.assertIn({"$ref": "#/components/schemas/CreateScoreResponse"},
                      schemas["CreateScoresResponse"]["oneOf"])

    def test_const_keyword_is_dropped_but_properties_named_const_are_kept(self):
        self.upstream["components"]["schemas"]["Thing"] = {
            "type": "object",
            "properties": {
                "type": {"type": "string", "const": "thing"},
                "const": {"type": "integer", "const": 1},
            },
            "oneOf": [{"const": "a"}, {"type": "string"}],
        }
        result = MODULE.prepare_spec(self.upstream, self.compatibility)
        thing = result["components"]["schemas"]["Thing"]
        self.assertEqual(thing["properties"]["type"], {"type": "string"})
        self.assertEqual(thing["properties"]["const"], {"type": "integer"})
        self.assertEqual(thing["oneOf"], [{}, {"type": "string"}])
        self.assertEqual(MODULE.strip_const(result), 0)

    def test_preparation_is_idempotent_and_does_not_mutate_input(self):
        original = json.dumps(self.upstream)
        self.assertEqual(MODULE.prepare_spec(self.result, self.compatibility), self.result)
        self.assertEqual(json.dumps(self.upstream), original)

    def test_unchanged_download_still_reaches_generator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "scripts", root / "scripts")
            shutil.copyfile(ROOT / "openapi.yml", root / "openapi.yml")
            mock_bin = root / "bin"
            mock_bin.mkdir()
            # Stop at the generator invocation: no generated files or Cargo
            # are needed to demonstrate that unchanged input is composed.
            for name, source in {
                "curl": '#!/bin/sh\ncp "$UNCHANGED_SPEC" "$2"\n',
                "docker": '#!/bin/sh\nexit 42\n',
                "python3": f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n',
            }.items():
                executable = mock_bin / name
                executable.write_text(source)
                executable.chmod(0o755)
            result = subprocess.run(
                ["bash", str(root / "scripts/generate-openapi-client.sh")],
                env={**os.environ, "UPDATE_SPEC": "true",
                     "UNCHANGED_SPEC": str(root / "openapi.yml"),
                     "PATH": str(mock_bin) + os.pathsep + os.environ["PATH"]},
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 42, result.stdout + result.stderr)
            composed = json.loads(
                (root / ".openapi-generator/compatible.json").read_text()
            )
            self.assertIn("/api/public/ingestion", composed["paths"])


if __name__ == "__main__":
    unittest.main()
