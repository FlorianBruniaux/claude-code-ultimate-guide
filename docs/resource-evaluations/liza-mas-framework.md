# Resource Evaluation: Liza (MAS framework)

**URL**: https://github.com/liza-mas/liza
**Type**: GitHub repository (framework)
**Evaluation date**: 2026-07-12 (source-code refresh 2026-08-28)
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.42.0

---

## Context: distinct from the earlier evaluation

On 2026-06-10, an evaluation ([`liza-mas-token-saving-cli-tools.md`](./liza-mas-token-saving-cli-tools.md)) rejected four **satellite tools** from the liza-mas org (scip-search, mdtoc, functional-clusters, stacklit-cli), all at 0-2 stars. Liza can use them through [optional toolchain profiles](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/support-docs/TOOLCHAIN.md), but does not require them: its [agent tool contract](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/contracts/AGENT_TOOLS.md) falls back to `rg`, `ast-grep`, and direct reads when an index or tool is unavailable. The earlier scores concern their standalone value to this guide. This evaluation covers a different object: **Liza the multi-agent framework itself** (`liza-mas/liza`), the Go orchestrator that can use those satellites. Author: Tangi Vass.

---

## Content summary

Liza is a spec-driven multi-agent coding system (MAS) with two modes (solo Pairing and Multi-Agent). Claimed hybrid architecture:

- **Deterministic Go supervisors** wrap each LLM agent and mechanically perform the critical actions (worktree management, merges, TDD enforcement, state transitions). Strict state machine, 43+ validation rules. Judgment stays with the agent.
- **Adversarial doer/reviewer pairs** on every activity (epic planning, user story writing, code planning, coding), PR-review style interaction until approval.
- **Behavioral contract**: 55+ documented LLM failure modes, each mapped to a countermeasure. Injected into every agent (the equivalent of a non-overridable "constitution").
- **Auditable YAML blackboard**: agent Kanban plus full historized state plus review comments.
- **Circuit breaker**: pattern detection (loops, repeated failures) triggers an automatic checkpoint. An explicit andon cord (stop-the-line).
- **Wraps provider CLIs, not their APIs**: uses the existing subscription (Claude Max, ChatGPT Pro). The pinned catalog defines nine adapters: Claude Code, Codex, Cursor, OpenCode, Gemini, Mistral, Kimi, Qwen, and Devin. Gemini and Mistral are disabled in that snapshot.
- 13 roles across 4 phases (spec, architecture, coding, integration). Isolated git worktrees. 35k LOC Go plus 92k of tests.

## Source-code refresh: 2026-08-28

