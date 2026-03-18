#!/bin/bash
# .claude/hooks/test-on-change.sh
# Event: PostToolUse
# Detects and runs associated tests after code changes
# Part of validation pipeline pattern

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only run after Edit/Write operations
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Skip if not a code file
if [[ ! "$FILE_PATH" =~ \.(ts|tsx|js|jsx|py|go|rs)$ ]]; then
    exit 0
fi

# Find associated test file
TEST_FILE=""
BASENAME=$(basename "$FILE_PATH" | sed 's/\.[^.]*$//')
DIRNAME=$(dirname "$FILE_PATH")

# Common test patterns
for pattern in "${BASENAME}.test.ts" "${BASENAME}.test.js" "${BASENAME}_test.py" "${BASENAME}_test.go"; do
    if [[ -f "$DIRNAME/$pattern" ]]; then
        TEST_FILE="$DIRNAME/$pattern"
        break
    fi
done

# Try adjacent __tests__ directory
if [[ -z "$TEST_FILE" ]]; then
    for pattern in "__tests__/${BASENAME}.test.ts" "__tests__/${BASENAME}.test.js"; do
        if [[ -f "$DIRNAME/$pattern" ]]; then
            TEST_FILE="$DIRNAME/$pattern"
            break
        fi
    done
fi

# If test file found, run it
if [[ -n "$TEST_FILE" ]]; then
    # Determine test runner
    if [[ -f "package.json" ]]; then
        TEST_CMD="npm test -- $TEST_FILE"
    elif [[ -f "pytest.ini" || -f "pyproject.toml" ]]; then
        TEST_CMD="pytest $TEST_FILE"
    elif [[ -f "go.mod" ]]; then
        TEST_CMD="go test $(dirname $TEST_FILE)"
    else
        exit 0
    fi

    # Run tests
    TEST_OUTPUT=$($TEST_CMD 2>&1 || true)

    # Check for failures
    if echo "$TEST_OUTPUT" | grep -qE "(FAIL|failed|error|Error)"; then
        cat << EOF
{
  "systemMessage": "⚠ Tests failed in $TEST_FILE:\n\n$TEST_OUTPUT\n\nFix implementation or update tests."
}
EOF
    fi
fi

exit 0
