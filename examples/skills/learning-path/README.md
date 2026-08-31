# Executable Claude Code Learning Path

This dependency-free prototype turns the existing [seven-module learning path](../../../guide/learning-path/README.md) into a local progression. It stores only learner-owned state in `.claude/learning/claude-code-guide-progress.json` under the target project.

## What it does

- creates one of four tracks: Beginner, Practitioner, Production, or Maintainer;
- unlocks modules only after their prerequisites have recorded evidence;
- requires a non-empty evidence note for every completion;
- produces a deterministic next module, current status, and due-review list;
- schedules reviews at 1, 3, 7, 14, 30, 60, and 90 days;
- writes the JSON state atomically and refuses corrupt state.

It is a local learning aid. It does not prove competence, upload evidence, or replace a human review of an exercise.

## Quick start

Use the public self-assessment workflow first:

```text
/self-assessment quick
```

Then start the lowest track matching your immediate goal:

```bash
python3 examples/skills/learning-path/scripts/progress.py init --track Beginner
python3 examples/skills/learning-path/scripts/progress.py next
```

After performing the exercise, record the evidence:

```bash
python3 examples/skills/learning-path/scripts/progress.py complete module-01 \
  --evidence "Installed Claude Code, ran /help, and recorded the version."
python3 examples/skills/learning-path/scripts/progress.py status
python3 examples/skills/learning-path/scripts/progress.py due
```

For another project, pass its root explicitly:

```bash
python3 examples/skills/learning-path/scripts/progress.py --root /path/to/project init --track Practitioner
```

## Tracks

| Track | Intended result | Required modules |
| --- | --- | --- |
| Beginner | Work safely through a first Claude Code workflow | 01, 02, 03 |
| Practitioner | Build reusable local agent and skill workflows | 01 to 05 |
| Production | Add hooks, verification, and advanced coordination | 01 to 07 |
| Maintainer | Maintain shared practices and operational safeguards | 01 to 07 |

The diagnostic helps select a starting track, but it does not remove prerequisite checks. A learner who selects Production still completes the sequence in order.

## Module map

| Module | Guide page | Required exercise |
| --- | --- | --- |
| 01 | [Installation and setup](../../../guide/learning-path/01-installation.md) | [View available commands](../../../guide/learning-path/01-installation.md#exercise-1-view-available-commands) |
| 02 | [Core loop](../../../guide/learning-path/02-core-loop.md) | [Complete loop](../../../guide/learning-path/02-core-loop.md#exercise-the-complete-loop) |
| 03 | [Memory and configuration](../../../guide/learning-path/03-memory.md) | [Create your CLAUDE.md](../../../guide/learning-path/03-memory.md#exercise-create-your-claudemd) |
| 04 | [Agents and specialization](../../../guide/learning-path/04-agents.md) | [Create a test-writer agent](../../../guide/learning-path/04-agents.md#exercise-create-a-test-writer-agent) |
| 05 | [Skills and automation](../../../guide/learning-path/05-skills.md) | [Create a domain skill](../../../guide/learning-path/05-skills.md#exercise-create-a-domain-skill) |
| 06 | [Hooks and events](../../../guide/learning-path/06-hooks.md) | [Create a validation hook](../../../guide/learning-path/06-hooks.md#exercise-create-a-validation-hook) |
| 07 | [Advanced patterns](../../../guide/learning-path/07-advanced.md) | [Build a multi-agent workflow](../../../guide/learning-path/07-advanced.md#exercise-build-your-first-multi-agent-workflow) |

The canonical machine-readable map is [assets/path.yaml](assets/path.yaml). It uses JSON syntax, which is valid YAML, so the standard-library-only Python tool can parse it without PyYAML.

## State and recovery

The state file contains only the selected track, module completion dates, and evidence notes. `init` will not overwrite it. Every save writes a complete temporary file in the same directory, flushes it, and atomically replaces the old file.

If `status`, `next`, `complete`, or `due` reports corrupt state, stop. Preserve a copy of `.claude/learning/claude-code-guide-progress.json` for inspection, repair it manually only after identifying the cause, or remove it deliberately and start a new profile. The prototype will not guess how to recover learner evidence.

## Tests

```bash
python3 -m unittest -v examples/skills/learning-path/tests/test_progress.py
```

The focused suite covers profile creation, atomic persistence, prerequisite enforcement, evidence gates, next-module selection, review intervals, and corrupt-state failure.
