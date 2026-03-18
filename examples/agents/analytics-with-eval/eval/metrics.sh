#!/bin/bash
# Analytics Agent Metrics Analysis
# Analyzes collected metrics from .claude/logs/analytics-metrics.jsonl
# Produces summary statistics, safety reports, and recommendations
#
# Usage:
#   ./metrics.sh                    # Analyze all metrics
#   ./metrics.sh --since 2026-02-01 # Filter by date
#   ./metrics.sh --report           # Generate formatted report

set -euo pipefail

# Configuration
LOG_FILE="${1:-.claude/logs/analytics-metrics.jsonl}"
SINCE_DATE="${2:-}"

# Check dependencies
if ! command -v jq > /dev/null 2>&1; then
  echo "Error: jq is required but not installed." >&2
  echo "Install: brew install jq (macOS) or apt-get install jq (Linux)" >&2
  exit 1
fi

# Check log file exists
if [ ! -f "$LOG_FILE" ]; then
  echo "Error: Log file not found: $LOG_FILE" >&2
  echo "Ensure analytics agent has been used and hook is configured." >&2
  exit 1
fi

# Filter by date if specified
if [ -n "$SINCE_DATE" ]; then
  METRICS=$(jq -c "select(.timestamp >= \"$SINCE_DATE\")" "$LOG_FILE")
else
  METRICS=$(cat "$LOG_FILE")
fi

# Count total queries
TOTAL=$(echo "$METRICS" | wc -l | xargs)

if [ "$TOTAL" -eq 0 ]; then
  echo "No metrics found."
  exit 0
fi

# Calculate date range
FIRST_DATE=$(echo "$METRICS" | head -1 | jq -r '.timestamp' | cut -d'T' -f1)
LAST_DATE=$(echo "$METRICS" | tail -1 | jq -r '.timestamp' | cut -d'T' -f1)

# Safety analysis
SAFETY_PASS=$(echo "$METRICS" | jq -s 'map(select(.safety == "PASS")) | length')
SAFETY_FAIL=$(echo "$METRICS" | jq -s 'map(select(.safety == "FAIL")) | length')
SAFETY_PASS_PCT=$((SAFETY_PASS * 100 / TOTAL))
SAFETY_FAIL_PCT=$((SAFETY_FAIL * 100 / TOTAL))

# Execution time analysis (if available)
EXEC_TIMES=$(echo "$METRICS" | jq -r 'select(.exec_time != null and .exec_time != "null") | .exec_time' || echo "")
if [ -n "$EXEC_TIMES" ]; then
  HAS_EXEC_TIME=true
  # Convert to seconds (assuming format like "0.23s" or "2.1s")
  EXEC_TIMES_SEC=$(echo "$EXEC_TIMES" | sed 's/s$//' | sort -n)
  EXEC_COUNT=$(echo "$EXEC_TIMES_SEC" | wc -l | xargs)
  EXEC_MEAN=$(echo "$EXEC_TIMES_SEC" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
  EXEC_MEDIAN=$(echo "$EXEC_TIMES_SEC" | awk '{arr[NR]=$1} END {print arr[int(NR/2)]}')
  EXEC_P95=$(echo "$EXEC_TIMES_SEC" | awk '{arr[NR]=$1} END {print arr[int(NR*0.95)]}')
  EXEC_P99=$(echo "$EXEC_TIMES_SEC" | awk '{arr[NR]=$1} END {print arr[int(NR*0.99)]}')
else
  HAS_EXEC_TIME=false
fi

# Top failure reasons
FAILURE_REASONS=$(echo "$METRICS" | jq -r 'select(.safety == "FAIL") | .safety_reason' | sort | uniq -c | sort -rn | head -5)

# Print report
echo "=== Analytics Agent Metrics Report ==="
echo ""
echo "Period: $FIRST_DATE to $LAST_DATE"
echo "Total queries: $TOTAL"
echo ""

echo "Safety Checks:"
echo "  PASS: $SAFETY_PASS ($SAFETY_PASS_PCT%)"
echo "  FAIL: $SAFETY_FAIL ($SAFETY_FAIL_PCT%)"
echo ""

if [ "$HAS_EXEC_TIME" = true ]; then
  echo "Execution Time (based on $EXEC_COUNT queries with timing data):"
  echo "  Mean:   ${EXEC_MEAN}s"
  echo "  Median: ${EXEC_MEDIAN}s"
  echo "  P95:    ${EXEC_P95}s"
  echo "  P99:    ${EXEC_P99}s"
  echo ""
fi

if [ "$SAFETY_FAIL" -gt 0 ]; then
  echo "Common Safety Failures:"
  echo "$FAILURE_REASONS" | while read -r line; do
    COUNT=$(echo "$line" | awk '{print $1}')
    REASON=$(echo "$line" | cut -d' ' -f2-)
    echo "  - $REASON ($COUNT occurrences)"
  done
  echo ""
fi

# Recommendations
echo "Recommendations:"
if [ "$SAFETY_FAIL_PCT" -gt 10 ]; then
  echo "  ⚠️  HIGH: ${SAFETY_FAIL_PCT}% safety failures detected"
  echo "      Action: Review agent instructions to emphasize safety rules"
fi

if [ "$HAS_EXEC_TIME" = true ]; then
  if (( $(echo "$EXEC_P95 > 5.0" | bc -l) )); then
    echo "  ⚠️  P95 execution time > 5s"
    echo "      Action: Review slow queries, add indexes, or optimize filters"
  fi
fi

if [ "$SAFETY_FAIL" -eq 0 ]; then
  echo "  ✅ No safety failures - agent following rules correctly"
fi

if [ "$TOTAL" -lt 10 ]; then
  echo "  ℹ️  Low sample size ($TOTAL queries)"
  echo "      Action: Collect more data before drawing conclusions"
fi

echo ""
echo "Next Steps:"
echo "  1. Review failed queries: jq 'select(.safety == \"FAIL\")' $LOG_FILE"
echo "  2. Generate monthly report: cp eval/report-template.md reports/$(date +%Y-%m).md"
echo "  3. Update agent instructions based on patterns"
echo ""

# Optional: Export for further analysis
# echo "$METRICS" | jq -s '.' > analytics-metrics-export.json
# echo "Exported to: analytics-metrics-export.json"
