# PR triage: Phase 4 worktree setup

Loaded on demand by `pr-triage` when the user asks for local worktrees. Heading levels below keep the original Phase 4 numbering.

## Phase 4: Worktree Setup (opt-in)

Creates local git worktrees for each selected PR so you can run, test, or review code without switching branches.

**Never triggered automatically.** Only via Phase 1 navigation or explicit user request.

### Step 4.1: Cache check + PR list

**Cache check**: before using data from Phase 1, verify it is less than 30 minutes old:

```bash
CACHE_FILE="/tmp/pr-triage-prs.json"
CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || echo 0) ))
if [ "$CACHE_AGE" -gt 1800 ]; then
  echo "STALE_CACHE"
fi
```

If `STALE_CACHE` → re-run the Phase 1 data gathering before continuing.

**Filter**: exclude Draft PRs and bot PRs (Dependabot, renovate, etc.):

```bash
python3 -c "
import json
prs = json.load(open('/tmp/pr-triage-prs.json'))
filtered = [
  p for p in prs
  if not p['isDraft']
  and not any(bot in p['author']['login'].lower() for bot in ['dependabot', 'renovate', 'snyk'])
]
import sys; json.dump(filtered, sys.stdout, indent=2)
" > /tmp/pr-triage-phase4.json
```

If 0 PRs after filtering → display `No reviewable PRs available for worktree (all are drafts or bots).` + end Phase 4.

**Display grouped by author** (use display name if available, fallback to login):

```
## PRs available for worktree (non-draft)

### Alice Martin (@alice)
  [1] #123: feat(auth): add OAuth2 support
      Branch: feat/oauth2  |  Size: M  |  CI: clean

### Bob Chen (@bob)
  [2] #456: fix(api): handle empty response
      Branch: fix/empty-response  |  Size: S  |  CI: dirty ⚠️
```

### Step 4.2: Selection

Ask via `AskUserQuestion` (multiSelect):

```
question: "Which PRs do you want to create a worktree for?"
header: "Worktree Setup"
multiSelect: true
options:
  - label: "All"
    description: "Create worktrees for all {N} listed PRs"
  - label: "[1] #{num}: {title} ({author})"
    description: "Branch: {branch} | Size: {size} | CI: {ci}"
  - label: "None"
    description: "Cancel, return to menu"
```

If "None" → end Phase 4.

### Step 4.3: Sequential creation

**Execution model**: Claude runs **one bash command per PR**, reads its output, updates its internal state (created / existing / failed), then moves to the next. Never a bash loop wrapping all PRs.

For each selected PR, Claude sets variables explicitly then runs:

```bash
PR_NUM="123"
BRANCH_NAME="feat/oauth2"
WORKTREE_NAME="${BRANCH_NAME//\//-}"
REPO_ROOT="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
WORKTREE_DIR="$REPO_ROOT/.worktrees/$WORKTREE_NAME"

# Already exists?
if [ -d "$WORKTREE_DIR" ]; then
  echo "STATUS:EXISTING:$PR_NUM:$WORKTREE_DIR"
  exit 0
fi

# .gitignore check (fail-fast)
if ! grep -qE "^\.worktrees/?$" "$REPO_ROOT/.gitignore" 2>/dev/null; then
  echo "STATUS:GITIGNORE_MISSING:$PR_NUM"
  exit 1
fi

# Fetch remote branch
if ! git fetch origin "$BRANCH_NAME" 2>/tmp/wt-fetch-$PR_NUM.log; then
  echo "STATUS:FETCH_FAILED:$PR_NUM"
  exit 1
fi

mkdir -p "$REPO_ROOT/.worktrees"

# Create worktree (branch local exists or not)
if ! git branch --list "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
  git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR" "origin/$BRANCH_NAME" \
    2>/tmp/wt-err-$PR_NUM.log
else
  git worktree add "$WORKTREE_DIR" "$BRANCH_NAME" \
    2>/tmp/wt-err-$PR_NUM.log
fi

if [ $? -ne 0 ]; then
  if grep -q "already checked out" /tmp/wt-err-$PR_NUM.log; then
    echo "STATUS:ALREADY_CHECKED_OUT:$PR_NUM"
  else
    echo "STATUS:CREATE_FAILED:$PR_NUM"
  fi
  exit 1
fi

# Optional: symlink node_modules (Node.js projects, avoids reinstall)
[ -d "$REPO_ROOT/node_modules" ] && ln -sf "$REPO_ROOT/node_modules" "$WORKTREE_DIR/node_modules"

# Copy project-specific files listed in .worktreeinclude (if present)
if [ -f "$REPO_ROOT/.worktreeinclude" ]; then
  while IFS= read -r entry || [ -n "$entry" ]; do
    [[ "$entry" =~ ^#.*$ || -z "$entry" ]] && continue
    entry="$(echo "$entry" | xargs)"
    [ -e "$REPO_ROOT/$entry" ] && {
      mkdir -p "$(dirname "$WORKTREE_DIR/$entry")"
      cp -R "$REPO_ROOT/$entry" "$WORKTREE_DIR/$entry"
    }
  done < "$REPO_ROOT/.worktreeinclude"
fi

echo "STATUS:CREATED:$PR_NUM:$WORKTREE_DIR"
```

