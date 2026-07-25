# Resource Evaluation: Liza (MAS framework)

**URL**: https://github.com/liza-mas/liza
**Type**: GitHub repository (framework)
**Evaluation date**: 2026-07-12 (updated 2026-07-15)
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1

---

## Context: distinct from the earlier evaluation

On 2026-06-10, an evaluation ([`liza-mas-token-saving-cli-tools.md`](./liza-mas-token-saving-cli-tools.md)) rejected the **satellite tools** from the liza-mas org (scip-search, mdtoc, functional-clusters, stacklit-cli), all at 0-2 stars, all coupled to the framework. This evaluation covers a different object: **Liza the multi-agent framework itself** (`liza-mas/liza`), the Go orchestrator that uses those satellites. Author: Tangi Vass.

---

## Content summary

Liza is a spec-driven multi-agent coding system (MAS) with two modes (solo Pairing and Multi-Agent). Claimed hybrid architecture:

- **Deterministic Go supervisors** wrap each LLM agent and mechanically perform the critical actions (worktree management, merges, TDD enforcement, state transitions). Strict state machine, 43+ validation rules. Judgment stays with the agent.
- **Adversarial doer/reviewer pairs** on every activity (epic planning, user story writing, code planning, coding), PR-review style interaction until approval.
- **Behavioral contract**: 55+ documented LLM failure modes, each mapped to a countermeasure. Injected into every agent (the equivalent of a non-overridable "constitution").
- **Auditable YAML blackboard**: agent Kanban plus full historized state plus review comments.
- **Circuit breaker**: pattern detection (loops, repeated failures) triggers an automatic checkpoint. An explicit andon cord (stop-the-line).
- **Wraps provider CLIs, not their APIs**: uses the existing subscription (Claude Max, ChatGPT Pro). BYOM: Claude Code, Codex CLI, OpenCode, Kimi, Mistral, Gemini.
- 13 roles across 4 phases (spec, architecture, coding, integration). Isolated git worktrees. 35k LOC Go plus 92k of tests.

---

## Relevance score: 3/5

| Score | Meaning |
|-------|---------|
| ~~5~~ | ~~Critical, major gap in the guide~~ |
| ~~4~~ | ~~Highly relevant, significant improvement~~ |
| **3** | **Relevant, useful complement (as a reference architecture)** |
| ~~2~~ | ~~Marginal~~ |
| ~~1~~ | ~~Out of scope~~ |

