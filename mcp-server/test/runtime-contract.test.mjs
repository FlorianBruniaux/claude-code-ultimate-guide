import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import test from 'node:test'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const root = resolve(import.meta.dirname, '..')
const guideRoot = resolve(root, '..')
const manifest = JSON.parse(readFileSync(resolve(guideRoot, 'machine-readable/mcp-product.json'), 'utf8'))
const expectedUris = JSON.parse(readFileSync(resolve(import.meta.dirname, 'fixtures/expected-resource-uris.json'), 'utf8'))

async function withRuntime(run, { command = process.execPath, args = [resolve(root, 'dist/index.js')], cwd = root, env } = {}) {
  const transport = new StdioClientTransport({ command, args, cwd, env, stderr: 'pipe' })
  const client = new Client({ name: 'runtime-contract-test', version: '1' })
  try {
    await client.connect(transport)
    return await run(client)
  } finally {
    await client.close()
  }
}

test('JSON-RPC runtime exactly matches the generated manifest', async () => {
  await withRuntime(async (client) => {
    const [tools, resources, prompts] = await Promise.all([client.listTools(), client.listResources(), client.listPrompts()])
    assert.deepEqual(tools.tools.map(({ name, description, inputSchema, annotations }) => ({ name, description, input_schema: inputSchema, ...(annotations === undefined ? {} : { annotations }) })).sort((a, b) => a.name.localeCompare(b.name)), manifest.runtime.tools)
    assert.deepEqual(resources.resources.map(({ name, uri, description, mimeType }) => ({ name, uri, description, mime_type: mimeType })).sort((a, b) => a.name.localeCompare(b.name)), manifest.runtime.resources)
    assert.deepEqual(prompts.prompts.map(({ name, description, arguments: args }) => ({ name, description, arguments: args ?? [] })).sort((a, b) => a.name.localeCompare(b.name)), manifest.runtime.prompts)
    assert.deepEqual(resources.resources.map(({ uri }) => uri).sort(), expectedUris)
    for (const resource of resources.resources) {
      const result = await client.readResource({ uri: resource.uri })
      assert.ok(result.contents[0].text.length > 0)
      assert.equal(result.contents[0].mimeType, resource.mimeType)
      if (resource.uri === 'claude-code-guide://translations') JSON.parse(result.contents[0].text)
    }
  })
})

test('offline list operations use only bundled data', async () => {
  await withRuntime(async (client) => {
    assert.equal((await client.listTools()).tools.length, 17)
    assert.equal((await client.listResources()).resources.length, 6)
    assert.equal((await client.listPrompts()).prompts.length, 1)
  }, { env: { ...process.env, HTTPS_PROXY: 'http://127.0.0.1:9', HTTP_PROXY: 'http://127.0.0.1:9', NO_PROXY: '' } })
})
