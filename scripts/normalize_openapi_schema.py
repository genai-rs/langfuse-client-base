#!/usr/bin/env python3

"""Normalize OpenAPI schema constructs that break Rust code generation.

Normalizations applied:

1. Invalid numeric schema combinations where a node is declared as
   `type: integer` with `format: float|double`. OpenAPI treats floating-point
   values as `type: number` with `format: float|double`. Keeping
   `type: integer` there can lead to duplicate generated enum variants in Rust.

2. The JSON-Schema / OpenAPI-3.1 `const` keyword. The upstream Langfuse spec
   declares `openapi: 3.0.1` yet uses `const` (e.g. on
   `unstableCodeEvaluationRuleEvaluatorReference.type`), which OpenAPI Generator
   rejects during 3.0 spec validation with:

       attribute components.schemas.<name>.const is unexpected

   `const: X` is semantically a single-value enum, so we drop the line, leaving
   the plain `type:`/`description:` that a 3.0 document expects.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TYPE_RE = re.compile(r"^(\s*)(-\s*)?type:\s*([\"']?)([^\"'#\s]+)([\"']?)(\s*(#.*)?)$")
FORMAT_RE = re.compile(r"^\s*format:\s*([\"']?)([^\"'#\s]+)([\"']?)(\s*(#.*)?)$")
# Match the `const` schema keyword only when it carries an inline *scalar*
# value (e.g. `const: code`). The first value character must not be `#` (a
# comment, i.e. a bare `const:` property key) nor `{`/`[` (an inline flow
# collection -- see limitation below).
#
# Known limitation: const values that are collections rather than scalars are
# left untouched, whether block-form (`const:` opening an indented mapping /
# sequence) or inline flow-form (`const: {...}` / `const: [...]`). A line-based
# pass cannot tell such a schema keyword apart from a property literally named
# "const" without full structural parsing. Upstream only uses inline scalar
# const; if that ever changes, spec validation fails loudly and this can be
# revisited.
CONST_RE = re.compile(r"^\s*(?:-\s+)*([\"']?)const\1:\s+(?![#{[])\S.*$")
# A node whose value introduces a YAML block scalar (`|`, `>`, with optional
# chomping/indent indicators in either order -- `|-`, `|2`, `|2-`, `>4+` -- and
# a trailing comment). Its indented body is free text, so any `const:` lines
# within it must be preserved. Matched against the content past any leading
# `- ` sequence markers, so it covers both `key: |` and bare `- |` forms.
BLOCK_SCALAR_RE = re.compile(r"^(?:[^:#]+:\s*)?[|>][+\-0-9]*\s*(#.*)?$")


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _content_indent(line: str) -> int:
    """Column where a node's content begins, past indentation and `- ` markers."""
    i = _leading_spaces(line)
    length = len(line)
    while i + 1 < length and line[i] == "-" and line[i + 1] == " ":
        i += 2
        while i < length and line[i] == " ":
            i += 1
    return i


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


def strip_const_keyword(text: str) -> tuple[str, int]:
    """Drop OpenAPI-3.1 `const` keyword lines that break 3.0 spec validation."""
    lines = text.splitlines(keepends=True)
    kept = []
    changes = 0

    # Indentation of the node introducing the block scalar we are currently
    # inside, or None when not inside one. Body lines are anything indented
    # deeper (blank lines belong to the body too).
    block_indent: int | None = None

    for line in lines:
        stripped = line.rstrip("\n")

        if block_indent is not None:
            if stripped.strip() == "" or _leading_spaces(stripped) > block_indent:
                # Still inside the block scalar body -- preserve verbatim.
                kept.append(line)
                continue
            block_indent = None

        content_col = _content_indent(stripped)
        content = stripped[content_col:]
        if BLOCK_SCALAR_RE.match(content):
            # A bare `- |` entry is indented relative to its dash; a `key: |`
            # value is indented relative to the key. Track whichever applies so
            # the body threshold is correct in both cases.
            block_indent = (
                _leading_spaces(stripped) if content[0] in "|>" else content_col
            )
            kept.append(line)
            continue

        if CONST_RE.match(stripped):
            changes += 1
            continue

        kept.append(line)

    return "".join(kept), changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize OpenAPI schema constructs for Rust generation."
    )
    parser.add_argument("spec", type=Path, help="Path to OpenAPI YAML file")
    args = parser.parse_args()

    content = args.spec.read_text(encoding="utf-8")
    normalized, numeric_changes = normalize_text(content)
    normalized, const_changes = strip_const_keyword(normalized)
    changes = numeric_changes + const_changes

    if changes > 0:
        args.spec.write_text(normalized, encoding="utf-8")
        details = []
        if numeric_changes:
            details.append(f"{numeric_changes} numeric type(s)")
        if const_changes:
            details.append(f"{const_changes} const keyword(s)")
        print(f"Normalized {', '.join(details)} in {args.spec}")
    else:
        print(f"No schema normalization needed in {args.spec}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
