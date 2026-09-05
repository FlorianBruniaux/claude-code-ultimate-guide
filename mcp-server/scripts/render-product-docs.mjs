import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const START_MARKER = '<!-- mcp-product:start -->'
const END_MARKER = '<!-- mcp-product:end -->'
const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const manifestPath = resolve(guideRoot, 'machine-readable/mcp-product.json')
const statsPath = resolve(guideRoot, 'machine-readable/mcp-stats.json')

const documentPaths = {
  packageReadme: resolve(packageRoot, 'README.md'),
  rootReadme: resolve(guideRoot, 'README.md'),
  guide: resolve(guideRoot, 'guide/ultimate-guide.md'),
  changelog: resolve(guideRoot, 'CHANGELOG.md'),
}

function countOccurrences(source, value) {
  return source.split(value).length - 1
}

export function replaceGeneratedBlock(source, generated) {
  const startCount = countOccurrences(source, START_MARKER)
  const endCount = countOccurrences(source, END_MARKER)
  if (startCount !== 1 || endCount !== 1) {
    throw new Error('document must contain exactly one start and end marker')
  }

  const startIndex = source.indexOf(START_MARKER)
  const endIndex = source.indexOf(END_MARKER)
  if (startIndex >= endIndex) throw new Error('start marker must precede end marker')

  const contentStart = startIndex + START_MARKER.length
  return `${source.slice(0, contentStart)}\n${generated.trim()}\n${source.slice(endIndex)}`
}

function asciiPunctuation(value) {
  return String(value)
    .replaceAll('—', '-')
    .replaceAll('–', '-')
    .replaceAll('→', '->')
    .replaceAll('“', '"')
    .replaceAll('”', '"')
    .replaceAll('’', "'")
}

function tableCell(value) {
  return asciiPunctuation(value).replaceAll('|', '\\|').replace(/\s+/g, ' ').trim()
}

function toolRows(manifest) {
  return manifest.runtime.tools
    .map((tool) => `| \`${tool.name}\` | ${tableCell(tool.description)} |`)
    .join('\n')
}

function resourceRows(manifest) {
  return manifest.runtime.resources
    .map((resource) => `| \`${resource.uri}\` | \`${resource.mime_type}\` | ${tableCell(resource.description)} |`)
    .join('\n')
}

function promptRows(manifest) {
  return manifest.runtime.prompts
    .map((prompt) => `| \`${prompt.name}\` | ${tableCell(prompt.description)} |`)
    .join('\n')
}

function readCommands(manifest) {
  const commandDirectory = resolve(guideRoot, '.claude/commands/ccguide')
  const discovered = readdirSync(commandDirectory)
    .filter((name) => name.endsWith('.md'))
    .map((name) => name.slice(0, -3))
    .sort()
  const declared = [...manifest.companions.slash_commands].sort()
  if (JSON.stringify(discovered) !== JSON.stringify(declared)) throw new Error('command manifest mismatch')

  return discovered.map((name) => {
    const path = resolve(guideRoot, `.claude/commands/ccguide/${name}.md`)
    const source = readFileSync(path, 'utf8')
    const description = source.match(/^description:\s*(.+)$/m)?.[1]
    if (!description) throw new Error(`missing description in ${path}`)
    return { name, description }
  })
}

function commandRows(commands) {
  return commands
    .map((command) => `| \`/ccguide:${command.name}\` | ${tableCell(command.description)} |`)
    .join('\n')
}

function summaryRows(manifest) {
  const rows = [
    ['Tools', manifest.runtime.tools.length, manifest.runtime.tools.map(({ name }) => `\`${name}\``).join(', ')],
    ['Resources', manifest.runtime.resources.length, manifest.runtime.resources.map(({ uri }) => `\`${uri}\``).join(', ')],
    ['Prompts', manifest.runtime.prompts.length, manifest.runtime.prompts.map(({ name }) => `\`${name}\``).join(', ')],
    ['Companion commands', manifest.companions.slash_commands.length, manifest.companions.slash_commands.map((name) => `\`/ccguide:${name}\``).join(', ')],
  ]
  return rows.map(([kind, count, names]) => `| ${kind} | ${count} | ${names} |`).join('\n')
}

function projectConfig(packageName, version) {
  return `\`\`\`json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "${packageName}@${version}"]
    }
  }
}
\`\`\``
}

function nodeBadge(nodeEngine) {
  return `![Node.js ${nodeEngine}](https://img.shields.io/badge/node-${encodeURIComponent(nodeEngine)}-brightgreen)`
}

