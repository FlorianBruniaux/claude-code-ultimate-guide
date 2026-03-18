---
title: "MCP Servers Ecosystem"
description: "Validated community MCP servers evaluated for production readiness and security"
tags: [mcp, reference, integration]
---

# MCP Servers Ecosystem

**Last updated**: February 2026 • **Next review**: March 2026

This guide covers validated community MCP servers beyond the official Anthropic servers. All servers listed have been evaluated for production readiness, maintenance activity, and security.

> **Not sure whether to use an MCP server or a CLI tool?** See the [MCP vs CLI Decision Guide](./mcp-vs-cli.md) for a full breakdown of tradeoffs, a decision matrix, and guidance by situation.

## Table of Contents

- [Official vs Community Servers](#official-vs-community-servers)
- [Evaluation Framework](#evaluation-framework)
- [Ecosystem Evolution](#ecosystem-evolution)
- [Validated Community Servers](#validated-community-servers)
  - [Browser Automation](#browser-automation)
  - [DevOps & Infrastructure](#devops--infrastructure)
  - [Security & Code Analysis](#security--code-analysis)
  - [Code Search & Analysis](#code-search--analysis)
  - [Documentation & Knowledge](#documentation--knowledge)
  - [Project Management](#project-management)
  - [Orchestration](#orchestration)
- [Production Deployment](#production-deployment)
- [Monthly Watch Methodology](#monthly-watch-methodology)
- [Excluded Servers](#excluded-servers)

---

## Official vs Community Servers

| Type | Examples | Characteristics | Use When |
|------|----------|-----------------|----------|
| **Official** | filesystem, memory, brave-search, github | Anthropic-maintained, guaranteed stability | Default choice, core functionality |
| **Community** | Playwright, Semgrep, Kubernetes | Maintained by orgs/individuals, can be production-ready | Specialized needs, ecosystem integration |

**Key difference**: Official servers have Anthropic SLA backing, community servers require individual evaluation.

---

## Evaluation Framework

All community servers are evaluated against these criteria:

| Criterion | Threshold | Justification |
|-----------|-----------|---------------|
| **GitHub Stars** | ≥50 | Minimum community validation |
| **Recent Release** | <3 months | Active maintenance |
| **Documentation** | README + examples + config | Reduces adoption friction |
| **Tests/CI** | ✅ Automated | Ensures stability |
| **Use Case** | Not covered by official servers | Avoids redundancy |
| **License** | OSS required | Sustainability and auditability |

**Quality Score Components**:
- Maintenance (10 points): Release frequency, issue response time
- Documentation (10 points): README completeness, examples, troubleshooting
- Tests (10 points): Test coverage, CI/CD automation
- Performance (10 points): Response time, resource efficiency
- Adoption (10 points): Community usage, production deployments

**Total Score**: `/50` → Normalized to `/10` for final rating.

---

## Ecosystem Evolution

**Major developments (January 2026)**:

### Linux Foundation Standardization

MCP becomes official standard via **Agentic AI Foundation** under Linux Foundation governance.

- **Announcement**: [YouTube - Linux Foundation](https://www.youtube.com/watch?v=btNbIY7KYwg)
- **Impact**: Enterprise adoption, long-term stability guarantee

### Advanced MCP Tool Use

Anthropic deploys optimizations for MCP context management:

- **Deferred loading**: Tools loaded on-demand, not upfront
- **Search-based tools**: Efficient tool discovery in large sets
- **Announcement**: [Josh Twist LinkedIn](https://www.linkedin.com/posts/joshtwist_anthropic-recently-dropped-advanced-mcp-activity-7399492619581718528-g-Ip)

### MCPB Bundle Format

Standardized bundle format for one-click MCP server installation (replaces runtime dependency management).

- **Discussion**: [Reddit - r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1qkzdh0/mcp_server_installs_are_nondeterministic_heres/)
- **Benefit**: Deterministic installations, reduced setup friction

### MCP Apps (Interactive Work Tools)

Claude now supports interactive tools via MCP Apps spec:

- **Examples**: Slack drafting, Figma diagrams, Asana timelines
- **Announcement**: [Smol.ai Newsletter](https://news.smol.ai/issues/26-01-26-mcp-apps)
- **Deep dive**: See [guide/architecture.md:656](../core/architecture.md#mcp-extensions-apps-sep-1865)

### IDE Integration

**Visual Studio 2026** natively integrates Azure MCP Server, GitHub Copilot Chat, and MCP clients.

- **Announcement**: [Microsoft DevBlogs](https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/)

---

## Version Control (Official Servers)

These foundational MCP servers provide version control automation for all development workflows. **Official Anthropic servers** with guaranteed stability.

### Git MCP (Anthropic)

**Official Anthropic server** for Git repository interaction via Model Context Protocol. Provides programmatic access to Git operations with structured output and cross-platform safety.

**Repository**: [modelcontextprotocol/servers/git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
**License**: MIT
**Status**: Early development (API subject to change)
**Stars**: 77,908+ (parent repo)

**Use Cases**:
- **Automated commit workflows**: AI generates commit messages, stages changes, commits
- **Log analysis**: Filter commits by date, author, branch with structured output
- **Branch management**: Create feature branches, checkout, filter by SHA
- **Token-efficient diffs**: Control context lines for focused code reviews
- **Multi-repo automation**: Manage multiple repositories in monorepo setups

#### Key Features

| Tool | Description | Parameters |
|------|-------------|------------|
| `git_status` | Working tree status (staged, unstaged, untracked) | - |
| `git_log` | Commit history with advanced filtering | `max_count`, `skip`, `start_timestamp`, `end_timestamp`, `author` |
| `git_diff` | Diff between commits/branches | `target`, `source`, `context_lines` |
| `git_diff_unstaged` | Unstaged changes | `context_lines` |
| `git_diff_staged` | Staged changes | `context_lines` |
| `git_commit` | Create commit | `message` |
| `git_add` | Stage files/patterns | `files` |
| `git_reset` | Unstage files | `files` |
| `git_branch` | List/filter branches | `contains`, `not_contains` |
| `git_create_branch` | Create new branch | `name` |
| `git_checkout` | Switch branches/commits | `ref` |
| `git_show` | Show commit details | `revision` |

**Advanced Filtering** (`git_log`):
- **ISO 8601 dates**: `2024-01-15T14:30:25`
- **Relative dates**: `2 weeks ago`, `yesterday`, `last month`
- **Absolute dates**: `2024-01-15`, `Jan 15 2024`
- **Author filtering**: `--author="John Doe"`

#### Setup

**Installation (3 methods)**:

```bash
# Method 1: UV (recommended) - one-liner
uvx mcp-server-git --repository /path/to/repo

# Method 2: pip + Python module
pip install mcp-server-git
python -m mcp_server_git

# Method 3: Docker (sandboxed)
docker run -v /path/to/repo:/repo ghcr.io/modelcontextprotocol/mcp-server-git
```

**Claude Code Configuration** (`~/.claude.json`):

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/Users/you/projects/myrepo"]
    }
  }
}
```

**Multi-repo support**:

```json
{
  "mcpServers": {
    "git-main": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/main-repo"]
    },
    "git-docs": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/docs-repo"]
    }
  }
}
```

#### IDE Integrations

**One-click install buttons available for**:
- **Claude Desktop** (macOS/Windows/Linux)
- **VS Code** (Stable + Insiders)
- **Zed**
- **Zencoder**

See [official README](https://github.com/modelcontextprotocol/servers/tree/main/src/git#quickstart) for integration links.

#### Quality Score

**8.5/10** ⭐⭐⭐⭐⭐

| Criterion | Score | Notes |
|-----------|-------|-------|
| Maintenance | 10/10 | Anthropic-backed, active development |
| Documentation | 9/10 | Comprehensive README, examples, but early dev warnings |
| Tests | 8/10 | Automated CI, improving coverage |
| Performance | 8/10 | Fast (<100ms), structured output reduces tokens |
| Adoption | 8/10 | Official server, 77K+ stars, wide IDE support |

#### Limitations & Workarounds

| Limitation | Workaround |
|------------|-----------|
| **Early development** (API changes) | Pin version in production, monitor releases |
| **No interactive rebase** (`-i` flag) | Use Bash tool for `git rebase -i` |
| **No reflog support** | Use Bash tool for `git reflog` |
| **No git bisect** | Use Bash tool for `git bisect` |
| **Single repo per instance** | Configure multiple MCP server instances |

#### Decision Matrix: Git MCP vs GitHub MCP vs Bash Tool

**When to use which tool**:

| Operation | Git MCP | GitHub MCP | Bash Tool | Justification |
|-----------|---------|------------|-----------|---------------|
| **Local commits** | ✅ Best | ❌ | ⚠️ OK | Structured output, cross-platform safe |
| **Branch management** | ✅ Best | ❌ | ⚠️ OK | `git_branch` filtering, SHA contains/excludes |
| **Diff/log analysis** | ✅ Best | ❌ | ⚠️ OK | `context_lines` control, token-efficient |
| **Staging files** | ✅ Best | ❌ | ⚠️ OK | Pattern matching (`git_add`), safer |
| **PR creation** | ❌ | ✅ Best | ⚠️ gh CLI | GitHub API, labels, assignees, reviewers |
| **Issue management** | ❌ | ✅ Best | ⚠️ gh CLI | GitHub-specific operations |
| **CI/CD status checks** | ❌ | ✅ Best | ⚠️ gh CLI | GitHub Actions integration |
| **Interactive rebase** | ❌ | ❌ | ✅ Best | Git MCP doesn't support `-i` flag |
| **Reflog recovery** | ❌ | ❌ | ✅ Best | Advanced Git operations |
| **Git bisect debugging** | ❌ | ❌ | ✅ Best | Complex debugging workflows |
| **Multi-tool pipelines** | ✅ | ✅ | ❌ | MCP servers compose with other MCP tools |

**Decision Tree**:

```
Is it a GitHub-specific operation (PRs, Issues, Actions)?
├─ YES → Use GitHub MCP
└─ NO → Is it a core Git operation (commit, branch, diff, log)?
    ├─ YES → Use Git MCP (structured, safe, token-efficient)
    └─ NO → Is it an advanced Git feature (rebase -i, reflog, bisect)?
        ├─ YES → Use Bash tool (flexibility)
        └─ NO → Default to Git MCP (safer, structured)
```

**Workflow Examples**:

| Workflow | Tool Chain | Justification |
|----------|-----------|---------------|
| **Feature development** | Git MCP (`git_create_branch` + `git_commit`) → GitHub MCP (PR) | Atomic, structured, full lifecycle |
| **Commit history analysis** | Git MCP (`git_log` with `start_timestamp: "2 weeks ago"`) | Token-efficient filtering, relative dates |
| **Code review preparation** | Git MCP (`git_diff` with `context_lines: 3`) | Focused context, reduced tokens |
| **Clean up commits (rebase)** | Bash tool (`git rebase -i HEAD~5`) | Interactive mode not in Git MCP |
| **Recover lost commits** | Bash tool (`git reflog`) | Reflog not exposed in Git MCP |
| **Bug hunting with bisect** | Bash tool (`git bisect start/good/bad`) | Bisect workflow not in Git MCP |
| **Automated release flow** | Git MCP (commit + tag) → GitHub MCP (create release) | Full automation, structured |

#### Resources

- **GitHub**: https://github.com/modelcontextprotocol/servers/tree/main/src/git
- **Parent Repo**: https://github.com/modelcontextprotocol/servers (77,908+ stars)
- **MCP Inspector**: Debug tool support for live testing
- **Docker Hub**: `ghcr.io/modelcontextprotocol/mcp-server-git`

---

## Validated Community Servers

### Browser Automation

#### Playwright MCP (Microsoft)

**Official Microsoft server** for browser automation optimized for LLMs. Uses accessibility trees instead of screenshots, reducing token usage.

**Use Case**: AI coding agents verify their work in browsers (E2E testing, bug verification).

**Key Features**:

| Capability | Details |
|------------|---------|
| Browser Automation | Navigate, click, fill, hover (Playwright API) |
| Content Extraction | Structured data via accessibility trees |
| Screenshots | Full-page + element-specific |
| JavaScript Execution | Run code in page context |
| Session Management | Persistent browser state |
| Supported Browsers | Chromium, Firefox, WebKit |

**Setup**:

```bash
# Installation
npm install @microsoft/playwright-mcp
# or
npx @microsoft/playwright-mcp
```

**Claude Code Configuration** (`~/.claude.json`):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["--yes", "@microsoft/playwright-mcp"]
    }
  }
}
```

**Example Usage**:

```
User: "Navigate to example.com, log in with email test@example.com, then take a screenshot"

Claude: [Uses playwright_navigate → playwright_type → playwright_click → playwright_screenshot]

Result: Screenshot + accessibility tree in context
```

**Quality Score**: **8.8/10** ⭐⭐⭐⭐⭐

| Dimension | Score | Notes |
|-----------|-------|-------|
| Maintenance | 9/10 | Bi-weekly releases, active Microsoft team |
| Documentation | 9/10 | README complete, examples, Playwright Live videos |
| Tests | 10/10 | Extensive test suite, CI/CD automated |
| Performance | 8/10 | Fast snapshots (~200ms), memory-efficient |
| Adoption | 8/10 | 2890+ uses (Smithery.ai tracking) |

**Limitations & Workarounds**:

| Limitation | Workaround |
|------------|-----------|
| Single browser session | Use session ID to persist state |
| No cross-domain iframe access | Restrict to same-origin content |
| Screenshot size limits (4K max) | Use element snapshots for large pages |

**Alternatives**:

| Server | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Playwright MCP** | Accessibility trees, LLM-native | No vision model support |
| Browserbase MCP | Cloud-based, stealth mode | API costs, latency |
| Puppeteer MCP | Lightweight, JS-only | Less structured data |

**Resources**:
- **GitHub**: https://github.com/microsoft/playwright-mcp
- **Releases**: https://github.com/microsoft/playwright-mcp/releases
- **Playwright Live Demo**: https://youtu.be/CNzg1aPwrKI

---

#### Browserbase MCP

**Official Browserbase server** for cloud browser automation. Includes Stagehand AI agent for autonomous task execution.

**Use Case**: Complex web interactions requiring stealth mode, proxy support, or autonomous execution (web scraping, form filling, data extraction).

**Key Features**:

| Capability | Details |
|------------|---------|
| Browser Control | Chromium via Browserbase cloud |
| Stagehand Agent | Autonomous task execution (e.g., "book a flight") |
| Data Extraction | CSS selectors + schema-based structured extraction |
| Anti-Detection | Stealth mode, proxy support, rotation |
| Multi-Model | OpenAI, Claude, Gemini, custom LLM |

**Setup**:

```bash
npm install @browserbasehq/mcp-server-browserbase
```

**Configuration**:

```json
{
  "mcpServers": {
    "browserbase": {
      "command": "npx",
      "args": ["@browserbasehq/mcp-server-browserbase"],
      "env": {
        "BROWSERBASE_API_KEY": "YOUR_KEY",
        "BROWSERBASE_PROJECT_ID": "YOUR_PROJECT_ID",
        "GEMINI_API_KEY": "YOUR_GEMINI_KEY"
      }
    }
  }
}
```

**Quality Score**: **7.6/10** ⭐⭐⭐⭐

**Cost**: Freemium (paid API usage), ~$0.10/session

**Limitations**:

| Limitation | Workaround |
|------------|-----------|
| Latency (~500ms cloud) | Batch operations, cache results |
| API costs | Use for high-value extractions only |
| Stagehand limitations | Fall back to manual playwright_* tools |

**Resources**:
- **GitHub**: https://github.com/browserbase/mcp-server-browserbase
- **Official Docs**: https://www.browserbase.com

---

#### Chrome DevTools MCP

**Official Anthropic server** for Chrome DevTools Protocol integration. Provides debugging and inspection capabilities via Chrome's native DevTools APIs.

**Use Case**: Debugging web applications, inspecting runtime state, monitoring network requests, and analyzing performance. Complements Playwright MCP (testing) with development-focused debugging capabilities.

**Key Features**:

| Capability | Details |
|------------|---------|
| Console Access | Read browser console logs, errors, warnings |
| Network Monitor | Inspect HTTP requests, responses, headers |
| DOM Inspection | Query DOM structure, element properties |
| JavaScript Execution | Execute arbitrary JS in page context |
| Performance Profiling | CPU profiles, memory snapshots |

**Setup**:

```bash
npm install @modelcontextprotocol/server-chrome-devtools
```

**Configuration**:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-chrome-devtools"]
    }
  }
}
```

**When to Use**:

| Scenario | Use Chrome DevTools MCP | Use Playwright MCP |
|----------|------------------------|-------------------|
| Debug runtime errors | ✅ Console logs, stack traces | ❌ Limited error visibility |
| Inspect network calls | ✅ Full request/response details | ⚠️ Basic navigation only |
| Test user interactions | ❌ Not designed for testing | ✅ Click, type, navigate |
| Profile performance | ✅ CPU/memory profiling | ❌ No profiling tools |
| Automate workflows | ❌ Manual debugging focus | ✅ E2E test automation |

**Limitations**:
- Requires Chrome browser running with DevTools Protocol enabled
- Manual setup (launch Chrome with `--remote-debugging-port`)
- Not suitable for automated testing (use Playwright for that)
- Performance overhead when profiling enabled

**Resources**:
- **npm**: https://www.npmjs.com/package/@modelcontextprotocol/server-chrome-devtools
- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/

---

### DevOps & Infrastructure

#### Kubernetes MCP (Red Hat)

**Official Containers Community server** (Red Hat-backed) for Kubernetes/OpenShift management in natural language.

**Use Case**: DevOps/SRE uses Claude to query/configure cluster ("kubectl in natural language").

**Key Features**:

| Capability | Details |
|------------|---------|
| Resource CRUD | Create, Read, Update, Delete any K8s resource |
| Pod Operations | Logs, events, exec, metrics (top) |
| Deployment Management | Scale, rollout, status |
| Config Management | View/update ConfigMaps, Secrets |
| CRD Support | Custom Resource Definitions |
| Multi-Cluster | Switch kubeconfig contexts |
| OpenShift Support | Native OpenShift resources |

**Setup**:

```bash
# Docker
docker run -it --rm \
  --mount type=bind,src=$HOME/.kube/config,dst=/home/mcp/.kube/config \
  ghcr.io/containers/kubernetes-mcp-server

# Native (Go binary)
go install github.com/containers/kubernetes-mcp-server@latest
kubernetes-mcp-server
```

**Claude Desktop Configuration**:

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=/home/user/.kube/config,dst=/home/mcp/.kube/config",
        "ghcr.io/containers/kubernetes-mcp-server"
      ]
    }
  }
}
```

**Example Usage**:

```
User: "Show me all pods in production namespace with memory usage >500Mi"
Claude: [Uses list_resources for pods + metrics]
Result: List of pods with memory stats

User: "Scale the backend deployment to 5 replicas"
Claude: [Uses patch_resource]
Result: Deployment scaled
```

**Quality Score**: **8.4/10** ⭐⭐⭐⭐

**Security**: RBAC enforcement, kubeconfig auth, no privilege escalation

**Limitations**:

| Limitation | Workaround |
|------------|-----------|
| Requires kubeconfig access | Use ServiceAccount + RBAC for safety |
| Limited node shell access | Use `kubectl exec` for debugging |
| CRD discovery lag | Pre-document CRDs for AI context |

**Resources**:
- **GitHub**: https://github.com/containers/kubernetes-mcp-server
- **Red Hat Docs**: https://developers.redhat.com/articles/2025/09/25/kubernetes-mcp-server-ai-powered-cluster-management

---

#### Vercel MCP

**Community server** for Vercel platform (deployments, projects, env vars, teams).

**Use Case**: AI assistant generates Next.js code, creates Vercel project, configures env vars, triggers deployment — full CI/CD loop without leaving IDE.

**Key Features**:

| Capability | Details |
|------------|---------|
| Deployments | List, get details, create, monitor status |
| Projects | List, create, update settings |
| Environment Variables | Get, set, manage secrets |
| Teams | List, create, manage |
| Domains | List, configure, DNS management |
| Functions | Monitor Vercel Functions, logs |

**Setup**:

```bash
git clone https://github.com/nganiet/mcp-vercel
cd vercel-mcp
npm install
```

**Configuration**:

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npm",
      "args": ["start"],
      "env": {
        "VERCEL_API_TOKEN": "YOUR_VERCEL_TOKEN"
      }
    }
  }
}
```

**Quality Score**: **7.6/10** ⭐⭐⭐⭐

**Note**: Vercel also has an official MCP server. This community version offers comprehensive API coverage.

**Resources**:
- **GitHub**: https://github.com/nganiet/mcp-vercel
- **Vercel Docs**: https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel
- **Official Vercel MCP**: https://vercel.com/docs/mcp/vercel-mcp

---

### Security & Code Analysis

#### Semgrep MCP

**Official Semgrep server** for vulnerability scanning (SAST, secrets, supply chain). Includes custom rules engine.

**Use Case**: Claude Code generates code, Semgrep automatically scans for security issues, proposes fixes ("secure by default").

**Key Features**:

| Capability | Details |
|------------|---------|
| Quick Scan | Fast security check on code snippet |
| Full Scan | Comprehensive SAST using p/ci ruleset |
| Custom Rules | Scan with user-provided Semgrep rules |
| AST Generation | Abstract Syntax Tree for analysis |
| Ruleset Support | Pre-built rulesets (OWASP, CWE, etc.) |
| Language Coverage | Python, JS/TS, Java, Go, C#, Rust, PHP, etc. |

**Setup**:

```bash
# Via uvx (recommended)
uvx semgrep-mcp

# Or pip
pip install semgrep-mcp
```

**Claude Code Configuration**:

```bash
claude mcp add semgrep -- uvx semgrep-mcp
```

**Cursor Configuration** (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "semgrep": {
      "command": "uvx",
      "args": ["semgrep-mcp"],
      "env": {
        "SEMGREP_APP_TOKEN": "your_token"
      }
    }
  }
}
```

**Example Usage**:

```
User: "Scan this Python code for SQL injection vulnerabilities"

Code:
  def search(query):
      return db.execute(f"SELECT * FROM users WHERE name = '{query}'")

Claude: [Uses security_check tool]

Result: [VULNERABLE] SQL injection detected at line 2.
  Fix: Use parameterized queries:
  return db.execute("SELECT * FROM users WHERE name = ?", [query])
```

**Quality Score**: **9.0/10** ⭐⭐⭐⭐⭐

| Dimension | Score | Notes |
|-----------|-------|-------|
| Maintenance | 10/10 | Official, frequent releases |
| Documentation | 9/10 | Comprehensive docs, examples |
| Tests | 10/10 | Extensive test coverage |
| Performance | 7/10 | Good, complexity-dependent (~500ms per scan) |
| Adoption | 9/10 | Enterprise standard (5000+ companies) |

**Alternatives**:

| Server | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Semgrep** | Comprehensive SAST, custom rules | Slower on large codebases |
| GitGuardian | Secrets-focused, fast | Limited SAST coverage |
| SonarQube | Enterprise, detailed reports | Heavier, more setup |

**Resources**:
- **GitHub**: https://github.com/semgrep/mcp
- **Official Docs**: https://semgrep.dev/docs/mcp
- **Rules Registry**: https://semgrep.dev/r
- **Pricing**: https://semgrep.dev/pricing (free tier for MCP)

---

### Code Search & Analysis

#### Grepai MCP

**Community server** for semantic code search and call graph analysis via local Ollama embeddings. Searches code by intent ("payment flow", "auth logic") instead of exact patterns, and traces function call relationships.

**Repository**: [yoanbernabeu/grepai](https://github.com/yoanbernabeu/grepai)
**License**: MIT
**Status**: Active development
**Privacy**: Fully local (Ollama + nomic-embed-text), no data leaves your machine

**Use Case**: Developer needs to understand unfamiliar codebase → grepai finds relevant code by natural language description and maps function dependencies, without reading entire files.

**Key Features**:

| Capability | Details |
|------------|---------|
| `grepai_search` | Semantic search by natural language query (e.g., "error handling middleware") |
| `grepai_trace_callers` | Find all functions that call a given symbol |
| `grepai_trace_callees` | Find all functions called by a given symbol |
| `grepai_trace_graph` | Full call graph (callers + callees) with configurable depth |
| `grepai_index_status` | Health check: indexed files, chunks, configuration |

**Token Efficiency**:

| Workflow | Tokens | Verdict |
|----------|--------|---------|
| Grep + Read files (brute force) | ~15K | Noisy, lots of irrelevant context |
| grepai search + trace | ~4K | Targeted, relevant results only |
| grepai alone (no follow-up) | ~2-3K | Fast discovery |

**Setup**:

```bash
# Install grepai
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh

# Install Ollama + embedding model
brew install ollama
ollama pull nomic-embed-text

# Initialize in your project
cd /path/to/project
grepai init  # Choose: ollama, nomic-embed-text, gob

# Index your codebase
grepai index

# Optional: watch for file changes (auto-reindex)
grepai watch
```

**Claude Code Configuration**:

```bash
claude mcp add grepai -- grepai mcp
```

**`.mcp.json` (project-scoped)**:

```json
{
  "mcpServers": {
    "grepai": {
      "command": "grepai",
      "args": ["mcp"]
    }
  }
}
```

**Example Usage**:

```
User: "Find the authentication flow in this codebase"

Claude: [Uses grepai_search query="authentication flow" limit=5]

Result: 3 relevant files with line numbers and similarity scores
  - src/auth/middleware.ts:12-45 (0.89)
  - src/routes/login.ts:8-32 (0.85)
  - src/utils/jwt.ts:1-28 (0.78)

User: "What calls the validateToken function?"

Claude: [Uses grepai_trace_callers symbol="validateToken"]

Result: Call graph showing 4 callers across 3 files
  - authMiddleware → validateToken
  - refreshHandler → validateToken
  - wsAuthGuard → validateToken
  - testHelper → validateToken
```

**Quality Score**: **7.8/10** ⭐⭐⭐⭐

| Dimension | Score | Notes |
|-----------|-------|-------|
| Maintenance | 8/10 | Active development, responsive maintainer |
| Documentation | 7/10 | Good README, MCP integration docs |
| Tests | 7/10 | CI present, growing coverage |
| Performance | 8/10 | Fast local embeddings (~2s search), no network latency |
| Adoption | 9/10 | Growing community, production use in Claude Code setups |

**Limitations & Workarounds**:

| Limitation | Workaround |
|------------|-----------|
| Requires Ollama running locally | `brew services start ollama` (auto-start) |
| Index can become stale | Use `grepai watch` for auto-reindex |
| Not ideal for exact pattern matching | Use native Grep tool for regex patterns |
| Embedding model download (~270MB) | One-time `ollama pull nomic-embed-text` |

**Alternatives**:

| Server | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Grepai** | Local, private, semantic + call graphs | Requires Ollama setup |
| Native Grep | Instant, exact patterns | No semantic understanding |
| GitHub Code Search | Cloud-based, cross-repo | Requires GitHub, no call graphs |

**Cross-reference**: See [ultimate-guide.md — MCP Servers: Grepai](./ultimate-guide.md) for detailed usage patterns, prompt strategies, and integration with other MCP servers.

**Resources**:
- **GitHub**: https://github.com/yoanbernabeu/grepai
- **Ollama**: https://ollama.com
- **Embedding Model**: nomic-embed-text (nomic-ai)

---

### Documentation & Knowledge

#### Context7 MCP

**Official Upstash server** for real-time library documentation (LangChain, Anthropic SDK, etc.). Eliminates API hallucination.

**Use Case**: Claude Code needs to use a library API → Context7 provides up-to-date docs + examples.

**Key Features**:

| Capability | Details |
|------------|---------|
| Library Search | Find docs for 500+ libraries |
| Code Examples | Language-specific examples (Python, TS, etc.) |
| API Reference | Detailed function signatures, parameters |
| Version Filtering | Docs for specific library versions |
| Smart Ranking | AI-ranked by relevance + project usage |

**Setup**:

```bash
# Local
npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

**Claude Code Configuration (local)**:

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

**Claude Code Configuration (remote/HTTP)**:

```bash
claude mcp add --transport http --header "CONTEXT7_API_KEY: YOUR_API_KEY" \
  context7 https://mcp.context7.com/mcp
```

**Example Usage**:

```
User: "Show me how to use Claude's streaming API with the Python SDK"

Claude: [Uses context7 search]

Result: Official Python SDK docs + example code for streaming
```

**Quality Score**: **8.2/10** ⭐⭐⭐⭐

**Limitations**:

| Limitation | Workaround |
|------------|-----------|
| Limited library coverage | Fallback to web search for obscure libs |
| Version lag (1-2 days) | Use official repo for cutting-edge |
| Hallucination risk (low but exists) | Cross-verify with official docs |

**Alternatives**:

| Server | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Context7** | Real-time, version-specific | API key required |
| Web Search | Comprehensive, free | Slow, hallucination risk |
| Static RAG | Fast, local | Outdated, no versions |

**Resources**:
- **GitHub**: https://github.com/upstash/context7
- **Official Site**: https://context7.com
- **LobeHub Registry**: https://lobehub.com/mcp/upstash-context7

**ctx7 CLI companion**: Context7 also ships a CLI (`npx ctx7`) that handles skill discovery and MCP setup from the terminal. `ctx7 skills suggest` auto-detects project dependencies and recommends matching skills; `ctx7 setup --claude` runs a wizard that configures MCP or CLI+Skills mode automatically. See §5.5 of the ultimate guide for the full workflow.

---

### Project Management

#### Linear MCP

**Community server** for Linear (project management SaaS). GraphQL API with issue management, projects, teams, comments.

**Use Case**: Claude Code automatically creates tickets, updates status, links issues in Linear (closes loop between development and project management).

**Key Features**:

| Capability | Details |
|------------|---------|
| Issue Management | List, get, create, update, delete, search |
| Projects | List, create, update, assign |
| Teams & Users | Team management, member assignment |
| Comments | Add, list, with position tracking |
| Cycles | Sprint/cycle management |
| Webhooks | Subscribe to Linear events (optional) |

**Setup**:

```bash
# NPM or uvx
npm install mcp-linear
# or
uvx mcp-linear
```

**Claude Code Configuration**:

```bash
claude mcp add linear -- npx -y mcp-linear --api-key YOUR_LINEAR_API_KEY
```

**Example Usage**:

```
User: "Create a bug ticket in Linear for the CSS layout issue I just found"

Claude: [Uses linear.issues.create with team key, title, description]

Result: Ticket created, issue ID returned

User: "Update ticket SOFT-123 status to 'In Progress'"

Claude: [Uses linear.issues.update]

Result: Status changed
```

**Quality Score**: **7.6/10** ⭐⭐⭐⭐

**Note**: Community-maintained (not Linear Inc.), but active and well-documented.

**Limitations**:

| Limitation | Workaround |
|------------|-----------|
| Timeout issues (fixed after 1h) | Implement heartbeat, firewall checks |
| 65KB field limit | Auto-chunking for comments |
| GraphQL complexity | Split complex queries automatically |

**Alternatives**:

| Server | Advantage | Disadvantage |
|--------|-----------|--------------|
| **Linear MCP** | Modern GraphQL, startup-friendly | Community-maintained |
| Jira MCP | Enterprise, complex workflows | Heavier, older API |
| GitHub Issues | Built-in, free | Limited project management |

**Resources**:
- **GitHub**: https://github.com/tacticlaunch/mcp-linear
- **Linear API**: https://developers.linear.app
- **Docs**: https://jan.ai/docs/desktop/mcp-examples/productivity/linear

---

### Orchestration

#### MCP-Compose

**Community tool** for managing multiple MCP servers Docker Compose-style. Declarative YAML configuration, multi-transport support (STDIO/HTTP/SSE).

**Use Case**: Developer needs 5+ MCP servers; Docker Compose-like config simplifies lifecycle management.

**Key Features**:

| Capability | Details |
|------------|---------|
| YAML Configuration | Docker Compose-style server definitions |
| Multi-Transport | STDIO, HTTP, SSE, TCP support |
| Container Runtimes | Docker, Podman, native processes |
| Network Management | Automatic Docker network creation |
| Health Monitoring | Connection pooling, session management |
| HTTP Proxy | Single unified HTTP endpoint |
| Hot Reload | Update config without restart |

**Setup**:

```bash
git clone https://github.com/phildougherty/mcp-compose
cd mcp-compose
cargo build --release
```

**Configuration** (`mcp-compose.yaml`):

```yaml
version: "1.0"
mcpServers:
  filesystem:
    command: npx
    args:
      - "@modelcontextprotocol/server-filesystem"
      - "/tmp"
    transport: stdio

  memory:
    command: npx
    args:
      - "@modelcontextprotocol/server-memory"
    transport: stdio
    env:
      DEBUG: "true"

  postgres:
    image: postgres:15
    transport: tcp
    port: 5432
    env:
      POSTGRES_PASSWORD: secret

proxy:
  port: 3000
  listen: "127.0.0.1"
```

**Generate Claude Desktop Config**:

```bash
./mcp-compose create-config --type claude --output ~/.claude.json
```

**Start Servers**:

```bash
./mcp-compose up
# Single unified HTTP proxy at http://localhost:3000
```

**Quality Score**: **7.4/10** ⭐⭐⭐⭐

**Limitations**:

| Limitation | Workaround |
|------------|-----------|
| Cargo build required | Use pre-built binary (if available) |
| YAML learning curve | Provide templates for common setups |
| Debug complexity | Use mcp-compose logs for troubleshooting |

**Resources**:
- **GitHub**: https://github.com/phildougherty/mcp-compose
- **Docker Compose Docs**: https://docs.docker.com/compose/
- **MCP Protocol Spec**: https://modelcontextprotocol.io

---

#### Packmind

**Community tool** for distributing engineering standards as AI context across multiple agents and repositories. Exposes an MCP server for creating and managing playbook standards directly from Claude Code (or any MCP-capable agent).

**Use Case**: Engineering team maintains one playbook; Packmind MCP server lets Claude Code propose new standards or update existing ones during a session without leaving the editor.

**Key Features**:

| Capability | Details |
|------------|---------|
| Standards Creation | Create/update playbook entries via MCP tools |
| Multi-Agent Output | Generates CLAUDE.md, .cursor/rules, Copilot instructions from one source |
| Knowledge Ingestion | Pull context from GitHub, Slack, Jira, GitLab, Confluence, Notion via their MCP servers |
| Self-hosted | Docker/Kubernetes, Apache-2.0 CLI |

**Resources**:
- **GitHub**: https://github.com/PackmindHub/packmind
- **Demo use cases**: https://github.com/PackmindHub/demo-use-case-skills

> **Cross-ref**: Full tool evaluation in [third-party-tools.md — Engineering Standards Distribution](./third-party-tools.md#engineering-standards-distribution).

---

## Production Deployment

### Security Checklist

- [ ] **API keys** stored in `.env`, not in config files
- [ ] **RBAC/permissions** reviewed (especially Kubernetes, Semgrep)
- [ ] **Rate limits** understood (Linear GraphQL complexity, Vercel API)
- [ ] **Fallback mechanisms** for API downtime implemented
- [ ] **Monitoring + logging** enabled for all MCP servers

### Quick Start Stack

**MVP (Essentials)**:

1. **Playwright MCP** — E2E testing, web verification
2. **Semgrep MCP** — Security-first coding

**Important Additions**:

3. **Context7 MCP** — API reference accuracy
4. **Linear MCP** (optional) — Issue tracking integration

**DevOps/SRE Stack**:

5. **Kubernetes MCP** — Cluster management
6. **Vercel MCP** — Next.js deployment automation

**Complex Setups**:

7. **MCP-Compose** — Multi-server orchestration
8. **Browserbase MCP** — Heavy web automation (premium)

### Installation Examples

```bash
# Playwright (browser testing)
npm install @microsoft/playwright-mcp

# Semgrep (security)
uvx semgrep-mcp

# Context7 (documentation)
npx -y @upstash/context7-mcp --api-key YOUR_API_KEY

# Linear (project management)
npm install mcp-linear
```

### Performance Metrics

| Metric | Median | Range | Notes |
|--------|--------|-------|-------|
| **Response Time** | ~200ms | 100-500ms | Cloud-dependent (Browserbase ~500ms) |
| **Token Overhead** | ~200-500 tokens | Minimal for structured output | Accessibility trees vs screenshots |
| **Setup Time** | ~5 minutes | 2-10 minutes | Cargo build (MCP-Compose) = 10 min |

---

## Monthly Watch Methodology

This section documents the process for maintaining this guide with monthly ecosystem updates.

### Sources to Monitor

**Official Sources**:
- [Anthropic MCP GitHub](https://github.com/modelcontextprotocol/servers)
- [Anthropic Blog](https://www.anthropic.com/news)
- [MCP Protocol Spec](https://modelcontextprotocol.io)

**Community Sources**:
- [GitHub topic: mcp-servers](https://github.com/topics/mcp-servers) (7260+ servers)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) (75.5k stars)
- [MCP Registry](https://github.blog/ai-and-ml/generative-ai/how-to-find-install-and-manage-mcp-servers-with-the-github-mcp-registry/)

**Discussions**:
- [Reddit r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/)
- [Reddit r/mcp](https://www.reddit.com/r/mcp/)
- [X/Twitter #MCPServer](https://twitter.com/search?q=%23MCPServer)

**Technical Articles**:
- [Blog Skyvia](https://blog.skyvia.com/best-mcp-servers/)
- [Builder.io Blog](https://www.builder.io/blog/best-mcp-servers-2026)
- [Cyberpress](https://cyberpress.org/best-mcp-servers/)

### Monthly Review Checklist

- [ ] **Official servers**: Check Anthropic GitHub for new releases
- [ ] **Community servers**: Review GitHub topics for trending servers (≥50 stars, <3 months release)
- [ ] **Ecosystem changes**: Monitor Anthropic blog for protocol updates
- [ ] **Server health**: Re-evaluate existing servers (releases, issues, maintenance)
- [ ] **Security**: Check for disclosed vulnerabilities (GitHub Security Advisories)
- [ ] **Deprecations**: Identify archived or unmaintained servers
- [ ] **Update guide**: Add new validated servers, remove deprecated ones

### Evaluation Template

For each candidate server:

1. **Basic Validation**:
   - GitHub stars ≥50?
   - Last release <3 months?
   - Documentation complete (README + examples + config)?
   - Tests/CI present?

2. **Quality Scoring** (see [Evaluation Framework](#evaluation-framework)):
   - Maintenance: `/10`
   - Documentation: `/10`
   - Tests: `/10`
   - Performance: `/10`
   - Adoption: `/10`
   - **Total**: `/50` → Normalized to `/10`

3. **Use Case Analysis**:
   - What gap does it fill?
   - Is it already covered by official servers?
   - What are the alternatives?

4. **Decision**:
   - **Integrate** (score ≥8): Add full section to guide
   - **Monitor** (score 6-7): Add to [Watch List](../../docs/resource-evaluations/watch-list.md), re-evaluate next month
   - **Reject** (score <6): Document reason in [Excluded Servers](#excluded-servers)

### Integration Workflow

When adding a new server:

1. Create section in appropriate category (Browser Automation, DevOps, etc.)
2. Include:
   - Use case description
   - Key features table
   - Setup instructions
   - Configuration examples
   - Quality score
   - Limitations & workarounds
   - Alternatives comparison
   - Resources (GitHub, docs, tutorials)
3. Update [Quick Start Stack](#quick-start-stack) if MVP-relevant
4. Update [Production Deployment](#production-deployment) checklist if security-critical

---

## Excluded Servers

Servers evaluated but not included in the validated list:

| Server | Reason | Source | Date Evaluated |
|--------|--------|--------|----------------|
| **X/Twitter MCP** | API instability, frequent auth issues, inconsistent maintenance | [Cursor Forum](https://forum.cursor.com/t/linear-mcp-commonly-errors-out-and-requires-turning-off-then-on/148816) | Jan 2026 |
| **Vector Search MCP** | <50 stars, incomplete documentation | [LobeHub](https://lobehub.com/mcp/hugoduncan-mcp-vector-search) | Jan 2026 |
| **GitHub MCP** | Archived, migrated to official Go SDK | [GitHub Changelog](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/) | Jan 2026 |
| **Jira MCP (sooperset)** | No recent release (last: June 2025), less stable than Linear | [GitHub Releases](https://github.com/sooperset/mcp-atlassian/releases) | Jan 2026 |

---

## Statistics & Insights

### Distribution by Category

| Category | Servers | Use Cases |
|----------|---------|-----------|
| **Browser Automation** | 3 (Playwright, Browserbase, Chrome DevTools) | Testing, debugging, data extraction |
| **DevOps/Infrastructure** | 2 (Vercel, Kubernetes) | Deployment, cluster management |
| **Security/Code Analysis** | 1 (Semgrep) | Vulnerability scanning, secure coding |
| **Code Search/Analysis** | 1 (Grepai) | Semantic search, call graph analysis |
| **Documentation/Knowledge** | 1 (Context7) | API reference, code examples |
| **Project Management** | 1 (Linear) | Issue tracking, sprint planning |
| **Orchestration** | 1 (MCP-Compose) | Multi-server management |

### Maintainer Types

- **Official Servers** (6): Playwright (Microsoft), Browserbase, Semgrep, Context7, Kubernetes (Red Hat), Chrome DevTools (Anthropic)
- **Community Servers** (4): Linear, Vercel, MCP-Compose, Grepai (well-designed, actively maintained)

---

**Last updated**: February 2026
**Next review**: March 2026
**Maintainer**: Claude Code Ultimate Guide Team

---

*Back to [main guide](./ultimate-guide.md) | [README](./README.md)*