**Status handling** (Claude maintains internal state between PRs):

| Status | Claude action |
|--------|--------------|
| `STATUS:CREATED:NUM:PATH` | Add to "created" list |
| `STATUS:EXISTING:NUM:PATH` | Add to "existing" list → offer pull in Step 4.4 |
| `STATUS:FETCH_FAILED:NUM` | Warn + continue to next PR |
| `STATUS:GITIGNORE_MISSING:NUM` | Fail-fast: show fix instructions + stop Phase 4 |
| `STATUS:ALREADY_CHECKED_OUT:NUM` | Warn: "Branch already checked out in another worktree. Run `git worktree list` to locate it." |
| `STATUS:CREATE_FAILED:NUM` | Warn + continue to next PR |

**GITIGNORE_MISSING fix instructions**:
```
.worktrees/ is not in .gitignore. Add it to avoid accidentally committing worktree files:
  echo ".worktrees/" >> .gitignore
Then re-run Phase 4.
```

### Step 4.4: Update existing worktrees

If any `STATUS:EXISTING` collected, offer a single prompt:

```
Existing worktrees detected:
  PR #123: .worktrees/feat-oauth2
  PR #789: .worktrees/fix-session-leak

- [Pull all] git pull --ff-only in all existing worktrees
- [#123] Pull PR #123 only
- [Skip] Leave as-is
```

For each selected pull, Claude runs (one command per worktree):

```bash
PR_NUM="123"
BRANCH_NAME="feat/oauth2"
WORKTREE_DIR="/abs/path/.worktrees/feat-oauth2"

cd "$WORKTREE_DIR" && git pull origin "$BRANCH_NAME" --ff-only 2>/tmp/wt-pull-$PR_NUM.log
echo "PULL_STATUS:$?:$PR_NUM"
```

If `PULL_STATUS` ≠ 0:
```
⚠️ PR #123: --ff-only failed (branches have diverged)
   Manual fix: cd .worktrees/feat-oauth2 && git pull --rebase
```

### Step 4.5: Summary

```
## Worktrees ready

| PR | Author | Branch | Path | Status |
|----|--------|--------|------|--------|
| #123 | Alice | feat/oauth2 | .worktrees/feat-oauth2 | Created |
| #456 | Bob | fix/empty-response | .worktrees/fix-empty-response | Created |
| #789 | Alice | fix/session-leak | .worktrees/fix-session-leak | Updated (pull) |
| #321 | Carol | feat/chat | .worktrees/feat-chat | Fetch failed ⚠️ |

Note: if a PR modifies package.json, install dependencies manually:
  cd .worktrees/<branch-name> && npm install   # or pnpm/yarn/bun

Next steps:
  cd .worktrees/<branch-name>
  claude
```

### `.worktreeinclude` convention

Create a `.worktreeinclude` file at the repo root to list files Phase 4 copies into each new worktree. Useful for local config files not tracked in git:

```
# .worktreeinclude
.env.local
.env.test
config/local.json
```
