# HTTP client

`Configuration.client` is a [`timvw_rust_runtime::Client`](https://docs.rs/timvw-rust-runtime): a
[tower](https://docs.rs/tower) service that sends every request. This page covers what it does by default and how to
change it; the [runtime's guide](https://docs.rs/timvw-rust-runtime) has the details.

## Retries

`Configuration::new()` (and `Configuration::default()`) sends with reqwest and retries `429`, `408`, `5xx` and failed
connections (Cargo feature `retry`, on by default), honouring `Retry-After` and backing off with jitter otherwise.
Without the `retry` feature, or with a client of your own, nothing is retried.

## Timeouts, logging and middleware

Timeouts, logging (Cargo feature `tracing`), extra headers, rate limits and your own middleware are tower layers on
the client:

```rust
use std::time::Duration;
use langfuse_client_base::apis::configuration::Configuration;

let mut configuration = Configuration::new();
configuration.client = configuration
    .client
    .clone()
    .layer(timvw_rust_runtime::trace::TraceLayer::new())
    .layer(timvw_rust_runtime::timeout::TimeoutLayer::new(Duration::from_secs(30)));
```

`Client::from_service` replaces reqwest with any tower service (a test double, another HTTP stack), and
`Client::from_reqwest` takes a `reqwest::Client` you configured yourself.

## Per-call options

Every operation takes optional `.options(&RequestOptions)`, applied after everything the generated code sets:

- a header replaces the request's values under that name (authentication included);
- query parameters are appended;
- `base_url` sends this one call to another base URL (another region or deployment), keeping the operation's path and
  query.

```rust
use langfuse_client_base::apis::{health_api, RequestOptions};

let options = RequestOptions::new()
    .header("x-request-source", "batch-job")?
    .base_url("https://us.cloud.langfuse.com")?;
let health = health_api::health_health()
    .configuration(&configuration)
    .options(&options)
    .call()
    .await?;
```

Per-call options also win over a
[`ProviderLayer`](https://docs.rs/timvw-rust-runtime/latest/timvw_rust_runtime/provider/struct.ProviderLayer.html) on
the client: it does not replace a header or query parameter the options set, and it does not move a call that has a
base URL of its own.

## TLS

The default client is reqwest without default features: choose a TLS backend with this crate's `rustls` (the
default) or `native-tls` feature. See [platforms](platforms.md#tls-backend).
