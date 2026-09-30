---
name: mcp-integration-reference
description: "Template for skills that integrate with an MCP server. Demonstrates the reference file pattern: Claude reads a domain-specific MCP cheatsheet before making any tool calls, reducing query failures caused by server-specific gotchas. Fork this skill and replace the Sentry example with your target MCP."
allowed-tools: Read mcp__<your-mcp>__*
effort: high
metadata:
  version: 1.0.0
---

# MCP integration reference pattern

> This is a template skill. It shows how to structure a skill that wraps an MCP server. Replace `sentry` with your MCP server name and adapt the reference file at `references/sentry-mcp.md`.

## What this pattern solves

When a skill calls an MCP server without prior context, Claude guesses at the query syntax. This works for simple calls but breaks on anything with non-obvious behavior: pagination quirks, required parameter combinations, rate limits, or subtle format restrictions.

The fix: a `references/<mcp-name>.md` file that captures all the gotchas. The skill reads this file before making any MCP call. Zero guessing.

Three types of content go in the reference file:
1. Parameter semantics that differ from what the tool name implies
2. Known error patterns and their root causes
3. Working query examples (copy-paste, no thinking required)

---

## Step 1: Read the MCP reference file

**Before doing anything else**, read the full MCP reference:

```
Read: references/sentry-mcp.md
```

This file contains query syntax, known gotchas, and working examples for the Sentry MCP. Do not skip this step.

---

## Step 2: Gather scope from user

Ask the user:

- **Time range**: Last 24h? 7 days? Custom range?
- **Environments**: `production`, `staging`, or both?
- **Projects**: All projects or specific ones? (Default: all)

If the user says "just run it with defaults", use:
- Time range: last 72 hours
- Environment: `production` only
- Projects: all

---

## Step 3: Fetch error data

Using the tool knowledge from Step 1, fetch:

1. **Issue list**: Active unresolved issues, ordered by frequency
2. **Event details**: Full stack traces for the top 5 issues by event count

Cap results at 50 issues. If more exist, note the count and focus on the highest-frequency items.

---

## Step 4: Group and analyze

Group issues by root cause, not by error message. Two issues with different messages can share the same underlying cause (shared code path, same external dependency, same config).

For each group:
- Count of issues in the group
- Earliest first-seen date
- Affected users count (if available)
- Most likely root cause (one sentence, evidence-based)
- Relevant file paths from the stack trace

---

## Step 5: Generate report

Output a markdown report with this structure:

```markdown
# Error Report: [Project or Scope]

**Period**: [start] to [end]
**Environment**: [env]
**Total active issues**: [N]

## Summary

[2-3 sentences: what is the overall health picture?]

## Issue Groups

### Group 1: [Root Cause Label]

| Attribute      | Value                    |
|----------------|--------------------------|
| Issues         | N                        |
| Total events   | N                        |
| Affected users | N                        |
| First seen     | YYYY-MM-DD               |
| Key file       | path/to/file.py:line     |

**Root cause**: [One paragraph. Specific, evidence-based. Point to file and line.]

**Suggested investigation**: [One or two concrete next steps.]

---

[Repeat for each group]

## Out of Scope

[List issues explicitly excluded and why. Example: "404s on /static/ excluded - expected behavior for SPA asset versioning."]
```

---

## Scope rules

- This skill detects and describes issues. It does not modify code or create tickets.
- If an issue is ambiguous, flag it as "needs investigation" rather than guessing.
- Do not include informational logs or warnings unless they correlate directly with errors.

---

## Adapting this template

To fork this skill for a different MCP:

1. Copy this directory: `cp -r examples/skills/mcp-integration-reference examples/skills/<your-skill>/`
2. Rename `references/sentry-mcp.md` to `references/<your-mcp>.md`
3. Replace the reference file content with your MCP's gotchas
4. Update `allowed-tools` in the frontmatter to match your MCP tool names
5. Adjust the analysis steps to match your data domain

The pattern works for any MCP that has non-obvious query behavior: Datadog, PagerDuty, Linear, Jira, Posthog, Mixpanel, etc.
