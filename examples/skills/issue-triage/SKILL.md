---
name: issue-triage
description: >
  3-phase issue backlog management: audit open issues, deep analyze selected ones, draft and execute
  triage actions with mandatory validation. Args: "all" to analyze all, issue numbers to focus
  (e.g. "42 57"), "en"/"fr" for language, no arg = audit only in French.
tags: [github, issue, triage, maintainer, multi-agent]
---

# Issue Triage

3-phase workflow for maintainers: automated audit of all open issues, opt-in deep analysis via parallel agents, and validated triage actions (comments, labels, closures).

## When to Use This Skill

| Skill | Usage | Output |
|-------|-------|--------|
| `/issue-triage` | Sort, analyze, and act on an issue backlog | Triage tables + analysis + executed actions |
| `/pr-triage` | Sort, review, and comment on a PR backlog | Triage table + reviews + posted comments |

**Triggers**:
- Manually: `/issue-triage` or `/issue-triage all` or `/issue-triage 42 57`
- Proactively: when >10 open issues without label, or stale issues >30 days detected

---

## Language

- Check the argument passed to the skill
- If `en` or `english` → tables and summary in English
- If `fr`, `french`, or no argument → French (default)
- Note: GitHub comments and labels (Phase 3) are ALWAYS in English (international audience)

---

## Configuration

Thresholds used throughout the workflow. Edit to match your project:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `staleness_days` | 30 | Days without activity before flagging as stale |
| `very_stale_days` | 90 | Days without activity before flagging as very stale |
| `jaccard_threshold` | 60% | Minimum Jaccard similarity to flag two issues as duplicates |
| `closed_compare_count` | 20 | Number of recent closed issues to compare for duplicate detection |
| `open_limit` | 100 | Maximum open issues to fetch and analyze |

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

# Open issues (exclude PRs, limit 100)
gh issue list --state open --limit 100 \
  --json number,title,author,createdAt,updatedAt,labels,body,comments,assignees,milestone

# Recent closed issues (for duplicate detection)
gh issue list --state closed --limit 20 \
  --json number,title,body,labels,stateReason

# Open PRs (bodies for cross-reference detection)
gh pr list --state open --limit 50 --json number,title,body

# Collaborators (to distinguish reporter types)
gh api "repos/{owner}/{repo}/collaborators" --jq '.[].login'
```

**Collaborators fallback**: if `gh api .../collaborators` returns 403/404:
```bash
# Extract authors from last 10 merged PRs
gh pr list --state merged --limit 10 --json author --jq '.[].author.login' | sort -u
```
If still ambiguous, ask via `AskUserQuestion`.

**Note**: `comments` field in `gh issue list --json comments` returns the count, not content. For Phase 2, fetch full content separately: `gh issue view {num} --json comments`.

### Analysis Dimensions

Run all 6 dimensions for each open issue:

#### 1. Categorization

Classify each issue by reading `title` + first 200 chars of `body`:

| Category | Label | Criteria |
|----------|-------|----------|
| Bug | `bug` | Describes broken behavior, unexpected output, crash |
| Feature Request | `enhancement` | Asks for new functionality |
| Question / Support | `question` | User asking how something works |
| Documentation | `documentation` | Missing or incorrect docs |
| Out of Scope | `wontfix` | Clearly outside project boundaries |
| Unclear | `needs-info` | Body empty, too vague to categorize |

If body is empty → category is always `Unclear` (never assume).

#### 2. Cross-reference to PRs

Scan each open PR body for references to the issue number:
- Patterns: `fixes #N`, `closes #N`, `resolves #N`, `fix #N`, `close #N` (case-insensitive, `N` = issue number)
- Use regex locally on the `body` fields already fetched — do NOT make N additional API calls
- If found: flag issue as "PR-linked" with PR number

#### 3. Duplicate Detection via Jaccard Similarity

**Algorithm (self-contained — no external library)**:

For each open issue, compute Jaccard similarity against all other open issues AND the 20 most recent closed issues.

```
Step 1 — Normalize title + first 300 chars of body:
  - Lowercase the full text
  - Strip category prefixes: "feat:", "fix:", "bug:", "chore:", "docs:", "test:", "refactor:"
  - Remove punctuation: .,!?;:'"()[]{}-_/\@#

Step 2 — Tokenize:
  - Split on whitespace
  - Remove stop words: the a an is in on to for of and or with this that it can not no be
  - Remove tokens shorter than 3 characters

Step 3 — Compute Jaccard:
  tokens_A = set of tokens from issue A
  tokens_B = set of tokens from issue B
  jaccard = |tokens_A ∩ tokens_B| / |tokens_A ∪ tokens_B|

Step 4 — Flag:
  - If jaccard >= 0.60: mark as potential duplicate
  - Report: "Similar to #N (Jaccard: 0.72)"
  - Keep the OLDER issue as canonical; newer = duplicate candidate
```

