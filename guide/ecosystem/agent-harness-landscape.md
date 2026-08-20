---
title: "Agent Harness Comparison"
description: "What an agent harness is, and a single comparison table across CLI, IDE, and cloud coding agents, spanning open source, source-available, and proprietary tools, plus the frameworks, SDKs, sandboxes, and protocols people mistake for harnesses."
tags: [agents, harness, comparison, opencode, gemini-cli, crush, deepseek-harness, cline, roo-code, kilo-code, openhands, goose, aider, swe-agent, devin]
---

# Agent Harness Comparison

An **agent harness** is the runtime built around a model that turns raw text generation into something that can act on a codebase: the tool definitions the model can call, the context fed into each turn, the permission layer that gates a given action, the loop that executes a tool call and feeds the result back in, the memory that survives past one session, and the recovery path when a session or a tool call fails mid-task. The model writes text. The harness decides what that text is allowed to do, and what happens next.

The framing is not invented for this page. Simon Willison has argued on his blog that the useful definition of an agent is a system that runs tools in a loop against a goal, deciding the next action from each result, rather than a specific product category. The SWE-agent paper (Yang et al., Princeton, presented at NeurIPS 2024) formalized a narrower version of the same idea for coding specifically: the **agent-computer interface**, the layer of commands and observations a coding agent needs between itself and a real repository to act reliably instead of guessing at raw shell output.

That framing cuts across how this guide is already organized. [Agent Tools: Beyond Claude Code](./agentic-tools.md) profiles the CLI harnesses in depth, one section per tool. [AI Ecosystem §6](./ai-ecosystem.md#section-6) covers IDE-embedded agents from a hybrid-workflow angle: when to reach for Cursor or Windsurf alongside Claude Code, not just what they are. Neither page tries to put every harness, across every interface, in one table. This page does that instead.

This page answers *which* harness. [Agent Harness Engineering](../core/agent-harness.md) answers *what's inside one*: the nine components a harness needs (while-loop engine, context management, tool registry, permission enforcement, and more), the lethal-trifecta security model, and the CI/CD and observability patterns that come with running one in production. Read that page for the internals, this one for the field.

---

## Core Coding Harnesses

Twenty-five harnesses, from CLI-only open source projects to IDE-embedded proprietary products to cloud-only autonomous agents. Entries with a full profile elsewhere in this guide link to it rather than repeating it here.

| Harness | Vendor/Steward | Interface | Models | Openness | Positioning |
|---------|-----------------|-----------|--------|----------|--------------|
| Claude Code | Anthropic | CLI/IDE/Desktop/Cloud | Claude models | Proprietary | Anthropic's reference harness: deep hooks, skills, subagents, plugins |
| Codex | OpenAI | CLI/IDE/Desktop/Cloud | OpenAI + compatible | Apache-2.0 CLI, backing services proprietary | Sandboxed execution as the default posture, AGENTS.md, skills, MCP |
| [Gemini CLI](./agentic-tools.md#16-gemini-cli-google) | Google | CLI | Gemini | Apache-2.0 | Official Google harness, generous free tier, GEMINI.md by default |
| DeepSeek Harness (dsh) | DeepSeek | Local web UI + headless | DeepSeek + multi-provider (Anthropic, OpenAI, Azure, Bedrock, Vertex, custom endpoints) | MIT | "Everything is a plugin" architecture on the Cordis framework; developer preview, not production-ready |
| Qwen Code | Alibaba/Qwen | CLI | Qwen + compatible | Apache-2.0 | Gemini CLI fork retuned for open-weight Qwen models |
| Cline | Cline | VS Code extension + CLI | Multi-provider | Apache-2.0 | Plan/act loop with per-step human approval and cost transparency |
| Roo Code | Community fork | VS Code/Cursor | Multi-provider | Apache-2.0 | Cline lineage, custom modes, strong MCP story; the upstream repo was reported archived as of the last check against the source catalog behind this table, confirm current status before depending on it |
| Kilo Code | Kilo-Org | VS Code + CLI | Multi-provider | Source-available | Cline/Roo Code lineage descendant with a provider and tool marketplace |
| [opencode](./agentic-tools.md#15-opencode-anomaly-formerly-sst) | Anomaly (formerly SST) | CLI, client/server | 75+ providers, including local models | MIT | Highest star count in this category; the agent runs as a server a terminal, IDE, or another machine connects to |
| [OpenHands](./agentic-tools.md#24-openhands-all-hands-ai) | All Hands AI | Web/CLI/Docker/Cloud | Multi-provider | Open core, Cloud/Enterprise paid | Dependency-graph parallel execution, Docker sandbox, browser tool |
| [Goose](./agentic-tools.md#14-goose-aaifblock) | Block/AAIF (Linux Foundation) | CLI + Desktop | Multi-provider | Apache-2.0 | MCP + ACP extensions, reusable recipes, a different model per subagent |
| [Aider](./agentic-tools.md#13-aider) | Aider-AI | CLI | Multi-provider | Apache-2.0 | Git-native precise editing, the original terminal pair programmer; release cadence has slowed |
| [SWE-agent](./agentic-tools.md#22-swe-agent-princeton) | Princeton | CLI/runtime | Multi-provider | MIT | Autonomous issue resolution, research and benchmark-oriented |
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

The DeepSeek Harness entry deserves one more caveat, since its architecture is more interesting than its current maturity. It runs on Node ^22.19.0 or >=24, ships four preset modes (Standard, PTC/Code Mode where the model writes a TypeScript program that composes tool calls in a worker thread, Minimal for benchmarks, and Cordis/Creation for plugin experimentation), and logs every message, tool call, and permission decision for full session replay. Its approval system fails closed and logs every decision, but as of this writing it offers no "always allow" rule and no remembered-permissions store, and the approval prompt shows a tool name and reason without the full arguments, a real gap when deciding whether to trust a call. Independent research from Tencent (arXiv 2608.16393) ran 14,560 controlled prompt-injection tests against the live runtime paired with DeepSeek V4 Flash on one commit and configuration, and measured an overall success rate around 5.3-5.6%, rising to 17% for fake-completion text attacks, 25.5% for hidden Unicode payloads in files, and 16% through the Skills file channel. The finding worth carrying forward is not the specific percentages, which will move as the harness matures, it is that sandboxing alone did not close these channels, and provenance tracking plus independent action authorization still mattered on top of it. Telemetry defaults to off; its optional FULL mode can export complete session event copies with no built-in redaction, a real data-handling caveat for anyone who enables it. Never run its `danger-full-access` sandbox preset on a primary machine.

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
