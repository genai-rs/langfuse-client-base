# Generation

`scripts/generate-openapi-client.sh` regenerates the crate from Langfuse's published OpenAPI specification. The Rust
code comes from the [timvw-rust](https://github.com/timvw/openapi-generator-timvw-rust) generator; nothing is patched
after generation.

The pipeline in short: fetch the spec (with `UPDATE_SPEC=true`) → compose the legacy v3 bindings into the generator
input → record a generation manifest → generate with timvw-rust → `cargo fmt`. CI then builds, tests and compares the
public API with the last release.

```bash
python3 -m pip install -r scripts/requirements.txt

# Regenerate from the checked-in openapi.yml
./scripts/generate-openapi-client.sh

# Update to the latest OpenAPI spec and regenerate
UPDATE_SPEC=true ./scripts/generate-openapi-client.sh

# Use a locally built generator image
GENERATOR_IMAGE=timvw-rust:dev ./scripts/generate-openapi-client.sh
```

Requirements: Docker (runs the generator image `ghcr.io/timvw/openapi-generator-timvw-rust:<version>-og<version>`),
Python 3 and a Rust toolchain.

## What is generated and what is not

Generated, and replaced on every run: `src/` (`src/apis/`, `src/models/` and `src/lib.rs`, which includes `README.md`
as the crate docs) and `docs/` (the reference pages for every API and model). Hand-maintained: `Cargo.toml`,
`README.md` and `.gitignore` (listed in `.openapi-generator-ignore`), and everything the generator does not write:
these guides (`guides/`), `tests/`, `examples/`, `scripts/` and `migration/`. The guides live in `guides/` rather than
under `docs/` because the script deletes `docs/` before generating.

Because `README.md` is the crate's documentation, its Rust code blocks are doctests (`cargo test --doc`), and its links
are absolute so they work on docs.rs.

## The generator and its options

The composed spec is rendered by timvw-rust, which already produces the crate's conventions: bon builders, crate docs
from `README.md`, non-panicking `deepObject` queries, rustdoc-clean links. Models are held by value (boxed only on a
cycle), inline schemas and union variants have stable names, unions with a tag decode by it, integers are `i64` unless
the spec says `format: int32`, `Default` exists only where it is a valid value, closed enums implement `FromStr`, and an
enum or tagged union a response can hold has an `Unknown` catch-all for values the spec does not list. The options set
in the script (`typedEnumParameters`, `deprecatedAttributes`) and why the others stay off are commented there.

To change the generated code, change the generator (a rule or an option), release it, and bump `TIMVW_RUST_VERSION` in
the script.

## Legacy v3 bindings

Generation composes the upstream `openapi.yml` with `scripts/legacy_v3_compatibility.json`, a snapshot of the removed
v3 operations and models from commit `28f072145f3e340274a18e0d477a186a3977edfc` (`prepare_compatible_spec.py`). It also
preserves the published score operation names and single-score unions. The upstream snapshot stays separate;
compatibility rules are reapplied on every generation, including when the downloaded specification is unchanged.

## Checks

- `python3 -m unittest discover -s tests -p 'test_*.py'`: the script tests (spec composition, generation manifest, the generate workflow).
- `cargo test --all-features`, including the README's doctests and mocked-HTTP smoke tests.
- `scripts/check_public_api.sh`: compares the public API with the latest release tag (see
  [CONTRIBUTING](../CONTRIBUTING.md#public-api-check)); a breaking release ships the census and a migration note in
  [`migration/`](../migration) (see [upgrading](upgrading.md)).
