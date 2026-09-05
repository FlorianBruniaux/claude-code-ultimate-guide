# claude-code-ultimate-guide-mcp

<!-- mcp-product:start -->
[![npm version](https://img.shields.io/npm/v/claude-code-ultimate-guide-mcp)](https://www.npmjs.com/package/claude-code-ultimate-guide-mcp) [![npm downloads](https://img.shields.io/npm/dm/claude-code-ultimate-guide-mcp)](https://www.npmjs.com/package/claude-code-ultimate-guide-mcp) ![Node.js >=18.14.1](https://img.shields.io/badge/node-%3E%3D18.14.1-brightgreen) ![MIT license](https://img.shields.io/badge/license-MIT-blue)

Search the Claude Code Ultimate Guide, open exact source sections, inspect releases, and retrieve production templates from any MCP-compatible coding client.

## Install in 30 seconds

### Claude Code

Install for the current user:

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.1
```

For a project-scoped configuration, add this to `.mcp.json` at the repository root:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.1"]
    }
  }
}
```

### Codex

```bash
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.1
```

### Cursor

Add this server entry to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.1"]
    }
  }
}
```

### VS Code

Add this to `.vscode/mcp.json`:

```json
{
  "servers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.1"]
    }
  }
}
```

## Three useful sequences

1. Find and read: `search_guide({ query: "hooks" })`, then `read_section({ path: "..." })` with the returned path.
2. Discover and retrieve a template: `search_examples({ query: "pre-commit lint" })`, then `get_example({ name: "..." })`.
3. Track official documentation: run `init_official_docs()` once, then `refresh_official_docs()` and `diff_official_docs()` when you want a new comparison.

## Generated capabilities

This section is rendered from `machine-readable/mcp-product.json` for package 1.3.1 and guide 3.43.0.

| Capability | Count | Names |
| --- | ---: | --- |
| Tools | 17 | `compare_versions`, `diff_official_docs`, `get_changelog`, `get_cheatsheet`, `get_digest`, `get_example`, `get_release`, `get_threat`, `init_official_docs`, `list_examples`, `list_threats`, `list_topics`, `read_section`, `refresh_official_docs`, `search_examples`, `search_guide`, `search_official_docs` |
| Resources | 6 | `claude-code-guide://agent-harnesses`, `claude-code-guide://distribution-channels`, `claude-code-guide://llms`, `claude-code-guide://reference`, `claude-code-guide://releases`, `claude-code-guide://translations` |
| Prompts | 1 | `claude-code-expert` |
| Companion commands | 5 | `/ccguide:daily`, `/ccguide:diff-docs`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:search-docs` |

### Tools

| Tool | Description |
| --- | --- |
| `compare_versions` | Show what changed between two Claude Code CLI versions. Lists all releases in range with aggregated highlights and breaking changes. |
| `diff_official_docs` | Compare the baseline and current official Anthropic Claude Code docs snapshots. Shows added, removed, and modified pages. No network call - reads local files only. Run init_official_docs() first, then refresh_official_docs() when you want to update the current snapshot. |
| `get_changelog` | Return the last N entries from the Claude Code Ultimate Guide CHANGELOG. Shows what changed in the guide itself (not Claude Code CLI releases - use get_release() for that). |
| `get_cheatsheet` | Return the Claude Code cheatsheet - a compact 1-page reference covering the most important commands, shortcuts, config options, and workflows. |
| `get_digest` | Return a digest of guide and Claude Code CLI changes for a given period. Combines guide CHANGELOG entries + official Claude Code releases in the time window. |
| `get_example` | Fetch a production-ready template or example from the guide (agents, skills, commands, hooks, scripts). Pass a partial name to search for matching examples. |
| `get_release` | Get details about Claude Code CLI official releases. Pass a version to get a specific release, or omit to get the latest and recent history. |
| `get_threat` | Look up a specific threat by ID from the security threat database. Supports CVE IDs (e.g. "CVE-2025-53109") and technique IDs (e.g. "T001"). |
| `init_official_docs` | Fetch the official Anthropic Claude Code docs (llms-full.txt) and store a local snapshot as the diff baseline. Run this first. Safe to re-run - overwrites previous baseline AND current. Takes ~5s (fetches ~1.2MB from Anthropic). |
| `list_examples` | List all production-ready templates in the guide by category (agents, commands, hooks, skills, scripts). Use get_example(name) to fetch the content of any specific template. |
| `list_threats` | Browse the security threat database. Without a category, returns a summary with counts. With a category, returns the full list for that section. |
| `list_topics` | List all top-level topics and categories in the Claude Code Ultimate Guide. Useful for exploring what the guide covers before searching. |
| `read_section` | Read a section from a guide file (markdown, YAML, examples). Supports pagination via offset, or a "#heading-slug" anchor to jump straight to a section (as returned by search_guide()). Use after search_guide() to fetch the full content at a specific location. |
| `refresh_official_docs` | Re-fetch the official Anthropic Claude Code docs and update the "current" snapshot without touching the baseline. Run this to update the comparison target before diffing. Takes ~5s (fetches ~1.2MB from Anthropic). |
| `search_examples` | Semantic search across all production-ready templates by intent (e.g. "hook lint", "agent code review"). Different from get_example (exact name) and list_examples (category browse). |
| `search_guide` | Search the Claude Code Ultimate Guide by topic, keyword, or question. Covers features, hooks, agents, MCP, skills, commands, and best practices. Use this FIRST for any Claude Code question instead of web search. |
| `search_official_docs` | Search the official Anthropic Claude Code documentation by keyword or topic. Uses the local current snapshot - no network call. Run init_official_docs() first. |

### Resources

| Resource URI | MIME type | Description |
| --- | --- | --- |
| `claude-code-guide://agent-harnesses` | `application/json` | Evidence-backed Agent Harness Map dataset. Separates the broad source catalog, guide supplements, strict runtime map, and adjacent control planes. Unknown evidence is preserved as unknown. |
| `claude-code-guide://distribution-channels` | `text/yaml` | Publication channels, attributed URLs, asset states, dates, and 30-day outcome fields for the guide. |
| `claude-code-guide://llms` | `text/plain` | llms.txt - machine-readable identity and navigation file for the Claude Code Ultimate Guide. |
| `claude-code-guide://reference` | `text/yaml` | Complete structured index of the Claude Code Ultimate Guide. Use as fallback when search_guide() results are insufficient. |
| `claude-code-guide://releases` | `text/yaml` | Claude Code official releases history - condensed highlights and breaking changes for each version. |
| `claude-code-guide://translations` | `application/json` | Version, provenance, freshness, and coverage status for maintained and community translations of the guide. |

