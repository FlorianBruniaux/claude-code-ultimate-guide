---
name: cyber-defense-team
description: "Orchestrate a 4-agent cyber defense pipeline to analyze log files for threats. Use when investigating security logs, detecting anomalies in access patterns, classifying breach severity, or generating incident reports from nginx/auth/syslog files."
allowed-tools: Read Bash
argument-hint: "[log-file-path]"
effort: high
metadata:
  version: 1.0.0
---

# Cyber defense team skill

Orchestrate a 4-agent pipeline that analyzes log files for security threats and produces an incident report.

## Pipeline architecture

```
[You] -> Team Lead (this skill)
           |
           |-[1]-> log-ingestor    (haiku)  -> cyber-defense-events.json
           |
           |-[2]-> anomaly-detector (sonnet) -> cyber-defense-anomalies.json
           |                                    (reads events.json)
           |-[3]-> risk-classifier  (sonnet) -> cyber-defense-risk.json
           |                                    (reads anomalies.json)
           `-[4]-> threat-reporter  (sonnet) -> cyber-defense-report.md
                                               (reads all 3 JSON files)
```

Stages 2 and 3 are sequential (each depends on previous output). Stage 4 runs after all data is ready.

## Execution steps

### Step 1: Validate input

Check that the log file exists (or that log content was provided inline). If the path doesn't exist, tell the user immediately and don't proceed.

### Step 2: Spawn log ingestor

Use the Agent tool to spawn the `log-ingestor` agent:

```
Task: Parse the log file at [log_path] and write structured events to cyber-defense-events.json.
Log path: [log_path]
```

Wait for completion. Confirm `cyber-defense-events.json` was created.

### Step 3: Spawn anomaly detector

Use the Agent tool to spawn the `anomaly-detector` agent:

```
Task: Read cyber-defense-events.json and detect anomalies. Write results to cyber-defense-anomalies.json.
```

Wait for completion. If `anomalies_found: 0`, skip to Step 5 (reporter still runs).

### Step 4: Spawn risk classifier

Use the Agent tool to spawn the `risk-classifier` agent:

```
Task: Read cyber-defense-anomalies.json and classify overall risk. Write result to cyber-defense-risk.json.
```

### Step 5: Spawn threat reporter

Use the Agent tool to spawn the `threat-reporter` agent:

```
Task: Read cyber-defense-events.json, cyber-defense-anomalies.json, and cyber-defense-risk.json. Generate a complete incident report and save it to cyber-defense-report.md.
```

### Step 6: Summarize for user

Read `cyber-defense-risk.json` and present:

```
Analysis complete

Risk Level : HIGH
Score      : 74/100
Threats    : 2 anomalies detected
Report     : cyber-defense-report.md

Primary threat: Brute force attack from 192.168.1.105
Immediate action required: [first recommended_action]
```

## Error handling

- Agent fails at step 2: Tell user, stop pipeline, show raw error.
- Agent fails at step 3+: Show partial results, note which stage failed.
- Log file not found: "File [path] not found. Provide a valid path or paste log content."

## Cost estimate

| Stage | Model | Typical tokens |
|-------|-------|----------------|
| log-ingestor | haiku | ~2K |
| anomaly-detector | sonnet | ~3K |
| risk-classifier | sonnet | ~2K |
| threat-reporter | sonnet | ~3K |
| **Total** | | **~10K** |

For large log files (>10K lines), log-ingestor may use up to 20K tokens.

## Example usage

```
/cyber-defense-team /var/log/nginx/access.log
/cyber-defense-team /tmp/auth.log
```
