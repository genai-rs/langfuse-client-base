# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0](https://github.com/genai-rs/langfuse-client-base/compare/v0.3.0...v0.4.0) - 2025-10-02

### Added

- add bon builder post processing

### Other

- *(deps)* Update openapitools/openapi-generator-cli Docker tag to v7.16.0
- remove decorative emoji from README
- *(deps)* migrate config renovate.json5
- *(deps)* Update mozilla-actions/sccache-action action to v0.0.9
- *(deps)* Update github-actions
- align renovate config with library defaults
- replace***REMOVED*** with ***REMOVED***

## [0.3.0](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.7...v0.3.0) - 2025-09-19

### Other

- update generated client from latest OpenAPI spec
- update generated client from latest OpenAPI spec
- align workflows with openai-client-base

## [0.2.7](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.6...v0.2.7) - 2025-09-12

### Added

- reorganize GitHub workflows by tool

### Fixed

- fix doc test failures in README examples
- update branch protection rules for new job names

### Other

- temporarily allow force pushes to rewrite author metadata
- fix duplicate 'script' key in generate-client workflow
- enforce App-only auth in generate-client and release-plz; remove PAT fallback
- update required checks to consolidated names
- inline reusable workflows into CI/Dependencies/Security and remove -common files
- consolidate automated and regular CI; run audit in main CI; remove automated-only workflows
- update generated client from latest OpenAPI spec
- robust App/PAT selection without GITHUB_TOKEN; avoid secret refs in if; continue-on-error for app token step
- remove GITHUB_TOKEN fallback to ensure PR events trigger via App/PAT only
- use GitHub App token with fallback; ensure PR events trigger checks
- *(generate)* remove unsupported update-branch input; update PR branch via pulls.updateBranch API
- *(generate)* always run create-pull-request with base=main + update-branch=true; remove update-automated-prs workflow
- update automated PR branches using pulls.updateBranch instead of merge-branch action
- auto-update automated/* PR branches from main on PR events and push
- *(security)* remove reserved GITHUB_TOKEN from reusable workflow_call; use github.token in cargo-audit
- use github.head_ref in skip conditions to avoid push-event context errors
- fix push-event condition by coalescing missing pull_request fields in if expressions
- *(pre-commit)* drop trufflehog args; use upstream hook defaults
- *(renovate)* use branchPrefix automated/renovate/ and add 'automated' label for CI routing
- adopt automated/* + automated label routing; rename to CI/Dependencies (Automated PRs); set release-plz pr_branch_prefix; update nightly branch
- align on single 'automated' label; remove 'bot' label usage
- unify bot branch prefix (bot/*); route bot/release-plz/renovate PRs to bot CI; add labels
- *(bot-prs)* trigger based on branch name only (release-plz*, auto/update-generated-client)
- run bot PR checks for release-plz branches; skip normal CI/deps/security for release-plz to avoid duplicates
- *(bot-prs)* set job names to match required status contexts
- *(bot-prs)* skip gitleaks on pull_request_target (not supported)
- *(bot-prs)* inline security jobs under CI workflow and remove separate security-bot-prs; fix failing run
- *(security-bot-prs)* simplify condition to head ref match
- *(generate)* lighten verification; rely on PR CI for build/test; update PR messaging
- avoid double-running on auto/update-generated-client by skipping normal PR jobs
- set required status contexts to job-based names (reusable workflows)
- *(bot-prs)* trigger on app/github-actions + restrict to auto/update-generated-client
- reuse common workflows; enable checks on bot PRs; align required status checks
- require conversation resolution on main
- fix topics format and branch protection (min supported) for Settings app

### Security

- schedule-only; keep cargo audit gating in CI
- remove PR-time TruffleHog; keep GH Secret Scanning + Push Protection and pre-commit
- drop gitleaks; enable GH Secret Scanning + Push Protection; add pre-commit TruffleHog; require TruffleHog status

## [0.2.6](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.5...v0.2.6) - 2025-08-30

### Other

- add crate-level documentation from README

## [0.2.5](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.4...v0.2.5) - 2025-08-30

### Added

- configure Renovate to manage OpenAPI Generator Docker tag

## [0.2.4](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.3...v0.2.4) - 2025-08-30

### Added

- enhance security hygiene
- add comprehensive CI hardening
- add deterministic codegen with Docker support

### Fixed

- correct TruffleHog configuration for push events
- add GITLEAKS_LICENSE to secrets scan workflow
- update deny.toml to version 2 format and fix license allowlist
- remove unused dev-dependencies
- ensure all code is formatted after generation
- formatting issues
- deduplicate security checks between CI and Security workflows
- update nightly workflow to use Docker instead of npm

### Other

- improve Renovate configuration organization
- remove unnecessary actions-permissions.md
- update README generation section to reflect current script
- improve README with clear guidance and platform notes
- add caching to speed up CI
- remove CODEGEN.md as requested
- always use Docker for generation, remove npm option
- unify generation script with Docker support
- use official OpenAPI Generator Docker image

## [0.2.3](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.2...v0.2.3) - 2025-08-29

### Other

- use wildcard version in README installation example

## [0.2.2](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.1...v0.2.2) - 2025-08-29

### Added

- add comparison link to release-plz PR template
- add debug logging to diagnose workflow triggering issues
- add manual dispatch support to skip-ci workflow
- implement release-plz status check bypass with dual merge options
- configure auto-merge for release-plz PRs
- add GitHub release and PR body templates to release-plz
- add GitHub settings configuration ([#29](https://github.com/genai-rs/langfuse-client-base/pull/29))

### Fixed

- remove duplicate changelog content
- correct release-plz template variables
- enable rebase merge for linear history ([#32](https://github.com/genai-rs/langfuse-client-base/pull/32))

### Other

- remove custom skip-ci system, use admin override instead
- rename label from 'release-plz' to 'skip-ci'

## [0.2.1](https://github.com/genai-rs/langfuse-client-base/compare/v0.2.0...v0.2.1) - 2025-08-29

### Added

- store OpenAPI spec locally and optimize generation ([#26](https://github.com/genai-rs/langfuse-client-base/pull/26))

### Fixed

- sync Cargo.toml version with crates.io ([#27](https://github.com/genai-rs/langfuse-client-base/pull/27))
- revert manual version bump to let release-plz handle it ([#24](https://github.com/genai-rs/langfuse-client-base/pull/24))

## [0.2.0] - 2025-01-29

### Breaking Changes
- Upgraded MSRV from 1.75.0 to 1.82.0 (requires Rust 1.82+)
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

[Unreleased]: https://github.com/genai-rs/langfuse-client-base/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/genai-rs/langfuse-client-base/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/genai-rs/langfuse-client-base/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/genai-rs/langfuse-client-base/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/genai-rs/langfuse-client-base/releases/tag/v0.1.0