---
title: "Talk Preparation Pipeline: From Idea to Slides with AI"
description: "6-stage skill pipeline that transforms raw material into a conference talk with AI-generated slides"
tags: [workflow, skills, pipeline, presentation, ai-handoff]
---

# Talk Preparation Pipeline: From Idea to Slides with AI

> **Confidence**: Tier 2 — Validated in production on real conference talks (DevWithAI Lyon, 2026).

Transform a raw article, transcript, or notes into a complete conference talk — including a Kimi-ready prompt for AI-generated slides. Six stages, two modes, one human-in-the-loop checkpoint.

---

## Table of Contents

1. [TL;DR](#tldr)
2. [When to Use](#when-to-use)
3. [Prerequisites](#prerequisites)
4. [Pipeline Overview](#pipeline-overview)
5. [Stage-by-Stage Guide](#stage-by-stage-guide)
6. [The Kimi Handoff](#the-kimi-handoff)
7. [Human-in-the-Loop Checkpoints](#human-in-the-loop-checkpoints)
8. [Adapting the Pipeline](#adapting-the-pipeline)
9. [Real-World Example](#real-world-example)
10. [Common Pitfalls](#common-pitfalls)
11. [Design Patterns Showcased](#design-patterns-showcased)
12. [See Also](#see-also)

---

## TL;DR

```
Source Material (article / transcript / notes)
        │
        ▼
[Stage 1] EXTRACT ─────────────── {slug}-summary.md
        │
        ├──────────────────────────────────────┐
        │                                      │
        ▼ (--rex only)                         ▼
[Stage 2] RESEARCH               [Stage 3] CONCEPTS
  git-archaeology.md              concepts.md
  changelog-analysis.md           concepts-enriched.md
  timeline.md                         │
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
              [Stage 4] POSITION
                angles.md
                titre.md
                descriptions.md
                feedback-draft.md
                       │
                  [CHECKPOINT]
             User selects angle + title
                       │
                       ▼
              [Stage 5] SCRIPT
                pitch.md
                slides.md
                kimi-prompt.md ──► Copy-paste into Kimi.com
                       │
                       ▼
             [Stage 6] REVISION
              revision-sheets.md
```

Two modes: **REX** (talk with real-world proof — git history, metrics) and **Concept** (idea/thesis-based — skips Stage 2).

---

## When to Use

This pipeline fits when you have a talk to prepare and either:

- **A REX to tell**: You built something, shipped it, have real metrics — and want to turn that into a structured conference talk
- **A concept to develop**: You have an article, notes, or ideas you want to turn into a structured presentation

Suitable formats:
- Conference talks (20-45 min)
- Meetup presentations (15-30 min)
- Internal tech talks
- Workshop openings

Not suited for: slide-deck updates for recurring meetings, short lightning talks under 10 min, or situations where you have no existing material to work from.

---

## Prerequisites

**Required**:
- Claude Code with skills installed (see [examples/skills/talk-pipeline/](../../examples/skills/talk-pipeline/))
- Source material: article `.mdx`, transcript `.md`, notes, or mix
- Talk metadata: slug, event name, date, duration, audience description

**For REX mode only**:
- Access to the git repository you want to analyze
- Optional: `CHANGELOG.md` path if different from repo root

**For Kimi slide generation (Stage 5 output)**:
- Free account at [kimi.com](https://kimi.com) (no API needed — just copy-paste)

**Optional but recommended**:
- `talks/` directory in your project root for output files
- 1-2 trusted peers available for the feedback draft (Stage 4)

---

## Pipeline Overview

### Output files per mode

| File | Stage | REX | Concept |
|------|-------|-----|---------|
| `{slug}-summary.md` | 1 | ✓ | ✓ |
| `{slug}-git-archaeology.md` | 2 | ✓ | — |
| `{slug}-changelog-analysis.md` | 2 | ✓ | — |
| `{slug}-timeline.md` | 2 | ✓ | — |
| `{slug}-concepts.md` | 3 | ✓ | ✓ |
| `{slug}-concepts-enriched.md` | 3 | ✓ (if repo) | — |
| `{slug}-angles.md` | 4 | ✓ | ✓ |
| `{slug}-titre.md` | 4 | ✓ | ✓ |
| `{slug}-descriptions.md` | 4 | ✓ | ✓ |
| `{slug}-feedback-draft.md` | 4 | ✓ | ✓ |
| `{slug}-pitch.md` | 5 | ✓ | ✓ |
| `{slug}-slides.md` | 5 | ✓ | ✓ |
| `{slug}-kimi-prompt.md` | 5 | ✓ | ✓ |
| `{slug}-revision-sheets.md` | 6 | ✓ | ✓ |

REX mode: 13-14 files. Concept mode: 10 files.

### Naming convention

All outputs follow `talks/{YYYY}-{slug}-{stage-label}.md`. Example for slug `devwithai` in 2026:

```
talks/2026-devwithai-summary.md
talks/2026-devwithai-git-archaeology.md
talks/2026-devwithai-concepts.md
talks/2026-devwithai-angles.md
...
```

---

## Stage-by-Stage Guide

### Stage 1: Extract

**What it does**: Reads the source material and produces a structured summary — narrative arc, key metrics, main themes, gaps.

| | |
|--|--|
| **Input** | Source file + metadata (slug, event, date, duration, audience, mode) |
| **Output** | `{slug}-summary.md` |
| **Tools used** | Read, Write, AskUserQuestion |
| **Mode** | REX + Concept |

**Key rules**:
- Auto-detects source type (REX vs Concept) based on signals (dates, metrics, "I shipped" vs "I think")
- Extracts every measurable metric with its source — no invented numbers
- Flags gaps explicitly rather than hiding them

**Invocation**:
```
/talk-stage1-extract
```

Or via the orchestrator:
```
/talk-pipeline --stage=extract --slug=my-talk --event="Conf 2026" --date=2026-06-15 --duration=30 --audience="senior devs"
```

**Review before moving on**:
- Arc narrative is coherent (not generic: "this talk is about AI...")
- All metrics have an explicit source
- Gaps are listed (even if it's "no major gaps")
- Type detection is correct (REX / Concept / Hybrid)

---

### Stage 2: Research (REX mode only)

**What it does**: Git archaeology — extracts velocity metrics, cross-references CHANGELOG, builds a factual timeline verified by git (not estimated).

| | |
|--|--|
| **Input** | `{slug}-summary.md` + repo path |
| **Output** | `git-archaeology.md`, `changelog-analysis.md`, `timeline.md` |
| **Tools used** | Bash (read-only git commands), Read, Write |
| **Mode** | REX only — **automatically skipped in Concept mode** |

**Key rules**:
- Read-only git commands only — never modifies the repository
- Dates not found in git are marked "unverified" — never estimated
- Contradictions between sources are flagged, not silently resolved

**Git commands used** (read-only):
```bash
git log --pretty=format:"%Y-%m" | sort | uniq -c   # velocity by month
git shortlog -sn --no-merges                         # contributors
git tag --sort=version:refname                       # releases
git log --merges --oneline | wc -l                   # PRs merged
```

**Review before moving on**:
- Timeline covers the full period from summary
- No estimated dates — all verified
- Velocity peaks have contextual notes

---

### Stage 3: Concepts

**What it does**: Builds a numbered, scored catalogue of all concepts in the material. Each concept gets a talk-potential score (HIGH / MEDIUM / LOW).

| | |
|--|--|
| **Input** | `{slug}-summary.md` + `{slug}-timeline.md` (optional) |
| **Output** | `{slug}-concepts.md`, `{slug}-concepts-enriched.md` (if repo available) |
| **Tools used** | Read, Write |
| **Mode** | REX + Concept |

**Score criteria**:
- **HIGH**: Demonstrable, counter-intuitive, has verified numbers, actionable in 30 seconds
- **MEDIUM**: Useful but expected, missing proof or numbers
- **LOW**: Too abstract, over-covered, hard to illustrate in a slide

**Scoring discipline**: Maximum 30% HIGH — being selective is the point.

**Review before moving on**:
- 15+ concepts identified (20+ for REX with repo access)
- Scores are calibrated (not all HIGH, not all LOW)
- Each concept has a 1-2 sentence concrete description

---

### Stage 4: Position + CHECKPOINT

**What it does**: Generates strategic angles, titles, descriptions, and a peer-feedback draft. Then **stops and waits** for your angle + title choice.

| | |
|--|--|
| **Input** | `{slug}-summary.md` + `{slug}-concepts.md` + event constraints |
| **Output** | `angles.md`, `titre.md`, `descriptions.md`, `feedback-draft.md` |
| **Tools used** | Read, Write, AskUserQuestion |
| **Mode** | REX + Concept |

**What gets generated**:
- **3-4 angles**: each with forces, weaknesses, audience fit, verdict (scored /5)
- **Recommendation**: one clear choice with structured justification
- **3-5 titles** per angle
- **Description short** (~100 words abstract) + **description long** (~250 words CFP)
- **Feedback draft**: ready-to-send message for peer validation (3 formats: Slack DM, email, LinkedIn post)

**CHECKPOINT display** (mandatory before Stage 5):

```
---
CHECKPOINT : Choix angle + titre

J'ai généré 4 fichiers :
- talks/{YYYY}-{slug}-angles.md    → {n} angles analysés
- talks/{YYYY}-{slug}-titre.md     → {n} options de titre
- talks/{YYYY}-{slug}-descriptions.md
- talks/{YYYY}-{slug}-feedback-draft.md

Avant de lancer le script (Stage 5), j'ai besoin de ton choix :

1. Quel angle tu retiens ? (recommandé : Angle {X} — {nom})
2. Quel titre tu préfères ? (recommandé : "{titre}")

Tu peux aussi modifier, mixer, ou proposer quelque chose d'autre.
---
```

**Stage 5 cannot start without explicit user confirmation.**

**Review before confirming**:
- You've read the feedback draft and optionally sent it to a peer
- The recommended angle can sustain the full duration without repetition
- The title is concrete (no jargon, no click-bait)

---

### Stage 5: Script

**What it does**: Builds the complete talk in 5 acts with speaker notes, the slide specification, and the Kimi prompt.

| | |
|--|--|
| **Input** | summary + concepts + timeline (optional) + **validated angle + title** |
| **Output** | `{slug}-pitch.md`, `{slug}-slides.md`, `{slug}-kimi-prompt.md` |
| **Tools used** | Read, Write |
| **Mode** | REX + Concept |

**Three deliverables**:

1. **`pitch.md`**: The 5-act narrative with speaker notes, timing, key moments. What you say — not what you read from slides.

2. **`slides.md`**: Slide-by-slide spec: title, visual description, key text (≤30 words), speaker notes, duration, act number. Ready to hand to a designer or pass to Kimi.

3. **`kimi-prompt.md`**: Complete prompt for [kimi.com](https://kimi.com) — includes design system, color palette, typography specs, full slide content, and screenshot placeholders. Copy-paste ready.

**1-idea-per-slide rule**: If a slide needs an "and" to describe it, split it.

**Review before moving on**:
- Timing check: total ≤ duration + 10% buffer
- Speaker notes read naturally out loud (test this)
- Kimi prompt has no `{PLACEHOLDER}` left unfilled

---

### Stage 6: Revision

**What it does**: Produces revision sheets for during and after the talk — quick navigation by act, master concept table, Q&A cheat-sheet, glossary.

| | |
|--|--|
| **Input** | `pitch.md` + `slides.md` + `concepts.md` |
| **Output** | `{slug}-revision-sheets.md` |
| **Tools used** | Read, Write |
| **Mode** | REX + Concept |

**What's in the revision sheets**:
- **Navigation** with anchor links by act
- **Per-act breakdown**: key concepts + metrics + anecdotes + probable Q&A
- **Master table**: concept → 1-2 sentence definition → URL to share
- **Q&A cheat-sheet**: 6-10 probable questions with short answers (≤20 sec to say)
- **Metrics block**: all numbers in one place
- **External resources**: links mentioned in the talk
- **Glossary**: technical terms, max 10 words each

**Purpose**: Someone asks a question → find the section → share the URL in 5 seconds.

---

## The Kimi Handoff

Stage 5 generates `{slug}-kimi-prompt.md` — a complete prompt for [kimi.com](https://kimi.com).

**What to do with it**:
1. Open the generated file
2. Verify no `{PLACEHOLDER}` remains (search the file)
3. Go to [kimi.com](https://kimi.com) — free account, no API needed
4. Start a new conversation
5. Copy-paste the entire prompt
6. Kimi generates the presentation (PowerPoint or PDF)

**Iterating with Kimi**:
- After the first generation, review slides against your `slides.md` spec
- Add follow-up messages for individual adjustments: "Slide 7: make the number larger, remove the bullet list"
- For screenshots: replace `SCREENSHOT AREA` placeholders manually after export

**The design system** embedded in the template:
- Dark theme (#0a0a0a background)
- Orange accent (#f97316) for key numbers and CTAs
- Inter/SF Pro typography
- Max 30 words per slide, numbers as heroes
- WCAG AA contrast ratio (projector-safe)

**Why Kimi?** At the time of writing, Kimi produces higher-quality conference presentations from detailed prompts than most alternatives. The template is Kimi-tuned but the design system and slide structure work with any AI presentation tool.

---

## Human-in-the-Loop Checkpoints

The pipeline has two human checkpoints:

### Checkpoint 1: Stage 1 metadata collection

If talk metadata (slug, event, date, duration, audience, mode) isn't provided upfront, Stage 1 uses `AskUserQuestion` to collect them before proceeding. This avoids generating a summary you'd discard.

### Checkpoint 2: Stage 4 — Angle + Title selection (mandatory)

This is the pipeline's critical gate. Stage 5 cannot start without an explicit human choice.

**Why this matters**: The angle and title determine everything that follows — the 5-act structure, which concepts surface, the Kimi prompt tone. An automated choice here would produce a generic talk. This is the one decision that must be yours.

**What to do at the checkpoint**:
1. Read `angles.md` — don't skip it, the recommendation may be wrong for your context
2. Optionally send `feedback-draft.md` to a trusted peer (takes 10 minutes, saves 2 hours of rework)
3. Reply with your choice (can be the recommendation, a modification, or something entirely different)

---

## Adapting the Pipeline

### Lightning talk (10-15 min)

- Keep Stages 1, 3, 4, 5 — skip Stage 2 even in REX mode
- In Stage 3: limit to 8-10 concepts (filter ruthlessly to HIGH only)
- In Stage 4: generate 2 angles maximum
- In Stage 5: target ~8-10 slides, ~2 min/slide
- Skip Stage 6 (not needed for short format)

### 45-minute talk

- Full pipeline, all stages
- In Stage 3: target 25-35 concepts (gives you enough to fill 5 solid acts)
- In Stage 5: 20-25 slides, allow 3 min/slide average
- Stage 6 becomes critical (Q&A lasts 10-15 min)

### Workshop (90+ min)

- Run the pipeline up to Stage 4
- In Stage 5: replace slides.md with an activities spec (exercises, timing, breakout groups)
- The Kimi prompt section becomes optional (less relevant for workshop materials)

### No git repo available (REX without code)

- Use `--rex` mode if you have metrics from other sources (analytics, dashboards, incident reports)
- In Stage 2: replace git commands with manual data collection from those sources
- Be stricter about sourcing — "unverified" metrics don't survive the talk

---

## Real-World Example

**Talk**: "Dev with AI" REX — How we shipped a complex project in 7 months with AI tooling

**Mode**: REX
**Event**: DevWithAI Lyon, February 2026
**Duration**: 30 minutes
**Source material**: 12,000-word article in `.mdx`

**Files generated (16 total)**:

```
talks/2026-devwithai-summary.md              (Stage 1)
talks/2026-devwithai-git-archaeology.md      (Stage 2)
talks/2026-devwithai-changelog-analysis.md   (Stage 2)
talks/2026-devwithai-timeline.md             (Stage 2)
talks/2026-devwithai-concepts.md             (Stage 3)
talks/2026-devwithai-concepts-enriched.md    (Stage 3)
talks/2026-devwithai-angles.md               (Stage 4)
talks/2026-devwithai-titre.md                (Stage 4)
talks/2026-devwithai-descriptions.md         (Stage 4)
talks/2026-devwithai-feedback-draft.md       (Stage 4)
talks/2026-devwithai-pitch.md                (Stage 5)
talks/2026-devwithai-slides.md               (Stage 5)
talks/2026-devwithai-kimi-prompt.md          (Stage 5)
talks/2026-devwithai-revision-sheets.md      (Stage 6)
```

**Key metrics surfaced by Stage 2**:
- 1,200 commits over 7 months (verified by `git log`)
- 3 main contributors
- 97% traffic reduction after a specific migration (sourced from CHANGELOG v1.1.0)
- Velocity peak in month 4 (2x normal pace)

**Angle chosen** (from 3 generated): "The builder's journey" — REX angle showing what it's actually like to build with AI tooling over months, not a feature demo

**Kimi output**: Dark-theme deck, 20 slides, numbers-as-heroes design, generated in ~90 seconds

---

## Common Pitfalls

### Metrics without sources

Stage 1 extracts metrics but doesn't verify them. Stage 2 verifies. If you're in Concept mode, any metric you mention in the talk must be sourced explicitly in your summary — or removed. Audiences ask "where did that number come from?" and "I looked it up" is not an answer.

### Overloaded slides

The Kimi prompt enforces 30 words per slide, but the pitch.md you write in Stage 5 may drift toward bullet lists. Test the 1-idea-per-slide rule: if you need "and" to describe the slide's content, split it.

### Skipping the CHECKPOINT

Running Stage 5 without a validated angle + title produces a technically correct script for the wrong talk. Stage 4's recommendation is a good starting point, not a final answer — your audience knowledge matters.

### Sending the feedback draft too late

The feedback draft is generated in Stage 4, before the script exists. That's intentional — peer feedback at the angle/title stage is actionable. Feedback on a finished script mostly generates regret.

### Generic speaker notes

Speaker notes in `pitch.md` should read as natural speech. If you catch yourself writing "in this slide, we discuss...", rewrite it as what you'd actually say to the room. The Kimi prompt copies these notes — they need to be conversational.

---

## Design Patterns Showcased

This pipeline is interesting from a Claude Code perspective because it demonstrates several advanced patterns in one coherent system.

### Skill chaining with file-based state

Each stage writes files that the next stage reads. State persists between skill invocations through the filesystem — no in-memory coupling. You can run Stage 3 a week after Stage 2 without losing context.

```
Stage 1 → writes {slug}-summary.md
Stage 2 → reads {slug}-summary.md → writes 3 new files
Stage 3 → reads summary + timeline → writes 2 new files
...
```

### Tool permission scoping

Stage 2 is the only stage that needs Bash (for git commands). Every other stage is Read + Write only. This is intentional — the minimal footprint for each stage means less surface for mistakes.

```yaml
# Stage 2 only
allowed-tools:
  - Write
  - Read
  - Bash
```

### Human-in-the-loop gates

Stage 4 uses `AskUserQuestion` to surface the CHECKPOINT — not as a convenience, but as a structural requirement. The skill won't proceed to Stage 5 without an explicit human response. This is the pattern for "Claude proposes, human decides."

### AI-to-AI handoff

Stage 5 generates a prompt for a second AI system (Kimi). Claude doesn't generate slides directly — it generates the specification that another AI executes. This pattern lets you combine strengths: Claude for structured narrative reasoning, Kimi for visual presentation generation.

```
Claude (Stage 5) → kimi-prompt.md → Kimi.com → slides.pptx
```

### Two execution modes with conditional stage skip

The `--rex` / `--concept` flag controls which stages run. Stage 2 skips automatically in Concept mode. The orchestrator (`/talk-pipeline`) handles routing — individual stage skills are mode-agnostic.

---

## See Also

- **Skill templates**: [`examples/skills/talk-pipeline/`](../../examples/skills/talk-pipeline/)
- **PDF Generation workflow**: [`guide/workflows/pdf-generation.md`](./pdf-generation.md) — for generating handouts from the talk content
- **Spec-First workflow**: [`guide/workflows/spec-first.md`](./spec-first.md) — complementary pattern for structured work with Claude
- **Skill structure reference**: [`examples/skills/skill-creator/SKILL.md`](../../examples/skills/skill-creator/SKILL.md)

---

**Last updated**: February 2026
