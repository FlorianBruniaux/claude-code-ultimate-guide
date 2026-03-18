---
description: Search official Anthropic Claude Code docs by keyword
---

Use the `search_official_docs` MCP tool with query: $ARGUMENTS

If no query is given, ask the user what they want to search for.

Default limit: 5 results.

Present each result with:
- Section title
- Source URL (reproduce verbatim)
- Excerpt showing the relevant content

If no snapshot exists, tell the user to run /ccguide:init-docs first.
