# ICM Session Starter
> Paste this at the beginning of any Claude Code session to activate ICM context.
> Requires ICM installed and configured: `brew tap rtk-ai/tap && brew install icm`
> then `icm init --mode mcp && icm init --mode hook && icm init --mode skill`

---

# Context — ICM (Infinite Context Memory) active in this session

ICM is installed and configured on this machine. Use it to store and retrieve persistent
memory across sessions, bypassing context window limits.

## Available MCP tools

The `icm` MCP server is running. You have access to 22 `icm_*` tools for storing,
recalling, and managing persistent memory.

**Direct CLI** (via Bash if needed):

```bash
# Store a memory
icm store --topic "<project-slug>" --content "<fact>" --importance high|medium|low|critical

# Recall by semantic query
icm recall "<natural language query>"

# Inspect
icm stats          # count, topics, avg weight
icm topics         # list all topics
icm list           # list recent memories

# Manage
icm forget <id>    # delete by ID
icm decay          # apply temporal decay
icm prune          # remove low-weight entries
```

**Important (v0.5.0 syntax)**:
- `--importance` is an enum: `critical / high / medium / low` — not a float
- No `memory` subcommand — use `icm store`, `icm recall` directly
- Permanent knowledge graph: `icm memoir` (separate layer, no decay)

## Slash commands

- `/recall <query>` — search ICM memory
- `/remember <content>` — store a memory in ICM

## How memories work

Two layers:
- **Memories** (episodic): timestamped entries with temporal decay based on importance.
  `critical` importance never decays. `low` fades over time.
- **Memoir** (semantic): permanent knowledge graph with typed relations
  (`depends_on`, `contradicts`, `superseded_by`, `part_of`, and 5 others).

Search is hybrid: BM25 full-text (30%) + vector similarity (70%).

A `PostToolUse` hook runs automatically — every N tool calls, ICM extracts context
and stores it without any explicit action from you.

## Suggested usage in this session

```bash
# At session start — recall relevant context
icm recall "<current feature or topic>"

# When making a key decision
icm store --topic "<project>" --content "<decision and rationale>" --importance high

# For permanent architectural facts
icm memoir add-concept -m "<project>" -n "<concept>"
```

## DB location

`~/Library/Application Support/dev.icm.icm/memories.db`
