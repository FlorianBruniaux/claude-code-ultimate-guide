---
title: "AI Unit Economics"
description: "How to model the real cost per accepted task in agentic AI development: attempts, retries, review, rework, routing, progressive spend controls, and autonomous-agent break-even"
tags: [cost, ops, guide]
---

# AI Unit Economics

> **Audience**: Tech leads, platform engineers, and engineering managers who need to reason about what agentic AI costs per accepted unit of work, not just what shows up on the monthly invoice.
>
> **Scope**: The economic reasoning behind agentic development cost. For the technical implementation of budgets and per-team enforcement, see [api-gateway.md](./api-gateway.md). For per-session logging and cost estimation, see [observability.md](./observability.md).

---

## A note on what this page is

This page combines original synthesis with limited reproducible research. Production coding-agent traces can measure token use and reconstructed spend while omitting task acceptance. Coding benchmarks can measure resolution and cost under a narrower harness while missing production traffic, engineer review, and organizational controls. Neither evidence type is a fleet forecast by itself.

The page therefore separates measured evidence, illustrative arithmetic, and operating recommendations. Every attributed claim names its source. Where a number is illustrative rather than measured, it says so.

---

## 1. Why agentic cost is not SaaS cost

Classic SaaS pricing is a fixed cost per seat. You pay the same whether a user runs one report or a hundred. Capacity planning is a headcount question, and the finance team can forecast next quarter by counting licenses.

Agentic AI breaks that model in three ways.

**The invoice varies per attempt, not only per seat.** A developer with a Claude Code license does not create one fixed inference cost. Each run consumes a different mix of input, output, cache, tool, and sub-agent work. An attempt is the observable billing unit. An accepted task is the management denominator because failed attempts still consume tokens and human review.

**The cost of the same task varies run to run.** Ask an agent to fix the same failing test twice and you can get two different token totals. The model may re-read a file it already saw, take an extra reasoning step, or call one more tool. Variance is inherent, not a defect. It means you budget against a distribution, not a fixed line item.

**Failed work still costs money.** A run that loops without converging, re-reads the same large file five times, or explores a dead end burns input and output tokens the whole way. In classic SaaS a failed action is free. Here, a task that produces nothing can cost more than one that succeeds, because failure often means more iterations, not fewer. The invoice grows even when the output does not, which is what catches teams off guard.

The framing that captures the stakes came out of an enterprise AI transformation account: a token is intelligence and real value, and the work is turning tokens into industrial ROI (*The Product Crew, AI transformation field report, 2026, in the context of Ask For The Moon*). Restated for this page: every token you spend is a bet that the work it produces is worth more than the token cost. Unit economics is the discipline of checking whether that bet pays off, task by task.

---

## 2. Building a cost per accepted task

Measure each attempt first, then aggregate every attempt that contributed to an accepted result. A Claude Code run decomposes into these billable components:

| Component | What it is | Typical driver |
|-----------|-----------|----------------|
| Input tokens | Everything sent to the model: prompt, files read, tool results, conversation history | Context size, number of file reads |
| Output tokens | Everything the model generates: reasoning, code, explanations | Task complexity, verbosity |
| Cache writes | Context written to the prompt cache on first use | First read of a large stable file |
| Cache reads | Context served from cache instead of full input price | Repeated reads of the same context |
| Tool calls | Each tool invocation adds its result to the next input | Number of Read, Bash, Grep, WebFetch calls |
| Sub-agent runs | Each sub-agent is its own input plus output cost | Number and depth of delegated tasks |

Output tokens can dominate the bill because output is priced several times higher than input. At Anthropic's public rates verified 2026-08-31, Sonnet 5 costs $2 per million input tokens and $10 per million output tokens, while Opus 5 costs $5 and $25. A task that generates a lot of code or long reasoning can therefore cost more on the output side even when its input is larger. Source: [Claude model pricing](https://platform.claude.com/docs/en/about-claude/pricing).

### A concrete calculation

Take a mid-sized pull request: an agent reads eight files, reasons about a change, edits four of them, and runs the test suite twice. A rough token budget:

```
Input side:
  8 file reads          ~40,000 tokens (first read, priced as input or cache write)
  2 test-run outputs      ~8,000 tokens (tool results fed back as input)
  reasoning re-reads     ~20,000 tokens (context resent on each turn)
  system + instructions   ~5,000 tokens
  -----------------------------------
  input subtotal         ~73,000 tokens

Output side:
  reasoning              ~12,000 tokens
  4 file edits            ~6,000 tokens
  explanations            ~2,000 tokens
  -----------------------------------
  output subtotal        ~20,000 tokens
```

