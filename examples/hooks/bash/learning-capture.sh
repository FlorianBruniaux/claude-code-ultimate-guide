#!/bin/bash
# Hook: Stop - Capture one learning insight at session end
# Event: Stop (when Claude finishes responding)
# Purpose: Build a learning journal with minimal friction
#
# Exit codes:
#   0 = success (always returns 0 to not block session end)
#
# Output: Appends to ~/claude-learnings.md
#
# Configuration:
#   CLAUDE_LEARNING_LOG - Custom log path (default: ~/claude-learnings.md)
#   CLAUDE_LEARNING_SKIP - Set to 1 to skip prompt

set -e

# Configuration
LOG_FILE="${CLAUDE_LEARNING_LOG:-$HOME/claude-learnings.md}"
SKIP_PROMPT="${CLAUDE_LEARNING_SKIP:-0}"

# Skip if disabled
if [[ "$SKIP_PROMPT" == "1" ]]; then
    exit 0
fi

# Read hook input (not used but consumed to avoid errors)
INPUT=$(cat)

# Get project context
PROJECT_NAME=$(basename "${CLAUDE_PROJECT_DIR:-$(pwd)}")
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

# Ensure log file directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Create log file with header if it doesn't exist
if [[ ! -f "$LOG_FILE" ]]; then
    cat > "$LOG_FILE" << 'HEADER'
# Claude Learning Journal

A record of insights captured during coding sessions.

---

HEADER
fi

# Return system message prompting for learning capture
# The user's response will be logged by the next invocation
# (This is a non-blocking prompt approach)
cat << EOF
{
  "systemMessage": "Session ending. Quick reflection:\n\nWhat's ONE thing you learned this session?\n\n(Type your answer, or 'skip' to end without logging)\n\nLogging to: $LOG_FILE"
}
EOF

exit 0
