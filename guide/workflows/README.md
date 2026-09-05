---
title: "Claude Code Workflows"
description: "Step-by-step guides for common development patterns with Claude Code"
tags: [workflow, guide, reference]
---

# Claude Code Workflows

Step-by-step guides for common development patterns with Claude Code.

---

## 🔍 Search & Discovery

### [Search Tools Mastery](./search-tools-mastery.md) ⭐ NEW

**Master the art of code search by combining rg, grepai, Serena & ast-grep**

Learn when to use each tool, how to combine them for maximum efficiency, and real-world workflows including:
- Exploring unknown codebases
- Large-scale refactoring
- Security audits
- Framework migrations
- Performance optimization

**Key Topics**:
- Quick decision matrix
- Complete feature comparison
- 5 combined workflows
- Performance benchmarks
- Common pitfalls
- Tool selection cheatsheet

---

## 🎯 Development Workflows

### [Plan-Driven Development](./plan-driven.md)

Structure complex tasks with planning mode before execution.

**When to use**: Multi-step features, architectural changes, uncertainty about approach

### [TDD with Claude](./tdd-with-claude.md)

Test-Driven Development workflow: write tests first, implement after.

**When to use**: Critical functionality, regression prevention, API design

### [Spec-First Development](./spec-first.md)

Write specifications before code for better requirements clarity.

**When to use**: Team collaboration, complex features, documentation-first projects

### [Iterative Refinement](./iterative-refinement.md)

Improve code through multiple refinement cycles.

**When to use**: Quality improvements, performance optimization, code cleanup

### [Best-of-N: Generate, Select, and Verify](./best-of-n.md)

Generate a declared set of independent candidates, score every candidate against a frozen rubric, verify the selected result outside its generation context, and preserve the proof log.

**When to use**: Several plausible solutions with material trade-offs and a reviewer or executable check that can distinguish them

**Reusable assets**: [Best-of-N skill](../../examples/skills/best-of-n/SKILL.md) and [TESTING.md proof record](../../examples/claude-md/TESTING.md)

### [Skeleton Projects](./skeleton-projects.md) ⭐ NEW

Use existing battle-tested repositories as scaffolding for new projects.

**When to use**: Starting new projects, standardizing team patterns, rapid prototyping from proven foundations

### [Team AI Instructions](./team-ai-instructions.md)

Scale CLAUDE.md across a multi-developer, multi-tool team with profile-based module assembly.

**When to use**: Team 5+ devs, multiple AI tools (Claude Code + Cursor/Windsurf), mixed OS

### [Changelog Fragments](./changelog-fragments.md) ⭐ NEW

**Enforce per-PR documentation with a 3-layer system: CLAUDE.md rule + UserPromptSubmit hook + CI gate**

Eliminates merge conflicts on `CHANGELOG.md`, captures context at implementation time, and ensures DB migrations are never silently deployed. Includes a reusable `UserPromptSubmit` hook pattern for enforcing any mandatory workflow step.

**Key Topics**:
- CLAUDE.md workflow rule for autonomous fragment creation
- `UserPromptSubmit` hook with 3-tier priority (enforcement, discovery, contextual)
- Conditional suggestion pattern: "if PR-intent without fragment-mention"
- CI enforcement with independent migration check job

### [Smart-Suggest Routing](./smart-suggest-routing.md) ⭐ NEW

**Two-engine `UserPromptSubmit` hook system: regex enforcement + self-calibrating BM25 lexical scoring**

Injects ranked skill suggestions as `additionalContext` so Claude proposes the right skill even when phrasing was never anticipated. BM25 generalizes from scenario examples; the regex layer handles enforcement patterns. Both run in parallel on every prompt.

**Key Topics**:
- Regex vs BM25 decision table (when each engine wins)
- Corpus format: 10+ positive + 3+ negative scenarios per skill
- `build-index.js`: leave-one-out calibration, F-beta threshold, `ok`/`excluded`/`conflict` status
- Wiring two hooks in parallel via settings.json
- Detached background index rebuild when corpus changes

### [RPI: Research → Plan → Implement](./rpi.md) ⭐ NEW

**3-phase feature development with explicit validation gates between phases**

Build features in three locked phases: Research feasibility first, plan the implementation second, write code third. Each phase produces a concrete artifact (RESEARCH.md → PLAN.md → code). Each gate requires an explicit GO before the next phase starts.

**When to use**: Features with unclear feasibility, more than a day of work, unknown technical territory, or anywhere discovering a wrong assumption late is costly

