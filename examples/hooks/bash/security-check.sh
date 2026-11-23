#!/bin/bash
# PreToolUse hook - Block commands containing secrets
# Place in: .claude/hooks/security-check.sh
# Register in: .claude/settings.json (PreToolUse, matcher "Bash")
#
# Blocks with exit 2 and a stderr message: Claude sees the stderr text as the
# denial reason. (A top-level "decision": "block" is deprecated for PreToolUse,
# which uses hookSpecificOutput.permissionDecision.)

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL" == "Bash" ]]; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

    # Check for common secret patterns
    PATTERNS=(
        "password="
        "PASSWORD="
        "secret="
        "SECRET="
        "api_key="
        "API_KEY="
        "apikey="
        "token="
        "TOKEN="
        "aws_access_key"
        "AWS_ACCESS_KEY"
        "aws_secret"
        "AWS_SECRET"
        "private_key"
        "PRIVATE_KEY"
    )

    for PATTERN in "${PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -qi "$PATTERN"; then
            echo "Blocked: potential secret detected in command: $PATTERN" >&2
            exit 2
        fi
    done

    # Check for hardcoded credentials in common formats
    # API keys (typically long alphanumeric strings)
    if echo "$COMMAND" | grep -qE "(sk-[a-zA-Z0-9]{20,}|pk_[a-zA-Z0-9]{20,}|[a-f0-9]{32,})"; then
        echo "Blocked: potential API key or hash detected in command" >&2
        exit 2
    fi
fi

# Allow the command
exit 0
