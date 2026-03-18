# claude-code-ultimate-guide-mcp

MCP server for the [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) — search, read, and explore 20,000+ lines of documentation directly from Claude Code or any MCP-compatible client.

No need to clone the repo. The guide's structured index is bundled in the package (~130KB compressed), and file content is fetched from GitHub on demand with 24h local cache.

## Installation

### Quick start (npx)

Add to `~/.claude.json` (user-level, all projects):

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp"]
    }
  }
}
```

### Global install

```bash
npm install -g claude-code-ultimate-guide-mcp
```

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "claude-code-guide-mcp"
    }
  }
}
```

### Per-project

Add to `.claude/settings.json` at your repo root.

## Tools

### Search & Navigation

| Tool | Signature | Description |
|------|-----------|-------------|
| `search_guide` | `(query, limit?)` | Search by keyword or question across 882 indexed entries. Returns ranked results with GitHub links. |
| `read_section` | `(path, offset?, limit?)` | Read a file section with pagination (500 lines max per call). Returns GitHub + guide site links. |
| `list_topics` | `()` | Browse all 25 topic categories in the guide with entry counts. |

### Templates & Examples

| Tool | Signature | Description |
|------|-----------|-------------|
| `get_example` | `(name)` | Fetch a production-ready template by exact name (agents, hooks, commands, skills). |
| `list_examples` | `(category?)` | List all templates by category with GitHub links. Categories: `agents`, `commands`, `hooks`, `skills`, `scripts`. |
| `search_examples` | `(query, limit?)` | Semantic search across all templates by intent (e.g. `"hook lint"`, `"agent code review"`). |

### What's New

| Tool | Signature | Description |
|------|-----------|-------------|
| `get_changelog` | `(count?)` | Last N entries from the guide CHANGELOG (default 5, max 20). |
| `get_digest` | `(period)` | Combined digest of guide changes + Claude Code CLI releases. Period: `day`, `week`, `month`. |
| `get_release` | `(version?, count?)` | Claude Code CLI release details. Pass a version (e.g. `"2.1.59"`) or omit for latest + recent N. |
| `compare_versions` | `(from, to?)` | Diff between two Claude Code versions: aggregated highlights and breaking changes for all releases in range. |

### Security Intelligence

| Tool | Signature | Description |
|------|-----------|-------------|
| `get_threat` | `(id)` | Look up a CVE (e.g. `"CVE-2025-53109"`) or attack technique (e.g. `"T001"`) from the threat database. |
| `list_threats` | `(category?)` | Browse the threat database. Without category: global summary with counts. With category: full section list. Categories: `cves`, `authors`, `skills`, `techniques`, `mitigations`, `sources`. |

### Quick Reference

| Tool | Signature | Description |
|------|-----------|-------------|
| `get_cheatsheet` | `(section?)` | Full cheatsheet or filtered to a specific section (e.g. `"hooks"`, `"agents"`, `"mcp"`). |

## Resources

| URI | Description |
|-----|-------------|
| `claude-code-guide://reference` | Full structured index (94KB YAML, ~900 entries) — use as fallback when search isn't enough |
| `claude-code-guide://releases` | Claude Code official releases history (YAML) |
| `claude-code-guide://llms` | Guide identity/navigation file (llms.txt) |

## Prompts

| Prompt | Args | Description |
|--------|------|-------------|
| `claude-code-expert` | `question?` | Activates expert mode with optimal workflow: search → read → example → YAML fallback |

## Onboarding (first run)

After installing the MCP server, run this in any Claude Code session for a personalized guided tour:

```bash
claude "Use the claude-code-guide MCP server. Activate the claude-code-expert prompt, then run a personalized onboarding: ask me 3 questions about my goal, experience level, and preferred tone — then build a custom learning path using search_guide and read_section to navigate the guide with live source links."
```

This replaces the static URL-fetch approach with live search across 900+ indexed entries, always up to date, with GitHub + guide site links on every result.