### [GitHub Actions Workflows](./github-actions.md) ⭐ NEW

**5 production-ready patterns for automating PR reviews, issue triage, and quality gates**

Connect Claude directly to your GitHub workflow via the official `claude-code-action`. Two modes: interactive (`@claude` mentions) and fully automated (push/schedule triggers).

**Key Topics**:
- Setup via `/install-github-app` (30-second quickstart)
- Pattern 1: On-demand PR review via `@claude` mention
- Pattern 2: Automatic review on every push
- Pattern 3: Issue triage and labeling
- Pattern 4: Security-focused review on sensitive paths
- Pattern 5: Scheduled weekly repo health check
- Cost control, concurrency, fork safety

**When to use**: Any team wanting AI-powered code review without managing infrastructure

---

### [Multi-Provider Code Review](./multi-provider-code-review.md) ⭐ NEW

**Run Claude Code Action alongside CodeRabbit and Greptile without triplicate findings**

Non-redundant architecture for three automated reviewers on the same PR: Claude owns deep semantic review and the merge-blocking gate, a deterministic tool owns PASS/FAIL pre-merge checks, a RAG tool owns cross-file invariants. Covers the CI gate script, batching for large PRs, delta-review, and cross-tool deduplication.

**When to use**: Running more than one automated code reviewer and finding the same issue reported three times, or wanting Claude's findings to actually block merge instead of just commenting

---

### [Cognitive Mode Switching](./gstack-workflow.md) ⭐ NEW

Switch between specialist roles across your ship cycle: strategic product gate, architecture review, paranoid code review, automated release, native browser QA, and retrospective.

**When to use**: Ship cycles where you want explicit separation between product direction, engineering rigor, review, and release, rather than one generic assistant handling all phases

---

## 🎨 Design & Content

### [Design to Code](./design-to-code.md)

Convert design mockups (Figma, wireframes) into working code.

**When to use**: Frontend development, UI implementation, design system work

### [OG Image Generation](./og-image-generation.md)

Generate social preview images dynamically at build time with Satori and resvg.

**When to use**: Astro projects, keeping social previews accurate without maintaining static PNGs

### [PDF Generation](./pdf-generation.md)

Generate professional PDFs using Quarto/Typst with Claude Code.

**When to use**: Reports, documentation, whitepapers, technical documents

### [Talk Preparation Pipeline](./talk-pipeline.md) ⭐ NEW

6-stage skill pipeline: raw material → structured talk → AI-generated slides via Kimi.

**When to use**: Conference talks, meetup presentations, internal tech talks (from article, transcript, or notes)

### [TTS Setup](./tts-setup.md)

Configure Text-to-Speech for Claude Code responses (Agent Vibes integration).

**When to use**: Audio feedback, accessibility, hands-free coding

---

## 🔬 Code Exploration

### [Exploration Workflow](./exploration-workflow.md)

Systematically explore and understand unfamiliar codebases.

**When to use**: New projects, legacy code, documentation gaps

**Related**: See [Search Tools Mastery](./search-tools-mastery.md) for advanced multi-tool exploration strategies.

---

## Multi-Agent & Advanced

### [Dynamic Workflows](./dynamic-workflows.md) ⭐ NEW

JavaScript scripts that orchestrate tens to hundreds of subagents with deterministic control flow, parallel fan-out, and automatic resume on interruption.

**When to use**: Multi-stage parallelizable work, long-running jobs, tasks needing structured data handoffs between phases, or any situation where a single agent would hit context limits

**Key Topics**:
- Primitive reference: `agent()`, `parallel()`, `pipeline()`, `phase()`, `log()`, `budget`
- `pipeline()` vs `parallel()` with benchmark data (3x latency difference, 2x token difference)
- Schema-structured outputs across phases
- 5 named patterns: adversarial verification, loop-until-dry, judge panels, multi-modal sweep, plan-execute-review
- Behavioral guarantees: determinism constraints, resume/caching, concurrency caps

---

### [Agent Teams](./agent-teams.md)

Orchestrate multiple specialized agents working in parallel on complex tasks.

**When to use**: Tasks that benefit from parallelism, specialized expertise, or independent verification

### [Agent Teams Quick Start](./agent-teams-quick-start.md)

Fast-track guide to setting up your first agent team in under 30 minutes.

**When to use**: New to multi-agent patterns, want to experiment before committing to full setup

### [Dual-Instance Planning](./dual-instance-planning.md)

