#!/bin/bash
# SubagentStop hook for analytics-agent metrics collection
# Runs when the analytics-agent subagent finishes and logs quality, safety and
# performance metrics for the SQL it produced.
#
# Input: the hook JSON arrives on stdin. SubagentStop provides `agent_type` and
# `last_assistant_message` (the subagent's final response text).
#
# Setup:
#   1. Copy to .claude/hooks/post-response-metrics.sh
#   2. chmod +x .claude/hooks/post-response-metrics.sh
#   3. Register under hooks.SubagentStop in .claude/settings.json (see README.md)
#   4. mkdir -p .claude/logs
#
# Requires: jq

set -euo pipefail

# Configuration
LOG_FILE="${CLAUDE_LOGS_DIR:-.claude/logs}/analytics-metrics.jsonl"
AGENT_NAME="analytics-agent"

if ! command -v jq > /dev/null 2>&1; then
  echo "post-response-metrics: jq is required" >&2
  exit 0
fi

INPUT=$(cat)

# Only log the analytics agent (the settings matcher already filters, this is a safeguard)
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // empty')
if [ "$AGENT_TYPE" != "$AGENT_NAME" ]; then
  exit 0
fi

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Extract the first ```sql fenced block from the subagent's final message
RESPONSE=$(echo "$INPUT" | jq -r '.last_assistant_message // empty')
QUERY=$(printf '%s\n' "$RESPONSE" | awk '/^```sql/{f=1; next} /^```/{if (f) exit} f')

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

# Build JSON log entry (jq handles escaping)
LOG_ENTRY=$(jq -cn \
  --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg query "$QUERY" \
  --arg exec_time "$EXEC_TIME" \
  --arg safety "$SAFETY" \
  --arg safety_reason "$SAFETY_REASON" \
  --arg row_count "$ROW_COUNT" \
  --arg error "$ERROR" \
  '{timestamp: $timestamp, query: $query, exec_time: $exec_time, safety: $safety, safety_reason: $safety_reason, row_count: $row_count, error: $error}')

# Append to log file
echo "$LOG_ENTRY" >> "$LOG_FILE"

# Optional: Alert on safety failures
if [ "$SAFETY" = "FAIL" ]; then
  echo "⚠️  SAFETY CHECK FAILED: $SAFETY_REASON" >&2
  echo "Query: $QUERY" >&2
fi

exit 0
