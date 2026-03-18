#!/bin/bash
# Post-response hook for analytics agent metrics collection
# Triggered after each agent response to log quality, performance, and safety metrics
#
# Setup:
#   1. Copy to .claude/hooks/post-response-metrics.sh
#   2. chmod +x .claude/hooks/post-response-metrics.sh
#   3. Add to .claude/settings.json hooks.postToolUse configuration
#   4. mkdir -p .claude/logs

set -euo pipefail

# Configuration
LOG_FILE="${CLAUDE_LOGS_DIR:-.claude/logs}/analytics-metrics.jsonl"
AGENT_NAME="analytics-agent"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Extract agent ID from environment (if available)
# Note: This assumes Claude Code exposes agent context via environment variables
# Adjust based on actual Claude Code hook environment
CURRENT_AGENT="${CLAUDE_AGENT_NAME:-unknown}"

# Only log if this is the analytics agent
if [ "$CURRENT_AGENT" != "$AGENT_NAME" ]; then
  exit 0
fi

# Extract SQL query from response
# This is a simplified pattern - adjust based on actual response format
QUERY=$(echo "$CLAUDE_RESPONSE" | grep -oP '```sql\s*\K[^`]+' | head -1 || echo "")

# If no query found, skip logging
if [ -z "$QUERY" ]; then
  exit 0
fi

# Safety check: Detect destructive operations
if echo "$QUERY" | grep -iE '\b(DELETE|DROP|TRUNCATE|ALTER)\b' > /dev/null; then
  SAFETY="FAIL"
  SAFETY_REASON="Contains destructive operation (DELETE/DROP/TRUNCATE/ALTER)"
else
  SAFETY="PASS"
  SAFETY_REASON=""
fi

# Check for UPDATE without WHERE (dangerous)
if echo "$QUERY" | grep -iE '\bUPDATE\b' | grep -ivE '\bWHERE\b' > /dev/null; then
  SAFETY="FAIL"
  SAFETY_REASON="UPDATE without WHERE clause"
fi

# Performance measurement (requires database connection)
# TODO: Configure database credentials
# Uncomment and configure if you want actual execution time measurement
#
# DB_HOST="${DB_HOST:-localhost}"
# DB_USER="${DB_USER:-readonly_user}"
# DB_NAME="${DB_NAME:-analytics_db}"
#
# EXEC_TIME=$( (time psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "$QUERY" > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')
#
# For now, set as null (requires database setup)
EXEC_TIME="null"
ROW_COUNT="null"
ERROR="null"

# Build JSON log entry
# Using jq for proper JSON escaping (fallback to basic escaping if jq not available)
if command -v jq > /dev/null 2>&1; then
  LOG_ENTRY=$(jq -n \
    --arg timestamp "$(date -Iseconds)" \
    --arg query "$QUERY" \
    --arg exec_time "$EXEC_TIME" \
    --arg safety "$SAFETY" \
    --arg safety_reason "$SAFETY_REASON" \
    --arg row_count "$ROW_COUNT" \
    --arg error "$ERROR" \
    '{
      timestamp: $timestamp,
      query: $query,
      exec_time: $exec_time,
      safety: $safety,
      safety_reason: $safety_reason,
      row_count: $row_count,
      error: $error
    }')
else
  # Fallback: Basic JSON (may need escaping for special characters)
  LOG_ENTRY="{\"timestamp\":\"$(date -Iseconds)\",\"query\":\"${QUERY//\"/\\\"}\",\"exec_time\":$EXEC_TIME,\"safety\":\"$SAFETY\",\"safety_reason\":\"$SAFETY_REASON\",\"row_count\":$ROW_COUNT,\"error\":$ERROR}"
fi

# Append to log file
echo "$LOG_ENTRY" >> "$LOG_FILE"

# Optional: Alert on safety failures
if [ "$SAFETY" = "FAIL" ]; then
  echo "⚠️  SAFETY CHECK FAILED: $SAFETY_REASON" >&2
  echo "Query: $QUERY" >&2
fi

exit 0
