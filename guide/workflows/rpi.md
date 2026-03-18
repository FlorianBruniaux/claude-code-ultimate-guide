---
title: "RPI: Research → Plan → Implement"
description: "A 3-phase feature development pattern with explicit validation gates between phases"
tags: [workflow, architecture, design-patterns, validation]
---

# RPI: Research → Plan → Implement

> **Confidence**: Tier 2 — Synthesized from production team patterns. The gate-based structure aligns with Anthropic's guidance on agent task decomposition and agentic loop control.

Build features in three locked phases: Research feasibility first, plan the implementation second, write code third. Each phase produces a concrete artifact. Each gate requires an explicit GO before the next phase starts.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [When to Use RPI](#when-to-use-rpi)
3. [How the Gates Work](#how-the-gates-work)
4. [Phase 1: Research](#phase-1-research)
5. [Phase 2: Plan](#phase-2-plan)
6. [Phase 3: Implement](#phase-3-implement)
7. [Slash Command Templates](#slash-command-templates)
8. [Worked Example](#worked-example)
9. [Comparison to Other Workflows](#comparison-to-other-workflows)
10. [Tips and Troubleshooting](#tips-and-troubleshooting)
11. [See Also](#see-also)

---

## TL;DR

```
Phase 1 — Research:
  Claude explores feasibility, surfaces risks, asks decision questions
  Output: RESEARCH.md
  Gate: You decide GO / NO-GO

Phase 2 — Plan:
  Claude writes architecture decisions, user stories, test plan
  Output: PLAN.md
  Gate: You approve the plan before any code is written

Phase 3 — Implement:
  Claude implements step by step, tests pass before each next step
  Output: working code + passing tests
  Gate: each implementation step validated before the next begins
```

**Best for**: Features with unclear feasibility, more than a day of work, unknown technical territory, or anything where discovering a wrong assumption late is costly.

---

## When to Use RPI

### Use RPI When

- **Feasibility is unknown**: You have an idea but aren't sure it holds up technically
- **Scope is large**: More than a day's worth of implementation work
- **Requirements are fuzzy**: You know the outcome you want, not the path to get there
- **Risk of wrong direction is high**: Security, payments, data migrations, integrations with external systems
- **You've been surprised before**: A feature looked simple, turned out to involve 6 other systems

### Skip RPI When

| Scenario | Better Approach |
|----------|----------------|
| Fix is obvious (typo, wrong color) | Direct edit |
| Feature is well-understood, requirements are clear | [Spec-First](./spec-first.md) or [dual-instance](./dual-instance-planning.md) |
| Exploration mode — you don't know what you want yet | Exploration workflow |
| Tiny change, single file | Just do it |

### Decision Heuristic

Ask yourself: "If the research phase reveals a serious problem, am I glad I didn't spend 2 days implementing first?"

If yes, run RPI. The research phase typically takes 30-60 minutes and can save many hours.

---

## How the Gates Work

RPI has two human gates and one automated gate per implementation step.

```
[Idea]
   |
   v
[Phase 1: Research]
   |
   +- NO-GO -> Stop. Document why. Archive RESEARCH.md.
   |
   +- GO -------------------------------------------------------->
                                                                 |
                                                       [Phase 2: Plan]
                                                                 |
                                          +- Needs revision -> iterate with Claude
                                          |
                                          +- Approved -------------------------------->
                                                                                      |
                                                                          [Phase 3: Implement]
                                                                              Step 1 -> Test gate
                                                                              Step 2 -> Test gate
                                                                              Step 3 -> Test gate
                                                                                   |
                                                                                [Done]
```

**Gate 1 (after Research)**: You read RESEARCH.md and make a GO/NO-GO decision. This is the most important gate — it prevents building the wrong thing entirely.

**Gate 2 (after Plan)**: You review PLAN.md before any code is written. Minor revisions happen here at zero cost.

**Step gates (during Implement)**: Each implementation step must have passing tests before Claude moves to the next step. Automated, no human action required unless a step fails.

---

## Phase 1: Research

### What Research Covers

The research phase answers five questions:

1. **What already exists?** Relevant code, libraries, prior attempts in the codebase
2. **What needs to be built?** Scope boundary, components to create vs modify
3. **What are the risks?** Technical, security, integration, performance
4. **What are the decision points?** Architecture choices that affect the whole plan
5. **What is the effort estimate?** Rough sizing before committing to a plan

Claude explores the codebase, reads relevant files, checks dependencies, and surfaces any constraint that would change the plan. The result is RESEARCH.md.

### Starting Research

Create the feature folder and invoke research:

```bash
mkdir -p .claude/features/[feature-name]
```

Then in Claude:

```
/rpi:research [feature description]
```

Or without the slash command:

```
Run RPI Phase 1 (Research) for: [feature description]

Save output to .claude/features/[feature-name]/RESEARCH.md
Use Plan Mode to explore without modifying code.
```

### RESEARCH.md Template

```markdown
# Research: [Feature Name]

**Date**: [YYYY-MM-DD]
**Requested**: [One-sentence description of the feature]
**Status**: PENDING DECISION

---

## What Exists Today

### Relevant Code
- [file path]: [what it does, why it matters]
- [file path]: [what it does, why it matters]

### Relevant Libraries
- [library]: [currently used / available / needs to be added]

### Prior Attempts or Related Work
- [any existing partial implementation, related PR, note in codebase]

---

## What Needs to Be Built

### New Files
- [file path]: [purpose]
- [file path]: [purpose]

### Files to Modify
- [file path]: [what changes, why]

### External Dependencies
- [dependency]: [reason needed, version constraint if any]

---

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| [risk description] | Low/Med/High | Low/Med/High | [mitigation or blocker] |

---

## Architecture Decision Points

Questions that need a decision before planning can start:

1. **[Decision]**: Option A (pros: X, cons: Y) vs Option B (pros: X, cons: Y)
2. **[Decision]**: [Options and trade-offs]

---

## Effort Estimate

- Research-to-plan: [time]
- Implementation: [time range]
- Testing: [time]
- **Total estimate**: [range]

**Confidence in estimate**: Low / Medium / High
**Why**: [reason for confidence level]

---

## Recommendation

[GO / NO-GO / NEEDS CLARIFICATION]

[1-3 sentences explaining the recommendation]

---

**Decision**: [ ] GO  [ ] NO-GO  [ ] NEEDS CLARIFICATION
**Notes**: [human fills this in]
```

### What a NO-GO Looks Like

Not every research phase ends in GO. Common NO-GO reasons:

- **Technical blocker**: External API doesn't support the required operation
- **Scope creep discovered**: "Simple feature" turns out to require rewriting the auth layer
- **Better alternative exists**: Research reveals an existing library or config change that solves the problem more simply
- **Risk too high for now**: The feature is valid but the timing is wrong

Archive NO-GO research docs — they're valuable records of decisions made and why.

---

## Phase 2: Plan

### What the Plan Covers

Phase 2 starts only after you mark RESEARCH.md with GO. Claude reads the research doc and produces a precise implementation plan.

A good plan is specific enough that a different engineer (or Claude in a new session) could execute it without asking questions.

```
/rpi:plan .claude/features/[feature-name]/RESEARCH.md
```

Or without the slash command:

```
Run RPI Phase 2 (Plan) using:
- Research: .claude/features/[feature-name]/RESEARCH.md

Save output to .claude/features/[feature-name]/PLAN.md
Do not write any code yet. Plan only.
```

### PLAN.md Template

```markdown
# Plan: [Feature Name]

**Date**: [YYYY-MM-DD]
**Research**: [link to RESEARCH.md]
**Estimated effort**: [from research]
**Risk level**: Low / Medium / High

---

## Summary

[2-4 sentences: what this implements, major design decisions taken, what it does NOT include]

---

## Architecture Decisions

[Record decisions made from the research decision points]

1. **[Decision]**: Chose [Option] because [reason]
2. **[Decision]**: Chose [Option] because [reason]

---

## Implementation Steps

Steps must be sequential and independently testable.

### Step 1: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 2 starts]

### Step 2: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 3 starts]

[...continue for all steps]

---

## Success Criteria

- [ ] [Testable criterion — describes observable behavior, not implementation]
- [ ] [Testable criterion]
- [ ] All step test gates pass

---

## Out of Scope

Explicitly list what this plan does NOT cover:
- [thing excluded]
- [thing excluded]

---

## Risks Accepted

[From RESEARCH.md risks, list which are accepted and how they're mitigated]

---

## Rollback Plan

If implementation fails mid-way:
- [what to undo]
- [how to restore previous state]

---

**Plan approved?** [ ] YES — proceed to implementation
**Revision notes**: [human fills this in if changes needed]
```

### Reviewing the Plan

Read PLAN.md carefully before approving. The goal is to catch design problems now, not during implementation. Specific things to check:

- Implementation steps are in the right order, with no hidden dependencies
- Test gates are concrete and runnable (not "it looks right")
- Out-of-scope is explicit (prevents Claude from over-building)
- Rollback plan exists for anything touching data or shared state

If the plan needs changes, ask Claude to revise before approving. This is free — revision after approval costs implementation time.

---

## Phase 3: Implement

### The Step-Gate Pattern

Implementation runs step by step. Each step has a test gate. Claude does not start the next step until the current gate passes.

```
/rpi:implement .claude/features/[feature-name]/PLAN.md
```

Or without the slash command:

```
Run RPI Phase 3 (Implement) using:
- Plan: .claude/features/[feature-name]/PLAN.md

Rules:
- Implement one step at a time
- After each step, run the test gate specified in the plan
- Do not start the next step until the test gate passes
- If a test gate fails, stop and report the failure — do not improvise a fix
- Commit after each step that passes its gate
```

### What Happens During Implementation

Claude works through the plan's steps sequentially. For each step:

1. Implements the specified files and changes
2. Runs the test gate (unit tests, integration check, or manual verification)
3. If gate passes: commits with a message referencing the step, announces readiness for the next step
4. If gate fails: reports the failure, the specific test output, and the likely cause. Does not attempt to fix unless you confirm.

The step-commit pattern gives you a clean git history that mirrors the plan. If something goes wrong in Step 4, you can roll back to the Step 3 commit cleanly.

### Step-Gate Failure Protocol

When a test gate fails, Claude reports:

```
Step [N] gate failed.

Gate: [what was supposed to pass]
Output:
[actual test output]

Likely cause: [Claude's diagnosis]
Options:
1. Fix: [specific change that would likely fix it]
2. Revise plan: [if the plan step itself has a flaw]
3. Stop and investigate: [if the failure reveals something unexpected]

Which should I do?
```

You decide. Claude does not auto-fix and proceed — that's how implementations drift from plans.

---

## Slash Command Templates

Save these to `.claude/commands/` to invoke each phase directly.

### `/rpi:research`

Save to `.claude/commands/rpi-research.md`:

```markdown
# RPI Phase 1: Research

Run feasibility research for the requested feature.

## Instructions

1. Enter Plan Mode (do not modify files during research)
2. Explore the codebase to answer these questions:
   - What already exists that's relevant?
   - What files will need to change or be created?
   - What are the technical risks?
   - What decisions need to be made before planning?
   - What is a rough effort estimate?
3. Save output to `.claude/features/$ARGUMENTS/RESEARCH.md` using the template below
4. End with a clear recommendation: GO, NO-GO, or NEEDS CLARIFICATION
5. Ask the user for their GO/NO-GO decision before proceeding

## Constraints

- Do NOT write any code
- Do NOT modify any files
- Do NOT start planning implementation steps
- If uncertain about scope, surface it as a decision point
```

### `/rpi:plan`

Save to `.claude/commands/rpi-plan.md`:

```markdown
# RPI Phase 2: Plan

Create an implementation plan based on approved research.

## Pre-check

Before starting:
1. Read the RESEARCH.md file specified in $ARGUMENTS
2. Verify it has a GO decision marked
3. If no GO decision found, stop and ask the user to decide first

## Instructions

1. Read RESEARCH.md carefully
2. Create PLAN.md in the same feature folder
3. Architecture decisions: resolve all decision points from research
4. Implementation steps: each step must have a concrete test gate
5. Success criteria: observable, testable, not implementation-internal
6. Out-of-scope: explicit list of what this plan does NOT cover
7. Do NOT write any implementation code
8. After writing the plan, ask the user to review and approve

## Constraints

- Do NOT write implementation code
- Steps must be sequential and independently testable
- Test gates must be runnable commands or precise manual checks, not vague descriptions
- Each step should be achievable in a single focused session
```

### `/rpi:implement`

Save to `.claude/commands/rpi-implement.md`:

```markdown
# RPI Phase 3: Implement

Implement the feature following an approved plan, one step at a time.

## Pre-check

Before starting:
1. Read the PLAN.md file specified in $ARGUMENTS
2. Verify it has an approval marked
3. If no approval found, stop and ask the user to approve first

## Instructions

For each step in the plan:
1. Read the step description carefully
2. Implement only what the step specifies — nothing more
3. Run the test gate exactly as written in the plan
4. If the gate passes:
   - Commit with message: "feat([feature]): step [N] — [step name]"
   - Announce step completion and readiness for next step
5. If the gate fails:
   - Report the exact failure output
   - Diagnose the likely cause
   - Present options (fix, revise plan, stop)
   - Wait for human decision before proceeding

## Constraints

- Never skip a test gate
- Never start the next step before the current gate passes
- Never modify files outside the scope of the current step
- If you encounter something unexpected that changes the plan, stop and report it
- Commit after each passing step — not at the end
```

---

## Worked Example

**Request**: "Add rate limiting to the public API endpoints."

### Phase 1: Research Output (abbreviated)

```markdown
# Research: API Rate Limiting

**Date**: 2026-03-12
**Status**: PENDING DECISION

## What Exists Today

- `src/middleware/` — has auth middleware, no rate limiting
- `package.json` — express-rate-limit not installed, redis available
- `src/routes/api.ts` — 14 public endpoints, unauthenticated routes mixed with authenticated ones

## What Needs to Be Built

- Rate limiter middleware for public endpoints
- Separate limits for authenticated vs unauthenticated users
- Redis store for distributed rate limiting (app runs on 3 instances)

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| Redis connection failure disables all API access | Low | High | Need fallback to in-memory if Redis unavailable |
| Rate limit too aggressive — breaks existing integrations | Medium | High | Need to survey current usage patterns first |

## Architecture Decision Points

1. **Library**: express-rate-limit (maintained, battle-tested) vs custom middleware
2. **Bypass for trusted IPs**: Allow internal services to bypass rate limiting?

## Effort Estimate

- Implementation: 2-4 hours
- Testing: 2 hours
- **Total**: 4-6 hours

**Recommendation**: GO — standard problem, good library options, main risk is Redis fallback which is solvable.
```

**Human decision**: GO. Use express-rate-limit. No IP bypass for now.

### Phase 2: Plan (abbreviated)

```markdown
# Plan: API Rate Limiting

**Risk level**: Medium (shared Redis state, potential to block legitimate traffic)

## Architecture Decisions

1. Library: express-rate-limit with rate-limit-redis store
2. No IP bypass initially — revisit if internal service issues arise
3. Unauthenticated: 100 requests/15 minutes. Authenticated: 1000 requests/15 minutes.
4. Redis failure fallback: in-memory store (accepts single-instance inconsistency)

## Implementation Steps

### Step 1: Install dependencies and configure Redis store

**Files**: `package.json`, `src/config/rate-limit.ts`
**Test gate**: `npm install` completes, `src/config/rate-limit.ts` exports config without errors

### Step 2: Implement rate limiter middleware

**Files**: `src/middleware/rate-limit.ts`
**Test gate**: Unit test — limiter blocks 101st request from same IP within 15 minutes

### Step 3: Apply to routes

**Files**: `src/routes/api.ts`
**Test gate**: Integration test — unauthenticated route returns 429 after 100 requests; authenticated route does not

### Step 4: Add Redis fallback

**Files**: `src/config/rate-limit.ts`
**Test gate**: Test with Redis unavailable — API still responds (200, not 500), in-memory limiting active
```

**Human review**: Approved.

### Phase 3: Implementation

Claude implements Step 1, runs the gate (`npm install` + import check), commits `feat(rate-limit): step 1 — dependencies and config`. Then Step 2, Step 3, Step 4 in sequence. Each commit is clean. Each gate must pass before proceeding.

---

## Comparison to Other Workflows

| Workflow | Phase structure | Human gates | Best for |
|----------|----------------|------------|----------|
| **RPI** | Research + Plan + Implement | GO/NO-GO + plan approval | Unknown feasibility, >1 day, high risk of wrong direction |
| **Dual-Instance** | Plan + Implement (separate Claude instances) | Plan approval | Known features needing careful execution, spec-heavy work |
| **Spec-First** | Spec + Implement | None (spec is implicit gate) | Design-focused work, API contracts, team alignment |
| **TDD** | Test-first + Implement | None (tests are the gate) | Test coverage as driver, refactoring, incremental behavior |
| **Direct** | None | None | Simple changes, obvious scope, less than 2 hours |

### RPI vs Dual-Instance

Dual-instance separates planning and implementation into two Claude instances with strict role enforcement. It works well when you already know what you're building and want a high-quality plan. RPI adds a feasibility phase before planning, which makes it better for ambiguous requests. If you already have a clear spec, skip Research and use dual-instance or spec-first.

### RPI vs Spec-First

Spec-first is design-oriented: you define what the system should do, then Claude implements it. RPI is implementation-oriented with validation gates: you describe a goal, Claude researches how to achieve it, then the two of you agree on a plan before touching code. Use spec-first when the design is clear. Use RPI when the technical path is not.

### RPI vs Direct Coding

For anything under 2 hours with a clear scope, just ask Claude to do it. RPI adds overhead that isn't justified for small tasks. The research phase alone takes 30-60 minutes. That overhead pays off on multi-day features where discovering a wrong assumption late is much more expensive.

---

## Tips and Troubleshooting

### Claude Skips to Implementation in Research Phase

**Problem**: Claude starts writing code during the research phase.

**Solution**: Use Plan Mode (Shift+Tab twice) explicitly for the research phase. Include this line in the research command:

```
You are in Plan Mode. Do not modify files. Do not write implementation code.
Research only. Output goes to RESEARCH.md.
```

Or add to your CLAUDE.md:

```markdown
## RPI Rules
- /rpi:research runs in Plan Mode only — no file modifications
- /rpi:plan produces only PLAN.md — no implementation code
- /rpi:implement runs one step at a time, waits for test gate before next step
```

### Research Phase Runs Too Long

**Problem**: Claude explores the entire codebase instead of focusing on what's relevant.

**Solution**: Scope the research explicitly:

```
/rpi:research payment-processing

Focus area: src/payments/, src/routes/checkout.ts
Do not explore: frontend, auth, unrelated backend modules
Time budget: complete research in one session
```

### Plan Has Too Many Steps

**Problem**: PLAN.md has 12 steps, making the implementation unwieldy.

**Solution**: A plan with more than 6-8 steps usually needs a scope reduction, not more granular implementation. Ask Claude:

```
The plan has too many steps. What is the minimal viable scope that delivers
the core value? Revise the plan to implement only that, with a clear
"Future work" section for the rest.
```

### Test Gates Are Vague

**Problem**: A step's test gate says "verify it works" rather than a specific command.

**Solution**: Reject vague gates before approving the plan. Push back with:

```
Step 3's test gate is "verify rate limiting works." Make it specific:
what command do I run, and what output do I expect to see when it passes?
```

A good test gate:

```
Test gate: `npm test src/middleware/rate-limit.test.ts` — all 4 tests pass
```

A bad test gate:

```
Test gate: rate limiting is working correctly
```

### A Step Gate Fails Repeatedly

**Problem**: Step 2's gate keeps failing even after attempted fixes.

**Solution**: Two failures means investigate the plan, not keep iterating on fixes.

```
Stop implementation. The Step 2 gate has failed twice.
Review the plan — is the test gate achievable given the Step 1 output?
Do we need to revise the plan before continuing?
```

---

## File Structure Summary

```
.claude/
└── features/
    └── [feature-name]/
        ├── RESEARCH.md     # Phase 1 output (human annotates GO/NO-GO)
        └── PLAN.md         # Phase 2 output (human annotates approval)

.claude/commands/
├── rpi-research.md         # /rpi:research slash command
├── rpi-plan.md             # /rpi:plan slash command
└── rpi-implement.md        # /rpi:implement slash command
```

Archive completed features:

```bash
mkdir -p .claude/features/_archive
mv .claude/features/payment-processing .claude/features/_archive/
```

The archive is a learning resource: completed RESEARCH.md and PLAN.md files show how previous features were reasoned about.

---

## See Also

- [dual-instance-planning.md](./dual-instance-planning.md) — Two-instance pattern for spec-heavy implementation
- [spec-first.md](./spec-first.md) — Design-first workflow using CLAUDE.md as contract
- [tdd-with-claude.md](./tdd-with-claude.md) — Combine with TDD for test-gate implementation
- [task-management.md](./task-management.md) — Managing multi-phase tasks across sessions
- **Main guide**: Advanced Patterns section — Multi-instance and planning pattern overview