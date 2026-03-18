# Slack Template

Compact, scannable, emoji-rich. Ready to paste.

## FR Template

```
:newspaper: *{title_fr}*

{highlights_fr}

:link: {link}
```

## EN Template

```
:newspaper: *{title_en}*

{highlights_en}

:link: {link}
```

## Field Rules

### title (max 60 chars)

```
FR: "Guide v3.20.5 - Reference visuelle"
EN: "Guide v3.20.5 - Visual reference"

FR: "Recap semaine : 4 releases"
EN: "Week recap: 4 releases"
```

### highlights (3-5 lines)

Each line: Slack emoji + short description. No bold in bullet text.

```
FR:
:art: 4 nouveaux diagrammes ASCII (TDD, UVAL, securite, incidents)
:brain: 30 nouvelles questions quiz (257 total)
:shield: Guide sandbox isolation Docker
:mag: 9 patterns avances identifies via claudelog.com

EN:
:art: 4 new ASCII diagrams (TDD, UVAL, security, incidents)
:brain: 30 new quiz questions (257 total)
:shield: Docker sandbox isolation guide
:mag: 9 advanced patterns identified via claudelog.com
```

### link

GitHub repo URL.

## Slack Emoji Reference

Use standard Slack emojis that render in all workspaces:

| Emoji | Code | Use For |
|-------|------|---------|
| :newspaper: | `:newspaper:` | Title marker |
| :art: | `:art:` | Visual content, diagrams, UI |
| :brain: | `:brain:` | Quiz, learning, knowledge |
| :shield: | `:shield:` | Security content |
| :mag: | `:mag:` | Research, analysis, competitive intel |
| :wrench: | `:wrench:` | Tools, workflows, configuration |
| :books: | `:books:` | New guides, documentation |
| :chart_with_upwards_trend: | `:chart_with_upwards_trend:` | Growth metrics |
| :white_check_mark: | `:white_check_mark:` | Fixes, corrections |
| :link: | `:link:` | Link marker |
| :arrow_right: | `:arrow_right:` | Growth indicator (X -> Y) |

## Constraints

- Max 500 characters total
- Emoji budget: 4-6 (1 title + 1 per highlight + 1 link)
- No hype words
- FR: tutoiement
- EN: American English
- Single link (GitHub)
- No hashtags (not a Slack convention)
- Use Slack formatting: `*bold*`, `_italic_`, `:emoji:` codes
