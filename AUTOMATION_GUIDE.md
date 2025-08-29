# Instructions for***REMOVED***

This file contains important instructions and context for***REMOVED*** when working on this project.

## Repository Context

This is the **langfuse-client-base** repository - an auto-generated OpenAPI client for Langfuse.

- **Generated Code**: All code in `src/` is auto-generated. Do not edit directly.
- **Ergonomic Wrapper**: For the high-level API, see [langfuse-ergonomic](https://github.com/genai-rs/langfuse-ergonomic)

## Recent Migration (2025-08-29)

This repository was migrated from the monorepo at timvw/langfuse-rs to a standalone repository in the genai-rs organization. Key changes:

1. **Simplified Configuration**: Removed workspace configuration - this is now a single-package repository
2. **Minimal CI**: Reduced to just build verification and security audit (no tests for generated code)
3. **Simplified Docs**: CONTRIBUTING.md reduced to 26 lines focusing on generation only
4. **Simplified Renovate**: Basic dependency updates only (39 lines instead of 215)
5. **Version**: Successfully released v0.1.1 via release-plz

### Known Issues Fixed
- release-plz.toml no longer uses [workspace] configuration
- All clippy warnings are suppressed for generated code
- Repository is still technically a fork but has full permissions via organization settings

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
1. Downloads the latest OpenAPI spec
2. Backs up the custom Cargo.toml
3. Generates the client
4. Restores the custom Cargo.toml
5. Formats the generated code

### Handling Generated Code Issues

- Clippy warnings in generated code are suppressed via Cargo.toml:
  ```toml
  [lints.clippy]
  all = "allow"
  ```
- Formatting is automatically applied after generation
- The custom Cargo.toml is preserved across regenerations

## CI/CD

- GitHub Actions runs on every push and PR
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