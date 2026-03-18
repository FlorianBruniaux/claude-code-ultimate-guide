# Session Retrospective Template

A structured prompt to run at the end of Claude Code sessions. The goal is to capture
knowledge while it's fresh and turn it into durable rules — keeping your `CLAUDE.md`
accurate as the project evolves.

## The Prompt

Copy this and paste it into Claude at the end of a session:

```
Session complete. Before we close, run a quick retrospective:

1. What patterns did we establish that should be permanent rules in CLAUDE.md?
2. What did I correct that Claude got wrong? Should a rule prevent that?
3. What worked well that we should replicate in future sessions?
4. Were any architectural decisions made that CLAUDE.md should record?
5. Is there anything currently in CLAUDE.md that this session proved wrong or outdated?

Output a knowledge feed — 3 to 5 bullets max, high-signal items only.
Skip anything obvious, generic, or already in CLAUDE.md.
Format each item as an actionable rule ready to copy in.
```

## When to Run It

| Trigger | Run retro? |
|---------|-----------|
| Feature or major refactor completed | Yes |
| Debugging session that uncovered a systemic gap | Yes |
| Architectural decision made | Yes |
| Onboarding session where someone flagged missing context | Yes |
| Monthly, even if nothing major happened | Yes — catches accumulation |
| Trivial session (typo fix, doc edit) | No |

Monthly is the minimum cadence even for quiet projects. Small drifts accumulate silently.

## What Good Output Looks Like

Claude should return something like this (not verbatim — but this level of specificity):

```
Knowledge Feed — 2025-09-15

1. Pattern established: All database queries go through the repository layer, never called
   directly from route handlers. Rule to add: "Never call Prisma directly from route
   handlers — use the repository functions in src/db/."

2. Correction: I suggested lodash for array manipulation. You redirected to native array
   methods. Rule to add: "Don't import lodash — use native JS array methods. The bundle
   cost isn't worth it for our use case."

3. Architecture decision: We decided to keep auth logic in middleware, not in individual
   route handlers. Rule to add: "Auth checks belong in src/middleware/auth.ts — not in
   route handlers. If a route needs special auth logic, extend the middleware."

4. Stale rule: CLAUDE.md still references the old Express v4 error handler signature.
   We're on v5. Remove: "Express error handlers take 4 arguments (err, req, res, next)."
   Update to: "Express v5 error handlers: async errors propagate automatically — no need
   to call next(err)."
```

## After the Retro

### Review the output

Not everything Claude surfaces belongs in `CLAUDE.md`. Ask:

- Is this specific to our project, or generic advice Claude already knows?
- Is it actionable? Would a new Claude session make the same mistake without this rule?
- Is it already covered? Search before adding — duplicates reduce adherence.

### Update CLAUDE.md

Add new rules to the most relevant section. Remove any stale rules Claude flagged.

### Commit with a traceable message

```bash
git add CLAUDE.md
git commit -m "context: [what changed and why]"
```

Meaningful commit messages create a traceable history of how your AI context evolved. Useful
for debugging: "Claude started doing X wrong after we made change Y" becomes diagnosable
from git log.

Examples of good commit messages:

```
context: add lodash ban — use native array methods
context: clarify auth middleware pattern after refactor
context: remove Express v4 error handler rule — now on v5
context: document payment webhook idempotency requirement
context: add Prisma-direct query ban after code review
```

## Team Usage

When multiple people work with Claude on the same project, retros become especially valuable.
Each developer may get different corrections — different gaps in `CLAUDE.md` surface from
different angles. Consider:

- Running a retro at the end of any PR that involved significant Claude-assisted work
- Including `CLAUDE.md` in PR reviews as a standing agenda item
- Doing a quarterly joint retro with the whole team to review accumulated changes

The `CLAUDE.md` file is a shared asset. Its quality reflects how well the team maintains it.
