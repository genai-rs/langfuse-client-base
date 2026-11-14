"""Comment- and formatting-insensitive parsing of public enums and trait impls.

Used by compare_public_api.py. The parser is deliberately small: it strips
comments and string literals, then scans balanced brackets, which is enough for
the generated sources of these crates (no macros produce public enums/impls).
"""
import re

OPEN, CLOSE = "<([{", ">)]}"


def mask(text):
    """Drop comments and empty string literals; keep everything else (and line structure)."""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j == -1 else j
            continue
        if text.startswith("/*", i):
            depth, i = 1, i + 2
            while i < n and depth:
                if text.startswith("/*", i):
                    depth, i = depth + 1, i + 2
                elif text.startswith("*/", i):
                    depth, i = depth - 1, i + 2
                else:
                    i += 1
            out.append(" ")
            continue
        raw = re.match(r'b?r(#*)"', text[i:i + 260]) if c in "rb" and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")) else None
        if raw:
            end = text.find('"' + raw.group(1), i + raw.end())
            i = n if end == -1 else end + 1 + len(raw.group(1))
            out.append('""')
            continue
        if c == '"':
            i += 1
            while i < n and text[i] != '"':
                i += 2 if text[i] == "\\" else 1
            i += 1
            out.append('""')
            continue
        out.append(c)
        i += 1
    return "".join(out)


def normalize(fragment):
    """Canonical spelling of a type/declaration fragment: no layout, no trailing commas."""
    text = re.sub(r"\s+", " ", fragment).strip()
    text = re.sub(r" (?=\W)|(?<=[^\w>]) ", "", text)
    text = re.sub(r",(?=[>)\]}])", "", text)
    text = text.replace(",", ", ")
    return re.sub(r"(?<!:):(?!:)", ": ", text)


def _split_top_level(body):
    """Split at commas outside any bracket (arrows are not brackets)."""
    parts, depth, start, i = [], 0, 0, 0
    while i < len(body):
        if body.startswith(("->", "=>"), i):
            i += 2
            continue
        ch = body[i]
        if ch in OPEN:
            depth += 1
        elif ch in CLOSE:
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(body[start:i])
            start = i + 1
        i += 1
    parts.append(body[start:])
    return [p for p in parts if p.strip()]


def _matching(text, start):
    """Index just past the bracket that closes text[start]."""
    depth, i = 0, start
    while i < len(text):
        if text.startswith(("->", "=>"), i):
            i += 2
            continue
        if text[i] in OPEN:
            depth += 1
        elif text[i] in CLOSE:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def _strip_attributes(entry):
    entry = entry.strip()
    while entry.startswith("#"):
        bracket = entry.find("[")
        if bracket == -1:
            break
        entry = entry[_matching(entry, bracket):].strip()
    return entry


def public_enums(text):
    """{enum name: {variant name: normalized declaration}} for every `pub enum` in a source file."""
    masked = mask(text)
    out = {}
    for match in re.finditer(r"(?<![\w:])pub\s+enum\s+(?:r#)?(\w+)", masked):
        i = match.end()
        depth = 0
        while i < len(masked):  # skip generics / where clause up to the body
            ch = masked[i]
            if masked.startswith("->", i):
                i += 2
                continue
            if ch in "<(":
                depth += 1
            elif ch in ">)":
                depth -= 1
            elif ch == "{" and depth == 0:
                break
            elif ch == ";" and depth == 0:
                i = -1
                break
            i += 1
        if i < 0 or i >= len(masked):
            continue
        body = masked[i + 1:_matching(masked, i) - 1]
        variants = {}
        for entry in _split_top_level(body):
            entry = _strip_attributes(entry)
            name = re.match(r"(?:r#)?(\w+)", entry)
            if not name:
                continue
            variants[name.group(1)] = name.group(1) + normalize(entry[name.end():])
        out[match.group(1)] = variants
    return out


def public_type_names(text):
    return set(re.findall(r"(?<![\w:])pub\s+(?:struct|enum|type|trait|union)\s+(?:r#)?(\w+)", mask(text)))


def trait_impls(text):
    """Normalized headers of `impl ... Trait for Type` items, with the self type's base name."""
    masked = mask(text)
    out = []
    for match in re.finditer(r"(?m)^[ \t]*(?:unsafe\s+)?impl\b", masked):
        i = match.end()
        depth = 0
        while i < len(masked):
            if masked.startswith(("->", "=>"), i):
                i += 2
                continue
            ch = masked[i]
            if ch in "<([":
                depth += 1
            elif ch in ">)]":
                depth -= 1
            elif ch in "{;" and depth == 0:
                break
            i += 1
        header = normalize(masked[match.start():i])
        header_spaced = re.sub(r"\s+", " ", masked[match.start():i]).strip()
        # top-level " for " separates the trait from the self type
        depth, split = 0, None
        for pos, ch in enumerate(header_spaced):
            if ch in "<([":
                depth += 1
            elif ch in ">)]":
                depth -= 1
            elif depth == 0 and header_spaced.startswith(" for ", pos) and not header_spaced[:pos].rstrip().endswith(("impl", "unsafe impl")):
                split = pos
                break
        if split is None:
            continue
        self_type = header_spaced[split + 5:].split(" where ")[0].strip()
        base = re.match(r"(?:&\s*(?:'\w+\s+)?(?:mut\s+)?)?((?:\w+::)*)(\w+)", self_type)
        out.append((header, base.group(2) if base else self_type))
    return out
