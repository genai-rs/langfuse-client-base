//! Extended configuration with transport control knobs
//!
//! This module provides a builder pattern for creating Configuration instances
//! with fine-grained control over HTTP transport settings.

use std::time::Duration;
use crate::apis::configuration::{Configuration, BasicAuth, ApiKey};

/// Builder for creating Configuration with advanced transport settings
#[derive(Debug, Clone)]
pub struct ConfigurationBuilder {
    base_path: String,
    user_agent: Option<String>,
    basic_auth: Option<BasicAuth>,
    oauth_access_token: Option<String>,
    bearer_access_token: Option<String>,
    api_key: Option<ApiKey>,
    // Transport knobs
    timeout: Option<Duration>,
    connect_timeout: Option<Duration>,
    pool_idle_timeout: Option<Duration>,
    pool_max_idle_per_host: Option<usize>,
    tcp_nodelay: Option<bool>,
    tcp_keepalive: Option<Duration>,
    http1_only: bool,
    gzip: bool,
    brotli: bool,
    deflate: bool,
    trust_dns: bool,
    https_only: bool,
    retry_count: usize,
    retry_delay: Duration,
}

impl Default for ConfigurationBuilder {
    fn default() -> Self {
        Self {
            base_path: "https://cloud.langfuse.com".to_string(),
            user_agent: Some(format!("langfuse-client-base/{}", env!("CARGO_PKG_VERSION"))),
            basic_auth: None,
            oauth_access_token: None,
            bearer_access_token: None,
            api_key: None,
            // Sensible defaults
            timeout: Some(Duration::from_secs(30)),
            connect_timeout: Some(Duration::from_secs(10)),
            pool_idle_timeout: Some(Duration::from_secs(90)),
            pool_max_idle_per_host: Some(32),
            tcp_nodelay: Some(true),
            tcp_keepalive: None,
            http1_only: false,
            gzip: true,
            brotli: true,
            deflate: true,
            trust_dns: false,
            https_only: true,
            retry_count: 3,
            retry_delay: Duration::from_millis(100),
        }
    }
}

impl ConfigurationBuilder {
    /// Create a new configuration builder
    pub fn new() -> Self {
        Self::default()
    }

    /// Set the base path for API requests
    pub fn base_path(mut self, base_path: impl Into<String>) -> Self {
        self.base_path = base_path.into();
        self
    }

    /// Set the user agent string
    pub fn user_agent(mut self, user_agent: impl Into<String>) -> Self {
        self.user_agent = Some(user_agent.into());
        self
    }

    /// Set basic authentication credentials
    pub fn basic_auth(mut self, public_key: impl Into<String>, secret_key: impl Into<String>) -> Self {
        self.basic_auth = Some((public_key.into(), Some(secret_key.into())));
        self
    }

    /// Set OAuth access token
    pub fn oauth_access_token(mut self, token: impl Into<String>) -> Self {
        self.oauth_access_token = Some(token.into());
        self
    }

    /// Set bearer access token
    pub fn bearer_access_token(mut self, token: impl Into<String>) -> Self {
        self.bearer_access_token = Some(token.into());
        self
    }

    /// Set API key
    pub fn api_key(mut self, key: impl Into<String>, prefix: Option<String>) -> Self {
        self.api_key = Some(ApiKey {
            key: key.into(),
            prefix,
        });
        self
    }

    // Transport knobs

