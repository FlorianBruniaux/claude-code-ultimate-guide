# Claude Code Ultimate Guide MCP server

Technical reference for `claude-code-ultimate-guide-mcp`, the local stdio server that exposes this guide to MCP-compatible coding clients.

Status checked on 2026-08-31:

- public npm package: `1.2.10`
- public runtime handshake: `1.2.0`
- public runtime surface: 17 tools, 3 resources, 1 prompt
- repository release candidate: `1.3.0`
- candidate runtime surface: 17 tools, 5 resources, 1 prompt
- official MCP Registry: the namespace was not returned by the registry API

The public-package facts above were measured by starting `claude-code-ultimate-guide-mcp@1.2.10` and calling the MCP list methods. The candidate facts come from the generated [product manifest](../../machine-readable/mcp-product.json) and its live contract test.

## TL;DR

Use the MCP server when you want a coding client to search the guide, open the exact source section, retrieve a production template, or inspect Claude Code releases without loading the full guide into context.

The server runs locally over stdio. Version `1.3.0` has no first-party telemetry. Some tools can contact GitHub or Anthropic when invoked and can write local cache files. Downloads are not users, active installations, sessions, or executions.

Install the currently published package:

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.2.10
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.2.10
```

The `1.3.0` commands elsewhere in this release branch are release-candidate commands. They become runnable from npm only after `1.3.0` is published.

## What the server solves

The guide is too large to inject in full for every question. The MCP server provides a smaller discovery and retrieval loop:

1. search the structured guide index;
2. return matching paths and anchors;
3. read only the relevant source section;
4. fetch a specific template or release record when needed.

This reduces irrelevant context. It does not guarantee that an answer is correct, current, or appropriate for a specific repository. The client still has to inspect the retrieved source and verify time-sensitive claims.

## Install by client

All examples below use the public npm version observed on 2026-08-31. Pinning the version makes installation reproducible.

### Claude Code

User scope:

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.2.10
claude mcp list
```

Project scope in `.mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.2.10"]
    }
  }
}
```

Remove the user-scoped entry:

```bash
claude mcp remove --scope user claude-code-guide
```

### Codex

```bash
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.2.10
codex mcp list
```

Remove it with:

```bash
codex mcp remove claude-code-guide
```

### Cursor

Add this entry to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.2.10"]
    }
  }
}
```

### VS Code

Add this entry to `.vscode/mcp.json`:

```json
{
  "servers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.2.10"]
    }
  }
}
```

## First useful query

Ask the client:

> Search the Claude Code Ultimate Guide for session-scoped hooks. Open the most relevant source section and cite its path and heading.

The expected tool sequence is:

```text
search_guide({ query: "session-scoped hooks" })
read_section({ path: "<path returned by search_guide>" })
```

For a template, start with `search_examples`, then call `get_example` with the returned name. For official documentation changes, run `init_official_docs` once, then `refresh_official_docs` and `diff_official_docs` when you need a new comparison.

## Architecture and data flow

```text
MCP client
  -> local stdio process started through npx
     -> bundled indexes and datasets
     -> optional GitHub fetch for guide content and templates
     -> optional Anthropic fetch for official documentation snapshots
     -> local cache under ~/.cache/claude-code-guide/
```

The MCP protocol travels through the child process standard input and standard output. There is no hosted guide MCP endpoint in this architecture. The client controls when the local process starts and which tools it calls.

## Tools, resources, and prompt

The `1.3.0` candidate exposes the following generated contract:

| Capability | Count | Purpose |
| --- | ---: | --- |
| Tools | 17 | Search, source retrieval, templates, releases, threats, and official documentation snapshots |
| Resources | 5 | Reference index, release history, `llms.txt`, Agent Harness Map, and translation metadata |
| Prompts | 1 | `claude-code-expert` search and retrieval workflow |

Tools by workflow:

| Workflow | Tools |
| --- | --- |
| Guide discovery | `search_guide`, `read_section`, `list_topics` |
| Templates | `get_example`, `list_examples`, `search_examples` |
| Guide and release history | `get_changelog`, `get_digest`, `get_release`, `compare_versions`, `get_cheatsheet` |
| Security reference | `get_threat`, `list_threats` |
| Official Anthropic docs | `init_official_docs`, `refresh_official_docs`, `diff_official_docs`, `search_official_docs` |

Candidate resources:

- `claude-code-guide://reference`
- `claude-code-guide://releases`
- `claude-code-guide://llms`
- `claude-code-guide://agent-harnesses`
- `claude-code-guide://translations`

The candidate searches 1,755 generated index entries. The public `1.2.10` package exposes only the first three resources. The Agent Harness Map and translation metadata are candidate additions until `1.3.0` is published.

## Bundled content, GitHub fetch, and cache

The package bundles the structured reference, release history, guide navigation, and other declared resource datasets. Initialization, list operations, and guide search use bundled data.

These tools can fetch content from GitHub when a local checkout or usable cache entry is not available:

- `read_section`
- `get_example`
- `get_cheatsheet`
- `get_changelog`
- `get_digest`
- `get_threat`
- `list_threats`

Successful GitHub responses can be cached under `~/.cache/claude-code-guide/<version>/` for 24 hours. When `GUIDE_ROOT` points to a local guide checkout, content tools read from that checkout instead.

`init_official_docs` and `refresh_official_docs` fetch Anthropic documentation and store separate local snapshots. `diff_official_docs` and `search_official_docs` read those snapshots without making a network request.

## Network and privacy boundary

Version `1.3.0` has no first-party telemetry, analytics endpoint, device identifier, or event upload. MCP requests and responses are not sent to this project's author.

Network access is tool-specific:

