// Cheatsheet Template - Web Design Reproduction (Light Theme)
// Inspired by claude-code-ultimate-guide-landing design
// 2-column layout with visual components matching the web

// ==========================================
// COLOR PALETTE - Bold Guy (Warm Beige + Orange Brûlé, Print Optimized)
// ==========================================

#let bg-primary = white
#let bg-card = rgb("#fef7f0")          // Warm secondary bg - subtle card background
#let bg-code = rgb("#f0e8df")          // Warm tertiary bg - code blocks
#let text-primary = rgb("#1a1207")     // Dark warm brown - main text
#let text-secondary = rgb("#4a3f31")   // Medium warm brown - secondary text
#let text-muted = rgb("#6b6053")       // Warm muted brown - muted text
#let border-color = rgb("#d4cdc5")     // Warm border - visible on print
#let accent = rgb("#d4520a")           // Orange brûlé - better print rendering
#let success = rgb("#15803d")          // Green 700 - print safe
#let danger = rgb("#b91c1c")           // Red 700 - print safe
#let warning = rgb("#b45309")          // Amber 700 - readable on print

// Context zones colors
#let zone-green = rgb("#dcfce7")       // Green 100
#let zone-yellow = rgb("#fef3c7")      // Amber 100
#let zone-orange = rgb("#fed7aa")      // Orange 200
#let zone-red = rgb("#fee2e2")         // Red 100

// ==========================================
// CONTEXT BAR COMPONENT
// ==========================================

#let context-bar(green: "0-50%", yellow: "50-70%", orange: "70-90%", red: "90%+") = {
  set text(size: 8pt, weight: "medium", fill: text-primary)

  grid(
    columns: (1fr, 1fr, 1fr, 1fr),
    gutter: 0pt,

    // Green zone
    rect(
      fill: zone-green,
      stroke: 1pt + success,
      inset: 8pt,
      width: 100%,
      height: 100%,
      align(center)[#text(fill: success)[✅ #green]]
    ),

    // Yellow zone
    rect(
      fill: zone-yellow,
      stroke: 1pt + warning,
      inset: 8pt,
      width: 100%,
      height: 100%,
      align(center)[#text(fill: warning)[⚠️ #yellow]]
    ),

    // Orange zone
    rect(
      fill: zone-orange,
      stroke: 1pt + rgb("#ea580c"),
      inset: 8pt,
      width: 100%,
      height: 100%,
      align(center)[#text(fill: rgb("#ea580c"))[🔶 #orange]]
    ),

    // Red zone
    rect(
      fill: zone-red,
      stroke: 1pt + danger,
      inset: 8pt,
      width: 100%,
      height: 100%,
      align(center)[#text(fill: danger)[🚨 #red]]
    ),
  )
}

// ==========================================
// CARD COMPONENT (matches web card style)
// ==========================================

#let card(title: none, body) = {
  block(
    fill: bg-card,
    stroke: 1pt + border-color,
    radius: 8pt,
    inset: 16pt,
    width: 100%,
    breakable: true,
    [
      #if title != none [
        #text(14pt, weight: "bold", fill: text-primary)[#title]
        #v(10pt)
      ]
      #body
    ]
  )
  v(12pt)
}

// ==========================================
// DO/DON'T GRID COMPONENT
// ==========================================

#let do-dont(dont-items, do-items) = {
  grid(
    columns: (1fr, 1fr),
    gutter: 12pt,

    // DON'T column
    block(
      fill: danger.lighten(85%),
      stroke: 1pt + danger,
      radius: 6pt,
      inset: 12pt,
      width: 100%,
      [
        #text(12pt, weight: "bold", fill: danger)[❌ Don't]
        #v(8pt)
        #for item in dont-items [
          • #text(size: 9pt, fill: text-primary)[#item]
          #v(4pt)
        ]
      ]
    ),

    // DO column
    block(
      fill: success.lighten(85%),
      stroke: 1pt + success,
      radius: 6pt,
      inset: 12pt,
      width: 100%,
      [
        #text(12pt, weight: "bold", fill: success)[✅ Do]
        #v(8pt)
        #for item in do-items [
          • #text(size: 9pt, fill: text-primary)[#item]
          #v(4pt)
        ]
      ]
    ),
  )
}

// ==========================================
// GOLDEN RULES COMPONENT
// ==========================================

#let golden-rules(rules) = {
  card(title: "The Golden Rules")[
    #for (i, rule) in rules.enumerate() [
      #grid(
        columns: (auto, 1fr),
        gutter: 10pt,

        // Number badge
        box(
          fill: accent,
          inset: (x: 8pt, y: 6pt),
          radius: 50%,
          width: 24pt,
          height: 24pt,
          align(center + horizon)[
            #text(11pt, weight: "bold", fill: white)[#str(i + 1)]
          ]
        ),

        // Rule text
        align(horizon)[
          #text(10pt, fill: text-primary)[#rule]
        ]
      )
      #v(8pt, weak: true)
    ]
  ]
}

// ==========================================
// FICHE RÉCAP COMPONENT
// 2-column layout: "Points à retenir" | "Par où commencer ?"
// ==========================================

