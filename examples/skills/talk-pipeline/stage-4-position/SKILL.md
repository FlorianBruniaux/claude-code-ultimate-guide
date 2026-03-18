---
name: talk-stage4-position
description: Stage 4 — Strategic angles, titles, descriptions, peer feedback draft. Includes mandatory CHECKPOINT before script can start.
tags: [talk, pipeline, presentation, stage-4, checkpoint]
allowed-tools:
  - Write
  - Read
  - AskUserQuestion
---

# Talk Stage 4: Position + CHECKPOINT

Generates strategic angles, titles, descriptions, and a peer-feedback draft. Then **stops and waits** for your angle + title choice before Stage 5 can proceed.

## When to Use This Skill

- After Stage 3 (Concepts) — needs the concept catalogue
- When deciding how to frame the talk
- Before sending the CFP (uses the generated descriptions directly)

## What This Skill Does

1. **Reads inputs** — summary + concepts + event constraints
2. **Generates angles** — 3-4 distinct angles with force/weakness analysis
3. **Recommends** — one clear choice with structured justification
4. **Generates titles** — 3-5 options per angle
5. **Generates descriptions** — short abstract + long CFP description
6. **Generates feedback draft** — ready-to-send message (3 formats)
7. **CHECKPOINT** — displays choice request and waits for user response
8. **Saves 4 files**

## Input

- `talks/{YYYY}-{slug}-summary.md` (required)
- `talks/{YYYY}-{slug}-concepts.md` (required)
- Event constraints: duration, audience, CFP format if applicable

## Output

- `talks/{YYYY}-{slug}-angles.md`
- `talks/{YYYY}-{slug}-titre.md`
- `talks/{YYYY}-{slug}-descriptions.md`
- `talks/{YYYY}-{slug}-feedback-draft.md`

## angles.md Format

```markdown
# Talk Angles — {provisional title}

**Goal**: Choose the angle that maximizes impact for {audience}.
**Audience**: {audience description}

---

## Angle 1: {Angle name}

**Pitch**: {2-3 sentences describing the talk from this angle}

**Strengths**:
- {strength 1}
- {strength 2}

**Weaknesses**:
- {weakness 1}
- {weakness 2}

**Audience fit**: Strong / Medium / Weak — {short justification}

**Verdict**: ⭐⭐⭐⭐⭐ (out of 5)

---

[Angle 2, Angle 3, (optional Angle 4) — same structure]

---

## Recommendation: Angle {X}, enriched by the others

**Angle {X} is the right choice.** Here's why:

### 1. It's the only angle that integrates the others
[Structure showing how other angles feed into the main one]

### 2. The narrative arc is natural and compelling
[Why the story holds better with this angle]

### 3. The metrics lend credibility throughout
[Which metrics support this angle most]

### 4. The final message emerges naturally
[How the conclusion flows from this angle]

---

## Recommended structure with sub-angles

| Act | Duration | Main angle | Integrated sub-angle |
|-----|----------|-----------|---------------------|
| 1. {name} | {n} min | {main angle} | {sub-angle} |
...
```

## titre.md Format

```markdown
# Titles — Talk {slug}

**Selected angle**: Angle {X} — {name}
**Constraints**: {duration} min | {audience}

---

## Titles for the recommended angle

### Option 1 (recommended)
**{Main title}**
*Optional subtitle: {subtitle}*

Strengths: {why this title works}
Audience appeal: {who it hooks}

### Option 2
**{Title}**
Strengths: {strengths}

[Options 3-5]

---

## Titles for alternative angles (backup)

### If Angle 2 chosen
- **{title}**
- **{title}**

[If Angle 3 chosen — same]

---

## Verdict

**Recommendation**: Option 1 — "{title}"
**Why**: {short justification}
```

## descriptions.md Format

```markdown
# Descriptions — Talk {slug}

---

## Short description (abstract, ~100 words)

{Full text — direct, engaging, starts with the impact or concrete promise.
Not "In this talk, we will..."}

---

## Long description (CFP, ~250 words)

{Full text — context, what the audience will learn, who it's for.
Includes key metrics if available.
Direct and factual tone.}

---

## Speaker pitch (bio-ready, ~50 words)

{Speaker introduction in 1-2 sentences, their relationship to the topic}

---

## Tags / Keywords

{5-10 relevant tags for CFP or search}
```

## CHECKPOINT (mandatory — Step 7)

After generating and saving the 4 files, display:

```
---
CHECKPOINT: Angle + Title choice

I've generated 4 files:
- talks/{YYYY}-{slug}-angles.md    → {n} angles analyzed
- talks/{YYYY}-{slug}-titre.md     → {n} title options
- talks/{YYYY}-{slug}-descriptions.md
- talks/{YYYY}-{slug}-feedback-draft.md

Before starting the script (Stage 5), I need your choice:

1. Which angle do you choose? (recommended: Angle {X} — {name})
2. Which title do you prefer? (recommended: "{title}")

You can also modify, combine, or propose something different.
Reply to start the script.
---
```

**Do not invoke Stage 5 without explicit user confirmation.**

## Angle Generation Rules

- Minimum 3 angles, maximum 4 (beyond that it's noise)
- Each angle must be genuinely distinct (not variations of the same)
- The recommendation must be clear and argued — not "your choice"
- Always test: "can this angle sustain the full duration without repeating?"

## Anti-patterns

- Click-bait titles ("What nobody tells you about AI")
- Recommending the last angle listed by default (recency bias)
- Descriptions that read like slide summaries
- Skipping the CHECKPOINT — it's the pipeline's most important control point
- Marketing language in descriptions (revolutionary, game-changer)

## Validation Checklist

- [ ] 3-4 angles with force/weakness/audience-fit analysis
- [ ] Clear recommendation with structured justification
- [ ] 3-5 titles for the recommended angle
- [ ] Short description (~100 words) and long description (~250 words)
- [ ] Feedback draft generated from template
- [ ] CHECKPOINT displayed clearly
- [ ] 4 files saved

## Tips

- Send `feedback-draft.md` to a peer before the checkpoint — 10 minutes of external feedback can save hours of rework on the script
- The recommendation is a starting point, not an order — your audience knowledge overrides any algorithmic suggestion
- Weak titles are usually too abstract: test each title by asking "would someone in the hallway stop walking to read this?"

## Templates

- Peer feedback formats: [`templates/feedback-draft.md`](templates/feedback-draft.md)

## Related

- [Stage 3: Concepts](../stage-3-concepts/SKILL.md) — prerequisite
- [Stage 5: Script](../stage-5-script/SKILL.md) — starts after this CHECKPOINT
- [Orchestrator](../orchestrator/SKILL.md)
