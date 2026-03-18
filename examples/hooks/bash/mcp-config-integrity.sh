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
#       "SessionStart": [
#         "bash examples/hooks/bash/mcp-config-integrity.sh"
#       ]
#     }
#   }
#
# Initial setup (run once to create baseline):
#   sha256sum ~/.claude.json > ~/.claude/.mcp-baseline.sha256
#
# Exit codes:
#   0 = allow (config unchanged or no baseline)
#   Non-zero outputs systemMessage warnings
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

# === GLOBAL MCP CONFIG CHECK ===
if [[ -f "$MCP_CONFIG" ]]; then
    # Check if baseline exists
    if [[ -f "$MCP_BASELINE" ]]; then
        # Compute current hash
        CURRENT_HASH=$(sha256sum "$MCP_CONFIG" 2>/dev/null | awk '{print $1}')
        BASELINE_HASH=$(awk '{print $1}' "$MCP_BASELINE" 2>/dev/null || echo "")

        if [[ -n "$CURRENT_HASH" && -n "$BASELINE_HASH" && "$CURRENT_HASH" != "$BASELINE_HASH" ]]; then
            WARNINGS+=("MCP config modified since baseline was created. Review ~/.claude.json for unauthorized changes. Run 'sha256sum ~/.claude.json > ~/.claude/.mcp-baseline.sha256' to update baseline if changes are legitimate.")
        fi
    else
        # No baseline - suggest creating one
        WARNINGS+=("No MCP config baseline found. Consider running: sha256sum ~/.claude.json > ~/.claude/.mcp-baseline.sha256")
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
    if echo "$MCP_CONTENT" | grep -qE 'https?://[^"]+' | grep -vE 'npm|github|registry'; then
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

    # Output as systemMessage
    echo "{\"systemMessage\": \"MCP INTEGRITY CHECK: ${WARNING_MSG}\"}"
fi

# Always exit 0 (warn, don't block session start)
exit 0
