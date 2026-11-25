#!/bin/bash
# Hook: PostToolUse - Log all Claude Code operations for monitoring
# Exit 0 = allow (always)
#
# This hook logs all tool operations to JSONL files for later analysis.
# Use session-stats.sh to analyze the logs.
#
# Logs are stored in: ~/.claude/logs/activity-YYYY-MM-DD.jsonl
#
# Environment variables:
#   CLAUDE_LOG_DIR     - Override log directory (default: ~/.claude/logs)
#   CLAUDE_LOG_TOKENS  - Enable token estimation (default: true)
#
# The session id comes from the `session_id` field of the hook input.
#
# Place in: .claude/hooks/session-logger.sh
# Register in: .claude/settings.json under PostToolUse event

set -e

# Configuration
LOG_DIR="${CLAUDE_LOG_DIR:-$HOME/.claude/logs}"
ENABLE_TOKENS="${CLAUDE_LOG_TOKENS:-true}"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Log file for today
LOG_FILE="$LOG_DIR/activity-$(date +%Y-%m-%d).jsonl"

# Read JSON from stdin
INPUT=$(cat)

# Extract tool information
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
TOOL_INPUT=$(echo "$INPUT" | jq -c '.tool_input // {}')
# PostToolUse sends the result as `tool_response` (string or object)
TOOL_OUTPUT=$(echo "$INPUT" | jq -r '(.tool_response // "") | if type == "string" then . else tojson end')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Extract relevant details based on tool type
FILE_PATH=""
COMMAND=""

case "$TOOL_NAME" in
    Read|Write|Edit)
        FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // .path // ""')
        ;;
    Bash)
        COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // ""' | head -c 200)
        ;;
    Grep|Glob)
        FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.path // .pattern // ""')
        ;;
esac

# Estimate tokens (rough heuristic: ~4 chars per token)
TOKENS_INPUT=0
TOKENS_OUTPUT=0

if [[ "$ENABLE_TOKENS" == "true" ]]; then
    INPUT_LEN=${#TOOL_INPUT}
    OUTPUT_LEN=${#TOOL_OUTPUT}
    TOKENS_INPUT=$((INPUT_LEN / 4))
    TOKENS_OUTPUT=$((OUTPUT_LEN / 4))
fi

# Get project directory (if available)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Build log entry
LOG_ENTRY=$(jq -n \
    --arg timestamp "$TIMESTAMP" \
    --arg session_id "$SESSION_ID" \
    --arg tool "$TOOL_NAME" \
    --arg file "$FILE_PATH" \
    --arg command "$COMMAND" \
    --arg project "$PROJECT_NAME" \
    --argjson tokens_in "$TOKENS_INPUT" \
    --argjson tokens_out "$TOKENS_OUTPUT" \
    '{
        timestamp: $timestamp,
        session_id: $session_id,
        tool: $tool,
        file: (if $file != "" then $file else null end),
        command: (if $command != "" then $command else null end),
        project: $project,
        tokens: {
            input: $tokens_in,
            output: $tokens_out,
            total: ($tokens_in + $tokens_out)
        }
    } | with_entries(select(.value != null))'
)

# Append to log file
echo "$LOG_ENTRY" >> "$LOG_FILE"

# Always allow
exit 0
