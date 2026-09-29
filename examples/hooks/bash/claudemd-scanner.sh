#!/bin/bash
# =============================================================================
# CLAUDE.md Injection Scanner Hook
# =============================================================================
# Event: SessionStart (runs when Claude Code session begins)
# Purpose: Detect potential prompt injection attacks in CLAUDE.md files
#
# Installation:
#   Add to .claude/settings.json:
#   {
#     "hooks": {
#       "SessionStart": [{
#         "matcher": "",
#         "hooks": ["bash examples/hooks/bash/claudemd-scanner.sh"]
#       }]
#     }
#   }
#
# What it detects:
#   - "ignore previous instructions" patterns (common injection technique)
#   - Shell command execution attempts (curl|bash, wget|sh, eval)
#   - Base64 encoded content (potential obfuscation)
#   - Suspicious HTML comments that might hide instructions
# =============================================================================

set -euo pipefail

# Define suspicious patterns (case-insensitive)
SUSPICIOUS_PATTERNS=(
    "ignore.*previous.*instruction"
    "ignore.*all.*instruction"
    "disregard.*instruction"
    "forget.*instruction"
    "new.*instruction.*follow"
    "curl.*\|.*bash"
    "curl.*\|.*sh"
    "wget.*\|.*bash"
    "wget.*\|.*sh"
    "eval\s*\("
    "base64.*decode"
    "\$\(.*curl"
    "\$\(.*wget"
    "<!--.*ignore"
    "<!--.*instruction"
)

WARNINGS=()

# Function to scan a file for suspicious patterns
scan_file() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        return 0
    fi

    for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
        if grep -qiE "$pattern" "$file" 2>/dev/null; then
            WARNINGS+=("Suspicious pattern in $file: matches '$pattern'")
        fi
    done

    # Check for very long single lines (potential obfuscation)
    if awk 'length > 500' "$file" | grep -q .; then
        WARNINGS+=("Warning: $file contains very long lines (potential obfuscation)")
    fi

    # Check for uncommon Unicode characters (potential homoglyph attack)
    # LC_ALL=C makes the range byte-wise, so any byte >= 0x80 (part of a multibyte
    # character) counts as non-ASCII. Portable: BSD grep has no -P.
    if LC_ALL=C grep $'[\x80-\xff]' "$file" 2>/dev/null | grep -qiE "instruction|ignore|run|execute"; then
        WARNINGS+=("Warning: $file contains non-ASCII characters near sensitive keywords")
    fi
}

# Scan all potential CLAUDE.md locations
scan_file "CLAUDE.md"
scan_file ".claude/CLAUDE.md"

# Also scan any .md files in .claude/ directory that might be loaded
if [[ -d ".claude" ]]; then
    for md_file in .claude/*.md; do
        [[ -f "$md_file" ]] && scan_file "$md_file"
    done
fi

# Output warnings if any found
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    # Construct JSON response with system message
    WARNING_TEXT="SECURITY WARNING - Suspicious content detected:\\n"
    for warning in "${WARNINGS[@]}"; do
        WARNING_TEXT+="- $warning\\n"
    done
    WARNING_TEXT+="\\nReview these files before proceeding. See: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/guide/ultimate-guide.md#security-warning-claudemd-injection"

    echo "{\"systemMessage\": \"$WARNING_TEXT\"}"
fi

# Always exit 0 to not block session (just warn)
exit 0
