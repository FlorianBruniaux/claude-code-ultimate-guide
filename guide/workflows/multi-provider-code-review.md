---
title: "Multi-Provider Code Review: Non-Redundant Automated PR Review"
description: "Run Claude Code Action alongside CodeRabbit and Greptile without triplicate findings: role separation, a blocking CI gate, batching for large PRs, and cross-tool deduplication"
tags: [workflow, ci-cd, code-review, github-actions, coderabbit, greptile]
---

# Multi-Provider Code Review: Non-Redundant Automated PR Review

> **Confidence**: Tier 2. Pattern derived from a production codebase that has run this exact three-provider setup for an extended period. The architecture principle (distinct, non-overlapping roles per tool) generalizes; the specific severity thresholds, domain names, and file-count cutoffs in the examples are illustrative starting points, not universal defaults.

Running two or three automated reviewers on the same PR without a plan produces the same finding three times in three different comment styles, which trains developers to skim past all of them. The fix is not picking one tool over the others, it's giving each tool a job the other two don't do, and writing that boundary down where every config file can see it.

This page documents that architecture: Claude Code Action for deep semantic review and the only tool allowed to block merge, a deterministic linter-style tool (CodeRabbit or equivalent) for PASS/FAIL pre-merge checks, and a cross-file RAG tool (Greptile or equivalent) for invariants that span multiple files. It builds directly on the [GitHub Actions Workflows](./github-actions.md) patterns and the [ready-made templates](../../examples/github-actions/) in this repo; read those first if you're starting from zero.

---

## Table of Contents

