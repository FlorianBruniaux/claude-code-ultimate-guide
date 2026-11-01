---
name: update-infos-release
description: Update Claude Code releases tracking (guide + landing + version bump)
argument-hint: "[bump-type]"
---

# Release Management Workflow

Automate Claude Code releases tracking and guide version management.

## Usage

```
/update-infos-release          # Update CC releases only (no guide version bump)
/update-infos-release patch    # Update CC + bump guide patch (3.9.11 → 3.9.12)
/update-infos-release minor    # Update CC + bump guide minor (3.9.11 → 3.10.0)
/update-infos-release major    # Update CC + bump guide major (3.9.11 → 4.0.0)
```

## Workflow Steps

### 1. Check for New Claude Code Releases

```bash
./scripts/update-cc-releases.sh
```

If new versions detected, continue. Otherwise, stop.

### 2. Update Claude Code Releases Tracking

**Files to update:**
- `machine-readable/claude-code-releases.yaml`
- `guide/core/claude-code-releases.md`
- `mcp-server/content/claude-code-releases.yaml` (byte-identical copy)
- `llms.txt`, `machine-readable/llms.txt`, `mcp-server/content/llms.txt` (tracked version sentence)
- Landing: `src/data/releases.ts`, `src/data/seo-editorial-contract.mjs` (`LATEST_CLAUDE_CODE_RELEASE_DATE`) and its pinned test `src/data/seo-editorial-contract.test.ts`

**Process:**
1. Read latest release notes from the command output; the summary it prints can omit versions, so list every `## ` heading of the saved changelog newer than the tracked version
2. Date each version from npm publication metadata (`https://registry.npmjs.org/@anthropic-ai%2Fclaude-code`, `time` field); skip versions without an upstream changelog entry
3. Update YAML with condensed highlights
4. Update Markdown with expanded details
5. Add the new entries to the landing `releases.ts` (newest first, `latest: true` on the newest, five `initiallyVisible: true`) and move the latest release date in `seo-editorial-contract.mjs` and its test

**Condensation rules for YAML:**
- ⭐ Major features get star emoji
- Breaking changes → `breaking:` array
- Bug fixes → single line
- 2-4 highlights max (focus on user-facing changes)
- Skip internal/SDK changes unless breaking

### 3. Guide Version Bump (if requested)

**If bump-type specified:**

```bash
# Read current version
cat VERSION

# Bump version
# patch: 3.9.11 → 3.9.12
# minor: 3.9.11 → 3.10.0
# major: 3.9.11 → 4.0.0

# Update VERSION file
echo "X.Y.Z" > VERSION

# Sync version across docs
./scripts/sync-version.sh
```

**Files synced by script:**
- `README.md`
- `guide/cheatsheet.md`
- `guide/ultimate-guide.md`
- `machine-readable/reference.yaml`

### 4. Update CHANGELOG.md

**Add entry:**

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Documentation

- **Claude Code Releases**: Updated tracking to vA.B.C
  - [Feature 1]
  - [Feature 2]
  - [Feature 3]

[If guide version bump:]
### Version Bump

- Bumped guide version: [old] → [new]
- Reason: [major features added / significant updates / breaking changes in CC]
```

### 4.5. Verify the automatic Claude Code RSS source

The landing RSS implementation in `src/pages/rss.xml.ts` emits Claude Code release items automatically from `src/data/releases.ts`. Update that release registry within the authorized landing scope; do not add a second manual Claude Code release item to `src/data/rss-entries.ts`.

Manual RSS entries remain available for guide-side news, including a release of the guide itself. Follow `docs/workflows/landing-sync.md` for that separate branch. A Claude Code CLI release and a guide release are different events.

Inspect the current RSS implementation for the emitted release link instead of copying a historical anchor example. After an authorized landing build, check the generated feed for duplicate items for the updated CLI release and confirm its link matches the implementation. Report an unavailable build or feed as unverified.

Done when the updated CLI release is supplied by the automatic source, no duplicate manual item was introduced, and feed verification passed or its limitation was reported.

### 4.7. Sync MCP Server Content

`mcp-server/content/` is a bundled copy of 3 source files, published to npm as `claude-code-ultimate-guide-mcp`. It does NOT auto-update, sync it every time the tracking YAML changes:

```bash
cp machine-readable/claude-code-releases.yaml mcp-server/content/claude-code-releases.yaml
cp machine-readable/reference.yaml mcp-server/content/reference.yaml
cp llms.txt mcp-server/content/llms.txt

