# Landing Page Pattern Reference

Documentation of the established landing page pattern used in `claude-code-ultimate-guide-landing` and `claude-cowork-guide-landing`.

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | None (vanilla) | Simplicity, no build step, easy hosting |
| Styling | Single CSS file | Maintainable, no preprocessor needed |
| JavaScript | Vanilla + MiniSearch CDN | Minimal dependencies, lazy-loaded |
| Deployment | GitHub Pages + Actions | Free, automatic, reliable |
| Search | MiniSearch with fallback | Client-side, fast, no backend needed |

## File Structure

```
project-landing/
├── index.html              # Main landing (all sections)
├── styles.css              # Complete stylesheet (~3000 lines)
├── search.js               # Search modal + keyboard nav
├── search-data.js          # Search index arrays
├── *-data.js               # Additional data files (optional)
├── favicon.svg             # Project icon
├── robots.txt              # SEO
├── CLAUDE.md               # Claude instructions
├── README.md               # Repo documentation
├── assets/                 # Images, screenshots
└── .github/workflows/
    └── static.yml          # Pages deployment
```

## HTML Structure

### Document Head

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Project Name] - [Tagline]</title>
  <meta name="description" content="[Description]">

  <!-- SEO -->
  <link rel="canonical" href="https://[user].github.io/[repo]-landing/">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="[Title]">
  <meta property="og:description" content="[Description]">
  <meta property="og:url" content="[URL]">
  <meta property="og:image" content="[og-image.png]">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="[Title]">
  <meta name="twitter:description" content="[Description]">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="favicon.svg">

  <!-- Styles -->
  <link rel="stylesheet" href="styles.css">
</head>
```

### Body Structure

```html
<body>
  <a href="#main" class="skip-link">Skip to content</a>

  <header class="header">...</header>

  <main id="main">
    <section class="hero">...</section>
    <section class="features">...</section>
    <section class="install">...</section>
    <section class="faq">...</section>
    <!-- More sections -->
  </main>

  <footer class="footer">...</footer>

  <!-- Search Modal -->
  <div id="search-modal" class="search-modal" role="dialog" aria-modal="true">...</div>

  <!-- Scripts (order matters) -->
  <script src="search-data.js"></script>
  <script src="search.js"></script>
</body>
```

## Section Patterns

### Header

```html
<header class="header">
  <div class="container header-content">
    <a href="/" class="logo">
      <span class="logo-icon">>_</span>
      <span class="logo-text">[Project Name]</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <ul class="nav-list">
        <li><a href="#features">Features</a></li>
        <li><a href="#install">Install</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </nav>
    <div class="header-actions">
      <button class="search-btn" aria-label="Search (Cmd+K)">
        <span>Search</span>
        <kbd>⌘K</kbd>
      </button>
      <a href="[github-url]" class="btn btn-github-star">
        ⭐ Star on GitHub
      </a>
    </div>
  </div>
</header>
```

### Hero Section

```html
<section class="hero">
  <div class="container">
    <div class="hero-badges">
      <img src="https://img.shields.io/badge/..." alt="...">
      <!-- More badges -->
    </div>
    <h1 class="hero-title">[Main Title]</h1>
    <p class="hero-tagline">[Tagline/TL;DR]</p>
    <div class="hero-stats">
      <span class="stat"><strong>[N]</strong> features</span>
      <span class="stat"><strong>[N]</strong> examples</span>
    </div>
    <div class="hero-ctas">
      <a href="#install" class="btn btn-primary">Quick Start</a>
      <a href="[github]" class="btn btn-secondary">View on GitHub</a>
    </div>
  </div>
</section>
```

### Risk Banner (Optional)

```html
<div class="risk-banner" role="alert">
  <div class="container">
    <span class="risk-icon">⚠️</span>
    <span class="risk-text">
      <strong>Risk Disclosure:</strong> [Warning text]
    </span>
    <a href="#risk-disclosure" class="risk-link">Learn more →</a>
  </div>
</div>
```

### Features Grid

```html
<section id="features" class="features">
  <div class="container">
    <h2 class="section-title">Features</h2>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">[emoji/icon]</div>
        <h3 class="feature-title">[Title]</h3>
        <p class="feature-desc">[Description]</p>
      </div>
      <!-- More cards -->
    </div>
  </div>
