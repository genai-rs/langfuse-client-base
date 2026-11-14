# Upgrading

Releases that change the generated public API, or the `timvw-rust-runtime` types it exposes, are breaking (a
minor-version bump). Each one has a migration note in [`migration/`](../migration), next to the census of
what changed in the public API (`api-diff-<from>-to-<to>.json`, written by `scripts/check_public_api.sh`). The
[CHANGELOG](../CHANGELOG.md) lists every release.

- **0.25** (Langfuse spec update): `PromptVersionUpdateRequest.new_labels` is `Option<Option<Vec<String>>>`, the new
  `remove_labels` removes labels, and `PromptVersionUpdateRequest::new()` takes no arguments. See
  [`api-diff-0.24.0-to-0.25.0.md`](../migration/api-diff-0.24.0-to-0.25.0.md).
- **0.24** (timvw-rust 0.29.0, runtime 0.4): `apis::Error::Io` is removed; `RequestOptions::base_url` moves one call to
  another base URL; per-call options win over `ProviderLayer`. See
  [`api-diff-0.23.0-to-0.24.0.md`](../migration/api-diff-0.23.0-to-0.24.0.md).
- **0.23** (timvw-rust 0.27.0, runtime 0.3): no API change; runtime 0.3 (`ProviderLayer`, `Retry-After` dates) and
  WebAssembly. See [`api-diff-0.22.0-to-0.23.0.md`](../migration/api-diff-0.22.0-to-0.23.0.md).
- **0.22** (timvw-rust 0.26.0, runtime 0.2): credentials are `SecretString`s (`Some(secret_key.into())`) and every
  operation takes optional `.options(&RequestOptions)`. See
  [`api-diff-0.21.0-to-0.22.0.md`](../migration/api-diff-0.21.0-to-0.22.0.md).
- **0.21** (timvw-rust 0.25.0): requests go through `timvw-rust-runtime`, a tower service. See
  [`api-diff-0.20.0-to-0.21.0.md`](../migration/api-diff-0.20.0-to-0.21.0.md).
- **0.20** (timvw-rust 0.22.0): nullable OpenAI token-detail counts. See
  [`api-diff-0.19.0-to-0.20.0.md`](../migration/api-diff-0.19.0-to-0.20.0.md).
- **0.19** (timvw-rust 0.21.0): request bodies by reference, boxed errors with headers, validation. See
  [`api-diff-0.18.0-to-0.19.0.md`](../migration/api-diff-0.18.0-to-0.19.0.md).
- **0.18**: role-based auth for blob storage integrations. See
  [`api-diff-0.17.0-to-0.18.0.md`](../migration/api-diff-0.17.0-to-0.18.0.md).
- **0.17** (timvw-rust 0.14.0): the generator's typed rendering (unions, open enums, `i64` integers, boxing only on
  cycles). See [`api-diff-0.16.2-to-0.17.0.md`](../migration/api-diff-0.16.2-to-0.17.0.md).
