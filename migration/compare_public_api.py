import json
import re
from pathlib import Path
import argparse
from serde_attributes import serde_field_attributes
from rust_declarations import public_enums, public_type_names, trait_impls

parser = argparse.ArgumentParser(description="Compare public Rust source declarations between two crate source trees.")
parser.add_argument("registry_src", type=Path, help="Reference src/ directory (a published crate or a git ref's src/)")
parser.add_argument("candidate_src", type=Path, help="Candidate src/ directory")
parser.add_argument("--reference-label", default=None, help="How the reference tree is described in the report (default: its path)")
parser.add_argument("--candidate-label", default=None, help="How the candidate tree is described in the report (default: its path)")
parser.add_argument("--fail-on-change", action="store_true", help="Exit 1 when any public declaration differs")
args = parser.parse_args()
old, new = args.registry_src, args.candidate_src


def files(root):
    return {str(p.relative_to(root)): p for p in root.rglob("*.rs")}


def fields(path):
    result = {}
    if not path.exists():
        return result
    active_struct = None
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.search(r"pub struct (\w+)\s*\{", line)
        if match:
            active_struct = match.group(1)
            result[active_struct] = {}
            i += 1
            continue
        if active_struct:
            if line.strip() == "}":
                active_struct = None
            else:
                match = re.match(r"\s*pub (?:r#)?(\w+)\s*:\s*(.*)", line)
                if match:
                    name, tail = match.groups()
                    typ = tail
                    depth = sum(tail.count(a) - tail.count(b) for a, b in (("<", ">"), ("(", ")"), ("[", "]")))
                    while depth > 0 or not re.search(r",\s*$", typ):
                        if i + 1 >= len(lines):
                            break
                        i += 1
                        continuation = lines[i].strip()
                        typ += " " + continuation
                        depth += sum(continuation.count(a) - continuation.count(b) for a, b in (("<", ">"), ("(", ")"), ("[", "]")))
                    nesting = 0
                    end = len(typ)
                    for pos, char in enumerate(typ):
                        nesting += (char in "<([{") - (char in ">)]}")
                        if char == "," and nesting == 0:
                            end = pos
                            break
                    typ = typ[:end].strip()
                    result[active_struct][name] = re.sub(r"\s+", " ", typ)
        i += 1
    return result


def api_functions(root):
    out = {}
    for rel, path in files(root).items():
        text = path.read_text()
        for match in re.finditer(r"pub (?:async )?fn (\w+)\s*\(", text):
            name = match.group(1)
            start = match.start()
            brace = text.find("{", match.end())
            semi = text.find(";", match.end())
            ends = [x for x in (brace, semi) if x != -1]
            sig = text[start:min(ends) if ends else match.end()]
            sig = re.sub(r"\s+", " ", sig).strip()
            out[(rel, name)] = sig
    return out


old_files, new_files = files(old), files(new)
old_fields = {f: fields(p) for f, p in old_files.items()}
new_fields = {f: fields(p) for f, p in new_files.items()}
field_changes = []
for file in sorted(old_fields.keys() | new_fields.keys()):
    old_models, new_models = old_fields.get(file, {}), new_fields.get(file, {})
    for model in sorted(old_models.keys() | new_models.keys()):
        before, after = old_models.get(model, {}), new_models.get(model, {})
        for field in sorted(before.keys() | after.keys()):
            if before.get(field) != after.get(field):
                field_changes.append({"file": file, "model": model, "field": field, "registry": before.get(field), "current": after.get(field)})


def model_exports(root):
    text = (root / "models/mod.rs").read_text()
    return set(re.findall(r"pub use self::[^:]+::([A-Za-z0-9_]+);", text))


def enum_declarations(root):
    """{(file, enum): {variant: normalized declaration}} for every public enum, generic ones included."""
    out = {}
    for rel, path in files(root).items():
        for enum, variants in public_enums(path.read_text()).items():
            out[(rel, enum)] = variants
    return out


def public_trait_impls(root, public_types):
    """{(file, self type): {impl header}} for trait impls whose self type is a public type of the crate."""
    out = {}
    for rel, path in files(root).items():
        for header, self_type in trait_impls(path.read_text()):
            if self_type in public_types:
                out.setdefault((rel, self_type), set()).add(header)
    return out


def public_types(root):
    names = set()
    for path in files(root).values():
        names |= public_type_names(path.read_text())
    return names


def derive_attributes(root):
    out = {}
    for rel, path in files(root).items():
        text = path.read_text()
        for match in re.finditer(r"#\[derive\(([^)]*)\)\]\s*pub\s+(?:struct|enum)\s+(\w+)", text, re.S):
            derives = sorted(x.strip() for x in match.group(1).split(",") if x.strip())
            out[(rel, match.group(2))] = derives
    return out


