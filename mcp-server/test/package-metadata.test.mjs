import assert from 'node:assert/strict'
import { once } from 'node:events'
import { readFileSync } from 'node:fs'
import { readdir } from 'node:fs/promises'
import { spawn } from 'node:child_process'
import { resolve } from 'node:path'
import test from 'node:test'

const root = resolve(import.meta.dirname, '..')
const pkg = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8'))
const packageLock = JSON.parse(readFileSync(resolve(root, 'package-lock.json'), 'utf8'))

function minimumNodeVersion(range) {
  const match = /^>=\s*(\d+)(?:\.(\d+))?(?:\.(\d+))?$/.exec(range)
  assert.ok(match, `unsupported Node engine range in metadata test: ${range}`)
  return match.slice(1).map((part) => Number(part ?? 0))
}

function compareVersions(left, right) {
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return left[index] - right[index]
  }
  return 0
}

async function builtJavascript() {
  const files = (await readdir(resolve(root, 'dist')))
    .filter((file) => file.endsWith('.js'))
    .sort()
  return files.map((file) => readFileSync(resolve(root, 'dist', file), 'utf8')).join('\n')
}

test('built runtime uses package.json version', async () => {
  const source = await builtJavascript()
  const escaped = pkg.version.replaceAll('.', '\\.')
  assert.match(source, new RegExp(`claude-code-ultimate-guide-mcp/${escaped}`))
  assert.doesNotMatch(source, /claude-code-ultimate-guide-mcp\/(1\.0\.0|1\.1\.0)/)
})

test('advertised Node floor covers the resolved production server dependency floor', () => {
  const nodeServer = packageLock.packages['node_modules/@hono/node-server']
  assert.ok(nodeServer, '@hono/node-server must be resolved in the production lock')
  assert.equal(nodeServer.dev, undefined, '@hono/node-server must remain a production dependency')

  const advertisedFloor = minimumNodeVersion(pkg.engines.node)
  const dependencyFloor = minimumNodeVersion(nodeServer.engines.node)
  assert.ok(
    compareVersions(advertisedFloor, dependencyFloor) >= 0,
    `package Node floor ${pkg.engines.node} is below @hono/node-server ${nodeServer.version} floor ${nodeServer.engines.node}`,
  )
})

test('MCP initialize handshake reports package.json version', async () => {
  const child = spawn(process.execPath, [resolve(root, 'dist/index.js')], {
    cwd: root,
    stdio: ['pipe', 'pipe', 'pipe'],
  })
  const response = new Promise((resolveResponse, reject) => {
    let output = ''
    child.stdout.setEncoding('utf8')
    child.stdout.on('data', (chunk) => {
      output += chunk
      for (const line of output.split('\n')) {
        if (!line.trim()) continue
        try {
          const message = JSON.parse(line)
          if (message.id === 1) resolveResponse(message)
        } catch {
          // Wait for a complete JSON line.
        }
      }
    })
    child.once('error', reject)
  })

  child.stdin.end(JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'test', version: '1' } },
  }) + '\n')

  let timeout
  const timeoutPromise = new Promise((_, reject) => {
    timeout = setTimeout(() => reject(new Error('initialize timed out')), 5000)
  })
  const message = await Promise.race([response, timeoutPromise])
  clearTimeout(timeout)
  assert.equal(message.result.serverInfo.version, pkg.version)
  child.kill('SIGTERM')
  await once(child, 'exit')
})

test('cache namespace uses the injected package version', async () => {
  const source = await builtJavascript()
  assert.match(source, /claude-code-guide", PACKAGE_VERSION/)
})
