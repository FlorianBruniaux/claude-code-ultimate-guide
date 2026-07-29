---
name: release
description: Release guide version (CHANGELOG + VERSION + README + landing sync + commit + push)
argument-hint: "<patch|minor|major>"
---

# Guide Release Workflow

Release a new version of the Claude Code Ultimate Guide.

## Usage

```
/release patch    # 3.20.4 → 3.20.5
/release minor    # 3.20.4 → 3.21.0
/release major    # 3.20.4 → 4.0.0
```

## Step 1: Validate

1. Parse `$ARGUMENTS` — must be exactly one of: `patch`, `minor`, `major`. If missing or invalid, ask.
2. Run `git status` in the guide repo. If working tree is clean with no staged changes, abort: "Nothing to release."
3. Read `VERSION` file → current version.

## Step 2: Compute New Version

Apply semver bump to current version:
- `patch`: X.Y.Z → X.Y.(Z+1)
- `minor`: X.Y.Z → X.(Y+1).0
- `major`: X.Y.Z → (X+1).0.0

Write the new version to `VERSION`.
Display: `3.20.4 → 3.20.5 (patch)`

## Step 3: Draft CHANGELOG Entry

**Do NOT auto-generate from diff.** Instead:

1. Run `git diff --stat` and `git diff --name-only` to identify changed areas
2. Run `git log --oneline` since last tag/release to see recent commits
3. Read the modified files to understand what changed
4. **Draft** a structured CHANGELOG entry:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- [new features, new files, new sections]

### Changed
- [modifications to existing content]

### Fixed
- [corrections, bug fixes]
```

5. **Present the draft to the user** and ask for confirmation or edits
6. Only after approval, insert into `CHANGELOG.md` after the `## [Unreleased]` line

## Step 4: Update Counts

Calculate current metrics:

```bash
# Quiz questions count (sum across all YAML files)
grep -r '  - id:' quiz/questions/ | wc -l
# Templates count
find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" | wc -l
# Guide lines
wc -l guide/ultimate-guide.md
```

Update these counts wherever they appear in:
- `README.md`
- `machine-readable/reference.yaml`
- `CLAUDE.md` (the VERSION reference in Key Files table)
- `llms.txt` (root) — Version, Last Updated, Lines, Templates, Quiz (3 occurrences total)
- `llms-full.txt` (root) — same Metadata fields + these additional occurrences:
  - "For Learning" section: `Interactive Quiz (N questions)` URL text
  - "Template Library (N templates)" section heading
  - FAQ answer (first FAQ entry, line starting with "A: The most comprehensive...")
  - Repo tree comment: `quiz/ # N-question interactive quiz`
- `machine-readable/llms.txt` — must be identical to root `llms.txt` at all times

Only update values that actually changed. Don't touch counts that are still correct.

**Verification gate — run after updating, before moving to Step 5:**

```bash
VERSION=$(cat VERSION)
QUIZ=$(grep -r '  - id:' quiz/questions/ | wc -l | tr -d ' ')
TEMPLATES=$(find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" | wc -l | tr -d ' ')

echo "=== llms.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:" llms.txt

echo "=== llms-full.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:\|Template Library\|question interactive" llms-full.txt

echo "=== machine-readable/llms.txt check ==="
grep "Version:\|Quiz Questions:\|Production Templates:" machine-readable/llms.txt

echo "=== Expected: VERSION=$VERSION QUIZ=$QUIZ TEMPLATES=$TEMPLATES ==="
```

All three files must show the same values. If any mismatch, fix before continuing.

## Step 5: Sync Version

```bash
./scripts/sync-version.sh
```

This propagates the version into: README.md, cheatsheet.md, ultimate-guide.md, reference.yaml.

**Also updates**:
- "Last Update" badge in README.md (date + version)
- Footer date in README.md ("Updated daily · Feb 10, 2026")

## Step 5.5: Sync MCP Server Content

`mcp-server/content/` is a bundled copy of 3 source files, published to npm. It does NOT auto-update, sync it manually every release:

```bash
cp machine-readable/claude-code-releases.yaml mcp-server/content/claude-code-releases.yaml
cp machine-readable/reference.yaml mcp-server/content/reference.yaml
cp llms.txt mcp-server/content/llms.txt

# Bump mcp-server/package.json version (patch, unless tool code also changed → minor)
cd mcp-server && npm run build && cd ..
```

Commit `mcp-server/content/*` + `mcp-server/package.json` (dist/ is gitignored, rebuilt at publish time).

**Publish** (irreversible, public — always confirm with the user before running):
```bash
cd mcp-server && npm publish && cd ..
```

## Step 6: Sync Landing

Working directory: `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/`

1. Update guide version in `index.html` (footer + FAQ sections)
2. Update quiz question count in `index.html`, `quiz/index.html`, `learning/index.html` if changed
3. Update templates count in `index.html`, `examples/index.html` if changed
4. If quiz YAML files were modified, compile them:
   ```bash
   ./scripts/compile-questions.sh
   ```
5. Update `CLAUDE.md` in the landing repo if counts changed

**Verification gate:**
```bash
./scripts/check-landing-sync.sh
```
Must pass with 0 issues. If it fails, fix the mismatches and re-run until it passes.

## Step 6.5: Add RSS Entry

In the landing repo, add an entry to `src/data/rss-entries.ts`:

1. Read the CHANGELOG entry just drafted (Step 3)
2. Draft an entry of type `guide_release`:

```typescript
{
  type: 'guide_release',
  title: 'Claude Code Ultimate Guide vX.Y.Z',
  date: 'Mon DD, YYYY',   // today's date, same format as releases.ts
  description: '[1-2 sentences from CHANGELOG highlights, plain text no HTML]',
  link: 'https://cc.bruniaux.com/releases/',
},
```

3. **Prepend** it at the top of the `rssEntries` array (newest first).
4. Present the draft to the user. Adjust wording if needed, then write.

**Rule**: always add an entry for patch/minor/major — even small patches are worth tracking.

## Step 7: Commit & Push Both Repos

### Guide repo

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
git add [all modified files — list them explicitly]
git commit -m "release: vX.Y.Z - [short description from CHANGELOG]

[2-3 line summary of main changes]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

### Landing repo

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing
git add [all modified files — list them explicitly]
git commit -m "sync: guide vX.Y.Z - [short description]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push
```

## Step 8: Summary

Display:

```
Release vX.Y.Z Complete

Guide:   commit [hash] ([N] files)
Landing: commit [hash] ([N] files)
Sync:    All checks passed

Changes:
- [CHANGELOG summary, 2-3 bullets]

Tip: Run `/guide-recap latest` to generate social posts for this release.
```

## Error Handling

- **No argument** → Ask: "Which bump type? (patch/minor/major)"
- **Clean working tree** → Abort: "Nothing to release. Commit changes first."
- **Sync check fails** → Fix and re-verify (do not commit with sync errors)
- **Git push fails** → Show error, do not rollback

## Relation to Other Commands

| Command | Purpose |
|---------|---------|
| `/release` | Release the guide itself (THIS) |
| `/update-infos-release` | Track Anthropic's Claude Code releases |
| `/sync` | Verify sync status (read-only) |
| `/version` | Display versions (read-only) |
| `/changelog` | View CHANGELOG entries (read-only) |

No overlap: `/release` manages guide releases, `/update-infos-release` manages CC release tracking.