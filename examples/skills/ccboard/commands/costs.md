---
name: costs
description: Open ccboard costs analysis tab
category: analytics
---

# Costs Analysis Command

Launch ccboard and jump directly to the costs tracking and analytics tab.

## Features

- **3 Views**:
  - Overview: Total costs and breakdown
  - By Model: Cost per AI model (Opus, Sonnet, Haiku)
  - Daily Trend: Cost evolution over time

- **Token Breakdown**:
  - Input tokens (prompt)
  - Output tokens (generation)
  - Cache read tokens (reused)
  - Cache write tokens (stored)

- **Pricing**: Automatic calculation based on 2024 Anthropic rates

## Usage

```bash
# Open costs tab directly
/costs

# Alternative: run with tab argument
ccboard --tab costs
```

## Costs Tab Navigation

- `1` : Overview view
- `2` : By Model view
- `3` : Daily Trend view
- `Tab` : Switch between views
- `↑/↓` : Scroll through data

## Example Output

```
Total Tokens: 17.32M
Total Cost: $9,145.20

Breakdown by Model:
- Opus 4.5:   76% ($7,828)  ████████████████
- Sonnet 4.5: 14% ($1,314)  ███
- Haiku 3.5:  10% ($3)      █

Token Distribution:
- Input:       10.70M (65%)
- Output:      4.58M  (28%)
- Cache Read:  1.01M  (6%)
- Cache Write: 1.04B  (1%)
```

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

# Launch ccboard with Costs tab (tab index 5, accessible with '6' key)
# For now, launch and user presses '6'
exec ccboard
```

**Note**: Currently launches ccboard in dashboard view. Press `6` to access Costs tab.
Future version will support `ccboard --tab costs` for direct access.
