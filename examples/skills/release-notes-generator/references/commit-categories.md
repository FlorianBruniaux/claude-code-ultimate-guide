# Commit Categorization Rules

This document defines how to categorize commits based on Conventional Commits format.

## Primary Categories

### Features (`feat:`)
**CHANGELOG**: New Features
**Slack**: Yes - always include
**Examples**:
- `feat(dashboard): add export report system`
- `feat(search): add fuzzy matching`
- `feat(api): add batch operations endpoint`

### Bug Fixes (`fix:`)
**CHANGELOG**: Bug Fixes
**Slack**: Yes - if user-facing; No - if internal
**Examples**:
- `fix(auth): correct token refresh flow` -> Include in Slack
- `fix(test): correct mock setup` -> Do NOT include in Slack

### Performance (`perf:`)
**CHANGELOG**: Technical Improvements > Performance
**Slack**: Yes - simplified ("Performance improvement")
**Examples**:
- `perf(api): optimize N+1 queries with batching`
- `perf(build): reduce bundle size by 30%`

### Security (`security:` or `fix(security):`)
**CHANGELOG**: Security
**Slack**: Yes - always, with appropriate detail level
**Examples**:
- `security: fix CVE-2025-55182 dependency RCE`
- `fix(security): prevent XSS in user input`

## Secondary Categories (CHANGELOG only)

### Refactoring (`refactor:`)
**CHANGELOG**: Technical Improvements > Architecture
**Slack**: No
**Examples**:
- `refactor(hooks): migrate to new pattern`
- `refactor(permissions): extract to service layer`

### Documentation (`docs:`)
**CHANGELOG**: Documentation (if significant)
**Slack**: No
**Examples**:
- `docs: update CLAUDE.md with new patterns`
- `docs(api): add endpoint documentation`

### Tests (`test:`)
**CHANGELOG**: Tests (count only)
**Slack**: No
**Examples**:
- `test(api): add endpoint integration tests`
- `test(e2e): add workflow tests`

### Chores (`chore:`)
**CHANGELOG**: No (unless significant)
**Slack**: No
**Examples**:
- `chore: update dependencies`
- `chore(ci): fix workflow permissions`

### Style (`style:`)
**CHANGELOG**: No
**Slack**: No
**Examples**:
- `style: apply prettier formatting`
- `style(eslint): fix linting errors`

## Scope Patterns

Common scopes:

| Scope | Area |
|-------|------|
| `auth` | Authentication |
| `billing` | Billing and payments |
| `api` | API endpoints |
| `ui` | UI components |
| `dashboard` | Dashboard features |
| `notifications` | Notification system |
| `search` | Search functionality |
| `user` | User management |
| `db` | Database and migrations |
| `permissions` | Permission system |
| `admin` | Admin panel |

## Breaking Changes

Indicated by `!` after type/scope or `BREAKING CHANGE:` in footer:
- `feat(api)!: change status enum`
- `fix(auth)!: require new token format`

**CHANGELOG**: Breaking Changes section
**Slack**: Yes - with migration instructions

## PR Number Extraction

Extract PR numbers from:
1. Commit message: `(#123)`
2. Merge commit: `Merge pull request #123`
3. GitHub API: cross-reference with commit SHA

## Error Tracker Issue Linking

Match patterns:
- `[error-tracker]: PROJECT-XX`
- `fixes PROJECT-XX`
- `closes #XX` (GitHub issue)

## Statistics Calculation

Count for release stats:
- **PRs**: Unique PR numbers
- **Features**: `feat:` commits
- **Bugs**: `fix:` commits (excluding test/internal)
- **Improvements**: `perf:` + `refactor:` + UI improvements
- **Security**: `security:` commits
- **Breaking**: Commits with `!` or `BREAKING CHANGE`
