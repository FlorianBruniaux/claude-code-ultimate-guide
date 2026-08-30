---
title: "Code as Agent Harness (arXiv 2605.18747): Agent Harness Engineering"
description: "An evidence-backed guide to agent harness engineering: runtime loops, context, tools, state, permissions, verification, observability, and automated harness optimization."
tags: [guide, agents, architecture, security, observability]
keywords:
  - "code as agent harness arxiv 2605.18747"
  - "agent harness"
  - "agent harness engineering"
  - "what is an agent harness"
  - "meta harness"
  - "harness optimizer"
  - "2605.18747"
---

# Agent Harness Engineering

> **Confidence**: Tier 1 for the architecture framing; Tier 2 for cross-product performance claims. Controlled studies show measurable harness effects, but do not establish that the harness always matters more than the model.
>
> **Reading time**: ~35 minutes

---

## The core claim

A raw LLM is not an agent. It becomes one when connected to a harness. The useful unit of evaluation is therefore the **model-harness pair**, not either component in isolation.

The 2026 [Agent System and Harness Design survey](https://arxiv.org/abs/2606.20683) decomposes an execution harness into observation, context, control, action, state, and verification. [Code as Agent Harness](https://arxiv.org/abs/2605.18747) adds a code-centric view: code is not only an output but the executable substrate for tools, memory, control, coordination, and verification. These are useful taxonomies, not performance proofs.

Controlled evidence supports a narrower claim. In [The Scaffold Effect in Coding Agents](https://arxiv.org/abs/2607.22585), two fixed models were tested across three harnesses on 50 Terminal-Bench Pro tasks. Harness choice changed tokens per solved task by up to 40 times, while paired pass-rate differences stayed within 0 to 8 percentage points and were mostly not statistically significant. The harness can dominate cost and failure behavior without dominating task accuracy. Conversely, model quality or model-harness compatibility can remain the binding constraint. Report the pair, the task set, and the budget.

This page uses **agent harness** in its runtime sense: the system that owns the agent loop, tools, context, state, and permissions. A repository can also provide a **repository harness** around that runtime: its instructions, setup, task state, and verification gates. The distinction matters because a project can improve its repository harness without replacing Claude Code, and a team can switch runtime harnesses without discarding every project practice.

This page covers what is inside the runtime. For the repository layer, see [Repository Harness Engineering](../ultimate-guide.md#925-harness-engineering). For feedback loops, executable workflow graphs, stopping rules, and judgment boundaries, use [Loop & Graph Engineering](./loop-graph-engineering.md). For a dated comparison of specific products across CLI, IDE, and cloud, see the [Agent Harness Landscape](../ecosystem/agent-harness-landscape.md).

![A user goal moves through six harness stages: context building, LLM reasoning, policy gating, guarded tool execution, verification, and an accepted result. Observability spans every stage, constraints govern policy and runtime, and feedback returns accepted results to the context builder.](../images/agent-harness-reliability-loop.webp)

*The LLM is one stage in the reliability loop. Context, policy, guarded execution, verification, observability, constraints, and feedback determine whether the model's proposal becomes an accepted result.*

### Choose the right entry point

| Question | Canonical page |
|---|---|
| What does a runtime harness contain, and how do its controls work? | This [Agent Harness Engineering](./agent-harness.md) page |
| How should loops, workflow graphs, state transitions, stopping rules, and judgment be designed? | [Loop & Graph Engineering](./loop-graph-engineering.md) |
| Which runtime, orchestrator, framework, or adjacent project should I compare? | [Agent Harness Landscape](../ecosystem/agent-harness-landscape.md) |
| What does a specific coding-agent product support? | [Agent Tools: Beyond Claude Code](../ecosystem/agentic-tools.md) |
| What distinguishes a runtime, repository, evaluation harness, and orchestrator? | [Glossary](./glossary.md) |
| Which Claude Code release introduced a behavior? | [Claude Code Releases](./claude-code-releases.md) and its [machine-readable history](../../machine-readable/claude-code-releases.yaml) |

The pages remain separate on purpose. Engineering concepts change more slowly than product inventories, licences, feature evidence, and popularity signals. Combining both would make the architectural reference inherit the catalog's dated snapshot and maintenance cycle.

---

## Table of Contents

0. [Four Layers, Four Responsibilities](#0-four-layers-four-responsibilities)
1. [Three Foundational Properties](#1-three-foundational-properties)
2. [The Nine Components](#2-the-nine-components)
3. [The Lethal Trifecta: Security Model](#3-the-lethal-trifecta-security-model)
4. [CI/CD Agentic Patterns](#4-cicd-agentic-patterns)
5. [Digital Twin Testing](#5-digital-twin-testing)
6. [Observability Stack](#6-observability-stack)
7. [Test Distribution and Component-Stacking Anti-patterns](#7-test-distribution-and-component-stacking-anti-patterns)
8. [Creator-Verifier Pattern](#8-creator-verifier-pattern)
9. [Reference Architecture](#9-reference-architecture)
10. [Practitioner Video Evidence](#10-practitioner-video-evidence)
11. [Harness Optimizers and Meta-Harnesses](#11-harness-optimizers-and-meta-harnesses)

---

## 0. Four Layers, Four Responsibilities

The word *harness* is overloaded. This guide uses four layers so a model, a runtime, a repository setup, and a fleet manager are not treated as interchangeable products.

| Layer | Responsibility | Examples | What it does not replace |
|-------|----------------|----------|--------------------------|
| **Model** | Generates and reasons over tokens | Claude, GPT, Gemini, DeepSeek, Qwen | Tools, policy, durable state, or execution |
| **Runtime harness** | Runs the agent loop and mediates tool use, context, permissions, and recovery | Claude Code, Codex, Gemini CLI, DeepSeek Harness, OpenCode | Project-specific instructions and delivery gates |
| **Repository harness** | Makes one codebase legible and verifiable to a runtime | `CLAUDE.md`/`AGENTS.md`, `init.sh`, lockfiles, task state, tests; Liza's installed contracts and guardrails | The runtime's model routing, tool loop, or sandbox |
| **Orchestrator** | Coordinates multiple runs, workspaces, or harnesses | Symphony, Vibe Kanban, AgentBox, Proliferate, Liza | The underlying runtime agent loop |

The boundary is practical. If a product can only schedule or inspect Claude Code and Codex sessions, it is an orchestrator. If it supplies an iterative model-and-tools loop itself, it is a runtime harness. If it is committed with the repository and tells any compatible runtime how to work safely, it is a repository harness.

A product can span two layers without owning all four. [Liza](https://github.com/liza-mas/liza) installs behavioral contracts, skills, settings, and guardrails into a repository, then coordinates external coding-agent CLIs through worktrees, durable task state, leases, doer/reviewer roles, recovery, and merge gates. Claude Code, Codex, or another selected CLI still owns the inner tool loop. The [Landscape profile](../ecosystem/agent-harness-landscape.md#liza-a-repository-harness-and-control-plane-combined) records the pinned code evidence and security limits.

A **harness optimizer** or **meta-harness** sits outside those four operating layers. It proposes changes to a target harness, evaluates candidates, and promotes or rejects versions. It does not replace the runtime loop or the fleet orchestrator. It improves them under an explicit search and evaluation protocol.

### Loop, graph, harness, and orchestrator are different views

These terms answer different questions. Treating them as competing product categories hides the boundary that matters.

| View | Primary question | Core artifact |
|-------|------------------|---------------|
| **Loop engineering** | What feedback repeats, and what stops the repetition? | Goal, action, observation, verification, stopping rule |
| **Graph engineering** | Which nodes, edges, state transitions, joins, and checkpoints are executable? | Versioned workflow graph and shared state schema |
| **Harness engineering** | What context, tools, policy, state, verification, and recovery bound execution? | Runtime and repository controls |
| **Orchestration** | How are runs, workspaces, queues, budgets, and people coordinated? | Scheduler or control plane |

[Loop Engineering](https://addyo.substack.com/p/loop-engineering) is a useful practitioner label for replacing repeated manual prompts with a system that finds work, dispatches it, checks it, and decides what happens next. It is not a formal standard. [Graph Engineering in the Era of LLM Agents](https://arxiv.org/abs/2608.21156) and [What Makes Prompts a Graph](https://arxiv.org/abs/2607.27578) propose a broader graph-engineering vocabulary, but both are recent preprints. The mechanisms are older than the label: the official [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) already models shared state, nodes, fixed or conditional edges, and parallel super-steps, while its [persistence layer](https://docs.langchain.com/oss/python/langgraph/persistence) provides checkpoints, interruption, replay, and fault recovery.

A loop can be encoded as a graph. A graph can coordinate several loops. A harness can execute either while adding permissions, context, tools, verification, and recovery. An orchestrator can schedule several harnesses without owning their inner loops. Compare products inside the same layer before comparing feature counts.

---

## 1. Three Foundational Properties

arXiv 2605.18747 ("Code as Agent Harness", May 2026) formalizes three properties that distinguish a harness from a simple LLM wrapper:

**Executability**: the harness can verify what the agent actually did, not just what it said it would do. A harness that only logs prompts and completions is not executable, because it cannot distinguish a successful tool call from a hallucinated one.

**Inspectability**: when something fails, the harness produces actionable diagnostic output. Stack traces pointing to the prompt assembly step. Friction events tagged with which rules and skills were active. Token consumption by component. Without inspectability, debugging an agent failure requires reconstructing the session from logs, which is expensive and often incomplete.

**Statefulness**: the harness maintains continuity between sessions. Session state is externalized, not held in the model's context window. When the agent resumes after a context reset, it can reconstruct where it was without the human providing a full briefing. Anthropic's own telemetry shows the 99.9th percentile session duration passed 45 minutes in January 2026, up from 25 minutes in October 2025. At that length, statefulness is not optional.

---

## 2. The Nine Components

These nine components appear across Claude Code, Anthropic SDK, OpenAI Agents SDK, LangGraph, AWS Bedrock AgentCore, and Factory.ai Missions. No single tool implements all nine in exactly the same way, but the structure is consistent enough to use as an evaluation checklist when assessing a harness against a new tool or framework.

### 2.1 While-Loop Engine

The main loop: perceive (read context, tool outputs, latest user instruction), plan (call LLM with assembled prompt), act (execute tools). This is the heartbeat. Anthropic SDK, OpenAI Agents SDK, and LangGraph implement it differently (Anthropic is streaming-first, LangGraph is graph-based), but all three have this loop as the core abstraction.

Where problems emerge: loops that don't cap iterations, loops that don't handle LLM refusals or ambiguous tool calls, loops that let the context grow without summarization until they hit the window limit and abort.

#### Three loop horizons

A useful practitioner model separates three feedback horizons. The terms are not a formal standard, but they expose where a correction should become durable.

| Horizon | Boundary | Typical controls | Where it usually lives |
|---|---|---|---|
| **Inner loop** | One agent run | Tool results, targeted tests, skills, local checks | Runtime plus repository harness |
| **Outer loop** | Task or pull request | Agentic QA, full test suites, deeper review, independent verifiers | Repository harness plus CI |
| **Meta loop** | Across many runs | Failure mining, recurring review analysis, harness search, rule and verifier updates | Team process, optimizer, or meta-harness |

The [AI Native DevCon interview on harness engineering](https://www.youtube.com/watch?v=D_cw-k0F1DM&t=243s) describes the inner loop as fast feedback while the agent works, the [outer loop](https://www.youtube.com/watch?v=D_cw-k0F1DM&t=340s) as slower checks around the pull-request boundary, and the [meta loop](https://www.youtube.com/watch?v=D_cw-k0F1DM&t=427s) as continuous improvement across failures. This model turns repeated human correction into a maintenance signal. A review comment that recurs should become a test, rule, skill, hook, or verifier at the earliest loop that can catch it.

Build one bounded loop before adding autonomous layers. In a [2026 context-engineering interview](https://www.youtube.com/watch?v=Usufn8IQJgw&t=3112s), Dex Horthy describes a lights-off software factory that removed human testing and review, accumulated failures, and was shut down. That is a practitioner retrospective, not a controlled study, but it identifies a concrete failure mode: autonomy expanded faster than verification and recovery.

The meta loop can now be automated. [Meta-Harness](https://arxiv.org/abs/2603.28052) searches harness code using prior source, scores, and execution traces. [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850) represents editable components as files and couples every change to a prediction that the next evaluation can falsify. Automation does not remove the need for held-out tests or budgets. It makes those boundaries more important.

### 2.2 Context Management

What goes into the prompt on each loop iteration: conversation history, tool outputs, retrieved memory, current task state, rules from CLAUDE.md. The challenge is that context is finite and expensive. Strategies:

- **Compaction / summarization**: replace earlier turns with a compressed summary. Claude Code compacts automatically near its context threshold and also exposes `/compact` for an explicit compaction. `PreCompact` and `PostCompact` hooks let teams inspect or react to that boundary.
- **Sliding window**: keep the last N turns verbatim, summarize everything before.
- **Retrieval-augmented context**: retrieve relevant chunks from long-term storage rather than carrying everything in the window.

The ACE pipeline (see [context-engineering.md §6](./context-engineering.md#6-the-ace-pipeline)) is the Config-Persistence layer above context management: it governs what rules and skills are loaded across sessions.

[Agentic Context Engineering](https://arxiv.org/abs/2510.04618) treats context as an evolving playbook rather than a repeatedly rewritten summary. The paper reports gains of 10.6% on agent benchmarks and 8.6% on finance tasks through incremental generation, reflection, and curation. Cite those as method results, not proof that adding more context is better. The operational principle is smaller: preserve useful detail, attach feedback to an inspectable artifact, and test the evolved context against held-out tasks.

#### Context beyond the repository

Repository files are only one source of truth. Product decisions may live in Linear, interface constraints in Figma, component behavior in Storybook, and operational history in incident systems. Marc Sloan's [2026 talk on product and design constraints](https://www.youtube.com/watch?v=tf6VNGH3tRk&t=523s) argues that this external context must become accessible to the agent without silently drifting away from its source.

| Access pattern | Strength | Failure mode |
|---|---|---|
| Live tool or MCP access | Fresh data and direct attribution | Availability, permission, and prompt-injection risk |
| Versioned repository snapshot | Reproducible and reviewable with the code | Snapshot can become stale |
| Synchronization bridge | Combines freshness with a local artifact | Sync failures can create two conflicting truths |

Record the source, retrieval time, and freshness expectation for external context. If an agent cannot tell whether a design decision is current, the context builder has moved uncertainty into the prompt instead of resolving it.

### 2.3 Tool Registry

The catalog of available tools: name, schema, description, permissions, cost estimate. A static tool registry loads all tool schemas on every call. A dynamic registry ("tool search on demand") loads only what the current task plausibly needs.

Anthropic's internal data (cited in the Fowler article, source: practitioner post) cites a 37% reduction in token usage from dynamic tool dispatch versus static loading. This number is not independently replicated, but the directional claim is credible: giving the model 40 tool schemas when it needs 4 adds noise and cost.

For sensitive MCP (Model Context Protocol) tools, put authentication and authorization at the execution boundary. An identity-aware gateway is one production pattern, but it is not a default property of MCP or Claude Code. The required control depends on the tool's data, side effects, and deployment model. See [MCP Servers Ecosystem](../ecosystem/mcp-servers-ecosystem.md) and [Security Hardening](../security/security-hardening.md).

### 2.4 Sub-Agent Management

Delegation to specialized sub-agents with their own context windows and task scope. The orchestrator spawns a worker, provides a bounded task description, and receives a structured result. The worker does not share the orchestrator's full context; it receives only what it needs.

Factory.ai Missions formalizes this: an orchestrator agent decomposes requirements, delegates implementation to workers, and routes completed work to adversarial validator agents. On a documented Slack clone project, independent validators caught 81 problems before any code was merged, generating 34% of the implementation work as "fix features."

Claude Code subagents inherit the parent session's permission mode by default. That is runtime behavior, not proof of least privilege. Narrow each agent with `tools`, `disallowedTools`, and `permissionMode`, and use `isolation: worktree` when parallel writers must not share a checkout. See [Tools Reference](./tools-reference.md), [Agent Teams](../workflows/agent-teams.md), and the [worktree isolation definition](./glossary.md#worktree-isolation).

### 2.5 Native Tools and Loadable Skills

Claude Code exposes native tools for file access, search, shell execution, web access, delegation, and other runtime operations. Skills are different: they are loadable instruction and resource modules invoked through the `Skill` tool. A skill can include scripts and deterministic checks, but the skill itself is not inherently deterministic because the model still interprets its instructions and chooses actions.

Test deterministic scripts and validators with ordinary assertions. Test the model-mediated part of a skill with behavioral tasks, expected boundaries, and human or calibrated evaluator review. The [Tools Reference](./tools-reference.md) documents the runtime tool surface; the [skills examples](../../examples/skills/) show the separate packaging model.

### 2.6 Session Persistence

State that survives context resets and session interruptions. Not the same as long-term memory (which is a higher-level concept). Persistence at the harness level means: the agent can reconstruct its current task state from externalized artifacts rather than from the in-context conversation history.

Factory.ai Missions uses a shared artifact layer (validation contracts, feature lists, skill definitions) to survive the context limits of multi-day missions. E2B and Northflank provide this at the infrastructure level via persistent sandbox state. Anthropic Claude Managed Agents provide it as a product feature with checkpointing.

### 2.7 Dynamic Prompt Assembly

The step that turns the current state (task description + relevant context + tool definitions + memory + rules) into the actual prompt sent to the LLM. This is not standardized across frameworks. LangChain, LangGraph, and the Anthropic SDK each have different abstractions.

The places where assembly goes wrong: rule injection that conflicts with the user instruction, tool schemas that overlap in ways that confuse the model's selection, memory retrieval that surfaces outdated context. Harnesses that make assembly visible (logging the final assembled prompt, not just the response) are dramatically easier to debug.

Ryan Lopopolo's [2026 harness-engineering talk](https://www.youtube.com/watch?v=c8bE0cj7vHY&t=674s) frames the repository as an environment that must make the team's standard of good work legible and surface the right context just in time. The operational test is simple: if the same review feedback appears twice, decide whether it belongs in a formatter, linter, test, architecture decision record, skill, or verifier. Prompt text is only one possible control.

### 2.8 Lifecycle Hooks

Injection points that fire at defined runtime events. Claude Code does not expose generic `pre-LLM` and `post-LLM` hooks. Its event model includes instruction loading, permission requests, tool use, compaction, subagent and teammate lifecycle, worktree changes, session lifecycle, and failure events. The exact list and blocking semantics live in [Hooks Events Reference](./hooks-events-reference.md).

Hooks are where you insert observability instrumentation, permission validation, rate limiting, output sanitization, and audit logging. Only events with documented blocking semantics can stop an action. Async hooks are appropriate for telemetry that does not need to interrupt the loop.

### 2.9 Permission Enforcement

Every consequential action needs an enforcement boundary before execution. Depending on risk, that boundary can combine explicit approval, permission rules, sandboxing, network policy, scoped credentials, and post-execution verification. Human review remains useful for high-impact decisions, but repeated approval prompts are not a complete isolation strategy.

Two useful structural mechanisms are:

1. **Sandbox isolation**: the agent runs in an environment where destructive actions are physically impossible, not just disallowed by policy but literally impossible given the network, filesystem, and process constraints. Kubernetes agent-sandbox, E2B microVMs, and Northflank BYOC runners implement this at the hardware level.

2. **Identity gateway**: sensitive tool calls are authenticated at call time with a scoped session credential rather than a broad static API key. Strata Maverics and Microsoft Entra Agent ID implement this pattern with OAuth OBO (On-Behalf-Of) flows that scope permissions to the current task context.

Claude Code now supplies additional primitives for this layer: `sandbox.network.strictAllowlist` denies non-allowlisted sandbox traffic without prompting, worktree isolation separates concurrent edits, and `--restricted` removes command and code execution plus `WebFetch` unless explicitly restored. These controls reduce exposure, but they do not establish that every MCP integration uses per-session identity or that every action is sandboxed.

A [2026 interview with Claude Code creator Boris Cherny](https://www.youtube.com/watch?v=julbw1JuAz0&t=3176s) describes the permission system as a layered combination of classifiers, static analysis, pattern allowlists, conservative defaults, and a human decision when the system is unsure. This is useful design rationale from a product creator. Current behavior still needs to be checked against official documentation and the [Claude Code release history](./claude-code-releases.md).

### Claude Code implementation checkpoint

The nine-component model is product-independent. The table below maps it to Claude Code behavior through v2.1.250 without turning this page into a second release log.

| Harness concern | Current Claude Code mechanisms | Release evidence |
|---|---|---|
| Context and state | Automatic and explicit compaction; `PreCompact` and `PostCompact` hooks; automatic memory | v2.1.247, v2.1.105, v2.1.76, v2.1.59 |
| Tool and prompt assembly | Deferred tool loading, `alwaysLoad` MCP option, `InstructionsLoaded` hook | v2.1.121, v2.1.69 |
| Delegation | Background subagents, inherited permission mode, concurrency and nesting limits, conversation forking, prompt-cache inheritance | v2.1.198, v2.1.212, v2.1.217, v2.1.219, v2.1.232 |
| Isolation and policy | Worktree isolation and later hardening, strict network allowlist, `--restricted` launch mode | v2.1.49, v2.1.50, v2.1.222, v2.1.219, v2.1.248 |
| Recovery and coordination | Cross-session messaging, per-agent cache TTL, subagent model fallback | v2.1.224, v2.1.248, v2.1.247 |
| Inspection and control | Permission, tool, compaction, instruction, failure, agent, teammate, and worktree hook events | v2.1.69 to v2.1.219 |

Use the [human-readable release history](./claude-code-releases.md) for interpretation and [`claude-code-releases.yaml`](../../machine-readable/claude-code-releases.yaml) for version-level lookup. `reference.yaml` provides stable topic routes into this page and the surrounding guide.

---

## 3. The Lethal Trifecta: Security Model

Simon Willison coined this term in 2025 (see [martinfowler.com/articles/202508-ai-thoughts.html](https://martinfowler.com/articles/202508-ai-thoughts.html)):

**Private data + untrusted content + external communication = documented exfiltration vector.**

Any two of the three are manageable. All three together, without structural isolation, create a path where an attacker plants instructions in data the agent will read (a document, a code comment, a Jira ticket), the agent processes those instructions using its access to private data, and then uses its communication capabilities to exfiltrate.

This is not theoretical. GitHub Security has documented prompt injection attacks in Copilot via malicious repository content. The defense is not better prompt engineering; it is structural isolation.

[AgentDojo](https://arxiv.org/abs/2406.13352) makes the threat measurable with 97 realistic tasks and 629 security test cases for agents that consume untrusted tool data. [CaMeL](https://arxiv.org/abs/2503.18813) demonstrates a structural response: trusted control flow is separated from untrusted data flow, and capabilities enforce policy when tools are called. CaMeL reports 77% task success with provable security versus 84% for its undefended system. Security has a utility cost, but the boundary is enforceable outside the model.

### Defense layers

| Layer | Mechanism | Implementation |
|-------|-----------|---------------|
| Network isolation | Agent cannot reach external endpoints except an explicit allowlist | GitHub Agentic Workflows: Squid proxy on allowlist; Northflank: egress firewall |
| Filesystem isolation | Agent writes to a temporary workspace, not the host filesystem | Kubernetes agent-sandbox, E2B microVM |
| Identity scoping | Every tool call carries a per-session credential with minimum required permissions | Strata Maverics, Microsoft Entra Agent ID |
| Output validation | Agent-generated content passes through a threat detection step before reaching any production surface | GitHub Agentic Workflows: Safe Outputs pattern (Semgrep + TruffleHog + LlamaGuard) |
| Read-only execution context | Agent reads the codebase but cannot write directly; writes go through a PR/review gate | GitHub Agentic Workflows default posture |

### Why human review alone fails

Anthropic's internal data (shared responsibility model documentation, April 2026): 93% of agent permission requests in production are approved without adequate review. This is not a criticism of the humans involved; it is a structural consequence of volume and cognitive load. When a human approves 50 permission dialogs per hour, individual approval becomes a formality.

The defense that scales: structural isolation (makes certain actions impossible) and second-agent validation (creator-verifier pattern, Section 8). Human review remains appropriate for high-stakes, low-frequency decisions, not for routine agent actions.

---

## 4. CI/CD Agentic Patterns

Three platforms have productized agents as a CI/CD primitive. The choice between them is an architectural decision, not a feature comparison.

### GitHub Agentic Workflows

The central concept: `gh aw compile` takes an agent workflow definition in Markdown and produces a `.lock.yml`, a hardened GitHub Actions file that executes the workflow with enforced isolation. The compilation step is where security properties are baked in, not added later.

**Execution model**: agent runs in a read-only context. It can analyze and generate. Any write (commit, comment, deployment) goes through "Safe Outputs", a separate job that validates the generated artifact before it touches production surfaces. Safe Outputs runs Semgrep (SAST), TruffleHog (secrets detection), and LlamaGuard (harmful content) on agent-generated diffs before they are applied.

**Code review integration**: GitHub Copilot Code Review has processed 60M+ code reviews as of 2026. On Code Review Bench (Martian, March 2026, 200,000+ open-source PRs, 17 tools evaluated), Augment Code leads at 62.8% recall, Copilot at 53.3%. Graphite leads precision at 75% but recall at 8.8% (high precision means few false positives, low recall means many real bugs missed). No tool dominates both metrics.

**c-CRAB benchmark** (arXiv 2603.23448): Claude Code achieves 32.1% pass rate on pull requests with executable test suites as oracles. The union of four tools reaches 41.5%. These are ceiling numbers; average production use is lower.

**Best for**: organizations that want GitHub-native audit trails and a straightforward integration with existing Actions pipelines.

### AWS Bedrock AgentCore

A managed runtime for production agents: versioning of agent definitions, Memory for cross-session state persistence, native Observability (OTel-compatible), and continuous evaluation on 1-2% of live traffic. The eval-on-traffic feature catches silent degradation: a model upgrade that regresses quality without triggering any explicit alarm.

**Best for**: organizations already invested in the AWS ecosystem that need managed state persistence and want continuous quality monitoring without building their own eval infrastructure.

### GitLab Duo

Fix CI/CD Pipeline reached General Availability in GitLab 18.8. When a pipeline fails, Duo reads up to 150 KiB of logs, diagnoses the root cause, and proposes a fix as a Merge Request. CI Expert Agent is in beta as of 18.11 for broader pipeline assistance.

**Key constraint**: 150 KiB log limit. Pipelines with verbose output beyond this threshold get truncated context, which degrades diagnosis quality before routing failures through this path.

**Best for**: GitLab-centric organizations that want agent-assisted CI diagnosis without adopting a separate platform.

---

## 5. Digital Twin Testing

Agents cannot be tested safely in production on the first pass. The standard practice for testing non-AI software is staging environments. For agents that call external services (Slack, Jira, Okta, Google Drive), staging means either burning real API quota or using behavioral mocks that simulate the service accurately enough to surface integration bugs.

**The behavioral mock distinction**: a static mock returns a fixed response. A behavioral mock maintains internal state that evolves logically through sequences of interactions, replicates rate limiting, delayed state propagation, and conditional dependencies. An agent that retries after a 429 response will behave differently against a mock that accurately replicates Slack's rate limit window versus one that just returns 200 for everything.

### Current coverage by service

| Service | Best available mock | Coverage |
|---------|---------------------|---------|
| Slack | Slack-Mock (github.com/Skellington-Closet/slack-mock) | 7 interaction channels: Web API, RTM, Events API, Slash Commands, Webhooks, Interactive Buttons, message delivery. State management included. Most complete. |
| Google Drive | Mockoon pre-configured sample | REST API surface. Limited behavioral state. |
| Okta | Community patterns, DevForum | Authentication flows and identity lifecycle. No official mock. Custom build required. |
| Jira | Atlassian-recommended staging environments | Separate app keys for isolation. Not a behavioral mock. |
| Generic HTTP | WireMock (stateful), Beeceptor (AI-powered, multi-protocol) | No behavioral state for specific services, but configurable for arbitrary HTTP. |

Materialize ("always-current digital twins") takes a different approach: real-time sync with operational systems, with logical isolation. Closer to a managed staging environment than a mock. Useful when agents need authentic data distributions rather than plausible-but-fake test data.

LangWatch Scenario SDK ([langwatch.ai/scenario](https://langwatch.ai/scenario)) is the only attempt at systematic behavioral agent testing without requiring a real running service: it simulates multi-turn conversations against an agent-user that generates realistic inputs, while an agent-judge evaluates whether the system agent met its success criteria.

---

## 6. Observability Stack

The open-source baseline that works in production, documented by independent organizations:

```
OpenLLMetry (Traceloop)       ← instrumentation layer (Python + TypeScript)
      +
OpenInference (Arize)         ← semantic schema for LLM/agent attributes
      ↓
Langfuse or Arize Phoenix      ← tracing backend + eval storage
      +
DeepEval or LangWatch Scenario ← quality evaluation
```

For enterprise with governance requirements, add Strata Maverics or Entra Agent ID in the identity layer.

### OpenTelemetry GenAI conventions (August 2026 status)

The canonical [OpenTelemetry GenAI registry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) defines shared fields for conversations, system instructions, tool definitions, tool-call IDs, arguments, results, workflow names, token usage, and operations such as `execute_tool`, `invoke_agent`, and `invoke_workflow`. The GenAI conventions are still evolving and several definitions have moved to the dedicated semantic-conventions repository, so pin the version used by production instrumentation.

Do not record full content by default. System instructions, retrieval queries, tool arguments, and tool results may contain secrets or personal data. Prefer identifiers, sizes, hashes, allowlisted fields, and explicit redaction. Enable payload capture only for a bounded diagnostic purpose with retention and access controls.

### What to instrument first

1. **Every LLM call**: latency, input tokens, output tokens, model name, finish reason.
2. **Every tool call**: tool name, arguments (redacted if sensitive), result success/failure, latency.
3. **Session-level**: total tokens per session, session duration, task completion (binary).
4. **Eval scores**: task completion rate, tool correctness rate (correct tools used / total tools used).

### Operational measures beyond telemetry

Token and latency traces explain resource use. They do not establish that the agent produced acceptable work. Add outcome and control-flow measures that connect a run to its reviewed result.

| Measure | Why it matters | Source prompt |
|---|---|---|
| Turns to accepted completion | Reveals friction hidden by a final pass/fail score | Patrick Debois discusses [turn count as an agent-enablement signal](https://www.youtube.com/watch?v=I9RWrW32QEw&t=700s) |
| Manual takeovers and human review comments | Measures where the harness still depends on rescue | The AI Native DevCon interview proposes tracking [takeovers and pull-request comments](https://www.youtube.com/watch?v=D_cw-k0F1DM&t=2898s) |
| Requirement coverage | Prevents a broad success score from hiding one missed contract | Executable-spec verifiers can report one verdict per requirement |
| Evidence completeness | Requires commands, outputs, tests, screenshots, or traces for claims of completion | Simon Willison demonstrates a [Markdown proof artifact built from commands and outputs](https://www.youtube.com/watch?v=owmJyKVu5f8&t=461s) |
| Latency distribution | Captures slow tails that a mean or median hides | Amit Kushwaha argues for [distribution-aware agent benchmarks](https://www.youtube.com/watch?v=guhTp2Q8VX0&t=810s) |
| Controlled recovery | Tests whether state survives an interruption without duplicated or lost work | Interrupt the run at a defined point, then inspect its resumed trajectory |
| Repeated-run reliability | Separates a task solved once from behavior that succeeds consistently | [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666) defines consistency, robustness, predictability, and safety as separate dimensions |
| Harness-model pair | Prevents a model name from absorbing harness-specific cost and failure behavior | [The Scaffold Effect](https://arxiv.org/abs/2607.22585) reports harness-specific cost and failure fingerprints under fixed models |

Report denominators and distributions. "Eight accepted tasks out of ten" is inspectable. "The agent usually succeeds" is not. For latency and cost, include at least the median and a tail percentile when the sample supports it. For small pilots, publish every result instead of implying statistical precision.

Datadog, Honeycomb, New Relic, and MLflow all support OTel GenAI conventions. Arize Phoenix processes 1 trillion spans per month across DoorDash, Instacart, Reddit, Uber, and Booking.com, making it the most documented production scale for an open-source option in this space.

### LLM-as-judge limitations

JudgeBiasBench (arXiv 2604.23178, Hongli Zhou et al., April 2026) measured more than 50% error rates for frontier models on advanced bias detection tests. Style bias is the dominant pattern: scores of 0.76-0.92, versus position bias below 0.04. The practical consequence: an LLM judge approves stylistically polished but incorrect outputs significantly more often than it should. True negative rates for identifying invalid outputs typically sit below 25%.

No commercial platform (Arize, LangWatch, Openlayer, Langfuse as of May 2026) publicly documents how it neutralizes style bias in its evaluators.

The working solution: use LLM-as-judge for qualitative dimensions that cannot be evaluated deterministically (tone, explanation quality, context sensitivity). Use code-based checks for anything that can be evaluated mechanically (tool selection correctness, structured output schema compliance, regression tests on known examples). Do not use LLM-as-judge alone as the quality gate for production traffic.

---

## 7. Test Distribution and Component-Stacking Anti-patterns

An empirical study across 39 open-source agent frameworks and 439 agentic applications (arXiv 2509.19185) found that more than 70% of testing effort in agentic systems targets the deterministic components (tools, APIs, workflow logic), while less than 5% targets the Plan Body, the LLM reasoning core. Adoption of dedicated LLM evaluation tools (DeepEval) was below 1% despite those tools' high marketing visibility.

This is structurally backwards. The deterministic components are the most testable with standard unit tests and will fail loudly when broken. The LLM reasoning core is where the non-obvious, non-deterministic failures live: the ones that produce plausible-looking but wrong outputs, miss edge cases in tool selection, or hallucinate capability claims.

**Recommended rebalancing**: give the Plan Body its own behavioral and repeated-run tests instead of assigning an arbitrary percentage target. The pass^k pattern addresses non-determinism: run a critical test several times and report how many executions pass. Promptfoo's `--repeat` flag implements this. LangWatch Scenario SDK does it at the multi-turn simulation level.

For deterministic components: standard unit tests, schema validation, explicit tool call checks. For LLM reasoning: behavioral simulation (LangWatch Scenario), LLM-as-judge with bias awareness, regression suites on known-good examples from production.

Tests are necessary, but a green suite is not a complete proof bundle. Simon Willison's [2026 engineering-practices talk](https://www.youtube.com/watch?v=owmJyKVu5f8&t=415s) pairs tests with captured commands and outputs, then identifies [sandboxing as the main execution boundary](https://www.youtube.com/watch?v=owmJyKVu5f8&t=980s). For an agentic coding task, retain the requirement map, relevant commands, outputs, test results, review verdict, and any visual or runtime evidence needed to reproduce acceptance.

Do not assume that stacking planning, tools, memory, reflection, and retrieval is monotonic. [Cross-Component Interference](https://arxiv.org/abs/2605.05716) tested all 32 subsets of five components on HotpotQA and GSM8K. A single-tool configuration exceeded the all-in system by 32% on HotpotQA; a three-component subset exceeded it by 79% on GSM8K. This is a preprint over two benchmarks, but its design supports a strong engineering rule: start with the smallest sufficient harness and require each added component to pass a paired ablation and regression test.

---

## 8. Creator-Verifier Pattern

The creator-verifier pattern assigns production and evaluation to separate steps or agents. It is a useful design candidate, not a guaranteed accuracy multiplier.

The evidence is mixed. [Self-Refine](https://arxiv.org/abs/2303.17651) reports gains from iterative same-model feedback across seven tasks. [Multiagent Debate](https://arxiv.org/abs/2305.14325) reports improvements on selected reasoning and factuality tasks. Conversely, [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) finds that intrinsic self-correction without external feedback can fail or degrade answers. [Scalable oversight experiments](https://arxiv.org/abs/2407.04622) find task-dependent rather than universal gains, and [LLM-as-a-judge bias research](https://arxiv.org/abs/2410.02736) documents systematic evaluator biases. Anthropic's [evaluator-optimizer guidance](https://www.anthropic.com/engineering/building-effective-agents) therefore recommends the pattern when evaluation criteria are clear and iterative refinement produces measurable value.

A fresh context is only one dimension of independence. A verifier can still share the creator's blind spots when both depend on the same model family, specification, tools, retrieval corpus, reward signal, or missing runtime evidence. Assess at least five dimensions:

| Independence dimension | Failure when shared | Stronger design |
|------------------------|---------------------|-----------------|
| **Context** | The reviewer inherits the creator's framing and assumptions | Give the reviewer requirements, artifact, and evidence without the creator's chain of reasoning |
| **Model or provider** | Correlated blind spots and self-preference | Stratify results by model and test provider diversity where risk justifies the cost |
| **Evidence and tools** | Both agents inspect the same incomplete signals | Add deterministic tests, runtime traces, external sources, or a different inspection tool |
| **Role and incentives** | The reviewer optimizes for agreement or style | Require per-requirement pass/fail verdicts and evidence, not a generic quality score |
| **Escalation authority** | A probabilistic verdict silently becomes final | Define appeal, timeout, human checkpoint, and fail-closed rules for high-impact decisions |

Measure rescued failures, false accepts, false rejects, regressions, latency, and cost. Counting reviewer calls or using a different role name does not establish independence.

Liza implements this pattern as doer/reviewer pairs backed by a deterministic supervisor. Its [state machine and merge authority](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/specs/architecture/supervision-model.md) can reject invalid transitions even when an agent proposes them. That is stronger than a role name in a prompt, but it still needs outcome evaluation: a structurally separate reviewer can share the same model, incomplete specification, or missing evidence as the doer.

The pinned Liza configuration makes the boundary visible. Some high-impact planning stages require a quorum of two and mark provider diversity as `preferred`, while the coding pair uses a quorum of one. Liza's own [architectural issues ledger](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/specs/architecture/architectural-issues.md) states that provider diversity is not enforced at verdict submission, reviewer accuracy is not yet measured, and human checkpoints remain load-bearing. The code enforces workflow legality; it does not prove that a legal reviewer verdict is correct.

### Judgment allocation: where responsibility actually sits

A stopping condition answers when a loop ends. It does not by itself establish that the result is good enough. Every production design should record who sets the quality bar, what evidence is admissible, who decides that the evidence is sufficient, and who handles exceptions.

| Decision | Default owner | Evidence | Escalate when |
|----------|---------------|----------|---------------|
| Product intent and acceptable risk | Accountable human or product authority | Requirements, policy, risk classification | Intent is ambiguous or impact is high |
| Task decomposition and routing | Orchestrator or planning agent | Typed task graph, dependencies, budgets | Fan-out is large, irreversible, or crosses domains |
| Execution | Runtime and repository harness | Tool results, sandbox events, changed artifacts | A permission, policy, or environmental boundary is reached |
| Mechanical acceptance | Deterministic gate | Tests, schemas, linters, policy checks, reproducible commands | Coverage is incomplete or a check is flaky |
| Semantic sufficiency | Reviewer agent for bounded work, accountable human for high-impact work | Requirement-level verdicts plus inspected evidence | The verifier is uncertain, conflicted, or outside its evidence boundary |
| Release or policy exception | Human or external policy authority | Signed approval and auditable rationale | Never silently auto-approve an exception |

This is the useful insight from the loop-engineering debate: human judgment does not necessarily disappear when prompts are automated. It moves to loop design, quality criteria, exception policy, and final accountability. [Own the Outer Loop](https://addyo.substack.com/p/own-the-outer-loop) presents this as a practitioner design principle. Treat the exact placement as a risk decision, not a universal rule.

Practical implementation: spawn a second agent with the output artifact and the original requirements. Ask whether the output satisfies each requirement. Do not ask "is this good?" Ask "does this satisfy requirement X?" with explicit pass/fail for each.

An executable-spec variant makes that contract more granular:

1. A planner extracts explicit requirements and acceptance evidence from the task.
2. One verifier evaluates each requirement independently, in parallel where isolation allows it.
3. Each verifier inspects the relevant codebase state, not only the produced diff.
4. Runtime behavior is checked in an ephemeral browser or sandbox when static inspection cannot prove it.
5. The harness aggregates per-requirement verdicts and preserves the evidence behind each one.

Shachar Azriel presents this architecture in [Executable Specs: Building a Verification Layer for Agentic Coding](https://www.youtube.com/watch?v=aWrGSM5vVyc&t=861s). The talk documents an implementation approach. It does not independently prove the resulting product's accuracy, so treat the pattern as a design candidate and test it against real repository tasks.

This does not eliminate hallucination; it catches the subset of hallucinations that are inconsistent with the stated requirements. For catching hallucinations that are internally consistent but factually wrong, you need domain-specific test cases.

---

## 9. Reference Architecture

```
User instruction
      ↓
┌─────────────────────────────────────────────────────────────────┐
│                       HARNESS                                    │
│                                                                  │
│  ┌─────────────┐      ┌──────────────┐      ┌───────────────┐   │
│  │   Context   │      │  While-Loop  │      │  Permission   │   │
│  │  Management │◄────►│    Engine    │◄────►│  Enforcement  │   │
│  └─────────────┘      └──────┬───────┘      └───────────────┘   │
│                              │                                    │
│  ┌─────────────┐      ┌──────▼───────┐      ┌───────────────┐   │
│  │   Session   │      │   Dynamic    │      │   Lifecycle   │   │
│  │ Persistence │◄────►│   Prompt     │◄────►│    Hooks      │   │
│  └─────────────┘      │  Assembly   │      └───────────────┘   │
│                        └──────┬───────┘                          │
│  ┌─────────────┐             │              ┌───────────────┐   │
│  │    Tool     │      ┌──────▼───────┐      │  Sub-Agent    │   │
│  │  Registry   │◄────►│  LLM Call    │◄────►│  Management   │   │
│  └─────────────┘      └──────────────┘      └───────────────┘   │
│                                                                  │
│  ┌─────────────┐                                                  │
│  │  Built-in   │                                                  │
│  │   Skills    │                                                  │
│  └─────────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
      ↓
┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
│   Sandbox    │      │   Identity   │      │  Observability   │
│  (E2B/k8s/  │      │  Gateway     │      │  (OTel + eval)   │
│  Northflank) │      │(Strata/Entra)│      │                  │
└──────────────┘      └──────────────┘      └──────────────────┘
```

---

## 10. Practitioner Video Evidence

This ledger connects the architecture to dated practitioner and product-creator testimony. Every quoted sentence below was checked against the local WebVTT transcript and links to the corresponding YouTube timestamp. Capitalization and punctuation are normalized; wording is preserved. The transcript proves what was said at that point in the video. It does not prove that a product still behaves that way, that a reported outcome generalizes, or that an interview claim was independently measured.

Use three evidence levels throughout this page:

- **Official current evidence** for product behavior, limits, licences, and availability.
- **Creator interviews** for dated design rationale and historical product decisions.
- **Practitioner talks** for methods, failure reports, and hypotheses that still require local validation.

| Source | Timestamped verbatim | What it supports | Evidence boundary |
|---|---|---|---|
| [Harness Engineering: The New Discipline of Agentic Dev](https://www.youtube.com/watch?v=D_cw-k0F1DM), AI Native DevCon interview, 2026-07-08 | ["Never tell the agent more than once how to do a thing before it gets codified somewhere in the inner or outer loop."](https://www.youtube.com/watch?v=D_cw-k0F1DM&t=459s) | Inner, outer, and meta feedback loops | Practitioner model, not a formal standard; speaker name is not established by the local metadata |
| [Patrick Debois, The Rise of Agent Enablement](https://www.youtube.com/watch?v=I9RWrW32QEw), 2026-07-08 | ["We're not building the thing, we're building the thing that builds the thing."](https://www.youtube.com/watch?v=I9RWrW32QEw&t=98s) | Agent enablement as system design | Organizational framing, not a benchmark result |
| [Ryan Lopopolo, Harness Engineering: How to Build Software When Humans Steer and Agents Execute](https://www.youtube.com/watch?v=c8bE0cj7vHY), 2026-06-19 | ["I never want to give the same review feedback twice."](https://www.youtube.com/watch?v=c8bE0cj7vHY&t=668s) | Codifying recurring feedback into the harness | Practitioner workflow and definition |
| [Marc Sloan, Harness Engineering Beyond Code](https://www.youtube.com/watch?v=tf6VNGH3tRk), 2026-06-20 | ["Product and design context is important to agents, but it lives outside the code base."](https://www.youtube.com/watch?v=tf6VNGH3tRk&t=523s) | External product and design context | Practitioner talk; integration trade-offs require local testing |
| [Boris Cherny, Building Claude Code](https://www.youtube.com/watch?v=julbw1JuAz0), 2026-03-04 | ["If you're not sure, just ask the human and then they can decide."](https://www.youtube.com/watch?v=julbw1JuAz0&t=3301s) | Conservative permission fallback | Creator interview; current behavior belongs in official docs and release notes |
| [Dax Raad, Building OpenCode](https://www.youtube.com/watch?v=1VqKUrxR2C8), 2026-05-27 | ["You need some kind of control plane to like set up all the providers, permissions, budget controls, rate limits."](https://www.youtube.com/watch?v=1VqKUrxR2C8&t=2048s) | Separation between runtime and organizational control plane | Creator interview and dated product claim, not proof of current availability |
| [Simon Willison, Engineering Practices That Make Coding Agents Work](https://www.youtube.com/watch?v=owmJyKVu5f8), 2026-03-19 | ["I think tests are no longer even remotely optional."](https://www.youtube.com/watch?v=owmJyKVu5f8&t=415s) | Tests, proof artifacts, and sandboxing | Practitioner recommendation |
| [Shachar Azriel, Executable Specs: Building a Verification Layer for Agentic Coding](https://www.youtube.com/watch?v=aWrGSM5vVyc), 2026-06-15 | ["The code is how we ground that agent to reality."](https://www.youtube.com/watch?v=aWrGSM5vVyc&t=868s) | Requirement-level verification against actual code | Architecture described by the speaker; outcomes are not independently verified here |
| [Amit Kushwaha, Benchmarking the Agent Era](https://www.youtube.com/watch?v=guhTp2Q8VX0), 2026-07-10 | ["You can't talk about mean and medians. Now you have to talk about in terms of distributions."](https://www.youtube.com/watch?v=guhTp2Q8VX0&t=810s) | Multi-turn, multi-tool, tail-aware measurement | Benchmark-methodology talk; specific performance claims require the underlying study |
| [Dex Horthy, Context Engineering](https://www.youtube.com/watch?v=Usufn8IQJgw), 2026-07-15 | ["If you want to do loops engineering, you should build one loop at a time and keep them small and contained."](https://www.youtube.com/watch?v=Usufn8IQJgw&t=3509s) | Bounded loops before lights-off automation | Practitioner interview and retrospective, not a controlled study |
| [Pavan Belagatti, What Is a Software Factory?](https://www.youtube.com/watch?v=0nM1ygBm8tA), 2026 | ["Agents do the work, humans provide the gates."](https://www.youtube.com/watch?v=0nM1ygBm8tA&t=97s) | Separation between the execution loop and the governance loop | Practitioner short and Port-oriented framing; no comparative reliability or productivity measurement |

The source list is selective. It includes videos that add a distinct mechanism, metric, or failure boundary to this page. Inclusion is not an endorsement of every claim in a talk.

---

## 11. Harness Optimizers and Meta-Harnesses

A runtime harness improves one agent run. A harness optimizer improves the code and configuration that govern future runs. The optimizer can edit prompts, context policies, tools, middleware, memory, control flow, verification, or routing, then use an external evaluator to decide which candidate survives.

| Work | Optimization surface | Reported evidence | Boundary |
|---|---|---|---|
| [Automated Design of Agentic Systems](https://proceedings.iclr.cc/paper_files/paper/2025/hash/36b7acf6f6010652b3f2a433774a66fe-Abstract-Conference.html), ICLR 2025 | Code-defined agent systems | Meta Agent Search discovers prompts, tools, and workflows that transfer across domains and models | System-level search; not every result isolates a fixed-model harness effect |
| [AFlow](https://arxiv.org/abs/2410.10762), ICLR 2025 | Code-represented workflows | 5.7% average improvement across six benchmarks | Heterogeneous model-plus-workflow baselines |
| [ACE](https://arxiv.org/abs/2510.04618), ICLR 2026 | Context and memory playbooks | +10.6% on agent benchmarks and +8.6% on finance tasks | Context optimization, not whole-harness search |
| [GEPA](https://arxiv.org/abs/2507.19457), ICLR 2026 Oral | Prompts from reflected trajectories | 6% average gain over GRPO across six tasks, with up to 35 times fewer rollouts | Prompt optimizer; model control varies by experiment |
| [Meta-Harness](https://arxiv.org/abs/2603.28052), 2026 preprint | End-to-end harness code | +7.7 points with four times fewer context tokens; +4.7 points across five held-out models on 200 math problems | TerminalBench search and final evaluation reuse the same 89 tasks; total search compute is not reduced to one comparable cost figure |
| [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850), 2026 preprint | Prompt, tools, middleware, skills, subagents, and memory | Terminal-Bench 2 pass@1 rises from 69.7% to 77.0% over ten iterations | Coding-focused preprint; external replication remains limited |
| [HarnessOpt-Bench](https://arxiv.org/abs/2608.06301), 2026 preprint | The optimizer itself | Five optimizer models, four downstream tasks, 111 scored runs | Benchmark protocol, not a production optimizer |

The evidence is promising but young. Do not promote a candidate because its development score improved. A credible optimization run needs:

1. **Frozen invariants:** target model, tool permissions, task contract, grader, and resource limits remain fixed unless the experiment declares otherwise.
2. **Separated data:** detailed development traces, bounded validation feedback, and a hidden test partition that the optimizer cannot inspect.
3. **Explicit budgets:** evaluation calls, task attempts, tokens, wall time, and human interventions are metered.
4. **Versioned candidates:** every change has a diff, rationale, predicted benefit, regression risk, score, and rollback path.
5. **Multi-metric promotion:** success, accepted-task cost, latency distribution, repeated-run reliability, and failure severity all participate in the decision.
6. **External evaluation:** the optimizer cannot alter the evaluator, reveal hidden cases, or award its own final score.

[HarnessOpt-Bench](https://arxiv.org/abs/2608.06301) is the clearest current protocol: a trusted execution environment hides the test partition, enforces evaluation budgets, meters resources, and preserves candidate versions. [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825) explains why those controls matter: task and reward defects can distort reported agent performance by up to 100% in relative terms, and its checklist reduced CVE-Bench overestimation by 33%.

The practical conclusion is not “self-improving agents solve harness engineering.” It is that harness engineering can become an auditable experiment when the search space, evidence, budget, and promotion boundary are explicit.

---

## See Also

- [Agent Harness Landscape](../ecosystem/agent-harness-landscape.md): dated product map, evidence states, and selection protocol
- [Architecture](./architecture.md): Claude Code's master loop, tools, context, agents, permissions, and MCP integration
- [Tools Reference](./tools-reference.md) and [Hooks Events Reference](./hooks-events-reference.md): exact runtime surfaces
- [Context Engineering](./context-engineering.md) and [Memory Systems](./memory-systems.md): prompt assembly, persistence, retrieval, and drift
- [Agent Evaluation](../roles/agent-evaluation.md) and [Observability](../ops/observability.md): acceptance evidence, traces, metrics, and failure analysis
- [Security Hardening](../security/security-hardening.md) and [Native Sandbox](../security/sandbox-native.md): prompt-injection defense and execution boundaries
- [Agent Teams](../workflows/agent-teams.md) and [Agentic Software Factories](../workflows/agentic-software-factories.md): multi-agent coordination above one loop
- [Repository Harness Engineering](../ultimate-guide.md#925-harness-engineering): project-level instructions, setup, state, and verification gates
- [Machine-Readable References](../../machine-readable/README.md): release history, topic anchors, and normalized harness data

---

*Last updated: August 2026. Claude Code implementation mapping checked through v2.1.250. Practitioner quotations checked against the yt-insights WebVTT corpus snapshot generated on 2026-08-25. Academic evidence checked against primary sources through 2026-08-28. arXiv 2605.18747 (Code as Agent Harness) is the primary code-centric survey; arXiv 2606.20683 supplies the six-responsibility runtime taxonomy.*
