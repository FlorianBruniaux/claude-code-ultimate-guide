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
const canonicalGuidePath = resolve(guideRoot, 'guide/ecosystem/claude-code-guide-mcp.md')

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

  assert.throws(
    () => renderer.buildRenderPlan([
      { path: 'valid.md', source: `${start}\nold\n${end}\n`, generated: 'new' },
      { path: 'invalid.md', source: 'missing markers', generated: 'new' },
    ]),
    /invalid\.md: document must contain exactly one start and end marker/,
  )
})

test('renderer derives the Node badge and dependency security disclosure from manifest facts', async () => {
  const renderer = await import(pathToFileURL(rendererPath).href)
  const fixture = structuredClone(manifest)
  fixture.package.node_engine = '>=18.14.1'
  fixture.package.dependencies = { model_context_protocol_sdk: '1.30.0' }
  fixture.security = {
    audit_as_of: '2026-08-31',
    production_vulnerabilities: 0,
    development_only_vulnerabilities: { low: 1, packages: ['esbuild'] },
  }

  const packageReadme = renderer.renderPackageReadme(fixture, [])
  const changelog = renderer.renderChangelog(fixture)
  assert.match(packageReadme, /!\[Node\.js >=18\.14\.1\]\(https:\/\/img\.shields\.io\/badge\/node-%3E%3D18\.14\.1-brightgreen\)/)
  assert.match(changelog, /@modelcontextprotocol\/sdk 1\.30\.0/)
  assert.match(changelog, /zero production vulnerabilities on 2026-08-31/)
  assert.match(changelog, /one low-severity development-only esbuild advisory remains/)
  assert.match(changelog, /npm trusted-publisher binding remains an external prerequisite/)
  assert.match(changelog, /required reviewer on the `mcp-production` environment remains an external prerequisite/)
  assert.match(changelog, /repository code does not verify either setting/)
  assert.doesNotMatch(changelog, /is protected by the `mcp-production` environment|uses npm trusted publishing/)
  assert.ok(changelog.includes(`\`${fixture.package.mcp_registry_name}\``))
  assert.match(changelog, /monthly npm, GSC, and GA4 dashboard/)
  assert.match(changelog, /missing Google access remains unavailable rather than zero/)
  assert.match(changelog, /canonical technical guide/)
  assert.doesNotMatch(changelog, /zero vulnerabilities overall/)

  fixture.security.production_vulnerabilities = 2
  assert.match(renderer.renderChangelog(fixture), /2 production vulnerabilities on 2026-08-31/)
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

test('renderer rejects the removed bootstrap mode without changing documents', () => {
  const before = renderedFiles.map((file) => readFileSync(file, 'utf8'))
  const result = spawnSync(process.execPath, [rendererPath, '--bootstrap'], { cwd: packageRoot, encoding: 'utf8' })
  assert.notEqual(result.status, 0)
  assert.match(result.stderr, /usage: node scripts\/render-product-docs\.mjs \[--check\]/)
  assert.deepEqual(renderedFiles.map((file) => readFileSync(file, 'utf8')), before)
})

test('every generated network boundary includes digest fetching behavior', () => {
  const packageReadme = readFileSync(renderedFiles[0], 'utf8')
  const rootReadme = readFileSync(renderedFiles[1], 'utf8')
  const guide = readFileSync(renderedFiles[2], 'utf8')
  const boundaries = [
    packageReadme.slice(packageReadme.indexOf('## Local data, network, and cache behavior'), packageReadme.indexOf('## Privacy')),
    rootReadme.match(/The list operations[^\n]+/)?.[0] ?? '',
    guide.slice(guide.indexOf('#### Data and network boundary'), guide.indexOf('See the [package README]')),
  ]
  for (const [index, boundary] of boundaries.entries()) {
    assert.match(boundary, /get_digest/, `${renderedFiles[index]} must identify get_digest as network and cache capable`)
  }
})

test('canonical MCP guide is complete and reachable from every product index', () => {
  const canonicalGuide = readFileSync(canonicalGuidePath, 'utf8')
  const requiredHeadings = [
    '## TL;DR',
    '## What the server solves',
    '## Install by client',
    '## First useful query',
    '## Architecture and data flow',
    '## Tools, resources, and prompt',
    '## Bundled content, GitHub fetch, and cache',
    '## Network and privacy boundary',
    '## Offline behavior',
    '## Compatibility',
    '## Limitations',
    '## Troubleshooting',
    '## Version and dated npm statistics',
    '## Changelog and source',
  ]
  for (const heading of requiredHeadings) {
    assert.match(canonicalGuide, new RegExp(`^${heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'm'))
  }
  assert.match(canonicalGuide, /downloads are not users, active installations, sessions, or executions/i)
  assert.match(canonicalGuide, /no first-party telemetry/i)

  const indexedSurfaces = [
    resolve(guideRoot, 'README.md'),
    resolve(guideRoot, 'guide/README.md'),
    resolve(guideRoot, 'guide/ultimate-guide.md'),
    resolve(guideRoot, 'machine-readable/reference.yaml'),
    resolve(guideRoot, 'llms.txt'),
  ]
  for (const surface of indexedSurfaces) {
    assert.match(readFileSync(surface, 'utf8'), /guide\/ecosystem\/claude-code-guide-mcp\.md|\.\/ecosystem\/claude-code-guide-mcp\.md|\.\/guide\/ecosystem\/claude-code-guide-mcp\.md|ecosystem\/claude-code-guide-mcp\.md/)
  }

  assert.equal(
    readFileSync(resolve(guideRoot, 'machine-readable/reference.yaml'), 'utf8'),
    readFileSync(resolve(packageRoot, 'content/reference.yaml'), 'utf8'),
  )
  const llms = readFileSync(resolve(guideRoot, 'llms.txt'), 'utf8')
  assert.equal(llms, readFileSync(resolve(guideRoot, 'machine-readable/llms.txt'), 'utf8'))
  assert.equal(llms, readFileSync(resolve(packageRoot, 'content/llms.txt'), 'utf8'))
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
    'npm ci && npm test && npm run manifest:check && npm run docs:product:check && npm run registry:metadata:check && npm pack --dry-run --json',
  )
  const workflow = readFileSync(resolve(guideRoot, '.github/workflows/index-integrity.yml'), 'utf8')
  assert.match(workflow, /working-directory: mcp-server\s+run: npm run release:check/)
  const pathLines = workflow.split('\n').map((line) => line.trim())
  for (const path of ['README.md', 'CHANGELOG.md', '.claude/commands/ccguide/**']) {
    assert.equal(pathLines.filter((line) => line === `- "${path}"`).length, 2, `${path} must trigger push and pull request checks`)
  }
})