    /// Set request timeout (default: 30s)
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = Some(timeout);
        self
    }

    /// Set connection timeout (default: 10s)
    pub fn connect_timeout(mut self, timeout: Duration) -> Self {
        self.connect_timeout = Some(timeout);
        self
    }

    /// Set pool idle timeout (default: 90s)
    pub fn pool_idle_timeout(mut self, timeout: Duration) -> Self {
        self.pool_idle_timeout = Some(timeout);
        self
    }

    /// Set maximum idle connections per host (default: 32)
    pub fn pool_max_idle_per_host(mut self, max: usize) -> Self {
        self.pool_max_idle_per_host = Some(max);
        self
    }

    /// Enable/disable TCP nodelay (default: true)
    pub fn tcp_nodelay(mut self, enabled: bool) -> Self {
        self.tcp_nodelay = Some(enabled);
        self
    }

    /// Set TCP keepalive interval
    pub fn tcp_keepalive(mut self, interval: Duration) -> Self {
        self.tcp_keepalive = Some(interval);
        self
    }

    /// Force HTTP/1 only (disable HTTP/2) (default: false)
    pub fn http1_only(mut self, enabled: bool) -> Self {
        self.http1_only = enabled;
        self
    }

    /// Enable/disable gzip decompression (default: true)
    pub fn gzip(mut self, enabled: bool) -> Self {
        self.gzip = enabled;
        self
    }

    /// Enable/disable brotli decompression (default: true)
    pub fn brotli(mut self, enabled: bool) -> Self {
        self.brotli = enabled;
        self
    }

    /// Enable/disable deflate decompression (default: true)
    pub fn deflate(mut self, enabled: bool) -> Self {
        self.deflate = enabled;
        self
    }

    /// Use trust-dns for DNS resolution (default: false)
    pub fn trust_dns(mut self, enabled: bool) -> Self {
        self.trust_dns = enabled;
        self
    }

    /// Only allow HTTPS connections (default: true)
    pub fn https_only(mut self, enabled: bool) -> Self {
        self.https_only = enabled;
        self
    }

    /// Set retry count for failed requests (default: 3)
    pub fn retry_count(mut self, count: usize) -> Self {
        self.retry_count = count;
        self
    }

    /// Set delay between retries (default: 100ms)
    pub fn retry_delay(mut self, delay: Duration) -> Self {
        self.retry_delay = delay;
        self
    }

    /// Build the Configuration
    pub fn build(self) -> Result<Configuration, String> {
        let mut client_builder = reqwest::Client::builder();

        // Apply timeouts
        if let Some(timeout) = self.timeout {
            client_builder = client_builder.timeout(timeout);
        }
        if let Some(timeout) = self.connect_timeout {
            client_builder = client_builder.connect_timeout(timeout);
        }

        // Apply pool settings
        if let Some(timeout) = self.pool_idle_timeout {
            client_builder = client_builder.pool_idle_timeout(Some(timeout));
        }
        if let Some(max) = self.pool_max_idle_per_host {
            client_builder = client_builder.pool_max_idle_per_host(max);
        }

        // Apply TCP settings
        if let Some(nodelay) = self.tcp_nodelay {
            client_builder = client_builder.tcp_nodelay(nodelay);
        }
        if let Some(interval) = self.tcp_keepalive {
            client_builder = client_builder.tcp_keepalive(Some(interval));
        }

        // Apply HTTP version settings
        if self.http1_only {
            client_builder = client_builder.http1_only();
        }

        // Apply compression settings
        client_builder = client_builder.gzip(self.gzip);
        client_builder = client_builder.brotli(self.brotli);
        client_builder = client_builder.deflate(self.deflate);

        // Apply DNS settings
        #[cfg(feature = "trust-dns")]
        if self.trust_dns {
            client_builder = client_builder.trust_dns(true);
        }

        // Apply HTTPS-only
        client_builder = client_builder.https_only(self.https_only);

        // Set user agent
        if let Some(ref user_agent) = self.user_agent {
            client_builder = client_builder.user_agent(user_agent);
        }

        // Build the client
        let client = client_builder
            .build()
            .map_err(|e| format!("Failed to build HTTP client: {}", e))?;

        Ok(Configuration {
            base_path: self.base_path,
            user_agent: self.user_agent,
            client,
            basic_auth: self.basic_auth,
            oauth_access_token: self.oauth_access_token,
            bearer_access_token: self.bearer_access_token,
            api_key: self.api_key,
        })
    }
}

/// Create a Configuration from environment variables
pub fn from_env() -> Result<Configuration, String> {
    let mut builder = ConfigurationBuilder::new();

    // Set base path from env
    if let Ok(host) = std::env::var("LANGFUSE_HOST") {
        builder = builder.base_path(host);
    }

    // Set auth from env
    if let (Ok(public_key), Ok(secret_key)) = (
        std::env::var("LANGFUSE_PUBLIC_KEY"),
        std::env::var("LANGFUSE_SECRET_KEY"),
    ) {
        builder = builder.basic_auth(public_key, secret_key);
    }

    // Optional timeout from env
    if let Ok(timeout_str) = std::env::var("LANGFUSE_TIMEOUT") {
        if let Ok(timeout_secs) = timeout_str.parse::<u64>() {
            builder = builder.timeout(Duration::from_secs(timeout_secs));
        }
    }

    // Optional connect timeout from env
    if let Ok(timeout_str) = std::env::var("LANGFUSE_CONNECT_TIMEOUT") {
        if let Ok(timeout_secs) = timeout_str.parse::<u64>() {
            builder = builder.connect_timeout(Duration::from_secs(timeout_secs));
        }
    }

    // Optional retry count from env
    if let Ok(retry_str) = std::env::var("LANGFUSE_RETRY_COUNT") {
        if let Ok(retry_count) = retry_str.parse::<usize>() {
            builder = builder.retry_count(retry_count);
        }
    }

    // Optional HTTP/1 only from env
    if let Ok(http1_only) = std::env::var("LANGFUSE_HTTP1_ONLY") {
        if http1_only.to_lowercase() == "true" || http1_only == "1" {
            builder = builder.http1_only(true);
        }
    }

    builder.build()
}