---
title: "Best-of-N and Verification Evidence"
description: "Primary research and local practitioner-evidence coverage for the Best-of-N and proof-log method"
tags: [evaluation, verification, best-of-n, evidence]
---

# Best-of-N and Verification Evidence

This record supports the bounded claims in [Best-of-N: Generate, Select, and Verify](../../guide/workflows/best-of-n.md). It distinguishes primary research from local practitioner evidence and does not treat either as proof that a workflow will work in every repository.

## Primary research used

| Source | What the paper directly supports | What it does not support |
| --- | --- | --- |
| Wang et al., 2022, [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) | Sampling diverse reasoning paths and selecting a consistent answer improved results on the paper's arithmetic and commonsense benchmarks. | A general guarantee for software changes, design decisions, majority vote, or self-review. |
| Lightman et al., 2023, [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) | In the reported MATH experiments, process supervision outperformed outcome supervision for their training setup. | That an LLM reviewer can replace executable repository checks. |
| Chow et al., 2024, [Inference-Aware Fine-Tuning for Best-of-N Sampling](https://arxiv.org/abs/2412.15287) | BoN selects the best response from multiple generated responses through a verifier; the paper reports task-specific gains and costs. | That a generator's preferred answer is a reliable verifier, or that the same N fits all tasks. |
| Kenton et al., 2024, [On scalable oversight with weak LLMs judging strong LLMs](https://arxiv.org/abs/2407.04622) | Oversight results varied by task. The authors report that best-of-n sampling had little effect on judge accuracy in their experimental setup. | A universal rejection of Best-of-N or a universal measure of reviewer independence. |

The protocol therefore requires a fixed rubric, an explicit stop rule, executable verification where possible, and recorded reviewer provenance. These are engineering controls. The papers motivate testing them; they do not certify the controls for an unmeasured workflow.

## Local YouTube practitioner-evidence check

**Date:** 2026-08-31  
**Tool:** `/Users/florianbruniaux/Sites/perso/yt-insights/.venv/bin/yt-insights`  
**Mode:** read-only local search only. No discovery, subtitle download, indexing, model inference, or network acquisition was requested.

| Query or inspection | Result | Coverage consequence |
| --- | --- | --- |
| `yt-insights catalog stats` | `Error: catalog database is unavailable or invalid` | No durable catalog counts were available. |
| `yt-insights search "best of n" --limit 10 --json` | `Error: Search index does not exist. Run 'yt-insights index' first.` | No timestamped transcript matches were available. |
| `yt-insights search "verification testing" --limit 10 --json` | Not run after the missing-index result. | The second query would have the same absent-index boundary and would not add evidence. |

**Conclusion:** local practitioner evidence is `UNKNOWN`, not negative evidence. This page makes no claim about YouTube coverage, creator practice, or video recommendations. A future evidence pass must record the configured database path, corpus acquisition date, indexed channels and languages, exact query, result count, video IDs, timestamps, and transcript provenance before citing a practitioner statement.

## Method boundary

The workflow distinguishes candidate generation, selection, synthesis, majority vote, executable verification, and independent review because they make different claims. A majority can select a frequent answer without testing it. A synthesis creates a new artifact. A green command proves only the behavior exercised in its recorded environment. An independent reviewer is a control with measurable context separation, not a status label.

The portable [verification proof-log template](../../examples/claude-md/TESTING.md) records those boundaries so a human or another agent can inspect what was actually run, rejected, or left unknown.