## Usage examples

```
# Search
search_guide("hooks")
search_guide("cost optimization")
search_guide("custom agents")

# Read content
read_section("guide/ultimate-guide.md", 8077)
read_section("guide/cheatsheet.md")

# Templates
get_example("code-reviewer")
get_example("pre-commit hook")
list_examples("agents")
list_examples("hooks")
search_examples("hook lint")
search_examples("agent code review")

# What's new
get_digest("week")
get_digest("month")
get_changelog(10)
get_release()
get_release("2.1.59")
compare_versions("2.1.50", "2.1.59")
compare_versions("2.0.0")

# Security
get_threat("CVE-2025-53109")
get_threat("T001")
list_threats()
list_threats("cves")
list_threats("techniques")

# Quick reference
get_cheatsheet()
get_cheatsheet("hooks")
list_topics()
```

## Slash command shortcuts

Install the companion slash commands for one-keystroke access in Claude Code. They live in `.claude/commands/ccguide/` of the guide repo — copy or symlink to `~/.claude/commands/ccguide/` for global availability.

```bash
# From the guide repo root
cp -r .claude/commands/ccguide ~/.claude/commands/ccguide
```

Once installed, these commands are available in any Claude Code session:

| Command | Example | What it does |
|---------|---------|--------------|
| `/ccguide:search <query>` | `/ccguide:search hooks` | Search + auto-read top results |
| `/ccguide:cheatsheet [section]` | `/ccguide:cheatsheet hooks` | Full cheatsheet or filtered |
| `/ccguide:digest <period>` | `/ccguide:digest week` | Guide + CC releases digest |
| `/ccguide:example <name>` | `/ccguide:example code-reviewer` | Fetch a template |
| `/ccguide:examples [category]` | `/ccguide:examples agents` | List templates by category |
| `/ccguide:release [version]` | `/ccguide:release 2.1.59` | CC CLI release details |
| `/ccguide:changelog [count]` | `/ccguide:changelog 10` | Recent guide CHANGELOG |
| `/ccguide:topics` | `/ccguide:topics` | Browse all 25 categories |

## Custom agent

A `claude-code-guide` agent is included in `.claude/agents/claude-code-guide.md`. It uses Haiku (fast, cheap) and searches the guide automatically before answering Claude Code questions.

Copy to your `~/.claude/agents/` to use it globally:

```bash
cp .claude/agents/claude-code-guide.md ~/.claude/agents/claude-code-guide.md
```

Then invoke with: `use claude-code-guide agent to answer: how do I configure hooks?`

## Dev mode (local repo)

If you've cloned the guide repo, set `GUIDE_ROOT` to read files locally instead of fetching from GitHub:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/claude-code-ultimate-guide/mcp-server/dist/index.js"],
      "env": {
        "GUIDE_ROOT": "/path/to/claude-code-ultimate-guide"
      }
    }
  }
}
```

With `GUIDE_ROOT` set:
- YAML indexes loaded from the local repo (stays in sync with local changes)
- File content read directly from disk (no GitHub fetch, no cache)

## Bundled content

The npm package includes (~130KB compressed total):
- `content/reference.yaml` — 94KB structured index (~900 entries, ~882 indexed)
- `content/claude-code-releases.yaml` — 27KB releases history (76 releases)
- `content/llms.txt` — 8KB identity file

Guide markdown files (3.5MB) are **not** bundled — they're fetched from GitHub on demand and cached at `~/.cache/claude-code-guide/{version}/`.

## Cache

File content is cached at `~/.cache/claude-code-guide/{package-version}/` with 24h TTL. If offline, stale cache is served as fallback. If no cache exists and offline, tools return inline summaries from the YAML index instead.

## MCP Inspector

Test locally with the official MCP Inspector:

```bash
cd mcp-server
npm run build
GUIDE_ROOT=.. npx @modelcontextprotocol/inspector node dist/index.js
```
