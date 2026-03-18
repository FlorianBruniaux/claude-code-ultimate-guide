#!/bin/bash
# .claude/hooks/auto-checkpoint.sh
# Event: Stop
# Auto-creates git stash checkpoint when Claude Code session ends
# Inspired by checkpoint pattern for safe experimentation

set -euo pipefail

INPUT=$(cat)

# Extract session metadata
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    # Create descriptive stash name
    STASH_NAME="claude-checkpoint-${BRANCH}-${TIMESTAMP}"

    # Stash with descriptive message
    git stash push -u -m "$STASH_NAME" >/dev/null 2>&1

    # Log checkpoint creation
    LOG_DIR="$HOME/.claude/logs"
    mkdir -p "$LOG_DIR"
    echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Created checkpoint: $STASH_NAME (session: $SESSION_ID)" \
        >> "$LOG_DIR/checkpoints.log"

    # Notify user
    cat << EOF
{
  "systemMessage": "✓ Checkpoint created: $STASH_NAME\n\nRestore with:\n  git stash list  # find the checkpoint\n  git stash apply stash@{N}  # restore it"
}
EOF
fi

exit 0