# Bump mcp-server/package.json version (patch, unless server code also changed → minor)
cd mcp-server && npm run build && cd ..
```

Commit `mcp-server/content/*` + `mcp-server/package.json` (dist/ is gitignored, rebuilt at publish time). Ask the user before running `npm publish` (irreversible, public).

### 5. Verify Synchronization

```bash
./scripts/check-landing-sync.sh
```

**Expected output:**
```
✅ Version guide:    X.Y.Z
✅ Templates:        N
✅ Quiz questions:   N
✅ Guide lines:      N
✅ Claude Code:      vA.B.C
```

If mismatches, fix before committing.

### 6. Commit and Push

**Two repositories to update:**

#### Guide Repository

```bash
cd /path/to/claude-code-ultimate-guide

git add \
  VERSION \
  CHANGELOG.md \
  README.md \
  guide/cheatsheet.md \
  guide/ultimate-guide.md \
  guide/core/claude-code-releases.md \
  machine-readable/reference.yaml \
  machine-readable/claude-code-releases.yaml \
  mcp-server/content/claude-code-releases.yaml \
  llms.txt machine-readable/llms.txt mcp-server/content/llms.txt

# If version bump:
git commit -m "release: vX.Y.Z

- Update Claude Code releases tracking (vOLD → vNEW)
- [Bump type]: vOLD_GUIDE → vNEW_GUIDE
- Update CHANGELOG with release details

[attribution line provided by your host]"

# If CC releases only:
git commit -m "docs: update Claude Code releases to vA.B.C

- Update latest tracked version: vOLD → vNEW
- Add vNEW highlights: [feature1], [feature2], [feature3]
- [Any breaking changes or fixes]
- Update dates: YYYY-MM-DD

[attribution line provided by your host]"

git push
```

#### Landing Repository

```bash
cd ../claude-code-ultimate-guide-landing

pnpm test   # the release-date contract test pins the latest date
git add src/data/releases.ts src/data/seo-editorial-contract.mjs src/data/seo-editorial-contract.test.ts

git commit -m "docs: sync Claude Code vA.B.C release history

- Add vNEW to releases.ts and move the latest release date

[attribution line provided by your host]"

git push
```

### 7. Summary Output

Display to user:

```
✅ Release Update Complete

Guide Repository:
- Version: [old] → [new]
- Claude Code: vA.B.C
- Commit: [hash]
- Files: [count] updated

Landing Repository:
- Claude Code release history: vA.B.C
- Commit: [hash]
- Files: [count] updated

Synchronization: ✅ All synced

Next Steps:
1. Verify the deploy run: gh run list -R FlorianBruniaux/claude-code-ultimate-guide-landing --workflow deploy.yml --limit 1 (its smoke job checks that /releases/ announces the latest version)
2. Check https://cc.bruniaux.com/releases/
3. [If major release] Update social media / announcements
```

## Error Handling

**If no new Claude Code versions:**
```
ℹ️ No new Claude Code releases detected.
Current tracked: vX.Y.Z
Latest available: vX.Y.Z

Aborting. Nothing to update.
```

**If sync check fails:**
```
❌ Synchronization check failed:
[List mismatches]

Please fix manually before committing.
Run: ./scripts/check-landing-sync.sh
```

**If git operations fail:**
```
❌ Git operation failed: [error]

Manual intervention required.
Check: git status
```

## Examples

### Example 1: Update CC releases only

```
User: /update-infos-release

Output:
✅ New Claude Code release detected: v2.1.15
   Date: 2026-01-22
   Highlights:
   - New feature X
   - Fix for Y
   - Improvement Z

Updating tracking files...
✅ YAML updated
✅ Markdown updated
✅ Landing releases.ts updated

Verifying sync... ✅ All synced

Committing changes...
✅ Guide: commit abc1234
✅ Landing: commit def5678

✅ Release Update Complete
```

### Example 2: Update CC + minor bump

```
User: /update-infos-release minor

Output:
✅ New Claude Code release detected: v2.2.0
   Major release with significant features

Current guide version: 3.9.11
Bumping to: 3.10.0 (minor)

Updating files...
✅ Claude Code tracking updated
✅ Guide version bumped
✅ CHANGELOG updated
✅ All docs synced

Verifying sync... ✅ All synced

Committing changes...
✅ Guide: commit abc1234 (8 files)
✅ Landing: commit def5678 (1 file)

✅ Release Update Complete (v3.10.0)
```

## Implementation Notes

- **Recovery**: If a step fails, stop and report the partial state. Preserve pre-existing and concurrent edits; restore only changes owned by this operation after checking that their current state still matches what it wrote. Do not use `git reset --hard`.
- **Idempotency**: Can be run multiple times safely
- **Validation**: Always verify sync before committing
- **User confirmation**: Ask before version bump if ambiguous
- **Smart defaults**: No bump = CC update only

## Related Commands

- `/version` - Check current versions (guide + CC)
- `/changelog` - View recent CHANGELOG entries
- `/sync` - Run sync check without updates
