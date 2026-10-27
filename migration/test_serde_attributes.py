import tempfile
import unittest
from pathlib import Path

from migration.serde_attributes import serde_field_attributes


class SerdeFieldAttributesTest(unittest.TestCase):
    def test_single_line_attribute_attaches_to_the_next_field_only(self):
        source = '''
#[serde(rename = "name", skip_serializing_if = "Option::is_none")]
pub name: Option<String>,
pub index: i32,
'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "model.rs"
            path.write_text(source)
            result = serde_field_attributes(path)

        self.assertIn('rename = "name"', result["name"])
        self.assertIn('skip_serializing_if = "Option::is_none"', result["name"])
        self.assertEqual(result["index"], "")

    def test_multiline_attribute_and_following_field_are_kept_separate(self):
        source = '''
#[serde(
    rename = "stream",
    default,
    with = "::serde_with::rust::double_option",
    skip_serializing_if = "Option::is_none"
)]
pub stream: Option<Option<bool>>,
pub next_field: Option<bool>,
'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "model.rs"
            path.write_text(source)
            result = serde_field_attributes(path)

        for expected in (
            'rename = "stream"',
            "default",
            'with = "::serde_with::rust::double_option"',
            'skip_serializing_if = "Option::is_none"',
        ):
            self.assertIn(expected, result["stream"])
        self.assertEqual(result["next_field"], "")


if __name__ == "__main__":
    unittest.main()
