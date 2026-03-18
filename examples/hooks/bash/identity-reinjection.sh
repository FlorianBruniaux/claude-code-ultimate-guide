#!/bin/bash
# .claude/hooks/identity-reinjection.sh
# Event: UserPromptSubmit
# Non-blocking guard: re-injects agent identity if context compaction erased it
#
# Problem: When Claude compacts context during a long session, agents configured
# with a specific role (team lead, reviewer, etc.) can "forget" their identity.
# The compacted transcript no longer contains the original system instructions.
#
# Solution: Store identity in a file. After each user message, check whether the
# last assistant response includes the expected identity marker. If not, inject
# the identity as additionalContext so the next response re-establishes the role.
#
# Setup:
#   1. Create .claude/agent-identity.txt with your agent's identity instructions
#   2. Set IDENTITY_MARKER to a short string that should appear in agent responses
#      (e.g. "LEAD:", "REVIEWER:", "DEVELOPER:")
#   3. Wire this hook to UserPromptSubmit in settings.json
#
# Output format: UserPromptSubmit additionalContext injection
# Properties:
#   - Silent no-op when identity is present (zero overhead)
#   - Silent no-op when no identity file configured
#   - Never blocks — exits 0 in all cases
#   - Compatible with agent teams (SubagentStart, SubagentStop) and solo sessions
#
# Based on pattern from Nick Tune: https://nick-tune.me/blog/2026-02-28-hook-driven-dev-workflows-with-claude-code/

set -uo pipefail

INPUT=$(cat)

# Identity file: customize path or override via env
IDENTITY_FILE="${CLAUDE_IDENTITY_FILE:-.claude/agent-identity.txt}"
IDENTITY_MARKER="${CLAUDE_IDENTITY_MARKER:-}"

# No-op: identity file not configured
if [[ ! -f "$IDENTITY_FILE" ]]; then
    exit 0
fi

IDENTITY=$(cat "$IDENTITY_FILE")

# No-op: empty identity
if [[ -z "$IDENTITY" ]]; then
    exit 0
fi

# Default marker: first non-empty, non-comment line of the identity file
if [[ -z "$IDENTITY_MARKER" ]]; then
    IDENTITY_MARKER=$(grep -m1 -v '^#' "$IDENTITY_FILE" | head -c 40 || true)
fi

# Read transcript to check last assistant message
TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || true)

if [[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]]; then
    exit 0
fi

# Extract the last assistant message from the transcript
LAST_ASSISTANT=$(jq -r '
    [.[] | select(.role == "assistant")] | last | .content |
    if type == "array" then map(select(.type == "text") | .text) | join("") else . end
' "$TRANSCRIPT_PATH" 2>/dev/null || true)

# Identity is intact: no action needed
if echo "$LAST_ASSISTANT" | grep -qF "$IDENTITY_MARKER" 2>/dev/null; then
    exit 0
fi

# Identity marker missing from last response — re-inject
# This happens after context compaction strips the original system instructions
jq -n \
    --arg context "[Identity reminder — your role and instructions follow. Resume your role immediately.]\n\n$IDENTITY" \
    '{"additionalContext": $context}'

exit 0
