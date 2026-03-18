#!/bin/bash
# .claude/hooks/file-guard.sh
# Event: PreToolUse
# Unified file protection with pattern matching and bash bypass detection
# Prevents Claude from reading/writing protected files

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Only check file operations
if [[ "$TOOL_NAME" != "Read" && "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Load protection patterns from .agentignore or .aiignore
IGNORE_FILE=""
if [[ -f ".agentignore" ]]; then
    IGNORE_FILE=".agentignore"
elif [[ -f ".aiignore" ]]; then
    IGNORE_FILE=".aiignore"
fi

# Default critical patterns (if no ignore file)
CRITICAL_PATTERNS=(
    ".env"
    ".env.local"
    ".env.production"
    "*.key"
    "*.pem"
    "*.p12"
    "credentials.json"
    "secrets.yaml"
    "config/secrets/*"
    ".aws/credentials"
    ".ssh/id_*"
)

# Check against patterns
is_protected() {
    local file="$1"

    # Check ignore file patterns
    if [[ -n "$IGNORE_FILE" ]]; then
        while IFS= read -r pattern; do
            # Skip comments and empty lines
            [[ "$pattern" =~ ^#.*$ || -z "$pattern" ]] && continue

            # Convert gitignore pattern to bash glob
            if [[ "$file" == $pattern || "$file" =~ $pattern ]]; then
                return 0
            fi
        done < "$IGNORE_FILE"
    fi

    # Check critical patterns
    for pattern in "${CRITICAL_PATTERNS[@]}"; do
        if [[ "$file" == $pattern || "$file" =~ $pattern ]]; then
            return 0
        fi
    done

    return 1
}

# Detect bash variable expansion bypass attempts
detect_bypass() {
    local file="$1"

    # Check for variable expansion patterns
    if [[ "$file" =~ \$\{?[A-Za-z_][A-Za-z0-9_]*\}? ]]; then
        return 0
    fi

    # Check for command substitution
    if [[ "$file" =~ \$\( || "$file" =~ \` ]]; then
        return 0
    fi

    return 1
}

# Validate file path
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Check for bypass attempts
if detect_bypass "$FILE_PATH"; then
    cat << EOF
{
  "block": true,
  "systemMessage": "⛔ File access blocked: Variable expansion detected in path\n\nPath: $FILE_PATH\n\nThis looks like a bypass attempt. Use literal paths only."
}
EOF
    exit 1
fi

# Check protection patterns
if is_protected "$FILE_PATH"; then
    cat << EOF
{
  "block": true,
  "systemMessage": "⛔ File access blocked: Protected file\n\nPath: $FILE_PATH\n\nThis file is protected by .agentignore or security policy.\nTo access it, remove from ignore file and confirm manually."
}
EOF
    exit 1
fi

exit 0
