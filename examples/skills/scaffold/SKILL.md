---
name: scaffold
description: "Interactive coach that asks 4-5 questions to decide whether a use case needs an agent, a skill, a hook, or a rule, then generates a ready-to-use template. Start it with /scaffold (no arguments); it runs only on request."
effort: medium
disable-model-invocation: true
---

# Claude Code scaffold coach

Interactive wizard that identifies the right Claude Code component for your use case and generates a ready-to-use template. Custom commands are now part of skills, so the choices are agent, skill (manual or automatic), hook, or rule.

**Usage**: `/scaffold` (no arguments needed). Start the conversation.

---

## Phase 1: Discovery

Open with this prompt, then wait for the user's answer before asking anything else:

> What do you want to automate or build? One sentence is enough to start.

Once you have a rough idea, ask the following questions in order. Skip a question if a previous answer already answers it.

### Q1: Trigger

> How is this triggered?
>
> a) I run it myself with a slash command (e.g. `/something`)
> b) It should fire automatically when Claude takes an action (writes a file, runs bash, finishes a session...)
> c) It should apply all the time, every session, without me doing anything

- If **b** → likely a **Hook** (jump to Q_hook)
- If **c** → likely a **Rule** (jump to Q_rule)
- If **a** → continue with Q2

### Q2: Domain expertise

> Does this require deep, project-specific expertise?
> For example: knowing your GraphQL schema, your migration conventions, your internal API patterns, your cost model...

- If **yes, deep expertise** → likely an **Agent** (jump to Q_agent)
- If **no, more of a checklist or procedure** → continue with Q3

### Q3: Complexity

> How much context and logic does this involve?
>
> a) A lot: multiple rules, domain-specific examples, nuanced judgment
> b) Straightforward: a few steps, a template, some bash

- If **a** → likely a **Skill** with supporting files (`references/`, `scripts/`)
- If **b** → likely a **Skill** (a single `SKILL.md`, which replaces the older custom command)

### Q4: Reuse scope

> Who needs this?
>
> a) Just me
> b) My whole team
> c) It needs to be invokable by other agents automatically

- **c** → strengthens **Agent** (needs a `description:` field that other agents can read)
- **b** → strengthens **Skill** (committed to the repository so the team gets it)
- **a** → can stay a personal **Skill** in `~/.claude/skills/`

### Q5: Output type

> What should happen at the end?
>
> a) A report or analysis: Claude reads and explains, no files touched
> b) Code or files generated
> c) An action taken (commit, push, API call...)
> d) Claude's behavior changes permanently (always does X, never does Y)

- **a** → read-only Agent (no `Write` or `Bash` in tools)
- **b/c** → Agent or Skill with write access (set `disable-model-invocation: true` when the action has side effects)
- **d** → Rule, or Hook if conditional on a specific event

---

## Internal decision tree (do not display, use to reason)

```
Triggered automatically?
  ├─ On Claude action (Write, Bash, SessionEnd...) -> Hook
  └─ Always active, no trigger -> Rule

Triggered manually?
  ├─ Deep domain expertise required?
  │   ├─ Yes + invokable by other agents -> Agent
  │   └─ Yes + manual use only -> Agent or Skill
  └─ Procedure / checklist, no special expertise?
      ├─ Complex, lots of project-specific context -> Skill with supporting files
      └─ Simple, a few steps -> Skill (single SKILL.md)

Common hybrid cases:
  - Agent + Skill: specialist agent + a user-invoked skill that delegates to it
  - Rule + Hook: permanent behavior + blocking on a specific action
  - Skill + Agent: skill with `context: fork` and `agent:` that runs in a subagent
```

---

## Phase 2: Recommendation

After the questions, display this structure:

```
## Diagnosis

You want to: [one-line summary of the use case]

## Recommendation: [TYPE]

**Why?**
[2-3 sentences: trigger type, complexity level, reuse scope]

**What it would NOT be, and why:**
- Not an agent because [short reason]
- Not a rule because [short reason]
[adjust based on actual candidates]

**Hybrid case?** [Yes / No]
[If yes: explain the combination and which file to create first]
```

---

## Phase 3: Scaffold

Ask: "Generate the scaffold file?"

If yes, produce the template below based on the detected type.

---

### Agent scaffold

```markdown
---
name: [kebab-case-name]
description: "[What this agent does in one sentence. When to invoke it. Example triggers for other agents.]"
model: sonnet
tools: Read, Grep, Glob[, Write, Bash (add only if this agent must modify files or run commands)]
---

# [Agent Name]

[One paragraph: what this agent is for, what it is NOT for, and when to prefer another agent.]

## Context

[Stack, conventions, or domain knowledge this agent needs to be effective.]

## When to invoke

- [Concrete trigger 1]
- [Concrete trigger 2]
- [Concrete trigger 3]

## Protocol

### Step 1: Read context

```bash
# What to read before reasoning
cat CLAUDE.md 2>/dev/null
```

### Step 2: Analyze

[What to look for. Patterns to detect. Red flags to surface.]

### Step 3: Output

[Exact output format: use a markdown code block to show the structure.]

## Red flags

| Pattern | Risk |
|---------|------|
| [pattern] | [impact] |

## What this agent does NOT do

- [Scope boundary 1]
- [Scope boundary 2: point to another agent if relevant]
```

