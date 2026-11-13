# langfuse-client-base 0.23 → 0.24.0: timvw-rust 0.29.0, runtime 0.4

This release generates with `timvw-rust` 0.29.0 and moves to `timvw-rust-runtime` 0.4. The Langfuse spec and
openapi-generator (7.27.0) are unchanged. The census (`api-diff-0.23.0-to-0.24.0.json`) shows no change to models,
fields or operation signatures; it does not cover the `apis::Error` enum, which loses its `Io` variant. It is a minor
release because of that variant and because the runtime's types (`Configuration.client`, `Error::Http`,
`RequestOptions`) are now those of 0.4.

## What changes

- **`apis::Error::Io` and its `From<std::io::Error>` are removed.** Nothing produced them: the Langfuse API has no file
  uploads, and a failure to send or read a request is `Error::Http`.
- **`RequestOptions::base_url`** (runtime 0.4): the generated functions declare `Configuration.base_path` to the
  request, and `.options(&RequestOptions::new().base_url("https://...")?)` sends one call to another base URL, keeping
  the operation's path and query.
- **Per-call options win over `ProviderLayer`**: it no longer replaces a header or query parameter the options set,
  nor moves a call that has a base URL of its own.
- **reqwest-middleware** is no longer part of the generator; this crate already sent through the runtime.

## Upgrading

- Remove `match` arms on `Error::Io`.
- Code that builds its own `timvw_rust_runtime::Client` (or layers) or names `RequestOptions` moves to
  `timvw-rust-runtime` 0.4: bump the requirement to `0.4` and `cargo update -p timvw-rust-runtime`.
