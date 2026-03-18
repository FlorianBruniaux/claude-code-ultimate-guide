---
name: pr-triage
description: >
  4-phase PR backlog management: audit open PRs, deep review selected ones, post validated
  review comments, and optionally create local worktrees for hands-on review. Args: "all"
  to review all, PR numbers to focus (e.g. "42 57"), "en"/"fr" for language, no arg = audit only.
tags: [github, pr, triage, review, maintainer, multi-agent, worktree]
---

# PR Triage

4-phase workflow for maintainers: automated audit of all open PRs, opt-in deep review via parallel agents, validated comment posting, and optional worktree setup for local review.

## When to Use This Skill

| Skill | Usage | Output |
|-------|-------|--------|
| `/pr-triage` | Sort, review, and comment on a PR backlog | Triage table + reviews + posted comments |
| `/review-pr` | Review a single PR in depth | Inline PR review |

**Triggers**:
- Manually: `/pr-triage` or `/pr-triage all` or `/pr-triage 42 57`
- Proactively: when >5 PRs open without review, or stale PR >14 days detected

---

## Language

- Check the argument passed to the skill
- If `en` or `english` → tables and summary in English
- If `fr`, `french`, or no argument → French (default)
- Note: GitHub comments (Phase 3) are ALWAYS in English (international audience)

---

## Configuration

Thresholds used throughout the workflow. Edit to match your project:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `staleness_days` | 14 | Days without activity before flagging as stale |
| `overlap_threshold` | 50% | Shared files % to flag as overlapping |
| `cluster_min_prs` | 3 | Author PR count to trigger cluster suggestion |
| `xl_cutoff_additions` | 1000 | Additions above which a PR is classified XL |
| `xl_cutoff_files` | 10 | Changed files above which a PR is "too large" |

---

## Preconditions

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

If either fails, stop and explain what is missing.

---

## Phase 1 — Audit (always executed)

### Data Gathering (parallel commands)

```bash
# Repo identity
gh repo view --json nameWithOwner -q .nameWithOwner

# Open PRs with full metadata (body for cross-reference issues)
gh pr list --state open --limit 50 \
  --json number,title,author,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,mergeable,reviewDecision,statusCheckRollup,body

# Collaborators (to distinguish internal from external PRs)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Collaborators fallback**: if `gh api .../collaborators` returns 403/404:
```bash
# Extract authors from last 10 merged PRs
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
If still ambiguous, ask via `AskUserQuestion`.

For each PR, fetch existing reviews AND changed files:

```bash
gh api "repos/{owner}/{repo}/pulls/{num}/reviews" \
  --jq '[.[] | .user.login + ":" + .state] | join(", ")'

# Changed files (required for overlap detection)
gh pr view {num} --json files --jq '[.files[].path] | join(",")'
```

**Rate-limiting note**: fetching files requires N API calls (1 per PR). For repos with 20+ PRs, prioritize candidates for overlap detection (same functional domain, same author).

**Note**: `author` is an object `{login: "..."}` — always extract `.author.login`.

### Analysis

**Size classification**:
| Label | Additions |
|-------|-----------|
| XS | < 50 |
| S | 50–200 |
| M | 200–500 |
| L | 500–1000 |
| XL | > 1000 |

Size format: `+{additions}/-{deletions}, {files} files ({label})`

**Detections**:
- **Overlaps**: compare file lists across PRs — if >50% files in common → cross-reference
- **Clusters**: author with 3+ open PRs → suggest review order (smallest first)
- **Staleness**: no activity for >14 days → flag "stale"
- **CI status**: via `statusCheckRollup` → `clean` / `unstable` / `dirty`
- **Reviews**: approved / changes_requested / none

**PR ↔ Issue linking**:
- Scan each PR `body` for `fixes #N`, `closes #N`, `resolves #N` (case-insensitive)
- If found, display in the table: `Fixes #42` in the Action/Status column

**Categorization**:

_Internal PRs_: author in collaborators list

_External — Ready_: additions ≤ 1000 AND files ≤ 10 AND `mergeable` ≠ `CONFLICTING` AND CI clean/unstable

_External — Problematic_: any of:
- additions > 1000 OR files > 10
- OR `mergeable` == `CONFLICTING` (merge conflict)
- OR CI dirty (statusCheckRollup contains failures)
- OR overlap with another open PR (>50% shared files)

### Output — Triage Table

```
## Open PRs ({count})

### Internal PRs
| PR | Title | Size | CI | Status |
| -- | ----- | ---- | -- | ------ |

### External — Ready for Review
| PR | Author | Title | Size | CI | Reviews | Action |
| -- | ------ | ----- | ---- | -- | ------- | ------ |

### External — Problematic
| PR | Author | Title | Size | Problem | Recommended Action |
| -- | ------ | ----- | ---- | ------- | ------------------ |

### Summary
- Quick wins: {XS/S PRs ready to merge}
- Risks: {overlaps, XL sizes, CI dirty}
- Clusters: {authors with 3+ PRs}
- Stale: {PRs with no activity >14d}
- Overlaps: {PRs touching the same files}
```

