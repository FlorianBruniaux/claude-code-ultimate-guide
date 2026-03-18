---
name: talk-pipeline
description: Orchestrator for the complete talk preparation pipeline (REX or Concept mode). Runs all 6 stages in sequence with human-in-the-loop checkpoints.
tags: [talk, pipeline, presentation, orchestrator]
allowed-tools:
  - Write
  - Read
  - AskUserQuestion
  - Task
---

# Talk Pipeline Orchestrator

Orchestrates the complete talk preparation pipeline — from raw material to revision sheets. Can run the full pipeline or a single isolated stage.

## Modes

- `--rex`: REX talk with git/code proof (changelog, commits, measured metrics)
- `--concept`: Conceptual talk from article, ideas, notes (skips Stage 2)

## Usage

```
/talk-pipeline                          # full pipeline, asks for context
/talk-pipeline --stage=extract          # run a single isolated stage
/talk-pipeline --rex                    # REX mode (git archaeology included)
/talk-pipeline --concept                # Concept mode (skip research)
/talk-pipeline --rex --slug=my-talk --event="Conf 2026" --date=2026-06-15 --duration=30
```

## Context Collection

Ask with AskUserQuestion if not provided:

```
- slug         : kebab-case identifier (e.g., my-talk-topic)
- event        : event name (e.g., Conf 2026, Tech Meetup)
- date         : talk date (YYYY-MM-DD)
- duration     : duration in minutes (e.g., 30)
- audience     : audience profile (e.g., senior devs, tech leads, non-tech)
- type         : --rex or --concept
- source_path  : path to source material (article .mdx, transcript .md, notes)
- repo_path    : (REX only) path to git repository for archaeology
```

## Workflow

1. **Collect context** — AskUserQuestion for required metadata
2. **Route by mode** — `--rex` vs `--concept` (skip Stage 2 if concept)
3. **Run Stage 1** — `/talk-stage1-extract` — always first
4. **Run Stages 2-4 in parallel** (after Stage 1 confirmed)
   - REX: extract → research + concepts + position (in parallel)
   - Concept: extract → concepts + position (in parallel, skip research)
5. **CHECKPOINT** — wait for angle + title choice (Stage 4 output)
6. **Run Stage 5** — `/talk-stage5-script` with validated choice
7. **Run Stage 6** — `/talk-stage6-revision`
8. **Final summary** — list all generated files with their paths

## Dependency Graph

```
         extract (Stage 1)
               |
    ┌──────────┼──────────┐
    v          v          v
research    concepts   position
(Stage 2)   (Stage 3)  (Stage 4)
[--rex only]            [CHECKPOINT]
    |          |          |
    └──────────┼──────────┘
               v
          script (Stage 5)
               |
               v
         revision (Stage 6)
```

## Stage Routing (--stage=X)

If `--stage` is provided, run only the corresponding skill:

| Stage | Skill to invoke |
|-------|----------------|
| extract | /talk-stage1-extract |
| research | /talk-stage2-research |
| concepts | /talk-stage3-concepts |
| position | /talk-stage4-position |
| script | /talk-stage5-script |
| revision | /talk-stage6-revision |

## Output Naming Convention

```
talks/{YYYY}-{slug}-summary.md           # extract
talks/{YYYY}-{slug}-git-archaeology.md   # research
talks/{YYYY}-{slug}-changelog-analysis.md
talks/{YYYY}-{slug}-timeline.md
talks/{YYYY}-{slug}-concepts.md          # concepts
talks/{YYYY}-{slug}-concepts-enriched.md
talks/{YYYY}-{slug}-angles.md            # position
talks/{YYYY}-{slug}-titre.md
talks/{YYYY}-{slug}-descriptions.md
talks/{YYYY}-{slug}-feedback-draft.md
talks/{YYYY}-{slug}-pitch.md             # script
talks/{YYYY}-{slug}-slides.md
talks/{YYYY}-{slug}-kimi-prompt.md
talks/{YYYY}-{slug}-revision-sheets.md   # revision
```

## Final Summary Format

After Stage 6 completes, display:

```
Pipeline complete. Files generated:

Stage 1 — Extract:
  ✓ talks/{YYYY}-{slug}-summary.md

Stage 2 — Research (REX only):
  ✓ talks/{YYYY}-{slug}-git-archaeology.md
  ✓ talks/{YYYY}-{slug}-changelog-analysis.md
  ✓ talks/{YYYY}-{slug}-timeline.md

Stage 3 — Concepts:
  ✓ talks/{YYYY}-{slug}-concepts.md
  ✓ talks/{YYYY}-{slug}-concepts-enriched.md (if repo available)

Stage 4 — Position:
  ✓ talks/{YYYY}-{slug}-angles.md
  ✓ talks/{YYYY}-{slug}-titre.md
  ✓ talks/{YYYY}-{slug}-descriptions.md
  ✓ talks/{YYYY}-{slug}-feedback-draft.md

Stage 5 — Script:
  ✓ talks/{YYYY}-{slug}-pitch.md
  ✓ talks/{YYYY}-{slug}-slides.md
  ✓ talks/{YYYY}-{slug}-kimi-prompt.md   ← copy-paste into kimi.com

Stage 6 — Revision:
  ✓ talks/{YYYY}-{slug}-revision-sheets.md

Next step: open kimi-prompt.md, verify no {PLACEHOLDER} remains, paste into kimi.com.
```

## Anti-patterns

- Do not run Stage 5 without an explicit angle + title choice from the user
- Do not run Stage 2 (research) in `--concept` mode
- Do not proceed to the next stage if an upstream stage failed
- Do not invent metrics or dates not present in the source material

## Validation

- [ ] All upstream files exist before launching a downstream stage
- [ ] Stage 4 CHECKPOINT respected before script
- [ ] Outputs named per convention `talks/{YYYY}-{slug}-{stage}.md`
- [ ] No empty placeholders in generated files

## Tips

- The orchestrator is the recommended entry point for first use
- For repeat users who know the pipeline, running individual stage skills is faster
- The `--stage=X` flag is useful for rerunning a single stage without redoing the full pipeline

## Related

- [Stage 1: Extract](../stage-1-extract/SKILL.md)
- [Stage 2: Research](../stage-2-research/SKILL.md)
- [Stage 3: Concepts](../stage-3-concepts/SKILL.md)
- [Stage 4: Position](../stage-4-position/SKILL.md)
- [Stage 5: Script](../stage-5-script/SKILL.md)
- [Stage 6: Revision](../stage-6-revision/SKILL.md)
- [Full workflow guide](../../../guide/workflows/talk-pipeline.md)
