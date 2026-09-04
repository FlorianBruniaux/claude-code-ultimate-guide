import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'
import test from 'node:test'
import { npmReleaseEnvironment, RELEASE_NPM_CACHE_ENV } from '../scripts/npm-release-cache.mjs'

const packageRoot = resolve(import.meta.dirname, '..')

test('release cache contract replaces an unusable ambient npm cache', () => {
  const cache = resolve(tmpdir(), 'ccguide-explicit-cache')
  const env = npmReleaseEnvironment(cache, {
    npm_config_cache: '/dev/null/unwritable-ambient-cache',
    SENTINEL: 'preserved',
  })

  assert.equal(env.npm_config_cache, cache)
  assert.equal(env[RELEASE_NPM_CACHE_ENV], cache)
  assert.equal(env.npm_config_audit, 'false')
  assert.equal(env.npm_config_fund, 'false')
  assert.equal(env.SENTINEL, 'preserved')
})

test('release orchestration warms the explicit cache before archive tests', () => {
  const releaseCheck = readFileSync(resolve(packageRoot, 'scripts/run-release-check.mjs'), 'utf8')
  const archiveTest = readFileSync(resolve(packageRoot, 'test/package-archive.test.mjs'), 'utf8')
  const ciIndex = releaseCheck.indexOf("runNpm(['ci'")
  const testIndex = releaseCheck.indexOf("runNpm(['test'])")

  assert.match(releaseCheck, /npmReleaseEnvironment\(resolve\(tempDirectory, 'npm-cache'\)\)/)
  assert.ok(ciIndex >= 0 && ciIndex < testIndex)
  assert.match(archiveTest, /process\.env\[RELEASE_NPM_CACHE_ENV\]/)
  assert.match(archiveTest, /'cache-warm-install'/)
  assert.match(archiveTest, /'--offline'/)
})
