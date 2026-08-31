import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const packageName = 'claude-code-ultimate-guide-mcp'
const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const defaultOutput = resolve(guideRoot, 'machine-readable/mcp-public-runtime.json')
const semver = /^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/
const strictUtcTimestamp = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/

function option(name) {
  const index = process.argv.indexOf(name)
  if (index === -1) return undefined
  const value = process.argv[index + 1]
  if (value === undefined || value.startsWith('--')) throw new Error(`${name} requires a value`)
  return value
}

function validateVersion(value, label) {
  if (typeof value !== 'string' || !semver.test(value)) {
    throw new Error(`${label} must be a valid semantic version`)
  }
  return value
}

function validateSnapshotAt(value) {
  const parsed = new Date(value)
  const canonical = Number.isNaN(parsed.getTime()) ? undefined : parsed.toISOString().replace('.000Z', 'Z')
  if (!strictUtcTimestamp.test(value) || canonical !== value) {
    throw new Error('--snapshot-at must use YYYY-MM-DDTHH:mm:ssZ with a valid UTC date')
  }
  return value
}

function readFixture(path) {
  const fixture = JSON.parse(readFileSync(resolve(path), 'utf8'))
  validateVersion(fixture.npm_version, 'fixture npm_version')
  if (typeof fixture.command !== 'string' || fixture.command === '') throw new Error('fixture command must be a non-empty string')
  if (!Array.isArray(fixture.args) || fixture.args.some((value) => typeof value !== 'string')) {
    throw new Error('fixture args must be an array of strings')
  }
  if (fixture.cwd !== undefined && (typeof fixture.cwd !== 'string' || fixture.cwd === '')) {
    throw new Error('fixture cwd must be a non-empty string when provided')
  }
  return {
    npmVersion: fixture.npm_version,
    command: fixture.command,
    args: fixture.args,
    cwd: fixture.cwd === undefined ? packageRoot : resolve(fixture.cwd),
  }
}

function publicPackageRuntime() {
  let rawVersion
  try {
    rawVersion = execFileSync('npm', ['view', packageName, 'version', '--json'], {
      cwd: packageRoot,
      encoding: 'utf8',
      timeout: 30_000,
      maxBuffer: 1024 * 1024,
    })
  } catch (error) {
    if (error?.code === 'ETIMEDOUT' || error?.signal === 'SIGTERM') {
      throw new Error('npm view timed out after 30 seconds; check registry connectivity and retry')
    }
    const detail = String(error?.stderr ?? error?.message ?? error).trim().split('\n').at(-1)
    throw new Error(`npm view failed${detail ? `: ${detail}` : ''}`)
  }
  const npmVersion = validateVersion(JSON.parse(rawVersion), 'published npm version')
  return {
    npmVersion,
    command: process.platform === 'win32' ? 'npx.cmd' : 'npx',
    args: ['--yes', `${packageName}@${npmVersion}`],
    cwd: guideRoot,
  }
}

function capabilityNames(values, label) {
  const names = values.map(({ name }) => name)
  if (names.some((name) => typeof name !== 'string' || name === '')) throw new Error(`${label} contains an invalid name`)
  const duplicates = [...new Set(names.filter((name, index) => names.indexOf(name) !== index))].sort()
  if (duplicates.length > 0) throw new Error(`${label} contains duplicate names: ${duplicates.join(', ')}`)
  return names.sort((left, right) => left.localeCompare(right))
}

async function collectPages({ method, resultKey, request }) {
  const values = []
  const seenCursors = new Set()
  let cursor
  while (true) {
    let page
    try {
      page = await request(cursor === undefined ? undefined : { cursor })
    } catch {
      throw new Error(`${method} returned an invalid response`)
    }
    if (!Array.isArray(page?.[resultKey])) throw new Error(`${method} returned an invalid response`)
    values.push(...page[resultKey])
    const nextCursor = page.nextCursor
    if (nextCursor === undefined) return values
    if (typeof nextCursor !== 'string' || nextCursor === '') throw new Error(`${method} returned an invalid nextCursor`)
    if (seenCursors.has(nextCursor)) throw new Error(`${method} pagination cycle detected at cursor "${nextCursor}"`)
    seenCursors.add(nextCursor)
    cursor = nextCursor
  }
}

async function collectRuntimeSnapshot({ command, args, cwd }) {
  const transport = new StdioClientTransport({ command, args, cwd, stderr: 'pipe' })
  const client = new Client({ name: 'claude-code-guide-public-runtime-snapshot', version: '1' })
  try {
    await client.connect(transport)
    const serverInfo = client.getServerVersion()
    if (serverInfo === undefined) throw new Error('MCP server did not return serverInfo')
    const capabilities = client.getServerCapabilities()
    if (capabilities === undefined) throw new Error('MCP server did not return capabilities')
    for (const capability of ['tools', 'resources', 'prompts']) {
      if (capabilities[capability] === undefined) throw new Error(`MCP server does not advertise ${capability} capability`)
    }
    const [tools, resources, prompts] = await Promise.all([
      collectPages({ method: 'tools/list', resultKey: 'tools', request: (params) => client.listTools(params) }),
      collectPages({ method: 'resources/list', resultKey: 'resources', request: (params) => client.listResources(params) }),
      collectPages({ method: 'prompts/list', resultKey: 'prompts', request: (params) => client.listPrompts(params) }),
    ])
    return { serverInfo, tools, resources, prompts }
  } finally {
    await client.close()
  }
}

async function main() {
  const fixturePath = option('--fixture')
  const outputOption = option('--output')
  if (fixturePath !== undefined && outputOption === undefined) throw new Error('--output is required with --fixture')
  const outputPath = resolve(outputOption ?? defaultOutput)
  if (fixturePath !== undefined && outputPath === defaultOutput) {
    throw new Error('--fixture cannot write the canonical public runtime snapshot')
  }
  const snapshotAt = validateSnapshotAt(option('--snapshot-at') ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'))
  const runtimeCommand = fixturePath === undefined ? publicPackageRuntime() : readFixture(fixturePath)
  const runtime = await collectRuntimeSnapshot(runtimeCommand)
  const tools = capabilityNames(runtime.tools, 'tools')
  const resources = capabilityNames(runtime.resources, 'resources')
  const prompts = capabilityNames(runtime.prompts, 'prompts')
  const serverName = runtime.serverInfo.name
  const serverVersion = runtime.serverInfo.version
  if (typeof serverName !== 'string' || serverName === '') throw new Error('MCP server did not return a valid name')
  validateVersion(serverVersion, 'MCP server version')

  const snapshot = {
    schema_version: 1,
    snapshot_at: snapshotAt,
    package: { name: packageName, npm_version: runtimeCommand.npmVersion },
    server_info: { name: serverName, version: serverVersion },
    capabilities: { tools, resources, prompts },
    counts: { tools: tools.length, resources: resources.length, prompts: prompts.length },
  }
  writeFileSync(outputPath, `${JSON.stringify(snapshot, null, 2)}\n`)
}

try {
  await main()
} catch (error) {
  console.error(`generate-public-runtime-snapshot: ${error instanceof Error ? error.message : String(error)}`)
  process.exitCode = 1
}
