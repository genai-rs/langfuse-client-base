# langfuse-client-base

[![Crates.io](https://img.shields.io/crates/v/langfuse-client-base.svg)](https://crates.io/crates/langfuse-client-base)
[![Documentation](https://docs.rs/langfuse-client-base/badge.svg)](https://docs.rs/langfuse-client-base)
[![CI](https://github.com/genai-rs/langfuse-client-base/workflows/CI/badge.svg)](https://github.com/genai-rs/langfuse-client-base/actions)
[![MSRV](https://img.shields.io/badge/MSRV-1.83.0-blue)](https://releases.rs/docs/1.83.0/)
[![License](https://img.shields.io/crates/l/langfuse-client-base)](./LICENSE-MIT)

Auto-generated Rust client for the [Langfuse](https://langfuse.com) API, based on the official OpenAPI specification.

> [!WARNING]
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
- Async/await support with Tokio
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
use langfuse_client_base::apis::ingestion_api;

let config = Configuration {
    base_path: "https://cloud.langfuse.com".to_string(),
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".to_string()))),
    ..Default::default()
};

// Use the API...
```

### Using Environment Variables

```rust,no_run
use std::env;
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: env::var("LANGFUSE_HOST").unwrap_or_else(|_| "https://cloud.langfuse.com".to_string()),
    basic_auth: Some((
        env::var("LANGFUSE_PUBLIC_KEY").expect("LANGFUSE_PUBLIC_KEY not set"),
        Some(env::var("LANGFUSE_SECRET_KEY").expect("LANGFUSE_SECRET_KEY not set"))
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
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".to_string()))),
    ..Default::default()
};
```

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
# Generate client (always uses Docker)
./scripts/generate-openapi-client.sh

# Update to latest OpenAPI spec and regenerate
UPDATE_SPEC=true ./scripts/generate-openapi-client.sh
```

## License

Licensed under either of:
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

## Contributing

This is auto-generated code. To make changes, please update the generation process or contribute to the [main repository](https://github.com/genai-rs/langfuse-ergonomic).
