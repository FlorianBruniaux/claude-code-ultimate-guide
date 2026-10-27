# Agent Harness Engineering Patterns (AHEP)

**Reviewed**: 2026-10-27. **Initial and final score**: 3/5. Use as inspiration and as a cited reference for the classic-pattern crosswalk. Do not copy text, diagrams or entries.

## Sources and evidence

| Source | Contribution | Limit |
|---|---|---|
| [ashishpatel26/agent-harness-engineering-pattern](https://github.com/ashishpatel26/agent-harness-engineering-pattern), read 2026-10-27 | Single HTML page with 192 classic patterns in 13 chapters, each mapped onto a part of an agent harness | No license, so all rights reserved. Repository created 2026-10-27 with 0 stars at reading time |
| [Published site](https://ashishpatel26.github.io/agent-harness-engineering-pattern/), read 2026-10-27 | Same content, rendered | A single page of about 1.7 MB; no per-entry sources |

Each entry follows one template: an everyday comparison, the classic meaning, the role in the agent system, the role in a large company, steps with a code sketch, a "be careful" note and a fit badge.

## What is worth keeping

The appendix of 15 "important fixes" is the strongest asset. Each fix describes a harness failure that a reader can test for. Examples listed in the appendix:

- an unresolved path guard;
- insert-before-act idempotency;
- a hidden tool that is not blocked at dispatch;
- a frozen kill switch;
- secret scrubbing limited to headers;
- a cache key without a tenant;
- `run_in_executor` not copying `contextvars`;
- hash sharding that breaks data residency.

These read as anti-patterns with a concrete failure, which a catalog of names alone does not give.

## Weaknesses

- Exhaustive-catalog bias: the 192 entries include patterns with little agent relevance, such as CRTP, Twin and Single Table Inheritance.
- The page claims "0 loose fits" and also says "the loose fits are listed here". The two statements contradict each other.
- The review of the entries is likely an LLM self-review. This is an inference from the page, not a stated fact.
- The Testing and Evals chapter holds only 4 patterns.
- No entry cites a source, so no mapping can be checked from the page alone.

## Decision

Cite AHEP as one independent voice in the classic-to-harness crosswalk, and use the "important fixes" appendix as a prompt for the guide's own failure checklist, with each failure re-derived from official Claude Code documentation or a reproducible test.

Reuse the idea and the structure only. The license forbids reuse of text and diagrams. Where AHEP and another crosswalk agree on a pairing, the guide can present the pairing as a consensus row. A pairing that appears only in AHEP stays marked as a single-source proposal.

Do not infer from this evaluation that the 192 mappings are correct, that the fixes were run against a real harness, or that AHEP reflects Claude Code behavior. None of that was tested. A repository created on the day of review also has no track record of maintenance or community correction. Leak-derived repositories on the same topic were excluded from this work.
