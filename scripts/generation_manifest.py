#!/usr/bin/env python3
"""Write deterministic provenance for a generated Langfuse client."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REVISION_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")
SOURCE_REVISION_RE = re.compile(r"/blob/([0-9a-fA-F]{7,64})/")
# Everything that shapes the generator input or output besides the generator
# image itself. Rust-specific fixes live in the generator (timvw-rust), so only
# the spec composition and this pipeline remain.
TRANSFORMATION_SCRIPT_PATHS = (
    "scripts/generate-openapi-client.sh",
    "scripts/generation_manifest.py",
    "scripts/prepare_compatible_spec.py",
)
# <generator version>[-og<openapi-generator version>]: the image bundles one
# openapi-generator release, and the tag names both.
IMAGE_TAG_RE = re.compile(r"(.+):v?(\d+\.\d+\.\d+)(?:-og(\d+\.\d+\.\d+))?")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    *,
    upstream_url: str,
    upstream_revision: str | None,
    project_root: Path,
    raw_spec: Path,
    composed_spec: Path,
    compatibility_file: Path,
    generator_image: str,
) -> dict[str, Any]:
    if upstream_revision:
        if not REVISION_RE.fullmatch(upstream_revision):
            raise ValueError("upstream revision must be a hexadecimal commit id")
        upstream_revision = upstream_revision.lower()

    compatibility = json.loads(compatibility_file.read_text(encoding="utf-8"))
    source_url = compatibility.get("source")
    if not isinstance(source_url, str):
        raise ValueError("compatibility source must contain a source URL")
    source_revision_match = SOURCE_REVISION_RE.search(source_url)

    image_match = IMAGE_TAG_RE.fullmatch(generator_image)
    if not image_match:
        raise ValueError("generator image must include a semantic version tag")

    transformation_scripts = [
        {
            "path": relative_path,
            "revision": sha256_file(project_root / relative_path),
        }
        for relative_path in sorted(TRANSFORMATION_SCRIPT_PATHS)
    ]

    return {
        "schema_version": 1,
        "upstream": {
            "path": "openapi.yml",
            "url": upstream_url,
            "revision": upstream_revision,
            "raw_sha256": sha256_file(raw_spec),
        },
        "composed_input": {
            "format": "openapi-json",
            "path": ".openapi-generator/compatible.json",
            "sha256": sha256_file(composed_spec),
        },
        "compatibility": {
            "path": "scripts/legacy_v3_compatibility.json",
            "source_url": source_url,
            "source_version": (
                source_revision_match.group(1).lower()
                if source_revision_match
                else None
            ),
            "source_sha256": sha256_file(compatibility_file),
        },
        "generator": {
            "image": generator_image,
            "version": image_match.group(2),
            "openapi_generator_version": image_match.group(3),
        },
        "transformation_scripts": transformation_scripts,
    }


def write_manifest(manifest: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-url", required=True)
    parser.add_argument("--upstream-revision", default="")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--raw-spec", type=Path, required=True)
    parser.add_argument("--composed-spec", type=Path, required=True)
    parser.add_argument("--compatibility-file", type=Path, required=True)
    parser.add_argument("--generator-image", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = build_manifest(
        upstream_url=args.upstream_url,
        upstream_revision=args.upstream_revision or None,
        project_root=args.project_root,
        raw_spec=args.raw_spec,
        composed_spec=args.composed_spec,
        compatibility_file=args.compatibility_file,
        generator_image=args.generator_image,
    )
    write_manifest(manifest, args.output)
    print(f"Wrote generation provenance to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
