---
title: "Analytics Agent with Built-in Evaluation"
description: "Production-ready analytics agent with automated metrics collection and safety validation"
tags: [agents, template, testing, performance]
---

# Analytics agent with built-in evaluation

**Template**: Production-ready analytics agent with automated metrics collection

**Use Case**: SQL query generation with quality tracking, performance monitoring, and safety validation

**Related Guide**: [Agent Evaluation](../../../guide/roles/agent-evaluation.md)

---

## What's included

| File | Purpose |
|------|---------|
| `analytics-agent.md` | Agent definition with evaluation criteria |
| `hooks/post-response-metrics.sh` | Automated metrics logging after each response |
| `eval/metrics.sh` | Analysis script for aggregating collected metrics |
| `eval/report-template.md` | Template for monthly evaluation reports |

---

## Setup

### 1. Copy agent to project

```bash
# Copy agent definition
cp analytics-agent.md ~/.claude/agents/

# Or for project-specific:
cp analytics-agent.md /path/to/project/.claude/agents/
```

### 2. Install hook

```bash
# Copy hook to project
cp hooks/post-response-metrics.sh /path/to/project/.claude/hooks/

# Make executable
chmod +x /path/to/project/.claude/hooks/post-response-metrics.sh
```

### 3. Configure hook trigger

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "analytics-agent",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/post-response-metrics.sh"
          }
        ]
      }
    ]
  }
}
```

`SubagentStop` fires when a subagent finishes and matches on the agent type. The hook receives JSON on stdin, including `agent_type` and `last_assistant_message`. It needs `jq`.

### 4. Create logs directory

```bash
mkdir -p /path/to/project/.claude/logs
```

---

## Usage

### Invoke agent

```bash
# In Claude Code session
"Use analytics-agent to generate a SQL query for [task description]"
```

### Check metrics

```bash
# View raw metrics log
cat .claude/logs/analytics-metrics.jsonl

# Run analysis (optional arguments: log file, then start date)
./examples/agents/analytics-with-eval/eval/metrics.sh .claude/logs/analytics-metrics.jsonl 2026-02-01
```

### Generate monthly report

```bash
# Copy template
cp eval/report-template.md reports/analytics-2026-02.md

# Fill in metrics from metrics.sh output
```

---

## Metrics collected

The hook automatically logs:

| Metric | Description | Source |
|--------|-------------|--------|
| `timestamp` | ISO 8601 timestamp | System |
| `query` | Generated SQL query | Agent response |
| `exec_time` | Query execution time | Database |
| `safety` | PASS/FAIL for destructive ops | Query analysis |
| `row_count` | Rows returned | Database |
| `error` | Error message if query failed | Database |

**Log format**: JSONL (JSON Lines) in `.claude/logs/analytics-metrics.jsonl`

---

## Example metrics output

```bash
$ ./eval/metrics.sh

=== Analytics Agent Metrics Report ===
Period: 2026-02-01 to 2026-02-10

Total queries: 45
Safety checks:
  - PASS: 42 (93%)
  - FAIL: 3 (7%)

Execution time:
  - Mean: 2.3s
  - Median: 1.8s
  - P95: 5.2s
  - P99: 8.1s

Common failures:
  1. DELETE without WHERE clause (2 occurrences)
  2. DROP TABLE in query (1 occurrence)

Recommendations:
  - Review agent instructions to emphasize WHERE clause requirement
  - Add explicit prohibition on DROP operations
```

---

## Customization

### Modify safety checks

Edit the destructive-operation check in `hooks/post-response-metrics.sh`:

```bash
# Add more patterns
if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE|ALTER'; then
  SAFETY="FAIL"
fi
```

### Add custom metrics

Extend the JSON log structure:

```bash
# Add a field to the jq object that builds LOG_ENTRY
--arg your_metric "$VALUE" \
'{timestamp: $timestamp, query: $query, your_metric: $your_metric}'
```

### Change log location

Set the `CLAUDE_LOGS_DIR` environment variable, or edit `LOG_FILE` in the hook script.

---

## Troubleshooting

### Hook not triggering

**Check**:
1. Hook is executable: `ls -l .claude/hooks/*.sh`
2. Hook is enabled in settings.json
3. The `SubagentStop` matcher equals the agent `name`: `analytics-agent` (hyphenated)

**Debug**:
```bash
# Test hook manually with a SubagentStop payload
echo '{"agent_type":"analytics-agent","last_assistant_message":"```sql\nSELECT 1;\n```"}' \
  | ./.claude/hooks/post-response-metrics.sh
```

### No metrics in log

**Check**:
1. Log directory exists: `mkdir -p .claude/logs`
2. Write permissions: `touch .claude/logs/test.log`
3. Query extraction pattern matches your SQL format

### Metrics analysis fails

**Check**:
1. `jq` is installed: `which jq`
2. Log file is valid JSONL: `jq . .claude/logs/analytics-metrics.jsonl`

---

## Production considerations

### Performance

- The hook runs once per subagent run, not per tool call
- The log grows by one JSON line per query: rotate it periodically

### Privacy

- Logs contain actual SQL queries (may include sensitive data)
- Add to `.gitignore`: `.claude/logs/`
- Consider redacting sensitive values in hook script

### Database connection

- Hook requires database access for `exec_time` measurement
- Configure connection in hook script or use environment variables
- Ensure read-only credentials for safety

---

## Related resources

- **[Agent Evaluation Guide](../../../guide/roles/agent-evaluation.md)**: Complete evaluation methodology
- **[Hooks Documentation](../../../guide/ultimate-guide.md#7-hooks)**: Hook system reference
- **[nao Framework](https://github.com/getnao/nao/)**: Production analytics agent framework (inspiration)

---

## License

Same as the parent repository (see the LICENSE file at the repository root)

**Questions?** Open an issue or discussion in the main repository.
