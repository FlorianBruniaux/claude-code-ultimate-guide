#!/bin/bash
# =============================================================================
# Repository Integrity Scanner Hook
# =============================================================================
# Event: PreToolUse (runs before Read on potentially malicious files)
# Note: files attached with @ in a prompt are inserted without a Read call, so this
# hook does not see them (use a Read deny rule for those paths)
# Purpose: Scan repository files for injection vectors before processing
#
# This hook detects prompt injection attempts hidden in:
#   - README.md, SECURITY.md (hidden HTML comments)
#   - package.json, pyproject.toml (malicious scripts)
#   - .claude/, .cursor/ configs (tampered configurations)
#   - CONTRIBUTING.md (social engineering instructions)
#
# Installation:
#   Add to .claude/settings.json:
#   {
#     "hooks": {
#       "PreToolUse": [{
#         "matcher": "Read",
#         "hooks": [{ "type": "command", "command": "bash examples/hooks/bash/repo-integrity-scanner.sh" }]
#       }]
#     }
#   }
#
# Exit codes:
#   0 = allow (safe or not a target file)
#   2 = block (injection detected)
#
# References:
#   - CVE-2025-54135: RCE via config file rewriting
#   - CVE-2025-54136: Team backdoor via post-approval config tampering
# =============================================================================

set -euo pipefail

# Read the hook input from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input // empty')

# Only check Read operations
[[ "$TOOL_NAME" != "Read" ]] && exit 0

FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')
[[ -z "$FILE_PATH" ]] && exit 0

# Check if file exists
[[ ! -f "$FILE_PATH" ]] && exit 0

FILENAME=$(basename "$FILE_PATH")
DIRNAME=$(dirname "$FILE_PATH")

# === HIGH-RISK FILES ===
# These files are common injection vectors
HIGH_RISK_FILES=(
    "README.md"
    "readme.md"
    "SECURITY.md"
    "CONTRIBUTING.md"
    "CHANGELOG.md"
)

# === CONFIG FILES ===
# Configuration files that could contain malicious settings
CONFIG_FILES=(
    "package.json"
    "pyproject.toml"
    "setup.py"
    "setup.cfg"
    "Makefile"
    ".pre-commit-config.yaml"
)

# === CLAUDE/CURSOR CONFIG ===
# IDE config files that could be tampered
IDE_CONFIG_PATTERNS=(
    ".claude"
    ".cursor"
    ".vscode"
    ".idea"
)

# Function to check for injection patterns
check_injection_patterns() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    # === HIDDEN HTML COMMENTS ===
    # Look for HTML comments with instruction-like content
    if echo "$content" | grep -qiE '<!--.*\b(ignore|override|system|execute|run|eval|inject)\b.*-->'; then
        echo "BLOCKED: Hidden HTML comment with suspicious instructions in: $file" >&2
        return 1
    fi

    # === ROLE OVERRIDE PATTERNS ===
    if echo "$content" | grep -qiE 'ignore (previous|all|your) instructions|you are now|pretend (you are|to be)|from now on|new instructions:'; then
        echo "BLOCKED: Prompt injection pattern detected in: $file" >&2
        return 1
    fi

    # === BASE64 IN COMMENTS ===
    # Long base64 strings in comments could be encoded instructions
    if echo "$content" | grep -qE '(#|//|<!--).*[A-Za-z0-9+/]{40,}={0,2}'; then
        # Try to decode and check for injection
        local encoded
        encoded=$(echo "$content" | grep -oE '[A-Za-z0-9+/]{40,}={0,2}' | head -1)
        local decoded
        decoded=$(echo "$encoded" | base64 -d 2>/dev/null || echo "")
        if echo "$decoded" | grep -qiE 'ignore|override|system|jailbreak'; then
            echo "BLOCKED: Base64-encoded injection detected in: $file" >&2
            return 1
        fi
    fi

    return 0
}

# Function to check package.json for suspicious scripts
check_package_json() {
    local file="$1"

    # Extract scripts section
    local scripts
    scripts=$(jq -r '.scripts // {} | to_entries[] | "\(.key): \(.value)"' "$file" 2>/dev/null || echo "")

    # Suspicious script patterns
    SUSPICIOUS_PATTERNS=(
        "curl.*|.*bash"
        "wget.*|.*sh"
        "eval\("
        "base64.*-d"
        "nc -"
        "reverse.*shell"
        "/dev/tcp/"
        "\\$\\(.*\\)"  # Command substitution
    )

    for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
        if echo "$scripts" | grep -qiE "$pattern"; then
            echo "BLOCKED: Suspicious npm script detected in $file: pattern '$pattern'" >&2
            return 1
        fi
    done

    return 0
}

# Function to check Python setup files
check_python_setup() {
    local file="$1"
    local content
    content=$(cat "$file" 2>/dev/null || echo "")

    # Suspicious patterns in setup files
    if echo "$content" | grep -qiE 'os\.system|subprocess\.(run|call|Popen)|exec\(|eval\(|__import__.*os'; then
        # Warning only - these could be legitimate
        echo '{"systemMessage": "Warning: Python setup file contains code execution patterns. Verify legitimacy before installing."}'
    fi

    return 0
}

# === MAIN CHECKS ===

# Check high-risk markdown files
for risk_file in "${HIGH_RISK_FILES[@]}"; do
    if [[ "$FILENAME" == "$risk_file" ]]; then
        check_injection_patterns "$FILE_PATH" || exit 2
        break
    fi
done

# Check config files
for config_file in "${CONFIG_FILES[@]}"; do
    if [[ "$FILENAME" == "$config_file" ]]; then
        case "$FILENAME" in
            package.json)
                check_package_json "$FILE_PATH" || exit 2
                ;;
            pyproject.toml|setup.py|setup.cfg)
                check_python_setup "$FILE_PATH" || exit 2
                ;;
            Makefile)
                check_injection_patterns "$FILE_PATH" || exit 2
                ;;
        esac
        break
    fi
done

# Check IDE config directories
for ide_pattern in "${IDE_CONFIG_PATTERNS[@]}"; do
    if [[ "$DIRNAME" == *"$ide_pattern"* || "$FILE_PATH" == *"$ide_pattern"* ]]; then
        # Extra scrutiny for IDE configs
        check_injection_patterns "$FILE_PATH" || exit 2

        # Check for suspicious config modifications
        if [[ "$FILENAME" == *.json ]]; then
            # (no `local`: this block runs at top level, outside any function)
            content=$(cat "$FILE_PATH" 2>/dev/null || echo "")

            # Look for hooks pointing to external URLs or suspicious commands
            if echo "$content" | grep -qiE '"hooks".*"(curl|wget|bash|sh|nc|python|node)'; then
                echo "BLOCKED: Suspicious hook command in IDE config: $FILE_PATH" >&2
                exit 2
            fi
        fi
        break
    fi
done

# All checks passed
exit 0
