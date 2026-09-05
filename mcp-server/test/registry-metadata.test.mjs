import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'
import test from 'node:test'
import { parse as parseYaml } from 'yaml'

const packageRoot = resolve(import.meta.dirname, '..')
const guideRoot = resolve(packageRoot, '..')
const packagePath = resolve(packageRoot, 'package.json')
const serverPath = resolve(packageRoot, 'server.json')
const rendererPath = resolve(packageRoot, 'scripts/render-registry-metadata.mjs')
const workflowPath = resolve(guideRoot, '.github/workflows/publish-mcp.yml')
const manifestPath = resolve(guideRoot, 'machine-readable/mcp-product.json')

const expectedDescription = 'Search the Claude Code Ultimate Guide, official Anthropic documentation, releases, examples, security references, agent harness data, and translations from any MCP-compatible client.'
const expectedKeywords = [
  'mcp',
  'mcp-server',
  'model-context-protocol',
  'claude',
  'claude-code',
  'codex',
  'cursor',
  'documentation-search',
  'ai-agents',
  'developer-tools',
]

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'))
}

function expectedServer(packageJson) {
  return {
    $schema: 'https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json',
    name: 'io.github.FlorianBruniaux/claude-code-guide',
    title: 'Claude Code Ultimate Guide',
    description: 'Search the Claude Code Ultimate Guide and machine-readable references from any MCP client.',
    repository: {
      url: 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide',
      source: 'github',
    },
    version: packageJson.version,
    packages: [
      {
        registryType: 'npm',
        identifier: packageJson.name,
        version: packageJson.version,
        transport: { type: 'stdio' },
      },
    ],
  }
}

const actionPins = {
  'actions/checkout': { sha: 'd23441a48e516b6c34aea4fa41551a30e30af803', version: 'v6' },
  'actions/setup-node': { sha: '249970729cb0ef3589644e2896645e5dc5ba9c38', version: 'v6' },
  'actions/upload-artifact': { sha: 'ea165f8d65b6e75b540449e92b4886f43607fa02', version: 'v4' },
  'actions/download-artifact': { sha: 'd3f86a106a0bac45b974a628896c90dbdf5c8093', version: 'v4' },
}

function step(job, name) {
  const match = job.steps.find((candidate) => candidate.name === name)
  assert.ok(match, `missing workflow step: ${name}`)
  return match
}

test('npm metadata exposes the package and official MCP Registry identities', () => {
  const packageJson = readJson(packagePath)
  assert.equal(packageJson.description, expectedDescription)
  assert.deepEqual(packageJson.keywords, expectedKeywords)
  assert.equal(packageJson.homepage, 'https://cc.bruniaux.com/mcp/')
  assert.equal(packageJson.mcpName, 'io.github.FlorianBruniaux/claude-code-guide')
  assert.deepEqual(packageJson.repository, {
    type: 'git',
    url: 'git+https://github.com/FlorianBruniaux/claude-code-ultimate-guide.git',
    directory: 'mcp-server',
  })
  assert.equal(packageJson.dependencies.zod, '^4.3.6')
  assert.equal(packageJson.scripts['registry:metadata'], 'node scripts/render-registry-metadata.mjs')
  assert.equal(packageJson.scripts['registry:metadata:check'], 'node scripts/render-registry-metadata.mjs --check')
  assert.equal(
    packageJson.scripts['release:check'],
    'npm ci && npm test && npm run manifest:check && npm run docs:product:check && npm run registry:metadata:check && npm pack --dry-run --json',
  )

  const manifest = readJson(manifestPath)
  assert.equal(manifest.package.registry_name, packageJson.name)
  assert.equal(manifest.package.mcp_registry_name, packageJson.mcpName)
})

test('registry metadata renderer produces the complete deterministic server document', async () => {
  assert.ok(existsSync(rendererPath), 'render-registry-metadata.mjs must exist')
  const renderer = await import(pathToFileURL(rendererPath).href)
  const packageJson = readJson(packagePath)
  const expected = expectedServer(packageJson)
  assert.deepEqual(renderer.buildRegistryMetadata(packageJson), expected)
  assert.equal(renderer.renderRegistryMetadata(packageJson), `${JSON.stringify(expected, null, 2)}\n`)

  assert.ok(existsSync(serverPath), 'server.json must exist')
  assert.deepEqual(readJson(serverPath), expected)
  const check = spawnSync(process.execPath, [rendererPath, '--check'], { cwd: packageRoot, encoding: 'utf8' })
  assert.equal(check.status, 0, `${check.stdout}${check.stderr}`)
})

test('server description satisfies the current registry schema length boundary', () => {
  const serverJson = readJson(serverPath)
  assert.equal(serverJson.$schema, 'https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json')
  assert.ok(Array.from(serverJson.description).length <= 100, `server description has ${Array.from(serverJson.description).length} characters; schema maximum is 100`)
})

