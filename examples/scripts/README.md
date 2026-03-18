---
title: "Scripts"
description: "Utility scripts for Claude Code power users: audits, health checks, and session management"
tags: [template, debugging, security, workflows]
---

# Scripts

Utility scripts for Claude Code power users.

## Overview

| Script | Description |
|--------|-------------|
| `audit-scan.sh` | Security and quality audit of Claude Code setup |
| `check-claude.sh/.ps1` | Health check for Claude Code installation |
| `clean-reinstall-claude.sh/.ps1` | Clean reinstall of Claude Code |
| `fresh-context-loop.sh` | Run Claude Code in fresh context loops |
| `session-search.sh` | Search across Claude Code session histories |
| `cc-sessions.py` | Advanced session search with incremental indexing (Python) |
| `session-stats.sh` | Statistics about Claude Code sessions |
| `bridge.py` | Bridge: Claude Code → doobidoo → LM Studio |
| `bridge-plan-schema.json` | JSON Schema for bridge plan v1 format |
| `migrate-arguments-syntax.sh` | Migrate v1 → v2 slash command argument syntax (bash) |
| `migrate-arguments-syntax.ps1` | Migrate v1 → v2 slash command argument syntax (PowerShell) |
| `rtk-benchmark.sh` | Benchmark RTK token savings vs raw commands |
| `sync-claude-config.sh` | Sync Claude config files across machines |
| `sonnetplan.sh` | Run Claude with Sonnet replacing Opus (cost optimization alias) |
| `test-prompt-caching.ts` | Verify Anthropic prompt caching is active (no deps, fetch only) |
| `smart-suggest-roi.py` | Analyze acceptance rate of smart-suggest hook suggestions vs session activity |

---

## Bridge Script (Claude Code → LM Studio)

**Purpose**: Execute Claude Code plans locally via LM Studio for cost savings.

### Architecture

```
┌──────────────┐     store_memory      ┌─────────────────┐
│ Claude Code  │ ─────────────────────►│    doobidoo     │
│   (Opus)     │   tag: "plan"         │   SQLite + Vec  │
│   PLANNER    │   status: "pending"   │ ~/.mcp-memory-  │
└──────────────┘                       │  service/       │
                                       └────────┬────────┘
                                                │
                                                │ Direct SQLite read
                                                ▼
                                       ┌─────────────────┐
                                       │   bridge.py     │
                                       │                 │
                                       │ • PlanReader    │
                                       │ • StepExecutor  │
                                       │ • Validator     │
                                       └────────┬────────┘
                                                │
                                                │ HTTP POST
                                                │ /v1/chat/completions
                                                ▼
                                       ┌─────────────────┐
                                       │    LM Studio    │
                                       │  localhost:1234 │
                                       └─────────────────┘
```

### Requirements

```bash
pip install httpx
```

- **doobidoo MCP server** with SQLite backend (`~/.mcp-memory-service/`)
- **LM Studio** running on `localhost:1234` with a loaded model

### Usage

```bash
# Check LM Studio is running
python bridge.py --health

# List pending plans
python bridge.py --list

# Execute all pending plans
python bridge.py

# Execute specific plan
python bridge.py --plan plan_auth_refactor

# Verbose mode
python bridge.py -v
```

### Workflow

#### 1. Claude Code creates the plan

In Claude Code (Opus), store a plan via doobidoo:

```
store_memory("""
{
  "$schema": "bridge-plan-v1",
  "id": "plan_auth_refactor",
  "status": "pending",
  "context": {
    "project": "/path/to/project",
    "objective": "Refactor authentication to use JWT",
    "files_context": {
      "src/auth.py": "LOAD",
      "src/config.py": "REFERENCE"
    }
  },
  "steps": [
    {
      "id": 1,
      "type": "analysis",
      "description": "Analyze current auth implementation",
      "prompt": "Analyze the authentication code and identify migration points for JWT.",
      "validation": {"type": "non_empty"}
    },
    {
      "id": 2,
      "type": "code_generation",
      "description": "Generate JWT middleware",
      "prompt": "Generate a JWT authentication middleware based on the analysis.",
      "depends_on": [1],
      "validation": {"type": "syntax_check"},
      "file_output": "src/jwt_auth.py"
    }
  ]
}
""", tags=["plan"])
```

#### 2. Execute via bridge

```bash
python bridge.py
# Reads plan from doobidoo SQLite
# Executes each step via LM Studio
# Stores results back in doobidoo
```

