# Platforms

## Cargo features

- `rustls` (default): TLS with rustls.
- `native-tls`: the platform's TLS instead.
- `retry` (default): the default client retries `429`, `408`, `5xx` and failed connections (see
  [HTTP client](http-client.md#retries)).
- `tracing`: `timvw_rust_runtime::trace::TraceLayer`, which logs each request and retry with `tracing`.

## TLS backend

The default client is reqwest (through `timvw-rust-runtime`) without its default features, so the TLS backend is
chosen through this crate's features. `rustls`, the default, is pure Rust and builds the same everywhere. For native
TLS (OpenSSL on Linux, Schannel on Windows, Security Framework on macOS):

```toml
[dependencies]
langfuse-client-base = { version = "0.x", default-features = false, features = ["native-tls", "retry"] }
```

Use the current version from the crates.io badge on the [README](../README.md), or
`cargo add langfuse-client-base --no-default-features --features native-tls,retry`.

## Alpine Linux / musl

When building for Alpine Linux or other musl-based systems with `native-tls`:

```dockerfile
RUN apk add --no-cache openssl-dev musl-dev
```

## Static linking

For fully static binaries with rustls:

```bash
RUSTFLAGS="-C target-feature=+crt-static" cargo build --release --target x86_64-unknown-linux-musl
```

## WebAssembly

The crate builds for `wasm32-unknown-unknown` with `default-features = false` (the browser does TLS):

```toml
langfuse-client-base = { version = "0.x", default-features = false }
```

Retries (feature `retry`) back off with browser timers.

## Minimum supported Rust version

The MSRV is the one of `timvw-rust-runtime` (see the MSRV badge). To build on it, resolve dependency versions that
support it: `CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS=fallback cargo update` (or `resolver = "3"` in your workspace).
