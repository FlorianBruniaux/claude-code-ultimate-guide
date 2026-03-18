---
name: talk-stage6-revision
description: Stage 6 — Revision sheets for during and after the talk. Master concept table, Q&A cheat-sheet, glossary, external resources.
tags: [talk, pipeline, presentation, stage-6]
allowed-tools:
  - Write
  - Read
---

# Talk Stage 6: Revision

Produces revision sheets usable during and after the talk. Quick navigation by act, master concept table with URLs to share, Q&A cheat-sheet, and glossary.

## When to Use This Skill

- After Stage 5 (Script) — needs pitch + slides
- Before a talk where Q&A is expected
- To create a shareable resource for attendees

## What This Skill Does

1. **Reads all inputs** — pitch + slides + concepts (+ timeline if available)
2. **Extracts navigation** — table of contents with anchors per act
3. **Rebuilds by act** — key concepts + metrics + anecdotes + probable Q&A
4. **Builds master table** — all concepts + definitions + URLs
5. **Builds Q&A cheat-sheet** — 6-10 questions + short answers + links
6. **Builds glossary** — technical terms from the talk
7. **Lists external resources**
8. **Assembles and saves**

## Input

- `talks/{YYYY}-{slug}-pitch.md` (required)
- `talks/{YYYY}-{slug}-slides.md` (required)
- `talks/{YYYY}-{slug}-concepts.md` (required)
- `talks/{YYYY}-{slug}-timeline.md` (optional — for metrics accuracy)

## Output

`talks/{YYYY}-{slug}-revision-sheets.md`

## Output Format

```markdown
# Revision Sheets — {title}

**Date**: {date} · **Talk duration**: {n} min + {n} min Q&A
**Purpose**: Someone asks a question → find the section → share the URL in 5 seconds

---

## Quick navigation

| Section | Content |
|---------|---------|
| [Act 1](#act-1) | {1-line summary} |
| [Act 2](#act-2) | {1-line summary} |
| [Act 3](#act-3) | {1-line summary} |
| [Act 4](#act-4) | {1-line summary} |
| [Act 5](#act-5) | {1-line summary} |
| [Conclusion](#conclusion) | {1-line summary} |
| [Master Table](#master-table) | All concepts + URLs |
| [Q&A Cheat-sheet](#qa-cheat-sheet) | {n} anticipated questions + answers |
| [Resources](#external-resources) | Links mentioned in the talk |

---

## ACT 1: {Title} (Slides 1-{n})

**~{n} min · {period or context}**

### Key concepts

| Concept | Short definition | URL to share |
|---------|-----------------|--------------|
| **{Concept}** | {1-2 concrete sentences} | {URL or "no direct link"} |
...

### Metrics to know

```
{Metrics as code block — one per line, format: value → context}
```

### Storytelling / Anecdotes

- **{Anecdote name}**: "{Quote or summary}"

### Probable Q&A for Act {n}

| Question | Short answer |
|----------|-------------|
| "{probable question}" | {direct answer, 2-3 sentences max} |

---

[Repeat for each act]

---

## Conclusion (Slides {n}-{n})

**~{n} min**

### Summary metrics (the big numbers)

```
{All summary metrics — one per line}
```

### {N} actions for Monday (if applicable)

1. **{Action 1}**: {description + why}
2. **{Action 2}**: {description + why}
3. **{Action 3}**: {description + why}

---

## Master Table: Concept → Definition → URL to share

**The core deliverable. Every technical concept from the talk.**

| Concept | Definition (1-2 sentences) | Slide | URL to share | Notes |
|---------|--------------------------|-------|--------------|-------|
| **{Concept}** | {precise, concise definition} | {n} | {URL or "pure storytelling"} | {guide section if applicable} |
...

---

## Q&A Cheat-sheet

**The {n} most probable questions + short answers + URL to send**

---

### Q1 — "{Question}"

**Short answer**:
{Answer in 3-5 bullets}

**To go further**:
- {Link 1 with context}
- {Link 2 with context}

---

[Q2 through Q{n} — same structure]

---

## External Resources Mentioned in the Talk

### Priority URLs to share

| Resource | URL | Context |
|----------|-----|---------|
| **{Resource}** | `{url}` | {why it's important} |
...

### Studies and external sources (if applicable)

| Source | URL | How used in the talk |
|--------|-----|---------------------|
| **{Source}** | `{url}` | {how it's cited} |

---

## Quick Glossary (memory aid if you blank)

| Term | Ultra-short definition |
|------|----------------------|
| {term} | {10 words max} |
...

---

*Generated {date}. Source: slides, concepts, pitch.*
```

## Construction Rules

### Master Table
- Include ALL technical concepts mentioned in pitch and slides
- URL = link to a public resource (GitHub, docs, guide) — no dead links
- If no link: note "pure storytelling, no guide section" or "concept specific to the project"
- Definition = what you'd say if someone in the room asked "what's that?"

### Q&A Cheat-sheet
- 6 questions minimum, 10 maximum
- Select the most probable questions for the audience
- Short answer = what you'd say orally in 20 seconds max
- "To go further" = actionable links, not vague references

### Metrics
- Code block format for metrics (faster to scan)
- One metric per line: `{value}` — {context}
- Always with units (%, ms, K, days...)

### Anecdotes
- Extract verbatim from pitch where possible (for memorization)
- Quote format for phrases to say exactly

## Anti-patterns

- Incomplete Master Table (missing concepts = unusable in Q&A)
- Q&A answers that are too long (if it exceeds 5 bullets, cut)
- Invented or approximate URLs (verify every link is real)
- Copy-pasting pitch descriptions without adapting to cheat-sheet format
- Forgetting the glossary (essential when you have a memory blank)

## Validation Checklist

- [ ] Quick navigation with working anchor links
- [ ] Each act has its section (concepts + metrics + Q&A)
- [ ] Master Table covers all pitch concepts (cross-check)
- [ ] Minimum 6 questions in Q&A cheat-sheet
- [ ] External resources listed with verified URLs
- [ ] Glossary present
- [ ] File saved: `talks/{YYYY}-{slug}-revision-sheets.md`

## Tips

- The revision sheets are the most re-used output — attendees ask for links, you pull up the master table in 5 seconds
- Build the Q&A from the audience profile: what are the 3 most skeptical questions a senior dev in that room would ask?
- The glossary is your safety net: you blank on a term mid-talk, glance at the glossary, recover in 2 seconds

## Related

- [Stage 5: Script](../stage-5-script/SKILL.md) — prerequisite
- [Orchestrator](../orchestrator/SKILL.md)
