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

1. Parse `$ARGUMENTS`: it must be exactly one of `patch`, `minor`, `major`. If missing or invalid, ask.
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
# Templates count (same definition as scripts/check-landing-sync.sh)
find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" -not -path '*/commands/*' | wc -l
# Guide lines
wc -l guide/ultimate-guide.md
```

Update these counts wherever they appear in:
- `README.md`
- `machine-readable/reference.yaml`
- `CLAUDE.md` (the VERSION reference in Key Files table)
- `llms.txt` (root): the sentence `Guide version X.Y.Z, tracking Claude Code up to vA.B.C (Month YYYY).`
- `llms-full.txt` (root): its metadata fields, if present, plus these occurrences:
  - "For Learning" section: `Interactive Quiz (N questions)` URL text
  - "Template Library (N templates)" section heading
  - FAQ answer (first FAQ entry, line starting with "A: The most comprehensive...")
  - Repo tree comment: `quiz/ # N-question interactive quiz`
- `machine-readable/llms.txt` and `mcp-server/content/llms.txt`: both must be identical to root `llms.txt` at all times

Only update values that actually changed. Don't touch counts that are still correct.

**Verification gate: run after updating, before moving to Step 5:**

```bash
VERSION=$(cat VERSION)
QUIZ=$(grep -r '  - id:' quiz/questions/ | wc -l | tr -d ' ')
TEMPLATES=$(find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" -not -path '*/commands/*' | wc -l | tr -d ' ')

echo "=== llms.txt check ==="
grep -n "Guide version" llms.txt

echo "=== llms-full.txt check ==="
grep -n "Version:\|Quiz Questions:\|Template Library\|question interactive" llms-full.txt

echo "=== llms.txt mirrors ==="
cmp llms.txt machine-readable/llms.txt && cmp llms.txt mcp-server/content/llms.txt && echo identical

echo "=== Expected: VERSION=$VERSION QUIZ=$QUIZ TEMPLATES=$TEMPLATES ==="
```

All values must match the expected line and the mirrors must be identical. If any mismatch, fix before continuing.

## Step 5: Sync Version

```bash
./scripts/sync-version.sh
```

This propagates the version into: README.md, cheatsheet.md, ultimate-guide.md, reference.yaml.

**Also updates**:
- "Last Update" badge in README.md (date + version)
- Footer date in README.md ("Updated daily · Feb 10, 2026")

## Step 5.5: Sync MCP Server Content

`mcp-server/content/` is a bundled copy of source files, published to npm. It does NOT auto-update, sync it manually every release:

```bash
cp machine-readable/claude-code-releases.yaml mcp-server/content/claude-code-releases.yaml
cp machine-readable/reference.yaml mcp-server/content/reference.yaml
cp machine-readable/translations.json mcp-server/content/translations.json
cp llms.txt mcp-server/content/llms.txt

# Bump mcp-server/package.json version (patch, unless tool code also changed → minor)
cd mcp-server && npm run build && cd ..
```

Commit `mcp-server/content/*` + `mcp-server/package.json` (dist/ is gitignored, rebuilt at publish time).

**Publish** (irreversible and public, always confirm with the user before running):
```bash
cd mcp-server && npm publish && cd ..
```

## Step 6: Sync Landing

Working directory: the sibling checkout `../claude-code-ultimate-guide-landing/`.

The landing is an Astro site. `src/pages/changelog/index.astro` reads `VERSION` at build time, so the guide version has no hard-coded copy to edit.

1. From the guide repo, run the sync check and edit only the landing files it names:
   ```bash
   ./scripts/check-landing-sync.sh
   ```
2. Quiz questions live as Markdown in the landing (`src/content/questions/`). If quiz YAML files were modified here, port the changed questions there. The sync check compares question counts only, so it does not catch an edited question.
3. Update `CLAUDE.md` in the landing repo if counts changed
4. Rebuild the guide reader before pushing the landing:
   ```bash
   cd ../claude-code-ultimate-guide-landing
   node scripts/prepare-guide-content.mjs && pnpm build
   ```

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

**Rule**: always add an entry for patch/minor/major, even small patches are worth tracking.

## Step 7: Commit & Push Both Repos

### Guide repo

```bash
git add [all modified files, listed explicitly]
git commit -m "release: vX.Y.Z - [short description from CHANGELOG]

[2-3 line summary of main changes]

[attribution line provided by your host]"
git push
```

### Landing repo

```bash
cd ../claude-code-ultimate-guide-landing
git add [all modified files, listed explicitly]
git commit -m "sync: guide vX.Y.Z - [short description]

[attribution line provided by your host]"
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
