#!/bin/bash
# permission-request.sh
# Event: PermissionRequest (runs when Claude Code is about to show a permission dialog)
# Use for custom approval logic or logging
#
# Input fields read: tool_name, tool_input, session_id, cwd
# Decision: print a `decision` object under hookSpecificOutput. Exit code 2 is NOT
# honored on this event: the permission flow proceeds unchanged and stderr is
# discarded, so a deny has to be returned as JSON.
#
# Installation (.claude/settings.json; the matcher filters on tool name):
#   {
#     "hooks": {
#       "PermissionRequest": [{
#         "matcher": "Bash|Write|Edit",
#         "hooks": [{ "type": "command", "command": "~/.claude/hooks/permission-request.sh" }]
#       }]
#     }
#   }

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Log permission request
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

LOG_ENTRY=$(jq -n \
  --arg timestamp "$TIMESTAMP" \
  --arg tool "$TOOL_NAME" \
  --arg session "$SESSION_ID" \
  '{timestamp: $timestamp, tool: $tool, session: $session}')

echo "$LOG_ENTRY" >> "$LOG_DIR/permissions-$(date +%Y-%m-%d).jsonl"

# Example: auto-deny file writes inside a production directory
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]] && [[ "${FILE_PATH:-$CWD}" == *"/production"* ]]; then
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PermissionRequest",
        decision: {
          behavior: "deny",
          message: "File writes in a production directory need manual approval outside Claude Code."
        }
      }
    }'
    exit 0
fi

# Example: warn the user about sudo (systemMessage is shown to the user; the
# permission dialog still appears because no decision is returned)
if [[ "$TOOL_NAME" == "Bash" && "$COMMAND" =~ (^|[[:space:];&|])sudo[[:space:]] ]]; then
    jq -n '{systemMessage: "Warning: Bash command requests sudo. Review carefully before approving."}'
fi

exit 0
