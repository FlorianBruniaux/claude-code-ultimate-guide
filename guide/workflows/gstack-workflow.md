---
title: "Cognitive Mode Switching"
description: "Switch between specialist roles across your ship cycle — strategic gate, architecture, paranoid review, release, browser QA, retrospective"
tags: [workflow, skills, planning, review, shipping, browser-automation]
---

# Cognitive Mode Switching

> **Confidence**: Tier 2 — Reference implementation: [gstack](https://github.com/garrytan/gstack) by Garry Tan (Y Combinator CEO), 1,100+ stars in 24h of launch (March 2026).

**Reading time**: ~10 min
**Prerequisites**: Claude Code skills basics, plan mode
**Related**: [Plan Pipeline](./plan-pipeline.md), [Plan-Driven Development](./plan-driven.md)

---

## TL;DR

One generic assistant blurs all phases together. This pattern gives each phase a distinct cognitive mode: you summon the right brain for the job, then switch when the work changes.

```
/plan-ceo-review  → "Are we building the right thing?"
/plan-eng-review  → "How do we make this buildable?"
/review           → "What will blow up in production?"
/ship             → Execute the release, no debate
/browse           → Does it actually work in the browser?
/retro            → How well did we ship this week?
```

The insight is that planning, reviewing, and shipping require fundamentally different cognitive postures — and a single assistant left in generic mode will blend them badly.

---

## The 6 Gears

| Command | Role | Core question | When to switch |
|---------|------|---------------|----------------|
| `/plan-ceo-review` | Founder / CEO | "Are we building the right thing?" | Before writing any code |
| `/plan-eng-review` | Eng manager / tech lead | "How do we make this buildable?" | After direction is locked |
| `/review` | Paranoid staff engineer | "What can still break in prod?" | Before merging |
| `/ship` | Release engineer | "Get the plane landed" | Branch is ready, no more debate |
| `/browse` | QA engineer | "Does it actually work?" | After deploy, against staging or prod |
| `/retro` | Engineering manager | "How well did we ship?" | Weekly or post-launch |

---

## The Gap This Fills: Pre-Implementation Strategic Gate

The hardest thing to get right with an AI coding assistant is not the implementation. It is the question that comes before: **are we building the right thing?**

Claude Code is optimized to build what you ask. If you say "add photo upload", it will add photo upload. It will not ask whether photo upload is actually the product. That is the problem `/plan-ceo-review` solves.

**Example**: You are building a Craigslist-style listing app.

- Request: "Let sellers upload a photo for their item"
- Literal implementation: file picker + image save
- What the real product is: helping sellers create listings that actually sell

If you run `/plan-ceo-review` first, the assistant is explicitly asked to challenge the literal request and find the product hiding inside it. The output becomes a different brief entirely: auto-identify the product from the photo, pull specs and pricing comps, draft title and description, suggest the hero image, detect low-quality photos before they go live.

That is a different feature. A better one. And you only get it by inserting an explicit gate before implementation starts.

**The three modes inside `/plan-ceo-review`**:
- **SCOPE EXPANSION** — find the 10-star product, ask "what would make this 10x better for 2x the effort?"
- **HOLD SCOPE** — accept the direction, make the plan bulletproof
- **SCOPE REDUCTION** — strip to the minimum viable version ruthlessly

The user selects the mode. The assistant commits to it and does not drift.

---

## /plan-eng-review: Making the Idea Buildable

Once direction is locked, the cognitive mode shifts from product intuition to engineering rigor. `/plan-eng-review` is where ideation stops and architecture starts.

What it should produce:
- Architecture diagram (components, boundaries, data flow)
- State machine for the core flow
- Sync vs async boundary decisions
- Failure modes and retry logic
- Trust boundaries (where do you accept external input?)
- Test matrix

The key unlock is **forcing diagram generation**. Diagrams surface hidden assumptions that prose conceals. A sequence diagram makes you specify who calls what. A state machine makes you enumerate every failure mode. Without them, "the system will handle it" stays vague indefinitely.

---

## /review: Paranoid Staff Engineer Mode

Passing tests do not mean the branch is safe. `/review` exists for the class of bugs that survive CI and hit production anyway.

What it checks:
- N+1 queries
- Race conditions (two tabs overwriting the same state)
- Trust boundary violations (accepting client-provided metadata without validation)
- Orphaned data on failure paths
- Missing indexes
- Bad retry logic
- Tests that pass while missing the real failure mode
- Prompt injection when LLM output flows into further processing

The posture is deliberate: imagine the production incident before it happens.

---

## /browse: Non-MCP Native Browser Automation

`/browse` is the most technically distinct piece of gstack. It is not a MCP server. It is a compiled native binary (TypeScript + Bun) that runs a persistent headless Chromium daemon.

**Why the architecture matters**:

| Approach | Cold start | Subsequent calls | State persistence |
|----------|-----------|-----------------|-------------------|
| MCP browser server | New connection per session | ~500ms+ | Lost between sessions |
| `/browse` native daemon | ~3s (once) | ~100-200ms | Cookies, tabs, auth persist |

This matters for QA workflows: logging into a staging environment once and then running a full navigation sequence stays fast because the daemon never restarts. No MCP socket overhead, no session reset.

**Available operations**: navigate, read page text, take screenshots, snapshot accessibility tree with refs, click/fill by ref, run JavaScript, inspect console logs, capture network requests.

**When to prefer this over MCP browser tools**:
- Latency-sensitive QA loops (10+ page checks in sequence)
- Environments where MCP server connections are restricted
- When you need browser state (auth, cookies) to persist across multiple commands in one session

**When to stick with MCP**: single-page checks, simpler environments, or when MCP browser tooling is already in place.

---

## Full Cycle Demo

```
# 1. Strategic gate — challenge the brief
[plan mode]
You: I want to add seller photo upload to the listing app.
     Sellers should be able to upload a photo and we create the listing from it.

You: /plan-ceo-review   (select SCOPE EXPANSION mode)

Claude: "Photo upload" is not the feature. The real job is helping sellers
        create listings that actually sell. Here's the 10-star version:
        auto-identify the product, pull specs and pricing comps from the web,
        draft title and description, suggest the best hero image...

# 2. Engineering gate — lock the architecture
You: /plan-eng-review

Claude: [Architecture diagram, async job boundaries, state machine for
        upload → classify → enrich → draft pipeline, failure modes,
        trust boundaries, test matrix]

# 3. Implement the plan
[exit plan mode, write code]

# 4. Paranoid review — find what tests missed
You: /review

Claude: Race condition: two tabs can overwrite cover-photo selection.
        Trust boundary: pulling web data into draft generation creates
        a prompt injection vector.
        Missing: orphan cleanup for failed uploads.

You: [fix the issues]

# 5. Ship
You: /ship

Claude: [Syncs main, runs tests, pushes branch, opens PR — done]

# 6. Browser QA against staging
You: /browse staging.myapp.com — test the listing flow

Claude: [Navigates routes, fills upload form, verifies enrichment renders,
        checks console for errors, screenshots each step]
        All pages load correctly. Listing flow works end to end.
```

---

## Install

```bash
# Install globally (~/.claude/skills/)
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

Or paste this directly into Claude Code and it handles the rest:

> Install gstack: run `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

For team installs (committed to repo so `git clone` just works for teammates), see the [gstack README](https://github.com/garrytan/gstack).

> **Note (March 2026)**: gstack was released March 11, 2026. The patterns are solid; the implementation is new. Verify the repository is actively maintained before adopting in a production workflow.

---

## When to Use This vs. Other Workflows

| Situation | This workflow | Alternative |
|-----------|---------------|-------------|
| Complex feature, direction uncertain | `/plan-ceo-review` first | [Spec-First](./spec-first.md) |
| Direction clear, architecture complex | `/plan-eng-review` | [Plan Pipeline](./plan-pipeline.md) |
| Need independent validation of plan | [Plan Pipeline](./plan-pipeline.md) `/plan-validate` | — |
| Browser automation, single page check | Any MCP browser tool | `/browse` (overkill) |
| Browser automation, multi-step QA loop | `/browse` | MCP tools (slower) |
| Want structured ADR learning loop | [Plan Pipeline](./plan-pipeline.md) | — |

The main differentiator from [Plan Pipeline](./plan-pipeline.md): gstack is a linear gear sequence you control manually. Plan Pipeline is a more automated orchestration with ADR memory and parallel agent teams. For solo developers who want explicit control over each phase, gstack is faster to adopt.

---

## See Also

- [Plan Pipeline](./plan-pipeline.md) — Automated 3-command workflow with ADR learning loop
- [Plan-Driven Development](./plan-driven.md) — Fundamentals of planning before coding
- [Iterative Refinement](./iterative-refinement.md) — Quality improvement cycles
- [gstack on GitHub](https://github.com/garrytan/gstack) — Source, install instructions, full skill prompts
