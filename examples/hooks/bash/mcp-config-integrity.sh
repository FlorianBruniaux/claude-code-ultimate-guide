#!/bin/bash
# =============================================================================
# MCP Config Integrity Hook
# =============================================================================
# Event: SessionStart (runs when Claude Code session begins)
# Purpose: Verify MCP configuration has not been tampered with
#
# This hook addresses CVE-2025-54135 and CVE-2025-54136 by:
#   - Computing hash of ~/.claude.json (MCP config location)
#   - Comparing against stored baseline
#   - Alerting on unauthorized modifications
#   - Checking project-level .mcp.json for suspicious content
#
# Installation:
#   Add to .claude/settings.json:
#   {
#     "hooks": {
#       "SessionStart": [{
#         "matcher": "startup",
#         "hooks": [{ "type": "command", "command": "bash examples/hooks/bash/mcp-config-integrity.sh" }]
#       }]
#     }
#   }
#
# Initial setup (run once to create baseline):
#   shasum -a 256 ~/.claude.json > ~/.claude/.mcp-baseline.sha256   # macOS
#   sha256sum ~/.claude.json > ~/.claude/.mcp-baseline.sha256       # Linux
#
# Exit codes:
#   0 = allow (config unchanged or no baseline)
#   Findings are printed as a systemMessage (shown to the user)
#
# References:
#   - CVE-2025-54135: RCE in Cursor via prompt injection rewriting mcp.json
#   - CVE-2025-54136: Persistent team backdoor via post-approval config tampering
# =============================================================================

set -euo pipefail

# Configuration paths
MCP_CONFIG="${HOME}/.claude.json"
MCP_BASELINE="${HOME}/.claude/.mcp-baseline.sha256"
PROJECT_MCP=".mcp.json"

WARNINGS=()

# macOS ships shasum, not sha256sum
sha256_of() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" 2>/dev/null | awk '{print $1}'
    else
        shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'
    fi
}

# === GLOBAL MCP CONFIG CHECK ===
if [[ -f "$MCP_CONFIG" ]]; then
    # Check if baseline exists
    if [[ -f "$MCP_BASELINE" ]]; then
        # Compute current hash
        CURRENT_HASH=$(sha256_of "$MCP_CONFIG")
        BASELINE_HASH=$(awk '{print $1}' "$MCP_BASELINE" 2>/dev/null || echo "")

        if [[ -n "$CURRENT_HASH" && -n "$BASELINE_HASH" && "$CURRENT_HASH" != "$BASELINE_HASH" ]]; then
            WARNINGS+=("MCP config modified since baseline was created. Review ~/.claude.json for unauthorized changes. Re-run the baseline command (shasum -a 256 or sha256sum on ~/.claude.json) to update baseline if changes are legitimate.")
        fi
    else
        # No baseline - suggest creating one
        WARNINGS+=("No MCP config baseline found. Create one with: shasum -a 256 ~/.claude.json > ~/.claude/.mcp-baseline.sha256 (sha256sum on Linux)")
    fi

    # === CHECK FOR SUSPICIOUS MCP SERVERS ===
    # Look for known risky patterns
    MCP_CONTENT=$(cat "$MCP_CONFIG" 2>/dev/null || echo "{}")

    # Check for dangerous flags
    if echo "$MCP_CONTENT" | grep -qiE '"--dangerous|"--allow-write|"--no-sandbox'; then
        WARNINGS+=("MCP config contains dangerous flags (--dangerous, --allow-write, or --no-sandbox). Review carefully.")
    fi

    # Check for unpinned versions (using @latest or no version)
    if echo "$MCP_CONTENT" | grep -qE '"[^"]*@latest"|"npx"[^}]*"-y"[^}]*"[^@"]+\"'; then
        WARNINGS+=("MCP config may contain unpinned versions (@latest or missing version). Pin to specific versions for security.")
    fi

    # Check for suspicious environment variables
    if echo "$MCP_CONTENT" | grep -qiE '"env"[^}]*"(PASSWORD|SECRET|TOKEN|API_KEY|PRIVATE_KEY)"'; then
        WARNINGS+=("MCP config contains potentially sensitive environment variables. Ensure these are not hardcoded secrets.")
    fi

    # Check for external URLs in commands
    # (the filter must sit inside the pipeline: `grep -q | grep` never matched)
    if echo "$MCP_CONTENT" | grep -oE 'https?://[^"]+' | grep -vE 'npm|github|registry' | grep -q .; then
        WARNINGS+=("MCP config references external URLs. Verify these are trusted sources.")
    fi
fi

# === PROJECT-LEVEL MCP CONFIG CHECK ===
if [[ -f "$PROJECT_MCP" ]]; then
    PROJECT_MCP_CONTENT=$(cat "$PROJECT_MCP" 2>/dev/null || echo "{}")

    # Check for dangerous flags in project config
    if echo "$PROJECT_MCP_CONTENT" | grep -qiE '"--dangerous|"--allow-write|"--no-sandbox'; then
        WARNINGS+=("Project .mcp.json contains dangerous flags. This could be a supply chain attack.")
    fi

    # Check for shell injection patterns
    if echo "$PROJECT_MCP_CONTENT" | grep -qE '\$\(|`[^`]+`|&&|\|\|'; then
        WARNINGS+=("Project .mcp.json contains shell metacharacters. Review for command injection.")
    fi

    # Check for base64-encoded content
    if echo "$PROJECT_MCP_CONTENT" | grep -qE '[A-Za-z0-9+/]{40,}={0,2}'; then
        WARNINGS+=("Project .mcp.json contains base64-like content. This could hide malicious payloads.")
    fi
fi

# === OUTPUT WARNINGS ===
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    WARNING_MSG=""
    for warning in "${WARNINGS[@]}"; do
        WARNING_MSG="${WARNING_MSG}⚠️ ${warning} "
    done

    # Output as systemMessage (jq escapes quotes and backslashes in the findings)
    jq -n --arg msg "MCP INTEGRITY CHECK: ${WARNING_MSG}" '{systemMessage: $msg}'
fi

# Always exit 0 (warn, don't block session start)
exit 0
