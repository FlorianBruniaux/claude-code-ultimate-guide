---
name: release-notes-generator
description: "Generate release notes in 3 formats (CHANGELOG.md, PR body, Slack announcement) from git commits. Automatically categorizes changes and converts technical language to user-friendly messaging. Use for releases, changelogs, version notes, what's new summaries, or ship announcements."
allowed-tools: Bash
effort: low
---

# Release notes generator

Generate comprehensive release notes in 3 formats from git commits.

## Workflow

1. **Analyze git history** since last release tag or specified version
2. **Fetch PR details** (titles, descriptions, labels) via `gh api`
3. **Categorize changes** into features, bug fixes, improvements, security, breaking changes
4. **Generate 3 outputs**: CHANGELOG.md section (technical), PR release body (semi-technical), Slack message (user-friendly)
5. **Transform language** from technical jargon to accessible messaging
6. **Alert on migrations** if database migrations are detected

## How to use

### Basic usage

```
Generate release notes since last release
```

```
Create release notes for version 0.18.0
```

### With specific range

```
Generate release notes from v0.17.0 to HEAD
```

### Preview only

```
Preview release notes without writing files
```

## Output formats

### 1. CHANGELOG.md Section

Technical format for developers:

```markdown
## [0.18.0] - 2025-12-08

### Objective
[1-2 sentence summary]

### New Features
#### [Feature Name] (#PR)
- **Description**: ...
- **Impact**: ...

### Bug Fixes
- **[Module]**: Description (#issue, [error-tracker] ISSUE-XX)

### Technical Improvements
#### Performance / UI/UX / Architecture
- [Description]

### Database Migrations
[If applicable]

### Statistics
- PRs: X
- Features: Y
- Bugs: Z
```

### 2. PR release body

Uses template from `.github/PULL_REQUEST_TEMPLATE/release.md`:
- Objective summary
- Features with specs links
- Bug fixes with error tracker references
- Improvements by category
- Migration instructions
- Deployment checklist

### 3. Slack announcement

Product-focused format from `.github/COMMUNICATION_TEMPLATE/slack-release.md`:
- **PR link** included for traceability
- Non-technical language
- Focus on user impact (end-users, admins, stakeholders)
- Emojis for readability
- Statistics summary

## Workflow integration

This skill integrates with the release workflow:

```
1. Analyze commits: git log <last-tag>..HEAD
2. Determine version number (MAJOR.MINOR.PATCH)
3. Generate 3 outputs
4. Create PR develop -> main with "Release" label
5. Update CHANGELOG.md
6. After merge: create git tag
7. Generate Slack announcement
```

## Tech-to-product transformation

The skill automatically transforms technical language:

| Technical | Product |
|-----------|---------|
| "N+1 query optimization with DataLoader" | "Faster list loading" |
| "AI embeddings implementation with pgvector" | "New intelligent search" |
| "Fix scope permissions in getPermissionScope()" | "Fixed access permissions bug" |
| "Migration webpack -> Turbopack" | *Do not communicate* |
| "React hooks refactoring" | *Do not communicate* |
| "Fix N+1 in user loaders" | "Performance improvement" |
| "Add retry logic for DB connection errors" | "Better connection stability" |

## Commit categories

Commits are categorized by conventional commit prefix:

| Prefix | Category | Include in Slack? |
|--------|----------|-------------------|
| `feat:` | New Features | Yes |
| `fix:` | Bug Fixes | Yes (if user-facing) |
| `perf:` | Performance | Yes (simplified) |
| `security:` | Security | Yes |
| `refactor:` | Architecture | No |
| `chore:` | Maintenance | No |
| `docs:` | Documentation | No |
| `test:` | Tests | No |
| `style:` | Style | No |

## Console output format

When generating release notes, ALWAYS display a clear summary in the console with:

### Migration alert (CRITICAL)

If migrations are detected, display prominently:

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [WARNING] DATABASE MIGRATIONS REQUIRED                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  This release contains X migration(s):                           ║
║                                                                  ║
║  • 20251210123456_add_feature_description                        ║
║  • 20251211094532_update_status_enum                             ║
║                                                                  ║
║  Action required BEFORE deployment:                              ║
║  → Run: [migration-command]                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

If NO migrations:

```
✅ [OK] No database migrations required
```

### Detection method

Check for new migration files since last release:

```bash
# Find new migrations since last tag
git diff <last-tag>..HEAD --name-only -- migrations/
```

## Example

**User**: "Generate release notes since v0.17.0"

**Output**:

```
Analyzing commits from v0.17.0 to HEAD...

Found:
- 15 commits
- 8 PRs merged
- 2 new features
- 5 bug fixes
- 3 improvements

╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [WARNING] DATABASE MIGRATIONS REQUIRED                      ║
╠══════════════════════════════════════════════════════════════════╣
║  This release contains 1 migration(s):                           ║
║  • 20251208143021_add_user_preferences                           ║
║  Action required: [migration-command]                             ║
╚══════════════════════════════════════════════════════════════════╝

--- CHANGELOG.md Section ---
[Technical format output]

--- PR Release Body ---
[Semi-technical format output]

--- Slack Announcement ---
[Product-focused format output]

Write to files? (CHANGELOG.md, clipboard for PR/Slack)
```

## Commands used

```bash
# Get last release tag
git tag --sort=-v:refname | head -n 1

# List commits since tag
git log <tag>..HEAD --oneline --no-merges

# Get PR details
gh api repos/{owner}/{repo}/pulls/{number}

# Get commit details
git show --stat <sha>
```

## Tips

- Run from repository root
- Ensure `gh` CLI is authenticated
- Review generated content before publishing
- Adjust product language for your audience
- Use `--preview` to see output without writing

## Reference files

- `assets/changelog-template.md` - CHANGELOG section template
- `assets/slack-template.md` - Slack announcement template
- `references/tech-to-product-mappings.md` - Transformation rules
- `references/commit-categories.md` - Categorization rules

## Related skills

- `github-actions-templates` - For CI/CD workflows
- `changelog-generator` - Original inspiration (ComposioHQ)
