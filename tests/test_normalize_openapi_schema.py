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


if __name__ == "__main__":
    unittest.main()
