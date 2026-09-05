import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'
import { spawn } from 'node:child_process'
import { resolve } from 'node:path'
import test from 'node:test'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const root = resolve(import.meta.dirname, '..')
const packageJson = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8'))
const manifestPath = resolve(root, '..', 'machine-readable', 'mcp-product.json')

async function withClient(run) {
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [resolve(root, 'dist/index.js')],
    stderr: 'pipe',
  })
  const client = new Client({ name: 'product-manifest-test', version: '1' })
  try {
    await client.connect(transport)
    return await run(client)
  } finally {
    await client.close()
  }
}

test('live MCP contract matches the generated product manifest', async () => {
  const runtime = await withClient(async (client) => ({
    serverInfo: client.getServerVersion(),
    tools: (await client.listTools()).tools,
    resources: (await client.listResources()).resources,
    prompts: (await client.listPrompts()).prompts,
  }))

  assert.equal(runtime.serverInfo.version, packageJson.version)
  assert.equal(runtime.tools.length, 17)
  assert.equal(runtime.resources.length, 6)
  assert.equal(runtime.prompts.length, 1)
  assert.ok(runtime.resources.some(({ uri }) => uri === 'claude-code-guide://translations'))
  assert.ok(runtime.resources.some(({ uri }) => uri === 'claude-code-guide://distribution-channels'))
  assert.ok(existsSync(manifestPath), 'machine-readable/mcp-product.json must be generated')
})
