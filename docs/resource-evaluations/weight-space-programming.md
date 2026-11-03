# Sparks of Weight-Space Programming (MIT CSAIL, November 2026)

**Reviewed**: 2026-11-03. **Initial and final score**: 3/5, integrated as a case study in [Autonomous Research Loops](../../guide/ecosystem/ai-ecosystem.md#case-study-when-the-loop-repairs-the-baseline).

The post is not about Claude Code. Its value for this guide is the Qwen experiment, an autonomous edit-measure-keep loop whose headline gain comes mostly from repairing a degenerate baseline. That is a failure mode any `/autoresearch` user can run into on code.

## Sources and evidence

| Source | Contribution | Limit |
|---|---|---|
| [Takehi, Teoh, Zhang, Khattab, blog post](https://rikiyat.github.io/blog/weight-space-programming/), 2026-11-02 | Eight experiments in which `gpt-6-astra` reads or writes small networks and edits Qwen3.5-0.8B | Blog post, no peer review; no human or algorithmic baseline for the "well past what we'd expect from humans or conventional algorithms" claim |
| [Experiment logs](https://github.com/RikiyaT/lm_understand-logs), read 2026-11-03 | Prompts, replies, code runs, forward-pass requests, evaluations and weight diffs; 1,125 turns audited as tool-free by the authors | Earlier prompt versions, working folders and the harness code are not published |
| [Experiment 8 README](https://github.com/RikiyaT/lm_understand-logs/blob/main/exp8_math/README.md) and [results excerpt](https://github.com/RikiyaT/lm_understand-logs/blob/main/exp8_math/eval/RESULTS_excerpt.md) | Run table, three different edits for 10, 25 and 50 passes, truncation shares, unreported prompt versions, Gemma follow-up | One run per budget, no variance across runs |
| [First prompt of the 50-pass run](https://github.com/RikiyaT/lm_understand-logs/blob/main/exp8_math/runs/p50c/turns/t001/prompt.txt) | Shows that the task named repetition as an in-scope failure to repair | Read for one run only |
| [Edited checkpoint model card](https://huggingface.co/RikiyaT/Qwen3.5-0.8B-weight-space-programming), read 2026-11-03 | Third-party re-run (akhaliq with ML Intern, 2026-11-02): 51.0% on MATH-500, 500 problems x 4 samples, 31.6% truncated | Base model re-tested on a 25-problem smoke test only (5.0%, 95% truncated); same sampling as the post |
| [Qwen3.5-0.8B model card](https://huggingface.co/Qwen/Qwen3.5-0.8B), read 2026-11-03 | Thinking-loop warning, recommended sampling, IFEval 44.0 (thinking) and 52.1 (non-thinking) at temperature 1.0 | Different harness; MATH-500 not reported on the card |
| [Hacker News thread](https://news.ycombinator.com/item?id=50341174), [top-ranked comment](https://news.ycombinator.com/item?id=50347685), 2026-11-03 | Critique from a commenter who states research in weight-space learning: prior art (ROME), small networks, steering vector, no evidence for the superhuman framing | Pseudonymous; affiliation not verified; dates ROME to 2023, the paper is from 2022 |
| [ROME](https://rome.baulab.info/), Meng et al., NeurIPS 2022 | Prior art for targeted weight edits (rank-one MLP updates) | Factual associations, not behavior repair |
| [Arditi et al., "Refusal in Language Models Is Mediated by a Single Direction"](https://arxiv.org/abs/2406.11717), arXiv 2024-06-17 | Prior art for removing one direction from the weights to remove a behavior (refusal) | Title and date checked through the arXiv API; the paper body was not re-read for this evaluation |

## What holds

- The edited checkpoint scores as reported under the post's protocol, confirmed by an independent re-run.
- Experiment 3 (language and copying heads from the middle blocks of three character-level transformers, no forward pass, ground truth measured separately) is the best-controlled reading result.
- The logs include every prompt, reply, code run and evaluation behind the reported runs, which makes the critique below checkable.

## What does not hold as stated

- **Capability gain.** 93% of the unedited model's MATH-500 answers hit the 32,768-token limit. The gain coincides with a drop in truncation (33.1% after the 50-pass edit); with one run per budget, the logs do not separate the two effects. The authors write that "Fixing loops, however, is not the same as making a model better at math", and the Gemma 3 270M follow-up, which does not loop, moved from 6.8 to at most 7.7.
- **Diagnosis found by the model.** The prompt named repetition as the example failure. A later prompt version without that example submitted no edit at 10 passes, and matched the published score at 25.
- **Baseline.** The evaluation uses temperature 0.6 and presence penalty 1.5 for the base model, while the model card reports benchmarks at temperature 1.0. No published run compares the edit with the base model at the card's settings, in non-thinking mode, or with a token budget.
- **Novelty of the edit.** The 10-pass edit is `W' = W - 1.5 u(u^T W)` on 30 matrices, a rank-one subtraction of the same family as directional ablation, scaled by 1.5 rather than a plain projection. The 25-pass edit zeroes one attention head. The 50-pass edit subtracts the direction from 64 output columns of the MLPs in layers 15 and 19.
- **Game-playing networks.** One-shot networks beat PPO at 100M steps in three MinAtar games but lose to PPO at 500M steps in Seaquest (53.1 against 88.9). The model was given each game's source code. The post gives no win rates for Go.

## Not verified here

- That `gpt-6-astra` is a publicly available OpenAI model. The logs name it; a Perplexity research pass reported an OpenAI announcement dated 2026-09-03, not opened for this evaluation.
- Reactions and partial reproductions on X (Krentsel, Singh, Angel, Wegner), Latent Space and Turing Post, reported by the same research pass.
- Any decoding-only fix for Qwen3.5-0.8B loops. This evaluation ran no model.

## Decision

Integrate as a case study in the autoresearch section: six checks for any measure-and-keep loop, each tied to an observation in the logs. Do not cite the post as evidence that models can improve other models' capabilities, or that they outperform humans at reading weights.

## Technical challenge

A separate guide-reviewer pass on 2026-11-03 checked internal consistency and editorial markers across the guide subsection, this file, the index row and the CHANGELOG entry; it could not fetch the primary sources. It flagged causal wording ("tracks", "mostly loop repair"), an overstated identity with Arditi et al., the attribution of `gpt-6-astra` stated as fact, two unsourced superlatives and a check that was generic. All were corrected. The numbers and quotes it could not check were read at source during the evaluation: the logs README, results excerpt and first prompt, both model cards and the Hacker News API, on 2026-11-03.
