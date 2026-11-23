#!/bin/bash
# .claude/hooks/typecheck-on-save.sh
# Event: PostToolUse (matcher "Edit|Write")
# Runs TypeScript compiler on changed files after edits
# Part of validation pipeline pattern
#
# On errors the hook prints {"decision": "block", "reason": ...}. For PostToolUse the
# tool already ran, so this adds the reason next to the tool result so Claude sees
# the compiler output. A systemMessage would only be shown to the user.
# Note: `tsc --noEmit <file>` ignores tsconfig.json compiler options; for a
# project-wide check run `npx tsc --noEmit -p tsconfig.json` instead.

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
    jq -n --arg file "$FILE_PATH" --arg out "$TSC_OUTPUT" \
        '{decision: "block", reason: ("TypeScript errors in " + $file + ":\n\n" + $out + "\n\nFix these before proceeding.")}'
fi

exit 0