1. [Why Three Providers, Not One](#why-three-providers-not-one)
2. [Role Separation](#role-separation)
3. [The Non-Duplication Rule](#the-non-duplication-rule)
4. [Blocking Merge: the CI Gate](#blocking-merge-the-ci-gate)
5. [Scaling to Large PRs: Batching](#scaling-to-large-prs-batching)
6. [Cutting Redundant Reviews: Delta-Review](#cutting-redundant-reviews-delta-review)
7. [Cross-Tool Deduplication](#cross-tool-deduplication)
8. [Known Friction: Rule Drift Across Configs](#known-friction-rule-drift-across-configs)
9. [Interactive Companions vs. CI](#interactive-companions-vs-ci)
10. [Setup Checklist](#setup-checklist)
11. [See Also](#see-also)

---

## Why Three Providers, Not One

A single review pass, no matter how good the model, misses things a differently-shaped tool catches. Claude Code Action reasons deeply about a diff in the context of the full codebase but reviews one PR at a time. A dedicated RAG-based tool like Greptile indexes the whole repo up front and can answer "does this new query respect the scoping rule enforced everywhere else," a question that requires searching dozens of unrelated files, not just the diff. A deterministic linter-style tool like CodeRabbit's custom checks can enforce a PASS/FAIL rule (no `console.log` in production code, financial totals stay symmetric) with zero false-negative risk, something an LLM-based reviewer will occasionally miss under time or context pressure.

The failure mode to avoid is stacking three tools that all try to do the first job. That triples review noise for zero coverage gain, and it's the default outcome if you install three code-review bots without deciding who owns what.

---

## Role Separation

| Provider | Job | Can it block merge? | Why this job fits this tool |
|----------|-----|---------------------|------------------------------|
| **Claude Code Action** | Deep semantic review: logic errors, security (IDOR, auth, injection), architecture violations, data integrity | Yes, via the [CI gate](#blocking-merge-the-ci-gate) | Full codebase context per PR, reasons about intent, not just pattern-matches |
| **CodeRabbit** (or equivalent) | PR summaries, auto-labelling, deterministic PASS/FAIL pre-merge checks | Optional, only for checks with a hard binary criterion | Cheap, fast, no false-negative risk on rules with a clear yes/no answer |
| **Greptile** (or equivalent) | Cross-file invariants: dependency chains, "does every caller of X respect rule Y," patterns that repeat across distant files | No | RAG-indexed search across the whole repo, not scoped to the diff |

Adjust the "job" column to your stack, not the principle. If your deterministic-check tool is something else (a custom lint rule, a separate CI job, Semgrep), the role still belongs in that column, not duplicated into the LLM reviewer's prompt.

---

## The Non-Duplication Rule

Write the boundary into every config file, not just into a wiki page nobody reads mid-review-setup. Concretely:

- `.github/prompts/code-review.md` (Claude): a one-line header noting it owns deep semantic review and the merge gate, not style nits already caught by a linter.
- `.coderabbit.yaml` (or equivalent): a comment at the top stating it should not duplicate the LLM reviewer or the RAG tool. See the [template in this repo](../../examples/github-actions/.coderabbit.yaml).
- `.greptile/rules.md` (or equivalent): same non-duplication note, explicit about which invariants live here because they require cross-file search, not because they were easiest to write down. See the [template](../../examples/github-actions/.greptile/rules.md).

When a rule accidentally ends up in two configs, don't leave it, pick whichever tool has the actual vantage point for that check and remove it from the other. A rule about SQL injection in one specific router belongs in the LLM prompt (it needs to read the surrounding code to judge intent). A rule that a given Redis key must always be scoped by tenant ID everywhere in the codebase belongs in the RAG tool's rulebook (it needs to search every caller, not just the diff).

---

## Blocking Merge: the CI Gate

Automated review comments are advisory by default, nothing stops a merge unless a required CI check fails. The pattern that makes Claude's findings block bad merges: post the review as structured markdown with a parseable severity count, then run a small script that reads that count and fails the job if it's non-zero.

The [`gate` job](../../examples/github-actions/claude-code-review.yml) in this repo's template does exactly this: it fetches the review Claude just posted, regex-matches `### 🔴 Must Fix (n)` from the summary table, and calls `core.setFailed()` if `n > 0`. Add that job's name to your branch protection's required status checks, and a 🔴 finding now genuinely blocks the merge button, not just guilt-trips the author in a comment thread.

Two things this depends on:

1. The reviewer's prompt must emit a **parseable** severity count in a stable format. If you change the heading text in your prompt file, update the gate script's regex to match.
2. Severity calibration must reflect actual business risk, not pattern frequency. A permission-check bug on a path handling sensitive data should be 🔴 regardless of how common that pattern is elsewhere in the codebase; a purely internal admin-tool bug can reasonably cap at 🟡. Write that calibration into the prompt file explicitly, don't leave it to the model's default judgment.

---

## Scaling to Large PRs: Batching

A single review pass over a 150-file PR either times out or spreads the model's attention so thin that findings get shallow. The [batched workflow template](../../examples/github-actions/claude-code-review-batched.yml) in this repo handles this: a `check-size` job counts changed files, and above a threshold (75 in the shipped example, tune to your PR size distribution), a matrix job splits the diff by domain (migrations, backend services, API routes, frontend, tests) and runs each slice as an independent, parallel review. A final synthesis job merges the per-domain findings into one deduplicated severity table.

This keeps the same prompt file (`code-review.md`) as the source of truth for review criteria, only the scope changes per matrix job, via `append_system_prompt` restricting each batch to its domain's file globs. No duplicated review logic to maintain between the small-PR and large-PR paths.

---

## Cutting Redundant Reviews: Delta-Review

Re-reviewing the entire diff on every push to a long-lived PR burns tokens re-checking code Claude already approved on the previous push. A delta-review step compares the SHA embedded in the previous review (post it as an HTML comment, `<!-- reviewed-sha: abc123 -->`, inside the review body) against the current push's SHA, and scopes the new review to only the files touched since.

This repo does not ship a ready-made delta-review template, because the right implementation depends on how a given project already tracks review state (a marker comment, a label, a separate check run keyed by commit SHA). The mechanics are the same regardless: read the last marker, run `git diff <last-sha>..HEAD --name-only`, and pass that file list into the prompt the same way the batched workflow scopes a matrix job by domain.

---

## Cross-Tool Deduplication

When two or three bots comment on the same PR, the LLM reviewer can read what the others already posted before writing its own findings, and skip anything already flagged. This is what the `multi-reviewer-synthesis` job in [`claude-code-review.yml`](../../examples/github-actions/claude-code-review.yml) does after the fact (waits for external bots, then synthesizes consensus vs. unique catches). For tighter coupling, the same `mcp__github__list_pull_request_files`-style read access lets Claude's own review step check existing PR comments before posting, and explicitly note "already flagged by CodeRabbit" instead of repeating the finding under a different wording.

---

## Known Friction: Rule Drift Across Configs

There is no single generator that pushes one source of truth into all three provider configs. Canonical conventions live in whatever internal docs a project already maintains, and each provider config is a manual, condensed transcription of the relevant subset, kept short on purpose since the reviewing tool should not have to load and parse an entire internal wiki on every PR.

The practical cost: a file-exclusion list (lockfiles, generated code, migrations) ends up duplicated across the workflow's `paths-ignore`, CodeRabbit's `path_filters`, and Greptile's `ignorePatterns`. Nothing catches drift automatically when one list gets updated and the other two don't. Periodically audit the three configs against each other and against the canonical docs; treat a mismatch as a signal the review setup itself needs maintenance, not just the code it reviews.

---

## Interactive Companions vs. CI

Everything above runs unattended in CI. A separate, complementary layer is a handful of local Claude Code skills a developer runs by hand during active work: a quick check of the current PR's CI/review/preview status, a pull of everything posted since the last push across every bot and human reviewer, and a periodic retrospective audit across the last N PRs to spot findings bots keep flagging that no rule file covers yet. These are developer-convenience tools, not part of the CI pipeline, worth building as project-local skills once the CI-side architecture above is stable, not before.

---

## Setup Checklist

1. Copy `claude-code-review.yml` + `prompts/code-review.md` (see [GitHub Actions Workflows](./github-actions.md) for the base setup)
2. Fill in the prompt's stack context and a severity calibration table matched to your product's actual risk profile, not a generic OWASP list
3. Add the `gate` job's name to branch protection's required status checks
4. If your PRs regularly exceed ~50-75 files, add `claude-code-review-batched.yml` and tune the domain globs
5. If you have budget for a deterministic pre-merge checker, add it (CodeRabbit or equivalent) with an explicit non-duplication header and PASS/FAIL-only custom checks
6. If you have budget for a cross-file RAG reviewer, add it (Greptile or equivalent) and scope its rulebook to invariants that genuinely need repo-wide search
7. Schedule a periodic pass comparing all provider configs against each other for rule drift

---

## See Also

- [GitHub Actions Workflows](./github-actions.md): the base patterns this architecture extends
- [Ready-to-use templates](../../examples/github-actions/): `claude-code-review.yml`, `claude-code-review-batched.yml`, `.coderabbit.yaml`, `.greptile/`
- [Code Review (managed feature)](./code-review.md): Anthropic's own multi-agent PR review service, an alternative to self-hosting this architecture on Teams/Enterprise plans
- [`examples/agents/code-reviewer.md`](../../examples/agents/code-reviewer.md): anti-hallucination protocol referenced by the prompt template above
