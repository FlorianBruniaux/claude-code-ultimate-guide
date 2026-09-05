import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { mkdtemp, rm } from 'node:fs/promises'
import { spawnSync } from 'node:child_process'
import { resolve } from 'node:path'
import { tmpdir } from 'node:os'
import test from 'node:test'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const packageRoot = resolve(import.meta.dirname, '..')
const guideRoot = resolve(packageRoot, '..')
const manifest = JSON.parse(readFileSync(resolve(guideRoot, 'machine-readable/mcp-product.json'), 'utf8'))
const packageJson = JSON.parse(readFileSync(resolve(packageRoot, 'package.json'), 'utf8'))
const [binaryName] = Object.keys(packageJson.bin)

function sortByName(values) {
  return [...values].sort((left, right) => left.name.localeCompare(right.name))
}

function contractFromLists(tools, resources, prompts) {
  return {
    tools: sortByName(tools.map(({ name, description, inputSchema, annotations }) => ({ name, description, input_schema: inputSchema, ...(annotations === undefined ? {} : { annotations }) }))),
    resources: sortByName(resources.map(({ name, uri, description, mimeType }) => ({ name, uri, description, mime_type: mimeType }))),
    prompts: sortByName(prompts.map(({ name, description, arguments: args }) => ({ name, description, arguments: args ?? [] }))),
  }
}

async function withClient(command, args, cwd, run) {
  const transport = new StdioClientTransport({ command, args, cwd, stderr: 'pipe' })
  const client = new Client({ name: 'package-archive-test', version: '1' })
  try {
    await client.connect(transport)
    return await run(client)
  } finally {
    await client.close()
  }
}

test('npm package excludes development files and preserves the MCP list contract', async () => {
  const tempDirectory = await mkdtemp(resolve(tmpdir(), 'ccguide-mcp-pack-'))
  try {
    const env = { ...process.env, npm_config_cache: resolve(tempDirectory, 'npm-cache') }
    const pack = spawnSync('npm', ['pack', '--json', '--pack-destination', tempDirectory], { cwd: packageRoot, encoding: 'utf8', env })
    assert.equal(pack.status, 0, pack.stderr)
    const [archive] = JSON.parse(pack.stdout)
    assert.equal(archive.name, packageJson.name)
    assert.equal(archive.version, packageJson.version)
    const required = ['dist/index.js', 'content/reference.yaml', 'content/translations.json']
    const forbidden = [/\.env/, /\.npmrc/, /^test\//, /^scripts\//, /\.map$/]
    for (const path of required) assert.ok(archive.files.some((file) => file.path === path), `missing ${path}`)
    for (const { path } of archive.files) for (const pattern of forbidden) assert.doesNotMatch(path, pattern)
    assert.ok(archive.unpackedSize <= 12 * 1024 * 1024)

    const install = resolve(tempDirectory, 'install')
    const tarball = resolve(tempDirectory, archive.filename)
    const installed = spawnSync('npm', ['install', '--prefix', install, '--ignore-scripts', '--no-audit', '--no-fund', tarball], {
      cwd: tempDirectory, encoding: 'utf8', env, timeout: 60_000, maxBuffer: 1024 * 1024,
    })
    assert.equal(installed.status, 0, `clean npm install of ${archive.filename} failed or timed out after 60s (signal: ${installed.signal ?? 'none'}). Check registry connectivity and npm cache permissions.\nstdout:\n${installed.stdout}\nstderr:\n${installed.stderr}`)
    await withClient(resolve(install, 'node_modules/.bin', binaryName), [], install, async (client) => {
      const [tools, resources, prompts] = await Promise.all([client.listTools(), client.listResources(), client.listPrompts()])
      assert.deepEqual(contractFromLists(tools.tools, resources.resources, prompts.prompts), manifest.runtime)
      for (const resource of resources.resources) {
        const result = await client.readResource({ uri: resource.uri })
        assert.ok(result.contents[0].text.length > 0, `${resource.uri} must be readable`)
        assert.equal(result.contents[0].mimeType, resource.mimeType)
        if (resource.uri === 'claude-code-guide://translations') JSON.parse(result.contents[0].text)
      }
    })
  } finally {
    await rm(tempDirectory, { recursive: true, force: true })
  }
})
