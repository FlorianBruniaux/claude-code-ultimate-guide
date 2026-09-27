# AutoHarness: learned skills need an acceptance contract

**Reviewed:** 2026-09-27. **Score:** 3/5 as a case study. **Decision:** integrate the maintenance pattern and failure cases; do not recommend automatic installation at the inspected revision.

[AutoHarness 0.5.3 at the inspected revision](https://github.com/tigerless-labs/autoharness/tree/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b) maintains a skill library through hooks, reflection, staged proposals and promotion. It does not provide the whole repository harness, application tests or merge policy.

## Evidence from the inspection

The supplied suite passed 410 tests with one live-marked placeholder deselected, using Python 3.13.13 and pytest 9.1.1 in a disposable copy on September 26. Sixteen additional targeted reproductions exposed properties not covered by that passing suite. These deliberately chosen cases are not a representative failure rate. No plugin was installed into the working configuration, no real model was invoked and no improvement in accepted-task quality was measured.

| Boundary | Reproduced observation | Pinned implementation |
|---|---|---|
| File ownership | Creation could overwrite a user-owned skill; cleanup could remove a foreign temporary file | [promoter](https://github.com/tigerless-labs/autoharness/blob/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness/hook/promoter.py#L139), [store](https://github.com/tigerless-labs/autoharness/blob/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness/lib/skill_store.py#L82) |
| Proposal transport | `absorbed_into` was lost between staging and promotion; failed destination changes could still be followed by source archival | [transport](https://github.com/tigerless-labs/autoharness/blob/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness/stage_skill/server.py#L139) |
| Recall capacity | A synthetic set of 100 mature view-only skills remained indexed with a configured project capacity of 50 | [lifecycle](https://github.com/tigerless-labs/autoharness/blob/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness/lib/lifecycle.py#L21) |
| Provenance and candidates | Fabricated evidence was accepted without transcript association; a newly supplied invalid Python helper bypassed the check of existing files | [validation](https://github.com/tigerless-labs/autoharness/blob/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness/lib/validate.py#L127) |
| Recovery | Controlled interleavings lost a counter update and a queued proposal; interruption could leave an old body with a new helper | [hook and storage sources](https://github.com/tigerless-labs/autoharness/tree/ca39a72e4353ebef11b7de13c1fc7fa5f4df421b/src/autoharness) |

The inspection also exercised synthetic redaction and local permission-dispatch cases. Those do not establish a live permission escape or a real secret leak, and coverage in the alternative fork mode cannot be transferred to the default bundle mode.

## Integration decision

Retain the proposal/validation/write split, then qualify each boundary: source association, contradiction disposition, promotion owner, whole-candidate validation, file ownership, coherent activation and recovery. Keep viewed, invoked, succeeded and useful as different events. Bound recalled context independently of retained storage; protect mandatory rare rules during removal experiments.

Use [Memory Systems](../../guide/core/memory-systems.md#qualify-learned-rules-before-promotion), [Agent Harness Engineering](../../guide/core/agent-harness.md) and [Loop & Graph Engineering](../../guide/core/loop-graph-engineering.md). The new [local control exercise](../../examples/workflows/review-control-demo.py) is an independent simulated example; it does not fix or certify AutoHarness.

## Limits

The README's external benchmark material is not a measured benefit of this installed plugin. The inspection does not provide a causal comparison of tasks with and without AutoHarness. New upstream revisions need reinspection. The case supports acceptance tests, not claims that unrelated repositories contain the same defects.
