---
name: plan-pipeline
description: "Coordinate the plan-to-merged-PR pipeline: product direction (ceo-review), architecture (eng-review), implementation plan (start), validation (validate), execution (execute). Use when planning and shipping a non-trivial feature end to end, or to resume the pipeline from a given stage. Not for small changes (use plan mode)."
argument-hint: "[--from=ceo-review|eng-review|start|validate|execute]"
allowed-tools: Read Write Bash Agent
effort: high
disable-model-invocation: true
---

# Plan pipeline orchestrator

Orchestrates the complete plan-to-execution pipeline. Can run the full pipeline or a single isolated stage.

The five stage skills below live in flat sibling directories (`plan-pipeline-ceo-review`, `plan-pipeline-eng-review`, `plan-pipeline-start`, `plan-pipeline-validate`, `plan-pipeline-execute`), because only `<skill-name>/SKILL.md` one level deep is loaded. Each stage skill is user-invoked only (`disable-model-invocation: true`), since start and execute write files, commit, and open a PR. After each stage, report its output path and tell the user which stage command to run next; continue once they have run it.

## Stages

| Stage | Skill | Purpose |
|-------|-------|---------|
| 1 | `/plan-pipeline-ceo-review` | Challenge the brief, lock product direction |
| 2 | `/plan-pipeline-eng-review` | Lock architecture, diagrams, and test matrix |
| 3 | `/plan-pipeline-start` | 5-phase planning: PRD, research, ADRs, task list |
| 4 | `/plan-pipeline-validate` | 2-layer validation before any code is written |
| 5 | `/plan-pipeline-execute` | Worktree isolation, parallel agents, quality gate, PR |

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
2. **ceo-review**: run `/plan-pipeline-ceo-review` (product direction gate, skipped with `--from=eng-review` or later)
3. **eng-review**: run `/plan-pipeline-eng-review` (architecture gate, skipped with `--from=start` or later)
4. **CHECKPOINT**: ask user to confirm direction and architecture before planning
5. **start**: run `/plan-pipeline-start`, produce `docs/plans/plan-{name}.md`
6. **CHECKPOINT**: present plan for review before validation
7. **validate**: run `/plan-pipeline-validate` (structural checks + specialist agents)
8. **execute**: run `/plan-pipeline-execute` (worktree isolation, parallel agents, quality gate, PR)

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
