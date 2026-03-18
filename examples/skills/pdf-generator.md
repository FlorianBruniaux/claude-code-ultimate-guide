---
name: pdf-generator
description: Generate professional PDFs using Quarto/Typst stack with modern design template
version: 1.0.0
---

# PDF Generator Skill

Generate professional PDFs with modern typography using Quarto + Typst.

## Skill Purpose

This skill assists with:
- Setting up Quarto/Typst projects
- Creating document templates
- Generating PDFs from Markdown
- Troubleshooting rendering issues
- Customizing design systems

## Stack

| Tool | Version | Role |
|------|---------|------|
| **Quarto** | ≥1.4.0 | Document rendering engine |
| **Typst** | 0.13.0 | Modern typography (integrated) |
| **Pandoc** | 3.x | Markdown conversion (integrated) |

### Pipeline de génération

```
  SOURCE              OUTIL           TEMPLATE              OUTPUT
  ──────              ─────           ────────              ──────

  .qmd  ──────────► Quarto ────► --to whitepaper-typst ──► Typst 0.13 ──► .pdf ✅
  (Markdown           │           (_extensions/               (~270K–1.7M,
  + YAML)             │            typst-template.typ)         stylé)
                      │
                      └──────► --to epub ──► Pandoc ──────────────────► .epub
                                             + epub-styles.css

  ⚠️  --to pdf (sans template) → PDF petit, non stylé → Toujours préférer --to whitepaper-typst
```

### Formats disponibles

```
  ┌──────────────────────┬────────────────────────┬──────────────────┐
  │ Format               │ Commande               │ Sortie           │
  ├──────────────────────┼────────────────────────┼──────────────────┤
  │ PDF stylé ✅         │ --to whitepaper-typst  │ ~270K–1.7M       │
  │ PDF standard ❌      │ --to pdf               │ ~80-190K, brut   │
  │ EPUB                 │ --to epub              │ epub-output/     │
  └──────────────────────┴────────────────────────┴──────────────────┘
```

## Quick Start

### Installation

```bash
# macOS
brew install quarto

# Linux
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb

# Windows
winget install Posit.Quarto
```

### Generate PDF

```bash
# Single file
quarto render document.qmd

# All files
quarto render *.qmd

# Preview with hot-reload
quarto preview document.qmd
```

## YAML Frontmatter Template

```yaml
---
title: "Document Title"
subtitle: "Optional subtitle"
author: "Author Name"
date: 2026-01-17
date-format: "MMMM YYYY"
format:
  typst:
    toc: true
    toc-depth: 2
    section-numbering: "1.1"
lang: en
---
```

### Available Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | string | Main title (cover page) |
| `subtitle` | string | Optional subtitle |
| `author` | string | Author(s) |
| `date` | date | ISO format (YYYY-MM-DD) |
| `date-format` | string | Display format (`MMMM YYYY`) |
| `toc` | boolean | Show table of contents |
| `toc-depth` | number | TOC depth (1-3) |
| `section-numbering` | string | Format (`1.1`, `1.a`) |
| `lang` | string | Language (`fr`, `en`) |

## Project Structure

```
project/
├── _extensions/
│   └── custom-template/
│       ├── _extension.yml      # Extension metadata
│       ├── typst-template.typ  # Main template
│       └── typst-show.typ      # Quarto → Typst bridge
├── document.qmd                # Source file
└── document.pdf                # Generated output
```

## Markdown Syntax

### Page Breaks

```markdown
{{< pagebreak >}}
```

### Code Blocks

Standard fenced blocks with syntax highlighting:

````markdown
```bash
npm install
```
````

### Tables

```markdown
| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
```

### Images

```markdown
![Caption](path/to/image.png){width=50%}
```

## Custom Template

### Extension Configuration

Create `_extensions/mytemplate/_extension.yml`:

```yaml
title: My Template
author: Your Name
version: 1.0.0
contributes:
  formats:
    typst:
      template: typst-template.typ
      template-partials:
        - typst-show.typ
```