**File**: `.claude/agents/[name].md`

---

### Simple skill scaffold (replaces a custom command)

```markdown
---
name: [name]
description: "[What this skill does in one sentence. Use when ...]"
argument-hint: "[arg] [--flag]"
disable-model-invocation: true   # keep for workflows with side effects; drop for read-only skills
effort: medium
---

# [Skill Name]

[Brief description. What problem it solves. When to use it vs alternatives.]

## Arguments

- `[arg]`: [description] (default: [value])
- `--flag`: [description]

## Usage

```bash
/[name]              # Basic usage
/[name] --flag       # With flag
```

---

## Phase 1: [First phase name]

[What Claude does in this phase.]

```bash
# Example commands if applicable
```

## Phase 2: [Second phase name]

[What Claude does.]

## Phase 3: Output

[Output format. Use a markdown block to show the structure.]

\$ARGUMENTS
```

**File**: `.claude/skills/[name]/SKILL.md` (the older `.claude/commands/[name].md` format still works but is not recommended for new work)

---

### Skill scaffold with supporting files

```markdown
---
name: [skill-name]
description: "[What this skill does. Use when [trigger situations]. Not for [sibling skill boundary].]"
effort: medium
---

# [Skill Name]

[What this skill does and when it applies. Distinguish from similar skills.]

## Trigger phrases

- "[phrase that activates this skill]"
- "[alternative phrasing]"

## When to use

- [Scenario 1]
- [Scenario 2]

## Workflow

### 1. [First action]: [brief description]

[Details]

### 2. [Second action]: [brief description]

[Details]

### 3. Deliver output

[Output format]

## Conventions to follow

[Project-specific rules, naming conventions, or patterns this skill must respect.]

## Common pitfalls

- [Mistake 1 and how to avoid it]
- [Mistake 2 and how to avoid it]

\$ARGUMENTS
```

**File**: `.claude/skills/[name]/SKILL.md`, with optional `references/` and `scripts/` next to it (reference scripts with `${CLAUDE_SKILL_DIR}`)

---

### Hook scaffold

```bash
#!/usr/bin/env bash
# =============================================================================
# [name].sh: [PreToolUse | PostToolUse | UserPromptSubmit | Stop] Hook
# =============================================================================
# [What this hook does in one line]
# Fires on: [event] matching [tool or pattern]
#
# Exit 0 = allow / continue
# Exit 2 = block with message (effect depends on the event, see the hooks reference)
#
# stdin: JSON payload from Claude Code
# =============================================================================

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# --- Main logic ---

# [Your validation logic here]
# Example: block writes to protected paths
# FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
# if [[ "$FILE" == *"/secrets/"* ]]; then
#   echo "Blocked: writes to /secrets/ are not allowed" >&2
#   exit 2
# fi

exit 0
```

**File**: `.claude/hooks/[name].sh`

Also add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/[name].sh" }]
      }
    ]
  }
}
```

---

### Rule scaffold

```markdown
# [Rule Title] (Auto-loaded)

## Directive

[The rule in one imperative sentence.]

## When it applies

[Triggers, file types, or situations where this rule activates.]

## Required behavior

[What Claude must do concretely, be specific.]

## Anti-patterns

Do NOT:
- [Forbidden example]

Do:
- [Correct behavior]

---

**Auto-loaded**: This file is loaded automatically at session start.
```

**File**: `.claude/rules/[name].md`

Reference in `CLAUDE.md` if not in an auto-loaded directory.

---

## Quick reference

If the user is unsure, show this table:

| Type | Trigger | Expertise needed | Complexity | Typical example |
|------|---------|-----------------|------------|-----------------|
| **Agent** | Manual or automatic | High, domain-specific | Multi-step analysis | `migration-reviewer`, `dbt-specialist` |
| **Skill** | Manual `/name` or automatic | Low to high | A few steps up to a rich workflow with supporting files | `/commit`, `/release`, `tdd-workflow`, `api-review` |
| **Hook** | Automatic on event | None (bash logic) | Script | `security-gate.sh`, `format-on-save.sh` |
| **Rule** | Permanent, every session | None (prose) | Instructions | `no-direct-push.md`, `english-only.md` |

---

## Sources

- Component types overview: [Section 3](../../../guide/ultimate-guide.md)
- Agent examples: [agents/](../../agents/)
- Hook examples: [hooks/](../../hooks/)
- Skill examples: [skills/](../../skills/)
