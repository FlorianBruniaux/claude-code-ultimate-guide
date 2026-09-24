# Jev / TypeSafe AI: typed decisions for software

**Status:** work in progress, reviewed September 21, 2026. **Initial and final score: 3/5**, retained after an independent editorial challenge. Decision: research candidate for routing and structured-decision workflows; no general performance recommendation or native Claude Code integration established.

## What the interface changes

TypeSafe's [September 15 announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev) introduces Jev as its first System One Model. The [API introduction](https://docs.typesafe.ai/introduction) describes a shared state and typed questions rather than a chat completion. Its primitives are [Choice](https://docs.typesafe.ai/primitives/choice), [Score](https://docs.typesafe.ai/primitives/score) and [Noul](https://docs.typesafe.ai/primitives/noul). They support different tasks: an exclusive choice, an ordinal assessment and a binary probability.

This is relevant to an agent harness that needs a bounded decision before selecting a skill, a document or another model. It does not establish Jev as a replacement backend for Claude Code's conversational tool loop.

## Claims that need their conditions

| Claim | Evidence and boundary |
|---|---|
| 193.6 times faster, 444.6 times cheaper | TypeSafe's own [workflow evaluations](https://evals.typesafe.ai/), described as the high end of expected gains. Its adapter makes comparison LLMs produce probability distributions, adding cost and latency. Reference answers come from other models, not human ground truth. |
| 150 ms | The launch article gives an approximate 70 to 500 ms range under its test conditions. This does not establish a universal latency guarantee. |
| $42 per billion input tokens | The [model documentation](https://docs.typesafe.ai/models) lists the direct-service price, equivalent to $0.042 per million. Workflow costs also include downstream calls and retries. |
| Free outputs forever | Output pricing is currently zero in the documented direct offering. A perpetual contractual guarantee was not established. |
| Zero hallucinations | The launch article defines the displayed zero through schema conformance, not empirical absence of wrong decisions. |
| Exact confidence | The [confidence documentation](https://docs.typesafe.ai/confidence) defines a distribution statistic. It must not be relabeled as the exact probability that a decision is correct. |
| A new architecture, claimed by the vendor | The materials reviewed do not provide enough architecture, training-data and objective details to reproduce Jev. No direct Jev/RLCD scientific paper was found in this search; that does not prove none exists. |

The [Jev 1.13 limitations page](https://docs.typesafe.ai/model-jaggedness/jev-1.13), reviewed by its publisher on September 17, documents injection susceptibility, context degradation and failures in numerical or date-related tasks. Schema validity does not remove these failure modes.

## Independent reports already exist

The [anisselbd phishing benchmark](https://github.com/anisselbd/jev-phishing-bench) reports 62.6% accuracy for Jev versus 81.3% for Haiku 4.5 on 2,000 emails with synthetic bodies. The initial protocol sends nine questions to Jev and requests a direct verdict from Haiku. A controlled comparison then fits regressions over the same five signals for both models. On its 1,000-email holdout, these workflows report 95.0% for Jev and 93.2% for Haiku, versus 91.8% for the rule baseline; the Jev/Haiku accuracy difference is not statistically significant (p=0.063). The dataset is strongly separable with simple rules. Test the complete workflow against a non-LLM baseline before transferring a headline score to another task.

Other original reports include [AbdelStark's classification pilot](https://github.com/AbdelStark/jev-benchmarks), [WallerChen's measurements](https://github.com/WallerChen/jev-measured) and [JevBench](https://github.com/fstandhartinger/jevbench). Their sample sizes, synthetic data, threshold selection and access paths require separate review. These reports were consulted, not rerun.

## What to measure before integration

Start with skill routing against a lexical BM25 baseline, ticket triage or RAG passage selection. Fix labels, model versions and prompts. Keep threshold calibration separate from the final test and group related paraphrases in the same split. Compare accuracy, automatic coverage, errors among accepted cases, end-to-end p50/p95 and cost per correct decision, including retries and escalation.

Use class probabilities for calibration metrics. Do not interpret a distribution-concentration statistic as correctness probability. [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html) supplies the calibration framework; [SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html) supplies risk/coverage definitions. These papers are background, not disclosures about Jev's internals.

## Editorial decision and review triggers

The score reflects relevance to bounded harness decisions and available documentation. It does not rate model quality. Keep the entry provisional until a representative local benchmark and the remaining community evidence have been reviewed. Revisit on a model/API change, a reproducible independent result or a formal RLCD disclosure. Any eventual guide addition should distinguish a suggested route from an authorization to execute an action.

No API test, deployment, account-specific data-policy review or production recommendation was performed for this evaluation.
