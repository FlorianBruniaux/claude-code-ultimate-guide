# LinkedIn Template

Target: ~1300 characters. Structure: hook + context + bullets + CTA + hashtags.

## FR Template

```
{hook_line_fr}

{context_line_fr}

{bullet_1_fr}
{bullet_2_fr}
{bullet_3_fr}

{cta_fr}

#ClaudeCode #CodingWithAI #DeveloperTools
```

## EN Template

```
{hook_line_en}

{context_line_en}

{bullet_1_en}
{bullet_2_en}
{bullet_3_en}

{cta_en}

#ClaudeCode #CodingWithAI #DeveloperTools
```

## Field Rules

### hook_line (1 line, max 150 chars)

The highest-scored highlight, transformed to user value. May include 0-1 emoji.

| Pattern | FR Example | EN Example |
|---------|------------|------------|
| Number-led | `30 nouvelles questions quiz pour tester vos connaissances Claude Code` | `30 new quiz questions to test your Claude Code knowledge` |
| Question | `Vous apprenez mieux en visuel ? 4 nouveaux diagrammes ASCII` | `Visual learner? 4 new ASCII diagrams just added` |
| Source-led | `Pat Cullen partage son workflow de code review multi-agent` | `Pat Cullen shares his multi-agent code review workflow` |

### context_line (1-2 lines, max 200 chars)

Version reference + what changed at a high level.

```
FR: "Guide v3.20.5 - mise a jour de la reference visuelle."
EN: "Guide v3.20.5 - visual reference update."
```

For week mode:
```
FR: "N releases cette semaine dans le Claude Code Ultimate Guide."
EN: "N releases this week in the Claude Code Ultimate Guide."
```

### bullets (3 items, each max 200 chars)

Top 3 highlights by score. Each starts with a relevant emoji (max 1 per bullet).

```
FR:
- [emoji] [Transformed highlight in vous-form]
- [emoji] [Transformed highlight in vous-form]
- [emoji] [Transformed highlight in vous-form]

EN:
- [emoji] [Transformed highlight, direct "you" address]
- [emoji] [Transformed highlight, direct "you" address]
- [emoji] [Transformed highlight, direct "you" address]
```

### cta (1 line, max 150 chars)

Soft value statement or genuine question. Links to landing site.

```
FR: "Guide complet disponible en open source : {landing_url}"
EN: "Full guide available open source: {landing_url}"
```

### hashtags (1 line, exactly 3)

Fixed: `#ClaudeCode #CodingWithAI #DeveloperTools`

Add 1 topic-specific tag if clearly relevant: `#CodeReview`, `#Security`, `#TDD`

## Constraints

- Total post: 1100-1500 characters
- Emoji budget: 3-4 total (0-1 hook, 1 per bullet, 0-1 CTA)
- No hype words (see tone-guidelines.md)
- FR: vouvoiement
- EN: American English
