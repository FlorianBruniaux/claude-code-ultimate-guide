# ccboard Activity Module — Implementation Plan

**Date**: 2026-02-21
**Status**: Draft
**Target repo**: [ccboard](https://github.com/FlorianBruniaux/ccboard)
**Triggered by**: User question on monitoring Claude Code file/command/network activity

---

## Context

ccboard currently covers session management, cost tracking, and basic stats. The missing layer is *activity auditing*: what files did Claude Code read, what commands did it execute, what URLs did it fetch?

Session JSONL files already contain this data — every `tool_use` block in `type: "assistant"` messages is a complete record of Claude Code's actions. The Activity module parses these and surfaces them in a dedicated Tab 10.

---

## Architecture

### New Files

```
ccboard-core/
├── src/
│   ├── parsers/
│   │   └── activity.rs          # Parse tool_use blocks from JSONL
│   └── models/
│       └── activity.rs          # Structs: ToolCall, FileAccess, BashCommand, NetworkCall, Alert

ccboard-tui/
└── src/
    └── tabs/
        └── activity.rs          # Tab 10 — TUI rendering

ccboard-web/
└── src/
    └── pages/
        └── activity.rs          # /activity route — Web UI rendering
```

### Modified Files

```
ccboard-core/src/db/schema.rs    # Add activity_events table
ccboard-core/src/db/queries.rs   # Add activity query functions
ccboard-tui/src/app.rs           # Register Tab 10
ccboard-web/src/router.rs        # Register /activity route
```

---

## Data Models

```rust
// ccboard-core/src/models/activity.rs

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ToolCall {
    pub id: String,
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub tool_name: String,
    pub input: serde_json::Value,
    pub duration_ms: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileAccess {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub path: String,
    pub operation: FileOperation,   // Read | Write | Edit | Glob | Grep
    pub line_range: Option<(usize, usize)>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum FileOperation {
    Read,
    Write,
    Edit,
    Glob,
    Grep,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BashCommand {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub command: String,
    pub is_destructive: bool,       // Heuristic: rm -rf, git push --force, etc.
    pub output_preview: String,     // First 200 chars of output
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkCall {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub url: String,
    pub tool: NetworkTool,          // WebFetch | WebSearch | McpCall
    pub domain: String,             // Extracted from URL
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NetworkTool {
    WebFetch,
    WebSearch,
    McpCall { server: String },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Alert {
    pub session_id: String,
    pub timestamp: DateTime<Utc>,
    pub severity: AlertSeverity,
    pub category: AlertCategory,
    pub detail: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AlertSeverity {
    Info,
    Warning,
    Critical,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AlertCategory {
    CredentialAccess,    // .env, *.pem, id_rsa
    DestructiveCommand,  // rm -rf, git push --force, DROP TABLE
    ExternalExfil,       // WebFetch to unknown domain
    ScopeViolation,      // Write outside project root
    ForcePush,           // git push --force
}
```

---

## Parser

```rust
// ccboard-core/src/parsers/activity.rs

pub fn parse_tool_calls(session_jsonl: &Path) -> Result<Vec<ToolCall>> {
    // 1. Stream-read JSONL (don't load entire file)
    // 2. Filter lines where .type == "assistant"
    // 3. Extract .message.content[].type == "tool_use" blocks
    // 4. Map to ToolCall structs
    // 5. Return Vec<ToolCall>
}

pub fn classify_tool_calls(calls: Vec<ToolCall>) -> ActivitySummary {
    // Fan out into typed collections
    ActivitySummary {
        file_accesses: extract_file_accesses(&calls),
        bash_commands: extract_bash_commands(&calls),
        network_calls: extract_network_calls(&calls),
        alerts: generate_alerts(&calls),
    }
}

fn is_destructive_command(cmd: &str) -> bool {
    let patterns = [
        "rm -rf", "rm -r ", "git push --force", "git push -f",
        "DROP TABLE", "DROP DATABASE", "truncate ", "git reset --hard",
        "git clean -f", "pkill", "kill -9",
    ];
    patterns.iter().any(|p| cmd.to_lowercase().contains(p))
}

fn is_sensitive_file(path: &str) -> bool {
    let patterns = [".env", ".pem", "id_rsa", "id_ed25519", ".p12",
                    "secrets.json", "credentials.json", ".npmrc", ".netrc"];
    patterns.iter().any(|p| path.contains(p))
}
```

---

## SQLite Schema

```sql
-- Add to ccboard-core/src/db/schema.rs migrations

CREATE TABLE IF NOT EXISTS activity_events (
    id          TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    timestamp   TEXT NOT NULL,
    tool_name   TEXT NOT NULL,
    input_json  TEXT NOT NULL,      -- Full tool input as JSON
    duration_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_activity_session ON activity_events(session_id);
CREATE INDEX IF NOT EXISTS idx_activity_tool    ON activity_events(tool_name);
CREATE INDEX IF NOT EXISTS idx_activity_ts      ON activity_events(timestamp);

CREATE TABLE IF NOT EXISTS activity_alerts (
    id          TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    timestamp   TEXT NOT NULL,
    severity    TEXT NOT NULL,      -- 'info' | 'warning' | 'critical'
    category    TEXT NOT NULL,
    detail      TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

---

## TUI Tab (Tab 10)

### Layout

```
┌─ Activity ─────────────────────────────────────────────────────────┐
│ Session: my-project / 2026-02-21 14:32  [←][→] navigate sessions  │
├─────────────────────────────────────────────────────────────────────┤
│ [Files 47] [Commands 12] [Network 3] [Alerts ⚠ 2] [Timeline]      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FILES                                                               │
│  14:32:01  READ   src/main.rs                                       │
│  14:32:04  READ   src/lib.rs                                        │
│  14:32:09  EDIT   src/main.rs          ← lines 45-67               │
│  14:32:15  WRITE  src/new_module.rs                                 │
│  14:32:20  READ   ⚠ .env              ← credential access          │
│                                                                      │
│  [j/k scroll] [Enter: expand] [f: filter] [a: alerts only]         │
└─────────────────────────────────────────────────────────────────────┘
```

### Tabs within Activity

| Sub-tab | Key | Content |
|---------|-----|---------|
| Files | `1` | File reads/writes/edits with path, timestamp, line range |
| Commands | `2` | Bash commands, destructive flag, output preview |
| Network | `3` | WebFetch URLs, MCP calls, domain list |
| Alerts | `4` | Auto-flagged events by severity |
| Timeline | `5` | Chronological view of all actions (merged) |

### Keybindings

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Switch sub-tabs |
| `j` / `k` | Scroll list |
| `Enter` | Expand item (full command / full path / response preview) |
| `f` | Filter by pattern |
| `a` | Jump to Alerts sub-tab |
| `s` | Jump to session picker |
| `/` | Search within current view |
| `y` | Copy selected item to clipboard |
| `e` | Export current view to JSON |

---

## Web UI Page (/activity)

```
GET /activity                    → Session picker → redirect to /activity?session=ID
GET /activity?session=ID         → Full activity view for session
GET /activity?session=ID&tab=files
GET /activity?session=ID&tab=commands
GET /activity?session=ID&tab=network
GET /activity?session=ID&tab=alerts
GET /activity?session=ID&tab=timeline

GET /api/activity/:session_id              → Full ActivitySummary JSON
GET /api/activity/:session_id/files        → Vec<FileAccess>
GET /api/activity/:session_id/commands     → Vec<BashCommand>
GET /api/activity/:session_id/network      → Vec<NetworkCall>
GET /api/activity/:session_id/alerts       → Vec<Alert>
GET /api/activity/:session_id/timeline     → Vec<ToolCall> sorted by timestamp
```

---

## Alert Detection Rules

| Rule | Condition | Severity |
|------|-----------|----------|
| Credential file access | `Read` path matches `*.env`, `*.pem`, `id_rsa`, `id_ed25519`, `secrets.json` | Warning |
| Destructive bash command | `Bash` input matches `rm -rf`, `git push --force`, `DROP TABLE`, `git reset --hard` | Critical |
| Force push | `Bash` input contains `git push` with `--force` or `-f` flag | Critical |
| External URL fetch | `WebFetch` URL domain not in project's known domains | Info |
| Write outside project root | `Write`/`Edit` path is outside `$PWD` at session start | Warning |
| Large file write | `Write` content size > 100KB | Info |
| Secrets in bash output | `Bash` output preview matches `sk-`, `ghp_`, `AKIA` (AWS key prefix) | Critical |

Alerts are generated at parse time and stored in `activity_alerts`. They do **not** block Claude Code — ccboard is read-only.

---

## Performance Constraints

### Requirements

- Startup time: < 2s for 1000+ sessions (same as current ccboard guarantee)
- JSONL parsing: lazy — only parse when session is selected, not on startup
- SQLite cache: parse once, cache `activity_events` by session_id + mtime. Invalidate on file change.
- Memory: stream JSONL line-by-line, never load full file

### Caching Strategy

```
Session selected
    → Check SQLite: activity_events WHERE session_id = ? AND mtime = file_mtime
    → Cache hit: return from DB (< 10ms)
    → Cache miss: parse JSONL → insert to DB → return (< 500ms for typical session)
```

### Index Strategy

Parse activity index (tool counts, alert counts) at startup alongside session metadata — same lazy-index pattern used for session list. Full detail only on demand.

```
Startup:
    For each session: read first/last line only → session metadata
    Do NOT parse tool_use blocks

On session select:
    Check SQLite cache → parse if stale → display
```

---

## Implementation Phases

### Phase 1: Parser + Models (1-2 days)

- [ ] `activity.rs` models
- [ ] `activity.rs` parser (stream JSONL, extract tool_use)
- [ ] Alert detection rules
- [ ] Unit tests for parser with fixture JSONL files

### Phase 2: SQLite Integration (1 day)

- [ ] Schema migration
- [ ] Cache queries (insert / select / invalidate)
- [ ] Benchmark: 1000 sessions cold start

### Phase 3: TUI Tab (2-3 days)

- [ ] Tab 10 registration in `app.rs`
- [ ] Files sub-tab rendering
- [ ] Commands sub-tab rendering
- [ ] Network sub-tab rendering
- [ ] Alerts sub-tab rendering
- [ ] Timeline sub-tab rendering
- [ ] Keybindings

### Phase 4: Web UI (1-2 days)

- [ ] API endpoints
- [ ] /activity page routing
- [ ] HTML rendering (same style as existing pages)

### Phase 5: Polish (1 day)

- [ ] Export to JSON (`e` key in TUI)
- [ ] Clipboard copy (`y` key)
- [ ] Filter (`f` key)
- [ ] Documentation update in ccboard README

---

## Out of Scope

- **Real-time monitoring** (watching live session as it runs) — future phase
- **Cross-session aggregation** (e.g., "all files read this week") — future phase
- **Alert notifications** (desktop/Slack notifications) — future phase
- **Blocking rules** (ccboard stays read-only, no Claude Code process interaction)

---

## Related

- `guide/observability.md` — Section "Activity Monitoring" and "External Monitoring Tools"
- `guide/data-privacy.md` — What leaves your machine and why
- ccboard README — Architecture and contribution guide
