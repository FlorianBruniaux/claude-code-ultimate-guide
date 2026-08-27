---
title: "AI Executive Agents: Virtual C-Suites and Board Simulators"
description: "How far the persona/agent pattern goes when applied to named executive roles (CFO, CMO, CHRO, General Counsel, board of directors): OpenExecutive deep dive, open-source alternatives, a routing table by role, and the augmentation-vs-replacement question"
tags: [ecosystem, multi-agent, orchestration, personas]
---

# AI Executive Agents: Virtual C-Suites and Board Simulators

> **Confidence**: Mixed. OpenExecutive, Gstack, and crewAI are Tier 1/2 (verified against source repos, active development). Most other open-source projects listed here are Tier 3 (single-digit to low-hundreds GitHub stars, early-stage, verify before adopting). Commercial products are cited from vendor-published claims, not independently audited.

**Reading time**: ~12 min
**Prerequisites**: [Multi-agent orchestration](../workflows/README.md), [Cognitive Mode Switching (Gstack)](../workflows/gstack-workflow.md)
**Related**: [AI Ecosystem](./ai-ecosystem.md), [Third-Party Tools](./third-party-tools.md), [AI Roles](../roles/ai-roles.md)

---

## TL;DR

The persona/agent pattern that Claude Code skill packs use for engineering roles (see [Gstack](../workflows/gstack-workflow.md)) is being applied to named business executive roles: CFO, CMO, CHRO, General Counsel, COO, board of directors. [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) is the most complete open-source example: 8 specialist Claude agents behind one coherent "Executive" persona. It has peers, most of them small and early. Almost none of these projects claim legal or fiduciary authority: the entire category positions itself as augmentation, not replacement, regardless of how aggressive the marketing copy reads.

```
Persona          →  a role definition layered on a general model (tone, scope, priorities)
Agent            →  a persona + tools + state + goal-directed multi-step behavior
AI executive     →  an agent explicitly named after a C-suite/board role, with enough
                     autonomy and persistence to be treated as a virtual team member
```

---

## Gstack Is Not This Category

Before going further: [Gstack](../workflows/gstack-workflow.md) (Garry Tan, 124.8K+ stars) is a 6-skill workflow suite for **software engineering** (`/plan-ceo-review`, `/plan-eng-review`, `/review`, `/ship`, `/browse`, `/retro`). The `/plan-ceo-review` command name invites confusion, but it is a pre-implementation product gate inside a coding session, not a persona that simulates a Chief Executive Officer for business decisions. If you came here looking for Gstack because of that command name, see [Cognitive Mode Switching](../workflows/gstack-workflow.md) instead. What Gstack does share with the projects below is the underlying architecture: role definitions + shared context + slash-command workflows inside a single repo. That pattern is the throughline of this page, applied to a different domain.

---

## OpenExecutive: Reference Architecture

[OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) (SenteLabsAI, Apache 2.0, 838 stars as of 2026-08-27) is the most explicit mapping of the persona/agent pattern onto a standard executive committee. Eight specialist Claude agents sit behind one coherent "Executive" persona, never exposed individually to the user:

```
User message
    ↓
Executive Orchestrator (claude-sonnet-4-6)
    ↓ tool use → parallel specialist calls
CSO / CFO / CHRO / GC / COO / CMO / CPO / Board Communications
    ↓ each specialist retrieves relevant context from ChromaDB
Built-in MBA knowledge + company documents
    ↓
Synthesized executive response
```

Stack: Python 3.11 + FastAPI backend, Next.js 15 UI, ChromaDB for RAG (built-in knowledge base + uploaded company documents, two separate collections), SQLite for episodic memory (a background `claude-haiku-4-5` pass extracts decisions after every response), a single-instance scheduler for proactive follow-ups, and integrations for Slack, email, Telegram, Google Chat, and Discord. `claude-opus-4-7` handles deep reasoning for CSO/CFO/GC/Board; the rest default to `claude-sonnet-4-6`. It also runs on OpenRouter or local OpenAI-compatible servers (Ollama, LM Studio, vLLM) instead of the Anthropic API.

Two things are worth flagging rather than taking at face value. First, the tagline "Harvard MBA-level knowledge" is marketing copy, not a verifiable claim: the knowledge base is a git-tracked Markdown corpus seeded into ChromaDB, its actual depth is not audited here. Second, the README documents no explicit guardrail distinguishing "this is a recommendation" from "this is a decision," despite the General Counsel and Board Communications agents touching legal and governance territory where that distinction matters most. What is genuinely solid: prompt caching is correctly structured (persona, company profile, and knowledge index cached separately, dynamic RAG content injected into the user turn, never the cached system prompt), and the project ships a real eval gate, 29 scenarios across all 8 domains, scored by `claude-opus-4-7` as an LLM-as-judge on 5 dimensions, with a CI gate requiring ≥3.5/5 average and blocking any dimension that drops more than 10% versus `main`.

