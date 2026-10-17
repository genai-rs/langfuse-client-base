#!/usr/bin/env python3
"""Keep the published v3 Rust interface while consuming the current Cloud spec."""

import argparse
import copy
import json
from pathlib import Path

import yaml

COMPATIBILITY_FILE = Path(__file__).with_name("legacy_v3_compatibility.json")


def prepare_spec(spec: dict, compatibility: dict) -> dict:
    result = copy.deepcopy(spec)
    for path, methods in compatibility["paths"].items():
        target = result["paths"].setdefault(path, {})
        for method, legacy in methods.items():
            if method not in target:
                target[method] = copy.deepcopy(legacy)
            else:
                # Upstream renamed/moved these operations between Rust modules.
                # Retain their published identity, but consume current wire docs.
                target[method]["operationId"] = legacy["operationId"]
                target[method]["tags"] = copy.deepcopy(legacy["tags"])
    schemas = result["components"]["schemas"]
    for name, schema in compatibility["components"]["schemas"].items():
        if name in ("CreateScoresRequest", "CreateScoresResponse"):
            # v3 supports both a single score and batches. The v4-only spec
            # narrows these unions and would remove published enum variants.
            schemas[name] = copy.deepcopy(schema)
        else:
            schemas.setdefault(name, copy.deepcopy(schema))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    spec = yaml.safe_load(args.spec.read_text(encoding="utf-8"))
    compatibility = json.loads(COMPATIBILITY_FILE.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(prepare_spec(spec, compatibility), indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
