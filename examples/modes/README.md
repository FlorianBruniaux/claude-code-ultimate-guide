---
title: "Behavioral Modes"
description: "Ready-to-use behavioral mode files for customizing Claude Code behavior"
tags: [config, template, workflows]
---

# Behavioral Modes

Ready-to-use behavioral mode files for Claude Code. Copy to `~/.claude/` and reference in your `CLAUDE.md`.

## Available Modes

| Mode | File | Purpose |
|------|------|---------|
| **Learning** | [MODE_Learning.md](./MODE_Learning.md) | Just-in-time explanations when techniques are first used |

## Installation

### 1. Copy the mode file

```bash
cp MODE_Learning.md ~/.claude/
```

### 2. Reference in your CLAUDE.md

Add to `~/.claude/CLAUDE.md`:

```markdown
# Behavioral Modes
@MODE_Learning.md
```

### 3. Add flags (optional)

Add to `~/.claude/FLAGS.md` for flag-based activation:

```markdown
**--learn**
- Trigger: User requests learning mode, "why/how" questions
- Behavior: Enable just-in-time explanations with first-occurrence tracking

**--no-learn**
- Trigger: User wants pure execution without educational offers
- Behavior: Suppress all learning mode offers
```

## Usage

```bash
# Activate for entire session
claude --learn

# Focus on specific domain
claude --learn focus:git
claude --learn focus:architecture

# Batch explanations at task end
claude --learn batch
```

## More Modes: SuperClaude Framework

This guide includes only **Learning Mode**. For a complete behavioral framework with additional modes, check out [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework):

| Mode | Purpose |
|------|---------|
| **Orchestration** | Smart tool selection, parallel execution optimization |
| **Task Management** | Hierarchical task tracking with persistent memory |
| **Token Efficiency** | Symbol-enhanced compression (30-50% token reduction) |
| **Learning** | Just-in-time skill development (included here) |

SuperClaude also includes:
- `FLAGS.md` — Behavioral flags (`--delegate`, `--learn`, etc.) *Note: `--think`/`--ultrathink` are cosmetic only since v2.0.67 — thinking is now on by default with Opus 4.5*
- `PRINCIPLES.md` — Engineering principles (SOLID, DRY, evidence-based)
- `RULES.md` — Actionable rules with priority system
- MCP server documentation (Context7, Sequential, Serena)

## See Also

- [Guide Section 10.5: SuperClaude Framework](../../guide/ultimate-guide.md#105-superclaude-framework) — Full documentation
- [SuperClaude Repository](https://github.com/SuperClaude-Org/SuperClaude_Framework) — Complete framework
