#!/bin/bash
# Hook: PreToolUse - Block dangerous actions
# Exit 0 = allow, Exit 2 = block (stderr message shown to Claude)
#
# Place in: .claude/hooks/dangerous-actions-blocker.sh
# Register in: .claude/settings.json under PreToolUse event

set -e

# Read JSON from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# Canonicalize a path: resolve symlinks, "..", and duplicate slashes.
# Works when the leaf does not exist yet (Write creates new files): the
# deepest existing ancestor is resolved and the remainder re-attached.
canonicalize_path() {
    local target="$1"
    [[ -z "$target" ]] && return 0
    [[ "$target" != /* ]] && target="$(pwd)/$target"

    if command -v python3 >/dev/null 2>&1; then
        if python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$target" 2>/dev/null; then
            return 0
        fi
    fi

    # Fallback without python3: walk up to the deepest existing directory.
    local suffix="" probe="$target" resolved=""
    while [[ ! -d "$probe" && "$probe" != "/" && "$probe" != "." ]]; do
        suffix="/$(basename "$probe")$suffix"
        probe="$(dirname "$probe")"
    done
    resolved=$(cd -P "$probe" 2>/dev/null && pwd -P) || resolved="$probe"
    [[ "$resolved" == "/" ]] && resolved=""
    printf '%s\n' "${resolved}${suffix}"
}

# True when $1 is the same path as $2, or sits under it.
# Compares whole path segments, so /tmpfoo is not "inside" /tmp.
path_is_within() {
    local child="$1" parent="$2"
    [[ -z "$parent" || -z "$child" ]] && return 1
    parent="${parent%/}"
    if [[ -z "$parent" ]]; then
        [[ "$child" == /* ]]
        return
    fi
    [[ "$child" == "$parent" || "$child" == "$parent"/* ]]
}

# === BASH: Dangerous commands ===
if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')

    # Recursive delete aimed at a root target: /, /*, ~, $HOME.
    # An anchored regex is used instead of a substring test, otherwise
    # "rm -rf /" matches every absolute path and blocks legitimate
    # deletions such as /tmp/build or /Users/me/project/dist.
    # Tolerates flag order (-rf, -fr, -r -f, --recursive --force),
    # optional quotes around the target, and trailing whitespace.
    RM_ROOT_PATTERN='(^|[;&|(]|[[:space:]])[[:space:]]*rm([[:space:]]+(-[a-zA-Z]+|--[a-zA-Z-]+))*[[:space:]]+(-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)([[:space:]]+(-[a-zA-Z]+|--[a-zA-Z-]+))*[[:space:]]+['\''"]?(/|~|\$\{?HOME\}?)[*/]*['\''"]?[[:space:]]*($|[;&|])'

    if echo "$COMMAND" | grep -qE "$RM_ROOT_PATTERN"; then
        echo "BLOCKED: Recursive delete of a root target (/, /*, ~, \$HOME) detected" >&2
        exit 2
    fi

    # Dangerous patterns (literal substrings)
    DANGEROUS_PATTERNS=(
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
        if echo "$COMMAND" | grep -qi "$pattern"; then
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

    ALLOWED_ROOTS=("$PROJECT_DIR" "$CLAUDE_HOME" "/tmp")

    if [[ -n "$EXTRA_ALLOWED" ]]; then
        # Split without a here-string. `read -ra <<<` makes bash write a temp
        # file, so on a read-only or restricted TMPDIR the hook died with
        # "cannot create temp file for here document" and exited 1. Only exit 2
        # blocks a PreToolUse hook, so that failure mode let the write through
        # unchecked: a security control that fails open. Word splitting on IFS
        # needs no temp file. `set -f` stops a path containing * from globbing.
        _old_ifs=$IFS
        IFS=':'
        set -f
        # shellcheck disable=SC2206
        EXTRA_PATHS=($EXTRA_ALLOWED)
        set +f
        IFS=$_old_ifs
        for extra in "${EXTRA_PATHS[@]}"; do
            [[ -n "$extra" ]] && ALLOWED_ROOTS+=("$extra")
        done
    fi

    # A raw prefix test is bypassed by a symlink pointing outside the
    # allowed roots, and it wrongly rejects the reverse case (/tmp is a
    # symlink to /private/tmp on macOS). Both sides are canonicalized.
    REAL_FILE_PATH=$(canonicalize_path "$FILE_PATH")

    is_allowed=false
    for allowed_path in "${ALLOWED_ROOTS[@]}"; do
        real_allowed=$(canonicalize_path "$allowed_path")
        if path_is_within "$REAL_FILE_PATH" "$real_allowed"; then
            is_allowed=true
            break
        fi
    done

    if [[ "$is_allowed" == "false" ]]; then
        echo "BLOCKED: Editing outside project is forbidden: $FILE_PATH" >&2
        echo "Resolved to: $REAL_FILE_PATH" >&2
        echo "Allowed paths: $PROJECT_DIR, $CLAUDE_HOME, /tmp" >&2
        [[ -n "$EXTRA_ALLOWED" ]] && echo "Additional allowed: $EXTRA_ALLOWED" >&2
        exit 2
    fi
fi

# === DELETE: Always warn ===
if [[ "$TOOL_NAME" == "Bash" ]]; then
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')
    if echo "$COMMAND" | grep -qE "rm -r|rmdir|unlink"; then
        # Warning but not blocking (exit 0)
        echo '{"systemMessage": "Warning: File deletion detected. Verify this is intentional."}'
    fi
fi

# Allow by default
exit 0
