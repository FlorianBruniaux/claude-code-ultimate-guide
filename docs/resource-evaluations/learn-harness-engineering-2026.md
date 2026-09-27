# Walkinglabs: learning harness engineering

**Reviewed:** 2026-09-27. **Score:** 3/5 for teaching examples and control-testing counterexamples. **Decision:** selective integration; no production-readiness endorsement.

The inspected [course revision](https://github.com/walkinglabs/learn-harness-engineering/tree/77e7a3e21469dcbece2558086c8d91657abeaa40) contains 14 lectures, eight project pages and four product analyses in its English core. The inspection read those 26 pages and the relevant generator, validators, graph skeleton and project scripts. Translation presence was inventoried, not linguistically audited.

## What the exercises establish

| Observed case | Interpretation and source |
|---|---|
| A generated fixture with verification command `false # test build` received a structural 100/100 while executing verification exited 1 | The [generator and scorer](https://github.com/walkinglabs/learn-harness-engineering/blob/77e7a3e21469dcbece2558086c8d91657abeaa40/skills/harness-creator/scripts/lib/harness-utils.mjs) inspect structure; the score is not a reliability rate. |
| A separate shell fixture passed 7/7 critical checks but scored 9/71 overall | The [shell audit](https://github.com/walkinglabs/learn-harness-engineering/blob/77e7a3e21469dcbece2558086c8d91657abeaa40/tools/audit-harness.sh) checks conventions. Preserve both denominators. |
| A simulated checker accepted `not approved` and a test-looking string without running the test | The [graph skeleton](https://github.com/walkinglabs/learn-harness-engineering/blob/77e7a3e21469dcbece2558086c8d91657abeaa40/docs/en/lectures/lecture-14-graph-engineering/code/maker_checker_graph.py#L47) uses substring matching. Its `merge` node only prints; no Git merge was performed. |

The reproductions used disposable fixtures, Node 24.16.0, Python 3.14.7 and macOS Bash 3.2.57 on September 26. They do not measure frequency across projects. No live agent benchmark or Electron application test was performed.

## Integration

Use the course for session handoffs, scope, verification and the distinction between loops and graphs. Preserve its pedagogical status. A workflow graph does not supply permissions, a worktree does not isolate a process, and an in-memory checkpoint does not prove restart durability.

The frequently repeated claim that a weak model reaches frontier performance is not demonstrated by this course. The [Anthropic application-development report](https://www.anthropic.com/engineering/harness-design-long-running-apps) compares Opus 4.5 configurations with materially different budgets; it does not isolate a small-model substitution.

The [harness guide](../../guide/core/agent-harness.md), [loop guide](../../guide/core/loop-graph-engineering.md) and [executable control exercise](../../examples/workflows/review-control-demo.py) own the practical additions. The local exercise tests its own simulated contract, not a repaired version of Walkinglabs.

## Review boundary

The source inspection and editorial challenge distinguish structural checks, simulated routing and live effects. Model rankings, course learning outcomes, product internals and translation accuracy remain outside this evaluation. Re-evaluate the pinned claims before applying them to a later revision.
