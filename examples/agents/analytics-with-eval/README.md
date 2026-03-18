---
title: "Analytics Agent with Built-in Evaluation"
description: "Production-ready analytics agent with automated metrics collection and safety validation"
tags: [agents, template, testing, performance]
---

# Analytics Agent with Built-in Evaluation

**Template**: Production-ready analytics agent with automated metrics collection

**Use Case**: SQL query generation with quality tracking, performance monitoring, and safety validation

**Related Guide**: [Agent Evaluation](../../../guide/agent-evaluation.md)

---

## What's Included

| File | Purpose |
|------|---------|
| `analytics-agent.md` | Agent definition with evaluation criteria |
| `hooks/post-response-metrics.sh` | Automated metrics logging after each response |
| `eval/metrics.sh` | Analysis script for aggregating collected metrics |
| `eval/report-template.md` | Template for monthly evaluation reports |

---

## Setup

### 1. Copy Agent to Project

```bash
# Copy agent definition
cp analytics-agent.md ~/.claude/agents/

# Or for project-specific:
cp analytics-agent.md /path/to/project/.claude/agents/
```

### 2. Install Hook

```bash
# Copy hook to project
cp hooks/post-response-metrics.sh /path/to/project/.claude/hooks/

# Make executable
chmod +x /path/to/project/.claude/hooks/post-response-metrics.sh
```

### 3. Configure Hook Trigger

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "postToolUse": [
      {
        "command": ".claude/hooks/post-response-metrics.sh",
        "enabled": true,
        "description": "Log analytics agent metrics"
      }
    ]
  }
}
```

### 4. Create Logs Directory

```bash
mkdir -p /path/to/project/.claude/logs
```

---

## Usage

### Invoke Agent

```bash
# In Claude Code session
"Use analytics-agent to generate a SQL query for [task description]"
```

### Check Metrics

```bash
# View raw metrics log
cat .claude/logs/analytics-metrics.jsonl

# Run analysis
./examples/agents/analytics-with-eval/eval/metrics.sh
```

### Generate Monthly Report

```bash
# Copy template
cp eval/report-template.md reports/analytics-2026-02.md

# Fill in metrics from metrics.sh output
```

---

## Metrics Collected

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

## Example Metrics Output

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

### Modify Safety Checks

Edit `hooks/post-response-metrics.sh` line 12-16:

```bash
# Add more patterns
if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE|ALTER'; then
  SAFETY="FAIL"
fi
```

### Add Custom Metrics

Extend the JSON log structure:

```bash
echo "{
  \"timestamp\":\"$(date -Iseconds)\",
  \"query\":\"$QUERY\",
  \"your_metric\":\"$VALUE\"
}" >> .claude/logs/analytics-metrics.jsonl
```

### Change Log Location

Update `POST_RESPONSE_LOG` variable in hook script.

---

## Troubleshooting

### Hook Not Triggering

**Check**:
1. Hook is executable: `ls -l .claude/hooks/*.sh`
2. Hook is enabled in settings.json
3. Agent name matches: `analytics-agent` (hyphenated)

**Debug**:
```bash
# Test hook manually
export CLAUDE_RESPONSE='{"content":"SELECT * FROM users;"}'
./.claude/hooks/post-response-metrics.sh
```

### No Metrics in Log

**Check**:
1. Log directory exists: `mkdir -p .claude/logs`
2. Write permissions: `touch .claude/logs/test.log`
3. Query extraction pattern matches your SQL format

### Metrics Analysis Fails

**Check**:
1. `jq` is installed: `which jq`
2. Log file is valid JSONL: `jq . .claude/logs/analytics-metrics.jsonl`

---

## Production Considerations

### Performance

- Hook adds ~50ms overhead per response
- Log file grows ~200 bytes per query
- Rotate logs monthly to prevent bloat

### Privacy

- Logs contain actual SQL queries (may include sensitive data)
- Add to `.gitignore`: `.claude/logs/`
- Consider redacting sensitive values in hook script

### Database Connection

- Hook requires database access for `exec_time` measurement
- Configure connection in hook script or use environment variables
- Ensure read-only credentials for safety

---

## Related Resources

- **[Agent Evaluation Guide](../../../guide/agent-evaluation.md)**: Complete evaluation methodology
- **[Hooks Documentation](../../../guide/ultimate-guide.md#5-hooks)**: Hook system reference
- **[nao Framework](https://github.com/getnao/nao/)**: Production analytics agent framework (inspiration)

---

## License

Same as parent repository (MIT)

**Questions?** Open an issue or discussion in the main repository.
