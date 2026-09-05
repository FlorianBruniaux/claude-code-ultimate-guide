// Whitepaper Template for Claude Code Ultimate Guide
// Version 3.0 - Modern Design (Validated Perplexity Jan 2026)
// Inspired by Stripe, Vercel, Linear design systems

// ==========================================
// COLOR PALETTE - Bold Guy (Warm Beige + Orange Brûlé)
// ==========================================

#let primary = rgb("#1a1207")      // Dark warm brown - titles, dark text
#let secondary = rgb("#4a3f31")    // Medium warm brown - subtitles
#let accent = rgb("#d4520a")       // Orange brûlé - accents, links
#let muted = rgb("#6b6053")        // Warm muted brown - metadata, captions
#let light-bg = rgb("#f5f0eb")     // Warm beige - backgrounds
#let border-light = rgb("#d4cdc5") // Warm border - borders

// Callout colors (Material Design standard)
#let info-bg = rgb("#e0f2fe")
#let info-border = rgb("#0284c7")
#let warning-bg = rgb("#fef3c7")
#let warning-border = rgb("#d97706")
#let success-bg = rgb("#dcfce7")
#let success-border = rgb("#16a34a")
#let danger-bg = rgb("#fee2e2")
#let danger-border = rgb("#dc2626")

// ==========================================
// CALLOUT BOX FUNCTIONS
// ==========================================

#let callout(type: "info", title: none, body: none, background_color: none, icon_color: none, icon: none, body_background_color: none, ..args) = {
  let (bg, border, icon-char) = if background_color != none {
    (background_color, if icon_color != none { icon_color } else { accent }, "📌")
  } else if type == "info" {
    (info-bg, info-border, "💡")
  } else if type == "warning" {
    (warning-bg, warning-border, "⚠️")
  } else if type == "success" {
    (success-bg, success-border, "✅")
  } else if type == "danger" {
    (danger-bg, danger-border, "🚨")
  } else {
    (light-bg, accent, "📌")
  }

  block(
    fill: bg,
    stroke: (left: 4pt + border),
    inset: (left: 12pt, right: 12pt, top: 10pt, bottom: 10pt),
    radius: (right: 4pt),
    width: 100%,
    breakable: true,
    [
      #if title != none [
        #text(weight: "bold", fill: border)[#icon-char #title]
        #v(4pt)
      ]
      #if body != none { body }
    ]
  )
}

// Shorthand functions
#let info(title: none, body: none) = callout(type: "info", title: title, body: body)
#let warning(title: none, body: none) = callout(type: "warning", title: title, body: body)
#let success(title: none, body: none) = callout(type: "success", title: title, body: body)
#let danger(title: none, body: none) = callout(type: "danger", title: title, body: body)

// ==========================================
// MAIN DOCUMENT FUNCTION
// ==========================================

