---
name: dashboard
description: Launch ccboard TUI dashboard
category: monitoring
---

# Dashboard Command

Launch the interactive ccboard TUI to visualize and monitor your Claude Code usage.

## Features

- **8 Interactive Tabs**: Dashboard, Sessions, Config, Hooks, Agents, Costs, History, MCP
- **Real-time Monitoring**: File watcher for live updates
- **MCP Management**: Server status and configuration
- **Cost Tracking**: Token usage and pricing analytics
- **Session Explorer**: Browse and search conversation history
- **File Editing**: Press `e` to edit files in $EDITOR

## Usage

```bash
# Launch TUI dashboard
/dashboard

# Alternative: run directly
ccboard
```

## Navigation

- `1-8` : Jump to specific tab
- `Tab` / `Shift+Tab` : Navigate tabs
- `q` : Quit
- `F5` : Refresh data
- `e` : Edit selected file
- `o` : Reveal file in finder

## Requirements

ccboard must be installed. If not installed, run:
```bash
/ccboard-install
```

## Implementation

```bash
#!/bin/bash

# Check if ccboard is installed
if ! command -v ccboard &> /dev/null; then
    echo "❌ ccboard is not installed"
    echo ""
    echo "Install with:"
    echo "  /ccboard-install"
    echo ""
    echo "Or manually:"
    echo "  cargo install ccboard"
    exit 1
fi

# Launch ccboard TUI
exec ccboard
```
