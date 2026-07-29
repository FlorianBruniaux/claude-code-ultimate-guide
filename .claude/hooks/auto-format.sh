#!/bin/bash
# Auto-format hook (async) - Runs Prettier after Edit/Write
# Usage: Called by Claude Code PostToolUse hook

set -euo pipefail

# Get file path from environment variable
FILE_PATH="${CLAUDE_FILE_PATH:-}"

if [ -z "$FILE_PATH" ]; then
  echo "❌ [auto-format] No file path provided" >&2
  exit 0
fi

# Only format certain file types
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.md|*.yml|*.yaml)
    # Check if prettier is available
    if command -v pnpm >/dev/null 2>&1; then
      pnpm prettier --write "$FILE_PATH" >/dev/null 2>&1 || true
      echo "✨ [auto-format] Formatted: $FILE_PATH" >&2
    elif command -v npx >/dev/null 2>&1; then
      npx -y prettier --write "$FILE_PATH" >/dev/null 2>&1 || true
      echo "✨ [auto-format] Formatted: $FILE_PATH" >&2
    fi
    ;;
  *)
    # Not a formattable file, skip silently
    ;;
esac

exit 0
