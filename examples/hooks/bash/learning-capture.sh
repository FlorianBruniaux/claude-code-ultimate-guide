#!/bin/bash
# Hook: Stop - Remind the user to capture one learning insight
# Event: Stop (fires each time Claude finishes responding, not only at session end)
# Purpose: Build a learning journal with minimal friction
#
# This hook only DISPLAYS a reminder. It cannot read the user's answer, so the
# insight has to be appended to the journal by hand (or by a prompt you give
# Claude). To avoid repeating the reminder after every response, it fires once
# per session, tracked by a marker file next to the journal.
#
# Exit codes:
#   0 = success (always returns 0)
#
# Output: systemMessage (shown to the user) pointing at ~/claude-learnings.md
#
# Configuration:
#   CLAUDE_LEARNING_LOG - Custom log path (default: ~/claude-learnings.md)
#   CLAUDE_LEARNING_SKIP - Set to 1 to skip the reminder
#
# Installation (.claude/settings.json; Stop has no matcher):
#   {
#     "hooks": {
#       "Stop": [{
#         "hooks": [{ "type": "command", "command": "~/.claude/hooks/learning-capture.sh" }]
#       }]
#     }
#   }

set -e

# Configuration
LOG_FILE="${CLAUDE_LEARNING_LOG:-$HOME/claude-learnings.md}"
SKIP_PROMPT="${CLAUDE_LEARNING_SKIP:-0}"

# Skip if disabled
if [[ "$SKIP_PROMPT" == "1" ]]; then
    exit 0
fi

# Read hook input; the session id keys the once-per-session marker
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
if [[ -z "$SESSION_ID" ]]; then
    exit 0
fi

# Ensure log file directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Remind once per session
MARKER="$(dirname "$LOG_FILE")/.claude-learning-reminded-${SESSION_ID}"
if [[ -f "$MARKER" ]]; then
    exit 0
fi
touch "$MARKER"

# Create log file with header if it doesn't exist
if [[ ! -f "$LOG_FILE" ]]; then
    cat > "$LOG_FILE" << 'HEADER'
# Claude Learning Journal

A record of insights captured during coding sessions.

---

HEADER
fi

jq -n --arg log "$LOG_FILE" \
    '{systemMessage: ("Quick reflection: what is ONE thing you learned this session? Add it to " + $log)}'

exit 0
