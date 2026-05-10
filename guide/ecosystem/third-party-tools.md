---
title: "Third-Party Tools for Claude Code"
description: "Community tools for token tracking, session management, configuration, security scanning, project context bootstrapping, hook utilities, and alternative UIs"
tags: [reference, integration, plugin, security]
---

# Third-Party Tools for Claude Code

> Community tools for token tracking, session management, configuration, hook utilities, and alternative UIs.
>
> **Last verified**: April 2026

## Table of Contents

1. [About This Page](#about-this-page)
2. [Token & Cost Tracking](#token--cost-tracking)
3. [Session Management](#session-management)
4. [Configuration Management](#configuration-management)
5. [Security Scanning](#security-scanning)
6. [Configuration Quality](#configuration-quality)
7. [Project Context Bootstrapping](#project-context-bootstrapping)
8. [Engineering Standards Distribution](#engineering-standards-distribution)
9. [Hook Utilities](#hook-utilities)
10. [Alternative UIs](#alternative-uis)
11. [Multi-Agent Orchestration](#multi-agent-orchestration)
12. [Plugin Ecosystem](#plugin-ecosystem)
13. [Known Gaps](#known-gaps)
14. [Recommendations by Persona](#recommendations-by-persona)

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

> **Cross-ref**: Full docs at [ultimate-guide.md Section 9](#command-output-optimization-with-rtk)

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

> **Cross-ref**: For manual Claude Code configuration, see [ultimate-guide.md Section 4](./ultimate-guide.md) (CLAUDE.md, settings, hooks, commands).

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

Tools that audit Claude Code configurations for vulnerabilities — secrets, permission misconfigs, hook injection, MCP server risks, and prompt injection vectors.

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

> **See also**: [Security Hardening guide](security-hardening.md) for manual hook and permission patterns.

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

**Limitations**: Early-stage tool (March 2026, ~65 stars at time of writing). Multi-tool support (Claude Code + Cursor + Codex + Copilot) may produce generically adequate configs rather than deeply Claude Code-specific ones. Scoring rubric is not exposed as a standalone document — the categories are deterministic but not user-visible without reading the source.

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
| **Status** | Early-stage (released April 2026, ~386 stars at time of writing) — APIs may evolve |

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
- **[Ultimate Guide Section 9](./ultimate-guide.md)** - Multi-instance workflows, git worktrees, orchestration frameworks

**Quick reference**:

| Tool | Type | Key Feature |
|------|------|-------------|
| [Gas Town](https://github.com/steveyegge/gastown) | Multi-agent workspace | Steve Yegge's agent-first workspace manager |
| [multiclaude](https://github.com/dlorenc/multiclaude) | Multi-agent spawner | tmux + git worktrees (383+ stars) |
| [agent-chat](https://github.com/justinabrahms/agent-chat) | Monitoring UI | Real-time SSE monitoring for Gas Town/multiclaude |
| [abtop](https://github.com/graykode/abtop) | Fleet TUI monitor | htop-style: tokens, context %, rate limits, ports, subagent tree (584+ stars) |
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
- **[Superpowers](https://github.com/obra/superpowers)** — Complete software development methodology suite (95k+ stars, 7.5k forks, MIT). 7 context-aware skills covering the full development arc: spec elicitation through Socratic brainstorming, detailed implementation planning (2-5 min tasks with exact file paths), subagent-driven development with two-stage review (spec compliance then code quality), mandatory TDD enforcement (code written before a test gets deleted), code review, git worktree management, and branch lifecycle completion (merge/PR/discard decision). Skills trigger automatically based on context — no manual invocation needed. Install: `/plugin install superpowers@claude-plugins-official`. Created by Jesse Vincent (Prime Radiant), MIT. Also supports Cursor, Codex, OpenCode, and Gemini CLI.
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

---

## Related Resources

- [Observability](../ops/observability.md) - DIY session monitoring, logging hooks, cost tracking scripts
- [AI Ecosystem](./ai-ecosystem.md) - Complementary AI tools (Perplexity, Gemini, NotebookLM)
- [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) - Validated community MCP servers
- [Architecture](../core/architecture.md) - How Claude Code works internally
- [Ultimate Guide Section 8](./ultimate-guide.md) - Plugin system and marketplaces
