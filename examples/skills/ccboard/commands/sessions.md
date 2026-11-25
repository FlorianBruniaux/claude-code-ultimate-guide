---
description: List or search recent Claude Code sessions with ccboard
argument-hint: "[search text]"
---

# Sessions

```bash
if ! command -v ccboard >/dev/null 2>&1; then echo "ccboard is not installed. Install it with /ccboard-install or: cargo install ccboard"; exit 1; fi
# no argument: the 10 most recent sessions
ccboard recent 10 --json
# with an argument: search by id, project, message or branch
ccboard search "$ARGUMENTS" --since 30d --limit 20 --json
```

Use the first command when no argument was given and the second otherwise. Summarize the sessions and do not paste raw message text into shared places. `ccboard info <session-id>` shows one session in detail.
