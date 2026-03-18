# Twitter/X Template

Two modes: single tweet (280 chars) or thread (2-3 tweets).

## Single Tweet

Use when: 1-2 highlights, simple version update.

### FR Template

```
{hook_line_fr}

{highlight_fr}

{link}
```

### EN Template

```
{hook_line_en}

{highlight_en}

{link}
```

### Rules

- Max 280 characters total (including link)
- Max 2 emojis
- Link to GitHub repo
- FR: tutoiement
- EN: direct address

## Thread (2-3 tweets)

Use when: 3+ highlights, rich version/week.

### FR Template

```
Tweet 1/N:
{hook_line_fr}

{context_fr}

Thread [down_arrow]

---

Tweet 2/N:
{highlight_1_fr}
{highlight_2_fr}

---

Tweet 3/N (optional):
{highlight_3_fr}

{cta_fr}
{link}
```

### EN Template

```
Tweet 1/N:
{hook_line_en}

{context_en}

Thread [down_arrow]

---

Tweet 2/N:
{highlight_1_en}
{highlight_2_en}

---

Tweet 3/N (optional):
{highlight_3_en}

{cta_en}
{link}
```

## Field Rules

### hook_line (max 100 chars)

Shortest form of top highlight. Must fit in first tweet with context.

| Pattern | FR | EN |
|---------|-----|-----|
| Number-led | `30 nouvelles questions quiz Claude Code` | `30 new Claude Code quiz questions` |
| Direct | `Nouveau guide : sandbox isolation Docker` | `New guide: Docker sandbox isolation` |

### context (max 80 chars)

```
FR: "Guide v3.20.5 vient de sortir"
EN: "Guide v3.20.5 just dropped"
```

### highlights (max 120 chars each)

Transformed entries, one per line. No bullet points (use line breaks).

```
FR: "4 diagrammes ASCII pour TDD, UVAL, securite"
EN: "4 ASCII diagrams for TDD, UVAL, security"
```

### cta (max 60 chars)

```
FR: "Tout est open source"
EN: "All open source"
```

### link

GitHub repo URL. Counts toward 280 char limit (23 chars for t.co).

## Decision: Single vs Thread

| Condition | Format |
|-----------|--------|
| 1-2 highlights, all fit in 280 chars | Single tweet |
| 3+ highlights or rich content | Thread (2-3 tweets) |
| Week with multiple versions | Thread |
| Only maintenance changes | Single tweet (or skip) |

## Constraints

- Each tweet: max 280 characters
- Emoji budget: 2 total across thread
- No hype words
- FR: tutoiement
- EN: American English
- Thread max: 3 tweets (not 5+)
