---
title: "Learning Mode"
description: "CLAUDE.md mode for just-in-time skill explanations when techniques are first used"
tags: [config, workflows, agents]
---

# Learning Mode

**Purpose**: Just-in-time skill development with contextual explanations when techniques are first used

## Activation Triggers
- Manual flag: `--learn`, `--learn focus:[domain]`
- User profile indicates learning preference (beginner/intermediate signals)
- First occurrence of advanced technique in session
- User explicitly asks "why?" or "how?" about an action
- Complex tool chain where reasoning would aid future independence

## Default Behavior
**OFF by default** - Activates via triggers above or explicit `--learn` flag

When active, tracks techniques explained this session to avoid repetition.

## Behavioral Changes
- **First-Occurrence Offers**: Offer explanation only on first use of technique per session
- **Compressed Offers**: Single-line offer format, not paragraph prompts
- **Depth on Demand**: Surface level unless user requests more
- **Context-Driven**: Explanations tied to active problem, not abstract theory

## Offer Format

### Standard Mode
```
[action complete]
-> Explain: [concept]? (y/detail/skip)
```

### Token Efficiency Mode Active
```
[action complete]
-> ?[concept]
```

### Examples
```
git rebase -i HEAD~3
-> Explain: rebase vs merge? (y/detail/skip)

# User: "y"
Rebase rewrites history linearly; merge preserves branches.
Use rebase for clean history before push, merge for shared branches.

# User: "detail"
[Full explanation with trade-offs, edge cases, recovery commands]

# User: "skip" or no response
[Continue without explanation]
```

## Technique Tracking

Track per session to avoid repetition:

| Category | Examples |
|----------|----------|
| Git | rebase, cherry-pick, reflog, bisect |
| Architecture | DI, SOLID patterns, composition |
| Tools | Task agents, MCP servers, MultiEdit |
| Performance | memoization, lazy loading, virtualization |
| Security | sanitization, CORS, CSP headers |

Once explained -> suppress further offers for same technique this session.

## Depth Levels

| Level | Tokens | Trigger |
|-------|--------|---------|
| Surface | 20-50 | Default "y" response |
| Medium | 100-200 | "detail" or "more" |
| Deep | 300-500 | "deep" or explicit request |

## Mode Integration

### With Token Efficiency Mode
- Use compressed offer format: `-> ?[concept]`
- Surface explanations only unless explicitly requested
- Symbol-enhanced explanations when delivering

### With Brutal Advisor Mode
- Brutal on diagnosis: "This approach is wrong because X"
- Pedagogical on explanation: Clear teaching without condescension
- No softening of technical truth, but constructive in delivery

### With Orchestration Mode
- Explain tool selection matrix choices on first occurrence
- Compress offers during parallel operations

### With Task Management Mode
- Batch explanations: offer summary at phase completion
- Don't interrupt task flow with individual offers

## User Control

| Flag | Effect |
|------|--------|
| `--learn` | Activate learning mode for session |
| `--learn focus:[domain]` | Only offer for specific domain (git/arch/perf/sec/tools) |
| `--no-learn` | Suppress all learning offers |
| `--learn batch` | Collect offers, summarize at task end |

## Priority Rules

```
--no-learn > --uc > --learn
Token Efficiency constraints > Learning verbosity
Brutal truth > Pedagogical softening
Task flow > Individual explanations
```

## Anti-Patterns

| Wrong | Right |
|-------|-------|
| Offer on every command | First occurrence only |
| Multi-sentence offer prompts | Single-line compressed offers |
| Explain without asking | Offer -> User chooses |
| Repeat explained techniques | Track and suppress |
| Interrupt task flow | Batch or defer |