The repository was cloned at commit [`a22c12381c5d884d2586a48aaaa517bca184f9cf`](https://github.com/liza-mas/liza/commit/a22c12381c5d884d2586a48aaaa517bca184f9cf), not evaluated from the README alone. The checkout contained 1,081 tracked files, 76,343 lines of non-test Go, 185,249 lines of Go tests, and 296 `_test.go` files. The README's older 35k/92k figures are therefore stale, not current size measurements.

Code and tests confirm the persistent YAML blackboard, file-locked state changes, lease and generation fencing, worktree isolation, forbidden task transitions, doer/reviewer submission and verdict flows, recovery operations, and supervised merge gates. The exact commit passed the upstream [Ubuntu](https://github.com/liza-mas/liza/actions/runs/33061917377/job/98482510741) and [macOS](https://github.com/liza-mas/liza/actions/runs/33061917377/job/98482510513) jobs on 2026-08-27. The suite was not executed locally because the review host did not have Go installed.

The refreshed classification is **repository harness plus adjacent control plane**, not runtime harness. Liza's [provider catalog](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/provider-catalog.yaml) invokes external coding-agent CLIs, which retain ownership of their inner model-and-tool loops. It also exposes the main security boundary: several adapters enable broad modes such as `--approve-all`, `--dangerously-skip-permissions`, or `--permission-mode dangerous`. Worktree isolation reduces git collisions but does not confine filesystem, credential, or network access.

Current GitHub metadata on 2026-08-28: 363 stars, 49 forks, Apache-2.0, latest release [v0.8.0](https://github.com/liza-mas/liza/releases/tag/v0.8.0) from 2026-06-03. Liza now has a dedicated [Agent Tools profile](../../guide/ecosystem/agentic-tools.md#48-liza) and appears as the fifteenth adjacent control plane in the [Agent Harness Map](../../guide/ecosystem/agent-harness-landscape.md#liza-a-repository-harness-and-control-plane-combined).

### Loop, graph, and responsibility refresh: 2026-08-29

Two private comparison notes from Tangi Vass prompted a second code pass focused on loop engineering, graph engineering, and the boundary between human and agent judgment. The useful claim survives, but in a narrower form than the notes propose.

The pinned [`pipeline.yaml`](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/internal/embedded/pipeline.yaml) is a stable organization graph: roles, doer/reviewer pairs, state vocabularies, quorums, and transitions. Runtime tasks plus dependencies form a changing work graph. The source therefore supports describing Liza as a domain-specific executable graph. It does not support calling Liza a general graph runtime: [`TransitionDef`](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/internal/pipeline/config.go) has source, destination, trigger, and cardinality, but no general edge schema, join policy, or arbitrary node program.

The code also sharpens the responsibility claim. Mechanical guards can reject illegal transitions, stale leases, missing dependencies, and unmet quorums. They cannot prove semantic correctness. Liza's own [architectural issues ledger](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/specs/architecture/architectural-issues.md) says cross-pair decomposition judgment is a consequential single gate, provider diversity is not enforced at verdict submission, and reviewer accuracy is unmeasured. Human availability is load-bearing for manual checkpoint runs, not for every execution path. In Multi-Agent mode, [`auto_resume`](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/support-docs/CONFIGURATION.md#auto-resume-auto_resume) automatically advances `CHECKPOINT` and `COMPLETED` states. In Pairing mode, [`yolo`](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/support-docs/ADVERSARIAL_PAIRING.md) pre-approves doer-side human prompts only; it does not waive reviewer approvals, validation, stop conditions, merge-conflict handling, or user stop instructions. Human authority therefore remains load-bearing for governance and irreversible effects even when live human availability is not an execution prerequisite.

The same applies to `capability × harnessability`. Harnessability is retained as a useful evaluation dimension, not a calibrated scalar. The guide now measures required-check completion, policy violations, recovery, false accepts, false rejects, interventions, wait time, and repeated-run cost for a specific model-harness pair.

An independent practitioner report was also found after the original evaluation. Hippolyte Durix's [Ippon case write-up](https://blog.ippon.fr/2026/04/29/premier-rex-multi-agent-liza/) records a small Spring Boot, Vue.js, and PostgreSQL catalog run with roughly 30 tasks, 5 automated sprints, 35 review verdicts, 3 corrected rejections, and 3 to 4 hours of human time. It also reports massive token consumption, manual planning validation, and no cross-provider reviewer test. This improves the evidence state from "no third-party report" to "one bounded practitioner report". It does not establish production readiness, comparative cost, or semantic correctness because the project was deliberately simple, figures are self-reported, and no comparable artifact-level baseline is published.

### Additional source: Agent Harness Landscape

On 2026-09-02, Liza maintainer Tangi Vass reviewed the [Agent Harness Landscape profile](../../guide/ecosystem/agent-harness-landscape.md#liza-a-repository-harness-and-control-plane-combined), classified its synthesis as accurate, and proposed three narrow refinements. The pinned repository supports all three:

1. **Provider enumeration.** The [provider catalog](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/provider-catalog.yaml) contains nine adapters, including Cursor. Gemini and Mistral are disabled in that snapshot.
2. **Permission-path scope.** Five adapters expose an opt-in ACP path with `--approve-all`, but only OpenCode and Devin use broad permission modes on their default CLI paths. Codex, Cursor, and Qwen use the broad flag only through ACP; Claude defaults to `--permission-mode auto`.
3. **Human availability.** Manual checkpoints require a live human when `auto_resume` is disabled. `auto_resume` can advance `CHECKPOINT` and `COMPLETED` automatically, while Pairing `yolo` pre-approves only doer-side prompts. Reviewer approval, validation, stop conditions, merge-conflict handling, and user stop instructions continue to apply. Human authority remains load-bearing for governance and irreversible effects.

These refinements do not change the repository-harness-plus-control-plane classification, the 3/5 score, or the evidence boundary between inspectable enforcement design and measured task effectiveness.

---

## Relevance score: 3/5

| Score | Meaning |
|-------|---------|
| ~~5~~ | ~~Critical, major gap in the guide~~ |
| ~~4~~ | ~~Highly relevant, significant improvement~~ |
| **3** | **Relevant, useful complement (as a reference architecture)** |
| ~~2~~ | ~~Marginal~~ |
| ~~1~~ | ~~Out of scope~~ |

**Rationale**: Liza is the most complete open-source match we have found for the governance pattern presented at the GenAI France meetup (Solario/Maleus, July 2026) and documented in `guide/workflows/spec-first.md` (section "Full-cycle AI software factories"). It mechanically answers the first three governance questions from that section, where OpenHands and spec-kitty cover only part. The value to the guide is architectural: a concrete implementation of mechanical governance rather than prompt-level governance. Its 363 stars and passing project CI are adoption and maintenance signals, not independent production validation.

---

## Cross-check against the four governance pillars (spec-first.md)

| Governance pillar (Solario/Maleus talk) | Liza | OpenHands (already covered) | spec-kitty (already covered) |
|------------------------------------------|------|------------------------------|------------------------------|
| 1. Deterministic gate vs LLM self-assessment | ✅ Go supervisors enforce state/merge/TDD | ⚠️ Automated merge but no code-enforced supervisor | ⚠️ Human review, no code gate |
| 2. Stop-the-line (andon cord) | ✅ Explicit circuit breaker | ❌ Not documented | ❌ Not documented |
| 3. Traceability / audit trail | ✅ Historized YAML blackboard | ⚠️ Cloud/Enterprise only | ✅ Merge audit trail |
| 4. Spec stays authoritative | ⚠️ Human-driven Spec Evolution Protocol, audited but not code-enforced | ❌ | ⚠️ Versioned specs |

It is the only one of the three OSS projects to document a circuit breaker (pillar 2), the point flagged as "few platforms document it explicitly" in spec-first.md.

Liza's pinned [Spec Evolution Protocol](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/specs/protocols/sprint-governance.md#spec-evolution-protocol) defines change triggers, blocks affected tasks, requires a spec changelog and `spec_updated` activity-log entry, assesses impact, then resumes the tasks. This is a procedural long-term synchronization mechanism. The repository does not show that these steps are code-enforced, and its [architectural issues ledger](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/specs/architecture/architectural-issues.md#spec-corpus-lacks-lifecycle-management) still records missing automated lifecycle and staleness controls.

---

## The project's own competitive survey (added 2026-07-15)

Liza ships a 660-line competitive survey at [`specs/architecture/competition-survey/mas-survey.md`](https://github.com/liza-mas/liza/blob/24b35b90801450fb8b0599358efccdda3810145d/specs/architecture/competition-survey/mas-survey.md). It taxonomizes the MAS field into seven categories and profiles eight direct competitors (BMAD-METHOD, gstack, MetaGPT/MGX, CrewAI, OpenAI Symphony, Paperclip, Ruflo, GSD) plus nine adjacent projects.

**Genuine analytical value.** The per-competitor breakdown (what it is, philosophy, trust model, where it falls short, what's worth adopting) is technically argued rather than dismissive, and the "Ideas worth adopting" sections show honest reading. The architectural critique of GSD is the strongest piece: GSD's orchestrators are themselves LLM agents, so there is no hard trust boundary between orchestrator and subagent (LLM-on-LLM), versus Liza's deterministic Go supervisors (Go-on-LLM). That distinction is real and reusable independently of Liza.

**Three limitations that disqualify it as a citable source for competitive verdicts.**

First, the taxonomy is built to produce a category of one. "Behavioral enforcement systems (Liza). One entry." and "Enterprise trust remains unsolved by everyone except Liza" are positioning claims, not survey findings. A classification whose seventh bucket contains only its author is a marketing artifact.

Second, the traction figures do not form one comparable snapshot. Every numeric competitor figure checked through `gh api` on 2026-07-15 was lower than the API count observed that day, but the survey assigns different as-of dates to its rows. Liza's own qualitative "Early" entry had also moved from 322 to 336 stars by 2026-07-28:

| Framework | Survey figure | Actual (2026-07-15) | Actual (2026-07-28) | Gap |
|-----------|---------------|---------------------|-----|-----|
| gstack ([garrytan/gstack](https://github.com/garrytan/gstack)) | ~100.7k | 122,026 | 124,807 | -17% |
| Paperclip ([paperclipai/paperclip](https://github.com/paperclipai/paperclip)) | 14k, "just launched" | 73,770 | 74,902 | -81% |
| GSD ([gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)) | 37k | 64,742 | 64,798 | -43% |
| MetaGPT ([FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)) | 64k | 69,384 | 69,538 | -8% |
| CrewAI ([crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)) | 45k | 55,565 | 56,233 | -19% |
| BMAD ([bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)) | ~45.2k | 50,631 | 51,183 | -11% |
| Symphony ([openai/symphony](https://github.com/openai/symphony)) | "New" | 25,969 | 26,265 | n/a |
| Liza | "Early" | 322 | 336 | n/a |

Repository star counts are cumulative and usually rise, so a stale sample often falls below a later observation; counts can also fall. The uniform direction in this sample does not establish systematic bias or intent. The substantive defect is dating gstack to 2026-05-22 and BMAD to 2026-04-20, then comparing them in one matrix without a common as-of date. The practical effect is that the "Stars: Liza = Early vs GSD = 37k" row cannot serve as a current comparison. At the 2026-07-15 check, the corresponding counts were 322 and 64,742.

Third, the survey's "Code Quality Evidence" section reports a Claude Code Opus 4.6 assessment generated and published by the project, including an A grade and six five-star subsystem ratings. This is internal qualitative feedback, not independent evidence or a reproducible benchmark. Its quantitative snapshot is also stale against the pinned review: 27,926 lines of production Go in the assessment versus 76,343 at `a22c123`. The project's own issues ledger separately records contract-effectiveness self-certification as an open concern. The section should be labelled as an internal self-assessment with its date, scope, and method, or replaced by independently reproducible measurements before supporting comparative code-quality claims.

**Consequence for the guide**: use the survey as a lead list of projects to investigate, never as a source of figures or of competitive verdicts. Every number in this evaluation and in the guide sections it fed was re-derived from the GitHub API. This preserves the confidence boundaries below and does not change the 3/5 score, since the score already rested on architecture rather than on the author's claims.

---

## Recommendations

**Where integrated**: the original mention remains in `guide/workflows/spec-first.md` as the OSS counterpoint to commercial software factories. The 2026-08-28 refresh adds a dedicated evidence-pinned profile to `guide/ecosystem/agentic-tools.md`, a classified row and boundary note to the Agent Harness Map, and focused cross-references from architecture, evaluation, and security. This wider treatment follows from the new source-code evidence, not from the small increase in stars.

**Do not** re-list its satellite tools: rejected on 2026-06-10, decision unchanged.

**Side effect worth keeping (2026-07-15)**: reading the survey surfaced three genuine gaps in `guide/ecosystem/agentic-tools.md`, now filled with independently verified data: MetaGPT (§3.5), Symphony (§4.4), Paperclip (§4.5). That is the survey's real value to this repo, as a map of what we had not covered, not as a description of those projects.

---

## Challenge

**Objection tested**: "363 stars and no independent production report. Why 3/5 and not 2/5 like its satellites?"

**Answer**: The score does not reward adoption (which is low) but architectural uniqueness and teaching value. Liza is the only OSS project identified that mechanically answers the first three governance questions from the talk as one coherent system, with 76,343 lines of non-test Go at the reviewed commit rather than a collection of prompts. It serves as an existence proof: "here is what mechanical governance looks like". Its satellites were rejected because they duplicated Serena/grepai, already covered; the framework has no equivalent in the guide. The mention is framed explicitly as "reference architecture, not a dependency to adopt".

**Second objection (reassessed 2026-09-01)**: "The survey's dated comparisons are unreliable. Does that disqualify the whole project?"

**Answer**: No, because the score never rested on the survey. The architectural claims that justify 3/5 (Go supervisors, circuit breaker, behavioral contract) were verified against the repo and the project docs, not against the competitive document. Mixed as-of dates and an internal LLM assessment make the comparisons unsuitable as independent evidence. They do not establish the author's intent or a systematic bias.

**Risk of not integrating**: a reader looking for "a concrete OSS example of a circuit breaker / deterministic supervisor for coding agents" would find nothing, while Liza exists and documents it.

---

## Fact-check

| Claim | Verified | Source/Comment |
|-------|----------|----------------|
| liza-mas/liza: 363 stars, 49 forks, Apache-2.0 | ✅ | GitHub API, 2026-08-28; previous snapshots retained in the historical comparison above |
| Created 2026-01-17, pushed 2026-07-15 | ✅ | Same, active project |
| README: BMAD "~45.2k stars" | ⚠️ Lower than later snapshot | Actual: 50,631 on 2026-07-15, then 51,183 on 2026-07-28 |
| README: CrewAI "45k stars" | ⚠️ Lower than later snapshot | Actual: 55,565 on 2026-07-15, then 56,233 on 2026-07-28 |
| README: MetaGPT "64k stars" | ⚠️ Lower than later snapshot | Actual: 69,384 on 2026-07-15, then 69,538 on 2026-07-28 |
| Survey: gstack "~100.7k", GSD "37k", Paperclip "14k" | ⚠️ Lower than later snapshot | Actual: 122,026 / 64,742 / 73,770 on 2026-07-15; then 124,807 / 64,798 / 74,902 on 2026-07-28 |
| Survey: MetaGPT "no release since v0.8.1 (April 2024)" | ✅ | Confirmed: `gh api repos/FoundationAgents/MetaGPT/releases/latest` returns v0.8.1, 2024-04-22. Last commit January 2026. Stars: 69,384 then, 69,538 now as of 2026-07-28 |
| Survey: Symphony "Apache 2.0 initially reported, some sources say MIT" | ✅ Apache-2.0 | `gh api`, 2026-07-15. The ambiguity is resolved, it is Apache-2.0. Stars: 25,969 then, 26,265 now as of 2026-07-28 |
| "L4 Collaborative Agent Networks alongside BMAD and BEADS" | ❌ Not independent | The only support for this ranking is Liza's README. Attributed to **Soufiane Keli, VP Software Engineering at Octo Technology (Accenture)**, not IBM as an earlier search in this session suggested. A Perplexity deep-research (2026-07-12) independently confirms no formal L1-L5 model is published on the Octo blog or elsewhere by Keli; the L1-L5 frameworks actually published (metacto, nextagile, boye-co) are by other authors. This is a comment-level endorsement, not a benchmark. Do not cite as external validation. |
| Third-party practitioner evidence | ⚠️ One bounded report | [Ippon, 2026-04-29](https://blog.ippon.fr/2026/04/29/premier-rex-multi-agent-liza/): small catalog project, ~30 tasks, 5 sprints, 35 verdicts, 3 corrected rejections, 3 to 4 human hours, massive token use. Useful REX, not a production or comparative benchmark. |
| Author: Tangi Vass, Staff Data/Backend Engineer | ✅ | Confirmed by his Medium articles and the project docs (lizamas.mintlify.app) |
| Strict role separation (Coder never merges, Reviewer never implements) | ✅ Documented | README plus project docs; consistent with the deterministic supervisor claim, not audited in code |
| 55+ failure modes and 43+ validation rules | ⚠️ Not exhaustively audited | README counts; representative state, lease, recovery, worktree, review, and merge mechanisms were inspected in source and tests at `a22c123` |
| 76,343 non-test Go LOC, 185,249 Go test LOC, 296 Go test files | ✅ | Counted from the cloned tracked files at `a22c123`, 2026-08-28 |
| Provider compatibility (Gemini 2.5 Flash "incompatible") | ⚠️ Not tested | Self-reported by the author, no independent reproduction |
| Survey claim: ~200-line goal doc produced a full three-tier app in one run | ❌ Unverifiable | The survey itself states the supporting run artifacts live in a "non-public Diagnosis Design repo". Not citable. |

---

## Final decision

| Criterion | Value |
|-----------|-------|
| **Final score** | 3/5 |
| **Action** | Mention in Spec-First, Agent Harness Map, Agent Harness Engineering, Agent Tools, Agent Evaluation, and Security Hardening |
| **Confidence** | Medium-high for architecture and classification; low for production outcomes and independent adoption evidence |
| **Suggested review** | In 3-6 months if adoption grows (raise to 4/5 on real traction plus third-party production feedback). Signals to watch: first substantial HN/Reddit thread, active forks other than the author's, one independent production report. |

### External sources (updated 2026-08-29)

- Official docs: [lizamas.mintlify.app](https://lizamas.mintlify.app/)
- Author articles (Tangi Vass, Medium): ["Behavior, Posture, Know-How"](https://medium.com/@tangi.vass/behavior-posture-know-how-the-three-layers-that-make-ai-agents-useful-d485388442eb), ["Turning AI Coding Agents into Senior Engineering Peers"](https://medium.com/@tangi.vass/turning-ai-coding-agents-into-senior-engineering-peers-c3d178621c9e), ["I Tried to Kill Vibe Coding"](https://medium.com/@tangi.vass/i-tried-to-kill-vibe-coding-i-built-adversarial-vibe-coding-without-the-vibes-bc4a63872440)
- Project genesis: [how-liza-grew-up.md](https://github.com/liza-mas/liza/blob/main/docs/how-liza-grew-up.md)
- Competitive survey: [mas-survey.md](https://github.com/liza-mas/liza/blob/24b35b90801450fb8b0599358efccdda3810145d/specs/architecture/competition-survey/mas-survey.md) (pinned commit; treat as a lead list, not a source)
- Independent practitioner report: [Hippolyte Durix, Ippon, "Du PDD au multi-agent : mon premier REX avec Liza"](https://blog.ippon.fr/2026/04/29/premier-rex-multi-agent-liza/)
- Related practitioner and research framing: [Loop Engineering](https://addyo.substack.com/p/loop-engineering), [Own the Outer Loop](https://addyo.substack.com/p/own-the-outer-loop), [LangGraph Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [Graph Engineering](https://arxiv.org/abs/2608.21156), and [What Makes Prompts a Graph](https://arxiv.org/abs/2607.27578)

---

*Report refreshed from a local clone for Claude Code Ultimate Guide v3.42.0.*
