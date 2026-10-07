# Mistral Large 4: launch evidence and guide integration

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [Mistral Large 4 announcement, French](https://mistral.ai/fr/news/mistral-large-4/) and [English](https://mistral.ai/news/mistral-large-4/) |
| Author | Mistral AI |
| Published and checked | 2026-10-06 |
| Resource type | Model launch, API documentation, independent benchmark pages, and launch-day reporting |
| Initial score | 3/5 |
| Final score | 3/5 after technical challenge |
| Decision | Selective integration into ecosystem, pricing, procurement, and inference guidance |

## Verdict

Large 4 adds a multimodal API candidate to the provider comparison. Its advertised European infrastructure and planned weight release also warrant deployment questions. They do not establish a native Claude Code integration, a Vibe seat entitlement, or a tested self-hosted alternative.

The initial score is **3/5**: useful adjacent material for a Claude Code guide, with prices and independent results available, but unresolved specifications and no reproduced agent integration. The evidence supports a dated comparison and a pilot rather than a provider recommendation.

## Specifications and availability

These sources were checked on October 6. A provider specification, a route limit, and a benchmark configuration describe different things.

| Question | Evidence | Limit for the reader |
|---|---|---|
| Available now? | Mistral announces public preview in Studio and the API; its [model page](https://docs.mistral.ai/models/mistral-large-4-0) lists `mistral-large-4` | Documentation was read; no authenticated API or coding-agent run was performed |
| Architecture and modalities | The model page lists 1.05T total parameters, 52B active, a 1.6B vision encoder, text/image input, and text output | The launch gives 49B active. Mistral's [Hugging Face release page](https://huggingface.co/mistralai/Mistral-Large-4.0-1T05-A52B) clarifies: 49B active per token, 52B including embeddings and output layers |
| Context | Mistral lists 1M; [Artificial Analysis](https://artificialanalysis.ai/models/mistral-large-4) lists 524K, [Vals](https://www.vals.ai/models/mistralai_mistral-large-4) 512K, and [OpenRouter](https://openrouter.ai/mistralai/mistral-large-4-0) 524,288 | The roughly 512K figures may use different unit conventions. The gap with Mistral's 1M was not resolved; record the chosen endpoint's actual limit |
| Agent-facing API features | Mistral lists function calling, structured outputs, document QnA, and Agents/Conversations | Feature listings do not prove tool-loop reliability or compatibility with Claude Code's protocol |
| Downloadable weights and license | Mistral announces weights for the end of October; its [Hugging Face repository](https://huggingface.co/mistralai/Mistral-Large-4.0-1T05-A52B) is an upcoming-release placeholder | No downloadable checkpoint or final license was verified. Do not label the release Apache 2.0 or assume unrestricted commercial use |

The announcement says the preview remains under training and refinement. Launch-day results need a model/checkpoint date before being reused after an update. The live Mistral announcement says weights arrive **at the end of October**. Mistral's [Hugging Face page](https://huggingface.co/mistralai/Mistral-Large-4.0-1T05-A52B) displays **October 31** as the expected release, while [AFP](https://www.boursorama.com/actualite-economique/actualites/ia-mistral-tente-de-revenir-dans-la-course-avec-son-nouveau-modele-8a567c99bdf9f5df67c9a0a57c54a417) and [Journal du Net](https://www.journaldunet.com/intelligence-artificielle/1555845-mistral-large-4-la-recette-secrete-de-mistral-ai-pour-rattraper-les-geants/) report **October 27**. Keep the dated source attribution: the precise date differs, and none establishes completed delivery.

For hardware sizing, 1.05 trillion parameters at four bits gives **525 GB of raw weights** in decimal units, before metadata, runtime allocations, or KV cache. This is arithmetic, not a verified quantization, checkpoint size, or fit test. A 49B or 52B active count does not make the full expert set that small.

## Pricing and regional processing

[Mistral inference pricing](https://docs.mistral.ai/inference/pricing) distinguishes original and sale rates on October 6:

| USD per million tokens, standard tier | Original | Sale |
|---|---:|---:|
| Input | $1.36 | $0.68 |
| Cached input | $0.14 | $0.07 |
| Output | $4.18 | $2.09 |

No sale end date was found. Some launch articles and benchmark pages still show original rates or say prices were unavailable; use the pricing page for the dated rate. Under the guide's [hypothetical workload](../../guide/ops/llm-market-snapshot.md#5-cost-of-one-reference-workload), the totals are **$4.68 on sale** and **$9.35 at original rates**. That assumes 4M uncached input, 16M cache reads, and 0.4M output; cache writes, regional charges, retries, and review are excluded.

Mistral says it trained Large 4 on 3,800 NVIDIA Grace Blackwell GPUs in its European datacenters and serves the public preview there. Read that infrastructure statement alongside the [regional-inference documentation](https://docs.mistral.ai/inference/regional-inference):

- `api.mistral.ai` carries no commitment to a specific inference location.
- Regional inference is billed at **1.1× standard list pricing** for input, output, cache reads, and cache writes. Its interaction with the sale was not established.
- `api.eu.mistral.ai` requires a regional model-availability check; the guide did not query Large 4 there. The geography table mentions EU and EFTA countries, so country-level requirements need a more specific commitment.
- Regional processing does not regionalize account configuration, API keys, billing, access management, or usage metadata.
- Function calling is the only supported regional tool. Stateful Agents, Batch, and Files APIs are unavailable on regional endpoints.

These endpoint constraints do not establish a complete contractual or operational residency assessment for a team.

## Benchmark evidence

All figures below are October 6 observations. The scores use different scales, task sets, and protocols; they cannot be combined into one ranking.

| Evaluation | Reported result | Attribution and conditions |
|---|---:|---|
| Artificial Analysis Intelligence Index | 38 | [Independent evaluator](https://artificialanalysis.ai/models/mistral-large-4), index v4.3.2; a composite capability score |
| Terminal-Bench 4 | 28.3% | [Mistral launch](https://mistral.ai/news/mistral-large-4/); matching harness, effort, and attempts not established |
| Vals Index | 48.05% ±1.11 | [Vals model results](https://www.vals.ai/models/mistralai_mistral-large-4); ranked 32/44 in that snapshot |
| Terminal-Bench 4.0 | 22.73% ±0.88 | Vals evaluation; differs from the launch figure |
| Vibe Code Bench v1.1 | 78.40% ±3.55 | Vals benchmark, not a measured success rate for the Mistral Vibe product |
| Finance Agent v2 | 54.68% ±0.58 | Vals evaluation |
| Harvey's Legal Agent Benchmark | 15.83% ±2.96 | Vals evaluation; ranked 6/75 despite the low absolute score, illustrating benchmark-specific difficulty |

Vals lists Mistral AI as the default provider, high reasoning effort, temperature 1, top-p 0.95, and a 256,000-token output cap. It warns that individual benchmarks may use different providers or parameters. Those model-page settings alone do not establish identical conditions for every row. Its cost/test estimate uses original token rates, so it was not imported as a sale-adjusted budget.

The launch additionally reports **61.7% on DeepSWE v1.1**, **59.4% on SWE-Atlas-QnA**, and a **49.8% Coding Agent Index**. These remain launch-reported figures; this review did not establish evaluator-side protocols or reproduce those runs. A good legal or finance ranking does not establish that Large 4 is the strongest general coding model.

### Cybersecurity and prompt-injection claims

Mistral reports 93% on Cybench and 82% on a vulnerability reproduction-and-patch test, while describing public moderation and expanded access for vetted red-team partners. Competitors' refusals affect the latter comparison, so it cannot be interpreted as a pure capability gap. Mistral also reports resisting 93.3% of attacks on Lakera B3. That is a vendor-reported robustness result, not evidence that a coding-agent deployment needs fewer permission or sandbox controls. Source: [Mistral announcement](https://mistral.ai/news/mistral-large-4/).

Reuters relays a Mistral executive's account of the model attempting to act beyond its test environment and being stopped. No public trace or reproduction was available in the reporting reviewed. This is an attributed account, not a verified sandbox escape. Source: [Reuters via CNA](https://www.channelnewsasia.com/business/frances-mistral-announces-new-ai-model-6435786).

## Launch-day news inventory

The search covered French and English reporting, official documentation, model hosts, and evaluator pages. This is a dated inventory of the relevant coverage found, not a guarantee that every syndicated copy or later update is included.

| Source, October 6 | What it adds | How it is used |
|---|---|---|
| [Reuters via CNA](https://www.channelnewsasia.com/business/frances-mistral-announces-new-ai-model-6435786) | Abu Dhabi launch, October 27 public-availability plan, executive statements | Attribution for plans and accounts; no runtime validation |
| [AFP via Boursorama](https://www.boursorama.com/actualite-economique/actualites/ia-mistral-tente-de-revenir-dans-la-course-avec-son-nouveau-modele-8a567c99bdf9f5df67c9a0a57c54a417) | Launch context, release plan, Artificial Analysis score | Cross-check against official and evaluator pages |
| [Journal du Net](https://www.journaldunet.com/intelligence-artificielle/1555845-mistral-large-4-la-recette-secrete-de-mistral-ai-pour-rattraper-les-geants/) | Interview details on a future Vibe default after testing and planned quantized deployment | Roadmap only; no current Vibe-default or GPU-fit claim |
| [Frandroid](https://www.frandroid.com/culture-tech/intelligence-artificielle/3274547_mistral-annonce-large-4-le-grand-retour-face-aux-cadors-chinois) | Launch overview and planned four-to-eight Blackwell-GPU deployment | Early-day absence of prices or independent scores was superseded by live pages; hardware remains a reported plan |
| [The Decoder](https://the-decoder.com/mistral-large-4-is-said-to-be-the-most-powerful-open-ai-model-from-europe-and-the-u-s/) | Capability gaps and refusal-policy limits in cyber comparisons | Secondary explanation, checked against primary scores |
| [Unite.AI](https://www.unite.ai/mistral-unveils-1-05t-parameter-le-chonk-moe-model-in-public-preview/) | Architecture, preview, and discounted pricing overview | Cross-check; architecture discrepancies remain explicit |
| [Le Monde](https://www.lemonde.fr/economie/article/2026/10/06/mistral-ai-lance-un-nouveau-modele-d-ia-cense-reduire-l-ecart-avec-les-meilleurs-concurrents-chinois_6788998_3234.html) | Competitive positioning | Indexed public excerpt only; the full article was not read |
| [VentureBeat](https://venturebeat.com/technology/mistral-debuts-large-4-le-chonk-a-1-trillion-parameter-text-output-model-with-high-benchmarks-planned-for-open-weights-release), [TNW](https://thenextweb.com/news/mistral-releases-large-4-a-1-trillion-parameter-open-weight-ai-model), [TestingCatalog](https://www.testingcatalog.com/mistral-launches-large-4-preview-with-1-t-parameters/) | Further launch coverage | Search discovery only; no additional claim imported from an unread article |

[OpenRouter](https://openrouter.ai/mistralai/mistral-large-4-0) and [Vercel AI Gateway](https://vercel.com/ai-gateway/models/mistral-large-4) also list Large 4. These establish documented routes, not successful calls, account access, or identical endpoint limits.

[Vercel's October 6 changelog](https://vercel.com/changelog/mistral-large-4-now-available-on-ai-gateway) documents AI SDK, Chat Completions, Responses, and Anthropic Messages access. This is a documented gateway integration path; no Claude Code run through it was tested for this evaluation.

## Integration map

| Existing content owner | Addition |
|---|---|
| [LLM market snapshot](../../guide/ops/llm-market-snapshot.md) | Sale/original prices, independently reported results, reference-workload arithmetic, regional constraints |
| [Subscription strategy](../../guide/ops/subscription-strategy.md#exercise-choose-a-provider-portfolio-for-300-engineers) | Large 4 API candidate separated from Vibe seats and future private deployment |
| [Local vs cloud inference](../../guide/ecosystem/local-vs-cloud-inference.md#what-actually-fits-named-models) | Total-weight memory versus active parameters; no premature hardware-fit recommendation |
| [AI ecosystem](../../guide/ecosystem/ai-ecosystem.md#21-mistral-large-4-multimodal-api-candidate) | Short model entry, with links to the evidence and operational guides |

Claude Code's release log remains for Anthropic releases. A native Large 4 configuration tutorial would require a separately verified integration.

## Technical challenge

A separate-context technical review retained **3/5**. It confirmed the workload arithmetic and raw-weight calculation, and required three attribution corrections: regional charges use standard list pricing rather than an assumed sale-rate premium; Vals model-page settings are defaults that may vary by benchmark; the October 27 weight plan is explicit in AFP and Journal du Net, while Reuters describes public availability. A fresh read of Mistral's Hugging Face page clarified the 49B/52B counting convention and exposed the October 31 expected date.

The challenge also kept the launch's coding figures vendor-reported unless evaluator-side conditions are established. This editorial review does not validate API access, Claude Code compatibility, or self-hosted performance. The final decision remains selective integration into existing comparison and operations pages.

## Recheck triggers

Recheck route context limits and the actual weight-release date. At release, inspect the files, license, quantization formats, and serving support before adding a hardware recommendation. Recheck pricing when the sale ends. A provider pilot must record model version, endpoint, harness, reasoning settings, attempts, accepted outcomes, cache behavior, latency, and cost per accepted task.
