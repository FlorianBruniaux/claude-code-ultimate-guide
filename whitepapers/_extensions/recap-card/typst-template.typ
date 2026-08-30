// Recap Card Template - Claude Code Ultimate Guide
// Thematic 1-page memo cards, print-optimized
// Bold Guy palette (Warm Beige + Orange Brûlé)

// ==========================================
// COLOR PALETTE
// ==========================================

#let bg-primary = white
#let bg-card = rgb("#fef7f0")
#let bg-code = rgb("#f0e8df")
#let text-primary = rgb("#1a1207")
#let text-secondary = rgb("#4a3f31")
#let text-muted = rgb("#6b6053")
#let border-color = rgb("#d4cdc5")
#let accent = rgb("#d4520a")
#let success = rgb("#15803d")
#let danger = rgb("#b91c1c")
#let warning = rgb("#b45309")

// ==========================================
// BADGE COMPONENT
// ==========================================

#let difficulty-badge(level) = {
  let (bg, fg, label) = if level == "beginner" {
    (success.lighten(80%), success, "Beginner")
  } else if level == "intermediate" {
    (warning.lighten(80%), warning, "Intermediate")
  } else {
    (danger.lighten(80%), danger, "Advanced")
  }
  box(
    fill: bg,
    stroke: 0.5pt + fg,
    inset: (x: 6pt, y: 3pt),
    radius: 10pt,
    text(7pt, weight: "bold", fill: fg)[#label]
  )
}

#let category-badge(cat) = {
  box(
    fill: accent.lighten(85%),
    stroke: 0.5pt + accent,
    inset: (x: 6pt, y: 3pt),
    radius: 10pt,
    text(7pt, weight: "bold", fill: accent)[#cat]
  )
}

// ==========================================
// CARD COMPONENT
// ==========================================

#let rc-card(title: none, accent-border: false, body) = {
  let stroke-style = if accent-border {
    (left: 3pt + accent, rest: 0.5pt + border-color)
  } else {
    1pt + border-color
  }
  block(
    fill: bg-card,
    stroke: stroke-style,
    radius: 6pt,
    inset: 10pt,
    width: 100%,
    breakable: false,
    [
      #if title != none [
        #text(9pt, weight: "bold", fill: text-primary)[#title]
        #v(6pt)
      ]
      #body
    ]
  )
  v(8pt)
}

// ==========================================
// DO/DON'T COMPONENT
// ==========================================

#let rc-dodont(dont-items, do-items) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 10pt,

    block(
      fill: danger.lighten(88%),
      stroke: (left: 3pt + danger, rest: 0.5pt + danger.lighten(50%)),
      radius: 4pt,
      inset: 10pt,
      width: 100%,
      breakable: false,
      [
        #text(9pt, weight: "bold", fill: danger)[❌ Don't]
        #v(6pt)
        #for item in dont-items [
          #text(8pt, fill: text-primary)[• #item]
          #parbreak()
        ]
      ]
    ),

    block(
      fill: success.lighten(88%),
      stroke: (left: 3pt + success, rest: 0.5pt + success.lighten(50%)),
      radius: 4pt,
      inset: 10pt,
      width: 100%,
      breakable: false,
      [
        #text(9pt, weight: "bold", fill: success)[✅ Do]
        #v(6pt)
        #for item in do-items [
          #text(8pt, fill: text-primary)[• #item]
          #parbreak()
        ]
      ]
    ),
  )
}

// ==========================================
// QUICK REFERENCE TABLE COMPONENT
// ==========================================

#let rc-quickref(items) = {
  // items: array of (command, description) pairs
  block(
    fill: bg-card,
    stroke: 1pt + border-color,
    radius: 6pt,
    inset: 0pt,
    width: 100%,
    clip: true,
    [
      #block(
        fill: accent.lighten(88%),
        width: 100%,
        inset: (x: 10pt, y: 6pt),
        [#text(8pt, weight: "bold", fill: accent)[Quick Reference]]
      )
      #block(
        inset: (x: 10pt, y: 6pt),
        width: 100%,
        [
          #for (cmd, desc) in items [
            #grid(
              columns: (auto, 1fr),
              gutter: 8pt,
              box(
                fill: bg-code,
                inset: (x: 5pt, y: 2pt),
                radius: 3pt,
                text(
                  7.5pt,
                  font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
                  fill: text-primary
                )[#cmd]
              ),
              align(horizon)[
                #text(7.5pt, fill: text-secondary)[#desc]
              ]
            )
            #v(4pt)
          ]
        ]
      )
    ]
  )
}

// ==========================================
// SECTION LABEL
// ==========================================

#let rc-label(text-content) = {
  text(7.5pt, weight: "bold", fill: accent, tracking: 0.08em)[#upper(text-content)]
  v(4pt)
}

