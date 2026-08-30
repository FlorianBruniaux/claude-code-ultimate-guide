# Resource Evaluation: Loop & Graph Engineering evidence set

**Evaluated:** 2026-08-30
**Decision:** Integrate as a conceptual reference
**Confidence:** High for framework documentation and pinned Liza architecture; medium for terminology and general design claims
**Scope:** terminology, executable workflow contracts, durable execution, judgment allocation, observability, and bounded implementation cases

## Decision

Create and maintain a canonical page at [`guide/core/loop-graph-engineering.md`](../../guide/core/loop-graph-engineering.md). It fills a real navigation gap between the runtime-oriented [Agent Harness Engineering](../../guide/core/agent-harness.md), the product inventory in the [Agent Harness Landscape](../../guide/ecosystem/agent-harness-landscape.md), and the measurement guidance in [Agent Evaluation](../../guide/roles/agent-evaluation.md).

The page must not present Loop Engineering or Graph Engineering as settled standards, or as evidence that graph-based systems outperform simpler loops. It should teach contracts and boundaries that readers can test now.

## Evidence classification

| Source | Type | What it supports | Evidence boundary |
|---|---|---|---|
| [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | Primary framework documentation | explicit state, nodes, fixed and conditional edges, parallel super-steps, compile-time structure checks | Documents LangGraph behavior, not a universal reliability claim |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Primary framework documentation | `InMemorySaver` for experimentation, thread-scoped checkpoints, cross-thread stores, and persistent checkpointers for production | Use a durable backend when state must survive a process restart; application idempotency remains separate |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts#rules-of-interrupts) | Primary framework documentation | resuming a dynamic interrupt restarts the containing node, so pre-interrupt effects can run again | This does not define all replay or failed-attempt behavior; apply idempotency to the relevant execution boundary |
| [Temporal Workflow Execution](https://docs.temporal.io/workflow-execution) | Primary workflow-engine documentation | durable workflow execution, event history, replay, state transitions | Temporal is a workflow engine, not an LLM-agent runtime by itself |
| [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md) | Primary open specification, Development status | agent, model, request, response, token, and tool telemetry fields | Vocabulary can change. Use an adapter and version local graph and judgment fields. |
| [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | Primary product documentation | agentic loop, tool observation, and verification behavior | Documents Claude Code behavior, not an explicit general graph runtime |
| [Claude Code memory and AGENTS.md compatibility](https://code.claude.com/docs/en/memory#agentsmd) | Primary product documentation | Claude Code reads `CLAUDE.md`; an existing `AGENTS.md` can be imported or symlinked | `AGENTS.md` alone is not the supported direct project-instruction file for Claude Code |
| [Graph Engineering in the Era of LLM Agents](https://arxiv.org/abs/2608.21156) | Primary research preprint | current graph-engineering framing and research agenda | Recent preprint; conceptual contribution, not independent performance proof |
| [What Makes Prompts a Graph](https://arxiv.org/abs/2607.27578) | Primary research preprint | operational prompt-graph vocabulary and boundary analysis | Recent single-author preprint; use as a proposal, not a standard |
| [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) | Explicitly qualified practitioner REX | outer-loop framing, maker/checker separation, state as a working record | Personal practice account, not controlled evidence or product documentation |
| [Liza pinned source](https://github.com/liza-mas/liza/tree/a22c12381c5d884d2586a48aaaa517bca184f9cf) | Primary source-code evidence | stable pipeline configuration, external runtime ownership, control-plane mechanics | Exact source boundary documented in [Liza evaluation](./liza-mas-framework.md) |
| [Ippon Liza REX](https://blog.ippon.fr/2026/04/29/premier-rex-multi-agent-liza/) | Explicitly qualified third-party practitioner REX | one bounded multi-agent coding project, human checkpoints, operational friction | Not a production benchmark, comparative study, independence proof, or proof of semantic correctness |

## Source handling

The supplied research report was used as a discovery map only. Its broken footnotes and secondary links were not treated as proof. Its numerical claims were not carried into the canonical page. Every externally sourced claim in the page links to primary documentation, a primary preprint, pinned source evidence, or an explicitly labelled REX.

## Content assessment

| Criterion | Assessment | Rationale |
|---|---|---|
| Relevance | 5/5 | The guide already uses the terms across harness, evaluation, observability, and Liza material. A canonical boundary page reduces duplication and category errors. |
| Novelty | 4/5 | The individual mechanisms exist elsewhere, but the contract-first integration of loop, graph, durability, and judgment allocation is missing. |
| Evidence quality | 4/5 | Strong official framework and specification sources; terminology remains emerging and product outcomes are deliberately not generalized. |
| Actionability | 5/5 | Includes loop and graph contract fields, a bounded example, anti-patterns, and a readiness checklist. |
| Duplication risk | Controlled | The page links to, rather than restating, the detailed runtime components, security model, and product inventory. |

## Editorial constraints

- Keep the guide page in English.
- State that Loop Engineering is practitioner vocabulary and Graph Engineering is emerging research terminology.
- Do not publish performance, productivity, or cost figures from the supplied report without a direct, scoped source and an evidence boundary.
- Distinguish the following claims: framework behavior, source-code architecture, practitioner experience, and general engineering recommendation.
- Use Liza as a bounded control-plane case. Do not call it a general graph runtime or claim that deterministic workflow legality proves task correctness.
- Do not make LLM-as-judge or creator-verifier separation the sole acceptance mechanism.

## Final decision

**Action:** Integrate and cross-link.

**What the page establishes:** a practical vocabulary and verifiable contracts for feedback loops, workflow graphs, durable state, routing, judgment, and evidence.

**What it does not establish:** that graph-based systems are universally superior, that a multi-agent reviewer is independent by default, or that an orchestrator makes human release authority unnecessary.
