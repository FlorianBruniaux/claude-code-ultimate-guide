import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const START_MARKER = '<!-- mcp-product:start -->'
const END_MARKER = '<!-- mcp-product:end -->'
const scriptDirectory = resolve(fileURLToPath(new URL('.', import.meta.url)))
const packageRoot = resolve(scriptDirectory, '..')
const guideRoot = resolve(packageRoot, '..')
const manifestPath = resolve(guideRoot, 'machine-readable/mcp-product.json')

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

function renderPackageReadme(manifest, commands) {
  const packageName = manifest.package.registry_name
  const version = manifest.package.version
  return `[![npm version](https://img.shields.io/npm/v/${packageName})](https://www.npmjs.com/package/${packageName}) [![npm downloads](https://img.shields.io/npm/dm/${packageName})](https://www.npmjs.com/package/${packageName}) ![Node.js 18+](https://img.shields.io/badge/node-%3E%3D18-brightgreen) ![MIT license](https://img.shields.io/badge/license-MIT-blue)

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

\`read_section\`, \`get_example\`, \`get_cheatsheet\`, \`get_changelog\`, and threat lookups can fetch files from GitHub when content is not available locally. Successful responses are written to \`~/.cache/claude-code-guide/${version}/\` for 24 hours; stale cached content is used when the network is unavailable. With \`GUIDE_ROOT\` set to a local guide checkout, these tools read that checkout instead.

\`init_official_docs\` and \`refresh_official_docs\` fetch Anthropic's official documentation and write a separate local snapshot under \`~/.cache/claude-code-guide/\`. \`diff_official_docs\` and \`search_official_docs\` read those snapshots.

## Privacy

The server has no first-party telemetry. MCP protocol messages use standard input and standard output. Network-capable tools contact GitHub or Anthropic only when invoked, and their local cache or snapshot writes stay on the machine running the server.

## Limitations

- Full guide Markdown is not bundled. A first uncached section, example, cheatsheet, changelog, or threat lookup can require GitHub.
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

## Contributing

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

The list operations and search index use bundled content. Section, example, cheatsheet, changelog, and threat tools can fetch GitHub content and write a 24-hour local cache. The official-doc initialization and refresh tools fetch Anthropic documentation and write separate local snapshots.

[Installation, privacy, limitations, and diagnostics](./mcp-server/README.md)

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

List operations and the search index use bundled package content. Section, example, cheatsheet, changelog, and threat tools may fetch GitHub content and write a 24-hour local cache. The official-doc initialization and refresh tools fetch Anthropic documentation and write separate local snapshots. The server is therefore not fully offline or purely read-only.

See the [package README](../mcp-server/README.md) for Cursor and VS Code configuration, privacy, limitations, and diagnostics.`
}

function renderChangelog(manifest) {
  const version = manifest.package.version
  return `- **MCP product documentation and aggregate release gate** (\`machine-readable/mcp-product.json\`, \`mcp-server/scripts/render-product-docs.mjs\`, package and guide documentation): rendered current package ${version} capabilities into marker-delimited surfaces, corrected Claude Code and Codex install commands plus project \`.mcp.json\` configuration, documented bundled versus network and local-write behavior, and published only the ${manifest.companions.slash_commands.length} companion command files that exist. The release gate now checks the live JSON-RPC contract, packed archive, manifest, generated documentation, tests, and dry-run package contents through \`npm run release:check\`.`
}

function insertBootstrapMarkers(path, source) {
  if (source.includes(START_MARKER) || source.includes(END_MARKER)) {
    throw new Error(`${path} already contains a product marker`)
  }

  if (path === documentPaths.packageReadme) {
    const title = '# claude-code-ultimate-guide-mcp\n\n'
    if (!source.startsWith(title)) throw new Error(`${path} has an unexpected title`)
    return `${title}${START_MARKER}\nbootstrap\n${END_MARKER}\n`
  }

  if (path === documentPaths.rootReadme) {
    const sectionStart = source.indexOf('## 🔌 MCP Server: Use the guide from any Claude Code session')
    const sectionEnd = source.indexOf('\n---\n', sectionStart)
    if (sectionStart < 0 || sectionEnd < 0) throw new Error(`${path} legacy MCP section not found`)
    const section = `## MCP Server: Use the guide from any coding client\n\n${START_MARKER}\nbootstrap\n${END_MARKER}\n`
    return `${source.slice(0, sectionStart)}${section}${source.slice(sectionEnd)}`
  }

  if (path === documentPaths.guide) {
    const sectionStart = source.indexOf('### 📖 This Guide as an MCP Server')
    const nextSection = source.indexOf('### 🌐 Community MCP Servers Ecosystem', sectionStart)
    if (sectionStart < 0 || nextSection < 0) throw new Error(`${path} legacy MCP section not found`)
    const section = `### This Guide as an MCP Server\n\n${START_MARKER}\nbootstrap\n${END_MARKER}\n\n---\n\n`
    return `${source.slice(0, sectionStart)}${section}${source.slice(nextSection)}`
  }

  if (path === documentPaths.changelog) {
    const unreleased = '## [Unreleased]\n\n'
    const index = source.indexOf(unreleased)
    if (index < 0) throw new Error(`${path} [Unreleased] heading not found`)
    const insertion = `${START_MARKER}\nbootstrap\n${END_MARKER}\n\n`
    return `${source.slice(0, index + unreleased.length)}${insertion}${source.slice(index + unreleased.length)}`
  }

  throw new Error(`unsupported bootstrap document: ${path}`)
}

function loadManifest() {
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'))
  if (manifest.schema_version !== 1) throw new Error(`unsupported manifest schema: ${manifest.schema_version}`)
  return manifest
}

export function renderProductDocs({ check = false, bootstrap = false } = {}) {
  const manifest = loadManifest()
  const commands = readCommands(manifest)
  const generatedByPath = new Map([
    [documentPaths.packageReadme, renderPackageReadme(manifest, commands)],
    [documentPaths.rootReadme, renderRootReadme(manifest, commands)],
    [documentPaths.guide, renderGuideSection(manifest, commands)],
    [documentPaths.changelog, renderChangelog(manifest)],
  ])

  const stale = []
  for (const [path, generated] of generatedByPath) {
    let source = readFileSync(path, 'utf8')
    if (bootstrap) source = insertBootstrapMarkers(path, source)
    const rendered = replaceGeneratedBlock(source, generated)
    if (rendered === readFileSync(path, 'utf8')) continue
    if (check) stale.push(path)
    else writeFileSync(path, rendered, 'utf8')
  }

  if (stale.length > 0) {
    throw new Error(`stale MCP product documentation:\n${stale.map((path) => `- ${path}`).join('\n')}`)
  }
}

function runCli() {
  const args = process.argv.slice(2)
  const allowed = new Set(['--check', '--bootstrap'])
  if (args.some((arg) => !allowed.has(arg)) || args.length > 1) {
    throw new Error('usage: node scripts/render-product-docs.mjs [--check|--bootstrap]')
  }
  renderProductDocs({ check: args[0] === '--check', bootstrap: args[0] === '--bootstrap' })
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    runCli()
  } catch (error) {
    console.error(`${basename(process.argv[1])}: ${error instanceof Error ? error.message : String(error)}`)
    process.exitCode = 1
  }
}
