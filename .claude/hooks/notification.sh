#!/bin/bash
# Notification hook (async) - Plays sound on notifications
# Usage: Called by Claude Code Notification hook

set -euo pipefail

# macOS notification sound
if [[ "$OSTYPE" == "darwin"* ]]; then
  # Play system sound (async, don't block if fails)
  afplay /System/Library/Sounds/Glass.aiff 2>/dev/null || true
fi

exit 0
