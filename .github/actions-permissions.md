# GitHub Actions Permissions

This document outlines the permissions required for each workflow in this repository.

## Workflow Permissions

### CI (`ci.yml`)
- **contents**: read (checkout code)
- **checks**: write (post check results)

### Release (`release-plz.yml`)
- **contents**: write (create releases, tags)
- **pull-requests**: write (create/update PRs)
- **packages**: write (publish to crates.io)

### Generate Client (`generate-client.yml`)
- **contents**: write (commit generated code)
- **pull-requests**: write (create PR if changes)

### Security Scanning (`secrets.yml`)
- **contents**: read (scan code)
- **security-events**: write (upload findings)

### Dependency Updates (Renovate)
- **contents**: write (update dependencies)
- **pull-requests**: write (create/update PRs)

## Best Practices

1. **Use minimum required permissions** for each workflow
2. **Prefer workflow-level permissions** over job-level
3. **Use `permissions: {}` to drop all permissions** when none needed
4. **Audit permissions regularly** to ensure they're still minimal
5. **Use GITHUB_TOKEN** instead of PAT when possible

## Security Notes

- The default GITHUB_TOKEN has limited scope to the repository
- Personal Access Tokens (PATs) should be avoided unless necessary
- Secrets should be stored in GitHub Secrets, never in code
- Use environment protection rules for production deployments