def serde_field_attribute_changes(old_root, new_root, field_diffs):
    changed = []
    for entry in field_diffs:
        rel, field = entry["file"], entry["field"]
        before = serde_field_attributes(old_root / rel).get(field)
        after = serde_field_attributes(new_root / rel).get(field)
        if before != after:
            changed.append({"file": rel, "model": entry["model"], "field": field, "registry": before, "current": after})
    return changed


old_exports, new_exports = model_exports(old), model_exports(new)
old_fns, new_fns = api_functions(old), api_functions(new)
old_enums, new_enums = enum_declarations(old), enum_declarations(new)
old_variants = {key: set(value) for key, value in old_enums.items()}
new_variants = {key: set(value) for key, value in new_enums.items()}
payload_changes = []
for key in sorted(old_enums.keys() & new_enums.keys()):
    before, after = old_enums[key], new_enums[key]
    for variant in sorted(before.keys() & after.keys()):
        if before[variant] != after[variant]:
            payload_changes.append({"file": key[0], "enum": key[1], "variant": variant, "registry": before[variant], "current": after[variant]})
all_public_types = public_types(old) | public_types(new)
old_impls, new_impls = public_trait_impls(old, all_public_types), public_trait_impls(new, all_public_types)
impl_changes = []
for key in sorted(old_impls.keys() | new_impls.keys()):
    before, after = old_impls.get(key, set()), new_impls.get(key, set())
    if before != after:
        impl_changes.append({"file": key[0], "type": key[1], "added": sorted(after - before), "removed": sorted(before - after)})
old_derives, new_derives = derive_attributes(old), derive_attributes(new)
variant_changes = []
for key in sorted(old_variants.keys() | new_variants.keys()):
    before, after = old_variants.get(key, set()), new_variants.get(key, set())
    if before != after:
        variant_changes.append({"file": key[0], "enum": key[1], "added": sorted(after - before), "removed": sorted(before - after)})
result = {
    "source_heads": {"reference": args.reference_label or str(old), "candidate": args.candidate_label or str(new)},
    "method": "Source declaration census of public model exports, struct fields, enum variants (names and tuple/struct payloads, generic enums such as apis::Error<T> included), function signatures, and hand-written trait impls (e.g. From) on public types, plus derive and serde-field-attribute differences. This is not an exhaustive Rust public API or semver check: it does not expand derives or macros, resolve blanket impls, or resolve every visibility/re-export interaction.",
    "registry_source_rs_files": len(old_files),
    "current_source_rs_files": len(new_files),
    "source_files_added": sorted(new_files.keys() - old_files.keys()),
    "source_files_removed": sorted(old_files.keys() - new_files.keys()),
    "source_files_modified": sorted(f for f in old_files.keys() & new_files.keys() if old_files[f].read_bytes() != new_files[f].read_bytes()),
    "model_exports_added": sorted(new_exports - old_exports),
    "model_exports_removed": sorted(old_exports - new_exports),
    "public_functions_added_or_signature_changed": [{"file": f, "name": n, "signature": new_fns[(f, n)]} for (f, n) in sorted(new_fns) if old_fns.get((f, n)) != new_fns[(f, n)]],
    "public_functions_removed_or_signature_changed": [{"file": f, "name": n, "signature": old_fns[(f, n)]} for (f, n) in sorted(old_fns) if new_fns.get((f, n)) != old_fns[(f, n)]],
    "public_model_field_changes": field_changes,
    "public_enum_variant_changes": variant_changes,
    "public_derive_changes": [{"file": f, "type": t, "registry": old_derives.get((f, t)), "current": new_derives.get((f, t))} for (f, t) in sorted(old_derives.keys() | new_derives.keys()) if old_derives.get((f, t)) != new_derives.get((f, t))],
    "serde_field_attribute_changes": serde_field_attribute_changes(old, new, field_changes),
    "public_enum_variant_payload_changes": payload_changes,
    "public_trait_impl_changes": impl_changes,
}
result["counts"] = {
    "model_exports_added": len(result["model_exports_added"]),
    "model_exports_removed": len(result["model_exports_removed"]),
    "public_functions_added_or_signature_changed": len(result["public_functions_added_or_signature_changed"]),
    "public_functions_removed_or_signature_changed": len(result["public_functions_removed_or_signature_changed"]),
    "public_model_field_changes": len(field_changes),
    "public_enum_types_with_variant_changes": len(variant_changes),
    "public_enum_variants_added": sum(len(x["added"]) for x in variant_changes),
    "public_enum_variants_removed": sum(len(x["removed"]) for x in variant_changes),
    "public_derive_changes": len(result["public_derive_changes"]),
    "serde_field_attribute_changes": len(result["serde_field_attribute_changes"]),
    "public_enum_variant_payload_changes": len(payload_changes),
    "public_types_with_trait_impl_changes": len(impl_changes),
    "public_trait_impls_added": sum(len(x["added"]) for x in impl_changes),
    "public_trait_impls_removed": sum(len(x["removed"]) for x in impl_changes),
}
print(json.dumps(result, indent=2))
if args.fail_on_change and any(result["counts"].values()):
    raise SystemExit(1)
