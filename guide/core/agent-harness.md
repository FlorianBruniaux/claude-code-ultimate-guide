---
title: "Code as Agent Harness (arXiv 2605.18747): Agent Harness Engineering"
description: "A practical companion to the Code as Agent Harness paper (arXiv 2605.18747): the nine components that turn a raw LLM into a reliable production agent, from while-loop engine to permission enforcement."
tags: [guide, agents, architecture, security, observability]
keywords:
  - "code as agent harness arxiv 2605.18747"
  - "agent harness"
  - "agent harness engineering"
  - "what is an agent harness"
  - "2605.18747"
---

# Agent Harness Engineering

> **Confidence**: Tier 1 — Multiple independent sources (Martin Fowler, arXiv 2605.18747, Anthropic, O'Reilly, AWS, GitHub) converge on this framing.
>
> **Reading time**: ~25 minutes

---

## The core claim

A raw LLM is not an agent. It becomes one when connected to a harness.

Martin Fowler, Addy Osmani, O'Reilly's 2026 AI Radar, and arXiv 2605.18747 (May 2026) all converge on this: the relevant unit of engineering is not the model but the infrastructure that wraps it. Fowler defines a harness as a "cybernetic governor" combining feed-forward and feedback to regulate agent behavior toward a desired state. The harness is what makes "AI generates most of the code" sustainable at scale rather than a gradual drift toward unmaintainable systems.

As of May 2026, 57% of organizations have agents running in production, and 32% cite quality as their primary obstacle (LangChain State of Agent Engineering). The teams that have closed this gap have one thing in common: they engineered the harness, not just the prompt.

---

## Table of Contents

1. [Three Foundational Properties](#1-three-foundational-properties)
2. [The Nine Components](#2-the-nine-components)
3. [The Lethal Trifecta: Security Model](#3-the-lethal-trifecta-security-model)
4. [CI/CD Agentic Patterns](#4-cicd-agentic-patterns)
5. [Digital Twin Testing](#5-digital-twin-testing)
6. [Observability Stack](#6-observability-stack)
7. [Test Distribution Anti-pattern](#7-test-distribution-anti-pattern)
8. [Creator-Verifier Pattern](#8-creator-verifier-pattern)
9. [Reference Architecture](#9-reference-architecture)

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

### 2.2 Context Management

What goes into the prompt on each loop iteration: conversation history, tool outputs, retrieved memory, current task state, rules from CLAUDE.md. The challenge is that context is finite and expensive. Strategies:

- **Compaction / summarization**: replace earlier turns with a compressed summary. Claude Code's `/compact` does this manually; robust harnesses do it automatically when usage crosses a threshold.
- **Sliding window**: keep the last N turns verbatim, summarize everything before.
- **Retrieval-augmented context**: retrieve relevant chunks from long-term storage rather than carrying everything in the window.

The ACE pipeline (see [context-engineering.md §6](./context-engineering.md#6-the-ace-pipeline)) is the Config-Persistence layer above context management: it governs what rules and skills are loaded across sessions.

### 2.3 Tool Registry

The catalog of available tools: name, schema, description, permissions, cost estimate. A static tool registry loads all tool schemas on every call. A dynamic registry ("tool search on demand") loads only what the current task plausibly needs.

Anthropic's internal data (cited in the Fowler article, source: practitioner post) cites a 37% reduction in token usage from dynamic tool dispatch versus static loading. This number is not independently replicated, but the directional claim is credible: giving the model 40 tool schemas when it needs 4 adds noise and cost.

MCP (Model Context Protocol) tools must pass through a gateway that validates the calling agent's identity before the tool executes. This is not an optional hardening step; it is the baseline for preventing privilege escalation via chained tool calls.

### 2.4 Sub-Agent Management

Delegation to specialized sub-agents with their own context windows and task scope. The orchestrator spawns a worker, provides a bounded task description, and receives a structured result. The worker does not share the orchestrator's full context; it receives only what it needs.

Factory.ai Missions formalizes this: an orchestrator agent decomposes requirements, delegates implementation to workers, and routes completed work to adversarial validator agents. On a documented Slack clone project, independent validators caught 81 problems before any code was merged, generating 34% of the implementation work as "fix features."

Key constraint: sub-agent permissions must not be inherited from the parent. The principle of least privilege applies at the delegation boundary.

### 2.5 Built-in Skills

Native operations that do not require an LLM call: file read/write, web search, code execution, shell commands. Claude Code formalizes skills as loadable modules since late 2025. The distinction matters: a skill is deterministic (read this file, run this test), while an agent action involves LLM reasoning.

The test distribution anti-pattern (Section 7 below) is partly caused by conflating skill testing (deterministic, unit-testable) with agent reasoning testing (probabilistic, requires LLM-as-judge or behavioral simulation).

### 2.6 Session Persistence

State that survives context resets and session interruptions. Not the same as long-term memory (which is a higher-level concept). Persistence at the harness level means: the agent can reconstruct its current task state from externalized artifacts rather than from the in-context conversation history.

Factory.ai Missions uses a shared artifact layer (validation contracts, feature lists, skill definitions) to survive the context limits of multi-day missions. E2B and Northflank provide this at the infrastructure level via persistent sandbox state. Anthropic Claude Managed Agents provide it as a product feature with checkpointing.

### 2.7 Dynamic Prompt Assembly

The step that turns the current state (task description + relevant context + tool definitions + memory + rules) into the actual prompt sent to the LLM. This is not standardized across frameworks. LangChain, LangGraph, and the Anthropic SDK each have different abstractions.

The places where assembly goes wrong: rule injection that conflicts with the user instruction, tool schemas that overlap in ways that confuse the model's selection, memory retrieval that surfaces outdated context. Harnesses that make assembly visible (logging the final assembled prompt, not just the response) are dramatically easier to debug.

### 2.8 Lifecycle Hooks

Injection points that fire at defined moments: pre-LLM-call, post-LLM-call, pre-tool-execution, post-tool-execution, on-error. Claude Code implements this via the settings.json hooks system. AWS Bedrock AgentCore and GitHub Agentic Workflows have their own hook models.

Hooks are where you insert: observability instrumentation, permission validation, rate limiting, output sanitization, audit logging. Hooks that run inline (blocking) can abort bad actions before they execute. Hooks that run async (fire-and-forget) are appropriate for logging that doesn't need to interrupt the loop.

### 2.9 Permission Enforcement

Every action passes through the policy layer. Not as a human review (see Section 3 for why that fails at scale), but as a structural enforcement that happens before the tool call executes.

The two mechanisms that work:

1. **Sandbox isolation**: the agent runs in an environment where destructive actions are physically impossible, not just disallowed by policy but literally impossible given the network, filesystem, and process constraints. Kubernetes agent-sandbox, E2B microVMs, and Northflank BYOC runners implement this at the hardware level.

2. **Identity gateway**: every MCP tool call is authenticated at call time with a per-session credential, not a static API key. Strata Maverics and Microsoft Entra Agent ID implement this with OAuth OBO (On-Behalf-Of) flows that scope permissions to the current task context.

---

## 3. The Lethal Trifecta: Security Model

Simon Willison coined this term in 2025 (see [martinfowler.com/articles/202508-ai-thoughts.html](https://martinfowler.com/articles/202508-ai-thoughts.html)):

**Private data + untrusted content + external communication = documented exfiltration vector.**

Any two of the three are manageable. All three together, without structural isolation, create a path where an attacker plants instructions in data the agent will read (a document, a code comment, a Jira ticket), the agent processes those instructions using its access to private data, and then uses its communication capabilities to exfiltrate.

This is not theoretical. GitHub Security has documented prompt injection attacks in Copilot via malicious repository content. The defense is not better prompt engineering; it is structural isolation.

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

**Key constraint**: 150 KiB log limit. Pipelines with verbose output beyond this threshold get truncated context, which degrades diagnosis quality. Worth knowing before routing all failures through this path.

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

### OTel GenAI conventions (May 2026 status)

| Span type | Status | Key attributes |
|-----------|--------|---------------|
| `gen_ai.client` | Stable | `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens` |
| `gen_ai.agent` | Experimental | `gen_ai.agent.name`, `gen_ai.agent.id` — may change |
| Events | Stable | Prompt/completion content as structured events |
| Metrics | Stable | Token counters, latency histograms |

The experimental status of `gen_ai.agent` spans matters: attributes may be renamed or restructured before stabilization. Production harnesses using agent spans today should expect a remapping cost when the spec stabilizes. OpenInference (Arize) and OpenLLMetry (Traceloop) address this by providing a stable schema on top of the evolving OTel spec.

### What to instrument first

1. **Every LLM call**: latency, input tokens, output tokens, model name, finish reason.
2. **Every tool call**: tool name, arguments (redacted if sensitive), result success/failure, latency.
3. **Session-level**: total tokens per session, session duration, task completion (binary).
4. **Eval scores**: task completion rate, tool correctness rate (correct tools used / total tools used).

Datadog, Honeycomb, New Relic, and MLflow all support OTel GenAI conventions. Arize Phoenix processes 1 trillion spans per month across DoorDash, Instacart, Reddit, Uber, and Booking.com, making it the most documented production scale for an open-source option in this space.

### LLM-as-judge limitations

JudgeBiasBench (arXiv 2604.23178, Hongli Zhou et al., April 2026) measured more than 50% error rates for frontier models on advanced bias detection tests. Style bias is the dominant pattern: scores of 0.76-0.92, versus position bias below 0.04. The practical consequence: an LLM judge approves stylistically polished but incorrect outputs significantly more often than it should. True negative rates for identifying invalid outputs typically sit below 25%.

No commercial platform (Arize, LangWatch, Openlayer, Langfuse as of May 2026) publicly documents how it neutralizes style bias in its evaluators.

The working solution: use LLM-as-judge for qualitative dimensions that cannot be evaluated deterministically (tone, explanation quality, context sensitivity). Use code-based checks for anything that can be evaluated mechanically (tool selection correctness, structured output schema compliance, regression tests on known examples). Do not use LLM-as-judge alone as the quality gate for production traffic.

---

## 7. Test Distribution Anti-pattern

An empirical study across 39 open-source agent frameworks and 439 agentic applications (arXiv 2509.19185) found that more than 70% of testing effort in agentic systems targets the deterministic components (tools, APIs, workflow logic), while less than 5% targets the Plan Body, the LLM reasoning core. Adoption of dedicated LLM evaluation tools (DeepEval) was below 1% despite those tools' high marketing visibility.

This is structurally backwards. The deterministic components are the most testable with standard unit tests and will fail loudly when broken. The LLM reasoning core is where the non-obvious, non-deterministic failures live: the ones that produce plausible-looking but wrong outputs, miss edge cases in tool selection, or hallucinate capability claims.

**Recommended rebalancing**: allocate at minimum 20-30% of testing effort to the Plan Body. The pass^k pattern addresses non-determinism: run a critical test 3-5 times and require it to pass in k out of k runs. Promptfoo's `--repeat` flag implements this. LangWatch Scenario SDK does it at the multi-turn simulation level.

For deterministic components: standard unit tests, schema validation, explicit tool call checks. For LLM reasoning: behavioral simulation (LangWatch Scenario), LLM-as-judge with bias awareness, regression suites on known-good examples from production.

---

## 8. Creator-Verifier Pattern

A structural pattern that consistently improves output correctness: one agent (or agent step) generates, a separate agent verifies, with no shared context between the two.

The data:

- Microsoft Agent Framework, AutoGen Studio, and Google ADK have all adopted this as a standard pattern.
- Playwright Test Agents implements it as a three-agent architecture: planner designs the test strategy, generator writes the test code, healer fixes failures.
- Independent verification improves correctness by +12 to +26% versus self-verification across documented implementations.
- Factory.ai Missions: adversarial validators caught 81 problems in a Slack clone project, generating 34% of the implementation work as fix features.
- OpenAI Codex's auto-review system reduced human approval requirements by a factor of 200x versus manual review.

The underlying reason self-verification fails: the model that generated the output carries the same biases and context as the model that reviews it. Verification by a fresh model instance, with only the artifact and the success criteria in context, is structurally different from self-review.

Practical implementation: spawn a second agent with the output artifact and the original requirements. Ask whether the output satisfies each requirement. Do not ask "is this good?" Ask "does this satisfy requirement X?" with explicit pass/fail for each.

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

## See Also

- [Context Engineering](./context-engineering.md) — ACE pipeline, signal taxonomy, drift management
- [Security Hardening](../security/security-hardening.md) — production safety, injection defense
- [DevOps & SRE](../ops/devops-sre.md) — CI/CD integration patterns
- [AI Roles](../roles/ai-roles.md) — Harness Engineer, Agent Identity Architect, AI Eval Engineer
- [Spec-First Development](../workflows/spec-first.md) — spec as the input to the harness

---

*Last updated: May 2026. arXiv 2605.18747 (Code as Agent Harness) is the primary academic source for the three properties. Martin Fowler's Harness Engineering article is the primary practitioner reference. Both were published in 2025-2026.*