export function renderPackageReadme(manifest, commands) {
  const packageName = manifest.package.registry_name
  const version = manifest.package.version
  return `[![npm version](https://img.shields.io/npm/v/${packageName})](https://www.npmjs.com/package/${packageName}) [![npm downloads](https://img.shields.io/npm/dm/${packageName})](https://www.npmjs.com/package/${packageName}) ${nodeBadge(manifest.package.node_engine)} ![MIT license](https://img.shields.io/badge/license-MIT-blue)

Search the Claude Code Ultimate Guide, open exact source sections, inspect releases, and retrieve production templates from any MCP-compatible coding client.

## Install in 30 seconds

### Claude Code

Install for the current user:

\`\`\`bash
claude mcp add --scope user claude-code-guide -- npx -y ${packageName}@${version}
\`\`\`

For a project-scoped configuration, add this to \`.mcp.json\` at the repository root:

${projectConfig(packageName, version)}

### Codex

\`\`\`bash
codex mcp add claude-code-guide -- npx -y ${packageName}@${version}
\`\`\`

### Cursor

Add this server entry to \`.cursor/mcp.json\`:

${projectConfig(packageName, version)}

### VS Code

Add this to \`.vscode/mcp.json\`:

\`\`\`json
{
  "servers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "${packageName}@${version}"]
    }
  }
}
\`\`\`

## Three useful sequences

1. Find and read: \`search_guide({ query: "hooks" })\`, then \`read_section({ path: "..." })\` with the returned path.
2. Discover and retrieve a template: \`search_examples({ query: "pre-commit lint" })\`, then \`get_example({ name: "..." })\`.
3. Track official documentation: run \`init_official_docs()\` once, then \`refresh_official_docs()\` and \`diff_official_docs()\` when you want a new comparison.

## Generated capabilities

This section is rendered from \`machine-readable/mcp-product.json\` for package ${version} and guide ${manifest.guide.version}.

| Capability | Count | Names |
| --- | ---: | --- |
${summaryRows(manifest)}

### Tools

| Tool | Description |
| --- | --- |
${toolRows(manifest)}

### Resources

| Resource URI | MIME type | Description |
| --- | --- | --- |
${resourceRows(manifest)}

### Prompts

| Prompt | Description |
| --- | --- |
${promptRows(manifest)}

### Companion Claude Code commands

The repository contains these command files. They are not installed by the npm package.

| Command | Description |
| --- | --- |
${commandRows(commands)}

## Local data, network, and cache behavior

The package bundles the reference index, release history, guide navigation, Agent Harness Map, and translation metadata. Initialization and list operations use bundled content and do not require the network.

\`read_section\`, \`get_example\`, \`get_cheatsheet\`, \`get_changelog\`, \`get_digest\`, and threat lookups can fetch files from GitHub when content is not available locally. Successful responses are written to \`~/.cache/claude-code-guide/${version}/\` for 24 hours; stale cached content is used when the network is unavailable. With \`GUIDE_ROOT\` set to a local guide checkout, these tools read that checkout instead.

\`init_official_docs\` and \`refresh_official_docs\` fetch Anthropic's official documentation and write a separate local snapshot under \`~/.cache/claude-code-guide/\`. \`diff_official_docs\` and \`search_official_docs\` read those snapshots.

## Privacy

The server has no first-party telemetry. MCP protocol messages use standard input and standard output. Network-capable tools contact GitHub or Anthropic only when invoked, and their local cache or snapshot writes stay on the machine running the server.

## Limitations

- Full guide Markdown is not bundled. A first uncached section, example, cheatsheet, changelog, digest, or threat lookup can require GitHub.
- Official-doc search and diff require a local snapshot created by \`init_official_docs\`.
- The five \`/ccguide:*\` companion commands must be installed from the repository separately.
- The MCP Registry listing is not advertised until its API returns the published namespace.

## Diagnostics

Verify the package binary and JSON-RPC surface with the MCP Inspector:

\`\`\`bash
npx -y @modelcontextprotocol/inspector npx -y ${packageName}@${version}
\`\`\`

For local development:

\`\`\`bash
npm ci
npm run build
GUIDE_ROOT=.. node dist/index.js
\`\`\`

## Technical guide and contributing

Read the [canonical technical guide](../guide/ecosystem/claude-code-guide-mcp.md) for the published-versus-candidate boundary, architecture, privacy, offline behavior, and dated statistics.

Issues and pull requests are welcome in the [Claude Code Ultimate Guide repository](https://github.com/FlorianBruniaux/claude-code-ultimate-guide). Run \`npm run release:check\` from \`mcp-server/\` before submitting package changes.`
}

