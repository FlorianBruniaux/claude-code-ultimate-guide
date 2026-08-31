import { createHash } from 'node:crypto'
import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { parse as parseYaml } from 'yaml'
import { collectRuntimeSnapshot } from './runtime-snapshot.mjs'
import { countReferenceEntries } from '../dist/product-metrics.js'

const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const manifestPath = resolve(guideRoot, 'machine-readable/mcp-product.json')

/** @typedef {{
 * schema_version: 1,
 * package: { name: string, version: string, registry_name: string, mcp_registry_name: string, node_engine: string, dependencies: { model_context_protocol_sdk: string } },
 * guide: { version: string, line_count: number, index_entries: number, claude_code_releases: number },
 * runtime: {
 *   tools: Array<{name: string, description: string, input_schema: object, annotations?: object}>,
 *   resources: Array<{name: string, uri: string, description: string, mime_type: string}>,
 *   prompts: Array<{name: string, description: string, arguments: object[]}>
 * },
 * companions: { slash_commands: string[] },
 * security: { audit_as_of: string, production_vulnerabilities: number, development_only_vulnerabilities: { low: number, packages: string[] } },
 * source_digest: `sha256:${string}`
 * }} ProductManifestV1 */

function sortByName(values) { return [...values].sort((left, right) => left.name.localeCompare(right.name)) }

function sourcePaths() {
  const commands = readdirSync(resolve(guideRoot, '.claude/commands/ccguide'))
    .filter((name) => name.endsWith('.md'))
    .map((name) => `.claude/commands/ccguide/${name}`)
  const tools = readdirSync(resolve(packageRoot, 'src/tools'))
    .filter((name) => name.endsWith('.ts'))
    .map((name) => `mcp-server/src/tools/${name}`)
  return [
    'VERSION', 'guide/ultimate-guide.md', 'machine-readable/reference.yaml',
    'machine-readable/claude-code-releases.yaml', 'mcp-server/package-lock.json', 'mcp-server/package.json',
    'mcp-server/src/server.ts', 'mcp-server/src/resources/index.ts', 'mcp-server/src/prompts/index.ts',
    ...commands, ...tools,
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
  const packageLock = JSON.parse(readFileSync(resolve(packageRoot, 'package-lock.json'), 'utf8'))
  const reference = parseYaml(readFileSync(resolve(guideRoot, 'machine-readable/reference.yaml'), 'utf8'))
  const releases = parseYaml(readFileSync(resolve(guideRoot, 'machine-readable/claude-code-releases.yaml'), 'utf8'))
  const runtime = await collectRuntimeSnapshot({ command: process.execPath, args: [resolve(packageRoot, 'dist/index.js')], cwd: packageRoot })
  const sdk = packageLock.packages['node_modules/@modelcontextprotocol/sdk']
  if (!sdk?.version) throw new Error('@modelcontextprotocol/sdk is missing from package-lock.json')
  const releaseAudit = packageJson.releaseAudit
  if (!releaseAudit) throw new Error('releaseAudit is missing from package.json')
  return {
    schema_version: 1,
    package: {
      name: runtime.serverInfo.name,
      version: runtime.serverInfo.version,
      registry_name: packageJson.name,
      mcp_registry_name: packageJson.mcpName,
      node_engine: packageJson.engines.node,
      dependencies: { model_context_protocol_sdk: sdk.version },
    },
    guide: { version: readFileSync(resolve(guideRoot, 'VERSION'), 'utf8').trim(), line_count: lineCount(resolve(guideRoot, 'guide/ultimate-guide.md')), index_entries: countReferenceEntries(reference), claude_code_releases: (releases.releases ?? []).length },
    runtime: {
      tools: sortByName(runtime.tools).map(({ name, description, inputSchema, annotations }) => ({ name, description, input_schema: inputSchema, ...(annotations === undefined ? {} : { annotations }) })),
      resources: sortByName(runtime.resources).map(({ name, uri, description, mimeType }) => ({ name, uri, description, mime_type: mimeType })),
      prompts: sortByName(runtime.prompts).map(({ name, description, arguments: args }) => ({ name, description, arguments: args ?? [] })),
    },
    companions: { slash_commands: sourcePaths().filter((path) => path.startsWith('.claude/commands/')).map((path) => path.split('/').pop().replace(/\.md$/, '')).sort() },
    security: {
      audit_as_of: releaseAudit.asOf,
      production_vulnerabilities: releaseAudit.productionVulnerabilities,
      development_only_vulnerabilities: releaseAudit.developmentOnlyVulnerabilities,
    },
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
