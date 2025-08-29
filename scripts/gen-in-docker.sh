#!/bin/bash
set -euo pipefail

# Generate OpenAPI client using official Docker image for reproducible builds

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Use the official OpenAPI Generator image with pinned version
OPENAPI_GENERATOR_VERSION="7.10.0"
OPENAPI_IMAGE="openapitools/openapi-generator-cli:v${OPENAPI_GENERATOR_VERSION}"

echo "🐳 Using official OpenAPI Generator Docker image: ${OPENAPI_IMAGE}"

# Ensure openapi.yml exists
if [ ! -f "$PROJECT_ROOT/openapi.yml" ]; then
    echo "❌ openapi.yml not found. Run with UPDATE_SPEC=true to download it first."
    exit 1
fi

echo "🔧 Generating Rust client in Docker container..."
docker run --rm \
    -v "$PROJECT_ROOT:/local" \
    -u "$(id -u):$(id -g)" \
    "$OPENAPI_IMAGE" generate \
    -i /local/openapi.yml \
    -g rust \
    -o /local \
    --additional-properties=packageName=langfuse-client-base \
    --additional-properties=packageVersion=0.2.3 \
    --additional-properties=library=reqwest \
    --additional-properties=supportAsync=true \
    --additional-properties=preferUnsignedInt=false \
    --additional-properties=useSingleRequestParameter=false

echo "🧹 Cleaning up generated files..."
rm -f "$PROJECT_ROOT/.travis.yml"
rm -f "$PROJECT_ROOT/git_push.sh"
rm -rf "$PROJECT_ROOT/.openapi-generator"

echo "🎨 Formatting generated code..."
cd "$PROJECT_ROOT"
cargo fmt --all

echo "✅ Docker-based generation complete!"