function renderRootReadme(manifest, commands) {
  const packageName = manifest.package.registry_name
  const version = manifest.package.version
  return `Install the guide as a stdio MCP server and query it from Claude Code, Codex, Cursor, VS Code, or another MCP client.

\`\`\`bash
claude mcp add --scope user claude-code-guide -- npx -y ${packageName}@${version}
codex mcp add claude-code-guide -- npx -y ${packageName}@${version}
\`\`\`

Project-scoped Claude Code configuration belongs in \`.mcp.json\`:

${projectConfig(packageName, version)}

| Capability | Count | Names |
| --- | ---: | --- |
${summaryRows(manifest)}

The list operations and search index use bundled content. Section, example, cheatsheet, changelog, digest (\`get_digest\`), and threat tools can fetch GitHub content and write a 24-hour local cache. The official-doc initialization and refresh tools fetch Anthropic documentation and write separate local snapshots.

[Canonical technical guide, installation, privacy, limitations, and dated statistics](./guide/ecosystem/claude-code-guide-mcp.md)

[Package README and diagnostics](./mcp-server/README.md)

Companion commands rendered from the repository: ${commands.map(({ name }) => `\`/ccguide:${name}\``).join(', ')}.`
}

function renderGuideSection(manifest, commands) {
  const packageName = manifest.package.registry_name
  const version = manifest.package.version
  return `The Claude Code Ultimate Guide ships a stdio MCP server so coding clients can search the bundled reference, read source sections, inspect releases, and retrieve templates.

#### Installation

\`\`\`bash
claude mcp add --scope user claude-code-guide -- npx -y ${packageName}@${version}
codex mcp add claude-code-guide -- npx -y ${packageName}@${version}
\`\`\`

For project-scoped Claude Code use, add the server to \`.mcp.json\`:

${projectConfig(packageName, version)}

#### Generated capabilities

| Capability | Count | Names |
| --- | ---: | --- |
${summaryRows(manifest)}

| Tool | Description |
| --- | --- |
${toolRows(manifest)}

| Resource URI | MIME type | Description |
| --- | --- | --- |
${resourceRows(manifest)}

| Companion command | Description |
| --- | --- |
${commandRows(commands)}

#### Data and network boundary

List operations and the search index use bundled package content. Section, example, cheatsheet, changelog, digest (\`get_digest\`), and threat tools may fetch GitHub content and write a 24-hour local cache. The official-doc initialization and refresh tools fetch Anthropic documentation and write separate local snapshots. The server is therefore not fully offline or purely read-only.

See the [canonical technical guide](ecosystem/claude-code-guide-mcp.md) for the published-versus-candidate boundary, Cursor and VS Code configuration, privacy, offline behavior, limitations, diagnostics, and dated statistics. The [package README](../mcp-server/README.md) remains the package-level quick reference.`
}

