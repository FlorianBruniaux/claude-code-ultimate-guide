import { createHash } from 'node:crypto'
import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { resolve, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { parse as parseYaml } from 'yaml'
import { collectRuntimeSnapshot } from './runtime-snapshot.mjs'
import { countReferenceEntries } from '../dist/product-metrics.js'

const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const manifestPath = resolve(guideRoot, 'machine-readable/mcp-product.json')

function sortByName(values) { return [...values].sort((left, right) => left.name.localeCompare(right.name)) }

function sourcePaths() {
  const commands = readdirSync(resolve(guideRoot, '.claude/commands/ccguide'))
    .filter((name) => name.endsWith('.md'))
    .map((name) => `.claude/commands/ccguide/${name}`)
  return [
    'VERSION', 'guide/ultimate-guide.md', 'machine-readable/reference.yaml',
    'machine-readable/claude-code-releases.yaml', 'mcp-server/package.json',
    'mcp-server/src/server.ts', 'mcp-server/src/resources/index.ts', 'mcp-server/src/prompts/index.ts',
    ...commands,
  ].sort()
}

function sourceDigest() {
  const hash = createHash('sha256')
  for (const path of sourcePaths()) {
    hash.update(path)
    hash.update('\0')
    hash.update(readFileSync(resolve(guideRoot, path)))
  }
  return `sha256:${hash.digest('hex')}`
}

function lineCount(path) {
  const content = readFileSync(path, 'utf8')
  return content === '' ? 0 : content.split('\n').length - (content.endsWith('\n') ? 1 : 0)
}

/** @returns {Promise<ProductManifestV1>} */
async function buildManifest() {
  const packageJson = JSON.parse(readFileSync(resolve(packageRoot, 'package.json'), 'utf8'))
  const reference = parseYaml(readFileSync(resolve(guideRoot, 'machine-readable/reference.yaml'), 'utf8'))
  const releases = parseYaml(readFileSync(resolve(guideRoot, 'machine-readable/claude-code-releases.yaml'), 'utf8'))
  const runtime = await collectRuntimeSnapshot({ command: process.execPath, args: [resolve(packageRoot, 'dist/index.js')], cwd: packageRoot })
  return {
    schema_version: 1,
    package: { name: runtime.serverInfo.name, version: runtime.serverInfo.version, registry_name: packageJson.name },
    guide: { version: readFileSync(resolve(guideRoot, 'VERSION'), 'utf8').trim(), line_count: lineCount(resolve(guideRoot, 'guide/ultimate-guide.md')), index_entries: countReferenceEntries(reference), claude_code_releases: (releases.releases ?? []).length },
    runtime: {
      tools: sortByName(runtime.tools).map(({ name, description, inputSchema, annotations }) => ({ name, description, input_schema: inputSchema, ...(annotations === undefined ? {} : { annotations }) })),
      resources: sortByName(runtime.resources).map(({ name, uri, description, mimeType }) => ({ name, uri, description, mime_type: mimeType })),
      prompts: sortByName(runtime.prompts).map(({ name, description, arguments: args }) => ({ name, description, arguments: args ?? [] })),
    },
    companions: { slash_commands: sourcePaths().filter((path) => path.startsWith('.claude/commands/')).map((path) => path.split('/').pop().replace(/\.md$/, '')).sort() },
    source_digest: sourceDigest(),
  }
}

const output = `${JSON.stringify(await buildManifest(), null, 2)}\n`
if (process.argv.includes('--check')) {
  const current = readFileSync(manifestPath, 'utf8')
  if (current !== output) {
    const index = [...current].findIndex((character, offset) => character !== output[offset])
    throw new Error(`mcp-product.json is stale at byte ${index < 0 ? Math.min(current.length, output.length) : index}`)
  }
} else {
  writeFileSync(manifestPath, output)
}
