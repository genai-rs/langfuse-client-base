#![allow(deprecated)]
use std::error;
use std::fmt;

/// Extra headers and query parameters for one call: `.options(&options)` on an operation's builder.
pub use timvw_rust_runtime::RequestOptions;

#[derive(Debug, Clone)]
pub struct ResponseContent<T> {
    pub status: timvw_rust_runtime::StatusCode,
    pub content: String,
    pub entity: Option<T>,
    /// The response's headers (`retry-after`, `x-request-id`, rate limits, ...).
    pub headers: timvw_rust_runtime::header::HeaderMap,
}

#[derive(Debug)]
pub enum Error<T> {
    /// Building the request, sending it through the client's service, or reading the response body failed.
    Http(timvw_rust_runtime::Error),
    Serde(serde_json::Error),
    ResponseError(Box<ResponseContent<T>>),
}

impl<T> fmt::Display for Error<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (module, e) = match self {
            Error::Http(e) => ("http", e.to_string()),
            Error::Serde(e) => ("serde", e.to_string()),
            Error::ResponseError(e) => ("response", format!("status code {}", e.status)),
        };
        write!(f, "error in {}: {}", module, e)
    }
}

impl<T: fmt::Debug> error::Error for Error<T> {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        Some(match self {
            Error::Http(e) => e,
            Error::Serde(e) => e,
            Error::ResponseError(_) => return None,
        })
    }
}

impl<T> From<timvw_rust_runtime::Error> for Error<T> {
    fn from(e: timvw_rust_runtime::Error) -> Self {
        Error::Http(e)
    }
}

impl<T> From<serde_json::Error> for Error<T> {
    fn from(e: serde_json::Error) -> Self {
        Error::Serde(e)
    }
}

/// Percent-encodes a path segment: a space is `%20` (form encoding's `+` would be a literal plus in a path).
pub fn urlencode<T: AsRef<str>>(s: T) -> String {
    ::url::form_urlencoded::byte_serialize(s.as_ref().as_bytes())
        .collect::<String>()
        .replace('+', "%20")
}

pub fn parse_deep_object(prefix: &str, value: &serde_json::Value) -> Vec<(String, String)> {
    if let serde_json::Value::Object(object) = value {
        let mut params = vec![];

        for (key, value) in object {
            match value {
                serde_json::Value::Object(_) => params.append(&mut parse_deep_object(
                    &format!("{}[{}]", prefix, key),
                    value,
                )),
                serde_json::Value::Array(array) => {
                    for (i, value) in array.iter().enumerate() {
                        params.append(&mut parse_deep_object(
                            &format!("{}[{}][{}]", prefix, key, i),
                            value,
                        ));
                    }
                }
                serde_json::Value::String(s) => {
                    params.push((format!("{}[{}]", prefix, key), s.clone()))
                }
                _ => params.push((format!("{}[{}]", prefix, key), value.to_string())),
            }
        }

        return params;
    }

    // Non-object values (e.g. array items) are emitted as a plain key/value pair.
    let value = match value {
        serde_json::Value::String(s) => s.clone(),
        _ => value.to_string(),
    };
    vec![(prefix.to_string(), value)]
}

/// Internal use only
/// A content type supported by this client.
#[allow(dead_code)]
enum ContentType {
    Json,
    Text,
    Unsupported(String),
}

impl From<&str> for ContentType {
    fn from(content_type: &str) -> Self {
        if content_type.starts_with("application") && content_type.contains("json") {
            Self::Json
        } else if content_type.starts_with("text/plain") {
            Self::Text
        } else {
            Self::Unsupported(content_type.to_string())
        }
    }
}

pub mod annotation_queues_api;
pub mod blob_storage_integrations_api;
pub mod comments_api;
pub mod dataset_items_api;
pub mod dataset_run_items_api;
pub mod datasets_api;
pub mod evaluation_rules_api;
pub mod evaluators_api;
pub mod experiments_api;
pub mod feedback_api;
pub mod health_api;
pub mod ingestion_api;
pub mod legacy_metrics_v1_api;
pub mod legacy_observations_v1_api;
pub mod legacy_score_v1_api;
pub mod llm_connections_api;
pub mod media_api;
pub mod metrics_api;
pub mod models_api;
pub mod observations_api;
pub mod opentelemetry_api;
pub mod organizations_api;
pub mod projects_api;
pub mod prompt_version_api;
pub mod prompts_api;
pub mod scim_api;
pub mod score_configs_api;
pub mod scores_api;
pub mod scores_v3_api;
pub mod sessions_api;
pub mod skills_api;
pub mod trace_api;
pub mod unstable_dashboard_widgets_api;
pub mod unstable_dashboards_api;
pub mod unstable_topics_api;

pub mod configuration;
