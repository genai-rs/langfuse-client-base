# langfuse-client-base

[![Crates.io](https://img.shields.io/crates/v/langfuse-client-base.svg)](https://crates.io/crates/langfuse-client-base)
[![Documentation](https://docs.rs/langfuse-client-base/badge.svg)](https://docs.rs/langfuse-client-base)
[![CI](https://github.com/genai-rs/langfuse-client-base/workflows/CI/badge.svg)](https://github.com/genai-rs/langfuse-client-base/actions)
[![MSRV](https://img.shields.io/badge/MSRV-1.88.0-blue)](https://releases.rs/docs/1.88.0/)
[![License](https://img.shields.io/crates/l/langfuse-client-base)](./LICENSE-MIT)

Auto-generated Rust client for the [Langfuse](https://langfuse.com) API, based on the official OpenAPI specification.

> **Important:** most users should use [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic) instead.
> 
> This is a low-level, auto-generated client intended as a building block for higher-level abstractions.
> The ergonomic wrapper provides:
> - Simplified APIs with builder patterns
> - Automatic batching and retries
> - Environment-based configuration
> - Improved error handling
> - Built-in OpenTelemetry integration
>
> **Only use this crate directly if you need:**
> - Raw access to all OpenAPI endpoints
> - Custom retry/batching logic
> - Minimal dependencies

## Features

- Complete API coverage from OpenAPI specification
- Async/await support with Tokio; requests go through [`timvw-rust-runtime`](https://docs.rs/timvw-rust-runtime), a tower service (reqwest by default) with retries
- Choice of TLS backend (rustls or native-tls)
- Strong typing with serde

## Installation

```toml
[dependencies]
langfuse-client-base = "*" # See https://crates.io/crates/langfuse-client-base for latest version
```

## Usage

This crate provides low-level API bindings. Most users should use the ergonomic wrapper instead.

### Basic Configuration

```rust
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: "https://cloud.langfuse.com".to_string(),
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".into()))),
    ..Default::default()
};

// Use the API...
```

### Legacy v3 compatibility

The client retains the published v3 ingestion, traces, sessions, dataset-run,
observations, metrics, and score bindings for existing self-hosted deployments.
These bindings do not make legacy endpoints available on v4 servers. See the
[Langfuse v3 to v4 migration guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4)
for server availability and migration to OpenTelemetry ingestion and v2 reads.

For a server that still supports v3 batch ingestion:

```rust,no_run
# #![allow(deprecated)]
use langfuse_client_base::{apis::{configuration::Configuration, ingestion_api}, models};

# async fn legacy_ingestion() -> Result<(), Box<dyn std::error::Error>> {
let config = Configuration {
    basic_auth: Some(("your-public-key".into(), Some("your-secret-key".into()))),
    ..Default::default()
};
let request = models::IngestionBatchRequest::new(Vec::new());
let response = ingestion_api::ingestion_batch()
    .configuration(&config)
    .ingestion_batch_request(&request)
    .call()
    .await?;
# Ok(())
# }
```

### Using Environment Variables

```rust,no_run
use std::env;
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: env::var("LANGFUSE_HOST").unwrap_or_else(|_| "https://cloud.langfuse.com".to_string()),
    basic_auth: Some((
        env::var("LANGFUSE_PUBLIC_KEY").expect("LANGFUSE_PUBLIC_KEY not set"),
        Some(env::var("LANGFUSE_SECRET_KEY").expect("LANGFUSE_SECRET_KEY not set").into())
    )),
    ..Default::default()
};
```

### Self-Hosted Instances

For self-hosted Langfuse instances:

```rust
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: "https://your-domain.com/langfuse".to_string(),  // Custom base path
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".into()))),
    ..Default::default()
};
```

## HTTP client, retries and middleware

`Configuration.client` is a [`timvw_rust_runtime::Client`](https://docs.rs/timvw-rust-runtime): a tower service.
`Configuration::new()` sends with reqwest and retries `429`, `408`, `5xx` and failed connections (feature `retry`, on
by default), honouring `Retry-After`. Timeouts, logging (feature `tracing`), extra headers, rate limits and your own
middleware are tower layers:

```rust,ignore
use std::time::Duration;

let mut configuration = langfuse_client_base::apis::configuration::Configuration::new();
configuration.client = configuration
    .client
    .clone()
    .layer(timvw_rust_runtime::trace::TraceLayer::new())
    .layer(tower::timeout::TimeoutLayer::new(Duration::from_secs(30)));
```

The [runtime's guide](https://docs.rs/timvw-rust-runtime) covers retries, timeouts, logging, middleware, rate limits
and tests without a network. WebAssembly (`wasm32-unknown-unknown`) works with `default-features = false`. Upgrading from 0.22: runtime 0.3; see
[`migration/api-diff-0.22.0-to-0.23.0.md`](https://github.com/genai-rs/langfuse-client-base/blob/main/migration/api-diff-0.22.0-to-0.23.0.md).
Upgrading from 0.21: credentials are `SecretString`s (`Some(secret_key.into())`) and every operation takes
optional `.options(&RequestOptions)`; see
[`migration/api-diff-0.21.0-to-0.22.0.md`](https://github.com/genai-rs/langfuse-client-base/blob/main/migration/api-diff-0.21.0-to-0.22.0.md).
Upgrading from 0.20: see
[`migration/api-diff-0.20.0-to-0.21.0.md`](https://github.com/genai-rs/langfuse-client-base/blob/main/migration/api-diff-0.20.0-to-0.21.0.md).

## Platform Notes

### TLS Backend

By default, this crate uses `rustls` for TLS, which provides:
- A pure Rust implementation
- Smaller binary size
- Better cross-platform compatibility

For native TLS (OpenSSL on Linux, Schannel on Windows, Security Framework on macOS):

```toml
[dependencies]
langfuse-client-base = { version = "*", default-features = false, features = ["native-tls"] }
```

### Alpine Linux / musl

When building for Alpine Linux or other musl-based systems with `native-tls`:

```dockerfile
RUN apk add --no-cache openssl-dev musl-dev
```

### Static Linking

For fully static binaries with rustls:

```bash
RUSTFLAGS="-C target-feature=+crt-static" cargo build --release --target x86_64-unknown-linux-musl
```

## Generation

This client is generated from the OpenAPI specification using Docker for reproducible builds.

```bash
python3 -m pip install -r scripts/requirements.txt

# Generate client (always uses Docker)
./scripts/generate-openapi-client.sh

# Update to latest OpenAPI spec and regenerate
UPDATE_SPEC=true ./scripts/generate-openapi-client.sh
```

Generation composes the upstream `openapi.yml` with
`scripts/legacy_v3_compatibility.json`, a snapshot of the removed v3 operations
and models from commit `28f072145f3e340274a18e0d477a186a3977edfc`.
It also preserves the published score operation names and single-score unions.
The upstream snapshot stays separate; compatibility rules are reapplied on every
generation, including when the downloaded specification is unchanged.

The composed spec is rendered by the
[timvw-rust](https://github.com/timvw/openapi-generator-timvw-rust) generator,
a build of openapi-generator's `rust` generator that already produces the
crate's conventions (bon builders, crate docs from `README.md`, non-panicking
`deepObject` queries, rustdoc-clean links). Its options, set in
`scripts/generate-openapi-client.sh`, also decide the API's shape: models are
held by value (boxed only on a cycle), inline schemas and union variants have
stable names, unions with a tag decode by it, integers are `i64` unless the
spec says `format: int32`, `Default` exists only where it is a valid value,
closed enums implement `FromStr`, and an enum or tagged union a response can
hold has an `Unknown` catch-all for values the spec does not list. See
`migration/api-diff-0.16.2-to-0.17.0.md` for the move to these rules in 0.17.
Nothing is patched after generation; `Cargo.toml`, `README.md` and `.gitignore` are hand-maintained and
listed in `.openapi-generator-ignore`.

## License

Licensed under either of:
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

## Contributing

This is auto-generated code. To make changes, please update the generation process or contribute to the [main repository](https://github.com/genai-rs/langfuse-ergonomic).
