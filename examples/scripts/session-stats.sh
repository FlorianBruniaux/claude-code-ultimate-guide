#!/bin/bash
# session-stats.sh - Analyze Claude Code session logs
#
# Analyzes logs created by session-logger.sh hook and outputs statistics
# about tool usage, estimated costs, and session patterns.
#
# Usage:
#   ./session-stats.sh                    # Today's summary
#   ./session-stats.sh --range week       # Last 7 days
#   ./session-stats.sh --range month      # Last 30 days
#   ./session-stats.sh --date 2026-01-14  # Specific date
#   ./session-stats.sh --json             # Machine-readable output
#   ./session-stats.sh --project myapp    # Filter by project
#
# Environment:
#   CLAUDE_LOG_DIR - Log directory (default: ~/.claude/logs)
#
# Cost rates (per 1K tokens, configurable):
#   CLAUDE_RATE_INPUT  - Input token rate (default: 0.002 for Sonnet 5)
#   CLAUDE_RATE_OUTPUT - Output token rate (default: 0.010 for Sonnet 5)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
LOG_DIR="${CLAUDE_LOG_DIR:-$HOME/.claude/logs}"
RATE_INPUT="${CLAUDE_RATE_INPUT:-0.002}"
RATE_OUTPUT="${CLAUDE_RATE_OUTPUT:-0.010}"

# Defaults
OUTPUT_MODE="human"
DATE_RANGE="today"
SPECIFIC_DATE=""
PROJECT_FILTER=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            OUTPUT_MODE="json"
            shift
            ;;
        --range)
            DATE_RANGE="$2"
            shift 2
            ;;
        --date)
            SPECIFIC_DATE="$2"
            DATE_RANGE="specific"
            shift 2
            ;;
        --project)
            PROJECT_FILTER="$2"
            shift 2
            ;;
        --help|-h)
            grep '^#' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Check if log directory exists
if [[ ! -d "$LOG_DIR" ]]; then
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        echo '{"error": "No logs found", "log_dir": "'"$LOG_DIR"'"}'
    else
        echo -e "${RED}No logs found in $LOG_DIR${NC}"
        echo "Enable session-logger.sh hook to start collecting logs."
    fi
    exit 1
fi

# Determine which log files to analyze
LOG_FILES=()

case "$DATE_RANGE" in
    today)
        TODAY=$(date +%Y-%m-%d)
        [[ -f "$LOG_DIR/activity-$TODAY.jsonl" ]] && LOG_FILES+=("$LOG_DIR/activity-$TODAY.jsonl")
        ;;
    week)
        for i in {0..6}; do
            DATE=$(date -v-${i}d +%Y-%m-%d 2>/dev/null || date -d "-$i days" +%Y-%m-%d)
            [[ -f "$LOG_DIR/activity-$DATE.jsonl" ]] && LOG_FILES+=("$LOG_DIR/activity-$DATE.jsonl")
        done
        ;;
    month)
        for i in {0..29}; do
            DATE=$(date -v-${i}d +%Y-%m-%d 2>/dev/null || date -d "-$i days" +%Y-%m-%d)
            [[ -f "$LOG_DIR/activity-$DATE.jsonl" ]] && LOG_FILES+=("$LOG_DIR/activity-$DATE.jsonl")
        done
        ;;
    specific)
        [[ -f "$LOG_DIR/activity-$SPECIFIC_DATE.jsonl" ]] && LOG_FILES+=("$LOG_DIR/activity-$SPECIFIC_DATE.jsonl")
        ;;
esac

