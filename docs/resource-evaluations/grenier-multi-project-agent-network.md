# Resource Evaluation: Multi-Project Agent Network (Mathieu Grenier)

**URL**: https://mathieugrenier.fr (blog "Coder avec Claude, c'est facile et rapide"), article dated 2026-08-15
**Type**: Personal blog post, French, first-person field report
**Author**: Mathieu Grenier, CTO at Easystrat (Montpellier), managing ~10 engineers remotely from Japan
**Evaluation date**: 2026-08-16
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1
**Method**: full read of the article, cross-check of its novelty claim against `guide/` via grep, and against a 2026-08-14 ecosystem research pass covering Symphony, Gas Town, Paperclip, Beads, OpenClaw and scape.work. No access to the author's `.pi` codebase, which is not published.

> **Name collision warning**: `docs/resource-evaluations/grenier-agent-skill-quality.md` (2026-02-07, scored 3/5) attributes its source to a "Mathieu Grenier, Staff Eng + Growth @ MosaicML/Databricks, ex-Shopify". That is a different person from this article's author, or an attribution error in the earlier file. The two evaluations must not be merged or cross-linked as the same author. The earlier attribution is worth re-verifying on its own.

---

## Content summary

The author runs an agentic network built on **Pi** (a third-party harness, state under `~/.pi/`), not on Claude Code's native primitives. Until this week each project had one orchestrator delegating to sub-agents (coder, runner, scout, memory-curator) with no channel between orchestrators. The article documents the move to multi-project operation, enabled by a bidirectional messaging layer.

**Transport**: unix sockets under `~/.pi/coms/sockets/`, per-project registries, JSON envelopes (`prompt`, `response`, `ping`, `nudge`), acknowledgements, and a five-hop limit. Tools exposed: `coms_send`, `coms_get`, `coms_await`, `coms_reply`, `coms_check`.

**Central agent**: a `.pi` meta-orchestrator that explicitly does not pilot anything. Project orchestrators send it grievances, which it sorts into four categories (Ambiguity, False info, Struggle, Suggestion), submits the sort to the human for validation, delegates the implementation, then verifies by reading the result rather than trusting the report.

**Fixes shipped into `~/.pi/extensions/`**: `coms.ts` re-resolves the sender at `coms_reply` time, keeps pending messages on timeout, raises inbound TTL from 5 to 30 minutes, caches already-delivered replies, and detects a dead or rotated receiver. Automatic nudge at 5 minutes. `pi-delegate.ts` maintains a per-delegate JSON status file (output preview, steps, exit code) for non-blocking supervision.

**Stated scale**: five to six projects live. The author is explicit that this is not yet true parallelism, and that domain coordinators (agents owning a set of projects rather than one) are the next step.

---

## What is genuinely useful

Two items are concrete, transferable, and absent from the guide.

**The steering rule.** "On steer un agent qui dévie, jamais un agent qui progresse." Learned the hard way: a well-intentioned steer made a runner loop for roughly 10 minutes answering messages instead of advancing. The rule is counter-intuitive, general to any supervised-agent setup, and expensive to discover alone. The article backs it with the inverse cases where steering was correct: a runner stuck 12 minutes writing a script without ever executing it (declared failed and relaunched), a grep loop that killed itself (redirected in five lines, "PIDs fixes, pas de boucle"), a `cache:clear` runner drifting 22 seconds in useless directory discovery (re-dispatched with an absolute workdir: 18 seconds, exit 0).

**The single-writer pattern applied to agents.** The frontend's memory-curator has no write permission. After producing three items it asked, over the message bus, for its orchestrator to strike a batch in the orchestration plan. The orchestrator performed the write. Result: no duplicates, no write conflict. This is the standard single-writer principle transposed to a multi-agent file-editing context, and it is the direct mitigation for the write-conflict failure mode that appears whenever several agents share a plan file.

A third detail is worth noting without being a pattern in itself: the meta-orchestrator verifies delegated work by reading the artifact, never on the delegate's word. Rare discipline, cheap to adopt.

---

## The novelty claim does not hold

The article states that "le multi-projet / multi-repo comme unité d'orchestration de premier ordre n'apparaît nulle part dans la littérature" and that a central meta-orchestrator interviewing its sub-orchestrators to improve the tooling is "réellement nouveau comme pattern nommé de bout en bout".

The cited sources explain the gap: LangGraph (January 2024), AutoGen group chat, metaswarm (February 2026), Microsoft Agent Framework A2A (April 2026), plus three generic French-language orchestration pages. The search covered enterprise and academic multi-agent frameworks and missed the entire 2026 wave of coding-agent orchestrators.

