---
name: handoff-create
description: Generate a structured handoff document from the current session. Captures scope, relevant files with line numbers, key discoveries, work completed, current status, next steps, and code snippets. Use before ending a session or handing work to another agent.
argument-hint: "[optional-filename]"
effort: low
disable-model-invocation: true
---

Generate a structured handoff document from our current conversation and save it to `claudedocs/handoffs/handoff_YYYYMMDD_HHMMSS.md` (or use the filename provided as `$ARGUMENTS[0]` if given).

Create the `claudedocs/handoffs/` directory if it does not exist.

## Document structure

Include exactly these sections:

```markdown
# Handoff: [Task Name] - [YYYY-MM-DD HH:MM]

## Task

[One sentence: what is being accomplished]

## Scope

[What needs to be done. Be specific about boundaries: what is in scope and what is explicitly out of scope]

## Files

[All relevant files touched or needed. Format: `path/to/file:line` when a specific line matters]

- `src/auth/middleware.ts:45` - token validation logic
- `tests/auth.spec.ts` - test suite for this change
- `docs/api.md` - needs update after implementation

## Discoveries

[Key findings and insights from the work so far. Things the next agent needs to know that are not obvious from the code]

- [Discovery 1]
- [Discovery 2]

## Work Done

[Completed tasks. Append-only: never remove prior entries. Include commit hashes when available]

- [x] Task A completed (commit: abc1234)
- [x] Task B completed

## Status

[Current state: what is done, what remains, test status, blockers]

## Next Steps

[Actionable checklist of remaining tasks, in order]

1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## Code

[Relevant code snippets with context. Focus on the parts a resuming agent needs to understand immediately]

\`\`\`typescript
// Key implementation detail
\`\`\`
```

## Rules

- Keep it under 600 words total. A resuming agent should be able to load this and proceed within 30 seconds of reading.
- Use `path/to/file:line` format for all file references. Line numbers matter.
- "Work Done" is append-only. Never remove previous entries.
- Do not include the full git diff or full file contents. Include only the code snippets that are non-obvious.

After saving, confirm the file path.
