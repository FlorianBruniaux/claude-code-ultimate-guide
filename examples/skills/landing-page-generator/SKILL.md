---
name: landing-page-generator
description: Generate complete landing pages from repositories. Analyzes README, features, and structure to create static sites following established patterns. Use for new project landings, open-source showcases, documentation portals.
tags: [landing-page, static-site, github-pages, marketing]
---

# Landing Page Generator

Generate a complete, deploy-ready landing page from any repository by analyzing its documentation and structure.

## When to Use This Skill

- Creating a landing page for a GitHub repository
- Generating static sites from existing documentation
- Standardizing landing pages across multiple projects
- Converting README content to marketing/showcase pages

## What This Skill Does

1. **Analyze Repository**: Read README.md, CHANGELOG.md, package.json/VERSION, docs/, assets/
2. **Extract Content**: Identify title, tagline, features, installation, screenshots
3. **Map to Sections**: Hero, Features, Install, FAQ, Footer (+ optional: Risk Banner, Pricing)
4. **Generate Landing**: Create complete static site (HTML + CSS + JS)
5. **Deploy-Ready Output**: Include GitHub Actions workflow for GitHub Pages

## How to Use

### Basic Usage

```
/landing-page-generator from ~/path/to/repo
```

### With Options

```
/landing-page-generator from ~/path/to/repo --risk-banner --pricing-table
```

### Available Options

| Option | Description | Default |
|--------|-------------|---------|
| `--risk-banner` | Add prominent warning/disclaimer banner above fold | false |
| `--pricing-table` | Include pricing comparison section | false |
| `--screenshots <path>` | Path to screenshots folder | ./assets/ |
| `--theme [dark\|light]` | Color theme variant | dark |
| `--search` | Enable Cmd+K search | true |
| `--output <path>` | Output directory | ./[repo-name]-landing/ |

## Workflow

### Step 1: Repository Analysis

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

### Step 2: Content Extraction Map

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

### Step 3: Section Generation

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

### Step 4: Output Structure

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

## Tech Stack

- **No build step**: Pure HTML + CSS + JS
- **Search**: MiniSearch lazy-loaded from CDN with fallback
- **Deployment**: GitHub Pages via Actions
- **Styling**: CSS custom properties, responsive, dark theme default
- **Accessibility**: Skip links, ARIA labels, keyboard navigation

## CSS Patterns (from established landings)

### Component Classes

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

### CSS Variables

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

## Related Use Cases

- Open-source project showcases
- Documentation portals
- Product landing pages
- Tool/utility marketing sites

## References

See `references/landing-pattern.md` for detailed pattern documentation.
See `assets/` for reusable templates and snippets.