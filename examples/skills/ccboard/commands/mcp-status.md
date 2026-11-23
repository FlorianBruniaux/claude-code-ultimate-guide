---
description: Open the MCP servers tab of the ccboard TUI
---

# MCP status

The MCP tab is part of the interactive TUI, so run it in a separate terminal.

```bash
if ! command -v ccboard >/dev/null 2>&1; then echo "ccboard is not installed. Install it with /ccboard-install or: cargo install ccboard"; exit 1; fi
ccboard --version
```

Tell the user to run `ccboard`, press `?` for the current tab keys, and open the MCP tab. Server status detection relies on the process list and is reported as unknown on Windows.
