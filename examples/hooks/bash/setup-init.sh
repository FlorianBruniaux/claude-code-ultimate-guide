#!/bin/bash
# setup-init.sh
# Event: Setup
# Fires only for `claude --init-only`, or `claude -p --init` / `claude -p --maintenance`
# (matcher "init" or "maintenance"). It does NOT fire on a normal start.
#
# Setup hooks cannot block and Claude Code discards their JSON output (systemMessage,
# additionalContext and so on), so this hook reports through plain stdout and stderr.
# With `-p`, a Setup hook's stdout, stderr and exit code appear in the run output.
#
# Installation (.claude/settings.json):
#   {
#     "hooks": {
#       "Setup": [{
#         "matcher": "init",
#         "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/setup-init.sh" }]
#       }]
#     }
#   }
#
# Input fields read: session_id, cwd, trigger ("init" or "maintenance")

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
CWD=$(echo "$INPUT" | jq -r '.cwd // "unknown"')
TRIGGER=$(echo "$INPUT" | jq -r '.trigger // "unknown"')

# Create log directory if needed
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

# Log setup event
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$TIMESTAMP] Setup hook triggered ($TRIGGER) - Session: $SESSION_ID - CWD: $CWD" >> "$LOG_DIR/setup.log"

# Check project requirements
if [[ -f "package.json" && ! -d "node_modules" ]]; then
    echo "Project setup incomplete: node_modules missing. Run 'npm install' before continuing."
fi

# Report git status
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current)
    UNCOMMITTED=$(git status --short | wc -l | tr -d ' ')

    if [[ $UNCOMMITTED -gt 0 ]]; then
        echo "Git status: on branch $BRANCH with $UNCOMMITTED uncommitted changes."
    fi
fi

exit 0
