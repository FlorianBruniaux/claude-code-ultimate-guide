# Resource Evaluation: Fusion (multi-agent orchestrator)

**URL**: https://github.com/Runfusion/Fusion
**Type**: GitHub repository (orchestrator, MIT), npm `@runfusion/fusion`
**Evaluation date**: 2026-07-15
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1
**Method**: source analysis of a local clone at commit `8fe122d77`, 6 parallel agents, all claims verified against code rather than documentation

---

## Content summary

Fusion positions itself as "a software factory, run by a multi-agent orchestrator". Concretely: a pnpm TypeScript monorepo (12 packages, 18 bundled plugins) that drives AI coding agents across a kanban board, one git worktree per task, with a real-time dashboard, a configurable workflow engine, and runtime plugins to plug in third-party CLIs.

Two domain hierarchies coexist, which the README's kanban framing hides:

- **Task** on a board: `triage` (shown as "Planning") to `todo` to `in-progress` to `in-review` to `done` to `archived`, each task isolated in a `fusion/{task-id}` worktree.
- **Mission to Milestone to Slice to Feature**, with an Autopilot activating the next Slice when the current one completes, and Contract Assertions (typed acceptance criteria) checked by a Validator Run.

Four CLI adapters have native telemetry (Claude Code, Codex, Droid, and Pi, their own CLI). Cursor and Grok exist but in a separate, weaker category ("runtime plugins", no structured telemetry). Autonomy is a setting, not a doctrine: `planner oversight` accepts `off`, `observe`, `steer`, `autonomous`, defaulting to `autonomous`. The only non-bypassable human gate is merge, plus destructive or external-service actions.

---

## The one idea worth taking: double-checkout adversarial verification

`packages/engine/src/mission-verification.ts` (986 lines) implements the sharpest answer we have seen to the core problem of AI-assisted coding: **the agent that declares "done" on broken code**.

The mechanism, verified in code:

- The read-only AI judge is explicitly **subordinate**, not authoritative (lines 4-6): "The Validator Run's read-only AI judge cannot run code, so its 'pass' on a behavioral assertion is advisory only."
- A real disposable checkout: `fs.mkdtemp(os.tmpdir(), "fn-verify-")` then `git worktree add --detach <tmp> <revision>` (lines 338-341). Never the live worktree, never the repo root.
- **The anti-cheat** (line 26, verdict logic at line 555): an agent-supplied regression test must **FAIL** on a second disposable checkout at the merge-base (before the fix) and pass on the implementation. A test that passes on both sides proves nothing and is rejected. This kills `expect(true).toBe(true)` as a way to turn a task green.
- Three typed verdicts (line 63): `pass | fail | inconclusive`. `inconclusive` is routed whenever infrastructure cannot conclude and is never folded into `fail` (line 581), so a flaky CI does not generate remediation churn.

**This module is dead code in production.** `mission-execution-loop.ts` imports it `import type` only (lines 28 and 112). The real implementation is imported by three test files and nothing else. `verificationCapability` is never wired at the single production instantiation point (`runtimes/in-process-runtime.ts:543-570`), and the code handles that case by leaving behavioral assertions failed (line 813). Git history: created 2026-06-12, last touched 2026-06-19, 5 commits total.

Built, tested, never shipped. The pattern remains excellent and is MIT-licensed, therefore directly copyable.

---

## What is actually wired versus advertised

Verified by tracing runtime imports (not `import type`) to a known entry point.

| Feature | Status | Evidence |
|---|---|---|
| Missions / Autopilot | Wired | `new MissionAutopilot(...)` at `in-process-runtime.ts:537`, `cli/src/commands/dashboard.ts:1609` |
| Shared branch groups | Wired | Broad non-test footprint: `executor.ts`, `merger.ts`, `group-merge-coordinator.ts`, `pr-nodes.ts`, `store.ts`, `mission-store.ts` |
| Multi-node orchestration | Wired | `new RemoteNodeRuntime(...)` at `project-manager.ts:224` |
| `spawn_agent` / `delegate_task` | Wired | `executor.ts`, `agent-heartbeat.ts`, `triage.ts`, `agent-tools.ts` |
| Behavioral validator | **Dead in production** | Type-only import, never instantiated outside tests |
| Evals | Behind a flag, **off by default** | `evalsView` absent from `DEFAULT_ON_EXPERIMENTAL_FEATURES` (`core/src/experimental-features.ts:25`); their own doc calls the view and cron execution "dormant" without it |
| "Signals", "Connectors" (README) | Not found in code | Zero occurrences of `SignalsPanel`/`SignalType`; likely marketing names for the existing diagnostic badges |

The engine is real and runs. The quality and verification layer is the part that is still a construction site, which is the exact inverse of what the README sells.

---

## Project health: the disqualifying number

Measured on `origin/main` (bypassing the local token-compression proxy, which silently truncated git output to 50 lines and produced a false first-commit date on the first pass).

| Metric | Value |
|---|---|
| First commit | 2026-03-25 (repo under 4 months old) |
| Commits on main | 11,333 |
| Contributors displayed | 32 |
| **gsxdsm + bot identities** | **10,665 commits, 94%** |
| Second human (Dustin Byrne) | 373 commits, 3.3% |
| Last 30 days | gsxdsm 2,203 / second human 55 (factor 40) |

**Bus factor = 1.** The 32 contributors are a statistical illusion. Commit velocity peaked in May (4,328) and is declining: 2,617 in June, roughly 1,900 on July's run rate.

