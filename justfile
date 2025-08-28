# List available recipes
default:
    @just --list

# Install dependencies and setup environment
init:
    rustup update
    cargo --version
    @echo "Checking for openapi-generator-cli..."
    @which openapi-generator-cli > /dev/null || npm install -g @openapitools/openapi-generator-cli
    @echo "✅ Development environment ready!"

# Generate OpenAPI client
generate:
    ./scripts/generate-openapi-client.sh

# Build all crates
build:
    cargo build --all

# Run all tests
test:
    cargo test --all

# Run linting checks
lint:
    cargo clippy --all -- -D warnings

# Format code
fmt:
    cargo fmt --all

# Check code formatting without changing files
fmt-check:
    cargo fmt --all -- --check

# Run all checks (format, lint, test)
check: fmt-check lint test
    cargo check --all

# Run a specific example
run-example name:
    cargo run --example {{name}}

# Run the basic usage example
example-basic:
    cargo run --example basic_usage

# Run the LLM chain example
example-chain:
    cargo run --example llm_chain

# Clean build artifacts
clean:
    cargo clean
    rm -f scripts/openapi.yml

# Generate documentation
doc:
    cargo doc --all --no-deps --open

# Publish to crates.io (dry run)
publish-dry:
    cargo publish --dry-run -p langfuse-client-base
    cargo publish --dry-run -p langfuse-ergonomic

# Watch for changes and run checks
watch:
    cargo watch -x check -x test