Jaccard is computed at runtime using the fetched data — no API calls beyond Phase 1 gather.

#### 4. Risk Classification

Assign Red / Yellow / Green based on signals in title + body:

| Level | Color | Criteria |
|-------|-------|----------|
| Critical | Red | Security vulnerability, data loss, regression blocking users, crash in production |
| Needs Attention | Yellow | Missing validation, performance degradation, breaking change undocumented, Unclear with no response for >7 days |
| Normal | Green | Everything else |

#### 5. Staleness

| Status | Criterion |
|--------|-----------|
| Active | Updated within 30 days |
| Stale | No activity 30–90 days |
| Very Stale | No activity >90 days |

Use `updatedAt` field. Staleness does NOT depend on comments count — a commented-on issue with old `updatedAt` is still stale.

#### 6. Recommendations

One recommended action per issue:

| Situation | Action |
|-----------|--------|
| Category = Unclear, body empty | Comment requesting details |
| Jaccard >= 0.60 with known issue | Close as duplicate, link original |
| Very stale + no assignee | Comment requesting status, suggest close |
| Risk = Red | Pin to top of triage, escalate immediately |
| Category = OOS | Close with explanation |
| PR-linked | No action needed (tracked via PR) |
| Normal + labeled | No action needed |

### Output — Triage Tables

```
## Open Issues ({count})

### Critical — Immediate Attention (Risk: Red)
| # | Title | Category | Reporter | Days Open | Action |
|---|-------|----------|----------|-----------|--------|

### PR-Linked (tracked in open PRs)
| # | Title | Category | PR | Days Open |
|---|-------|----------|----|-----------|

### Active Issues
| # | Title | Category | Labels | Reporter | Days | Action |
|---|-------|----------|--------|----------|------|--------|

### Duplicate Candidates
| # | Title | Similar To | Jaccard | Action |
|---|-------|------------|---------|--------|

### Stale Issues
| # | Title | Category | Last Activity | Reporter | Action |
|---|-------|----------|---------------|----------|--------|

### Summary
- Total open: {N}
- Critical (Red): {count}
- PR-linked: {count}
- Duplicate candidates: {count}
- Stale (30–90d): {count}
- Very stale (>90d): {count}
- Unlabeled: {count}
- Recommended actions: {comment: N, label: N, close: N}
```

0 issues → display `No open issues.` and stop.

**Protection rules** (apply to all phases):
- Never close an issue authored by a collaborator without explicit user confirmation
- Never re-label an issue that already has labels (only add missing labels)
- If body is empty → always request details before any other action
- Never auto-close a Red issue without user confirmation

### Automatic Copy

After displaying the triage tables, copy to clipboard using platform-appropriate command:

```bash
UNAME=$(uname -s)
if [ "$UNAME" = "Darwin" ]; then
  pbcopy <<'EOF'
{full triage tables}
EOF
elif command -v xclip &>/dev/null; then
  echo "{full triage tables}" | xclip -selection clipboard
elif command -v wl-copy &>/dev/null; then
  echo "{full triage tables}" | wl-copy
elif command -v clip.exe &>/dev/null; then
  echo "{full triage tables}" | clip.exe
fi
```

Confirm: `Triage tables copied to clipboard.` (EN) / `Tableaux copiés dans le presse-papier.` (FR)

---

## Phase 2 — Deep Analysis (opt-in)

### Issue Selection

**If argument passed**:
- `"all"` → all issues with recommended actions
- Numbers (`"42 57"`) → only those issues
- No argument → propose via `AskUserQuestion`

**If no argument**, display:

```
question: "Which issues do you want to analyze in depth?"
header: "Deep Analysis"
multiSelect: true
options:
  - label: "All ({N} issues with recommended actions)"
    description: "Launch parallel analysis agents for each actionable issue"
  - label: "Critical only ({M} Red issues)"
    description: "Focus on high-risk issues requiring immediate action"
  - label: "Duplicate candidates ({K} issues)"
    description: "Verify Jaccard similarity with full body + comments"
  - label: "Stale only ({J} stale issues)"
    description: "Decide which stale issues to close vs. revive"
  - label: "Skip"
    description: "Stop here — audit only"
```

If "Skip" → end workflow.

### Executing Analysis

For each selected issue, launch an analysis agent via **Task tool in parallel**:

```
subagent_type: general
model: sonnet
prompt: |
  Analyze GitHub issue #{num}: "{title}"

  **Metadata**: Category={category}, Risk={risk}, Days open={days}, Labels={labels}
  **Reporter**: @{author} ({collaborator? "collaborator" : "external"})
  **Assignees**: {assignees or "none"}

  **Body**:
  {body}

  **Comments** (fetch via: gh issue view {num} --json comments):
  {comments[].body — truncate at 5000 chars total}

  **Duplicate candidates**: {jaccard_results or "none found"}
  **Linked PRs**: {pr_refs or "none"}

  Tasks:
  1. Verify the category assigned in Phase 1 (correct? suggest alternative if not)
  2. If duplicate candidate: confirm or deny similarity with rationale
  3. If Unclear/needs-info: identify exactly what information is missing
  4. Suggest the most appropriate action with exact text if a comment is needed
  5. Estimate effort to fix if it's a Bug or Feature Request (XS/S/M/L/XL)

  Return structured output:
  ### Verification
  ### Duplicate Analysis
  ### Missing Information
  ### Recommended Action
  ### Effort Estimate
```

