import importlib.util
import pathlib
import unittest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "scripts" / "normalize_openapi_schema.py"
SPEC = importlib.util.spec_from_file_location("normalize_openapi_schema", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
normalize_text = MODULE.normalize_text
strip_const_keyword = MODULE.strip_const_keyword


class NormalizeOpenApiSchemaTests(unittest.TestCase):
    def test_integer_float_is_normalized_to_number(self) -> None:
        source = """components:\n  schemas:\n    MapValue:\n      oneOf:\n        - type: integer\n          format: float\n          nullable: true\n"""

        normalized, changes = normalize_text(source)

        self.assertEqual(changes, 1)
        self.assertIn("- type: number", normalized)
        self.assertIn("format: float", normalized)
        self.assertNotIn("- type: integer\n          format: float", normalized)

    def test_plain_integer_stays_unchanged(self) -> None:
        source = """components:\n  schemas:\n    SomeValue:\n      oneOf:\n        - type: integer\n          nullable: true\n"""

        normalized, changes = normalize_text(source)

        self.assertEqual(changes, 0)
        self.assertEqual(normalized, source)

    def test_double_format_is_normalized(self) -> None:
        source = """components:\n  schemas:\n    SomeValue:\n      oneOf:\n        - type: integer\n          format: double\n"""

        normalized, changes = normalize_text(source)

        self.assertEqual(changes, 1)
        self.assertIn("- type: number", normalized)
        self.assertIn("format: double", normalized)


class StripConstKeywordTests(unittest.TestCase):
    def test_inline_schema_const_is_stripped(self) -> None:
        source = "        type:\n          type: string\n          const: code\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 1)
        self.assertNotIn("const: code", stripped)
        self.assertIn("type: string", stripped)

    def test_quoted_schema_const_is_stripped(self) -> None:
        source = '        type:\n          type: string\n          "const": code\n'

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 1)
        self.assertNotIn("const", stripped)

    def test_property_named_const_is_preserved(self) -> None:
        source = "      properties:\n        const:  # literal property name\n          type: string\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 0)
        self.assertEqual(stripped, source)

    def test_const_text_inside_block_scalar_is_preserved(self) -> None:
        source = "        description: |\n          Example usage:\n            const: code\n          keep this line\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 0)
        self.assertEqual(stripped, source)

    def test_block_scalar_with_indent_and_chomping_indicators(self) -> None:
        source = "        description: |2-\n          const: keep\n        next: value\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 0)
        self.assertIn("const: keep", stripped)

    def test_sibling_const_after_sequence_block_scalar_is_stripped(self) -> None:
        source = "      - description: |\n          body text\n        const: code\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 1)
        self.assertIn("body text", stripped)
        self.assertNotIn("const: code", stripped)

    def test_property_named_const_with_inline_schema_is_preserved(self) -> None:
        source = "      properties:\n        const: { type: string, description: literal property }\n        keep:\n          type: string\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 0)
        self.assertEqual(stripped, source)

    def test_bare_sequence_block_scalar_body_is_preserved(self) -> None:
        source = "      examples:\n        - |\n          const: literal\n        - type: string\n"

        stripped, changes = strip_const_keyword(source)

        self.assertEqual(changes, 0)
        self.assertIn("const: literal", stripped)


if __name__ == "__main__":
    unittest.main()
