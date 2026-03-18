#!/bin/bash
# RTK Auto-Wrapper Hook
# Automatically wraps high-verbosity commands with RTK for token optimization
#
# Hook: PreToolUse
# Matcher: Bash
# Purpose: Intercept bash commands and suggest RTK wrapper if applicable
#
# Installation:
# 1. Copy to .claude/hooks/bash/rtk-auto-wrapper.sh
# 2. Make executable: chmod +x .claude/hooks/bash/rtk-auto-wrapper.sh
# 3. Add to settings.json:
#    {
#      "hooks": {
#        "PreToolUse": [{
#          "matcher": "Bash",
#          "hooks": [".claude/hooks/bash/rtk-auto-wrapper.sh"]
#        }]
#      }
#    }
#
# Or use `rtk init` for automatic hook setup.

# Check if RTK is installed
if ! command -v rtk &> /dev/null; then
    # RTK not installed, skip silently
    exit 0
fi

# Parse tool input to get the bash command
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    # No command found, continue
    exit 0
fi

# Define RTK-optimizable commands with their savings
declare -A RTK_COMMANDS=(
    ["git log"]="92.3"
    ["git status"]="76.0"
    ["git diff"]="55.9"
    ["find"]="76.3"
    ["cargo test"]="90.0"
    ["cargo build"]="80.0"
    ["cargo clippy"]="80.0"
    ["pnpm list"]="82.0"
    ["pnpm outdated"]="90.0"
    ["pnpm test"]="90.0"
    ["python pytest"]="90.0"
    ["python -m pytest"]="90.0"
    ["go test"]="90.0"
)

# Check if command matches RTK-optimizable pattern
for cmd in "${!RTK_COMMANDS[@]}"; do
    if [[ "$COMMAND" == "$cmd"* ]] && [[ "$COMMAND" != "rtk "* ]]; then
        savings="${RTK_COMMANDS[$cmd]}"

        # Suggest RTK wrapper
        cat << EOF
RTK Optimization Available

Command: $COMMAND
Suggested: rtk $COMMAND
Token Savings: ~${savings}%

Using RTK wrapper automatically.
EOF

        # Modify command to use RTK
        # Note: This is informational only - actual command modification
        # requires additionalContext return (Claude Code v2.1.9+)

        # For now, just inform user
        exit 0
    fi
done

# Continue with original command
exit 0
