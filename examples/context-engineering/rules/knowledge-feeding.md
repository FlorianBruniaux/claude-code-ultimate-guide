# Knowledge Feeding Protocol

Context engineering is not a one-time setup — it accumulates value over time as Claude learns what works for your project. This file defines when and how to capture that learning back into your `CLAUDE.md`.

## When to Feed Knowledge

Run this protocol at the end of any session that:

- Completed a feature or meaningful code change
- Discovered a new pattern that worked well and should become standard
- Hit a mistake that required correction (especially if the mistake was repeated)
- Made an architectural decision that will affect future work
- Established a preference for a library, tool, or approach

Skip it for trivial sessions (typo fixes, doc edits, minor config changes).

## The Knowledge Feed Prompt

Paste this into Claude at the end of qualifying sessions:

```
Before we close this session, run a knowledge feed:

1. What patterns did we establish that should become permanent rules?
2. What did I correct or redirect that should be a rule to prevent recurrence?
3. Were any architectural decisions made that CLAUDE.md should record?
4. Is there anything in CLAUDE.md that this session proved wrong or outdated?

Output only high-signal items (3-5 max). Use the knowledge feed format below.
Skip anything obvious or already covered.
```

## Knowledge Feed Output Format

Claude should output discoveries in this structure:

```markdown
## Knowledge Feed — [YYYY-MM-DD]

### New Pattern (if applicable)
**What**: [One sentence describing the pattern]
**Why**: [Why this is the right approach for this project]
**Rule to add**:
> [Exact text to paste into CLAUDE.md, ready to copy]

### Anti-Pattern Found (if applicable)
**What happened**: [What Claude did wrong or what was corrected]
**Why it's wrong here**: [Project-specific reason, not generic best practice]
**Rule to add**:
> Never: [specific behavior to avoid and why]

### Architecture Decision (if applicable)
**Decision**: [What was decided]
**Rationale**: [Why — especially if it goes against common practice]
**Rule to add**:
> [Exact text to paste into CLAUDE.md]

### Stale Rule to Remove (if applicable)
**Rule**: [Current rule in CLAUDE.md]
**Why remove**: [What changed that makes this obsolete]
```

## Integration Workflow

After receiving the knowledge feed:

1. **Review before adding** — not all patterns generalize. Ask: "Would a new team member need to know this, or is it context-specific to this session?"
2. **Copy relevant rules** into the appropriate section of `CLAUDE.md`
3. **Remove any rules** Claude flagged as stale
4. **Commit the update** with a meaningful message:

```bash
git add CLAUDE.md
git commit -m "context: [short description of what was learned]"

# Examples:
# context: add zod validation rule after form refactor
# context: remove Redux rule — migrated to Zustand
# context: document payment webhook idempotency pattern
```

## Quality Filter

Before adding any rule to `CLAUDE.md`, check:

- **Is it specific to this project?** Generic best practices don't belong here — Claude already knows them.
- **Is it actionable?** "Be careful with async code" is useless. "Always check for race conditions in the order state machine" is useful.
- **Is it already covered?** Search for similar rules before adding. Duplicates dilute adherence.
- **Will it still be true in 6 months?** Avoid rules tied to temporary states ("we're migrating to X so don't use Y yet").

## Ownership

Knowledge feeding works best when it's a team habit, not one person's job. Any team member who works with Claude can contribute a knowledge feed. The person who reviews the PR for `CLAUDE.md` changes is responsible for quality filtering.
