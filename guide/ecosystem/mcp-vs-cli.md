---
title: "MCP vs CLI: Decision Guide"
description: "When to use MCP servers vs CLI tools in Claude Code workflows. Tradeoffs, decision dimensions, and guidance by situation."
tags: [mcp, cli, tokens, architecture, decision]
keywords:
  - "context7 mcp vs cli"
  - "mcp vs cli"
  - "cli vs mcp"
  - "context7 cli vs mcp"
  - "claude code mcp vs cli"
  - "figma mcp vs cli"
  - "linear mcp vs cli"
---

# MCP vs CLI: Decision Guide

**Last updated**: May 2026

> Interactive version with guidance table and practitioner quotes: [cc.bruniaux.com/ecosystem/mcp-vs-cli/](https://cc.bruniaux.com/ecosystem/mcp-vs-cli/)

The debate emerged from a rapid succession of interface paradigms: browser-based AI (2022-23), then AI in the IDE with MCP connecting agents to external services (2024-25), then full CLI agents that execute commands and write files without an intermediary layer (2025-26). That progression explains why the question exists at all.

This page compares two integration patterns for giving Claude Code access to external tools and services: MCP servers and CLI tools. Neither is universally better. The right choice depends on your context, and most real workflows end up using both.

---

## What each approach does

**MCP servers** inject tool schemas into Claude's context at session start. Claude sees a structured list of available tools with parameters, types, and descriptions. It then calls those tools natively, receiving structured responses.

**CLI tools** are shell commands that Claude invokes via Bash. Claude drives them the same way a developer would: constructing command strings, parsing text output. No schema injection at startup. The shell is the interface.

---

## Tradeoffs

### MCP strengths

| Advantage | Detail |
|-----------|--------|
| **Structured interface** | Tool schemas guide Claude precisely, fewer hallucinated flags or arguments |
| **Complex auth** | OAuth, token refresh, secrets rotation handled by the server, not the prompt |
| **Structured output** | JSON responses are directly parseable by Claude and downstream agents |
| **Observability** | Remote MCP servers can log every call, essential for enterprise usage tracking and ROI attribution |
| **Distribution at scale** | Update the server once, all connected clients get the change. No per-machine package management. |
| **Non-technical users** | Users who never touch a terminal can access tools transparently via MCP connectors |
| **Weaker models** | A structured schema compensates when the model is less capable of parsing CLI help text |

### CLI strengths

| Advantage | Detail |
|-----------|--------|
| **Zero context overhead** | No schema injected at startup. Since v2.1.7 lazy loading closes most of the gap, but CLI is still the absolute minimum. |
| **Deterministic actions** | Explicit commands with predictable output are easier to audit and test |
| **Human + AI use** | The same CLI wrapper works for a developer running it manually and for Claude |
| **Frontier models** | Claude Opus/Sonnet (current generation) can drive complex CLIs (aws-cli, glab, gh) without a structured schema |
| **Speed** | No connection setup, no MCP handshake, direct subprocess execution |
| **Simplicity** | Easier to debug, log, and reason about than a remote server call chain |
| **Skills encapsulation** | A CLI wrapped in a skill is transparent to the user and keeps the tool logic version-controlled |

### MCP weaknesses

| Weakness | Detail |
|----------|--------|
| **Schema token cost** | Since v2.1.7, lazy loading (MCP Tool Search) means unused tools inject only their name, not their full schema. Cost is still non-zero: tool names load at startup, full schemas load on first use. The pre-v2.1.7 worst case (~55K tokens for a 5-server setup) now averages ~8.7K (an 85% reduction), but not zero. |
| **Connection overhead** | Session startup takes longer with many MCP servers connected |
| **Debugging difficulty** | Failures inside an MCP server are harder to trace than a failed shell command |
| **Maintenance complexity** | Running, updating, and securing remote MCP servers adds infrastructure |
| **Overkill for simple APIs** | A GitLab MCP that surfaces 20% of glab's functionality is worse than glab itself |

### CLI weaknesses

| Weakness | Detail |
|----------|--------|
| **No observability** | Shell commands on a local machine are invisible to ops/management tooling |
| **Distribution problem** | Keeping CLIs updated across a team requires package management discipline (brew, scoop, etc.) |
| **Weaker models struggle** | A less capable model may hallucinate flags or misread help text; schemas help |
| **No multi-agent structure** | CLI output requires parsing; structured MCP responses are more reliable across agent-to-agent handoffs |
| **Non-tech user barrier** | A non-technical user cannot be expected to have a configured CLI environment |

---

## The API wrapper pattern

Most production MCP servers for SaaS tools sit on top of existing REST or GraphQL APIs. The server translates tool calls into HTTP requests against those APIs, processes responses, and returns structured output to the agent. It does not add backend capabilities that the underlying API lacks.

Official documentation from four major providers confirms this directly:

- **Notion**: "converted MCP tool calls into HTTP API calls to Notion's public API" (Notion engineering blog)
- **Sentry**: "middleware to the upstream Sentry API, optimized for coding assistants like Cursor and Claude Code" (sentry-mcp README)
- **Slack**: "a wrapper around an external API, like Slack" (Slack developer docs)
- **GitHub**: "integrates with GitHub, allowing LLMs to interact with repositories via the GitHub API" (github-mcp-server README)

The practical consequence: a CLI script calling the same REST or GraphQL API has the same capabilities. MCP and CLI reach the same backend, with the same credentials, triggering the same operations. The difference is the interface layer, not what the backend can do.

What MCP adds that a CLI cannot replicate:

- **OAuth token management**: server-held auth with browser redirect flows (Slack, Google Drive, Figma, hosted Notion). A CLI can hold an API key in an env var, but not a refresh token or a PKCE exchange, which require server-side state.
- **LLM-tuned schemas**: curated tool selection, not the full API surface, with parameter types and descriptions calibrated for agent reasoning.
- **Centralized hosting**: one deployment serves many clients; CLIs require per-machine installation and per-user credential configuration.
- **Usage attribution**: remote MCP servers associate each tool call with a user and session, feeding observability dashboards. Local CLI calls on developer machines are invisible.

This sharpens the decision criterion. If a service authenticates via API key or environment token, a CLI calling the same API is functionally equivalent to an MCP server. The question becomes whether you need OAuth, centralized observability, or cross-client standardization. If none of those apply, the CLI avoids the schema overhead and reaches the same backend.

---

## The four decision dimensions

Before asking "MCP or CLI?", answer these four questions. They rank from most to least constraining.

### 1. Who is the end user?

This is the dominant variable. Everything else is secondary.

- **Non-technical user** (using a chat interface, no terminal) → **MCP or skill-encapsulated CLI**. You cannot expose a raw CLI to a non-dev user. Connectors must be MCP-based or wrapped invisibly in a skill that handles the CLI internally.
- **Technical user / developer** → continue to question 2.

### 2. Which model is driving the tool?

- **Frontier model** (Claude Opus/Sonnet, current generation) → strong enough to drive complex CLIs directly. A structured MCP schema adds overhead without proportional benefit.
- **Smaller or local model** (Qwen, Mistral, lighter deployments) → structured MCP schemas compensate for weaker CLI parsing ability. MCP is more reliable here.

### 3. Does your organization need observability?

- **Yes** (enterprise, C-level reporting, compliance, ROI attribution on AI spend) → **MCP Remote server**. Local CLI calls are invisible. A remote MCP server can log every tool invocation, associate it with a user, and feed dashboards. You cannot replicate this with CLIs on local machines.
- **No** (individual dev, local workflow) → observability is not a constraint. CLI is fine.

### 4. How often does the tool schema change?

- **Stable API** (mature tool, versioned interface) → MCP investment pays off over time.
- **Rapidly changing** or **thin wrapper** → CLI is cheaper to maintain. A hand-rolled glab wrapper that exposes only the 5 commands you actually use is more durable than a GitLab MCP that duplicates the full API surface.

---

## Guidance by situation

Quick reference, not rules, but directional defaults.

| Situation | Lean toward | Rationale |
|-----------|-------------|-----------|
| Non-technical user, chat interface | **MCP / Skill** | CLI is inaccessible; connectors must be invisible |
| Frontier model (Claude, current generation), developer workflow | **CLI** | Model handles it natively; schemas are overhead |
| Smaller/local model | **MCP** | Schema guides the model reliably |
| Enterprise, observability required | **MCP Remote** | Only way to log, attribute, and report on usage |
| Team distribution (10+ devs) | **MCP** | Central update vs per-machine CLI maintenance |
| Individual dev, local machine | **CLI or skill** | Simpler, faster, no infrastructure |
| Deterministic actions (git, CI, deploy) | **CLI** | Explicit commands, predictable output, auditable |
| Complex auth (OAuth, token refresh) | **MCP** | Server handles auth; CLI would require credential plumbing |
| Tight context budget / many tools loaded | **CLI** | Still the minimum-overhead option. Lazy loading (v2.1.7+) reduces MCP cost significantly, but CLI has zero schema cost by design. |
| Agent-to-agent structured output | **MCP** | JSON responses are more reliable than parsed CLI text |
| Debugging / prototyping a new integration | **CLI** | Easier to inspect, faster to iterate |
| Browser automation (non-frontier model) | **MCP** | Playwright MCP structures interaction reliably |
| Browser automation (frontier model, Claude Code) | **CLI + skill** | playwright-cli + skill reported faster and more efficient in practice |
| GitLab / GitHub access | **CLI** (glab, gh) | Official CLIs are richer than most MCP wrappers |
| Documentation lookup (Context7) | **MCP** | No CLI equivalent; structured doc retrieval has no shell analog |

---

## Per-server recommendation

The table below applies the four decision dimensions to the 18 most commonly discussed MCP servers. "Verdict" is the default for a developer using a frontier model on a local machine. Your context (non-technical users, enterprise observability, or a smaller model) may shift any row toward MCP.

| MCP Server | Verdict | CLI Alternative | Reason |
|------------|---------|-----------------|--------|
| GitHub MCP | **Use CLI** | `gh` | `gh` covers the full API surface; model knows it from training; official GitHub MCP was archived |
| GitLab MCP | **Use CLI** | `glab` | Official CLI is richer than the MCP wrapper; practitioner consensus confirms |
| Git MCP (Anthropic) | **Use CLI** | `git` | Git is the CLI the model knows best; MCP schema adds cost without structural benefit on frontier models |
| Filesystem MCP | **Use CLI** | `cat`, `ls`, `find` | Shell commands are universal; no benefit from schema overhead |
| Docker MCP | **Use CLI** | `docker` | Docker CLI is universally known; no widely adopted MCP adds comparable value |
| AWS MCP | **Use CLI** | `aws-cli` | aws-cli v2 covers the full surface; model drives it natively from training knowledge |
| Terraform MCP | **Use CLI** | `terraform` | Deterministic plan/apply workflow; CLI output is structured and auditable |
| Semgrep MCP | **Use CLI** | `semgrep` | Mature CLI, well-documented; MCP adds value mainly in CI/CD observability contexts |
| Playwright MCP | **Depends** | `playwright-cli` + skill | Frontier model: CLI + skill is faster. Smaller model: MCP structures browser interaction reliably |
| Kubernetes MCP | **Depends** | `kubectl` | Auth complexity and multi-cluster setups favor MCP; simple operations favor kubectl |
| Vercel MCP | **Depends** | `vercel` CLI | CLI for deploy, env, and domains; MCP for dashboard integration and team workflow comments |
| Sentry MCP | **Use MCP** | `sentry-cli` (CI/CD scoped) | `sentry-cli` handles releases, source map uploads, and CI/CD ops, but has no equivalent for interactive issue querying. MCP provides structured error triage for coding agents. |
| Slack MCP | **Use MCP** | none | OAuth required; no practical CLI for workspace access from an agent |
| Notion MCP | **Use MCP** | none | OAuth required; API-key access is limited to integrations, not user-scoped workspace access |
| Google Drive MCP | **Use MCP** | none | OAuth 2.1 with refresh token rotation; cannot be replicated by a skill or CLI |
| Figma MCP | **Use MCP** | none | OAuth required; design file access has no CLI equivalent |
| Linear MCP | **Use MCP** | none | MCP handles GraphQL complexity; structured project management without raw API calls |
| Context7 MCP | **Use MCP** | none | No CLI equivalent for curated, version-specific doc retrieval |

The pattern: if the service has a mature CLI the model knows from training, use the CLI. If the service requires OAuth or has no CLI, use MCP. "Depends" means the decision hinges on model capability or specific workflow needs.

> Take the interactive quiz (6 questions, under 1 minute): [cc.bruniaux.com/mcp-or-cli/](https://cc.bruniaux.com/mcp-or-cli/)

---

## The hybrid is the default

Most production workflows don't choose one. They use both, with each covering the layer it handles best.

**A practical example** (from practitioners):

- **Inner layer** (local dev iteration, git, file ops, shell scripts) → CLI, fast, deterministic, no overhead
- **Outer layer** (CI/CD, shared infrastructure, cross-team services) → MCP Remote, observable, centralized, scalable
- **Skill layer** (user-facing actions, CLI tools encapsulated for non-tech users) → CLIs wrapped in skills, transparent to the end user

The mistake is applying one answer to both layers. A solo developer building a Claude Code workflow for themselves should mostly use CLIs. A team deploying an AI assistant to non-technical colleagues should mostly use MCP.

---

## Token cost of MCP schemas: what the numbers look like

Since v2.1.7 (January 2026), Claude Code uses **MCP Tool Search** (lazy loading) by default. This changes the token math significantly, but does not eliminate schema cost entirely.

**How lazy loading works:** instead of injecting all tool schemas at session start, Claude receives only tool names in an `<available-deferred-tools>` block. Full schemas are fetched via `ToolSearch` only when Claude decides to call a specific tool. Unused tools in a session cost only their name in context (~0 schema tokens), not the full definition.

**Measured impact** (Anthropic benchmarks, 5-server setup):

| Scenario | Token overhead | Note |
|----------|---------------|------|
| Before v2.1.7 (eager loading) | ~55,000 tokens | All schemas preloaded |
| After v2.1.7 (lazy loading) | ~8,700 tokens | 85% reduction |
| CLI (no MCP) | ~0 tokens | Baseline |

The old worst-case claim of "500-2,000 tokens per server" described eager loading, which is no longer the default. With lazy loading, the cost per unused server is near zero. The cost per *used* server (~600 tokens per tool schema loaded on demand) remains real, but is now pay-per-use rather than always-on.

**What still adds overhead even with lazy loading:**

- Tool names are still injected at startup (one line per tool per server)
- Schemas load at first invocation; long sessions using many tools accumulate cost
- Connection setup per server is unchanged (latency, not tokens)
- Many connected MCP servers still means more names in context, even if schemas stay deferred

**Configuration** (v2.1.9+): the `ENABLE_TOOL_SEARCH` environment variable controls the threshold. `auto:N` triggers lazy loading when MCP tools exceed N% of context (default 10%).

**Mitigation strategies** (still relevant, lower urgency):

- Load MCP servers selectively per project (project-level config vs global config)
- Use CLI tools for high-frequency tight loops where any overhead compounds (compile → test → fix)
- Monitor token usage per session to identify which schemas are being loaded at invocation time
- Consider a CLI wrapper for tools you use constantly but don't need structured output from

---

## Tooling in this space

| Tool | What it does | Status |
|------|-------------|--------|
| **RTK** (Rust Token Killer) | Filters CLI output before it reaches Claude's context (reduces response verbosity, not schema overhead) | Production-ready, actively maintained |
| **mcporter** (steipete, now under openclaw) | TypeScript runtime for calling MCP servers from scripts, generating CLI wrappers, and emitting typed TS clients. Useful for testing MCP servers and writing hooks that need MCP access. | 4.8K stars (2026-07-27, was 3K), MIT, ready to use. Repo transferred to `openclaw/mcporter`. |
| **mcp2cli** (knowsuchagency) | Converts MCP/OpenAPI/GraphQL to runtime CLI, eliminating schema injection. Benchmarked at 32× token reduction on the 43-tool GitHub MCP server (44K → 1.4K tokens). | 2.3K stars (2026-07-27, was ~1.9K), Show HN Best of March 2026, production-viable for remote MCP servers with 10+ tools. See [full breakdown](./third-party-tools.md#mcp2cli). |
| **Klavis AI / Strata** (Klavis-AI/klavis, YC X25) | Hosted catalog of 50+ MCP servers with enterprise OAuth; Strata attacks catalog-size cost directly via "progressive discovery" instead of exposing every tool upfront. | 5.8K stars (2026-07-27, was ~5.5K). On the vendor's own MCPMark benchmark: +15.2% pass@1 vs. the official GitHub MCP server, +13.4% vs. the official Notion server, alongside 85-100x token reduction. Vendor-reported, not independently reproduced, but notable for including a task-success metric rather than only a token count. Paid tiers from $79/mo. |
| **Arcade.dev** (ArcadeAI/arcade-mcp) | Open-source Python framework fronting 7,500+ ready-made tools across 81 MCP servers (Slack, Google Workspace, Salesforce). | Framework is open source; the hosted runtime is paid. Vendor benchmark against Composio on 8 CRM queries: 7,426 tokens vs. 747,083 (100x+). Still a vendor comparison, and still no task-resolution metric, only token count. |

Note on mcp2cli: the token savings are real for direct API use, remote MCP servers, and CI/CD pipelines, benchmarked independently by Firecrawl, Scalekit, and CircleCI. For standard Claude Code sessions where lazy loading (v2.1.7+) already defers most schemas, the gain is smaller. mcp2cli applies most clearly when you drive MCP tools from scripts or agents that don't have deferred loading built in.

**A separate axis, easy to conflate with the table above**: every tool listed here reduces token cost. Klavis's OAuth and hosted-catalog side sits on a different axis entirely, access governance, who is allowed to call what, with which credential, under which approval, and that is where it overlaps with tools like Executor rather than with mcp2cli or Arcade. Confusing the two axes makes a governance tool look weak on a table whose column headers were never measuring what it does. That category is covered separately: [enterprise-governance.md §3.5](../security/enterprise-governance.md#35-watch-executor-the-registry-pattern-as-a-product).

---

## MCP vs Skills

Skills (`.claude/skills/*.md`) are a third integration paradigm, distinct from both MCP servers and CLI tools. Conflating them with CLIs is the most common framing error in this space.

**What each layer does:**

- **Skills** encode *how the agent should behave*: step-by-step workflows, decision trees, and SOPs written in markdown. They are loaded on demand into the agent's context and guide its reasoning without injecting external tool schemas.
- **MCP servers** provide *structured access to external systems* (APIs, databases, file systems) with typed tool interfaces the agent calls directly.
- **CLI tools** provide *command-line access to external systems*: the agent constructs shell commands and parses text output.

Skills and MCP address different layers, not the same problem. A skill can describe when and how to invoke an MCP tool (check this field, then call that tool) while the MCP server handles the actual connection. Asking "should I write a skill or an MCP server?" usually means the layers are being conflated.

### The OAuth boundary

This is MCP's clearest structural advantage over skills, and it's not a matter of convenience.

A skill can instruct an agent to "authenticate with Google Drive before proceeding." What it cannot do is hold a refresh token, complete a browser redirect, or manage a PKCE exchange. Those operations require server-side state, which a markdown file does not have.

Enterprise SaaS APIs (Google Workspace, Salesforce, Slack, GitHub) require OAuth 2.1 with refresh token rotation. When that is the authentication mechanism, MCP is not just more convenient: it is the only option that works without asking the user to paste credentials manually at the start of every session.

Practical test: if the service authenticates via an API key in a header, a skill or CLI can handle it. If it requires a browser redirect or server-held refresh token, that belongs in MCP.

### Community consensus (2026)

The debate has largely settled on a three-layer model rather than a binary choice:

- **Skills** handle *what to do and when*: workflow orchestration, decision guidance, reproducible agent behavior
- **MCP** handles *connectivity and auth*: external systems that require structured interfaces, OAuth, or enterprise observability
- **CLI** handles *deterministic local operations*: git, file ops, test runners, anything the model can drive directly from training knowledge

The convergence is now part of the spec: SEP-2640 ("Skills Over MCP") proposes distributing skills as MCP resources, so users install workflows the same way they install tool servers. The two paradigms are being unified rather than forced to compete.

---

## What practitioners say

A few representative perspectives from experienced Claude Code users:

> "I prefer CLI for deterministic actions. For GitLab interactions I use glab (the GitLab MCP is too limited) wrapped in a custom CLI, usable by both humans and AI." (practitioner)

> "On Claude Code with frontier models, fewer MCPs is better. I replaced playwright-mcp with playwright-cli plus skill, faster and more effective. I still use context7-mcp only because I haven't found a CLI equivalent." (practitioner)

> "The CLI vs MCP debate is only happening among devs doing dev things. But there's one fundamental constraint: you cannot propose a CLI solution to a non-technical user who just wants to use their tool simply." (practitioner)

> "For enterprise industrialization, observability is non-negotiable. CLI on a local machine is a black box. MCP Remote gives you the logging that C-levels need to attribute investment." (practitioner)

> "Frontier models are strong enough to drive a CLI directly. A weaker local model will struggle, that's where MCP schemas earn their overhead." (practitioner)

---

*Back to [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) | [Third-Party Tools](./third-party-tools.md) | [Main guide](../ultimate-guide.md)*
