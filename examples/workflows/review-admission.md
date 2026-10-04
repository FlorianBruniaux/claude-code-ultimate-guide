---
name: review-admission
description: "Define shared review capacity, pause and resume rules, and a tabletop exercise"
complexity: intermediate
time: varies
domain: testing
status: experimental
keywords: [review, capacity, queue, agents]
---

# Review admission policy worksheet

This is a proposed policy worksheet, not an installed scheduler or a validated throughput improvement. Apply it to one service and a comparable class of changes.

| Field | Team decision |
|---|---|
| Queue and accountable owner | |
| Eligible change class and excluded work | |
| User-facing result and evidence of completion | Name the behavior or resolved problem; record release and adoption separately from review acceptance |
| Known defect and earlier preventive check | Keep the incident, a case the check must reject, and a neighboring valid case it must allow |
| Baseline observation window | |
| Arrival event | First declaration of readiness at a stated revision |
| Acceptance event | Acceptance by the required policy at that revision |
| Queued work and reserved slots | Count unique changes; track in-flight authors separately |
| Age measure and owner-approved limit | |
| Pause rule | Pause new authoring when the queue or age limit is reached, capacity is unavailable, or telemetry is stale |
| Resume rule | Use a lower queue threshold, acceptable age, fresh telemetry, and available verification capacity |
| Work allowed during pause | Existing review, agreed corrections, incident response within existing authority |
| Urgent exception | Named approver, reason, bounded scope, displaced work, expiry |
| Cost of this policy | Reviewer effort, repeated checks, false blocks, bypasses and maintenance work |

Start with declared availability and a named verifier. The first pilot can remain a manual policy. If admission is automated, reserve a verification slot atomically before dispatch and make release or conversion idempotent under a stable reservation identity. Reconcile an uncertain acknowledgement before retrying. A canceled task does not count as an accepted change. Corrections remain attached to their original change. A new revision invalidates affected acceptance evidence.

Every deferred task records its reason, owner, resumption condition and expiry or review point. Repeated deferrals require reconsideration, reduced scope, reassignment or explicit cancellation under the agreed policy. Expiring a reservation does not authorize its previous holder to continue. Do not infer fatigue from activity telemetry or add a scheduler merely to implement this worksheet.

## Tabletop exercise

The following numbers are synthetic policy inputs, not recommended team limits. Assume a queue limit of three occupied/reserved slots, resume at one or fewer, a chosen age limit, and fresh telemetry.

| State or event | Expected decision |
|---|---|
| Two occupied slots; two authors request admission together | Reserve one slot, admit one author, queue the other; never overbook |
| Three occupied slots; existing reviewer completes a check | Allow the review to finish; do not cancel it because authoring is paused |
| Two slots after acceptance | Stay paused until the resume condition is met |
| One slot but its oldest change exceeds the age limit | Stay paused; resolve the aging change |
| One slot, acceptable age, fresh telemetry, reviewer available | Resume admission under the reservation rule |
| Queue data unavailable or reviewer unavailable | Pause new authoring; retain records and route the blocker to the owner |
| Urgent request without named exception approval | Keep queued |

Record observed decisions when exercising an implementation. Until then, these are expected outcomes only. Compare equivalent change classes over comparable windows. Track accepted changes, escaped defects, human effort and time to the named user result alongside queue size so that faster approvals do not masquerade as improvement. If the policy delays the complete result or blocks valid work without preventing the known failure, revise it with the owner.

The [local control exercise](review-control-demo.py) tests durable budgets and concurrent effects on a simulated service. It does not implement this capacity policy or measure human availability.
