import { createHash } from 'node:crypto'
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const slugs = ['00-introduction', '01-quick-start', '02-core-workflow', '03-memory-files', '04-agents', '05-skills', '06-commands', '07-hooks', '08-mcp', '09-advanced-patterns', '10-reference', '11-ai-ecosystem', '12-appendices']
const hash = text => createHash('sha256').update(text).digest('hex')

// Match the landing's fence-aware H2 splitter; retain original file line offsets.
export function generateChapterRanges(source, reference) {
  const text = source.replace(/\r\n/g, '\n')
  let body = text
  const fmEnd = text.indexOf('\n---', 3)
  if (text.startsWith('---') && fmEnd !== -1) body = text.slice(fmEnd + 4).trimStart()
  const skippedLines = text.slice(0, text.length - body.length).split('\n').length - 1
  const lines = text.split('\n')
  let chapter = 0
  let fence = ''
  const ranges = [{ from: 1, to: lines.length, slug: slugs[0] }]
  for (let index = skippedLines; index < lines.length; index++) {
    const line = lines[index]
    const trim = line.trim()
    const marker = trim.match(/^(`{3,}|~{3,})/)
    if (marker) {
      if (!fence) fence = marker[1]
      else if (marker[1][0] === fence[0] && marker[1].length >= fence.length && /^[`~]+$/.test(trim)) fence = ''
    }
    if (fence) continue
    let next = null
    const numbered = line.match(/^## (\d+)\./)
    const summary = line.match(/^## 📌 Section (\d+)/)
    if (numbered) next = Number(numbered[1])
    else if (summary) next = Number(summary[1])
    else if (chapter >= 9 && /^## [A-G]\.\d+/.test(line)) next = 10
    else if (/^## Appendix [A-Z]:/.test(line) || /^## About\b/.test(line)) next = 12
    if (next !== null && slugs[next] && next !== chapter) {
      ranges.at(-1).to = index
      ranges.push({ from: index + 1, to: lines.length, slug: slugs[next] })
      chapter = next
    }
  }
  return { sourceSha256: hash(source), referenceSha256: hash(reference), lineCount: lines.length, ranges }
}

function main() {
  const packageRoot = fileURLToPath(new URL('..', import.meta.url))
  const options = { guide: resolve(packageRoot, '../guide/ultimate-guide.md'), reference: resolve(packageRoot, 'content/reference.yaml'), output: resolve(packageRoot, 'src/lib/chapter-ranges.generated.json') }
  let check = false
  const args = process.argv.slice(2)
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--check') check = true
    else {
      const key = args[i].slice(2)
      if (!args[i].startsWith('--') || !(key in options) || !args[i + 1]) throw new Error('Expected --guide, --reference, --output or --check')
      options[key] = resolve(args[++i])
    }
  }
  const generated = JSON.stringify(generateChapterRanges(readFileSync(options.guide, 'utf8'), readFileSync(options.reference, 'utf8')), null, 2) + '\n'
  if (check) {
    if (readFileSync(options.output, 'utf8') !== generated) throw new Error('Chapter ranges are stale; regenerate from the current guide and bundled reference')
  } else writeFileSync(options.output, generated)
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main() } catch (error) { console.error(error.message); process.exitCode = 1 }
}
