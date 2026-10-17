# Model axes infographics

Two editorial infographics in English, generated with Google Gemini (`gemini-3-pro-image`) and reviewed for text, arrows and claims against the pages that use them. They summarize the guide's prose; they do not describe Claude's internal architecture, which Anthropic does not publicly document.

| Topic | Image | Used in |
| --- | --- | --- |
| Eight terms, seven axes | [English infographic](model-axes-en-gemini.webp) | [AI Concept Boundaries](../../core/ai-concept-boundaries.md#architecture-size-class-modality-and-task) |
| Memory counts every expert, compute counts two | [English infographic](moe-memory-compute-en-gemini.webp) | [Local vs cloud inference](../../ecosystem/local-vs-cloud-inference.md#what-actually-fits-named-models) |

The axes infographic sorts eight common model terms by the axis they describe: model class, architecture, size class, input modality, training objective, task or product label, and representation unit. The labels are not exclusive categories; one model can combine several of them. The page table gives each row a source and the change it makes for a Claude Code user.

The MoE infographic uses Mixtral's published routing, two of eight experts per token at each layer, as an example. All experts stay in memory while only the selected ones compute. Other MoE models use different expert counts, and some alternate dense and MoE layers. Sources: [Mixtral of Experts](https://arxiv.org/html/2401.04088), [Switch Transformers](https://ar5iv.labs.arxiv.org/html/2101.03961).

Both assets are 1376 × 768 WebP files converted from the native JPEG responses at quality 90, without cropping, padding or upscaling. They follow the cream graph-paper style of the [harness review infographics](../harness-review/README.md). The pages carry equivalent prose and link to the full-size images for narrow screens.
