#!/usr/bin/env python3
"""
Merge dependency tables from the OpenAPI generator without overwriting curated versions.

The generator rewrites `Cargo.toml` with exact dependency versions. We prefer to keep the
versions we curate in the repository so regeneration does not churn dependency updates.
This script merges the generated dependency tables into the existing `Cargo.toml` while
preserving the version requirement (including any leading range operators) for entries
that already exist in the project.

New dependencies from the generated file are appended as-is so the build continues to
work if upstream templates start requiring additional crates.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SECTION_NAMES = ("dependencies", "dev-dependencies", "build-dependencies")


@dataclass
class Entry:
    key: Optional[str]
    text: str


def extract_section(body: str, name: str) -> Tuple[List[Entry], Dict[str, Entry]]:
    """Return the parsed entries and mapping for the given dependency section."""
    pattern = re.compile(
        rf"(?ms)^\[{re.escape(name)}\]\n(.*?)(?=^\[|\Z)"
    )
    match = pattern.search(body)
    if not match:
        return [], {}

    section_body = match.group(1)
    entries: List[Entry] = []
    mapping: Dict[str, Entry] = {}

    current_key: Optional[str] = None
    current_lines: List[str] = []

    def flush() -> None:
        nonlocal current_key, current_lines
        if current_lines:
            entry_text = "\n".join(current_lines)
            entry = Entry(current_key, entry_text)
            entries.append(entry)
            if current_key is not None:
                mapping.setdefault(current_key, entry)
        current_key = None
        current_lines = []

    for raw_line in section_body.splitlines():
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if not stripped:
            flush()
            entries.append(Entry(None, line))
            continue

        if stripped.startswith("#"):
            flush()
            entries.append(Entry(None, line))
            continue

        key_match = re.match(r"\s*([A-Za-z0-9_\-]+)\s*=", line)
        if key_match:
            flush()
            current_key = key_match.group(1)
            current_lines = [line]
        else:
            if not current_lines:
                entries.append(Entry(None, line))
            else:
                current_lines.append(line)

    flush()
    return entries, mapping


def extract_version(entry_text: str) -> Optional[str]:
    """Return the version string from a dependency entry if present."""
    simple_match = re.match(
        r'\s*[A-Za-z0-9_\-]+\s*=\s*"([^"]+)"', entry_text, flags=re.DOTALL
    )
    if simple_match:
        return simple_match.group(1)

    version_match = re.search(r'(version\s*=\s*")([^"]+)(")', entry_text)
    if version_match:
        return version_match.group(2)
    return None


def replace_version(entry_text: str, new_version: str) -> str:
    """Replace the version string inside an entry with the provided value."""
    if "version" in entry_text:
        return re.sub(
            r'(version\s*=\s*")([^"]+)(")',
            lambda m: f'{m.group(1)}{new_version}{m.group(3)}',
            entry_text,
            count=1,
        )

    return re.sub(
        r'^(\s*[A-Za-z0-9_\-]+\s*=\s*")([^"]+)(".*)',
        lambda m: f'{m.group(1)}{new_version}{m.group(3)}',
        entry_text,
        count=1,
        flags=re.DOTALL,
    )


def render_section(header: str, entries: List[Entry]) -> str:
    lines: List[str] = [f"[{header}]"]
    for entry in entries:
        lines.append(entry.text)
    if lines and lines[-1] != "":
        lines.append("")
    return "\n".join(lines)


def merge_section(
    section: str,
    original_entries: List[Entry],
    generated_entries: List[Entry],
    generated_map: Dict[str, Entry],
    key_to_generated_sections: Dict[str, Set[str]],
    original_versions: Dict[Tuple[str, str], str],
) -> List[Entry]:
    """Merge dependency entries while preserving curated versions and avoiding duplicates."""
    merged: List[Entry] = []
    processed: set[str] = set()

    for entry in original_entries:
        if entry.key is None:
            merged.append(entry)
            continue

        generated_sections = key_to_generated_sections.get(entry.key)
        if not generated_sections:
            merged.append(entry)
            continue

        if section not in generated_sections:
            continue

        generated_entry = generated_map.get(entry.key)
        if generated_entry is None:
            merged.append(entry)
            continue

        updated_text = generated_entry.text
        original_version = original_versions.get((section, entry.key))
        if original_version is not None:
            updated_text = replace_version(updated_text, original_version)

        merged.append(Entry(entry.key, updated_text))
        processed.add(entry.key)

    for entry in generated_entries:
        if entry.key is None:
            continue
        if entry.key in processed:
            continue
        generated_sections = key_to_generated_sections.get(entry.key)
        if not generated_sections or section not in generated_sections:
            continue

        updated_text = entry.text
        original_version = original_versions.get((section, entry.key))
        if original_version is not None:
            updated_text = replace_version(updated_text, original_version)

        merged.append(Entry(entry.key, updated_text))
        processed.add(entry.key)

    return merged


def update_cargo(original: Path, generated: Path) -> None:
    original_text = original.read_text()
    generated_text = generated.read_text()

    updated_text = original_text

    original_sections: Dict[str, List[Entry]] = {}
    original_versions: Dict[Tuple[str, str], str] = {}
    for section in SECTION_NAMES:
        orig_entries, _ = extract_section(updated_text, section)
        original_sections[section] = orig_entries
        for entry in orig_entries:
            if entry.key:
                version = extract_version(entry.text)
                if version is not None:
                    original_versions[(section, entry.key)] = version

    generated_sections: Dict[str, Tuple[List[Entry], Dict[str, Entry]]] = {}
    key_to_generated_sections: Dict[str, Set[str]] = {}
    for section in SECTION_NAMES:
        gen_entries, gen_map = extract_section(generated_text, section)
        generated_sections[section] = (gen_entries, gen_map)
        for key in gen_map:
            key_to_generated_sections.setdefault(key, set()).add(section)

    for section in SECTION_NAMES:
        orig_entries = original_sections.get(section, [])
        gen_entries, gen_map = generated_sections.get(section, ([], {}))

        if not gen_entries and not orig_entries:
            continue

        merged_entries = merge_section(
            section,
            orig_entries,
            gen_entries,
            gen_map,
            key_to_generated_sections,
            original_versions,
        )
        if merged_entries:
            new_section = render_section(section, merged_entries)
        else:
            new_section = ""

        if new_section and not new_section.endswith("\n"):
            new_section += "\n"
        if new_section and not new_section.endswith("\n\n"):
            new_section += "\n"

        pattern = re.compile(
            rf"(?ms)^\[{re.escape(section)}\]\n.*?(?=^\[|\Z)"
        )

        if pattern.search(updated_text):
            updated_text = pattern.sub(new_section, updated_text, count=1)
        else:
            if new_section:
                if not updated_text.endswith("\n"):
                    updated_text += "\n"
                updated_text += new_section + "\n"

    original.write_text(updated_text)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: merge_cargo_dependencies.py <path-to-Cargo.toml> <path-to-generated>",
            file=sys.stderr,
        )
        return 1

    cargo_path = Path(argv[1]).resolve()
    generated_path = Path(argv[2]).resolve()

    if not cargo_path.exists():
        print(f"Cargo.toml not found: {cargo_path}", file=sys.stderr)
        return 1
    if not generated_path.exists():
        print(f"Generated Cargo.toml not found: {generated_path}", file=sys.stderr)
        return 1

    update_cargo(cargo_path, generated_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
