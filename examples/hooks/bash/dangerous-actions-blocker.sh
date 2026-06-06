#!/bin/bash
# Hook: PreToolUse - Block dangerous actions
# Exit 0 = allow, Exit 2 = block (stderr message shown to Claude)
#
# Place in: .claude/hooks/dangerous-actions-blocker.sh
# Register in: .claude/settings.json under PreToolUse event

set -euo pipefail

# Read JSON from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# === BASH: Dangerous commands ===
if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')

    # Dangerous patterns
    DANGEROUS_PATTERNS=(
        "rm -rf /"
        "rm -rf ~"
        "rm -rf \$HOME"
        "dd if="
        "mkfs"
        ":(){:|:&};:"          # Fork bomb
        "> /dev/sda"
        "chmod -R 777 /"
        "chown -R"
        "sudo rm"
        "DROP DATABASE"
        "DROP TABLE"
        "--no-preserve-root"
    )

    for pattern in "${DANGEROUS_PATTERNS[@]}"; do
        if [[ "$COMMAND" == *"$pattern"* ]]; then
            echo "BLOCKED: Dangerous command detected: '$pattern'" >&2
            exit 2
        fi
    done

    # Block force push to main/master
    if echo "$COMMAND" | grep -qE "git push.*(-f|--force).*(main|master)"; then
        echo "BLOCKED: Force push to main/master is forbidden" >&2
        exit 2
    fi

    # Block npm publish without confirmation
    if echo "$COMMAND" | grep -qE "npm publish|pnpm publish|yarn publish"; then
        echo "BLOCKED: Package publication requires manual confirmation" >&2
        exit 2
    fi

    # Block bash commands that reference credential files
    CREDENTIAL_FILE_PATTERNS=(
        ".env"
        ".env.local"
        ".env.production"
        ".aws/credentials"
        ".ssh/id_rsa"
        ".ssh/id_ed25519"
        ".ssh/id_ecdsa"
        "credentials.json"
        "serviceAccountKey.json"
        "secrets.yaml"
        "secrets.yml"
    )

    for cred in "${CREDENTIAL_FILE_PATTERNS[@]}"; do
        cred_regex=$(printf '%s' "$cred" | sed 's/\./\\./g')
        if echo "$COMMAND" | grep -qP "${cred_regex}(?![a-zA-Z0-9._-])"; then
            echo "BLOCKED: Command references credential file: '$cred'" >&2
            exit 2
        fi
    done

    # Check for potential secrets in command
    SECRET_PATTERNS=(
        "password="
        "secret="
        "api_key="
        "apikey="
        "token="
        "aws_access_key"
        "aws_secret"
        "private_key"
    )

    for pattern in "${SECRET_PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -qiF "$pattern"; then
            echo "BLOCKED: Potential secret detected in command: '$pattern'" >&2
            exit 2
        fi
    done
fi

# === EDIT/WRITE: Sensitive files ===
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
    FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')

    # Protected files
    PROTECTED_FILES=(
        ".env"
        ".env.local"
        ".env.production"
        ".env.development"
        "credentials.json"
        "serviceAccountKey.json"
        "id_rsa"
        "id_ed25519"
        "id_ecdsa"
        ".npmrc"
        ".pypirc"
        "secrets.yml"
        "secrets.yaml"
    )

    FILENAME=$(basename "$FILE_PATH")
    for protected in "${PROTECTED_FILES[@]}"; do
        if [[ "$FILENAME" == "$protected" ]]; then
            echo "BLOCKED: Editing sensitive file '$FILENAME' is forbidden" >&2
            exit 2
        fi
    done

    # Block editing outside project (with configurable exceptions)
    PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
    CLAUDE_HOME="${HOME}/.claude"

    # Allowed paths (configurable via environment variable)
    # Format: colon-separated paths - e.g., ALLOWED_PATHS="/custom/path:/other/path"
    EXTRA_ALLOWED="${ALLOWED_PATHS:-}"

    # Check if path is allowed
    is_allowed=false

    # Current project
    [[ "$FILE_PATH" == "$PROJECT_DIR"* ]] && is_allowed=true

    # Claude Code directory (~/.claude/) - plans, logs, settings
    [[ "$FILE_PATH" == "$CLAUDE_HOME"* ]] && is_allowed=true

    # Temporary files
    [[ "$FILE_PATH" == "/tmp"* ]] && is_allowed=true

    # Additional configured paths
    if [[ -n "$EXTRA_ALLOWED" ]]; then
        IFS=':' read -ra EXTRA_PATHS <<< "$EXTRA_ALLOWED"
        for allowed_path in "${EXTRA_PATHS[@]}"; do
            [[ "$FILE_PATH" == "$allowed_path"* ]] && is_allowed=true
        done
    fi

    if [[ "$is_allowed" == "false" ]]; then
        echo "BLOCKED: Editing outside project is forbidden: $FILE_PATH" >&2
        echo "Allowed paths: $PROJECT_DIR, $CLAUDE_HOME, /tmp" >&2
        [[ -n "$EXTRA_ALLOWED" ]] && echo "Additional allowed: $EXTRA_ALLOWED" >&2
        exit 2
    fi
fi

# === DELETE: Always warn ===
if [[ "$TOOL_NAME" == "Bash" ]]; then
    if echo "$COMMAND" | grep -qE "rm -r|rmdir|unlink"; then
        # Warning but not blocking (exit 0)
        echo '{"systemMessage": "Warning: File deletion detected. Verify this is intentional."}'
    fi
fi

# Allow by default
exit 0
