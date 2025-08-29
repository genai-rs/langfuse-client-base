#!/bin/bash
set -euo pipefail

# Generate OpenAPI client using Docker for reproducible builds

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🐳 Building codegen Docker image..."
docker build -f "$PROJECT_ROOT/docker/Dockerfile.codegen" -t langfuse-codegen "$PROJECT_ROOT"

echo "🔧 Generating client in Docker container..."
docker run --rm \
    -v "$PROJECT_ROOT:/workspace" \
    -u "$(id -u):$(id -g)" \
    -e UPDATE_SPEC="${UPDATE_SPEC:-false}" \
    langfuse-codegen

echo "✅ Docker-based generation complete!"