# Code Generation Guide

This repository contains auto-generated Rust client code from the Langfuse OpenAPI specification.

## Prerequisites

- **Docker** (required for generation)
- **Python 3** (for TOML processing)

## Quick Generation

```bash
# Generate client (uses Docker for reproducible builds)
./scripts/generate-openapi-client.sh

# Update OpenAPI spec and generate
UPDATE_SPEC=true ./scripts/generate-openapi-client.sh
```

## Pinned Versions

- **OpenAPI Generator Docker**: `7.10.0` (official Docker image)
- **OpenAPI Spec Source**: `https://cloud.langfuse.com/generated/api/openapi.yml`
- **Target Rust Version**: `1.82.0` (MSRV)

## Generation Process

1. **Download/Validate OpenAPI spec** from Langfuse
2. **Backup custom files** (Cargo.toml, README.md, .gitignore)
3. **Generate Rust client** using openapi-generator-cli
4. **Clean up** generated artifacts we don't need
5. **Restore custom files** and merge dependencies
6. **Format code** with `cargo fmt`

## Docker-based Generation

All generation uses the official OpenAPI Generator Docker image for reproducible builds:

```bash
# The script automatically uses Docker
./scripts/generate-openapi-client.sh

# Or run Docker directly:
docker run --rm \
    -v "$(pwd):/local" \
    openapitools/openapi-generator-cli:v7.10.0 generate \
    -i /local/openapi.yml \
    -g rust \
    -o /local \
    --additional-properties=packageName=langfuse-client-base
```

## Debugging Generation Issues

```bash
# Manual generation with debug using Docker
docker run --rm \
    -v "$(pwd):/local" \
    openapitools/openapi-generator-cli:v7.10.0 generate \
    -i /local/openapi.yml \
    -g rust \
    -o /tmp/debug-output \
    --additional-properties=packageName=langfuse-client-base
```

## Custom Files (Never Edit Generated Code)

**Preserved across generation:**
- `Cargo.toml` (metadata + custom features, dependencies merged)
- `README.md` 
- `.gitignore`
- `.github/` directory
- `scripts/` directory

**Generated (DO NOT EDIT):**
- `src/` - All Rust source code
- `docs/` - API documentation

## Troubleshooting

**"Python script failed":**
- Check Python 3 is available: `python3 --version`
- Install required modules: `pip3 install toml`

**Docker generation fails:**
- Ensure Docker is running: `docker --version`
- Pull the image manually: `docker pull openapitools/openapi-generator-cli:v7.10.0`
- Check file permissions on openapi.yml