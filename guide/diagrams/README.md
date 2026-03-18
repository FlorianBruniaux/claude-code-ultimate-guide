---
title: "Claude Code — Visual Diagrams"
description: "48 Mermaid interactive diagrams covering all major Claude Code concepts"
tags: [reference, architecture, diagrams, mermaid]
---

# Claude Code — Visual Diagrams

48 interactive Mermaid diagrams organized in 10 thematic files. Each diagram includes a Mermaid version (rendered natively on GitHub) and an ASCII fallback.

> For ASCII-only diagrams and a printable visual reference → [visual-reference.md](../core/visual-reference.md)

---

## Visual Palette

All diagrams use the consistent Bold Guy palette:

| Color | Hex | Usage |
|-------|-----|-------|
| Warm Beige | `#F5E6D3` | User actions, input nodes |
| Orange Brûlé | `#E87E2F` | Key decisions, Claude actions |
| Soft Green | `#7BC47F` | Success paths, recommendations |
| Alert Red | `#E85D5D` | Danger, anti-patterns, risks |
| Neutral Gray | `#B8B8B8` | Infrastructure, passive elements |
| Light Blue | `#6DB3F2` | Information, documentation refs |

## Mermaid Conventions

| Shape | Syntax | Meaning |
|-------|--------|---------|
| Rounded rect | `(text)` | Process step, action |
| Diamond | `{text}` | Decision point |
| Stadium | `([text])` | Start / End terminal |
| Hexagon | `{{text}}` | External system or API |
| Subroutine | `[[text]]` | Internal Claude Code component |
| Cylinder | `[(text)]` | Data store, persistent state |

---

## Navigation

| File | Diagrams | Topics |
|------|----------|--------|
| [01-foundations.md](./01-foundations.md) | 4 | 4-layer model, workflow pipeline, decision tree, permission modes |
| [02-context-and-sessions.md](./02-context-and-sessions.md) | 4 | Context zones, memory hierarchy, session teleportation, fresh context |
| [03-configuration-system.md](./03-configuration-system.md) | 4 | Config precedence, skills vs commands vs agents, agent lifecycle, hooks |
| [04-architecture-internals.md](./04-architecture-internals.md) | 4 | Master loop, tool categories, system prompt assembly, sub-agent isolation |
| [05-mcp-ecosystem.md](./05-mcp-ecosystem.md) | 4 | MCP ecosystem map, MCP architecture, rug pull attack, config hierarchy |
| [06-development-workflows.md](./06-development-workflows.md) | 5 | TDD cycle, spec-first pipeline, plan-driven, iterative refinement, AI fluency paths |
| [07-multi-agent-patterns.md](./07-multi-agent-patterns.md) | 5 | Agent topologies, worktrees, dual-instance, horizontal scaling, decision matrix |
| [08-security-and-production.md](./08-security-and-production.md) | 4 | 3-layer defense, sandbox decision, verification paradox, CI/CD pipeline |
| [09-cost-and-optimization.md](./09-cost-and-optimization.md) | 4 | Model selection, cost optimization, subscription tiers, token reduction |
| [10-adoption-and-learning.md](./10-adoption-and-learning.md) | 3 | Onboarding paths, UVAL protocol, trust calibration |
| [11-context-engineering.md](./11-context-engineering.md) | 4 | 3-layer context system, adherence degradation, modular architecture, rule placement |
| [12-enterprise-governance.md](./12-enterprise-governance.md) | 3 | Governance risk tiers, MCP approval workflow, data classification |
| **Total** | **48** | |

---

## Navigate by Use Case

### "I'm new to Claude Code — where do I start?"
1. [Quick Decision Tree](./01-foundations.md#quick-decision-tree) — Should I use Claude Code?
2. [9-Step Workflow Pipeline](./01-foundations.md#9-step-workflow-pipeline) — How does it work?
3. [Permission Modes](./01-foundations.md#permission-modes-comparison) — What are the safety modes?
4. [Onboarding Paths](./10-adoption-and-learning.md#onboarding-adaptive-learning-paths) — Which path fits me?

### "I want to understand the architecture"
1. [The Master Loop](./04-architecture-internals.md#the-master-loop) — Core execution engine
2. [System Prompt Assembly](./04-architecture-internals.md#system-prompt-assembly) — How context is built
3. [4-Layer Context System](./01-foundations.md#chatbot-to-context-system-4-layer-model) — The transformation model
4. [Tool Categories](./04-architecture-internals.md#tool-categories) — What tools are available

### "I'm worried about security"
1. [MCP Rug Pull Attack](./05-mcp-ecosystem.md#mcp-rug-pull-attack-chain) — The main threat vector
2. [3-Layer Defense](./08-security-and-production.md#security-3-layer-defense) — How to protect yourself
3. [Sandbox Decision Tree](./08-security-and-production.md#sandbox-decision-tree) — When to sandbox
4. [Verification Paradox](./08-security-and-production.md#the-verification-paradox) — Don't trust Claude to verify itself

### "I want to reduce my token costs"
1. [Model Selection Decision Flow](./09-cost-and-optimization.md#model-selection-decision-flow) — Pick the right model
2. [Cost Optimization Tree](./09-cost-and-optimization.md#cost-optimization-decision-tree) — Systematic cost reduction
3. [Token Reduction Pipeline](./09-cost-and-optimization.md#token-reduction-strategies-pipeline) — RTK + session hygiene
4. [Context Management Zones](./02-context-and-sessions.md#context-management-zones) — Manage context size

### "I want to use multiple agents"
1. [Agent Teams Topology](./07-multi-agent-patterns.md#agent-teams-topology-3-patterns) — 3 orchestration patterns
2. [Multi-Instance Decision Matrix](./07-multi-agent-patterns.md#multi-instance-decision-matrix) — Which pattern to use?
3. [Git Worktree Multi-Instance](./07-multi-agent-patterns.md#git-worktree-multi-instance-pattern) — Parallel isolation
4. [Sub-Agent Context Isolation](./04-architecture-internals.md#sub-agent-context-isolation) — How agents are isolated

### "I want to set up MCP servers"
1. [MCP Ecosystem Map](./05-mcp-ecosystem.md#mcp-server-ecosystem-map) — What servers exist
2. [MCP Architecture](./05-mcp-ecosystem.md#mcp-architecture-client-server) — How it works
3. [MCP Config Hierarchy](./05-mcp-ecosystem.md#mcp-config-hierarchy) — Where configs live

### "I want to govern Claude Code across my team"
1. [Governance Risk Tiers](./12-enterprise-governance.md#governance-risk-tiers) — Which control level fits your context?
2. [MCP Governance Workflow](./12-enterprise-governance.md#mcp-governance-workflow) — Approval pipeline for MCP servers
3. [Data Classification Rules](./12-enterprise-governance.md#data-classification--claude-code-access-rules) — What Claude can and cannot access

### "I want to improve Claude's context adherence"
1. [Rule Placement Decision Tree](./11-context-engineering.md#rule-placement-decision-tree) — Where does this rule go?
2. [3-Layer Context System](./11-context-engineering.md#the-3-layer-context-system) — Global / Project / Session
3. [Context Budget & Adherence](./11-context-engineering.md#context-budget--adherence-degradation) — Why rules stop being followed
4. [Modular Architecture](./11-context-engineering.md#monolithic-vs-modular-architecture) — Path-scoping as the fix

---

*Back to [guide/README.md](../README.md) | ASCII diagrams → [visual-reference.md](../core/visual-reference.md)*
