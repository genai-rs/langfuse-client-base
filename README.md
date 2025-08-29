# langfuse-client-base

[![Crates.io](https://img.shields.io/crates/v/langfuse-client-base.svg)](https://crates.io/crates/langfuse-client-base)
[![Documentation](https://docs.rs/langfuse-client-base/badge.svg)](https://docs.rs/langfuse-client-base)
[![CI](https://github.com/genai-rs/langfuse-client-base/workflows/CI/badge.svg)](https://github.com/genai-rs/langfuse-client-base/actions)
[![License](https://img.shields.io/crates/l/langfuse-client-base)](./LICENSE-MIT)

Auto-generated Rust client for the [Langfuse](https://langfuse.com) API, based on the official OpenAPI specification.

## ⚠️ Note

This is a low-level, auto-generated client. For a more ergonomic API, use [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic).

## Features

- Complete API coverage from OpenAPI specification
- Async/await support with Tokio
- Choice of TLS backend (rustls or native-tls)
- Strong typing with serde

## Installation

```toml
[dependencies]
langfuse-client-base = "0.1"
```

## Usage

This crate provides low-level API bindings. Most users should use the ergonomic wrapper instead.

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

## Generation

This client is generated from the OpenAPI specification:

```bash
./scripts/generate-openapi-client.sh
```

## License

Licensed under either of:
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT license ([LICENSE-MIT](LICENSE-MIT))

## Contributing

This is auto-generated code. To make changes, please update the generation process or contribute to the [main repository](https://github.com/genai-rs/langfuse-ergonomic).