The `Fusion` and `Fusion (runfusion.ai)` commit identities (4,123 commits) are the agents themselves. Fusion is largely written by Fusion.

---

## Scale and debt

| File | Lines |
|---|---|
| `packages/engine/src/executor.ts` | **19,328** |
| `packages/engine/src/merger.ts` | 12,487 |
| `packages/engine/src/self-healing.ts` | 12,183 |
| `packages/dashboard/app/api/legacy.ts` | 11,627 |
| **Total (excluding tests and node_modules)** | **727,279** |

**Dual storage backend maintained in parallel.** `packages/core/src/` holds both `sqlite-adapter.ts` + `db.ts` and a `postgres/` directory, with both dependencies (`embedded-postgres`, `postgres@^3.4.9`). Every store exists twice: `agent-store.ts` (122.7 KB) beside `async-agent-store.ts`, `mission-store.ts` beside `async-mission-store.ts` (83.3 KB) plus `async-mission-store-queries.ts` (85.8 KB). The Postgres migration is a full parallel rewrite with the old path still standing, which explains the flood of `pg-*` and `postgres-*` changesets. `ROADMAP.md` still lists that migration as "planned" while the cutover review is dated 2026-07-14.

---

## Security posture: weak by default on all three layers

| Layer | Real default protection |
|---|---|
| Agent execution | None. `sandbox.backend = native` by default. bubblewrap backend exists but is opt-in and Linux-only (`docs/sandbox.md`). The worktree is the only boundary. |
| Agent heartbeat | None. `agent-heartbeat.ts:595` is a literal system prompt granting "coding-capable workspace tools (read/write/edit/bash)". The real readonly allowlist (`workflow-step-tool-policy.ts:4-25`, raising `ReadonlyViolationError`) only covers workflow-step gate nodes. Zero occurrences of `toolMode` in `agent-heartbeat.ts`. |
| Plugins | None. Plugins run in the Fusion process. The two barriers (AI scan on load, signature verification) are both optional and off by default. |

The pattern is consistent: fail-closed mechanisms on the older workflow-step path, security-by-prompt on the newer agent path. Typical of a project shipping faster than it hardens.

---

## Licensing

MIT throughout. 12 packages all declared MIT, no CLA, no BSL/SSPL/Elastic v2 component hiding in the tree. Legally the cleanest part of the file, and it matters: the double-checkout pattern can be copied outright with attribution.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 4 | The double-checkout anti-cheat is the best answer we have found to agent self-certification |
| Production reliability | 1 | Bus factor 1, under 4 months old, dual backend mid-migration, no default sandbox |
| Documentation quality | 2 | 337-line domain glossary and serious standing rules, but describes behavior that does not happen |
| Adoptability | 1 | 727K lines, a 19K-line file, upstream at roughly 100 commits/day |
| Guide value | 5 | Fills a real gap (absent from the guide) and provides a measured case study nobody else has |
| **Overall** | **4** | High value as documented material, not as an adoptable tool |

---

## Decision

**Integrate as a case study within a week. Do not recommend as a tool.**

Three angles to carry into the guide:

1. **The double-checkout pattern** deserves its own section. It is the concrete answer to the "decorative CI" trap already documented at `guide/workflows/spec-first.md:979-988` and to the Refute-or-Promote paper (arXiv:2604.19049) cited at the same place. Fusion supplies a readable, MIT-licensed reference implementation.
2. **Fusion as a market entry** in `guide/ecosystem/agentic-tools.md`, in the orchestrator category, with an explicit early-preview and bus-factor-1 caveat.
3. **The involuntary lesson, which is the most valuable part.** Fusion proves a single developer with agents can ship 727K lines in under 4 months. It also proves what that produces: documentation describing a product that does not quite exist, tested-but-unwired code, a 19K-line file, and two storage backends in parallel. This is not "how to build a software factory". It is **what happens when agentic velocity is bounded by no architecture**. No one is documenting this, and the measurements here are first-hand.

---

## Method note

The first pass at git statistics returned a false first-commit date (2026-07-13) and a suspiciously round "50 commits", because the local RTK token-compression proxy truncates command output. Re-running through `rtk proxy` produced the real history. Worth remembering for any future repo-health measurement in this environment.

Equally worth remembering: `import type` and `import("...").Type` erase at compile time and prove no runtime wiring. Checking that a file exists, or even that it is imported, says nothing about whether it runs. That distinction is what separated Fusion's advertised verification layer from its actual behavior, and it is likely a generalized trap across this market.

---

## Sources

All paths relative to a clone of `github.com/Runfusion/Fusion` at commit `8fe122d77`:

`packages/engine/src/mission-verification.ts`, `packages/engine/src/mission-execution-loop.ts`, `packages/engine/src/runtimes/in-process-runtime.ts`, `packages/engine/src/agent-heartbeat.ts`, `packages/engine/src/workflow-step-tool-policy.ts`, `packages/engine/src/executor.ts`, `packages/engine/src/scheduler.ts`, `packages/engine/src/project-manager.ts`, `packages/core/src/experimental-features.ts`, `packages/core/src/store.ts`, `packages/plugin-sdk/src/index.ts`, `docs/sandbox.md`, `docs/acp-contract.md`, `docs/mcp.md`, `CONCEPTS.md`, `STRATEGY.md`, `ROADMAP.md`, `LICENSE`.
