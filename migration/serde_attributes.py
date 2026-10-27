import re
from pathlib import Path


def serde_field_attributes(path: Path):
    """Map each public struct field to its directly preceding serde attributes."""
    out = {}
    if not path.exists():
        return out

    lines = path.read_text().splitlines()
    pending = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("#[serde("):
            attribute = [line.strip()]
            depth = line.count("(") - line.count(")")
            while depth > 0 and i + 1 < len(lines):
                i += 1
                attribute.append(lines[i].strip())
                depth += lines[i].count("(") - lines[i].count(")")
            pending.extend(attribute)
            i += 1
            continue

        field = re.match(r"\s*pub (?:r#)?(\w+)\s*:", line)
        if field:
            out[field.group(1)] = " ".join(pending) if pending else ""
            pending = []
        elif line.strip() and not line.strip().startswith(("///", "//", "#[")):
            pending = []
        i += 1

    return out
