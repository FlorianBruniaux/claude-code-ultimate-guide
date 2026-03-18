---
description: Fetch official Anthropic Claude Code docs and store as local baseline snapshot
---

Use the `init_official_docs` MCP tool.

This fetches ~1.2MB from Anthropic (takes ~5s) and stores 4 local cache files in ~/.cache/claude-code-guide/.
Both the baseline and current snapshots are set to this version.

After success, tell the user:
- How many sections were found
- The snapshot path
- That they can now run /ccguide:diff-docs after /ccguide:refresh-docs to see what changed
