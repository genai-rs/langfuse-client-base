# langfuse-client-base 0.21 → 0.22.0: timvw-rust 0.26.0, runtime 0.2

This release generates with `timvw-rust` 0.26.0 and moves to `timvw-rust-runtime` 0.2. The Langfuse spec
(`openapi.yml`) and openapi-generator (7.27.0) are unchanged, and `scripts/generate-openapi-client.sh` only changes its
image tag. The census is `api-diff-0.21.0-to-0.22.0.json` (`compare_public_api.py` against v0.21.0): no model, field or
operation is added or removed; every operation gets one optional argument and the credentials change type.

## What changes

- **Credentials are `SecretString`s (breaking).** The password of `basic_auth` is `Option<SecretString>` (as are
  `bearer_access_token`, `oauth_access_token` and `ApiKey::key`), from `secrecy`, re-exported as
  `apis::configuration::{SecretString, ExposeSecret}`. `Debug` stays redacted and the `Authorization` header is marked
  sensitive.
- **Per-call request options (additive).** Every operation's builder takes `.options(&options)`, a
  `timvw_rust_runtime::RequestOptions` (re-exported as `apis::RequestOptions`) with extra headers and query parameters.
- **Retries (runtime 0.2).** Jittered backoff; `Retry-After`/`retry-after-ms` honoured up to 60 s instead of capped at
  8 s; a longer one is returned at once.

## Upgrading

```rust
// 0.21
basic_auth: Some((public_key, Some(secret_key))),
// 0.22
basic_auth: Some((public_key, Some(secret_key.into()))),
```

A lock file that holds `timvw-rust-runtime` 0.1 updates with `cargo update -p timvw-rust-runtime`.
