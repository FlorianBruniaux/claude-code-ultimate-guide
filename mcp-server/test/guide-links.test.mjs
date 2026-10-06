import assert from 'node:assert/strict'
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve, join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { spawnSync } from 'node:child_process'
import test from 'node:test'
import { buildSync } from 'esbuild'

const packageRoot = resolve(import.meta.dirname, '..')
const guideRoot = resolve(packageRoot, '..')
async function withUrls(run) {
  const directory = mkdtempSync(join(tmpdir(), 'guide-links-test-'))
  try {
    buildSync({ entryPoints: [join(packageRoot, 'src/lib/urls.ts')], outfile: join(directory, 'urls.mjs'), bundle: true, platform: 'node', format: 'esm' })
    return await run(await import(pathToFileURL(join(directory, 'urls.mjs')).href), directory)
  } finally { rmSync(directory, { recursive: true, force: true }) }
}

test('the bundled session-scoped hooks reference links to the rendered Hooks chapter', async () => {
  const reference = readFileSync(join(packageRoot, 'content/reference.yaml'), 'utf8')
  const line = Number(reference.match(/^hooks_session_scoped:\s*(\d+)/m)?.[1])
  assert.ok(Number.isInteger(line) && line > 0)
  const heading = readFileSync(join(guideRoot, 'guide/ultimate-guide.md'), 'utf8').split('\n')[line - 1]
  assert.match(heading, /Session-Scoped Hooks/)
  await withUrls(({ guideSiteUrl, formatLinks }) => {
    assert.equal(guideSiteUrl('guide/ultimate-guide.md', line), 'https://cc.bruniaux.com/guide/ultimate-guide/07-hooks/')
    assert.match(formatLinks('guide/ultimate-guide.md', line), /Guide: https:\/\/cc\.bruniaux\.com\/guide\/ultimate-guide\/07-hooks\//)
  })
})

test('real rendered chapter transitions route boundary lines inclusively', async () => {
  // Independent oracle checked against guide 3.44.1 headings and landing splitter rules.
  // Keep these expectations independent of chapter-ranges.generated.json.
  const boundaries = [
    [259, '00-introduction', '01-quick-start'], [1649, '01-quick-start', '02-core-workflow'],
    [4828, '02-core-workflow', '03-memory-files'], [6352, '03-memory-files', '04-agents'],
    [7241, '04-agents', '05-skills'], [8801, '05-skills', '06-commands'],
    [9738, '06-commands', '07-hooks'], [11631, '07-hooks', '08-mcp'],
    [14222, '08-mcp', '09-advanced-patterns'], [23738, '09-advanced-patterns', '10-reference'],
    [25023, '10-reference', '11-ai-ecosystem'], [25688, '11-ai-ecosystem', '12-appendices'],
  ]
  await withUrls(({ guideSiteUrl }) => {
    for (const [start, previous, next] of boundaries) {
      assert.equal(guideSiteUrl('guide/ultimate-guide.md', start - 1), `https://cc.bruniaux.com/guide/ultimate-guide/${previous}/`)
      assert.equal(guideSiteUrl('guide/ultimate-guide.md', start), `https://cc.bruniaux.com/guide/ultimate-guide/${next}/`)
    }
  })
})

test('invalid and outside-snapshot line numbers fall back to the guide root', async () => {
  await withUrls(({ guideSiteUrl, githubUrl }) => {
    for (const line of [0, -1, 1.5, NaN, Infinity, 999999]) {
      assert.equal(guideSiteUrl('guide/ultimate-guide.md', line), 'https://cc.bruniaux.com/guide/ultimate-guide/')
    }
    assert.equal(guideSiteUrl('examples/hooks/example.sh', 12), null)
    assert.equal(githubUrl('examples/hooks/example.sh', 12), 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/hooks/example.sh#L12')
  })
})

test('generation ignores fenced chapter headings, preserves original CRLF offsets and detects drift', () => {
  const directory = mkdtempSync(join(tmpdir(), 'chapter-generator-test-'))
  try {
    const guide = join(directory, 'guide.md')
    const reference = join(directory, 'reference.yaml')
    const output = join(directory, 'chapters.json')
    const source = [
      '---', 'title: fixture', '---', '', '# Introduction', '## 1.1 Start',
      '````md', '## 7.1 fake', '```', '## 8.1 still fake', '````',
      '~~~', '## 11.1 fake', '~~~', '## 📌 Section 7 TL;DR',
      '## 8.1 MCP', '## 9.1 Advanced', '## A.1 Reference',
      '## 11.1 Ecosystem', '## About This Guide', '## 99.1 Unknown chapter',
    ].join('\r\n')
    writeFileSync(guide, source); writeFileSync(reference, 'fixture: 15\n')
    const run = (...flags) => spawnSync(process.execPath, [join(packageRoot, 'scripts/generate-chapter-ranges.mjs'), '--guide', guide, '--reference', reference, '--output', output, ...flags], { encoding: 'utf8' })
    const generated = run()
    assert.equal(generated.status, 0, generated.stderr)
    assert.deepEqual(JSON.parse(readFileSync(output, 'utf8')).ranges, [
      { from: 1, to: 5, slug: '00-introduction' },
      { from: 6, to: 14, slug: '01-quick-start' },
      { from: 15, to: 15, slug: '07-hooks' },
      { from: 16, to: 16, slug: '08-mcp' },
      { from: 17, to: 17, slug: '09-advanced-patterns' },
      { from: 18, to: 18, slug: '10-reference' },
      { from: 19, to: 19, slug: '11-ai-ecosystem' },
      { from: 20, to: 21, slug: '12-appendices' },
    ])
    assert.equal(run('--check').status, 0)
    writeFileSync(guide, source.replace('# Introduction', '# Introduction\r\nextra line'))
    assert.equal(run('--check').status, 1)
    assert.equal(run().status, 0)
    assert.equal(JSON.parse(readFileSync(output, 'utf8')).ranges.find(r => r.slug === '07-hooks').from, 16)
  } finally { rmSync(directory, { recursive: true, force: true }) }
})

test('a modified local guide snapshot falls back instead of trusting bundled line ranges', async () => {
  await withUrls(async (urls, directory) => {
    const local = join(directory, 'local-guide')
    mkdirSync(join(local, 'guide'), { recursive: true }); mkdirSync(join(local, 'machine-readable'))
    writeFileSync(join(local, 'guide/ultimate-guide.md'), '# Different guide\n')
    writeFileSync(join(local, 'machine-readable/reference.yaml'), 'hooks_session_scoped: 1\n')
    const script = 'import {guideSiteUrl} from ' + JSON.stringify(pathToFileURL(join(directory, 'urls.mjs')).href) + '; console.log(guideSiteUrl("guide/ultimate-guide.md",10043))'
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', script], { env: { ...process.env, GUIDE_ROOT: local }, encoding: 'utf8' })
    assert.equal(result.status, 0, result.stderr)
    assert.equal(result.stdout.trim(), 'https://cc.bruniaux.com/guide/ultimate-guide/')
  })
})

test('standalone bundled routing works when filesystem access to any guide is denied', async () => {
  await withUrls(async (urls, directory) => {
    const bundle = join(directory, 'urls.mjs')
    const moduleUrl = 'data:text/javascript;base64,' + Buffer.from(readFileSync(bundle, 'utf8')).toString('base64')
    const script = 'import {guideSiteUrl} from ' + JSON.stringify(moduleUrl) + '; console.log(guideSiteUrl("guide/ultimate-guide.md",10043))'
    const env = { ...process.env }; delete env.GUIDE_ROOT
    const result = spawnSync(process.execPath, ['--permission', '--input-type=module', '-e', script], { env, cwd: directory, encoding: 'utf8' })
    assert.equal(result.status, 0, result.stderr)
    assert.equal(result.stdout.trim(), 'https://cc.bruniaux.com/guide/ultimate-guide/07-hooks/')
  })
})
