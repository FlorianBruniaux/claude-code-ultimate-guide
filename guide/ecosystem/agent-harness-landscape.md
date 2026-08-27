---
title: "Agent Harness Comparison"
description: "What an agent harness is, and a single comparison table across CLI, IDE, and cloud coding agents, spanning open source, source-available, and proprietary tools, plus the frameworks, SDKs, sandboxes, and protocols people mistake for harnesses."
tags: [agents, harness, comparison, opencode, gemini-cli, kimi-code, pi, oh-my-pi, crush, deepseek-harness, cline, roo-code, kilo-code, openhands, goose, aider, swe-agent, devin]
---

# Agent Harness Comparison

An **agent harness** is the runtime built around a model that turns raw text generation into something that can act on a codebase: the tool definitions the model can call, the context fed into each turn, the permission layer that gates a given action, the loop that executes a tool call and feeds the result back in, the memory that survives past one session, and the recovery path when a session or a tool call fails mid-task. The model writes text. The harness decides what that text is allowed to do, and what happens next.

The framing is not invented for this page. Simon Willison has argued on his blog that the useful definition of an agent is a system that runs tools in a loop against a goal, deciding the next action from each result, rather than a specific product category. The SWE-agent paper (Yang et al., Princeton, presented at NeurIPS 2024) formalized a narrower version of the same idea for coding specifically: the **agent-computer interface**, the layer of commands and observations a coding agent needs between itself and a real repository to act reliably instead of guessing at raw shell output.

