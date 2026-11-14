# Automation Context Guide

This file captures the background and workflow expectations for anyone (human teammates or coding agents) working on this project.

## Repository Context

This is the **langfuse-client-base** repository - an auto-generated OpenAPI client for Langfuse.

- **Generated Code**: All code in `src/` is auto-generated. Do not edit directly.
- **Ergonomic Wrapper**: For the high-level API, see [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic)

## Development Workflow

### Git Workflow
- **NEVER commit directly to main branch**
- Always create a feature branch first
- Create a pull request for review
- Example workflow:
  ```bash
  git checkout -b feat/your-feature-name
  # make changes
  git add -A
  git commit -m "feat: your commit message"
  git push origin feat/your-feature-name
  gh pr create --title "feat: your feature" --body "Description of changes"
  ```

### Pre-commit Checks
- **ALWAYS run pre-commit checks before committing**:
  ```bash
  cargo fmt --all -- --check
  cargo clippy --all-targets --all-features -- -D warnings
  cargo test --all
  ```
- If formatting issues are found, run `cargo fmt --all` to fix them

### Commit Messages
- Use conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation only
  - `chore:` for maintenance tasks
  - `test:` for test additions/changes

## Code Generation

### Regenerating the Client

To regenerate the client from the latest OpenAPI specification:

```bash
./scripts/generate-openapi-client.sh
```

**Important**: The generation script:
1. Downloads the latest OpenAPI spec (only with `UPDATE_SPEC=true`; otherwise it uses the checked-in `openapi.yml`)
2. Composes the legacy v3 interface into the generator input
3. Records a generation manifest
4. Generates the client with the `timvw-rust` generator image
5. Formats the generated code

See [guides/generation.md](guides/generation.md) for the details.

`Cargo.toml`, `README.md` and `.gitignore` are listed in `.openapi-generator-ignore`,
so the generator never writes them. Rust-specific fixes belong in the generator
(https://github.com/timvw/openapi-generator-timvw-rust), not in scripts.

### Handling Generated Code Issues

- Clippy warnings in generated code are suppressed via Cargo.toml:
  ```toml
  [lints.clippy]
  all = "allow"
  ```
- Formatting is automatically applied after generation
- The custom Cargo.toml is never overwritten (`.openapi-generator-ignore`)

## CI/CD

- GitHub Actions runs on every push and PR: build, clippy, tests (including the README doctests and the script
  tests), the public API check and the shared security workflow
- release-plz creates automated release PRs
- Packages are published to crates.io on release

## Important Notes

1. **Generated Code**: All code in `src/` is auto-generated. Don't edit it directly.
2. **Token Scopes**: crates.io tokens must have the pattern `langfuse-*` for publishing
3. **Documentation**: docs.rs builds documentation automatically after crates.io publish

## Repository Links
- GitHub: https://github.com/genai-rs/langfuse-client-base
- crates.io: https://crates.io/crates/langfuse-client-base
- docs.rs: https://docs.rs/langfuse-client-base
- Langfuse API docs: https://langfuse.com/docs/api
