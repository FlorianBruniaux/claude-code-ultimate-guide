---
name: ccboard-web
description: Launch ccboard web interface
category: monitoring
---

# Web Interface Command

Launch the ccboard web UI for browser-based monitoring and visualization.

## Features

- **Web Dashboard**: Access ccboard from any browser
- **Live Updates**: Server-Sent Events (SSE) for real-time data
- **Responsive Design**: Works on desktop, tablet, mobile
- **Same Data**: Shares data layer with TUI (single binary)
- **Concurrent Access**: Multiple users can view simultaneously

## Usage

```bash
# Launch web UI on default port 3333
/ccboard-web

# Or specify custom port
ccboard web --port 8080
```

## Access

Once launched, open in your browser:
```
http://localhost:3333
```

## Modes

ccboard supports 3 execution modes:

1. **TUI only** (default):
   ```bash
   ccboard
   ```

2. **Web only**:
   ```bash
   ccboard web --port 3333
   ```

3. **Both simultaneously**:
   ```bash
   ccboard both --port 3333
   ```
   Runs TUI in terminal + web server on port 3333

## Web UI Features

- Dashboard with real-time stats
- Sessions browser with pagination
- Configuration viewer (read-only)
- Hooks, agents, costs visualization
- MCP server status
- History and search

## Requirements

ccboard must be installed. Run `/ccboard-install` if needed.

## Implementation

```bash
#!/bin/bash

# Check if ccboard is installed
if ! command -v ccboard &> /dev/null; then
    echo "❌ ccboard is not installed"
    echo "Run: /ccboard-install"
    exit 1
fi

# Default port
PORT="${1:-3333}"

echo "🌐 Launching ccboard web interface..."
echo "Access at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Launch web UI
exec ccboard web --port "$PORT"
```

**Note**: Web UI is currently in development. TUI is the primary interface with full feature set.