**Fallback if parallel agents unavailable**: run analysis sequentially, one issue at a time. Notify user: `Running sequential analysis (parallel agents not available).`

Fetch full comments via:
```bash
gh issue view {num} --json comments --jq '.comments[].body'
```

Aggregate all reports. Display a summary after all analyses complete.

---

## Phase 3 — Actions (mandatory validation)

### Draft Generation

For each analyzed issue, generate the appropriate action using the template `templates/issue-comment.md`.

**3 action types**:

| Type | Command | When |
|------|---------|------|
| Comment | `gh issue comment {num} --body-file -` | Needs info, stale ping, OOS explanation |
| Label | `gh issue edit {num} --add-label "{label}"` | Unlabeled issue with clear category |
| Close | `gh issue close {num} --reason "not planned"` | Duplicate, OOS, very stale |

**Rules**:
- Language for comments: **English** (international audience)
- Labels added: use existing repo labels only (fetch with `gh label list`)
- Close reason: `"not planned"` for OOS/duplicate, `"completed"` only if a fix was merged
- Never post a comment AND close in the same action without user seeing both drafts
- Always attach a comment when closing (explain why)

### Display and Validation

**Display ALL drafted actions** in format:

```
---
### Draft — Issue #{num}: {title}

**Action**: {Comment / Label / Close + Comment}
**Reason**: {1 sentence}

{full comment text if applicable}

---
```

Then request validation via `AskUserQuestion`:

```
question: "These actions are ready. Which ones do you want to execute?"
header: "Execute Triage Actions"
multiSelect: true
options:
  - label: "All ({N} actions)"
    description: "Execute all drafted triage actions"
  - label: "Issue #{x} — {title_truncated} ({action_type})"
    description: "Execute only this action"
  - label: "None"
    description: "Cancel — execute nothing"
```

(Generate one option per issue + "All" + "None")

### Execution

For each validated action:

```bash
# Comment
gh issue comment {num} --body-file - <<'TRIAGE_EOF'
{comment}
TRIAGE_EOF

# Label
gh issue edit {num} --add-label "{label}"

# Close with comment
gh issue comment {num} --body-file - <<'TRIAGE_EOF'
{close comment}
TRIAGE_EOF
gh issue close {num} --reason "not planned"
```

Confirm each action: `Action executed on issue #{num}: {title}`

If "None" → `No actions executed. Workflow complete.`

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| 0 open issues | Display `No open issues.` + stop |
| Body empty | Category = Unclear, action = request details, never assume |
| Collaborator as reporter | Protect from auto-close, flag explicitly in table |
| Jaccard inconclusive (0.55–0.65) | Flag as "possible duplicate — verify manually" |
| Label not in repo | Skip label action, notify user to create the label first |
| Issue already closed during workflow | Skip silently, note in summary |
| `gh api .../collaborators` 403/404 | Fallback to last 10 merged PR authors |
| Parallel agents unavailable | Run sequential analysis, notify user |
| Very large body (>5000 chars) | Truncate to 5000 chars with `[truncated]` note |
| Milestone assigned | Include in table, never close milestoned issues without confirmation |

---

## Notes

- Always derive owner/repo via `gh repo view`, never hardcode
- Use `gh` CLI (not `curl` GitHub API) except for collaborators list
- `comments` in `gh issue list --json comments` = count only; full content requires `gh issue view {num} --json comments`
- Never execute any action without explicit user validation in chat
- Drafted actions must be visible BEFORE any `gh issue comment` or `gh issue close`
- Jaccard is computed locally — no external API, no library, pure set operations on fetched data
- Signature on all comments: `*Triaged via Claude Code /issue-triage*`

---

## Related: /pr-triage

| | `/issue-triage` | `/pr-triage` |
|--|----------------|--------------|
| **Scope** | Issue backlog | PR backlog |
| **Use when** | Catching up on reporter feedback, periodic issue cleanup | Catching up after PR accumulation |
| **Phases** | 3 (audit + deep analysis + actions) | 3 (audit + deep review + comments) |
| **Agents** | Parallel sub-agents per issue | Parallel sub-agents per PR |
| **Duplicate detection** | Jaccard similarity on title+body | File overlap % between PRs |
| **Actions** | Comment / label / close | GitHub review comment |
| **Validation** | AskUserQuestion before executing | AskUserQuestion before posting |

**Decision rule**: use `/issue-triage` for issue backlog management, `/pr-triage` for code review backlog.
