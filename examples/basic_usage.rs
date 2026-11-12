//! Basic usage example for langfuse-client-base
//!
//! This example shows how to configure the client using environment variables.
//!
//! To run this example:
//! ```bash
//! export LANGFUSE_PUBLIC_KEY="your-public-key"
//! export LANGFUSE_SECRET_KEY="your-secret-key"
//! export LANGFUSE_HOST="https://cloud.langfuse.com"  # Optional
//! cargo run --example basic_usage
//! ```

use langfuse_client_base::apis::configuration::Configuration;
use std::env;

fn main() {
    // Load configuration from environment variables
    let config = Configuration {
        base_path: env::var("LANGFUSE_HOST")
            .unwrap_or_else(|_| "https://cloud.langfuse.com".to_string()),
        basic_auth: Some((
            env::var("LANGFUSE_PUBLIC_KEY")
                .expect("Please set LANGFUSE_PUBLIC_KEY environment variable"),
            Some(
                env::var("LANGFUSE_SECRET_KEY")
                    .expect("Please set LANGFUSE_SECRET_KEY environment variable"),
            ),
        )),
        ..Default::default()
    };

    println!("Configuration created successfully!");
    println!("Base URL: {}", config.base_path);

    // This crate provides low-level, auto-generated bindings; call the
    // functions in `langfuse_client_base::apis` with this configuration.
}
