---
name: land-and-deploy
description: Merge PR, wait for CI, verify deploy, run canary. The complete landing pipeline.
argument-hint: "[--skip-checks] [--env staging|production]"
effort: high
disable-model-invocation: true
---

# Land and deploy

Complete landing pipeline: merge the PR, wait for CI, verify the deployment, run a health check.

Picks up where `/ship` left off. `/ship` creates the PR. This command merges it and verifies production.

**Non-interactive by default.** The user said "land it", so land it. Stop only for the critical readiness gate and hard blockers.

## Instructions

### Step 1: Pre-flight

```bash
# Verify GitHub CLI is authenticated
gh auth status

# Detect PR from current branch (or use argument if provided)
gh pr view --json number,state,title,url,mergeStateStatus,mergeable,baseRefName,headRefName
```

**Stop conditions:**
- GitHub CLI not authenticated → "Run `gh auth login` first"
- No PR exists → "No PR found for this branch. Run `/ship` first."
- PR already merged → "PR is already merged."
- PR is closed → "PR is closed. Reopen it first."

---

### Step 2: CI status check

```bash
# Check current CI status
gh pr checks --json name,state,status,conclusion

# Check for merge conflicts
gh pr view --json mergeable -q .mergeable
```

**Stop conditions:**
- Required checks FAILING → show failing checks, stop
- `mergeable` is `CONFLICTING` → "PR has merge conflicts. Resolve them and push before landing."
- Required checks PENDING → proceed to Step 3 (wait for CI)
- All checks passing → skip to Step 3.5 (readiness gate)

---

### Step 3: Wait for CI (if pending)

```bash
# Watch CI checks with 15-minute timeout
gh pr checks --watch --fail-fast
```

- CI passes → continue to Step 3.5
- CI fails → stop, show failures
- Timeout (15 min) → "CI has been running for 15 minutes. Investigate manually."

Record CI wait duration for the deploy report.

---

### Step 3.5: Pre-Merge readiness gate

**This is the one critical confirmation before an irreversible merge.** Collect all evidence, then get explicit approval.

#### Review staleness check

```bash
# How many commits since the last review in this branch?
git log --oneline $(git merge-base HEAD origin/main)..HEAD | wc -l

# What changed after any review was done?
git log --oneline -10
```

Staleness thresholds:
- 0–3 commits since review → CURRENT (green)
- 4+ commits, touching code → STALE (yellow, review may not reflect current code)
- No review found → NOT RUN (yellow)

#### Test results

```bash
# Run tests now (fast tests only)
npm test 2>/dev/null || pnpm test 2>/dev/null || \
  pytest --tb=short -q 2>/dev/null || \
  go test ./... 2>/dev/null

# Check exit code
echo "Tests exit code: $?"
```

Failing tests = BLOCKER. Cannot merge with failing tests.

#### Documentation check

```bash
# Were CHANGELOG and docs updated on this branch?
git diff --name-only $(git merge-base HEAD origin/main)...HEAD -- \
  README.md CHANGELOG.md ARCHITECTURE.md CONTRIBUTING.md CLAUDE.md VERSION
```

If CHANGELOG.md and VERSION were NOT modified and the diff includes new features → WARNING.

#### Readiness report

Present a summary and ask for explicit confirmation:

```
╔══════════════════════════════════════════════════════════╗
║              PRE-MERGE READINESS REPORT                  ║
╠══════════════════════════════════════════════════════════╣
║  PR: #NNN: [title]                                       ║
║  Branch: feature-branch → main                           ║
║                                                          ║
║  REVIEWS                                                 ║
║    Review:     CURRENT / STALE (N commits) / NOT RUN     ║
║                                                          ║
║  TESTS                                                   ║
║    Fast tests: PASS / FAIL (blocker)                     ║
║                                                          ║
║  DOCUMENTATION                                           ║
║    CHANGELOG:  Updated / NOT UPDATED (warning)           ║
║    VERSION:    Bumped / NOT BUMPED (warning)             ║
║                                                          ║
║  WARNINGS: N  |  BLOCKERS: N                             ║
╚══════════════════════════════════════════════════════════╝

Options:
  A) Merge (all checks green)
  B) Don't merge yet, address warnings first
  C) Merge anyway (I understand the risks)
```

If the user chooses B, list exactly what needs to be done and stop.

---

### Step 4: Merge the PR

```bash
# Merge (auto-detect method from repo settings, delete branch after)
gh pr merge --auto --delete-branch

# Fallback if auto-merge is not enabled
# gh pr merge --squash --delete-branch
```

Record the merge commit SHA and timestamp.

If merge fails with permission error → "You don't have merge permissions. Ask a maintainer to merge."

If merge queue is active, poll until merged:

```bash
# Poll every 30 seconds, timeout after 30 minutes
gh pr view --json state -q .state
```

---

### Step 5: Platform detection

Detect how this project deploys so we know what to verify.

```bash
# Detect platform from config files
[ -f fly.toml ]         && echo "PLATFORM: fly"
[ -f render.yaml ]      && echo "PLATFORM: render"
[ -f vercel.json ] || [ -d .vercel ] && echo "PLATFORM: vercel"
[ -f netlify.toml ]     && echo "PLATFORM: netlify"
[ -f Procfile ]         && echo "PLATFORM: heroku"
[ -f railway.toml ]     && echo "PLATFORM: railway"

# Detect GitHub Actions deploy workflows
for f in .github/workflows/*.yml .github/workflows/*.yaml; do
  [ -f "$f" ] && grep -qiE "deploy|release|production|cd" "$f" 2>/dev/null && echo "DEPLOY_WORKFLOW: $f"
done

# Classify diff scope (frontend / backend / docs / config)
git diff --name-only $(git merge-base HEAD~1 origin/main)...HEAD | \
  awk '{
    if (/\.(css|scss|tsx|jsx|html|svg)$/ || /components|pages|public\//) f=1;
    if (/api\/|server\/|backend\/|\.(go|py|rb|java)$/) b=1;
    if (/README|CHANGELOG|docs\/|\.(md)$/) d=1;
    if (/\.env|config\/|\.toml$|\.yaml$/) c=1;
  } END {
    if (f) print "SCOPE_FRONTEND=true";
    if (b) print "SCOPE_BACKEND=true";
    if (d) print "SCOPE_DOCS=true";
    if (c) print "SCOPE_CONFIG=true";
  }'
```