#### 3. Retrieve results in Claude Code

```
search_by_tag(["result", "plan_auth_refactor"])
# Returns all execution results
```

### Plan Schema

See `bridge-plan-schema.json` for the complete JSON Schema.

| Field | Required | Description |
|-------|----------|-------------|
| `$schema` | Yes | Must be `"bridge-plan-v1"` |
| `id` | Yes | Unique plan ID (e.g., `plan_auth_refactor`) |
| `status` | Yes | `pending`, `in_progress`, `completed`, `failed` |
| `context.objective` | Yes | High-level goal description |
| `context.project` | No | Absolute path to project root |
| `context.files_context` | No | Files to inject (`LOAD`) or reference |
| `steps` | Yes | Array of execution steps |

### Step Types

| Type | Use Case |
|------|----------|
| `analysis` | Analyze code, identify patterns, plan changes |
| `code_generation` | Generate new code from scratch |
| `code_modification` | Modify existing code |
| `decision` | Make architectural or design decisions |

### Validation Types

| Type | Description |
|------|-------------|
| `non_empty` | Output is not empty (default) |
| `json` | Valid JSON output |
| `syntax_check` | Valid Python syntax |
| `contains_keys` | JSON contains specific keys |

### Failure Handling

| on_failure | Behavior |
|------------|----------|
| `retry_with_context` | Retry with error feedback (default) |
| `skip` | Skip step, continue execution |
| `halt` | Stop entire plan |

### Cost Savings

- **Planning** (Opus): ~$0.50-2.00 per complex plan
- **Execution** (LM Studio): Free (local)
- **ROI**: 80-90% cost reduction on implementation tasks

### Limitations

| Limitation | Mitigation |
|------------|------------|
| Local model quality varies | Strict validation + retries |
| No MCP tools in LM Studio | Inject file content in context |
| Limited context window | Truncate old results |
| No streaming | 120s timeout per step |

---

## Audit Scan

Security and quality audit of your Claude Code configuration.

```bash
./audit-scan.sh
```

Checks:
- Sensitive data in CLAUDE.md files
- Permission configurations
- MCP server security
- Hook script safety

---

## Health Check

Quick verification of Claude Code installation.

```bash
# macOS/Linux
./check-claude.sh

# Windows
./check-claude.ps1
```

---

## Clean Reinstall

Complete reinstall preserving configurations.

```bash
# macOS/Linux
./clean-reinstall-claude.sh

# Windows
./clean-reinstall-claude.ps1
```

---

## Fresh Context Loop

Run Claude Code with fresh context for long-running tasks.

```bash
./fresh-context-loop.sh --iterations 5 --project /path/to/project
```

---

## Session Search

Search across all Claude Code session histories.

```bash
./session-search.sh "authentication"
```

---

## Session Manager (Advanced)

Advanced CLI for session search, browse, resume & pattern discovery with incremental indexing.

**vs session-search.sh**: Faster search (~200ms vs ~400ms), partial ID resume, branch filter, worktree support, incremental JSONL index, and `discover` subcommand for automated config optimization.

**GitHub**: [FlorianBruniaux/cc-sessions](https://github.com/FlorianBruniaux/cc-sessions)

```bash
# Search in current project
cc-sessions search "notion"

# Search all projects
cc-sessions --all search "stripe"

# Filter by date and branch
cc-sessions search "auth" --since 7d --branch develop

# Recent sessions
cc-sessions recent 10

# Resume with partial ID
cc-sessions resume 8d472d

# JSON output for scripting
cc-sessions --json search "prisma" | jq -r '.[].id'

# Discover recurring patterns (n-gram, local, free)
cc-sessions --all discover

# Discover with semantic analysis via claude --print
cc-sessions --all discover --llm

# JSON output for scripting
cc-sessions --all discover --json | jq '.[] | select(.category == "skill")'
```

**Install from GitHub**:
```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/cc-sessions/main/cc-sessions \
  -o ~/.local/bin/cc-sessions && chmod +x ~/.local/bin/cc-sessions
```

**Or copy locally**: `cp cc-sessions.py ~/bin/cc-sessions && chmod +x ~/bin/cc-sessions`

> [GitHub repo](https://github.com/FlorianBruniaux/cc-sessions) · [Gist](https://gist.github.com/FlorianBruniaux/992d4d1107592d9e98ca9d89838871c6)

---

## Session Stats

Get statistics about your Claude Code usage.

```bash
./session-stats.sh
```
