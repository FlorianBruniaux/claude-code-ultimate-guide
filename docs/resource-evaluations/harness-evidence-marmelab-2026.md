# Harness evidence: Marmelab and comparative studies

**Reviewed**: 2026-09-26. **Score**: 4/5 for selective integration into existing pages.

## Source roles

| Source | Contribution | Evidence boundary |
|---|---|---|
| [François Zaninotto, The State Of AI Harness Engineering 2026](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html) | Harness tests, permitted cases, usage observation and retirement of obsolete controls | Repository inventory and practitioner synthesis; corpus counts were not reproduced. The author discloses maintaining Atomic CRM, one of the selected projects. |
| [The Scaffold Effect, v1](https://arxiv.org/html/2607.22585v1) | Compare model-harness pairs and separate token efficiency from financial outcomes | Limited benchmark sample; local billing, review cost and equivalent quality are not established by its token ratio. |
| [Natural-Language Agent Harnesses, v1](https://arxiv.org/html/2603.25723v1) | Verifier ablations and disagreement between intermediate and final acceptance | Results concern the sampled tasks and tested runtime, not every independent reviewer. |
| [Code Review Agent Benchmark, v3](https://arxiv.org/html/2603.23448v3) | Inspect executable review evaluators and their repair stage | Selected human concerns and structural tests constrain what the score means. |
| [Evaluating AGENTS.md, v1](https://arxiv.org/html/2602.11988v1) | Qualify context-file claims | See the [corrected source evaluation](./agents-md-empirical-study-2602-11988.md); retain study conditions. |
| [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Durable progress and application checks across sessions | First-party implementation experience; no local recovery or browser test was executed for this integration. |

## Editorial decision

Use existing sections in [Agent Harness Engineering](../../guide/core/agent-harness.md), [Agent Evaluation](../../guide/roles/agent-evaluation.md) and [Repository Harness Engineering](../../guide/ultimate-guide.md#925-repository-harness-engineering). A new general harness guide would duplicate their scope.

Correct the unsupported production-ceiling interpretation of c-CRAB. Add the verifier counterexample, positive and negative control tests, owner and retirement conditions, protected evaluation criteria and explicit uncertainty. Keep those procedures separate from reports of executed behavior.

## Technical challenge

An independent technical-writer review found no factual blocker in the new guide passages. It identified two older context-file summaries that contradicted the correction; both were revised, along with the corresponding note in Memory Systems. This review covers the added evidence and its nearby consistency, not all historical claims or executable examples in the guide.

## Limits

The supplied research synthesis was a discovery aid. Primary sources support the additions; the synthesis is not independent corroboration of the author's own articles. No repository benchmark was rerun, no complete Reddit or Hacker News corpus was collected, and no runtime deployment was validated. Current product inventories and older claims elsewhere in the guide remain outside this scoped revision.
