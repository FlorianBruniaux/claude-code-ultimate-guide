---
title: "Anthropic weekly watch (March 16-23, 2026)"
type: "weekly-watch"
date: "2026-03-23"
score: 3
action: "partial-integration"
sources:
  - "Perplexity research synthesis (secondary source — no direct URL)"
  - "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
  - "https://platform.claude.com/docs/en/release-notes/overview"
  - "https://www.anthropic.com/81k-interviews"
---

# Anthropic weekly watch (March 16-23, 2026)

## Summary

Perplexity synthesis covering five event clusters in the March 16-23 window: Claude Code 2.1.81, Python SDK v0.85.0/v0.86.0, two Platform API release notes entries (thinking.display + model capabilities fields), and the "What 81,000 people want from AI" research blog.

## Score: 3/5

**Justification**: Secondary source (Perplexity synthesis, not primary docs). CC 2.1.81 is already tracked in our releases YAML/MD. The real value is two undocumented API platform features (`thinking.display: "omitted"` + model capabilities fields) that belong in the extended thinking section. Python SDK changes are out of scope for a Claude Code CLI guide. The 81k study is too far from the guide's technical audience.

## Gap analysis

| Item | Status in guide | Priority |
|------|----------------|----------|
| CC 2.1.81 (`--bare`, `--channels`) | ✅ Already in claude-code-releases.md | — |
| `--bare` scripted mode tradeoffs (vs standard `-p`, CI/CD implications) | ⚠️ Noted in releases, not in scripted usage / CI section | **P1** |
| `thinking.display: "omitted"` | ❌ Missing from extended thinking section | **P1** |
| Model capabilities API fields (`capabilities` object, `max_input_tokens`) | ❌ Missing entirely | P2 |
| Python SDK v0.85.0/v0.86.0 (413/529 handling, filesystem memory tools) | Out of scope (CC CLI guide) | Skip |
| "What 81,000 people want from AI" | Out of scope (adoption context, not technical) | Skip |

## Integration recommendations

### P1 — `thinking.display: "omitted"` (platform API, March 16)

**Where**: `guide/ultimate-guide.md` — Extended Thinking section (search for "extended_thinking" or "thinking budget")

**What to add**: Small subsection or note explaining:
- `thinking.display: "omitted"` hides the thinking text in the response while preserving the `signature` field for multi-turn continuity
- Use case: faster streaming, cleaner UX when thinking content isn't needed by the end user
- Billing unchanged: charged at full thinking token cost regardless of display setting
- Tradeoff: internal auditing or labeling workflows that rely on thinking text must use a different display mode

### P2 — Model capabilities API fields (Platform API, March 18)

**Where**: `guide/ultimate-guide.md` — API Integration section or a new "Model Discovery" note

**What to add**: `GET /v1/models` and `GET /v1/models/{model_id}` now return `max_input_tokens`, `max_tokens`, and a `capabilities` object. This enables dynamic model selection in orchestrators instead of hardcoded capability maps.

### P1 — `--bare` flag scripted mode tradeoffs (missed in initial pass)

**Where**: `guide/ultimate-guide.md` — scripted / CI/CD usage section (search for `-p` flag, headless, pipeline)

**What to add**: `--bare` vs standard `-p` tradeoff table. `--bare` skips hooks, LSP, plugin sync, and skill directory walks; requires `ANTHROPIC_API_KEY` or `apiKeyHelper` (no OAuth). Fast and minimal for CI scripts, but loses all observability that hooks provide. Team environments needing audit trails should use standard `-p` instead.

## Fact-check

| Claim | Status | Source |
|-------|--------|--------|
| CC 2.1.81 adds `--bare` flag | ✅ Verified | claude-code-releases.md line 30 |
| CC 2.1.81 adds `--channels` relay | ✅ Verified | claude-code-releases.md line 24 |
| `thinking.display: "omitted"` preserves signature | ⚠️ Unverified | Platform release notes (secondary source); needs verification against official docs |
| Billing unchanged for omitted thinking | ⚠️ Unverified | Same — plausible but not confirmed in guide or official docs directly |
| Model capabilities fields added March 18 | ⚠️ Unverified | Platform release notes (secondary source) |
| 80,508 participants from 159 countries | ⚠️ Unverified | Blog Anthropic (anthropic.com/81k-interviews — not fetched) |
| Python SDK v0.85.0 date: March 16 | ⚠️ Unverified | NewReleases.io proxy, not GitHub directly |

**Note on fact-check scope**: The synthesis is a Perplexity digest of release notes and blog posts. The CC 2.1.81 claims are verifiable against our tracked YAML. The API platform features need cross-checking against `https://platform.claude.com/docs/en/release-notes/overview` before integration into the guide.

## Challenge (technical-writer)

**Score maintained: 3/5** (two API gaps + one missed CLI gap don't clear the 4/5 threshold of "major integrable improvement")

Key corrections from challenge:

- **`thinking.display: "omitted"` is more significant than flagged.** Guide covers extended thinking from CLI perspective only (lines 13539-13632). Multi-turn API patterns with chain continuity are entirely absent. Relevant to orchestrator builders. Shifts priority from "gap" to "absent concept."
- **Model capabilities API is underweighted.** `GET /v1/models` with `capabilities` object enables runtime-dynamic model selection in multi-agent routing — a pattern the guide documents as manual-only today. Not a metadata footnote; it is a pattern shift.
- **`--bare` flag scripting implications missed in initial pass.** Releases tracking says "covered" but guide does not document `--bare` vs standard `-p` tradeoffs for CI/CD. Added as P1.
- **Python SDK: skip, not P3.** Guide has always scoped away from the Python SDK. No hedge needed.
- **81k study: reject (score 1), not "P4 or skip."** Study covers Claude.ai consumer users wanting from AI generally. Off-topic for a Claude Code CLI guide.

**Risks of non-integration**: Orchestrator builders pay unnecessary token costs or break chain continuity from not knowing `thinking.display: "omitted"`. CI pipeline authors get no guidance on when `--bare` is appropriate vs risky.

## Decision

- **Score final**: 3/5
- **Action**: Partial integration (3 gaps: `thinking.display` P1 + model capabilities P2 + `--bare` P1)
- **Confidence**: Medium (secondary source; CC releases verified, API platform claims need verification)
- **Next step**: Fetch official platform release notes to confirm `thinking.display` and model capabilities fields before editing the guide
