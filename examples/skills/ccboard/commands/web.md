---
description: Launch the ccboard web interface
---

# Web interface

```bash
if ! command -v ccboard >/dev/null 2>&1; then echo "ccboard is not installed. Install it with /ccboard-install or: cargo install ccboard"; exit 1; fi
ccboard web --port 3333   # replace 3333 when the user gave a port
```

The server stays in the foreground until stopped, so start it in a separate terminal or as a background task. Then open http://localhost:3333 (or the chosen port).

The web frontend is embedded only in the Homebrew and release binaries. A binary built with `cargo install ccboard` serves the API without a frontend. `ccboard both --port 3333` runs the TUI and the web server together.
