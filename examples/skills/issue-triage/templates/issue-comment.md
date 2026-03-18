# Issue Comment Templates

Use these templates to generate GitHub issue comments during `/issue-triage` Phase 3. Comments are posted in **English** (international audience).

---

## Template 1 — Ack / Info Request

Use when: issue is `Unclear` or `needs-info`, body is missing context, reproduction steps are absent.

```markdown
Thanks for opening this issue!

To help us investigate, could you provide the following?

- **Steps to reproduce**: A minimal sequence of actions that triggers the behavior
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**: OS, version, relevant config (if applicable)

Once we have this information, we can prioritize and route the issue appropriately.

---
*Triaged via Claude Code /issue-triage*
```

---

## Template 2 — Duplicate

Use when: Jaccard similarity >= 60% with an existing open or recently closed issue.

```markdown
Thanks for reporting this! After reviewing the backlog, this appears to be a duplicate of #{original_number}.

{original_number} is tracking the same underlying behavior: {one-sentence description of original}.

I'm closing this issue to consolidate discussion there. If you believe this is a distinct issue with different root cause or scope, please reopen with additional context explaining the difference.

---
*Triaged via Claude Code /issue-triage*
```

---

## Template 3 — Close Stale

Use when: issue has had no activity for >90 days and no assignee, or no response to a previous info request for >30 days.

```markdown
This issue has been inactive for {days} days without updates or response.

We're closing it to keep the backlog actionable. If this is still relevant to you, please reopen and provide:

- Current status: is this still reproducible?
- Any additional context or workarounds you've found

We're happy to pick this back up if it's still blocking you.

---
*Triaged via Claude Code /issue-triage*
```

---

## Template 4 — Close Out of Scope

Use when: issue describes functionality clearly outside the project's stated scope.

```markdown
Thanks for the suggestion! After review, this falls outside the current scope of this project.

{Briefly explain why — e.g., "This project focuses on X; Y is handled by Z" or "This would require changes to the underlying architecture that are not planned."}

You might find what you're looking for in:
- {alternative project or tool if known}
- {documentation link if relevant}

Feel free to open a discussion if you'd like to explore this further.

---
*Triaged via Claude Code /issue-triage*
```

---

## Formatting Rules

**Tone**: Professional, direct, respectful. The reporter invested time to file the issue.

**Rules**:
- Never imply the reporter is wrong or wasted time
- Be specific when referencing duplicates (title + number, not just number)
- For close stale: always invite to reopen — do not make it feel permanent
- For OOS: offer an alternative when possible, even if vague
- No superlatives ("great issue", "awesome report") — factual only

**Customization points** (replace in all templates):
- `{original_number}`: issue number of the canonical duplicate
- `{one-sentence description}`: short summary of the original issue
- `{days}`: days since last activity (from `updatedAt`)
- Inline explanations marked with `{...}`: always fill before posting

**Signature** (required on all comments):
```
*Triaged via Claude Code /issue-triage*
```
