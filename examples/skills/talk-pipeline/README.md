# Talk pipeline skills

6-stage skill pipeline that transforms raw material (article, transcript, notes) into a complete conference talk with AI-generated slides.

## Install

Claude Code loads skills only from `.claude/skills/<skill-name>/SKILL.md`, one level deep, so the orchestrator and each stage are separate sibling directories. From the repository root, copy them to your project's skills folder:

```bash
mkdir -p .claude/skills
cp -r examples/skills/talk-pipeline examples/skills/talk-stage* .claude/skills/
```

Or install only the stages you need (each stage is independent). The orchestrator runs the stages by name, so it needs all of them.

## Stages

| Stage | Skill file (relative to this directory) | Mode | Description |
|-------|-----------|------|-------------|
| 1 | `../talk-stage1-extract/SKILL.md` | REX + Concept | Extract source material into structured summary |
| 2 | `../talk-stage2-research/SKILL.md` | REX only | Git archaeology + timeline |
| 3 | `../talk-stage3-concepts/SKILL.md` | REX + Concept | Scored concept catalogue |
| 4 | `../talk-stage4-position/SKILL.md` | REX + Concept | Angles, titles, descriptions + CHECKPOINT |
| 5 | `../talk-stage5-script/SKILL.md` | REX + Concept | 5-act pitch + slides spec + Kimi prompt |
| 6 | `../talk-stage6-revision/SKILL.md` | REX + Concept | Revision sheets + Q&A cheat-sheet |
| 0 | `SKILL.md` (this directory) | REX + Concept | Run the full pipeline from one invocation |

## Quick start

**Full pipeline (recommended)**:
```
/talk-pipeline
```
The orchestrator asks for metadata and runs all applicable stages.

**Single stage**:
```
/talk-stage1-extract
/talk-stage4-position
```

**With flags**:
```
/talk-pipeline --rex --slug=my-talk --event="Conf 2026" --duration=30
/talk-pipeline --concept --slug=my-idea
```

## Output convention

All files land in `talks/` at your project root:
```
talks/{YYYY}-{slug}-summary.md
talks/{YYYY}-{slug}-git-archaeology.md
talks/{YYYY}-{slug}-concepts.md
talks/{YYYY}-{slug}-angles.md
talks/{YYYY}-{slug}-pitch.md
talks/{YYYY}-{slug}-kimi-prompt.md
...
```

## Using the Kimi prompt

Stage 5 generates `{slug}-kimi-prompt.md`. To generate slides:
1. Open the file and verify no `{PLACEHOLDER}` remains
2. Go to [kimi.com](https://kimi.com) (free, no API needed)
3. Copy-paste the entire prompt
4. Kimi generates a dark-theme presentation with your slide content

## Documentation

Full workflow guide: [guide/workflows/talk-pipeline.md](../../../guide/workflows/talk-pipeline.md)
