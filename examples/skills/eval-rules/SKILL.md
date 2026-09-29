---
name: eval-rules
description: "Audit Claude Code instruction rules in .claude/rules/ and ~/.claude/rules/: frontmatter, paths glob validity against real files, symlink load status, and day-to-day usefulness, then update rules with the user. Use for first-time rules setup, rules that apply too often or never, or periodic rules hygiene. Not for Codex .rules command-approval files."
allowed-tools: Read Glob Bash Edit
effort: medium
argument-hint: "[path to rules dir, default: .claude/rules/]"
---

# Rules Evaluator

Discover every Claude Code rule file, validate its structure and `paths` globs against the real project, then review each rule with the user so the rules directory ends in better shape than it started.

This skill covers Claude Code instruction rules in `.claude/rules/` and `~/.claude/rules/`. It does not cover Codex `.rules` files, which are Starlark command-approval policies, not instructions. See "Codex" below.

## When to Use

- Writing `.claude/rules/` files for the first time
- A rule never seems to apply, or applies to everything
- Moving `@` imports from CLAUDE.md into path-scoped rules
- Periodic hygiene: are these rules still accurate and useful?
- After onboarding to a new codebase

## Key Concepts

| Mechanism | When it loads |
|---|---|
| `@file` import in CLAUDE.md | Session start |
| Project rule without `paths` | Session start, same priority as `.claude/CLAUDE.md` |
| Project rule with `paths` | When Claude reads a file matching a pattern, not on every tool use |
| User rule in `~/.claude/rules/` | Applies to every project; loaded before project rules. Whether `paths` scoping applies to user rules is not documented: report it as unverified instead of assuming |

- All `.md` files under `.claude/rules/` are discovered recursively.
- `paths` is the only frontmatter field Claude Code reads from a rule; other fields are ignored without an error. It accepts a YAML list or a comma-separated string.
- If the frontmatter YAML does not parse, Claude Code ignores the frontmatter and loads the rule as if it had no `paths`, so a broken scoped rule silently becomes always-on.
- Brace expansion works (`"src/**/*.{ts,tsx}"`). A rule's whole `paths` list shares a budget of 1,000 expanded patterns and 4 MiB; a pattern over budget is used unexpanded and its literal braces match nothing.
- A `[` that cannot be read as a bracket expression (for example `photos [2024/**`) makes that pattern invalid: it matches nothing, the other patterns still work. Escape a literal bracket as `\[`.
- Project rules are skipped when `project` is excluded from `--setting-sources`.
- User rules load before project rules; neither overrides the other, so a conflict between them is a defect to resolve.

### Symlinked rules

- A symlink whose target is inside the working directory loads normally.
- A symlink whose target is outside the working directory is treated like an external import: it does not load until external imports are approved for the project, and after approval only the linked rules without `paths` load.
- A symlink to a network path (UNC share, `/net`, `/Network`) never loads. `\\wsl$` paths are not network paths.
- Circular symlinks are detected and handled.
- The documentation says the approval prompt appears only for `@path` imports, but Claude Code v2.1.284 fixed externally symlinked rules being skipped without any prompt and now asks for the same approval. On older versions, an external symlinked rule is skipped silently.

To share rules across projects without approval, put them in `~/.claude/rules/`.

## Scoring Criteria (12 pts per scoped rule)

| # | Criterion | Max | What is checked |
|---|---|---|---|
| 1 | **frontmatter parses** | 1 | Frontmatter, when present, is valid YAML (a broken block turns the rule always-on) |
| 2 | **paths field** | 2 | Present (1) + at least one non-empty pattern, as a list or comma-separated string (1) |
| 3 | **pattern validity** | 3 | Each pattern (up to 3 checked) matches at least one file and is not invalid or over the expansion budget |
| 4 | **scope** | 2 | Not dead (1) + not too broad: under 30% of the project files counted in Step 1 (1) |
| 5 | **content quality** | 3 | Clear title (1) + specific, actionable rules (1) + under 150 lines (1) |
| Bonus | **focus** | +1 | Under 15 rules in the file |

**Always-on rules** (no `paths`): score criteria 1 and 5 only (4 pts, plus bonus), mark them `always-on`, and decide in the interactive step whether they should be scoped.

**Symlinked rules**: add a load-status note (`loads`, `needs external-import approval`, `loads only after approval and only if unscoped`, `never loads: network path`). A rule that cannot load gets status `Fix` regardless of score.

**Thresholds:** Good >= 83%, Needs work 58-82%, Fix < 58%.

