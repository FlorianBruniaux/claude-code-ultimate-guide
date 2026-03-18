---
description: Compare official Anthropic docs baseline vs current snapshot (no network — instant)
---

Use the `diff_official_docs` MCP tool.

No network call — reads local index files only (~50KB each). Instant.

Present the results clearly:
- Added sections (new pages in the official docs)
- Removed sections
- Modified sections with line delta and first changed line
- Unchanged count

If no baseline exists, tell the user to run /ccguide:init-docs first.
If no current snapshot exists, tell the user to run /ccguide:refresh-docs first.
If no changes, confirm everything is in sync and suggest running /ccguide:refresh-docs to update.
