---
title: "Guide Documentation"
description: "Index of all core documentation files for mastering Claude Code"
tags: [guide, reference]
---

# Guide Documentation

Core documentation for mastering Claude Code, organized by topic.

---

## Getting Started

| File | Description | Time |
|------|-------------|------|
| [**learning-path/**](./learning-path/README.md) | **Structured 7-module learning path** for beginners: Installation, Core Loop, Memory, Agents, Skills, Hooks, Advanced Patterns | 8-11 hours |
| [learning-path/01-installation.md](./learning-path/01-installation.md) | Module 01: Install Claude Code and verify it works | 15 min |
| [learning-path/02-core-loop.md](./learning-path/02-core-loop.md) | Module 02: Understand the interaction loop and context | 45 min |
| [learning-path/03-memory.md](./learning-path/03-memory.md) | Module 03: Create CLAUDE.md and configure memory | 1 hour |
| [learning-path/04-agents.md](./learning-path/04-agents.md) | Module 04: Create specialized agents | 1.5 hours |
| [learning-path/05-skills.md](./learning-path/05-skills.md) | Module 05: Build reusable skills | 1.5 hours |
| [learning-path/06-hooks.md](./learning-path/06-hooks.md) | Module 06: Create automation hooks | 1 hour |
| [learning-path/07-advanced.md](./learning-path/07-advanced.md) | Module 07: Multi-agent orchestration | 2-3 hours |

---

## Core Reference

| File | Description | Time |
|------|-------------|------|
| [ultimate-guide.md](./ultimate-guide.md) | Complete reference covering all Claude Code features | ~3 hours |
| [cheatsheet.md](./cheatsheet.md) | 1-page printable quick reference | 5 min |
| [core/architecture.md](./core/architecture.md) | How Claude Code works internally (master loop, tools, context) | 25 min |
| [core/tools-reference.md](./core/tools-reference.md) | **Complete tools reference**: all 40 built-in tools, permission rule formats, per-tool behaviors (Bash timeouts, Edit read-before-edit, Glob cap, WebFetch lossy), and how-to for Monitor, Workflow, agent teams, Cron, Tasks API | 20 min |
| [core/methodologies.md](./core/methodologies.md) | 15 development methodologies reference (TDD, SDD, BDD, etc.) | 20 min |
| [core/visual-reference.md](./core/visual-reference.md) | Visual cheatsheet — ASCII diagrams for key concepts | 5 min |
| [core/claude-code-releases.md](./core/claude-code-releases.md) | Official release history (condensed) | 10 min |
| [core/known-issues.md](./core/known-issues.md) | **Critical bugs tracker**: security issues, token consumption, verified community reports | 15 min |
| [core/context-engineering.md](./core/context-engineering.md) | **Context Engineering**: token budget, modular architecture, team assembly, ACE pipeline, quality measurement | 25 min |
| [core/memory-systems.md](./core/memory-systems.md) | **Memory Systems**: native stack (CLAUDE.md, Auto Memory, Auto Dream), cross-session tools (claude-mem, agentmemory, ICM), team sharing, multi-agent patterns, architecture, risks, decision flowchart | 30 min |
| [core/glossary.md](./core/glossary.md) | **Glossary**: official Claude Code terminology (31 terms, paragraph format, with links to guide sections) | 5 min |
| [core/community-patterns.md](./core/community-patterns.md) | **Community Patterns**: ~130 community-coined patterns, workflow terms, AI engineering concepts, and quick-reference definitions | 10 min |
| [diagrams/](./diagrams/) | **Visual Diagrams Series**: 41 Mermaid interactive diagrams for model selection, agent lifecycle, security, multi-agent patterns | 15 min |

---

## Security

| File | Description | Time |
|------|-------------|------|
| [security/security-hardening.md](./security/security-hardening.md) | Security threats, MCP vetting, injection defense | 25 min |
| [security/sandbox-isolation.md](./security/sandbox-isolation.md) | Docker Sandboxes, cloud alternatives, safe autonomy workflows | 10 min |
| [security/sandbox-native.md](./security/sandbox-native.md) | Native Claude Code sandbox: configuration and security model | 10 min |
| [security/production-safety.md](./security/production-safety.md) | Production safety: guardrails, review gates, rollback strategies | 15 min |
| [security/data-privacy.md](./security/data-privacy.md) | Data retention and privacy guide | 10 min |
| [security/enterprise-governance.md](./security/enterprise-governance.md) | **Org-level governance**: usage charters, MCP approval workflow, guardrail tiers (Starter/Standard/Strict/Regulated), compliance | 25 min |

---

## Ecosystem

| File | Description | Time |
|------|-------------|------|
| [ecosystem/ai-ecosystem.md](./ecosystem/ai-ecosystem.md) | Complementary AI tools (Perplexity, Gemini, Kimi, NotebookLM, TTS) | 30 min |
| [ecosystem/agentic-tools.md](./ecosystem/agentic-tools.md) | **Agent tools comparison**: Hermes Agent, Codex CLI, Aider, Devin, SWE-agent, CrewAI, LangGraph, AutoGen, decision framework | 20 min |
| [ecosystem/mcp-servers-ecosystem.md](./ecosystem/mcp-servers-ecosystem.md) | **Community MCP servers**: 8 validated servers (Playwright, Semgrep, Kubernetes, etc.) with production configs | 25 min |
| [ecosystem/third-party-tools.md](./ecosystem/third-party-tools.md) | **Community tools**: GUIs, TUIs, config managers, token trackers, alternative UIs | 15 min |
| [ecosystem/context-engineering-tools.md](./ecosystem/context-engineering-tools.md) | **Context & token optimization**: output compression (RTK, Headroom), prompt compression (LLMLingua), AI gateways (Edgee, Portkey), RAG, LLMOps | 20 min |
| [ecosystem/remarkable-ai.md](./ecosystem/remarkable-ai.md) | Remarkable AI usage patterns and power-user techniques | 10 min |
| [ecosystem/practitioner-insights.md](./ecosystem/practitioner-insights.md) | **Practitioner field reports**: 65 paraphrased insights from IFTTD, Devoxx, Dev With AI Meetup, ByteByteGo, and Stanford Online, organized by theme (context engineering, agentic patterns, LLM evaluation, agent security, DevX and adoption) | 20 min |
| [ecosystem/team-knowledge-base.md](./ecosystem/team-knowledge-base.md) | **Team knowledge infrastructure**: 3-tier framework (static Markdown vault, MCP connectors for live systems, RAG at scale), RAG threshold (~100-1000 docs), Atlassian/Notion/GitBook MCP, Onyx/LlamaCloud/Ragie, plugin distribution, Code+Cowork bridge | 18 min |

---

## Roles & Adoption

| File | Description | Time |
|------|-------------|------|
| [roles/ai-roles.md](./roles/ai-roles.md) | AI roles mapping: when to use Claude Code vs Claude Desktop vs API | 10 min |
| [roles/adoption-approaches.md](./roles/adoption-approaches.md) | Implementation strategies for teams | 15 min |
| [roles/learning-with-ai.md](./roles/learning-with-ai.md) | Guide for juniors on using AI without losing skills | 15 min |
| [roles/agent-evaluation.md](./roles/agent-evaluation.md) | **Agent quality metrics**: Measuring custom agent effectiveness with hooks, tests, and feedback loops | 20 min |

---

## Operations

| File | Description | Time |
|------|-------------|------|
| [ops/devops-sre.md](./ops/devops-sre.md) | FIRE framework for infrastructure diagnosis and incident response | 30 min |
| [ops/observability.md](./ops/observability.md) | Session monitoring and cost tracking | 15 min |
| [ops/ai-traceability.md](./ops/ai-traceability.md) | AI attribution, disclosure policies, git-ai, compliance | 20 min |
| [ops/team-metrics.md](./ops/team-metrics.md) | **Team metrics for AI-augmented engineering**: DORA, SPACE, DX Core 4, AI-specific signals, by team size (5–25 people) | 20 min |
| [ops/ai-unit-economics.md](./ops/ai-unit-economics.md) | **AI unit economics**: per-task cost decomposition, real cost levers (routing, sub-agent isolation, exit criteria), autonomous agent break-even point, team budget governance | 15 min |

---

## Workflows

Hands-on guides for effective development patterns:

| File | Description |
|------|-------------|
| [workflows/tdd-with-claude.md](./workflows/tdd-with-claude.md) | Test-Driven Development with Claude |
| [workflows/spec-first.md](./workflows/spec-first.md) | Spec-First Development (SDD) |
| [workflows/plan-driven.md](./workflows/plan-driven.md) | Using /plan mode effectively |
| [workflows/iterative-refinement.md](./workflows/iterative-refinement.md) | Iterative improvement loops |
| [workflows/tts-setup.md](./workflows/tts-setup.md) | Add text-to-speech narration to Claude Code (18 min) |
| [workflows/task-management.md](./workflows/task-management.md) | Multi-session task tracking, TodoWrite migration |
| [workflows/agent-teams.md](./workflows/agent-teams.md) | Orchestrating multi-agent teams for complex tasks |
| [workflows/agent-teams-quick-start.md](./workflows/agent-teams-quick-start.md) | Quick start guide for agent team patterns |
| [workflows/agentic-software-factories.md](./workflows/agentic-software-factories.md) | Orientation map: from a single session to a software factory, and when a closed platform actually wins |
| [workflows/dual-instance-planning.md](./workflows/dual-instance-planning.md) | Dual-instance planning: Opus plans, Sonnet executes |
| [workflows/event-driven-agents.md](./workflows/event-driven-agents.md) | Event-driven agent coordination patterns |
| [workflows/support-csm-agent.md](./workflows/support-csm-agent.md) | Internal support/CSM agent: ticket triage, DB diagnosis, CRM via MCP |
| [workflows/plan-pipeline.md](./workflows/plan-pipeline.md) | End-to-end plan pipeline: start, validate, execute |
| [workflows/design-to-code.md](./workflows/design-to-code.md) | Convert Figma/wireframes to working code |
| [workflows/exploration-workflow.md](./workflows/exploration-workflow.md) | Systematically explore unfamiliar codebases |
| [workflows/pdf-generation.md](./workflows/pdf-generation.md) | Generate professional PDFs with Quarto/Typst |
| [workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md) | Master rg, grepai, Serena, ast-grep combined workflows |
| [workflows/skeleton-projects.md](./workflows/skeleton-projects.md) | Use battle-tested repos as scaffolding for new projects |
| [workflows/talk-pipeline.md](./workflows/talk-pipeline.md) | 6-stage talk preparation: raw material to slides |
| [workflows/team-ai-instructions.md](./workflows/team-ai-instructions.md) | Scale CLAUDE.md across multi-developer teams |

---

## Cowork Documentation

For knowledge workers using Claude Cowork (agentic desktop):

| Resource | Description |
|----------|-------------|
| **[Cowork Hub](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/README.md)** | Complete Cowork documentation |
| [Getting Started](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/01-getting-started.md) | Setup and first workflow |
| [Capabilities](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/02-capabilities.md) | What Cowork can/cannot do |
| [Security Guide](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/03-security.md) | Safe usage practices |
| [Prompt Library](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/prompts) | 50+ ready-to-use prompts |
| [Cheatsheet](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/cheatsheet.md) | 1-page quick reference |

---

## Recommended Reading Order

1. **New users**: Start with Quick Start section in `ultimate-guide.md`
2. **Daily reference**: Print `cheatsheet.md`
3. **Team leads**: Read `roles/adoption-approaches.md` for rollout strategies
4. **Security focus**: `security/security-hardening.md` then `security/sandbox-isolation.md`
5. **Deep architecture**: `core/architecture.md` then `diagrams/`

---

*Back to [main README](../README.md)*
