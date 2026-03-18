---
title: "Plan-Validate-Execute Pipeline"
description: "Production-grade 3-command workflow with dynamic agent teams, ADR learning loop, and automated execution from PRD to merged PR"
tags: [workflow, agents, architecture, advanced]
---

# Plan-Validate-Execute Pipeline

> **Confidence**: Tier 2 — Battle-tested by production teams shipping AI-first products at scale. Extends native `/plan` mode with structured agent orchestration and institutional memory.

A complete development workflow in 3 commands: plan with a dynamic research team, validate with independent specialist reviewers, execute with parallel agents. Each run improves the next through an ADR learning loop that progressively reduces human interruptions.

**Reading time**: ~25 min
**Prerequisites**: Sub-agents, Task tool, worktrees, basic ADR concepts
**Related**: [Plan-Driven Development](./plan-driven.md), [Agent Teams](./agent-teams.md), [Spec-First](./spec-first.md)

---

## Table of Contents

1. [TL;DR](#tldr)
2. [Philosophy](#philosophy)
3. [The Three Commands](#the-three-commands)
4. [Dynamic Agent Pool](#dynamic-agent-pool)
5. [ADR Learning Loop](#adr-learning-loop)
6. [CLAUDE.md Discipline](#claudemd-discipline)
7. [Context Management](#context-management)
8. [When to Use](#when-to-use)
9. [Cost Profile](#cost-profile)
10. [See Also](#see-also)

---

## TL;DR

```
/plan-start    → 5-phase planning: PRD analysis + dynamic research team + ADRs
/plan-validate → 2-layer review: structural checks + trigger-based specialist agents
/plan-execute  → worktree + TDD + parallel execution + PR + merge + cleanup
```

**What makes this different from `/plan` mode**:
- Research is done by specialized agents in parallel, not one agent sequentially
- Validation is independent from planning (no confirmation bias)
- Every significant decision generates an ADR that auto-resolves future decisions
- Execution spawns per-task agents in a git worktree, commits per task, handles everything through to merged PR

**Run `/clear` between each command** to reset context and avoid compacting overhead.

---

## Philosophy

### Non-Prescriptive AI-First

Tell Claude **what** to achieve, never **how** to implement it. The moment you prescribe implementation details, you're using your knowledge as a ceiling instead of Claude's as a floor.

A good opening prompt for a new project:
```
How should I use you most effectively to build this platform?
```

Let Claude propose the architecture. Your job is to validate decisions, not dictate them.

### No Bandaids, No Workarounds

Hard rule for every agent in the pipeline:

> We build state-of-the-art software. Always choose the best-in-class architecture, the most robust pattern, and the industry-standard approach.

Build time and effort are irrelevant to architectural decisions. Never factor implementation complexity into option assessments. The right solution is always the best solution.

**Enforcement checklist** (apply before implementing):
- [ ] Am I using a backward-compatibility flag, shim, or legacy mode?
- [ ] Would a new project following current official docs do it this way?
- [ ] Am I porting old patterns instead of learning the new ones?
- [ ] Am I patching one component when the fix belongs at the system level?

If any answer is yes: stop, fix at the correct level.

### Why Independent Validation?

Validators that didn't write the plan are not anchored to its assumptions. Research shows multi-agent review with adversarial framing catches significantly more issues than self-review. The average plan produces ~18 issues when challenged by an independent team — ~95% auto-resolve from existing ADRs and first principles.

---

## The Three Commands

### `/plan-start` — 5-Phase Planning

**Phase 1: PRD & Design Analysis** *(interactive, no agents)*

Read the PRD and surface issues in 3 buckets before any agent work:
- Missing requirements (unclear acceptance criteria, unspecified edge cases)
- Ambiguous requirements (multiple valid interpretations)
- Compliance concerns (security, data privacy, API contracts)

Present options with pros/cons, record decisions. Skip for non-PRD work (refactors, infra, bug fixes).

If UI changes are in scope, extend to design analysis: screen inventory, state catalog (empty/loading/populated/error), interaction specs, animation patterns, accessibility (ARIA), design token updates.

**Phase 2: Technical Analysis** *(1-2 Explore agents + interactive)*

Check existing ADRs and PATTERNS.md first. If 3+ confirmed ADRs match the decision → auto-resolve without asking. Otherwise:
- Spawn Explore agents for targeted codebase research
- Present architecture decisions with options and recommendations
- Create ADR documents for significant decisions (see [ADR Learning Loop](#adr-learning-loop))
- Update PATTERNS.md

**Phase 3: Scope Assessment** *(automatic + user approval)*

Apply trigger rules against the agent pool (see [Dynamic Agent Pool](#dynamic-agent-pool)). Present the proposed team with justification for each agent. User can add or remove agents before research starts.

| Tier | Agent Count | Label |
|------|-------------|-------|
| 0 | 0 | Solo (inline research) |
| 1 | 1-3 | Focused |
| 2 | 4-6 | Standard |
| 3 | 7-9 | Comprehensive |
| 4 | 10+ | Full Spectrum |

**Phase 4: Research & Plan Creation** *(dynamic team)*

- Tier 0: inline research, no agents
- Tier 1+: spawn approved agents in parallel (background), lead monitors via TaskOutput loop
- `planning-coordinator` (Opus) synthesizes all reports into final plan
- Commit plan file, ADRs, and creation artifacts

Output: `docs/plans/plan-{name}.md` + `docs/adr/ADR-XXXX.md` + `docs/plans/metrics/{name}.json`

**Auto-transition**: no unresolved ambiguity → auto-start `/plan-validate`

---

### `/plan-validate` — 2-Layer Validation

**Layer 1: Structural** *(inline, instant)*

Mechanical checks that don't need agents:
- Plan format and completeness (all required sections present)
- Task ordering and dependency chain (no circular deps)
- File existence checks (files listed for modification actually exist)
- ADR consistency (plan aligns with its ADRs)
- CLAUDE.md rule compliance

**Layer 2: Specialist Review** *(trigger-based, 0-8 agents)*

| Agent | Trigger | Model |
|-------|---------|-------|
| `security-reviewer` | Auth, payments, PII, RBAC, new APIs | Opus |
| `db-migration-reviewer` | New tables, columns, indexes, migrations | Opus |
| `performance-reviewer` | New resolvers, queries, routes, new deps | Sonnet |
| `design-system-reviewer` | New UI components, visual styling | Sonnet |
| `ux-reviewer` | New pages, forms, interactions | Sonnet |
| `cross-platform-reviewer` | Web + mobile, or shared packages | Sonnet |
| `native-app-reviewer` | Mobile screens, native UI packages | Sonnet |
| `integration-reviewer` | New services, libraries, OTEL config | Opus |

No agents selected automatically for trivial plans. A payments feature might trigger 4+.

**Auto-Fix Phase**

Every issue must be resolved — no skipping. Triage:
1. Issues matching existing ADR decisions → auto-resolve
2. Issues matching confirmed PATTERNS.md entries → auto-resolve
3. Issues resolvable from first principles → auto-resolve
4. Residual → human decision → new rule → auto-resolved next time

**Auto-transition**: all issues resolved → auto-start `/plan-execute`

---

### `/plan-execute` — Execution to Merged PR

Single command handles everything:

1. **Worktree creation** — isolated branch from current branch
2. **TDD scaffolding** — write failing tests first for TDD-marked tasks
3. **Level-based parallel execution** — detect independent tasks, spawn per-task agents, commit per task
4. **Drift detection** — flag if implementation diverges from plan
5. **Quality gate** — parallel tests + integration smoke test (GraphQL probe, container log scan, plan-defined smoke commands)
6. **Pre-PR docs update** — PRD reconciliation + plan archival (in worktree)
7. **PR creation and merge** — squash merge, clean commit message
8. **Post-merge metrics** — execution data committed to metrics file
9. **Worktree cleanup** — remove branch and worktree

If quality gate fails: up to 3 auto-fix attempts by dedicated debug agents. Still failing → notify human.

---

## Dynamic Agent Pool

Agents are **not** hardcoded in CLAUDE.md. They are defined at invocation time — description, trigger criteria, and model selection embedded in the plan phase where they're spawned. This keeps CLAUDE.md lightweight while giving each agent full context for its role.

### Research Pool (`/plan-start`)

| Agent | Trigger | Model |
|-------|---------|-------|
| `code-explorer` | Always | Sonnet |
| `arch-researcher` | Multi-layer changes (2+ layers) | Sonnet |
| `database-analyst` | Any DB schema changes | Sonnet |
| `security-analyst` | Auth, payments, PII, RBAC | Opus |
| `test-analyzer` | Non-trivial feature | Sonnet |
| `cross-platform-specialist` | Mobile parity needed | Sonnet |
| `native-app-specialist` | Tasks touch mobile/UI | Sonnet |
| `design-system-researcher` | UI changes in scope | Sonnet |
| `dependency-researcher` | New packages being added | Sonnet |
| `devops-specialist` | Docker, env vars, CI/CD | Sonnet |
| `integration-researcher` | New services, libraries, OTEL | Opus |
| `planning-coordinator` | Always (when 2+ agents) | Opus |

**Key design choices**:
- Opus only for high-stakes roles (security, integration, coordination)
- Sonnet for standard research (good quality, lower cost)
- `planning-coordinator` only spawned when 2+ agents are selected — it synthesizes, it doesn't research

### Validation Pool (`/plan-validate`)

See Layer 2 table above. These are different agents from the research pool — validators are not biased by the creation process.

---

## ADR Learning Loop

Every significant architectural decision generates an ADR. Over time, ADRs compound into institutional memory that reduces human interruptions.

### What Triggers an ADR

**Always create an ADR for:**
- Choice between multiple valid interaction patterns (overlay vs page, drawer vs modal)
- New animation or transition patterns not in existing conventions
- Platform divergence decisions (web vs mobile behavior)
- Loading state strategy that introduces a new pattern
- Auth strategy, DB schema approach, service boundary decisions
- New dependency selections with architectural implications

**Do NOT create an ADR for:**
- Decisions dictated by an approved source or existing convention
- Minor layout choices within established patterns
- Obvious state catalog entries (standard empty/loading/error states)

### Maturity Levels

```
1 ADR  → Watching   — tracked, not yet prescriptive
2 ADRs → Emerging   — presented as recommended default with precedent context
3+ ADRs → Confirmed — auto-resolved during planning (no human input needed)
          → Candidate for promotion to CLAUDE.md as hard rule
```

### The Loop

```
/plan-start Phase 2     →  ADR created
                               ↓
                        PATTERNS.md updated
                               ↓
/adr-review (periodic)  →  Detect patterns across ADRs
                               ↓
                        Propose CLAUDE.md promotions
                               ↓
Future /plan-start      ←  Confirmed rules auto-resolve decisions
```

Run `/adr-review` every 10-15 plans to batch-analyze patterns and propose CLAUDE.md additions.

**The compounding effect**: a project with 20 plans auto-resolves ~80% of architecture decisions. Human input focuses on genuinely novel decisions only.

---

## CLAUDE.md Discipline

### Hard Limit: 120 Lines

Every line in CLAUDE.md costs context on every request. A 300-line CLAUDE.md is overhead that runs before every single prompt. Set and enforce a hard limit.

**What earns a line in CLAUDE.md:**
- First principles (hard rules that override agent preferences)
- Confirmed ADR patterns (3+ occurrences)
- Project-specific conventions that agents cannot infer from the codebase
- Pointers to sub-files

**What should NOT be in CLAUDE.md:**
- Full content of design systems, env configs, architecture docs
- Rules that apply to <10% of tasks
- Explanations and rationale (write those in ADRs)

### Pointer Strategy

Instead of loading all context into CLAUDE.md, use pointers:

```markdown
## Context Files (load only when relevant)
- @docs/DESIGN_SYSTEM.md    — when UI changes are in scope
- @docs/ARCHITECTURE.md     — when service boundaries are touched
- @docs/ENV_CONFIG.md       — when Docker or env vars are modified
- @docs/ADR_PATTERNS.md     — during planning phases
```

Agents load only what their task requires. A backend task never loads the design system. Context stays clean.

### Regular Trimming

Review CLAUDE.md every 10-15 plans alongside `/adr-review`. Promote confirmed patterns, remove rules that have become obvious through codebase conventions, trim anything that hasn't been referenced.

---

## Context Management

### `/clear` Between Steps

Run `/clear` between `/plan-start`, `/plan-validate`, and `/plan-execute`. Each command is self-contained — the plan file on disk is the handoff artifact, not in-memory context.

Without `/clear`: context accumulates across all phases, compacting triggers earlier, agents inherit irrelevant context from previous phases, and token costs increase significantly.

### Why This Works

Each command reads its inputs from disk (plan files, ADRs, codebase). There's no state that needs to live in the context window between steps. The discipline of clearing between steps is what makes the pipeline scale to large projects without hitting context limits mid-execution.

---

## When to Use

### ✅ Use This Pipeline When

- Feature requires multiple files and layers (API + DB + UI)
- Security-sensitive changes (auth, payments, PII)
- Complex DB migrations
- New external service integrations
- Anything where a planning mistake would be expensive to undo
- Team projects where decision history matters

### ❌ Don't Use When

- Typo fix, trivial refactor (use standard `/plan` mode)
- Exploratory prototyping where requirements are unknown
- Hotfix under time pressure (use dual-instance planning instead)
- Changes touching ≤2 files with no architectural decisions

### ⚡ Tier 0 Shortcut

For small but non-trivial changes, still run the pipeline but the system will detect Tier 0 scope and skip agent spawning — research happens inline, validation is Layer 1 only, execution is single-agent. Same commands, lower overhead.

---

## Cost Profile

| Phase | Cost Driver | Approximate Range |
|-------|-------------|-------------------|
| `/plan-start` Tier 0 | Inline research only | $0.10-0.30 |
| `/plan-start` Tier 1-2 | 2-6 Sonnet agents | $0.50-2.00 |
| `/plan-start` Tier 3 | 7+ agents + Opus coordinator | $2.00-8.00 |
| `/plan-validate` | 0-8 agents | $0.20-3.00 |
| `/plan-execute` | Per-task agents + quality gate | $0.50-5.00 |
| **Typical feature (Tier 2)** | Full pipeline | **$2-10** |

Cost compounds as ADR coverage grows: fewer agents needed, fewer validation issues, faster execution.

Use `/plan-metrics` periodically to review historical cost trends and calibrate estimates.

---

## See Also

- [Plan-Driven Development](./plan-driven.md) — native `/plan` mode, lighter alternative
- [Dual-Instance Planning](./dual-instance-planning.md) — simpler 2-instance pattern
- [Agent Teams](./agent-teams.md) — native parallel coordination (experimental)
- [Task Management](./task-management.md) — Tasks API for cross-session coordination
- [Spec-First Development](./spec-first.md) — CLAUDE.md as specification contract
- [ADR Writer Agent](../../examples/agents/adr-writer.md) — standalone ADR generation
- [Plan Challenger Agent](../../examples/agents/plan-challenger.md) — adversarial plan review