| Operation | Network | Local write |
| --- | --- | --- |
| List capabilities and search bundled index | No | No |
| Read uncached guide content or templates | GitHub, when needed | 24-hour cache |
| Initialize or refresh official docs | Anthropic | Local snapshots |
| Diff or search existing official-doc snapshots | No | No |

The MCP client, npm, `npx`, GitHub, Anthropic, and the machine operator can have their own logs or policies. Those systems are outside this server's first-party telemetry boundary.

### Telemetry decision for 1.3.0

Centralized product telemetry is deliberately not implemented in `1.3.0`. Download counts do not justify adding a tracking endpoint, and they cannot establish active usage.

Any future proposal requires a reviewed privacy decision before code exists. The minimum acceptance criteria are:

- disabled by default and enabled by an explicit user action;
- no query text, arguments, file paths, returned content, repository identity, hostname, or account identity;
- a locally generated random identifier that the user can reset;
- only package version, tool name, success or failure, and coarse latency;
- a documented endpoint, retention period, deletion process, and exact payload schema;
- an immediate disable mechanism and a public way to inspect emitted events.

Until those conditions are approved and implemented, the accurate claim is no first-party telemetry.

## Offline behavior

The server is partially offline, not fully offline.

- capability listing, topic listing, release data, resources, and index search work from bundled content;
- cached guide content can be read while the cache remains usable;
- uncached Markdown sections and templates can require GitHub;
- official-doc search and diff require snapshots previously created with network access;
- the first `npx` execution can require npm registry access unless the package is already cached or installed.

For development or controlled offline use, install dependencies ahead of time, build the package, and start `dist/index.js` from a local checkout with `GUIDE_ROOT` set.

## Compatibility

| Requirement | Candidate `1.3.0` |
| --- | --- |
| Transport | local stdio |
| Node.js | `>=18.14.1` |
| MCP SDK | `@modelcontextprotocol/sdk` `1.30.0` |
| Tested client configuration shapes | Claude Code, Codex, Cursor, VS Code |
| Package manager entry point | `npx` |

Other MCP clients can work if they support local stdio servers and the same command-plus-arguments model. That statement is protocol compatibility, not a claim that every client release has been tested.

## Limitations

- The full guide Markdown is not bundled.
- The npm package version and its MCP handshake version can diverge. Public `1.2.10` reports `1.2.0`; the `1.3.0` candidate derives the handshake from `package.json` and tests that contract.
- The official MCP Registry namespace is prepared but was absent from the registry API snapshot on 2026-08-31.
- Companion `/ccguide:*` command files live in the repository and are not installed by the npm package.
- Search retrieves candidate sections; it does not replace source review or freshness checks.
- No metric in this repository measures active users.

## Troubleshooting

| Symptom | Check | Action |
| --- | --- | --- |
| Client cannot start the server | `node --version` and `npx --version` | Use Node.js `>=18.14.1` and verify npm registry access |
| Client shows no tools | `claude mcp list` or `codex mcp list` | Check the server name, command, arguments, and configuration scope |
| `1.3.0` cannot be downloaded | `npm view claude-code-ultimate-guide-mcp version` | Use public `1.2.10` until the candidate is published |
| Source read fails offline | Inspect `~/.cache/claude-code-guide/` | Retry with network access, set `GUIDE_ROOT`, or prefill the cache through an earlier successful read |
| Official-doc search says no snapshot exists | Check the official-doc cache directory | Run `init_official_docs`, which requires Anthropic network access |
| Configuration is stale | Remove and re-add the server | Use the client-specific removal command shown above |

Inspect the JSON-RPC surface with the MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector npx -y claude-code-ultimate-guide-mcp@1.2.10
```

## Version and dated npm statistics

Two machine-readable snapshots serve different questions:

- [mcp-stats.json](../../machine-readable/mcp-stats.json) records npm package history, daily distribution, and official-registry presence.
- [mcp-dashboard.json](../../machine-readable/mcp-dashboard.json) records one completed calendar month across npm, GSC, and GA4 with explicit availability states.

### Public package snapshot

Snapshot time: `2026-08-31T15:06:00Z`. Last complete UTC day: 2026-08-30. Unit: npm package downloads.

| Period | Downloads |
| --- | ---: |
| Since launch, 2026-02-28 through 2026-08-30 | 8,590 |
| Year to date, 2026-01-01 through 2026-08-30 | 8,590 |
| Trailing 30 complete days, 2026-08-01 through 2026-08-30 | 5,252 |
| Trailing 7 complete days, 2026-08-24 through 2026-08-30 | 125 |

For the trailing 30 complete days, the daily median was 31.5, the mean was 175.1, the maximum was 727, and the median absolute deviation was 31.5. The mean is strongly affected by recorded spikes. The snapshot preserves those observations but does not assign a cause.

### Reproducible monthly dashboard

The completed July 2026 UTC snapshot records 1,459 npm downloads. GSC for the landing page, GSC for the portfolio page, and GA4 for the portfolio page are marked `unavailable` because the required Google access and property configuration were absent during collection. They are not reported as zero.

The monthly workflow uses exact page URL or path filters, publishes aggregate page and package metrics only, and keeps missing sources explicit. npm downloads can include installs, CI runs, cache misses, bots, and repeated downloads. They do not identify unique or active people.

## Changelog and source

- [MCP package README](../../mcp-server/README.md)
- [Generated product contract](../../machine-readable/mcp-product.json)
- [Monthly dashboard collector](../../scripts/collect-mcp-dashboard.py)
- [Guide changelog](../../CHANGELOG.md)
- [Source repository](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)
- [npm package](https://www.npmjs.com/package/claude-code-ultimate-guide-mcp)

Release changes must update the generated product manifest, pass `npm run release:check` in `mcp-server/`, and keep the public-package snapshot separate from unreleased candidate capabilities.
