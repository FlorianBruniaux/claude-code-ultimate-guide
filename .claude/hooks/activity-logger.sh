#!/bin/bash
# Activity logger hook (async) - Logs all tool usage
# Usage: Called by Claude Code PostToolUse hook

set -euo pipefail

# Create logs directory
LOGS_DIR="$HOME/.claude/logs"
mkdir -p "$LOGS_DIR"

# Log file with today's date
LOG_FILE="$LOGS_DIR/activity-$(date +%Y-%m-%d).jsonl"

# Get tool info from environment
TOOL_NAME="${TOOL_NAME:-unknown}"
TOOL_INPUT="${TOOL_INPUT:-}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-unknown}"

# Create JSON log entry
LOG_ENTRY=$(cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "tool": "$TOOL_NAME",
  "project": "$PROJECT_DIR",
  "input_length": ${#TOOL_INPUT}
}
EOF
)

# Append to log file
echo "$LOG_ENTRY" >> "$LOG_FILE"

exit 0