if [[ ${#LOG_FILES[@]} -eq 0 ]]; then
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        echo '{"error": "No logs found for specified range", "range": "'"$DATE_RANGE"'"}'
    else
        echo -e "${YELLOW}No logs found for range: $DATE_RANGE${NC}"
    fi
    exit 0
fi

# Combine and filter logs
COMBINED_LOGS=$(cat "${LOG_FILES[@]}" 2>/dev/null || true)

if [[ -n "$PROJECT_FILTER" ]]; then
    COMBINED_LOGS=$(echo "$COMBINED_LOGS" | jq -c "select(.project == \"$PROJECT_FILTER\")" 2>/dev/null || true)
fi

if [[ -z "$COMBINED_LOGS" ]]; then
    if [[ "$OUTPUT_MODE" == "json" ]]; then
        echo '{"error": "No matching logs found"}'
    else
        echo -e "${YELLOW}No matching logs found${NC}"
    fi
    exit 0
fi

# Calculate statistics
TOTAL_OPS=$(echo "$COMBINED_LOGS" | wc -l | tr -d ' ')
TOTAL_TOKENS_IN=$(echo "$COMBINED_LOGS" | jq -s '[.[].tokens.input // 0] | add')
TOTAL_TOKENS_OUT=$(echo "$COMBINED_LOGS" | jq -s '[.[].tokens.output // 0] | add')
TOTAL_TOKENS=$((TOTAL_TOKENS_IN + TOTAL_TOKENS_OUT))

# Cost calculation
COST_INPUT=$(echo "scale=4; $TOTAL_TOKENS_IN * $RATE_INPUT / 1000" | bc)
COST_OUTPUT=$(echo "scale=4; $TOTAL_TOKENS_OUT * $RATE_OUTPUT / 1000" | bc)
COST_TOTAL=$(echo "scale=4; $COST_INPUT + $COST_OUTPUT" | bc)

# Tool breakdown
TOOL_STATS=$(echo "$COMBINED_LOGS" | jq -s 'group_by(.tool) | map({tool: .[0].tool, count: length}) | sort_by(-.count)')

# Session count
SESSION_COUNT=$(echo "$COMBINED_LOGS" | jq -s '[.[].session_id] | unique | length')

# Project breakdown
PROJECT_STATS=$(echo "$COMBINED_LOGS" | jq -s 'group_by(.project) | map({project: .[0].project, count: length}) | sort_by(-.count)')

# Most edited files
FILE_STATS=$(echo "$COMBINED_LOGS" | jq -s '[.[] | select(.file != null)] | group_by(.file) | map({file: .[0].file, count: length}) | sort_by(-.count) | .[0:10]')

# Output
if [[ "$OUTPUT_MODE" == "json" ]]; then
    jq -n \
        --arg range "$DATE_RANGE" \
        --argjson total_ops "$TOTAL_OPS" \
        --argjson sessions "$SESSION_COUNT" \
        --argjson tokens_in "$TOTAL_TOKENS_IN" \
        --argjson tokens_out "$TOTAL_TOKENS_OUT" \
        --argjson tokens_total "$TOTAL_TOKENS" \
        --arg cost_in "$COST_INPUT" \
        --arg cost_out "$COST_OUTPUT" \
        --arg cost_total "$COST_TOTAL" \
        --argjson tools "$TOOL_STATS" \
        --argjson projects "$PROJECT_STATS" \
        --argjson files "$FILE_STATS" \
        '{
            range: $range,
            summary: {
                total_operations: $total_ops,
                sessions: $sessions,
                tokens: {
                    input: $tokens_in,
                    output: $tokens_out,
                    total: $tokens_total
                },
                estimated_cost: {
                    input: ($cost_in | tonumber),
                    output: ($cost_out | tonumber),
                    total: ($cost_total | tonumber),
                    currency: "USD"
                }
            },
            tools: $tools,
            projects: $projects,
            top_files: $files
        }'
else
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}        Claude Code Session Statistics - $DATE_RANGE${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "${BLUE}Summary${NC}"
    echo "  Total operations:  $TOTAL_OPS"
    echo "  Sessions:          $SESSION_COUNT"
    echo ""

    echo -e "${BLUE}Token Usage${NC}"
    printf "  Input tokens:      %'d\n" "$TOTAL_TOKENS_IN"
    printf "  Output tokens:     %'d\n" "$TOTAL_TOKENS_OUT"
    printf "  Total tokens:      %'d\n" "$TOTAL_TOKENS"
    echo ""

    echo -e "${BLUE}Estimated Cost (configured standard rates; excludes cache discounts)${NC}"
    printf "  Input:   \$%.4f\n" "$COST_INPUT"
    printf "  Output:  \$%.4f\n" "$COST_OUTPUT"
    printf "  ${GREEN}Total:   \$%.4f${NC}\n" "$COST_TOTAL"
    echo ""

    echo -e "${BLUE}Tools Used${NC}"
    echo "$TOOL_STATS" | jq -r '.[] | "  \(.tool): \(.count)"'
    echo ""

    echo -e "${BLUE}Projects${NC}"
    echo "$PROJECT_STATS" | jq -r '.[] | "  \(.project): \(.count)"'
    echo ""

    echo -e "${BLUE}Most Edited Files${NC}"
    echo "$FILE_STATS" | jq -r '.[] | "  \(.file | split("/")[-1]): \(.count)"' | head -5
    echo ""

    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Logs: $LOG_DIR"
    echo -e "Rate config: \$${RATE_INPUT}/1K in, \$${RATE_OUTPUT}/1K out"
    echo ""
fi