---

## Open-Source Alternatives to OpenExecutive

Verified directly against the GitHub API on 2026-08-27, not against secondary write-ups (an earlier research pass for this page cited inflated or wrong numbers from blog posts; treat any AI-executive-agent claim you read elsewhere the same way until you check the repo yourself).

| Project | Author | Stars | License | Last push | Roles | Differentiator |
|---|---|---|---|---|---|---|
| [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive) | SenteLabsAI | 838 | Apache 2.0 | 2026-08-26 | CSO, CFO, CHRO, GC, COO, CMO, CPO, Board Comms | Most complete mapping to a standard C-suite; production-grade eval suite |
| [Become CEO](https://github.com/wanikua/become-ceo) | wanikua | 60 | MIT | 2026-03-13 | Engineering, Finance, Marketing, DevOps, Legal, Management, Chief of Staff | Discord-native: 7 bots, one per role, built on the Clawdbot framework |
| [OneManCompany](https://github.com/1mancompany/OneManCompany) | 1mancompany | 398 | Apache 2.0 | 2026-08-26 | User-defined (not prescribed) | Not a persona set. An "agentic operating system" that orchestrates hierarchical agent teams one level above Claude Code / Codex-style tools |
| [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent) | daniel-st3 | 7 | none detected | 2026-03-08 | CFO only | Narrow and cheap: FastAPI + LangGraph + Next.js + Claude Haiku, CSV upload to board-ready dashboard, claimed $0.003/run |
| [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board) | granman3 | 0 | none detected | 2026-02-22 | 4-member board | Debate format instead of consensus: agents are prompted to challenge each other, not converge. Essentially undiscovered (0 stars, no license file, meaning no reuse rights are granted by default) |
| [crewAI](https://github.com/crewaiinc/crewai) | crewAI Inc | 57,664 | MIT | 2026-08-27 | None (framework) | Not an executive product. The general-purpose multi-agent orchestration substrate several vendor tools in this space are likely built on |

Read the star counts as a maturity signal, not a quality signal: a project with 7 or 0 stars can still be technically sound, it just means almost nobody has looked at the code yet. Quorum Virtual Board shipping with no license file is a real adoption blocker, not a formality: without one, default copyright applies and you have no legal right to reuse, modify, or self-host the code.

---

## Routing Table: Which Project for Which Role

| Looking for | Open source | Commercial | Note |
|---|---|---|---|
| A full virtual executive team | OpenExecutive · Become CEO · OneManCompany (build-your-own) | BattleTested (62 agents / 10 departments) · Ghost CEO (AI Boardroom) | OpenExecutive has the most complete standard C-suite mapping; Become CEO trades breadth for a Discord-native interface |
| CFO | [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent) | [Nume](https://www.nume.ai/) · [Zeni AI CFO Agent](https://www.zeni.ai/ai-agents/ai-cfo-agent) | AI CFO Agent is self-hosted and narrow (startup finance dashboards only) |
| CMO | none found | [Okara](https://okara.ai/) · [Improvado](https://improvado.io/blog/ai-cmo) (concept, not a standalone product) | No credible open-source AI CMO surfaced in this research pass |
| COO | none found | [Tericsoft](https://www.tericsoft.com/blogs/ai-coo-fleet-operations-agent) | Vertical-specific (fleet operations), not general-purpose |
| CHRO / People | none found | none branded as "AI CHRO" | Confirmed gap. HR responsibilities are split across Phenom, Greenhouse, HireVue, Pymetrics, Culture Amp, BetterUp, Workday Adaptive Planning, Oracle Cloud HCM, none marketed as an executive persona |
| General Counsel / Legal | OpenExecutive's GC agent · Become CEO's Legal bot (both embedded, not standalone) | [GC AI](https://gc.ai/) | No standalone open-source "AI General Counsel" found |
| Chief of Staff | Become CEO's Chief of Staff bot (embedded) | [alfred_](https://get-alfred.ai/ai-chief-of-staff) · Lindy AI Chief of Staff · [Viktor](https://viktor.com/ai-chief-of-staff) | The most mature commercial category in this entire landscape: email/calendar triage (alfred_), SaaS workflow execution (Lindy), Slack/Teams operations (Viktor) |
| Sales / CRO | OpenExecutive's CSO agent (embedded) | [Salesforce Agentforce](https://www.salesforce.com/sales/ai-sales-agent/guide/) · [Veetee AI Chief Sales Officer](https://veeteetechnologies.com/artificial-intelligence-leadership) | Salesforce's advantage is direct CRM data access, not model quality |
| Board of directors / advisors | [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board) (0 stars, no license) | [Diligent AI Board Member](https://ai.boardroom.diligentoneplatform.com/) · Personal Board AI (consumer) | Diligent claims hundreds of active director users; Quorum is the only open-source board-debate implementation found but is effectively unadopted |
| Build your own from scratch | [crewAI](https://github.com/crewaiinc/crewai) | - | General framework, not a persona product |

---

## Augmentation, Not Replacement (So Far)

Across every project surveyed here, the marketing language ranges from cautious to aggressive ("no full-time CFO required"), but not one claims legal personhood, fiduciary duty, or final decision authority. The closest thing to a theoretical exception is the **Synthetic Director** concept proposed by law firm Stirling & Rose in 2023: an AI system registered with a regulator, assigned a unique identifier, and subject to a "functional competence test" against real directorial duties (preventing insolvent trading, complying with constitutional obligations), with power to suspend or terminate it for aberrant behavior. That framework does not exist in any jurisdiction's law today. It is worth knowing about because it is the only serious attempt to define what accountability would even look like if one of these agents were ever given real authority, not because any product here is close to qualifying.

Two adoption barriers apply regardless of how good the underlying model gets. First, data integration: an AI CFO or AI CMO is only as good as the accounting, CRM, and ad-platform data it can actually reach, and most organizations' data is messier than a demo. Second, the EU AI Act's compliance deadlines and the absence of case law on AI-influenced executive decisions mean that any agent touching hiring, termination, or financial disclosure sits in genuinely unresolved legal territory, not just cautious vendor copy.

For the general Claude Code framing of augmentation versus replacement (a different context, dev tools rather than business roles, but the same underlying philosophy), see [AI Ecosystem: Augmentation, Not Replacement](./ai-ecosystem.md#philosophy-augmentation-not-replacement).

---

## When to Actually Use One of These

- **You want to see the pattern implemented end-to-end**: read [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive)'s source. It is the most complete reference architecture in this list, and Apache 2.0 permits forking it for your own domain.
- **You want a narrow, cheap, single-role agent**: AI CFO Agent (CFO) or a comparable narrow commercial tool is a smaller bet than adopting a full virtual executive team.
- **You want chief-of-staff-style operational triage today**: this is the one category with mature, funded commercial products (alfred_, Lindy, Viktor). Don't build this yourself first.
- **You're looking for an AI CHRO**: it does not exist as a branded product yet. Compose recruiting (Phenom, Greenhouse), performance (Culture Amp, BetterUp), and workforce planning (Workday Adaptive Planning) tools instead, or build the orchestration layer yourself on crewAI.
- **You're evaluating this for an actual board decision or legal question**: nothing in this list carries fiduciary or legal authority. Treat every output as a recommendation for a human to verify, not a decision.

---

## Sources

- [OpenExecutive](https://github.com/SenteLabsAI/OpenExecutive), [Become CEO](https://github.com/wanikua/become-ceo), [Quorum Virtual Board](https://github.com/granman3/quorum-virtual-board), [OneManCompany](https://github.com/1mancompany/OneManCompany), [AI CFO Agent](https://github.com/daniel-st3/ai-cfo-agent), [crewAI](https://github.com/crewaiinc/crewai): star counts, licenses, and last-push dates pulled directly from the GitHub API on 2026-08-27.
- [Nume](https://www.nume.ai/), [Zeni AI CFO Agent](https://www.zeni.ai/ai-agents/ai-cfo-agent), [Okara](https://okara.ai/), [Improvado](https://improvado.io/blog/ai-cmo), [Tericsoft](https://www.tericsoft.com/blogs/ai-coo-fleet-operations-agent), [Diligent AI Board Member](https://ai.boardroom.diligentoneplatform.com/), [GC AI](https://gc.ai/), [Veetee Technologies](https://veeteetechnologies.com/artificial-intelligence-leadership), [Salesforce AI Sales Agents](https://www.salesforce.com/sales/ai-sales-agent/guide/), [alfred_](https://get-alfred.ai/ai-chief-of-staff), [Viktor](https://viktor.com/ai-chief-of-staff): vendor-published product pages, not independently audited for traction or accuracy claims.
- [Synthetic Directors: The Hybrid Boardroom](https://stirlingandrose.com/2023/10/20/synthetic-directors-the-hybrid-boardroom-of-ai-and-human-collaboration/) (Stirling & Rose, 2023).
- [AI and the CHRO](https://www.imd.org/ibyimd/human-resources/ai-and-the-chro-redefining-human-capital-leadership/) (IMD) for the AI-CHRO gap and adjacent HR tooling.
