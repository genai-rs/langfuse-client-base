#!/bin/bash
set -euo pipefail

# Script to generate the Langfuse client from OpenAPI specification

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BASE_CLIENT_DIR="$PROJECT_ROOT"
OPENAPI_URL="https://cloud.langfuse.com/generated/api/openapi.yml"
OPENAPI_FILE="$SCRIPT_DIR/openapi.yml"

echo "🔧 Generating Langfuse client from OpenAPI specification..."

# Check if openapi-generator-cli is installed
if ! command -v openapi-generator-cli &> /dev/null; then
    echo "❌ openapi-generator-cli is not installed."
    echo "Installing via npm..."
    npm install -g @openapitools/openapi-generator-cli
fi

# Download the latest OpenAPI specification
echo "📥 Downloading OpenAPI specification..."
curl -o "$OPENAPI_FILE" "$OPENAPI_URL"

# Backup our custom files before generation
echo "📝 Backing up custom files..."
cp "$BASE_CLIENT_DIR/Cargo.toml" "$BASE_CLIENT_DIR/Cargo.toml.custom" 2>/dev/null || true
cp "$BASE_CLIENT_DIR/.gitignore" "$BASE_CLIENT_DIR/.gitignore.custom" 2>/dev/null || true
cp "$BASE_CLIENT_DIR/README.md" "$BASE_CLIENT_DIR/README.md.custom" 2>/dev/null || true

# Generate the client
echo "🏗️ Generating Rust client..."
openapi-generator-cli generate \
    -i "$OPENAPI_FILE" \
    -g rust \
    -o "$BASE_CLIENT_DIR" \
    --additional-properties=packageName=langfuse-client-base \
    --additional-properties=packageVersion=0.1.0 \
    --additional-properties=library=reqwest \
    --additional-properties=supportAsync=true \
    --additional-properties=preferUnsignedInt=false \
    --additional-properties=useSingleRequestParameter=false

# Clean up generated files we don't need
echo "🧹 Cleaning up generated files..."
rm -f "$BASE_CLIENT_DIR/.travis.yml"
rm -f "$BASE_CLIENT_DIR/.gitignore"
rm -f "$BASE_CLIENT_DIR/git_push.sh"
rm -rf "$BASE_CLIENT_DIR/.openapi-generator"

# Restore our custom files
echo "📝 Restoring custom files..."
if [ -f "$BASE_CLIENT_DIR/Cargo.toml.custom" ]; then
    mv "$BASE_CLIENT_DIR/Cargo.toml.custom" "$BASE_CLIENT_DIR/Cargo.toml"
fi
if [ -f "$BASE_CLIENT_DIR/.gitignore.custom" ]; then
    mv "$BASE_CLIENT_DIR/.gitignore.custom" "$BASE_CLIENT_DIR/.gitignore"
fi
if [ -f "$BASE_CLIENT_DIR/README.md.custom" ]; then
    mv "$BASE_CLIENT_DIR/README.md.custom" "$BASE_CLIENT_DIR/README.md"
fi

# Format the generated code
echo "🎨 Formatting generated code..."
cd "$PROJECT_ROOT"
cargo fmt --all

echo "✅ Client generation complete!"
echo ""
echo "Note: The generated client is in $BASE_CLIENT_DIR"
echo "      The code has been automatically formatted with cargo fmt."