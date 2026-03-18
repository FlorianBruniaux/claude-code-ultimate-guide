---
title: "Guide Documentation"
description: "Index of all core documentation files for mastering Claude Code"
tags: [guide, reference]
---

# Guide Documentation

Core documentation for mastering Claude Code, organized by topic.

---

## Core Reference

| File | Description | Time |
|------|-------------|------|
| [ultimate-guide.md](./ultimate-guide.md) | Complete reference covering all Claude Code features | ~3 hours |
| [cheatsheet.md](./cheatsheet.md) | 1-page printable quick reference | 5 min |
| [core/architecture.md](./core/architecture.md) | How Claude Code works internally (master loop, tools, context) | 25 min |
| [core/methodologies.md](./core/methodologies.md) | 15 development methodologies reference (TDD, SDD, BDD, etc.) | 20 min |
| [core/visual-reference.md](./core/visual-reference.md) | Visual cheatsheet — ASCII diagrams for key concepts | 5 min |
| [core/claude-code-releases.md](./core/claude-code-releases.md) | Official release history (condensed) | 10 min |
| [core/known-issues.md](./core/known-issues.md) | **Critical bugs tracker**: security issues, token consumption, verified community reports | 15 min |
| [core/context-engineering.md](./core/context-engineering.md) | **Context Engineering**: token budget, modular architecture, team assembly, ACE pipeline, quality measurement | 25 min |
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
| [ecosystem/mcp-servers-ecosystem.md](./ecosystem/mcp-servers-ecosystem.md) | **Community MCP servers**: 8 validated servers (Playwright, Semgrep, Kubernetes, etc.) with production configs | 25 min |
| [ecosystem/third-party-tools.md](./ecosystem/third-party-tools.md) | **Community tools**: GUIs, TUIs, config managers, token trackers, alternative UIs | 15 min |
| [ecosystem/remarkable-ai.md](./ecosystem/remarkable-ai.md) | Remarkable AI usage patterns and power-user techniques | 10 min |

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
| [workflows/dual-instance-planning.md](./workflows/dual-instance-planning.md) | Dual-instance planning: Opus plans, Sonnet executes |
| [workflows/event-driven-agents.md](./workflows/event-driven-agents.md) | Event-driven agent coordination patterns |
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
