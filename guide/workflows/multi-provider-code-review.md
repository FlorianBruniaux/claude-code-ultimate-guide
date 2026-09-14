---
title: "Multi-Provider Code Review: Non-Redundant Automated PR Review"
description: "Run Claude Code Action alongside CodeRabbit and Greptile without triplicate findings: role separation, a blocking CI gate, batching for large PRs, and cross-tool deduplication"
tags: [workflow, ci-cd, code-review, github-actions, coderabbit, greptile]
---

# Multi-Provider Code Review: Non-Redundant Automated PR Review

> **Evidence boundary**: this is a design pattern informed by project configuration, not a validated end-to-end deployment contract. Inspect effective provider execution, permissions, output handling and branch policy in your repository. Severity thresholds, domain names and file-count cutoffs are illustrative starting points; the gate example has unresolved limits documented below.

Running two or three automated reviewers on the same PR without a plan produces the same finding three times in three different comment styles, which trains developers to skim past all of them. The fix is not picking one tool over the others, it's giving each tool a job the other two don't do, and writing that boundary down where every config file can see it.

This page separates semantic review, executable checks and cross-file investigation. Claude Code Action, CodeRabbit and Greptile can contribute to these roles, but a provider name does not establish deterministic behavior or merge authority. Assign required checks through repository policy. The [GitHub Actions Workflows](./github-actions.md) and [templates](../../examples/github-actions/) provide implementation examples with limits described below. [Loop & Graph Engineering](../core/loop-graph-engineering.md#5-allocate-judgment-explicitly) explains acceptance authority and reviewer independence.

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

A different tool can expose a blind spot, but additional coverage must be measured. Repository search can help investigate callers outside the diff. Executable lint rules and tests provide repeatable checks for specified properties; they can still miss cases outside their model, scope or implementation. An AI reviewer emitting PASS/FAIL is not thereby deterministic. In particular, do not assume that CodeRabbit custom checks have the same guarantees as a compiler or a tested lint rule.

Stacking overlapping tools can increase duplicate findings without enough additional validated defects to justify the cost. Measure unique confirmed findings, false alerts and adjudication effort before expanding the fleet.

---

## Role Separation

| Provider | Job | Can it block merge? | Why this job fits this tool |
|----------|-----|---------------------|------------------------------|
| **Claude Code Action** | Deep semantic review: logic errors, security (IDOR, auth, injection), architecture violations, data integrity | Yes, via the [CI gate](#blocking-merge-the-ci-gate) | Full codebase context per PR, reasons about intent, not just pattern-matches |
| **CodeRabbit** (or equivalent) | PR summaries and configured review checks | Only through an explicit required-check policy with verified execution and output handling | Evaluate each check's actual mechanism and error behavior; binary output is not a reliability guarantee |
| **Executable lint rules and tests** | Specified syntax, type and behavior constraints | Yes, where repository policy requires them | Repeatable within their inputs and environment; coverage and test quality limit detection |
| **Greptile** (or equivalent) | Cross-file invariants: dependency chains, "does every caller of X respect rule Y," patterns that repeat across distant files | No | RAG-indexed search across the whole repo, not scoped to the diff |

Adjust the "job" column to your stack, not the principle. If your deterministic-check tool is something else (a custom lint rule, a separate CI job, Semgrep), the role still belongs in that column, not duplicated into the LLM reviewer's prompt.

---

### Separate discovery from verification evidence

In [Using LLMs to Secure Source Code, at 12:19](https://www.youtube.com/watch?v=imFedndyXYQ&t=739s), Eugene Yan describes a verifier that does not receive the discovery agent's reasoning trace and tries to refute candidate vulnerabilities. Applied to review, this means giving the verifier the claim, relevant source and reproducible evidence while avoiding a persuasive author narrative as its only input.

This is a practitioner method, not proof that a second model makes a finding correct. Preserve the verifier's attempts, counterexamples and unresolved questions, and adjudicate against the requirement. Different provider names alone do not establish independent evidence.

---

## The Non-Duplication Rule

Write the boundary into every config file, not just into a wiki page nobody reads mid-review-setup. Concretely:

- `.github/prompts/code-review.md` (Claude): a one-line header noting it owns deep semantic review and the merge gate, not style nits already caught by a linter.
- `.coderabbit.yaml` (or equivalent): a comment at the top stating it should not duplicate the LLM reviewer or the RAG tool. See the [template in this repo](../../examples/github-actions/.coderabbit.yaml).
- `.greptile/rules.md` (or equivalent): same non-duplication note, explicit about which invariants live here because they require cross-file search, not because they were easiest to write down. See the [template](../../examples/github-actions/.greptile/rules.md).

Assign an owner to each rule and distinguish intentional defense in depth from duplicate comments. SQL injection may need both executable analysis and contextual review. Tenant scoping may need repository search plus tests across callers. Deduplicate the reported finding after independent checks; do not remove a useful control merely because another tool examines the same risk.

---

## Blocking Merge: the CI Gate

An automated comment does not establish merge authority. A required check or required approving review must be part of the effective repository policy. Parsing a severity count is one input to a check; it is not a sufficient acceptance contract.

**Template limitation:** the [`gate` example](../../examples/github-actions/claude-code-review.yml) selects the last returned review without establishing its provider, current commit or run identity, and treats an absent severity match as zero. It also skips the gate after an unsuccessful review job. Do not use that example as a required acceptance gate without replacing these behaviors and testing failure cases. A passing or skipped job can otherwise conceal missing review evidence.

An acceptance gate needs:

1. A versioned output schema tied to the expected provider, repository, run, current revision and covered scope. Missing, malformed, stale, partial or failed evidence must not become a clear outcome. Test those cases explicitly.
2. Severity calibration based on consequences, including data access and external effects. An internal admin tool can still be critical. Record the owner, permitted deferrals and recovery requirements.
3. Effective required checks, expected check publishers, approving identities and bypass rules. Verify the policy, not just the workflow file. See [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

Record the base, merge base, tested integration revision and exact PR revisions combined. A new base or merge group invalidates the previous integration result. [Merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) need checks that run on the group, not only the individual PR. Two low-risk changes can interact in a high-impact way.

Human deep review can be selective under a documented policy, with sensitive paths assigned to an owner. Before relying on recoverability, exercise detection, containment and restoration after an incorrectly accepted change. Resuming the reviewer process does not restore application data or compensate external effects.

---

## Scaling to Large PRs: Batching

A single review pass over a 150-file PR either times out or spreads the model's attention so thin that findings get shallow. The [batched workflow template](../../examples/github-actions/claude-code-review-batched.yml) in this repo handles this: a `check-size` job counts changed files, and above a threshold (75 in the shipped example, tune to your PR size distribution), a matrix job splits the diff by domain (migrations, backend services, API routes, frontend, tests) and runs each slice as an independent, parallel review. A final synthesis job merges the per-domain findings into one deduplicated severity table.

This keeps the same prompt file (`code-review.md`) as the source of truth for review criteria, only the scope changes per matrix job, via `append_system_prompt` restricting each batch to its domain's file globs. No duplicated review logic to maintain between the small-PR and large-PR paths.

---

## Cutting Redundant Reviews: Delta-Review

Re-reviewing the entire diff on every push to a long-lived PR burns tokens re-checking code Claude already approved on the previous push. A delta-review step compares the SHA embedded in the previous review (post it as an HTML comment, `<!-- reviewed-sha: abc123 -->`, inside the review body) against the current push's SHA, and scopes the new review to only the files touched since.

This repo does not ship a ready-made delta-review template, because the right implementation depends on how a given project already tracks review state (a marker comment, a label, a separate check run keyed by commit SHA). The mechanics are the same regardless: read the last marker, run `git diff <last-sha>..HEAD --name-only`, and pass that file list into the prompt the same way the batched workflow scopes a matrix job by domain.

A marker is only a locator, not authenticated evidence. Validate its publisher and run, and invalidate affected review when requirements, dependencies, base, provider configuration or combined changes differ. Include impacted callers and consumers even when their files did not change. An unchanged filename list does not establish unchanged risk.

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
3. Replace the illustrative gate's evidence handling, exercise stale/missing/malformed/failed results, then configure and inspect the effective required-check policy
4. If your PRs regularly exceed ~50-75 files, add `claude-code-review-batched.yml` and tune the domain globs
5. Assign repeatable invariants to executable lint rules or tests; evaluate AI review checks separately and document which results can block
6. If you have budget for a cross-file RAG reviewer, add it (Greptile or equivalent) and scope its rulebook to invariants that genuinely need repo-wide search
7. Schedule a periodic pass comparing all provider configs against each other for rule drift

---

## See Also

- [GitHub Actions Workflows](./github-actions.md): the base patterns this architecture extends
- [Ready-to-use templates](../../examples/github-actions/): `claude-code-review.yml`, `claude-code-review-batched.yml`, `.coderabbit.yaml`, `.greptile/`
- [Code Review (managed feature)](./code-review.md): Anthropic's own multi-agent PR review service, an alternative to self-hosting this architecture on Teams/Enterprise plans
- [`examples/agents/code-reviewer.md`](../../examples/agents/code-reviewer.md): anti-hallucination protocol referenced by the prompt template above
