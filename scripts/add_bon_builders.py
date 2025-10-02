#!/usr/bin/env python3
"""
Add bon::Builder derives to generated structs in src/models.
Only applies to actual structs, not enums or sub-types.
"""

import re
import sys
from pathlib import Path

def add_bon_builder_to_all_structs(root_dir: Path) -> None:
    """Add bon::Builder to all structs in the models directory."""
    models_dir = root_dir / "src" / "models"
    if not models_dir.exists():
        print(f"⚠️ Models directory not found at {models_dir}")
        return

    for file_path in models_dir.glob("*.rs"):
        if file_path.name == "mod.rs":
            continue

        content = file_path.read_text()
        if "bon::Builder" in content:
            continue

        lines = content.splitlines()
        modified = False
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("#[derive(") and i + 1 < len(lines):
                next_line = lines[i + 1]
                if re.match(r"^pub struct \w+ \{", next_line):
                    closing_paren = line.rfind(")")
                    if closing_paren != -1:
                        lines[i] = line[:closing_paren] + ", bon::Builder" + line[closing_paren:]
                        modified = True
            i += 1

        if modified:
            file_path.write_text("\n".join(lines))
            print(f"Added bon::Builder derives in {file_path}")

def add_bon_builder_to_other_structs(root_dir: Path) -> None:
    """Add bon::Builder to common request/response structs that benefit from builders."""
    models_dir = root_dir / "src" / "models"
    other_patterns = [
        "create_message_request.rs",
        "create_thread_request.rs",
        "create_run_request.rs",
        "submit_tool_outputs_run_request.rs",
        "modify_assistant_request.rs",
        "modify_thread_request.rs",
        "modify_message_request.rs",
        "modify_run_request.rs",
    ]

    for pattern in other_patterns:
        file_path = models_dir / pattern
        if not file_path.exists():
            continue

        content = file_path.read_text()
        if "bon::Builder" in content:
            continue

        struct_match = re.search(r"^pub struct (\w+) \{", content, re.MULTILINE)
        if not struct_match:
            continue

        struct_name = struct_match.group(1)
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("#[derive(") and idx + 1 < len(lines):
                next_line = lines[idx + 1]
                if next_line.startswith(f"pub struct {struct_name} {{"):
                    closing_paren = line.rfind(")")
                    if closing_paren != -1:
                        lines[idx] = line[:closing_paren] + ", bon::Builder" + line[closing_paren:]
                        file_path.write_text("\n".join(lines))
                        print(f"Added bon::Builder to {struct_name} in {file_path.name}")
                    break

def main() -> None:
    root_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(f"Adding bon::Builder derives under {root_dir}")
    add_bon_builder_to_all_structs(root_dir)
    add_bon_builder_to_other_structs(root_dir)
    print("Done adding bon::Builder derives")

if __name__ == "__main__":
    main()
