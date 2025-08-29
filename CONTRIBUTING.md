# Contributing to langfuse-client-base

Thank you for your interest in contributing to langfuse-client-base! This guide will help you get started.

**Note**: This repository contains auto-generated code. Most contributions should be made to the generation process or to the [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic) repository.

## Development Setup

### Prerequisites

- Rust 1.75 or later
- Node.js 18+ (for OpenAPI generator)
- Java 11+ (for OpenAPI generator v7.x)

### Getting Started

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/langfuse-client-base.git
cd langfuse-client-base
```

2. Verify dependencies:
```bash
cargo build
cargo test
```

## Development Workflow

### Making Changes

**Important**: The code in `src/` is auto-generated. Changes should be made to:
- The generation script (`scripts/generate-openapi-client.sh`)
- The custom Cargo.toml configuration
- Documentation files

1. **Create a feature branch:**
```bash
git checkout -b feat/your-feature-name
# or: fix/your-bug-fix
# or: docs/your-docs-change
```

2. **Make your changes**
   - Update generation scripts if needed
   - Update documentation
   - Test the generation process

3. **Run pre-commit checks:**
```bash
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all
```

4. **Commit your changes:**
```bash
git add -A
git commit -m "feat: your descriptive commit message"
```

Use [conventional commits](https://www.conventionalcommits.org/):
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `chore:` for maintenance tasks
- `test:` for test changes
- `refactor:` for code refactoring

5. **Push and create a PR:**
```bash
git push origin feat/your-feature-name
gh pr create  # or use GitHub web UI
```

## Code Guidelines

### Rust Code

- Follow Rust naming conventions
- Use `cargo fmt` for formatting
- Fix all `cargo clippy` warnings
- Write idiomatic Rust code
- Add documentation comments for public APIs

### Generated Code

This crate contains auto-generated code from the OpenAPI specification. 

**DO NOT** edit files in `src/` directly. Instead:

1. Update the OpenAPI generation script if needed
2. Regenerate the client:
```bash
./scripts/generate-openapi-client.sh
```

### Testing

Ensure all tests pass:

```bash
cargo test --all-features
```

## Pull Request Process

1. **Ensure CI passes:** All GitHub Actions checks must pass
2. **Update documentation:** Include any necessary documentation updates
3. **Add tests:** New features should include tests
4. **Update CHANGELOG:** Note your changes if they're user-facing
5. **Request review:** Tag maintainers for review

## Project Structure

```
langfuse-client-base/
├── src/                    # Auto-generated code (do not edit)
├── docs/                   # Generated API documentation
├── scripts/                # Generation scripts
├── Cargo.toml             # Custom package configuration
└── .github/workflows/      # CI/CD configuration
```

## Release Process

Releases are automated using [release-plz](https://release-plz.ieni.dev/):

1. Merge changes to `main`
2. release-plz creates a release PR automatically
3. Review and merge the release PR
4. Packages are published to crates.io automatically

## Getting Help

- Open an [issue](https://github.com/genai-rs/langfuse-client-base/issues) for bugs or feature requests
- Check existing issues before creating a new one
- For ergonomic API contributions, see [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic)
- Join the [Langfuse community](https://langfuse.com/docs/community) for general questions

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project (MIT OR Apache-2.0).