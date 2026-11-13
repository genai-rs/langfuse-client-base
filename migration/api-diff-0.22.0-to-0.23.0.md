# langfuse-client-base 0.22 → 0.23.0: timvw-rust 0.27.0, runtime 0.3

This release generates with `timvw-rust` 0.27.0 and moves to `timvw-rust-runtime` 0.3. The Langfuse spec and
openapi-generator (7.27.0) are unchanged and the generated code is the same; the census
(`api-diff-0.22.0-to-0.23.0.json`) shows no public API change. It is a minor release because the runtime's types
(`Configuration.client`, `Error::Http`) are now those of 0.3.

## What changes

- **Runtime 0.3:** `ProviderLayer`, `Retry-After` HTTP dates, `RetryPolicy::server_directed_429`, `Upload` and
  downloads (`Response::save_to`), an SSE idle timeout.
- **WebAssembly:** the crate builds for `wasm32-unknown-unknown` with `default-features = false` (the browser does TLS);
  retries back off with browser timers.

## Upgrading

Code that builds its own `timvw_rust_runtime::Client` (or layers) moves to `timvw-rust-runtime` 0.3:
`cargo update -p timvw-rust-runtime` and bump the requirement to `0.3`.
