import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { basename, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { npmReleaseEnvironment } from './npm-release-cache.mjs'

const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const tempDirectory = mkdtempSync(resolve(tmpdir(), 'ccguide-mcp-release-'))
const env = npmReleaseEnvironment(resolve(tempDirectory, 'npm-cache'))

function runNpm(args) {
  const result = spawnSync('npm', args, { cwd: packageRoot, env, stdio: 'inherit' })
  if (result.error) throw result.error
  if (result.status !== 0) {
    throw new Error(`npm ${args.join(' ')} exited with ${result.status ?? result.signal ?? 'unknown status'}`)
  }
}

try {
  runNpm(['ci', '--no-audit', '--no-fund'])
  runNpm(['test'])
  runNpm(['run', 'manifest:check'])
  runNpm(['run', 'docs:product:check'])
  runNpm(['run', 'registry:metadata:check'])
  runNpm(['pack', '--dry-run', '--json'])
} catch (error) {
  console.error(`${basename(process.argv[1])}: ${error instanceof Error ? error.message : String(error)}`)
  process.exitCode = 1
} finally {
  rmSync(tempDirectory, { recursive: true, force: true })
}