At Sonnet 5 public rates verified 2026-08-31 ($2 input, $10 output per million):

```
input:  73,000 / 1,000,000 x $2   = $0.146
output: 20,000 / 1,000,000 x $10  = $0.200
                                    -------
                     attempt total ~ $0.35
```

The same illustrative attempt on Opus 5 lands near $0.87, about 2.5 times more at public token rates. The token counts above are hypothetical and do not establish a typical PR cost. They show how to price one attempt before retries, review, rework, or acceptance.

### A minimal cost function

Expressed as pseudo-code, the per-task cost is a sum over turns and sub-agents:

```
cost_per_attempt =
    sum over each model turn:
        input_tokens  * input_rate
      + output_tokens * output_rate
      + cache_write_tokens * cache_write_rate
      + cache_read_tokens  * cache_read_rate
  + sum over each sub_agent:
        cost_per_attempt(sub_agent)   # recursive: sub-agents have their own turns

cost_per_accepted_task =
    (sum(cost_per_attempt)
      + human_review_cost
      + rework_cost
      + infrastructure_cost)
    / accepted_tasks
```

If `accepted_tasks` is zero, do not manufacture a ratio. Report the number of attempts, total spend, review time, and zero accepted tasks. Compare models or workflows only on the same task sample and acceptance gate.

