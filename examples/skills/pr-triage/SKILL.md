---
name: pr-triage
description: "Triage a pull request backlog in 4 phases: audit, deep code review, validated comments, and optional local worktrees. Use when triaging pull requests, catching up on pending code reviews, or managing a backlog of open PRs. Not for a single PR (use review-pr) or issues (use issue-triage)."
argument-hint: "[all | PR numbers] [en|fr]"
allowed-tools: Bash Read
effort: medium
disable-model-invocation: true
---

# PR triage

4-phase workflow for maintainers: automated audit of all open PRs, opt-in deep review via parallel agents, validated comment posting, and optional worktree setup for local review.

## When to use this skill

| Skill | Usage | Output |
|-------|-------|--------|
| `/pr-triage` | Sort, review, and comment on a PR backlog | Triage table + reviews + posted comments |
| `/review-pr` | Review a single PR in depth | Inline PR review |

**Invocation**: `/pr-triage` (audit only), `/pr-triage all`, or `/pr-triage 42 57`. Manual only, because Phase 3 posts comments and Phase 4 creates worktrees.

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

## Phase 1: Audit (always executed)

### Data Gathering (parallel commands)

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
gh pr list --state open --limit 50 \
  --json number,title,author,createdAt,updatedAt,additions,deletions,changedFiles,isDraft,mergeable,reviewDecision,statusCheckRollup,body
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

Save the `gh pr list` JSON to `/tmp/pr-triage-prs.json` (for example with `tee`); Phase 4 reads it from there.

**Collaborators fallback**: if `gh api .../collaborators` returns 403/404:
```bash
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
If still ambiguous, ask via `AskUserQuestion`.

For each PR, fetch reviews and changed files:

```bash
gh api "repos/{owner}/{repo}/pulls/{num}/reviews" \
  --jq '[.[] | .user.login + ":" + .state] | join(", ")'
gh pr view {num} --json files --jq '[.files[].path] | join(",")'
```

**Notes**: Fetching files requires 1 API call per PR; for 20+ PRs, prioritize overlap candidates. The `author` field is an object; always extract `.author.login`.

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
- **Overlaps**: compare file lists across PRs; if >50% files in common → cross-reference
- **Clusters**: author with 3+ open PRs → suggest review order (smallest first)
- **Staleness**: no activity for >14 days → flag "stale"
- **CI status**: via `statusCheckRollup` → `clean` / `unstable` / `dirty`
- **Reviews**: approved / changes_requested / none

**PR ↔ Issue linking**:
- Scan each PR `body` for `fixes #N`, `closes #N`, `resolves #N` (case-insensitive)
- If found, display in the table: `Fixes #42` in the Action/Status column

**Categorization**:

_Internal PRs_: author in collaborators list

_External, Ready_: additions ≤ 1000 AND files ≤ 10 AND `mergeable` ≠ `CONFLICTING` AND CI clean/unstable

_External, Problematic_: any of:
- additions > 1000 OR files > 10
- OR `mergeable` == `CONFLICTING` (merge conflict)
- OR CI dirty (statusCheckRollup contains failures)
- OR overlap with another open PR (>50% shared files)

### Output: Triage table

```
## Open PRs ({count})

### Internal PRs
| PR | Title | Size | CI | Status |
| -- | ----- | ---- | -- | ------ |

### External: Ready for Review
| PR | Author | Title | Size | CI | Reviews | Action |
| -- | ------ | ----- | ---- | -- | ------- | ------ |

### External: Problematic
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

### Navigation post-phase 1

After displaying the triage table, ask via `AskUserQuestion`:

```
question: "What would you like to do next?"
header: "Next Step"
options:
  - label: "Phase 2: Deep review"
    description: "Analyze selected PRs with code-reviewer agents and generate comment drafts"
  - label: "Phase 4: Create worktrees"
    description: "Set up local worktrees for hands-on review (skips comment generation)"
  - label: "Done"
    description: "End the workflow here"
```

Note: Phase 3 (posting comments) is NOT offered here, as it requires the drafts generated in Phase 2. If the user picks "Phase 4", Phase 2 → Phase 3 remains accessible afterward.

### Automatic copy

After displaying the triage table, copy to clipboard using platform-appropriate command:

```bash
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

## Phase 2: Deep Review (opt-in)

### PR selection

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
    description: "Stop here, audit only"
```

**Draft PR behavior**:
- Draft PRs are EXCLUDED from "All external" and "Ready only"
- Draft PRs are INCLUDED in "Problematic only" (they need attention)
- To review a draft: type its number explicitly (e.g. `42`)

If "Skip" → end workflow.

### Executing reviews

For each selected PR, launch a `code-reviewer` agent via the **Agent tool in parallel**:

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

## Phase 3: Comments (mandatory validation)

### Draft generation

For each reviewed PR, generate a GitHub comment using the template `templates/review-comment.md`.

**Rules**:
- Language: **English** (international audience)
- Tone: professional, constructive, factual
- Always include at least 1 positive point
- Quote code lines when relevant (format `file:42`)

### Display and validation

**Display ALL drafted comments** in format:

```
---
### Draft: PR #{num}: {title}

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
  - label: "PR #{x}: {title_truncated}"
    description: "Post only on this PR"
  - label: "None"
    description: "Cancel, post nothing"
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

## Project-specific checklist

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

## Phase 4: Worktree Setup (opt-in)

Creates local git worktrees for each selected PR so you can run, test, or review code without switching branches. **Never triggered automatically.** Only via the Phase 1 navigation or an explicit user request.

Read `${CLAUDE_SKILL_DIR}/references/worktree-setup.md` and follow it. It covers the cache check, PR selection, one `git worktree add` per PR, updating existing worktrees, the summary table, and the `.worktreeinclude` convention.

---

## Edge cases

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
