#!/bin/bash
set -euo pipefail

# Script to generate the Langfuse client from OpenAPI specification

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BASE_CLIENT_DIR="$PROJECT_ROOT"
OPENAPI_URL="https://cloud.langfuse.com/generated/api/openapi.yml"
OPENAPI_FILE="$PROJECT_ROOT/openapi.yml"

# Environment variables
UPDATE_SPEC="${UPDATE_SPEC:-false}"
# Keep in sync with openapitools.json. You can override via env.
OPENAPI_GENERATOR_VERSION="${OPENAPI_GENERATOR_VERSION:-7.17.0}"

echo "🔧 Generating Langfuse client from OpenAPI specification..."

# Always use Docker for reproducible generation
echo "🐳 Using Docker for generation (OpenAPI Generator v${OPENAPI_GENERATOR_VERSION})"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

GENERATOR_CMD="docker run --rm -v $PROJECT_ROOT:/local -u $(id -u):$(id -g) openapitools/openapi-generator-cli:v${OPENAPI_GENERATOR_VERSION}"

# Download or use local OpenAPI specification
if [ "$UPDATE_SPEC" = "true" ]; then
    echo "📥 Downloading latest OpenAPI specification..."
    curl -o "$OPENAPI_FILE.new" "$OPENAPI_URL"
    
    # Check if spec has changed
    if [ -f "$OPENAPI_FILE" ]; then
        if diff -q "$OPENAPI_FILE" "$OPENAPI_FILE.new" > /dev/null; then
            echo "✅ OpenAPI spec unchanged, no update needed"
            rm "$OPENAPI_FILE.new"
            exit 0
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

# Backup our custom files before generation
echo "📝 Backing up custom files..."
cp "$BASE_CLIENT_DIR/Cargo.toml" "$BASE_CLIENT_DIR/Cargo.toml.original" 2>/dev/null || true
cp "$BASE_CLIENT_DIR/.gitignore" "$BASE_CLIENT_DIR/.gitignore.custom" 2>/dev/null || true
cp "$BASE_CLIENT_DIR/README.md" "$BASE_CLIENT_DIR/README.md.custom" 2>/dev/null || true

# Generate the client
echo "🏗️ Generating Rust client..."

# Run the generator (Docker paths)
$GENERATOR_CMD generate \
    -i "/local/openapi.yml" \
    -g rust \
    -o "/local" \
    --additional-properties=packageName=langfuse-client-base \
    --additional-properties=packageVersion=0.1.0 \
    --additional-properties=library=reqwest \
    --additional-properties=supportAsync=true \
    --additional-properties=supportMiddleware=true \
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
if [ -f "$BASE_CLIENT_DIR/.gitignore.custom" ]; then
    mv "$BASE_CLIENT_DIR/.gitignore.custom" "$BASE_CLIENT_DIR/.gitignore"
fi
if [ -f "$BASE_CLIENT_DIR/README.md.custom" ]; then
    mv "$BASE_CLIENT_DIR/README.md.custom" "$BASE_CLIENT_DIR/README.md"
fi

# Merge Cargo.toml without letting the generator overwrite curated dependency versions
echo "📝 Merging Cargo.toml changes..."
if [ -f "$BASE_CLIENT_DIR/Cargo.toml.original" ]; then
    mv "$BASE_CLIENT_DIR/Cargo.toml" "$BASE_CLIENT_DIR/Cargo.toml.generated"
    mv "$BASE_CLIENT_DIR/Cargo.toml.original" "$BASE_CLIENT_DIR/Cargo.toml"

    python3 "$SCRIPT_DIR/merge_cargo_dependencies.py" \
        "$BASE_CLIENT_DIR/Cargo.toml" \
        "$BASE_CLIENT_DIR/Cargo.toml.generated"

    rm -f "$BASE_CLIENT_DIR/Cargo.toml.generated"
fi

# Remove any leftover backups if they still exist
rm -f "$BASE_CLIENT_DIR/.gitignore.custom" \
      "$BASE_CLIENT_DIR/README.md.custom" \
      "$BASE_CLIENT_DIR/Cargo.toml.original"

# Apply post-generation patches
echo "🔧 Applying post-generation patches..."
bash "$SCRIPT_DIR/patch_generated.rs.sh" "$BASE_CLIENT_DIR"

# Inject crate-level docs from README into lib.rs for docs.rs discoverability
echo "📚 Injecting crate-level docs into src/lib.rs..."
if [ -f "$BASE_CLIENT_DIR/src/lib.rs" ]; then
    # Only inject if not already present
    if ! grep -q "#!\[doc = include_str!\(\"../README.md\"\)\]" "$BASE_CLIENT_DIR/src/lib.rs"; then
        tmpfile=$(mktemp)
        {
            echo "#![doc = include_str!(\"../README.md\")]";
            echo;
            cat "$BASE_CLIENT_DIR/src/lib.rs";
        } > "$tmpfile"
        mv "$tmpfile" "$BASE_CLIENT_DIR/src/lib.rs"
    fi
fi

# Format all code including examples
echo "🎨 Formatting all code (src, tests, examples)..."
cd "$PROJECT_ROOT"
cargo fmt --all

echo "✅ Client generation complete!"
echo ""
echo "Note: The generated client is in $BASE_CLIENT_DIR"
echo "      The code has been automatically formatted with cargo fmt."
