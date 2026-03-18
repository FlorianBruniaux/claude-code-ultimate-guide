---
name: talk-stage3-concepts
description: Stage 3 — Build a numbered, scored concept catalogue. Every concept gets HIGH / MEDIUM / LOW talk-potential rating.
tags: [talk, pipeline, presentation, stage-3]
allowed-tools:
  - Write
  - Read
---

# Talk Stage 3: Concepts

Builds an exhaustive catalogue of all identifiable concepts in the source material. Each concept is numbered, categorized, and scored for its talk potential.

## When to Use This Skill

- After Stage 1 (and Stage 2 if REX mode)
- Before Stage 4 (Position needs the concept catalogue)
- When you want a structured inventory of what's available before choosing an angle

## What This Skill Does

1. **Reads the summary** — loads `{slug}-summary.md`
2. **Reads the timeline** (if available) — enriches scoring with verified dates
3. **Extracts concepts** — full scan of the source material
4. **Categorizes** — assigns each concept to a domain category
5. **Scores** — HIGH / MEDIUM / LOW for talk potential
6. **Optional repo enrichment** — if repo_path is provided, analyzes AI config concepts
7. **Writes output files**

## Input

- `talks/{YYYY}-{slug}-summary.md` (required)
- `talks/{YYYY}-{slug}-timeline.md` (optional — enriches REX concepts)
- `repo_path` (optional — for config/infrastructure concept extraction)

## Output

- `talks/{YYYY}-{slug}-concepts.md` (main catalogue)
- `talks/{YYYY}-{slug}-concepts-enriched.md` (if repo_path provided)

## Scoring Criteria

### HIGH — Strong potential
- Demonstrable live or with a screenshot
- Counter-intuitive or surprising (triggers a reaction)
- Associated with verifiable numbers
- Concrete and actionable (explainable in 30 seconds)
- Differentiator vs other talks on the same topic

### MEDIUM — Moderate potential
- Useful but expected (not surprising)
- Missing concrete proof or numbers
- Too specific to one particular context
- Needs too much explanation for a 30-min talk

### LOW — Weak potential
- Too abstract or philosophical without concrete grounding
- Already heavily covered by other speakers
- Requires specific technical background
- Hard to illustrate in a slide

**Scoring discipline**: Max 30% HIGH. If everything is HIGH, nothing is.

## Standard Categories

| Category | Description |
|----------|-------------|
| **Architecture** | Technical decisions, stack, structural patterns |
| **Tooling** | Tools, workflows, automations |
| **Philosophy** | Principles, mindsets, approaches |
| **Workflow** | Work processes, habits |
| **Knowledge Transfer** | Onboarding, team, knowledge sharing |
| **Problems** | Obstacles encountered, trade-offs |
| **Open Source** | Contributions, sharing, community |
| **AI Config** | AI configuration, profiles, knowledge feeding |
| **AI Infrastructure** | Agents, skills, hooks, commands |
| **AI Quality** | Review, tests, anti-patterns |
| **AI Security** | Security hooks, guardrails |
| **Optimization** | Performance, cost/token reduction |

Adapt or create categories if the talk has domain-specific areas.

## Output Format

### concepts.md

```markdown
# Key Concepts — {provisional title}

**Date**: {date}
**Source**: {source path} × Summary × Timeline (if available)

---

## Concept table

| # | Concept | Category | Short description | Talk potential |
|---|---------|----------|------------------|----------------|
| 1 | **{Concept name}** | {Category} | {1-2 concrete sentences} | HIGH / MEDIUM / LOW |
...

---

## Category breakdown

| Category | Count | HIGH concepts | Examples |
|----------|-------|---------------|---------|
| {category} | {n} | {n} | {examples} |
...
| **TOTAL** | **{N}** | **{N HIGH}** | |

---

## Recommendations for positioning

{3-5 sentences on concept clusters that could form the talk's acts.
Which HIGH concepts reinforce each other? What narrative arc is emerging?}
```

### concepts-enriched.md (if repo available)

Same structure but focused on what the repo analysis reveals:
- Specialized agents (count, size, roles)
- Invocable skills (catalogue, domains covered)
- System hooks (events, logic)
- Modular config (profiles, modules, pipeline)
- Project-specific code patterns

For each enriched concept, include:
- **Exact source**: file and approximate line
- **Demo-able**: yes/no (can it be shown in a slide or live?)

## Anti-patterns

- Creating overly granular concepts (one feature = one concept max)
- Scoring HIGH by default — be selective
- Omitting LOW concepts (they're useful in positioning as "angles to avoid")
- Duplicating very similar concepts (merge them instead)
- Analyzing repo code if the repo isn't accessible

## Validation Checklist

- [ ] Minimum 15 concepts identified (20+ for REX with repo)
- [ ] Each concept has a 1-2 sentence concrete description
- [ ] Scores are calibrated (not all HIGH, not all LOW)
- [ ] Categories cover the summary's themes
- [ ] Positioning recommendations present
- [ ] Files saved to correct paths

## Tips

- The concept catalogue is what Stage 4 (Position) draws from — the richer it is, the better the angle choices
- LOW concepts are valuable: they define the boundaries of what NOT to put in the talk
- If two concepts feel very similar, merge them — a smaller, sharper list beats a long diluted one

## Related

- [Stage 1: Extract](../stage-1-extract/SKILL.md) — prerequisite
- [Stage 2: Research](../stage-2-research/SKILL.md) — provides timeline (REX)
- [Stage 4: Position](../stage-4-position/SKILL.md) — reads this catalogue
- [Orchestrator](../orchestrator/SKILL.md)
