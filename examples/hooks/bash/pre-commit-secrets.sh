#!/bin/bash
# pre-commit-secrets.sh - Pre-commit hook to detect secrets in staged files
# Version: 1.0.0
# Purpose: Prevent accidental commits of API keys, tokens, and credentials
#
# Installation:
#   cp examples/hooks/bash/pre-commit-secrets.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Test:
#   echo "GITHUB_TOKEN=ghp_test" > test.txt
#   git add test.txt
#   git commit -m "Test"
#   # Should fail with secret detection error

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Secret patterns (extended regex)
declare -A PATTERNS=(
    ["OpenAI API Key"]="sk-[A-Za-z0-9]{48}"
    ["GitHub Token (ghp)"]="ghp_[A-Za-z0-9]{36}"
    ["GitHub Token (gho)"]="gho_[A-Za-z0-9]{36}"
    ["GitHub Token (ghu)"]="ghu_[A-Za-z0-9]{36}"
    ["GitHub Token (ghs)"]="ghs_[A-Za-z0-9]{36}"
    ["GitHub Token (ghr)"]="ghr_[A-Za-z0-9]{36}"
    ["AWS Access Key"]="AKIA[A-Z0-9]{16}"
    ["AWS Secret Key"]="[A-Za-z0-9/+=]{40}"
    ["Anthropic API Key"]="sk-ant-[A-Za-z0-9-]{95,}"
    ["Generic API Key"]="api[_-]?key[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{20,}"
    ["Generic Secret"]="secret[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{20,}"
    ["Generic Token"]="token[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9]{20,}"
    ["Database URL with Password"]="(postgres|mysql|mongodb)://[^:]+:[^@]+@"
    ["Private Key"]="-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ["JWT Token"]="eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
)

# Whitelisted patterns (safe to ignore)
WHITELIST=(
    "your_token_here"
    "your_key_here"
    "example.com"
    "localhost"
    "placeholder"
    "XXXXXX"
    "\${env:"  # Template variable syntax
    "sk-ant-example"  # Example in documentation
)

# Files to always skip (even if staged)
SKIP_FILES=(
    "*.md"  # Documentation often contains example secrets
    "*.txt" # Same for text files
    "*example*"
    "*template*"
    "*.sample"
)

# Check if a file should be skipped
should_skip_file() {
    local file=$1
    for pattern in "${SKIP_FILES[@]}"; do
        # Convert glob to regex
        local regex="${pattern//\*/.*}"
        if [[ $file =~ $regex ]]; then
            return 0  # Skip this file
        fi
    done
    return 1  # Don't skip
}

# Check if a match is whitelisted
is_whitelisted() {
    local match=$1
    for whitelist in "${WHITELIST[@]}"; do
        if [[ $match == *"$whitelist"* ]]; then
            return 0  # Whitelisted
        fi
    done
    return 1  # Not whitelisted
}

# Main secret detection logic
detect_secrets() {
    local files
    files=$(git diff --cached --name-only --diff-filter=ACM)

    if [ -z "$files" ]; then
        exit 0  # No staged files
    fi

    local found_secrets=0
    local secrets_report=""

    # Iterate through staged files
    while IFS= read -r file; do
        # Skip if file should be ignored
        if should_skip_file "$file"; then
            continue
        fi

        # Skip if file doesn't exist (deleted)
        if [ ! -f "$file" ]; then
            continue
        fi

        # Get staged content
        local content
        content=$(git show ":$file" 2>/dev/null || continue)

        # Check each pattern
        for pattern_name in "${!PATTERNS[@]}"; do
            local pattern="${PATTERNS[$pattern_name]}"
            local matches
            matches=$(echo "$content" | grep -noE "$pattern" || true)

            if [ -n "$matches" ]; then
                # Check each match against whitelist
                while IFS= read -r match; do
                    local line_num="${match%%:*}"
                    local matched_text="${match#*:}"

                    if ! is_whitelisted "$matched_text"; then
                        found_secrets=1
                        secrets_report+="  ${file}:${line_num} - ${pattern_name}\n"
                        secrets_report+="    Content: ${matched_text:0:50}...\n"
                    fi
                done <<< "$matches"
            fi
        done
    done <<< "$files"

    # Report findings
    if [ $found_secrets -eq 1 ]; then
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}✗ COMMIT BLOCKED: Secrets detected in staged files${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${YELLOW}Found potential secrets:${NC}"
        echo -e "$secrets_report"
        echo ""
        echo -e "${YELLOW}Remediation steps:${NC}"
        echo "  1. Remove secrets from files"
        echo "  2. Use environment variables: \${env:VAR_NAME}"
        echo "  3. Store secrets in ~/.claude/.env (gitignored)"
        echo "  4. See: guide/ultimate-guide.md Section 8.3.1"
        echo ""
        echo -e "${YELLOW}If this is a false positive:${NC}"
        echo "  - Edit .git/hooks/pre-commit and add to WHITELIST array"
        echo "  - Or skip hook: git commit --no-verify (USE WITH CAUTION)"
        echo ""
        exit 1
    fi

    exit 0
}

# Run detection
detect_secrets
