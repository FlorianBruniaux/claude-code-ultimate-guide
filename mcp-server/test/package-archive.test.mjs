import assert from 'node:assert/strict'
import { mkdtemp, rm } from 'node:fs/promises'
import { spawnSync } from 'node:child_process'
import { resolve } from 'node:path'
import { tmpdir } from 'node:os'
import test from 'node:test'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

const packageRoot = resolve(import.meta.dirname, '..')

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
    const required = ['dist/index.js', 'content/reference.yaml', 'content/translations.json']
    const forbidden = [/\.env/, /\.npmrc/, /^test\//, /^scripts\//, /\.map$/]
    for (const path of required) assert.ok(archive.files.some((file) => file.path === path), `missing ${path}`)
    for (const { path } of archive.files) for (const pattern of forbidden) assert.doesNotMatch(path, pattern)
    assert.ok(archive.unpackedSize <= 12 * 1024 * 1024)

    const install = resolve(tempDirectory, 'install')
    const tarball = resolve(tempDirectory, archive.filename)
    const installed = spawnSync('npm', ['install', '--prefix', install, '--ignore-scripts', '--no-audit', '--no-fund', tarball], { cwd: tempDirectory, encoding: 'utf8', env })
    assert.equal(installed.status, 0, installed.stderr)
    await withClient(resolve(install, 'node_modules/.bin/claude-code-ultimate-guide-mcp'), [], install, async (client) => {
      assert.equal((await client.listTools()).tools.length, 17)
      assert.equal((await client.listResources()).resources.length, 5)
      assert.equal((await client.listPrompts()).prompts.length, 1)
    })
  } finally {
    await rm(tempDirectory, { recursive: true, force: true })
  }
})
