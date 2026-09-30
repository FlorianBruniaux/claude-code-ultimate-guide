---
name: landing-page-generator
description: "Generate complete, deploy-ready landing pages from any repository. Use when creating a homepage for an open-source project, building a project website, converting a README into a marketing page, or standardizing landing pages across multiple repos."
allowed-tools: Read Bash Write
effort: medium
---

# Landing page generator

Generate a complete, deploy-ready landing page from any repository by analyzing its documentation and structure.

## When to use this skill

- Creating a landing page for a GitHub repository
- Generating static sites from existing documentation
- Standardizing landing pages across multiple projects
- Converting README content to marketing/showcase pages

## What this skill does

1. **Analyze Repository**: Read README.md, CHANGELOG.md, package.json/VERSION, docs/, assets/
2. **Extract Content**: Identify title, tagline, features, installation, screenshots
3. **Map to Sections**: Hero, Features, Install, FAQ, Footer (+ optional: Risk Banner, Pricing)
4. **Generate Landing**: Create complete static site (HTML + CSS + JS)
5. **Deploy-Ready Output**: Include GitHub Actions workflow for GitHub Pages

## How to use

### Basic usage

```
/landing-page-generator from ~/path/to/repo
```

### With options

```
/landing-page-generator from ~/path/to/repo --risk-banner --pricing-table
```

### Available options

| Option | Description | Default |
|--------|-------------|---------|
| `--risk-banner` | Add prominent warning/disclaimer banner above fold | false |
| `--pricing-table` | Include pricing comparison section | false |
| `--screenshots <path>` | Path to screenshots folder | ./assets/ |
| `--theme [dark\|light]` | Color theme variant | dark |
| `--search` | Enable Cmd+K search | true |
| `--output <path>` | Output directory | ./[repo-name]-landing/ |

## Workflow

### Step 1: Repository analysis

Read and analyze these files from the source repo:

```
README.md        → Primary content source (title, tagline, features, install)
CHANGELOG.md     → Version info, recent changes
package.json     → Version number, dependencies, metadata
VERSION          → Alternative version source
docs/            → Additional documentation pages
assets/          → Screenshots, images
LICENSE          → License type for badge
```

### Step 2: Content extraction map

| Source | Target Section | Extraction Method |
|--------|---------------|-------------------|
| README title/badges | Hero | First H1 + shield.io badge lines |
| README TL;DR | Hero tagline | First paragraph or blockquote after title |
| README features | Features grid | H2/H3 sections with bullet lists |
| README install | Quick Start | Code blocks with shell commands |
| README usage | Examples | Code blocks with examples |
| README FAQ | FAQ | Details/summary or H3+P patterns |
| CHANGELOG | What's New | Latest 1-3 releases |
| assets/*.png | Screenshots | Gallery section |

### Step 3: Section generation

Generate these sections in order:

1. **Header** (sticky)
   - Logo/project name
   - Nav links: Features, Install, FAQ
   - Actions: Search (Cmd+K), GitHub Star, primary CTA

2. **Risk Banner** (if `--risk-banner`)
   - Orange/warning style above fold
   - Clear, visible disclaimer text
   - Link to detailed disclosure section

3. **Hero Section**
   - Title from README H1
   - Tagline from TL;DR/first paragraph
   - Stats badges (version, license, platform)
   - CTAs: "Quick Start" (primary), "View on GitHub" (secondary)

4. **Architecture/Overview** (if diagram in README)
   - ASCII diagram converted to styled block
   - Or overview cards

5. **Features Grid**
   - 4-6 feature cards from README features
   - Icon + title + description pattern

6. **Pricing Table** (if `--pricing-table`)
   - Plans comparison table
   - Multipliers/usage table if present

7. **Screenshots Gallery** (if assets exist)
   - Tab-based or carousel gallery
   - Captions from alt text

8. **Quick Start Section**
   - One-liner install command (featured code block)
   - Setup steps
   - First usage example

9. **Risk Disclosure** (if `--risk-banner`)
   - Full disclaimer section
   - ToS considerations
   - Recommendations

10. **FAQ Section**
    - Generated from README FAQ or common questions
    - Collapsible details pattern

11. **Related Projects** (if links in README)
    - Cards linking to dependencies/related repos

12. **Footer**
    - Quick links
    - License badge
    - Version info
    - Author/repo links

### Step 4: Output structure

```
[project-name]-landing/
├── index.html              # Main landing page
├── styles.css              # Complete stylesheet
├── search.js               # Cmd+K search functionality
├── search-data.js          # Search index (FAQ, features)
├── favicon.svg             # Generated or copied
├── robots.txt              # SEO
├── CLAUDE.md               # Project instructions
├── README.md               # Landing repo documentation
├── assets/                 # Copied screenshots
│   └── [copied from source]
└── .github/
    └── workflows/
        └── static.yml      # GitHub Pages deployment
```

### Step 5: Validation checkpoint

Before finalizing, verify:
- All sections render correctly in a browser
- Links point to valid targets (GitHub repo, docs, install commands)
- Responsive layout works at mobile (375px), tablet (768px), and desktop (1280px) widths
- Accessibility: skip links present, ARIA labels on interactive elements, color contrast passes WCAG AA

## Tech stack

- **No build step**: Pure HTML + CSS + JS
- **Search**: MiniSearch lazy-loaded from CDN with fallback
- **Deployment**: GitHub Pages via Actions
- **Styling**: CSS custom properties, responsive, dark theme default
- **Accessibility**: Skip links, ARIA labels, keyboard navigation

## CSS Patterns (from established landings)

### Component classes

```css
/* Buttons */
.btn, .btn-primary, .btn-secondary, .btn-github-star, .btn-outline

/* Cards */
.feature-card, .comparison-card, .path-card

/* Layout */
.container, .features-grid, .hero, .section

/* Utilities */
.visually-hidden, .skip-link
```

### CSS variables

```css
:root {
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-border: #30363d;
  --color-text: #c9d1d9;
  --color-text-muted: #8b949e;
  --color-primary: #58a6ff;
  --color-success: #3fb950;
  --color-warning: #d29922;
  --color-danger: #f85149;
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --radius: 6px;
}
```

## Example

**User**: `/landing-page-generator from ~/projects/my-project --risk-banner --pricing-table`

**Output**:

Creates `~/projects/my-project-landing/` with:
- Complete landing page showcasing the multi-provider router
- Prominent ToS risk banner (orange, above fold)
- Provider cards (Anthropic, Copilot, Ollama)
- Pricing tables from README
- Screenshots gallery
- GitHub Pages deployment ready

## Tips

- Always include `--risk-banner` for projects with legal/ToS considerations
- Screenshots significantly improve landing quality - ensure assets/ is populated
- The skill preserves README language (English/French)
- Review generated FAQ - may need customization
- Test responsive design after generation

## References

See `references/landing-pattern.md` for detailed pattern documentation.
See `assets/` for reusable templates and snippets.
