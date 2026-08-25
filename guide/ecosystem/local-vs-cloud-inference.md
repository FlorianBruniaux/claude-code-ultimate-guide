---
title: "Local vs Cloud: LLM Hardware and Inference Economics"
description: "Comparable hardware builds for running large open-weight models locally, cloud GPU rental pricing, and cloud API throughput for Claude and GPT-5.6, with sourced numbers and a decision framework"
tags: [ecosystem, hardware, local-llm, cloud, cost, benchmarks]
---

# Local vs Cloud: LLM Hardware and Inference Economics

> **Reading time**: ≈20 minutes
>
> **Purpose**: Answer one question with numbers instead of vibes: for running a large open-weight model (70B to 400B+ parameters), when does a local hardware purchase beat renting a cloud GPU or paying per token, and what actually fits on what machine.

---

## Table of Contents

- [Data Snapshot Date](#data-snapshot-date)
- [Sizing Local Hardware with llmfit](#sizing-local-hardware-with-llmfit)
- [Ten Comparable Hardware Configurations](#ten-comparable-hardware-configurations)
- [What Actually Fits: Named Models](#what-actually-fits-named-models)
- [Cloud GPU Rental Pricing](#cloud-gpu-rental-pricing)
- [One-Year Cost Projections](#one-year-cost-projections)
- [Cloud API Throughput: Claude vs GPT-5.6](#cloud-api-throughput-claude-vs-gpt-56)
- [Why Cloud and Local Tokens/Sec Are Not Comparable](#why-cloud-and-local-tokenssec-are-not-comparable)
- [Decision Diagram](#decision-diagram)
- [Decision Framework](#decision-framework)
- [Switching Providers at the CLI Level](#switching-providers-at-the-cli-level)

---

## Data Snapshot Date

Every price, spec, and throughput number on this page is a snapshot from **August 2026**. GPU prices move by double digits in weeks, cloud providers reprice without notice, and model families get replaced. Treat the tables as a method to reproduce, not a permanent price list. The queries and CLI commands used to produce this page are included so you can rerun them.

For a live view instead of this fixed snapshot, two trackers update continuously rather than on a fixed schedule: [llm-stats.com](https://llm-stats.com/llm-updates) (benchmark scores, arena votes, and API pricing pulled directly from providers) and [benchlm.ai](https://benchlm.ai/) (401+ models across 46 leaderboard categories, including tokens/sec and time-to-first-token, explicitly excluding algorithmically-generated benchmark data). Neither replaces the hardware-fit math on this page, which still needs `llmfit` against your own target model.

---

## Sizing Local Hardware with llmfit

Before buying anything, check what a given memory budget can actually run. [`llmfit`](https://github.com/AlexsJones/llmfit) (MIT, `brew install llmfit`) detects your hardware and scores its model database for fit, speed, and quality.

```bash
llmfit system                                    # detect current hardware
llmfit --memory 96G --ram 128G fit --json         # simulate a different memory budget
llmfit --memory 96G --ram 128G info "meta-llama/Llama-3.3-70B-Instruct"
```

Two limits to know before trusting its output:

**`--memory` overrides GPU VRAM, `--ram` overrides system RAM. They are not interchangeable.** On a discrete Nvidia GPU, only VRAM holds model weights during normal inference; system RAM is not usable for that purpose except through CPU offload, which drops throughput below 5 tokens/sec. On Apple Silicon and AMD's Ryzen AI unified-memory chips, the two numbers should be set equal, because there is only one physical memory pool.

**The tool cannot switch inference backend.** It detects the backend of the machine it runs on (Metal, CUDA, ROCm) and keeps using that backend's speed model even when you override memory size to simulate different hardware. Run it on an Nvidia machine for Nvidia numbers, an Apple Silicon machine for Apple numbers. Simulating an RTX PRO 6000 from a MacBook gives you a correct memory-capacity answer (what fits) and a wrong throughput answer (tokens/sec), because the tool is still computing speed from the Mac's Metal roofline model, not from CUDA.

---

## Ten Comparable Hardware Configurations

Bare GPUs are not comparable to laptops or appliances. The table below only lists complete systems: CPU, memory, GPU, and storage together, sorted by increasing price. For workstation builds around a bare Nvidia GPU (no fixed CPU from the vendor), the CPU column shows one realistic example, not a spec.

| # | Configuration | CPU | System memory | GPU | Storage | Price (Aug 2026) |
|---|---|---|---|---|---|---|
| 1 | AMD Ryzen AI Halo | Ryzen AI Max+ 395, Zen 5, 16 cores/32 threads | 128 GB unified LPDDR5x | Radeon 8060S integrated, 40 CU RDNA 3.5, no dedicated VRAM | 2 TB SSD | ≈$3,999 (≈€3,700-4,000) |
| 2 | NVIDIA DGX Spark | Grace, 20 Arm cores (10x Cortex-X925 + 10x Cortex-A725) | 128 GB unified LPDDR5x | GB10 Blackwell, 6,144 CUDA cores (48 SM), no dedicated VRAM | 4 TB NVMe (included) | ≈$4,699 (≈€4,180-4,700) |
| 3 | MacBook Pro, Apple M5 Pro | Apple M5 Pro, 15 or 18 cores | 48 GB unified | Integrated GPU, 20 cores | 2 TB SSD | ≈€4,500-5,000 |
| 4 | Workstation, 1x RTX 5090 | *Example*: AMD Ryzen 9 9950X, 16 cores | 64-128 GB DDR5 (host only) | RTX 5090, 21,760 CUDA cores, 32 GB GDDR7 dedicated | 2-4 TB NVMe | ≈€5,000-6,000 |
| 5 | MacBook Pro, Apple M5 Max | Apple M5 Max, 18 cores | 128 GB unified | Integrated GPU, 40 cores | 2 TB SSD | ≈€5,500-6,500 |
| 6 | AMD Ryzen AI Max PRO 400 ("Gorgon Halo") | Ryzen AI Max+ PRO 495, Zen 5, 16 cores/32 threads, up to 5.2 GHz | 192 GB unified + 160 GB dedicated graphics memory | Radeon 8065S integrated, 40 CU RDNA 3.5 | 2-4 TB (estimated) | Unannounced, ≈€5,000-10,000 est. (Q3 2026 launch, no independent benchmark exists) |
| 7 | Workstation, dual RTX 5090 | *Example*: AMD Threadripper 7960X, 24 cores | 128-256 GB DDR5 (host only) | 2x RTX 5090, 43,520 CUDA cores combined, 64 GB GDDR7 combined, no NVLink | 4 TB NVMe | ≈€8,000-12,000 |
| 8 | Mac Studio, Apple M5 Ultra | Apple M5 Ultra, 36 cores | 256 GB unified | Integrated GPU, 80 cores | 4 TB SSD | ≈€12,000 |
| 9 | Workstation, RTX PRO 6000 Blackwell | *Example*: AMD Threadripper PRO 7975WX, 32 cores | 128-256 GB DDR5 ECC (host only) | RTX PRO 6000, 24,064 CUDA cores, 96 GB GDDR7 ECC dedicated | 4 TB NVMe | ≈€16,000-18,000 (the card alone is ≈€14,000) |
| 10 | Workstation, dual RTX PRO 6000 Blackwell | *Example*: AMD Threadripper PRO 7995WX, 96 cores | 256 GB+ DDR5 ECC (host only) | 2x RTX PRO 6000, 48,128 CUDA cores combined, 192 GB GDDR7 combined, no NVLink | 4-8 TB NVMe | ≈€30,000-32,000+ |

Sources: Nvidia RTX 5090 and RTX PRO 6000 Blackwell core counts and VRAM confirmed via [Central Computer](https://www.centralcomputer.com/pny-nvidia-rtx-pro-6000-graphics-card-96gb-gddr6-24-064-cuda-cores-pci-express-5-0-x16-600w-vcnrtxpro6000b-pb.html) and [Schneider Digital](https://shop.schneider-digital.com/en/graphics-cards/nvidia/rtx-pro-blackwell-series/nvidia-rtx-pro-6000-blackwell-workstation-edition-96gb-pcie-5.0-x16) (card price ≈€14,000). GB10 specs from [Arm Learning Paths](https://learn.arm.com/learning-paths/laptops-and-desktops/dgx_spark_llamacpp/1_gb10_introduction/) and [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/). Radeon 8060S CU count from [TechPowerUp](https://www.techpowerup.com/342635/amd-readies-ryzen-ai-max-388-8c-16t-and-full-40-cu-radeon-8060s-gpu). Apple M5 Pro/Max chip specs (core counts, memory bandwidth, confirmed 24/48/64 GB tiers) from [Apple's own tech specs page](https://support.apple.com/en-mide/126318). Apple has not published M5 Ultra specs; the 256 GB / 36-core / 80-core figures come from pre-launch reporting, not an Apple source.

---

## What Actually Fits: Named Models

Sorting `llmfit`'s database by raw parameter count surfaces obscure or roleplay-oriented fine-tunes that happen to fit in memory, not the flagship models most people actually want to run. Querying `llmfit info` against each lab's own official repo (not a third-party quant mirror) gives a cleaner starting point, but `llmfit`'s HuggingFace scrape has its own data-quality gaps (see the Kimi K3 row below, where it was off by roughly 2x). Every parameter count and MoE expert count in this table was cross-checked a second time against each lab's own model card, GitHub repo, or official announcement, not `llmfit` alone.

This table uses the current generation as of August 2026, not the mid-2024/2025 models (Llama 3.x, Qwen2.5, Mixtral, original DeepSeek-V3) that dated an earlier version of this page.

| Hardware memory budget | Model that fits | Architecture | Full weight VRAM required |
|---|---|---|---|
| 32 GB VRAM (1x RTX 5090) | **`Qwen/Qwen3.8-27B`** (Aug 2026, Apache 2.0) | Dense, ≈27B | 14.2 GB, large headroom |
| 48 GB unified (MacBook Pro M5 Pro) | Qwen3.8-27B fits easily; **`meta-llama/Llama-4-Scout-17B-16E`** (109B total, MoE) does not quite fit | MoE, 17B active / 16 experts | 55.6 GB required, exceeds 48 GB |
| 64 GB VRAM (dual RTX 5090) | **`meta-llama/Llama-4-Scout-17B-16E`** | MoE, 109B total, 17B active | 55.6 GB, comfortable |
| 96-128 GB (RTX PRO 6000, Mac Studio M5 Max, DGX Spark, Ryzen AI Halo) | Llama-4-Scout fits with large headroom; no confirmed current-generation flagship lands specifically between 56 GB and 200 GB as of this snapshot | | |
| 192-256 GB (dual RTX PRO 6000, Mac Studio M5 Ultra) | **`meta-llama/Llama-4-Maverick-17B-128E`** (≈400B total, MoE) | MoE, 17B active / 128 experts | 205.7 GB, fits 256 GB, marginal on 192 GB |
| Any config on this page | **`zai-org/GLM-5.2`** (≈753B total, MoE, MIT). `GLM-5.3` (Aug 17, 2026) is the same base model with a post-training coding upgrade; weights ship staged, roughly two weeks after announcement | MoE, ≈40B active / 256 experts | 385.9 GB, exceeds everything here |
| Any config on this page | **`deepseek-ai/DeepSeek-V4-Pro-0813`** (1.6T total, MoE, MIT, GA Aug 13, 2026) | MoE, **49B active** (officially confirmed) | 845.4 GB, does not fit |
| Any config on this page | **`Qwen/Qwen3.8-2.4T-A95B`** (2.4T total, MoE, open-weight base of the hosted Qwen3.8-Max) | MoE, ≈95B active / 512 experts | 1,253 GB, does not fit |
| Any config on this page | **`MoonshotAI/Kimi-K3`** (**2.8T total**, confirmed via Moonshot's own GitHub repo, Aug 2026) | MoE, 16 of 896 experts active (≈50B active, calculated) | ≈1,430 GB estimated (extrapolated from DeepSeek-V4-Pro's VRAM-per-parameter ratio; `llmfit`'s own entry for this repo reports an incorrect 5,527B total and was not used) |

Sources for the officially-confirmed figures: [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B), [Llama 4 announcement](https://ai.meta.com/blog/llama-4-multimodal-intelligence/), [Llama-4-Scout model card](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E), [DeepSeek-V4-Pro model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro), [GLM-5.2 announcement](https://datanorth.ai/news/zhipu-ai-releases-glm-5-2), [Kimi K3 GitHub repo](https://github.com/MoonshotAI/Kimi-K3).

**MoE full weight is not optional, even though only a few experts compute per token.** `llmfit` reports both a "full model" VRAM figure and a much smaller "active" figure (for example DeepSeek-V4-Pro-0813 shows 845.4 GB full versus 63.6 GB active). The active figure describes the compute cost of a single forward pass, not what you can get away with loading. Because routing picks a different expert combination for every token, the entire expert set has to stay resident in memory (or be swapped in from very fast storage at a steep latency cost); there is no shortcut where only the "active" slice needs to fit. The full-weight column above is the one that determines whether a model runs on a given machine.

The frontier gap widened rather than narrowed since the previous generation covered here: DeepSeek-V3 needed 350.6 GB at 4-bit, its August 2026 successor DeepSeek-V4-Pro needs 845.4 GB, and neither Qwen's 2.4T-parameter MoE nor Moonshot's 5.5T-parameter Kimi-K3 fit on anything in this hardware lineup, including the €30,000+ dual RTX PRO 6000 workstation. Reaching that class of model requires either quantization aggressive enough that `llmfit` no longer rates it usable, or a budget and interconnect (NVLink-class, not the PCIe-only multi-GPU builds on this page) well past this page's scope.

---

## Cloud GPU Rental Pricing

Hourly, on-demand, per GPU. USD figures kept as published; EUR given only where the provider quotes EUR directly.

| Provider | GPU | Price/hour |
|---|---|---|
| OVHcloud | H100 80 GB | €2.80 ($2.99) |
| OVHcloud | A100 80 GB | $3.07 |
| OVHcloud | L40S 48 GB | $1.80 |
| RunPod (Secure Cloud) | L40S 48 GB | $0.99 |
| RunPod (Community Cloud) | L40S 48 GB | $0.79 |
| Lambda | H100 80 GB SXM | $3.99-4.29 depending on node size |
| Lambda | A6000 48 GB (RTX PRO 6000-class) | $1.09 |
| GMI Cloud | H100 80 GB | $2.00 |
| GMI Cloud | H200 | $2.60 |
| Hetzner (`GEX131`, dedicated bare-metal, not elastic hourly cloud) | RTX PRO 6000 Blackwell Max-Q 96 GB | €1.4247 (€889/month flat, excl. VAT) |
| Decentralized (Vast.ai-class marketplace) | H100 80 GB | $2.50-3.89 |
| AWS | H100 80 GB (no direct AWS tariff found; market range per [AltStreet](https://altstreet.investments/tools/gpu/gpu-price-comparison)) | $8.00-12.29, mid estimate $10 |
| AWS | H200, `p5en.48xlarge`, on-demand (8-GPU node, per GPU) | $7.91 |
| AWS | H200, `p5en.48xlarge`, spot (per GPU) | $3.37 |

AWS does not sell a single-GPU H200 instance: the smallest P5en node is already 8 GPUs at $63.30/hour total. For a "one GPU as a remote workstation" use case, OVHcloud, Lambda, GMI Cloud, or RunPod fit the shape of the need better than AWS. GMI Cloud in particular undercuts OVHcloud on H100 (\$2.00/h vs OVH's \$2.99/h). Hetzner's GEX131 is a dedicated server, not a per-second elastic cloud instance: it bills a flat monthly rate regardless of how many hours you actually use that month, which is why it doesn't appear in the hourly-prorated table below. Sources: [OVHcloud price list](https://us.ovhcloud.com/public-cloud/prices/), [Cloud Mercato H100-380](https://pcr.cloud-mercato.com/providers/ovh/flavors/H100-380), [Lambda pricing](https://lambda.ai/pricing), [RunPod L40S](https://www.runpod.io/gpu-models/l40s), [Vantage EC2 P5en](https://instances.vantage.sh/aws/ec2/p5en.48xlarge), [GMI Cloud pricing](https://www.gmicloud.ai/en/pricing), [Hetzner GEX131 press release](https://www.hetzner.com/pressroom/new-gex131/).

---

## One-Year Cost Projections

`annual cost = price/hour × hours/day × 365`. Three usage patterns, same GPU class (H100/H200), across providers.

| Provider / GPU | 4h/day | 8h/day | 24/7 |
|---|---|---|---|
| OVH H100 80 GB | ≈€4,088 | ≈€8,176 | ≈€24,528 |
| GMI Cloud H100 80 GB | ≈$2,920 (≈€2,716) | ≈$5,840 (≈€5,431) | ≈$17,520 (≈€16,294) |
| GMI Cloud H200 | ≈$3,796 (≈€3,530) | ≈$7,592 (≈€7,061) | ≈$22,776 (≈€21,182) |
| Decentralized H100 (≈$3/h) | ≈$4,380 | ≈$8,760 | ≈$26,280 |
| Lambda H100 80 GB | ≈$6,263 (≈€5,825) | ≈$12,527 (≈€11,650) | ≈$37,580 (≈€34,955) |
| AWS H200 spot | ≈$4,925 (≈€4,580) | ≈$9,850 (≈€9,161) | ≈$29,547 (≈€27,479) |
| AWS H200 on-demand | ≈$11,552 (≈€10,743) | ≈$23,104 (≈€21,487) | ≈$69,309 (≈€64,457) |
| AWS H100 (≈$10/h estimate) | ≈$14,600 (≈€13,578) | ≈$29,200 (≈€27,156) | ≈$87,600 (≈€81,468) |

Hetzner's GEX131 (RTX PRO 6000 Blackwell 96 GB) doesn't fit this hourly-prorated format since it bills a flat €889/month regardless of hours used, but at 12 months of straight rental (€10,668/year) it is worth comparing directly against buying: see below.

Cross-referenced against the hardware table above:

**At light usage (4h/day), OVH's rental cost for one year (≈€4,088) roughly equals the purchase price of the cheapest machines on this page** (Ryzen AI Halo, DGX Spark, ≈€3,700-4,700). Buying wins from year two onward at this usage level, on the cheapest provider.

**Renting the exact RTX PRO 6000 tier beats buying it, even at full-time usage for a year.** A full year of Hetzner's GEX131 (€10,668) is cheaper than the ≈€14,000 the same RTX PRO 6000 Blackwell card costs to buy outright, before even adding a host system. This overturns the general "buy wins at 24/7" pattern for this specific GPU tier: Hetzner's bare-metal dedicated-server pricing (no hypervisor overhead, no cloud margin stack) undercuts every hourly cloud provider on this page for that card by a wide margin, and undercuts the purchase price too. If your workload fits a single RTX PRO 6000's 96 GB, renting one from Hetzner is the better default over buying, unless you specifically need the hardware for more than roughly 16 months or have a data-sovereignty requirement that rules out a rented dedicated server.

**GMI Cloud is the cheapest elastic (per-second, not dedicated) H100/H200 option found on this page, undercutting even OVHcloud.** At 24/7, GMI's H100 (≈€16,294/year) costs less than OVH's H100 (≈€24,528/year) for the identical GPU class, and its H200 (≈€21,182/year) still comes in under OVH's H100.

**AWS is not economically viable for this use case at any usage level.** Even at 4h/day, AWS H100 (≈€13,578/year) costs nearly as much as an entire RTX PRO 6000 workstation bought once. At 24/7, AWS H100 (≈€81,468/year) funds close to three dual-RTX-PRO-6000 workstations (≈€30,000 each) in a single year of rental.

---

## Cloud API Throughput: Claude vs GPT-5.6

OpenAI's GPT-5.6 family (launched July 9, 2026) ships in three durable capability tiers named after celestial bodies: **Sol** (flagship), **Terra** (balanced mid-tier), **Luna** (fast, cheap). All three are available in ChatGPT, Codex, and the API, and generally available on Amazon Bedrock. Anthropic's current lineup for comparison: **Claude Opus 5** (flagship) and **Claude Sonnet 5** (mid-tier), both defaults in Claude Code.

| Model | Typical throughput | Max-effort/benchmark throughput | Time to first token | Price ($/M tokens, in/out) |
|---|---|---|---|---|
| GPT-5.6 Sol | ≈70 tok/s (OpenRouter P50) | 74.3 tok/s (ArtificialAnalysis) | ≈138.6s in max reasoning mode | $5 / $30 |
| GPT-5.6 Terra | ≈58 tok/s (OpenRouter P50) | n/a | ≈2.48s | $2 / $12 (cut 20% from launch, effective July 30, 2026) |
| GPT-5.6 Luna | ≈112 tok/s (OpenRouter P50) | 140.7 tok/s (ArtificialAnalysis) | ≈150.7s in max reasoning mode | $0.20 / $1.20 (cut 80% from launch, effective July 30, 2026) |
| Claude Sonnet 5 | ≈75.9 tok/s (ArtificialAnalysis, max effort) | n/a | not published | $2 / $10 |
| Claude Opus 5 | **≈26 tok/s average** (LLM-Benchmarks production telemetry, min 5.3, max 60.9) | n/a | ≈2.87s | $5 / $25 (fast mode research preview: $10 / $50) |

Claude Opus 5's ≈26 tok/s average comes from production telemetry across real calls, not a single benchmark preset, a materially lower number than the ≈55-80 tok/s figures reported for Opus 5 under lighter-effort presets on other trackers. Anthropic optimizes Opus 5 for reasoning depth, not raw streaming speed.

On specialized hardware (Cerebras wafer-scale systems, not a standard cloud GPU), Sol reaches roughly **750 tok/s**, about 10x the typical cloud API rate. This confirms the throughput ceiling is set by deployment infrastructure and multi-tenant scheduling, not by the model's architecture alone.

Sources: [OpenRouter Sol](https://openrouter.ai/openai/gpt-5.6-sol), [OpenRouter Terra](https://openrouter.ai/openai/gpt-5.6-terra), [OpenRouter Luna](https://openrouter.ai/openai/gpt-5.6-luna), [ArtificialAnalysis Sol](https://artificialanalysis.ai/models/gpt-5-6-sol), [ArtificialAnalysis Luna](https://artificialanalysis.ai/models/gpt-5-6-luna), [ArtificialAnalysis Sonnet 5](https://artificialanalysis.ai/models/claude-sonnet-5), [LLM-Benchmarks Anthropic](https://llm-benchmarks.com/providers/anthropic), [OpenAI price-performance update](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/), [Cerebras](https://www.cerebras.ai/blog/getting-the-most-out-of-gpt-5-6-sol-terra-and-luna).

---

## Why Cloud and Local Tokens/Sec Are Not Comparable

Comparing a cloud API's tokens/sec to a local GPU's tokens/sec is comparing a car's speed on a congested highway to the same car's speed on an empty road. Three concrete mechanisms cause the gap:

**Cloud time-to-first-token often hides invisible reasoning.** Sol and Luna's 138-150 second TTFT figures under max-reasoning presets come from internal reasoning tokens that are computed and counted but never streamed to the client. A locally run quantized model has no such phase; TTFT drops to tens of milliseconds once weights are loaded.

**Cloud infrastructure optimizes aggregate throughput across every concurrent user, not your single request.** Dynamic batching, shared queues, and paid priority tiers (Opus 5's fast mode at 2x price is exactly this, sold openly) all trade individual latency for total system utilization. A local GPU serves only you; there is no queue.

**Cloud frontier models and local models are not the same size or precision.** Sol and Opus 5 run at full precision on hundreds of billions of parameters. A local deployment typically runs 4-8 bit quantized weights on 7-70B parameters. Illustrative local ranges from the same evidence base: a 7B model on an RTX-4090-class GPU reaches roughly 100-150 tok/s, a 13B model 50-100 tok/s, a 30B model 20-50 tok/s, a 70B model on a single GPU 10-30 tok/s. These numbers land in the same range as Terra and Luna's cloud figures by coincidence of scale, not because the comparison is meaningful.

One measured data point from this page's own research process: `llmfit system` on a real MacBook Pro M5 Max reported **171 GB/s measured RAM bandwidth**, well below the ≈460-614 GB/s Apple lists as the chip's theoretical peak. Real, measured, sustained bandwidth on your actual machine is the number that predicts your actual tokens/sec, not a spec sheet peak.

---

## Decision Diagram

```mermaid
flowchart TD
    A([Need to run a large LLM]) --> B{Data must stay<br/>on your own infra?}

    B -->|Yes| C{Need over 70B<br/>or max quality?}
    B -->|No| D{Usage pattern?}

    C -->|Yes, up to 405B| E([Buy local hardware:<br/>Mac Studio M5 Ultra<br/>or dual RTX PRO 6000])
    C -->|No, 70B fits| F([Buy local hardware:<br/>RTX PRO 6000<br/>or Mac Studio M5 Max])

    D -->|Light or bursty| G([License a managed API:<br/>Claude or GPT-5.6])
    D -->|Sustained, 4-8h/day| H([Rent a cloud GPU:<br/>OVHcloud, Lambda, RunPod])
    D -->|Heavy, 24/7| I{Committed for<br/>over a year?}

    I -->|Yes| E
    I -->|No, short-term burst| H

    style A fill:#F5E6D3,color:#333
    style B fill:#E87E2F,color:#fff
    style C fill:#E87E2F,color:#fff
    style D fill:#E87E2F,color:#fff
    style I fill:#E87E2F,color:#fff
    style E fill:#7BC47F,color:#333
    style F fill:#7BC47F,color:#333
    style G fill:#6DB3F2,color:#fff
    style H fill:#6DB3F2,color:#fff

    click B href "#decision-framework" "Data sovereignty requirement"
    click C href "#what-actually-fits-named-models" "Model size vs quality"
    click D href "#one-year-cost-projections" "Usage pattern"
    click E href "#ten-comparable-hardware-configurations" "Buy: large local hardware"
    click F href "#ten-comparable-hardware-configurations" "Buy: single-GPU local hardware"
    click G href "#cloud-api-throughput-claude-vs-gpt-56" "License: managed API"
    click H href "#cloud-gpu-rental-pricing" "Rent: cloud GPU"
    click I href "#one-year-cost-projections" "Time horizon"
```

<details>
<summary>ASCII version</summary>

```
Need to run a large LLM
└─ Data must stay on your own infra?
   ├─ Yes → Need over 70B or max quality?
   │        ├─ Yes, up to 405B → BUY: Mac Studio M5 Ultra or dual RTX PRO 6000
   │        └─ No, 70B fits    → BUY: RTX PRO 6000 or Mac Studio M5 Max
   └─ No  → Usage pattern?
            ├─ Light or bursty      → LICENSE: managed API (Claude or GPT-5.6)
            ├─ Sustained, 4-8h/day  → RENT: cloud GPU (OVHcloud, Lambda, RunPod)
            └─ Heavy, 24/7          → Committed for over a year?
                                       ├─ Yes            → BUY (see above)
                                       └─ No, short burst → RENT (see above)
```

</details>

## Decision Framework

**Light or bursty usage, no data sovereignty requirement**: use a managed API (Claude, GPT-5.6) or a specialized inference provider. No hardware to maintain, pay only for what you use.

**Sustained usage, 4-8 hours a day, open-weight models up to 70B**: rent a GPU. OVHcloud's H100 at ≈€4,000-8,000/year beats every local hardware option on this page at that usage level. Avoid AWS for this shape of workload; it is priced for enterprises with different constraints, not for a single sustained GPU.

**Heavy or 24/7 usage, sustained over more than a year**: buy, on elastic hourly clouds specifically. The break-even against elastic cloud rental (even the cheapest provider tested, GMI Cloud) lands inside twelve months once usage crosses roughly 12-16 hours/day. The one exception on this page: Hetzner's dedicated-server GEX131 (RTX PRO 6000 Blackwell 96 GB) rents for less per year (€10,668) than the card costs to buy outright (≈€14,000), so for that specific GPU tier, renting stays the better default even at full-time usage, unless data sovereignty or a horizon past ≈16 months tips it toward buying.

**Need genuinely huge models (400B-class, MoE up to ≈400B) locally**: only the Mac Studio M5 Ultra 256 GB and the dual RTX PRO 6000 Blackwell workstation on this page can host a model the size of Llama 4 Maverick (401.6B total) at a usable quantization, and both do so at the edge of their memory budget. Anything past that (GLM-5.2, DeepSeek-V4-Pro, or the multi-trillion-parameter MoE releases) does not fit on anything covered here.

**Data never leaves the building is a hard requirement**: this eliminates managed APIs and cloud rental outright, regardless of the economics above. Buy local hardware sized with `llmfit` against your actual target model, not against a marketing spec sheet.

---

## Switching Providers at the CLI Level

Everything above is about which hardware or API to run inference on. A separate, complementary problem is how to point Claude Code itself at whichever backend you picked without rewriting configuration every time. [cc-copilot-bridge](https://ccbridge.bruniaux.com/) is a routing layer for the Claude Code CLI that toggles between three backends with a three-character command: `ccd` for Anthropic direct (pay-per-token), `ccc` for a GitHub Copilot subscription, and `cco` for fully offline local inference via Ollama. It doesn't change any of the hardware-fit or cost math on this page, it changes which backend Claude Code talks to once you've decided. Current release is v1.5.3, with a v2 in progress. Worth flagging: the Copilot route relies on a reverse-engineered API, which the project's own documentation notes may violate GitHub Copilot's Terms of Service.
