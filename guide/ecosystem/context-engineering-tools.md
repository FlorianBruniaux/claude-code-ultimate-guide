---
title: "Context Engineering: Tools & Ecosystem"
description: "A practical map of the tools that compress, optimize, route, and observe LLM context — from CLI output filters to AI gateways to LLMOps platforms"
tags: [context, tokens, optimization, ecosystem, tools, advanced]
---

# Context Engineering: Tools & Ecosystem

> **Confidence**: Tier 1/2. Core concepts based on published research and production data. Third-party tool details based on public documentation, GitHub API star counts verified 2026-07-07.
>
> **Related**: [Context Engineering (configuration guide)](../core/context-engineering.md) | [Third-Party Tools](./third-party-tools.md) | [MCP Servers Ecosystem](./mcp-servers-ecosystem.md)

This page maps the ecosystem of tools that help you manage what enters the context window and what doesn't. It complements the [configuration-focused context engineering guide](../core/context-engineering.md), which covers CLAUDE.md structure and path-scoping. Here the focus is on the broader tooling landscape: output compression, prompt compression, AI gateways, RAG optimization, observability, and inference infrastructure.

---

## Table of Contents

1. [The Mental Model](#1-the-mental-model)
2. [Core Concepts](#2-core-concepts) (MVC, context rot, semantic priming, ghost tokens)
3. [Output Compression: CLI & Tool Output](#3-output-compression-cli--tool-output) (RTK, Headroom, pxpipe, tilth, Token Savior, context-mode, stacklit, Cloudflare Code Mode MCP)
4. [Prompt Compression](#4-prompt-compression) (LLMLingua, Selective Context, AutoCompressors/Gisting, RECOMP, AttnComp, TOON)
5. [AI Gateways](#5-ai-gateways)
6. [RAG Optimization](#6-rag-optimization)
7. [Memory Systems](#7-memory-systems)
8. [KV Cache Infrastructure](#8-kv-cache-infrastructure)
9. [LLMOps & Observability](#9-llmops--observability)
10. [Tool Selection by Use Case](#10-tool-selection-by-use-case)
11. [Research Landscape](#11-research-landscape)

---

## 1. The Mental Model

The framing that makes everything else click: **the context window is RAM, not disk**.

RAM is fast, expensive, and finite. You don't load everything you own into RAM before running a program. You load exactly what the program needs, right when it needs it. The same applies to LLM context: every token you put there displaces something else, costs money, and competes for the model's attention.

This reframes the engineering challenge. It's not "how do I give the model more information?" but "what is the minimum viable set of information the model needs to succeed?" Every technique in this page is an answer to that second question.

The parallel with system architecture holds further. A CPU without good memory management stalls. An LLM without good context management hallucinates, loses coherence, and drifts toward generic outputs. Optimizing context is not a cost-cutting exercise — it's a reliability investment.

---

## 2. Core Concepts

### Minimum Viable Context (MVC)

MVC is the principle of providing exactly the information needed for the task, nothing more. It has two failure modes that look opposite but stem from the same cause:

- **Under-context**: the model lacks necessary information, hallucinates or produces generic output
- **Over-context**: the model is overwhelmed with irrelevant information, attention diffuses, adherence degrades

The research on adherence degradation (see [context engineering guide, section 2](../core/context-engineering.md#2-the-context-budget)) quantifies the over-context failure: a CLAUDE.md over 400 lines typically drops adherence to ~60%. The cause is attention diffusion — too many potentially relevant signals compete for the model's limited attention budget.

MVC is not about minimalism for its own sake. It's about precision. A 300-token system prompt that covers exactly what the model needs beats a 3,000-token prompt that buries the critical instruction on page five.

### Context Rot

Context rot describes the degradation in model behavior as context length grows during a session. The most studied form is the "lost-in-the-middle" phenomenon: models consistently underweight information placed in the middle of a long context, attending primarily to the beginning and end.

Empirical consequences in practice:

- Instructions near the top of a CLAUDE.md file are followed more consistently than instructions at the bottom
- In long agentic sessions, earlier constraints lose salience as new content pushes them toward the middle
- Tool outputs from the start of a session are often effectively "forgotten" after several rounds of interaction

Mitigation: `/compact` at 70% context usage (not 90%), structured note-taking hooks, and session restarts for fundamentally new task contexts. The `/compact` command summarizes conversation history, moving stale content out of the active attention window while preserving continuity.

### Semantic Priming Hypothesis

An observation from compression research with practical implications: when you ultra-compress a context (removing most tokens), the model does not recall the removed information verbatim. Instead, the compressed context acts as a *semantic prime* — it activates relevant latent knowledge that was already present in the model's weights from training.

This matters because it means heavily compressed context can perform better than its information density suggests. The model is not reconstructing facts from the context; it's being pointed toward relevant knowledge it already has. For well-trained domains, a 10-token hint may activate more relevant knowledge than a 100-token verbatim extract.

The practical implication: prefer keywords and structural cues over prose when context is tight. "Use OpenAPI 3.1, strict mode, no nullable" retrieves more precise behavior than two paragraphs explaining the same thing.

### Context Rot vs. Token Cost: The Two Pressures

Context management operates under two simultaneous pressures that pull in opposite directions:

| Pressure | Cause | Effect | Mitigation |
|----------|-------|--------|------------|
| **Context Rot** | Too much content | Attention diffusion, lost-in-middle | Prune, compact, scope |
| **Token Cost** | Every token billed | Budget overrun, latency increase | Compress, filter, cache |

Compression addresses cost. Pruning addresses rot. Good context engineering does both.

### Context Quality After Compaction ("Ghost Tokens")

Most of the tooling in this page answers "how many tokens did we save?" A newer, narrower angle asks a different question: after `/compact` or any lossy summarization pass, how much of what remains is still load-bearing, versus dead weight that survived compaction by accident? The term circulating for the latter is "ghost tokens": content that costs budget but no longer does useful work, distinct from the noise MVC targets before compaction ever runs.

`alexgreensh/token-optimizer` is the tool most associated with this framing (1,748 stars as of 2026-07-27, up from 1,565 in June and 947 in May 2026, the fastest-growing entry in this category by percentage). Rather than reporting a single reduction percentage, it targets what survives a compaction pass and whether that surviving content is still relevant to the task at hand.

This is a genuinely distinct question from the raw-reduction metrics reported elsewhere on this page (Headroom's 92% on code search, RTK's 60 to 90% on shell output). Raw reduction measures how much was cut. Post-compaction quality measures whether what was kept is still correct and relevant. A tool could score well on the first metric and poorly on the second, if it happens to prune the wrong content. Treat this as an emerging measurement dimension, not yet a mature tooling category. Watch this angle rather than adopt it as a solved problem.

---

## 3. Output Compression: CLI & Tool Output

Tool outputs, shell command results, test logs, and database query responses share a structural problem: they contain 70–95% boilerplate. A passing test suite logs hundreds of success lines for the one failure you care about. A `git log` dumps metadata for every commit when you need three fields. This noise enters the context window verbatim unless intercepted.

### RTK (Rust Token Killer)

RTK is a CLI proxy that intercepts command output before it reaches Claude's context, applying purpose-built filters that surface signal and discard noise. It integrates via a Claude Code hook, so standard commands are transparently rewritten.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| **Install** | `brew install rtk-ai/tap/rtk` or `cargo install rtk` |
| **Stars** | 69,042 (GitHub API, 2026-07-07), up from 446 in March 2026 and 24,397 in April 2026 |
| **Integration** | Claude Code hook via `rtk init --global` |

A roughly 2.8x jump in under three months is a steep curve for a CLI proxy. It is plausible given the tool's growing bundling into other agents' default setups (see below), but treat the figure as unverified against the full star-history graph rather than confirmed growth, and re-check before quoting it in a high-stakes context.

Measured savings across command categories:

| Command | Reduction |
|---------|-----------|
| `rtk git log` | 92% |
| `rtk git status` | 76% |
| `rtk vitest run` | 99%+ |
| `rtk cargo test` | 89% avg |
| `rtk pnpm outdated` | 70–85% |

The design philosophy: suppress successful output, surface failures. A test suite that passes 300 tests and fails 2 should show 2 lines, not 302. This matches how a developer reads output — context should match that cognitive model.

RTK supports custom filters via TOML DSL (`.rtk/filters.toml`) for project-specific output patterns without writing Rust. See [Third-Party Tools: RTK](./third-party-tools.md#rtk-rust-token-killer) for the complete feature reference.

**Real-world cost impact**: Real-world billing data from the codepointer substack ($926 API bill, analyzed) shows that bash output accounts for roughly 12% of total token usage in a typical Claude Code session, not the dominant source. File reads represent approximately 65%. At 60-90% compression on bash output alone, RTK's real API cost impact is in the range of 6-10% of the total bill, not 60-90%. The per-command savings are genuine; the headline "60-90% savings" refers to the compression ratio on the commands RTK processes, not to overall session cost reduction. For total context efficiency, pair RTK with a file-read compression tool like lean-ctx or tilth (see below).

### Headroom

Headroom compresses what enters the context from tool outputs, structured data, and conversation history. Its output shaper also reduces what comes back from the model, making it one of the few tools that operates on both sides of the LLM call.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) |
| **Docs** | [headroom-docs.vercel.app](https://headroom-docs.vercel.app/docs) |
| **Stars** | 62,778 (GitHub API, 2026-07-27), 4,754 forks (was 57,223 / 4,205 on 2026-07-07) |
| **Author** | Tejas Chopra (Senior Engineer, Netflix) |
| **License** | Apache 2.0 |
| **Install** | `pip install "headroom-ai[all]"` or `npm install headroom-ai` |
| **Version** | v0.25.0 (June 2026, latest verified) |

> **URL correction**: Earlier versions of this guide linked `headroom.ai` (unrelated domain) and later `github.com/chopratejas/headroom` (the author's personal fork). The project has since moved to the `headroomlabs-ai` org; the old personal slug now redirects, a standard GitHub org transfer.

**Reported cost impact**: the maintainer cites aggregate savings of "~$700K across 200B tokens processed." This is self-reported with no third-party audit found. Treat it as a marketing signal, not a verified figure, distinct from the per-workload benchmark numbers below, which do publish methodology.

**Five deployment modes**:

1. Python library: `compress(messages)` directly in application code
2. TypeScript/npm: `withHeadroom()` / `compress()`
3. HTTP proxy: `headroom proxy --port 8787`, then set `ANTHROPIC_BASE_URL=http://localhost:8787`
4. MCP server: `headroom mcp install` (exposes `headroom_compress`, `headroom_retrieve`, `headroom_stats`)
5. Agent wrap: `headroom wrap claude|codex|cursor|aider|copilot`

**Compress-Cache-Retrieve (CCR)**: Instead of sending verbose tool output to the model, Headroom replaces it with a `{{HEADROOM_TAG_N}}` placeholder, stores the original in a local SQLite store (HNSW vector index + FTS5 full-text index), and registers a retrieval handle. The model calls `headroom_retrieve(tag)` when it needs the original data. Multiple agents (Claude + Codex) can share the same SQLite store for cross-agent context handoff.

**Output shaper** (`HEADROOM_OUTPUT_SHAPER=1`): appends a brevity instruction at the end of the system prompt (cache prefix is preserved) and reduces model effort on turns that follow successful tool results. Savings are reported as "estimated" using a 10% holdout control group with 95% confidence intervals.

**Benchmark scope**: The published token reductions (code search 92%, SRE debugging 92%, GitHub triage 73%) are measured on specific structured content types under optimal conditions, not full-session spend. An independent measurement found approximately 47% full-session reduction. Accuracy benchmarks (GSM8K 0.870 to 0.870, TruthfulQA +0.030) are N=100 samples, run on v0.5.18, not independently reproduced. Reproduction command: `python -m headroom.evals suite --tier 1`.

**Known issues (June 2026, check the issue tracker for current resolution status)**:

- **Issue #714**: CCR originals expire after 5 minutes (LRU TTL). Long-running agent jobs that pause between steps will hit retrieval failures when the cache expires. No persistent fallback is documented for this case.
- **Issue #1158**: `headroom wrap claude` silently caps context at 200K for Claude Max subscribers (the `context-1m-2025-08-07` beta header is dropped). Claude Max users should use `headroom mcp install` instead of `wrap`.
- **Issue #1227** (security, unresolved as of June 2026): CCR endpoints lack loopback protection and use permissive CORS. A local web page can read cached tool outputs without authentication. Avoid CCR if the host runs alongside untrusted local web content.
- **Issue #1209**: In some configurations, CCR stores the `{{HEADROOM_TAG_N}}` placeholder as the original, so `headroom_retrieve` returns the placeholder rather than the actual data. PR #1208 filed.
- **Issue #1233**: `CodeAwareCompressor` generates invalid Python syntax on roughly 28% of real files containing modern syntax (match/case, walrus operator, nested async). Silent fallback to uncompressed output in those cases.

**When to choose Headroom over RTK**: RTK handles unstructured CLI text and drops content you definitively do not need. Headroom is the right choice for structured data (JSON payloads, database results, API responses) where you cannot predict upfront which parts the model will need, and where lossless retrieval is a requirement. The two tools complement each other; RTK operates at the shell output layer, Headroom at the structured data layer.

**Production note**: Core compression is functional. CCR has reliability issues under bugs #714 and #1209 above. For Claude Max users, prefer MCP mode over `headroom wrap`.

### pxpipe

pxpipe is the first production tool built on optical/visual context compression specifically for Claude Code and the Anthropic API: instead of shrinking text, it rewrites large context blocks as images before the request leaves the machine. See [Context Engineering: Optical and Visual Context Compression](../core/context-engineering.md#optical-and-visual-context-compression) for the research lineage (DeepSeek-OCR, AgentOCR, Glyph, VIST).

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/teamchong/pxpipe](https://github.com/teamchong/pxpipe) |
| **License** | MIT, TypeScript |
| **Stars** | 4,277 (GitHub API, 2026-07-07), up from 586 at launch in May 2026, roughly 7x in under two months |
| **Install** | `npx pxpipe-proxy` |

**Mechanism**: a local proxy intercepts `/v1/messages` calls and, above a computed cost-effectiveness threshold, rewrites large `tool_result` blocks, already-collapsed older turns, and the static system-prompt/tool-doc block into PNG images (1928px-wide columns, roughly 92,000 characters per page, roughly 4,761 vision tokens per page). It never touches model output, recent turns, or sparse prose, where text stays cheaper per character. The text-vs-image break-even is around 19 characters per token; the maintainer's observed Claude Code traffic averages 1.91 characters per token, so most large content is worth imaging. Exact-byte content (passwords, hashes, IDs) is explicitly excluded from rendering and flagged in the README as a documented lossy-recall risk, not a solved problem.

```bash
npx pxpipe-proxy
ANTHROPIC_BASE_URL=http://127.0.0.1:47821 claude
```

**Benchmarks**: 59 to 70% end-to-end bill reduction, measured per-request via a parallel counterfactual `count_tokens` call logged to `~/.pxpipe/events.jsonl` and cross-checked against actual billed usage, a reproducible methodology rather than a marketing estimate. SWE-bench Lite pilot: 10/10 passing in both arms at -65% request size (small n, disclosed as such in the README). Verbatim recall of hex strings: 13/15 correct on Fable 5, 0/15 on Opus, numbers the README states plainly rather than hides.

**Model allowlist**: defaults to `claude-fable-5` and `gpt-5.6`. Opus 4.7/4.8 and GPT-5.5 are opt-in because of measured higher misread rates on rendered images.

**When to choose pxpipe over Headroom**: same API-gateway layer, different modality. Headroom compresses text to text (reversible, retrieval-based); pxpipe rasterizes text to images (lossy on exact strings, not retrieval-based). They complement rather than compete: pxpipe is Claude Code/Anthropic-API-specific with limited GPT support, not a multi-agent generalist tool like Headroom.

### tilth

tilth is an MCP server for code navigation that targets the largest single source of token usage in Claude Code sessions: file reads. Rather than returning full file contents, it provides structural navigation via tree-sitter, so the model reads shapes and relationships instead of raw text.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/jahala/tilth](https://github.com/jahala/tilth) |
| **Install** | `cargo install tilth` then `tilth install claude-code` |
| **Architecture** | MCP server, installs into Claude Code |
| **Parser** | tree-sitter (multi-language) |

The core tools it exposes:

- **File read with auto-outline**: for large files, instead of the full text, returns a structural skeleton with section names and line ranges. The model requests specific ranges on demand.
- **Symbol search**: definitions, usages, and resolved callees in a single call, replacing the grep-then-read loop.
- **`--callers`**: all call sites of a symbol, structurally, not via text search.
- **`--deps`**: imports and dependents of a file, useful before a refactor to understand blast radius.
- **`grok <symbol>`**: everything about one symbol in one call: signature, callers, callees, sibling functions, associated tests.
- **Structural diff**: change summary at the function level, not the line level.
- **Session dedup**: symbols already shown in the session are marked `[shown earlier]` rather than re-expanded.

**Benchmarks** (160 runs across 4 real repositories, metric = cost per correct answer):

| Model | Without tilth | With tilth | Cost change | Accuracy change |
|-------|--------------|------------|-------------|----------------|
| Sonnet 4.6 | baseline | tilth | -44% | 84% → 94% |
| Opus 4.6 | baseline | tilth | -39% | 91% → 92% |
| Haiku 4.5 | baseline | tilth | -38% | 54% → 73% |
| Average | | | -40% | 76% → 86% |

The "cost per correct answer" framing is meaningful: it captures both the efficiency gain and the accuracy improvement simultaneously. A tool that saves tokens but degrades output quality is not useful. tilth shows gains on both dimensions.

Why file reads are the right target: they represent about 65% of total token usage in a real Claude Code session (versus ~12% for bash output). Compressing the larger pool produces proportionally larger savings on the total bill.

**Install:**

```bash
cargo install tilth
tilth install claude-code   # registers the MCP server in Claude Code
```

No per-project configuration is needed after global install.

**Comparison with lean-ctx**: Both tilth and lean-ctx use tree-sitter to compress file reads. lean-ctx operates as a hook-level redirect (intercepts native Read calls at the MCP layer), while tilth exposes explicit navigation tools the model calls directly. lean-ctx is more transparent and requires no change to how the model requests files. tilth gives the model more control over what it fetches but requires it to use the tilth tools rather than standard read operations. On teams that want the model to actively navigate code structure rather than have reads compressed passively, tilth's explicit tools fit better.

### Token Savior

Token Savior is a three-in-one MCP server: structural code navigation by symbol (replacing full-file reads), Bash output compaction for 34 common CLI tools, and persistent cross-session memory via SQLite with FTS5.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: Mibayy/token-savior](https://github.com/Mibayy/token-savior) |
| **Install** | `pip install "token-savior-recall[mcp]"` then `ts init --agent claude --yes` |
| **Stars** | ~1,000 (June 2026) |
| **Language** | Python 3.11+ |
| **Last commit** | April 2026 (C99/C11 and GLSL support added) |

**Core navigation tools** (via the `optimized` profile, 15+ tools):

- `find_symbol(name)` - locate functions and classes across the indexed codebase
- `get_function_source(name)` - retrieve implementation without loading the full file
- `get_full_context(identifier)` - extended context around a symbol
- `get_change_impact(identifier)` - dependency chain for blast-radius analysis before refactoring
- `build_commit_summary` - recent git changes without reading every file
- `memory_index` / `memory_search` - store and retrieve session learnings across runs
- `ts_discover()` - scan past transcripts for missed optimization opportunities

**Bash compaction**: 34 output compactors for git, pytest, jest, kubectl, and similar tools, activated via `TS_BASH_COMPACT=1` and PostToolUse hooks. Outputs above 4KB fall back to full capture. This feature is opt-in and accounts for a significant share of the reported gains; skipping it reduces the savings substantially.

**6 tool profiles** (controls how many tools the model sees, useful when manifest budget is constrained): `full`, `core`, `nav`, `lean`, `ultra`, `tiny`. The `tiny` profile exposes 6 tools; roughly 60 others are reachable via `ts_search` on demand.

**Language support**: Python, TypeScript/JavaScript, Go, Rust, C#, C/C99/C11, GLSL, plus config formats (JSON, YAML, TOML, INI, ENV, HCL/Terraform, Dockerfile, Markdown).

**tsbench results** (Claude Opus 4.7, 96 tasks, synthetic 2,000-line codebase, `--seed 42`, author-created benchmark):

| Metric | Without Token Savior | With Token Savior |
|--------|---------------------|-------------------|
| Task completion | 78.3% | 97.9% |
| Active tokens/task | ~16,800 | ~3,929 (-77%) |
| Wall time/task | ~111s | ~26.6s (-76%) |

The project separately reports 97% reduction in characters injected across 170+ real sessions. No independent third-party reproduction of the benchmark has been published. Behavior on large codebases (100K+ lines) has not been benchmarked under controlled conditions.

```bash
# Recommended install
pip install "token-savior-recall[mcp]"
ts init --agent claude --yes   # merges hooks into ~/.claude/settings.json

# Or without global install
WORKSPACE_ROOTS=/your/project uvx token-savior
```

**Comparison with tilth**: tilth (Rust, 14 languages, controlled benchmark across 4 real repositories) focuses on structural code navigation and file outlines. Token Savior adds Bash output compaction and persistent cross-session memory, features tilth does not have. Choose tilth for a faster, independently benchmarked code navigation layer. Choose Token Savior if you also need Bash compaction and memory persistence across sessions.

### context-mode

context-mode is an MCP server that operates at the boundary between tools and context, intercepting tool call outputs before they reach the conversation window and applying compression or selective retrieval. It also implements a session tracking layer using SQLite with FTS5 full-text search, enabling semantic retrieval of earlier session content after `/compact` discards raw history.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: mksglu/context-mode](https://github.com/mksglu/context-mode) |
| **Stars** | 18,654 (GitHub API, 2026-07-07), up from 14,149 in May 2026 (+32% in about 2 months) |
| **License** | ELv2 (commercial SaaS planned) |
| **Platforms** | Claude Code plugin, Gemini CLI, Copilot, Cursor, Kiro, Zed, and 11 others (17 total, up from 12 in May 2026) |
| **Claims** | 98% MCP output compression, 65–75% response compression |

The growth rate reads as consolidation of an already-mature tool rather than a new-entrant spike: other projects now cite context-mode as a dependency or reference, a sign of an ecosystem forming around it rather than just end users adopting it.

**How the MCP output sandbox works**: Instead of routing raw tool call output directly into the conversation, context-mode intercepts the result, applies compression, and injects a summary with a retrieval handle. The full output is accessible on demand if the model requests it, similar in spirit to Headroom's lossless architecture but operating specifically on MCP tool boundaries.

**Session memory after `/compact`**: context-mode uses SQLite + FTS5 to index session history. When `/compact` runs and discards raw conversation history, the SQLite index persists. Subsequent retrieval queries use BM25 ranking to surface relevant earlier context without reloading the full transcript.

**"Think in Code" pattern**: context-mode v1.0.64 documented a pattern where, instead of reading files to answer an exploratory question, the model writes and executes a script that queries or counts, then reads only the result. This is covered in depth as a named technique in the [context engineering guide](../core/context-engineering.md).

**When to choose context-mode**: If you run Claude Code alongside other platforms (Cursor, Gemini CLI) and want a single context management layer that works across all of them. Also useful when MCP tool outputs are large and structured, and you need post-compact session retrieval beyond what `/compact` alone provides.

**Comparison with RTK and Headroom**: RTK operates at the shell command level (CLI output), Headroom at the structured data/API response level. context-mode operates specifically at the MCP tool boundary and adds session persistence. These tools are complementary.

### stacklit

stacklit generates a machine-readable index of a repository's package structure, exported symbols, and dependencies. An agent reads this index in a single call (~250 tokens) instead of spending 50,000+ tokens exploring files to understand the codebase structure.

| Attribute | Details |
|-----------|---------|
| **Source** | [GitHub: glincker/stacklit](https://github.com/glincker/stacklit) |
| **Install** | `npm install -g stacklit` |
| **Integration** | Auto-configures Claude Code, Cursor, and Aider via `stacklit setup` |
| **Claimed reduction** | 50,000+ tokens of exploration compressed to ~250 tokens |

**How it works**: `stacklit generate-json` scans the repository and writes `stacklit.json`, a structured map of packages, exports with type signatures, dependency graph, git activity heatmap, and framework hints. `stacklit setup` injects a compact codebase map into agent configuration files automatically. `stacklit diff` detects when the index is stale after file additions or deletions.

```bash
# One-time setup per repository
stacklit generate-json    # create the index
stacklit setup            # inject into Claude Code / Cursor / Aider config

# Maintenance
stacklit diff             # check if index is stale
stacklit generate-json    # re-index after structure changes
```

**Worktree compatibility**: generates per-repository indexes with no centralized state. Unlike grepai (which requires a local embedding index) or Serena (which connects to a language server), stacklit produces a static JSON file that works in git worktrees and ephemeral CI environments without additional setup.

**Comparison with RTK and context-mode**: RTK intercepts CLI output during a session. context-mode intercepts MCP tool output in real time. stacklit eliminates exploration-phase token spend before the session starts, by making the repo structure known from the first message. The three tools target different moments in a session's lifecycle and are complementary.

### Cloudflare Code Mode MCP

A different category of tool-schema cost: an MCP server with hundreds or thousands of endpoints loads a schema per tool, and that schema overhead can dwarf the actual task. Cloudflare's Code Mode MCP (`cloudflare/mcp`) addresses this at the API-surface level rather than the output level.

Instead of exposing one MCP tool per endpoint, it exposes exactly two meta-tools, `search()` and `execute()`, backed by a typed SDK. The model writes and runs JavaScript in a sandboxed V8 instance (Dynamic Worker Loader) that calls the typed SDK, rather than receiving a schema definition for every possible endpoint upfront. For Cloudflare's full API surface (2,500+ endpoints), this drops the schema-loading cost from roughly 1.17M tokens to about 1,000, a 99.9% reduction on that specific dimension.

This is a shipped production feature at a major infrastructure vendor, not a side project or a research prototype. It generalizes a pattern worth naming explicitly: when a tool surface is large and mostly unused per session, exposing a code-execution interface over the API instead of one MCP tool per endpoint moves the token cost from "loaded upfront for every session" to "paid only for the endpoints actually called." See [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) for how this interacts with Claude Code's MCP tool-count guidance ([Progressive Disclosure](../core/context-engineering.md#progressive-disclosure) in the core context engineering guide recommends fewer than 80 total tools across active servers; a code-execution MCP server sidesteps that ceiling entirely by exposing 2 tools regardless of API surface size).

### Zero-install approach: claude-token-efficient

[claude-token-efficient](https://github.com/drona23/claude-token-efficient) (5,884 stars, verified 2026-07-27) is a single `CLAUDE.md` file that instructs Claude to generate concise responses. No binary, no MCP server, no hooks.

The creator claims approximately 63% output token reduction. No methodology is published for that figure. The approach works within a real but narrow scope: if verbose model output is your primary cost driver, a style instruction in `CLAUDE.md` costs nothing to try. It cannot compress shell output, file reads, or tool responses. Those require tools like RTK, lean-ctx, Headroom, or tilth. The near-6K star count reflects genuine demand for zero-config options, not validated performance across diverse workloads.

Use it as a starting point. When you hit the ceiling, the tools above address what a `CLAUDE.md` file cannot.

---

## 4. Prompt Compression

Prompt compression operates at the model-input level: reducing the token count of the prompt itself before it is sent to the LLM. This differs from output compression (which intercepts tool responses) and context pruning (which manages session history).

### LLMLingua / LLMLingua-2

LLMLingua (Microsoft Research) is the most studied prompt compression framework. It uses a small language model to evaluate the "importance" of each token in a prompt, then removes the least important tokens up to a target compression ratio.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/microsoft/LLMLingua](https://github.com/microsoft/LLMLingua) |
| **Max compression** | 20x |
| **Performance loss** | ~1.5% on GSM8K and BBH benchmarks |
| **Approach (v1)** | Perplexity-based token scoring via small LM |
| **Approach (v2)** | Data distillation from GPT-4, token classification |

LLMLingua-2 improves on the original by treating compression as a classification problem (keep vs. drop) rather than a ranking problem. The classifier is trained via distillation from GPT-4 annotations, making it faster and more generalizable across domains.

The Semantic Priming Hypothesis (see section 2) explains why 20x compression can retain 98.5% of task performance: the model is not recalling compressed text literally. It's using the compressed tokens as semantic anchors into its own pre-trained knowledge. High-frequency tokens (function words, connectives) are often dropped; domain keywords and structural markers are preserved.

**When to use**: Long system prompts, repetitive RAG contexts, few-shot examples where the examples are verbose. Not suitable for code (syntax is load-bearing) or numerical data (every digit matters).

### Selective Context

Selective Context (Li et al., 2023) predates LLMLingua and scores lexical units (tokens, phrases, or sentences) by Shannon self-information rather than raw perplexity. It is generally cited as LLMLingua's direct predecessor, and LLMLingua has since superseded it in practice. Reported compression/quality figures for it vary by source; treat any specific ratio you find as a secondary-source citation, not a confirmed benchmark result.

### AutoCompressors and Gist Tokens (Soft-Prompt Compression)

A distinct family that compresses context into learned vectors instead of shorter text. **AutoCompressors** (Chevalier et al., EMNLP 2023) fine-tune a base model to summarize long segments into reusable "summary vectors." **Gisting** (Mu, Li & Goodman, Stanford, NeurIPS 2023) trains a model to compress a prompt into a handful of cacheable "gist tokens" by modifying attention masks during standard fine-tuning, reporting up to 26x compression with minimal quality loss on the Alpaca+ dataset.

Neither technique is deployed in production tooling as of mid-2026: both require fine-tuning the target model itself, which breaks the "works on any LLM" portability that made LLMLingua adoptable. Worth knowing these exist as a category; not yet something to install.

### RECOMP (RAG-Specific Compression)

RECOMP (Xu et al., arXiv 2310.04408) compresses retrieved documents before they enter the prompt, rather than compressing the assembled prompt as a whole (complementary to the Anthropic Contextual Retrieval approach described in §6 below). Two trainable compressors: an extractive one that selects useful sentences, an abstractive one that generates a distilled multi-document summary. Reported gains on Natural Questions, TriviaQA, and HotpotQA for frozen LMs. Still a research technique, not an industry-standard tool, but the underlying principle (compress at retrieval time, not prompt-assembly time) has informed later RAG-compression work.

### AttnComp (Research Direction)

AttnComp (not yet a shipping product as of March 2026) proposes replacing perplexity scoring with cross-attention patterns as the compression metric. The argument: perplexity measures how "surprising" a token is given its predecessors — useful for language modeling, but only loosely correlated with task relevance. Cross-attention patterns directly show which tokens the model attends to for a given output, making it a more principled importance metric.

Published results show AttnComp outperforms LLMLingua at equivalent compression ratios. Monitor for OSS release.

### TOON (Token-Oriented Object Notation)

TOON operates at a different level than LLMLingua or AttnComp: it is a data serialization format, not a compression algorithm applied after the fact. Instead of scoring and dropping tokens from an existing prompt, it re-encodes structured data (arrays of objects, tabular records) into a denser textual notation before that data ever reaches the model, keyed columns declared once instead of repeated per row, the way CSV avoids repeating field names.

`xaviviro/python-toon` provides a Python encoder/decoder, and production case studies (Scalevise, among others cited in the press) report 50%+ token reduction plus a 15% latency improvement on structured, tabular payloads.

The gains are entirely format-dependent: near zero on deeply nested, non-uniform JSON (there is no repeated flat structure to exploit), maximal on flat tabular arrays (API list responses, database query results, CSV-shaped data). Before adopting TOON, check whether your actual payloads are tabular; if they are deeply nested objects, LLMLingua's semantic scoring is the better fit.

---

## 5. AI Gateways

AI gateways sit between your application and the LLM provider. They handle routing, rate limiting, cost management, and increasingly, active context transformation. The gateway category is where infrastructure and context engineering overlap.

### Edgee

Edgee is a Rust-based AI gateway. Its compression features shipped as **Compressor V2** (announced July 2, 2026): three independent layers, each targeting a different part of the request.

| Layer | What it compresses | Measured effect (Edgee's own benchmark) |
|-------|--------------------|-------------------------------------------|
| **Brevity** | Model output (strips narrated planning, "I'll first read the file, then...") | ~30% median cost reduction, 6 SWE-bench Lite coding tasks |
| **Tool Surface Reduction (TSR)** | MCP `tools[]` catalog, collapsed to one virtual `search` tool | ~33% token-volume reduction, ~10% cost reduction, 8 MCP tasks |
| **Tool result trimming** | Conversation history / tool outputs | ~10% cost reduction, 6 coding tasks (carried over and refined from V1) |

**Source**: [Edgee Blog, Introducing Compressor V2](https://www.edgee.ai/blog/posts/introducing-compressor-v2-three-compression-layers-measured-end-to-end-for-a-50-cost-reduction) | [github.com/edgee-ai/edgee](https://github.com/edgee-ai/edgee)

**Relationship to RTK**: Edgee's own post names RTK as the direct inspiration for the tool-result-trimming layer. Structurally, RTK can only ever cover that one layer: it runs as a local shell hook and has no access to the MCP tool catalog or the model's own output. For a Claude Code user already running RTK, Edgee's brevity layer is the genuinely new capability; TSR overlaps with what Claude Code's native MCP Tool Search already does for free (§ [MCP Tool Search](../core/architecture.md#mcp-tool-search-lazy-loading)), and trimming overlaps with what RTK already does locally.

**Reading the "50% combined" claim critically**: the three numbers above come from three separate experiments on two different workloads (coding vs. MCP), never measured together on the same sessions. The "50%" in the post's title tracks closest to brevity's raw aggregate (+51.1%, pulled up by one outlier task), relabeled as the combined figure. It is not an end-to-end measurement of all three layers running at once, and the effects are not mechanically additive (less narration also means less history left to trim). The statistical design is genuinely careful: paired per-task comparison, a sign test chosen over a paired t-test because cost differences are heavy-tailed, and a nonce injected into each replicate to defeat prompt-cache contamination between runs. But the sample sizes are small enough to matter — at n=6, the best achievable two-sided sign-test p-value is 0.031, meaning a perfect 6-of-6 result was the *only* outcome that could clear the conventional 0.05 threshold; one task flipping drops it to 5/6, p=0.22, not significant. The post also never reports SWE-bench Lite's actual metric, resolution rate (the share of issues whose patch still passes tests), only token cost. A cheaper agent that solves fewer tickets is not a net win, and Edgee's own benchmark repository (`edgee-ai/compression-lab`) confirms it tracks token consumption "rather than task completion rates."

**A second, separate set of numbers exists, and it tells a different story.** Edgee's documentation (distinct from the blog post) reports production averages across real customer traffic: brevity ~6.5%, tool result trimming ~19%, tool surface reduction ~25% (labeled "in development," i.e. not yet fully shipped), and an aggregate ~20% token-bill reduction across active customers over a rolling 30-day window. These production figures diverge sharply from the controlled benchmark above: brevity's real-world effect (6.5%) sits far below its benchmark median (~30%) or headline aggregate (+51.1%), while trimming's production effect (19%) nearly doubles its benchmark result (~10%). The same page answers the resolution-rate gap with one line, "zero measurable drift on SWE-Bench Verified samples," but gives no sample size, no definition of "measurable," and no confidence interval. It reads as a direct response to the resolution-rate critique, without the statistical rigor the benchmark post itself otherwise demonstrates. Source: [Edgee docs, Why Edgee?](https://www.edgee.ai/docs/introduction/why-edgee)

### Portkey

Portkey is the more established player in the AI gateway category, with a broader feature set centered on unified routing across multiple LLM providers.

| Attribute | Details |
|-----------|---------|
| **Source** | [portkey.ai](https://portkey.ai) |
| **Model support** | 250+ LLMs via unified API |
| **Features** | Routing, fallbacks, load balancing, caching, guardrails |
| **Observability** | Built-in tracing and cost tracking |

Portkey's semantic caching layer is particularly relevant for context optimization: identical or near-identical requests are cached and returned without an LLM call. In applications with repetitive query patterns (helpdesks, code review bots, internal search), cache hit rates can reduce total LLM calls by 30–60%.

**Gateway vs. Output Compression**: these categories complement each other. RTK/Headroom compress what goes into the context from tool outputs. Gateways compress or route the assembled prompt before it hits the model. Both reduce total token spend, but they intercept at different points in the pipeline.

### LiteLLM

[LiteLLM](https://github.com/BerriAI/litellm) is the most widely deployed self-hosted alternative: an MIT-licensed Python proxy with Redis-backed caching, virtual keys, and per-team/per-user budget caps. Unlike Edgee or Portkey, it ships no active compression layer of its own: its cost lever is caching and routing, not token-level compression of what gets sent. Pairs well with RTK or lean-ctx (which handle compression) when the goal is also centralized budget enforcement across a team. See [api-gateway.md](../ops/api-gateway.md) for the budget-enforcement side of this.

### Semantic Caching as a Library: GPTCache

Portkey's semantic caching (above) and Anthropic's prompt caching (§8) both require an exact or near-exact prefix match. [GPTCache](https://github.com/zilliztech/GPTCache) (Zilliz, Apache 2.0) targets a different case: it caches the full *response*, keyed by the embedding of the query, and serves it for any new query above a cosine-similarity threshold, skipping the LLM call entirely rather than reducing what gets sent to it. It's a library to integrate into your own code (not a drop-in gateway), with pluggable vector backends (Milvus, FAISS) and storage backends (Redis, MongoDB); embedding lookup adds roughly 3–8ms. Hit-rate figures of 30 to 70% circulate in vendor and blog material but are not independently verified. Treat them as an order of magnitude, not a measured number, until you benchmark your own traffic.

---

## 6. RAG Optimization

Retrieval-Augmented Generation has a well-documented failure mode: the retrieval step returns chunks that are semantically relevant in isolation but lack the context to be useful. A fragment mentioning "Q3 revenue grew 3%" is meaningless without the company name and year — both of which may have been in the same document but in a different chunk.

### Anthropic Contextual Retrieval

Anthropic's contextual retrieval method addresses chunk isolation by pre-contextualizing each fragment before indexing. A short LLM-generated preamble is prepended to each chunk, situating it within the document it came from.

```
Before: "Revenue grew 3% in Q3."

After: "From Acme Corp Q3 2024 earnings report: Revenue grew 3% in Q3."
```

The preamble is generated once per chunk at indexing time, not at retrieval time. With prompt caching, the cost of generating preambles for a large document corpus is reduced by ~90% (the document is cached; only the per-chunk instruction varies).

Published results from Anthropic's evaluation:

| Method | Failure Rate Reduction |
|--------|----------------------|
| Contextual embeddings only | 35% |
| Contextual BM25 (keyword + semantic) | 49% |
| Contextual embeddings + BM25 + reranking | 67% |

The combination of semantic search (embeddings), keyword search (BM25), and a reranking step that re-orders results by relevance to the actual query produces the best outcomes. Reranking providers include Cohere and Voyage AI.

Cost at scale: generating contextual preambles for 1M document tokens costs approximately $1.02 after prompt caching. For most production corpora, this is a one-time indexing cost.

### JIT / Agentic Search

Traditional RAG loads the retrieval results at the start of the request. JIT (Just-in-Time) retrieval defers this: the agent starts with minimal context and retrieves information on-demand as the task reveals what it actually needs.

This matters for agent workflows with unpredictable information requirements. A code debugging agent may need one set of docs for a Python error and a completely different set for the database error encountered two steps later. Loading both upfront wastes context; loading neither forces hallucination. JIT retrieval threads the needle.

In Claude Code terms: this is what the agent does naturally when it uses tools (`list_directory`, `read_file`, `grep`) rather than receiving a pre-assembled context. The "search when needed" pattern is a design principle, not just a Claude capability.

### Query-Side Indexing: Semantic Chunking and Synthetic Questions

Two indexing-time techniques consistently improve retrieval quality beyond what better embeddings alone achieve.

**Semantic chunking** splits documents by logical unit (paragraph, section, argument block) rather than by a fixed token count. A 500-token boundary drawn mid-sentence produces two fragments that are individually ambiguous and poorly retrieve against any query. Splitting at paragraph or section boundaries preserves the unit of meaning, even when chunk sizes become irregular.

**Synthetic question generation** takes each chunk and asks an LLM: what questions would this chunk answer? Those generated questions are indexed alongside (or instead of) the raw chunk text. At query time, user questions match indexed questions far more reliably than they match prose, because the vocabulary and phrasing align better. The technique is formalized in the doc2query line of work (Nogueira & Lin, 2019) and in HyDE (Hypothetical Document Embeddings, Gao et al., 2022). In production systems, practitioners have observed retrieval improvements in the 10% range on their evaluation sets, though gains vary significantly with dataset and embedding model.

The two techniques compose well with Anthropic's contextual retrieval approach described above: contextualize each chunk first, then generate synthetic questions from the contextualized version. The questions inherit the surrounding document context and produce richer index entries.

*Source: Guillaume Laforge (Developer Advocate, Google Cloud), [IFTTD ep 361 "Pourquoi le RAG n'est pas mort"](https://www.ifttd.io/episodes/rag); doc2query: Nogueira & Lin (2019); HyDE: Gao et al. (2022).*

### RAG Triad Evaluation

The RAG Triad is a framework for evaluating RAG output quality across three dimensions:

| Dimension | Question | What it catches |
|-----------|----------|----------------|
| **Context Relevance** | Is the retrieved context relevant to the question? | Retrieval failures |
| **Answer Relevance** | Is the answer relevant to the question? | Generation drift |
| **Groundedness** | Is the answer supported by the retrieved context? | Hallucination |

All three can fail independently. A system can retrieve perfectly relevant context and still hallucinate (groundedness failure). It can generate a relevant answer not supported by what was retrieved. Evaluating all three simultaneously identifies which part of the RAG pipeline is the weak link.

Arize Phoenix implements the RAG Triad as a production evaluation framework (see section 9).

---

## 7. Memory Systems

Long-running agents face a variant of the context rot problem: session history grows until it exceeds the context window, or until early context is effectively ignored. Memory systems solve this by moving information out of the context window and into persistent storage, retrieving it on demand.

### Short-Term: Compaction and Structured Note-Taking

For Claude Code specifically, two mechanisms handle session-level memory:

**`/compact`** summarizes the conversation history, replacing the raw exchange with a dense summary. The model retains continuity but the token count resets substantially. Use at 70% context usage, not 90%.

**Structured note-taking via hooks** is the agentic version: a PostToolUse hook writes key decisions, discovered facts, and task state to a notes file. The agent loads this file at the start of the next session. This sidesteps context rot entirely for multi-session work — the notes file sits at the start of the context (maximum attention) and contains only curated information.

**Auto Memory (v2.1.59+)** and **Auto Dream** provide native CC alternatives: Claude writes its own `MEMORY.md` between sessions, and a background sub-agent consolidates it after ≥5 sessions and ≥24 hours. See [Memory Systems: Auto Memory](../core/memory-systems.md#22-auto-memory-v21594).

### Long-Term: External Memory Systems

For multi-session and multi-agent workflows, persistent memory systems store information outside the context window and retrieve it selectively. The CC ecosystem has a three-tier model:

**Individual (no team)**: claude-mem (89K stars, hooks-based auto-capture), agentmemory (26K stars, BM25+vector+graph fusion, 95.2% R@5), ICM (Rust binary, dual decay+graph architecture, `brew install icm`). Stars verified 2026-07-27.

**Team sharing**: CLAUDE.md + `.mcp.json` + skills committed to the repo (the Trinity, zero infra). Mem0 Cloud MCP for pooled team memory. Zep/Graphiti for temporal knowledge graphs.

**The RAG-vs-Memory distinction**: RAG is the model's access to external world knowledge (docs, codebase, web). Memory is its access to user-specific and session-specific knowledge (preferences, past decisions, continuity). Both are retrieval systems serving different parts of the information architecture. A well-designed agent uses both.

> **Canonical reference**: [Memory Systems guide](../core/memory-systems.md) — 20-tool comparison table, architecture patterns, risk matrix, decision flowchart, and benchmarks.

---

## 8. KV Cache Infrastructure

This section has two parts. The first covers Anthropic's prompt caching mechanics as they apply to Claude Code, including how Claude Code structures requests to maximize hit rates. The second covers self-hosted inference infrastructure for teams deploying their own LLMs.

### What is the KV Cache?

During the prefill phase (processing the input), the transformer computes Key-Value pairs for every token in the context. These pairs are stored in GPU VRAM, not as raw text or token hashes. For a 100K-token prefix on Opus, the KV data occupies approximately 500MB–1GB of VRAM.

For subsequent requests that share a prefix (e.g., the same system prompt), these stored KV values can be reused rather than recomputed. This is KV cache reuse. The autoregressive nature of transformers imposes one strict constraint: only prefixes can be cached. If token N changes, the KV entries for tokens N+1 onward must be recomputed. A modification anywhere in the prefix invalidates everything downstream.

Without KV cache reuse, every request processes the full context from scratch. With effective caching, only the unique portion of each request (the user message, new tool results) requires fresh computation. Anthropic's prompt caching reduces both latency and cost: cached tokens on Opus are billed at approximately $0.50/M versus $5/M for uncached input tokens. Cache hits require the shared prefix to be long enough (typically 1,024+ tokens) and recent enough (cache expires after approximately 5 minutes without access).

### KV Cache Compression: Research Frontier

Distinct from prompt *caching* (reusing an unchanged prefix) is KV cache *compression*: shrinking the cached tensors themselves, since the KV cache can consume up to 70% of inference memory on long contexts. Three technique families dominate current research: selective token eviction (keep the most relevant, discard the rest), quantization (lower numerical precision), and low-rank compression. Recent work like ChunkKV compresses by semantic chunk rather than token-by-token to preserve linguistic coherence, and TurboQuant (ICLR 2026) applies a random orthogonal rotation before quantization to even out variance. This is an active systems/MLOps research area as of 2026, not yet standardized tooling you install. It matters primarily to teams running self-hosted inference (below), not to Claude Code API users, whose caching is fully managed by Anthropic.

### How Claude Code Uses Prompt Caching

Claude Code structures every request to maximize cache hit rate. The request order matters because of the prefix constraint: items that change most often must appear last.

**Request structure (most stable to least stable)**:

1. **System prompt** — Identical across all Claude Code users on the same version. Shared cache: all users on the same version benefit from the same cached KV entries when Anthropic serves the system prompt from shared GPU memory.
2. **Tool definitions** — Static per session. Locked at session start. Adding or removing tools mid-session invalidates the entire conversation cache, which is why Claude Code locks the tool list when a session begins.
3. **Project config / CLAUDE.md** — Injected as message content (via `<system-reminder>` blocks in messages), not in the system prompt.
4. **Conversation history** — The sliding breakpoint: only new turns require fresh computation.

**Why CLAUDE.md is not in the system prompt**: If CLAUDE.md content were injected into the system prompt, each user's prefix would be unique (different projects, different configs), and the shared caching benefit of the ~30K-token system prompt would disappear. By keeping the system prompt identical for all users and injecting CLAUDE.md as message content, Anthropic can amortize the system prompt computation cost across every concurrent Claude Code session. CLAUDE.md still gets cached once it appears in the conversation history, but the system prompt itself stays universally shared.

**Production hit rates**: In real Claude Code sessions, prompt caching achieves approximately 96% hit rate. The simple reason is that the system prompt, tool definitions, CLAUDE.md content, and prior conversation turns all hit the cache; only the new user turn and the model's response are fresh computation.

### Cache Anti-Patterns

**Timestamps in the system prompt**: Any frequently-changing value in the system prompt prefix breaks caching by making every user's prefix unique. A Hacker News user reported recovering over 20 percentage points of cache hit rate by moving a timestamp field from the system prompt prefix into a message. The fix: move dynamic values (current date, git branch, file modification times) into message content, not the system prompt.

**Adding or removing tools mid-session**: Because tool definitions sit between the system prompt and conversation history in the request prefix, any change to the tool list invalidates the cache for the entire conversation. Claude Code avoids this by locking tool definitions at session start.

### Plan Mode: A Cache-Stable Design Pattern

Plan Mode restricts write access during planning phases. A naive implementation would be to remove write tools from the tool list while in Plan Mode. The problem: removing tools from the list changes the prefix, invalidating the entire session cache.

Claude Code's actual implementation: rather than removing tools, two new tools are added (`EnterPlanMode` and `ExitPlanMode`). The full tool list remains constant across mode switches. Mode behavior is conveyed through instructions in messages, not through changes to the tool definitions. The cache prefix stays identical whether Plan Mode is on or off.

This is a concrete example of a broader design principle: prefer instruction-level mode switching over structural changes to the request prefix.

### Compaction vs `/clear` for Cache Continuity

Compaction (`/compact`) preserves the cache. The compaction request reuses the same system prompt and tool definitions prefix, so cached KV entries from earlier in the session remain valid after compaction runs. Only the conversation history portion is replaced with the summary.

`/clear` followed by more than approximately 5 minutes of inactivity can result in a full cold start. The TTL for cached entries expires during the idle time, so the next request finds no cached KV entries for the system prompt or tool definitions. This is one reason Claude Code defaults to compaction rather than hard resets for long sessions: compaction preserves continuity without triggering cache expiration.

### Self-Hosted KV Cache Infrastructure

The following tools apply to teams deploying their own LLMs rather than using Anthropic's managed API.

### vLLM (PagedAttention)

vLLM is the dominant open-source inference engine for self-hosted LLMs. Its key innovation is PagedAttention: KV cache memory is allocated in fixed-size pages (analogous to OS virtual memory pages) rather than contiguous blocks.

Traditional KV cache allocation wastes 60–80% of GPU memory through fragmentation (allocating worst-case space per sequence). PagedAttention reduces this waste to under 4% by sharing pages across requests and allocating on demand.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) |
| **Key innovation** | PagedAttention (non-contiguous KV cache) |
| **Memory waste** | Reduced from 60–80% to <4% |

### SGLang (RadixAttention)

SGLang introduces RadixAttention: KV cache entries are organized as a radix tree (trie structure) keyed on the token sequence. When two requests share a prefix, their shared prefix's KV entries are reused automatically.

This is particularly powerful for:

- Multiple requests sharing the same system prompt (the trie stores it once)
- RAG pipelines where the retrieved document is constant across many queries
- Multi-agent systems where a base context is shared across subagents

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/sgl-project/sglang](https://github.com/sgl-project/sglang) |
| **Key innovation** | RadixAttention (trie-based automatic cache reuse) |
| **Best for** | Shared-prefix workloads, multi-agent systems |

### Semantic Caching

Semantic caching operates above the model layer: instead of caching KV activations, it caches complete LLM responses keyed on semantic similarity of the request. A new request that is semantically close to a cached request returns the cached response without an LLM call.

Redis, with vector search extensions, is the most common implementation. In high-repetition workloads (FAQ bots, internal search, code review pipelines with similar patterns), semantic cache hit rates of 30–60% are achievable, with some production deployments reporting 73% cost reduction.

The risk: cached responses become stale. Semantic caching requires TTL policies aligned with how frequently the underlying knowledge changes.

---

## 9. LLMOps & Observability

You cannot optimize what you do not measure. The LLMOps tooling category provides the instrumentation layer: tracing, cost tracking, quality evaluation, and drift detection for LLM-powered systems.

### Langfuse

The leading open-source option. Langfuse traces LLM calls across complex multi-step agent workflows, capturing input/output at each step, latency, cost per call, and the full execution tree.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/langfuse/langfuse](https://github.com/langfuse/langfuse) |
| **License** | Open-source (MIT) |
| **Deployment** | Self-hosted or cloud |
| **Best for** | Self-hosting requirements, cost analysis, trace debugging |

Key features for context optimization: per-session token cost breakdowns, trace comparison (which prompt variant is cheaper?), and custom evaluation metrics you can run on stored traces without rerunning the agent.

### LangSmith

LangSmith is Anthropic-adjacent (LangChain ecosystem) and the standard choice if you are building on LangChain or LangGraph. It excels at debugging chained operations where understanding the execution graph is as important as the individual LLM calls.

| Attribute | Details |
|-----------|---------|
| **Source** | [smith.langchain.com](https://smith.langchain.com) |
| **Best for** | LangChain/LangGraph workloads, chain debugging, A/B testing |
| **Features** | Dataset management, automated evaluation, regression testing |

### Arize Phoenix

Phoenix specializes in RAG quality evaluation, implementing the RAG Triad natively. It traces retrieval operations alongside generation, so you can correlate retrieval quality with final answer quality.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) |
| **License** | Open-source |
| **Specialty** | RAG evaluation, LLM-as-judge metrics, embedding drift |

Particularly useful for: identifying when retrieval is the bottleneck (context relevance failures) versus generation (groundedness failures). This distinction determines whether you fix the retriever or the prompt.

### Maxim AI

Maxim AI focuses on continuous evaluation: running automated evals against every production trace, not just offline test sets. It supports LLM-as-a-judge workflows (using an LLM to score another LLM's output) and A/B testing of prompt variants against production traffic.

| Attribute | Details |
|-----------|---------|
| **Source** | [getmaxim.ai](https://www.getmaxim.ai) |
| **Best for** | Continuous eval, A/B testing in production, regression detection |

### TruLens

TruLens implements the RAG Triad evaluation framework as an open-source library. It can be embedded directly in your application code, running evaluations inline as part of the application rather than in a separate observability platform.

| Attribute | Details |
|-----------|---------|
| **Source** | [github.com/truera/trulens](https://github.com/truera/trulens) |
| **License** | Open-source |
| **Best for** | Inline RAG evaluation, library integration, RAG Triad scoring |

### Choosing an Observability Tool

| Need | Recommended |
|------|------------|
| Self-host everything, cost analysis | Langfuse |
| LangChain ecosystem, chain debugging | LangSmith |
| RAG quality evaluation specifically | Arize Phoenix |
| Continuous prod eval, A/B testing | Maxim AI |
| Embed RAG Triad in app code | TruLens |

These tools are not mutually exclusive. Langfuse for tracing plus Phoenix for RAG evaluation is a common combination.

---

## 10. Tool Selection by Use Case

### You are a Claude Code user (individual developer)

| Problem | Tool |
|---------|------|
| Command outputs flooding context | RTK |
| File reads consuming most of context budget | tilth, lean-ctx, or Token Savior |
| Monitoring token spend | ccusage (see [Third-Party Tools](./third-party-tools.md)) |
| Context growing too long in a session | `/compact` at 70% usage |
| Forgetting past session decisions | ICM memory system |
| Claude ignoring rules from long CLAUDE.md | Path-scoping (see [context engineering guide](../core/context-engineering.md)) |

### You are building an AI application

| Problem | Tool |
|---------|------|
| Tool output JSON too verbose | Headroom |
| Prompts too long, need compression | LLMLingua |
| Routing across multiple LLM providers | Portkey |
| Compression + guardrails at the edge | Edgee |
| RAG chunks losing context | Anthropic Contextual Retrieval |
| Tracing agent execution | Langfuse or LangSmith |
| RAG quality measurement | Arize Phoenix |
| Continuous evaluation | Maxim AI |

### You are deploying a self-hosted LLM

| Problem | Tool |
|---------|------|
| GPU memory efficiency | vLLM (PagedAttention) |
| Shared-prefix caching (multi-agent, RAG) | SGLang (RadixAttention) |
| Caching repeated queries semantically | Redis with vector search |

---

## 11. Research Landscape

Active research directions that have not yet shipped as production tools (March 2026), plus a newer batch of April to July 2026 papers proposing concrete mitigation architectures rather than further documenting the original context-rot problem: ACON, Recursive Language Models, Context Kubernetes, AMA-Bench, ContextBudget, and Classifier Context Rot. Full summary with confidence levels: [Context Engineering: New Research Directions](../core/context-engineering.md#new-research-directions-april-to-july-2026).

### SlimInfer (Dynamic Token Pruning)

SlimInfer identifies redundant token representations in intermediate transformer layers and prunes them during inference. Published results: 2.53x speedup on Time-to-First-Token for LLaMA 3.1 without measurable quality degradation. The mechanism: mid-layer representations for many tokens converge to near-identical values; pruning these redundant representations saves computation without losing information.

### TopV (Visual Token Pruning)

For multimodal models (vision-language models), image tokens dominate context usage. A 1024x1024 image can generate thousands of visual tokens, most of which encode uninformative patches (backgrounds, margins). TopV formulates patch selection as an optimization problem (Sinkhorn algorithm), retaining only the visual regions relevant to the reasoning task. Published results show significant TTFT reduction on VLM inference with maintained task performance.

### The Token Reduction Effect on Hallucination

A finding that cuts across multiple research directions: token reduction in generative models does not just reduce cost — it measurably reduces hallucination and "overthinking" on simple queries. The mechanism is not fully understood, but the correlation is consistent across studies. Shorter, more precise contexts yield more grounded, less verbose outputs. This strengthens the case for MVC as a reliability principle, not just a cost principle.

---

> **Cross-references**
>
> - [Context Engineering (configuration guide)](../core/context-engineering.md) — CLAUDE.md hierarchy, path-scoping, budget management
> - [Third-Party Tools](./third-party-tools.md) — RTK full reference, ccusage, ICM, and other CC-specific tools
> - [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) — MCP as dynamic context injection
> - [Observability](../ops/observability.md) — Monitoring Claude Code in production
> - [Ultimate Guide: Memory Systems](.#memory-hierarchy) — Complete memory architecture for Claude Code
