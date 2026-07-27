---
title: "Claude Code Community Tools: 40+ Extensions for Token Tracking, Context & Orchestration (2026)"
description: "40+ Claude Code extensions verified against public repos, with install commands and when-to-use comparisons: token tracking, context compression, orchestration, security scanning."
tags: [reference, integration, plugin, security]
---

# Claude Code Community Tools: 40+ Extensions Verified June 2026

This page catalogs community-built tools that extend Claude Code, organized by use case. Every entry has been verified against its public repository or package registry. For each category, the "When to use" comparison explains which tool fits which workflow, because the right choice depends on your stack and constraints, not just star count.

This is not a list of AI tools that complement Claude Code generally. It covers only tools whose primary purpose is extending the Claude Code CLI itself. For broader AI ecosystem coverage, see [AI Ecosystem](./ai-ecosystem.md). For MCP server recommendations, see [MCP Servers Ecosystem](./mcp-servers-ecosystem.md).

> **Last verified**: June 2026. 40+ tools across 17 categories.

## Table of Contents

1. [About This Page](#about-this-page)
2. [Token & Cost Tracking](#token--cost-tracking)
3. [Context Compression](#context-compression)
4. [Session Management](#session-management)
5. [Configuration Management](#configuration-management)
6. [Security Scanning](#security-scanning)
7. [Configuration Quality](#configuration-quality)
8. [Project Context Bootstrapping](#project-context-bootstrapping)
9. [Engineering Standards Distribution](#engineering-standards-distribution)
10. [Hook Utilities](#hook-utilities)
11. [Alternative UIs](#alternative-uis)
12. [Multi-Agent Orchestration](#multi-agent-orchestration)
13. [Knowledge Graph](#knowledge-graph)
14. [Plugin Ecosystem](#plugin-ecosystem)
15. [Skills Observability](#skills-observability)
16. [Known Gaps](#known-gaps)
17. [Recommendations by Persona](#recommendations-by-persona)

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

> **Cross-ref**: The main guide covers basic ccusage commands at [ultimate-guide.md Section 2.4](../ultimate-guide.md) (cost monitoring).
> For DIY cost tracking with hooks, see [Observability](../ops/observability.md).

---

### CodeBurn

CodeBurn reads the same `~/.claude/projects/` JSONL session logs as ccusage, but answers a different question. Where ccusage answers "how much did I spend?", CodeBurn answers "what did I spend it on?" by breaking token usage down by turn type and correlating spend with git history via its `yield` command.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: getagentseal/codeburn](https://github.com/getagentseal/codeburn) |
| **Install** | `npm install -g codeburn` or `npx codeburn` |
| **Stars** | 8,100+ (June 2026; third-party indexers may show ~2.7K due to update lag) |
| **Language** | Node.js 22.13+ |
| **Version** | v0.9.13 (June 14, 2026) |
| **Multi-provider** | Claude Code, Codex, Gemini CLI, Cursor, Cline/Roo |

**Key features**:

- `codeburn` - interactive TUI dashboard (last 7 days by default)
- `codeburn today` / `codeburn month` / `codeburn overview` / `codeburn report` - time-scoped summaries
- `codeburn optimize` - scans for waste patterns: retry loops, redundant re-reads, abandoned sessions
- `codeburn compare` - side-by-side model performance breakdown
- `codeburn yield` - correlates sessions with git commits (which sessions shipped code vs. which were abandoned or reverted)
- `codeburn models` - per-model token and cost breakdown
- `codeburn export` - CSV or JSON output
- `codeburn menubar` - macOS menu bar widget (SwiftBar)
- `codeburn plan set [claude-max|claude-pro|custom]` - subscription plan tracking
- MCP server (v0.9.12+): exposes usage and savings data to other agents

**Turn classification**: CodeBurn classifies every turn into 13 categories using local deterministic pattern matching (no LLM calls). Categories include Coding, Debugging, Refactoring, Testing, Exploration, Brainstorming, Planning, Feature Dev, Delegation, Git Ops, and Conversation. The most diagnostic finding in practice: "Conversation" turns (model responding without tool use) often account for 40-56% of session spend. Creator-reported examples include a JWT auth task where 5,200 of 15,600 tokens went to type corrections, and a PostgreSQL migration where 19,400 of 40,700 tokens went to foreign key debugging. These are illustrative data points, not reproducible benchmarks.

**Limitations**: Read-only, so it cannot interrupt a runaway session. Cost estimates use LiteLLM pricing rather than Anthropic billing API data, so figures can differ by $1-2/session from invoices. Format-dependent: an Anthropic JSONL schema change will break parsing until CodeBurn updates. Not listed in the awesome-claude-code registry.

**When to use CodeBurn vs ccusage**: ccusage is the right default for cost monitoring and billing-window tracking. CodeBurn adds forensic analysis: which turn types drive your spend, which sessions produced code that shipped, where retry loops inflate costs. Use both together.

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

> **Security reminder**: Before running any community CLI tool with `npx`, review its npm page and source for red flags. For Straude, the compiled source is readable and consistent with its stated purpose. See the [resource evaluation](../../docs/resource-evaluations/straude-evaluation.md) for the full analysis.

---

### RTK (Rust Token Killer)

A CLI proxy that filters command outputs **before** they reach Claude's context. 73,531 stars, 4,597 forks (GitHub API, 2026-07-27), up from 69,042 on 2026-07-07, 446 in March 2026, and 24,397 in April 2026, continuing the same steep growth curve that's worth checking against the full star-history graph before quoting in a high-stakes context.

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

> **Cross-ref**: Full docs at [ultimate-guide.md Section 9](#command-output-optimization-with-rtk)

---

### Claude Code Usage Monitor

Real-time usage monitor with burn-rate predictions and session-level warnings. The highest-starred dedicated monitoring tool for Claude Code as of May 2026, with approximately 7,955 stars (8,540 as of 2026-07-27).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) |
| **Install** | `npx ccusage@latest` (CLI) or web UI (see GitHub) |
| **Stars** | ~7,955 (May 2026) |

**Key features**:

- Tracks token consumption, message counts, and cost over 5-hour session billing windows
- Shows current burn rate and forecasts when the session limit will be reached
- Displays warnings before limits are hit, not after
- Works regardless of billing mode: parses local session files on disk rather than intercepting API traffic, so it covers both API key billing and Claude Max/Pro subscriptions equally

**When to choose over ccusage**: If you primarily want real-time warnings and a burn-rate forecast rather than historical reports and aggregated analytics. Both read the same local session files; the difference is the interface and emphasis.

---

### claude-spend

One-shot spend check for Claude Code sessions. The simplest entry point for occasional cost visibility without setting up a full monitoring dashboard.

| Attribute | Details |
|-----------|---------|
| **Install** | `npx claude-spend` |

**Key features**:

- Single command: no configuration required
- Reads local Claude Code session files (same source as ccusage)
- Shows per-conversation and per-model token consumption

**When to use**: Ad-hoc cost checks without committing to a persistent monitoring setup. For recurring tracking, ccusage provides more depth.

---

### cc-statistics

Cross-agent statistics dashboard that aggregates cost and token data across multiple AI coding tools in a single view.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: androidZzT/cc-statistics](https://github.com/androidZzT/cc-statistics) |
| **Stars** | 109 (GitHub API, 2026-07-07), up from 87 in May 2026, slow steady growth rather than a breakout |

**Key features**:

- Covers Claude Code, Gemini CLI, OpenAI Codex, and Cursor in one dashboard
- Costs, token counts, and efficiency metrics across agents
- Useful for teams running multiple AI tools who want a unified view

**When to use**: If your workflow spans more than one AI coding assistant and you want to compare cost and usage across them.

---

### claude-context-optimizer

Claude Code plugin focused on surfacing where context budget is actually going, rather than just reporting total spend.

| Attribute | Details |
|-----------|---------|
| **Stars** | ~48 (May 2026) |

**Key features**:

- Context heatmaps: visualizes which files and instructions consume the most tokens
- Wasted context detection: flags instructions that rarely influence model output
- Git-aware analysis: cross-references file context consumption against edit frequency to identify high-cost, low-edit files
- ROI reports and budget alerts

**When to use**: When you have a context efficiency problem (context growing too fast, adherence degrading) and need to identify the specific sources, rather than just the total size.

---

### A note on the Layer 4 billing blind spot

API-level gateways (Helicone, Portkey, Langfuse, Bifrost, Compresr) intercept HTTP calls and measure token usage at the API layer. This works well for applications calling the Anthropic API directly. It does not work for Claude Code Max or Pro subscriptions, because Claude Code connects directly to Anthropic servers using subscription credentials rather than an API key. There is no HTTP layer for a gateway to intercept.

All four tools above (Claude Code Usage Monitor, claude-spend, cc-statistics, claude-context-optimizer) work by parsing local session files that Claude Code writes to disk. This approach is billing-mode-agnostic: it works equally on API key billing and on Max/Pro subscriptions. If you are on a Max subscription and your gateway shows zero Claude Code traffic, that is expected behavior, not a misconfiguration.

---

## Context Compression

Tools that reduce tokens entering LLM context through compression, lazy-loading, or intelligent filtering — complementary to the tracking tools above.

### lean-ctx

A local-first context compression CLI and MCP server written in Rust. Installs once globally and activates in every Claude Code project without per-project configuration.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: yvgude/lean-ctx](https://github.com/yvgude/lean-ctx) |
| **Install** | `curl -fsSL https://raw.githubusercontent.com/yvgude/lean-ctx/main/skills/lean-ctx/scripts/install.sh \| bash && lean-ctx setup` |
| **Language** | Rust |
| **Stars** | ~1 366 |
| **Version** | v3.6.3 |

**How it works**

lean-ctx registers as a global MCP server (`~/.claude.json`) and installs three hooks in `~/.claude/settings.json` that fire on every tool call:

- `PreToolUse hook redirect` — intercepts native Read calls and routes them to `ctx_read` (AST parsing + file cache)
- `PreToolUse hook rewrite` — routes Bash calls through `ctx_shell` (pattern-based shell compression)
- `PostToolUse / SessionEnd hook observe` — feeds the CCP cross-session memory

**The 4 compression dimensions**

- **File reads with AST parsing**: tree-sitter parses TypeScript, Python, Rust, and 15 other languages. `signatures` mode returns only type and function signatures (no bodies). `map` mode returns exports and dependencies. A 2364-line `schema.prisma` compresses to ~200 tokens. Unchanged files are served from cache at ~13 tokens on re-read.
- **Shell output**: 60+ compression patterns specific to git, cargo, npm, docker, and kubectl. `git log -10 --stat` becomes 10 commit lines plus a single summary.
- **Cross-session memory (CCP — Context Continuity Protocol)**: stores a ~400-token session summary on exit. The next session loads it rather than cold-reading 50,000+ tokens of prior context.
- **Codebase graph**: SQLite-backed dependency graph built from tree-sitter imports/exports across 18 languages. `ctx_overview` uses it to score files by import centrality and surface the most connected modules first.

**Measured benchmarks (TypeScript/T3 monorepo, 2455 files)**

| Metric | Value |
|--------|-------|
| Overall compression rate | 57.8% |
| ctx_read savings rate | 86% |
| ctx_search savings rate | 72% |
| Tokens saved in one day | 1.3M |
| schema.prisma 2364L in signatures mode | ~200 tokens (99%) |
| File re-read (cache hit) | 13 tokens |

Results are lower on Markdown-heavy repos — the AST parser finds less structure to compress in documentation files than in TypeScript or Rust source.

**RTK vs lean-ctx: complementary layers**

Both tools reduce token consumption but operate at different points in the pipeline and do not conflict:

| Layer | Tool | What it compresses |
|-------|------|--------------------|
| CLI output (shell hook) | RTK | git, cargo, npm, tsc output text |
| File reads (MCP redirect) | lean-ctx | File content via AST + cache |
| Cross-session memory | lean-ctx | Session summaries via CCP |

RTK compresses shell output more aggressively (60-90% savings). lean-ctx's savings come almost entirely from file reads (86% of its total savings on measured sessions). Use both together.

**Monitoring**

```bash
lean-ctx gain           # dashboard: tokens saved, USD, top commands
lean-ctx gain --daily   # day-by-day breakdown
lean-ctx cep            # efficiency score /100 (compression, cache hit rate, consistency)
lean-ctx dashboard      # web UI at localhost:3333
```

A global `/lean-ctx-audit` slash command (`~/.claude/commands/lean-ctx-audit.md`) runs a full audit from within any session. See [context-engineering.md §12](../core/context-engineering.md#12-token-compression-tools) for the full tool comparison and setup guide.

**When to adopt lean-ctx**

Highest value on TypeScript, Rust, or Python projects where large files are read repeatedly within a session, sessions fill context before the task completes, or cross-session memory matters. Less impactful on documentation repos where most files are Markdown.

> **Note**: lean-ctx releases frequently. Run `lean-ctx setup` after upgrades to refresh hook and MCP registration. For shell output filtering only, RTK is the simpler starting point.

---

### tilth

An MCP server for structural code navigation, targeting the largest single token cost in a Claude Code session: file reads. Instead of loading full file contents, tilth exposes tree-sitter-powered tools the model calls explicitly to navigate code by shape rather than by text.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/jahala/tilth](https://github.com/jahala/tilth) |
| **Install** | `cargo install tilth` then `tilth install claude-code` |
| **Language** | Rust |
| **Architecture** | MCP server (installs into Claude Code) |
| **Parser** | tree-sitter (multi-language) |

**Key tools exposed to the model**:

- File read with auto-outline: large files return a structural skeleton with section names and line ranges; the model requests specific ranges on demand
- Symbol search: definitions, usages, and resolved callees in one call, replacing the grep-then-read loop
- `--callers`: all call sites of a symbol, structurally rather than via text search
- `--deps`: imports and dependents of a file, for understanding blast radius before a refactor
- `grok <symbol>`: signature, callers, callees, sibling functions, and associated tests for one symbol in one call
- Structural diff: changes summarized at the function level, not the line level
- Session dedup: symbols already shown in the current session are marked `[shown earlier]` instead of being re-expanded

**Benchmarks** (160 runs, 4 real repositories, metric = cost per correct answer):

| Model | Cost change | Accuracy change |
|-------|-------------|----------------|
| Sonnet 4.6 | -44% | 84% → 94% |
| Opus 4.6 | -39% | 91% → 92% |
| Haiku 4.5 | -38% | 54% → 73% |
| Average | -40% | 76% → 86% |

The benchmark metric is cost per correct answer, not tokens saved in isolation. This matters: a tool that saves tokens but degrades output quality provides no real value. tilth improves on both dimensions.

Why file reads are the right target: real-world billing data shows they account for approximately 65% of total token usage in a Claude Code session, versus roughly 12% for bash output. Tools that compress file reads move a larger share of the total cost than CLI output compressors can.

```bash
cargo install tilth
tilth install claude-code   # registers the MCP server in Claude Code
```

No per-project configuration is required after global install.

**Comparison with lean-ctx**: Both use tree-sitter to reduce file read token cost. lean-ctx works as a hook-level redirect that intercepts native Read calls transparently, requiring no change to model behavior. tilth exposes explicit navigation tools the model must call directly, giving it more control over what it fetches at the cost of requiring the model to use tilth's API rather than standard reads. Both approaches are valid; the right choice depends on whether you prefer passive compression or explicit navigation.

**When to use tilth**:

- TypeScript, Rust, or Python projects where large source files are read repeatedly
- Sessions where context fills before the task completes
- Codebases where call graph navigation (callers, callees, deps) is frequent
- When you want accuracy improvements alongside cost reduction, not just compression

---

### maki

A standalone TUI agent written in Rust (using ratatui) that replaces Claude Code entirely rather than augmenting it. maki is not a Claude Code plugin or MCP add-on; it is an alternative agent with its own interface and context management architecture.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/tontinton/maki](https://github.com/tontinton/maki) |
| **Language** | Rust (ratatui TUI) |
| **Architecture** | Standalone agent (replaces Claude Code) |
| **LLM providers** | Anthropic, OpenAI, Google, Copilot, Ollama, Mistral, DeepSeek, OpenRouter |

**Context efficiency tools built into maki**:

The `index` tool: tree-sitter skeleton with exact line ranges. Measured overhead per turn: +59 tokens (the index call itself). Measured saving per turn: -224 tokens on reads. Net: -165 tokens per turn. The maki README notes that bash output is only 12% of total token usage in a typical session, so RTK-style bash compression saves roughly 6% of total cost at best. File reads (65% of total) are where the larger gains are.

The `code_execution` tool: an embedded Python interpreter (monty) that can filter, transform, and aggregate data before it enters the context window. Instead of the model reading a raw file to count something, it writes and runs a script; only the result enters context.

The `task` tool: sub-agent delegation with dynamic model selection (haiku for simple subtasks, sonnet or opus for complex ones), keeping expensive model calls proportional to the reasoning actually required.

**Important distinction**: maki is architecturally separate from Claude Code. You cannot use maki as a Claude Code extension; choosing maki means replacing Claude Code for the sessions where you use it. Teams committed to the Claude Code ecosystem (hooks, skills, CLAUDE.md hierarchy, MCP registry) will not benefit from maki's internal tooling. maki is most relevant if you want a single tool that works across multiple LLM providers or prefer a self-contained Rust binary with no external dependencies.

**When to consider maki**:

- You work across multiple LLM providers and want a single interface
- You want fine-grained context management without installing separate MCP servers
- You are building or experimenting with agent architecture and want access to the internals

**When Claude Code remains the better fit**:

- You rely on Claude Code's hook system, skills, or CLAUDE.md path-scoping
- Your team shares MCP server configurations via `.mcp.json`
- You need Claude-specific features (extended thinking, Projects, memory systems)

---

### mcp2cli

A universal CLI bridge that converts any MCP server, OpenAPI spec, or GraphQL endpoint into shell commands — without injecting tool schemas into the LLM context. The key insight: most MCP clients push the full schema of every registered tool into context on every turn, whether the agent needs it or not. mcp2cli replaces that with lazy loading.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli) |
| **Install** | `uvx mcp2cli --help` (no-install) or `uv tool install mcp2cli` |
| **Language** | Python |
| **Stars** | ~1 900 |
| **Status** | Active (Show HN Best of March 2026) |

**How the lazy loading works**:

Instead of injecting full tool schemas (~44 000 tokens for a 43-tool GitHub MCP server), the agent:

1. Calls `mcp2cli --mcp <url> --list` → receives ~16 tokens per tool (name + short description)
2. Calls `mcp2cli --mcp <url> <tool-name> --help` → receives ~120 tokens (full schema, one tool)
3. Executes the tool with the right arguments

Full schemas never enter LLM context unless explicitly requested.

**Benchmarks** (independently reproduced by Firecrawl, Scalekit, CircleCI):

- GitHub MCP server (43 tools), simple task: 44 026 tokens (MCP native) vs 1 365 tokens (gh CLI / mcp2cli pattern) — 32× reduction
- Failure rate on the same tasks: MCP native 28%, CLI pattern 0% (context overflow = missed steps)
- 120 tools, 25 turns: MCP native injects ~362 000 tokens of schemas before any real work starts

**Key features**:

- **Multi-source**: MCP (HTTP/SSE/stdio), OpenAPI specs, GraphQL in one binary
- **Auth**: OAuth 2.1 with PKCE for interactive use, client credentials for CI/CD pipelines, cached token refresh
- **Daemon + connection pooling**: MCP connections take 2-5 seconds cold. The daemon keeps them warm for millisecond-latency reuse.
- **`--toon` format**: token-efficient output encoding that cuts response tokens 40-60% vs plain JSON
- **Semantic exit codes**: `validation_error`, `auth_failure`, `tool_error`, `connection_error` — shell scripts can branch without text parsing

```bash
# No-install test
uvx mcp2cli --mcp https://mcp.example.com/sse --list

# Execute a tool
mcp2cli --mcp https://mcp.example.com/sse search --query "test"

# Local stdio server
mcp2cli --mcp-stdio "npx @modelcontextprotocol/server-filesystem /tmp" --list

# OpenAPI spec
mcp2cli --spec ./openapi.json --base-url https://api.example.com list-pets

# Reusable config (baked alias)
mcp2cli bake create petstore --spec URL && mcp2cli @petstore --list
```

**When to use mcp2cli**:

- You use MCP servers with many tools (10+) and see context fill with schemas before any real work starts
- You want to debug or test an MCP server from the terminal without standing up a full client
- Your CI/CD pipeline consumes MCP tools programmatically

**When not to use it**:

- Enterprise multi-tenant contexts requiring per-user OAuth and audit logs — native MCP gateways handle this better
- Agents using well-known native CLIs (gh, git, kubectl): the model knows their interface from training data, no bridge needed
- Fewer than ~10 tools per server: the gain is real but not urgent

> **Naming caution**: at least four unrelated projects share the name "mcp2cli" on GitHub (Python, Go, Bun, and others). The reference implementation for this use case is [knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli). Verify the author before installing.

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

> **Cross-ref**: For session search from the CLI, see [session-search.sh](../../examples/scripts/session-search.sh) in [Observability](../ops/observability.md).

---

### agenttrace

A local TUI and report generator for inspecting AI coding-agent session history. It reads Claude Code JSONL logs alongside Codex CLI, Gemini CLI, Qwen Code, Cline, Aider, Cursor exports, OpenCode/OpenClaw, Hermes Agent, Pi, Oh My Pi, Kimi CLI, Copilot-style logs, and generic JSON/JSONL traces.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: luoyuctl/agenttrace](https://github.com/luoyuctl/agenttrace) |
| **Install** | `brew install luoyuctl/tap/agenttrace` or `go install github.com/luoyuctl/agenttrace/cmd/agenttrace@latest` |
| **Language** | Go |
| **License** | MIT |

**Key features**:

- Local dashboard for historical sessions, sorted by cost, tokens, elapsed time, and health
- Per-session diagnostics for tool failures, latency gaps, retry loops, large parameters, anomalies, and diffs
- JSON, Markdown, and HTML overview output for CI artifacts or team review
- CI gates for average health, critical sessions, and tool failure rate
- Demo mode (`agenttrace --demo`) for evaluating the UI before connecting local logs

**When to choose agenttrace over claude-code-viewer**:

- You need cost, latency, health, and failure diagnostics, not just conversation browsing
- You use multiple coding agents and want one local view across their session logs
- You want exportable reports or CI quality gates from session history

**Limitations**: It is a local inspection/reporting tool, not a live collaborative UI. Cost estimates depend on the model pricing data and token fields available in each agent log format.

---

### Entire CLI

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

> **Cross-ref**: For manual Claude Code configuration, see [ultimate-guide.md Section 4](../ultimate-guide.md) (CLAUDE.md, settings, hooks, commands).

---

### Claude Code Organizer

A web dashboard and MCP server for organizing Claude Code configs across the full scope hierarchy (Global > Workspace > Project).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: mcpware/claude-code-organizer](https://github.com/mcpware/claude-code-organizer) |
| **Install** | `npx @mcpware/claude-code-organizer` |
| **Language** | JavaScript (vanilla, zero dependencies) |
| **License** | MIT |

**Key features**:

- Scans 11 categories in `~/.claude/`: memories, skills, MCP servers, commands, agents, rules, configs, hooks, plugins, plans, sessions
- Visual scope inheritance tree showing what Claude loads per directory
- Drag-and-drop items between scopes with undo on every action
- Bulk operations (select multiple, move or delete at once)
- Real-time search and filter across all scopes
- MCP server mode (`--mcp`) so Claude can manage its own config programmatically

**Limitations**: No inline editing of config content yet. No Windows support. Dashboard is read-write for memories/skills/MCP but locked for hooks/plugins/configs.

---

## Security Scanning

Two complementary layers: tools that audit your Claude Code configuration for misconfigs, hook injection, and MCP risks; and agent-powered scanners that find logic-level vulnerabilities in the application code itself.

### AgentShield

A security scanner that grades your `.claude/` directory on a 0–100 scale (A–F) across 102 rules in 5 categories. Built at the Claude Code Hackathon (Cerebral Valley x Anthropic, Feb 2026).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: affaan-m/agentshield](https://github.com/affaan-m/agentshield) |
| **Install** | `npx ecc-agentshield scan` (zero-install) or `npm install -g ecc-agentshield` |
| **Language** | TypeScript (Node.js) |
| **License** | MIT |
| **Status** | Early-stage (released Feb 2026) — rules not independently audited |

**Key features**:

- **5 scan categories**: secrets (14 patterns: `sk-ant-`, `ghp_`, AWS, Stripe…), permissions (wildcard `Bash(*)`, missing deny lists), hooks (34 rules: command injection via `${var}`, data exfiltration, silent errors, reverse shells), MCP servers (23 rules: supply-chain, `npx -y`, remote transport), agents (25 rules: auto-run instructions, hidden Unicode directives, prompt reflection)
- **Auto-fix**: `agentshield scan --fix` — replaces hardcoded secrets with env var references
- **Multiple output formats**: terminal (default), JSON (`--format json`), Markdown, self-contained HTML
- **GitHub Action**: posts inline annotations on affected files, emits `score` and `grade` outputs, supports `fail-on-findings` threshold
- **Opus adversarial analysis** (`--opus --stream`): three-agent pipeline (Attacker → Defender → Auditor) using Opus 4.6 for deep threat modeling

```bash
# Scan your Claude Code config (no install required)
npx ecc-agentshield scan

# Auto-fix safe issues
agentshield scan --fix

# JSON output for CI
agentshield scan --format json

# Three-agent adversarial analysis (requires ANTHROPIC_API_KEY — incurs API cost)
agentshield scan --opus --stream
```

**GitHub Action**:

```yaml
- name: AgentShield Security Scan
  uses: affaan-m/agentshield@v1
  with:
    path: "."
    min-severity: "medium"
    fail-on-findings: "true"
```

**`runtimeConfidence` context**: findings are weighted by source — `active-runtime` (full weight) vs `template-example` (0.25x) vs `docs-example` (0.25x) — so a large MCP template catalog doesn't inflate the score like dozens of active servers.

**Limitations**:
- Rules are not independently audited — treat the grade as a useful signal, not a compliance certification
- `--opus` mode triggers Opus 4.6 API calls; budget accordingly before enabling in CI
- Project is 2 months old — API surface may evolve; pin to a specific version in production

> **See also**: [Security Hardening guide](../security/security-hardening.md) for manual hook and permission patterns.

### DeepSec

An agent-powered vulnerability scanner from Vercel Labs that finds logic-level security bugs in application code — the kind that regex-based SAST tools miss. Where AgentShield above audits your Claude Code configuration, DeepSec audits the application itself.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: vercel-labs/deepsec](https://github.com/vercel-labs/deepsec) |
| **Install** | `npx deepsec init` (bootstraps a `.deepsec/` directory at repo root) |
| **Language** | TypeScript |
| **License** | Apache 2.0 |
| **Status** | Vercel Labs — experimental, not production-ready |

**How it works**: DeepSec runs a 5-step pipeline. First a fast regex scan identifies sensitive zones (auth flows, crypto calls, user inputs). Then AI agents trace data flows through each candidate file and produce findings. A second agent pass revalidates those findings and consults git history to filter already-patched issues. Final output is structured Markdown or JSON, ready to paste into tickets.

**AI models used**: Claude Opus 4 with extended thinking (default) and GPT-5.5, via your existing Anthropic or OpenAI subscription. Vercel AI Gateway is recommended for production scans.

**False positive rate**: roughly 10–20% after the revalidation step.

```bash
# Initialize at repo root
npx deepsec init
cd .deepsec && pnpm install

# Run the full pipeline
pnpm deepsec scan       # fast regex pass
pnpm deepsec process    # AI agent investigation (slow, costs tokens)
pnpm deepsec triage     # P0/P1/P2 classification
pnpm deepsec revalidate # reduce false positives
pnpm deepsec export --format md-dir --out ./findings

# PR mode: scan only changed files (much cheaper)
pnpm deepsec process --diff

# Distributed mode for large monorepos (Vercel Sandboxes)
pnpm deepsec sandbox process --sandboxes 10 --concurrency 4
```

**When to use it**: DeepSec finds edge cases in authentication conditions and subtle data-flow issues that pattern-based tools won't surface. It's well-suited for a periodic deep audit on critical services or as a `--diff` gate on security-sensitive PRs — not as a per-commit scanner.

**Cost warning**: a full scan on a 50K-line codebase can cost $10–50 in Claude Opus tokens. Large monorepos can reach thousands of dollars. Run `--diff` mode for routine use; reserve full scans for targeted audits.

**Configuration**: create `.deepsec/INFO.md` (50–100 lines) documenting project-specific auth patterns and sensitive zones. Without it, agents reason without context and produce more false positives. A plugin system allows custom regex matchers aligned to your architecture.

**Security posture**: DeepSec has full shell access — treat it like a coding agent. Vercel recommends deploying in Sandbox microVMs (Firecracker) so API keys cannot be exfiltrated from worker processes.

> **See also**: [Vercel blog announcement](https://vercel.com/blog/introducing-deepsec-find-and-fix-vulnerabilities-in-your-code-base) for architecture details and real-world examples.

### SkillSpector

A security scanner from NVIDIA that vets skills before you install them. AgentShield audits your live config; DeepSec audits your application code. SkillSpector fills the gap that neither covers: static analysis of a skill file or repository before it touches your machine.

The motivation is concrete: a 2026 study (Liu et al.) on 42,447 skills from major marketplaces found 26.1% contained at least one vulnerability, and 5.2% showed likely malicious intent. Skills with executable scripts were 2.12x more likely to be vulnerable.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) |
| **Install** | `uv venv .venv && source .venv/bin/activate && make install` |
| **Language** | Python 3.12+ |
| **License** | Apache 2.0 |
| **Status** | Active (NVIDIA-maintained) |

**Detection coverage**

64 patterns across 16 categories. The categories most relevant to Claude Code users:

- **Prompt injection** (5 patterns): instruction overrides, hidden directives in comments, exfiltration commands, behavior manipulation, harmful content
- **Data exfiltration** (4 patterns): external transmission, env variable harvesting, file system enumeration, context leakage
- **MCP tool poisoning** (4 patterns): hidden instructions in metadata (HTML comments, zero-width chars, base64), unicode deception (homoglyphs, RTL overrides), parameter description injection, description-behavior mismatch
- **Trigger abuse** (3 patterns): overly broad trigger keywords, shadow commands (skill overriding a built-in), keyword baiting
- **Supply chain** (6 patterns): unpinned dependencies, `curl | bash` patterns, obfuscated/encoded execution, live CVE lookup via OSV.dev, abandoned packages, typosquatting
- **Rogue agent** (2 patterns): self-modification at runtime, unauthorized persistence via cron/startup scripts

The SC4 pattern is notable: it queries [OSV.dev](https://osv.dev) in real time to check declared dependencies against the full advisory database. No API key required; results are cached in-memory for 1 hour. Falls back to a static list if the network is unreachable.

**Two-stage pipeline**

Stage 1 is fast static analysis (regex + AST inspection on all files). Stage 2 is optional LLM semantic evaluation that filters false positives and adds human-readable explanations. The LLM prompt includes anti-jailbreak protections to prevent a malicious skill from manipulating its own audit.

```bash
# Scan a local skill directory (static only)
skillspector scan ./my-skill/ --no-llm

# Scan a GitHub repository
skillspector scan https://github.com/user/my-skill

# Scan a single SKILL.md
skillspector scan ./SKILL.md

# With LLM analysis (Anthropic)
export SKILLSPECTOR_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
skillspector scan ./my-skill/

# JSON output for scripting
skillspector scan ./my-skill/ --no-llm --format json --output report.json

# SARIF for IDE tooling and CI
skillspector scan ./my-skill/ --format sarif --output report.sarif
```

**Risk scoring**: CRITICAL findings add 50 points, HIGH add 25, MEDIUM add 10, LOW add 5. Skills containing executable scripts get a 1.3x multiplier. Scores above 50 trigger a "DO NOT INSTALL" recommendation.

**Docker option** for air-gapped environments or CI without Python:

```bash
docker build -t skillspector .
docker run --rm -v "$PWD:/scan" skillspector scan ./my-skill/ --no-llm
```

**When to use it**: before installing any skill from an unfamiliar source, especially those with executable scripts (`scripts/`, `.sh`, `.py` alongside the SKILL.md). Running with `--no-llm` takes a few seconds and catches the majority of supply-chain and exfiltration patterns. Enable LLM analysis for skills you're considering adding to a shared team setup.

**Reported precision**: ~87% after the LLM revalidation pass. Static-only mode has higher recall but more false positives on legitimate patterns like `subprocess` in build tools.

> **See also**: [NVIDIA SkillSpector README](https://github.com/NVIDIA/SkillSpector) for the full pattern catalog and Docker deployment guide.

---

## Configuration Quality

Tools that score, audit, and maintain the quality of existing AI agent configs over time — as opposed to creating them from scratch.

> **Context**: CLAUDE.md is not a one-time artifact. As a codebase evolves, the context it provides to the AI can drift: paths referenced no longer exist, domain knowledge becomes stale, new patterns emerge without being documented. The tools below address this maintenance layer.

### Caliber

A CLI that scores your AI agent config quality (0-100), generates tailored configs from codebase fingerprinting, and detects drift between your code and your CLAUDE.md. Works for Claude Code, Cursor, and Codex.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: rely-ai-org/caliber](https://github.com/rely-ai-org/caliber) |
| **Install** | `npx @rely-ai/caliber score` (zero-install) or `npm install -g @rely-ai/caliber` |
| **Language** | TypeScript (Node.js ≥20) |
| **License** | MIT |
| **Status** | Early-stage (released March 2026) — APIs may evolve |

**Key features**:

- **Local scoring**: deterministic 100-point rubric across 6 categories (Existence, Quality, Grounding, Accuracy, Freshness, Bonus) — no LLM calls, no API keys required
- **Drift detection**: git-based — detects when code commits outpace config updates; cache invalidates on tree signature or HEAD change
- **Config generation**: codebase fingerprinting (languages, frameworks, deps) → generates CLAUDE.md + MCP suggestions via your existing AI subscription (Claude Code seat, Cursor seat, or API key)
- **Review workflow**: score → propose → diff review → accept/decline → backup to `.caliber/backups/` → `caliber undo`
- **GitHub Action**: posts PR comments with score, grade, delta vs base branch; optional `fail-below` threshold blocks merge

```bash
# Score your current config (read-only, zero install)
npx @rely-ai/caliber score

# Generate or improve configs
npx @rely-ai/caliber init

# Detect drift after code changes
caliber refresh

# GitHub Action (fail PR if score < 75)
# uses: rely-ai-org/caliber@v1
# with: { fail-below: 75 }
```

**Score categories**:

| Category | Max | What it measures |
|----------|-----|-----------------|
| Existence | 25 | CLAUDE.md present, skills, MCP config, cross-platform parity |
| Quality | 25 | Token budget, code blocks, concreteness ratio, no duplicates |
| Grounding | 20 | % of project dirs/files referenced in config |
| Accuracy | 15 | Referenced paths exist on disk, commits since last config update |
| Freshness | 10 | Config staleness vs git history, no secrets |
| Bonus | 7 | Hooks configured, AGENTS.md, learned content present |

**Delta vs other config tools in this section**:

| Need | Existing tool | What Caliber adds |
|------|--------------|-------------------|
| Create config from scratch | AIBlueprint | — |
| Audit existing config quality | Nothing | Scored rubric + specific failing checks |
| Detect config drift from code | Nothing | Git-based drift detection |
| Distribute standards at org scale | Packmind | — |

**Limitations**: Early-stage tool (March 2026, ~65 stars at time of writing; the project has since rebranded to `ai-setup` under caliber-ai-org and reached 1,223 stars by 2026-07-27). Multi-tool support (Claude Code + Cursor + Codex + Copilot) may produce generically adequate configs rather than deeply Claude Code-specific ones. Scoring rubric is not exposed as a standalone document — the categories are deterministic but not user-visible without reading the source.

**Security note**: `caliber refresh` and `caliber watch` have write access to CLAUDE.md. Same risk class as Packmind: review generated output before accepting, particularly when using external sources (`caliber config`). Treat `.caliber/` config files with the same discipline as a secrets manager.

> **Cross-ref**: For scaffolding a config from scratch, see [AIBlueprint](#aiblueprint). For distributing and enforcing standards at org scale, see [Packmind](#packmind). For manual CLAUDE.md authorship, see [ultimate-guide.md Section 3](#31-memory-files-claudemd).

---

### context-evaluator

An OSS tool by Packmind that evaluates CLAUDE.md and AGENTS.md quality using 17 specialized AI evaluators. Available as a zero-install web app, pre-compiled binary, or Bun source install.

| Attribute | Details |
|-----------|---------|
| **Website** | [context-evaluator.ai](https://context-evaluator.ai) |
| **Source** | [GitHub: PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator) |
| **Install** | Zero-install at context-evaluator.ai, or binary from GitHub Releases |
| **Language** | TypeScript (Bun) + React frontend |
| **License** | MIT |
| **Status** | Active (Packmind experimental project, 2026) |

**Key features**:

- 17 evaluators split into 13 error types (existing issues) and 4 suggestion types (gaps from codebase analysis): content quality, structure/formatting, command completeness, testing guidance, security awareness, contradictory instructions, outdated paths, and more
- AGENTS.md and CLAUDE.md treated equivalently — works with Claude Code, Cursor, GitHub Copilot, and Codex formats
- Codebase fingerprinting: CLOC + folder analysis + config file detection runs first, so each evaluator prompt includes the project's actual languages, frameworks, and key folders. Issues are project-specific, not generic.
- **Unified mode**: when all files fit under 100K tokens, one agent evaluates them together and can detect cross-file contradictions. Above the threshold, agents run independently per file.
- **Automated remediation**: select issues from the web UI, choose a target format (Claude Code, Cursor, GitHub Copilot, Cursor), and the AI generates a `.patch` file. Apply manually with `git apply remediation.patch`. No changes committed without review.
- Multiple AI providers: Claude Code (default), Cursor, OpenCode, GitHub Copilot, OpenAI Codex

**Delta vs Caliber**:

| Feature | Caliber | context-evaluator |
|---------|---------|-------------------|
| No AI provider required | Yes (deterministic) | No (requires AI CLI) |
| Scoring rubric (0-100) | Yes | No |
| Git drift detection | Yes | No |
| LLM-based content review | No | Yes (17 evaluators) |
| Cross-file contradiction detection | No | Yes (unified mode) |
| Automated remediation (patch file) | No | Yes |
| Zero-install web version | No | Yes (context-evaluator.ai) |

**When to choose context-evaluator**:

- You want LLM-graded feedback on your CLAUDE.md's actual content, not a structural rubric
- Your config may have contradictory instructions, stale paths, or missing framework conventions that a deterministic score would not catch
- You want automated remediation with a reviewable diff (not an in-place rewrite)

**When to choose Caliber instead**:

- You need zero-LLM scoring for CI gates (`fail-below` threshold)
- You want git-based drift detection as code evolves

**Limitations**: Requires an AI provider with CLI access. Processing takes 1-3 minutes. No deterministic score for CI. No git drift detection.

> **Cross-ref**: For deterministic config scoring, see [Caliber](#caliber). For config generation from scratch, see [AIBlueprint](#aiblueprint). The Runtime Prompt Logging and Adaptive Unified/Parallel Mode patterns from this tool's source are documented in [Skill Design Patterns](../core/skill-design-patterns.md).

---

## Project Context Bootstrapping

Tools that compile structured codebase knowledge before a Claude Code session starts — so the AI understands routes, schema, dependencies, and high-impact files from the first message, without spending tokens on file exploration.

> **Context**: Claude Code explores a codebase by calling Glob, Grep, and Read. On large projects, this costs thousands of tokens before any real work begins. The tools below pre-compile that exploration into a single structured artifact (or a set of targeted wiki articles) that Claude reads once at session start. Think of it as "loading the project into RAM before the session opens."

### codesight

A zero-dependency CLI that analyzes a codebase via AST and generates structured context maps for Claude Code and other AI tools. Saves 7-12x tokens on base scan compared to manual file exploration; up to 83-131x with targeted wiki queries (self-reported on 3 production projects).

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: Houseofmvps/codesight](https://github.com/Houseofmvps/codesight) |
| **Install** | `npx codesight` (zero dependencies, zero config) |
| **Language** | TypeScript — borrows the TS compiler from your project when present |
| **License** | MIT |
| **Status** | Early-stage (released April 2026, ~386 stars at time of writing, 1,253 as of 2026-07-27), APIs may evolve |

**Core commands**:

```bash
# Scan current project — generates .codesight/ folder
npx codesight

# Generate wiki knowledge base (.codesight/wiki/) — targeted articles per topic
npx codesight --wiki

# Generate CLAUDE.md, .cursorrules, codex.md, AGENTS.md from project scan
npx codesight --init

# Show blast radius for a file (all files transitively affected by changing it)
npx codesight --blast src/lib/db.ts

# Start as MCP server (11 tools) — Claude calls it on demand
npx codesight --mcp

# Generate optimized config file for a specific AI tool
npx codesight --profile claude-code

# Watch mode — rescans on file changes
npx codesight --watch

# Open interactive HTML report in browser
npx codesight --open
```

**What gets generated**:

| File | Content |
|------|---------|
| `.codesight/CODESIGHT.md` | Combined context map — one file with full project understanding |
| `.codesight/routes.md` | Every API route with method, path, params, and what it touches (auth, db, cache, payments) |
| `.codesight/schema.md` | Every database model with fields, types, primary keys, foreign keys, relations |
| `.codesight/graph.md` | Import graph — which files import what, which files break the most things if changed |
| `.codesight/middleware.md` | Auth, rate limiting, CORS, validation, logging, error handlers |
| `.codesight/config.md` | Every env var (required vs default), config files, key dependencies |
| `.codesight/wiki/` | Persistent knowledge base: one article per topic (`auth.md`, `database.md`, `payments.md`, etc.) |

**Detection coverage**:

- Routes: 25+ frameworks auto-detected (Express, Hono, Fastify, NestJS, tRPC, FastAPI, and more)
- Schema: 10 ORMs (Drizzle, Prisma, TypeORM, Mongoose, SQLAlchemy, ActiveRecord, Ecto, Eloquent, Entity Framework, Sequelize)
- Components: React, Vue, Svelte, Flutter, SwiftUI
- Languages: TypeScript (full AST), JavaScript, Python, Go, Ruby, Elixir, Java, Kotlin, Rust, PHP, Dart, Swift, C# (regex fallback for non-TS)

**MCP integration** — once configured, Claude calls it directly without running `npx`:

```json
{
  "mcpServers": {
    "codesight": {
      "command": "npx",
      "args": ["codesight", "--mcp"]
    }
  }
}
```

Available MCP tools: `codesight_scan`, `codesight_get_wiki_index`, `codesight_get_wiki_article`, `codesight_get_routes`, `codesight_get_schema`, `codesight_get_blast_radius`, `codesight_get_hot_files`, `codesight_get_env`, `codesight_get_summary`, `codesight_lint_wiki`, `codesight_refresh`.

**How the wiki reduces token usage**:

| Question | Without wiki | With wiki |
|----------|-------------|-----------|
| "How does auth work?" | ~12K tokens (8+ file reads) | ~300 tokens (`auth.md`) |
| "What models exist?" | ~5K tokens (full CODESIGHT.md) | ~400 tokens (`database.md`) |
| New session start | ~5K tokens (full reload) | ~200 tokens (`index.md`) |

**At what scale to switch from CODESIGHT.md to wiki**: on small to medium projects (under ~1,500 files), loading `CODESIGHT.md` at session start via CLAUDE.md is practical. On large projects — a 1,700-file Next.js + tRPC monorepo generates a 35K-token CODESIGHT.md — loading the full file becomes counterproductive. Use `--wiki` + MCP server instead: Claude pulls one targeted article (~200-400 tokens) per question rather than loading the entire map upfront.

**Limitations and caveats**:

- Benchmarks are self-reported on 3 production projects — no independent verification at time of writing
- AST precision applies to TypeScript only; other languages use regex-based fallback
- `--init` generates a CLAUDE.md automatically — it can overwrite an existing one. Back up your CLAUDE.md before running this on a project with an established config
- Early-stage tool (April 2026): API surface may change across releases
- MongoDB projects correctly report 0 schema models (no SQL ORM declarations)
- Cloudflare Workers using raw HTTP handlers (no recognized framework) report 0 routes — the worker runtime falls outside the 25+ supported framework list
- Next.js App Router projects report 0 routes — file-based routing has no explicit route declarations for static analysis to parse; routes are inferred from file paths, not code patterns
- Rust projects produce near-empty output — no AST support, regex fallback captures only top-level module imports (`src/main.rs` → `mod X`); routes, structs, and business logic are invisible. Not useful on Rust codebases

**CI integration** (keeps context fresh on every push):

```yaml
name: codesight
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install -g codesight && codesight
      - uses: actions/upload-artifact@v4
        with:
          name: codesight
          path: .codesight/
```

> **Cross-ref**: For CLAUDE.md manual authorship and path-scoping, see [ultimate-guide.md Section 3](../ultimate-guide.md). For context window management strategies, see [context-engineering-tools.md](./context-engineering-tools.md). For MCP server configuration, see [mcp-servers-ecosystem.md](./mcp-servers-ecosystem.md).

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

> **Cross-ref**: For CLAUDE.md authorship at project scale, see [Section 3.5 — Team Configuration at Scale](#35-team-configuration-at-scale). For the Packmind MCP server, see [mcp-servers-ecosystem.md — Orchestration](./mcp-servers-ecosystem.md#orchestration).

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

### Agent Orchestrator (AO)

The open source, cross-platform equivalent of Conductor above: a desktop app and CLI that supervise multiple coding agent CLIs in parallel, each in its own git worktree, with an automatic feedback loop for CI failures, review comments, and merge conflicts.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/AgentWrapper/agent-orchestrator](https://github.com/AgentWrapper/agent-orchestrator) (renamed from `ComposioHQ/agent-orchestrator`, same repo) |
| **Install** | `npm install -g @aoagents/ao && ao start`, or desktop build for Windows/macOS/Linux |
| **License** | Apache-2.0 |
| **Platform** | Windows, macOS, Linux, plus a headless CLI mode |
| **Stars** | 8,100+ (July 2026, 5 months after creation) |

**What it adds over Conductor**: 23 supported agent CLI harnesses (Claude Code, Codex, Cursor, Aider, Goose, Devin, and 18 others) instead of 2, and it runs on any OS instead of macOS only. The core pattern is the same: isolated git worktree per session, a local daemon watching PR state, and automatic "nudges" sent back to the right agent session when CI fails, a reviewer comments, or a merge conflict appears.

**Two things worth knowing before adopting it**: the desktop app sends anonymized usage events (and redacted session recordings) to PostHog by default, disable it by setting `VITE_AO_POSTHOG_KEY` to an empty string before building. And despite some secondary coverage describing a "retry twice, then escalate to a human" mechanism for CI failures, that logic does not appear in the project's own README, architecture doc, or status doc as of July 2026, the documented behavior is a direct nudge back to the agent, not a bounded retry-then-escalate policy.

**When to choose AO over Conductor**: you're not on macOS, you use an agent CLI other than Claude Code or Codex, or you want the option to self-host without a proprietary desktop app. Conductor remains more polished and better integrated with Linear/Slack at this stage; AO is younger (416 open issues as of July 2026) and trades that maturity for openness and platform reach.

Full evaluation: [`docs/resource-evaluations/agent-orchestrator-composio.md`](../../docs/resource-evaluations/agent-orchestrator-composio.md).

---

### Piebald

A cross-platform desktop and web app for agentic AI development. Maintains full compatibility with Claude Code's hooks system and AGENTS.md conventions while adding multi-provider support and a full GUI environment.

| Attribute | Details |
|-----------|---------|
| **Source** | [piebald.ai](https://piebald.ai) / [docs.piebald.ai](https://docs.piebald.ai) |
| **GitHub** | [github.com/Piebald-AI](https://github.com/Piebald-AI) |
| **Platform** | Windows / macOS / Linux + Web |
| **Pricing** | Free (Basic) / $20/month (planned) |
| **Version** | v0.3.1 (May 2026) |

**Key features**:

- **Multi-provider**: Claude Pro/Max, GitHub Copilot, Amazon Bedrock, Google Antigravity, Qwen, and any OpenAI/Anthropic/Google-compatible endpoint — bring your own subscription
- **Claude Code compatibility**: Explicit support for hooks, AGENTS.md, MCP servers, permission modes, subagents, and chat compaction
- **Dev environment**: Git worktrees (first-class), integrated terminal, file browser, Git browser, and code editor (Pro)
- **Chat management**: Branching/forking, message queuing, slash commands, context management, desktop notifications
- **Configuration**: VS Code theme import, localization (i18n), color/font customization, web mode

**Windows gap**: All other "Alternative UIs" in this section are macOS/Linux only. Piebald is the only GUI option with native Windows support (no WSL required).

**Relation to Piebald-AI org**: The same team maintains [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — the most comprehensive public reverse-engineering of Claude Code's internal system prompts, cited throughout this guide.

**Limitations**: Proprietary, not open source. File browser and code editor require Pro tier.

**Note on Agent View**: Since v2.1.139, Claude Code has native multi-session management via `claude agents` (see [§9.17](#917-scaling-patterns-multi-instance-workflows)). Piebald remains the relevant choice for multi-provider workflows, Windows, and users who prefer a full GUI over the CLI.

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
- **[Ultimate Guide Section 9](../ultimate-guide.md)** - Multi-instance workflows, git worktrees, orchestration frameworks
- **[Agent Tools: Beyond Claude Code](./agentic-tools.md)** - Hermes Agent, Codex CLI, Devin, CrewAI, LangGraph, and other tools that are not Claude-Code-specific

**Quick reference**:

| Tool | Type | Key Feature |
|------|------|-------------|
| [Gas Town](https://github.com/steveyegge/gastown) | Multi-agent workspace | Steve Yegge's agent-first workspace manager |
| [multiclaude](https://github.com/dlorenc/multiclaude) | Multi-agent spawner | tmux + git worktrees (559 stars, 2026-07-27) |
| [agent-chat](https://github.com/justinabrahms/agent-chat) | Monitoring UI | Real-time SSE monitoring for Gas Town/multiclaude |
| [abtop](https://github.com/graykode/abtop) | Fleet TUI monitor | htop-style: tokens, context %, rate limits, ports, subagent tree (3,393 stars, 2026-07-27) |
| [Conductor](#conductor) | Desktop app | macOS parallel agents (also listed above) |
| [Piebald](#piebald) | Desktop/web app | Multi-provider + Windows + hooks compat (also listed above) |

---

### abtop

A Rust TUI that shows all active Claude Code and Codex CLI sessions in one screen — like htop, but for agent fleets.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: graykode/abtop](https://github.com/graykode/abtop) |
| **Install** | `curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh \| sh` or `cargo install abtop` |
| **Language** | Rust (ratatui) |
| **License** | MIT |
| **Platform** | macOS, Linux (WSL for Windows) |

**Key features**:

- Auto-discovery of Claude Code and Codex CLI sessions from local process/file state — no API key, no auth
- Per-session bars: token usage, context window %, rate limit quota
- Orphan port detection with one-key kill (`X`)
- Subagent tree (Claude Code only)
- tmux integration: press `Enter` to jump directly to the session pane
- `--once` flag for snapshot output (CI-friendly)
- `--setup` to install a rate-limit collection hook
- 10 built-in themes including 4 colorblind-friendly variants (`high-contrast`, `protanopia`, `deuteranopia`, `tritanopia`)

**Usage**:

```bash
abtop                    # Launch TUI (requires 120x40 terminal, degrades gracefully to 80x24)
abtop --once             # Print snapshot and exit
abtop --setup            # Install rate limit collection hook
abtop --theme dracula    # Launch with a specific theme
```

**Recommended setup with tmux**:

```bash
tmux new -s work
# pane 0: abtop
# pane 1: claude (project A)
# pane 2: claude (project B)
# Press Enter in abtop to jump to the active agent's pane
```

**Supported features by agent**:

| Feature | Claude Code | Codex CLI |
|---------|:-----------:|:---------:|
| Token tracking | ✅ | ✅ |
| Context window % | ✅ | ✅ |
| Rate limit | ✅ | ✅ |
| Subagents | ✅ | ❌ |
| Memory status | ✅ | ❌ |

> **When to use**: running 3+ concurrent agents across projects, hitting rate limits without knowing which session is responsible, or needing to spot orphaned ports left by a previous agent run.

---

## External Orchestration Frameworks

> **Architectural distinction**: The tools above (Gas Town, multiclaude) run multiple Claude Code instances side by side. External orchestration frameworks go further — they replace or augment Claude Code's internal orchestration layer with their own runtime, adding swarm coordination, persistent memory, and specialized agent pools on top. Use native Claude Code capabilities (Task tool, sub-agents) first; reach for these frameworks when you've exhausted them.

### Ruflo (formerly claude-flow)

**GitHub**: [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo) (66.3K stars as of 2026-07-27, up from 18.9K+ in March 2026)
**npm**: `ruflo` (formerly `claude-flow`) | **License**: MIT

The most adopted external orchestration framework for Claude Code. Transforms it into a multi-agent platform with hierarchical swarms (queen + workers), 98 specialized agents (coders, testers, reviewers, architects, security auditors), and persistent memory via SQLite (AgentDB).

**Two install paths** (very different surface areas):

| | Plugin path | CLI path |
|---|---|---|
| What you get | Slash commands + agent definitions per plugin | Full loop: 98 agents, 30 skills, MCP server, hooks, daemon |
| Files in workspace | Zero | `.claude/`, `.claude-flow/`, `CLAUDE.md`, helpers, settings |
| MCP server registered | No | Yes (`memory_store`, `swarm_init`, `agent_spawn`, etc.) |
| Best for | Trying a single plugin without committing | Production use |

```bash
# Plugin path
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo    # or any of the 33 available plugins

# CLI path (full install — inspect source first)
npx ruflo@latest init wizard
# Do NOT use the curl|bash variant: it pulls from the old repo name (claude-flow) and bypasses package manager security
```

**Core features**:
- Q-Learning router directing tasks to the right agent based on past patterns
- 30+ built-in skills, 27 hooks integrating natively with Claude Code
- MCP server with 314 tools (CLI path only)
- SQLite-backed session persistence with cross-agent memory sharing (AgentDB)
- **Agent federation**: zero-trust cross-machine collaboration via mTLS and ed25519 identity, with PII stripped before egress and behavioral trust scoring per peer. Unlike LangGraph or CrewAI (single-instance by default), Ruflo agents can coordinate across machines and organizations without sharing raw data. Controlled via 9 MCP tools and 10 CLI commands.
- 33 native plugins at the Claude Code marketplace (swarm, RAG memory, security, browser testing, IoT, and more)
- Optional web UI at [flo.ruv.io](https://flo.ruv.io/) and a GOAP goal planner at [goal.ruv.io](https://goal.ruv.io/)
- Non-interactive CI/CD mode

> **Note on claims**: The project publishes performance metrics (SWE-Bench scores, speed multipliers, 22M+ ecosystem downloads) without fully independent methodology. A SOTA benchmark gist comparing against LangGraph, AutoGen, and CrewAI exists but independent reproduction is not confirmed. Treat all figures as unverified.

> **Note on maturity**: Rebranded from claude-flow in early 2026. The npm package is now `ruflo` (confirmed). Inspect the source before deploying in production.

**When to use**: When Claude Code's native Task tool and sub-agents are insufficient, typically for complex multi-step pipelines requiring persistent state across many sessions, or for teams needing agents to coordinate across machines via federation.

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

**GitHub**: [github.com/Pipelex/pipelex](https://github.com/Pipelex/pipelex), 693 stars (2026-07-27, was 623 in March 2026)
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

## Knowledge Graph

### Graphify

A CLI tool that maps a codebase (plus any mix of docs, PDFs, images, and videos) into a queryable knowledge graph. Instead of asking Claude Code to re-read files every session to understand structure, you build the graph once and query it. The payoff: far fewer tokens spent on orientation, and surfaced connections that grep and manual browsing miss.

**GitHub**: [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)
**PyPI**: `graphifyy` (note the double-y — the single-y package is a different, unrelated project)
**License**: MIT | **Language**: Python 3.10+

| Attribute | Details |
|-----------|---------|
| **Install** | `uv tool install graphifyy` (recommended) or `pipx install graphifyy` |
| **Platforms** | Claude Code, Cursor, Copilot CLI, Aider, Codex, Gemini CLI, OpenCode, and 8+ more |
| **Verified** | May 2026 (v0.8.9) |

**Outputs per run:**

| File | Contents |
|------|---------|
| `graphify-out/graph.html` | Interactive visualization with clickable nodes and filtering |
| `graphify-out/GRAPH_REPORT.md` | Key concepts, surprising connections, suggested questions |
| `graphify-out/graph.json` | Structured graph data reused on every query |

**Under the hood — cache files in `graphify-out/`:**

Beyond the 3 public files, Graphify keeps a cache layer that powers incremental rebuilds. These hidden files appear after the first run:

| File | Role |
|------|------|
| `.graphify_ast.json` | Raw AST from tree-sitter — all code, no API call, often 15-20 MB |
| `.graphify_detect.json` | Output of `collect_files()` — the full file manifest |
| `.graphify_chunk_XX.json` | Batches of files sent to the AI API for semantic extraction |
| `.chunk_manifest_XX.json` | Which files belong to each chunk — used by `--update` to isolate changes |
| `.graphify_semantic.json` | Semantic embeddings after entity deduplication |
| `.graphify_uncached.txt` | Files not yet cached in the last run |
| `cache/` | Content hashes per file for change detection |

On `--update`: Graphify compares current content hashes against the cache, identifies which files changed, re-processes only their chunks via the AI API, then reconstructs `graph.json` from unchanged chunks plus the new ones. Files that haven't changed cost zero API tokens.

**Init in a project:**

```bash
# 1. Build the graph from project root
graphify .

# 2. Register with Claude Code — installs the /graphify skill
graphify install --platform claude

# 3. Commit the output so teammates start with a pre-built map
git add graphify-out/ && git commit -m "chore: add graphify knowledge graph"
# Or exclude it entirely: echo "graphify-out/" >> .gitignore

# 4. Subsequent runs: --update uses semantic caching by content hash
#    Only changed files get re-processed — saves API cost on large repos
graphify . --update
```

**Querying the graph:**

```bash
graphify query "what connects auth to the database?"
graphify path "UserService" "DatabasePool"
```

Once registered with Claude Code, the installed skill lets Claude read `graph.json` directly instead of crawling files — so queries happen inside the conversation without re-reading source.

**Key analytical features:**

- **God nodes**: highly-connected architectural hubs — the components that everything else depends on
- **Surprising connections**: cross-module links ranked by an unexpectedness score
- **Design rationale extraction**: pulls the WHY from inline comments and docstrings, not just the WHAT
- **Confidence tagging**: every relationship is tagged `EXTRACTED` (explicit import/call), `INFERRED` (deduced from context), or `AMBIGUOUS` (flagged for review)

**File support**: 31 programming languages, Markdown, RST, YAML, HTML, PDFs. Videos and audio: `pip install graphifyy[video]` (local faster-whisper, no external API call). Office documents: `pip install graphifyy[office]`.

**MCP server mode:**

```bash
# Exposes: query, shortest_path, god_nodes, neighbor_traversal tools
graphify mcp
```

For large codebases (graph.json above ~5 MB), MCP mode is significantly more efficient. Without it, Claude loads `GRAPH_REPORT.md` first for orientation, then pulls targeted sections of `graph.json` as needed. With MCP running, Claude calls `god_nodes`, `query "auth flow"`, or `shortest_path` directly and receives only the relevant subgraph — no full graph load into context. A 22 MB `graph.json` loaded in full costs far more tokens than 4-5 targeted MCP tool calls returning the same answer.

**How Claude uses the installed skill:**

After `graphify install --platform claude`, the skill injects a rule: if `graphify-out/` exists in the current project, treat architecture questions as graph queries rather than file reads. The resolution order in practice:

1. Claude reads `GRAPH_REPORT.md` first — compact (typically 150-200 KB), gives orientation on god nodes and surprising connections
2. For specific queries, Claude consults targeted sections of `graph.json`
3. With MCP server running: Claude calls `query`, `shortest_path`, `god_nodes`, or `neighbor_traversal` tools directly — far cheaper at scale

Without Graphify: Claude re-reads source files every session to understand structure, burning tokens on orientation. With Graphify: that cost is paid once at build time, then amortized across all sessions.

**Additional exports**: Wikipedia-style wiki with cross-community wikilinks, Obsidian vault with Canvas layouts, D3 collapsible-tree HTML, Mermaid call-flow diagrams with interactive zoom/pan, Neo4j graph push.

**Privacy**: Code files are processed locally via tree-sitter, no API calls for code analysis. Documents and PDFs are sent to your configured AI model API. For fully local inference: `pip install graphifyy[ollama]`.

**Team workflow**: Committing `graphify-out/` to git gives every teammate a shared map on clone. Graphify ships a git merge driver that prevents conflict markers in `graph.json`, and optional git hooks for automatic rebuilds on commit.

**Pipeline:** `detect() → extract() → build_graph() → cluster() → analyze() → report() → export()` — each stage isolated, no shared state. Adding a language requires registering an extractor in `extract.py` plus tree-sitter dependencies.

**Limitations:**

- Package name `graphifyy` (double-y) is the main friction point — `pip install graphify` installs an unrelated tool without any error
- Doc/PDF extraction makes AI API calls; cost scales with documentation volume, not code size
- v0.8.x evolves fast; some CLI flags shift between minor versions, check the changelog before upgrading

**When to use**: Large or unfamiliar codebases where Claude Code burns tokens re-reading files just to understand structure. Build the graph once, then query it. High-value for legacy code onboarding, monorepo navigation, and pre-PR architecture review.

---

## Skills Observability

### Skillsight

The only open-source tool for team-level skills usage analytics. Ingests Claude Code OTEL telemetry and shows which skills are actually invoked — by whom, how often, in which sessions — rather than which skills you think are being used.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub — PackmindHub/skillsight](https://github.com/PackmindHub/skillsight) |
| **Author** | Cédric Teyton (Packmind) |
| **License** | Apache 2.0 |
| **Version** | 0.2.1 (active, 101 commits) |
| **Stack** | Bun + Hono + PostgreSQL + React 18 (self-hosted Docker) |
| **Ingestion** | OTLP HTTP push from Claude Code, or Loki pull from Grafana Cloud |

**What it tracks:** skill invocations per user and session, plugin catalog (synced from Git marketplaces), cohort segmentation, audit log, real-time event stream.

**Two ingestion modes:**

*Direct OTLP push* — Claude Code sends telemetry straight to Skillsight. Lower latency, simpler setup:

```json
// ~/.claude/settings.json
{
  "env": {
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "http://your-skillsight:4200/api/v0/telemetry/v1/logs",
    "OTEL_EXPORTER_OTLP_LOGS_HEADERS": "Authorization=Bearer <your-ingestion-token>",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/json",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000"
  }
}
```

*Loki pull* — Skillsight polls a Grafana Cloud Loki endpoint on a configurable schedule. Useful if you already aggregate logs there.

The ingestion token is created from the Skillsight UI (`/tokens`) and has a separate JWT type from session tokens — it can only write telemetry, not access the admin interface.

**Setup (direct push):**

1. `docker compose up -d` — starts Skillsight on port 4200 + Postgres
2. Login at `http://localhost:4200` with the initial admin credentials
3. Navigate to the Onboarding page — it generates a complete settings.json snippet with a pre-created ingestion token
4. Copy the snippet into `~/.claude/settings.json` or your project `.claude/settings.json`
5. Run a Claude Code session — events appear in the dashboard within 5 seconds

**Deployment caveats (read before going to production):**

- **Never deploy without overriding `JWT_SECRET` and `ADMIN_PASSWORD_INITIAL`** — the shipped defaults are literal public strings (`change-me-in-production...` and `admin`). No boot-time warning is issued. Any instance reachable from the internet with these defaults is trivially compromised.
- **Set `PUBLIC_BASE_URL`** in your `.env` — this variable controls both CORS policy and the endpoint shown in the Onboarding snippet. Without it, the CORS is permissive (echoes request origin) and the snippet shows `https://your-domain.com`.
- **Run Drizzle migrations manually on upgrades** — the container does not run `drizzle-kit migrate` automatically at startup (as of v0.2.1). If upgrading from 0.1.x, run migrations before starting the new container or the app will crash against a stale schema.

These are known issues under active development. The fixes are straightforward; track resolution at the repo.

**Limitations:**

- Self-hosted only — no SaaS offering
- Marketplace source management is API-only (no UI yet, no curl examples in the docs)
- Image name mismatch in README (`skills-obs` vs actual `skillsight`) — follow the `docker-compose.yml`, not the README curl snippet
- v0.2.x — young project, some rough edges in docs; the CLAUDE.md is however genuinely useful for contributors

**When to use:** You want to know which skills your team actually invokes in practice vs which ones you deployed. Useful for skills library ROI, onboarding effectiveness measurement, and identifying dead skills.

> **Related:** [Packmind ContextOps Platform](#engineering-standards-distribution) — the same author's tool for *distributing* standards to AI agents. Skillsight tells you which skills are used; Packmind helps you author and sync them.
> **Evaluation:** [2026-05-18-skillsight-packmind.md](../../docs/resource-evaluations/2026-05-18-skillsight-packmind.md)

---

## Plugin Ecosystem

Claude Code's plugin system supports community-built extensions. For detailed documentation:

- **[Ultimate Guide Section 8](../ultimate-guide.md)** - Plugin system, commands, installation
- **[claude-plugins.dev](https://claude-plugins.dev)** - 11,989 plugins, 63,065 skills indexed
- **[claudemarketplaces.com](https://claudemarketplaces.com)** - Auto-scan GitHub for marketplace plugins
- **[agentskills.io](https://agentskills.io)** - Open standard for agent skills (26+ platforms)

**Notable skill packs**:
- **[Superpowers](https://github.com/obra/superpowers)**: Complete software development methodology suite (262K stars, 23.4K forks as of 2026-07-27, up from 95K+ stars / 7.5K forks earlier; MIT). 7 context-aware skills covering the full development arc: spec elicitation through Socratic brainstorming, detailed implementation planning (2-5 min tasks with exact file paths), subagent-driven development with two-stage review (spec compliance then code quality), mandatory TDD enforcement (code written before a test gets deleted), code review, git worktree management, and branch lifecycle completion (merge/PR/discard decision). Skills trigger automatically based on context — no manual invocation needed. Install: `/plugin install superpowers@claude-plugins-official`. Created by Jesse Vincent (Prime Radiant), MIT. Also supports Cursor, Codex, OpenCode, and Gemini CLI.
- **[gstack](https://github.com/garrytan/gstack)** — 6-skill workflow suite covering the full ship cycle: strategic product gate (`/plan-ceo-review`), architecture review (`/plan-eng-review`), paranoid code review (`/review`), automated release (`/ship`), native browser QA (`/browse`), and retrospective (`/retro`). Created by Garry Tan (Y Combinator CEO). See [Cognitive Mode Switching](../workflows/gstack-workflow.md) for the workflow pattern and adoption guide.
- **[Ponytail](https://github.com/DietrichGebert/ponytail)**: "Lazy senior dev" mode for AI agents. Before writing code, the agent stops at the first rung that holds: does this need to exist? → stdlib? → native platform feature? → installed dependency? → one line? → only then the minimum that works. Benchmarked at 80-94% less code, 47-77% lower cost, and 3-6x faster than an unconstrained agent across Haiku, Sonnet, and Opus (median of 10 runs, 5 tasks). Three intensity levels: `lite` (suggest the lazier path, let the user pick), `full` (enforce the ladder, default), `ultra` (YAGNI extremist, challenges the requirement in the same response). Deliberate shortcuts are marked with a `ponytail:` comment naming the ceiling and upgrade path; `/ponytail-debt` harvests them into a ledger so "later" stays visible. Four commands: `/ponytail [lite|full|ultra|off]`, `/ponytail-review` (over-engineering review of current diff), `/ponytail-audit` (whole-repo scan), `/ponytail-debt` (shortcut ledger). Install: `/plugin install ponytail@ponytail`. MIT. Supports 13 agents: Claude Code, Codex, GitHub Copilot CLI, Gemini CLI, Antigravity CLI, OpenCode, pi, OpenClaw, Cursor, Windsurf, Cline, Kiro, and VS Code with the Codex extension.
- **[fable-mode](https://github.com/mrtooher/fable-mode)**: Execution discipline skill for complex tasks, structured as a 4-step loop: (1) write a numbered stage map with expected outputs before touching anything, (2) delegate independent stages to parallel subagents where the runtime allows, (3) verify each stage with a check that can actually fail (tests, diffs, sources read — not self-assessment), (4) self-critique as a skeptical reviewer before delivery. Named after the Claude Fable model but works on any model; honest that it shapes procedure, not capability ceiling. Three variants: `fable-mode` (inline on current model), `fable-sonnet` (pins a Sonnet subagent), `fable-haiku` (pins a Haiku subagent for cost-sensitive work). Includes 4 worked examples across domains — API null-path bug, mis-attributed research claim, SQL nulls silently dropped from an AVG, multi-session refactor with no done criteria — each showing exactly where the failable check catches what one-shot misses. Two operational rules worth noting: surface accumulated warnings at threshold 3 rather than one by one; anchor sed replacements on word boundaries to avoid corrupting compound words. Install: copy the skill directory to wherever your Claude environment loads skills from (no plugin registry entry yet). No license. 802 stars, 86 forks as of 2026-07-27 (was 477 stars, 54 forks at 5 days post-launch in June 2026).

---

## Known Gaps

As of February 2026, the community tooling ecosystem has notable gaps:

| Gap | Description |
|-----|-------------|
| **Skills usage analytics** | ✅ **FILLED**: [Skillsight](https://github.com/PackmindHub/skillsight) (Packmind, launched May 2026) — self-hosted OTEL dashboard showing which skills are actually invoked per user/session. Deploy with caveats (see [Skills Observability](#skills-observability)). |
| **Visual skills editor** | No GUI for creating/editing `.claude/skills/` — must edit YAML/Markdown manually |
| **Visual hooks editor** | No GUI for managing hooks in `settings.json` — requires JSON editing |
| **Unified admin panel** | No single dashboard combining config, sessions, cost, and MCP management |
| **Session replay** | ✅ **FILLED**: Entire CLI (launched Feb 2026) provides rewindable checkpoints with full context replay |
| **Automated `.claude/` security scanning** | ✅ **FILLED**: [AgentShield](https://github.com/affaan-m/agentshield) (launched Feb 2026) — 102-rule scanner with A–F grading, `--fix`, and GitHub Action integration |
| **Agent-native issue tracking** | No established tool for markdown-based, git-committable issue tracking with Claude Code. [fp.dev](https://fp.dev/) is an early-stage solution (local-first, `/fp-plan` + `/fp-implement` skills, diff viewer) but lacks adoption signals and requires Apple Silicon for the desktop app. The Tasks API covers state persistence but issues aren't git-committable. |
| **Per-MCP-server profiler** | No way to measure token cost attributable to each MCP server individually |
| **Cross-platform config sync** | No tool syncs Claude Code config across machines (must manual copy `~/.claude/`) |
| **Programmatic sandboxed orchestration** | Watch: [Sandcastle](https://github.com/mattpocock/sandcastle) (`@ai-hero/sandcastle`, Matt Pocock) — TypeScript API for running agents in Docker/Podman/Vercel containers with branch strategy management and prompt templating. Unique niche but not guide-ready at v0.5.x (active bugs, TypeScript-only, requires separate `ANTHROPIC_API_KEY`, Docker/Podman hard dependency). Revisit at v1.0. |

---

## Recommendations by Persona

| Persona | Recommended Tools | Rationale |
|---------|-------------------|-----------|
| **Solo developer** | ccusage + claude-code-viewer | Cost awareness + session history review |
| **Small team (2-5)** | ccusage + Conductor or multiclaude | Cost tracking + parallel development |
| **Enterprise** | ccusage (MCP) + custom dashboards | Programmatic cost data + audit trails |
| **Python-centric** | ccburn + Claude Chic | Native Python ecosystem tools |
| **Multi-agent user** | Toad or Conductor | Unified agent management |
| **Config-heavy setup** | claude-code-config + AIBlueprint + Caliber | TUI config management + scaffolding + drift detection |
| **Codebase newcomer / monorepo** | Graphify | Build graph once, query structure instead of re-reading files every session |
| **Team skills adoption** | Skillsight | Measure which skills are actually invoked across the team, identify dead skills |
| **Over-engineering fighter** | Ponytail | Force the laziest solution that works; benchmark-verified 80-94% less code than unconstrained agents |

---

## Related Resources

- [Observability](../ops/observability.md) - DIY session monitoring, logging hooks, cost tracking scripts
- [AI Ecosystem](./ai-ecosystem.md) - Complementary AI tools (Perplexity, Gemini, NotebookLM)
- [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) - Validated community MCP servers
- [Architecture](../core/architecture.md) - How Claude Code works internally
- [Ultimate Guide Section 8](../ultimate-guide.md) - Plugin system and marketplaces

## Go further

- [AI Ecosystem](./ai-ecosystem.md) - complementary AI tools and integrations
- [Examples](../../examples/README.md) - ready-to-use Claude Code templates
