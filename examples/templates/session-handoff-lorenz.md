---
title: "Session Handoff Template"
description: "Structured context handoff template triggered at 85% context usage to preserve intent"
tags: [template, memory, workflows]
---

# Session Handoff Template

**Inspired by**: [Robin Lorenz's Context Engineering approach](https://www.linkedin.com/posts/robin-lorenz-54055412a_claudecode-contextengineering-aiengineering-activity-7425136701515251713) (Feb 2026)

**Purpose**: Structured handoff to preserve intent when approaching context limits. Triggers at **85% context usage** to prevent auto-compact quality degradation.

---

## Session Metadata

**Date**: YYYY-MM-DD
**Project**: [Project Name]
**Context Trigger**: X% (recommended: 85%)
**Session ID**: [Optional - for reference]

---

## ✅ Completed Work

List all work finished in this session with commit references:

- **[Task 1]**: Description of what was accomplished
  - Commit: `abc123`
  - Files: `src/feature.ts`, `tests/feature.test.ts`

- **[Task 2]**: Another completed item
  - Commit: `def456`
  - Files: `config/settings.json`

**Git status check**:
```bash
# Run before handoff to capture state
git status
git log -5 --oneline
```

---

## 🔄 Pending Tasks

Tasks started but not completed, with percentage and blockers:

- **[Task 3]**: Brief description
  - **Progress**: 80% complete
  - **Blocker**: Waiting for API key / Need to clarify requirements
  - **Next action**: [Specific next step]
  - **Files touched**: `src/pending-feature.ts`

- **[Task 4]**: Another pending item
  - **Progress**: Research phase (20%)
  - **Blocker**: Need architectural decision on X
  - **Next action**: Review options A vs B

---

## 🚧 Blockers & Issues

Critical blockers that need resolution before proceeding:

1. **[Blocker 1]**: Detailed description of what's blocking progress
   - **Impact**: What this blocks
   - **Workaround**: Temporary solution if any
   - **Resolution path**: How to unblock

2. **[Issue 1]**: Technical debt or bug discovered
   - **Severity**: High/Medium/Low
   - **Workaround**: Current mitigation

---

## ➡️ Next Steps

Prioritized action items for the next session:

1. **[High Priority]**: First action to take when resuming
2. **[High Priority]**: Second critical action
3. **[Medium]**: Follow-up task after priorities
4. **[Low]**: Nice-to-have or exploratory task

**Immediate start**: When resuming, begin with [specific file/task].

---

## 📌 Essential Context

Critical information that MUST be preserved (decisions, patterns, constraints):

### Architectural Decisions
- **Decision 1**: We chose approach X over Y because [rationale]
- **Pattern established**: All new features must follow [pattern]

### Technical Constraints
- **Constraint 1**: Can't use library X due to [reason]
- **Constraint 2**: Must maintain compatibility with [system]

### Domain Knowledge
- **Business rule**: Important rule discovered during implementation
- **Edge case**: [Unusual scenario] requires [special handling]

### Dependencies
- **External**: Waiting on [team/service] for [dependency]
- **Internal**: Feature X depends on completion of Y

---

## 🔄 Resume Instructions

**For next session**:

```bash
# Load this handoff into new session
cat claudedocs/handoffs/handoff-YYYY-MM-DD.md | claude -p

# Or reference manually
claude
# Then: "Continue from handoff document in claudedocs/handoffs/handoff-YYYY-MM-DD.md"
```

**Context check**:
```bash
# After resuming, verify context state
/status
```

**If context still high (>70%)**: Consider breaking into smaller focused sessions.

---

## 📊 Session Stats (Optional)

- **Turns**: ~X (approaching degradation threshold at 15-25 turns)
- **Context usage**: X% (triggered handoff at 85%)
- **Duration**: X hours
- **Commits**: X commits pushed

---

## 💡 Why This Template?

**Research-backed rationale**:

- **Auto-compact degrades quality**: LLM performance drops 50-70% on complex tasks at high context ([Context Rot Research](https://research.trychroma.com/context-rot))
- **Manual handoff preserves intent**: Structured documentation captures "what matters" vs "degraded version of everything"
- **85% threshold prevents auto-compact**: Auto-compact triggers at ~75% (VS Code) or ~95% (CLI), so 85% provides safety margin
- **Logical breakpoint > automatic compression**: Community consensus favors manual `/compact` at breakpoints

**Key principle**: "A handoff gives you a clean version of what matters" — Robin Lorenz

---

## 📚 Related Resources

- [Session Handoffs (Ultimate Guide)](../../guide/ultimate-guide.md#session-handoffs)
- [Auto-Compaction Research (Architecture)](../../guide/architecture.md#auto-compaction)
- [Fresh Context Pattern (Ultimate Guide)](../../guide/ultimate-guide.md#fresh-context-pattern)
- [Lorenz's Original Post](https://www.linkedin.com/posts/robin-lorenz-54055412a_claudecode-contextengineering-aiengineering-activity-7425136701515251713)

---

**Template Version**: 1.0
**Last Updated**: 2026-02-08
**Maintenance**: Update as research evolves
