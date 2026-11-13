# Usage

`langfuse-client-base` has a module per API tag under `apis` (`trace_api`, `scores_api`, `prompts_api`, …) with one
async function per operation, and a type per schema under `models`. Every function has a
[bon](https://bon-rs.com) builder: set the parameters, then `.call().await`. The
[API reference](https://docs.rs/langfuse-client-base) lists them all; the generated
[`docs/`](https://github.com/genai-rs/langfuse-client-base/tree/main/docs) has a page per API and model.

## Configuration

Langfuse authenticates with HTTP basic auth: the public key is the user name, the secret key the password. The secret
is a `SecretString`, redacted in `Debug`. `Configuration::default()` points at `http://localhost`: set `base_path` to
your Langfuse host.

```rust
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: "https://cloud.langfuse.com".to_string(),
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".into()))),
    ..Default::default()
};
```

From environment variables:

```rust
use std::env;
use langfuse_client_base::apis::configuration::Configuration;

let config = Configuration {
    base_path: env::var("LANGFUSE_HOST").unwrap_or_else(|_| "https://cloud.langfuse.com".to_string()),
    basic_auth: Some((
        env::var("LANGFUSE_PUBLIC_KEY").expect("LANGFUSE_PUBLIC_KEY not set"),
        Some(env::var("LANGFUSE_SECRET_KEY").expect("LANGFUSE_SECRET_KEY not set").into()),
    )),
    ..Default::default()
};
```

[`examples/basic_usage.rs`](../examples/basic_usage.rs) does the same (`cargo run --example basic_usage`).

### Self-hosted instances

Point `base_path` at your deployment, including any path prefix it is served under:

```rust
let config = Configuration {
    base_path: "https://your-domain.com/langfuse".to_string(),
    basic_auth: Some(("your-public-key".to_string(), Some("your-secret-key".into()))),
    ..Default::default()
};
```

## Calling an operation

```rust
use langfuse_client_base::apis::prompts_api;
use langfuse_client_base::models::Prompt;

let prompt = prompts_api::prompts_get()
    .configuration(&config)
    .prompt_name("movie-critic")
    .label("production")
    .call()
    .await?;
match prompt {
    Prompt::TextPrompt(text) => println!("{}", text.prompt),
    Prompt::ChatPrompt(chat) => println!("{} messages", chat.prompt.len()),
    Prompt::Unknown(value) => println!("a prompt type this client does not know: {value}"),
}
```

Unions decode by their tag, and a tag the spec does not list yet decodes to `Unknown` instead of failing.

## Legacy v3 compatibility

The client retains the published v3 ingestion, traces, sessions, dataset-run, observations, metrics and score bindings
for existing self-hosted deployments. These bindings do not make legacy endpoints available on v4 servers. See the
[Langfuse v3 to v4 migration guide](https://langfuse.com/self-hosting/upgrade/upgrade-guides/upgrade-v3-to-v4) for
server availability and migration to OpenTelemetry ingestion and v2 reads.

For a server that still supports v3 batch ingestion:

```rust
#![allow(deprecated)]
use langfuse_client_base::{apis::ingestion_api, models};

let request = models::IngestionBatchRequest::new(Vec::new());
let response = ingestion_api::ingestion_batch()
    .configuration(&config)
    .ingestion_batch_request(&request)
    .call()
    .await?;
```

How these bindings are kept is described in [generation](generation.md#legacy-v3-bindings).

## Errors

Every operation returns `Result<T, apis::Error<E>>`, where `E` is the operation's typed error (a variant per documented
error status, plus `UnknownValue`):

- `Error::ResponseError(response)`: the server answered with an error status. `response.status`, `response.headers`,
  the raw `response.content`, and `response.entity` decoded into `E` when the body matches.
- `Error::Http(e)`: building, sending or reading the request failed: `e.is_timeout()`, `e.is_connect()`, …
- `Error::Serde(e)`: a success response did not decode into the documented type.

```rust
use langfuse_client_base::apis::{projects_api, Error};

match projects_api::projects_get().configuration(&config).call().await {
    Ok(projects) => println!("{} projects", projects.data.len()),
    Err(Error::ResponseError(response)) => eprintln!("{}: {}", response.status, response.content),
    Err(e) => eprintln!("{e}"),
}
```

## Per-call options

Every operation takes optional `.options(&RequestOptions)`: extra headers, query parameters or another base URL for
one call. See [HTTP client](http-client.md#per-call-options).
