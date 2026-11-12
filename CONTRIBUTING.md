# Contributing to langfuse-client-base

This repository contains **auto-generated code** from the Langfuse OpenAPI specification. 

## ⚠️ Important Note

**Do not manually edit the generated code in `src/`**. All code is automatically generated and any manual changes will be overwritten during the next generation.

## Regenerating the Client

To update the client with the latest OpenAPI spec:

```bash
./scripts/generate-openapi-client.sh
```

## Public API check

`scripts/check_public_api.sh` compares the public Rust API in `src/` (model exports, struct fields, enum variants, function signatures, derives and serde attributes) against the latest release tag and writes `target/reports/public-api-diff.json`. It needs git tags (`git fetch --tags`) and exits 1 on any difference. Set `ALLOW_API_CHANGES=1` to let it pass when a change is intentional (for example a breaking release); document it in a migration note.

CI runs it on every PR, but it only *fails* a PR that changes the generation pipeline (`scripts/`, `migration/`, the generate workflow): such a change is compared against the PR's base commit and must reproduce that API, or ship the diff intentionally: label the PR `api-change` and add a migration note. Spec-driven regeneration PRs are expected to move the API, so for them the job is report-only.

## Reporting Issues

If you find issues with the generated client:
1. Check if it's an issue with the OpenAPI spec itself
2. Check if it's an issue with the generation process
3. Open an issue describing the problem
