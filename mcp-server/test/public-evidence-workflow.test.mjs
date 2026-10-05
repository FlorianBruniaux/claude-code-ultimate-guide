import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import test from 'node:test'
import { parse } from 'yaml'

const root = resolve(fileURLToPath(new URL('../..', import.meta.url)))
function workflow(name) {
  return parse(readFileSync(resolve(root, '.github/workflows', name), 'utf8'))
}

test('public evidence refresh follows successful publication and commits both version sources together', () => {
  const release = workflow('publish-mcp.yml')
  const refresh = release.jobs['refresh-public-evidence']
  assert.ok(refresh, 'publication must refresh its public evidence')
  assert.equal(refresh.needs, 'publish')
  assert.equal(refresh.uses, './.github/workflows/collect-mcp-stats.yml')
  assert.deepEqual(refresh.permissions, { contents: 'write' })

  const collector = workflow('collect-mcp-stats.yml')
  assert.ok('workflow_call' in collector.on, 'release must be able to call the collector')
  const steps = collector.jobs.collect.steps
  const runtimeIndex = steps.findIndex(step => step.run?.includes('snapshot:public-runtime'))
  const statisticsIndex = steps.findIndex(step => step.run?.includes('--changelog CHANGELOG.md'))
  const commitIndex = steps.findIndex(step => step.run?.includes('git commit'))
  assert.ok(runtimeIndex >= 0 && runtimeIndex < statisticsIndex && statisticsIndex < commitIndex)
  const commit = steps[commitIndex].run
  for (const command of ['git diff --quiet --', 'git add --']) {
    const line = commit.split('\n').find(line => line.includes(command))
    assert.ok(line?.includes('machine-readable/mcp-public-runtime.json'))
    assert.ok(line?.includes('machine-readable/mcp-stats.json'))
  }
})
