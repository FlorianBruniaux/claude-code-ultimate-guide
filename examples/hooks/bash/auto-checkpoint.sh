#!/bin/bash
# .claude/hooks/auto-checkpoint.sh
# Event: Stop (fires each time Claude finishes responding, not only at session end)
# Saves a git stash checkpoint of tracked changes after each response.
# Inspired by checkpoint pattern for safe experimentation
#
# `git stash create` + `git stash store` records a snapshot WITHOUT touching the
# working tree, so Claude keeps working on the same files. Untracked files are
# not included. A snapshot identical to the previous one is skipped.
#
# Installation (.claude/settings.json):
#   {
#     "hooks": {
#       "Stop": [{
#         "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-checkpoint.sh" }]
#       }]
#     }
#   }

set -euo pipefail

INPUT=$(cat)

# Loop guard: skip when Claude is already continuing because of a Stop hook
if [[ "$(echo "$INPUT" | jq -r '.stop_hook_active // false')" == "true" ]]; then
    exit 0
fi

SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Check if there are uncommitted changes to tracked files
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    STASH_NAME="claude-checkpoint-${BRANCH}-${TIMESTAMP}"

    # Snapshot commit; prints nothing when there is nothing to stash
    SNAPSHOT=$(git stash create "$STASH_NAME" 2>/dev/null || true)
    [[ -z "$SNAPSHOT" ]] && exit 0

    # Skip when the previous checkpoint already holds the same tree
    LAST_TREE=$(git rev-parse -q --verify 'refs/stash^{tree}' 2>/dev/null || true)
    if [[ -n "$LAST_TREE" && "$LAST_TREE" == "$(git rev-parse "${SNAPSHOT}^{tree}")" ]]; then
        exit 0
    fi

    git stash store -m "$STASH_NAME" "$SNAPSHOT" >/dev/null 2>&1

    # Log checkpoint creation
    LOG_DIR="$HOME/.claude/logs"
    mkdir -p "$LOG_DIR"
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Created checkpoint: $STASH_NAME (session: $SESSION_ID)" \
        >> "$LOG_DIR/checkpoints.log"

    # Notify user (systemMessage is shown to the user, not to Claude)
    jq -n --arg name "$STASH_NAME" \
        '{systemMessage: ("Checkpoint created: " + $name + "\nRestore with: git stash list (find it), then git stash apply stash@{N}")}'
fi

exit 0
