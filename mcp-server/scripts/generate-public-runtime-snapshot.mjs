import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { collectRuntimeSnapshot } from './runtime-snapshot.mjs'

const packageName = 'claude-code-ultimate-guide-mcp'
const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const defaultOutput = resolve(guideRoot, 'machine-readable/mcp-public-runtime.json')

function option(name) {
  const index = process.argv.indexOf(name)
  if (index === -1) return undefined
  const value = process.argv[index + 1]
  if (value === undefined || value.startsWith('--')) throw new Error(`${name} requires a value`)
  return value
}

function validateVersion(value, label) {
  if (typeof value !== 'string' || !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(value)) {
    throw new Error(`${label} must be a semantic version`)
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
  return {
    npmVersion: fixture.npm_version,
    command: fixture.command,
    args: fixture.args,
    cwd: fixture.cwd === undefined ? packageRoot : resolve(fixture.cwd),
  }
}

function publicPackageRuntime() {
  const rawVersion = execFileSync('npm', ['view', packageName, 'version', '--json'], {
    cwd: packageRoot,
    encoding: 'utf8',
  })
  const npmVersion = validateVersion(JSON.parse(rawVersion), 'published npm version')
  return {
    npmVersion,
    command: process.platform === 'win32' ? 'npx.cmd' : 'npx',
    args: ['--yes', `${packageName}@${npmVersion}`],
    cwd: packageRoot,
  }
}

function capabilityNames(values, label) {
  const names = values.map(({ name }) => name)
  if (names.some((name) => typeof name !== 'string' || name === '')) throw new Error(`${label} contains an invalid name`)
  if (new Set(names).size !== names.length) throw new Error(`${label} contains duplicate names`)
  return names.sort((left, right) => left.localeCompare(right))
}

function snapshotAt() {
  const value = option('--snapshot-at') ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z')
  if (Number.isNaN(Date.parse(value)) || !value.endsWith('Z')) throw new Error('--snapshot-at must be an ISO 8601 UTC timestamp')
  return value
}

const fixturePath = option('--fixture')
const runtimeCommand = fixturePath === undefined ? publicPackageRuntime() : readFixture(fixturePath)
const runtime = await collectRuntimeSnapshot({
  command: runtimeCommand.command,
  args: runtimeCommand.args,
  cwd: runtimeCommand.cwd,
})
const tools = capabilityNames(runtime.tools, 'tools')
const resources = capabilityNames(runtime.resources, 'resources')
const prompts = capabilityNames(runtime.prompts, 'prompts')
const serverName = runtime.serverInfo.name
const serverVersion = runtime.serverInfo.version
if (typeof serverName !== 'string' || serverName === '') throw new Error('MCP server did not return a valid name')
validateVersion(serverVersion, 'MCP server version')

const snapshot = {
  schema_version: 1,
  snapshot_at: snapshotAt(),
  package: {
    name: packageName,
    npm_version: runtimeCommand.npmVersion,
  },
  server_info: {
    name: serverName,
    version: serverVersion,
  },
  capabilities: { tools, resources, prompts },
  counts: {
    tools: tools.length,
    resources: resources.length,
    prompts: prompts.length,
  },
}

writeFileSync(resolve(option('--output') ?? defaultOutput), `${JSON.stringify(snapshot, null, 2)}\n`)
