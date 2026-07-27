r# Resource Evaluation #079 — Fabro: Graph-Based Workflow Orchestrator for AI Coding Agents

**Source:** [fabro.sh](https://fabro.sh) / [github.com/fabro-sh/fabro](https://github.com/fabro-sh/fabro)
**Type:** Open source tool (MIT) — standalone workflow orchestrator for AI coding agents
**Author:** Bryan from qlty.sh (bryan@qlty.sh)
**Evaluated:** 2026-03-17
**Maturity at evaluation:** Created 2026-03-13 (4 days old, 28 stars, now 1,449 as of 2026-07-28), 1 fork

---

## Summary

- **Workflow orchestrator for AI coding agents**: define pipelines as Graphviz DOT graphs with branching, loops, parallelism, and human approval gates — diffable and version-controlled
- **Multi-model routing**: CSS-like stylesheets assign different LLM models (Claude, OpenAI, Gemini) to specific workflow nodes, with automatic fallback chains
- **Git checkpointing per stage**: every stage commits code changes and execution metadata to a dedicated Git branch — unique feature with no direct equivalent found in the landscape
- **Cloud sandboxes**: isolated Daytona VMs with snapshot-based setup, network controls, SSH access, and automatic cleanup
- **Automatic retrospectives**: each run generates a cost/duration/narrative retrospective for continuous improvement
- **Direct Claude Code integration**: `curl -fsSL https://fabro.sh/install.md | claude` (security note: pipes directly into Claude, no intermediate review step)
- **Single Rust binary, zero runtime dependencies**: no Python, no Node.js, no Docker required
- **REST API + SSE streaming + React web UI**: run workflows programmatically or as a service

---

## Relevance Score

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap in the guide |
| 4 | Very relevant — Significant improvement |
| **3** | **Pertinent — Useful complement, Watch status** |
| 2 | Marginal — Secondary information |
| 1 | Out of scope — Not relevant |

**Final score: 3/5 (Watch)**

**Justification:** Fabro falls directly in the "External Orchestration Frameworks" category already documented in the guide (`third-party-tools.md`). Its DOT graph approach is architecturally distinct from all three existing entries (Ruflo equals swarms, Athena Flow equals hooks layer, Pipelex equals DSL). Git checkpointing per stage is a genuine differentiator, with no equivalent found in competing frameworks. Direct Claude Code integration via `claude` pipeline is legitimate. However, 28 stars (now 1,449 as of 2026-07-28) at 4 days old shows the same early maturity profile as Athena Flow (#073, score 2/5). Raised to 3/5 vs Athena Flow because of stronger architectural clarity, a wider feature set with more evidence, and a genuinely unique Git checkpointing angle.

---

## Comparison

| Aspect | Fabro | Guide (current state) |
|--------|-------|-----------------------|
| DOT graph pipeline definition | Unique approach | Not covered |
| Multi-model routing per node | CSS-like stylesheets | Not covered |
| Git checkpointing per stage | Concrete differentiator | Not covered anywhere |
| Cloud sandboxes (Daytona) | Declared, unverified in prod | Not covered |
| Human-in-the-loop approval gates | Hexagon nodes in DOT | Partially covered via Ruflo |
| External orchestration frameworks | External layer over Claude Code | Ruflo + Athena Flow + Pipelex |
| Maturity / community traction | 28 stars, 4 days | Ruflo at 18.9k stars |
| `curl \| claude` install security | Risk: no review step | Guide warns against `curl \| bash` |

---

## Competitive Landscape (Perplexity research, 2026-03-17)

Full competitive analysis conducted. Key findings:

| Tool | Category | Stars | Key difference from Fabro |
|------|----------|-------|--------------------------|
| **LangGraph** (LangChain) | Graph-based pipelines | ~34k | Python library (not standalone binary), general purpose (not coding-agent specific), no Git checkpointing |
| **Goose** (Block) | Coding agent orchestration | ~15k | Recipe-based (not graph), conversational architecture, no Git checkpointing — but much more mature |
| **OpenHands** | Coding agent platform | ~48k | Event-stream architecture, Docker sandboxes, research-oriented — no DOT graph, no Git checkpointing per stage |
| **Ruflo** | External orchestration (guide) | 18.9k | Swarm-based (queen + workers), npm, SQLite memory — no DOT graph, no Git checkpointing |
| **Athena Flow** | Hook-layer runtime (guide) | Watch | Hook → UDS → Node.js — entirely different architecture layer |
| **Pipelex** | MTHDS DSL (guide) | Watch | Declarative DSL for multi-LLM pipelines — different abstraction |
| **AutoGen** (Microsoft) | Multi-agent conversations | ~47.9k | General purpose, conversation-loop model, no coding-agent specifics |
| **CrewAI** | Role-based agent crews | ~34.7k | Role assignment model, no graph definition, no Git checkpointing |

**Fabro's unique combination** (no competitor does all three):
1. DOT graph workflow definition as a standalone binary
2. Git checkpointing per stage (code + metadata committed to branches)
3. Native Claude Code integration via `claude`

**Most relevant alternative for guide readers today**: LangGraph for graph-based workflows (much more mature, Python), Goose (Block) for coding agent orchestration (better traction, MIT).

---

## Recommendations

**When to integrate:** Add as Watch entry now. Promote to full entry in `guide/ecosystem/third-party-tools.md` under "External Orchestration Frameworks" when trigger is reached.

**Where:** After Athena Flow in `third-party-tools.md` External Orchestration Frameworks section.

**How:** Short entry (same format as Athena Flow) with:
- Architectural distinction (DOT graph — distinct from all three existing entries)
- Git checkpointing differentiator
- Security note on `curl | claude` install (same pattern as Ruflo's `curl | bash` warning)
- Status: "Published March 2026, not yet audited"

**Do NOT do:**
- Recommend the `curl | claude` install without a security note
- Present any feature as production-validated (no community evidence yet)
- Add before the traction trigger is reached

**Secondary discovery:** Goose (Block, github.com/block/goose) warrants its own evaluation (#080). 15k stars, MIT, recipes + subagents + 20 LLM providers — potentially more immediately relevant to the guide's audience.

---

## Challenge (technical-writer agent)

**Initial proposed score:** 4/5
**Score after challenge:** 3/5 (lowered)

Points raised:

- **Immaturity flag**: 28 stars / 4 days = same pattern as Athena Flow (score 2/5). Applying this inconsistently undermines the scoring framework. Compromise: 3/5 because Fabro shows more architectural evidence than Athena Flow at equivalent age.
- **`curl | claude` security**: more dangerous than typical `curl | bash` — pipes directly into the codebase with no review step. Guide's own security section would flag this. Must be noted in any future integration.
- **Ambitious unverified feature set**: cloud sandboxes, DOT routing, retrospectives — none validated by community use at evaluation time.
- **Risk of not integrating at this stage**: near zero. Category already covered by 3 entries.
- **What is genuinely novel**: DOT graph definition as diffable text (distinct from Ruflo/Pipelex/Athena) + Git checkpointing per stage = angles worth tracking.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| 28 GitHub stars | Verified (now 1,449 as of 2026-07-28) | GitHub API direct |
| Created 2026-03-13 | Verified | GitHub API `created_at` |
| Rust, single binary, zero deps | Verified | README |
| MIT license | Verified | GitHub API + README badge |
| `curl \| claude` install | Verified | README + fabro.sh landing |
| DOT graph workflows | Verified | README + example code |
| Daytona cloud sandboxes | Declared | README feature table (unaudited) |
| Supports Claude/OpenAI/Gemini | Declared | WebFetch landing (unaudited) |
| Git checkpointing per stage | Declared | README feature table (unaudited) |
| Automatic retrospectives | Declared | README feature table (unaudited) |
| Bryan from qlty.sh | Verified | `bryan@qlty.sh` in README |

**No corrections needed:** all claims traced to primary sources. Features marked "Declared" are present in README but not community-validated.

---

## Final Decision

- **Final score**: 3/5
- **Action**: Watch — add to `watch-list.md`, revisit when trigger reached
- **Re-eval trigger**: >200 GitHub stars OR practitioner write-up from production use
- **Confidence**: High on score, medium on features (project too recent for full audit)
- **Next action**: Evaluate Goose (Block) as #080 — more immediately relevant to guide's audience