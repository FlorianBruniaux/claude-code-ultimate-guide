---
name: release-notes
description: "Generate release notes in multiple formats from git commits"
---

# Release Notes Generator

Generate release notes in 3 formats from git commits for production releases.

## Process

1. **Analyze Git History**: Scan commits since last release tag
2. **Fetch PR Details**: Get titles, descriptions via `gh api`
3. **Categorize Changes**: Group by type (feat, fix, perf, etc.)
4. **Check Migrations**: Detect database migration files
5. **Generate 3 Outputs**: CHANGELOG, PR body, communication message
6. **Transform Language**: Convert tech jargon to product language

## Output Formats

### 1. CHANGELOG.md Section

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Summary
[1-2 sentence overview of this release]

### New Features
#### [Feature Name] (#PR)
- **Description**: User-facing functionality added
- **Impact**: How it benefits users

### Bug Fixes
- **[Module]**: Description (#issue, tracking-ID)

### Technical Improvements
- [Internal improvements, refactoring, performance]

### Database Migrations
[If applicable - list migration files]

### Statistics
- PRs: X | Features: Y | Fixes: Z | Files changed: N
```

### 2. PR Release Body

Uses your project's release template:
- `.github/PULL_REQUEST_TEMPLATE/release.md`
- `.github/pull_request_template_release.md`
- Or custom location specified in project config

### 3. Communication Announcement

Generate user-facing announcement (Slack, email, etc.):
- Non-technical language
- Focus on user impact
- Readable formatting (emojis optional)

Template location examples:
- `.github/COMMUNICATION_TEMPLATE/slack-release.md`
- `docs/templates/release-announcement.md`

## Migration Alert

**If migrations detected:**

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  [ATTENTION] DATABASE MIGRATIONS REQUIRED                    ║
╠══════════════════════════════════════════════════════════════════╣
║  This release contains X migration(s):                           ║
║  • 20250110_add_user_preferences                                 ║
║  • 20250112_create_audit_log_table                               ║
║  Action required: Run migration command after deployment         ║
╚══════════════════════════════════════════════════════════════════╝
```

**If no migrations:**
```
✅ [OK] No database migrations required
```

## Tech-to-Product Transformation

Convert technical commits to user-friendly descriptions:

| Technical | Product/User Language |
|-----------|----------------------|
| "Optimize N+1 queries with DataLoader" | "Faster loading times for lists" |
| "Implement AI embeddings with pgvector" | "New intelligent search feature" |
| "Fix permissions scope bug" | "Resolved access issue for certain users" |
| "Migration webpack -> Turbopack" | *Internal only - don't communicate* |
| "Refactor React hooks architecture" | *Internal only - don't communicate* |
| "Add rate limiting to API endpoints" | "Improved system stability and security" |

## Commit Categories

| Prefix | Category | Include in Announcement? |
|--------|----------|--------------------------|
| `feat:` | New Features | Yes |
| `fix:` | Bug Fixes | Yes (if user-facing) |
| `perf:` | Performance | Yes (simplified) |
| `security:` | Security | Yes |
| `refactor:` | Architecture | No |
| `chore:` | Maintenance | No |
| `docs:` | Documentation | No |
| `test:` | Tests | No |
| `build:` | Build System | No |
| `ci:` | CI/CD | No |

## Commands to Execute

```bash
# 1. Get last release tag
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1)

# 2. List commits since tag (excluding merges)
git log $LAST_TAG..HEAD --oneline --no-merges

# 3. Get commit details with PR numbers
git log $LAST_TAG..HEAD --format="%h %s" --no-merges

# 4. Check for migrations (adjust path to your ORM)
# Prisma:
git diff $LAST_TAG..HEAD --name-only -- prisma/migrations/
# Sequelize:
git diff $LAST_TAG..HEAD --name-only -- migrations/
# Django:
git diff $LAST_TAG..HEAD --name-only -- '**/migrations/*.py'
# Alembic:
git diff $LAST_TAG..HEAD --name-only -- alembic/versions/

# 5. Get PR details via GitHub CLI
gh api repos/{owner}/{repo}/pulls/{number}

# 6. Count statistics
TOTAL_PRS=$(git log $LAST_TAG..HEAD --oneline --merges | wc -l)
FEATURES=$(git log $LAST_TAG..HEAD --oneline --no-merges | grep -c 'feat:')
FIXES=$(git log $LAST_TAG..HEAD --oneline --no-merges | grep -c 'fix:')
```

## Semantic Versioning

Determine version number based on changes:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking change | MAJOR (X.0.0) | API removed, incompatible change |
| New feature | MINOR (0.X.0) | New functionality, backward-compatible |
| Bug fix / patch | PATCH (0.0.X) | Bug fixes only |

**Indicators**:
- `BREAKING CHANGE:` in commit body → MAJOR
- `feat:` commits present → MINOR
- Only `fix:` / `perf:` → PATCH

## Workflow Integration

Typical release workflow:

```
1. Verify all PRs merged to develop branch
2. Run: /release-notes (or specify version/range)
3. Review generated outputs for accuracy
4. Create PR: develop -> main with "release" label
5. Add generated CHANGELOG section to CHANGELOG.md
6. Use generated PR body as PR description
7. After merge: Create and push git tag
8. Post communication announcement (Slack/email/etc.)
9. Monitor deployment and migrations
```

## Git Tag Creation

After PR merge, create annotated tag:

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release v1.2.3: Brief description"

# Push tag to remote
git push origin v1.2.3

# Or push all tags
git push --tags
```

## Project-Specific Customization

Adapt these paths to your project:

```
# Migration detection (adjust ORM path)
prisma/migrations/        → Your ORM migration directory
db/migrate/               → Rails migrations
alembic/versions/         → Alembic migrations

# Template files (create if needed)
.github/PULL_REQUEST_TEMPLATE/release.md
.github/COMMUNICATION_TEMPLATE/announcement.md
docs/templates/release-notes.md
```

## Tips

- **Run from repository root**: Ensures git commands work correctly
- **Authenticate GitHub CLI**: Run `gh auth login` if needed
- **Review before publishing**: Always verify generated content
- **Breaking changes**: Search commit messages for `BREAKING CHANGE:`
- **Linked issues**: Include issue/ticket numbers for traceability
- **Database migrations**: Test in staging before production

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No tags found | Start from first commit |
| No commits since last tag | Error: "No changes to release" |
| Multiple tags on same commit | Use most recent by date |
| Pre-release tags (v1.0.0-beta.1) | Exclude from "last release" search |
| Commits without conventional format | Categorize as "Other Changes" |

## Usage Examples

```bash
# Generate release notes from last tag to HEAD
/release-notes

# Specify version manually
/release-notes v1.5.0

# Specify range
/release-notes from v1.4.0 to HEAD

# Preview without creating files
/release-notes --preview

# Include pre-release commits
/release-notes --include-pre-release
```

Version/Range: $ARGUMENTS