Run Opus for planning and Sonnet for execution in two coordinated Claude Code instances.

**When to use**: Complex features needing deep reasoning for architecture, cost-effective execution

### [Event-Driven Agents](./event-driven-agents.md)

Coordinate agents through hook events rather than direct orchestration.

**When to use**: Reactive workflows, hook-triggered automation, loosely-coupled agent pipelines

### [Plan Pipeline](./plan-pipeline.md)

Full end-to-end plan pipeline: /plan-start, /plan-validate, /plan-execute as a coherent workflow.

**When to use**: Any significant feature where planning rigor pays off before writing code

### [Task Management](./task-management.md)

Multi-session task tracking with TodoWrite, tasks API, and context persistence across sessions.

**When to use**: Long-running tasks spanning multiple sessions, team coordination, complex backlogs

### [Cross-Session Messaging](./cross-session-messaging.md) ⭐ NEW

`ListAgents` and `SendMessage`: how independent, already-running Claude Code sessions discover and message each other, on the same machine or across your account, without a human relaying context between terminals.

**When to use**: Coordinating sessions you started and steer yourself (parallel worktrees, per-role sessions, cross-machine hand-offs), distinct from Agent Teams (a lead session spawns and supervises its own teammates)

**Key Topics**:
- `ListAgents` discovery: subagents, teammates, local peers, cloud, Remote Control
- Same-machine socket delivery vs. cross-machine Remote Control routing
- Security model: `crossSessionInbound`, `isolatePeerMachines`, why a peer message never carries authority
- Version timeline and limitations (message size cap, burst throttling)

---

## Quick Selection Guide

| Your Situation | Recommended Workflow |
|----------------|---------------------|
| **New to codebase** | [Exploration Workflow](./exploration-workflow.md) + [Search Tools Mastery](./search-tools-mastery.md) |
| **Complex feature** | [Plan-Driven](./plan-driven.md) or [Spec-First](./spec-first.md) |
| **Need reliability** | [TDD with Claude](./tdd-with-claude.md) |
| **Several plausible solutions with a stable rubric** | [Best-of-N](./best-of-n.md) |
| **Large refactoring** | [Search Tools Mastery](./search-tools-mastery.md) |
| **UI implementation** | [Design to Code](./design-to-code.md) |
| **Code quality** | [Iterative Refinement](./iterative-refinement.md) |
| **New project from template** | [Skeleton Projects](./skeleton-projects.md) |
| **Team AI instructions** | [Team AI Instructions](./team-ai-instructions.md) |
| **Enforce mandatory workflow steps** | [Changelog Fragments](./changelog-fragments.md) |
| **Skill routing from natural-language prompts** | [Smart-Suggest Routing](./smart-suggest-routing.md) |
| **Unknown feasibility, multi-day feature** | [RPI: Research → Plan → Implement](./rpi.md) |
| **Documentation** | [PDF Generation](./pdf-generation.md) |
| **Social previews** | [OG Image Generation](./og-image-generation.md) |
| **Conference talk from raw material** | [Talk Preparation Pipeline](./talk-pipeline.md) |
| **Distribute a guide asset with attribution** | [Guide Distribution](../../docs/workflows/guide-distribution.md) |
| **Audio feedback** | [TTS Setup](./tts-setup.md) |
| **Deterministic multi-agent orchestration** | [Dynamic Workflows](./dynamic-workflows.md) |
| **Multi-agent tasks** | [Agent Teams](./agent-teams.md) |
| **First agent team** | [Agent Teams Quick Start](./agent-teams-quick-start.md) |
| **Cost-optimized planning** | [Dual-Instance Planning](./dual-instance-planning.md) |
| **Hook-driven automation** | [Event-Driven Agents](./event-driven-agents.md) |
| **Full plan workflow** | [Plan Pipeline](./plan-pipeline.md) |
| **Multi-session tracking** | [Task Management](./task-management.md) |
| **Coordinating sessions you already have open** | [Cross-Session Messaging](./cross-session-messaging.md) |
| **Strategic gate before coding** | [Cognitive Mode Switching](./gstack-workflow.md) |
| **Non-MCP browser automation** | [Cognitive Mode Switching](./gstack-workflow.md) |

---

## Contributing

New workflow ideas? Open an issue or PR in the main repository.

**Workflow Template Structure**:
1. Title & Purpose
2. When to Use
3. Prerequisites
4. Step-by-Step Guide
5. Real-World Examples
6. Common Pitfalls
7. Related Workflows

---

**Last updated**: March 2026