#let whitepaper(
  title: none,
  subtitle: none,
  author: none,
  date: none,
  abstract: none,
  version: "1.0",
  wp-version: "1.0.0",  // Ebook-specific version (independent from guide version)
  series: none,
  wp-number: none,  // NEW: Whitepaper number for geometric element
  cols: 1,
  margin: (x: 2.5cm, y: 2.5cm),
  paper: "a4",
  lang: "fr",
  region: "FR",
  font: ("Helvetica Neue", "Helvetica", "Arial"),
  fontsize: 11pt,
  sectionnumbering: "1.1",
  toc: true,
  toc_title: "Table des matières",
  toc_depth: 3,
  doc,
) = {
  // Document metadata
  set document(
    title: title,
    author: author,
  )

  set page(
    paper: paper,
    margin: (x: 0cm, y: 0cm),
    header: none,
    footer: none,
  )

  // ==========================================
  // COVER PAGE - Modern Minimalist Design
  // ==========================================

  // Clean white background with subtle accent elements

  // Top accent bar (thin)
  place(top + left, rect(
    width: 100%,
    height: 6pt,
    fill: accent,
  ))

  // Series badge (top center)
  if series != none {
    place(
      top + center,
      dy: 2cm,
      box(
        fill: light-bg,
        stroke: 1pt + border-light,
        inset: (x: 16pt, y: 8pt),
        radius: 4pt,
        text(10pt, fill: muted, weight: "medium", tracking: 0.05em)[
          #upper(series)
        ]
      )
    )
  }

  // Geometric circle with WP number (if provided) - positioned to the right
  if wp-number != none {
    place(
      right + top,
      dx: -3cm,
      dy: 4.5cm,
      circle(
        radius: 1.5cm,
        fill: accent.lighten(85%),
        stroke: 2pt + accent.lighten(50%),
        [
          #set align(center + horizon)
          #text(32pt, weight: "bold", fill: accent)[#wp-number]
        ]
      )
    )
  }

  // Title block - centered
  place(
    center + horizon,
    dy: if wp-number != none { 1.5cm } else { -1cm },
    block(width: 85%)[
      #align(center)[
        // Main title
        #text(32pt, weight: "bold", fill: primary, tracking: -0.02em)[#title]

        #v(0.6cm)

        // Separator line
        #box(width: 40%, height: 2pt, fill: accent)

        #v(0.6cm)

        // Subtitle
        #if subtitle != none [
          #text(16pt, fill: secondary)[#subtitle]
          #v(1.5cm)
        ]

        // Author
        #text(13pt, fill: muted, weight: "medium")[#author]
        #v(0.3cm)

        // Date
        #text(12pt, fill: muted)[#date]
        #v(1.2cm)

        // Version badges: ebook version (primary) + guide version (secondary)
        #box(
          fill: light-bg,
          stroke: 1pt + border-light,
          inset: (x: 14pt, y: 7pt),
          radius: 20pt,
          text(10pt, fill: muted)[v#wp-version]
        )
        #h(8pt)
        #box(
          stroke: 1pt + border-light,
          inset: (x: 10pt, y: 5pt),
          radius: 20pt,
          text(8pt, fill: muted.lighten(30%))[Guide v#version]
        )
      ]
    ]
  )

  // Claude Code Logo (bottom, above footer)
  place(
    bottom + center,
    dy: -4cm,
    box(
      clip: true,
      radius: 12pt,
      image("_extensions/whitepaper/assets/claude-code-ai-logo.jpg", width: 3.5cm)
    )
  )

  // Footer with site links
  place(
    bottom + center,
    dy: -1.5cm,
    text(9pt, fill: muted)[
      florian.bruniaux.com · cc.bruniaux.com
    ]
  )

  pagebreak()

  // ==========================================
  // MAIN DOCUMENT PAGES
  // ==========================================

  set page(
    paper: paper,
    margin: margin,
    header: context {
      if counter(page).get().first() > 1 [
        #text(9pt, fill: muted)[#title]
        #h(1fr)
        #text(9pt, weight: "semibold", fill: accent)[#counter(page).display()]
      ]
    },
    footer: [
      #text(8pt, fill: muted)[florian.bruniaux.com · cc.bruniaux.com]
      #h(1fr)
      #text(8pt, fill: muted)[v#wp-version · Guide v#version#if date != none [ · #date]]
    ],
    numbering: "1",
  )

  // Reset page counter after cover
  counter(page).update(1)

  // Text settings with improved line height
  set text(
    font: font,
    size: fontsize,
    lang: lang,
    region: region,
    fill: primary,
  )

  // Paragraph settings - 1.6 line height for readability
  set par(
    justify: true,
    leading: 0.75em,  // ~1.6 line height
  )

  // ==========================================
  // HEADING STYLES - Modern Typography
  // ==========================================

  set heading(numbering: sectionnumbering)

  // H1 - Chapter titles (22pt) - pagebreak before each chapter
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    set text(fill: primary, size: 22pt, weight: "bold", tracking: -0.02em)
    v(0.8em)
    block(it)
    v(0.8em)
  }

  // H2 - Section titles (18pt) - accent color
  show heading.where(level: 2): it => {
    set text(fill: accent, size: 18pt, weight: "bold")
    v(1.5em)
    block(it)
    v(0.75em)
  }

  // H3 - Subsection titles (14pt)
  show heading.where(level: 3): it => {
    set text(fill: secondary, size: 14pt, weight: "bold")
    v(1em)
    block(it)
    v(0.5em)
  }

  // H4 - Minor headings (12pt)
  show heading.where(level: 4): it => {
    set text(fill: secondary, size: 12pt, weight: "semibold")
    v(0.75em)
    block(it)
    v(0.25em)
  }

  // ==========================================
  // CODE BLOCKS - JetBrains Mono
  // ==========================================

  show raw.where(block: true): it => {
    set text(
      size: 9.5pt,
      font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
    )
    block(
      fill: light-bg,
      inset: 1em,
      radius: 6pt,
      stroke: (left: 3pt + accent),
      width: 100%,
      breakable: false,
      it
    )
  }

  // Inline code styling
  show raw.where(block: false): it => {
    box(
      fill: light-bg,
      inset: (x: 5pt, y: 2pt),
      radius: 3pt,
      text(
        size: 0.9em,
        font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
        it
      )
    )
  }

  // ==========================================
  // TABLE STYLING - Clean Modern
  // ==========================================

  set table(
    stroke: (x, y) => (
      top: if y == 0 { 2pt + primary } else { 0.5pt + border-light },
      bottom: if y == 0 { 1pt + primary } else { 0.5pt + border-light },
    ),
    fill: (x, y) => {
      if y == 0 { light-bg }
      else if calc.odd(y) { white }
      else { light-bg.lighten(60%) }
    },
    inset: 10pt,
  )

  // Allow tables to break across pages (prevents blank pages before large tables)
  show table: it => block(breakable: true, it)

  // Table header styling
  show table.cell.where(y: 0): set text(weight: "semibold", fill: primary)

  // ==========================================
  // LINK & TEXT STYLING
  // ==========================================

  show link: it => {
    set text(fill: accent, hyphenate: false)
    underline(offset: 2pt, stroke: 0.5pt + accent.lighten(50%), it)
  }

  show strong: set text(fill: primary, weight: "bold")
  show emph: set text(fill: secondary)

  // Horizontal rule styling (for --- separators)
  show line: it => {
    v(1em)
    align(center)[
      #box(width: 30%, height: 2pt, fill: accent.lighten(70%))
    ]
    v(1em)
  }

  // ==========================================
  // TABLE OF CONTENTS - Modern Style
  // ==========================================

  if toc {
    // TOC Title
    text(24pt, weight: "bold", fill: primary, tracking: -0.02em)[#toc_title]
    v(1.5em)

    // Standard outline
    outline(
      title: none,
      depth: toc_depth,
      indent: 1.5em,
    )

    pagebreak()
  }

  // ==========================================
  // MAIN CONTENT
  // ==========================================

  if cols == 1 {
    doc
  } else {
    columns(cols, doc)
  }
}

// ==========================================
// EXPORT CALLOUT FUNCTIONS
// ==========================================

// These can be used in documents:
// #info[Content here]
// #warning(title: "Attention")[Content here]
// #success[Best practice content]
// #danger(title: "Ne jamais faire")[Critical warning]
