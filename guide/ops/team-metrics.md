---
title: "Team Metrics for AI-Augmented Engineering"
description: "How to measure and pilot a tech-product team using AI. DORA, SPACE, and the metrics that matter when AI writes 70%+ of your code."
tags: [guide, metrics, dora, space, team, observability, ai-augmented]
---

# Team Metrics for AI-Augmented Engineering

> Velocity is easy to measure and easy to misread. AI raises the bar for what "moving fast" even means.

## Table of Contents

1. [The Measurement Problem](#the-measurement-problem)
2. [The DORA Foundation](#the-dora-foundation)
3. [DORA in an AI-Augmented Context](#dora-in-an-ai-augmented-context)
4. [Beyond DORA: The SPACE Framework](#beyond-dora-the-space-framework)
5. [AI-Specific Metrics](#ai-specific-metrics)
6. [Agentic Metrics: What DORA Doesn't Measure](#agentic-metrics-what-dora-doesnt-measure)
7. [Product Metrics (the often-missing layer)](#product-metrics-the-often-missing-layer)
8. [By Team Size](#by-team-size)
9. [Vanity Metrics to Drop](#vanity-metrics-to-drop)
10. [The 4-Question Test](#the-4-question-test)
11. [Tooling](#tooling)
12. [Probabilistic Delivery Forecasting](#probabilistic-delivery-forecasting)
13. [Implementation Roadmap](#implementation-roadmap)
14. [Reporting Delivery Capacity to a Skeptical Board](#reporting-delivery-capacity-to-a-skeptical-board)
15. [See Also](#see-also)

---

## The Measurement Problem

AI-assisted development changes delivery speed fast enough to break most existing benchmarks. A team shipping 2 features per sprint in 2022 might now ship 6, with AI generating 70-90% of the code. That looks like a win on every traditional scorecard, and it might genuinely be one — or the velocity is hiding shallow reviews, skill atrophy, and a growing pile of AI-generated technical debt that nobody fully understands.

The core tension: activity metrics spike immediately when you adopt AI tools, but quality and long-term maintainability signals are slower and harder to track. Sprint velocity, commits per day, and lines written all go up. Bug escape rate, time-to-understand a PR, and developer confidence are harder to wire up but far more informative.

This page gives engineering managers, tech leads, and CTOs a practical measurement stack — starting from the DORA foundation, layering in human factors via SPACE, then adding the AI-specific signals that the standard frameworks don't cover.

---

## The DORA Foundation

DORA (DevOps Research and Assessment) measures the health of your delivery system, not individual contributors. That distinction matters: it keeps metrics conversations focused on process improvement rather than surveillance. It's also the most validated framework in the field, backed by years of research across thousands of organizations.

The four core metrics:

### Deployment Frequency

**What it measures**: How often you deploy to production (or release to end users).

**How to measure**: Count production deployments per day, week, or month. Most CI/CD tools expose this directly (GitHub Actions, CircleCI, Vercel, etc.).

**2024 benchmarks**:

| Tier | Frequency |
|------|-----------|
| Elite | Multiple times per day |
| High | Once per day to once per week |
| Medium | Once per week to once per month |
| Low | Less than once per month |

**Common pitfall**: Teams conflate "deployment" with "release." If you deploy to prod but hide behind feature flags, the metric looks good but customer value isn't delivered. Track both deployment frequency and feature flag rollout cadence if your team uses flags heavily.

---

### Lead Time for Changes

**What it measures**: Time from a code commit to that code running in production.

**How to measure**: Timestamp at commit, timestamp at deployment. The delta is your lead time. Tools like LinearB and Faros.ai automate this from your CI/CD pipeline.

**2024 benchmarks**:

| Tier | Lead Time |
|------|-----------|
| Elite | Less than 1 hour |
| High | 1 hour to 1 week |
| Medium | 1 week to 1 month |
| Low | More than 6 months |

**Common pitfall**: Lead time measures calendar time, not active work time. A PR that sits in review for 3 days has 3 days of lead time even if the actual coding took 20 minutes. If your lead time is long, check where it's accumulating: is it in review queues, staging environments, or deployment pipelines?

---

### Change Failure Rate

**What it measures**: Percentage of deployments that cause a production incident or require a rollback.

**How to measure**: (Number of failed deployments) / (Total deployments). "Failed" means requiring a hotfix, rollback, or incident response. Define this clearly before measuring or you'll argue over what counts.

**2024 benchmarks**:

| Tier | Rate |
|------|------|
| Elite | 0-5% |
| High | 5-10% |
| Medium | 10-15% |
| Low | More than 15% |

**Common pitfall**: If you're not tracking incidents formally, this metric defaults to zero — which looks great but means nothing. Invest in an on-call system (PagerDuty, OpsGenie, even a Slack channel with a naming convention) before tracking CFR.

---

### Mean Time to Recovery (MTTR)

**What it measures**: How long it takes to restore service after a production failure.

**How to measure**: Time from incident alert to service restored. Track in your incident management system. Even a spreadsheet works if your incident volume is low.

**2024 benchmarks**:

| Tier | MTTR |
|------|------|
| Elite | Less than 1 hour |
| High | Less than 1 day |
| Medium | 1 day to 1 week |
| Low | More than 1 week |

**Common pitfall**: MTTR only tells you recovery speed, not root cause distribution. Combine with a lightweight post-mortem process so you know whether you're improving resilience or just getting faster at firefighting the same classes of issues.

---

### On the 2025 DORA Evolution

The 2025 DORA report made a significant methodological shift: the four-tier model (Elite/High/Medium/Low) was retired. DORA now identifies **7 organizational archetypes** measured across **8 dimensions** — throughput, stability, team performance, product performance, individual effectiveness, time on valuable work, friction, and burnout.

The implication for teams: stop chasing "Elite" as an endpoint. "Elite" on deployment frequency can coexist with burnout and high friction. The new model pushes you to identify your archetype (e.g., "Thriving Achievers," "Struggling Strugglers," "Balanced Performers") and improve your weakest dimensions rather than optimizing the metrics you're already good at. The four classic metrics remain valid input signals; they're just no longer the whole story.

---

## DORA in an AI-Augmented Context

Each DORA metric reacts differently when AI enters the development workflow. Understanding those effects helps you set the right targets and spot the right warning signs.

### Deployment Frequency

AI accelerates feature development, so your deployment cadence should increase — provided your pipeline can keep up. If deployment frequency stays flat after widespread AI adoption, the bottleneck is downstream: staging environments, manual QA gates, or review throughput, not coding speed. AI gives you more PRs to merge; it doesn't automatically improve the rest of the pipeline.

Watch for: deployment frequency climbing while change failure rate also climbs. That's AI-accelerated code that isn't being reviewed carefully.

### Lead Time for Changes

AI cuts coding time but has limited effect on the non-coding segments of lead time. PR review, staging validation, context-switching delays, and deployment windows are largely unchanged by AI assistance. If your lead time isn't improving alongside AI adoption, the constraint is in review velocity or pipeline automation, not coding. Map your lead time stages explicitly — code time, review wait, staging wait, deploy window — to know where the leverage is.

### Change Failure Rate

This is the metric most at risk when AI adoption outpaces review discipline. AI generates syntactically correct, structurally plausible code that can still have subtle behavioral errors. Teams that treat AI-generated PRs as "lower risk" and rubber-stamp reviews tend to see CFR creep up over 6-12 months. The failure mode is gradual: each individual AI PR looks fine, but the cumulative effect of reduced scrutiny shows up in production.

Track CFR separately for AI-generated code versus manually written code (most AI coding tools can tag commits). If AI-generated CFR is materially higher, your review process needs reinforcement, not your AI tooling.

### MTTR

AI genuinely helps here — if observability is already in place. AI-assisted diagnosis can cut time-to-root-cause significantly when the model has access to error logs, stack traces, and codebase context. But AI diagnosis is only as good as the signals it can read. A team without structured logging, without request tracing, and without alerting won't get a meaningful MTTR improvement from AI. The sequencing matters: instrument first, then expect AI to accelerate incident response.

### Raising the Baseline

The practical consequence of AI assistance at scale: "Medium" DORA is no longer a credible target. Anthropic's internal engineering data from January 2026 shows +67% PRs per engineer per day, with 70-90% of shipped code AI-assisted. If your team is operating at AI-assisted development and still sitting in Medium tier on deployment frequency or lead time, the constraint is in your processes and pipeline — not in your developers' output. Adjust your targets accordingly.

---

## Beyond DORA: The SPACE Framework

DORA measures the delivery system. SPACE measures the people inside it. Both are necessary; neither is sufficient alone.

SPACE was developed by researchers at GitHub, Microsoft, and the University of Victoria (published 2021). It covers five dimensions:

### Satisfaction and Well-being

Are developers satisfied with their work, tools, and processes? Are they experiencing burnout signals?

Measure with: quarterly developer experience survey (5-8 questions, anonymous). Track trend over time, not absolute score. A team scoring 3.2/5 that improves to 3.8/5 over 6 months is in a better position than one stuck at 4.0/5.

### Performance

Is the work being delivered actually working as intended? Does it meet quality and reliability expectations?

Measure with: Change Failure Rate (overlaps with DORA), Bug Escape Rate (bugs that reach production divided by total bugs), and customer satisfaction on specific features.

### Activity

What volume of work is being produced?

Measure with: Deployment Frequency, throughput (features shipped per cycle), PR merge rate.

Critical note: Activity is the easiest dimension to measure and the easiest to game. High commit count, high PR volume, high deployment frequency can all coexist with low actual value delivered. Activity metrics are inputs, not outcomes.

### Communication and Collaboration

Is knowledge flowing? Are teams unblocked and connected?

Measure with: PR review latency (time from PR open to first review), cross-team dependency resolution time, onboarding time for new contributors.

### Efficiency and Flow

Are developers able to do deep work without constant interruption? How much friction exists in the development process?

Measure with: self-reported flow state frequency (in your developer survey), context-switching frequency, ratio of unplanned work to planned work.

### The Velocity Trap

Teams can hit "High" on DORA deployment frequency while simultaneously scoring poorly on satisfaction, well-being, and efficiency. More deployments, but developers working nights to hit sprint commitments, skipping design discussions because AI makes coding fast enough to skip planning, accumulating cognitive debt from reviewing AI code they don't fully understand. SPACE catches this. DORA doesn't. Running both frameworks gives you the full picture.

### SPACE + DORA Together

Use DORA for your monthly leadership review: system health, delivery system performance. Use SPACE (specifically the satisfaction and efficiency dimensions) quarterly: human health, sustainable pace, skill development. Treat a divergence — strong DORA, weak SPACE — as a leading indicator of future DORA degradation. Burnt-out teams ship slower.

---

## AI-Specific Metrics

Standard frameworks weren't designed with AI-assisted development in mind. These metrics fill the gap.

### % AI-Assisted Code

The proportion of committed code that was AI-generated or AI-assisted. Available in Anthropic Contribution Metrics (Team and Enterprise plans), GitHub Copilot metrics dashboard, and similar tools for other AI coding assistants.

**Why it matters**: Provides context for everything else. A 5% increase in CFR is a different signal if AI assists 10% of your code versus 80%. Track this as denominator for all quality metrics.

**Watch for**: This number typically climbs over time as adoption increases. Benchmark it quarterly.

### AI Code vs Human Code Quality

Split your Change Failure Rate by code origin: AI-generated commits versus manually written commits. Most enterprise AI coding tools can tag commits or PRs.

If AI-generated CFR is within 2-3 percentage points of manual CFR, your review process is working. If AI-generated CFR is materially higher, review discipline has dropped. If it's lower, AI tooling may genuinely be improving code quality in your domain.

### Review Time: AI PRs vs Manual PRs

Compare average review time (open to merge) for AI-generated PRs versus manually written PRs. If AI PRs are getting merged significantly faster than manual ones, you may have a rubber-stamping problem.

AI-generated code requires at least as much review scrutiny as manually written code — arguably more, because it can be confidently wrong in non-obvious ways. A 30% faster review cycle for AI PRs is a yellow flag worth investigating.

### Developer Code Comprehension

A qualitative, binary signal: during PR review, can the author explain their AI-generated code in their own words — not just what it does, but why it does it that way?

Track this informally through your code review culture. If reviewers start noticing that authors can't explain their AI-generated submissions, that's a skill atrophy signal that will show up in higher CFR and longer MTTR 6-12 months later.

### Time-to-Understand a PR

A rough proxy for code clarity and maintainability: ask reviewers to self-report how long it took them to understand what a PR does (before they could evaluate whether it was correct). Track the median across your team.

Increasing time-to-understand suggests that code is growing more complex or less well-organized over time, regardless of who wrote it. AI-generated code can inflate this metric by producing syntactically dense implementations that are harder to reason about than simpler, more explicit alternatives.

---

## Agentic Metrics: What DORA Doesn't Measure

DORA and SPACE were designed for deterministic software systems. Agents introduce non-determinism, probabilistic quality, and failure modes that fall through every existing metric category. Three groups of metrics fill that gap.

### Why standard DORA is insufficient for agent workflows

DORA measures pipeline health, not output correctness. A study of 39 agent frameworks and 439 agentic applications (arXiv 2509.19185) found that 70% of test effort concentrates on deterministic components (tools, workflows) while less than 5% covers the LLM Plan Body — the central reasoning component most likely to produce incorrect results. Most DORA tooling has the same blind spot.

A second structural gap: DORA doesn't capture the cost of the verification loop. Agent-generated PRs require at least as much review scrutiny as manually written code, and in practice more, because subtle behavioral errors can appear in syntactically correct code. The standard deployment frequency and lead time metrics look identical whether review is thorough or rubber-stamped.

### Group 1: RCT-verifiable metrics

These replicate what METR and DeputyDev measured. Run them on real tasks, not synthetic benchmarks. They give you numbers calibrated to your own team rather than vendor estimates.

| Metric | What it measures | Published baseline |
|--------|-----------------|-------------------|
| Task completion time, AI vs. no AI | Actual speedup or slowdown for your task type | METR Study 1 (July 2025, arXiv 2507.09089): -19% for experienced developers on complex open-source repos. Perception gap: +39 points (developers believed they were 20% faster) |
| PR cycle time, AI-assisted vs. baseline | Pipeline throughput change | DeputyDev (arXiv 2509.19708): -31.8% PR cycle time (p=0.0018), n=300 engineers, 12 months |
| Pass rate on PRs with executable tests as oracle | How often agent-generated code actually passes functional validation | c-CRAB (arXiv 2603.23448, March 2026): Claude Code 32.1% pass rate on real PRs. Union of four tools: 41.5%. This is the practical ceiling for current AI code review quality |

The METR -19% figure applies specifically to L1-L2 workflows (Cursor Pro and Claude 3.5/3.7 Sonnet on complex existing repos). It is the only rigorous control-group measurement available for this context. Self-reported figures from McKinsey (20-45%), BCG (64%), and GitHub's own studies are not replicated under controlled conditions and should be treated as aspirational estimates, not planning inputs.

### Group 2: Agentic pipeline metrics

These require instrumentation via Langfuse, Arize Phoenix, or AWS Bedrock AgentCore. They do not replace DORA; they sit alongside it as a layer specific to non-deterministic systems.

| Metric | What it measures | Reference |
|--------|-----------------|-----------|
| Spec quality score | Completeness and precision of specs before agent execution. Acts as a leading indicator for output quality | No standard rubric yet; define internally. Factory.ai's pre-implementation validation contracts are the closest documented proxy |
| Validation contract pass rate | Percentage of agent-generated implementations that pass pre-defined behavioral contracts, measured before human review | Factory.ai Missions pattern: 81 problems detected in a Slack clone from spec alone, generating 34% of implementation work as fix features |
| Agent task completion rate | Tasks the agent completes without human correction, expressed as a percentage | Instrument via harness logs. Anthropic's internal data shows the 99.9th-percentile task duration grew from 25 to 45 minutes between October 2025 and January 2026, indicating agents are handling more complex tasks |
| Code review recall | Rate at which agent-generated review comments are acted on by developers | Code Review Bench (Martian, March 2026, 200,000+ open-source PRs): Augment Code 62.8% recall, GitHub Copilot 53.3% recall, Graphite 75% precision but only 8.8% recall |
| Cost per completed task | Token spend plus human review time per agent task that reaches a mergeable state | No industry benchmark published yet. Track manually: tokens consumed, cost per model call, and human review hours per task completion |
| Tokens per feature | Average tokens consumed per merged feature, crossed with Jira or Linear ticket boundaries. Better signal than tokens/request because it accounts for session count variation per feature | No industry benchmark. Track via ccboard project leaderboard (tokens/session × sessions per feature). Establish a baseline before optimizing; typical range for a complete PR is 500K-2M tokens on complex codebases |

### Group 3: Agent governance metrics

Sourced from Strata Identity Research 2026 and CSA/Zenity 2026. These reflect the state of organizational maturity rather than technical performance.

| Metric | Target state | 2026 baseline for context |
|--------|-------------|--------------------------|
| Agents with named human sponsor | Every active agent has an identifiable owner | Only 28% of organizations can link agent actions to a human sponsor in all environments (Strata 2026) |
| Real-time agent inventory coverage | All active agents appear in a central registry | 21% of organizations maintain a real-time inventory (Strata 2026) |
| Credential rotation frequency | Agent credentials rotate at least every 90 days | 44% of organizations still use static API keys for agent authentication (Strata 2026) |
| Permission violations detected | Violations detected as a share of estimated total violations | 53% of organizations have experienced an agent incident in the past 12 months; 58% took more than 5 hours to detect it (CSA/Zenity 2026) |

### The heavy-user review time contradiction

Digital Applied Q1 2026 (n=2,847 developers) found that heavy AI tool users spend 14-16 hours per week reviewing AI-generated code, compared to 11.4 hours per week for average users. This directly contradicts the narrative that AI reduces review burden. The most likely explanation: per-review unit efficiency may improve, but the volume of generated code grows faster than review capacity. Before committing to time-savings projections, measure your team's actual review time distribution across AI-generated and manually written PRs.

### The Uplevel Copilot study

Uplevel's study of Copilot adoption (uplevelteam.com, "genai-developers") found no significant change to coding speed, PR cycle time, or throughput after teams adopted Copilot, alongside a 41% increase in bug rate within PRs. Their "Sustained Always On" proxy for burnout risk, built from after-hours and weekend activity patterns, also declined more for developers without Copilot than for those with it over the same period.

Read this alongside the heavy-user review time contradiction above: two independent measurements now point the same direction. Neither speed nor throughput moves the way the adoption narrative predicts, and the metrics that do move (bug rate, review time, burnout proxy) move in the wrong direction. Treat any AI-tooling ROI claim resting on developer speed alone as unverified until you've checked it against your own bug rate and review-time data.

**Why the review hours cannot simply be absorbed**: defect detection in review has ceilings that were measured before AI existed and did not move when the tooling did. Past roughly 200-400 lines per review, or 60-90 minutes of sustained reviewing, detection degrades sharply. A 14-hour weekly review load is therefore not 14 hours of equivalent-quality review. See [The Attention Cost of the Review Shift](../roles/learning-with-ai.md#the-attention-cost-of-the-review-shift) for the underlying studies and the practices that keep review inside the effective band.

### pass^k for non-deterministic tests

Standard pass@1 is insufficient for agent-generated code. A test that passes once may fail on the next run because the output is non-deterministic. Promptfoo and LangChain both document the pass^k pattern: run critical tests k times consecutively, typically 3 to 5. A test passes only if it passes all k runs. This is not flaky-test detection — it is a deliberate quality gate for probabilistic systems. Apply it specifically to agent-generated suites, not to the full regression suite where the overhead would be prohibitive.

---

## Product Metrics (the often-missing layer)

Engineering metrics measure how code gets built. Product metrics measure whether the code is actually solving the right problems. Most engineering teams track the former and leave the latter entirely to product managers. That creates a gap where a team can be shipping fast, with high DORA scores, while the product drifts away from user needs.

### Time-to-Value

How long does it take a new user to reach their first success with your product? Define "first success" concretely — first completed task, first saved item, first report generated, whatever makes sense in your context.

Track this as a median across your user cohorts, and watch for regressions after major feature releases. AI can accelerate your feature shipping without improving, or even while degrading, the new user experience.

### Feature Adoption Rate

Of users who could use feature X, what percentage actually use it within 14 days of release? A feature shipped on time with clean DORA metrics that nobody uses is still a failed feature.

Segment by user cohort (new vs. returning users, different pricing tiers) to distinguish adoption problems from discoverability problems.

### Bug Escape Rate

Bugs found in production divided by total bugs (pre-production bugs + production bugs). Formula: `bugs_in_prod / (bugs_before_prod + bugs_in_prod)`.

If your Bug Escape Rate exceeds 20%, your QA and review processes are consistently failing to catch issues before they reach users. With AI-assisted development, this metric is worth watching closely: faster code generation combined with looser review can push Bug Escape Rate up even when absolute bug count stays flat.

### Feature CSAT

Customer satisfaction score tied to specific features, not the product as a whole. More actionable than NPS: instead of "how likely are you to recommend us," ask "how useful was feature X in completing task Y" on a 1-5 scale.

NPS is useful for brand-level sentiment but too lagging and too broad to steer development priorities. Feature CSAT gives you signal within 2-4 weeks of a release rather than 6-12 months.

---

## By Team Size

Different team sizes have different measurement overhead tolerances. A 5-person team that spends 20% of its time on metrics infrastructure is making a poor trade-off. A 25-person team without automated DORA tracking is flying blind. Here's a practical baseline for two common scales.

### 5-Person Team

**Metrics to track:**

| Metric | How | Frequency |
|--------|-----|-----------|
| Deployment Frequency | Count deploys manually or from CI | Weekly |
| Cycle Time (commit to prod) | Linear or GitHub timestamp diff | Per-PR, reviewed monthly |
| Time-to-value (product north star) | Analytics tool (Mixpanel, Amplitude, PostHog) | Monthly |
| Bugs in prod per month | Count in your issue tracker | Monthly |
| Developer satisfaction | 5-question anonymous form | Quarterly |

**Tooling**: GitHub Insights plus a shared spreadsheet. No dedicated dashboard needed at this size — the overhead isn't worth it. What matters is having the discipline to review these numbers in a monthly retrospective, not the precision of the tooling.

The instinct at this size is often to skip metrics entirely ("we're too small, we know each other, we talk daily"). Resist it. The value of metrics at 5 people isn't visibility — it's discipline. Naming a north star metric and checking it monthly forces conversations that daily standups don't.

### 25-Person Team

**Metrics to track:**

| Metric | How | Frequency |
|--------|-----|-----------|
| All 4 DORA metrics | LinearB or Faros.ai automated | Weekly (automated) |
| Cycle Time per squad (not global) | Same tooling, segmented | Weekly |
| Bug Escape Rate | Issue tracker + deploy markers | Monthly |
| Feature CSAT | In-app survey on key features | Per-release |
| % AI-assisted code | Anthropic Contribution Metrics | Monthly |
| Developer satisfaction | 8-question survey, anonymous | Quarterly |
| PR review time | GitHub Analytics / LinearB | Weekly |
| Time-to-value | Analytics tool | Monthly |

**Tooling**: LinearB or Faros.ai for DORA automation (connects to GitHub + your CI/CD pipeline, surfaces the four metrics without manual tracking), GitHub Analytics for AI contribution data, PostHog or Amplitude for product metrics.

At 25 people, global averages hide squad-level problems. A team with 3 squads that has 80% of its incidents originating from one squad will show a "Medium" CFR overall and miss the signal entirely. Track DORA per squad, not just per organization. Cycle time per team is especially valuable — it surfaces bottlenecks in specific parts of your codebase or process.

PR review time is a friction metric worth watching closely at this scale. When median PR review exceeds 24 hours, it creates context-switching overhead: developers move to other tasks while waiting, then need to re-load context when the review comes back. That re-loading cost doesn't appear in any standard metric, but it compounds across dozens of PRs per week.

---

## Vanity Metrics to Drop

| Drop This | Replace With | Why |
|-----------|-------------|-----|
| Sprint velocity | Cycle Time + Deployment Frequency | Velocity is gameable within 2 sprints by changing estimation practices. Cycle time is harder to fake. |
| Lines of code | Bug Escape Rate | LOC measures output volume. With AI, LOC goes up automatically. Bug Escape Rate measures output quality. |
| NPS alone | CSAT + Time-to-value | NPS is a lagging brand signal, not an engineering steering metric. CSAT on specific features is actionable within weeks. |
| Commits per day | Lead Time for Changes | Commit frequency measures activity. Lead time measures whether that activity actually ships value. |
| Story points | Throughput (features shipped) | Points are defined relative to the team's own baseline and gameable by re-pointing. Throughput counts real deliverables. |
| Code coverage % | Mutation testing score + Bug Escape Rate | Coverage tells you tests exist. Mutation testing tells you whether those tests would catch real bugs. |

Story points deserve a specific note in an AI context: if AI is generating boilerplate and scaffolding automatically, the effort to implement a "3-point story" has dropped significantly. Teams that haven't recalibrated their pointing will show velocity increases that reflect tool efficiency, not team capacity. Lead Time and Deployment Frequency are tool-agnostic — they measure output regardless of who or what did the work.

---

## The 4-Question Test

Before adding any metric to your tracking stack, run it through these four questions:

**1. Can you act on it within 2 weeks?**

If the answer is no, it's a reporting metric, not a steering metric. Reporting metrics belong in quarterly board decks, not in weekly team reviews. "Total API calls since launch" is a reporting metric. "API error rate last 7 days" is a steering metric.

**2. Does it explain why, not just what?**

"Churn is 5%" tells you nothing. "80% of churned users never completed their first workflow" tells you where to look. When evaluating a metric, ask: if this number moves, do I know what to investigate?

**3. Is it correlated to a business outcome?**

This is the tightest filter. Deployment frequency is correlated to revenue in high-iteration SaaS products. PR review time is correlated to developer satisfaction and retention. Feature CSAT is correlated to expansion revenue. Lines of code is correlated to nothing that matters.

**4. Can it be measured automatically?**

If collecting the metric requires manual work — someone pulling numbers from a spreadsheet, someone remembering to log an incident — it will be abandoned within 3 months when workload increases. Automate or drop.

**The rule**: fewer than 3 "yes" answers, drop the metric. A measurement stack with 5 rigorous metrics is more useful than one with 20 loosely defined ones. Most teams that fail at metrics fail by tracking too many things with too little precision, not by tracking too few.

---

## Tooling

| Tool | What It Does | Best For | Notes |
|------|-------------|---------|-------|
| LinearB | DORA automation + cycle time, connects to GitHub + Jira | 25+ people | Good out-of-box DORA dashboards, solid PR analytics |
| Faros.ai | DORA + custom engineering dashboards, open-source core | 25+ people | More configurable than LinearB, steeper setup |
| GitHub Analytics (Anthropic) | AI contribution metrics (% AI-assisted code, PR-level attribution) | Any Claude Code team | Enterprise/Team plan required |
| Sleuth | Deploy tracking + change failure rate, DORA-focused | 10+ people | Lightweight, CI/CD focused, no bloat |
| Axify | Full engineering metrics suite, DORA + flow + team health | 15+ people | Canadian startup, strong SPACE coverage |
| GitHub Insights | Basic activity metrics, free, built-in | Any size | Good enough for 5-10 person teams, not sufficient at scale |
| Spreadsheet | Manual tracking, always works, zero setup | Under 10 people | The right tool if automated setup overhead isn't justified yet |

No tool automatically surfaces the AI-specific metrics described earlier (CFR by code origin, review time comparison, comprehension signals). Those require either custom dashboards built on your CI/CD data or manual tracking. GitHub Analytics covers % AI-assisted code; the rest you'll wire up yourself or instrument in your PR template process.

Avoid tool sprawl. A team with LinearB, Jira, GitHub Insights, and two separate analytics tools will spend more time reconciling numbers than acting on them. Pick one DORA tool, one product analytics tool, and use GitHub Analytics for AI-specific data.

### Broader Delivery Intelligence Platforms

The table above covers the tools most teams reach for first. The 2026 market is wider than that, and worth a second look if the starter table doesn't fit your org's size or constraints.

| Tool | What It's For | Notes |
|------|---------------|-------|
| DX (getdx.com) | Developer intelligence platform built by researchers associated with the DX Core 4 / SPACE framework lineage | Positioned for larger organizations wanting a research-grounded metrics platform rather than a plug-and-play dashboard |
| Multitudes (multitudes.com) | Analytics and recommendations built directly on DORA, SPACE, and DevEx signals | Sends "nudges" when a metric indicates a team is blocked or overloaded, rather than just reporting the number |
| Swarmia (swarmia.com) | Cycle time breakdown (shipped 2022, still active): decomposes PR time into in-progress, waiting-for-review, and waiting-for-merge | Also publishes its own research on the productivity impact of AI coding tools (2025 blog) |
| Cortex.io | Positions itself as an "Engineering Operations Platform" and publishes its own "Engineering Intelligence Platforms: Top 8 Tools" category guide | Already cited elsewhere in this guide as a data source for PR size and change failure rate figures; not previously documented here as a delivery-intelligence tool in its own right |
| Jellyfish | Positions itself in 2026 as a "software engineering intelligence platform" explicitly built for AI-integrated organizations | Same note as Cortex.io: already cited as a data source elsewhere in this guide, now documented as a tool |
| Oobeya (oobeya.io) | Aggregates 20+ existing DevOps tools into a single layer, rather than being a standalone data source itself | Fits teams already running several disconnected DevOps tools who want one pane of glass instead of another data collector |
| Hatica (hatica.io) | Markets "gen AI-driven engineering analytics" | Thinner on documented specifics than the other entries in this table: the underlying LLM mechanism behind its analytics claims isn't publicly detailed. Worth a direct vendor conversation before committing, don't take the marketing framing at face value |

### AI-Generated Board Narratives

A genuinely new 2026 capability: some of these platforms now generate a written narrative from the metrics they already compute, rather than leaving that translation to a human. Two concrete examples.

**LinearB** generates an AI iteration summary from Jira, Git, PR, and deployment data, structured around three axes: what went well, what didn't, and what could improve. It's delivered automatically to Slack or Microsoft Teams at sprint end, replacing the manual retro write-up a tech lead would otherwise produce.

**Jellyfish's "AI Executive Report"** translates AI-tool adoption data (Copilot, Windsurf, and similar) into three dimensions built for a non-technical executive audience: adoption, output, and impact, the last framed as time saved, money saved, and risk reduced.

In both cases, the generative AI's role is explanation and prioritization of what the underlying analytics already computed, not the computation itself. The pass rate, the cycle time, the CFR split: those numbers come from the same instrumentation this page has covered throughout. The LLM's job is turning a table into three paragraphs a stakeholder will actually read. Treat it as a formatting and triage layer, not a new source of statistical insight.

---

## Probabilistic Delivery Forecasting

Every benchmark table on this page so far answers "how are we doing." This section answers a different question: "when will this ship," and it answers it with a probability distribution instead of a single date.

### Why a point estimate misleads

Traditional forecasting takes your velocity (story points or throughput per sprint) and divides it into remaining scope to produce a single date. That date carries false precision: it implies a certainty the underlying data never had. Two teams with identical average velocity can have wildly different variance, and variance is exactly what a point estimate throws away.

Monte Carlo forecasting instead runs your team's actual historical cycle times (or throughput) through thousands of simulated iterations and produces a distribution: "80% confidence between March 3 and March 20" instead of "March 12." That's a more honest answer, because it's the one your data can actually support.

### Tools

**ActionableAgile** (actionableagile.com) is a flow and predictability-focused analytics product, licensed via 55 Degrees AB, built around Monte Carlo forecasting. Its "Portfolio Forecaster" extends the same technique across multiple initiatives at once, useful when a board is asking about predictability across a roadmap rather than a single deliverable.

**Nave** (getnave.com) runs Monte Carlo simulation alongside a "Cycle Time Histogram" view. Nave's own documentation states the core constraint plainly: *"The sole requirement for Monte Carlo to work and give reliable answers is to use data produced by a predictable delivery system."* Even 20-30 completed items are enough if the workflow is stable, but a recent change to team composition or process should reset the data window so the forecast reflects current conditions, not a mix of old and new reality.

### What this does not fix

Monte Carlo forecasting is not a fix for an unstable or unpredictable delivery system. If your cycle times swing wildly because scope keeps changing mid-sprint, or because the team composition just shifted, the simulation will faithfully replicate that unpredictability as a wider distribution. It won't narrow the range for you. A wide, honest 80% confidence interval is still more useful than a false point estimate, but it's a symptom report, not a cure. Fix the underlying instability first; the forecast will narrow on its own once the process does.

---

## Implementation Roadmap

The most common failure mode in metrics programs is trying to instrument everything at once. Three phases:

### Phase 1: Weeks 1-2 — Instrument DORA

Connect your CI/CD pipeline to a metrics tool. For most teams this means connecting GitHub Actions (or equivalent) to LinearB, Faros, or Sleuth. Get Deployment Frequency and Lead Time automated first — they require the least manual work to configure. Change Failure Rate and MTTR require incident tracking to be in place, which takes slightly longer to set up.

Output: a live dashboard showing at minimum Deployment Frequency and Lead Time for Changes. Your first baseline numbers.

### Phase 2: Weeks 3-4 — Baseline and Set Targets

Once you have 2-4 weeks of data, establish your actual baseline. The temptation here is to compare to industry benchmarks immediately. Resist it. Set internal improvement targets first: "reduce Lead Time by 20% over the next quarter" is more actionable than "get to High tier." Your context — tech stack, deployment environment, team size, product type — affects what's achievable more than any benchmark.

Run your first developer satisfaction pulse (5 questions, anonymous, takes 10 minutes to build in Google Forms or Typeform). This is your SPACE baseline.

### Phase 3: Month 2 and Beyond — Layer in Product and AI Metrics

Once DORA is stable and automated, add the product metrics (time-to-value, feature CSAT) and AI-specific signals (% AI-assisted code, CFR by code origin). These require more setup — product analytics instrumentation, PR tagging conventions — but they're worth the investment once your DORA foundation is solid.

Review the full metric stack quarterly and prune ruthlessly. Any metric that hasn't driven a decision in the last 3 months is a reporting metric masquerading as a steering metric. Cut it.

---

## Reporting Delivery Capacity to a Skeptical Board

Everything above this section assumes the audience is your own team or your engineering leadership chain. A board that has watched past estimates slip needs a different approach, because the problem it's raising usually isn't the one a dashboard answers.

### The diagnostic: doubt is a trust problem, not a data problem

When a board starts doubting a team's delivery capacity after past estimates have slipped, adding more delivery dashboards rarely fixes it on its own. The board's doubt is almost always about trust and visibility: what caused the slip, and will it happen again. It is much less often about the data itself: board members generally don't disbelieve the velocity number on the screen, they disbelieve the story that number is supposed to support.

Be honest about the limits of what's provable here: no published study or vendor report actually measures whether delivery-intelligence tooling repairs executive trust. That's an evidence gap in the field, not a gap in this guide. Nothing in this section, and none of the tools covered earlier on this page, comes with proof that it fixes a board's confidence. What follows is a set of practices that reframe the conversation into one a board can act on, not a guaranteed remedy.

### Bring scenarios, not a velocity chart

A single velocity number invites a single question: can the team go faster. That's rarely the question worth answering, and it's an easy one to lose regardless of the real numbers behind it.

Bring 2 to 3 named delivery scenarios instead, each with a concrete timeline, a rework or cost estimate if sequencing gets compressed, and the business impact of picking that option. "Ship the full scope in Q3 at current pace" versus "compress two workstreams into Q2 at an estimated X% higher defect rate and Y additional engineer-weeks of rework" versus "cut scope Z and ship on the original date" is a decision a board can actually make. "Can the team go faster" is not.

### Cap strategic objectives, don't roadmap every feature

A fully detailed, multi-quarter feature roadmap looks like rigor and produces the opposite. Every feature-level commitment beyond roughly one quarter out is a precision claim your delivery system almost certainly can't back, and it erodes trust the moment reality diverges from the plan, which it will.

Cap the number of board-level strategic objectives instead, a small, named set, reviewed quarterly. Objectives survive a schedule slip better than feature line items do, because an objective describes an outcome the team is still steering toward even when the specific path changes.

### Separate committed scope from best-effort scope, and track the hit rate

Draw an explicit line between what the team commits to and what it will attempt on a best-effort basis. Then track, over time, how often committed scope actually ships as committed.

That hit-rate track record becomes the trust-rebuilding metric in its own right. A board that sees "when this team commits, it delivers" repeated release after release cares about that pattern more than it cares about any single throughput or velocity number. Trust rebuilds through a track record, not through a chart.

### Align stakeholders before the room, not in it

A plenary board meeting is a poor venue for first-time alignment on a contentious delivery question. Before walking in with scenarios and numbers, talk to board members individually and understand what's actually driving each one's doubt: comparison to other teams in the portfolio, external business pressure unrelated to engineering, or a specific past miss they haven't let go of. Those three causes call for different framing, and a plenary meeting doesn't give you the space to diagnose which one you're dealing with in the room.

### Where forecasting and AI narratives fit, and where they don't

The [probabilistic forecasting](#probabilistic-delivery-forecasting) tools covered earlier on this page give you the honest range behind each scenario in point two: "80% confidence between these two dates" is a more defensible number to bring into the room than a single point estimate, provided your delivery system is stable enough for the forecast to mean something. The [AI-generated board narratives](#tooling) from tools like LinearB and Jellyfish reduce the manual effort of translating sprint data into a written summary a non-technical board member can read.

Neither substitutes for the harder work above. A better forecast and a better-written summary still won't cap your roadmap, separate committed from best-effort scope, or have the individual conversations that surface what a specific board member actually doubts. Those three remain a management job, not a tooling job.

---

## See Also

- [Session Observability & Monitoring](./observability.md) — Claude Code session monitoring, cost tracking, usage patterns
- [AI Traceability](./ai-traceability.md) — Auditing AI-generated code contributions, attribution, and compliance
- [Learning With AI](../roles/learning-with-ai.md) — Individual developer growth in AI-augmented workflows, skill development signals
- [Agent Evaluation](../roles/agent-evaluation.md) — Quality metrics for custom Claude Code agents and automated workflows
