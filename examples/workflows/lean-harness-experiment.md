---
name: lean-harness-experiment
description: "Test one repository harness countermeasure against a known failure and its operating cost"
complexity: intermediate
time: varies
domain: testing
status: experimental
keywords: [lean, harness, countermeasure, evaluation]
---

# Repository harness countermeasure worksheet

Use this for one recurring failure in one class of task. It is a proposed experiment, not proof that a hook, skill or review agent improves delivery. Keep the owner and the original failure attached to the control.

| Decision | Record |
|---|---|
| User request and completed result | Name the behavior or resolved problem. Keep accepted code, release and user effect separate. |
| Failure to prevent | Preserve the failing input, wrong decision and revision where it occurred. |
| Point of failure | Source missing, wrong revision, not loaded, misread, check not executed, or result ignored. Mark uncertain stages `UNKNOWN`. |
| Candidate countermeasure | Put the check at the earliest reliable point of work. State whether it warns, blocks or requests human judgment. |
| False-claim case | Replay a case the control must reject. |
| Permitted neighbor | Replay a similar valid case the control must allow. |
| Alternate path | Try another editor, command or agent entry point that could bypass the control. |
| Execution proof | Record host, repository revision, command or event trace, check result and reviewer decision. |
| Cost | Count false blocks, retries, human takeovers, review wait, token or tool use where available, and upkeep. |
| Adoption decision | Owner accepts, revises or retires the control after comparing equivalent tasks over comparable windows. |

For a legacy migration, a citation check establishes that a source location exists. It does not establish what that code does. Follow the call path and run characterization cases on the existing application before modifying it. Move one usable unit through its normal review and release path, then check whether the old path can be retired. If a file's encoding or line endings matter, verify the resulting bytes through the actual write path and an alternate path.

For a context rule, distinguish **present**, **generated**, **loaded**, **used** and **effect verified**. Correct the authoritative source first, then replay the false claim and permitted neighbor. A shorter prompt or a new skill is only a candidate control until a running session uses it and the intended error falls.

For a shared reviewer queue, use the [review admission worksheet](review-admission.md). The harness experiment measures whether its new check prevents the named defect without shifting more work into waiting, repeated review or hidden bypasses. A local green test, CI acceptance and a user result are different observations; record each at its own boundary.
