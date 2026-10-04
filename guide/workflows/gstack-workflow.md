---
title: "Cognitive Mode Switching"
description: "A selected path through gstack: challenge demand, review architecture and code, test behavior, ship, and reflect"
tags: [workflow, skills, planning, review, shipping, browser-automation]
---

# Cognitive mode switching

> **Source**: [gstack](https://github.com/garrytan/gstack) by Garry Tan. This page selects six workflow steps from a larger, evolving skill pack; check the repository for the current command list.

**Reading time**: ~10 min
**Prerequisites**: Claude Code skills basics, plan mode
**Related**: [Plan Pipeline](./plan-pipeline.md), [Plan-Driven Development](./plan-driven.md)

---

## TL;DR

A coding agent can blur product decisions, implementation, review and release. This selected gstack path gives each step a distinct question, with the user choosing when an additional step earns its cost.

```
/plan-ceo-review  → "Are we building the right thing?"
/plan-eng-review  → "How do we make this buildable?"
/review           → "What can still break?"
/qa               → Test the changed behavior
/ship             → Complete the Git and PR workflow
/retro            → What should change next time?
```

Planning, reviewing, and shipping require fundamentally different cognitive postures. A single assistant left in generic mode blends them badly.

---

## Six selected gates

| Command | Role | Core question | When to switch |
|---------|------|---------------|----------------|
| `/plan-ceo-review` | Founder / CEO | "Are we building the right thing?" | When product direction is uncertain |
| `/plan-eng-review` | Eng manager / tech lead | "How do we make this buildable?" | After direction is locked |
| `/review` | Paranoid staff engineer | "What can still break in prod?" | Before merging |
| `/qa` | QA engineer | "Does the changed behavior work?" | Before the release decision, against a safe target |
| `/ship` | Release engineer | "Is the branch ready to publish?" | After review and applicable QA |
| `/retro` | Engineering manager | "How well did we ship?" | Weekly or post-launch |

---

## The gap this fills: Pre-Implementation strategic gate

The hardest thing to get right with an AI coding assistant is not the implementation. It is the question that comes before: **are we building the right thing?**

Claude Code is optimized to build what you ask. If you say "add photo upload", it will add photo upload. It will not ask whether photo upload is actually the product. That is the problem `/plan-ceo-review` solves.

**Example**: You are building a Craigslist-style listing app.

- Request: "Let sellers upload a photo for their item"
- Literal implementation: file picker + image save
- What the real product is: helping sellers create listings that actually sell

If you run `/plan-ceo-review` first, the assistant is explicitly asked to challenge the literal request and find the product hiding inside it. The output becomes a different brief entirely: auto-identify the product from the photo, pull specs and pricing comps, draft title and description, suggest the hero image, detect low-quality photos before they go live.

That is a different, larger feature proposal. It needs evidence that sellers want it and that the extra work is worth doing before it replaces the narrower request.

**The modes inside `/plan-ceo-review`** include expansion, selective expansion, hold scope and reduction. They are alternative ways to challenge a proposal, not a rule to increase scope. Choose one according to the user need and the cost of work already in progress.

The user selects the mode. The assistant commits to it and does not drift.

---

## /plan-eng-review: Making the idea buildable

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

## /review: Paranoid staff engineer mode

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

## Browser QA: `/qa` and `/browse`

Current gstack separates the browser driver from the QA workflow. [`/browse`](https://github.com/garrytan/gstack/blob/main/docs/skills.md) opens pages and inspects interactions; `/qa` chooses a test depth, records evidence and can reproduce a defect before a fix. Its browser path uses Aside when available and gstack's own browser otherwise. This page does not assert a speed advantage over another browser tool.

The Lean question is whether this check catches defects before they travel downstream without growing a queue of unreviewed reports. A passing browser probe covers only the behavior exercised, not every user outcome.

---

## Full cycle demo

This is an illustrative sequence, not a measured gstack outcome.

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

# 5. QA against a safe local or staging target
You: /qa staging.myapp.com

Claude: [Exercises the listing flow, records the cases tried and any failures]
        The tested listing path passes; other user outcomes remain unmeasured.

# 6. Ship after the release decision
You: /ship

Claude: [Runs release checks, then commits, pushes and opens a PR when authorized]
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

> **Current scope**: gstack has more skills than these six. Check its current README and the side effects of a skill before adding it to a project workflow.

---

## When to use this vs. other workflows

| Situation | This workflow | Alternative |
|-----------|---------------|-------------|
| Complex feature, direction uncertain | `/plan-ceo-review` first | [Spec-First](./spec-first.md) |
| Direction clear, architecture complex | `/plan-eng-review` | [Plan Pipeline](./plan-pipeline.md) |
| Need independent validation of plan | [Plan Pipeline](./plan-pipeline.md) `/plan-validate` | — |
| One-off browser inspection | `/browse` or an available browser tool | No QA result without an explicit check |
| Changed-flow verification | `/qa` | Record tested path, failures and untested behavior |
| Want structured ADR learning loop | [Plan Pipeline](./plan-pipeline.md) | — |

This page presents a selected sequence that you can invoke deliberately; the wider gstack pack also includes automated paths. [Plan Pipeline](./plan-pipeline.md) is a separate orchestration approach. Compare either against the actual wait and rework in your delivery flow rather than assuming more stages are better.

---

## See also

- [Plan Pipeline](./plan-pipeline.md): Automated 3-command workflow with ADR learning loop
- [Plan-Driven Development](./plan-driven.md): Fundamentals of planning before coding
- [Iterative Refinement](./iterative-refinement.md): Quality improvement cycles
- [gstack on GitHub](https://github.com/garrytan/gstack): Source, install instructions, full skill prompts
