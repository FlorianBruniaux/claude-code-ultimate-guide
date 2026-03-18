---
title: "Plan-Driven Development"
description: "Use /plan mode for non-trivial tasks to explore and propose implementation plans"
tags: [workflow, guide, architecture]
---

# Plan-Driven Development

> **Confidence**: Tier 1 — Based on Claude Code's native /plan mode functionality.

Use `/plan` mode for anything non-trivial. Claude explores the codebase (read-only), then proposes an implementation plan for your approval.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [The /plan Workflow](#the-plan-workflow)
3. [When to Use](#when-to-use)
4. [Plan File Structure](#plan-file-structure)
5. [Integration with Other Workflows](#integration-with-other-workflows)
6. [Tips](#tips)
7. [Advanced: Custom Markdown Plans (Boris Tane Pattern)](#advanced-custom-markdown-plans-boris-tane-pattern)
8. [See Also](#see-also)

---

## TL;DR

```
1. Enter Plan Mode (Shift+Tab twice) or ask complex question
2. Claude explores codebase (read-only)
3. Claude writes plan to .claude/plans/
4. You review and approve
5. Claude executes
```

---

## The /plan Workflow

### Step 1: Enter Plan Mode

Toggle Plan Mode with `Shift+Tab` (press twice to cycle Normal → Auto-Accept → Plan):
```
# Press Shift+Tab twice to enter Plan Mode
# (Plan Mode indicator appears in the UI)
```

Or ask a complex question that triggers plan mode automatically:
```
How should I refactor the authentication system to support OAuth?
```

### Step 2: Claude Explores

In plan mode, Claude:
- Reads relevant files
- Searches for patterns
- Understands existing architecture
- CANNOT make any changes

### Step 3: Claude Writes Plan

Claude creates a plan file at `.claude/plans/[name].md`:

```markdown
# Plan: Refactor Authentication for OAuth

## Summary
Add OAuth support while maintaining existing email/password auth.

## Files to Modify
- src/auth/providers/index.ts (add OAuth provider)
- src/auth/middleware.ts (handle OAuth tokens)
- src/config/auth.ts (OAuth config)

## Files to Create
- src/auth/providers/oauth.ts
- src/auth/providers/google.ts

## Implementation Steps
1. Create OAuth provider interface
2. Implement Google OAuth provider
3. Update middleware to detect token type
4. Add OAuth routes
5. Update config schema

## Risks
- Breaking existing sessions during migration
- Token format differences between providers
```

### Step 4: You Review

Review the plan for:
- Completeness (all requirements covered)
- Correctness (right approach for your codebase)
- Scope (not over-engineering)

### Step 5: Approve and Execute

```
Looks good. Proceed with the plan.
```

Or request changes:
```
Modify the plan: also add support for GitHub OAuth, not just Google.
```

---

## When to Use

### Use Plan Mode

| Scenario | Why |
|----------|-----|
| Multi-file changes | See all affected files upfront |
| Architecture changes | Validate approach before coding |
| New features | Ensure complete implementation |
| Unfamiliar codebase | Let Claude explore first |
| Risky operations | Review before execution |

### Skip Plan Mode

| Scenario | Why |
|----------|-----|
| Single-line fixes | Obvious, low risk |
| Typo corrections | No planning needed |
| Simple questions | Exploration, not implementation |
| Adding comments | Trivial change |

---

## Plan File Structure

Plans are stored in `.claude/plans/` with auto-generated names.

### Typical Plan Sections

```markdown
# Plan: [Title]

## Summary
[1-2 sentence overview]

## Context
[Why this change is needed]

## Files to Modify
[List of existing files that will change]

## Files to Create
[List of new files]

## Files to Delete
[List of files to remove, if any]

## Implementation Steps
[Ordered list of steps]

## Testing Strategy
[How to verify the changes]

## Risks & Mitigations
[What could go wrong and how to handle it]

## Open Questions
[Things to clarify before proceeding]
```

---

## Integration with Other Workflows

### Plan + TDD

```
# Enter Plan Mode (Shift+Tab twice), then:

I need to implement a rate limiter.
Plan the test cases first, then the implementation.
```

Claude plans both tests and implementation in proper TDD order.

### Plan + Spec-First

```
# Enter Plan Mode (Shift+Tab twice), then:

Review the Payment Processing spec in CLAUDE.md.
Create an implementation plan that satisfies all acceptance criteria.
```

### Plan + Task Tool

After plan approval, Claude can break down into tasks:

```
Approved. Create tasks from this plan and start implementing.
```

---

## Tips

### Be Specific About Scope

```
# Too vague (after entering Plan Mode via Shift+Tab twice)
Improve the API

# Better
Add pagination to the /users endpoint with cursor-based navigation.
Maintain backwards compatibility with existing clients.
```

### Request Plan Modifications

```
The plan looks good but:
- Add error handling for network failures
- Skip the caching optimization for now
- Include rollback procedure
```

### Use for Architecture Decisions

```
# Enter Plan Mode (Shift+Tab twice), then:

I'm considering two approaches for state management:
A) Redux Toolkit
B) Zustand

Explore the codebase and recommend which fits better.
```

### Save Plans for Documentation

Plans in `.claude/plans/` serve as decision documentation:
- Why certain approaches were chosen
- What files were expected to change
- Implementation order rationale

---

## Advanced: Custom Markdown Plans (Boris Tane Pattern)

> **Source**: Boris Tane, Engineering Lead @ Cloudflare — ["How I use Claude Code"](https://boristane.com/blog/how-i-use-claude-code/) (Feb 2026). 9 months of production usage.
> **Confidence**: Tier 2 — Practitioner-validated pattern, not official Anthropic documentation.

When Plan Mode isn't enough, iterative human/agent planning before any code is written.

### Why Custom Plans Over /plan

| Factor | Plan Mode (native) | Custom .md plan |
|--------|----------------|-----------------|
| **Persistence** | Lost on context compaction | Survives compaction, shareable |
| **Review surface** | Chat-based, linear | Structured file, diffs |
| **Iteration** | Back-and-forth in conversation | Annotate file, re-run |
| **Shared state** | Per-session | "Shared mutable state" between human and agent |
| **Best for** | Standard features, <30 min tasks | Complex features, architectural decisions |

**Decision rule**: Use Plan Mode (Shift+Tab twice) for known scope. Use custom `.md` plans when you expect misunderstandings or want explicit sign-off on approach before a single line of code.

---

### The Three-Phase Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: RESEARCH                                              │
│  → Emphatic prompt → research.md (written, not verbal)          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: PLANNING (Annotation Cycle)                           │
│  → plan.md draft → human annotates → agent updates → repeat    │
│  → Exit: plan approved, no open questions                       │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: IMPLEMENTATION                                        │
│  → Mechanical execution, decisions already made                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Emphatic Research

Claude skims without strong signal. Use emphatic language to force depth:

```
Research the authentication system in this codebase deeply.
Understand the intricacies of how sessions are managed, in great detail.
Cover edge cases, existing patterns, and any non-obvious dependencies.

Write your findings to research.md — do not implement anything.
```

**Why it works**: "deeply", "in great detail", "intricacies" shift Claude from surface scan to thorough investigation. Output must be written to a file — verbal summaries disappear on context compaction.

**Research.md should include**:
- Existing patterns and conventions
- File paths and key functions
- Non-obvious dependencies
- Constraints and risks identified

---

### Phase 2: The Annotation Cycle

The core of the Boris Tane pattern. Iterate on `plan.md` until ready, **before any implementation**.

```
┌──────────────────────────────────────────────────────────────┐
│                    ANNOTATION CYCLE                           │
│                                                              │
│  Human prompt ──→ Agent writes plan.md                       │
│       ↑                    ↓                                 │
│  Annotate plan    Human reviews plan.md                      │
│  (add comments,          ↓                                   │
│   ask questions,   Issues found?                             │
│   flag trade-offs)       ├─ Yes → Annotate → loop           │
│                          └─ No  → Approved → Phase 3        │
│                                                              │
│  Typical: 1-6 iterations before approval                     │
└──────────────────────────────────────────────────────────────┘
```

**Guard prompt** — always include this to prevent premature implementation:

```
Based on research.md, write a plan for implementing [feature].

Include: approach, affected file paths, code snippets for key decisions,
trade-offs considered, and open questions.

Write to plan.md. Do NOT implement anything yet.
```

**What plan.md should contain**:

```markdown
# Plan: [Feature Name]

## Approach
[Strategy and rationale]

## Files Affected
- path/to/file.ts — what changes and why
- path/to/other.ts — what changes and why

## Key Implementation Details
[Code snippets for non-obvious parts — not the full implementation]

## Trade-offs
- Option A vs B: chose A because X
- Considered but rejected: Y (reason)

## Open Questions
- [ ] Should we handle edge case Z?
- [ ] Does this affect the mobile client?
```

**Annotation example**:

```markdown
## Approach
Use JWT tokens stored in httpOnly cookies.
<!-- Human annotation: ✓ Agreed. But also consider refresh token rotation -->

## Open Questions
- [ ] Should we handle token expiry in middleware?
<!-- Human annotation: Yes, centralize this — don't leave it to each route -->
```

**Exit criteria** — plan is ready when:
- No open questions remain
- Trade-offs are documented and agreed
- File paths are specific (not "some auth file")
- Key snippets show the approach, not just describe it

> "The markdown file acts as shared mutable state between you and the agent." — Boris Tane

---

### Phase 3: Mechanical Implementation

Once the plan is approved, implementation becomes execution — no creative decisions left.

```
Implement everything in plan.md.
Work through each item sequentially.
Mark tasks as completed as you go with [x].
Do not stop between tasks to ask for confirmation — keep going until done.
```

**Feedback during implementation**:
- Keep it terse: short phrases or screenshots, not paragraphs
- Decisions are already made — redirect scope changes back to plan.md
- If something unexpected comes up: pause, update plan.md, continue

**Mindset shift**: Phase 3 is mechanical. All thinking happened in Phase 2.

---

### Complementary Techniques

| Technique | What | When |
|-----------|------|------|
| **Cherry-picking** | Implement subset of plan.md | Plan too large, ship incrementally |
| **Scope trimming** | Remove items from plan before implementing | Reduce risk, focus on core |
| **Reference-based guidance** | Point to existing code: "do it like auth.ts" | Enforce consistency |
| **Revert & re-scope** | `git revert` + restart with narrower plan | Plan went wrong, reset cleanly |

---

## See Also

- [exploration-workflow.md](./exploration-workflow.md) — Explore alternatives before planning
- [../ultimate-guide.md](../ultimate-guide.md) — Section 2.3 Plan Mode
- [tdd-with-claude.md](./tdd-with-claude.md) — Combine with TDD
- [spec-first.md](./spec-first.md) — Combine with Spec-First
- [iterative-refinement.md](./iterative-refinement.md) — Post-plan iteration
- [task-management.md](./task-management.md) — Track plan execution across sessions with Tasks API
- [dual-instance-planning.md](./dual-instance-planning.md) — Advanced: Use two Claude instances (planner + implementer) for quality-focused workflows