function formatInteger(value) {
  return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

function renderStatsChangelog(stats) {
  const downloads = stats.downloads
  const sinceLaunch = downloads.since_launch
  const yearToDate = downloads.year_to_date
  const last30 = downloads.last_30_days
  const last7 = downloads.last_7_days
  const registry = stats.registries.official_mcp.published
    ? 'published'
    : 'not returned by the official MCP Registry'
  return `<!-- mcp-stats:start -->
- **MCP public statistics snapshot** (\`machine-readable/mcp-stats.json\`): snapshot \`${stats.snapshot_at}\` for npm ${stats.public_version}; since launch ${sinceLaunch.start} through ${sinceLaunch.end}: ${formatInteger(sinceLaunch.count)} downloads; year to date ${yearToDate.start} through ${yearToDate.end}: ${formatInteger(yearToDate.count)} downloads; trailing 30 complete UTC days ${last30.start} through ${last30.end}: ${formatInteger(last30.count)} downloads; trailing 7 complete UTC days ${last7.start} through ${last7.end}: ${formatInteger(last7.count)} downloads. The package is ${registry}. Download counts are not users, active installations, sessions, or executions.
<!-- mcp-stats:end -->`
}

export function renderChangelog(manifest, stats = loadStats()) {
  const version = manifest.package.version
  const sdkVersion = manifest.package.dependencies.model_context_protocol_sdk
  const audit = manifest.security
  const productionCount = audit.production_vulnerabilities === 0 ? 'zero' : audit.production_vulnerabilities
  const development = audit.development_only_vulnerabilities
  const developmentCount = development.low === 1 ? 'one' : development.low
  const developmentPackages = development.packages.join(', ')
  const developmentAdvisory = development.low === 1 ? 'advisory remains' : 'advisories remain'
  return `- **MCP product documentation, registry metadata, and aggregate release gate** (\`machine-readable/mcp-product.json\`, \`mcp-server/server.json\`, deterministic renderers, package and guide documentation): rendered current package ${version} capabilities into marker-delimited surfaces, corrected Claude Code and Codex install commands plus project \`.mcp.json\` configuration, documented bundled versus network and local-write behavior including \`get_digest\`, and published only the ${manifest.companions.slash_commands.length} companion command files that exist. The canonical technical guide records the public npm package, observed runtime, and repository candidate as separate evidence states when their versions differ, and documents installation, architecture, privacy, offline behavior, troubleshooting, and dated metrics. The renderers validate every target before writing. The manual release workflow checks the live JSON-RPC contract, a clean consumer install of the exact packed archive, manifest, generated documentation, registry metadata, tests, and dry-run package contents through \`npm run release:check\`. It prepares checksum-pinned Registry validation before approval and an approval-gated publication sequence for \`${manifest.package.mcp_registry_name}\`. npm trusted-publisher binding remains an external prerequisite, and a required reviewer on the \`mcp-production\` environment remains an external prerequisite; repository code does not verify either setting. The reproducible monthly npm, GSC, and GA4 dashboard limits Google queries to the two MCP page URLs and aggregate metrics; missing Google access remains unavailable rather than zero. The separate npm public-runtime snapshot command starts the exact version returned by npm and writes sanitized capability names and counts to machine-readable/mcp-public-runtime.json; it excludes descriptions, resource URIs, prompt arguments, call arguments, results, user content, local paths, and user and request identifiers. Dependency security: @modelcontextprotocol/sdk ${sdkVersion}; \`npm audit --omit=dev\` reported ${productionCount} production vulnerabilities on ${audit.audit_as_of}; ${developmentCount} low-severity development-only ${developmentPackages} ${developmentAdvisory} in the full audit.

${renderStatsChangelog(stats)}`
}

function loadManifest() {
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'))
  if (manifest.schema_version !== 1) throw new Error(`unsupported manifest schema: ${manifest.schema_version}`)
  return manifest
}

function loadStats() {
  const stats = JSON.parse(readFileSync(statsPath, 'utf8'))
  if (stats.schema_version !== 1) throw new Error(`unsupported statistics schema: ${stats.schema_version}`)
  return stats
}

export function buildRenderPlan(targets) {
  return targets.map(({ path, source, generated }) => {
    try {
      return { path, source, rendered: replaceGeneratedBlock(source, generated) }
    } catch (error) {
      throw new Error(`${path}: ${error instanceof Error ? error.message : String(error)}`)
    }
  })
}

export function renderProductDocs({ check = false } = {}) {
  const manifest = loadManifest()
  const commands = readCommands(manifest)
  const generatedByPath = new Map([
    [documentPaths.packageReadme, renderPackageReadme(manifest, commands)],
    [documentPaths.rootReadme, renderRootReadme(manifest, commands)],
    [documentPaths.guide, renderGuideSection(manifest, commands)],
    [documentPaths.changelog, renderChangelog(manifest)],
  ])

  const plan = buildRenderPlan([...generatedByPath].map(([path, generated]) => ({
    path,
    generated,
    source: readFileSync(path, 'utf8'),
  })))
  const stale = plan.filter(({ source, rendered }) => source !== rendered)

  if (stale.length > 0) {
    if (check) throw new Error(`stale MCP product documentation:\n${stale.map(({ path }) => `- ${path}`).join('\n')}`)
    for (const { path, rendered } of stale) writeFileSync(path, rendered, 'utf8')
  }
}

function runCli() {
  const args = process.argv.slice(2)
  const allowed = new Set(['--check'])
  if (args.some((arg) => !allowed.has(arg)) || args.length > 1) {
    throw new Error('usage: node scripts/render-product-docs.mjs [--check]')
  }
  renderProductDocs({ check: args[0] === '--check' })
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    runCli()
  } catch (error) {
    console.error(`${basename(process.argv[1])}: ${error instanceof Error ? error.message : String(error)}`)
    process.exitCode = 1
  }
}
