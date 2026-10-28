---
title: "Dual-Instance Planning Workflow"
description: "Separate planning and implementation with versioned handoffs, explicit ownership, and evidence-based review"
tags: [workflow, architecture, design-patterns]
---

# Dual-Instance planning workflow

Use separate sessions for architecture and implementation when a task benefits from an explicit design contract. The architect explores alternatives with the human; the engineer receives selected requirements, implements them, and returns reviewable evidence.

**Evidence**: practitioner accounts from [Jon Williams](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) and [Sami Honkonen](https://samihonkonen.com/posts/how-the-architect-talks-to-the-engineer/). Neither supplies a controlled comparison establishing lower cost, fewer defects, or reviewer independence. The protocol below adapts their ideas for this guide; it is not a native Claude Code feature.

## Table of contents

1. [TL;DR](#tldr)
2. [When to use this pattern](#when-to-use-this-pattern)
3. [Setup](#setup)
4. [Complete workflow](#complete-workflow)
5. [Plan template](#plan-template)
6. [Cost analysis](#cost-analysis)
7. [Tips and troubleshooting](#tips-and-troubleshooting)
8. [See also](#see-also)

## TL;DR

1. The architect resolves the design with the human and writes a self-contained handoff.
2. The authorized decision owner approves an identified contract revision and assigns the engineer.
3. The engineer checks the live repository, implements within scope, and submits a diff with verification evidence.
4. The architect reviews the implementation against requirements and applicable decisions.
5. The authorized merge owner closes the task after acceptance; durable decisions remain discoverable.

Share the selected contract and relevant evidence. Keep exploratory conversation out of the handoff unless it explains a constraint or rejected alternative the engineer needs.

## When to use this pattern

Use it for ambiguous requirements, consequential architecture decisions, or work that will continue in another session or environment. A single session can be sufficient for a bounded change with clear acceptance criteria. Separation adds authoring, coordination, and review work, so evaluate that overhead on your own task mix.

### Comparison to other patterns

| Pattern | What it separates | Main coordination need |
|---|---|---|
| Single instance | Planning and execution phases in one session | Retain requirements and verify the result |
| Dual-instance | Architecture conversation and implementation context | Versioned handoff, ownership, review feedback |
| Parallel instances | Concurrent units of work | Isolated edits, dependency handling, integration |

These choices can compose. Two role prompts do not enforce tool permissions, and separate contexts do not make reviews informationally independent.

## Setup

From your project root, create an optional plan directory:

```bash
mkdir -p .claude/plans/{Review,Active,Completed}
```

`Review/`, `Active/`, and `Completed/` are coordination conventions. Moving a file does not establish approval, prevent duplicate dispatch, or grant permission to commit, push, or deploy. Record the decision owner, approved contract revision, and assigned engineer in the task system you already use. Concurrent dispatch needs an ownership mechanism that can reject a second claim if duplicate execution matters.

Keep durable decisions in a discoverable location such as `docs/decisions/`. If plans are private or ignored, the handoff must still be accessible to its intended recipient. Choose one authoritative contract and link other representations to its revision.

### Architect session

```text
Explore the requested change and resolve material requirements with me.
Write the selected contract using the Plan template below.
Identify assumptions, alternatives, acceptance criteria, and open blockers.
Your implementation review must also challenge the plan's assumptions.
Implementation and external actions require their own authorized scope.
```

### Engineer session

```text
Read the approved handoff and applicable project instructions.
Check the repository state and assignment before changing files.
Implement within scope, preserving unrelated changes.
Report changed files, revision, checks actually run, and remaining limits.
If an assumption changes the contract, return a concrete amendment for decision.
```

Configure tool access appropriate to each role using the project's [permission and sandbox controls](../security/security-hardening.md). A role prompt is an instruction, not proof that writes or external actions are blocked. Use separate worktrees when sessions can edit concurrently.

## Complete workflow

### Phase 1: Planning

The architect reads current code and existing decisions, then clarifies questions that affect scope or acceptance. The handoff must stand on its own: objective, exclusions, base revision and relevant working-tree state, files or symbols, implementation approach, acceptance checks, applicable ADRs, blockers, action permissions, and next owner.

For example, a CSV export change might require existing filters to be preserved, correct escaping of commas and quotes, and no new access to records the requester cannot read. Identify the export service and its tests by path and symbol. Line numbers are optional navigation aids tied to the inspected revision; invented future line ranges add no evidence.

### Phase 2: Human review

The authorized decision owner checks the contract before dispatch. Existing authorization can cover the next action without a redundant confirmation. An unresolved decision that changes scope or external effects must be settled before dependent work.

Record approval against the contract revision. An amendment affecting scope, constraints, or acceptance requires a new recorded decision; a silent edit after approval invalidates the previous binding.

An **ADR** records a durable architectural choice: context, decision, alternatives, and consequences. A handoff records the current unit of work. Many small tasks need no ADR. In Honkonen's account, an ADR moves from Proposed to Accepted when the human gives the green light, then stays Accepted as implementation proceeds. Later decisions can supersede it independently of ticket status.

### Phase 3: Implementation

The engineer verifies the base, relevant files, assignment, and applicability of approved decisions. If the repository changed, inspect the impact before resuming. Run checks supporting the acceptance criteria and report failures and unknowns explicitly. A passing check establishes only what it covers.

Honkonen uses a self-contained Linear handoff comment plus optional ADRs. His engineer submits a GitHub PR, and the architect reviews it there. His custom `eng review <run> --feedback "..."` command carries feedback back to the engineer. This belongs to his tooling; it is not a Claude Code command. Use your existing issue, file, or review channel with equivalent traceability.

### Phase 4: Verification

Keep coordination state, execution state, and acceptance evidence distinct:

| Task state | Next responsible role | Evidence needed in this example protocol |
|---|---|---|
| Backlog | Architect and decision owner | Captured request; unresolved design visible |
| Todo | Assigned engineer | Accessible handoff, approved revision, blockers resolved |
| In Progress | Engineer | Claimed assignment, active run or recorded interruption |
| In Review | Designated reviewer | Diff at an identified revision, required check results |
| Done | Authorized merge owner | Accepted revision integrated; required post-merge verification recorded |

These are proposed conventions, not locks or permission grants. A run can be queued, running, failed, or awaiting review while its ticket remains In Progress. An ADR can remain Accepted through later ticket states. Define recovery for a stalled run without treating ticket status as execution evidence.

The architect checks requirements, code, tests, and design assumptions. Because this reviewer helped create the plan, checking only plan compliance can preserve a shared mistake. Use independent acceptance criteria and deterministic checks, plus additional review where risk justifies it. See [reviewer-independence evaluation](../roles/agent-evaluation.md#evaluate-judgment-allocation-and-reviewer-independence).

Return actionable feedback tied to the reviewed revision: affected file or symbol, observed defect, acceptance criterion, and expected correction. Automated review comments need assessment. Required checks and repository policy determine whether integration is permitted.

### Phase 5: Archive

After authorized integration and required verification, close the ticket and archive the plan. Keep the ADR discoverable. Record the accepted revision, check results, unresolved follow-ups, and next owner where applicable.

Compress the summary for future readers while retaining links to audit history. Repeated flaky checks, failed recovery, and operational incidents may deserve their own issue; omitting noise from a task summary does not justify deleting that evidence.

## Plan template

Save this as a plan file or task comment. This template is a guide adaptation, not a reproduction of Honkonen's tooling.

```markdown
# Contract: [task ID and objective]

## Scope
- Desired behavior and explicit exclusions:
- Base revision and relevant uncommitted state:
- Contract revision and authoritative location:

## Decisions
- Applicable ADRs and status:
- Selected approach and important rejected alternatives:
- Assumptions and unresolved blockers:

## Implementation
- Relevant paths and symbols at the inspected revision:
- Ordered steps, dependencies, and boundaries to preserve:

## Acceptance
- Observable success criteria:
- Checks, fixtures, and expected evidence:
- What these checks cannot establish:

## Ownership and authorization
- Decision owner and approval bound to contract revision:
- Assigned engineer and assignment record:
- Permitted actions and limits:
- Reviewer, merge owner, and next owner:
```

For session continuity, reuse [handoff-create](../../examples/skills/handoff-create/SKILL.md), [handoff-resume](../../examples/skills/handoff-resume/SKILL.md), and [handoff-update](../../examples/skills/handoff-update/SKILL.md). Historical completion entries must be reconciled with live state before acting.

## Cost analysis

### Dual-instance vs single instance with corrections

There is no universal correction-loop count at which two instances become cheaper or faster. Compare equivalent tasks under the same acceptance rule and budget policy. Include planning, implementation, retries, review, coordination, human attention, and rework in cost per accepted task. Keep billed API cost separate from subscription expenditure and quota use.

Report [four clocks](../roles/agent-evaluation.md#evaluation-epochs-and-four-clocks): feedback latency, run duration, human attention, and elapsed time to the accepted result. A shorter engineer run can coexist with a longer review queue. Use repeated paired tasks and report uncertainty before claiming a benefit.

## Tips and troubleshooting

- **Context handoff**: send the selected contract and relevant source links. Add missing facts when discovered; avoid forwarding the whole exploratory transcript by default.
- **Plan drift**: distinguish implementation adjustments within scope from changes to requirements or acceptance. Amend the latter explicitly.
- **Resume**: inspect live state before relying on old completion claims. Do not blindly repeat a migration, push, or other side effect whose outcome is unclear.
- **Duplicate work**: name an owner and record a claim. Concurrent dispatch needs enforceable assignment if duplicates matter.
- **Overhead**: start with the existing issue and a short handoff. Add an orchestrator only when a demonstrated coordination failure warrants it.

## See also

- [AI Design Patterns: Plan-then-execute](../core/ai-design-patterns.md#plan-then-execute): the pattern behind the planner and implementer split
- [Main guide overview and comparison](../ultimate-guide.md#alternative-pattern-dual-instance-planning-vertical-separation)
- [Plan-driven development](plan-driven.md)
- [Cross-session messaging contracts](cross-session-messaging.md)
- [Task management and continuity](task-management.md#the-continuity-artifact-progressmd)
- [Source evaluation: Honkonen's protocol](../../docs/resource-evaluations/honkonen-architect-engineer.md)

**Sources**: [Jon Williams's practitioner post](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu), February 3, 2026; [Sami Honkonen, How the architect talks to the engineer](https://samihonkonen.com/posts/how-the-architect-talks-to-the-engineer/), August 24, 2026. The article and its author's LinkedIn post are one account, not independent corroboration.