0 PRs → display `No open PRs.` and stop.

### Navigation Post-Phase 1

After displaying the triage table, ask via `AskUserQuestion`:

```
question: "What would you like to do next?"
header: "Next Step"
options:
  - label: "Phase 2 — Deep review"
    description: "Analyze selected PRs with code-reviewer agents and generate comment drafts"
  - label: "Phase 4 — Create worktrees"
    description: "Set up local worktrees for hands-on review (skips comment generation)"
  - label: "Done"
    description: "End the workflow here"
```

Note: Phase 3 (posting comments) is NOT offered here — it requires the drafts generated in Phase 2. If the user picks "Phase 4", Phase 2 → Phase 3 remains accessible afterward.

### Automatic Copy

After displaying the triage table, copy to clipboard using platform-appropriate command:

```bash
# Detect platform and copy
UNAME=$(uname -s)
if [ "$UNAME" = "Darwin" ]; then
  pbcopy <<'EOF'
{full triage table}
EOF
elif command -v xclip &>/dev/null; then
  echo "{full triage table}" | xclip -selection clipboard
elif command -v wl-copy &>/dev/null; then
  echo "{full triage table}" | wl-copy
elif command -v clip.exe &>/dev/null; then
  echo "{full triage table}" | clip.exe
fi
```

Confirm: `Triage table copied to clipboard.` (EN) / `Tableau copié dans le presse-papier.` (FR)

---

## Phase 2 — Deep Review (opt-in)

### PR Selection

**If argument passed**:
- `"all"` → all external PRs
- Numbers (`"42 57"`) → only those PRs
- No argument → propose via `AskUserQuestion`

**If no argument**, display:

```
question: "Which PRs do you want to review in depth?"
header: "Deep Review"
multiSelect: true
options:
  - label: "All external"
    description: "Review {N} external PRs with parallel code-reviewer agents"
  - label: "Problematic only"
    description: "Focus on {M} risky PRs (CI dirty, too large, overlaps)"
  - label: "Ready only"
    description: "Review {K} PRs ready to merge"
  - label: "Skip"
    description: "Stop here — audit only"
```

**Draft PR behavior**:
- Draft PRs are EXCLUDED from "All external" and "Ready only"
- Draft PRs are INCLUDED in "Problematic only" (they need attention)
- To review a draft: type its number explicitly (e.g. `42`)

If "Skip" → end workflow.

### Executing Reviews

For each selected PR, launch a `code-reviewer` agent via **Task tool in parallel**:

```
subagent_type: code-reviewer
model: sonnet
prompt: |
  Review PR #{num}: "{title}" by @{author}

  **Metadata**: +{additions}/-{deletions}, {changedFiles} files ({size_label})
  **CI**: {ci_status} | **Reviews**: {existing_reviews} | **Draft**: {isDraft}

  **PR Body**:
  {body}

  **Diff**:
  {gh pr diff {num} output}

  Apply your security and architecture expertise. Use the project-specific checklist
  from the SKILL.md Configuration section if available.

  Return structured review:
  ### Critical Issues
  ### Important Issues
  ### Suggestions
  ### What's Good

  Be specific: quote file:line, explain the issue, suggest the fix.
```

**Fallback if parallel agents unavailable**: run reviews sequentially, one PR at a time. Notify user: `Running sequential review (parallel agents not available).`

Fetch diff via:
```bash
gh pr diff {num}
gh pr view {num} --json body,title,author -q '{body: .body, title: .title, author: .author.login}'
```

Aggregate all reports. Display a summary after all reviews complete.

---

## Phase 3 — Comments (mandatory validation)

### Draft Generation

For each reviewed PR, generate a GitHub comment using the template `templates/review-comment.md`.

**Rules**:
- Language: **English** (international audience)
- Tone: professional, constructive, factual
- Always include at least 1 positive point
- Quote code lines when relevant (format `file:42`)

### Display and Validation

**Display ALL drafted comments** in format:

```
---
### Draft — PR #{num}: {title}

{full comment}

---
```

Then request validation via `AskUserQuestion`:

```
question: "These comments are ready. Which ones do you want to post?"
header: "Post Comments"
multiSelect: true
options:
  - label: "All ({N} comments)"
    description: "Post on all reviewed PRs"
  - label: "PR #{x} — {title_truncated}"
    description: "Post only on this PR"
  - label: "None"
    description: "Cancel — post nothing"
```

(Generate one option per PR + "All" + "None")

### Posting

For each validated comment:

```bash
gh pr comment {num} --body-file - <<'REVIEW_EOF'
{comment}
REVIEW_EOF
```

Confirm each post: `Comment posted on PR #{num}: {title}`

