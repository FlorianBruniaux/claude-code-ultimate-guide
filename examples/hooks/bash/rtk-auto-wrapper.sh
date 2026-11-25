#!/bin/bash
# RTK Auto-Wrapper Hook
# Rewrites high-verbosity Bash commands to run through RTK for token optimization
#
# Hook: PreToolUse
# Matcher: Bash
# Purpose: Prefix known verbose commands with `rtk`, using `updatedInput`
#
# How it works: the hook reads the tool call from stdin and, when the command
# starts with one of the commands below, returns `hookSpecificOutput.updatedInput`
# with the command rewritten to `rtk <command>`. No `permissionDecision` is set, so
# the normal permission flow still applies to the rewritten command. Only the
# start of the command line is matched, so `rtk` is prefixed to the whole line.
#
# Installation:
# 1. Copy to .claude/hooks/rtk-auto-wrapper.sh
# 2. Make executable: chmod +x .claude/hooks/rtk-auto-wrapper.sh
# 3. Add to settings.json:
#    {
#      "hooks": {
#        "PreToolUse": [{
#          "matcher": "Bash",
#          "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/rtk-auto-wrapper.sh" }]
#        }]
#      }
#    }
#
# Or use `rtk init` for automatic hook setup.

INPUT=$(cat)

# Check if RTK is installed
if ! command -v rtk &> /dev/null; then
    # RTK not installed, skip silently
    exit 0
fi

# Parse the Bash command from the tool input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
    # No command found, continue
    exit 0
fi

# Define RTK-optimizable commands with their estimated savings (percent of output
# tokens; estimates carried over from the original example, not re-measured)
# Bash 3.2 compatible (macOS /bin/bash has no associative arrays): each entry
# is "name::value", split with ${entry%%::*} and ${entry#*::}.
RTK_COMMANDS=(
    "git log::92.3"
    "git status::76.0"
    "git diff::55.9"
    "find::76.3"
    "cargo test::90.0"
    "cargo build::80.0"
    "cargo clippy::80.0"
    "pnpm list::82.0"
    "pnpm outdated::90.0"
    "pnpm test::90.0"
    "python pytest::90.0"
    "python -m pytest::90.0"
    "go test::90.0"
)

# Check if command matches RTK-optimizable pattern
for entry in "${RTK_COMMANDS[@]}"; do
    cmd="${entry%%::*}"
    if [[ "$COMMAND" == "$cmd"* ]] && [[ "$COMMAND" != "rtk "* ]]; then
        savings="${entry#*::}"

        # updatedInput replaces the WHOLE tool input, so copy every field and
        # change only `command`. systemMessage is shown to the user.
        echo "$INPUT" | jq --arg savings "$savings" '{
          systemMessage: ("RTK wrapper applied: ~" + $savings + "% fewer output tokens for this command"),
          hookSpecificOutput: {
            hookEventName: "PreToolUse",
            updatedInput: (.tool_input | .command = ("rtk " + .command))
          }
        }'
        exit 0
    fi
done

# Continue with original command
exit 0
