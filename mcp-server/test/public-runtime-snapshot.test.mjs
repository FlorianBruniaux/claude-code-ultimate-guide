import assert from 'node:assert/strict'
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import test from 'node:test'

const packageRoot = resolve(import.meta.dirname, '..')
const guideRoot = resolve(packageRoot, '..')
const generator = resolve(packageRoot, 'scripts/generate-public-runtime-snapshot.mjs')
const canonicalOutput = resolve(guideRoot, 'machine-readable/mcp-public-runtime.json')

test('public collection runs the exact npm package outside its source directory', () => {
  const source = readFileSync(generator, 'utf8')
  assert.match(source, /args: \['--yes', `\$\{packageName\}@\$\{npmVersion\}`\]/)
  assert.match(source, /cwd: guideRoot/)
})

const fixtureServerSource = String.raw`
import { readFileSync } from 'node:fs'
import { createInterface } from 'node:readline'

const scenario = JSON.parse(readFileSync(process.argv[2], 'utf8'))
const lines = createInterface({ input: process.stdin })
lines.on('close', () => process.exit(0))
lines.on('line', (line) => {
  const message = JSON.parse(line)
  if (message.id === undefined) return
  let result
  if (message.method === 'initialize') {
    result = scenario.initialize
  } else {
    const cursor = message.params?.cursor ?? '__first__'
    result = scenario.pages?.[message.method]?.[cursor]
  }
  if (result === undefined) {
    process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: message.id, error: { code: -32601, message: 'Fixture response not found' } }) + '\n')
    return
  }
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: message.id, result }) + '\n')
})
`

function baseScenario() {
  return {
    initialize: {
      protocolVersion: '2025-11-25',
      capabilities: { tools: {}, resources: {}, prompts: {} },
      serverInfo: { name: 'fixture-public-server', version: '1.2.0-rc.1+server.5' },
    },
    pages: {
      'tools/list': {
        __first__: {
          tools: [{ name: 'zeta_tool', description: 'must not leave the process', inputSchema: { type: 'object' } }],
          nextCursor: 'tools-page-2',
        },
        'tools-page-2': {
          tools: [{ name: 'alpha_tool', description: 'must not leave the process', inputSchema: { type: 'object' } }],
        },
      },
      'resources/list': {
        __first__: {
          resources: [{ name: 'Private path', uri: 'file:///Users/example/private.txt', description: 'must not leave the process' }],
          nextCursor: 'resources-page-2',
        },
        'resources-page-2': {
          resources: [{ name: 'Guide', uri: 'claude-code-guide://guide', description: 'must not leave the process' }],
        },
      },
      'prompts/list': {
        __first__: {
          prompts: [{ name: 'guide_me', description: 'must not leave the process', arguments: [{ name: 'secret' }] }],
          nextCursor: 'prompts-page-2',
        },
        'prompts-page-2': {
          prompts: [{ name: 'troubleshoot', description: 'must not leave the process', arguments: [] }],
        },
      },
    },
  }
}

function runFixture({ scenario = baseScenario(), npmVersion = '1.2.10-beta.2+build.7', snapshotAt = '2026-08-31T16:00:00Z', includeOutput = true, outputPath } = {}) {
  const temporary = mkdtempSync(resolve(tmpdir(), 'mcp-public-runtime-'))
  try {
    const serverPath = resolve(temporary, 'fixture-server.mjs')
    const scenarioPath = resolve(temporary, 'scenario.json')
    const fixturePath = resolve(temporary, 'fixture.json')
    const resolvedOutput = outputPath ?? resolve(temporary, 'snapshot.json')
    writeFileSync(serverPath, fixtureServerSource)
    writeFileSync(scenarioPath, JSON.stringify(scenario))
    writeFileSync(fixturePath, JSON.stringify({
      npm_version: npmVersion,
      command: process.execPath,
      args: [serverPath, scenarioPath],
    }))
    const args = [generator, '--fixture', fixturePath, '--snapshot-at', snapshotAt]
    if (includeOutput) args.push('--output', resolvedOutput)
    const result = spawnSync(process.execPath, args, { cwd: packageRoot, encoding: 'utf8' })
    return {
      ...result,
      snapshot: existsSync(resolvedOutput) ? JSON.parse(readFileSync(resolvedOutput, 'utf8')) : undefined,
    }
  } finally {
    rmSync(temporary, { recursive: true, force: true })
  }
}

