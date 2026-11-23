#!/usr/bin/env bash
# velocity-governor.sh - Claude Code PreToolUse hook
# Throttles tool calls to stay under an estimated tokens-per-minute budget and
# avoid API rate limits.
#
# Environment variables:
#   CLAUDE_PROJECT_DIR      - absolute path of the project (set by Claude Code)
#   CLAUDE_VELOCITY_MAX_TPM - budget override (default: 50000 tokens/min)
#
# Anthropic API rate-limit headers (for tuning the budget):
#   anthropic-ratelimit-tokens-remaining
#   anthropic-ratelimit-tokens-reset
#   retry-after (on 429)
#
# Installation: add to .claude/settings.json under hooks.PreToolUse
# {
#   "hooks": {
#     "PreToolUse": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "bash examples/hooks/bash/velocity-governor.sh" }] }]
#   }
# }
#
# The hook sleeps until the current 60 second window ends when the budget is
# exceeded. It stays well under the default command timeout (600 seconds), but
# every tool call waits, so set a lower budget only if you accept that.

set -euo pipefail

# -- Configuration -------------------------------------------------------------
MAX_TOKENS_PER_MINUTE="${CLAUDE_VELOCITY_MAX_TPM:-50000}"
PROJECT_SLUG="${CLAUDE_PROJECT_DIR:-$PWD}"
PROJECT_SLUG="${PROJECT_SLUG//\//-}"
STATE_FILE="/tmp/claude-velocity-${PROJECT_SLUG}.json"

# -- Read stdin (JSON supplied by Claude Code) ---------------------------------
# The input is not used for the estimate below. It carries session_id, cwd,
# tool_name and tool_input for PreToolUse.
cat > /dev/null

# -- Load or initialize state --------------------------------------------------
now=$(date +%s)

if [[ -f "$STATE_FILE" ]]; then
  window_start=$(jq -r '.window_start // 0' "$STATE_FILE" 2>/dev/null || echo "$now")
  tokens_used=$(jq  -r '.tokens_used  // 0' "$STATE_FILE" 2>/dev/null || echo 0)
else
  window_start=$now
  tokens_used=0
fi

# -- Reset the sliding window (60 seconds) -------------------------------------
window_age=$(( now - window_start ))
if (( window_age >= 60 )); then
  window_start=$now
  tokens_used=0
fi

# -- Conservative cost estimate per tool call ----------------------------------
# One tool call is estimated at 500 tokens (read plus short write).
# Adjust CLAUDE_VELOCITY_MAX_TPM to match your API tier.
estimated_tokens=500
new_total=$(( tokens_used + estimated_tokens ))

# -- Throttle when the budget is exceeded --------------------------------------
if (( new_total > MAX_TOKENS_PER_MINUTE )); then
  remaining=$(( 60 - window_age ))
  if (( remaining > 0 )); then
    # Wait for the end of the current window
    sleep "$remaining"
    window_start=$(date +%s)
    new_total=$estimated_tokens
  fi
fi

# -- Persist state -------------------------------------------------------------
jq -n \
  --argjson ws "$window_start" \
  --argjson tu "$new_total" \
  '{window_start: $ws, tokens_used: $tu}' > "$STATE_FILE"

# -- Let the tool call through -------------------------------------------------
# exit 0 = continue normally. Exit 2 would block the call (only exit 2 blocks;
# exit 1 is a non-blocking error), but this hook throttles instead of blocking.
exit 0
