# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2025-01-29

### Changed
- Upgraded MSRV from 1.75.0 to 1.82.0
- Upgraded reqwest from 0.11 to 0.12
- Enabled changelog generation in release-plz

### Added
- Basic usage example demonstrating environment variable configuration
- CODEOWNERS file for repository governance
- Security audit job in CI workflow
- Cargo.lock generation in CI for security audits
- MSRV badge in README

### Fixed
- CI workflow to generate Cargo.lock for security audit

### Documentation
- Improved README with environment variable configuration examples
- Added self-hosted instance configuration example

## [0.1.1] - 2025-01-28

### Changed
- Repository detached from upstream fork
- Simplified repository structure for auto-generated code only

### Added
- Automated nightly OpenAPI client generation workflow
- GitHub Actions CI with multi-version testing (stable, beta, MSRV)
- release-plz integration for automated releases

### Fixed
- release-plz.toml configuration structure

## [0.1.0] - 2025-01-28

### Added
- Initial release of auto-generated Langfuse OpenAPI client
- Complete API coverage from OpenAPI specification
- Async/await support with Tokio
- Choice of TLS backend (rustls or native-tls)
- Strong typing with serde

[Unreleased]: https://github.com/genai-rs/langfuse-client-base/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/genai-rs/langfuse-client-base/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/genai-rs/langfuse-client-base/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/genai-rs/langfuse-client-base/releases/tag/v0.1.0