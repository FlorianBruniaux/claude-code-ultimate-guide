---
description: Show Claude Code token usage and cost figures from ccboard
---

# Costs

Run the non-interactive commands and summarize the result.

```bash
if ! command -v ccboard >/dev/null 2>&1; then echo "ccboard is not installed. Install it with /ccboard-install or: cargo install ccboard"; exit 1; fi
ccboard stats
ccboard report --format markdown --since 30d
```

`ccboard report` accepts `--budget <tokens>` and `--error-threshold <percent>`, which make it exit 1 when exceeded. Cost figures are estimates computed from local session data and ccboard's pricing table (`ccboard pricing`), not an invoice.
