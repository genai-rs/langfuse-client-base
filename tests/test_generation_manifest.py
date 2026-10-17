import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location(
    "generation_manifest", ROOT / "scripts/generation_manifest.py"
)
MODULE = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(MODULE)


class GenerationManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.raw = self.root / "openapi.yml"
        self.raw.write_bytes(b"openapi: 3.0.1\ninfo: {title: raw}\n")
        self.composed = self.root / "compatible.json"
        self.composed.write_bytes(b'{"openapi":"3.0.1","info":{"title":"composed"}}\n')
        self.compatibility = self.root / "compatibility.json"
        self.compatibility.write_text(
            json.dumps(
                {
                    "source": "https://github.com/genai-rs/langfuse-client-base/blob/"
                    "28f072145f3e340274a18e0d477a186a3977edfc/scripts/legacy.json",
                    "paths": {},
                }
            ),
            encoding="utf-8",
        )
        self.patch = self.root / "patch_generated.rs.sh"
        self.patch.write_text("#!/bin/sh\necho patch\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def build(self):
        return MODULE.build_manifest(
            upstream_url="https://cloud.langfuse.com/generated/api/openapi.yml",
            upstream_revision=None,
            raw_spec=self.raw,
            composed_spec=self.composed,
            compatibility_file=self.compatibility,
            patch_script=self.patch,
            generator_image="openapitools/openapi-generator-cli:v7.25.0",
        )

    def test_manifest_has_stable_fields_and_separate_input_hashes(self):
        manifest = self.build()

        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(
            manifest["upstream"]["url"],
            "https://cloud.langfuse.com/generated/api/openapi.yml",
        )
        self.assertIsNone(manifest["upstream"]["revision"])
        self.assertEqual(
            manifest["upstream"]["raw_sha256"], MODULE.sha256_file(self.raw)
        )
        self.assertEqual(
            manifest["composed_input"]["sha256"],
            MODULE.sha256_file(self.composed),
        )
        self.assertNotEqual(
            manifest["upstream"]["raw_sha256"],
            manifest["composed_input"]["sha256"],
        )
        self.assertEqual(
            manifest["compatibility"]["source_version"],
            "28f072145f3e340274a18e0d477a186a3977edfc",
        )
        self.assertEqual(
            manifest["compatibility"]["source_sha256"],
            MODULE.sha256_file(self.compatibility),
        )
        self.assertEqual(manifest["generator"]["version"], "7.25.0")
        self.assertEqual(
            manifest["patch_script"]["revision"], MODULE.sha256_file(self.patch)
        )

    def test_serialization_is_stable_and_sorted(self):
        output = self.root / ".openapi-generator/generation-manifest.json"
        manifest = self.build()

        with patch.dict(os.environ, {"SECRET_TOKEN": "must-not-be-recorded"}):
            MODULE.write_manifest(manifest, output)
        first = output.read_bytes()
        MODULE.write_manifest(self.build(), output)

        self.assertEqual(output.read_bytes(), first)
        self.assertLess(first.index(b'"compatibility"'), first.index(b'"composed_input"'))
        self.assertLess(first.index(b'"composed_input"'), first.index(b'"generator"'))
        self.assertNotIn(b"must-not-be-recorded", first)

    def test_changed_compatibility_input_changes_only_its_hash(self):
        before = self.build()
        self.compatibility.write_text(
            self.compatibility.read_text(encoding="utf-8") + "\n", encoding="utf-8"
        )
        after = self.build()

        self.assertNotEqual(
            before["compatibility"]["source_sha256"],
            after["compatibility"]["source_sha256"],
        )
        self.assertEqual(before["upstream"], after["upstream"])
        self.assertEqual(before["composed_input"], after["composed_input"])

    def test_upstream_revision_must_be_a_commit_id(self):
        with self.assertRaisesRegex(ValueError, "hexadecimal commit id"):
            MODULE.build_manifest(
                upstream_url="https://cloud.langfuse.com/generated/api/openapi.yml",
                upstream_revision="token=must-not-be-recorded",
                raw_spec=self.raw,
                composed_spec=self.composed,
                compatibility_file=self.compatibility,
                patch_script=self.patch,
                generator_image="openapitools/openapi-generator-cli:v7.25.0",
            )

    def test_available_upstream_revision_is_recorded(self):
        manifest = MODULE.build_manifest(
            upstream_url="https://cloud.langfuse.com/generated/api/openapi.yml",
            upstream_revision="A" * 40,
            raw_spec=self.raw,
            composed_spec=self.composed,
            compatibility_file=self.compatibility,
            patch_script=self.patch,
            generator_image="openapitools/openapi-generator-cli:v7.25.0",
        )

        self.assertEqual(manifest["upstream"]["revision"], "a" * 40)


if __name__ == "__main__":
    unittest.main()