</section>
```

### Code Block with Copy

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">[language]</span>
    <button class="copy-btn" onclick="copyCode(this)" aria-label="Copy code">
      📋 Copy
    </button>
  </div>
  <pre><code>[code content]</code></pre>
</div>
```

### FAQ Section

```html
<section id="faq" class="faq">
  <div class="container">
    <h2 class="section-title">FAQ</h2>
    <div class="faq-list">
      <details class="faq-item">
        <summary class="faq-question">[Question]?</summary>
        <div class="faq-answer">
          <p>[Answer]</p>
        </div>
      </details>
      <!-- More items -->
    </div>
  </div>
</section>
```

### Footer

```html
<footer class="footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-brand">
        <span class="logo">>_ [Project]</span>
        <p class="footer-tagline">[Short tagline]</p>
      </div>
      <nav class="footer-links">
        <a href="[github]">GitHub</a>
        <a href="#faq">FAQ</a>
        <a href="[docs]">Docs</a>
      </nav>
      <div class="footer-meta">
        <span>MIT License</span>
        <span>v[version]</span>
      </div>
    </div>
  </div>
</footer>
```

## CSS Architecture

### Custom Properties (Theme)

```css
:root {
  /* Colors - Dark Theme */
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-surface-hover: #21262d;
  --color-border: #30363d;
  --color-text: #c9d1d9;
  --color-text-muted: #8b949e;
  --color-heading: #f0f6fc;
  --color-primary: #58a6ff;
  --color-primary-hover: #79b8ff;
  --color-success: #3fb950;
  --color-warning: #d29922;
  --color-danger: #f85149;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;

  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', Consolas, 'Liberation Mono', monospace;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 2rem;
  --font-size-4xl: 2.5rem;

  /* Layout */
  --container-max: 1200px;
  --radius: 6px;
  --radius-lg: 12px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.3);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.3);
}
```

### Component Patterns

```css
/* Container */
.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius);
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-bg);
}

.btn-secondary {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

/* Cards */
.feature-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Grids */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-xl);
}
```

### Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 768px) {
  .hero-title { font-size: var(--font-size-3xl); }
  .header-actions { display: none; }
  .nav { display: none; }
  /* Mobile nav toggle */
}

/* Mobile */
@media (max-width: 480px) {
  .hero-ctas { flex-direction: column; }
  .features-grid { grid-template-columns: 1fr; }
}
```

## JavaScript Patterns

### Search Implementation

```javascript
(function() {
  'use strict';

  let searchIndex = null;
  let miniSearchLoaded = false;

  // Lazy load MiniSearch
  async function loadMiniSearch() {
    if (miniSearchLoaded) return;
    await loadScript('https://cdn.jsdelivr.net/npm/minisearch@7/dist/umd/index.min.js');
    miniSearchLoaded = true;
  }

  // Build index from window.SEARCH_* data
  function buildIndex() {
    const items = [
      ...(window.SEARCH_FEATURES || []),
      ...(window.SEARCH_FAQ || []),
    ];
    // ... index building
  }

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearchModal();
    }
  });
})();
```

### Copy Code Function

```javascript
async function copyCode(button) {
  const codeBlock = button.closest('.code-block');
  const code = codeBlock.querySelector('code').textContent;

  try {
    await navigator.clipboard.writeText(code);
    button.textContent = '✓ Copied!';
    setTimeout(() => {
      button.textContent = '📋 Copy';
    }, 2000);
  } catch (err) {
    console.error('Copy failed:', err);
  }
}
```

## Deployment

### GitHub Actions Workflow

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
```

## Accessibility Checklist

- [ ] Skip link to main content
- [ ] Semantic HTML (header, main, section, footer)
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation for modals
- [ ] Focus visible styles
- [ ] Color contrast WCAG AA
- [ ] Reduced motion respect
- [ ] Alt text on images

## SEO Checklist

- [ ] Descriptive title tag
- [ ] Meta description
- [ ] Canonical URL
- [ ] Open Graph tags
- [ ] Twitter Card tags
- [ ] Structured data (Schema.org)
- [ ] robots.txt
- [ ] Semantic heading hierarchy