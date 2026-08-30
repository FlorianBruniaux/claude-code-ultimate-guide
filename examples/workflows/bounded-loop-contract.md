---
name: bounded-loop-contract
description: Reference contract for a bounded agent loop with a separate verifier interface, evidence, and escalation
complexity: intermediate
time: 15 min
domain: architecture
prerequisites: [Python 3.10+]
status: stable
keywords: [agent-loop, graph, verification, budget, escalation]
---

# Bounded Agent Loop Contract

Use this pattern when one agent can complete the job through repeated action and verification. It keeps the control flow explicit without introducing a workflow framework.

The runnable companion is [`bounded-loop-example.py`](./bounded-loop-example.py).

## Contract

| Field | Required decision |
| --- | --- |
| Goal | What outcome is requested? |
| Action | What may change on each attempt? |
| Observation | What evidence did execution produce? |
| Verifier | Which independent check accepts or rejects the evidence? |
| Budget | How many attempts or how much cost may the loop consume? |
| Stop rule | What exact condition returns an accepted result? |
| Escalation | What happens when the budget expires? |

The example records every transition. A rejected attempt returns to `act`; a verified attempt moves to `accepted`; budget exhaustion moves to `escalated`.

```text
act -> verify -> accepted
 ^        |
 |        v
 +----- rejected

act or verify -> escalated  when the attempt budget is exhausted
```

## Run

```bash
python3 examples/workflows/bounded-loop-example.py
```

Expected result:

```text
accepted after 2 attempts
```

## When to move to a graph

Keep the loop while every rejected result returns to one next action. Introduce an explicit graph when the workflow needs several branches, parallel work, joins, persistent checkpoints, or different authorities for different transitions.

See [Loop & Graph Engineering](../../guide/core/loop-graph-engineering.md) for the design rules and [Agent Harness Engineering](../../guide/core/agent-harness.md) for the runtime boundary around the loop.