test('manual workflow separates reproducible preparation from protected publication', () => {
  assert.ok(existsSync(workflowPath), 'publish-mcp.yml must exist')
  const source = readFileSync(workflowPath, 'utf8')
  const workflow = parseYaml(source)
  assert.deepEqual(workflow.permissions, { contents: 'read' })
  assert.deepEqual(Object.keys(workflow.on), ['workflow_dispatch'])
  assert.deepEqual(workflow.on.workflow_dispatch.inputs.version, {
    description: 'Exact package version to publish',
    required: true,
    type: 'string',
  })

  const prepare = workflow.jobs.prepare
  const publish = workflow.jobs.publish
  assert.equal(prepare.environment, undefined)
  assert.equal(publish.needs, 'prepare')
  assert.equal(publish.environment, 'mcp-production')
  assert.deepEqual(publish.permissions, { contents: 'read', 'id-token': 'write' })

  for (const job of [prepare, publish]) {
    const setup = job.steps.find((candidate) => candidate.uses?.startsWith('actions/setup-node@'))
    assert.ok(setup, 'each job must set up Node')
    assert.equal(String(setup.with['node-version']), '24')
    for (const candidate of job.steps) {
      if (candidate.run) assert.doesNotMatch(candidate.run, /\$\{\{\s*inputs\.version\s*\}\}/, 'workflow input must enter shell only through an environment variable')
    }
  }

  const version = step(prepare, 'Validate requested version')
  assert.equal(version.env.RELEASE_VERSION, '${{ inputs.version }}')
  assert.match(version.run, /process\.env\.RELEASE_VERSION/)
  assert.match(version.run, /packageJson\.version/)
  assert.match(step(prepare, 'Run release checks').run, /npm run release:check/)

  const registryValidation = step(prepare, 'Validate official registry metadata')
  const registryValidationRun = registryValidation.run
  const publisherDownload = 'https://github.com/modelcontextprotocol/registry/releases/download/v1.8.1/mcp-publisher_linux_amd64.tar.gz'
  const publisherChecksum = 'a06c9096dcb9727c13555b6be26c7effa707b01f06a4c561ba7a3635443cf2cc'
  assert.match(registryValidationRun, /mktemp -d/)
  assert.ok(registryValidationRun.includes(publisherDownload))
  assert.ok(registryValidationRun.includes(publisherChecksum))
  const checksumIndex = registryValidationRun.indexOf('sha256sum --check --strict')
  const extractIndex = registryValidationRun.indexOf('tar -xzf')
  const validateIndex = registryValidationRun.indexOf(' validate ')
  assert.ok(checksumIndex >= 0 && checksumIndex < extractIndex && extractIndex < validateIndex)
  assert.doesNotMatch(registryValidationRun, / login | publish /)

  const pack = step(prepare, 'Pack release archive')
  assert.equal((pack.run.match(/npm pack --json --pack-destination/g) ?? []).length, 1)
  assert.match(pack.run, /tar -tzf/)
  assert.match(pack.run, /sha256sum/)
  assert.ok(prepare.steps.some((candidate) => candidate.uses?.startsWith('actions/upload-artifact@')))
  assert.ok(publish.steps.some((candidate) => candidate.uses?.startsWith('actions/download-artifact@')))
  assert.match(step(publish, 'Verify release archive').run, /sha256sum --check --strict/)
})

test('workflow pins every third-party action to an approved commit with a version comment', () => {
  const source = readFileSync(workflowPath, 'utf8')
  const workflow = parseYaml(source)
  for (const job of Object.values(workflow.jobs)) {
    for (const candidate of job.steps) {
      if (!candidate.uses) continue
      const [action, revision] = candidate.uses.split('@')
      const pin = actionPins[action]
      assert.ok(pin, `unapproved action: ${action}`)
      assert.equal(revision, pin.sha, `${action} must use the approved full commit`)
      const line = `uses: ${action}@${pin.sha} # ${pin.version}`
      assert.ok(source.includes(line), `${action} must retain the ${pin.version} comment`)
    }
  }
})

test('protected publication uses tokenless npm provenance, bounded smoke verification, and a pinned publisher', () => {
  assert.ok(existsSync(workflowPath), 'publish-mcp.yml must exist')
  const source = readFileSync(workflowPath, 'utf8')
  const workflow = parseYaml(source)
  const steps = workflow.jobs.publish.steps
  const names = steps.map(({ name }) => name)
  const npmStateIndex = names.indexOf('Check npm publication state')
  const npmIndex = names.indexOf('Publish package to npm')
  const smokeIndex = names.indexOf('Smoke test published package')
  const registryIndex = names.indexOf('Publish server to MCP Registry')
  assert.ok(npmStateIndex >= 0 && npmStateIndex < npmIndex && npmIndex < smokeIndex && smokeIndex < registryIndex)

  const npmState = steps[npmStateIndex]
  assert.equal(npmState.id, 'npm_status')
  assert.match(npmState.run, /npm view .*dist\.integrity --json/)
  assert.match(npmState.run, /createHash\('sha512'\)/)
  assert.match(npmState.run, /published_integrity.*archive_integrity/)
  assert.match(npmState.run, /grep -q 'E404'/)
  assert.match(npmState.run, /published=true.*GITHUB_OUTPUT/s)

  const npmPublish = steps[npmIndex]
  assert.equal(npmPublish.if, "steps.npm_status.outputs.published != 'true'")
  assert.match(npmPublish.run, /npm publish .*--provenance/)
  assert.doesNotMatch(source, /NODE_AUTH_TOKEN|NPM_TOKEN/)

  const smokeStep = steps[smokeIndex]
  const smoke = smokeStep.run
  assert.equal(smokeStep.env.MANIFEST_PATH, 'machine-readable/mcp-product.json')
  assert.match(smoke, /timeout 60s/)
  assert.match(smoke, /tools\/list/)
  assert.match(smoke, /resources\/list/)

  const registry = steps[registryIndex].run
  const checksum = 'a06c9096dcb9727c13555b6be26c7effa707b01f06a4c561ba7a3635443cf2cc'
  assert.match(registry, /mktemp -d/)
  assert.ok(registry.includes(checksum))
  assert.doesNotMatch(registry, /curl| validate /)
  const verifyIndex = registry.indexOf('sha256sum --check --strict')
  const extractIndex = registry.indexOf('tar -xzf')
  const loginIndex = registry.indexOf(' login github-oidc')
  const publishIndex = registry.indexOf(' publish ')
  assert.ok(verifyIndex >= 0 && verifyIndex < extractIndex)
  assert.ok(extractIndex < loginIndex && loginIndex < publishIndex)
})