| Claim | Counter-evidence |
|---|---|
| Bidirectional orchestrator-to-orchestrator messaging is the missing link | Claude Code **agent teams** ship a mailbox with true peer-to-peer teammate-to-teammate messaging, isolated 1M context per agent (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Documented in `guide/workflows/agent-teams.md:207-219` since the 2026-02-09 correction. Cross-session `SendMessage` became full peer-to-peer session messaging in the July-August 2026 releases (`guide/core/claude-code-releases.md`, 16 occurrences) |
| Multi-project / multi-repo as a first-class orchestration unit is undocumented | `github.com/steveyegge/gastown` coordinates Claude Code, Copilot, Codex and Gemini across separate workspaces with git-hook state persistence. ComposioHQ/AgentWrapper's `agent-orchestrator` describes itself as "Orchestrate parallel AI coding agents across any runtime, **any repo**, any issue tracker" (already evaluated: `docs/resource-evaluations/agent-orchestrator-composio.md`). OpenAI **Symphony** (Apache-2.0, April 2026) isolates a workspace per issue |
| A meta-agent improving its own delegation layer is a new named pattern | **Hermes** runs a GEPA loop: after each task it analyses what worked, extracts reusable patterns and auto-generates skills. Documented in `guide/ecosystem/agentic-tools.md:121-142`, with a community-reported 40% speedup once 20+ skills accumulate |
| Central coordinator that dispatches without doing domain work | The **Hub-and-Spoke Coordinator** in `guide/workflows/agent-teams.md:1526` states the same constraint verbatim: "It does no domain work itself, no research, no analysis, no generation." Also `guide/core/architecture.md:648` |

What may remain original is narrower than claimed and worth keeping: the **four-category grievance taxonomy** (Ambiguity, False info, Struggle, Suggestion), the human validation of the sort before any implementation, and the read-back verification. That is a methodological contribution, not a new architecture.

The author does hedge ("je le dis prudemment, ce n'est pas une preuve d'unicité absolue"), which is honest, and the framing here should credit that rather than treat the claim as an assertion of fact.

---

## Technical blind spots

**A fault-tolerant messaging layer is being rebuilt from scratch.** Look at the fix list: TTL raised 5 to 30 minutes, cache of already-delivered replies, sender re-resolution at reply time, dead or rotated receiver detection, automatic nudge at 5 minutes, five-hop limit, silent dead-letters, acknowledgements. These are the canonical problems of distributed messaging, solved since the 1980s. NATS, Redis Streams or ZeroMQ provide all of it with idempotency and persistence included. The five-hop limit is a packet TTL under another name. The "noms d'orchestrateurs qui rotent par session" problem is unstable identity, whose standard fix is a registry with an ID decoupled from the session name.

**No cost figure anywhere.** Five to six live projects, each with an orchestrator plus sub-agents, all exchanging messages, plus a meta-orchestrator interviewing everyone. `guide/workflows/agentic-software-factories.md:35` puts agent teams at **3x or more in tokens** versus a single agent, and an orchestrator-to-orchestrator mesh multiplies that again. Comparable public field reports state their numbers (u/croovies shows per-session dollars, another practitioner shows $115/day at API rates). This one states none, which is the first question any reader will ask.

**Hop limit is not loop detection.** Five hops bounds chain length, not cycles. Three orchestrators re-triggering each other on a cross-cutting problem burn quota in a circle with short chains each time. A conversation ID plus a per-exchange-tree token budget would close that.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 2 | Bidirectional agent messaging, multi-repo orchestration and self-improving harnesses all exist in shipped products; the grievance taxonomy is the only element not found elsewhere |
| Evidence quality | 4 | Dated, quantified incidents with durations, exit codes and named root causes; failures reported as readily as successes |
| Reproducibility | 2 | Built on Pi with unpublished `coms.ts` and `pi-delegate.ts`; no repo, no config sample, no schema. A reader cannot rebuild this from the article |
| Documentation quality | 2 | Clear and well-structured, but the novelty claim rests on a source set that predates the relevant products, and the article does not state its running cost |
| Guide value | 3 | Two transferable items absent from `guide/`, both landing in a section that already exists |
| **Overall** | **3** | Moderate. Integrate the two patterns, do not carry over the novelty framing |

---

## Decision

**Partial integration into `guide/workflows/agent-teams.md`, section "Advanced Orchestration Patterns" (line 1526).**

1. **Steering rule** as a named subsection: redirect an agent that is drifting, never one that is progressing. Include the counter-example (a steer on a healthy runner cost ~10 minutes of message-answering instead of work) and the positive cases (12-minute non-executing runner, self-killed grep loop, 22-second workdir drift). Source-attribute to the article.
2. **Single-writer pattern for shared plan files**: a read-only agent requests the write over the message bus, the orchestrator performs it. Connect it to the existing read/write separation already described for investigation agents, and to `guide/core/memory-systems.md:740` (Multi-Agent Shared Memory).

**Do not integrate**: the novelty claim, the transport architecture (five hops, socket registry, TTL tuning), and the meta-orchestrator framing. The first is contradicted by the guide's own content, the second is a reimplementation of standard messaging primitives, and the third duplicates the Hub-and-Spoke Coordinator already documented in the same file.

**Optional one-line mention**: the four-category grievance taxonomy with human validation of the sort, as a lightweight technique for feeding agent-reported friction back into tooling. Fits `guide/roles/agent-evaluation.md` next to the existing skill-self-improvement material rather than in agent-teams.

**Revisit trigger**: the `.pi` coms and delegate extensions are published under a license, cost figures are disclosed for the five-to-six-project setup, or the announced domain coordinators ship with a documented arbitration mechanism (which would genuinely extend beyond what agent teams and Gas Town cover today).

---

## Cross-references

- `guide/workflows/agent-teams.md:207-219` (mailbox, peer-to-peer), `:805` (when not to use), `:1526` (advanced patterns)
- `guide/diagrams/07-multi-agent-patterns.md:13` (three orchestration topologies)
- `guide/core/architecture.md:648` (Hub-and-Spoke Orchestration)
- `guide/ecosystem/agentic-tools.md:121-142` (Hermes GEPA self-improvement loop)
- `guide/ecosystem/ai-ecosystem.md:1804` (when NOT to use orchestrators), `:2346` (3 to 8 concurrent projects)
- `guide/ecosystem/third-party-tools.md:1342,1375` (multi-repo workspaces), `:1381` (Agent Orchestrator)
- `guide/workflows/agentic-software-factories.md:35` (3x token cost, six production cases)
- `docs/resource-evaluations/agent-orchestrator-composio.md` (any-repo orchestration, already evaluated)
- `docs/resource-evaluations/fusion-multi-agent-orchestrator.md` (multi-agent orchestrator case study)