If "None" → `No comments posted. Workflow complete.`

---

## Project-Specific Checklist

Add your stack's checklist to the agent prompt in Phase 2. Examples by stack:

**Node.js / TypeScript**:
- No `any` type without explicit justification
- `async/await` error handling (try/catch or `.catch()`)
- No unhandled promise rejections
- Input validation at API boundaries

**Python**:
- Type hints on all public functions
- Exception specificity (no bare `except:`)
- Resource cleanup (`with` statements, context managers)
- No mutable default arguments

**Rust**:
- `Result<T, E>` with `.context()` for error chain (no `.unwrap()` in production code)
- No `clone()` on hot paths without justification
- `lazy_static!` or `once_cell` for static regex
- Lifetime annotations where ownership is non-obvious

**Go**:
- Explicit error handling (no `_` discard without comment)
- `defer` for resource cleanup
- Context propagation in concurrent code
- No goroutine leaks

**Generic** (stack-agnostic):
- No secrets or hardcoded credentials
- New public functions have tests
- Breaking changes documented in PR body
- Dependencies added have clear justification

---

---

## Phase 4 — Worktree Setup (opt-in)

Creates local git worktrees for each selected PR so you can run, test, or review code without switching branches.

**Never triggered automatically** — only via Phase 1 navigation or explicit user request.

### Step 4.1 — Cache check + PR list

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
  [1] #123 — feat(auth): add OAuth2 support
      Branch: feat/oauth2  |  Size: M  |  CI: clean

### Bob Chen (@bob)
  [2] #456 — fix(api): handle empty response
      Branch: fix/empty-response  |  Size: S  |  CI: dirty ⚠️
```

### Step 4.2 — Selection

Ask via `AskUserQuestion` (multiSelect):

```
question: "Which PRs do you want to create a worktree for?"
header: "Worktree Setup"
multiSelect: true
options:
  - label: "All"
    description: "Create worktrees for all {N} listed PRs"
  - label: "[1] #{num} — {title} ({author})"
    description: "Branch: {branch} | Size: {size} | CI: {ci}"
  - label: "None"
    description: "Cancel — return to menu"
```

If "None" → end Phase 4.

### Step 4.3 — Sequential creation

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

# Optional: symlink node_modules (Node.js projects — avoids reinstall)
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

### Step 4.4 — Update existing worktrees

If any `STATUS:EXISTING` collected, offer a single prompt:

```
Existing worktrees detected:
  PR #123 — .worktrees/feat-oauth2
  PR #789 — .worktrees/fix-session-leak

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
⚠️ PR #123 — --ff-only failed (branches have diverged)
   Manual fix: cd .worktrees/feat-oauth2 && git pull --rebase
```

### Step 4.5 — Summary

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

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| 0 open PRs | Display `No open PRs.` + stop |
| Draft PR | Show in table, skip for review unless explicitly selected |
| Unknown CI | Display `?` in CI column |
| Review agent timeout | Show partial error, continue with others |
| `gh pr diff` empty | Skip this PR, notify user |
| Very large PR (>5000 additions) | Warn: "Partial review, diff truncated" |
| Collaborators API 403/404 | Fallback to last 10 merged PR authors |
| Parallel agents unavailable | Run sequential reviews, notify user |
| Phase 4: `.gitignore` missing `.worktrees/` | Fail-fast, show fix instructions, stop Phase 4 |
| Phase 4: branch already checked out | Warn with `git worktree list` hint, skip this PR |
| Phase 4: stale cache (>30min) | Re-fetch PR list before creating worktrees |
| Phase 4: PR modifies `package.json` | Warn in summary to run install manually |
| Phase 4: 0 non-draft PRs | Display message + end Phase 4 |

---

## Notes

- Always derive owner/repo via `gh repo view`, never hardcode
- Use `gh` CLI (not `curl` GitHub API) except for collaborators list
- `statusCheckRollup` can be null → treat as `?`
- `mergeable` can be `MERGEABLE`, `CONFLICTING`, or `UNKNOWN` → treat `UNKNOWN` as `?`
- Never post without explicit user validation in chat
- Drafted comments must be visible BEFORE any `gh pr comment`

---

## Related: /review-pr

| | `/pr-triage` | `/review-pr` |
|--|-------------|--------------|
| **Scope** | Full PR backlog | Single PR |
| **Use when** | Catching up after accumulation, periodic triage | Reviewing a specific incoming PR |
| **Phases** | 4 (audit + deep review + comments + worktrees) | 1 (review only) |
| **Agents** | Parallel sub-agents per PR | Single session |
| **Output** | Triage table + review reports + GitHub comments + local worktrees | Inline review |
| **Validation** | AskUserQuestion before posting | Manual decision |

**Decision rule**: use `/pr-triage` for backlog triage (5+ PRs), `/review-pr` for focused review of a single PR. Use Phase 4 when you want to run the code locally rather than just reading the diff.
