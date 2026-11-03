#!/bin/bash
# =============================================================================
# Output Secrets Scanner Hook
# =============================================================================
# Event: PostToolUse (runs after each tool execution)
# Purpose: Detect secrets that might leak in tool outputs
#
# This complements security-check.sh (which scans inputs). This hook scans
# outputs to catch secrets that Claude might inadvertently expose.
#
# Installation:
#   Add to .claude/settings.json:
#   {
#     "hooks": {
#       "PostToolUse": [{
#         "matcher": "",
#         "hooks": ["bash examples/hooks/bash/output-secrets-scanner.sh"]
#       }]
#     }
#   }
#
# What it detects:
#   - API keys (OpenAI, Anthropic, AWS, GCP, Azure, Stripe, etc.)
#   - Private keys and certificates
#   - Database connection strings with passwords
#   - GitHub/GitLab tokens
#   - JWT tokens
# =============================================================================

set -euo pipefail

# Read the hook input from stdin
INPUT=$(cat)

# Extract tool output from JSON (handle both formats)
TOOL_OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // .output // ""' 2>/dev/null || echo "")

# If no output or empty, exit cleanly
if [[ -z "$TOOL_OUTPUT" ]]; then
    exit 0
fi

# Secret patterns to detect
# Bash 3.2 compatible (macOS /bin/bash has no associative arrays): each entry
# is "name::value", split with ${entry%%::*} and ${entry#*::}.
SECRET_PATTERNS=(
    # API Keys
    "OpenAI API Key::sk-[a-zA-Z0-9]{20,}"
    "Anthropic API Key::sk-ant-[a-zA-Z0-9]{20,}"
    "AWS Access Key::AKIA[0-9A-Z]{16}"
    "AWS Secret Key::[0-9a-zA-Z/+]{40}"
    "GCP API Key::AIza[0-9A-Za-z_-]{35}"
    "Azure Key::[a-zA-Z0-9]{32,}"
    "Stripe Key::(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}"
    "Twilio Key::SK[a-f0-9]{32}"
    "SendGrid Key::SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}"
    "Slack Token::xox[baprs]-[0-9a-zA-Z-]{10,}"
    "Discord Token::[MN][A-Za-z0-9]{23,}\.[A-Za-z0-9-_]{6}\.[A-Za-z0-9-_]{27}"

    # Tokens
    "GitHub Token::(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}"
    "GitLab Token::glpat-[a-zA-Z0-9_-]{20,}"
    "NPM Token::npm_[a-zA-Z0-9]{36}"
    "PyPI Token::pypi-[a-zA-Z0-9_-]{50,}"
    "JWT Token::eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*"
    "Heroku API Key::[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"

    # Private Keys
    "Private Key::-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
    "PGP Private Key::-----BEGIN PGP PRIVATE KEY BLOCK-----"

    # Database
    "Database URL with Password::(postgres|mysql|mongodb)://[^:]+:[^@]+@"
    "Redis URL with Password::redis://:[^@]+@"

    # Generic (58% of leaked secrets are "generic" - GitGuardian 2025)
    "Generic API Key::(api[_-]?key|apikey|api[_-]?secret)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}"
    "Generic Secret::(secret|password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s'\"]{8,}"
    "Generic Token::(token|auth[_-]?token|access[_-]?token|bearer)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}"
    "Private Key Inline::['\"]?-----BEGIN[^-]+PRIVATE KEY-----"

    # Environment Variable Leakage
    "Env Dump Command::^(env|printenv|set)$"
    "Proc Environ Access::/proc/self/environ|/proc/[0-9]+/environ"
)

DETECTED_SECRETS=()
SCAN_ERRORS=()

# Check each pattern
for entry in "${SECRET_PATTERNS[@]}"; do
    secret_type="${entry%%::*}"
    pattern="${entry#*::}"
    # -e keeps a pattern that starts with "-" (private key header) from being
    # parsed as an option. grep exits 1 for "no match" and 2 for an error.
    if echo "$TOOL_OUTPUT" | grep -qiE -e "$pattern" 2>/dev/null; then
        DETECTED_SECRETS+=("$secret_type")
    elif [[ ${PIPESTATUS[1]} -gt 1 ]]; then
        SCAN_ERRORS+=("$secret_type")
    fi
done

# A pattern that grep could not run is not "no secret": say so
if [[ ${#SCAN_ERRORS[@]} -gt 0 ]]; then
    SCAN_ERRORS_LIST=$(printf ", %s" "${SCAN_ERRORS[@]}")
    echo "output-secrets-scanner: grep failed on pattern(s) ${SCAN_ERRORS_LIST:2}: output not fully scanned" >&2
    echo "{\"systemMessage\": \"SECRET SCAN INCOMPLETE: grep failed on ${#SCAN_ERRORS[@]} pattern(s), output not fully scanned.\"}"
fi

# If secrets detected, warn via systemMessage
if [[ ${#DETECTED_SECRETS[@]} -gt 0 ]]; then
    SECRETS_LIST=$(printf ", %s" "${DETECTED_SECRETS[@]}")
    SECRETS_LIST=${SECRETS_LIST:2}  # Remove leading ", "

    WARNING_MSG="SECRET LEAK WARNING: Potential secrets detected in output: $SECRETS_LIST. Do NOT commit or share this output. Consider using environment variables or a secrets manager."

    echo "{\"systemMessage\": \"$WARNING_MSG\"}"
fi

# Always exit 0 (warn, don't block)
exit 0