## Execution Instructions

### Step 1: Discovery

Find rule files with the file search capability:

```
.claude/rules/**/*.md
```

If an argument names another path, use it. Include `~/.claude/rules/` when the user asks for the full picture.

Count project files for the scope percentage from what the repository actually contains, not a fixed list of extensions:

```bash
git ls-files | wc -l          # inside a git repository
```

Outside git, count files while excluding `.git`, `node_modules`, build output and other ignored directories.

For every symlink in the rules tree, record the resolved target and whether it is inside the working directory or a network path.

Done when: every rule file is listed with its location (project or user), symlink status, and the project file count is recorded. If no rules directory exists, report it and stop.

### Step 2: Parse each rule

For each file: read it in full, extract the frontmatter, normalize `paths` (list or comma-separated string) into a list, classify the rule as scoped or always-on, and note parse errors, unknown fields (ignored by Claude Code), line count, and title.

Done when: every rule has a classification and a parse status.

### Step 3: Resolve patterns

For each pattern, resolve it against the project with the file search capability. Record the match count, up to 10 sample paths, and flag dead patterns, invalid `[` patterns, patterns whose brace expansion exceeds the budget, and patterns matching more than 30% of the counted files.

Done when: every pattern has a match count and a flag list.

### Step 4: Interactive review

Process rules one by one.

For a scoped rule, show the file, its patterns, match count and samples, then ask:

1. Is this scope right? (y / adjust)
2. Is this rule still useful day to day? (y / n / unsure)
3. Anything to add, remove or update in the content? (describe / skip)

For an always-on rule, show the file and line count, then ask:

1. This rule loads every session. Keep it always-on, scope it, or skip? (keep / scope / skip)
2. Is the content still accurate and useful? (y / n)

If the user chooses **scope**, propose a `paths` block derived from the rule content and apply it only after confirmation. Apply other confirmed edits directly and confirm each one. An "unsure" answer is recorded as "review in next audit" with no edit.

Done when: every rule has a recorded answer (confirmed, edited, flagged stale, unsure, or skipped).

### Step 5: Report

```
# Rules Audit: [project]
Date: [today] | Scanned: N rules (X scoped, Y always-on, Z symlinked)

| Status | Count |
|--------|-------|
| Good | N |
| Needs work | N |
| Fix | N |
| Always-on | N |
| Cannot load (symlink or network) | N |
| User confirmed useful | N |
| User flagged for update | N |
| User marked stale | N |

### payments.md (11/12) [scoped]
paths: `**/payments/**`, `src/billing/**`
Matches: 12 files (3.5% of 340 tracked files)

| Criterion | Score | Notes |
|---|---|---|
| frontmatter parses | 1/1 | ok |
| paths field | 2/2 | 2 patterns |
| pattern validity | 3/3 | all match |
| scope | 2/2 | well scoped |
| content quality | 2/3 | 158 lines |
```

End with a change summary: edits applied, rules flagged stale. Never delete a rule without an explicit "yes, delete it".

Done when: the report covers every rule found in Step 1.

## Codex

Codex has no equivalent of `.claude/rules/`. When the request is about Codex:

- **Instructions**: Codex reads `AGENTS.md` (or `AGENTS.override.md`) from the Codex home directory, then from the project root down to the working directory, and concatenates them up to `project_doc_max_bytes` (32 KiB by default). Audit those files instead.
- **`.rules` files** (for example `~/.codex/rules/default.rules`): these are experimental Starlark `prefix_rule()` policies that decide whether a command runs outside the sandbox (`allow`, `prompt`, `forbidden`). They are out of scope for this skill. Test them with `codex execpolicy check --pretty --rules <file> -- <command>`, and use each rule's `match` and `not_match` examples, which Codex validates when it loads the file.

## Edge Cases

- **Subdirectory rules** (`.claude/rules/frontend/react.md`): discovered and processed normally.
- **Symlinked rule**: apply the load-status rules above before scoring; do not assume it loads.
- **Invalid YAML frontmatter**: score criterion 1 as 0 and warn that the rule currently loads as always-on.
- **Empty file**: flag as broken, skip the interactive step, ask whether to delete it.
- **Dead pattern**: flag it and suggest a fix from the rule content.
- **Pattern matching more than 30% of files**: flag as too broad and suggest narrowing.
- **Rule not loading as expected**: add an `InstructionsLoaded` hook; its matcher filters on the load reason (`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`) and it logs which rule files load and when.
