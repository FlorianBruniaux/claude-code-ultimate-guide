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

# Load protection patterns from .agentignore or .aiignore (project-level),
# falling back to ~/.agentignore for global home-directory protection
IGNORE_FILE=""
if [[ -f ".agentignore" ]]; then
    IGNORE_FILE=".agentignore"
elif [[ -f ".aiignore" ]]; then
    IGNORE_FILE=".aiignore"
elif [[ -f "$HOME/.agentignore" ]]; then
    IGNORE_FILE="$HOME/.agentignore"
fi

# Filename-only patterns — matched against basename to avoid false positives
# (e.g. prevents "dotenv.py" matching ".env" via full-path regex)
FILENAME_PATTERNS=(
    ".env"
    ".env.local"
    ".env.production"
    "*.key"
    "*.pem"
    "*.p12"
    "credentials.json"
    "secrets.yaml"
)

# Path-based patterns — matched as substrings of the full path
PATH_PATTERNS=(
    ".aws/credentials"
    ".ssh/id_"
    "config/secrets/"
)

# Check against patterns
is_protected() {
    local file="$1"
    local basename
    basename=$(basename "$file")

    # Check filename patterns against basename only
    for pattern in "${FILENAME_PATTERNS[@]}"; do
        [[ "$basename" == $pattern ]] && return 0
    done

    # Check path patterns as substrings of full path
    for pattern in "${PATH_PATTERNS[@]}"; do
        [[ "$file" == *"$pattern"* ]] && return 0
    done

    # Check ignore file patterns against basename (filename patterns)
    # and full path (path-based patterns like "config/secrets/")
    if [[ -n "$IGNORE_FILE" ]]; then
        while IFS= read -r pattern; do
            [[ "$pattern" =~ ^#.*$ || -z "$pattern" ]] && continue
            [[ "$basename" == $pattern ]] && return 0
            [[ "$file" == *"$pattern"* ]] && return 0
        done < "$IGNORE_FILE"
    fi

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
