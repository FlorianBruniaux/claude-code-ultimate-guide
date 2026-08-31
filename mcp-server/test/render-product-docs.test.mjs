import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'
import test from 'node:test'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const packageRoot = resolve(import.meta.dirname, '..')
const guideRoot = resolve(packageRoot, '..')
const rendererPath = resolve(packageRoot, 'scripts/render-product-docs.mjs')
const manifest = JSON.parse(readFileSync(resolve(guideRoot, 'machine-readable/mcp-product.json'), 'utf8'))
const packageJson = JSON.parse(readFileSync(resolve(packageRoot, 'package.json'), 'utf8'))

const renderedFiles = [
  resolve(packageRoot, 'README.md'),
  resolve(guideRoot, 'README.md'),
  resolve(guideRoot, 'guide/ultimate-guide.md'),
  resolve(guideRoot, 'CHANGELOG.md'),
]

test('owned product surfaces contain no stale manual claims', () => {
  const files = [
    ...renderedFiles,
    resolve(packageRoot, 'src/prompts/index.ts'),
    resolve(packageRoot, 'package.json'),
  ]
  for (const file of files) {
    const source = readFileSync(file, 'utf8')
    assert.doesNotMatch(source, /1,693 indexed entries|900\+ indexed entries|20K\+ lines|26,000\+ line|882 indexed entries|9 tools covering/)
  }
  assert.doesNotMatch(readFileSync(resolve(guideRoot, 'README.md'), 'utf8'), /13 slash commands|13 commands `\/ccguide:/)
})

test('renderer strictly replaces one ordered marker block', async () => {
  const renderer = await import(pathToFileURL(rendererPath).href).catch(() => null)
  assert.ok(renderer, 'render-product-docs.mjs must exist and be importable')

  const start = '<!-- mcp-product:start -->'
  const end = '<!-- mcp-product:end -->'
  assert.equal(
    renderer.replaceGeneratedBlock(`before\n${start}\nold\n${end}\nafter\n`, 'new'),
    `before\n${start}\nnew\n${end}\nafter\n`,
  )
  assert.throws(() => renderer.replaceGeneratedBlock('no markers', 'new'), /exactly one start and end marker/)
  assert.throws(() => renderer.replaceGeneratedBlock(`${end}\n${start}`, 'new'), /start marker must precede end marker/)
  assert.throws(() => renderer.replaceGeneratedBlock(`${start}\n${start}\n${end}`, 'new'), /exactly one start and end marker/)
})

test('rendered product documentation is current and marker-delimited once', () => {
  const check = spawnSync(process.execPath, [rendererPath, '--check'], { cwd: packageRoot, encoding: 'utf8' })
  assert.equal(check.status, 0, `${check.stdout}${check.stderr}`)

  for (const file of renderedFiles) {
    const source = readFileSync(file, 'utf8')
    assert.equal(source.match(/<!-- mcp-product:start -->/g)?.length, 1, `${file} start marker`)
    assert.equal(source.match(/<!-- mcp-product:end -->/g)?.length, 1, `${file} end marker`)
  }
})

test('expert prompt derives changing index and release facts from bundled content', async () => {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [resolve(packageRoot, 'dist/index.js')],
    stderr: 'pipe',
  })
  const client = new Client({ name: 'render-product-docs-test', version: '1' })
  try {
    await client.connect(transport)
    const prompt = await client.getPrompt({ name: 'claude-code-expert', arguments: {} })
    const text = prompt.messages[0].content.text
    assert.match(text, new RegExp(`${manifest.guide.index_entries} indexed entries`))
    assert.match(text, new RegExp(`${manifest.guide.claude_code_releases} tracked releases`))
    assert.match(text, /the complete guide reference/)
    assert.doesNotMatch(text, /\d[\d,]*\+? line reference|Main reference \(\d|20K\+|26,000\+/)
  } finally {
    await client.close()
  }
})

test('release check is the CI package gate', () => {
  assert.equal(
    packageJson.scripts['release:check'],
    'npm ci && npm test && npm run manifest:check && npm run docs:product:check && npm pack --dry-run --json',
  )
  const workflow = readFileSync(resolve(guideRoot, '.github/workflows/index-integrity.yml'), 'utf8')
  assert.match(workflow, /working-directory: mcp-server\s+run: npm run release:check/)
})
