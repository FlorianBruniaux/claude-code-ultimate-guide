---
name: learning-path
description: Run the local Claude Code learning path, record evidence, and schedule evidence-based reviews.
---

# Claude Code Learning Path

Use this skill to follow a bounded, local progression through the existing seven-module guide. The engine selects only modules whose prerequisites are complete, saves nothing outside the current project's `.claude/learning/` directory, requires a non-empty evidence note, and rejects corrupt state.

## Start with the diagnostic

Run `/self-assessment quick` before choosing a track. It is a self-reporting aid, not a certification. Map its result deliberately:

| Self-assessment result | Learning-path track |
| --- | --- |
| Beginner | Beginner |
| Intermediate | Practitioner |
| Advanced | Production |

Maintainer is not a self-assessment result. Select it manually only when the goal is shared governance, such as maintaining team instructions, controls, or evidence practices.

Choose the lowest track that covers your immediate goal:

| Track | Outcome | Modules |
| --- | --- | --- |
| Beginner | Safe first daily workflow | 01 to 03 |
| Practitioner | Reusable project workflows | 01 to 05 |
| Production | Automation with verification controls | 01 to 07 |
| Maintainer | Shared practice and governance | 01 to 07 |

The module definitions, guide references, exercises, prerequisites, and review intervals are in [assets/path.yaml](assets/path.yaml). The source curriculum is the existing [seven-module learning path](../../../guide/learning-path/README.md).

## Commands

Run commands from the repository or project being learned. `CLAUDE_SKILL_DIR` is the installed-skill directory provided by Claude Code. `--root "$PWD"` makes the learner's current project, rather than the installed skill, the only state target.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/progress.py" --root "$PWD" init --track Beginner
python3 "${CLAUDE_SKILL_DIR}/scripts/progress.py" --root "$PWD" status
python3 "${CLAUDE_SKILL_DIR}/scripts/progress.py" --root "$PWD" next
python3 "${CLAUDE_SKILL_DIR}/scripts/progress.py" --root "$PWD" complete module-01 \
  --evidence "Installed Claude Code, ran /help, and recorded the version."
python3 "${CLAUDE_SKILL_DIR}/scripts/progress.py" --root "$PWD" due
```

The state file is `.claude/learning/claude-code-guide-progress.json`. It belongs to the learner's project, not this installed skill. `init` refuses to overwrite an existing state file. Keep the state local unless you deliberately decide to share the evidence.

## Completion gate

Before completing a module:

1. Read the linked guide page.
2. Do the linked exercise in a real project.
3. Record a concrete evidence note that another person can inspect, such as a command, changed file, test result, or review artifact.
4. Use `next` to retrieve the next unlocked module.

An empty note, an unmet prerequisite, an unknown module, a module outside the selected track, or corrupt state is an error. The tool does not infer completion from a percentage, a command exit code, or an assertion by the learner.

## Reviews

Each completion schedules reviews exactly at 1, 3, 7, 14, 30, 60, and 90 days after the recorded completion date. `due` returns all scheduled reviews due on or before today. Revisit the linked exercise and update a separate proof artifact if the knowledge has changed.

## Safety boundary

All writes are local and atomic. A malformed state file fails closed and remains untouched for inspection or recovery. The prototype does not call a network service, install packages, assess competence automatically, or edit the guide.

## Validation boundary

The runtime validates `path.yaml` with Python's JSON parser because the file uses the JSON subset of YAML. The bundled `quick_validate.py` skill validator imports PyYAML before it parses `SKILL.md` frontmatter. If that import fails, this frontmatter validation is `UNKNOWN`, not a successful skill validation. The dependency-free runtime tests can still establish that this exact path definition loads.
