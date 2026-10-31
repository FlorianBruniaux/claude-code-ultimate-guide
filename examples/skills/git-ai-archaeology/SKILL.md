---
name: git-ai-archaeology
description: "Git-history archaeology of a repository's AI coding harness (Copilot, Claude Code, Codex, Cursor, MCP, skills, agents, hooks). Use to date when each AI config appeared, trace how it spread, churned or was abandoned across modules, measure AI-assisted commits over time, or derive maturity phases. Not for auditing the current config or generic git stats."
effort: medium
---

# git-ai-archaeology

Reconstructs the history of an AI coding harness from git: which files appeared when, who maintained them, how they spread between modules, what was abandoned, and how AI-assisted commits evolved. A bundled script does the counting in one pass; the agent checks the classification and writes the narrative from the data.

**Output**: `{out}/{slug}-harness.json` and `{out}/{slug}-harness.md` (script), then `{out}/{slug}-git-archaeology.md` (narrative).

```
/git-ai-archaeology repo_path=/path/to/repo [out=./reports] [slug=name] [ref=main] [since=2025-01-01] [remotes=yes]
```

## Workflow

1. **Resolve the scope.** Check the path with `git -C {repo_path} rev-parse --git-dir`. Use the default branch as `ref` unless the user names one; a feature branch distorts every count. Decide whether to scan remote branches (`--remotes`) for unmerged harness work. Done when repo, ref, period and output directory are recorded.

2. **Run the script.**

   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/harness_archaeology.py \
     --repo {repo_path} --out {out} --ref {ref} [--since {since}] [--remotes] [--slug {slug}]
   ```

   It walks every non-merge commit touching a harness path once (`git log --raw --numstat -M`), so its cost grows with the length of the history, not with the number of runs. Presence, copies and staleness are read from the tree of `--ref`, not the working copy. With `--since`, files older than the window take their first commit in the window as creation date, and the report says how many. It exits non-zero without writing when the path is not a git repository. Done when it prints `harness_commits` and both files exist.

3. **Check the classification before trusting a number.** Read the "By tool family" and "Most edited files" tables. Look for false positives (a `commands/` folder of a test suite, an `agents/` folder of business docs) and for harness files the patterns miss:

   ```bash
   git -C {repo_path} -c core.quotePath=false ls-files | grep -iE 'agent|prompt|llm|copilot|claude|codex|cursor|mcp|skill' | grep -vE '\.(java|ts|py|go|kt)$' | head -50
   ```

   Rerun with `--extra-glob 'path/**'` (repeatable, family `custom`) for a missed location, and with `--exclude-glob 'path/**'` for files that are product content rather than harness, such as skills a repository publishes as examples. A false positive left in place is reported in the narrative's limits rather than hidden. Done when each family's files have been sampled and every correction is either rerun or listed.

4. **Read the events, then write the phases.** Work from the JSON, not from memory of typical projects. Use [the reading grid](references/reading-grid.md) to interpret each indicator. Look for: creation waves, the same file added to many modules on one day (propagation), files added then deleted within days (trial and error), renames from one tool's folder to another (migration), deletions whose subject states a policy, structuring commits, and work living only on remote branches. Derive phases from these breaks; their number and labels come from the data. Done when every phase names its period, its commit count and at least one hash.

5. **Compare usage with harness activity.** From the monthly table, set the AI-trailer share beside harness commits. A trailer is a lower bound: inline completion leaves none, and `Co-authored-by: Copilot` does not say which feature was used. The script counts a trailer when its e-mail belongs to a tool vendor, or when it names a tool with a bot or noreply e-mail, so a colleague named Claude does not count. Done when the narrative states the first month with AI trailers, the latest share and whether usage and harness work move together.

6. **Write `{slug}-git-archaeology.md`.** Sections: scope and method; key figures; timeline of first appearances per family; phases with evidence; spread and duplication; churn and abandonment; who maintains it (counts and shares only); usage versus harness; unmerged work; limits. Every figure comes from the JSON or a command quoted in the report. Done when the validation checklist below passes.

## Rules

- **Read-only.** No git command that writes, no checkout, no fetch unless the user asks.
- **Privacy.** Authors appear only as counts and shares. Do not print names or e-mails, even from `git shortlog`. The script hashes e-mails with a random salt per run, so hashes cannot be recomputed; pass `--salt` only to compare two runs, and keep that salt out of the output. With one or two contributors, a share still points at a person: say so.
- **Verify before asserting.** A date or event not found in git is written "not found", with the command tried.
- **A rename is not a creation.** The script follows renames between harness paths with `-M` and quotes the original creation date. A file moved in from a non-harness path shows as created on the move.
- **Show the flat months.** The script lists every month from the first harness commit on, including months without any commit.

## Validation checklist

- [ ] Ref is the default branch, or the report says why not
- [ ] Classification sampled; corrections rerun or listed as limits
- [ ] Each phase cites a period, a count and a hash
- [ ] Usage stated as a lower bound, with its first month and latest share
- [ ] No author name or e-mail in any output
- [ ] Both script outputs and the narrative exist in `{out}`
