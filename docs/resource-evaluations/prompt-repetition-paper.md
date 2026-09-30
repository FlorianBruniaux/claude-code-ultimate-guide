# Evaluation: Prompt repetition paper (arXiv:2512.14982)

**Date**: 2026-01-25
**Paper**: "Prompt Repetition Improves Non-Reasoning LLMs"
**Authors**: Yaniv Leviathan, Matan Kalman, Yossi Matias (Google Research)
**Published**: 17 Dec 2025
**arXiv**: https://arxiv.org/abs/2512.14982

---

## 1. Findings summary

### Core claim
Repeating the input prompt 2x improves accuracy for LLMs **without reasoning mode**, without increasing output length or latency.

### Tested Models (directly from paper)
- Gemini 2.0 Flash / Flash Lite
- GPT-4o / GPT-4o-mini
- **Claude 3 Haiku**
- **Claude 3.7 Sonnet**
- Deepseek V3

### Benchmarks
ARC (Challenge), OpenBookQA, GSM8K, MMLU-Pro, MATH, NameIndex, MiddleMatch

### Key results
| Metric | Value |
|--------|-------|
| Wins (no reasoning) | 47/70 benchmark-model combinations |
| Losses | 0 |
| With CoT/reasoning | 5 wins, 1 loss, 22 neutral |

### Claude-Specific Notes (from paper)
- Tested on Claude 3 Haiku and Claude 3.7 Sonnet
- **Latency increase** observed for Claude models on very long requests (repeat x3 or custom benchmarks)
- Likely due to prefill stage taking longer

---

## 2. Relevance to Claude Code

### Model situation (Jan 2026)

| Model | Thinking Mode | Prompt Repetition Applicable? |
|-------|---------------|-------------------------------|
| Opus 4.5 | ON by default (max budget) | NO - thinking already maximizes reasoning |
| Sonnet 4 | Not available | YES - could benefit |
| Haiku 3.5 | Not available | YES - could benefit |

### The problem

Claude Code uses:
- **Sonnet as default** (85% of usage per guide stats)
- **Haiku for simple tasks** (cost optimization)
- **Opus for complex tasks** (already has thinking mode)

The paper's technique is specifically for **non-reasoning** scenarios. This makes it potentially relevant for Sonnet/Haiku in Claude Code.

### The catch

1. **Input token cost doubles**: Repeating prompt = 2x input tokens
2. **Claude Code context is already under pressure**: Guide emphasizes context management (100K practical limit)
3. **Gain magnitude unclear**: Paper shows wins/losses but not absolute improvement %
4. **Claude-specific latency issue**: Paper notes increased latency for Claude on long prompts

---

## 3. Community reception

### Academic impact (as of 2026-01-25)
- **Citations**: 0 (paper is 5 weeks old)
- **Semantic Scholar**: Listed, no citations
- **Replications**: None found

### Community discussion
- **Hacker News**: 5+ submissions, max 3 points, 0 comments
- **Reddit r/MachineLearning**: No relevant posts
- **Reddit r/LocalLLaMA**: No relevant posts
- **Twitter/X**: No significant discussion found

### Assessment
Extremely low community engagement. No independent validation. No practical adoption reports.

---

## 4. Practical considerations for Claude Code

### Hypothetical hook implementation

```bash
# pre-prompt-hook.sh (EXPERIMENTAL)
#!/bin/bash
# Double the prompt for Sonnet/Haiku
if [[ "$CLAUDE_MODEL" != "opus"* ]]; then
  echo "${1}

---
(Repeated for accuracy)
${1}"
else
  echo "$1"
fi
```

### Problems with this approach

1. **No API access to modify prompts in Claude Code** - hooks can't intercept user input
2. **Would need SDK-level changes** - not a user-configurable feature
3. **Cost doubling** - doubles input tokens, may offset any accuracy gains
4. **Context bloat** - directly contradicts the guide's context hygiene principles

---

## 5. Evaluation matrix

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Validity** | 3/5 | Google Research paper, but no replications yet |
| **Applicability to Claude Code** | 2/5 | Relevant only to Sonnet/Haiku, not implementable by users |
| **Community Adoption** | 1/5 | Zero adoption, zero discussion |
| **Practical Implementation** | 1/5 | Can't intercept prompts in Claude Code |
| **Cost/Benefit** | 2/5 | 2x input tokens for uncertain gain |
| **Documentation Value** | 2/5 | Too niche, too experimental |

---

## 6. Recommendation

### Score: 2/5 - DO NOT INTEGRATE

### Rationale

1. **Wrong target**: The technique targets non-reasoning LLMs, but Claude Code's complex tasks already use Opus (with thinking). Simple tasks on Sonnet/Haiku don't need accuracy optimization - they need speed.

2. **Not user-implementable**: Users can't intercept their own prompts in Claude Code. This would require SDK changes, not documentation.

3. **Zero validation**: No replications, no community adoption, no real-world usage reports after 5 weeks.

4. **Cost-prohibitive**: Doubling input tokens contradicts Claude Code's emphasis on context efficiency and cost management.

5. **Niche application**: Even if valid, it only helps on specific benchmark-style tasks (multiple choice, math) - not the open-ended coding tasks Claude Code handles.

### What could change this

- Independent replications with Claude Sonnet 4
- Real-world adoption reports from Claude Code users
- Anthropic acknowledgment or integration
- Evidence that accuracy gains outweigh 2x input cost

### Alternative recommendation

If users want better accuracy on Sonnet:
- Use **OpusPlan** (Opus for planning, Sonnet for execution) - already documented
- Switch to Opus for critical decisions - already documented
- Use structured prompting (XML tags) - already documented

These are proven techniques in the guide that don't double costs.

---

## 7. Files to NOT update

- `guide/ultimate-guide.md` - No integration
- `examples/hooks/` - No experimental hook
- `machine-readable/reference.yaml` - No reference

---

## 8. Archive decision

**Action**: Keep this evaluation in `claudedocs/resource-evaluations/` for future reference.

If the paper gains traction (citations, replications, Anthropic mention), re-evaluate in Q2 2026.