### Design System (Typst)

```typst
// Colors (Slate + Indigo palette)
#let primary = rgb("#0f172a")      // Slate 900 - titles
#let secondary = rgb("#334155")    // Slate 700 - subtitles
#let accent = rgb("#6366f1")       // Indigo 500 - accents
#let muted = rgb("#64748b")        // Slate 500 - metadata
#let light-bg = rgb("#f8fafc")     // Slate 50 - code bg
#let border-light = rgb("#e2e8f0") // Slate 200 - borders
```

### Typography

```typst
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,
  justify: true,
)

// Code blocks
#show raw.where(block: true): it => {
  block(
    fill: light-bg,
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### Callout Boxes

```typst
#let info(title: "Note", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let warning(title: "Warning", body) = {
  block(
    fill: rgb("#FEF3C7"),
    stroke: (left: 3pt + rgb("#D97706")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let success(title: "Success", body) = {
  block(
    fill: rgb("#DCFCE7"),
    stroke: (left: 3pt + rgb("#16A34A")),
    inset: 12pt,
    [*#title*: #body]
  )
}

#let danger(title: "Danger", body) = {
  block(
    fill: rgb("#FEE2E2"),
    stroke: (left: 3pt + rgb("#DC2626")),
    inset: 12pt,
    [*#title*: #body]
  )
}
```

## Troubleshooting

### Quick Validation

```bash
# Check Quarto version
quarto --version  # >= 1.4.0

# Verify extension exists
ls _extensions/*/

# Validate code block pairs (must be even)
grep -c '^```' document.qmd

# Check encoding
file -i document.qmd  # Must show utf-8
```

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Nested code blocks break | Inner ` ``` ` closes outer | Use 4+ backticks for outer |
| Tables render as code | Unmatched ` ``` ` above | Check delimiter count |
| Extension not found | Wrong directory | Verify `_extensions/` path |
| Font warnings | Fonts not installed | Normal; uses fallbacks |
| Characters broken | Wrong encoding | Convert to UTF-8 |

### Nested Code Blocks

Use more backticks for outer block:

`````markdown
````markdown
# This is the outer block

```bash
echo "This is nested"
```

Outer continues...
````
`````

### Validation Script

```bash
#!/bin/bash
for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f has odd count ($count)"
  fi
done
```

### Full Validation Pipeline

```bash
#!/bin/bash
# validate-qmd.sh

echo "=== Validating QMD files ==="
errors=0

for f in *.qmd; do
  # Check code block pairs
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f - odd code block count ($count)"
    ((errors++))
  fi

  # Check UTF-8
  encoding=$(file -i "$f" | grep -o 'charset=[^;]*')
  if [[ "$encoding" != *"utf-8"* ]]; then
    echo "WARNING: $f - encoding is $encoding"
  fi
done

echo "=== Validation complete: $errors errors ==="
exit $errors
```

## Example Use Cases

### Technical Documentation

```yaml
---
title: "API Reference"
subtitle: "v2.0"
author: "Engineering Team"
date: 2026-01-17
format:
  typst:
    toc: true
    toc-depth: 3
---

# Authentication

All requests require an API key...
```

### Whitepaper Series

```yaml
---
title: "Security Best Practices"
series: "Engineering Whitepapers"
wp-number: "03"
author: "Security Team"
date: 2026-01-17
format:
  whitepaper-typst:
    toc: true
---
```

### Internal Report

```yaml
---
title: "Q1 Performance Report"
author: "Analytics Team"
date: 2026-01-17
date-format: "Q1 YYYY"
format:
  typst:
    toc: false
---
```

## Resources

- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Typst Documentation](https://typst.app/docs/)
- [Quarto + Typst Guide](https://quarto.org/docs/output-formats/typst.html)
- [Workflow Guide](../../guide/workflows/pdf-generation.md)