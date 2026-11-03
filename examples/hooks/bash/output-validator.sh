#!/bin/bash
# Hook: PostToolUse - Validate Claude's outputs for quality issues
# Exit 0 = allow (always), but emit systemMessage warnings
#
# This hook performs heuristic validation of Claude's outputs to detect:
# - Potential hallucinations (fabricated paths, functions)
# - Sensitive data leakage in outputs
# - High uncertainty indicators
#
# This is a lightweight heuristic check, not a full LLM evaluation.
# For deeper validation, use the output-evaluator agent.
#
# Place in: .claude/hooks/output-validator.sh
# Register in: .claude/settings.json under PostToolUse event

set -e

# Read JSON from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // empty')

# Only validate tools that produce code/content outputs
case "$TOOL_NAME" in
    Edit|Write|Bash)
        ;;
    *)
        exit 0
        ;;
esac

WARNINGS=()

# === FABRICATED FILE PATHS ===
# Detect paths that look suspicious (common hallucination patterns)
SUSPICIOUS_PATHS=(
    "/path/to/"
    "/your/project/"
    "/example/"
    "/foo/bar/"
    "/my/app/"
    "/user/project/"
    "C:\\Users\\User\\"
    "C:\\path\\to\\"
)

for pattern in "${SUSPICIOUS_PATHS[@]}"; do
    if [[ "$TOOL_OUTPUT" == *"$pattern"* ]]; then
        WARNINGS+=("Suspicious placeholder path detected: '$pattern'")
    fi
done

# === PLACEHOLDER CONTENT ===
# Detect common placeholder patterns that shouldn't be in production code
PLACEHOLDER_PATTERNS=(
    "TODO:"
    "FIXME:"
    "XXX:"
    "HACK:"
    "your-api-key"
    "your_api_key"
    "YOUR_API_KEY"
    "sk-..."
    "pk_test_"
    "pk_live_"
    "api_key_here"
    "replace_with"
    "insert_your"
    "placeholder"
    "example.com"
    "foo@bar.com"
    "test@test.com"
)

for pattern in "${PLACEHOLDER_PATTERNS[@]}"; do
    if [[ "$TOOL_OUTPUT" == *"$pattern"* ]]; then
        WARNINGS+=("Placeholder content detected: '$pattern'")
    fi
done

# === SENSITIVE DATA LEAKAGE ===
# Detect potential secrets in output (could indicate data exposure)
SECRET_PATTERNS=(
    # AWS
    'AKIA[0-9A-Z]{16}'
    # Generic API keys (long hex strings)
    '[a-f0-9]{32,}'
    # Private keys
    '-----BEGIN.*PRIVATE KEY-----'
    '-----BEGIN RSA'
    '-----BEGIN EC'
    # JWT tokens
    'eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.'
    # Password patterns
    'password["\x27]?\s*[=:]\s*["\x27][^"\x27]{8,}'
)

for pattern in "${SECRET_PATTERNS[@]}"; do
    # -e keeps a pattern that starts with "-" (private key header) from being
    # parsed as an option. grep exits 1 for "no match" and 2 for an error.
    if echo "$TOOL_OUTPUT" | grep -qE -e "$pattern" 2>/dev/null; then
        WARNINGS+=("Potential sensitive data in output (pattern: ${pattern:0:20}...)")
    elif [[ ${PIPESTATUS[1]} -gt 1 ]]; then
        WARNINGS+=("Secret scan failed (grep error) for pattern: ${pattern:0:20}...")
    fi
done

# === UNCERTAINTY INDICATORS ===
# Detect high uncertainty language that might indicate guessing
UNCERTAINTY_PATTERNS=(
    "I'm not sure"
    "I think it might"
    "probably"
    "possibly"
    "might be"
    "could be"
    "I believe"
    "I assume"
    "I guess"
    "if I recall"
    "from memory"
    "I don't have access"
    "I cannot verify"
)

UNCERTAINTY_COUNT=0
TOOL_OUTPUT_LOWER=$(echo "$TOOL_OUTPUT" | tr '[:upper:]' '[:lower:]')

for pattern in "${UNCERTAINTY_PATTERNS[@]}"; do
    pattern_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
    if [[ "$TOOL_OUTPUT_LOWER" == *"$pattern_lower"* ]]; then
        ((UNCERTAINTY_COUNT++))
    fi
done

if [[ $UNCERTAINTY_COUNT -ge 3 ]]; then
    WARNINGS+=("High uncertainty detected ($UNCERTAINTY_COUNT indicators) - verify output accuracy")
fi

# === INCOMPLETE IMPLEMENTATIONS ===
# Detect code that looks incomplete
INCOMPLETE_PATTERNS=(
    "not implemented"
    "NotImplementedError"
    "throw new Error.*implement"
    "// TODO"
    "# TODO"
    "pass  # "
    "raise NotImplemented"
    "undefined"
)

for pattern in "${INCOMPLETE_PATTERNS[@]}"; do
    if echo "$TOOL_OUTPUT" | grep -qiE "$pattern" 2>/dev/null; then
        WARNINGS+=("Incomplete implementation detected: '$pattern'")
    fi
done

# === HALLUCINATION INDICATORS ===
# Detect patterns that often indicate hallucinated content
HALLUCINATION_PATTERNS=(
    "According to the documentation"
    "As stated in"
    "The official guide says"
    "Based on the API reference"
)

for pattern in "${HALLUCINATION_PATTERNS[@]}"; do
    if [[ "$TOOL_OUTPUT" == *"$pattern"* ]]; then
        WARNINGS+=("Unverified reference claim: '$pattern' - verify source")
    fi
done

# === OUTPUT WARNINGS ===
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    WARNING_MSG="Output validation warnings:\\n"
    for warn in "${WARNINGS[@]}"; do
        WARNING_MSG+="  - $warn\\n"
    done
    WARNING_MSG+="\\nReview output carefully before accepting."

    # Emit as systemMessage (warning, not blocking)
    echo "{\"systemMessage\": \"$WARNING_MSG\"}"
fi

# Always allow (this hook warns, doesn't block)
exit 0