### Prompts

| Prompt | Description |
| --- | --- |
| `claude-code-expert` | Activate Claude Code expert mode with the optimal workflow for answering questions using the Ultimate Guide. |

### Companion Claude Code commands

The repository contains these command files. They are not installed by the npm package.

| Command | Description |
| --- | --- |
| `/ccguide:daily` | Daily update check - official Anthropic docs diff + guide/CC releases digest |
| `/ccguide:diff-docs` | Compare official Anthropic docs baseline vs current snapshot (no network - instant) |
| `/ccguide:init-docs` | Fetch official Anthropic Claude Code docs and store as local baseline snapshot |
| `/ccguide:refresh-docs` | Re-fetch official Anthropic Claude Code docs and update current snapshot (baseline unchanged) |
| `/ccguide:search-docs` | Search official Anthropic Claude Code docs by keyword |

## Local data, network, and cache behavior

The package bundles the reference index, release history, guide navigation, Agent Harness Map, and translation metadata. Initialization and list operations use bundled content and do not require the network.

`read_section`, `get_example`, `get_cheatsheet`, `get_changelog`, `get_digest`, and threat lookups can fetch files from GitHub when content is not available locally. Successful responses are written to `~/.cache/claude-code-guide/1.3.1/` for 24 hours; stale cached content is used when the network is unavailable. With `GUIDE_ROOT` set to a local guide checkout, these tools read that checkout instead.

`init_official_docs` and `refresh_official_docs` fetch Anthropic's official documentation and write a separate local snapshot under `~/.cache/claude-code-guide/`. `diff_official_docs` and `search_official_docs` read those snapshots.

## Privacy

The server has no first-party telemetry. MCP protocol messages use standard input and standard output. Network-capable tools contact GitHub or Anthropic only when invoked, and their local cache or snapshot writes stay on the machine running the server.

## Limitations

- Full guide Markdown is not bundled. A first uncached section, example, cheatsheet, changelog, digest, or threat lookup can require GitHub.
- Official-doc search and diff require a local snapshot created by `init_official_docs`.
- The five `/ccguide:*` companion commands must be installed from the repository separately.
- The MCP Registry listing is not advertised until its API returns the published namespace.

## Diagnostics

Verify the package binary and JSON-RPC surface with the MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector npx -y claude-code-ultimate-guide-mcp@1.3.1
```

For local development:

```bash
npm ci
npm run build
GUIDE_ROOT=.. node dist/index.js
```

## Technical guide and contributing

Read the [canonical technical guide](../guide/ecosystem/claude-code-guide-mcp.md) for the published-versus-candidate boundary, architecture, privacy, offline behavior, and dated statistics.

Issues and pull requests are welcome in the [Claude Code Ultimate Guide repository](https://github.com/FlorianBruniaux/claude-code-ultimate-guide). Run `npm run release:check` from `mcp-server/` before submitting package changes.
<!-- mcp-product:end -->
