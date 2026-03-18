---
title: "Session Observability & Monitoring"
description: "Track Claude Code usage, estimate costs, and identify patterns across development sessions"
tags: [observability, guide, performance]
---

# Session Observability & Monitoring

> Track Claude Code usage, estimate costs, and identify patterns across your development sessions.

## Table of Contents

1. [Why Monitor Sessions](#why-monitor-sessions)
2. [Session Search & Resume](#session-search--resume)
3. [Setting Up Session Logging](#setting-up-session-logging)
4. [Analyzing Session Data](#analyzing-session-data)
5. [Cost Tracking](#cost-tracking)
6. [Activity Monitoring](#activity-monitoring)
7. [External Monitoring Tools](#external-monitoring-tools)
8. [Proxying Claude Code](#proxying-claude-code)
9. [Patterns & Best Practices](#patterns--best-practices)
10. [Limitations](#limitations)

---

## Why Monitor Sessions

Claude Code usage can accumulate quickly, especially in active development. Monitoring helps you:

- **Understand costs**: Estimate API spend before invoices arrive
- **Identify patterns**: See which tools you use most, which files get edited repeatedly
- **Optimize workflow**: Find inefficiencies (e.g., repeatedly reading the same large file)
- **Track projects**: Compare usage across different codebases
- **Team visibility**: Aggregate usage for team budgeting (when combining logs)

---

## Session Search & Resume

After weeks of using Claude Code, finding past conversations becomes challenging. This section covers native options and community tools.

### Native Commands

| Command | Use Case |
|---------|----------|
| `claude -c` / `claude --continue` | Resume most recent session |
| `claude -r <id>` / `claude --resume <id>` | Resume specific session by ID |
| `claude --resume` | Interactive session picker |

Sessions are stored locally at `~/.claude/projects/<project>/` as JSONL files.

### Community Tools Comparison

| Tool | Install | List Speed | Search Speed | Dependencies | Resume Command |
|------|---------|------------|--------------|--------------|----------------|
| **session-search.sh** (this repo) | Copy script | **10ms** | **400ms** | None (bash) | ✅ Displayed |
| claude-conversation-extractor | `pip install` | 230ms | 1.7s | Python | ❌ |
| claude-code-transcripts | `uvx` | N/A | N/A | Python | ❌ |
| ran CLI | `npm -g` | N/A | Fast | Node.js | ❌ (commands only) |

### Recommended: session-search.sh

Zero-dependency bash script optimized for speed with ready-to-use resume commands.

**Install:**
```bash
cp examples/scripts/session-search.sh ~/.claude/scripts/cs
chmod +x ~/.claude/scripts/cs
echo "alias cs='~/.claude/scripts/cs'" >> ~/.zshrc
source ~/.zshrc
```

**Usage:**
```bash
cs                          # List 10 most recent sessions (~15ms)
cs "authentication"         # Single keyword search (~400ms)
cs "Prisma migration"       # Multi-word AND search (both must match)
cs -n 20                    # Show 20 results
cs -p myproject "bug"       # Filter by project name
cs --since 7d               # Sessions from last 7 days
cs --since today            # Today's sessions only
cs --json "api" | jq .      # JSON output for scripting
cs --rebuild                # Force index rebuild
```

**Output:**
```
2026-01-15 08:32 │ my-project             │ Implement OAuth flow for...
  claude --resume 84287c0d-8778-4a8d-abf1-eb2807e327a8

2026-01-14 21:13 │ other-project          │ Fix database migration...
  claude --resume 1340c42e-eac5-4181-8407-cc76e1a76219
```

Copy-paste the `claude --resume` command to continue any session.

### How It Works

1. **Index mode** (no filters): Uses cached TSV index. Auto-refreshes when sessions change. ~15ms lookup.
2. **Search mode** (with keyword/filters): Full-text search with 3s timeout. Multi-word queries use AND logic.
3. **Filters**: `--project` (substring match), `--since` (supports `today`, `yesterday`, `7d`, `YYYY-MM-DD`)
4. **Output**: Human-readable by default, `--json` for scripting. Excludes agent/subagent sessions.

### Alternative: Python Tools

If you prefer richer features (HTML export, multiple formats):

```bash
# Install
pip install claude-conversation-extractor

# Interactive UI
claude-start

# Direct search
claude-search "keyword"

# Export to markdown
claude-extract --format markdown
```

See [session-search.sh](../examples/scripts/session-search.sh) for the complete script.

---

### Session Resume Limitations & Cross-Folder Migration

**TL;DR**: Native `--resume` is limited to the current working directory by design. For cross-folder migration, use manual filesystem operations (recommended) or community automation tools (untested).

#### Why Resume is Directory-Scoped

Claude Code stores sessions at `~/.claude/projects/<encoded-path>/` where `<encoded-path>` is derived from your project's absolute path. For example:
- Project at `/home/user/myapp` → Sessions in `~/.claude/projects/-home-user-myapp-/`
- Project moved to `/home/user/projects/myapp` → Claude looks for `~/.claude/projects/-home-user-projects-myapp-/` (different directory)

**Design rationale**: Sessions store absolute file paths, project-specific context (MCP server configs, `.claudeignore` rules, environment variables). Cross-folder resume would require path rewriting and context validation, which isn't implemented yet.

**Related**: GitHub issue [#1516](https://github.com/anthropics/claude-code/issues/1516) tracks community requests for native cross-folder support.

#### Manual Migration (Recommended)

**When moving a project folder:**

```bash
# Before moving project
cd ~/.claude/projects/
ls -la  # Note the current encoded path

# Move your project
mv /old/location/myapp /new/location/myapp

# Rename session directory to match new path
cd ~/.claude/projects/
mv -- -old-location-myapp- -new-location-myapp-

# Verify
cd /new/location/myapp
claude --continue  # Should resume successfully
```

**When forking sessions to a new project:**

```bash
# Copy session files (preserves original)
cd ~/.claude/projects/
cp -n ./-source-project-/*.jsonl ./-target-project-/

# Copy subagents directory if exists
if [ -d ./-source-project-/subagents ]; then
  cp -r ./-source-project-/subagents ./-target-project-/
fi

# Resume in target project
cd /path/to/target/project
claude --continue
```

#### ⚠️ Migration Risks & Caveats

**Before migrating sessions, verify compatibility:**

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Hardcoded secrets** | Credentials exposed in new context | Audit `.jsonl` files before migration, redact if needed |
| **Absolute paths** | File references break if paths differ | Verify paths exist in target, or accept broken references |
| **MCP server configs** | Source MCP servers missing in target | Install matching MCP servers before resuming |
| **`.claudeignore` rules** | Different ignore patterns | Review differences, merge if needed |
| **Environment variables** | `process.env` context mismatch | Check `.env` files compatibility |

**When NOT to migrate sessions:**

- Conflicting dependencies (e.g., different Node.js versions, package managers)
- Database state differences (migrations applied in source, not in target)
- Authentication context (API tokens, OAuth sessions specific to source project)
- Security boundaries (migrating from private to public repo)

#### Community Automation Tool

**claude-migrate-session** by Jim Weller (inspired by Alexis Laporte) automates the manual process above:

- **Repository**: [jimweller/dotfiles](https://github.com/jimweller/dotfiles/tree/main/dotfiles/claude-code/skills/claude-migrate-session)
- **Features**: Global search with filtering, preserves `.jsonl` + subagents, uses ripgrep for performance
- **Status**: Personal dotfiles (0 stars/forks as of Feb 2026), limited adoption
- **Command**: `/claude-migrate-session <source> <target>`

**⚠️ Caveat**: This tool has minimal community testing. The manual approach is safer and gives you explicit control over what gets migrated. Test thoroughly before using in production workflows.

**Use cases for migration:**
- Forking prototype work into production codebase
- Moving debugging session to isolated test repository
- Continuing architecture discussion in a new project

#### Alternative: Entire CLI Session Portability

**Native limitation**: Claude Code's `--resume` is tied to absolute file paths, breaking on folder moves.

**Entire CLI solution**: Checkpoints are **path-agnostic**, enabling true session portability across project locations.

**How it works:**

```bash
# In source project
cd /old/location/myapp
entire capture --agent="claude-code"
[... work in Claude Code ...]
entire checkpoint --name="migration-complete"

# Move project to new location
mv /old/location/myapp /new/location/myapp

# Resume in target (works because Entire stores relative paths)
cd /new/location/myapp
entire resume --checkpoint="migration-complete"
claude --continue  # Resumes with full context
```

**Why Entire checkpoints are portable:**

| Aspect | Native `--resume` | Entire CLI |
|--------|-------------------|-----------|
| **Path storage** | Absolute paths in JSONL | Relative paths in checkpoints |
| **Cross-folder** | Breaks (different project encoding) | Works (path-agnostic) |
| **Context preservation** | Prompt history only | Prompts + reasoning + file states |
| **Agent handoffs** | No | Yes (between Claude/Gemini) |

**When to use Entire over manual migration:**

- ✅ Frequent project moves/forks
- ✅ Multi-agent workflows (Claude → Gemini handoffs)
- ✅ Session replay for debugging (rewind to exact state)
- ✅ Governance (approval gates on resume)

**Trade-off**: Adds tool dependency + storage overhead (~5-10% project size).

> **Full docs**: [AI Traceability Guide](./ai-traceability.md#51-entire-cli)

---

### Multi-Agent Orchestration Monitoring

For monitoring multiple concurrent Claude Code instances via external orchestrators (Gas Town, multiclaude), see:

- **agent-chat** (https://github.com/justinabrahms/agent-chat): Real-time Slack-like UI for agent communications
- **Architecture guide**: `guide/ai-ecosystem.md` Section 8.1 - Multi-Agent Orchestration Systems

**Architecture pattern** (for custom implementations):
1. Hook logs Task agent spawns: `.claude/hooks/multi-agent-logger.sh`
2. Store in SQLite: `~/.claude/logs/agents.db` (parent_id, child_id, timestamp, task)
3. Stream via SSE: Simple Go/Node HTTP server
4. Dashboard: React/HTML consuming SSE stream

**Native Claude Code monitoring** (this guide):
- Session search: `session-search.sh` (see [Session Search & Resume](#session-search--resume))
- Activity logs: `session-logger.sh` hook (see [Setting Up Session Logging](#setting-up-session-logging))
- Stats analysis: `session-stats.sh` (see [Analyzing Session Data](#analyzing-session-data))

**When to use external orchestrator monitoring**:
- Running Gas Town or multiclaude with 5+ concurrent agents
- Need real-time visibility into agent coordination
- Debugging orchestration failures (agent conflicts, merge issues)

**When native monitoring suffices**:
- Single Claude Code session or `--delegate` with <3 subagents
- Post-hoc analysis (logs, stats) is enough
- Budget/complexity constraints

---

## Setting Up Session Logging

### 1. Install the Logger Hook

Copy the session logger to your hooks directory:

```bash
# Create hooks directory if needed
mkdir -p ~/.claude/hooks

# Copy the logger (from this repo's examples)
cp examples/hooks/bash/session-logger.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/session-logger.sh
```

### 2. Register in Settings

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "~/.claude/hooks/session-logger.sh"
      }
    ]
  }
}
```

### 3. Verify Installation

Run a few Claude Code commands, then check logs:

```bash
ls ~/.claude/logs/
# Should see: activity-2026-01-14.jsonl

# View recent entries
tail -5 ~/.claude/logs/activity-$(date +%Y-%m-%d).jsonl | jq .
```

### Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `CLAUDE_LOG_DIR` | `~/.claude/logs` | Where to store logs |
| `CLAUDE_LOG_TOKENS` | `true` | Enable token estimation |
| `CLAUDE_SESSION_ID` | auto-generated | Custom session identifier |

---

## Analyzing Session Data

### Using session-stats.sh

```bash
# Copy the script
cp examples/scripts/session-stats.sh ~/.local/bin/
chmod +x ~/.local/bin/session-stats.sh

# Today's summary
session-stats.sh

# Last 7 days
session-stats.sh --range week

# Specific date
session-stats.sh --date 2026-01-14

# Filter by project
session-stats.sh --project my-app

# Machine-readable output
session-stats.sh --json
```

### Sample Output

```
═══════════════════════════════════════════════════════════
        Claude Code Session Statistics - today
═══════════════════════════════════════════════════════════

Summary
  Total operations:  127
  Sessions:          3

Token Usage
  Input tokens:      45,230
  Output tokens:     12,450
  Total tokens:      57,680

Estimated Cost (Sonnet rates)
  Input:   $0.1357
  Output:  $0.1868
  Total:   $0.3225

Tools Used
  Edit: 45
  Read: 38
  Bash: 24
  Grep: 12
  Write: 8

Projects
  my-app: 89
  other-project: 38
```

### Reading for Quality, Not Just Quantity

Token counts tell you how much you used Claude Code. JSONL logs can also tell you **how well your configuration is working** — if you know what to look for.

Beyond cost metrics, three patterns reliably signal that a skill, rule, or CLAUDE.md section needs updating:

**Repeated reads of the same file**

If Claude reads the same file 3+ times in one session, the content it needs probably isn't where it expects to find it. Consider moving the relevant context into a skill or CLAUDE.md section.

```bash
# Files read more than 3x in recent sessions
jq -r 'select(.tool == "Read") | .file' ~/.claude/logs/activity-*.jsonl \
  | sort | uniq -c | sort -rn | awk '$1 > 3'
```

**Tool failures on the same command**

A Bash command that fails repeatedly across sessions usually means a skill has an outdated path, renamed binary, or command that no longer works with your current stack.

```bash
# Failing commands
jq -r 'select(.tool == "Bash" and (.exit_code // 0) != 0) | .command' \
  ~/.claude/logs/activity-*.jsonl | sort | uniq -c | sort -rn | head -10
```

**High edit frequency on the same file**

Files edited heavily across sessions often indicate missing context — the file's purpose isn't clear to the agent, or conventions around it aren't documented.

```bash
# Most-edited files (proxy for context gaps)
jq -r 'select(.tool == "Edit") | .file' ~/.claude/logs/activity-*.jsonl \
  | sort | uniq -c | sort -rn | head -10
```

For each pattern you surface, ask: is there a skill, rule, or CLAUDE.md section that should cover this? See [§9.23 Configuration Lifecycle & The Update Loop](./ultimate-guide.md#923-configuration-lifecycle--the-update-loop) for the full workflow.

---

### Log Format

Each log entry is a JSON object:

```json
{
  "timestamp": "2026-01-14T15:30:00Z",
  "session_id": "1705234567-12345",
  "tool": "Edit",
  "file": "src/components/Button.tsx",
  "project": "my-app",
  "tokens": {
    "input": 350,
    "output": 120,
    "total": 470
  }
}
```

---

## Cost Tracking

### Token Estimation Method

The logger estimates tokens using a simple heuristic: **~4 characters per token**. This is approximate and tends to slightly overestimate.

### Cost Rates

Default rates are for Claude Sonnet. Adjust via environment variables:

```bash
# Sonnet rates (default)
export CLAUDE_RATE_INPUT=0.003   # $3/1M tokens
export CLAUDE_RATE_OUTPUT=0.015  # $15/1M tokens

# Opus rates (if using Opus)
export CLAUDE_RATE_INPUT=0.015   # $15/1M tokens
export CLAUDE_RATE_OUTPUT=0.075  # $75/1M tokens

# Haiku rates
export CLAUDE_RATE_INPUT=0.00025 # $0.25/1M tokens
export CLAUDE_RATE_OUTPUT=0.00125 # $1.25/1M tokens
```

### Budget Alerts (Manual Pattern)

Add to your shell profile for daily budget warnings:

```bash
# ~/.zshrc or ~/.bashrc
claude_budget_check() {
  local cost=$(session-stats.sh --json 2>/dev/null | jq -r '.summary.estimated_cost.total // 0')
  local threshold=5.00  # $5 daily budget

  if (( $(echo "$cost > $threshold" | bc -l) )); then
    echo "⚠️  Claude Code daily spend: \$$cost (threshold: \$$threshold)"
  fi
}

# Run on shell start
claude_budget_check
```

---

## Activity Monitoring

Cost tracking tells you *how much* you spend. Activity monitoring tells you *what Claude Code actually did*: which files it read, which commands it ran, which URLs it fetched. This is the audit layer.

### Session JSONL: The Ground Truth

Every tool call Claude Code makes is recorded in the session JSONL files at `~/.claude/projects/<project>/`. Each entry with `type: "assistant"` contains a `content` array where `type: "tool_use"` blocks document every action.

```bash
# Find your session files
ls ~/.claude/projects/-$(pwd | tr '/' '-')-/

# Inspect tool calls in a session
cat ~/.claude/projects/-your-project-/SESSION_ID.jsonl | \
  jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | {tool: .name, input: .input}'
```

### What Tool Calls Reveal

| Tool | What It Exposes |
|------|----------------|
| `Read` | Files accessed (path, line range) |
| `Write` / `Edit` | Files modified (path, content delta) |
| `Bash` | Commands executed (full command string) |
| `WebFetch` | URLs fetched (may include data sent in POST) |
| `Task` | Subagent spawns (prompt passed to sub-model) |
| `Glob` / `Grep` | Search patterns and scope |

### Practical Audit Queries

```bash
# All files read in a session
SESSION=~/.claude/projects/-your-project-/SESSION_ID.jsonl
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "Read") | .input.file_path' "$SESSION"

# All bash commands executed
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "Bash") | .input.command' "$SESSION"

# All URLs fetched
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "WebFetch") | .input.url' "$SESSION"

# Count tool usage by type
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' "$SESSION" | sort | uniq -c | sort -rn
```

### Sensitive Patterns to Watch

These tool call patterns are worth flagging in automated audits:

| Pattern | Risk | Detection |
|---------|------|-----------|
| `Read` on `.env`, `*.pem`, `id_rsa` | Credential access | `jq '... | select(.input.file_path | test("\\.(env|pem|key)$"))'` |
| `Bash` with `rm -rf`, `git push --force` | Destructive action | `jq '... | select(.input.command | test("rm -rf\|force-push"))'` |
| `WebFetch` on external URLs | Data exfiltration risk | `jq '... | select(.name == "WebFetch") | .input.url'` |
| `Write` on files outside project root | Scope creep | Check paths against working directory |

> **Security context**: Claude Code operates read-write on your filesystem with your user permissions. The JSONL audit trail is your record of what happened. For teams, consider syncing these logs to immutable storage.

---

## External Monitoring Tools

Beyond the hook-based approach above, the community has built purpose-specific tools. This is a factual snapshot as of early 2026.

| Tool | Type | What It Does | Install |
|------|------|-------------|---------|
| **ccusage** | CLI / TUI | Cost tracking from JSONL — the de-facto reference for pricing data. ~10K GitHub stars. | `npm i -g ccusage` |
| **claude-code-otel** | OpenTelemetry exporter | Emits spans to any OTEL collector. Integrates with Prometheus + Grafana dashboards. Enterprise-focused. | `npm i -g claude-code-otel` |
| **Akto** | SaaS / self-hosted | API security guardrails + audit trail. Intercepts at the API level, flags policy violations. | [akto.io](https://akto.io) |
| **MLflow Tracing** | CLI + SDK | Exact token counts, tool spans, LLM-as-judge evaluation. CLI mode: zero Python required. Best for ML/MLOps teams. | `pip install mlflow` → [see section below](#mlflow-tracing) |
| **ccboard** | TUI + Web | Unified dashboard for sessions, costs, stats. Activity/audit tab in development. | `cargo install ccboard` |

### Decision Guide

```
Want cost numbers fast?          → ccusage (CLI, 0 config)
Need enterprise audit trail?     → claude-code-otel + Grafana or Akto
Already using MLflow for ML?     → MLflow tracing integration (see below)
Need agent regression detection? → MLflow tracing + LLM-as-judge
Want a persistent TUI/Web UI?    → ccboard
```

### ccusage

```bash
npm i -g ccusage
ccusage          # Today's usage
ccusage --days 7 # Last 7 days
```

Reads directly from `~/.claude/projects/**/*.jsonl`. No API keys, no data sent externally. Source: [github.com/ryoppippi/ccusage](https://github.com/ryoppippi/ccusage).

### claude-code-otel

Exports Claude Code activity as OpenTelemetry spans:

```bash
npm i -g claude-code-otel
claude-code-otel --collector http://localhost:4318
```

Spans include tool name, duration, token counts. Plug into any OTEL-compatible backend (Jaeger, Tempo, Datadog). Source: [github.com/badger-99/claude-code-otel](https://github.com/badger-99/claude-code-otel).

### ccboard

```bash
cargo install ccboard
ccboard              # Launch TUI
ccboard --web        # Launch Web UI (localhost:3000)
```

Source: [github.com/FlorianBruniaux/ccboard](https://github.com/FlorianBruniaux/ccboard). An Activity tab covering file access, bash commands, and network calls is planned (see `docs/resource-evaluations/ccboard-activity-module-plan.md`).

### MLflow Tracing

**When to use**: Teams already in the MLflow/MLOps ecosystem, or anyone needing exact token counts + LLM-based quality evaluation. Not the right fit for solo devs wanting quick cost numbers (use ccusage instead).

**What makes it different from the other tools**: MLflow intercepts at the API level, not post-hoc from JSONL. It captures **exact** token counts (vs the ~15-25% variance of hook-based estimation) and enables **LLM-as-judge** regression detection — not just "what happened" but "was it good?".

#### Setup: CLI mode (no Python required)

Works with interactive `claude` sessions. Hooks into `.claude/settings.json`:

```bash
pip install "mlflow[genai]>=3.4"

# Enable tracing in current project directory
mlflow autolog claude

# With custom backend (recommended for persistence)
mlflow autolog claude -u sqlite:///mlflow.db

# With named experiment
mlflow autolog claude -n "my-project"

# Check status / disable
mlflow autolog claude --status
mlflow autolog claude --disable
```

Launch the UI to inspect traces:

```bash
mlflow server  # → http://localhost:5000
```

**What gets captured automatically**: user prompts, assistant responses, tool calls (name + inputs + outputs), token counts (exact), latency per call, session metadata.

#### Setup: SDK mode (Python agents)

```python
import mlflow
mlflow.anthropic.autolog()         # one line, before anything else
mlflow.set_experiment("my-agent")

# Use ClaudeSDKClient normally — all interactions are traced
# ⚠️ Only ClaudeSDKClient is supported. Direct API calls are not traced.
from anthropic import claude_agent_sdk
async with ClaudeSDKClient(options=AGENT_OPTIONS) as client:
    await client.query(query)
```

Requires: `mlflow>=3.5` + `claude-agent-sdk>=0.1.0`.

#### MCP server: bidirectional integration

Claude Code can query its own traces directly. Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "mlflow-mcp": {
      "command": "uv",
      "args": ["run", "--with", "mlflow[mcp]>=3.5.1", "mlflow", "mcp", "run"],
      "env": { "MLFLOW_TRACKING_URI": "<your-tracking-uri>" }
    }
  }
}
```

Once configured, you can ask Claude Code: *"Find all sessions where the backend-architect agent used more than 20 tool calls"* — it queries MLflow directly without copy-pasting IDs.

#### LLM-as-judge: agent regression detection

The key capability absent from all other tools in this section. After modifying an agent's instructions, measure whether quality improved or degraded:

```python
from mlflow.genai.scorers import scorer, ConversationCompleteness, RelevanceToQuery
from mlflow.entities.model_registry import Feedback

@scorer
def tool_efficiency(trace) -> int:
    """Count tool calls — lower is better for well-scoped tasks."""
    return len(trace.search_spans(span_type="TOOL"))

@scorer
def permission_blocks(trace) -> int:
    """Detect how often the agent was blocked by permission gates."""
    return sum(
        1 for span in trace.search_spans(span_type="TOOL")
        if span.outputs and "requires approval" in str(span.outputs).lower()
    )

# Run evaluation against recorded traces
traces = mlflow.search_traces(experiment_ids=["<id>"], max_results=50)
results = mlflow.genai.evaluate(
    data=traces,
    scorers=[
        tool_efficiency,
        permission_blocks,
        ConversationCompleteness(),
        RelevanceToQuery(),
    ]
)
```

**Built-in scorers**: `ConversationCompleteness`, `RelevanceToQuery`, `UserFrustration`, `SafetyScorer`.

**Custom scorers**: full access to the trace object (all spans, inputs, outputs, token counts).

#### Limitations

| Limitation | Detail |
|------------|--------|
| **CLI mode audience** | Best for interactive sessions; SDK mode required for programmatic agents |
| **SDK restriction** | Only `ClaudeSDKClient` — direct API calls bypass tracing |
| **PII risk** | Traces capture full conversation content. Redact before storing if working with sensitive data |
| **Production backend** | SQLite = dev only. Use PostgreSQL/MySQL for production |
| **OpenTelemetry** | MLflow 3.6+ exports to any OTEL-compatible backend (Datadog, Grafana, etc.) |

---

## Proxying Claude Code

A common question: "Can I run Proxyman/Charles to see what Claude Code sends to Anthropic?"

**Short answer**: Not directly. Here's why, and what works instead.

### Why System Proxies Don't Work

Claude Code is a Node.js process. By default, Node.js ignores system-level proxy settings (`HTTP_PROXY`, `HTTPS_PROXY`) — it uses its own TLS stack and doesn't read macOS/Windows proxy configurations.

Additionally, even if traffic flows through your proxy, the TLS certificate mismatch causes Claude Code to fail (`CERT_UNTRUSTED`).

### Option 1: Trust a MITM Certificate (Proxyman / Charles)

Force Node.js to trust your proxy's CA certificate:

```bash
# Export Proxyman's CA cert (File → Export → Root Certificate)
# Then point Node.js at it:
export NODE_EXTRA_CA_CERTS="/path/to/proxyman-ca.pem"

# Start Claude Code — traffic will now route through Proxyman
claude
```

Same approach works for Charles: `Help → SSL Proxying → Export Charles Root Certificate`.

**Caveats**:
- Some Claude Code versions use certificate pinning for `api.anthropic.com` — this may still fail
- This approach requires a running Proxyman/Charles instance listening on the configured port

### Option 2: Redirect API Traffic with ANTHROPIC_API_URL

Point Claude Code at a local interceptor instead of `api.anthropic.com`:

```bash
export ANTHROPIC_API_URL="http://localhost:8080"
claude
```

Run any HTTP proxy/logger on port 8080 that forwards to `https://api.anthropic.com`. This bypasses TLS entirely for the Claude Code → proxy hop.

**Use cases**: Logging request payloads, injecting headers, rate-limiting locally, replaying requests.

### Option 3: mitmproxy (Recommended)

[mitmproxy](https://mitmproxy.org) is the cleanest open-source solution. It provides a scriptable HTTPS proxy with a web UI and terminal interface.

```bash
# Install
brew install mitmproxy  # macOS
# or: pip install mitmproxy

# Start transparent proxy on port 8080
mitmproxy --listen-port 8080

# In a new terminal, point Claude Code at it
export NODE_EXTRA_CA_CERTS="$(python3 -c 'import mitmproxy.certs; print(mitmproxy.certs.Cert.default_ca_path())')"
export HTTPS_PROXY="http://localhost:8080"
claude
```

The mitmproxy web UI (`mitmweb`) at `http://localhost:8081` shows full request/response bodies — including the JSON payloads Claude Code sends to Anthropic.

**What you'll see**: System prompt, user messages, tool definitions, tool results, model parameters.

### Option 4: Minimal Python Logging Proxy

For a zero-dependency approach:

```python
# proxy.py — simple HTTPS logging proxy
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, json, sys

TARGET = "https://api.anthropic.com"

class LoggingProxy(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        print(json.dumps(json.loads(body), indent=2))  # Log request
        # Forward to Anthropic...

HTTPServer(("localhost", 8080), LoggingProxy).serve_forever()
```

```bash
python3 proxy.py &
export ANTHROPIC_API_URL="http://localhost:8080"
claude
```

> **Privacy note**: Proxied traffic includes everything in the conversation context — file contents Claude has read, your code, any secrets it encountered. Handle proxy logs accordingly.

---

## Patterns & Best Practices

### 1. Weekly Review

Set a calendar reminder to review weekly stats:

```bash
session-stats.sh --range week
```

Look for:
- Unusually high token usage days
- Repeated operations on same files (inefficiency signal)
- Project distribution (where time is spent)

### 2. Per-Project Tracking

Use `CLAUDE_SESSION_ID` to tag sessions by project:

```bash
export CLAUDE_SESSION_ID="project-myapp-$(date +%s)"
claude
```

### 3. Team Aggregation

For team-wide tracking, sync logs to shared storage:

```bash
# Example: sync to S3 daily
aws s3 sync ~/.claude/logs/ s3://company-claude-logs/$(whoami)/
```

Then aggregate with:

```bash
# Download all team logs
aws s3 sync s3://company-claude-logs/ /tmp/team-logs/

# Combine and analyze
cat /tmp/team-logs/*/activity-$(date +%Y-%m-%d).jsonl | \
  jq -s 'group_by(.project) | map({project: .[0].project, total_tokens: [.[].tokens.total] | add})'
```

### 4. Log Rotation

Logs accumulate over time. Add cleanup to cron:

```bash
# Clean logs older than 30 days
find ~/.claude/logs -name "*.jsonl" -mtime +30 -delete
```

---

## Limitations

### What This Monitoring CANNOT Do

| Limitation | Reason |
|------------|--------|
| **Exact token counts** | Claude Code CLI doesn't expose API token metrics |
| **TTFT (Time to First Token)** | Hook runs after tool completes, not during streaming |
| **Real-time streaming metrics** | No hook event during response generation |
| **Actual API costs** | Token estimates are heuristic, not from billing |
| **Model selection** | Log doesn't capture which model was used per request |
| **Context window usage** | No visibility into current context percentage |

### Accuracy Notes

- **Token estimates**: ~15-25% variance from actual billing
- **Cost estimates**: Use as directional guidance, not accounting
- **Session boundaries**: Sessions are approximated by ID, not exact API sessions

### What You CAN Trust

- **Tool usage counts**: Exact count of each tool invocation
- **File access patterns**: Which files were touched
- **Relative comparisons**: Day-to-day/project-to-project trends
- **Operation timing**: When tools were used (timestamp)

---

---

## Manager Audit Checklist

For engineering managers and team leads who need to verify Claude Code is being used appropriately within their team, these are the practical audit queries.

### Weekly Spot Check (5 minutes)

```bash
# Did anything unusual happen this week?

# 1. Files accessed outside project scope
find ~/.claude/projects/ -name "*.jsonl" -newer "$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)" 2>/dev/null | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Read") |
    .input.file_path' 2>/dev/null | \
  grep -v "^$(pwd)" | sort -u

# 2. Destructive commands run
find ~/.claude/projects/ -name "*.jsonl" -newer "$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)" 2>/dev/null | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Bash") |
    .input.command' 2>/dev/null | \
  grep -iE "(drop|delete|truncate|rm -rf|git push --force)"
```

### Compliance Reporting

For regulated environments, generate a summary of AI activity for auditors:

```bash
#!/bin/bash
# Monthly compliance report for Claude Code activity

START_DATE=${1:-$(date -d '30 days ago' +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)}
END_DATE=${2:-$(date +%Y-%m-%d)}
REPORT_FILE="ai-activity-report-${START_DATE}-${END_DATE}.json"

echo "Generating compliance report: $START_DATE to $END_DATE"

# Count sessions, tool calls, and file accesses
jq -s '{
  report_period: {start: "'"$START_DATE"'", end: "'"$END_DATE"'"},
  tool_usage: (group_by(.tool) | map({tool: .[0].tool, count: length})),
  unique_files_accessed: ([.[].file] | unique | length),
  sessions: ([.[].session_id] | unique | length)
}' ~/.claude/logs/activity-*.jsonl 2>/dev/null > "$REPORT_FILE" || \
  echo "No activity logs found. Set up session-logger.sh hook to enable."

echo "Report saved: $REPORT_FILE"
```

For a full governance setup with automatic audit trail logging, see [Enterprise AI Governance §6.2](../security/enterprise-governance.md#62-audit-trail-setup).

---

## Related Resources

- [Session Search Script](../examples/scripts/session-search.sh) - Fast session search & resume
- [Session Logger Hook](../examples/hooks/bash/session-logger.sh)
- [Stats Analysis Script](../examples/scripts/session-stats.sh)
- [Enterprise AI Governance](../security/enterprise-governance.md) - Org-level governance, audit trails, compliance
- [Third-Party Tools](../ecosystem/third-party-tools.md) - Community GUIs, TUIs, and dashboards (ccusage, ccburn, claude-code-viewer)
- [Data Privacy Guide](../security/data-privacy.md) - What data leaves your machine
- [Cost Optimization](./ultimate-guide.md#cost-optimization) - Tips to reduce spend