Bai et al. repeated coding-agent runs on the same SWE-bench Verified tasks across eight models and observed up to 30-fold variation in total tokens. Higher token use did not imply higher accuracy. The benchmark is not a production trace and does not include organization-level review cost, but it supports repeated trials and distribution reporting rather than a single-run estimate. Source: [Bai et al., "How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks", arXiv:2604.22750](https://arxiv.org/pdf/2604.22750), PDF pp. 1-4.

Cache reads are priced far below fresh input (a fraction of the input rate), which is why a stable, reused context is cheaper than one you rebuild every turn. That single fact drives most of the levers in the next section.

The raw token counts for a real session live in the JSONL files at `~/.claude/projects/<project>/`. Tools like `ccusage` (see [observability.md §External Monitoring Tools](./observability.md#external-monitoring-tools)) read those files and produce exact per-session costs, so you do not have to estimate by hand once you want real numbers.

### Do not estimate tokens by string length

The cost function above is only as good as the token counts you feed it. The usual shortcut is `chars / 4`, which appears in countless helpers as a one-liner:

```js
const estimateTokens = (text) => Math.ceil(text.length / 4);   // wrong in the unsafe direction
```

It holds for English prose and falls apart everywhere else. Measured against the real `cl100k_base` tokenizer (July 2026):

| Input type | Real tokens | `chars / 4` | Error |
|-----------|-------------|-------------|-------|
| English prose | 10 | 11 | +10% |
| JavaScript snippet | 23 | 15 | **-35%** |
| French text with accents | 22 | 17 | **-23%** |

Two properties make this worse than a plain inaccuracy.

The error direction is unsafe. The heuristic *underestimates* exactly where you care most, on code and on accented or non-Latin text, so it reports that a payload fits when it does not. A budget guard built on it lets through what it was written to stop, silently, and the failure surfaces later as a truncation or an API error rather than as a wrong number.

The tokenizer is the wrong one anyway. `cl100k_base` is OpenAI's. Claude uses a different tokenizer, so a `chars / 4` estimate aimed at a Claude context window stacks a second error on top of the first. For real numbers, count with the provider's own endpoint ([Anthropic's token counting API](https://docs.claude.com/en/docs/build-with-claude/token-counting)) or read actual usage from the response, and keep heuristics for rough sizing only.

**The subtler bug: count what you send, not what the user typed.**

Even a correct tokenizer gives a wrong answer when it measures the wrong string. A guard that counts the raw user message, then sends a prompt assembled from that message plus a system header, role prefixes, and an instruction block, is under-counting by everything the wrapper adds. The gap is invisible in tests, because it grows with formatting that tests usually skip.

Count the final serialized payload, immediately before the call, at the same place the request is built. If a fallback path trims the input to fit, it has to re-measure after trimming rather than assume the trim was enough.

If you already log truncation events, that is where the answer lives. A counter on "guard said it fit, provider disagreed" turns this from an argument into a measurement.

---

## 3. The real cost-reduction levers

Five levers move the per-task cost meaningfully. None of them require a pricing negotiation. They are engineering decisions.

### Route by complexity

Not every task needs the most capable model. A prompt that formats a file, renames a symbol, or answers a lookup may not need Opus-level reasoning. Routing simple prompts to a cheaper model can reduce the bill when the cheaper model-harness pair passes the same acceptance gate without adding retries, review, or rework.

"Routing" covers three different control boundaries:

| Routing level | Decision boundary | Economic advantage | Main risk |
|---|---|---|---|
| **Request level** | A gateway selects a model for each inference request inside a session | Can choose the cheapest model for an individual step | Model switches can lose cache locality or change behavior inside one task |
| **Task level** | A dispatcher selects the model-harness pair before the task starts | Keeps one task on a stable context and cache path | A wrong initial classification can leave the task underpowered |
| **Escalation or delegation** | One model escalates difficult work or delegates bounded work to another | Pays for the stronger model only where its judgment is needed | Coordination, duplicated context, and sub-agent review add cost |

Choose the routing level before comparing savings. A request router, a task dispatcher, and a two-model delegation pattern do not create the same token path or quality risk.

Two production accounts put bounded numbers on routing. One practitioner reported that routing prompts by complexity to cheaper models cut production cost by roughly half in the observed case (*Antonio Goncalves, [IFTTD ep 357](https://www.ifttd.io/)*). Databricks reports that its internal Smart Router reduced average task cost by more than 30% while roughly matching the most expensive model's quality. Neither account publishes a paired task sample, acceptance protocol, or confidence interval. Treat both as operating results to reproduce on internal tasks, not as portable savings constants. Source: [Databricks, "Managing AI Coding Costs at Scale"](https://www.databricks.com/blog/managing-ai-coding-costs-scale), 2026-08-07.

The "efficiency frontier" is a useful label for the candidate models that meet a task class's quality bar at the lowest cost. It is not a public leaderboard. Evaluate the model-harness pair on frozen representative tasks, repeated runs, the same acceptance gate, and total review and rework cost before moving traffic.

### Isolate heavy work in sub-agents

Pushing a heavy task into a sub-agent with its own clean context, which returns only a synthesis to the supervisor, keeps the main context from filling with intermediate detail (*Dev With AI Meetup, multiple speakers, 2026*). The economic effect is direct: the supervisor's context stays small, so every subsequent turn on the main thread resends fewer tokens. Without isolation, the intermediate output of a heavy task pollutes the main context and inflates the input cost of every turn that follows, for no added value.

The trade-off is that a sub-agent has its own input and output cost. Isolation pays off when the heavy task would otherwise bloat a long main thread. It does not pay off for a task so small that spawning a sub-agent costs more than the pollution it avoids. The order of magnitude to keep in mind: practitioner reports put naive multi-agent workflows at 3 to 10 times the token cost of a single-agent run on the same task (AugmentCode and Bearplex field guides, 2026, vendor-internal measurements, not peer-reviewed). Structured output contracts, history compression, and KV-cache sharing claw back 30 to 80% of that overhead (Zylos Research, 2026, analytical). Treat every added agent as a cost node that has to justify itself with a measurable accuracy gain, not a default.

### Cap iterations and set explicit exit criteria

The most avoidable cost is a loop that does not converge. An agent that keeps trying, re-reading the same files, and re-reasoning over the same context can spend several dollars producing nothing. Two guards prevent it: an explicit definition of done, so the agent knows when to stop, and a hard maximum on iterations, so a stuck run fails fast instead of burning tokens indefinitely. A run that hits the iteration cap and stops has a bounded cost. A run without a cap does not.

### Reuse cached context

Because cache reads are priced far below fresh input, a stable context that the model reads repeatedly is much cheaper than one rebuilt from scratch each turn. Keeping the large, stable parts of the context (project instructions, reference files, schemas) in a form the cache can serve turns repeated reads from a full-price input into a fraction of it. This compounds over a long session.

Routing policy participates in that cache design. Prefer a task-level decision before the session starts when the task can remain on one model-harness pair. If a request-level router may switch models mid-session, measure cache creation, cache reads, cold starts, and total accepted-task cost. A cheaper inference request can make the complete task more expensive when it invalidates a large reusable prefix.

The same lever applies on the tool-output side of the equation. A `git status` or `find` call in a large repo can return thousands of tokens of noise the model never needed. Tools like [rtk](https://github.com/rtk-ai/rtk) filter that CLI output before it reaches the model, cutting input tokens on those calls by a reported 60 to 90% without changing what the agent can act on.

### Audit what a skill or tool injects, not just what it costs to load

The skill or tool definition is rarely the expensive part. A skill instruction file that runs 10 to 20K tokens loads once per session and stays cheap. The expensive part is what the skill returns: a graph query result, a tool's raw output, a file dump pulled into context. That result does not disappear after the turn it was generated in. It sits in context and gets re-billed, at the cache-read rate, on every turn that follows for the rest of the session.

One practitioner's measured example shows the shape of the problem. A skill that itself loads at roughly 12K tokens was paired with a query whose injected result cost more than $1 on the call that generated it, then about $0.11 in cache-read on each subsequent turn (Marek Kalnik, CTO at Theodo, LinkedIn post, July 2026). A screenshot from the same post, taken from a session-log analysis tool the author uses to train his teams, showed one skill invocation costing $5.33 on 208.9K tokens mid-session, next to several `TASKCREATE` calls at roughly $0.001 each. The skill call alone ran more than five thousand times the cost of each call around it.

Some tasks genuinely need a large injected result, and a skill that supplies one on those tasks earns its cost back many times over. A skill configured to trigger on a broad, unconditioned pattern, any question about a codebase, for instance, pays its full injection cost on every match, whether or not that particular task needed the result. Asked whether the injection cost is offset by tokens saved elsewhere, the same practitioner answered plainly: it depends on the task, and no break-even point has been measured. On a run that was already burning $75 with no ceiling in sight, the injected context would have helped. On a routine question, it was five dollars spent for nothing (Marek Kalnik, in reply to a reader's question, same thread).

That is a governance decision, not a fixed rule, and it has to be made per skill, per project, against measured cost rather than assumption. Claude Code exposes the number needed to make it: the `/usage` per-category breakdown reports cost by skill, subagent, plugin, and MCP server over the last 24 hours or 7 days ([v2.1.149](../core/claude-code-releases.md#v21149-2026-05-23)). Before leaving a skill on a wide auto-trigger, pull that breakdown, find what the skill actually costs per invocation, and check that against how often the matched tasks genuinely need the context it pulls in. A skill that earns its cost on the tasks it fires on is a lever. One that does not is a tax added to every turn after it runs.

---

## 4. The break-even point of an autonomous agent

The appealing pitch for an autonomous agent is that it runs around the clock and never rests. The economic question is whether the work it produces around the clock is worth more than what it costs to run around the clock. There is a volume and complexity threshold below which a continuously running agent costs more than it returns.

Two forces set that threshold. Above it, an agent handling a high volume of well-scoped tasks earns its keep, because the alternative is a lot of human time on repetitive work. Below it, an agent left running on ambiguous or low-volume work spends tokens on exploration and re-work that a human would have short-circuited.

A concrete failure signal comes from a team that delegated to agents continuously without supervision and lost velocity as a result (*Dev With AI Meetup, Gallet & Dahan, 2026*). The lost velocity is a hidden cost that never appears on the token invoice. Time spent reviewing, correcting, or unwinding agent output is a real cost of the agent, even though it is paid in engineer hours rather than dollars per million tokens. Read that account as a warning sign, not a rule: it shows that unsupervised continuous delegation can push a team below the break-even line, where the total cost (tokens plus human cleanup) exceeds the value produced.

The infrastructure around a high-volume automated client is its own cost line. A client generating 10,000 to 50,000 operations per day needs capacity planning and rate limiting to stay within provider limits (*ByteByteGo, 2025*). At that volume, the cost of the surrounding infrastructure (queues, retries, rate-limit handling, monitoring) is added on top of the inference cost. Break-even is not only about tokens. It is about tokens plus the systems that keep a high-throughput agent inside its limits, plus the human time spent supervising it.

A practical way to reason about the threshold: estimate the fully loaded cost of an agent on a class of tasks (tokens plus infrastructure plus expected human cleanup), and compare it against the cost of the same work done by a human or a simpler non-agentic pipeline. If the agent is cheaper only when you ignore the cleanup, you are below break-even.

---

## 5. Budget and governance per team

Once you can compute cost per attempt and per accepted task, you can set budgets against them. The economic reasoning belongs here; the technical enforcement belongs in [api-gateway.md](./api-gateway.md).

The terminal policy depends on who or what is spending. An unattended agent, CI job, or service needs a hard terminal budget because no person is present to interpret a warning. Interactive developer traffic needs an earlier control sequence that can stop accidental spend without turning a legitimate high-value session into an unexplained outage.

| Stage | Interactive developer policy | Unattended workload policy |
|---|---|---|
| **Visibility** | Show current spend, spend rate, model, and remaining headroom | Emit the same telemetry to the service owner |
| **Warning** | Require a self-clearing acknowledgement when spend crosses an unusual threshold | Alert, but do not rely on acknowledgement |
| **Approval** | Require a manager or budget-owner approval at a higher threshold | Require a pre-approved budget increase before the next run |
| **Downshift** | Offer or enforce a lower-cost approved model when the task can continue safely | Use only when the fallback passed the same task acceptance gate |
| **Suspension** | Temporarily stop usage as the terminal control | Stop deterministically at the hard budget |

Databricks reports that the companies it interviewed generally treated hard user cutoffs as a last resort and used visibility plus increasing friction first. This is an informal multi-company observation, not proof that high spend implies high productivity. The control lesson is narrower: detect accidental spend early, preserve an explicit terminal limit, and choose the terminal action by workload identity. Source: [Databricks, "Managing AI Coding Costs at Scale"](https://www.databricks.com/blog/managing-ai-coding-costs-scale), 2026-08-07.

Size every threshold from measured attempt volume, acceptance rate, spend distribution, and expected review load. The mechanics of virtual keys, per-team budgets, model allowlists, usage dashboards, and progressive spend policy are covered in [api-gateway.md](./api-gateway.md). A basic hard cap returns a `429` when exceeded. Warnings, approval gates, and downshifts require an explicit policy layer and tested client behavior; do not assume a gateway provides them because it exposes a budget field.

Budgets should be sized against measured cost per accepted task, not guessed from token averages alone. A threshold set too low blocks legitimate work and pushes people to route around it. A policy with no acceptance, retry, review, or workload-identity denominator is an invoice limit, not an economic model. Measure first (§2), then set the visibility, warning, approval, downshift, and terminal thresholds.

---

## 6. How to read a vendor's cost-reduction claim

Every vendor selling a cost-optimization tool eventually publishes a number: "cuts token costs by 50%," "twice as fast." The first question worth asking is not whether the number is true, but how the comparison was built.

**Worked example: Databricks.** Databricks reports two internal outcomes: more than 30% lower average task cost from Smart Router while roughly matching the most expensive model's quality, and almost 50% fewer generated tokens and associated costs after harness and cache tuning with no observed developer-quality degradation. The article also says its summary savings are directional and based on an informal survey. It does not publish the sample, model mix, token-class decomposition, paired tasks, acceptance instrument, review cost, or uncertainty. The correct classification is *useful operating evidence with missing denominators*, not a transferable benchmark. Databricks also provides the gateway and meta-harness products discussed in the article, so the product conflict belongs beside the result. See the full [resource evaluation](../../docs/resource-evaluations/databricks-managing-ai-coding-costs-scale.md).

**Paired beats unpaired.** The most common trap is comparing an average "before" cost across one set of tasks against an average "after" cost across a different set. If task difficulty spans orders of magnitude (a 50-token lookup next to a 50,000-token refactor), the composition of the sample dominates the result more than the tool does. A vendor can present two non-comparable samples without lying and still show an artificial gain. A paired design fixes this: measure the same task with and without the tool, and look at the per-task difference. Each task becomes its own control, which cancels out cross-task difficulty variance.

**Sign test vs. paired t-test.** Once pairs are in hand, two classic tests compete for the job. A paired t-test assumes the differences are roughly normal and is sensitive to outliers: one task where the tool fails outright (a timeout, a runaway loop, a cost spike) can swing the whole mean. Cost and latency distributions are typically heavy-tailed, most tasks look similar, but a handful can cost 10 to 100 times more. In that setting the sign test holds up better against outliers: it ignores the magnitude of each difference and counts only, per pair, whether the tool did better or worse. Less statistical power, but it survives small samples where normality can't be checked.

**The significance ceiling at small n.** The sign test has a mathematical limit few readers know about. At n=6 pairs, the best achievable two-sided p-value is about 0.031 (2 × 0.5⁶), and that result requires the tool to win all 6 pairs with no exception. At 6 samples, only one configuration out of 64 clears the conventional 0.05 threshold, and it happens to be the perfect score. If a vendor reports a "significant" sign test on 6 or 8 tasks, check that the reported result is actually the maximum possible score. If it isn't, the test was likely misapplied.

**Reading a bootstrap confidence interval.** Bootstrapping resamples the observed data, with replacement, thousands of times to estimate the distribution of a statistic such as the median gain. The resulting interval gives a plausible range, not a certainty. A simple red flag is a very wide interval built on a small n. If a vendor reports "median gain of 40%, 95% CI between 5% and 90%," the interval spans a huge range, which means the sample is too small to settle the question. An impressive headline number paired with that wide an interval is a reason to ask for the full sample rather than the promoted mean.

**Median beats aggregate.** Citing the median is a more conservative choice than citing a mean or an aggregate total, precisely because the median resists outliers. A mean can be pulled upward by a single exceptional task, while the median reflects the typical case. When a vendor reports a mean rather than a median without justifying the choice, and never shows the underlying distribution, that omission is worth asking about.

**A token-volume cut is not a dollar cut.** The API prices token classes very differently. On Opus 4.8 (July 2026), model output runs $25 per million, fresh input $5, a cache read $0.50. Output is 50 times a cache read. So a tool that removes a large slab of cache_read tokens (a bloated tool catalog, a stale history) can advertise a 33% cut in token volume and deliver closer to 10% off the bill, because it trimmed the cheapest class. The reverse also holds: a tool that shortens the model's own output attacks the most expensive class and moves the dollar figure more than its token count suggests. When a claim is denominated in tokens, ask which class those tokens belong to before assuming the dollar figure follows.

**A generic illustration.** Say a tool claims "35% average token-cost reduction" across 20 tasks. If 18 of them show a 10 to 15% gain and 2 show a 300% gain (because the old pipeline happened to loop on exactly those cases), the overall average is dominated by those 2 outliers. The median tells a different, more representative story of what a typical task should expect.

**What a full evaluation covers: the SWE-bench Lite case.** This coding-agent benchmark measures the resolution rate of real GitHub issues, not just execution speed or cost. A tool that is twice as cheap but resolves half as many tickets is not a net improvement. That is a trade-off that needs pricing on both axes at once. Any cost claim that never mentions the associated success rate is telling an incomplete story (Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", 2023, [arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)).

A short checklist for the next "X% faster/cheaper" claim: is the comparison paired (same task, before and after), or two separate samples? Is the sample under 10 tasks, in which case a "significant" result needs to be near-perfect to actually be one? Is the cited number a median or a mean, and is the full distribution shown anywhere? Is the reduction quoted in token volume or in dollars, and if tokens, which class (output, fresh input, or the far cheaper cache read)? Is a confidence interval given, and is it tight or does it span a huge range? Is a success or quality rate mentioned alongside the cost, or is cost the only thing highlighted? Without these answers, a performance number is a marketing claim dressed in statistics, not evidence.

---

## 7. What this page does not cover yet

This page reasons about the cost model. It deliberately does not include:

- **A proprietary benchmark.** There is no measured dataset of cost-per-PR across teams here. The numbers in §2 are illustrative to teach the method, not results.
- **A provider pricing comparison.** Per-token prices change often enough that a comparison table would be stale within a release or two. For current rates, check the provider's pricing page and the live figures that tools like `ccusage` read from your own sessions.
- **A business-value model.** This page treats human-accepted work as the quality denominator. It does not price revenue per feature, defects avoided, customer impact, or regulatory risk. Connecting accepted engineering work to business value remains a separate exercise per team.

If you have measured attempts, acceptance decisions, retries, review time, and rework from your own workflow, use that evidence instead of the illustrative token budget in §2. Treat this page as a measurement framework, not a fleet benchmark.

---

## See Also

- [api-gateway.md](./api-gateway.md) for the technical implementation of budgets, virtual keys, and per-team caps
- [observability.md](./observability.md) for per-session cost estimation and the tools that read exact token counts
- [practitioner-insights.md](../ecosystem/practitioner-insights.md) for the field reports referenced here in full context
- [Databricks cost-management resource evaluation](../../docs/resource-evaluations/databricks-managing-ai-coding-costs-scale.md) for the routing, cache, and progressive-budget evidence boundaries
