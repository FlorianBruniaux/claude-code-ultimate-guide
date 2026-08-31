import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import test from 'node:test'

const root = resolve(import.meta.dirname, '..')
const pkg = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8'))

test('built runtime uses package.json version', () => {
  const source = readFileSync(resolve(root, 'dist/index.js'), 'utf8')
  const escaped = pkg.version.replaceAll('.', '\\.')
  assert.match(source, new RegExp(`claude-code-ultimate-guide-mcp/${escaped}`))
  assert.doesNotMatch(source, /claude-code-ultimate-guide-mcp\/(1\.0\.0|1\.1\.0)/)
})
