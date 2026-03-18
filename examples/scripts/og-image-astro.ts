/**
 * Dynamic OG Image Generator for Astro 5
 *
 * Generates a 1200x630 PNG at build time via Satori + resvg.
 * Place this file at: src/pages/og-image.png.ts
 *
 * Dependencies:
 *   pnpm add satori @resvg/resvg-js @fontsource/inter
 *
 * Usage:
 *   The file is auto-served at /og-image.png
 *   Reference it from your Layout:
 *     <meta property="og:image" content="/og-image.png" />
 *
 * IMPORTANT: Delete any existing public/og-image.png
 *   Static files in public/ take priority over API routes in dev mode.
 */

import type { APIRoute } from 'astro'
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readdirSync, readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

// ---------------------------------------------------------------------------
// Optional: count dynamic stats from your content at build time
// Remove if you don't need this
// ---------------------------------------------------------------------------
function countContentFiles(contentDir: string, extension = '.md'): number {
  try {
    let total = 0
    const entries = readdirSync(contentDir, { withFileTypes: true })
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const files = readdirSync(resolve(contentDir, entry.name))
        total += files.filter(f => f.endsWith(extension)).length
      } else if (entry.name.endsWith(extension)) {
        total++
      }
    }
    return total
  } catch {
    return 0
  }
}

// ---------------------------------------------------------------------------
// Stats to display — edit these to match your project
// ---------------------------------------------------------------------------
function getStats() {
  // Example: count quiz questions dynamically
  const questionCount = countContentFiles(
    resolve(__dirname, '../content/questions')
  )

  return [
    { value: questionCount > 0 ? `${questionCount}` : '200+', label: 'QUIZ QUESTIONS' },
    { value: '50+', label: 'TEMPLATES' },
    { value: '10k+', label: 'LINES OF DOCS' },
    { value: '500+', label: 'GITHUB STARS' },
  ]
}

// ---------------------------------------------------------------------------
// Stat card component (reused for each stat)
// ---------------------------------------------------------------------------
function statCard(value: string, label: string) {
  return {
    type: 'div',
    props: {
      style: {
        background: '#161b22',
        border: '1px solid #30363d',
        borderRadius: '10px',
        padding: '16px 24px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        minWidth: '200px',
      },
      children: [
        {
          type: 'span',
          props: {
            style: { fontSize: '36px', fontWeight: 800, color: '#f0883e', lineHeight: 1.2 },
            children: value,
          },
        },
        {
          type: 'span',
          props: {
            style: { fontSize: '13px', color: '#8b949e', letterSpacing: '0.1em', fontWeight: 500, marginTop: '4px' },
            children: label,
          },
        },
      ],
    },
  }
}

// ---------------------------------------------------------------------------
// Main route handler
// ---------------------------------------------------------------------------
export const GET: APIRoute = () => {
  const stats = getStats()

  // Font: use local woff (not woff2) from @fontsource — satori requires woff1 or TTF
  // woff2 and remote CDN URLs will fail silently or throw "Unsupported OpenType signature"
  const fontPath = resolve(
    __dirname,
    '../../node_modules/@fontsource/inter/files/inter-latin-400-normal.woff'
  )
  const fontData: ArrayBuffer = readFileSync(fontPath).buffer as ArrayBuffer

  const svg = satori(
    {
      type: 'div',
      props: {
        style: {
          width: '1200px',
          height: '630px',
          background: 'linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'Inter, sans-serif',
          position: 'relative',
          padding: '60px',
        },
        children: [
          // Subtle dot grid overlay
          {
            type: 'div',
            props: {
              style: {
                position: 'absolute',
                top: 0, left: 0, right: 0, bottom: 0,
                backgroundImage: 'radial-gradient(circle, #ffffff08 1px, transparent 1px)',
                backgroundSize: '40px 40px',
              },
            },
          },

          // Top badge pill — edit label to match your project type
          {
            type: 'div',
            props: {
              style: {
                background: '#21262d',
                border: '1px solid #30363d',
                borderRadius: '20px',
                padding: '6px 16px',
                color: '#e6edf3',
                fontSize: '14px',
                letterSpacing: '0.08em',
                fontWeight: 600,
                marginBottom: '24px',
              },
              children: 'FREE & OPEN SOURCE', // edit this
            },
          },

          // Title block — two lines, first white, second orange
          {
            type: 'div',
            props: {
              style: { display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '12px' },
              children: [
                {
                  type: 'span',
                  props: {
                    style: { fontSize: '72px', fontWeight: 800, color: '#e6edf3', lineHeight: 1.1 },
                    children: 'Your Project',  // edit this
                  },
                },
                {
                  type: 'span',
                  props: {
                    style: { fontSize: '72px', fontWeight: 800, color: '#f0883e', lineHeight: 1.1 },
                    children: 'Name Here',     // edit this
                  },
                },
              ],
            },
          },

          // Subtitle
          {
            type: 'div',
            props: {
              style: { fontSize: '20px', color: '#8b949e', marginBottom: '40px', textAlign: 'center' },
              children: 'Your project tagline goes here',  // edit this
            },
          },

          // Stats row
          {
            type: 'div',
            props: {
              style: { display: 'flex', gap: '16px', marginBottom: '40px' },
              children: stats.map(s => statCard(s.value, s.label)),
            },
          },

          // Author signature — bottom left
          // Remove this block if you don't want it
          {
            type: 'div',
            props: {
              style: {
                position: 'absolute',
                bottom: '36px',
                left: '48px',
                display: 'flex',
                alignItems: 'center',
                gap: '14px',
              },
              children: [
                {
                  type: 'span',
                  props: {
                    style: { fontSize: '28px', fontWeight: 800, color: '#c0522a', letterSpacing: '-0.02em' },
                    children: 'FB.',  // your initials
                  },
                },
                {
                  type: 'span',
                  props: {
                    style: { fontSize: '16px', color: '#8b949e', fontWeight: 400 },
                    children: 'your-domain.com',  // your domain
                  },
                },
              ],
            },
          },
        ],
      },
    },
    {
      width: 1200,
      height: 630,
      fonts: [{ name: 'Inter', data: fontData, weight: 400, style: 'normal' }],
    }
  )

  const resvg = new Resvg(svg as unknown as string, { fitTo: { mode: 'width', value: 1200 } })
  const png = resvg.render().asPng()

  return new Response(png.buffer as ArrayBuffer, {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=86400',
    },
  })
}
