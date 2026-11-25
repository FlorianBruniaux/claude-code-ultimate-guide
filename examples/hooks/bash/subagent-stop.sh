#!/bin/bash
# subagent-stop.sh
# Event: SubagentStop (runs when a subagent finishes responding)
# Use for logging or metrics
#
# Input fields read: session_id, agent_id, agent_type, agent_transcript_path,
# last_assistant_message. The input has no exit code and no duration, so this hook
# logs what is available. To measure duration, record a timestamp in a SubagentStart
# hook keyed by agent_id and subtract it here.
#
# Matcher: filters on agent_type (for example "Explore", "code-reviewer"). Omit it to
# log every subagent.
#
# Caution: on SubagentStop, JSON that sets decision "block" or
# hookSpecificOutput.additionalContext keeps the subagent running. This hook only
# logs and prints nothing.
#
# Installation (.claude/settings.json):
#   {
#     "hooks": {
#       "SubagentStop": [{
#         "hooks": [{ "type": "command", "command": "~/.claude/hooks/subagent-stop.sh" }]
#       }]
#     }
#   }

INPUT=$(cat)
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // "unknown"')
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id // "unknown"')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.agent_transcript_path // ""')
REPLY_CHARS=$(echo "$INPUT" | jq -r '(.last_assistant_message // "") | length')

# Log subagent completion
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

LOG_ENTRY=$(jq -n \
  --arg timestamp "$TIMESTAMP" \
  --arg agent_type "$AGENT_TYPE" \
  --arg agent_id "$AGENT_ID" \
  --arg session "$SESSION_ID" \
  --arg transcript "$TRANSCRIPT" \
  --argjson reply_chars "$REPLY_CHARS" \
  '{timestamp: $timestamp, agent_type: $agent_type, agent_id: $agent_id, session: $session, agent_transcript_path: $transcript, reply_chars: $reply_chars}')

echo "$LOG_ENTRY" >> "$LOG_DIR/subagents-$(date +%Y-%m-%d).jsonl"

exit 0
