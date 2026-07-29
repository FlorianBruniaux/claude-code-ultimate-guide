---
title: "Context Engineering"
description: "Comprehensive guide to filling Claude's context window with the right information at the right time — configuration hierarchy, budget management, modular architecture, team assembly, and quality measurement"
tags: [context, configuration, architecture, team, advanced]
---

# Context Engineering

> **Confidence**: Tier 1 — Based on official documentation, measured production data, and community validation.
>
> **Last updated**: March 2026

"Context engineering is the art of filling the context window with the right information at the right time." — Andrej Karpathy

This guide covers everything from the token math behind context budgets to building modular, team-scale configuration systems. It is a companion to the broader configuration sections in the ultimate guide — where those sections show individual techniques, this document shows how to compose them into a coherent system.

---

## Table of Contents

1. [What is Context Engineering](#1-what-is-context-engineering)
2. [The Context Budget](#2-the-context-budget)
3. [Configuration Hierarchy](#3-configuration-hierarchy)
4. [Modular Architecture](#4-modular-architecture)
5. [Team Assembly](#5-team-assembly)
6. [Context Lifecycle](#6-context-lifecycle)
7. [Quality Measurement](#7-quality-measurement)
8. [Context Reduction Techniques](#8-context-reduction-techniques)
9. [Maturity Assessment](#9-maturity-assessment)
10. [Token Audit Workflow](#10-token-audit-workflow)
11. [Research Patterns](#11-research-patterns-what-the-literature-shows)
12. [Attention Mechanics & Reliability](#17-attention-mechanics--reliability)
13. [Token Compression Tools](#18-token-compression-tools)

---

## 1. What is Context Engineering

### The Definition

Andrej Karpathy coined the phrase: **"Context engineering is the art of filling the context window with the right information at the right time."**

That single sentence contains three non-obvious requirements:

- **Filling**: the context window should be populated deliberately, not accidentally. Leaving it mostly empty wastes the model's capacity; leaving it chaotically full wastes your tokens and degrades output quality.
- **Right information**: not all information is equal. Architecture decisions are more valuable than linting preferences. Negative constraints ("never return raw SQL errors to the client") are more actionable than aspirational goals ("write clean code").
- **Right time**: path-scoped rules for backend code have no value when editing a frontend component. Loading everything always is the lazy approach that degrades adherence.

### A Contested Origin

Karpathy's mid-2025 post is the commonly credited source, but the attribution resurfaced as a live debate at the AI Engineer conferences in 2026. Dex Horthy, founder of HumanLayer and author of "12-Factor Agents," is now described in the AI Engineer conference's own materials as having coined the term, with an earlier antecedent: the "dumb zone," the 40 to 60% band of a large context window where recall degrades and reasoning weakens, based on an analysis of roughly 100,000 developer sessions. Treat this as a genuinely open question rather than a settled fact. What matters practically is not who said it first, but that two independent lines of observation, Karpathy's framing and Horthy's session-scale data, converge on the same conclusion: mid-window content is where instruction-following breaks down first.

### Prompt Engineering vs. Context Engineering

These terms are often conflated. The distinction matters:

| Dimension | Prompt Engineering | Context Engineering |
|-----------|-------------------|---------------------|
| Scope | One request | Entire session or system |
| Duration | Single interaction | Persistent across interactions |
| Effort | Per-request crafting | Upfront system design |
| Scale | Individual | Team-wide or organization-wide |
| Artifact | A prompt string | A configuration system |

**Prompt engineering** is about crafting the right question for one task. **Context engineering** is the system that ensures Claude has the right background knowledge before any task begins. You can have excellent prompts on top of poor context engineering and still get mediocre results — because the model lacks the structural understanding of your project, conventions, and constraints.

A practical analogy: prompt engineering is writing a good email to a contractor. Context engineering is the onboarding process, code style guide, architecture documentation, and team norms that ensure the contractor understands the project before reading a single email.

### Context Engineering vs. Context Optimization

Both terms appear in the literature and are sometimes used interchangeably. They are not the same.

| Dimension | Context Engineering | Context Optimization |
|-----------|--------------------|--------------------|
| Core question | What information should be in context? | What is the minimum set of high-signal tokens that maximizes the outcome? |
| Goal | Completeness and correctness | Efficiency and signal density |
| Method | Identify what the model needs to know | Remove everything it does not need to know |
| Failure mode | Missing critical information | Overshooting — too much irrelevant content |
| Output | A context system | A trimmed, high-fidelity prompt or config |

A useful mental model: context engineering answers "what to include," context optimization answers "what to cut."

In practice, you do both. The engineering pass builds the complete picture: architecture decisions, conventions, constraints. The optimization pass prunes it: removes redundancy, compresses verbose rules, archives outdated entries, path-scopes subsystem-specific content. The reduction techniques in Section 8 are the optimization pass.

**Synthesis vs. reasoning**

A related distinction worth naming explicitly:

- **Context synthesis** is stateful and iterative. It accumulates knowledge across sessions, updates when conventions change, and reflects project history. CLAUDE.md is context synthesis.
- **Reasoning** is ephemeral and disposable. Each inference step uses the context to produce an output, then discards the intermediate state. Claude's chain-of-thought is reasoning.

Treating reasoning artifacts (intermediate thoughts, debug traces, error outputs) as context synthesis material is a common mistake. It pollutes the context with ephemeral state and accelerates context rot. Separate what should persist (synthesis) from what should be discarded (reasoning noise).

### Why It Matters

LLMs are context-window computers. The quality of output is bounded by the quality of input. This is not a soft claim — it has a hard technical basis:

1. The model has no persistent memory between sessions (without explicit tooling). Every session starts from zero unless context is deliberately provided.
2. The model cannot infer unstated conventions. If you want TypeScript interfaces instead of `type` aliases, that must be stated. If you want errors logged before being thrown, that must be stated.
3. Models are sensitive to instruction placement and framing. An instruction buried in line 400 of a 500-line CLAUDE.md is less likely to be followed than one in the first 50 lines.

Teams that invest in context engineering consistently report fewer revision cycles, better adherence to conventions, and more predictable outputs. The investment is front-loaded (building the system), but the returns compound across every interaction.

A useful diagnostic reframe: **most AI output failures are context failures, not model failures.** When Claude generates a generic response, ignores a convention, or produces code that doesn't match your stack, the model is almost never broken — the context it received was incomplete, contradictory, or missing the right information at the right time. This reframe shifts troubleshooting from "the AI is bad at this" to "what is missing from the context?"

### The Three Layers

Context engineering in Claude Code operates across three distinct layers:

| Layer | Mechanism | Scope | When Loaded |
|-------|-----------|-------|-------------|
| **Global config** | `~/.claude/CLAUDE.md` | All projects | Always |
| **Project config** | `./CLAUDE.md` + path-scoped modules | Current project | Per session |
| **Session** | Inline instructions, `/add`, flags | Current session only | Runtime |

Each layer has different tradeoffs. Global config is always-on but cannot reference project-specific details. Session instructions are flexible but ephemeral. Project config is the workhorse: structured, versioned, reviewable.

Good context engineering means putting each piece of information in the right layer — not cramming everything into one file, and not leaving critical knowledge in the session layer where it evaporates after every conversation.

**Markdown files as shared persistent memory work better than a dedicated database for this purpose.** A plain Markdown file that multiple agents or sessions can read and append to serves as durable, human-readable memory without the operational overhead of standing up a store. Pairing that memory with a rules file that documents project conventions (naming, code style, architectural boundaries) gives the model the same onboarding a new engineer would need; without it, output quality and adherence to project style both suffer. (*Alex Gavrilescu, Devoxx, 2025. Konstantin Pavlov, 2025, reaches the same conclusion independently.*)

**A dedicated "research, then plan, then implement" sequence, each stage handed off through its own document, reduces rework on non-trivial tasks.** The pattern: a research document capturing findings with file and line-number references, then a plan document reviewed before any code changes, then implementation against that plan. Splitting research from planning from execution keeps each stage's context focused and gives a natural checkpoint to catch a wrong assumption before it propagates into code. (*Emmanuel Sciara, Dev With AI Meetup, 2026*)

### Static vs. Dynamic Context

The three-layer system above is *static context* — configuration files that are assembled before a session begins and remain stable throughout. Claude Code is primarily a static context system, which is why CLAUDE.md structure and path-scoping matter so much.

As you move toward agent workflows, a second category appears: *dynamic context*, assembled at inference time as the agent operates.

| Type | How assembled | Examples in Claude Code |
|------|--------------|-------------------------|
| **Static** | Before session, from files | CLAUDE.md, path-scoped modules, skills |
| **Dynamic** | At runtime, from tools | Tool outputs, file reads, web fetches, MCP data |

In practice, every Claude Code session uses both. The static context (your configuration) sets the behavioral envelope; the dynamic context (files Claude reads, tool results it processes) provides the specific information for each task. Context engineering covers both, but the failure modes differ: static context problems manifest as consistent convention violations; dynamic context problems manifest as Claude acting on stale or incomplete information mid-task.

For teams building automated pipelines and agents, Anthropic's September 2025 engineering post ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) covers the dynamic side in depth.

Anthropic's April 2026 [Managed Agents architecture](https://www.anthropic.com/engineering/managed-agents) pushes this further with a named separation: the harness and model ("brain"), the sandboxed execution layer ("hands"), and a durable session event log that lives entirely outside the context window. The harness reads from that log through a `getEvents()`-style interface, pulling positional slices back in on demand rather than keeping everything resident. Anthropic's stated rationale is that they cannot predict which context-management techniques future models will need, so durability belongs in the session layer while the context logic stays in the harness, which is expected to change. The companion post, ["Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), covers the open problem of preserving coherent progress across repeated context resets on multi-hour and multi-day tasks. See [AI Ecosystem §14](../ecosystem/ai-ecosystem.md#14-claude-managed-agents-cloud-hosted-platform) for the full architecture, including the append-only event log and checkpoint/restore mechanics already documented in this guide.

### Why Context Rot is Structural, Not Accidental

Transformer models attend to all tokens pairwise. That means the number of attention relationships in a context window grows as n², not n. Double the context length and you quadruple the number of relationships the model must weigh. At 200K tokens, this means billions of pairwise computations, and the model's attention becomes increasingly diffuse.

This is not a bug that future models will eliminate. It is a consequence of the architecture itself. Context rot, the progressive degradation of instruction adherence as context grows, is structurally baked in. The implication: you cannot solve context rot by relying on a larger context window. You solve it by keeping context lean and loading information just in time.

**The effect has been refined, not refuted.** A recurring critique through 2026 is that Needle-in-a-Haystack benchmarks measure only lexical retrieval. Once the question and the needle stop sharing obvious vocabulary (realistic, semantically ambiguous queries), degradation with length is worse than NIAH numbers suggest. One data point circulating in 2026, specific to its setup and not a general constant: Opus 4.6, used as a trajectory monitor on MonitorBench, dropped from 98.6% to 88% recall once 800K tokens of benign prior actions were prepended. Read it as evidence that the failure mode also hits monitor and classifier models, not just generation, rather than as a number to generalize past its own conditions.

**Just-in-time retrieval vs. pre-loading**

There are two strategies for giving Claude the information it needs:

| Strategy | Mechanism | When to use |
|----------|-----------|-------------|
| **Pre-loading (RAG)** | Retrieve and inject all potentially relevant context before inference | Known, stable context requirements |
| **Just-in-time retrieval** | Retrieve context on demand, exactly when and only when needed | Dynamic, task-specific context |

Pre-loading is the familiar RAG pattern: build a retrieval index, pull relevant chunks into the prompt upfront. It works when you know in advance what information the model will need.

Just-in-time retrieval is more demanding to implement but more effective at scale: the model retrieves information dynamically as the task demands it, using tool calls, MCP servers, or file reads. Only the information needed for the current step is in context.

Claude Code's behavior reflects this pattern: CLAUDE.md loads upfront (pre-loaded, always relevant), while file contents and tool results are retrieved at inference time via `read_file`, `glob`, `grep`, and MCP calls. The glob and grep tools are the JIT retrieval layer. They put specific file contents into context only when a task touches those files.

**In-context generation, plain RAG or a well-built prompt, often beats fine-tuning when the goal is teaching a model new knowledge.** Fine-tuning bakes facts into the weights through gradient updates, but it runs into a documented failure mode called the reversal curse: a model fine-tuned on "A is B" frequently cannot answer "what is B," even though the fact is logically symmetric. Retrieval keeps the fact as text in context rather than asking the model to generalize from a weight update, which sidesteps the problem entirely. Two independent Stanford courses converge on this point when advising teams choosing between the two approaches. (*Stanford CS25, 2026; CS230 Lecture 8, 2025*)

**Memory tool (beta)**

As of Claude Sonnet 4.5, Anthropic released a Memory tool in public beta. It allows Claude to store and retrieve persistent facts across sessions without manual CLAUDE.md management. The tool maintains a structured knowledge store that Claude queries when relevant context is needed.

This is distinct from CLAUDE.md: CLAUDE.md is static configuration (always loaded), while the Memory tool is dynamic retrieval (queried on demand). For teams building agents, the Memory tool reduces the need to manually encode knowledge in config files.

**Chain-of-thought in long tasks**

Chain-of-thought (CoT) prompting improves model reasoning on isolated tasks. However, Anthropic's engineering data shows it can hurt performance in long agentic tasks. The mechanism: CoT generates additional tokens, which extend context length, which accelerates context rot for subsequent steps. On tasks spanning 20+ tool calls, this effect is measurable.

The practical rule: use CoT for complex isolated reasoning steps, not as a blanket strategy for agentic workflows. In long runs, prefer compressed intermediate outputs over extended reasoning traces.

---

## 2. The Context Budget

### Token Math

A concrete baseline for a mid-size project:

| Source | Typical Token Range |
|--------|---------------------|
| Global CLAUDE.md | 1,000 – 3,000 tokens |
| Project CLAUDE.md (root) | 2,000 – 8,000 tokens |
| Path-scoped modules (all active) | 1,000 – 5,000 tokens |
| Imported skills / commands | 500 – 3,000 tokens |
| **Total always-on context** | **~5,000 – 20,000 tokens** |

Claude Sonnet 5 has a native 1M token context window. That means even a large always-on configuration budget (20K tokens) occupies about 2% of the window, leaving roughly 980K tokens for actual work: code files, conversation history, tool outputs. (Earlier models like Sonnet 4.6 topped out at 200K, where the same 20K budget cost about 10% of the window.)

The practical rule: **always-on context should stay below 5% of the context window.** Beyond that, you are displacing actual task content, which matters more per token than standing instructions.

### The 150-Instruction Ceiling

Empirical observation from teams running large CLAUDE.md files: beyond approximately 150 distinct rules, models begin selectively ignoring some of them. This is not a hard cutoff — it depends on rule complexity, overlap, and placement — but it is a reliable signal that more rules does not equal better adherence.

The mechanism is attention diffusion: when a prompt contains hundreds of potentially relevant constraints, the model's attention is split across them. High-salience rules (recent, strongly worded, placed early) crowd out lower-salience ones.

HumanLayer's production data shows teams with structured context — fewer, more specific rules, organized hierarchically — see 15-25% better adherence than teams with undifferentiated long rule lists.

Implication: **rule quality beats rule quantity.** Twenty specific, actionable rules outperform 200 generic aspirational ones.

### Adherence Degradation by File Size

```
Lines in CLAUDE.md    Adherence (estimated)
─────────────────     ─────────────────────
1 – 100               ~95%
100 – 200             ~88%
200 – 400             ~75%
400 – 600             ~60%
600+                  ~45% and falling
```

These are estimated baselines, not guarantees. Path-scoping and modular architecture can maintain higher adherence at larger total rule counts by ensuring that only relevant rules are in context at any given time.

### Signs of Context Overload

When always-on context becomes too large or too noisy, you see predictable failure modes:

- **Rule silencing**: Claude follows 80% of conventions consistently but ignores specific rules that should apply.
- **Contradictory behavior**: Claude applies a rule in some files but not others, or applies contradictory rules depending on phrasing.
- **Slow first responses**: The model spends more time processing a large context before generating output (observable in longer latency for simple tasks).
- **Generic outputs**: Instead of applying project-specific patterns, Claude falls back to generic best practices — a sign that project context is not being retained.

When you see these patterns, the diagnostic is: run a context audit (see Section 7), not more instructions.

### MECW: Maximum Effective Context Window

The advertised context window and the effective context window are not the same number. Enterprise context engineering deployments consistently find that meaningful accuracy degradation begins before the stated limit is reached. The commonly cited figure from production experience: approximately 92% of the advertised limit.

For Claude Opus 4 (200K advertised), this puts the practical ceiling at approximately 185K tokens before accuracy measurably degrades on complex reasoning tasks. The mechanism is the n² attention scaling described in Section 1 (Why Context Rot is Structural): as the context grows, attention operations scale quadratically, and mid-window positions receive diminishing effective weight.

Context rot degrades accuracy by 30%+ in mid-window positions under heavy context load. The practical implication: a 128K-token context window with high-quality, well-maintained content outperforms a 1M-token window with stale, accumulated content. The 1M window does not eliminate the problem; it delays it while increasing the cost of each request.

The question "should I just use the 1M context window?" is really a question about signal-to-noise, not capability. A larger window that accumulates tool output noise, expired conversation turns, and redundant instructions is not more powerful than a smaller, curated one. It is just more expensive and slower.

**Practical MECW targets**:

| Window | Advertised | Practical ceiling (92%) | When rot degrades accuracy |
|--------|-----------|------------------------|--------------------------|
| Claude Sonnet 4.6 | 200K | ~184K | ~150K+ |
| Claude Opus 4 | 200K | ~185K | ~150K+ |
| Claude Sonnet 5 | 1M | not yet benchmarked | not yet benchmarked |

These are engineering estimates, not guaranteed values. Treat them as planning figures: if your session regularly approaches 150K tokens, it is time to implement compaction, graduated offloading, or path-scoping before accuracy becomes a problem, not after.

**A sharp, non-linear quality drop shows up around 70% of the context budget used, rather than a smooth decline.** Nine speakers at the same meetup independently reported this same threshold, which this guide reads as a notably strong signal for a claim usually offered as a vague hunch. The practical consequence is about timing: purge or compact context before crossing that threshold, not after the drop already shows up in the output. (*Emmanuel Sciara, Dev With AI Meetup, 2026. Malo and Dorian, same event and year, describe the same shift as abrupt rather than gradual.*)

### Path-Scoping and Budget Efficiency

Path-scoping is the most effective single technique for reducing always-on context. Instead of loading all rules for all parts of the codebase, you load only the rules relevant to the files currently in context.

A typical project without path-scoping:

```
Always-on: root CLAUDE.md with backend + frontend + database + API rules = 8,000 tokens
```

The same project with path-scoping:

```
Always-on: root CLAUDE.md with shared rules = 2,000 tokens
Active when in src/api/: api module = +1,500 tokens
Active when in src/components/: frontend module = +1,200 tokens
Active when in prisma/: database module = +800 tokens
```

Result: 40-50% reduction in always-on context, with no loss of coverage. Each subsystem gets its full rule set, but only when working in that subsystem.

---

## 3. Configuration Hierarchy

### The Three-Layer Stack

```
┌──────────────────────────────────────────────┐
│  Global (~/.claude/CLAUDE.md)                │
│  Identity, tone, universal tools, cross-      │
│  project conventions                          │
├──────────────────────────────────────────────┤
│  Project (./CLAUDE.md + path modules)         │
│  Architecture decisions, stack conventions,   │
│  team rules, deployment procedures            │
├──────────────────────────────────────────────┤
│  Session (inline instructions, flags)         │
│  Ad-hoc overrides, experiment constraints,    │
│  one-off task parameters                      │
└──────────────────────────────────────────────┘
```

Later layers override earlier ones. A session instruction can override a project rule; a project rule can override a global default. This gives you escape hatches without requiring permanent changes to shared configuration.

### Global Configuration

**Location**: `~/.claude/CLAUDE.md`

**What belongs here**:
- Identity and communication style preferences
- Universal tool preferences (RTK, preferred CLI tools)
- Cross-project coding conventions (commit message format, PR style)
- Security constraints that apply everywhere
- Tone and output format defaults

**What does not belong here**:
- Project-specific architecture decisions
- Stack-specific rules (React hooks, Prisma patterns)
- Deployment or environment specifics
- Anything that changes per project

**Size target**: Keep global configuration under 200 lines. This is your always-on overhead for every session in every project. Bloating it hurts all projects equally.

```markdown
# Example: Minimal effective global CLAUDE.md

## Communication
- Respond in the same language the user writes in
- Prefer direct answers over preamble
- No em dashes in written output

## Git
- Commit messages: imperative mood, <72 chars subject line
- Never commit without being asked

## Code Style
- Prefer explicit error handling over silent failure
- Add TODO comments only when referencing a tracked issue
```

### Project Configuration

**Location**: `./CLAUDE.md` (project root)

**What belongs here**:
- Technology stack and versions in use
- Architecture decisions and their rationale
- Team conventions specific to this codebase
- File organization patterns
- Testing requirements and coverage targets
- Security constraints specific to this project
- Path-scope imports for subsystem modules

**Structure pattern**:

```markdown
# Project: [Name]

## Stack
- Language: TypeScript 5.3
- Framework: Next.js 14 (App Router)
- Database: PostgreSQL 16 via Prisma
- Testing: Vitest + React Testing Library

## Architecture
- Server Components by default; use `"use client"` only when interactivity requires it
- API routes in /app/api; no business logic in route handlers
- Business logic in /lib/services; each service is a plain function module

## Conventions
- File naming: kebab-case for files, PascalCase for React components
- Error handling: wrap service calls in Result<T, E> pattern (see lib/result.ts)
- Never expose raw database IDs in API responses; use UUIDs

## Path-Scoped Modules
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@prisma/CLAUDE-db.md
```

**The Goldilocks problem: altitude**

Two failure modes appear consistently in production CLAUDE.md files:

**Too vague**: "Write clean code," "Follow best practices," "Keep functions small." These instructions pass through the model without changing behavior. The model already has a concept of "clean code" that predates your instruction, and it defaults to that concept, which may not match what your project needs. Aspirational rules are ignored.

**Too granular**: "Use 2-space indentation," "Add a blank line after import blocks," "Prefix private methods with underscore." These are linter rules, not cognitive decisions. They belong in `.eslintrc`, `.editorconfig`, or `prettier.config.js`, enforced deterministically by tools, not probabilistically by an LLM. Putting them in CLAUDE.md wastes context budget and produces unreliable enforcement.

**The productive altitude**: Capture decisions the model would make differently without the instruction. The test is: "Would Claude, with no project context, reasonably do something different here?" If yes, the rule belongs in CLAUDE.md. If the answer is aspirational, cut it. If a linter enforces it, cut it.

| Altitude | Example | Verdict |
|----------|---------|---------|
| Too vague | "Write clean code" | Cut — model ignores, no behavior change |
| Too vague | "Follow best practices for security" | Cut — replace with specific constraints |
| Productive | "Never expose raw database IDs in API responses; use UUIDs" | Keep — specific, model would default otherwise |
| Productive | "Use the Result<T, E> pattern for service functions, not try/catch" | Keep — specific, overrides a common default |
| Too granular | "Use 2-space indentation" | Cut — delegate to Prettier |
| Too granular | "Add JSDoc comments to every function" | Cut — delegate to a lint rule |

The architecture choices, quality standards, and explicit "what not to do and why" rules are the productive altitude. The aspirational and the mechanical are noise.

### Session Configuration

**Mechanism**: Inline instructions, `/add-dir`, or system prompt flags for the current session.

**What belongs here**:
- One-off task constraints ("For this refactor, do not change the public API surface")
- Experiment parameters ("Use the new error format I'm testing in this file")
- Debug constraints ("Log every tool call for this session")
- Temporary overrides of project conventions

Session instructions are not persisted. They evaporate when the session ends. Any instruction that you find yourself repeating across sessions belongs in the project config, not the session layer.

### Decision Tree: Where Does This Rule Go?

```
Is this rule relevant to every project I work on?
├── Yes → Global CLAUDE.md
└── No ↓

Is this rule relevant to specific files or subsystems?
├── Yes → Path-scoped module (e.g., src/api/CLAUDE-api.md)
└── No ↓

Is this rule relevant to the whole project?
├── Yes → Project CLAUDE.md (root)
└── No ↓

Does this rule apply only to the current task or session?
├── Yes → Inline session instruction
└── No → Revisit: is it really a rule, or just a one-time preference?
```

### Import Chain and Override Semantics

The import chain flows: `global → project root → path-scoped modules → session`.

When conflicts exist:
- More specific overrides less specific (path-scoped beats root, root beats global)
- Later-declared beats earlier-declared at the same level
- Session instructions override all persistent config

**Practical example**: Your global config says "use two-space indentation." Your project config says "use four-space indentation for Python." Your session says "match the existing file style." The session instruction wins for this session, with four-space default for Python files, two-space for everything else.

Document your overrides explicitly. An undocumented override that contradicts a parent rule creates confusion during audits.

---

## 4. Modular Architecture

### The Problem with Monolithic Config

A 600-line CLAUDE.md with no structure is the most common failure mode in production contexts. Symptoms:

1. Rules from different domains mix together — a React component convention sits next to a database migration rule
2. Claude reads all 600 lines but the attention budget means rules on page 5 get less weight than rules on page 1
3. New team members can't find relevant rules quickly
4. Updates require scanning the entire file to find related rules before editing
5. Adherence degrades progressively as the file grows

The fix is architectural: decompose the monolith into focused modules, then use path-scoping to load each module only when relevant.

**A CLAUDE.md file that keeps growing hurts the model's performance directly, not just the token bill.** The common reflex when Claude gets something wrong is to add one more rule to the system prompt, on the assumption that more context can only help. Two independent talks from the same 2026 meetup reached the opposite conclusion: past a certain size, splitting rules into separate modular files outperforms piling them into one growing document, because the file itself becomes the bottleneck the model has to work around. (*Florian Allainmat, Dev With AI Meetup, 2026. Gallet and Dahan, same corpus and year, report the same independent finding.*)

### Path-Scoping Pattern

**Mechanism**: Claude Code supports `@path/to/file.md` imports in CLAUDE.md. When a path-scoped import is active, rules from that module are added to context only when files under the specified path are in scope.

**File structure**:

```
project/
├── CLAUDE.md                       # Root config, shared rules + @imports
├── src/
│   ├── api/
│   │   └── CLAUDE-api.md           # API-specific rules
│   ├── components/
│   │   └── CLAUDE-components.md    # React/UI-specific rules
│   └── lib/
│       └── CLAUDE-lib.md           # Utility/shared library rules
├── prisma/
│   └── CLAUDE-db.md                # Database and migration rules
└── tests/
    └── CLAUDE-tests.md             # Testing conventions
```

**Root CLAUDE.md with imports**:

```markdown
# Project Config

## Shared Rules
[...shared rules here...]

## Subsystem Modules
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@src/lib/CLAUDE-lib.md
@prisma/CLAUDE-db.md
@tests/CLAUDE-tests.md
```

**Example path-scoped module** (`src/api/CLAUDE-api.md`):

```markdown
# API Rules

- Route handlers in /app/api only; no business logic inline
- All endpoints must validate input with Zod before processing
- Error responses use the standard format: { error: string, code: string }
- Never log request bodies that may contain PII; log IDs only
- Rate limiting headers must be present on all public endpoints
- Authentication: verify JWT in middleware, not in individual handlers
```

This module's 6 rules are in context only when working in `src/api/`. They do not consume context budget when working in `src/components/`.

### Skills vs. Rules

This distinction is underused and matters:

| Dimension | Rules | Skills |
|-----------|-------|--------|
| Nature | Constraints, standards, conventions | Capabilities, procedures, workflows |
| When active | Always enforced | Invoked on demand |
| Example | "Never use `any` in TypeScript" | "How to add a new API endpoint" |
| Location | CLAUDE.md | `.claude/skills/` |
| Token cost | Always-on | Loaded only when invoked |

**Rules** define what Claude should and should not do by default. They set the boundaries of acceptable output.

**Skills** define how to do complex multi-step tasks that require specific knowledge of your project's patterns. They are loaded when Claude needs to perform a specific type of task, not always.

**Practical example**: A rule says "API endpoints must have Zod validation." A skill says "Here is the step-by-step pattern for creating a new API endpoint in this project, including the Zod schema pattern, the error handling wrapper, the auth middleware hook, and the test file structure."

Putting the endpoint creation procedure in a rule would mean loading 40 lines of procedural instructions for every session, even when you're not creating endpoints. Putting it in a skill means loading those 40 lines only when creating an endpoint.

**Rule**: `Never expose raw database IDs in API responses.`
**Skill**: `How to generate and use UUID-based public identifiers for entities.`

**Community skill libraries**

Pre-built skill collections reduce the upfront investment in modular context engineering:

- `anthropics/claude-code-skills` (official): Anthropic-maintained skill templates covering common development workflows
- `ibelick/ui-skills`: UI component and design system skills for frontend projects

These can be cloned, inspected, and adapted to your project conventions rather than built from scratch. Treat them as starting points — fork and modify to match your stack and naming conventions rather than using them verbatim.

### Progressive Disclosure

The principle: don't load everything upfront. Load what is needed for the task at hand.

**Core config (always-on)**:
- Architecture decisions and their rationale
- Coding standards and naming conventions
- Security constraints
- Tool preferences

**Contextual modules (loaded per task)**:
- Deployment procedures (load when deploying)
- API patterns (load when working in API layer)
- Test templates (load when writing tests)
- Database migration procedures (load when touching schema)

**Implementation pattern using skills**:

```
.claude/
├── skills/
│   ├── deploy-production.md      # Loaded when: "deploy this"
│   ├── add-api-endpoint.md       # Loaded when: "add endpoint for X"
│   ├── write-migration.md        # Loaded when: "add DB column"
│   └── create-component.md      # Loaded when: "create component for X"
```

Each skill file contains the step-by-step procedure with project-specific patterns. Claude loads it when the task type is detected, not proactively.

**MCP tool count and context budget**

MCP servers inject tool definitions into the system prompt. Each server adds its tool schemas, which consume context budget before any user content appears. Anthropic's engineering guidance recommends:

- Fewer than 10 MCP servers active per project
- Fewer than 80 total tools across all active servers

Beyond these thresholds, tool definition overhead measurably reduces the tokens available for actual task content. At 80+ tools, you are burning 15-20K tokens on tool schemas alone — budget that would otherwise go to code context, conversation history, and file contents.

The progressive disclosure principle applies to MCP servers as much as to rules. Load MCP servers contextually rather than activating all available servers for every project:

```json
{
  "mcpServers": {
    "database": { },
    "github": { }
  }
}
```

Resist the pattern of adding every available MCP server to a project's settings "just in case." Each inactive-but-loaded server is pure overhead. If a server is used in fewer than 20% of sessions in a project, it should not be in the default project config.

### Anti-Pattern: The Monolithic CLAUDE.md

**What it looks like**:

```markdown
# CLAUDE.md (600 lines)

## Rules
1. Use TypeScript
2. No any types
3. Run tests before committing
4. API endpoints need auth
5. Use Prisma for DB queries
6. React components in PascalCase
7. Deploy with ./scripts/deploy.sh
8. Check OWASP Top 10 before shipping
[...492 more rules...]
```

**Why it fails**:

- Rules 1-20 get ~95% attention weight; rules 500+ get ~30%
- Frontend dev reads backend DB rules they don't need and vice versa
- No logical grouping means finding relevant rules requires reading everything
- Adding a new rule requires checking the entire file for conflicts
- Adherence degrades continuously as the file grows

**The fix**:

1. Extract rules by domain into path-scoped modules
2. Keep the root CLAUDE.md to shared rules + import declarations
3. Move procedural knowledge to skills
4. Target root CLAUDE.md at under 150 lines after extraction

### Structural Metadata Files

Rules and structure are two different types of context. Conflating them produces files that are too large to load always-on but too important to skip.

**Rules context** answers: *how should I work in this project?* It lives in CLAUDE.md and path-scoped modules. It is relatively stable and almost always relevant.

**Structural context** answers: *what is the shape of this project?* How many API routes exist, which domains have components, where do the nested CLAUDE.md files live, how many Prisma models are there. This information is only needed for implementation tasks — creating a new file, adding a route, navigating an unfamiliar domain — and is irrelevant for debugging, documentation, or code review sessions.

Loading structural context always wastes tokens. Not having it at all means Claude browses the filesystem manually at the start of every implementation task, consuming turns and generating noise.

The pattern: a small, auto-generated YAML file (~1K tokens) that captures the structural shape of the codebase, registered in CLAUDE.md as a pointer rather than auto-imported.

**What to include** — five sections, nothing more:

| Section | Contents | Example |
|---------|----------|---------|
| `layers` | Architecture tiers with root paths and file counts | `routers: { root: "src/api", count: 33 }` |
| `component_domains` | Feature domains with paths and component counts | `{ name: "chat", count: 66 }` |
| `nested_contexts` | All CLAUDE.md / AI_INSTRUCTIONS.md under src/, with line count and focus | `{ path: "src/server/CLAUDE.md", lines: 45 }` |
| `stats` | Aggregate numbers: total files, test counts, schema model count | `total_ts_files: 543` |
| `key_paths` | Canonical paths Claude frequently gets wrong | `prisma_schema: "src/server/db/prisma/schema.prisma"` |

Keep the file below 1K tokens. Beyond that, you are adding detail that belongs in the actual source files.

**The pointer registration pattern**

Do not auto-load this file with `@machine-readable/code-map.yaml` in CLAUDE.md. Instead, register it in a reference table that tells Claude what the file contains and when to reach for it:

```markdown
## Context Indexes (load on demand)

| File | Contents | When to load |
|------|----------|--------------|
| machine-readable/code-map.yaml | Architecture layers (counts + roots), component domains, nested context files, project stats | Before any implementation task: new file, new route, new component |
| machine-readable/ai-config.yaml | Full AI tooling config: rules, skills, commands, agents, hooks | When auditing or modifying AI configuration |
| PROJECT_INDEX.md | Detailed architecture narrative, ADRs, domain glossary | Deep architectural work only |
```

This pattern scales: Claude reads the table at session start, knows what reference files exist and why, and loads them only when the current task warrants it. A debugging session never touches the code map. An implementation task loads it in one tool call.

**What "auto-generated" means in practice**

The generation script should do only three things: call `readdirSync` on each layer root to count files, walk the src tree to total `.ts`/`.tsx` files, and glob for nested CLAUDE.md files to populate `nested_contexts`. No AST parsing, no database queries, no network calls. The whole script runs in under a second. Add it to your `pnpm ai:sync` (or equivalent) task.

The key design constraint: **never add hand-curated content to this file.** The moment you do, you have a file that can drift. Auto-generated files cannot lie about the current state of the codebase; files with manual content can and will.

**Production example** (Méthode Aristote EdTech platform, ~1,300 source files):

```yaml
version: "1.0.0"
architecture: "Client → tRPC → Router → Service → Repository → Prisma"

layers:
  routers:
    root: "src/server/api/routers"
    description: "Tier 1 — Zod validation, delegate to service"
    count: 33
  services:
    root: "src/server/api/services"
    description: "Tier 2 — business logic, enforcePermission()"
    count: 61
  repositories:
    root: "src/server/api/repositories"
    description: "Tier 3 — CRUD Prisma only"
    count: 38

stats:
  total_ts_files: 543
  total_tsx_files: 798
  prisma_models: 48
  unit_tests: 268
```

With this file registered as a pointer, Claude answers "how many tRPC routers exist?" in a single lookup rather than walking `src/server/api/routers/` manually. For the implementation task "add a payment router", it immediately knows the correct root, the count, and the architectural constraint — before reading a single source file.

A ready-to-use template is available at [`examples/context-engineering/code-map-template.yaml`](../../examples/context-engineering/code-map-template.yaml).

---

## 5. Team Assembly

### The N × M × P Problem

At team scale, context engineering faces a combinatorial challenge:

- **N developers**: different roles, tools, communication preferences
- **M projects**: different stacks, conventions, deployment targets
- **P configurations**: each developer × each project needs a configuration

Maintaining N × M individual CLAUDE.md files manually is not sustainable. When a shared convention changes, you update N × M files. When a new project is created, you build from scratch. When a developer changes roles, you rebuild their configurations.

The solution is **profile-based assembly**: a single shared base of modules, with individual profiles that specify which modules to include and what personal preferences to overlay.

N × M × P becomes N profiles × 1 shared module base — manageable.

### Profile YAML Structure

Each team member has a profile YAML that declaratively specifies their configuration:

```yaml
# profiles/alice.yaml

profile:
  name: "Alice"
  role: "frontend"
  tools:
    - typescript
    - react
    - tailwind
  conventions:
    - atomic-design
    - accessibility-first
  communication:
    language: "en"
    verbosity: "concise"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md
    - frontend/testing-rtl.md
    - frontend/accessibility-checklist.md
  exclude:
    - backend/database-rules.md
    - backend/api-design.md
    - devops/deployment-procedures.md

overrides:
  - "Prefer named exports over default exports"
  - "Use Radix UI primitives before writing custom components"
```

```yaml
# profiles/bob.yaml

profile:
  name: "Bob"
  role: "backend"
  tools:
    - typescript
    - nodejs
    - postgresql
    - prisma
  communication:
    language: "en"
    verbosity: "detailed"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - backend/api-design.md
    - backend/database-rules.md
    - backend/error-handling.md
    - backend/performance-patterns.md
  exclude:
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md

overrides:
  - "Use structured logging (pino) with request context IDs"
  - "Always measure before optimizing; profile first"
```

### Module Library Structure

The shared module library lives in the repository and is version-controlled:

```
.claude/
├── modules/
│   ├── shared/
│   │   ├── core-rules.md           # Universal team standards
│   │   ├── git-conventions.md      # Commit and PR conventions
│   │   ├── security-baseline.md    # Non-negotiable security rules
│   │   └── testing-standards.md   # Coverage and test quality rules
│   ├── frontend/
│   │   ├── react-patterns.md
│   │   ├── tailwind-conventions.md
│   │   ├── testing-rtl.md
│   │   └── accessibility-checklist.md
│   ├── backend/
│   │   ├── api-design.md
│   │   ├── database-rules.md
│   │   ├── error-handling.md
│   │   └── performance-patterns.md
│   └── devops/
│       ├── deployment-procedures.md
│       ├── monitoring-conventions.md
│       └── infrastructure-rules.md
├── profiles/
│   ├── alice.yaml
│   ├── bob.yaml
│   └── carol.yaml
└── scripts/
    └── assemble-context.sh
```

### Assembly Script

The assembly script reads a profile and concatenates the specified modules into a CLAUDE.md:

```bash
#!/usr/bin/env bash
# scripts/assemble-context.sh

set -euo pipefail

PROFILE="${1:-}"
CHECK_MODE="${2:-}"

if [[ -z "$PROFILE" ]]; then
  echo "Usage: ./assemble-context.sh <profile-name> [--check]"
  exit 1
fi

PROFILE_FILE=".claude/profiles/${PROFILE}.yaml"
OUTPUT_FILE="CLAUDE.md"
MODULES_DIR=".claude/modules"

if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "Profile not found: $PROFILE_FILE"
  exit 1
fi

# Parse profile with yq or python
MODULES=$(python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
for m in profile['modules']['include']:
    print(m)
")

# Assemble output
ASSEMBLED=$(mktemp)

echo "# Claude Code Configuration" > "$ASSEMBLED"
echo "# Generated from profile: $PROFILE" >> "$ASSEMBLED"
echo "# Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$ASSEMBLED"
echo "" >> "$ASSEMBLED"

while IFS= read -r module; do
  MODULE_PATH="${MODULES_DIR}/${module}"
  if [[ -f "$MODULE_PATH" ]]; then
    echo "## From: ${module}" >> "$ASSEMBLED"
    cat "$MODULE_PATH" >> "$ASSEMBLED"
    echo "" >> "$ASSEMBLED"
  else
    echo "WARNING: module not found: $MODULE_PATH" >&2
  fi
done <<< "$MODULES"

# Append personal overrides
python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
overrides = profile.get('overrides', [])
if overrides:
    print('## Personal Overrides')
    for o in overrides:
        print(f'- {o}')
" >> "$ASSEMBLED"

if [[ "$CHECK_MODE" == "--check" ]]; then
  if diff -q "$OUTPUT_FILE" "$ASSEMBLED" > /dev/null 2>&1; then
    echo "OK: CLAUDE.md matches profile $PROFILE"
    rm "$ASSEMBLED"
    exit 0
  else
    echo "DRIFT: CLAUDE.md does not match profile $PROFILE"
    diff "$OUTPUT_FILE" "$ASSEMBLED"
    rm "$ASSEMBLED"
    exit 1
  fi
fi

mv "$ASSEMBLED" "$OUTPUT_FILE"
echo "Assembled CLAUDE.md from profile: $PROFILE"
```

**Usage**:

```bash
# Generate CLAUDE.md from a profile
./scripts/assemble-context.sh alice

# Check for drift (used in CI)
./scripts/assemble-context.sh alice --check
```

### CI Drift Detection

Team members regenerate their CLAUDE.md from profiles, but base modules evolve over time. Without drift detection, a developer may be running an outdated configuration — one that predates a security rule addition or a convention update.

A GitHub Actions job detects this:

```yaml
# .github/workflows/context-drift.yml

name: Context Drift Detection

on:
  schedule:
    - cron: '0 9 * * 1'   # Weekly, Monday 9am UTC
  push:
    paths:
      - '.claude/modules/**'

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install pyyaml

      - name: Check all profiles for drift
        run: |
          DRIFT=0
          for profile_file in .claude/profiles/*.yaml; do
            profile=$(basename "$profile_file" .yaml)
            echo "Checking profile: $profile"
            if ! ./scripts/assemble-context.sh "$profile" --check; then
              echo "DRIFT detected in profile: $profile"
              DRIFT=1
            fi
          done
          exit $DRIFT

      - name: Notify on drift
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Context drift detected — CLAUDE.md needs regeneration',
              body: 'One or more team profiles are out of sync with the current module library. Run `./scripts/assemble-context.sh <profile>` to regenerate.',
              labels: ['context-engineering']
            })
```

### Onboarding with Profiles

For new team members, the onboarding sequence becomes:

```bash
# 1. Copy a starter profile appropriate for your role
cp .claude/profiles/template-frontend.yaml .claude/profiles/yourname.yaml

# 2. Edit the profile for your preferences
vim .claude/profiles/yourname.yaml

# 3. Generate your CLAUDE.md
./scripts/assemble-context.sh yourname

# 4. Verify the output
cat CLAUDE.md

# 5. Commit your profile (not the generated CLAUDE.md — it's gitignored)
git add .claude/profiles/yourname.yaml
git commit -m "chore: add context profile for yourname"
```

Add `CLAUDE.md` to `.gitignore` at the project root. The profile YAML is the source of truth, not the generated file.

---

## 6. Context Lifecycle

### Instruction Debt

Rules accumulate. They are rarely removed. This is instruction debt: the gradual accumulation of rules that are outdated, redundant, or contradictory — each still consuming context budget.

Signs of instruction debt:

- A rule refers to a library you stopped using six months ago
- Two rules say opposite things about the same pattern
- A rule covers an edge case that only applied during a specific migration
- The same constraint is stated three times in different sections
- Developers comment out or ignore specific rules because they conflict with current practice

Instruction debt has compounding costs: each conflicting or irrelevant rule displaces a useful one, and models behave unpredictably when rules conflict.

**Quarterly audit rhythm**: Schedule a context audit every quarter (or after major project milestones). The audit prompt:

```
Review every rule in CLAUDE.md for:
1. Relevance: Does this still apply to the current stack and patterns?
2. Specificity: Is this actionable, or is it too vague to enforce?
3. Conflicts: Does this contradict another rule?
4. Coverage: Is this already covered by a more general rule?

For each rule, classify as: KEEP | UPDATE | ARCHIVE | DELETE
```

Run this as an actual Claude session, feeding the current CLAUDE.md and asking for a structured audit.

### The Update Loop

The most common mistake after a bad Claude output is to fix the output manually and move on. This is a wasted learning opportunity.

**Bad loop**:
```
Claude generates wrong pattern
→ Developer manually fixes it
→ Next session: Claude generates wrong pattern again
→ Developer manually fixes it again
→ Repeat indefinitely
```

**Good loop**:
```
Claude generates wrong pattern
→ Developer identifies the root cause (missing rule? vague rule? conflicting rules?)
→ Developer updates CLAUDE.md with a corrected or new rule
→ Next session: Claude generates correct pattern
→ Rule stays in config permanently
```

The update loop is how your configuration system learns from experience. Each bad output is a signal that something is missing or broken in your context engineering. Treat it as a bug report against CLAUDE.md, not just a one-off failure.

**Practical format for rule updates**:

When adding a rule from a failure, include the rationale inline:

```markdown
- Use the `Result<T, E>` type for service functions, not try/catch
  (Rationale: try/catch at service level hides error types from callers;
   Result forces explicit error handling at the call site)
```

The rationale serves two purposes: it helps future auditors understand why the rule exists, and it gives Claude better context for applying the rule correctly.

### Knowledge Feeding After Sprints

At the end of each sprint or release cycle, run a brief knowledge feeding session:

1. **New patterns**: "We standardized on X approach for Y type of problem in this sprint. Add this to CLAUDE.md."
2. **Anti-patterns discovered**: "We tried X and it caused Y. Add a rule to avoid it."
3. **Architecture decisions**: "We decided to use X over Y because Z. Document this so Claude doesn't suggest Y."
4. **Deprecated patterns**: "We're moving away from X. Add a rule to use Y instead and flag existing X usages."

This keeps the context system current without requiring large periodic overhauls.

### The ACE Pipeline

For teams that run Claude Code in automated or semi-automated workflows, the ACE pipeline provides a structured execution model. This is a config-persistence loop operating across sessions. It is distinct from arXiv:2510.04618 (Stanford/SambaNova, Oct 2025), which uses the same acronym for an inference-time context evolution technique. For the operational improvements that build on this pipeline, see Section 10 (Signal Taxonomy) and Section 11 (Loop Closure).

```
Assemble → Check → Execute
```

**Assemble**: Build context from the team profile + project modules. Produces a CLAUDE.md specific to the developer and task context.

**Check**: Run canary validation — a set of 3-5 test prompts that verify key behaviors before the actual task. If canary checks fail, fix the context issue before proceeding.

**Execute**: Run Claude with the validated context on the actual task.

```bash
#!/usr/bin/env bash
# ace.sh — Assemble, Check, Execute

PROFILE="${1:-}"
TASK="${2:-}"

if [[ -z "$PROFILE" || -z "$TASK" ]]; then
  echo "Usage: ./ace.sh <profile> <task-description>"
  exit 1
fi

echo "=== ASSEMBLE ==="
./scripts/assemble-context.sh "$PROFILE"

echo "=== CHECK ==="
./scripts/run-canaries.sh
CANARY_EXIT=$?

if [[ $CANARY_EXIT -ne 0 ]]; then
  echo "Canary checks failed. Fix context issues before executing."
  exit 1
fi

echo "=== EXECUTE ==="
claude "$TASK"
```

### Session Retrospective

At the end of each Claude Code session, before closing, ask:

```
Looking at what we built or changed in this session:
1. What patterns did we use that aren't in CLAUDE.md?
2. What did I have to correct that could become a rule?
3. What decisions did we make that should be documented?

Generate 3-5 candidate rules for CLAUDE.md based on this session.
```

This takes 2-3 minutes and generates concrete improvement candidates. You review them and decide which to add. Over time, this is how configuration systems accumulate genuine project knowledge rather than just generic rules.

### Context Chaining

Context chaining is a pattern where the output of one context window becomes the structured input of the next. Each session builds on the previous one, passing a curated summary forward rather than discarding state.

This is distinct from the Session-per-Concern pipeline (in the Fresh Context Pattern section), which separates concerns into isolated sessions. Context chaining allows perspectives to accumulate: each session's insights enrich the next session's starting context.

**Pattern structure**:

```
Session 1:
  Input: Task definition + CLAUDE.md
  Work: Research, exploration, initial implementation
  Output: summary.md (decisions, open questions, validated patterns)

Session 2:
  Input: Task definition + CLAUDE.md + summary.md from Session 1
  Work: Implementation building on Session 1 findings
  Output: updated summary.md + code artifacts

Session 3:
  Input: Task definition + CLAUDE.md + updated summary.md
  Work: Review, refinement, integration
  Output: final artifacts + lessons.md for CLAUDE.md update
```

The key discipline: the summary passed forward must be curated, not a raw transcript. Raw transcripts reintroduce context rot. A curated summary is 200-500 tokens of distilled findings: decisions made, approaches validated, dead ends marked.

**When to use**:
- Multi-day tasks where rebuilding context from scratch each session would be expensive
- Research tasks where early sessions produce findings that constrain later sessions
- Iterative design tasks where accumulated understanding matters across sessions

**When not to use**:
- Tasks with clean atomic boundaries (one session, one deliverable, fresh start next)
- Situations where early session assumptions turned out wrong and you want a clean break

Context chaining extends context intentionally. It is the opposite of the Ralph Loop, which discards state. Use chaining when accumulated understanding is an asset; use the Ralph Loop when accumulated state is a liability.

---

## 7. Quality Measurement

### Self-Evaluation Questions

Run these questions against your CLAUDE.md periodically (quarterly at minimum):

**Relevance**:
- Does this rule still apply to the current stack, libraries, and team practices?
- Was this rule written for a problem that no longer exists?
- Would a new team member understand why this rule exists?

**Specificity**:
- Is this rule specific enough for Claude to know when it applies?
- Does this rule have at least one concrete example or counter-example?
- Could two developers interpret this rule differently?

**Conflicts**:
- Does this rule contradict another rule in the same file?
- Does this rule contradict a rule in a path-scoped module?
- Does this rule contradict a global rule without explicitly overriding it?

**Coverage**:
- Is this rule a specific case of a more general rule that already exists?
- Is this rule already implied by the architecture decisions stated elsewhere?

A rule that fails more than one of these checks is a candidate for update or removal.

### Canary Checks

Canary checks are simple test prompts that verify Claude follows key conventions. Run them before and after major changes to CLAUDE.md to catch regressions.

**Structure**: 3-5 prompts that are simple enough to answer quickly, but specific enough to reveal adherence failures.

**Example canary set for a React/TypeScript project**:

```bash
# scripts/run-canaries.sh

PASS=0
FAIL=0

check() {
  local name="$1"
  local prompt="$2"
  local expected_pattern="$3"

  result=$(claude "$prompt" --output-format text 2>/dev/null)

  if echo "$result" | grep -qE "$expected_pattern"; then
    echo "PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $name"
    echo "  Expected pattern: $expected_pattern"
    echo "  Got: $(echo "$result" | head -5)"
    FAIL=$((FAIL + 1))
  fi
}

check "TypeScript interfaces" \
  "Generate a React component that accepts a name and age prop" \
  "interface.*Props"

check "Named exports" \
  "Create a utility function that formats a date" \
  "^export (function|const)"

check "No any type" \
  "Write a function that processes user data" \
  "^((?!: any).)*$"

check "Error result type" \
  "Write a service function that fetches user data from an API" \
  "Result<"

echo ""
echo "Canaries: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
```

**When to run canaries**:
- Before merging changes to CLAUDE.md
- After adding a new path-scoped module
- When a team member reports unexpected Claude behavior
- As part of the CI drift detection job

### Adherence Tracking

Informal but effective: for each key rule in CLAUDE.md, track how often Claude violates it across 10 consecutive interactions where the rule should apply.

| Rule | Violations / 10 | Status |
|------|----------------|--------|
| TypeScript interfaces for props | 1/10 | Healthy |
| Result type for service functions | 0/10 | Healthy |
| No raw database IDs in API responses | 3/10 | Review rule |
| Structured logging with request context | 5/10 | Rule too vague |
| OWASP Top 10 check before shipping | 8/10 | Not actionable as stated |

Rules with >20% violation rate are broken in one of three ways:
1. Too vague to apply consistently
2. Conflicting with another rule
3. Placed too late in the file to receive enough attention

**Fix for "too vague"**: Add a concrete example of compliance and a counter-example of violation.

**Fix for "conflicting"**: Find the conflict, decide which rule should win, update or remove the losing rule, and add an explicit note.

**Fix for "placed too late"**: Move the rule to the top third of the file, or to a more prominent position in its section.

### Context Debt Score

A single metric for the health of your context engineering system:

```
Context Debt Score = (total_rules / 150) × (conflicts_found / total_rules) × 100
```

Where:
- `total_rules` = count of distinct rules across all loaded config files
- `150` = the approximate attention ceiling
- `conflicts_found` = rules that contradict another rule

| Score Range | Status | Action |
|-------------|--------|--------|
| < 30 | Healthy | Standard quarterly audit |
| 30 – 60 | Degraded | Prune and deduplicate; fix conflicts |
| 60 – 80 | Poor | Major restructure needed |
| > 80 | Critical | Start from scratch with top 30 rules |

**Running the score calculation**:

```bash
# Count rules (approximate: lines starting with -)
TOTAL_RULES=$(grep -c "^- " CLAUDE.md 2>/dev/null || echo 0)

# Count conflicts requires manual review or an LLM audit pass
# Use: claude "Scan CLAUDE.md and count rules that contradict each other. Return the count."

echo "Total rules: $TOTAL_RULES"
echo "Run conflict audit manually or with Claude"
```

### Context Drift Detection

The existing adherence metrics (canary checks, violation rates) require human interpretation: you know a rule is being violated when you notice it. Systematic drift detection is a complementary layer that detects behavioral shifts automatically, before they surface as bad outputs.

These methods come from ML observability. They are more relevant for teams running Claude in automated pipelines than for interactive use, but the concepts apply in both contexts.

**Cosine distance method**

The simplest production-ready approach. Embed model outputs (responses to fixed probe prompts) and measure cosine distance from a known-good baseline embedding.

1. Define 5-10 fixed probe prompts that test key conventions (equivalent to canary prompts).
2. At a stable point ("golden baseline"), capture outputs and compute their embeddings.
3. On each subsequent run, compute outputs for the same prompts and measure cosine distance from baseline.
4. Alert when average distance exceeds a threshold (typically 0.15-0.20 for sentence-level embeddings).

What this catches: gradual style drift, convention erosion, changes in output structure — all before violation rates increase.

**Share of drifted features**

More granular than cosine distance. Instead of a single distance metric, track which specific embedding dimensions have shifted beyond a threshold. This tells you which aspects of the output have changed (length, formality, code style) rather than just that something changed.

Practical implementation requires an embedding model and a monitoring store. Start with cosine distance; add feature-level tracking only if you need to diagnose what is drifting.

**Maximum Mean Discrepancy (MMD)**

A kernel-based method for comparing two distributions of outputs. MMD answers: "Are the outputs from this period statistically different from the baseline period?" It handles high-dimensional embeddings robustly and does not require specifying which features to track.

MMD is more setup cost than cosine distance but produces fewer false positives when output variance is naturally high. Relevant for teams with significant output volume (hundreds of Claude runs per day).

**Statistical distance thresholds**

Regardless of method, thresholds matter:

| Distance metric | Alert threshold | Note |
|----------------|-----------------|------|
| Cosine distance | > 0.15 | Works for most sentence embeddings |
| Euclidean distance | Varies by dimensionality | Normalize embeddings first |
| Manhattan distance | Varies by dimensionality | More robust to outliers than Euclidean |

These are starting points. Calibrate against your baseline variance: if your outputs naturally vary widely (creative tasks), use a looser threshold.

**When to use drift detection**

- Automated pipelines where human review is not per-output
- After CLAUDE.md changes, to verify behavior stayed stable
- When upgrading Claude model versions (behavior shifts between versions)
- Regression detection after any context configuration change

For interactive development with regular human review, canary checks and violation rate tracking (already above) are sufficient.

### Useful Metrics to Track Over Time

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Always-on context size | `wc -w CLAUDE.md ~/.claude/CLAUDE.md` | < 5,000 words |
| Rule count | `grep -c "^- " CLAUDE.md` | < 150 |
| File age | `git log --follow -p CLAUDE.md | head -20` | Major review every 6 months |
| Violation rate per key rule | Manual spot checks | < 20% violation |
| Canary pass rate | `./scripts/run-canaries.sh` | 100% (all pass) |

---

## 8. Context Reduction Techniques

### Path-Scoping: The Highest-Leverage Technique

Path-scoping reduces always-on context by 40-50% with no loss of coverage. It is the single most impactful structural change for projects beyond ~200 lines of configuration.

Implementation steps:

1. Identify natural domain boundaries in your codebase (API, frontend, database, tests, infrastructure)
2. For each domain, create a `CLAUDE-{domain}.md` file in the domain directory
3. Move domain-specific rules from root CLAUDE.md to the appropriate module
4. Replace moved content in root CLAUDE.md with `@path/to/CLAUDE-domain.md` imports
5. Verify adherence with canary checks

Target after refactor: root CLAUDE.md at under 150 lines (shared rules + import declarations only).

### Negative Constraints

Empirically, negative constraints ("never do X") outperform positive instructions ("do X") by 15-25% for preventing bad patterns. This is counterintuitive — you might expect "do X" to be clearer. But in practice, the model needs to actively resist a temptation to do the wrong thing; explicitly naming the wrong thing and saying "never" is more salient.

| Pattern | Formulation | Adherence |
|---------|-------------|-----------|
| Positive (weaker) | "Use structured logging for all backend services" | ~75% |
| Negative (stronger) | "Never use console.log in backend services; use the structured logger (pino)" | ~90% |

**Technique**: For any rule where the wrong pattern is a common default (raw try/catch, console.log, default exports, any types), frame the rule as a negative constraint naming the specific pattern to avoid.

### Rule Compression

Long explanatory rules consume tokens and dilute attention. Compress explanations to their essence:

**Before** (verbose, 38 words):
```markdown
- When creating React components, always make sure to use TypeScript interfaces
  for props, and define them before the component declaration, not inline, to
  improve readability and enable reuse.
```

**After** (compressed, 9 words):
```markdown
- React props: TypeScript interface, declared before component, never inline.
```

The compressed version has higher adherence — shorter rules are processed with more attention weight per rule. Save explanations for the rationale format when they're truly needed for understanding.

**Compression heuristic**: If a rule takes more than one line, ask whether the extra content is a constraint or an explanation. Move explanations to comments (prefixed with `#` or a `>` blockquote) or rationale annotations. Keep the enforced constraint to one line.

### Deduplication

The same constraint stated multiple times (in different words) does not reinforce it — it dilutes the total attention budget. Find and remove semantic duplicates.

**Common sources of duplication**:
- One rule in a general section, one more specific version in a path-scoped module
- A rule added to fix a problem, without removing the vaguer original rule it supersedes
- Rules copied from different team members' configs during a merge

**Deduplication workflow**:

```
Scan CLAUDE.md for semantic duplicates. Two rules are duplicates if they
constrain the same behavior, even if worded differently. List all duplicate
pairs and recommend which version to keep based on specificity and clarity.
```

Run this as a Claude prompt against your CLAUDE.md. Review the suggestions and merge.

### The Archive Pattern

When removing a rule, you lose the knowledge of why it existed. That institutional memory can be valuable — six months later, someone may try to reintroduce the same pattern the rule was preventing.

Instead of deleting obsolete rules, archive them:

```
.claude/
├── CLAUDE.md              # Active rules
└── CLAUDE-archive.md      # Historical rules with retirement notes
```

**Archive entry format**:

```markdown
## Archived Rules

### [Retired 2026-01] Use MongoDB for session storage
Replaced by: Use PostgreSQL with the sessions table for session storage.
Reason: Standardized on single database; MongoDB was only used for sessions and added operational complexity.
```

The archive is not loaded by Claude — it is reference documentation for humans. It prevents the same debates and mistakes from recurring.

### The 80/20 Rule for Rules

Across most production configurations, 20% of rules account for 80% of Claude's consequential decisions. The other 80% of rules cover edge cases, stylistic preferences, and situations that rarely arise.

Identifying your top 20%:

1. List every rule in CLAUDE.md
2. For each rule, estimate: "How often does this rule meaningfully change Claude's output in a session?"
3. Rules that apply daily: keep, prioritize, place early
4. Rules that apply weekly: keep, place in middle
5. Rules that apply monthly: consider archiving or moving to a loaded-on-demand skill
6. Rules that apply rarely: archive

The goal is not to eliminate coverage — it's to ensure that the rules that matter most are not diluted by the rules that matter least.

**Placement matters**: Place your top 20% rules in the first third of CLAUDE.md. Attention weight is not uniform across a long document — early content has higher salience.

### Think in Code

Named by context-mode v1.0.64 and independently described by Contieri in April 2026 as "Ask for the Analyst, Not the Analysis," this pattern addresses a common source of token waste in exploration tasks.

**The problem**: To answer "which files import module X?", a naive agent opens and reads files one by one. With 30 candidate files, that's 30 tool calls and potentially 15,000+ tokens of file content loaded into context, the vast majority irrelevant to the actual question.

**The pattern**: Instead of reading files, instruct the agent to write and run a small script (bash, Python, jq) that queries, counts, or filters, then return only the result. The result is 1 tool call and approximately 50 tokens rather than 30 calls and 15,000 tokens.

**Examples**:

Finding which files import a module:
```bash
grep -r "import X" src/ --include="*.ts" | wc -l
```

Identifying files over a size threshold:
```bash
find src/ -name "*.ts" -size +50k | sort
```

Counting test coverage by directory:
```bash
find src/ -name "*.test.ts" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn
```

**When to apply it**: Any task that is "explore and report" rather than "edit." Discovery tasks, counting, pattern matching, dependency analysis, and finding files by content are all candidates. If you find yourself writing agent instructions that describe reading many files to gather statistics, the "Think in Code" pattern usually applies.

**Relationship to sub-agents**: Sub-agents execute in isolation with their own context budget. "Think in Code" keeps everything in the main agent but uses scripts as the exploration mechanism. Both approaches avoid loading irrelevant file content into context. For tasks that genuinely require reading file contents (edits, code review, understanding logic), sub-agents are the better fit. For pure discovery tasks that reduce to counts or lists, a single script call is faster and cheaper.

### Graduated Context Offloading

From LangGraph's Deep Agents SDK research into long-running agents, this three-tier cascade addresses context accumulation over time without losing access to the information.

**The problem**: A long-running agent that processes many files, API calls, and tool results accumulates context that grows until it hits window limits or degrades accuracy through context rot. Neither truncation (loses data) nor unlimited accumulation (loses accuracy) is correct.

**The three-tier cascade**:

**Tier 1 — Large tool outputs (threshold: 20K tokens)**: Offload to filesystem. Write the full output to a temp file and inject only the file path and a 10-line preview into context. The agent can request the full content if needed.

**Tier 2 — Accumulated tool call arguments (threshold: context approaching mid-point)**: Offload old tool invocations. Keep only the most recent N tool calls in full; summarize or drop arguments for older calls. Tool results are more valuable than tool call arguments for continuing the task.

**Tier 3 — Message history (threshold: context near limit)**: Lossy summarization of message history. Last resort only — this introduces the risks described in Section 11 (Progressive Summarization Risks). Apply only when Tiers 1 and 2 are exhausted.

**Claude Code equivalent using a PostToolUse hook**:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/offload-large-output.py"
      }]
    }]
  }
}
```

```python
# ~/.claude/hooks/offload-large-output.py
import json, sys, tempfile, os

data = json.load(sys.stdin)
output = data.get("tool_result", {}).get("content", "")

THRESHOLD = 20_000  # characters, roughly 5K tokens

if len(output) > THRESHOLD:
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False,
        prefix="/tmp/claude-output-"
    )
    tmp.write(output)
    tmp.close()
    preview = "\n".join(output.splitlines()[:10])
    print(json.dumps({
        "tool_result": {
            "content": (
                f"[Output too large — saved to {tmp.name}]\n"
                f"Preview (first 10 lines):\n{preview}\n"
                f"Use: cat {tmp.name}"
            )
        }
    }))
else:
    print(json.dumps(data))
```

This hook transparently intercepts large bash outputs, writes them to a temp file, and injects the path with a preview. The agent sees a compact summary and knows where to find the full content if it needs it. The same pattern applies to any tool type: MCP tool results, file reads, or API responses can all be offloaded to filesystem and referenced by path.

### Optical and Visual Context Compression

A distinct compression modality emerged in 2026, the first real modality shift in this discipline rather than an incremental improvement on text compression. Following DeepSeek-OCR's late-2025 demonstration that a model can decode more than 10x the token count from a small set of vision tokens, 2026 work (AgentOCR, Glyph, VIST) extends the idea to long documents: render the text as an image, pass it through a frozen vision encoder plus a trainable resampler, and hand the model compact visual tokens instead of raw text tokens. The 10x figure comes from the original DeepSeek-OCR paper under specific conditions; treat it as a compression ratio observed in that setup, not a universal multiplier.

pxpipe is the first production implementation of this pattern targeted specifically at Claude Code and the Anthropic API: a local proxy that rewrites large tool results, collapsed prior turns, and static system-prompt or tool-doc blocks into PNG images before the request leaves the machine, while leaving recent turns, model output, and sparse prose untouched. Exact-byte content (passwords, hashes, IDs) is explicitly excluded and documented as a lossy-recall risk rather than a solved problem. Full tool profile, benchmarks, and known limitations: [Context Engineering Tools: pxpipe](../ecosystem/context-engineering-tools.md#pxpipe).

**When it applies**: large, mostly-static blocks of text your model does not need to recall verbatim (system prompts, tool documentation, old conversation turns already summarized elsewhere). It does not apply to content where exact character-level recall matters, since visual token decoding has a measurable non-zero error rate on precise strings.

### Summary: Reduction Techniques by Impact

| Technique | Context Reduction | Effort | Adherence Impact |
|-----------|------------------|--------|-----------------|
| Path-scoping | 40-50% | Medium | +15-25% |
| Negative constraints | 0% (reformulation) | Low | +15-25% per rule |
| Rule compression | 20-30% | Low | +5-10% |
| Deduplication | 10-20% | Low | +5-15% |
| Archive pattern | 10-30% | Low | +5-10% |
| 80/20 prioritization | 0% (reordering) | Low | +10-20% |
| Think in Code | 90%+ on exploration tasks | Low | N/A (replaces calls) |
| Graduated offloading | Variable (tier-dependent) | Medium | Prevents rot |

The highest-leverage sequence for a project with context debt:

1. Path-scope (biggest structural win)
2. Deduplicate (removes noise)
3. Compress (sharpens remaining rules)
4. Archive (clears obsolete rules safely)
5. Reorder (prioritizes the rules that matter most)
6. Graduated offloading (for long-running or multi-step agent workflows)

---

## 9. Maturity Assessment

Context engineering capability develops in stages. Most teams reach Level 2 and stop — not because higher levels are complex, but because the failures at Level 2 are invisible. Output quality is acceptable, so the pressure to go further never appears. This assessment makes the gap visible.

### The Six Levels

| Level | Name | What exists | Failure mode |
|-------|------|-------------|--------------|
| **0** | No configuration | LLM with no CLAUDE.md | Generic outputs, zero project awareness |
| **1** | Flat config | Single CLAUDE.md, no structure | Rules pile up, adherence degrades after ~100 lines |
| **2** | Structured config | Sections, clear organization, global/project separation | Works solo, breaks at team scale |
| **3** | Modular config | Path-scoped modules, deliberate layering | Rules maintained but no verification |
| **4** | Measured config | Canary tests, adherence tracking, lifecycle management | System works but drifts silently over time |
| **5** | Engineered system | Profiles, CI drift detection, ACE pipeline, quarterly audit rhythm | — |

### Self-Assessment

Answer each question. Stop at the first "No" — that is your current level.

**Level 0 → 1**: Do you have a CLAUDE.md file in your project?

**Level 1 → 2**: Does your configuration distinguish between global conventions (in `~/.claude/CLAUDE.md`) and project-specific rules (in `./CLAUDE.md`)? Are sections clearly separated?

**Level 2 → 3**: Are subsystem-specific rules in path-scoped modules rather than the root CLAUDE.md? Does your root CLAUDE.md stay under 150 lines?

**Level 3 → 4**: Do you have canary checks that verify key conventions? Do you track violation rates for your most important rules? Do you run a context audit after major milestones?

**Level 4 → 5**: Do team members assemble their CLAUDE.md from profiles rather than editing it directly? Is there CI drift detection that alerts when configuration diverges from source modules? Do you run session retrospectives to feed new patterns back into configuration?

### What to Do at Each Level

| Your level | Next action |
|------------|-------------|
| 0 | Create a minimal CLAUDE.md with 5-10 rules. See §3 for what belongs there. |
| 1 | Split global and project config. Move cross-project preferences to `~/.claude/CLAUDE.md`. |
| 2 | Identify the 2-3 highest-traffic subsystems. Create path-scoped modules for them. |
| 3 | Write 3-5 canary prompts for your most violated rules. Automate them. |
| 4 | Introduce profiles for team members. Add CI drift detection. Start session retrospectives. |
| 5 | Maintain quarterly audits. The system is built — the work is ongoing calibration. |

Most teams move from Level 0 to Level 2 in a single afternoon. Moving from Level 3 to Level 4 requires a measurement habit, not more configuration. The bottleneck at the higher levels is not knowledge — it is the discipline to treat configuration as a living system rather than a one-time setup.

---

## 10. Signal Taxonomy and Causal Attribution

A flat friction score (errors × 3 + retries × 2) tells you how much friction happened but not which part of your configuration caused it. On a project running an ACE-v1 loop for ten weeks, this gap produced a misleading priority queue: Bash tool generated 3,377 retries vs 597 for Read vs 254 for Edit. Raw volume pointed at Bash as the problem, but the actual pattern was missing batching instructions, not a bad Bash rule. Without typed signals, a curator fixes the wrong layer.

> A note on naming: arXiv:2510.04618 (Stanford/SambaNova, Oct 2025) uses "ACE" for an inference-time context evolution technique. The ACE described here is a config-persistence loop operating across sessions, not within them. Different concept, same acronym. The v2 improvements below apply to this guide's definition.

### Signal Categories

Replace the flat score with a five-category taxonomy. Each event gets a category and an attribution candidate.

| Category | Definition | Example |
|---|---|---|
| **syntactic** | Tool error, parse failure, malformed call | `Invalid JSON in tool call` |
| **semantic** | Output rejected by user, retry with clarification | "No, I meant the other format" |
| **procedural** | Rule conflict, missing step, wrong execution phase | Write-before-Read violation |
| **alignment** | Tone violation, out-of-scope change, hallucinated claim | Claude adds unrequested refactoring |
| **performance** | Token overrun, context overflow, `/compact` forced mid-task | Session degrading at 85% context |

Weighting should reflect impact, not frequency. A single alignment violation in a production-critical flow costs more than 50 syntactic retries on a local script.

### Causal Attribution

For each friction event, capture the active context: which rule files were loaded, which skills were invoked, and which profile was active. This lets the Curator build a rule-to-friction correlation table without running LLM-as-judge over the full session history.

```yaml
# friction-event schema
id: evt_20260519_bash_batching_001
timestamp: "2026-05-19T14:32:00Z"
session_id: "2094ff6d"
category: procedural
tool: Bash
retry_count: 4
description: "Three sequential Bash calls where one batched call would have sufficed"
active_rules:
  - .claude/rules/lean-ctx.md
  - .claude/rules/bash-safety.md
active_skills: []
profile: default
suspected_cause: "lean-ctx.md missing explicit Bash batching instruction"
resolved: false
```

Store events as append-only YAML files or newline-delimited JSON. They are the raw material for the Curator; keep them local and gitignore them by default unless your team chooses a shared signal store (see Section 11).

### Per-Pattern Tracking

Beyond individual events, track friction by pattern over time. Replace a weekly total with a dict:

```yaml
friction_patterns:
  week: "2026-W20"
  write_before_read: 10
  gitignore_violation: 10
  exit_code_1_unchecked: 38
  bash_no_batching: 47
  permission_denied_hook: 12
```

The pattern time series is what lets you measure whether a merged rule had any effect. Without it, you are guessing.

---

## 11. Loop Closure: PR-Based Curation

The hidden failure mode at Level 5 is the open loop: the Curator generates suggestions but nothing gets merged. On the Aristote project over ten weeks of ACE-v1 operation, two curator reports separated by ten weeks proposed the same two rule candidates. Neither was merged. The loop was open, and the system produced reports instead of progress.

Closing the loop requires making the Curator's output easy to act on. The mechanism: the Curator generates a Git PR rather than a plain report.

### PR Anatomy

Each Curator PR contains four things:

1. **Config diff**: the exact rule or skill change proposed (a `git diff`-ready patch, not prose)
2. **Friction evidence**: the 3-5 friction events that drove the suggestion, with event IDs linking back to the signal files
3. **Canary results**: a before/after comparison on 10-20 probe prompts (see below)
4. **Escalation note**: if this suggestion was already proposed in a previous report and not acted on, the PR includes a counter ("This suggestion appeared in 2 prior reports without action")

A human reviews and merges or closes. The Curator never modifies rules directly. This is the "Augmented" in a mature context engineering workflow: the loop closes through human judgment, not automation.

### A/B Canary Probes

Before proposing a change, the Curator runs a small set of probe prompts against both the current config and the proposed config. Probes are simple, task-representative inputs that exercise the rule being changed.

```bash
# canary-ab.sh
OLD_CONFIG="$1"
NEW_CONFIG="$2"
PROBES_FILE="${3:-canary-probes.yaml}"

for probe in $(yq '.probes[].id' "$PROBES_FILE"); do
  question=$(yq ".probes[] | select(.id == \"$probe\") | .prompt" "$PROBES_FILE")
  old_out=$(run_with_config "$OLD_CONFIG" "$question")
  new_out=$(run_with_config "$NEW_CONFIG" "$question")
  compare_outputs "$probe" "$old_out" "$new_out"
done
```

Ten to twenty probes per PR is sufficient. Use cosine similarity for a first pass; run LLM-as-judge only on probes where similarity drops below 0.85. This keeps canary costs near zero for most PRs and reserving judgment for the edge cases that actually warrant it.

### Multi-timescale Operation

Running the Curator on a single cadence produces two failure modes: too frequent and you overwhelm reviewers, too infrequent and friction accumulates invisibly. Use three loops:

| Loop | Trigger | Action |
|---|---|---|
| Real-time | PostStop hook fires | Append friction event to local signal store |
| Weekly | Cron (Saturday 02:00) | Curator aggregates the week, generates PR if signal threshold met |
| Quarterly | Manual | Constitutional audit: check rule overlap, archive dormant skills, review profile consolidation candidates |

The quarterly loop is not automatable in any useful way. It requires reading the system's actual behavior, not just its logged signals.

### Signal Locality Decision

Where friction signals live determines what the Curator can access. Three options:

| Option | How it works | Best for |
|---|---|---|
| **A. Local cron** | Signals stay on the developer's machine; Curator runs as a macOS launchd job or local cron | Solo dev, privacy-first, no infra to maintain |
| **B. Pushed signal store** | PostStop hook pushes anonymized signals to a private repo or S3 bucket; Curator runs in CI | Teams of 5+, multi-dev reconciliation required (Section 14) |
| **C. Hosted dev env** | Signals land in a shared environment (Codespaces, Coder) by default | Teams already on hosted dev infrastructure |

Option A is the right default for solo developers. Option B is necessary for any team that wants cross-developer pattern analysis or multi-dev profile reconciliation; the signal store should be a private repo, not a SaaS platform, to keep sensitive path and tooling data off third-party servers. Option C is only worth considering if the team is already committed to hosted dev environments for other reasons.

### Suggestion Suppression

A suggestion that appears in three consecutive reports without any action taken should change state: it either moves to "pending human decision" with a blocking flag in the next PR, or it gets closed as "won't fix" with a documented reason. Allowing suggestions to repeat silently is the same failure mode as the open loop, just more subtle.

---

## 12. Ejection: Disciplined De-engineering

Every part of the context engineering stack helps you add more: more rules, more skills, more profile sections. None of it helps you remove what stopped working. This is the missing half of the discipline, and its absence is the reason Level 5 systems silently degrade.

Context debt accumulates through addition. A rule written for a sprint six months ago may conflict with three newer rules, fire on edge cases the author never anticipated, and generate friction on every session. Without an ejection mechanism, it stays forever because removing it feels risky and auditing it takes time nobody has.

### Ejection Heuristics

Three metrics drive ejection candidates:

**Activation threshold**: rules that have not fired in the past N months are likely dead weight. The signal: if the pattern they prevent hasn't appeared in the friction log, either the rule is working perfectly or nobody writes code that triggers it. Both cases suggest dormancy. Default: 3 months for skills, 6 months for rules.

**ROI tracking**: skills where the friction they produce (from overly strict enforcement, wrong-context triggers) exceeds the friction they prevent. The signal: the skill appears in `active_skills` fields of friction events more often than it appears in "resolved" events. Negative ROI over 4+ weeks is an ejection candidate.

**Profile overlap**: when a rule appears in more than 80% of individual developer profiles, it belongs in the shared config rather than in each profile. This is a consolidation proposal, not an ejection, but it reduces duplicate maintenance surface.

### Ejection vs. Archive

Ejection does not mean deletion. The Archive Pattern (Section 8) established the institutional memory reason for keeping retired rules with a retirement note. Ejection is the *automated detection* of what should be archived. The Curator flags candidates; a human makes the final call and moves the rule to `CLAUDE-archive.md` with a date and reason.

No commercial observability tool (Braintrust, Langfuse, Helicone, LangSmith) implements this pattern. They track what happened; they do not track what your configuration contains nor suggest removing the parts of it that are causing harm. The ejection mechanism is the discipline that commercial tools skip because it requires knowing your config schema, not just your prompt history.

---

## 13. Constitutional and Self-consistency Audits

A config that grows without constraint eventually contradicts itself. Rule A says "always use ESLint for formatting". Rule B says "prefer Biome for speed". A new developer reads both and does neither, because the rules conflict and the system gives no signal that they conflict. Constitutional audits catch this before it compounds.

### Constitutional Audit

Before each Curator PR lands, run a constraint check against two targets: the proposed change vs. the existing rule set, and the proposed change vs. an explicit `constitution.md`.

```yaml
# .claude/constitution.md (example)
invariants:
  - id: no-auto-commit
    rule: "Never commit without explicit user request"
    rationale: "2024-incident: automated commit bypassed review gate"
  - id: no-destructive-without-confirm
    rule: "Never run rm, DROP, or force-push without confirmation"
    rationale: "Production safety baseline"
  - id: diff-before-merge
    rule: "Always show diff before applying multi-file changes"
    rationale: "Preserves human review in the loop"
```

The constitutional check is two queries: does the proposed rule contradict any invariant, and does it conflict with any existing rule in `.claude/rules/`? Both queries can run as Claude prompts with the constitution and rule list as context. This costs a few hundred tokens per Curator run and prevents rule conflicts from silently accumulating.

The lineage of this pattern is Constitutional AI (Anthropic, 2022) and RLAIF: using a high-level value document to constrain a lower-level generation process. The transposition here is from output alignment (checking a model's responses) to config alignment (checking a rule system's internal consistency). The mechanism is simpler because the inputs are shorter and fully deterministic.

### Self-consistency Check

Systems that modify themselves accumulate a specific failure mode: the documentation claims a state that no longer matches reality. On a production ACE installation, the file `ace-improvement-loop.md` claimed "skills versioning 100% complete as of 2026-03-04". The actual state, measured six weeks later, was 20 out of 114 skills versioned (17%). The gap persisted because nobody audited the claims the system made about itself.

The self-consistency check runs weekly, separately from the Curator. It reads the claims in your ACE documentation and verifies them against the measured state:

| Claim type | How to verify |
|---|---|
| "N rules active" | `find .claude/rules -name "*.md" \| wc -l` |
| "Skills versioning X% complete" | `grep -l "^version:" .claude/skills/*/SKILL.md \| wc -l` divided by total skills |
| "Last curator run: date" | Check the most recent Curator PR creation date in git log |
| "Friction trending down" | Compare 4-week moving average from signal store |

When a claim diverges from the measured state by more than 10%, the check appends a "Self-consistency violations" section to the next Curator report. This is not a failure state; it is the system doing its job. Documentation rot is normal. Catching it weekly is not.

---

## 14. Multi-dev Profile Reconciliation

Profile-based assembly (Section 5) solves the N-devs × M-tools fragmentation problem by giving each developer a personal profile. Over time, a new problem emerges: individual profiles diverge. Developer A's profile adds a rule preventing direct production database access. Developer B adds the same rule two weeks later, worded slightly differently. Developer C never adds it. The rule that should be in the shared config ends up duplicated, inconsistent, and unenforceable.

This is specific to hierarchical config systems like Claude Code's three-tier structure (user `~/.claude/CLAUDE.md` + project `CLAUDE.md` + plugin rules). No commercial LLMOps tool solves this because none of them operates at the granularity of individual rule files across a team's config hierarchy.

### Detection

The reconciliation check scans all active developer profiles and identifies rules that appear in more than 50% of them:

```bash
# profile-reconcile.sh
PROFILES_DIR="${1:-.claude/profiles}"
THRESHOLD="${2:-0.5}"

all_rules=$(find "$PROFILES_DIR" -name "*.yaml" -exec yq '.includes[]' {} \; | sort | uniq -c | sort -rn)
total_profiles=$(find "$PROFILES_DIR" -name "*.yaml" | wc -l)

while IFS= read -r line; do
  count=$(echo "$line" | awk '{print $1}')
  rule=$(echo "$line" | awk '{print $2}')
  ratio=$(echo "scale=2; $count / $total_profiles" | bc)
  if (( $(echo "$ratio >= $THRESHOLD" | bc -l) )); then
    echo "HOIST CANDIDATE ($count/$total_profiles profiles): $rule"
  fi
done <<< "$all_rules"
```

A rule that appears in 4 out of 5 developer profiles belongs in the project-level `CLAUDE.md`, not in four separate profiles.

### Preservation

Not everything should be hoisted. Personal preferences stay personal: tone settings, verbosity levels, preferred explanation depth, language choices. The reconciliation check distinguishes behavioral rules (what Claude does) from preference rules (how Claude communicates). Behavioral rules above the threshold are hoist candidates; preference rules are never touched.

For a team of 5 or more developers, run the reconciliation check monthly. For teams above 10, run it as part of the quarterly constitutional audit. The output is a list of hoist candidates with a proposed diff for the shared config; a human reviews and applies. The check does not modify any file automatically.

---

## 15. Token Audit Workflow

Context engineering theory only converts to real gains once you measure your actual overhead. Most developers discover they are loading 40-60K tokens of fixed context before any user task begins: configuration files, rules, hooks output, memory files, and the Claude Code system prompt all compound. This section provides a reproducible audit workflow that takes under five minutes and produces an actionable plan.

### Real-World Session Benchmarks

Before auditing your overhead, calibrate against what practitioners observe on real codebases. The figures below come from heavy users on Max 200 plans running Opus 4.7 at high effort. Treat them as upper-range references: the same tasks at Sonnet-level effort run 30-50% lower.

**Per-turn (input + output combined)**

| Task type | Typical range |
|-----------|---------------|
| Simple question, 1-2 tool calls | 10-30K tokens |
| Targeted edit with file reads | 30-80K tokens |
| Feature implementation with exploration | 100-300K tokens |
| Heavy investigation (MCP, multi-agent, Datadog) | 300K-1M+ tokens |

**Per-session (full conversation)**

| Session type | Typical range |
|--------------|---------------|
| Quick fix | 100-300K tokens |
| Complete PR with tests | 500K-2M tokens |
| Long session with compaction | 5M-20M+ tokens |

The dominant cost driver is input tokens, not output. A 1,000-line file re-read five times in the same session adds roughly 50K input tokens on its own. MCP tools that return verbose JSON (Notion, Datadog, GitHub API responses) compound this quickly: a single Datadog query can push 20-50K tokens into context before the model even processes the data.

Team-level perspective: in a Slack community survey of Claude Code power users (May 2026), individual heavy users reported 300-430M tokens per day on complex agentic workflows; median team usage ran closer to 40K tokens per request across a mixed team (simple and complex tasks combined), with heavy users reaching 85K+.

Sub-agents shift the math. Each sub-agent operates in a shorter, focused context window, so per-agent token cost is lower. Total cost across all agents in a complex workflow is typically higher than a single long session because you are spawning many agents. What improves is quality and parallelism, not raw token efficiency.

### What Counts as Fixed Context

Every session starts with a baseline of tokens that Claude loads before processing a single user message:

| Component | Loaded when | Typical size |
|-----------|-------------|--------------|
| `~/.claude/CLAUDE.md` + `@imports` | Always | 5-15K tokens |
| Project `CLAUDE.md` | Always | 2-8K tokens |
| `.claude/rules/*.md` (auto-loaded) | Always | 5-40K tokens |
| `MEMORY.md` (project memory) | Always | 1-3K tokens |
| Claude Code system prompt | Always | ~7,500 tokens |
| Hook output | Per tool call | 0.1-2K tokens × call frequency |
| `.claude/commands/*.md` | On invocation only | 0 by default |
| `.claude/agents/*.md` | On invocation only | 0 by default |

The critical distinction: `.claude/rules/` loads every `.md` file at session start regardless of relevance. Commands and agents are lazy-loaded — they cost nothing until invoked. Rules files are the most common source of unexpected overhead.

### Step 1 — Measure the Components

Run these commands from your project root to get a breakdown by component:

```bash
# Project CLAUDE.md
echo "=== PROJECT CLAUDE.md ===" && wc -c CLAUDE.md

# Rules files sorted by size (your biggest opportunity)
echo "=== RULES FILES ===" && find .claude/rules -name "*.md" 2>/dev/null \
  | xargs wc -c 2>/dev/null | sort -rn | head -20

# Global config files
echo "=== GLOBAL ~/.claude ===" && ls -la ~/.claude/*.md 2>/dev/null \
  | awk '{print $5, $9}' | sort -rn
```

### Step 2 — Calculate Your Token Budget

Tokens ≈ characters ÷ 4 (rough but reliable for English/code mix).

```bash
# Full budget estimate
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat | wc -c)
MEMORY=$(find ~/.claude/projects -name "MEMORY.md" -path "*$(pwd | tr '/' '-')*" \
  2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
TOTAL=$(( GLOBAL + PROJECT + RULES + MEMORY + 30000 ))

echo "Global ~/.claude   : ~$(( GLOBAL / 4 )) tokens"
echo "Project CLAUDE.md  : ~$(( PROJECT / 4 )) tokens"
echo "Rules (auto-loaded): ~$(( RULES / 4 )) tokens"
echo "MEMORY.md          : ~$(( MEMORY / 4 )) tokens"
echo "System prompt      : ~7,500 tokens (estimate)"
echo "---"
echo "TOTAL              : ~$(( TOTAL / 4 )) tokens"
```

For context: Claude's window is 200K tokens. A 60K fixed overhead means 30% consumed before any work begins. Against a typical coding task that uses 20-40K additional tokens, that leaves less than half the window for actual output.

### Step 3 — Classify Rules by Usage Frequency

The rules files are usually where the biggest savings live. For each file in `.claude/rules/`, ask one question: how often is this relevant in a typical session?

| Class | Definition | Action |
|-------|------------|--------|
| **Always critical** | Applies to every task (coding conventions, output format, safety rules) | Keep auto-loaded |
| **Sometimes needed** | Relevant in 20-40% of sessions (debugging methodology, task management) | Keep auto-loaded if small; consider on-demand if large |
| **Rarely needed** | Relevant in under 10% of sessions (Figma workflow, Windows compatibility, design system) | Remove from auto-load |
| **Never needed** | Outdated, covered elsewhere, or not relevant to this project | Delete or archive |

Run this classification as a prompt:

```
Read every file in .claude/rules/. For each file, classify it as:
- ALWAYS: applies to most tasks in a typical session
- SOMETIMES: applies in 20-40% of sessions
- RARELY: applies in under 10% of sessions

Output a table: | File | Size (chars) | Class | Reasoning |
Sort by size descending within each class.
Calculate: total chars that could be removed from auto-load if RARELY files
are excluded.
```

### Step 4 — Audit Hook Overhead

Hooks that fire on `PreToolUse` or `PostToolUse` run on every tool call. Each invocation injects its stdout into the context. A hook that outputs 500 characters per call, running 150 times per session, adds 75K characters (~19K tokens) to the session context.

To check your hooks:

```bash
# List all hooks and their event types
cat ~/.claude/settings.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
hooks = data.get('hooks', {})
for event, hook_list in hooks.items():
    for h in hook_list:
        cmd = h.get('command', h.get('hooks', [{}])[0].get('command', '?'))
        print(f'{event}: {cmd[:80]}')
"
```

For each `PreToolUse` or `PostToolUse` hook, estimate its output size by running it manually and measuring stdout. Multiply by your average tool calls per session (check `/cost` after a typical session to get the tool call count).

**High-overhead patterns to look for:**
- Hooks that `cat` files or print multi-line summaries on every call
- Hooks that run `git status` or `git log` unconditionally
- `echo` statements used for debugging that were never removed

### Step 5 — Build the Action Plan

Typical savings without RAG or custom infrastructure:

| Action | Effort | Risk | Typical savings |
|--------|--------|------|----------------|
| Remove "auto-loaded" from rarely-used rules | 30 min | Low | 5-20K tokens |
| Split large rules files into core + detail | 1-2h | Low | 3-8K tokens |
| Trim hook stdout to essential fields | 1h | Low | 2-10K tokens |
| Compress verbose rules (see §8) | 1-2h | Low | 2-5K tokens |
| Archive outdated MEMORY.md entries | 30 min | Low | 1-2K tokens |

A realistic first pass typically yields 30-50% reduction in fixed context without touching anything that requires infrastructure.

### The RAG Question

You may encounter advice to move rules files into a vector database and retrieve them dynamically (RAG). This is a valid optimization at scale — it converts fixed overhead into per-query retrieval and enables precise lazy-loading.

Before investing in that infrastructure, verify the math honestly:

- How many tokens would you actually save? (Measure first with Steps 1-3)
- What is the setup cost? A pgvector or Chroma setup with a custom MCP server is a 1-2 week project for a working team
- At what point does the break-even occur? If your fixed context is already under 20K tokens after simple cleanup, RAG adds complexity for marginal gain

For most individual developers and small teams, classification-based lazy loading (removing the auto-load tag from rarely-used files) achieves 80% of the gains at 2% of the infrastructure cost. RAG earns its complexity when you have 50+ rule files and need automated, intent-based loading.

### Audit Prompt Template

The following prompt produces a complete audit report when run inside a project. Replace the path variables as needed:

```
# Token Audit — [PROJECT NAME]

Audit this Claude Code project configuration for token overhead.
Be systematic and exhaustive, not superficial.

**Step 1 — Inventory**
List every file that is loaded at session start:
- ~/.claude/CLAUDE.md and all @imported files (with line counts)
- ./CLAUDE.md (line count)
- .claude/rules/*.md (all files, sorted by size)
- Project MEMORY.md (line count)

For each file, note: lines, approximate tokens (chars ÷ 4), and one-sentence
description of what it contains.

**Step 2 — Budget calculation**
Calculate: total fixed-context tokens before any user task.
Show the breakdown by component. Express as % of Claude's 200K window.

**Step 3 — Signal/noise classification**
For every rules file, classify as ALWAYS / SOMETIMES / RARELY based on how
often it would apply in a typical session on this project.
Flag any file over 5K chars that is classified SOMETIMES or RARELY.

**Step 4 — Hook audit**
Read .claude/settings.json (and ~/.claude/settings.json).
For each hook: event type, command, estimated stdout per invocation, and
whether it fires on every tool call or only at session boundaries.
Flag hooks that inject more than 200 chars per PreToolUse or PostToolUse call.

**Step 5 — Action plan**
Produce a prioritized table:
| Action | Estimated token savings | Effort | Risk |
Sort by: savings descending, then effort ascending.
Include only actions achievable without external infrastructure (no RAG, no
vector databases, no custom MCP servers).

**Step 6 — RAG verdict**
Based on the remaining savings after Step 5, calculate whether RAG would be
worth it: estimate residual savings, estimate setup cost in hours, and state
clearly whether the infrastructure investment is justified.
```

---

## 16. Research Patterns: What the Literature Shows

Applied context engineering draws from academic research on how language models process long inputs. Four findings have practical implications for how you structure context in production agents.

### The Lost-in-the-Middle Effect

**Source**: Liu et al. (2023), Stanford — "Lost in the Middle: How Language Models Use Long Contexts"

Performance on retrieval and reasoning tasks degrades when relevant information is placed in the middle of a long context window. Models perform best when critical information appears at the beginning (primacy) or end (recency) of the context, and worst when it's buried in the middle.

The effect is consistent across model sizes and context lengths. A 20-document retrieval task can drop from ~70% accuracy when the answer is at position 1 to ~40% when it's at position 10, rising back toward 70% at position 20.

**Practical implications for agents:**

- Put the most decision-critical information at the start or end of your system prompt, not in the middle of a long CLAUDE.md
- When summarizing multiple sources, lead with the most relevant finding, not the most recent
- If you have a list of tool results, the first and last results will be recalled more reliably than those in the middle
- For evaluation tasks where Claude reviews N items, split into smaller batches rather than sending everything at once

The implication isn't that you should make contexts shorter — it's that position within the context window is a design variable, not an accident.

### Progressive Summarization Risks

Summarization pipelines that compress summaries of summaries lose information in ways that are invisible to the model. Each compression pass removes details, but the model's confidence doesn't decrease proportionally. By the third or fourth compression pass, the model can answer questions about the original content fluently, but the answers may no longer be accurate — it's confabulating based on what typically follows the compressed patterns it retained.

**The specific risks:**

- **Transactional facts disappear first**: Specific numbers, dates, names, and conditions get abstracted away in early compression passes while narrative structure is preserved
- **Confidence stays high**: The model doesn't know it's working from compressed information; it answers with the same certainty as if it had access to the original
- **No retrieval signal**: Unlike RAG, where a failed retrieval is visible, summarization failures are silent — the model produces fluent text regardless

**Mitigations:**

```markdown
<!-- In CLAUDE.md for research/summarization agents -->
## Summarization Rules
- Always retain exact numbers, dates, and proper nouns in summaries — never paraphrase them
- Mark summaries with their compression level: [summary-level-1], [summary-level-2]
- If you cannot find a specific fact in the summary you have access to, say so — do not reconstruct from plausible inference
```

For multi-step agents that compress context to stay within budget, limit the chain to 2 compression passes before going back to source material.

### Stratified Sampling for Calibration

When evaluating whether a context-engineering setup is working, random sampling misses systematic failures. A random sample from a 100-item test set might show 85% accuracy — but if the 15 failures cluster in a specific difficulty tier (long documents, ambiguous instructions, edge cases), you won't detect the pattern.

Stratified sampling divides the evaluation set into strata by a relevant attribute (document length, instruction ambiguity, source quality) and tests each stratum independently.

**For context engineering specifically:**

| Stratum | Why it matters |
|---------|----------------|
| Short context (< 5K tokens) | Baseline — should be near 100% |
| Medium context (5K–50K) | Where most real work happens |
| Long context (50K+) | Where degradation first appears |
| Position-critical (key info in middle) | Tests lost-in-the-middle directly |
| High-instruction density | Tests the 150-instruction ceiling |

If your accuracy on the long-context stratum is 20 points below the short-context stratum, that's a signal — add position-based structuring or implement chunked processing. Aggregate metrics would have hidden that gap.

### Claim-Source Mapping (Provenance Tracking)

In agents that synthesize information from multiple sources (web search, file reads, tool results), claims in the final output should be traceable to their source. Without provenance tracking, hallucinations are indistinguishable from accurate synthesis, and errors compound across agent steps.

**What claim-source mapping looks like:**

Rather than letting the agent produce a summary with no source attribution, structure the intermediate representation to keep claims linked to their source:

```python
# Each synthesis step preserves provenance
claims = [
    {"claim": "The API rate limit is 1000 req/min", "source": "tool:get_api_docs", "confidence": "direct"},
    {"claim": "The rate limit was increased in v2.3", "source": "web:release-notes-url", "confidence": "direct"},
    {"claim": "Rate limits reset every 60 seconds", "source": "inferred", "confidence": "inferred"},
]
```

Claims tagged as "inferred" or lacking a source should be flagged as uncertain in the final output, not presented with the same confidence as directly-sourced claims.

**Implementation pattern for multi-step agents:**

```markdown
<!-- In research agent system prompt -->
For every factual claim you include in your response:
- Tag it with the source (tool name, file path, URL, or "inferred")
- If you cannot identify the source, mark the claim as uncertain
- Do not present inferred conclusions with the same certainty as directly-observed facts
```

The difference between claim-source mapping as a QA mechanism vs as a compliance mechanism: compliance tracking asks "did we use authorized sources?", QA tracking asks "is this specific claim accurate?" Both are valuable but for different failure modes. Agents that handle factual queries or generate reports need the QA version.

### Chain-of-Thought as a Formal Compute Extension

**A model's "reasoning" is defined operationally as the intermediate tokens it generates between an input and an output, not as some separate cognitive faculty.** This reframing carries a formal backing: a transformer that is allowed to produce a chain of reasoning before answering can solve any problem solvable by a Boolean circuit, given a constant number of intermediate steps. This is the theoretical anchor for why extended thinking and chain-of-thought prompting change what a model is capable of, not just how it explains its answer: token budget spent on reasoning is compute budget, not commentary. (*Denny Zhou, Google DeepMind, Stanford CS25 V5, 2025*)

### New Research Directions (April to July 2026)

Research on context management shifted register during this window: earlier papers mostly documented context rot as a problem, while this batch proposes concrete mitigation architectures. Treat the results below with the confidence level noted for each; several are single-paper claims not yet independently reproduced.

| Paper | Contribution | Confidence |
|-------|--------------|------------|
| **ACON** ([arXiv:2510.00615](https://arxiv.org/pdf/2510.00615), updated June 2026) | Compresses both tool observations and interaction history into condensed natural-language representations, iteratively refining its own compression rules from analysis of agent failures. Updated figures: 26 to 54% peak-token reduction. | Update to an existing October 2025 paper, not a first publication |
| **Less Context, Better Agents** ([arXiv:2606.10209](https://arxiv.org/abs/2606.10209), June 2026) | Tests four context configurations on GPT-5 across 50 hotel expense-report tasks. Pruned-and-summarized history beats full history on both cost and success rate. | Independent research paper |
| **AMA-Bench** ([arXiv:2602.22769](https://arxiv.org/abs/2602.22769), February 2026) | Benchmark dedicated to long-horizon agent memory. Finds existing memory systems underperform because they rely on lossy similarity retrieval and miss causal or goal-relevant information, not just recency. | Research paper |
| **Agent Memory: Characterization and System Implications** ([arXiv:2606.06448](https://arxiv.org/abs/2606.06448), June 2026) | First systems-level study of what long-horizon stateful agent workloads actually look like at the infrastructure layer. | Research paper |
| **ContextBudget** ([arXiv:2604.01664](https://arxiv.org/pdf/2604.01664), April 2026) | Formalizes context management as a budget-allocation problem for research agents. | Research paper |
| **Classifier Context Rot** ([arXiv:2605.12366](https://arxiv.org/html/2605.12366v1), May 2026) | Shows the degradation pattern also affects classifier and monitor models that observe agent trajectories, not only generation. This is the source of the MonitorBench figure cited earlier in this section. | Research paper, distinct angle from Chroma's original context-rot finding |
| **Context Kubernetes** ([arXiv:2604.11623](https://arxiv.org/abs/2604.11623), April 2026) | Proposes treating enterprise context delivery as structurally analogous to container orchestration: a declarative YAML manifest, a reconciliation loop, and a three-tier permission model where agent authority stays a strict subset of human authority. | Prototype only, eight experiments, not adopted at scale, flag as early-stage |
| **Recursive Language Models (RLM)** ([arXiv:2512.24601](https://arxiv.org/abs/2512.24601), MIT CSAIL) | Treats an oversized input as an external variable in a Python REPL: the model writes code that recursively chunks and re-queries segments instead of ingesting everything in one pass. Claimed result: processing inputs two orders of magnitude beyond the base context window at comparable cost. | Single-paper, self-reported benchmark, not yet independently replicated at scale; present as a lab result, not an established fact |

**What changed practically**: Anthropic's own framing, restated in the [Managed Agents post](https://www.anthropic.com/engineering/managed-agents) above, moved the field's central question from "what words go in the prompt" to "what context configuration is most likely to produce the intended behavior." That reframing is now visible in the research agenda too: the newer papers target architecture (ACON's self-refining compression, Context Kubernetes' orchestration model, RLM's recursive delegation) rather than further documentation of the original context-rot finding.

---

## 17. Attention Mechanics & Reliability

Claude's attention is not uniform across the context window. Position within the prompt measurably affects whether information is used. This section covers the mechanics, the evidence behind them, and the patterns that compensate.

---

### The Lost-in-the-Middle Problem

Research by Liu et al. (*Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)) examined how large language models use information at different positions within long contexts. The finding: retrieval accuracy follows a U-shaped curve. Information placed at the start or end of a long context is recalled significantly more accurately than information placed in the middle.

For Claude specifically, NIAH (Needle-in-a-Haystack) benchmarks on the 100K context window showed that passage retrieval accuracy dropped from 98% for documents placed at the start or end to 27% for documents placed in the middle, a 71-point gap. Subsequent model releases improved middle-context recall, but the U-shaped bias persists at scale.

**Practical consequence:** Any information the model needs to use reliably should not be buried in the middle of a long context.

This has a direct implication for how to think about large context windows: treating a 1M-token window as a space to dump everything potentially relevant is an anti-pattern, not a capability demonstration. A practitioner who has worked extensively with RAG and context engineering at Google notes that exploiting a 1M-token window is not a sign of capability, and may in fact be its opposite; information in the middle of a very long context competes poorly for the model's attention regardless of window size. (*Guillaume Laforge, Developer Advocate, Google Cloud, [IFTTD ep 361](https://www.ifttd.io/episodes/rag)*)

---

### Primacy and Recency Placement

The two high-attention zones are the beginning (primacy) and the end (recency) of the context window. The sandwich pattern exploits both:

```
[System prompt — persistent constraints, persona, critical rules]
[User's long document or retrieved context — middle zone]
[End of user message — restate the task + any constraints that must hold]
```

For documents long enough that the middle-zone penalty matters (roughly above 20,000 tokens), place the most critical information at both ends:

```python
def build_analysis_prompt(document: str, critical_facts: list[str]) -> str:
    facts_block = "\n".join(f"- {f}" for f in critical_facts)
    
    return f"""CRITICAL FACTS (reference throughout your analysis):
{facts_block}

DOCUMENT TO ANALYZE:
{document}

REMINDER — apply these critical facts in your analysis:
{facts_block}

Now produce the analysis."""
```

Repeating critical facts at the end is not redundant. It compensates for the middle-zone attention drop on the primary document.

**Per-section passes for very long documents:**

For documents above 50,000 tokens, a single-pass analysis risks missing content in the middle sections. The per-section + integration pattern:

```python
def analyze_long_document(client, document: str, section_size: int = 8000) -> str:
    sections = split_into_sections(document, max_tokens=section_size)
    section_analyses = []
    
    for i, section in enumerate(sections):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": (
                    f"Analyze section {i+1} of {len(sections)}:\n\n{section}\n\n"
                    f"Focus on key facts, risks, and obligations. "
                    f"Note: this is one section of a longer document."
                )
            }]
        )
        section_analyses.append(response.content[0].text)
    
    # Integration pass with all section summaries in scope
    integration_prompt = "\n\n".join([
        f"SECTION {i+1} ANALYSIS:\n{analysis}"
        for i, analysis in enumerate(section_analyses)
    ])
    
    final_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"You have {len(sections)} section analyses from a single document. "
                f"Synthesize them into a complete analysis:\n\n{integration_prompt}"
            )
        }]
    )
    
    return final_response.content[0].text
```

Each section analysis is short and keeps the relevant content in the primacy position. The integration pass works on summaries rather than the full document, keeping everything within high-attention range.

---

### Context Window Size vs Attention Quality

Larger context windows do not mean better comprehension of large inputs. Attention quality degrades before the context window fills. In practice:

- Claude 3.5 Sonnet: noticeable quality degradation begins around 50,000-70,000 tokens of effective content
- Claude 3 Opus: similar degradation threshold, with a stronger middle-zone penalty
- Models with 1M-token windows: the window size enables more data to be present, not necessarily better use of that data

The misconception is treating context window size as a quality guarantee. A 200K-token input does not get the same per-token attention quality as a 10K-token input. For tasks requiring precise use of scattered facts, a well-structured 30K prompt often outperforms a raw-dump 200K prompt.

**Design rule:** fit the context to the task, not the task to the context.

---

### Persistent Facts Block

The persistent facts block is a structured section, placed at the start of the system prompt, containing facts the model must reference throughout the conversation. Unlike retrieval, it is verbatim inclusion: the facts are always in the primacy position, always in scope, and compatible with prompt caching.

```python
PERSISTENT_FACTS = """
## Reference: Company Context

Entity: Acme Corp (Delaware C-Corp, EIN: 12-3456789)
Fiscal year end: December 31
Applicable law: Delaware corporate law, US federal regulations
Jurisdiction for disputes: Court of Chancery, Delaware
Authorized shares: 10,000,000 common @ $0.001 par
"""

system_prompt = f"""{PERSISTENT_FACTS}

You are a contract analysis assistant. Use the company context above for all entity references.
[rest of system prompt]
"""
```

Persistent facts blocks are prompt-cache friendly: because they appear at a fixed position with static content, Anthropic's prompt caching will cache them after the first call, reducing cost and latency on subsequent turns.

Keep the persistent facts block under 500 tokens. Beyond that, retrieval with re-ranking is more effective because the block itself starts falling into the middle zone.

---

### Scratchpad Pattern

The scratchpad pattern gives the model persistent working memory across turns without relying on context accumulation. A synthetic assistant message at the start of the conversation holds structured state; the orchestrator updates it programmatically after each turn.

```python
def initialize_scratchpad(task_spec: dict) -> str:
    return f"""<scratchpad>
<task>{task_spec['description']}</task>
<status>in_progress</status>
<completed_steps>[]</completed_steps>
<pending_steps>{json.dumps(task_spec['steps'])}</pending_steps>
<working_notes></working_notes>
</scratchpad>"""

def update_scratchpad(scratchpad: str, updates: dict) -> str:
    for key, value in updates.items():
        scratchpad = re.sub(
            f"<{key}>.*?</{key}>",
            f"<{key}>{value}</{key}>",
            scratchpad,
            flags=re.DOTALL
        )
    return scratchpad

# Conversation structure:
messages = [
    {"role": "assistant", "content": initialize_scratchpad(task)},
    {"role": "user", "content": "Continue the task from your scratchpad."}
]

# After each turn, update the scratchpad with new state
new_scratchpad = update_scratchpad(
    messages[0]["content"],
    {
        "completed_steps": json.dumps(completed),
        "pending_steps": json.dumps(remaining),
        "working_notes": latest_notes
    }
)
messages[0]["content"] = new_scratchpad
```

The scratchpad stays in the primacy position (it is the first message) across all turns. Working notes accumulate there rather than growing the conversation history.

**Scratchpad vs rolling summary:** Use a scratchpad when you need structured state with programmatic update. Use rolling summaries when the accumulated context is unstructured conversation and you need to compress it.

---

### Rolling Context Summaries

As conversation history grows, older turns lose relevance but consume tokens. Rolling context summaries compress completed phases into a compact record before they drift into the middle zone.

```python
SUMMARY_TRIGGER_RATIO = 0.65  # summarize when context reaches 65% capacity

def maybe_summarize_history(
    client,
    messages: list[dict],
    context_limit: int,
    current_tokens: int
) -> list[dict]:
    if current_tokens / context_limit < SUMMARY_TRIGGER_RATIO:
        return messages
    
    # Separate messages to summarize from recent messages to keep verbatim
    keep_recent = 4  # keep last 4 turns verbatim
    to_summarize = messages[:-keep_recent]
    to_keep = messages[-keep_recent:]
    
    # Extract key facts before summarizing
    facts_response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract key facts, decisions, and open items from this conversation "
                    f"history as a compact list:\n\n"
                    + "\n".join(f"{m['role']}: {m['content']}" for m in to_summarize)
                )
            }
        ]
    )
    key_facts = facts_response.content[0].text
    
    summary_message = {
        "role": "assistant",
        "content": f"<conversation_summary>\n{key_facts}\n</conversation_summary>"
    }
    
    return [summary_message] + to_keep
```

Extract key facts before summarizing, not from the summary. Summaries lose edge cases and boundary conditions that often matter. A facts extraction pass with a smaller model (Haiku) is cheap and preserves more signal.

Trigger at 65% of the context limit rather than waiting for the 80% auto-compact threshold. Proactive compression keeps you in control of what is preserved.

---

## 18. Token Compression Tools

The previous sections focus on what to put in context. This section covers tooling that compresses what enters context at the pipeline level — reducing token volume before Claude ever processes it. These tools complement CLAUDE.md authorship: good context engineering reduces noise at design time, compression tools reduce volume at runtime.

Two independent tools operate at different layers of the Claude Code tool pipeline.

---

### Layer 1 — CLI Output: RTK

RTK (Rust Token Killer) is a CLI proxy that intercepts shell command output and compresses it before Claude reads it. It operates via a `PreToolUse` hook that rewrites commands like `git log` to `rtk git log`.

**What it compresses**: git, cargo, npm, pnpm, tsc, vitest, playwright, docker, kubectl, and more. Measured savings: 60-90% on supported commands.

**What it does not compress**: file reads, MCP tool results, anything not going through a Bash tool call.

```bash
brew install rtk-ai/tap/rtk   # or: cargo install rtk
rtk init --global              # installs PreToolUse hook + settings.json patch
rtk gain                       # dashboard: tokens saved per command
```

> **Cross-ref**: Full command reference and TOML filter DSL at [third-party-tools.md §RTK](../ecosystem/third-party-tools.md#rtk-rust-token-killer).

---

### Layer 2 — File Reads and Session Memory: lean-ctx

lean-ctx operates as a global MCP server that intercepts Read calls and Bash calls at the tool level, below RTK's shell hook. It uses tree-sitter AST parsing to extract only the relevant structure of a file rather than sending the full content.

**Installation** (one-time, global):

```bash
curl -fsSL https://raw.githubusercontent.com/yvgude/lean-ctx/main/skills/lean-ctx/scripts/install.sh | bash
lean-ctx setup   # registers MCP server + hooks in ~/.claude.json and ~/.claude/settings.json
```

No per-project setup required.

**The 10 read modes**

| Mode | What it returns | Best for |
|------|----------------|----------|
| `signatures` | Type and function signatures only | Large TypeScript/Rust files read for context |
| `map` | Exports and import dependencies | Understanding module relationships |
| `auto` | System selects based on file type and context usage | Default, safe for most cases |
| `full` | Full file, cached | Files you are about to edit |
| `diff` | Changed lines only | Re-reading a file after an edit |
| `lines:N-M` | Specific line range | Targeted inspection |
| `aggressive` | Maximum compression, syntax-stripped | Large files needed only for reference |
| `entropy` | High-entropy fragments only | Scanning for anomalies |
| `task` | Task-relevant lines | Active task set defined |

**Rule**: use `full` for files you will edit. Use `signatures` or `map` for files you are reading for context. The difference on a 2364-line file: `full` costs ~19,000 tokens, `signatures` costs ~200 tokens.

**Cache**: re-reading an unchanged file costs ~13 tokens regardless of file size. The cache is invalidated by file mtime.

**CCP (Context Continuity Protocol)**: on session end, lean-ctx writes a ~400-token summary of what was read, found, and decided. The next session loads it automatically, eliminating the cold-start cost of re-reading prior context.

**Measured benchmarks (TypeScript/T3 monorepo, 2455 files, 7063-node graph)**

| Metric | Value |
|--------|-------|
| Overall compression rate | 57.8% |
| ctx_read savings rate | 86% |
| Tokens saved in one day | 1.3M |
| schema.prisma 2364L → signatures | ~200 tokens (99%) |
| File re-read (cache hit) | 13 tokens |

**Monitoring your efficiency**

```bash
lean-ctx gain            # overall dashboard
lean-ctx gain --daily    # day-by-day savings
lean-ctx cep             # CEP score /100: compression, cache hit rate, consistency, mode diversity
lean-ctx sessions list   # session history with token counts
```

The `/lean-ctx-audit` slash command runs all of the above in one pass and synthesizes a report. Add it to `~/.claude/commands/lean-ctx-audit.md` to make it available in every project.

---

### Choosing between the two

RTK and lean-ctx do not overlap meaningfully. Their actual savings distribution from measured sessions:

| Source | Tool | % of total savings |
|--------|------|--------------------|
| File reads (AST) | lean-ctx | ~85% |
| Search results | lean-ctx | ~5% |
| Shell output | RTK | remainder |
| Shell output via lean-ctx | lean-ctx | <1% (RTK is better here) |

Install both. RTK handles CLI output; lean-ctx handles file reads and session memory.

**When lean-ctx adds the most value**: TypeScript, Rust, Python projects where large source files are read repeatedly, sessions run long enough that context fills before completion, and cross-session continuity matters.

**When lean-ctx adds less value**: Markdown-heavy documentation repos. The AST parser finds code examples embedded in Markdown rather than source structure. Gains exist but are lower than on code-first projects.

> **Cross-ref**: Full tool profiles at [third-party-tools.md §Context Compression](../ecosystem/third-party-tools.md#context-compression).

---

## Cross-References

- Architecture and project structure patterns: `guide/core/architecture.md`
- Methodology frameworks for AI-assisted development: `guide/core/methodologies.md`
- Hooks and automation for context management: `guide/ultimate-guide.md` §5 (Hooks)
- MCP server integration for extended context: `guide/ultimate-guide.md` §7 (MCP)
- Security considerations for context content: `guide/security/`
- Path-scoped module examples: `examples/` directory
- PRP methodology (Product Requirements Prompt, 5-layer structure): community framework by Wirasm/Widing — `guide/core/methodologies.md` for the full summary, or search the guide for "PRP" to see practical examples

---

*Part of the Claude Code Ultimate Guide. For the full reference, see `guide/ultimate-guide.md`.*
