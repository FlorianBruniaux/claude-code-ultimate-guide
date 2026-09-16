# Inside OpenAI's agentic software factory (Pragmatic Engineer, Sep 2026)

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [Inside OpenAI's agentic software factory](https://newsletter.pragmaticengineer.com/p/openai-software-factory) |
| Author | Gergely Orosz, The Pragmatic Engineer |
| Published | 2026-09-15 |
| Evaluated | 2026-09-16 |
| Resource type | Third-party journalist account sourced to seven named first-party engineers |
| Access | Paywalled after section 3. Sections 1 to 3, including the full pipeline description and the diagram, are in the free preview |
| Related | [OpenAI Harness Engineering](./2026-02-11-openai-harness-engineering.md) (same company, greenfield project, Feb 2026); [Anthropic CI test impact analysis](./2026-09-14-anthropic-ci-test-impact-analysis.md) (same bottleneck, competitor's infrastructure) |
| Decision | Integrate |
| Score | 4/5 |

## Verdict

The guide documents the agentic software factory up to the pull request and stops there. `guide/workflows/agentic-software-factories.md` describes six levels of orchestration, every one of which ends at a merged PR. A grep across `guide/` returns zero hits for incident-response agents, latency-regression agents, and per-change deployment agents that build their own dashboards. This article is the first dated operator account that names all three as running systems, with a named owner for each stage, which makes the missing half of the factory documentable rather than speculative.

The score stops at 4/5 for three reasons, each of which constrains how the material can be cited.

First, the article publishes velocity and publishes no quality. Roughly 10x load increase on delivery systems in six months, PRs per engineer on a hockey stick, 0% to 90% Codex adoption across non-engineering orgs in four months. There is no defect rate, no change failure rate, no rollback count, no incident count, and no escaped-defect figure anywhere in it. A factory that measures only its throughput is describing half of its own performance, and every number below is scoped accordingly.

Second, every figure is self-reported by OpenAI to a journalist, with no published counting methodology. "10x load on some systems" does not say which systems or against which baseline. These are operator statements, not measurements a reader can audit.

Third, the diagram circulating from this article is Gergely Orosz's editorial rendering, watermarked by The Pragmatic Engineer. It is not an OpenAI internal artifact. Readers who critique the architecture from the shape of the diagram are critiquing a journalist's summary. The guide cites the body text, never the diagram alone.

## Verified facts used for integration

Only the facts below are cited anywhere they are used in the guide. Each is attributed to the named speaker in the article.

**Pipeline stages, as described in the body text** (Venkat Venkataramani, VP Engineering Applied Infra, unless noted):

1. A human defines the desired outcome. Judgment, prioritization and taste move to this stage. Venkat states that engineers at OpenAI are becoming more like product managers than traditional systems engineers.
2. Codex gathers context. OpenAI moved its documentation inside the source code. Codex also reads Git and GitHub, Slack, Notion, internal data sources including Databricks and Datadog, and internal Codex skills, some of which are maintained by Codex itself. New engineers are directed to ask Codex during onboarding.
3. Codex implements changes and verifies the software works.
4. Build and test, then CI. The agent builds, runs tests, fixes what it breaks, opens a PR, then babysits the PR until CI is green, fixing failures and updating the PR itself. A separate perf harness routes problematic PRs to a Synthetics A/B framework for performance evaluation.
5. Agentic code review. Multiple agents, each with a domain-specialist configuration (data, infra, cloud, security), review in parallel. Changes are classified by risk: high-risk changes invoke more reviews or mandate a human reviewer after the agents finish; areas of the codebase can opt in to an agent that auto-approves low-risk PRs. The coding agent babysits the review comments and updates the PR.
6. Agentic deploy. After a human approves a change for production, the change is assigned an agent instructed to handhold it until it is safely and fully rolled out. For a feature-flag change, the agent locates the flag in the codebase, works out what the change does, decides which signals indicate success and failure, builds its own monitoring dashboard, and watches production signals. The stated long-term goal is a per-change autonomous SRE.
7. Observe production, using agent-generated dashboards plus OpenAI's internal observability stack. Venkat notes the change since the previous visit: engineers used to create dashboards per service, agents now create them at per-change deployment granularity.
8. Perf Factory. Agents sift alerts and dashboards, de-duplicate signals, identify real latency regressions, root-cause them and propose fixes, which re-enter the pipeline at the Codex stage.
9. Sevbot, the internal incident-response agent, built on Codex. On incident detection it collects context, determines possible mitigations but never executes any, and answers engineers' questions in the Slack channel. An engineer can tell it to apply a specific mitigation. The stated goal is autonomous mitigation of routine outages so nobody is woken outside working hours. On-call duty is explicitly stated to still exist.

**Load and scaling** (Venkat): roughly a 10x increase in load on some systems, described as growth that would take two or three years at most companies and took about six months at OpenAI. Version control, CI/CD and production release processes are all named as pressure points. He states that every month brings a new set of infrastructure scaling challenges.

**Stated position on PRs and code review** (Venkat, quoted): "the way we do code review today makes less and less sense, and the same is true for pull requests."

**The journalist's own recorded skepticism, and its answer** (Gergely Orosz, in an editorial note): he was skeptical that an agent told to be a cloud infra specialist would produce a different review from a generic agent. His stated resolution is that all Codex agents have full access to OpenAI's code and docs, so the specialist agent has gathered context about the cloud infra setup, and that what matters is how these agents are set up, the context they access, and their focus on one domain to make best use of a limited context window.

**Adoption** (Andrew Ambrosino, Desktop lead, and Akshay Nathan, Engineering Lead Productivity): non-engineering orgs including finance, recruitment and legal went from roughly 0% to 90% Codex usage over a four-month period. The Codex app shipped for Mac in February 2026 and Windows in March 2026; ChatGPT Work shipped in July 2026. OpenAI's internal Codex is stated to be more advanced than the external product because it is plugged into internal systems. Usage went from 60% to 90% between April and May, attributed to improved handling of long-running tasks and a `/goal` setting.

**The mobile bottleneck** (Sulman Choudhry, Head of Engineering ChatGPT): app store approval takes hours or days per update, which he describes as already painful and expected to worsen, with no solution in place today.

**Explicitly not claimed by the article**: any defect, escape, rollback, change-failure or incident rate; any comparison against a non-agentic baseline; any independent verification of any figure; any statement that low-risk auto-approved PRs have the same defect profile as human-reviewed ones.

## Comparison with existing guide coverage

| Aspect | Article | Guide before this integration | Action |
|---|---|---|---|
| Post-merge factory stages (deploy, observe, incident) | Stages 6 to 9, all named and owned | Absent. All six levels in `agentic-software-factories.md` end at the merged PR. Zero grep hits for incident-response or latency-regression agents | New section 6 in `agentic-software-factories.md` |
| Per-change deployment agent that builds its own dashboard | Described as running, with the stated per-change granularity change | Absent. The nearest neighbour is the ephemeral per-worktree observability stack in the Feb 2026 harness-engineering evaluation | Covered in the new section, with the retention question flagged as unanswered |
| Risk classification as review routing | Explicit: high-risk gets more agents plus a mandated human, low-risk areas can opt into agent auto-approval | `agent-harness.md` §4 and `ai-roles.md` mention agentic code review; no risk-tiered routing, no auto-approval tier | Covered in the new section |
| Domain-specialist reviewers: persona or context? | The journalist raises the objection and answers it with context scoping, not persona prompting | The guide's standing position is that context beats persona, but it has no operator account stating it | Cite as supporting evidence for the existing position |
| Incident agent that mitigates but never remediates | Sevbot proposes, never executes; a human triggers any mitigation | Absent | Covered, and named as the one loop OpenAI does not close |
| Delivery infrastructure buckling under agent volume | 10x load in six months, self-reported | `agentic-software-factories.md` §5 already documents this from Anthropic's side (25x CI jobs, single-writer rewrite) and from a source-level audit (Fusion) | Add as a second operator datapoint, explicitly scoped, in the existing §5 |
| Velocity published without quality | Total absence of defect metrics | §5 already argues the trap in general terms | Use as the cleanest available illustration |

## Fact-check

| Claim | Verified against |
|---|---|
| Title, author, publication date 2026-09-15, paywall boundary after section 3 | Direct fetch of the public URL, 2026-09-16. Sections 1 to 3 confirmed present in the free preview, sections 4 to 7 confirmed inaccessible |
| The nine-stage pipeline, Perf Factory, and Sevbot are in the free preview, not behind the paywall | Same fetch. The preview lists the nine-stage sequence, Perf Factory's role in latency regressions, and Sevbot's incident-response role with the autonomous-mitigation goal |
| All stage descriptions, quotes and figures above | The article body as supplied in full, cross-checked against the free preview for the portions it covers |
| The circulating diagram is the journalist's rendering, not an OpenAI artifact | The image carries The Pragmatic Engineer watermark and is captioned as the article's own illustration |
| `guide/` has no coverage of incident-response agents, perf-regression agents or per-change deploy agents | `grep -rli` for each term across `guide/`, run 2026-09-16, zero matches |
| Anthropic's independent account of the same CI bottleneck | [`2026-09-14-anthropic-ci-test-impact-analysis.md`](./2026-09-14-anthropic-ci-test-impact-analysis.md), already integrated |

## Documentation placement

- `guide/workflows/agentic-software-factories.md`, new section 6, "The half of the factory that runs after the merge". The page's six levels all stop at the PR; this closes that gap and keeps the page's editorial stance, which is that a stage is only real when you can name who owns the gate.
- `guide/workflows/agentic-software-factories.md` §5, two sentences adding OpenAI as a second operator datapoint alongside Anthropic's CI account.
- `machine-readable/reference.yaml` and `mcp-server/content/reference.yaml`: one `deep_dive` key for the new section.

## Rejected

**A dedicated page.** The material is one company's pipeline, not a general pattern with multiple independent implementations. A section inside the existing orientation map carries it, and the orientation map is where a reader asking "where does my factory stop?" already is.

**The adoption figures as evidence of anything transferable.** 0% to 90% Codex adoption among lawyers and recruiters at the company that builds Codex is not a datapoint about tool adoption anywhere else. Excluded from the integration.

**Any use of the diagram as an architecture reference.** It is a journalist's summary of an interview. Several of its apparent omissions, notably the absence of a feedback arrow from human code review, are contradicted by the body text, which states that the coding agent babysits review comments and updates the PR.