test('collects every MCP pagination page and writes only sorted public names', () => {
  const result = runFixture()
  assert.equal(result.status, 0, result.stderr)
  assert.deepEqual(result.snapshot, {
    schema_version: 1,
    snapshot_at: '2026-08-31T16:00:00Z',
    package: {
      name: 'claude-code-ultimate-guide-mcp',
      npm_version: '1.2.10-beta.2+build.7',
    },
    server_info: {
      name: 'fixture-public-server',
      version: '1.2.0-rc.1+server.5',
    },
    capabilities: {
      tools: ['alpha_tool', 'zeta_tool'],
      resources: ['Guide', 'Private path'],
      prompts: ['guide_me', 'troubleshoot'],
    },
    counts: { tools: 2, resources: 2, prompts: 2 },
  })
})

test('fails when an MCP pagination cursor repeats', () => {
  const scenario = baseScenario()
  scenario.pages['tools/list']['tools-page-2'].nextCursor = 'tools-page-2'
  const result = runFixture({ scenario })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /tools\/list pagination cycle detected at cursor "tools-page-2"/)
})

test('fails when capability names are duplicated across pages', () => {
  const scenario = baseScenario()
  scenario.pages['tools/list']['tools-page-2'].tools[0].name = 'zeta_tool'
  const result = runFixture({ scenario })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /tools contains duplicate names: zeta_tool/)
})

test('fails explicitly when a paginated response is incomplete', () => {
  const scenario = baseScenario()
  delete scenario.pages['resources/list']['resources-page-2'].resources
  const result = runFixture({ scenario })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /resources\/list returned an invalid response/)
})

test('fails when the server does not advertise a capability that will be listed', () => {
  const scenario = baseScenario()
  delete scenario.initialize.capabilities.prompts
  const result = runFixture({ scenario })
  assert.equal(result.status, 1)
  assert.match(result.stderr, /MCP server does not advertise prompts capability/)
})

test('fixture mode requires a non-canonical output path', () => {
  const missing = runFixture({ includeOutput: false })
  assert.equal(missing.status, 1)
  assert.match(missing.stderr, /--output is required with --fixture/)

  const canonicalBefore = readFileSync(canonicalOutput, 'utf8')
  const canonical = runFixture({ outputPath: canonicalOutput })
  assert.equal(canonical.status, 1)
  assert.match(canonical.stderr, /--fixture cannot write the canonical public runtime snapshot/)
  assert.equal(readFileSync(canonicalOutput, 'utf8'), canonicalBefore)
})

test('accepts SemVer prerelease and build identifiers but rejects invalid versions', () => {
  const invalidNpm = runFixture({ npmVersion: '01.2.3' })
  assert.equal(invalidNpm.status, 1)
  assert.match(invalidNpm.stderr, /fixture npm_version must be a valid semantic version/)

  const scenario = baseScenario()
  scenario.initialize.serverInfo.version = '1.02.3'
  const invalidServer = runFixture({ scenario })
  assert.equal(invalidServer.status, 1)
  assert.match(invalidServer.stderr, /MCP server version must be a valid semantic version/)
})

test('requires a strict, calendar-valid UTC timestamp', async (context) => {
  for (const value of ['2026-02-30T12:00:00Z', '2026-08-31T12:00:00+00:00', '2026-08-31T12:00:00.000Z']) {
    await context.test(value, () => {
      const result = runFixture({ snapshotAt: value })
      assert.equal(result.status, 1)
      assert.match(result.stderr, /--snapshot-at must use YYYY-MM-DDTHH:mm:ssZ with a valid UTC date/)
    })
  }
})
