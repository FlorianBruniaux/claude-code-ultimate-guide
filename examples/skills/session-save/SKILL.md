---
name: session-save
description: Save the current session state (decisions, modified files, current status, and next steps) to a handoff file for later resume.
effort: low
disable-model-invocation: true
---

# /session-save

Capture the current session into a structured handoff file so you (or another instance) can resume with full context. Creates a timestamped Markdown file in `.claude/sessions/`.

## When to Use

- Before ending a session that isn't complete
- Before switching to a different task
- Before context reaches 75%+ (to preserve the important parts)
- At natural milestones in a long task (after each phase)
- To hand off to a second Claude instance

## Instructions

Produce a handoff document with the following structure:

---

## Session Handoff: [TIMESTAMP]

### What Was Being Done
[One paragraph: the goal, the approach, where things stand right now]

### Files Modified This Session
[List every file that was created, edited, or deleted, with the nature of the change]

```
path/to/file.ts      - [what changed and why]
path/to/other.ts     - [what changed and why]
```

### Key Decisions Made
[Architectural choices, tradeoffs accepted, approaches rejected and why]

- **Decision**: [What was decided]
  - **Rationale**: [Why]
  - **Alternatives rejected**: [What else was considered]

### Current Status
[Where things are right now: what's working, what's broken, what's in-progress]

- Working: [...]
- In-progress: [...]
- Known issues: [...]

### Next Steps (Ordered)
[The exact next actions to take to continue, specific enough that a fresh context can pick up without re-reading everything]

1. [First action]: `path/to/file.ts` - [what to do]
2. [Second action]: [...]
3. [...]

### Context to Reload
[Files that must be read to resume with full understanding, keep this list short]

- `path/to/key-file.ts`: [why it matters]
- `CLAUDE.md`: project rules

### Blockers / Open Questions
[Anything unresolved that needs a decision or external input before proceeding]

- [ ] [Question or blocker]: [who/what can resolve it]

---

## Implementation

Save the handoff to `.claude/sessions/handoff-[YYYY-MM-DD-HHMM].md`. Then output the file path so the user knows where to find it.

## Resume Pattern

To resume from a handoff:

```
/session-resume .claude/sessions/handoff-YYYY-MM-DD-HHMM.md
```

Or manually: read the handoff file, then read the files listed in "Context to Reload" before continuing.

## Examples

### Example 1: Mid-Feature Save

```
/session-save
```

Claude captures:
- Auth middleware was being refactored (files: `src/middleware/auth.ts`, `src/middleware/jwt.ts`)
- Decision: switched from session tokens to JWTs (rationale: scales better across services)
- Status: JWT validation working, refresh logic in-progress
- Next: implement `refreshToken()` in `src/services/auth.service.ts`, then update tests

### Example 2: Context-Pressure Save

When context hits 70%, run `/session-save` before `/compact` to preserve decision context that compaction might lose.

## Notes

- Keep "Context to Reload" to 5 files max. The goal is a fast resume, not a full re-read.
- "Next Steps" should be specific enough that a cold-start Claude can execute step 1 without asking questions
- Don't save tool output or code snippets in the handoff; reference file paths instead.

---

**See also**:
- [Session Teleportation](../../../guide/ultimate-guide.md#916-session-teleportation): broader session management patterns
- [Instinct-Based Learning](../../../guide/ultimate-guide.md#924-instinct-based-continuous-learning): what to extract from sessions before closing
