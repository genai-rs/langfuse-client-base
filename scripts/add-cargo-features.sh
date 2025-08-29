#!/bin/bash
set -euo pipefail

# Script to add Cargo feature gates to generated API modules

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔧 Adding Cargo feature gates to API modules..."

# Note: This script adds feature gates to the generated code
# The API groupings are defined in Cargo.toml

# Update mod.rs to use feature gates
MOD_FILE="$PROJECT_ROOT/src/apis/mod.rs"
MOD_BACKUP="$PROJECT_ROOT/src/apis/mod.rs.backup"

# Backup the original mod.rs
cp "$MOD_FILE" "$MOD_BACKUP"

# Create a new mod.rs with feature gates
cat > "$MOD_FILE" << 'EOF'
use std::error;
use std::fmt;

#[derive(Debug, Clone)]
pub struct ResponseContent<T> {
    pub status: reqwest::StatusCode,
    pub content: String,
    pub entity: Option<T>,
}

#[derive(Debug)]
pub enum Error<T> {
    Reqwest(reqwest::Error),
    Serde(serde_json::Error),
    Io(std::io::Error),
    ResponseError(ResponseContent<T>),
}

impl<T> fmt::Display for Error<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let (module, e) = match self {
            Error::Reqwest(e) => ("reqwest", e.to_string()),
            Error::Serde(e) => ("serde", e.to_string()),
            Error::Io(e) => ("IO", e.to_string()),
            Error::ResponseError(e) => ("response", format!("status code {}", e.status)),
        };
        write!(f, "error in {}: {}", module, e)
    }
}

impl<T: fmt::Debug> error::Error for Error<T> {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        Some(match self {
            Error::Reqwest(e) => e,
            Error::Serde(e) => e,
            Error::Io(e) => e,
            Error::ResponseError(_) => return None,
        })
    }
}

impl<T> From<reqwest::Error> for Error<T> {
    fn from(e: reqwest::Error) -> Self {
        Error::Reqwest(e)
    }
}

impl<T> From<serde_json::Error> for Error<T> {
    fn from(e: serde_json::Error) -> Self {
        Error::Serde(e)
    }
}

impl<T> From<std::io::Error> for Error<T> {
    fn from(e: std::io::Error) -> Self {
        Error::Io(e)
    }
}

pub fn urlencode<T: AsRef<str>>(s: T) -> String {
    ::url::form_urlencoded::byte_serialize(s.as_ref().as_bytes()).collect()
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

    unimplemented!("Only objects are supported with style=deepObject")
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
            return Self::Json;
        } else if content_type.starts_with("text/plain") {
            return Self::Text;
        } else {
            return Self::Unsupported(content_type.to_string());
        }
    }
}

// API modules with feature gates

#[cfg(feature = "ingestion")]
pub mod ingestion_api;

#[cfg(feature = "tracing")]
pub mod trace_api;
#[cfg(feature = "tracing")]
pub mod sessions_api;
#[cfg(feature = "tracing")]
pub mod observations_api;

#[cfg(feature = "scoring")]
pub mod score_api;
#[cfg(feature = "scoring")]
pub mod score_configs_api;
#[cfg(feature = "scoring")]
pub mod score_v2_api;

#[cfg(feature = "datasets")]
pub mod datasets_api;
#[cfg(feature = "datasets")]
pub mod dataset_items_api;
#[cfg(feature = "datasets")]
pub mod dataset_run_items_api;

#[cfg(feature = "prompts")]
pub mod prompts_api;
#[cfg(feature = "prompts")]
pub mod prompt_version_api;

#[cfg(feature = "metrics")]
pub mod metrics_api;

#[cfg(feature = "models")]
pub mod models_api;
#[cfg(feature = "models")]
pub mod llm_connections_api;

#[cfg(feature = "projects")]
pub mod projects_api;
#[cfg(feature = "projects")]
pub mod organizations_api;

#[cfg(feature = "comments")]
pub mod comments_api;
#[cfg(feature = "comments")]
pub mod annotation_queues_api;

#[cfg(feature = "media")]
pub mod media_api;

#[cfg(feature = "admin")]
pub mod scim_api;

#[cfg(feature = "health")]
pub mod health_api;

// Configuration is always available
pub mod configuration;
EOF

echo "✅ Added feature gates to mod.rs"

# Now update the generate script to call this after generation
GENERATE_SCRIPT="$PROJECT_ROOT/scripts/generate-openapi-client.sh"
if ! grep -q "add-cargo-features.sh" "$GENERATE_SCRIPT"; then
    # Add call to this script after code formatting
    sed -i.bak '/cargo fmt --all/a\
\
# Add Cargo feature gates\
echo "🎨 Adding Cargo feature gates..."\
"$SCRIPT_DIR/add-cargo-features.sh"' "$GENERATE_SCRIPT"
    rm -f "$GENERATE_SCRIPT.bak"
    echo "✅ Updated generate-openapi-client.sh to add features"
fi

echo "✅ Cargo features script complete!"