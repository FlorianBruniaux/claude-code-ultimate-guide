# Brownfield Agentic Engineering (Addy Osmani, Sep 2026)

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [Brownfield Agentic Engineering](https://addyo.substack.com/p/brownfield-agentic-engineering) |
| Author | Addy Osmani (Elevate newsletter; the author's LinkedIn profile lists him as Member of Technical Staff at Anthropic) |
| Published | 2026-09-14 |
| Evaluated | 2026-09-29 |
| Resource type | Practitioner essay with cited third-party case studies |
| Related | [Bun Zig-to-Rust rewrite](./bun-rust-rewrite-claude-code.md) (cited by the essay, evaluated separately from its primary source) |
| Decision | Integrate |
| Score | 4/5 |

## Verdict

The guide's legacy material (`guide/ultimate-guide.md` §9.21) was written around the February 2026 COBOL playbook: discover, rank by coupling, plan, migrate incrementally with a parallel run. It had no operating procedure for where agents may act, no rule on who authors characterization tests, and no definition of when a migration is finished. It even recommended a compatibility wrapper without saying the wrapper has to go. This essay supplies all three, in a form that maps directly onto Claude Code controls (deny rules, hooks, path-scoped rules, fresh sessions).

The score stops at 4/5. The essay is an experienced practitioner's framework, not a measured study, and most of its numeric case studies are quoted from secondary accounts that this evaluation did not verify (see below). Only the claims listed under "Verified facts used" reach the guide with figures.

## Verified facts used for integration

| Claim | Status | Used in |
|---|---|---|
| Green, yellow and red zones; three rules (a person draws the map, zones move when earned, the zone sets the verbs) | Read in the source essay | §9.21 Step 2 |
| "Autonomy should follow blast radius, observability, and recoverability. A model's confidence is a poor guide." | Quoted verbatim | §9.21 Step 2 |
| Comprehension memo for yellow and red work, with every claim citing a file, issue, ownership record or dashboard | Read in the source essay | §9.21 Step 1, `guide/workflows/plan-driven.md` |
| The session making tests pass should not be the only author of those tests | Read in the source essay | §9.21 Step 4, `guide/workflows/tdd-with-claude.md` |
| "A migration is complete when the new path works and the old dependency is demonstrably gone." | Quoted verbatim | §9.21 Step 4 |
| SWE Refactor Bench: "Blindness", 28 of 520 runs pass all three stages | Checked against the [arXiv abstract](https://arxiv.org/abs/2608.23564) (20 tasks, 8 models, 5.4%, 13 tasks with no accepted solution, language rewrites 5.6 vs build toolchain 31.4). Full paper not read | §9.21 Step 4 |
| "Parallelize last"; "Parallelism multiplies the bottleneck you already have" | Read in the source essay | `guide/core/agent-harness.md` |
| Recurring corrections belong in a lint rule, hook, type, test or skill; prose only for what cannot be enforced | Read in the source essay | `guide/core/agent-harness.md`, `guide/core/memory-systems.md` |
| "Worktrees isolate changes, not behavior" | Read in the source essay; the shared stash list was reproduced locally with `git worktree add` and `git stash` | "Git Worktrees for Parallel Development" in `guide/ultimate-guide.md` |

## Not integrated

| Claim | Reason |
|---|---|
| Asana cleared an Enzyme backlog in two weeks for about $12,000 | Not verified against a primary source; the essay itself calls it a vendor-reported generation cost |
| VB6-to-C# study: 92% behavioral equivalence on simple features, 47% on complex | Study not identified or read |
| Shopify rebuilt the Shop app in twelve weeks; Spotify merges 650+ agent PRs a month; Stripe moved 3.7 million lines to TypeScript | Not verified; none changes a recommendation in the guide |
| Netflix GraphQL cutover with replay and shadow traffic | Mentioned generically (replay, shadow traffic) without the company figure |
| "Anthropic's own migration process stress-tests its rulebook on a disposable mini-migration" | No public source found; the Bun pilot on 3 files documents the same practice from a primary source |
| Teleport vulnerability-harness paragraph | Sponsored block marked `#ad` in the newsletter, not part of the essay |

## Challenge

**Objection**: zones are ordinary risk-based change management with new colors. **Answer**: yes, and that is the point. What the guide lacked was not the idea of risk but the binding between a risk tier and what an agent is permitted to do, plus the rule that the agent does not draw the map. That binding is enforceable in Claude Code (deny rules, hooks), which makes it guide material rather than management advice.

**Objection**: "delete the old path" contradicts the parallel-run principle already in §9.21. **Answer**: it does not; the two describe different moments. The integration states explicitly that the parallel run is a transition state and that completion requires removing the legacy path.
