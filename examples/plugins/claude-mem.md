---
title: "claude-mem Plugin Template"
description: "Automatic persistent memory plugin capturing tool calls and decisions across sessions"
tags: [plugin, memory, integration]
---

# claude-mem Plugin Template

**Purpose**: Automatic persistent memory across Claude Code sessions
**Repository**: https://github.com/thedotmack/claude-mem
**Type**: Official plugin (26.5k+ stars)
**License**: AGPL-3.0 + PolyForm Noncommercial

---

## What It Does

claude-mem automatically captures **everything Claude does** during your coding sessions:
- Tool calls (Read, Edit, Bash, Grep, etc.)
- Observations and discoveries
- Architectural decisions
- File modifications

Then **intelligently injects** relevant context when you reconnect to the project.

**Result**: No more "what did we do last time?" → Claude remembers.

---

## Installation

### Via Plugin Marketplace (Recommended)

```bash
# Add marketplace
/plugin marketplace add thedotmack/claude-mem

# Install plugin
/plugin install claude-mem

# Restart Claude Code
exit
claude
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/thedotmack/claude-mem.git ~/.claude/plugins/claude-mem

# Install dependencies
cd ~/.claude/plugins/claude-mem
bun install

# Restart Claude Code
```

---

## Configuration

### Default Configuration

claude-mem works **out of the box** with sensible defaults:

```json
{
  "worker": {
    "port": 37777,
    "host": "localhost"
  },
  "storage": {
    "location": "~/.claude-mem/claude-mem.db",
    "backend": "sqlite"
  },
  "indexation": {
    "provider": "chroma",
    "embeddings": "claude"
  },
  "privacy": {
    "excludeTags": ["<private>", "</private>"]
  }
}
```

### Custom Configuration

Create `~/.claude-mem/config.json`:

```json
{
  "worker": {
    "port": 38888,
    "host": "localhost"
  },
  "compression": {
    "enabled": true,
    "summaryLength": "medium"
  },
  "privacy": {
    "excludeTags": ["<private>", "</private>", "<secret>", "</secret>"],
    "autoDetectSecrets": false
  },
  "storage": {
    "maxObservations": 10000,
    "retentionDays": 90
  }
}
```

**Options**:

| Option | Values | Description |
|--------|--------|-------------|
| `compression.enabled` | true/false | Enable AI compression (default: true) |
| `compression.summaryLength` | short/medium/long | Summary verbosity |
| `privacy.autoDetectSecrets` | true/false | Auto-detect API keys (default: false) |
| `storage.maxObservations` | number | Max observations to store |
| `storage.retentionDays` | number | Auto-delete after N days |

---

## Usage

### Automatic Capture (Default Behavior)

**No commands needed** — claude-mem automatically:

1. **Captures** tool usage via lifecycle hooks
2. **Compresses** observations with AI summaries
3. **Indexes** via Chroma vector database
4. **Injects** relevant context at session start

**Example Session Flow**:

```
Session 1 (Day 1):
User: "Explore auth module"
Claude: [Reads auth.service.ts, session.middleware.ts]
claude-mem: [Captures] "Auth exploration: JWT validation, session middleware"

Session 2 (Day 2):
Claude: [Auto-injected]
"Previously: Explored auth module.
 Files: auth.service.ts, session.middleware.ts
 Key finding: JWT validation in validateToken()"
User: "Refactor auth to use jose library"
Claude: [Already has context, no re-reading]
```

---

### Natural Language Search (Skill)

Search your session history using natural language:

```bash
# Search for specific topics
"Search my memory for authentication decisions"
"What files did we modify for the payment bug?"
"Remind me why we chose Zod over Yup"
"Show me all sessions where we worked on the API"
```

The skill returns:
- Matching sessions with summaries
- Relevant observations
- File modification history
- Architectural decisions

---

### Web Dashboard

Access real-time UI at `http://localhost:37777`:

```bash
# Open dashboard
open http://localhost:37777

# Features:
# - Timeline view (all sessions chronologically)
# - Natural language search bar
# - Observation details (tool calls + results)
# - Session statistics (duration, tool usage, files modified)
# - Export/import functionality
```

**Dashboard Sections**:

| Section | Description |
|---------|-------------|
| **Timeline** | Chronological view of all sessions |
| **Search** | Natural language query interface |
| **Sessions** | List view with filters |
| **Statistics** | Usage analytics and trends |
| **Settings** | Privacy controls, storage management |

---

### Privacy Controls

#### Using `<private>` Tags

```markdown
<!-- In your prompts -->
Modify the database connection to use:
<private>
Host: prod-db-123.aws.com
Username: admin
Password: super-secret-password
API Key: sk-1234567890abcdef
</private>

<!-- claude-mem excludes content between <private> tags -->
```

#### Manually Exclude Observations

```bash
# Delete specific observation
curl -X DELETE http://localhost:37777/api/observations/obs_123

# Clear all observations for a session
curl -X DELETE http://localhost:37777/api/sessions/session_456/observations
```

#### Data Location

```bash
# Database location
~/.claude-mem/claude-mem.db

# Chroma index
~/.claude-mem/chroma/

# View database size
du -sh ~/.claude-mem/
```

---

## Advanced Features

### Progressive Disclosure

claude-mem uses a 3-layer approach to minimize tokens:

```
Layer 1: Search (50-100 tokens)
├─ Query: "Find authentication work"
├─ Returns: 5 session summaries
│
Layer 2: Timeline (500-1000 tokens)
├─ Query: "Show session abc123 timeline"
├─ Returns: Observation list
│
Layer 3: Details (full context)
└─ Query: "Get observation obs_456 details"
    Returns: Complete tool call + result
```