// ==========================================
// MAIN RECAP CARD FUNCTION
// ==========================================

#let recap-card(
  title: none,
  subtitle: none,
  card-number: none,
  category: none,
  difficulty: "beginner",
  author: "Florian BRUNIAUX",
  version: "1.0",
  date: none,
  lang: "fr",
  layout: "two-col",
  doc,
) = {
  // Document metadata
  set document(
    title: title,
    author: author,
  )

  set page(
    paper: "a4",
    margin: (x: 1.2cm, y: 1.2cm),
    header: none,
    footer: [
      #line(length: 100%, stroke: 0.5pt + border-color)
      #v(4pt)
      #grid(
        columns: (auto, 1fr, auto),
        align: (left, center, right),
        gutter: 0pt,
        text(6.5pt, fill: text-muted)[cc.bruniaux.com],
        text(6.5pt, fill: text-muted)[Claude Code Ultimate Guide],
        text(6.5pt, fill: text-muted)[v#version#if date != none [ · #date]]
      )
    ],
    numbering: none,
  )

  set text(
    font: ("Helvetica Neue", "Helvetica", "Arial"),
    size: 9pt,
    lang: lang,
    fill: text-primary,
  )

  set par(
    justify: false,
    leading: 0.55em,
    spacing: 0.7em,
  )

  // ==========================================
  // HEADER
  // ==========================================

  grid(
    columns: (1fr, auto),
    align: (top + left, top + right),
    gutter: 12pt,

    // Left: title block
    [
      #if card-number != none [
        #text(8pt, fill: text-muted)[#card-number]
        #h(6pt)
      ]
      #text(18pt, weight: "bold", fill: text-primary, tracking: -0.01em)[#title]
      #if subtitle != none [
        #v(3pt)
        #text(10pt, fill: text-secondary)[#subtitle]
      ]
    ],

    // Right: badges
    [
      #v(4pt)
      #if category != none { category-badge(category) }
      #h(4pt)
      #difficulty-badge(difficulty)
    ],
  )

  v(8pt)
  line(length: 100%, stroke: 2pt + accent)
  v(10pt)

  // ==========================================
  // HEADING STYLES
  // ==========================================

  show heading.where(level: 1): it => {
    v(8pt, weak: true)
    text(11pt, weight: "bold", fill: text-primary)[#it.body]
    v(5pt, weak: true)
  }

  show heading.where(level: 2): it => {
    v(6pt, weak: true)
    text(9pt, weight: "bold", fill: accent)[#it.body]
    v(4pt, weak: true)
  }

  show heading.where(level: 3): it => {
    v(5pt, weak: true)
    text(8.5pt, weight: "bold", fill: text-secondary)[#it.body]
    v(3pt, weak: true)
  }

  // ==========================================
  // CODE BLOCKS
  // ==========================================

  show raw.where(block: true): it => {
    set text(
      size: 7.5pt,
      font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
    )
    block(
      fill: bg-code,
      inset: 8pt,
      radius: 4pt,
      stroke: (left: 3pt + accent),
      width: 100%,
      breakable: false,
      it
    )
    v(5pt, weak: true)
  }

  show raw.where(block: false): it => {
    box(
      fill: bg-code,
      inset: (x: 4pt, y: 2pt),
      radius: 3pt,
      text(
        size: 0.88em,
        font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
        it
      )
    )
  }

  // ==========================================
  // TABLE STYLING
  // ==========================================

  set table(
    stroke: (x, y) => (
      top: if y == 0 { 1.5pt + accent } else { 0.5pt + border-color },
      bottom: if y == 0 { 1pt + accent } else { 0.5pt + border-color },
    ),
    fill: (x, y) => {
      if y == 0 { accent.lighten(90%) }
      else if calc.odd(y) { white }
      else { bg-card }
    },
    inset: 5pt,
  )

  show table.cell.where(y: 0): set text(weight: "bold", fill: accent, size: 8pt)

  // ==========================================
  // LISTS
  // ==========================================

  set list(
    marker: text(fill: accent)[•],
    indent: 8pt,
    body-indent: 5pt,
    spacing: 0.4em,
  )

  set enum(
    indent: 8pt,
    body-indent: 5pt,
    spacing: 0.4em,
  )

  // ==========================================
  // STRONG / EM
  // ==========================================

  show strong: set text(fill: text-primary, weight: "bold")
  show emph: set text(fill: text-secondary, style: "italic")

  // ==========================================
  // LINKS
  // ==========================================

  show link: it => {
    set text(fill: accent)
    underline(offset: 2pt, stroke: 0.5pt + accent.lighten(40%), it)
  }

  // ==========================================
  // CONTENT LAYOUT
  // ==========================================

  if layout == "two-col" {
    columns(2, gutter: 14pt, doc)
  } else {
    doc
  }
}
