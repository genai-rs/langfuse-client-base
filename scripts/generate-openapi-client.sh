#!/bin/bash
set -euo pipefail

# Script to generate the Langfuse client from OpenAPI specification

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BASE_CLIENT_DIR="$PROJECT_ROOT"
OPENAPI_URL="https://cloud.langfuse.com/generated/api/openapi.yml"
OPENAPI_FILE="$PROJECT_ROOT/openapi.yml"
COMPATIBLE_OPENAPI_FILE="$PROJECT_ROOT/.openapi-generator/compatible.json"
GENERATION_MANIFEST="$PROJECT_ROOT/.openapi-generator/generation-manifest.json"
COMPATIBILITY_FILE="$SCRIPT_DIR/legacy_v3_compatibility.json"

# Environment variables
UPDATE_SPEC="${UPDATE_SPEC:-false}"
# Keep in sync with openapitools.json. You can override via env.
OPENAPI_GENERATOR_VERSION="${OPENAPI_GENERATOR_VERSION:-7.26.0}"
# Custom generator (timvw-rust extends the stock rust generator; see
# https://github.com/timvw/openapi-generator-timvw-rust). Every Rust-specific
# fix lives in the generator: this script only prepares the spec and formats
# the output. The image tag names the generator version and the
# openapi-generator version it bundles. Override the image for local builds of
# the generator, e.g. GENERATOR_IMAGE=timvw-rust:0.2.0-og7.25.0.
TIMVW_RUST_VERSION="${TIMVW_RUST_VERSION:-0.2.0}"
GENERATOR_IMAGE="${GENERATOR_IMAGE:-ghcr.io/timvw/openapi-generator-timvw-rust:${TIMVW_RUST_VERSION}-og${OPENAPI_GENERATOR_VERSION}}"
GENERATOR_NAME="${GENERATOR_NAME:-timvw-rust}"
UPSTREAM_REVISION="${UPSTREAM_REVISION:-}"

echo "🔧 Generating Langfuse client from OpenAPI specification..."

# Always use Docker for reproducible generation
echo "🐳 Using Docker for generation ($GENERATOR_IMAGE, generator $GENERATOR_NAME, OpenAPI Generator v${OPENAPI_GENERATOR_VERSION})"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

GENERATOR_CMD="docker run --rm -v $PROJECT_ROOT:/local -u $(id -u):$(id -g) $GENERATOR_IMAGE"

# Download or use local OpenAPI specification
if [ "$UPDATE_SPEC" = "true" ]; then
    echo "📥 Downloading latest OpenAPI specification..."
    curl -o "$OPENAPI_FILE.new" "$OPENAPI_URL"

    # Check if spec has changed
    if [ -f "$OPENAPI_FILE" ]; then
        if diff -q "$OPENAPI_FILE" "$OPENAPI_FILE.new" > /dev/null; then
            echo "✅ OpenAPI spec unchanged; regenerating with current compatibility rules"
            rm "$OPENAPI_FILE.new"
        else
            echo "📝 OpenAPI spec has changed, updating..."
            mv "$OPENAPI_FILE.new" "$OPENAPI_FILE"
        fi
    else
        mv "$OPENAPI_FILE.new" "$OPENAPI_FILE"
    fi
else
    if [ ! -f "$OPENAPI_FILE" ]; then
        echo "❌ Local OpenAPI spec not found at $OPENAPI_FILE"
        echo "   Run with UPDATE_SPEC=true to download it"
        exit 1
    fi
    echo "📝 Using local OpenAPI specification from $OPENAPI_FILE"
fi

# Keep openapi.yml as the untouched upstream snapshot. Compose the published v3
# interface into a separate generator input so nightly downloads cannot erase
# it, and drop the 3.1-only `const` keyword the 3.0 validation rejects. The
# spec is otherwise passed to the generator as upstream publishes it: any other
# invalid construct fails generation (spec validation) and is fixed upstream.
echo "🧪 Composing the generator input..."
mkdir -p "$(dirname "$COMPATIBLE_OPENAPI_FILE")"
python3 "$SCRIPT_DIR/prepare_compatible_spec.py" "$OPENAPI_FILE" \
    "$COMPATIBLE_OPENAPI_FILE"

# Record only reviewed, non-secret generation inputs. The helper uses a fixed
# field set and validates optional revisions before writing the artifact.
python3 "$SCRIPT_DIR/generation_manifest.py" \
    --upstream-url "$OPENAPI_URL" \
    --upstream-revision "$UPSTREAM_REVISION" \
    --project-root "$PROJECT_ROOT" \
    --raw-spec "$OPENAPI_FILE" \
    --composed-spec "$COMPATIBLE_OPENAPI_FILE" \
    --compatibility-file "$COMPATIBILITY_FILE" \
    --generator-image "$GENERATOR_IMAGE" \
    --output "$GENERATION_MANIFEST"

# Generate the client. Hand-maintained files (Cargo.toml, README.md,
# .gitignore) and unwanted supporting files are listed in
# .openapi-generator-ignore, which the generator honours.
echo "🏗️ Generating Rust client..."

# Run the generator (Docker paths)
$GENERATOR_CMD generate \
    -i "/local/.openapi-generator/compatible.json" \
    -g "$GENERATOR_NAME" \
    -o "/local" \
    --additional-properties=packageName=langfuse-client-base \
    --additional-properties=packageVersion=0.1.0 \
    --additional-properties=library=reqwest \
    --additional-properties=supportAsync=true \
    --additional-properties=supportMiddleware=true \
    --additional-properties=preferUnsignedInt=false \
    --additional-properties=useSingleRequestParameter=false

# Drop OpenAPI Generator's transient metadata while keeping the provenance
# manifest available for CI artifact upload and local review.
echo "🧹 Cleaning up generated files..."
find "$BASE_CLIENT_DIR/.openapi-generator" -mindepth 1 -maxdepth 1 \
    ! -name "$(basename "$GENERATION_MANIFEST")" -exec rm -rf {} +

# Format all code including examples
echo "🎨 Formatting all code (src, tests, examples)..."
cd "$PROJECT_ROOT"
cargo fmt --all

echo "✅ Client generation complete!"
echo ""
echo "Note: The generated client is in $BASE_CLIENT_DIR"
echo "      The code has been automatically formatted with cargo fmt."
