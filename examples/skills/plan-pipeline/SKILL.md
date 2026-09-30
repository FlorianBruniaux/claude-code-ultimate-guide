---
name: plan-pipeline
description: "Orchestrates the complete planning pipeline: product direction (ceo-review) -> architecture (eng-review) -> implementation plan (start) -> validation (validate) -> execution (execute). Run stages individually or let the orchestrator coordinate the full flow."
allowed-tools: Read Write Bash Task
effort: high
---

# Plan pipeline orchestrator

Orchestrates the complete plan-to-execution pipeline. Can run the full pipeline or a single isolated stage.

## Stages

| Stage | Skill | Purpose |
|-------|-------|---------|
| 1 | `/plan-pipeline:ceo-review` | Challenge the brief, lock product direction |
| 2 | `/plan-pipeline:eng-review` | Lock architecture, diagrams, and test matrix |
| 3 | `/plan-pipeline:start` | 5-phase planning: PRD, research, ADRs, task list |
| 4 | `/plan-pipeline:validate` | 2-layer validation before any code is written |
| 5 | `/plan-pipeline:execute` | Worktree isolation, parallel agents, quality gate, PR |

## Usage

```
/plan-pipeline                     # full pipeline, asks for context
/plan-pipeline --from=start        # skip gates, start from planning phase
/plan-pipeline --from=validate     # validate an existing plan
/plan-pipeline --from=execute      # execute a validated plan
```

## When to use each stage

**ceo-review**: use before any significant feature when the direction is not locked. Especially valuable when the request is specific (specificity signals collapsed solution space).

**eng-review**: use after direction is locked. Required for features with async components, external dependencies, or multi-step flows.

**start**: use for any non-trivial feature touching more than 2 files or involving architecture decisions.

**validate**: always before execute. The cost of validation is negligible against the cost of discovering issues mid-execution.

**execute**: after validate confirms all issues are resolved.

## Workflow

1. **Collect context**: what are we building, and what stage do we start from?
2. **ceo-review**: product direction gate (can be skipped with `--from=eng-review` or later)
3. **eng-review**: architecture gate (can be skipped with `--from=start` or later)
4. **CHECKPOINT**: ask user to confirm direction and architecture before planning
5. **start**: run 5-phase planning, produce `docs/plans/plan-{name}.md`
6. **CHECKPOINT**: present plan for review before validation
7. **validate**: 2-layer validation (structural + specialist agents)
8. **execute**: worktree isolation -> parallel agents -> quality gate -> PR

## Dependency graph

```
   ceo-review
        |
   eng-review
        |
      start
        |
    validate
        |
    execute
```

## Notes

Each stage writes its output to disk before the next stage begins. If the pipeline is interrupted, resume with `--from=<stage>` using the correct stage name. All decisions are recorded in `docs/plans/plan-{name}.md` and the corresponding ADRs in `docs/adr/`.
