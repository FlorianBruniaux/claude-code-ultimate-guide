---
title: "Design Reference File"
description: "Keep brand-book.html and ui-kit.html at project root as permanent Claude Code context for consistent UI generation"
tags: [design-system, frontend, web, ui, consistency, brand, color-palette, tailwind]
---

# Design Reference File — CLAUDE.md Pattern

Keep `brand-book.html` and `ui-kit.html` at the project root as permanent context files. Claude Code reads them before generating any UI — every new page inherits your design system automatically.

Inspired by Boris Paillard's workflow (mixt.care, March 2026): once the design system is in place, new pages take 5 minutes instead of 30.

## The Problem

When building a website with Claude Code across multiple sessions, every new page risks drifting from the design — wrong colors, inconsistent typography, new component variants. Re-stating design constraints in each prompt is repetitive and unreliable.

## The Solution

Two HTML files at the project root act as a design memory Claude can read at any time:

- `brand-book.html` — color palette with semantic roles, fonts, CSS variables, WCAG contrast ratios
- `ui-kit.html` — documented components (buttons, forms, trust bars, section labels)

One CLAUDE.md instruction makes Claude reference them before every UI task.

## Project Structure

```
project/
├── brand-book.html     # Color palette + typography + CSS variables (permanent reference)
├── ui-kit.html         # Component library documented with Tailwind
├── CLAUDE.md           # Design system instruction below
├── src/
│   ├── styles/
│   │   └── tokens.css  # CSS variables extracted from brand-book.html
│   └── components/
└── ...
```

## CLAUDE.md Snippet

Add this to your project-level `CLAUDE.md`:

```markdown
## Design System

Always read `brand-book.html` and `ui-kit.html` before generating any UI component, page, or layout.

Rules:
- Never hardcode colors or font sizes — use CSS variables from brand-book.html
- Reuse components from ui-kit.html before creating new variants
- New pages must use the same design tokens (--color-primary, --font-primary, etc.)
- If a requested design element is not in the UI kit, document it in ui-kit.html after creating it
```

## Step 1 — Generate brand-book.html

```
Create a brand-book.html file at the project root.

For each color in my palette, display a card showing:
- Color swatch (120×80px block)
- Name, hex code, RGB values, HSL values
- CSS variable name (e.g. --color-primary)
- Semantic role: PRIMARY | DARK | LIGHT | ACCENT | NEUTRAL
- Usage rule in plain text (e.g. "CTAs, buttons, active links")
- WCAG contrast ratio vs white: X.X:1 — AA PASS/FAIL — AAA PASS/FAIL
- WCAG contrast ratio vs black: X.X:1 — AA PASS/FAIL — AAA PASS/FAIL

My palette:
[LIST YOUR COLORS AND ROLES HERE]

My fonts:
[LIST YOUR FONTS HERE]

Include a type scale section: 12px / 16px / 20px / 24px / 32px / 48px / 64px / 96px with rem equivalents.

At the bottom, output a copyable <style> block with all CSS variables (:root { ... }).

Style brand-book.html itself using these variables — it should demonstrate the design system.
```

## Step 2 — Generate ui-kit.html

```
Build ui-kit.html documenting my base components using Tailwind and the CSS variables from brand-book.html.

Include:
- Buttons: primary/secondary/ghost variants, 3 sizes (sm/md/lg)
- Trust bars with vertical color separators
- Section labels with horizontal rules (uppercase, letter-spacing)
- Typography specimens: h1–h4, body, caption — using --font-primary and --font-secondary
- Color swatches grid with contrast ratios displayed
- Form elements: input, select, textarea in default/focus/error states

Each component should show: component name, usage notes, and the Tailwind classes used.
Reference CSS variables from brand-book.html — no hardcoded values.
```

## Step 3 — WCAG Color Audit (optional but recommended)

Run this after generating the brand book to catch accessibility issues before building:

```
Audit the color palette in brand-book.html for WCAG 2.1 compliance:

1. For all likely foreground/background combinations, calculate exact contrast ratios (2 decimal places)
2. Flag pairs that fail WCAG AA: 4.5:1 for normal text, 3:1 for large text and UI components
3. Simulate deuteranopia, protanopia, tritanopia — flag problematic combinations
4. For each failing pair, suggest the minimum hex adjustment to pass AA while staying within 10% hue deviation
5. Output: markdown table with columns: Combination | Ratio | AA Normal | AA Large | AAA | Color Blind Safe

External references:
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- ColorOracle (color blindness simulator): https://colororacle.org/
```

## Step 4 — Scroll Animations (optional)

```
Add scroll animations to all cards and section titles using vanilla JS Intersection Observer.
Elements should fade in + slide up with 0.6s ease-out transitions, 100ms stagger between items.
Apply only to elements with [data-animate] attribute — opt-in, not global.
Do not use any animation library — vanilla JS only.
```

## Example — mixt.care Color Palette

Well-structured palette with semantic roles and CSS variables:

```css
:root {
  /* Colors */
  --color-primary: #5C1A2E;   /* Deep bordeaux — CTAs, buttons, active links */
  --color-dark: #3D2B1F;      /* Warm brown — body text, dark backgrounds */
  --color-accent: #B87333;    /* Copper — hover states, secondary highlights */
  --color-secondary: #6B5B8E; /* Soft violet — badges, illustrations */
  --color-light: #F5F0EA;     /* Cream — section backgrounds, cards */

  /* Typography */
  --font-primary: 'Geist', sans-serif;       /* Body text */
  --font-secondary: 'Newsreader', serif;     /* Emphasis, quotes */
  --font-display: 'Fraunces', serif;         /* Logo, display headings only */

  /* Type scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
  --text-3xl: 3rem;
  --text-display: 6rem;        /* Desktop statement footer */
  --text-display-mobile: 3rem;
}
```

**WCAG notes for this palette** (estimated):
- Bordeaux on cream: ~8.2:1 — AA PASS
- Brown on cream: ~9.1:1 — AA PASS
- White on bordeaux: ~8.2:1 — AA PASS
- Copper on white: ~3.1:1 — AA FAIL for normal text (use only for UI components or darken to #9B5F20)
- Violet on cream: ~4.8:1 — AA PASS

## When to Use This Pattern

- Building a marketing site, landing page, or product website with Claude Code
- When you need consistent design across multiple pages generated in different sessions
- Before starting UI work on any project with established brand guidelines
- Replacing manual design system documentation with an interactive, self-demonstrating reference

## Limitations

- Effective for static/marketing sites and MVPs — complex component libraries need a proper design system tool (Storybook, Figma)
- The 2h timeframe assumes you know your design intent before prompting (colors, fonts, layout direction)
- WCAG audit from Claude is estimated — verify critical pairs with WebAIM or a dedicated tool