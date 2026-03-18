---
title: "Third-Party Tools for Claude Code"
description: "Community tools for token tracking, session management, configuration, hook utilities, and alternative UIs"
tags: [reference, integration, plugin]
---

# Third-Party Tools for Claude Code

> Community tools for token tracking, session management, configuration, hook utilities, and alternative UIs.
>
> **Last verified**: March 2026

## Table of Contents

1. [About This Page](#about-this-page)
2. [Token & Cost Tracking](#token--cost-tracking)
3. [Session Management](#session-management)
4. [Configuration Management](#configuration-management)
5. [Engineering Standards Distribution](#engineering-standards-distribution)
6. [Hook Utilities](#hook-utilities)
7. [Alternative UIs](#alternative-uis)
8. [Multi-Agent Orchestration](#multi-agent-orchestration)
9. [Plugin Ecosystem](#plugin-ecosystem)
10. [Known Gaps](#known-gaps)
11. [Recommendations by Persona](#recommendations-by-persona)

---

## About This Page

This page catalogs **community-built tools that extend Claude Code**. Each tool has been verified against its public repository or package registry. Only tools with a public source (GitHub, npm, PyPI) are included.

**What this page is NOT**:
- Not a list of AI tools that complement Claude Code (see [AI Ecosystem](./ai-ecosystem.md))
- Not DIY monitoring scripts (see [Observability](../ops/observability.md))
- Not MCP server recommendations (see [MCP Servers Ecosystem](./mcp-servers-ecosystem.md))

---

## Token & Cost Tracking

### ccusage

The most mature cost tracking tool for Claude Code. Parses local session data to produce cost reports by day, month, session, or 5-hour billing window.

| Attribute | Details |
|-----------|---------|
| **Source** | [npm: ccusage](https://www.npmjs.com/package/ccusage) / [ccusage.com](https://ccusage.com) |
| **Install** | `bunx ccusage` (fastest) or `npx ccusage` |
| **Language** | TypeScript (Node.js 18+) |
| **Version** | 18.x (actively maintained) |

**Key features**:

- `ccusage daily` / `ccusage monthly` / `ccusage session` - aggregated cost reports
- `ccusage blocks --live` - real-time monitoring against 5-hour billing windows
- `--breakdown` flag for per-model cost split (Opus/Sonnet/Haiku)
- `--since` / `--until` date filtering
- JSON output (`--json`) for programmatic access
- Offline mode with cached pricing data
- MCP server integration (`@ccusage/mcp`)
- macOS widget (`ccusage-widget`) and [Raycast extension](https://www.raycast.com/nyatinte/ccusage)

**Limitations**: Relies on local JSONL parsing; cost estimates may differ from official Anthropic billing. No team aggregation without manual log merging.

> **Cross-ref**: The main guide covers basic ccusage commands at [ultimate-guide.md Section 2.4](./ultimate-guide.md) (cost monitoring).
> For DIY cost tracking with hooks, see [Observability](../ops/observability.md).

---

### ccburn

A Python TUI for visual token burn-rate tracking. Displays charts showing consumption rate relative to Claude's billing windows.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: JuanjoFuchs/ccburn](https://github.com/JuanjoFuchs/ccburn) / [Blog post](https://juanjofuchs.github.io/ai-development/2026/01/13/introducing-ccburn-visual-token-tracking.html) |
| **Install** | `pip install ccburn` |
| **Language** | Python 3.10+ (Rich + Plotext) |

**Key features**:

- Terminal charts showing token consumption over time
- Burn-rate indicators (on-track / slow-down warnings)
- Compact display mode
- Visual budget tracking against limits

**Limitations**: Python-only ecosystem. Smaller community than ccusage. No MCP integration.

**When to choose ccburn over ccusage**: If you prefer visual burn-rate charts over tabular reports, or if your toolchain is Python-based.

---

### Straude

A social dashboard for tracking and sharing Claude Code (and OpenAI Codex) usage stats. Push your daily token consumption and costs to a public leaderboard to track your streak, weekly spend, and global rank.

| Attribute | Details |
|-----------|---------|
| **Source** | [npm: straude](https://www.npmjs.com/package/straude) |
| **Website** | [straude.com](https://straude.com) |
| **Install** | `npx straude@latest` |
| **Language** | TypeScript (Node.js 18+) |
| **Version** | 0.1.9 (active development, created Feb 2026) |
| **Maintainer** | Community (oscar.hong2015@gmail.com) |

**Key features**:

- `straude` — smart sync: authenticate + push usage in one command
- `straude push --dry-run` — preview what would be submitted without sending
- `straude push --days N` — backfill last N days (max 7)
- `straude status` — streak, weekly spend, token totals, global rank
- Tracks both Claude Code (`ccusage`) and OpenAI Codex (`@ccusage/codex`)

**What is sent to the Straude server**:

Per day: cost in USD, token counts (input/output/cache creation/cache read), model names used (e.g. `claude-sonnet-4-6`), per-model cost breakdown. Plus: a SHA256 hash of the raw data, a random device UUID, and your machine hostname.

Your source code, API keys, and conversation content are **not** accessed or transmitted.

**Security notes**:

- Auth token stored in `~/.straude/config.json` with `0600` permissions (owner-only)
- Project is very young (created 2026-02-18, rapid iteration) — no public security audit
- Machine hostname is sent as `device_name`
- No published privacy policy as of March 2026
- Use `--dry-run` to verify what would be submitted before your first push

**When to choose Straude over ccusage/ccburn**:

Straude is the only tool in this list that is **social** — it uploads your stats to a shared platform. If you want a leaderboard, streak tracking, or to benchmark your usage against other developers, Straude is unique. If you want local-only cost visibility, ccusage or ccburn are better fits and carry no data-sharing implications.

> **Security reminder**: Before running any community CLI tool with `npx`, review its npm page and source for red flags. For Straude, the compiled source is readable and consistent with its stated purpose. See the [resource evaluation](../docs/resource-evaluations/straude-evaluation.md) for the full analysis.

---

### RTK (Rust Token Killer)

A CLI proxy that filters command outputs **before** they reach Claude's context. 446 stars, 38 forks, 700+ upvotes on r/ClaudeAI.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| **Website** | [rtk-ai.app](https://www.rtk-ai.app/) |
| **Install** | `brew install rtk-ai/tap/rtk` or `cargo install rtk` |
| **Language** | Rust (standalone binary) |
| **Version** | v0.28.0 |

**Key features**:

- `rtk git log` (92% reduction), `rtk git status` (76% reduction), `rtk git diff` (56% reduction)
- `rtk vitest run`, `rtk prisma`, `rtk pnpm` (70-90% reduction)
- `rtk python pytest`, `rtk mypy`, `rtk go test` (multi-language support)
- `rtk cargo test/build/clippy/nextest` (Rust toolchain)
- `rtk aws`, `rtk psql`, `rtk docker compose`, `rtk gt` (Graphite CLI)
- `rtk wc` - compact word/line/byte counts
- `rtk init --global` - hook-first install with settings.json auto-patch
- `rtk gain` / `rtk gain -p` - token savings analytics (global + per-project)
- **TOML Filter DSL**: add custom output filters for any command without writing Rust — `.rtk/filters.toml` (project) or `~/.config/rtk/filters.toml` (global), 33+ built-in filters
- `rtk rewrite` - single source of truth for hook command mapping (v0.25.0+, requires `rtk init --global` after upgrade)
- `exclude_commands` config to exclude specific commands from auto-rewriting

**When to choose RTK vs ccusage/ccburn**:

- RTK **reduces** token consumption (preprocessing)
- ccusage/ccburn **monitor** it (postprocessing)
- Use both together for maximum efficiency

**Limitations**: Not suitable for interactive commands or very small outputs (<100 chars).

> **Cross-ref**: Full docs at [ultimate-guide.md Section 9](./ultimate-guide.md#command-output-optimization-with-rtk)

---

## Session Management

### claude-code-viewer

A web-based UI for browsing and reading Claude Code conversation history (JSONL files).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: d-kimuson/claude-code-viewer](https://github.com/d-kimuson/claude-code-viewer) / [npm: @kimuson/claude-code-viewer](https://www.npmjs.com/package/@kimuson/claude-code-viewer) |
| **Install** | `npx @kimuson/claude-code-viewer` or `npm install -g @kimuson/claude-code-viewer` |
| **Language** | TypeScript (Node.js 18+) |
| **Version** | 0.5.x |

**Key features**:

- Project browser with session counts and metadata
- Full conversation display with syntax highlighting
- Tool usage results inline
- Real-time updates via Server-Sent Events (auto-refreshes when files change)
- Responsive design (desktop + mobile)

**Limitations**: Read-only (cannot edit or resume sessions). No cost data. Requires existing `~/.claude/projects/` history.

> **Cross-ref**: For session search from the CLI, see [session-search.sh](../examples/scripts/session-search.sh) in [Observability](../ops/observability.md).

---

ti### Entire CLI

Agent-native platform for Git-integrated session capture with rewindable checkpoints and governance layer.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: entireio/cli](https://github.com/entireio/cli) / [entire.io](https://entire.io) |
| **Install** | See GitHub (platform launched Feb 2026, early access) |
| **Language** | TypeScript |
| **Founded** | February 2026 by Thomas Dohmke (ex-GitHub CEO), $60M funding |

**Key features:**

- **Session Capture**: Automatic recording of AI agent sessions (Claude Code, Gemini CLI) with full context
- **Rewindable Checkpoints**: Restore to any session state with prompts + reasoning + file changes
- **Governance Layer**: Permission system, human approval gates, audit trails for compliance
- **Agent Handoffs**: Preserve context when switching between agents (Claude → Gemini)
- **Git Integration**: Stores checkpoints on separate `entire/checkpoints/v1` branch (no history pollution)
- **Multi-Agent Support**: Works with multiple AI agents simultaneously with context sharing

**Use cases:**

| Scenario | Why Entire CLI |
|----------|---------------|
| **Compliance (SOC2, HIPAA)** | Full audit trail: prompts → reasoning → outputs |
| **Multi-agent workflows** | Context preserved across agent switches |
| **Debugging AI decisions** | Rewind to checkpoint, inspect reasoning |
| **Governance** | Approval gates before production changes |
| **Team handoffs** | Resume sessions with full context |

**vs claude-code-viewer:**

| Feature | claude-code-viewer | Entire CLI |
|---------|-------------------|-----------|
| **Purpose** | Read-only history viewing | Active session management + replay |
| **Replay** | No | Yes (rewind to checkpoints) |
| **Context** | Conversation only | Prompts + reasoning + file states |
| **Governance** | No | Yes (approval gates, permissions) |
| **Multi-agent** | No | Yes (agent handoffs) |
| **Overhead** | None | ~5-10% storage |

**When to choose Entire over claude-code-viewer:**

- ✅ Need session replay/rewind functionality
- ✅ Enterprise compliance requirements (audit trails)
- ✅ Multi-agent workflows (Claude + Gemini)
- ✅ Governance gates (approval before deploy)
- ❌ Just want to browse history → Use claude-code-viewer (lighter)

**Limitations:**

- Very new (launched Feb 10-12, 2026) - limited production feedback
- Enterprise-focused (may be complex for solo developers)
- Storage overhead (~5-10% of project size for session data)
- macOS/Linux only (Windows via WSL)
- Early stage (v1.x) - expect API changes

**Delta vs common existing setups:**

| Need | Typical existing setup | What Entire adds |
|------|----------------------|-----------------|
| Tool call logging | Local JSONL (7-day rotation) | Reasoning + attribution %, Git-permanent |
| Human/AI attribution | Nothing | % per file, annotated per line, by model |
| Agent handoffs | Manual context copy | Context checkpoint auto-passed to next agent |
| Inter-dev handoff | Git commits/PRs | Shared readable checkpoints on `entire/checkpoints/v1` |
| Session persistence | Local only, ephemeral | Git-native, permanent, shareable |
| Governance | Custom pre-commit hooks | Policy-based approval gates + configurable audit export |

**Evaluation (2h spike recommended before team rollout):**

```bash
entire enable  # Install on throwaway branch

# After 2-3 normal sessions:
du -sh .git/refs/heads/entire/   # Storage per session → flag if > 10 MB
time git push                     # Push overhead → flag if > 5s
ls .git/hooks/                    # Verify no conflict with existing hooks
```

Stop criteria: checkpoint > 10 MB/session, push overhead > 5s, or hook conflicts.

> **Cross-ref**: Full Entire workflow with examples at [AI Traceability Guide](../ops/ai-traceability.md#51-entire-cli). For compliance use cases, see [Security Hardening](../security/security-hardening.md).

---

## Configuration Management

### claude-code-config

A TUI for managing `~/.claude.json` configuration, focused on MCP server management.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: joeyism/claude-code-config](https://github.com/joeyism/claude-code-config) |
| **Install** | `pip install claude-code-config` |
| **Language** | Python (Textual TUI) |

**Key features**:

- Visual MCP server management (add, edit, remove)
- Configuration file editing with validation
- TUI navigation for `~/.claude.json` structure

**Limitations**: Limited to `~/.claude.json` scope. Does not manage `.claude/settings.json`, hooks, or slash commands.

---

### AIBlueprint

A CLI that scaffolds pre-configured Claude Code setups with hooks, commands, statusline, and workflow automation.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: Melvynx/aiblueprint](https://github.com/Melvynx/aiblueprint) |
| **Install** | `npx aiblueprint-cli` |
| **Language** | TypeScript |

**Key features**:

- Pre-built security hooks
- Custom command templates
- Statusline configuration
- Workflow automation presets

**Limitations**: Opinionated configuration choices. Some features require a premium tier. Does not read existing config (scaffolds from scratch).

> **Cross-ref**: For manual Claude Code configuration, see [ultimate-guide.md Section 4](./ultimate-guide.md) (CLAUDE.md, settings, hooks, commands).

---

## Engineering Standards Distribution

Tools that solve the organizational-scale problem: keeping engineering standards in sync across dozens of repositories and multiple AI coding agents.

> **Context**: The guide covers CLAUDE.md authorship at the project level (Section 3 in the Ultimate Guide). The tools below address the next level — distributing and maintaining those standards across an entire engineering org.

### Packmind

An open-source "ContextOps" platform (Packmind's term for treating engineering context as a managed artifact with a lifecycle). Captures standards once, distributes as AI-readable context to every AI coding agent the team uses.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: PackmindHub/packmind](https://github.com/PackmindHub/packmind) |
| **Install** | `npx @packmind/cli init` |
| **License** | Apache-2.0 (CLI) — SaaS layer at packmind.com (pricing unspecified) |
| **Self-hosted** | Docker / Kubernetes |
| **Language** | TypeScript |

**Key features**:

- Single playbook → generates `CLAUDE.md` + slash commands + skills for Claude Code, `.cursor/rules/*.mdc` for Cursor, `.github/copilot-instructions.md` for Copilot, `AGENTS.md` for generic agents
- MCP server: create and manage standards directly from within a Claude Code session
- Continuous learning loop (claimed): bug fixed → root cause captured via Skill+MCP → playbook update proposed → human validates → distributed across repos
- Knowledge ingestion from team tools via MCP servers: GitHub PR comments, Slack, Jira, GitLab MRs, Confluence, Notion ([demo use cases](https://github.com/PackmindHub/demo-use-case-skills))

**Mental model**: Think of Packmind as the org-level version of the `.claude/rules/` modular pattern. Where `.claude/rules/*.md` keeps a single project consistent, Packmind keeps 40 repositories consistent — and syncs to every AI tool the team uses, not just Claude Code.

**Security note**: Centralizing CLAUDE.md distribution means a compromised Packmind repository can propagate malicious instructions to every developer's AI session simultaneously. Treat the Packmind configuration as a sensitive artifact, apply the same access controls as you would a secrets manager, and review proposed playbook updates carefully before merging.

> **Cross-ref**: For CLAUDE.md authorship at project scale, see [Section 3.5 — Team Configuration at Scale](../ultimate-guide.md#35-team-configuration-at-scale). For the Packmind MCP server, see [mcp-servers-ecosystem.md — Orchestration](./mcp-servers-ecosystem.md#orchestration).

---

## Hook Utilities

Tools that extend Claude Code's hook system with additional logic, conditional execution, or automation patterns. For DIY hook examples, see [the hooks section in the ultimate guide](../ultimate-guide.md).

### gitdiff-watcher

A Stop hook utility that enforces quality gates before Claude hands back control. Runs shell commands (build, tests, linting) only when relevant files have changed, making CLAUDE.md quality rules deterministic.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: fcamblor/gitdiff-watcher](https://github.com/fcamblor/gitdiff-watcher) |
| **Install** | `npx @fcamblor/gitdiff-watcher@0.1.0` (no global install needed) |
| **Language** | Node.js |
| **Version** | 0.1.0 — work in progress, APIs may change |
| **Author** | Florian Camblor |

**The problem it solves**: CLAUDE.md rules like "tests must pass before handoff" are non-deterministic. As context grows, these rules compete with recent tool outputs for the model's attention and can be deprioritized — so Claude sometimes returns control with broken code even when the rule is explicit. A Stop hook runs outside the LLM context, making it structurally impossible to skip.

**How it works**:

1. Takes a glob pattern (`--on`) and one or more shell commands (`--exec`)
2. On each Stop event, SHA-256 hashes all files matching the glob that appear in `git diff` (staged + unstaged)
3. Compares against the previous snapshot stored in `.claude/gitdiff-watcher.state.local.json`
4. If no relevant changes: exits 0 silently (no command runs)
5. If changes detected: runs all `--exec` commands
6. If any command fails (exit code 2): Claude receives the stderr and retries — the snapshot is NOT updated, so the check runs again next turn
7. On full success: updates the snapshot

**Example configuration** (`.claude/settings.json`):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npx @fcamblor/gitdiff-watcher@0.1.0 --on 'src/**/*.{ts,tsx}' --exec 'npm run build'",
            "timeout": 300,
            "statusMessage": "Checking TypeScript build..."
          },
          {
            "type": "command",
            "command": "npx @fcamblor/gitdiff-watcher@0.1.0 --on 'src/**/*.{ts,tsx}' --exec 'npm test -- --passWithNoTests'",
            "timeout": 300,
            "statusMessage": "Checking tests..."
          }
        ]
      }
    ]
  }
}
```

Multiple hooks run in parallel (Claude Code spawns one subagent per hook entry).

**Key behaviors**:

- **Conditional**: only fires when matching files changed — no wasted CI time on unrelated edits
- **Retry-safe**: failed runs preserve the snapshot, so the same check runs on the next attempt
- **Parallel**: multiple `--exec` commands within one hook entry run sequentially; use separate hook entries for parallel execution
- **Silent on no-op**: exits 0 without output when no relevant changes are detected

**Limitations**:

- v0.1.0 — explicitly "work in progress", CLI options and state file format may change
- Uses `git diff (staged + unstaged)` for file detection — files not tracked by git are not visible to the watcher
- Retry loops: a misconfigured check that always fails will cause Claude to retry indefinitely; add a `--exec-timeout` and ensure your commands have correct exit codes
- Each Stop hook failure starts a new Claude turn, consuming context — near the 200K limit, repeated failures accelerate context consumption

**When to use gitdiff-watcher vs a native Stop hook**:

The same quality gate can be written in ~20 lines of bash without gitdiff-watcher. Use gitdiff-watcher when you want the file-change conditional logic and state persistence without writing it yourself, or when you need parallel checks across a polyglot codebase (e.g., TypeScript build + Kotlin tests simultaneously).

> **Cross-ref**: Stop hook mechanics at [ultimate-guide.md hooks section](../ultimate-guide.md). For PostToolUse build checks (fires after every file edit, not at handoff), see the hooks section example at line ~8262.

---

## Alternative UIs

### Claude Chic

A styled terminal UI for Claude Code built on Anthropic's claude-agent-sdk. Replaces the default Claude Code TUI with a visually enhanced experience.

| Attribute | Details |
|-----------|---------|
| **Source** | [Blog: matthewrocklin.com](https://matthewrocklin.com/introducing-claude-chic/) / [PyPI: claudechic](https://pypi.org/project/claudechic/) |
| **Install** | `uvx claudechic` |
| **Language** | Python (Textual + claude-agent-sdk) |
| **Status** | Alpha |

**Key features**:

- Color-coded messages (orange: user, blue: Claude, grey: tools)
- Collapsible tool usage blocks
- Git worktree management from within the UI
- Multiple agents in a single window
- `/diff` viewer, vim keybindings (`/vim`), shell commands (`!ls`)
- Proper Markdown rendering with streaming

**Limitations**: Alpha status - expect breaking changes. Python dependency chain. Requires claude-agent-sdk. macOS/Linux only.

---

### Toad

A universal terminal frontend for AI coding agents. Supports Claude Code alongside Gemini CLI, OpenHands, Codex, and 12+ other agents via the Agent Client Protocol (ACP).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: batrachianai/toad](https://github.com/batrachianai/toad) / [willmcgugan.github.io/toad-released](https://willmcgugan.github.io/toad-released/) |
| **Install** | `curl -fsSL batrachian.ai/install \| sh` or `uv tool install -U batrachian-toad --python 3.14` |
| **Author** | Will McGugan (creator of Rich & Textual) |
| **Language** | Python (Textual) |

**Key features**:

- Unified interface across 12+ agent CLIs
- Full shell integration with tab completion
- `@` file context injection with fuzzy search
- Side-by-side diffs with syntax highlighting
- Jupyter-inspired block navigation
- Flicker-free character-level rendering

**Limitations**: macOS/Linux only (Windows via WSL). Agent support varies by ACP compatibility. No built-in session persistence yet (on roadmap).

---

### Conductor

A macOS desktop app for orchestrating multiple Claude Code (and Codex) instances in parallel using git worktrees, with integrated diff viewing, PR workflow, and GitHub automation.

| Attribute | Details |
|-----------|---------|
| **Source** | [conductor.build](https://conductor.build) |
| **Docs** | [docs.conductor.build](https://docs.conductor.build) |
| **Install** | Download from [conductor.build](https://conductor.build) |
| **Platform** | macOS only (Windows/Linux planned) |
| **Author** | Melty Labs |

**Workspace management**:

- One workspace per feature/bugfix, created with `⌘⇧N` or from a GitHub issue or Linear issue directly
- Workspaces organized by status: backlog → in progress → in review → done (v0.35.0)
- Group workspaces across multiple repos in a single view (v0.35.2)
- **Next Workspace** button (v0.36.4): jumps to the next workspace awaiting your input, so you never manually scan for blocked agents
- Archive completed workspaces while preserving full chat history

**Diff viewer & code editing**:

- Integrated diff viewer in the chat panel, turn-by-turn diffs per agent message (v0.22.0)
- Open diff with `⌘D`; navigate file-by-file without leaving Conductor
- **Manual Mode** (v0.37.0): built-in file editor with syntax highlighting and `⌘F` search — covers quick edits without opening a separate IDE
- Comment directly on diffs and send feedback to Claude (v0.10.0)

**GitHub & CI integration**:

- View GitHub Actions logs in the Checks tab (v0.33.2)
- Failing CI checks forwarded automatically to Claude for fixes (v0.12.0)
- Edit PR titles and descriptions directly in the Checks tab (v0.34.1)
- Sync PR comments from GitHub to Conductor (v0.25.4)
- Todos block workspace until checked off before merge (v0.28.4)
- Create PR with `⌘⇧P`

**Linear & other integrations**:

- Attach Linear issues to messages or open a Conductor workspace directly from a Linear issue (v0.15.0, v0.36.5)
- Deeplinks to Linear, Slack, VS Code within AI-generated responses
- Mermaid diagram support with pan/zoom and fullscreen

**Agent support**:

- Claude Code (default) + Codex side by side (v0.18.0); keyboard-navigable model picker
- Slash command autocomplete (e.g. `/restart` to restart Claude Code process)

**Reported workflow pattern (community)**:

Users working across 5+ parallel features on multiple repos report the following flow: create one workspace per feature (GitHub issue or Linear issue as context), let agents run, use the **Next Workspace** button to process only workspaces awaiting input, review diffs in-app, merge from the Checks tab. Reported combination with BMAD: one workspace per epic, one Claude agent for implementation and a second for the next story — described as a significant productivity multiplier for spec-driven development.

**Limitations**: macOS only (as of Mar 2026). Proprietary (not open source). Overlaps with multi-agent orchestration tools listed below.

---

### Claude Code GUI (VS Code Extension)

A third-party VS Code extension (not Anthropic's official extension) that adds a graphical layer on top of Claude Code.

| Attribute | Details |
|-----------|---------|
| **Source** | [VS Code Marketplace: MaheshKok.claude-code-gui](https://marketplace.visualstudio.com/items?itemName=MaheshKok.claude-code-gui) |
| **Install** | VS Code Marketplace → search "Claude Code GUI" |

**Note**: This is **not** the official [Claude Code for VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) extension by Anthropic. The official extension provides inline diffs, @-mentions, and plan review directly in the editor.

**Limitations**: Third-party, not Anthropic-maintained. Feature set may overlap with or lag behind the official extension.

---

## Multi-Agent Orchestration

This section covers tools for running **multiple Claude Code instances in parallel**. For detailed documentation, see:

- **[AI Ecosystem](./ai-ecosystem.md)** - Gas Town, multiclaude, agent-chat, claude-squad
- **[Ultimate Guide Section 9](./ultimate-guide.md)** - Multi-instance workflows, git worktrees, orchestration frameworks

**Quick reference**:

| Tool | Type | Key Feature |
|------|------|-------------|
| [Gas Town](https://github.com/steveyegge/gastown) | Multi-agent workspace | Steve Yegge's agent-first workspace manager |
| [multiclaude](https://github.com/dlorenc/multiclaude) | Multi-agent spawner | tmux + git worktrees (383+ stars) |
| [agent-chat](https://github.com/justinabrahms/agent-chat) | Monitoring UI | Real-time SSE monitoring for Gas Town/multiclaude |
| [Conductor](#conductor) | Desktop app | macOS parallel agents (also listed above) |

---

## External Orchestration Frameworks

> **Architectural distinction**: The tools above (Gas Town, multiclaude) run multiple Claude Code instances side by side. External orchestration frameworks go further — they replace or augment Claude Code's internal orchestration layer with their own runtime, adding swarm coordination, persistent memory, and specialized agent pools on top. Use native Claude Code capabilities (Task tool, sub-agents) first; reach for these frameworks when you've exhausted them.

### Ruflo (formerly claude-flow)

**GitHub**: [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo) — 18.9k stars (as of March 2026)
**npm**: `claude-flow` | **License**: MIT

The most adopted external orchestration framework for Claude Code. Transforms it into a multi-agent platform with hierarchical swarms (queen + workers), specialized agent pools (60+ agents: coders, testers, reviewers, architects...), and persistent memory via SQLite.

**Core features**:
- Q-Learning router directing tasks to the right agent based on past patterns
- 42+ built-in skills, 17 hooks integrating natively with Claude Code
- MCP server support for tool extension
- SQLite-backed session persistence with cross-agent memory sharing
- Non-interactive CI/CD mode

**Install** (inspect source before running):
```bash
npx ruflo@latest init --wizard
# Do NOT use the curl|bash variant — it pulls from the old repo name (claude-flow) and bypasses package manager security
```

> **Note on claims**: The project publishes performance metrics (SWE-Bench scores, speed multipliers) without published methodology. Treat as unverified until independently benchmarked.

> **Note on maturity**: Rebranded from claude-flow in early 2026. The transition is ongoing — verify npm package name and repo continuity before adopting in production.

**When to use**: When Claude Code's native Task tool and sub-agents are insufficient for your use case — typically complex multi-step pipelines requiring persistent state across many sessions, or workflows needing true parallel agent coordination beyond what `--dangerously-skip-permissions` + tmux achieves.

---

### Athena Flow

**GitHub**: [github.com/lespaceman/athena-flow](https://github.com/lespaceman/athena-flow) | **License**: MIT (claimed)
**Status**: Watch — published March 2026, not yet audited

A different architectural approach: instead of augmenting Claude Code's agent layer, Athena Flow sits at the **hooks layer**. It intercepts hook events via Unix Domain Socket (NDJSON), routes them through a persistent Node.js runtime, and provides a TUI for real-time observability and workflow control.

```
Claude Code → hook-forwarder → Unix Domain Socket → Athena Flow runtime → TUI
```

First shipped workflow: autonomous E2E test builder (Playwright CI-ready output). Roadmap: visual regression, API testing, Codex support.

**Not recommended yet** — source audit pending, project too new to assess stability. Revisit in 4-6 weeks.

---

### Pipelex + MTHDS

**GitHub**: [github.com/Pipelex/pipelex](https://github.com/Pipelex/pipelex) — 623 stars (Mars 2026)
**License**: MIT | **Language**: Python | **Standard**: [mthds.ai](https://mthds.ai)

> **Architectural distinction**: Pipelex n'orchestre pas des agents Claude Code — il fournit un **DSL déclaratif** (fichiers `.mthds`) pour définir des AI methods réutilisables. Là où Ruflo gère des swarms d'agents, Pipelex gère des pipelines multi-LLM typés et git-versionables.

Runtime Python pour le standard ouvert MTHDS. Une "AI method" est un workflow multi-étapes qui chaîne LLMs, OCR, et génération d'image — chaque étape typée et validée avant exécution. Les méthodes sont git-versionables, partageables via le hub communautaire [mthds.sh](https://mthds.sh), et peuvent être auto-générées par Claude Code.

**Intégration Claude Code** (Path A recommandé) :
```bash
pip install pipelex
npm install -g mthds
```
```
# Dans Claude Code :
/plugin marketplace add mthds-ai/skills
/plugin install mthds@mthds-ai-skills
/exit  # Relancer Claude Code

# Générer une méthode :
/mthds-build Analyse des CVs → scorecard + questions d'entretien

# Exécuter :
/mthds-run
```

**Cas d'usage** : workflows répétables à fort volume — traitement de documents, scoring de candidats, classification d'emails, analyse de contrats. Pas adapté à l'exploration créative open-ended où les agents natifs Claude Code restent plus appropriés.

**Status** : Watch — 8 mois d'existence, standard MTHDS pas encore validé à grande échelle. Surveiller la traction d'ici Q3 2026.

---

## Plugin Ecosystem

Claude Code's plugin system supports community-built extensions. For detailed documentation:

- **[Ultimate Guide Section 8](./ultimate-guide.md)** - Plugin system, commands, installation
- **[claude-plugins.dev](https://claude-plugins.dev)** - 11,989 plugins, 63,065 skills indexed
- **[claudemarketplaces.com](https://claudemarketplaces.com)** - Auto-scan GitHub for marketplace plugins
- **[agentskills.io](https://agentskills.io)** - Open standard for agent skills (26+ platforms)

**Notable skill packs**:
- **[gstack](https://github.com/garrytan/gstack)** — 6-skill workflow suite covering the full ship cycle: strategic product gate (`/plan-ceo-review`), architecture review (`/plan-eng-review`), paranoid code review (`/review`), automated release (`/ship`), native browser QA (`/browse`), and retrospective (`/retro`). Created by Garry Tan (Y Combinator CEO). See [Cognitive Mode Switching](../workflows/gstack-workflow.md) for the workflow pattern and adoption guide.

---

## Known Gaps

As of February 2026, the community tooling ecosystem has notable gaps:

| Gap | Description |
|-----|-------------|
| **Visual skills editor** | No GUI for creating/editing `.claude/skills/` — must edit YAML/Markdown manually |
| **Visual hooks editor** | No GUI for managing hooks in `settings.json` — requires JSON editing |
| **Unified admin panel** | No single dashboard combining config, sessions, cost, and MCP management |
| **Session replay** | ✅ **FILLED**: Entire CLI (launched Feb 2026) provides rewindable checkpoints with full context replay |
| **Agent-native issue tracking** | No established tool for markdown-based, git-committable issue tracking with Claude Code. [fp.dev](https://fp.dev/) is an early-stage solution (local-first, `/fp-plan` + `/fp-implement` skills, diff viewer) but lacks adoption signals and requires Apple Silicon for the desktop app. The Tasks API covers state persistence but issues aren't git-committable. |
| **Per-MCP-server profiler** | No way to measure token cost attributable to each MCP server individually |
| **Cross-platform config sync** | No tool syncs Claude Code config across machines (must manual copy `~/.claude/`) |

---

## Recommendations by Persona

| Persona | Recommended Tools | Rationale |
|---------|-------------------|-----------|
| **Solo developer** | ccusage + claude-code-viewer | Cost awareness + session history review |
| **Small team (2-5)** | ccusage + Conductor or multiclaude | Cost tracking + parallel development |
| **Enterprise** | ccusage (MCP) + custom dashboards | Programmatic cost data + audit trails |
| **Python-centric** | ccburn + Claude Chic | Native Python ecosystem tools |
| **Multi-agent user** | Toad or Conductor | Unified agent management |
| **Config-heavy setup** | claude-code-config + AIBlueprint | TUI config management + scaffolding |

---

## Related Resources

- [Observability](../ops/observability.md) - DIY session monitoring, logging hooks, cost tracking scripts
- [AI Ecosystem](./ai-ecosystem.md) - Complementary AI tools (Perplexity, Gemini, NotebookLM)
- [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) - Validated community MCP servers
- [Architecture](../core/architecture.md) - How Claude Code works internally
- [Ultimate Guide Section 8](./ultimate-guide.md) - Plugin system and marketplaces
