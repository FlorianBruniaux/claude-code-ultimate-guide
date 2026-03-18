#!/bin/bash
# .claude/hooks/typecheck-on-save.sh
# Event: PostToolUse
# Runs TypeScript compiler on changed files after edits
# Part of validation pipeline pattern

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only run after Edit/Write operations
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Only check TypeScript files
if [[ ! "$FILE_PATH" =~ \.(ts|tsx)$ ]]; then
    exit 0
fi

# Check if tsconfig exists
if [[ ! -f "tsconfig.json" ]]; then
    exit 0
fi

# Run tsc on the specific file (noEmit mode)
TSC_OUTPUT=$(npx tsc --noEmit "$FILE_PATH" 2>&1 || true)

# Check if there are errors (not just warnings)
if echo "$TSC_OUTPUT" | grep -q "error TS"; then
    cat << EOF
{
  "systemMessage": "⚠ TypeScript errors in $FILE_PATH:\n\n$TSC_OUTPUT\n\nFix these before proceeding."
}
EOF
fi

exit 0
