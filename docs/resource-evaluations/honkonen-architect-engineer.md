# Honkonen: How the architect talks to the engineer

**Reviewed**: 2026-10-17. **Editorial relevance**: 4/5, selective integration. This is a relevance judgment, not a measured workflow result.

## Source and evidence boundary

[Sami Honkonen's article](https://samihonkonen.com/posts/how-the-architect-talks-to-the-engineer/), August 24, 2026, and [his LinkedIn post](https://www.linkedin.com/posts/samihonkonen_my-ai-architect-and-engineer-never-share-share-7497615617869443072-4We9/) describe one practitioner's setup. The full article was read; the post and supplied diagram provide context, not independent corroboration. No private implementation, CI policy, run history, or production outcome was audited.

The architect works in Cursor and hands a self-contained Linear comment and optional repository ADRs to an engineer dispatched through custom `eng` tooling. The engineer returns a GitHub PR. Architecture review occurs on GitHub; detailed feedback returns through `eng review <run> --feedback "..."`, not through Linear. The article reports CI and Bugbot merge gates without supplying their implementation for this review.

## What adds value

The guide already described a planner/implementer split. The useful addition is the communication contract: selected requirements cross the boundary, durable decisions have their own owner, and task status identifies the next actor. Two contexts alone do not provide these properties.

| Integration | Why it is needed |
|---|---|
| Self-contained, versioned handoff | Prevent dependence on an unavailable exploratory conversation |
| Separate task, run, and ADR state | Avoid treating a turn marker as execution, acceptance, or authority |
| Review feedback bound to a revision | Make the correction actionable and traceable |
| Resume against live evidence | Preserve history without blindly trusting old completion claims |
| Evidence-based cost comparison | Remove unsupported monthly budgets and a universal two-correction-loop break-even claim |

The guide adds base-state recording, approval bound to contract revision, explicit action scope, assignment checks, and independent acceptance criteria as its own adaptations. These controls are not claims about the author's implementation. A new orchestrator, Linear dependency, or permanent always-on machine is unnecessary to teach the protocol.

## Challenge and decision

The 4/5 score reflects a concrete improvement to an existing workflow and correction of unsupported claims. It does not establish that separation improves plans, reduces defects, or costs less. An architect reviewing its own plan can preserve a shared error; fresh context does not establish independent judgment. A prompt cannot enforce permissions, and a task label cannot reject duplicate dispatch on its own.

The author's compressed final summary is useful for retrieval, but should not become a general instruction to discard incident or recurring-CI evidence. Our adaptation retains links to audit history and separates operational follow-ups from the task summary.

A separate technical-writer review checked attribution, evidence limits, score justification, and integration links. It retained 4/5 and identified two navigation/template consistency issues, corrected in the integration. This documentary challenge does not validate runtime behavior.

## Integrated locations

- [Dual-instance workflow and plan template](../../guide/workflows/dual-instance-planning.md).
- [Main guide overview](../../guide/ultimate-guide.md#alternative-pattern-dual-instance-planning-vertical-separation).
- [Task continuity](../../guide/workflows/task-management.md#how-this-composes-with-the-handoff-triad).
- Distributed templates: [create](../../examples/skills/handoff-create/SKILL.md), [resume](../../examples/skills/handoff-resume/SKILL.md), and [update](../../examples/skills/handoff-update/SKILL.md). These edits do not install or activate skills in either host.

Blog proposals remain separate from this guide integration. No article publication or measured local outcome is claimed.
