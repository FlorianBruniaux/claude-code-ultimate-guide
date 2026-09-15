# Agentic coding is straining CI: test impact analysis at Anthropic

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [Agentic coding is straining CI: here's how we scaled test impact analysis at Anthropic](https://claude.com/blog/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic) |
| Author | Sachin Malhotra, Anthropic |
| Published | 2026-09-14 |
| Evaluated | 2026-09-15 |
| Companion posts | [The AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) (already evaluated: [2026-08-26-anthropic-ai-native-sdlc-playbook.md](./2026-08-26-anthropic-ai-native-sdlc-playbook.md)); [AI CI/CD on-call](https://claude.com/blog/ai-ci-cd-on-call); [How Anthropic secures its AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle) |
| Resource type | Official first-party operator account (Anthropic engineering blog) |
| Decision | Integrate |
| Score | 4/5 |

## Verdict

`grep -rli "test impact analysis\|test selection" guide/` returns zero hits: the mechanism the article describes, a deterministic service that decides which tests run on each PR based on past results and package relevance, is entirely absent from the guide despite CI/CD agentic patterns already having a dedicated section (`guide/core/agent-harness.md#4-cicd-agentic-patterns`). That is a real gap, not a marginal one, and the source is a dated, first-party operator account rather than marketing copy: it names a concrete architecture (listener/selector split), a concrete failure mode (single-writer bottleneck under concurrent CI), a concrete fix (stateless journal, horizontal scaling), and states plainly which of its own techniques are not the insight.

The score stops at 4/5, not 5/5, for two reasons. First, the headline scale numbers (8x code shipped per quarter, 80% of code authored by Claude, tests grown 10x, CI jobs up 25x in six months) come from a single company with no published counting methodology, so they describe Anthropic's own trajectory, not an industry baseline. Second, the article measures its fix against one proxy, the hourly-max backlog of queued unprocessed job-result events going from a growing backlog to flat. It does not report an effect on change lead time, developer wait time, or CI cost, so "it worked" is demonstrated for the metric they chose to show, not for outcomes a reader might assume it implies.

## Verified facts used for integration

Only the facts below are cited anywhere they are used in the guide. No number is extrapolated or averaged.

**Scale, explicitly scoped to Anthropic and explicitly not arithmetically related** (the article's own parenthetical: not every test runs on every PR):
- Anthropic engineers ship 8x as much code per quarter as they did from 2021-2025.
- Claude authors 80% of that code and plays a large role in review and approval.
- Tests across the codebase grew 10x with "a nominal amount of engineers" added, and CI jobs grew 25x over a six-month period.
- Activity floor is raised by agents pushing overnight and on weekends, but stays bursty because human engineers still drive and approve a significant share of PRs.

**Why this matters specifically for agents** (the article's stated reason, not an inference): humans are good at recognizing which test failures don't apply to their change; agents need more context and direction, and a specific, valid set of tests lets them self-verify and iterate.

**v0 architecture and its failure mode**: a listener records CI test results; a selector reads that history to decide what runs on new PRs; both ran as a single process because a running per-test history needs a single writer, which is what blocked horizontal sharding. When the listener falls behind the PR queue: a bad merged change fails a test for everyone (multiple unnecessary investigations), a flaking dependency produces flaky reds that block merges, and a fixed or newly added test does not run until the listener catches up (regression risk). Quantified: 20 minutes of listener lag can mean tens of thousands of test updates not applied to the selector. An internal Claude Tag instance paged the author whenever listener lag exceeded 50,000 jobs behind.

**Patch sequence before the rewrite, each with its stated lifespan**: doubling the cores bought 70 days; sharding in February bought 29 days ("we didn't realize it would only buy us 29 days"); daily restarts in March, once the process hit its memory limit by mid-afternoon most weekdays, bought less than a day. Memory debugging found only four bugs, swapping the allocator did nothing, and profiling the loaded singleton further was judged too risky.

**The rewrite**: an in-memory data store where any listener worker can process any result, append it to a journal, and move on without holding state, stateless and horizontally scalable. A small consumer process rolls the journal into per-test history every few seconds for the selector to query. No database product is named, no latency SLO is published. Stated tradeoff: more expensive to run, easier to scale and memory-profile than a shaky singleton.

**Outcome shown**: a chart caption reporting the hourly-max backlog of queued unprocessed job-result events went from a growing weekly backlog to flat after cutover and tuning. No lead-time or cost metric is reported.

**Declared, not measured, project cost**: three weeks for a single engineer; a year ago, the author estimates it would have taken closer to a quarter. This is a stated estimate, not a measured duration, and is treated as such everywhere it is cited.

**Closing advice, quoted**: "assume your architecture will be at a 25x load within two quarters"; budget allowing, design v0 for 10-20x perceived scale; instrument so jobs in equals jobs out; keep state out of the process from the start; avoid running a critical service as a single instance unless you can measure it and any canary changes.

**Explicit caveats from the article itself**: stale selector data did not ship untested code, it mostly meant running tests that were already flaky or widespread-failing; the specific scaling techniques (bigger machine, sharding, restarts) are explicitly not the insight to take away; ownership was murky because no team wanted to own another piece of infrastructure and the CI team had bigger priorities.

## Comparison with existing guide coverage

| Aspect | Article | Guide before this integration | Action |
|---|---|---|---|
| Test impact analysis / test selection as a named mechanism | Central to the article | Absent (`grep` confirms zero hits) | Add as a subsection in `agent-harness.md` §4 |
| Why agents specifically need deterministic test selection (vs. humans triaging failures) | Explicit, quoted reasoning | Not covered | Lead the new subsection with this reasoning |
| AI-driven code volume as a downstream CI bottleneck, with a first-party datapoint | 10x tests / 25x CI jobs / nominal headcount | `team-metrics.md` already argues flat deployment frequency signals a downstream bottleneck, with no operator datapoint | Add the datapoint as supporting evidence, explicitly scoped |
| Verification infrastructure breaking under agent-driven velocity, as opposed to code quality breaking | 70/29/less-than-1-day patch sequence before a rewrite | `agentic-software-factories.md` §5 documents the same trap from a source-level code audit (Fusion) | Add as a from-the-inside counterpoint, same trap, different failure surface |

## Fact-check

| Claim used in this evaluation or in the integration | Verified against |
|---|---|
| All scale, architecture, failure-mode, patch-sequence, rewrite, outcome and advice claims listed above | Direct quotation or close paraphrase of the source article, 2026-09-14 |
| `guide/` has no existing "test impact analysis" or "test selection" coverage | `grep -rli "test impact analysis\|test selection" guide/`, run 2026-09-15, zero matches |
| Companion posts and their guide status | URLs confirmed live; SDLC playbook companion already integrated per `docs/resource-evaluations/2026-08-26-anthropic-ai-native-sdlc-playbook.md`; the other two companions (`ai-ci-cd-on-call`, `how-anthropic-secures-its-ai-native-software-development-lifecycle`) are referenced here as context only and are not separately fact-checked or integrated in this pass |

## Documentation placement

- `guide/core/agent-harness.md`, new subsection "Test Selection as an Agent Primitive" in section 4 (CI/CD Agentic Patterns).
- `guide/ops/team-metrics.md`, three to five lines after the Deployment Frequency paragraph in "DORA in an AI-Augmented Context", as a scoped operator datapoint plus dimensioning heuristic, not a benchmark.
- `guide/workflows/agentic-software-factories.md`, section 5 ("The unbounded velocity trap"), a short counterpoint paragraph: the same trap observed from inside a company's own verification infrastructure rather than from a third-party code audit.
- `machine-readable/reference.yaml` and `mcp-server/content/reference.yaml`: `deep_dive` key for the new agent-harness subsection.

## Rejected

A dedicated guide page for test impact analysis. The mechanism is narrow enough, and tightly enough coupled to the existing CI/CD Agentic Patterns section, that a subsection carries it without creating a new file the index has to maintain separately.
