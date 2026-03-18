---
name: talk-stage5-script
description: Stage 5 — 5-act pitch with speaker notes, slide spec, and Kimi prompt for AI slide generation. Requires validated angle + title from Stage 4.
tags: [talk, pipeline, presentation, stage-5, kimi]
allowed-tools:
  - Write
  - Read
---

# Talk Stage 5: Script

Produces the complete talk in 3 deliverables: the 5-act narrative with speaker notes, the slide specification, and the Kimi prompt ready to copy-paste.

**Prerequisite**: The user has validated angle + title at the Stage 4 CHECKPOINT. Do not run this stage without that confirmation.

## When to Use This Skill

- After Stage 4 CHECKPOINT is confirmed
- When you have a validated angle + title
- To produce the complete script and slide spec

## What This Skill Does

1. **Verifies inputs** — all upstream files + angle/title confirmation
2. **Loads the Kimi template** — from `templates/kimi-prompt-template.md`
3. **Builds the pitch** — 5-act structure with speaker notes and timing
4. **Builds the slide spec** — slide by slide with visual, text, notes
5. **Generates the Kimi prompt** — fills the template with talk content
6. **Saves 3 files**

## Input

- `talks/{YYYY}-{slug}-summary.md`
- `talks/{YYYY}-{slug}-concepts.md`
- `talks/{YYYY}-{slug}-angles.md`
- `talks/{YYYY}-{slug}-titre.md`
- `talks/{YYYY}-{slug}-timeline.md` (optional — enriches speaker notes)
- **Chosen angle + chosen title** (explicit user confirmation from Stage 4)

## Output

- `talks/{YYYY}-{slug}-pitch.md`
- `talks/{YYYY}-{slug}-slides.md`
- `talks/{YYYY}-{slug}-kimi-prompt.md`

## pitch.md Format

```markdown
# Pitch — {title}

**Event**: {event} | **Duration**: {duration} min | **Slides**: ~{n} slides
**Angle**: {selected angle}

---

## Global structure

| Act | Title | Duration | Slides |
|-----|-------|----------|--------|
| 1 | {act title} | {n} min | {n} slides |
...
| Total | | {duration} min | {n} slides |

---

## ACT 1: {TITLE} (Slides 1-{n}, ~{n} min)

{Narrative description of the act in 2-3 sentences — what happens, the emotion targeted}

---

**Slide {n} — {Slide title}**
- Visual: {visual description — simple, precise}
- Key text: {what appears on screen — max 10 words}
- Speaker notes: "{exact text to say — conversational, natural}"
- Duration: {n} min
- Pause: yes/no | {if yes: why, intended effect}

---

[Repeat for each slide in the act]

---

[Acts 2, 3, 4, 5 — same structure]

---

## Key moments (must not be rushed)

| Moment | Slide | What happens | Technique |
|--------|-------|-------------|-----------|
| {moment} | {n} | {description} | Pause / Number / Anecdote |

---

## Timing check

| Act | Planned | Buffer | Total |
|-----|---------|--------|-------|
| ACT 1 | {n} min | 30s | {n} min |
...
| **Total** | **{n} min** | **{n} min** | **{n} min** |

Q&A planned: {n} min
```

## slides.md Format

Slide-by-slide spec, ready to hand to a designer or pass to Kimi.

```markdown
# Slides Spec — {title}

**Total**: {n} slides | **Event**: {event} | **Date**: {date}

---

### SLIDE 1 — Title Slide

- **Main title**: {title}
- **Subtitle**: {subtitle or tagline}
- **Speaker**: {name}
- **Event**: {event} — {date}
- **Visual**: {background description — texture, image, mood}
- **Speaker notes**: "{text}"
- **Duration**: {n} sec

---

### SLIDE {n} — {Slide title}

- **Title**: {title}
- **Visual**: {precise visual description}
  - Type: {bar chart / timeline / diagram / big number / comparison table / screenshot placeholder}
  - Data: {specific values if chart}
- **Key text**: {what appears — max 30 words total}
- **Metrics displayed**: {numbers if metrics slide}
- **Speaker notes**: "{exact text}"
- **Duration**: {n} min
- **Act**: {act number}

---

[Repeat for each slide]

---

## Screenshots to capture

| Slide | Screenshot | Source | Status |
|-------|-----------|--------|--------|
| {n} | {description} | {tool/URL} | To capture / Available |
```

## kimi-prompt.md

Fill the template at `templates/kimi-prompt-template.md` with the talk's content.

Required sections to complete:
- Full title and subtitle
- Speaker name + event + date + duration + language + slide count
- Design requirements (adjust color palette if different from default)
- Slide Content Structure (section by section, all 5 acts)
- Screenshot placeholders (slides awaiting real captures)
- Tone reference (adapt to the talk's style)

**Verify no `{PLACEHOLDER}` remains in the final file** before handing to the user.

## Script Construction Rules

- **1 idea per slide** — never more, never less
- **Speaker notes = what you say, not what you read** — minimal slides, conversational notes
- **Numbers are heroes** — metrics appear large and alone on their slide
- **Anecdotes > explanations** — "one Tuesday morning, 3 bugs..." > "git worktrees enable parallelism"
- **Explicit transitions** — note the link between each act in the notes
- **Realistic timing** — add 10% buffer total (slides always run long)

## Anti-patterns

- Slides loaded with bullets (never more than 5 words per line)
- Speaker notes in technical jargon (read them aloud to validate)
- Vague Kimi prompt ("make it look nice") — each slide must be precise
- Omitting screenshot placeholders from the Kimi prompt
- Generating more slides than the duration allows (2-3 min/slide for REX)

## Validation Checklist

- [ ] Pitch covers 5 acts with coherent timing (±10% of target duration)
- [ ] Each slide has visual + text + speaker notes
- [ ] Key moments identified (pauses, punchlines, transitions)
- [ ] Slides spec ready to hand to a designer
- [ ] Kimi prompt complete (all template sections filled)
- [ ] Screenshots to capture listed with source
- [ ] No `{PLACEHOLDER}` remaining in kimi-prompt.md
- [ ] 3 files saved

## Using the Kimi Prompt

1. Open `{slug}-kimi-prompt.md`
2. Verify no `{PLACEHOLDER}` remains (search the file)
3. Go to [kimi.com](https://kimi.com) — free account, no API needed
4. Start a new conversation
5. Copy-paste the entire prompt
6. Kimi generates the presentation

For iterative refinement: add follow-up messages targeting specific slides. "Slide 7: make the number larger, remove the bullet list."

## Tips

- Speaker notes are the heart of this stage — they're what distinguishes a good talk from a good slide deck
- The Kimi template includes a dark design system with orange accent colors. Adapt `Color Palette` in the template if your brand has different colors
- Generate more slides than needed in the first pass, then cut — easier than writing from scratch

## Templates

- Kimi prompt: [`templates/kimi-prompt-template.md`](templates/kimi-prompt-template.md)

## Related

- [Stage 4: Position](../stage-4-position/SKILL.md) — prerequisite (CHECKPOINT required)
- [Stage 6: Revision](../stage-6-revision/SKILL.md) — reads pitch + slides
- [Orchestrator](../orchestrator/SKILL.md)
