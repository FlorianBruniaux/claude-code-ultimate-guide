import assert from 'node:assert/strict'
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import test from 'node:test'

const packageRoot = resolve(import.meta.dirname, '..')
const generator = resolve(packageRoot, 'scripts/generate-public-runtime-snapshot.mjs')

const fixtureServerSource = String.raw`
import { createInterface } from 'node:readline'

const replies = {
  initialize: {
    protocolVersion: '2025-11-25',
    capabilities: { tools: {}, resources: {}, prompts: {} },
    serverInfo: { name: 'fixture-public-server', version: '1.2.0' },
  },
  'tools/list': {
    tools: [
      { name: 'zeta_tool', description: 'must not leave the process', inputSchema: { type: 'object' } },
      { name: 'alpha_tool', description: 'must not leave the process', inputSchema: { type: 'object' } },
    ],
  },
  'resources/list': {
    resources: [
      { name: 'Private path', uri: 'file:///Users/example/private.txt', description: 'must not leave the process' },
      { name: 'Guide', uri: 'claude-code-guide://guide', description: 'must not leave the process' },
    ],
  },
  'prompts/list': {
    prompts: [
      { name: 'guide_me', description: 'must not leave the process', arguments: [{ name: 'secret' }] },
    ],
  },
}

const lines = createInterface({ input: process.stdin })
lines.on('close', () => process.exit(0))
lines.on('line', (line) => {
  const message = JSON.parse(line)
  if (message.id === undefined) return
  const result = replies[message.method]
  if (result === undefined) {
    process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: message.id, error: { code: -32601, message: 'Method not found' } }) + '\n')
    return
  }
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id: message.id, result }) + '\n')
})
`

test('writes a sorted, sanitized public runtime snapshot from the MCP list contract', () => {
  const temporary = mkdtempSync(resolve(tmpdir(), 'mcp-public-runtime-'))
  try {
    const serverPath = resolve(temporary, 'fixture-server.mjs')
    const fixturePath = resolve(temporary, 'fixture.json')
    const outputPath = resolve(temporary, 'snapshot.json')
    writeFileSync(serverPath, fixtureServerSource)
    writeFileSync(fixturePath, JSON.stringify({
      npm_version: '1.2.10',
      command: process.execPath,
      args: [serverPath],
    }))

    const result = spawnSync(process.execPath, [
      generator,
      '--fixture', fixturePath,
      '--snapshot-at', '2026-08-31T16:00:00Z',
      '--output', outputPath,
    ], { cwd: packageRoot, encoding: 'utf8' })

    assert.equal(result.status, 0, result.stderr)
    assert.deepEqual(JSON.parse(readFileSync(outputPath, 'utf8')), {
      schema_version: 1,
      snapshot_at: '2026-08-31T16:00:00Z',
      package: {
        name: 'claude-code-ultimate-guide-mcp',
        npm_version: '1.2.10',
      },
      server_info: {
        name: 'fixture-public-server',
        version: '1.2.0',
      },
      capabilities: {
        tools: ['alpha_tool', 'zeta_tool'],
        resources: ['Guide', 'Private path'],
        prompts: ['guide_me'],
      },
      counts: {
        tools: 2,
        resources: 2,
        prompts: 1,
      },
    })
  } finally {
    rmSync(temporary, { recursive: true, force: true })
  }
})
