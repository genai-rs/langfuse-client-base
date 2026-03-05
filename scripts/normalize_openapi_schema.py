#!/usr/bin/env python3

"""Normalize OpenAPI schema constructs that break Rust code generation.

Currently normalizes invalid numeric schema combinations where a node is
declared as `type: integer` with `format: float|double`.

OpenAPI treats floating-point values as `type: number` with
`format: float|double`. Keeping `type: integer` there can lead to duplicate
generated enum variants in Rust.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TYPE_RE = re.compile(r"^(\s*)(-\s*)?type:\s*([\"']?)([^\"'#\s]+)([\"']?)(\s*(#.*)?)$")
FORMAT_RE = re.compile(r"^\s*format:\s*([\"']?)([^\"'#\s]+)([\"']?)(\s*(#.*)?)$")


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")


def normalize_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    changes = 0

    for i, line in enumerate(lines):
        type_match = TYPE_RE.match(line.rstrip("\n"))
        if not type_match:
            continue

        type_value = _strip_quotes(type_match.group(4)).lower()
        if type_value != "integer":
            continue

        base_indent = len(type_match.group(1))
        is_list_item = type_match.group(2) is not None
        sibling_indent = base_indent + 2 if is_list_item else base_indent

        found_float_format = False

        for j in range(i + 1, len(lines)):
            candidate = lines[j]
            stripped = candidate.strip()

            if stripped == "":
                continue

            indent = _leading_spaces(candidate)

            if indent < sibling_indent:
                break

            if (
                is_list_item
                and indent == base_indent
                and candidate.lstrip(" ").startswith("- ")
            ):
                break

            if indent != sibling_indent:
                continue

            fmt_match = FORMAT_RE.match(candidate.rstrip("\n"))
            if not fmt_match:
                continue

            fmt_value = _strip_quotes(fmt_match.group(2)).lower()
            if fmt_value in {"float", "double"}:
                found_float_format = True
            break

        if not found_float_format:
            continue

        # Replace only the raw type token, preserving quotes/comments/spacing.
        start, end = type_match.span(4)
        lines[i] = line[:start] + "number" + line[end:]
        changes += 1

    return "".join(lines), changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize OpenAPI numeric type declarations."
    )
    parser.add_argument("spec", type=Path, help="Path to OpenAPI YAML file")
    args = parser.parse_args()

    content = args.spec.read_text(encoding="utf-8")
    normalized, changes = normalize_text(content)

    if changes > 0:
        args.spec.write_text(normalized, encoding="utf-8")
        print(
            f"Normalized {changes} schema entr{'y' if changes == 1 else 'ies'} in {args.spec}"
        )
    else:
        print(f"No numeric schema normalization needed in {args.spec}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
