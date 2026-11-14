"""End-to-end tests of migration/compare_public_api.py on small Rust source trees."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "migration/compare_public_api.py").exists())
SCRIPT = ROOT / "migration/compare_public_api.py"

MODELS_MOD = """
pub mod upload_body;
pub use self::upload_body::UploadBody;
"""

APIS_MOD = """
use std::fmt;

#[derive(Debug)]
pub enum Error<T> {
    /// Sending the request failed.
    Http(timvw_rust_runtime::Error),
    Serde(serde_json::Error),
    Io(std::io::Error),
    ResponseError(Box<ResponseContent<T>>),
}

impl<T> fmt::Display for Error<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "error in {}: {}", "x", "y")
    }
}

impl<T> From<serde_json::Error> for Error<T> {
    fn from(e: serde_json::Error) -> Self {
        Error::Serde(e)
    }
}

impl<T> From<std::io::Error> for Error<T> {
    fn from(e: std::io::Error) -> Self {
        Error::Io(e)
    }
}

/// Status-specific errors of one operation.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum CreateUploadError {
    Status400(models::ErrorResponse),
    UnknownValue(serde_json::Value),
}

struct Private;

impl From<u8> for Private {
    fn from(_: u8) -> Self {
        Private
    }
}
"""

UPLOAD_BODY = """
use crate::models;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum UploadBody {
    /// A file to upload.
    #[serde(skip)]
    File(Vec<u8>),
    Reference(Box<models::FileReference>),
    Named { name: String, id: Option<i32> },
}

impl From<Vec<u8>> for UploadBody {
    fn from(bytes: Vec<u8>) -> Self {
        Self::File(bytes)
    }
}
"""


def tree(root, files):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text))
    return root


class ComparePublicApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = {"models/mod.rs": MODELS_MOD, "models/upload_body.rs": UPLOAD_BODY, "apis/mod.rs": APIS_MOD}
        self.reference = tree(Path(self.temp.name) / "reference", self.base)

    def compare(self, **changes):
        files = dict(self.base)
        for rel, (old, new) in changes.items():
            self.assertIn(old, files[rel], "fixture edit does not apply")
            files[rel] = files[rel].replace(old, new)
        candidate = tree(Path(self.temp.name) / "candidate", files)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), str(self.reference), str(candidate), "--fail-on-change"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.stderr, "")
        return proc.returncode, json.loads(proc.stdout)

    def assert_only(self, report, **expected):
        nonzero = {k: v for k, v in report["counts"].items() if v}
        self.assertEqual(nonzero, expected)

    def test_unchanged_tree_reports_nothing(self):
        code, report = self.compare()
        self.assertEqual(code, 0)
        self.assert_only(report)

    def test_formatting_and_comment_changes_are_not_reported(self):
        code, report = self.compare(
            **{
                "models/upload_body.rs": (
                    "    Reference(Box<models::FileReference>),\n    Named { name: String, id: Option<i32> },",
                    "    // reworded comment\n    Reference(\n        Box< models::FileReference >,\n    ),\n"
                    "    Named {\n        name: String,\n        id: Option<i32>,\n    },",
                ),
                "apis/mod.rs": (
                    "impl<T> From<std::io::Error> for Error<T> {",
                    "/// Converts I/O errors.\nimpl<T>\n    From<std::io::Error>\n    for Error<T>\n{",
                ),
            }
        )
        self.assertEqual(code, 0)
        self.assert_only(report)

    def test_tuple_variant_payload_change_is_reported(self):
        code, report = self.compare(
            **{
                "models/upload_body.rs": (
                    "    File(Vec<u8>),\n    Reference(Box<models::FileReference>),",
                    "    File(timvw_rust_runtime::Upload),\n    Reference(timvw_rust_runtime::Upload),",
                )
            }
        )
        self.assertEqual(code, 1)
        self.assert_only(report, public_enum_variant_payload_changes=2)
        self.assertEqual(
            report["public_enum_variant_payload_changes"][0],
            {
                "file": "models/upload_body.rs",
                "enum": "UploadBody",
                "variant": "File",
                "registry": "File(Vec<u8>)",
                "current": "File(timvw_rust_runtime::Upload)",
            },
        )
        self.assertEqual(report["public_enum_variant_payload_changes"][1]["registry"], "Reference(Box<models::FileReference>)")

    def test_struct_variant_field_change_is_reported(self):
        code, report = self.compare(**{"models/upload_body.rs": ("id: Option<i32>", "id: Option<i64>")})
        self.assertEqual(code, 1)
        self.assert_only(report, public_enum_variant_payload_changes=1)
        self.assertEqual(report["public_enum_variant_payload_changes"][0]["current"], "Named{name: String, id: Option<i64>}")

    def test_variant_removal_from_generic_apis_error_is_reported(self):
        code, report = self.compare(**{"apis/mod.rs": ("    Io(std::io::Error),\n", "")})
        self.assertEqual(code, 1)
        self.assert_only(report, public_enum_types_with_variant_changes=1, public_enum_variants_removed=1)
        self.assertEqual(
            report["public_enum_variant_changes"],
            [{"file": "apis/mod.rs", "enum": "Error", "added": [], "removed": ["Io"]}],
        )

    def test_operation_error_enum_variant_change_is_reported(self):
        code, report = self.compare(**{"apis/mod.rs": ("Status400(models::ErrorResponse)", "Status400(models::OtherError)")})
        self.assertEqual(code, 1)
        self.assert_only(report, public_enum_variant_payload_changes=1)
        self.assertEqual(report["public_enum_variant_payload_changes"][0]["enum"], "CreateUploadError")

    def test_from_impl_removal_is_reported(self):
        removed = "impl<T> From<std::io::Error> for Error<T> {\n    fn from(e: std::io::Error) -> Self {\n        Error::Io(e)\n    }\n}\n"
        code, report = self.compare(**{"apis/mod.rs": (removed, "")})
        self.assertEqual(code, 1)
        self.assert_only(report, public_types_with_trait_impl_changes=1, public_trait_impls_removed=1)
        self.assertEqual(
            report["public_trait_impl_changes"],
            [{"file": "apis/mod.rs", "type": "Error", "added": [], "removed": ["impl<T> From<std::io::Error> for Error<T>"]}],
        )

    def test_from_impl_addition_on_model_is_reported(self):
        added = "impl From<String> for UploadBody {\n    fn from(name: String) -> Self {\n        Self::Named { name, id: None }\n    }\n}\n"
        code, report = self.compare(**{"models/upload_body.rs": ("impl From<Vec<u8>>", added + "\nimpl From<Vec<u8>>")})
        self.assertEqual(code, 1)
        self.assert_only(report, public_types_with_trait_impl_changes=1, public_trait_impls_added=1)
        self.assertEqual(report["public_trait_impl_changes"][0]["added"], ["impl From<String> for UploadBody"])

    def test_impls_on_private_types_and_inherent_impls_are_ignored(self):
        code, report = self.compare(
            **{
                "apis/mod.rs": ("impl From<u8> for Private {", "impl From<u16> for Private {"),
                "models/upload_body.rs": ("impl From<Vec<u8>>", "impl UploadBody {}\n\nimpl From<Vec<u8>>"),
            }
        )
        self.assertEqual(code, 0)
        self.assert_only(report)


if __name__ == "__main__":
    unittest.main()
