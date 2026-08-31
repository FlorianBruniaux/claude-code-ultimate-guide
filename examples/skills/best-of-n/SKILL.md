---
name: best-of-n
description: "Generate bounded independent candidates, score them against a frozen rubric, and verify the selected result with a proof log."
argument-hint: "<task> [--candidates 3|5]"
effort: high
disable-model-invocation: true
---

# Best-of-N Selection and Proof

Use this skill when a task has several plausible solutions, a wrong choice is costly, and a deterministic check or independent reviewer can evaluate the selected result. Do not use it for mechanical work with one clear implementation and a direct acceptance test.

Read the full method at [Best-of-N: Generate, Select, and Verify](../../../guide/workflows/best-of-n.md) before running the protocol.

## Inputs to collect before generation

- Task scope, exclusions, repository revision, environment, permissions, and budget.
- Acceptance criteria, mandatory failure conditions, and executable checks.
- A rubric with weights, observable anchors, passing threshold, tie-breaker, candidate count or predeclared batch schedule, and stop rule.
- The selected `TESTING.md` path. Start from the [portable proof-log template](../../claude-md/TESTING.md).

If any item is missing, return `needs_contract` and list the missing fields. Do not generate candidates first and invent the rubric afterward.

## Procedure

1. Freeze the contract in the proof log. Default to three candidates. Use five only when the expected improvement justifies the additional generation, scoring, and verification cost. If work runs in batches, declare every batch and the between-batch stop condition before generation.
2. Generate each candidate from the same frozen contract. Do not reveal candidate text, scores, or private reasoning across generators. Assign an opaque identifier to every generated candidate.
3. Preserve each candidate as a separate artifact. For code, use isolated diffs or worktrees from the same base revision. Add one proof-log line for every generated candidate, including every candidate in Best-of-5 and rejected candidates.
4. Blind provenance and presentation order for scoring when practical. Apply the fixed rubric to every candidate in the declared N, or to every candidate in the completed predeclared batch. Record criterion-level evidence and disqualify mandatory failures.
5. Select the highest passing candidate using the declared tie-breaker. Treat any combination of candidate fragments as a new synthesized candidate with its own ID, score, and verification.
6. Run the declared executable checks in the recorded environment. Capture commands, output location, exit status, artifact hash or revision, and uncovered scope.
7. If executable verification cannot decide the requirement, request a reviewer who did not generate the candidate and who receives a fresh task packet. Record shared model, context, tools, and repository access as correlation risks.
8. Finish the proof log with `PASS`, `FAIL`, or `UNKNOWN`. `UNKNOWN` blocks a claim that the requirement was verified.

## Guardrails

- Candidate generation is not selection. Selection is not synthesis. Majority vote is not evidence of correctness.
- Never use a self-grading generator as the only acceptance gate.
- Generate and score all candidates in the declared N before selection. A batched run may stop only after the complete predeclared batch is evaluated and its predeclared stop condition is met. Do not keep sampling until an answer feels persuasive.
- Do not claim candidates are independent solely because they came from different calls. State the isolation controls and remaining shared context.
- Preserve failed candidates and failed checks in the proof log. They bound what was actually tested.

## Required output

Return this concise record and write the full details to `TESTING.md`:

```text
BEST-OF-N RESULT
Task: <scope>
Contract: <rubric version, N or batch schedule, stop rule>
Candidates: <every generated candidate ID>
Selected: <candidate ID or none>
Verification: PASS | FAIL | UNKNOWN
Evidence: <proof-log path and artifact links>
Remaining limits: <uncovered scope or none>
```

## Connections

Use [Dynamic Workflows](../../../guide/workflows/dynamic-workflows.md) for durable parallel stages and schemas. Pair this skill with [TDD with Claude Code](../../../guide/workflows/tdd-with-claude.md), [Agent Evaluation](../../../guide/roles/agent-evaluation.md), [Code Review](../../../guide/workflows/code-review.md), and [AI traceability](../../../guide/ops/ai-traceability.md) when the result will be delivered or audited.
