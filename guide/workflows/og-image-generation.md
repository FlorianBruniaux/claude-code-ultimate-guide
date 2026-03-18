# Dynamic OG Image Generation with Astro

Generate social preview images automatically at build time instead of maintaining stale static PNGs. Every share on Twitter/X, LinkedIn, or Slack will show accurate, up-to-date stats.

## Why bother

Static OG images go stale. The day you add your 200th template or hit 1k GitHub stars, your social preview still shows the old numbers. Dynamic generation solves this once and stays accurate forever.

The pattern below uses Satori (Vercel) to render a React-like tree to SVG, then resvg to convert to PNG. It runs at build time in Astro — zero runtime cost, no external service.

## Stack

| Package | Role |
|---------|------|
| `satori` | Renders JSX-like object tree to SVG |
| `@resvg/resvg-js` | Converts SVG to PNG (Rust, fast) |
| `@fontsource/inter` | Local font files (woff1 format required) |

## Setup

```bash
pnpm add satori @resvg/resvg-js @fontsource/inter
```

Create the file at `src/pages/og-image.png.ts`. Astro automatically serves it at `/og-image.png`.

Reference it from your layout:

```html
<meta property="og:image" content="/og-image.png" />
<meta name="twitter:image" content="/og-image.png" />
```

See the ready-to-use template: [`examples/scripts/og-image-astro.ts`](../../examples/scripts/og-image-astro.ts)

## The pattern

```typescript
import type { APIRoute } from 'astro'
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

export const GET: APIRoute = () => {
  const fontData = readFileSync(
    resolve(__dirname, '../../node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')
  ).buffer as ArrayBuffer

  const svg = satori(
    { type: 'div', props: { style: { /* ... */ }, children: [ /* ... */ ] } },
    { width: 1200, height: 630, fonts: [{ name: 'Inter', data: fontData }] }
  )

  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng()

  return new Response(png.buffer as ArrayBuffer, {
    headers: { 'Content-Type': 'image/png' },
  })
}
```

## Dynamic stats from content

Count your content files at build time instead of hardcoding:

```typescript
function countQuestions(): number {
  const dir = resolve(__dirname, '../content/questions')
  let total = 0
  for (const cat of readdirSync(dir, { withFileTypes: true })) {
    if (cat.isDirectory()) {
      total += readdirSync(resolve(dir, cat.name))
        .filter(f => f.endsWith('.md')).length
    }
  }
  return total
}
```

Stats you can auto-count:
- Markdown files in a content directory (questions, articles, docs)
- YAML entries in a data file
- Line count of a large document

Stats to keep hardcoded (update manually):
- GitHub stars (dynamic, use `1.1k+` as a conservative label)
- Templates from another repo
- Performance benchmarks

## Gotchas

### Font format matters

Satori requires **woff1** or **TTF**. It will silently fail or throw an error with woff2 or remote CDN URLs that redirect to HTML.

```typescript
// Correct — local woff1 from @fontsource
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')

// Fails — woff2 not supported by resvg
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2')

// Fails — CDN may return HTML (redirects, auth walls)
await fetch('https://fonts.gstatic.com/s/inter/...')
```

### Static files shadow API routes

Astro dev server serves static files in `public/` **before** API routes. If you have a `public/og-image.png`, it will always be served instead of your dynamic endpoint.

**Delete it:**
```bash
rm public/og-image.png
```

Also check the project root and `dist/` — files there can shadow the route too. Diagnose with `curl -I http://localhost:4321/og-image.png`: if the response has a `Last-Modified` header, you are hitting a static file, not the API route.

### Browser cache

After removing the static file, do a hard refresh (`Cmd+Shift+R`) or test in a fresh incognito window. The browser may have cached the old PNG aggressively.

### `satori` is synchronous in newer versions

Some versions of satori return a `Promise<string>`, others return `string`. If you get a `[object Promise]` PNG, add `await`:

```typescript
const svg = await satori(tree, options)
```

## Testing

**Local preview** — visit directly in the browser:
```
http://localhost:4321/og-image.png
```

**Social preview simulation** — paste your prod URL into:
- [opengraph.xyz](https://www.opengraph.xyz) — generic OG debugger
- LinkedIn Post Inspector (`linkedin.com/post-inspector/`) — forces cache refresh for LinkedIn
- Twitter Card Validator (`cards-dev.twitter.com/validator`)

**CI check** — if you want to catch regressions, you can add a build step that checks the generated PNG file size is above a threshold:

```bash
# In CI after pnpm build
SIZE=$(wc -c < dist/og-image.png)
if [ "$SIZE" -lt 10000 ]; then
  echo "og-image.png looks too small ($SIZE bytes) — generation may have failed"
  exit 1
fi
```

## Variants

### Personal branding (no stats grid)

```typescript
children: [
  { type: 'span', props: { style: { fontSize: '48px', color: '#c0522a' }, children: 'FB.' } },
  { type: 'span', props: { style: { fontSize: '80px', fontWeight: 800, color: '#f5f5f5' }, children: 'Your Name' } },
  { type: 'span', props: { style: { fontSize: '24px', color: '#8b949e' }, children: 'Your tagline here' } },
]
```

### Project list badges

```typescript
['project-a.com', 'project-b.com', 'project-c.com'].map(label => ({
  type: 'div',
  props: {
    style: { background: '#161b22', border: '1px solid #30363d', borderRadius: '8px', padding: '8px 16px' },
    children: [{ type: 'span', props: { style: { color: '#c0522a' }, children: label } }],
  },
}))
```

### Terminal-style badge (for CLI tools)

```typescript
{
  type: 'div',
  props: {
    style: { background: '#21262d', border: '1px solid #30363d', borderRadius: '20px', padding: '6px 16px', color: '#3fb950', fontFamily: 'monospace' },
    children: '>_ your-cli-tool',
  },
}
```

## Keeping stats in sync

Maintain a single source of truth. When you update stats in the OG image, update them everywhere (landing page badges, README, etc.) in the same commit.

For projects with multiple landings, create a slash command `/update-stats-image-landings` that walks each repo and prompts you to verify each stat. This prevents drift across sites.
