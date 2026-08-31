import { readFileSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const packagePath = resolve(packageRoot, 'package.json')
const serverPath = resolve(packageRoot, 'server.json')

function requireNonEmptyString(value, field) {
  if (typeof value !== 'string' || value.trim() === '') throw new Error(`${field} must be a non-empty string`)
  return value
}

export function buildRegistryMetadata(packageJson) {
  const name = requireNonEmptyString(packageJson.name, 'package.json name')
  const version = requireNonEmptyString(packageJson.version, 'package.json version')
  const mcpName = requireNonEmptyString(packageJson.mcpName, 'package.json mcpName')

  return {
    $schema: 'https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json',
    name: mcpName,
    title: 'Claude Code Ultimate Guide',
    description: 'Search the Claude Code Ultimate Guide and machine-readable references from any MCP client.',
    repository: {
      url: 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide',
      source: 'github',
    },
    version,
    packages: [
      {
        registryType: 'npm',
        identifier: name,
        version,
        transport: { type: 'stdio' },
      },
    ],
  }
}

export function renderRegistryMetadata(packageJson) {
  return `${JSON.stringify(buildRegistryMetadata(packageJson), null, 2)}\n`
}

export function renderRegistryMetadataFile({ check = false } = {}) {
  const packageJson = JSON.parse(readFileSync(packagePath, 'utf8'))
  const output = renderRegistryMetadata(packageJson)
  if (check) {
    const current = readFileSync(serverPath, 'utf8')
    if (current !== output) {
      const index = [...current].findIndex((character, offset) => character !== output[offset])
      throw new Error(`server.json is stale at byte ${index < 0 ? Math.min(current.length, output.length) : index}`)
    }
    return
  }
  writeFileSync(serverPath, output, 'utf8')
}

function runCli() {
  const args = process.argv.slice(2)
  if (args.length > 1 || (args.length === 1 && args[0] !== '--check')) {
    throw new Error('usage: node scripts/render-registry-metadata.mjs [--check]')
  }
  renderRegistryMetadataFile({ check: args[0] === '--check' })
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    runCli()
  } catch (error) {
    console.error(`${basename(process.argv[1])}: ${error instanceof Error ? error.message : String(error)}`)
    process.exitCode = 1
  }
}
