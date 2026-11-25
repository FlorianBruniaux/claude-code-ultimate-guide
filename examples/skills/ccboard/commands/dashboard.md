---
description: Launch the ccboard TUI dashboard for Claude Code usage
---

# Dashboard

The ccboard TUI is interactive and needs a real terminal, so it cannot run inside this session's Bash tool. Check that it is installed, then tell the user to run it in a separate terminal.

```bash
if ! command -v ccboard >/dev/null 2>&1; then echo "ccboard is not installed. Install it with /ccboard-install or: cargo install ccboard"; exit 1; fi
ccboard --version
```

Tell the user to run `ccboard` in another terminal. Inside the TUI, `?` shows the current keys and tabs, `r` refreshes, `q` quits.

For numbers without opening the TUI, run `ccboard stats` and summarize the output.