#let fiche-recap(
  title: none,
  subtitle: none,
  wp-number: none,
  points: (),
  actions: (),
) = {
  // Header block
  block(
    fill: accent,
    inset: (x: 16pt, y: 10pt),
    width: 100%,
    radius: (top-left: 6pt, top-right: 6pt, bottom-left: 0pt, bottom-right: 0pt),
    [
      #grid(
        columns: (1fr, auto),
        align: (left + horizon, right + horizon),
        [
          #text(14pt, weight: "bold", fill: white)[#title]
          #if subtitle != none [
            #h(8pt)
            #text(10pt, fill: white)[— #subtitle]
          ]
        ],
        if wp-number != none [
          #box(
            stroke: 1pt + white,
            inset: (x: 8pt, y: 4pt),
            radius: 4pt,
            text(11pt, weight: "bold", fill: white)[#wp-number]
          )
        ]
      )
    ]
  )

  // Body: 2 columns
  block(
    fill: bg-card,
    stroke: (left: 2pt + accent, right: 2pt + accent, bottom: 2pt + accent),
    radius: (bottom-left: 6pt, bottom-right: 6pt, top-left: 0pt, top-right: 0pt),
    inset: 0pt,
    width: 100%,
    breakable: false,
    grid(
      columns: (1fr, 1fr),
      gutter: 0pt,

      // Left: Points à retenir
      block(
        inset: (x: 14pt, y: 12pt),
        width: 100%,
        [
          #text(10pt, weight: "bold", fill: accent)[Points à retenir]
          #v(8pt)
          #for point in points [
            #grid(
              columns: (auto, 1fr),
              gutter: 6pt,
              text(9pt, fill: accent)[▸],
              text(9pt, fill: text-primary)[#point]
            )
            #v(5pt, weak: true)
          ]
        ]
      ),

      // Right: Par où commencer ?
      block(
        fill: bg-primary,
        stroke: (left: 1.5pt + border-color),
        inset: (x: 14pt, y: 12pt),
        width: 100%,
        [
          #text(10pt, weight: "bold", fill: text-primary)[Par où commencer ?]
          #v(8pt)
          #for (i, action) in actions.enumerate() [
            #grid(
              columns: (auto, 1fr),
              gutter: 6pt,
              box(
                fill: accent,
                inset: (x: 5pt, y: 2pt),
                radius: 10pt,
                text(8pt, weight: "bold", fill: white)[#str(i + 1)]
              ),
              text(9pt, fill: text-primary)[#action]
            )
            #v(5pt, weak: true)
          ]
        ]
      )
    )
  )
  v(8pt)
}

// ==========================================
// MAIN CHEATSHEET FUNCTION
// ==========================================

#let cheatsheet(
  title: none,
  subtitle: none,
  author: none,
  date: none,
  version: "1.0",
  series: none,
  paper: "a4",
  lang: "en",
  region: "US",
  font: ("Helvetica Neue", "Helvetica", "Arial"),
  fontsize: 10pt,
  doc,
) = {
  // Document metadata
  set document(
    title: title,
    author: author,
  )

  set page(
    paper: paper,
    margin: (x: 1.5cm, y: 1.5cm),
    header: none,
    footer: [
      #grid(
        columns: (1fr, auto, 1fr),
        align: (left, center, right),

        text(7pt, fill: text-muted)[florian.bruniaux.com],
        text(7pt, fill: text-muted)[cc.bruniaux.com],
        text(7pt, fill: text-muted)[v#version]
      )
    ],
    numbering: none,
  )

  // Text settings
  set text(
    font: font,
    size: fontsize,
    lang: lang,
    region: region,
    fill: text-primary,
  )

  // Paragraph settings - compact for cheatsheet
  set par(
    justify: false,
    leading: 0.5em,
  )

  // ==========================================
  // HEADER - Compact
  // ==========================================

  align(center)[
    #text(20pt, weight: "bold", fill: text-primary, tracking: -0.01em)[#title]
    #v(4pt)
    #text(12pt, fill: text-secondary)[#subtitle]
    #v(6pt)
    #text(9pt, fill: text-muted)[v#version | #date]
  ]

  v(16pt)

  // Top accent line
  line(length: 100%, stroke: 2pt + accent)

  v(16pt)

  // ==========================================
  // HEADING STYLES - Compact
  // ==========================================

  show heading.where(level: 1): it => {
    set text(fill: text-primary, size: 14pt, weight: "bold")
    v(12pt, weak: true)
    block(it)
    v(8pt, weak: true)
  }

  show heading.where(level: 2): it => {
    set text(fill: accent, size: 12pt, weight: "bold")
    v(10pt, weak: true)
    block(it)
    v(6pt, weak: true)
  }

  show heading.where(level: 3): it => {
    set text(fill: text-secondary, size: 11pt, weight: "bold")
    v(8pt, weak: true)
    block(it)
    v(4pt, weak: true)
  }

  // ==========================================
  // CODE BLOCKS - Compact with left accent
  // ==========================================

  show raw.where(block: true): it => {
    set text(
      size: 8pt,
      font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
    )
    block(
      fill: bg-code,
      inset: 8pt,
      radius: 4pt,
      stroke: (left: 3pt + accent),
      width: 100%,
      breakable: true,
      it
    )
    v(6pt, weak: true)
  }

  // Inline code
  show raw.where(block: false): it => {
    box(
      fill: bg-code,
      inset: (x: 4pt, y: 2pt),
      radius: 3pt,
      text(
        size: 0.9em,
        font: ("JetBrains Mono", "Fira Code", "SF Mono", "Consolas", "monospace"),
        it
      )
    )
  }

  // ==========================================
  // TABLE STYLING - Clean and compact
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
    inset: 6pt,
  )

  show table.cell.where(y: 0): set text(weight: "bold", fill: accent, size: 9pt)

  // ==========================================
  // LINK STYLING
  // ==========================================

  show link: it => {
    set text(fill: accent)
    underline(offset: 2pt, stroke: 0.5pt + accent.lighten(40%), it)
  }

  show strong: set text(fill: text-primary, weight: "bold")

  // ==========================================
  // CALLOUTS - Compact
  // ==========================================

  // Standard callout boxes for info/warning/success/danger
  // These will be generated by Quarto's div syntax

  // ==========================================
  // 2-COLUMN LAYOUT
  // ==========================================

  columns(2, gutter: 16pt, doc)
}
