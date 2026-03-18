---
description: Daily update check — official Anthropic docs diff + guide/CC releases digest
---

Run this sequence in order. Present results as one consolidated report.

## Step 1 — Refresh official docs

Call `refresh_official_docs` MCP tool to fetch the latest Anthropic docs and update the current snapshot.

If it fails (no baseline), tell the user to run /ccguide:init-docs once first, then stop.

## Step 2 — Diff official docs

Call `diff_official_docs` MCP tool to compare baseline vs refreshed current.

## Step 3 — Guide + CC releases digest

Call `get_digest` MCP tool with period: "day"

---

## Output format

Present everything as a single daily briefing:

```
# Daily Claude Code Update — {today's date}

## Official Anthropic Docs
{diff results — added/removed/modified sections, or "No changes"}

## Guide + CC CLI
{digest results — guide CHANGELOG entries + CC releases from last 24h, or "No changes"}

---
Docs snapshot: {baseline date} → {current date}
```

Rules:
- If no changes anywhere: say so clearly in one line, no padding
- Reproduce ALL URLs verbatim (source URLs, GitHub links)
- If official docs unchanged AND no guide/CC updates: "Nothing changed in the last 24h."
- Keep it dense — this is a daily briefing, not a report