That framing cuts across how this guide is already organized. [Agent Tools: Beyond Claude Code](./agentic-tools.md) profiles the CLI harnesses in depth, one section per tool. [AI Ecosystem §6](./ai-ecosystem.md#section-6) covers IDE-embedded agents from a hybrid-workflow angle: when to reach for Cursor or Windsurf alongside Claude Code, not just what they are. Neither page tries to put every harness, across every interface, in one table. This page does that instead.

This page answers *which* harness. [Agent Harness Engineering](../core/agent-harness.md) answers *what's inside one*: the nine components a harness needs (while-loop engine, context management, tool registry, permission enforcement, and more), the lethal-trifecta security model, and the CI/CD and observability patterns that come with running one in production. Read that page for the internals, this one for the field.

> **Scope and verification**: this is a curated landscape, not a directory of every project calling itself an agent. The table includes products that own a coding-agent loop, then separates products that coordinate those loops. The eight rows added in this update were checked against their official repositories on **2026-08-27**; interface, licence, and activity can change after that snapshot.

---

## Core Coding Harnesses

Thirty-three harnesses, from CLI-only open source projects to IDE-embedded proprietary products to cloud-only autonomous agents. Entries with a full profile elsewhere in this guide link to it rather than repeating it here.

| Harness | Vendor/Steward | Interface | Models | Openness | Positioning |
|---------|-----------------|-----------|--------|----------|--------------|
| Claude Code | Anthropic | CLI/IDE/Desktop/Cloud | Claude models | Proprietary | Anthropic's reference harness: deep hooks, skills, subagents, plugins |
| Codex | OpenAI | CLI/IDE/Desktop/Cloud | OpenAI + compatible | Apache-2.0 CLI, backing services proprietary | Sandboxed execution as the default posture, AGENTS.md, skills, MCP |
| [Gemini CLI](./agentic-tools.md#16-gemini-cli-google) | Google | CLI | Gemini | Apache-2.0 | Official Google harness, generous free tier, GEMINI.md by default |
| [DeepSeek Harness (dsh)](./agentic-tools.md#18-deepseek-harness-dsh) | DeepSeek | Local web UI + headless | DeepSeek + multi-provider (Anthropic, OpenAI, Azure, Bedrock, Vertex, custom endpoints) | MIT | "Everything is a plugin" architecture on the Cordis framework; developer preview, not production-ready |
| Qwen Code | Alibaba/Qwen | CLI | Qwen + compatible | Apache-2.0 | Gemini CLI fork retuned for open-weight Qwen models |
| [Kimi Code CLI](https://github.com/MoonshotAI/kimi-code) | Moonshot AI | CLI + ACP | Kimi + configured providers | MIT | Extensible terminal coding agent with ACP integration |
| Cline | Cline | VS Code extension + CLI | Multi-provider | Apache-2.0 | Plan/act loop with per-step human approval and cost transparency |
| Roo Code | Community fork | VS Code/Cursor | Multi-provider | Apache-2.0 | Cline lineage, custom modes, strong MCP story; the upstream repo was reported archived as of the last check against the source catalog behind this table, confirm current status before depending on it |
| Kilo Code | Kilo-Org | VS Code + CLI | Multi-provider | Source-available | Cline/Roo Code lineage descendant with a provider and tool marketplace |
| [opencode](./agentic-tools.md#15-opencode-anomaly-formerly-sst) | Anomaly (formerly SST) | CLI, client/server | 75+ providers, including local models | MIT | Highest star count in this category; the agent runs as a server a terminal, IDE, or another machine connects to |
| [Pi](https://github.com/earendil-works/pi) | Community | CLI/TUI + SDK | Multi-provider | MIT | Minimal, extensible coding runtime for users who want to compose their own workflow |
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | Community | CLI/TUI | Multi-provider | MIT | Pi-derived power-user runtime with editor, browser, and debugger integrations |
| [OpenHands](./agentic-tools.md#24-openhands-all-hands-ai) | All Hands AI | Web/CLI/Docker/Cloud | Multi-provider | Open core, Cloud/Enterprise paid | Dependency-graph parallel execution, Docker sandbox, browser tool |
| [Goose](./agentic-tools.md#14-goose-aaifblock) | Block/AAIF (Linux Foundation) | CLI + Desktop | Multi-provider | Apache-2.0 | MCP + ACP extensions, reusable recipes, a different model per subagent |
| [Aider](./agentic-tools.md#13-aider) | Aider-AI | CLI | Multi-provider | Apache-2.0 | Git-native precise editing, the original terminal pair programmer; release cadence has slowed |
| [Open Interpreter](https://github.com/openinterpreter/openinterpreter) | Open Interpreter | CLI | Multi-provider | Apache-2.0 | General-purpose local execution agent that can also work against codebases |
| [crush](./agentic-tools.md#17-crush-charm) | Charm | CLI/TUI | Multi-provider | Source-available; see its licence | Terminal coding agent with per-project session persistence |
| [SWE-agent](./agentic-tools.md#22-swe-agent-princeton) | Princeton | CLI/runtime | Multi-provider | MIT | Autonomous issue resolution, research and benchmark-oriented |
| [Open SWE](https://github.com/langchain-ai/open-swe) | LangChain | GitHub/Linear/Slack + cloud | Multi-provider | MIT | Asynchronous coding-agent workflow designed for task systems and pull requests |
| [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | Community | CLI/TUI | DeepSeek-focused | MIT | Experimental terminal harness oriented around DeepSeek prefix-cache efficiency |
| [claw-code-agent](https://github.com/HarnessLab/claw-code-agent) | HarnessLab | CLI + local API | Configured providers | License not declared in GitHub metadata | Experimental Python implementation inspired by Claude Code's harness architecture |
| Cursor Agent | Cursor | IDE/CLI/Cloud | Multi-model | Proprietary | IDE-first agent with CLI and cloud execution modes; see [AI Ecosystem §6](./ai-ecosystem.md#section-6) for Claude Code hybrid-workflow guidance |
| Windsurf Cascade | Windsurf (Cognition) | IDE | Multi-model | Proprietary | IDE-first agent built around a persistent "Cascade" flow; see [AI Ecosystem §6](./ai-ecosystem.md#section-6) |
| Kiro | Amazon | IDE | Multi-model, Bedrock-backed | Proprietary | Spec-driven IDE agent that produces requirements and design docs before code |
| GitHub Copilot CLI | GitHub/Microsoft | CLI | Multi-model via Copilot | Proprietary | Terminal front end for Copilot's agent mode, tied to a Copilot subscription |
| Amp | Sourcegraph | CLI/IDE | Multi-model | Proprietary | Sourcegraph's agentic coding tool, built on the company's code-search background |
| Factory Droid | Factory | CLI/Cloud | Multi-model | Proprietary | "Droids" run coding and ops tasks, aimed at enterprise workflow automation |
| Warp (Agent Mode) | Warp | Terminal app | Multi-model | Proprietary | Agent mode built into the Warp terminal itself, not a separate CLI install |
| Jules | Google | Cloud, asynchronous | Gemini | Proprietary | Works in the background on a cloned repo and opens a pull request when done |
| Devin | Cognition | Web/Cloud | Proprietary model routing | Proprietary | Autonomous agent operating in a remote development environment, one of the earliest "AI software engineer" products |
| Replit Agent | Replit | Cloud IDE | Multi-model | Proprietary | Agent embedded in Replit's browser-based IDE; builds and deploys inside the same environment |
| Augment Code | Augment | IDE/CLI | Multi-model | Proprietary | Context-engine-focused coding agent aimed at large, existing codebases |
| Junie | JetBrains | IDE | Multi-model | Proprietary | JetBrains' agent embedded across its IDE family (IntelliJ, PyCharm, and others) |

**Proprietary and commercial entries above (Cursor Agent, Windsurf Cascade, Kiro, GitHub Copilot CLI, Amp, Factory Droid, Warp, Jules, Devin, Replit Agent, Augment Code, Junie): positioning only, not independently verified against vendor documentation in this pass.** Flag any inaccuracy for correction rather than treating these one-liners as current specifications.

DeepSeek Harness needs a maturity caveat. It is still a developer preview, and the project's sandbox and approval settings should be treated as part of the threat model, not as proof that an untrusted repository is safe. The architecture and the narrow external prompt-injection study previously summarized here now live in [DeepSeek Harness (dsh)](./agentic-tools.md#18-deepseek-harness-dsh), where the operational caveats can be read without making this comparison table a product manual.

---

## Orchestrators: Products Above the Runtime

The following products coordinate tasks, isolated workspaces, or multiple agent sessions. They are useful when the problem is a queue or a fleet. They are **not** counted in the thirty-three runtime harnesses above unless they also provide their own agent loop.

| Orchestrator | Role above the runtime | Openness | Snapshot source |
|--------------|------------------------|----------|-----------------|
| [Symphony](https://github.com/openai/symphony) | Coordinates multiple coding-agent runs and their outputs | Apache-2.0 | Official repository, 2026-08-27 |
| [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) | Task board and execution surface for parallel coding-agent work | Apache-2.0 | Official repository, 2026-08-27; check activity before adopting |
| [AgentBox](https://github.com/madarco/agentbox) | Gives individual agents isolated VM workspaces | MIT | Official repository, 2026-08-27 |
| [Proliferate](https://github.com/proliferate-ai/proliferate) | Runs multiple coding-agent sessions in parallel | AGPL-3.0 | Official repository, 2026-08-27 |
| [Eigent](https://github.com/eigent-ai/eigent) | Self-hosted multi-agent workspace | Apache-2.0 | Official repository, 2026-08-27 |
| [cc-haha](https://github.com/NanmiCoder/cc-haha) | Manages parallel Claude Code sessions and worktrees | MIT | Official repository, 2026-08-27 |
| [OpenAgents](https://github.com/openagents-org/openagents) | Connects coding agents to persistent shared workspaces | Apache-2.0 | Official repository, 2026-08-27 |

Use an orchestrator only after a single runtime harness is no longer the bottleneck. Parallel agents amplify both throughput and bad assumptions; each task still needs isolated scope, verification, and review.

---

## What's Not a Full Harness

These show up in the same conversations as coding agents, and none of them run a coding loop on their own. Worth naming so the boundary stays clear.

| Category | Examples | Why it's not a harness |
|----------|----------|--------------------------|
| Agent frameworks | LangGraph, CrewAI, AutoGen, PydanticAI, Agno, Mastra | Libraries for building an agent loop, not a ready-to-run one |
| Agent SDKs | Claude Agent SDK, OpenAI Agents SDK, Google ADK | Programmatic building blocks; Claude Code itself is built on the Claude Agent SDK |
| Sandboxes | E2B, Daytona, Modal | Execution isolation a harness calls into, not a harness itself |
| Memory layers | Mem0, Graphiti, Letta Memory | Persistent storage a harness can plug into, not the loop that decides what to remember |
| Observability | Langfuse, LangSmith, Braintrust, Phoenix | Watches a harness run; runs nothing on its own |
| Protocols | MCP, ACP, A2A | The wiring standard between a harness and its tools, or between two agents, not the harness |
| Models | Claude, GPT, Gemini, DeepSeek, Qwen, Kimi | The engine, not the vehicle: the same model behaves differently depending on which harness drives it |

---

## The Practical Read

Pick the lowest tier of complexity that solves the job in front of you. A single CLI harness answers most day-to-day coding work; reach for an orchestrator managing a fleet of harnesses only once a fleet is actually the problem, not before. For the CLI tools that have a full profile in this guide (Codex, Hermes Agent, Aider, Goose, opencode, Gemini CLI, crush, plus the autonomous tools in Section 2), see [Agent Tools: Beyond Claude Code](./agentic-tools.md). For guidance on running Claude Code alongside an IDE-embedded agent rather than choosing one exclusively, see [AI Ecosystem §6](./ai-ecosystem.md#section-6).