**Rationale**: Liza is the most complete open-source match we have found for the governance pattern presented at the GenAI France meetup (Solario/Maleus, July 2026) and documented in `guide/workflows/spec-first.md` (section "Full-cycle AI software factories"). It mechanically answers the four governance questions from that section, where OpenHands (no deterministic supervisor) and spec-kitty (worktree isolation but no behavioral contract and no circuit breaker) cover only part. The value to the guide is **architectural**, as a concrete illustration of what mechanical governance looks like versus prompt-level governance, not as a tool to adopt (322 stars, single author, unproven in production outside the author's own usage).

---

## Cross-check against the four governance pillars (spec-first.md)

| Governance pillar (Solario/Maleus talk) | Liza | OpenHands (already covered) | spec-kitty (already covered) |
|------------------------------------------|------|------------------------------|------------------------------|
| 1. Deterministic gate vs LLM self-assessment | ✅ Go supervisors enforce state/merge/TDD | ⚠️ Automated merge but no code-enforced supervisor | ⚠️ Human review, no code gate |
| 2. Stop-the-line (andon cord) | ✅ Explicit circuit breaker | ❌ Not documented | ❌ Not documented |
| 3. Traceability / audit trail | ✅ Historized YAML blackboard | ⚠️ Cloud/Enterprise only | ✅ Merge audit trail |
| 4. Spec stays authoritative | ⚠️ Front-loaded goal doc, no long-term sync | ❌ | ⚠️ Versioned specs |

It is the only one of the three OSS projects to document a circuit breaker (pillar 2), the point flagged as "few platforms document it explicitly" in spec-first.md.

---

## The project's own competitive survey (added 2026-07-15)

Liza ships a 660-line competitive survey at [`specs/architecture/competition-survey/mas-survey.md`](https://github.com/liza-mas/liza/blob/24b35b90801450fb8b0599358efccdda3810145d/specs/architecture/competition-survey/mas-survey.md). It taxonomizes the MAS field into seven categories and profiles eight direct competitors (BMAD-METHOD, gstack, MetaGPT/MGX, CrewAI, OpenAI Symphony, Paperclip, Ruflo, GSD) plus nine adjacent projects.

**Genuine analytical value.** The per-competitor breakdown (what it is, philosophy, trust model, where it falls short, what's worth adopting) is technically argued rather than dismissive, and the "Ideas worth adopting" sections show honest reading. The architectural critique of GSD is the strongest piece: GSD's orchestrators are themselves LLM agents, so there is no hard trust boundary between orchestrator and subagent (LLM-on-LLM), versus Liza's deterministic Go supervisors (Go-on-LLM). That distinction is real and reusable independently of Liza.

**Two problems that disqualify it as a citable source.**

First, the taxonomy is built to produce a category of one. "Behavioral enforcement systems (Liza). One entry." and "Enterprise trust remains unsolved by everyone except Liza" are positioning claims, not survey findings. A classification whose seventh bucket contains only its author is a marketing artifact.

Second, and more measurable: **the survey understates every competitor's traction, always in the same direction.** Verified via `gh api` on 2026-07-15:

| Framework | Survey figure | Actual (2026-07-15) | Gap |
|-----------|---------------|---------------------|-----|
| gstack ([garrytan/gstack](https://github.com/garrytan/gstack)) | ~100.7k | 122,026 | -17% |
| Paperclip ([paperclipai/paperclip](https://github.com/paperclipai/paperclip)) | 14k, "just launched" | 73,770 | -81% |
| GSD ([gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)) | 37k | 64,742 | -43% |
| MetaGPT ([FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)) | 64k | 69,384 | -8% |
| CrewAI ([crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)) | 45k | 55,565 | -19% |
| BMAD ([bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)) | ~45.2k | 50,631 | -11% |
| Symphony ([openai/symphony](https://github.com/openai/symphony)) | "New" | 25,969 | n/a |
| Liza | "Early" | 322 | n/a |

Staleness explains part of it (the doc is dated March-May 2026 and was read on 2026-07-15), but not the uniform direction, and not the survey's own internal inconsistency: it dates gstack to 2026-05-22 while dating BMAD to 2026-04-20, comparing figures taken a month apart in a single matrix. The practical effect is that the "Stars: Liza = Early vs GSD = 37k" row understates the real gap, which is 322 against 64,742.

**Consequence for the guide**: use the survey as a lead list of projects to investigate, never as a source of figures or of competitive verdicts. Every number in this evaluation and in the guide sections it fed was re-derived from the GitHub API. This reinforces the "Medium confidence" verdict below rather than changing the 3/5 score, since the score already rested on architecture rather than on the author's claims.

---

## Recommendations

**Where to integrate**: `guide/workflows/spec-first.md`, section "Full-cycle AI software factories", as the OSS counterpoint to the four commercial products (done). No dedicated section given adoption (322 stars). Cross-reference its behavioral contract to the "constitution" concept already present in the guide (methodologies.md BMAD, agent-harness.md).

**Do not** re-list its satellite tools: rejected on 2026-06-10, decision unchanged.

**Side effect worth keeping (2026-07-15)**: reading the survey surfaced three genuine gaps in `guide/ecosystem/agentic-tools.md`, now filled with independently verified data: MetaGPT (§3.5), Symphony (§4.4), Paperclip (§4.5). That is the survey's real value to this repo, as a map of what we had not covered, not as a description of those projects.

---

## Challenge

**Objection tested**: "322 stars, single author, 6 months. Why 3/5 and not 2/5 like its satellites?"

**Answer**: The score does not reward adoption (which is low) but architectural uniqueness and teaching value. Liza is the only OSS project identified that implements the four governance pillars from the talk as one coherent system, with real deterministic code (35k LOC Go) rather than a collection of prompts. It serves as an existence proof: "here is what mechanical governance looks like". Its satellites were rejected because they duplicated Serena/grepai, already covered; the framework has no equivalent in the guide. The mention is framed explicitly as "reference architecture, not a dependency to adopt".

**Second objection (2026-07-15)**: "The survey's numbers are systematically self-serving. Does that not disqualify the whole project?"

**Answer**: No, because the score never rested on the survey. The architectural claims that justify 3/5 (Go supervisors, circuit breaker, behavioral contract) were verified against the repo and the project docs, not against the competitive doc. Skewed competitive marketing is common and says little about code quality. It does say the author's self-reported comparisons need independent checking, which is what the fact-check table below already assumed.

**Risk of not integrating**: a reader looking for "a concrete OSS example of a circuit breaker / deterministic supervisor for coding agents" would find nothing, while Liza exists and documents it.

---

## Fact-check

| Claim | Verified | Source/Comment |
|-------|----------|----------------|
| liza-mas/liza: 322 stars, 48 forks, Apache-2.0 | ✅ | `gh api repos/liza-mas/liza`, 2026-07-15 (320/47 on 2026-07-12) |
| Created 2026-01-17, pushed 2026-07-15 | ✅ | Same, active project |
| README: BMAD "~45.2k stars" | ❌ Understated | Actual: 50,631 (`gh api`, 2026-07-15) |
| README: CrewAI "45k stars" | ❌ Understated | Actual: 55,565 (`gh api`, 2026-07-15) |
| README: MetaGPT "64k stars" | ❌ Understated | Actual: 69,384 (`gh api`, 2026-07-15) |
| Survey: gstack "~100.7k", GSD "37k", Paperclip "14k" | ❌ All understated | Actual: 122,026 / 64,742 / 73,770 (`gh api`, 2026-07-15). See survey section above. |
| Survey: MetaGPT "no release since v0.8.1 (April 2024)" | ✅ | Confirmed: `gh api repos/FoundationAgents/MetaGPT/releases/latest` returns v0.8.1, 2024-04-22. Last commit January 2026. |
| Survey: Symphony "Apache 2.0 initially reported, some sources say MIT" | ✅ Apache-2.0 | `gh api`, 2026-07-15. The ambiguity is resolved, it is Apache-2.0. |
| "L4 Collaborative Agent Networks alongside BMAD and BEADS" | ❌ Not independent | The only support for this ranking is Liza's README. Attributed to **Soufiane Keli, VP Software Engineering at Octo Technology (Accenture)**, not IBM as an earlier search in this session suggested. A Perplexity deep-research (2026-07-12) independently confirms no formal L1-L5 model is published on the Octo blog or elsewhere by Keli; the L1-L5 frameworks actually published (metacto, nextagile, boye-co) are by other authors. This is a comment-level endorsement, not a benchmark. Do not cite as external validation. |
| Third-party community reception | ❌ None found | No dedicated Hacker News or Reddit thread (WebSearch 2026-07-12). The only activity is in the project's own GitHub Discussions. Confirms tiny adoption. |
| Author: Tangi Vass, Staff Data/Backend Engineer | ✅ | Confirmed by his Medium articles and the project docs (lizamas.mintlify.app) |
| Strict role separation (Coder never merges, Reviewer never implements) | ✅ Documented | README plus project docs; consistent with the deterministic supervisor claim, not audited in code |
| 55+ failure modes, 43+ validation rules, 35k LOC Go | ⚠️ Not audited | Taken from the README, not verified line by line |
| Provider compatibility (Gemini 2.5 Flash "incompatible") | ⚠️ Not tested | Self-reported by the author, no independent reproduction |
| Survey claim: ~200-line goal doc produced a full three-tier app in one run | ❌ Unverifiable | The survey itself states the supporting run artifacts live in a "non-public Diagnosis Design repo". Not citable. |

---

## Final decision

| Criterion | Value |
|-----------|-------|
| **Final score** | 3/5 |
| **Action** | ✅ Mention as reference architecture in spec-first.md (no dedicated section) |
| **Confidence** | Medium (architecture unique and verified via API plus docs; adoption, third-party reception and performance claims unproven, and the project's own competitive figures are demonstrably skewed) |
| **Suggested review** | In 3-6 months if adoption grows (raise to 4/5 on real traction plus third-party production feedback). Signals to watch: first substantial HN/Reddit thread, active forks other than the author's, one independent production report. |

### External sources (WebSearch 2026-07-12, GitHub API 2026-07-15)

- Official docs: [lizamas.mintlify.app](https://lizamas.mintlify.app/)
- Author articles (Tangi Vass, Medium): ["Behavior, Posture, Know-How"](https://medium.com/@tangi.vass/behavior-posture-know-how-the-three-layers-that-make-ai-agents-useful-d485388442eb), ["Turning AI Coding Agents into Senior Engineering Peers"](https://medium.com/@tangi.vass/turning-ai-coding-agents-into-senior-engineering-peers-c3d178621c9e), ["I Tried to Kill Vibe Coding"](https://medium.com/@tangi.vass/i-tried-to-kill-vibe-coding-i-built-adversarial-vibe-coding-without-the-vibes-bc4a63872440)
- Project genesis: [how-liza-grew-up.md](https://github.com/liza-mas/liza/blob/main/docs/how-liza-grew-up.md)
- Competitive survey: [mas-survey.md](https://github.com/liza-mas/liza/blob/24b35b90801450fb8b0599358efccdda3810145d/specs/architecture/competition-survey/mas-survey.md) (pinned commit; treat as a lead list, not a source)
- All primary sources are either the repository or the author. No independent third-party source (press, HN, Reddit, company report) found as of this date.

---

*Report generated manually for Claude Code Ultimate Guide v3.41.1*