**Token savings**: ~10x reduction vs loading full history.

---

### Endless Mode (Beta)

Experimental feature for extended sessions:

```bash
# Enable in config
{
  "experimental": {
    "endlessMode": true
  }
}
```

**Claims** (not independently verified):
- ~95% context reduction
- 20x more tool calls before hitting limits
- Aggressive compression + smart summarization

⚠️ **Note**: Beta feature, use with caution in production.

---

### Export/Import

**Export session history**:

```bash
# Via dashboard
http://localhost:37777/export

# Via CLI
curl http://localhost:37777/api/export > claude-mem-backup.json
```

**Import on another machine**:

```bash
# Via dashboard
http://localhost:37777/import

# Via CLI
curl -X POST http://localhost:37777/api/import \
  -H "Content-Type: application/json" \
  -d @claude-mem-backup.json
```

---

## Cost Considerations

### API Compression Costs

| Usage Level | Sessions/Month | Observations | Est. Cost |
|-------------|----------------|--------------|-----------|
| **Light** | 10-20 | 200-400 | $0.30-0.60 |
| **Medium** | 50-80 | 1000-1600 | $1.50-2.40 |
| **Heavy** | 100-150 | 2000-3000 | $3.00-4.50 |

**Formula**: ~$0.15 per 100 observations processed

**Reducing costs**:

```json
{
  "compression": {
    "batchSize": 50,
    "interval": "hourly"
  }
}
```

Batch compression (hourly) reduces API calls vs per-observation compression.

---

### Storage Costs

**Local storage** (SQLite + Chroma):

| Usage Level | Storage |
|-------------|---------|
| **Light** (10 sessions/week) | 10-20 MB/month |
| **Medium** (50 sessions/week) | 50-100 MB/month |
| **Heavy** (100 sessions/week) | 100-200 MB/month |

**Cleanup strategies**:

```json
{
  "storage": {
    "retentionDays": 90,
    "autoCleanup": true
  }
}
```

---

## Troubleshooting

### Dashboard Not Loading

```bash
# Check if worker is running
curl http://localhost:37777/health
# Expected: {"status":"ok"}

# Restart worker
claude-mem restart

# Check logs
tail -f ~/.claude-mem/logs/worker.log
```

---

### High API Costs

```bash
# Check observation count
curl http://localhost:37777/api/stats
# Returns: {"observations": 5234, "sessions": 123}

# If too many observations:
# 1. Enable batching
# 2. Increase compression interval
# 3. Lower retention days
```

---

### Memory Not Injected

```bash
# Verify indexation
curl http://localhost:37777/api/index/status
# Expected: {"indexed": true, "observations": 1234}

# Manually trigger re-indexation
curl -X POST http://localhost:37777/api/index/rebuild
```

---

### Database Corruption

```bash
# Backup first
cp ~/.claude-mem/claude-mem.db ~/.claude-mem/claude-mem.db.backup

# Rebuild index
claude-mem index rebuild

# If still broken, reset (⚠️ loses all data)
rm -rf ~/.claude-mem/
claude-mem init
```

---

## License Considerations

### AGPL-3.0

**What it means**:

- ✅ Free for personal use
- ✅ Free for open-source projects
- ⚠️ Network use = must disclose source
- ⚠️ Modifications = must disclose source
- ❌ Can't use in closed-source SaaS without compliance

**Commercial use**:

If using in commercial product:
1. Review AGPL-3.0 requirements
2. Consider legal compliance
3. Alternative: Contact author for commercial license

**PolyForm Noncommercial** (ragtime/ directory):
- Separate license for specific components
- Stricter commercial restrictions

---

## When to Use claude-mem

### ✅ Use When:

- Multi-session projects (>1 week)
- Need to remember decisions across days/weeks
- Frequently reconnect to same project
- Value automatic capture over manual note-taking
- Want web dashboard for exploration

### ❌ Don't Use When:

- One-off quick tasks (<10 minutes)
- Extremely sensitive data (consider manual Serena instead)
- Commercial projects without AGPL compliance review
- Need cross-machine sync (not supported natively)
- Budget constraints (<$5/month for API compression)

---

## Comparison to Alternatives

| Tool | Purpose | Capture | Query |
|------|---------|---------|-------|
| **claude-mem** | Session memory | Auto (hooks) | Natural language |
| **Serena** | Symbol memory | Manual (`write_memory`) | Key lookup |
| **grepai** | Semantic search | N/A (search only) | Semantic |
| **CLAUDE.md** | Project context | Manual (write file) | Claude reads on start |

**Best used together**:
- claude-mem: Automatic session capture
- Serena: Manual architectural decisions
- grepai: Code discovery
- CLAUDE.md: Project guidelines

---

## Resources

**Official**:
- [GitHub Repository](https://github.com/thedotmack/claude-mem)
- [Documentation](https://github.com/thedotmack/claude-mem/wiki)
- [Release Notes](https://github.com/thedotmack/claude-mem/releases)

**Guides**:
- [Corti.com: Deep Dive](https://corti.com/claude-mem-persistent-memory-for-ai-coding-assistants/)
- [yuv.ai: Setup Guide](https://yuv.ai/blog/claude-mem)
- [YouTube: 5-Minute Setup](https://www.youtube.com/watch?v=ryqpGVWRQxA)

**Community**:
- [GitHub Issues](https://github.com/thedotmack/claude-mem/issues)
- [GitHub Discussions](https://github.com/thedotmack/claude-mem/discussions)

---

**Template Version**: 1.0.0
**Last Updated**: 2026-02-10
**Guide Version**: 3.24.0