**Decision tree:**
- Docs-only diff → skip deploy verification, go to Step 8
- No deploy workflow + no URL provided → ask user if this project has a web deploy
- Otherwise → proceed to Step 6

---

### Step 6: Wait for deploy

**GitHub Actions deploy workflow:**

```bash
# Find the run triggered by the merge commit
gh run list --branch main --limit 10 --json databaseId,headSha,status,conclusion,workflowName

# Poll until complete (30s interval, 20 min timeout)
gh run view <run-id> --json status,conclusion
```

**Platform-specific strategies:**

| Platform | Detection | Wait strategy |
|----------|-----------|---------------|
| Vercel / Netlify | Auto-deploy on push | Wait 60s for propagation, then check |
| Fly.io | `fly.toml` present | `fly status --app <app>`, check `started` status |
| Render | `render.yaml` present | Poll production URL until it responds with 200 |
| Heroku | `Procfile` present | `heroku releases --app <app> -n 1` |
| Railway | `railway.toml` present | Poll production URL |
| GitHub Actions only | `.github/workflows/` with deploy step | Poll `gh run view` |

If deploy fails → offer to investigate logs or create a revert commit.

Record deploy duration for the report.

---

### Step 7: Production health check

Use diff scope (from Step 5) to determine check depth:

| Diff Scope | Canary Depth |
|------------|--------------|
| Docs only | Already skipped in Step 5 |
| Config only | HTTP 200 smoke check only |
| Backend only | Status + response time check |
| Frontend (any) | Full: status + response time + content check |
| Mixed | Full check |

**Full health check sequence:**

```bash
# 1. Page loads (200 status)
curl -sf -o /dev/null -w "%{http_code}" "${PROD_URL}" 2>/dev/null

# 2. Response time check
curl -sf -o /dev/null -w "%{time_total}" "${PROD_URL}" 2>/dev/null

# 3. Health endpoint (if exists)
curl -sf "${PROD_URL}/health" 2>/dev/null || \
curl -sf "${PROD_URL}/api/health" 2>/dev/null

# 4. Content check: page is not blank
curl -sf "${PROD_URL}" 2>/dev/null | wc -c
```

Pass criteria:
- HTTP 200 status
- Response time under 10 seconds
- Page has content (>500 bytes)
- Health endpoint returns 200 (if configured)

If any check fails → offer to revert:

```
Post-deploy health check detected issues:
  [finding, specific]

Options:
  A) Investigate (this may be normal: cache warming, eventual consistency)
  B) Rollback (revert the merge commit)
  C) Continue (I'll monitor manually)
```

---

### Step 8: Revert (if needed)

```bash
# Fetch the latest base branch
git fetch origin main

# Create a revert commit
git checkout main
git revert <merge-commit-sha> --no-edit
git push origin main
```

If conflicts → "Revert has conflicts. Run `git revert <sha>` manually to resolve."
If branch protections → "Create a revert PR: `gh pr create --title 'revert: <title>'`"

---

### Step 9: Deploy report

```
LAND & DEPLOY REPORT
═════════════════════════════════════════
PR:           #NNN: [title]
Branch:       feature-branch → main
Merged:       [timestamp] (squash / merge)
Merge SHA:    [short SHA]

Timing:
  CI wait:    [Xm Ys / skipped]
  Deploy:     [Xm Ys / no workflow detected]
  Health:     [Xs / skipped]
  Total:      [end-to-end duration]

CI:           PASSED / FAILED / SKIPPED
Deploy:       PASSED / FAILED / NO WORKFLOW
Production:   HEALTHY / DEGRADED / SKIPPED / REVERTED
  Status:     [HTTP status code]
  Response:   [Xms]

VERDICT: DEPLOYED AND VERIFIED / DEPLOYED (UNVERIFIED) / REVERTED
═════════════════════════════════════════
```

---

### Step 10: Follow-up suggestions

After the deploy report, suggest relevant next steps:

- If production URL was verified: "Run `/canary <url>` for extended 10-minute monitoring."
- If new features were shipped: "Run `/document-release` to update project docs."

---

## Important rules

- **Never force push.** Use `gh pr merge` (it's safe).
- **Never skip CI.** Failing checks = stop.
- **Single-pass production check.** For extended monitoring, use `/canary`.
- **Revert is always an option.** At every failure point, offer revert as an escape hatch.
- **Delete the feature branch** after merge (via `--delete-branch`).
- **The goal**: user types `/land-and-deploy`, next thing they see is the deploy report.

## Usage

```
/land-and-deploy                                    # Auto-detect PR, no canary URL
/land-and-deploy https://app.example.com            # Auto-detect PR + verify this URL
/land-and-deploy 123                                # Specific PR number
/land-and-deploy 123 https://app.example.com        # PR number + verification URL
```

## Related commands

- `/ship`: run this first to create the PR
- `/canary`: extended post-deploy monitoring loop
- `/review-pr`: review the PR before landing

$ARGUMENTS
