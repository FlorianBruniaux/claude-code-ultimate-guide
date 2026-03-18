#!/bin/bash
# .claude/hooks/rtk-baseline.sh
# Event: SessionStart
# Save RTK gain baseline for session-summary.sh delta tracking
#
# This hook captures RTK's cumulative stats at session start.
# At session end, session-summary.sh reads this baseline, captures current stats,
# and computes the delta to show per-session RTK savings.
#
# Configuration:
#   SESSION_SUMMARY_RTK=0  - Force disable (skip baseline capture)
#   SESSION_SUMMARY_RTK=1  - Force enable
#   (default: auto-detect if rtk is in PATH)
#
# Place in: ~/.claude/hooks/rtk-baseline.sh
# Register in: ~/.claude/settings.json under SessionStart event

set -euo pipefail

RTK_ENABLED="${SESSION_SUMMARY_RTK:-auto}"

# Auto-detect RTK availability
if [[ "$RTK_ENABLED" == "auto" ]]; then
    command -v rtk &>/dev/null && RTK_ENABLED=1 || RTK_ENABLED=0
fi

# Skip if disabled or RTK not available
if [[ "$RTK_ENABLED" != "1" ]]; then
    exit 0
fi

# Build baseline file path (must match session-summary.sh)
baseline_key=$(echo "${CLAUDE_PROJECT_DIR:-$(pwd)}" | tr '/' '-')
baseline_file="/tmp/rtk-baseline${baseline_key}.txt"

# Capture current RTK cumulative stats
rtk gain > "$baseline_file" 2>/dev/null || true

exit 0
