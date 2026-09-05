# Claude Code Ultimate Guide

<table>
  <tr>
    <td width="64">
      <a href="https://www.florian.bruniaux.com/about/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide"><img src="https://cc.bruniaux.com/author.png" width="56" height="56" alt="Florian Bruniaux" /></a>
    </td>
    <td>
      <strong><a href="https://www.florian.bruniaux.com/about/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Florian BRUNIAUX</a></strong> &middot; AI Founding Engineer @ <a href="https://methode-aristote.fr/">Méthode Aristote</a><br />
      13 years from developer to CTO / VP Eng &middot; <a href="https://www.florian.bruniaux.com/blog/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Blog &#8599;</a> &middot; <a href="https://www.florian.bruniaux.com/projects/?utm_source=github&amp;utm_medium=readme&amp;utm_campaign=claude-code-ultimate-guide">Projects &#8599;</a>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://cc.bruniaux.com/"><img src="https://img.shields.io/badge/Interactive_Guide-cc.bruniaux.com-ff6b35?style=for-the-badge" alt="Open the interactive guide" /></a>
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/Guide-v3.43.0-brightgreen?style=flat-square" alt="Guide version 3.43.0" /></a>
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/Updated-Sep_5,_2026_·_v3.43.0-brightgreen?style=flat-square" alt="Updated Sep 5, 2026, guide version 3.43.0" /></a>
  <a href="https://creativecommons.org/licenses/by-sa/4.0/"><img src="https://img.shields.io/badge/Guide-CC_BY--SA_4.0-blue?style=flat-square" alt="Guide license: CC BY-SA 4.0" /></a>
  <a href="https://cc.bruniaux.com/mcp/"><img src="https://img.shields.io/badge/MCP-npx_ready-blueviolet?style=flat-square" alt="MCP server available through npx" /></a>
</p>

Learn Claude Code, build reliable agents, and scale their use safely. The website is the primary reading and discovery interface. This repository contains the canonical Markdown sources, reusable files, machine-readable indexes, and contribution history.

**Start here:** [complete a first task online](https://cc.bruniaux.com/guide/ultimate-guide/01-quick-start/) · [browse the guide portal](https://cc.bruniaux.com/guide/) · [open the complete sitemap](https://cc.bruniaux.com/sitemap/) · [read the Markdown source](./guide/ultimate-guide.md)

## Choose your next step

The table below is generated from [`machine-readable/navigation.json`](./machine-readable/navigation.json). The same contract feeds the public sitemap, so the repository and website expose the same intent model.

<!-- BEGIN GENERATED INTENT NAVIGATION -->
| Intent | Browse online |
|---|---|
| **Start** | [Guide portal](https://cc.bruniaux.com/guide/) · [Quick Start](https://cc.bruniaux.com/guide/ultimate-guide/01-quick-start/) · [Learning Paths](https://cc.bruniaux.com/learning/) · [Quick Reference](https://cc.bruniaux.com/cheatsheet/) · [AI Roles](https://cc.bruniaux.com/roles/) |
| **Build** | [Agent Harness Engineering](https://cc.bruniaux.com/guide/agent-harness/) · [Loop & Graph Engineering](https://cc.bruniaux.com/guide/loop-graph-engineering/) · [Context Engineering](https://cc.bruniaux.com/context-engineering/) · [Memory Systems](https://cc.bruniaux.com/memory-systems/) · [Workflows](https://cc.bruniaux.com/guide/workflows/) · [Methodologies](https://cc.bruniaux.com/methodologies/) · [MCP or CLI?](https://cc.bruniaux.com/mcp-or-cli/) · [Examples](https://cc.bruniaux.com/examples/) |
| **Scale** | [Security](https://cc.bruniaux.com/security/) · [Enterprise Governance](https://cc.bruniaux.com/guide/enterprise-governance/) · [Observability](https://cc.bruniaux.com/guide/observability/) · [Team Metrics](https://cc.bruniaux.com/team-metrics/) · [Team Adoption](https://cc.bruniaux.com/guide/adoption-approaches/) · [Subscription Strategy](https://cc.bruniaux.com/guide/subscription-strategy/) · [AI Unit Economics](https://cc.bruniaux.com/guide/ai-unit-economics/) · [Team Knowledge](https://cc.bruniaux.com/guide/team-knowledge-base/) · [API Gateway](https://cc.bruniaux.com/guide/api-gateway/) |
| **Resources** | [Resource Hub](https://cc.bruniaux.com/resources/) · [Downloads](https://cc.bruniaux.com/downloads/) · [Cheat Sheets](https://cc.bruniaux.com/cheatsheets/) · [Ebooks](https://cc.bruniaux.com/whitepapers/) · [Diagrams](https://cc.bruniaux.com/diagrams/) · [Ecosystem](https://cc.bruniaux.com/ecosystem/) · [Compare](https://cc.bruniaux.com/compare/) · [Glossary](https://cc.bruniaux.com/guide/glossary/) · [FAQ](https://cc.bruniaux.com/faq/) · [Guide MCP Server](https://cc.bruniaux.com/mcp/) · [Related Projects](https://cc.bruniaux.com/projects/) |
| **Updates** | [Guide Changelog](https://cc.bruniaux.com/changelog/) · [Claude Code Releases](https://cc.bruniaux.com/releases/) · [RSS Feed](https://cc.bruniaux.com/rss.xml) |
<!-- END GENERATED INTENT NAVIGATION -->

## Why this guide exists

Claude Code documentation explains the product. This guide connects product behavior to engineering decisions: what belongs in context, when to use an agent instead of a skill, how to verify generated work, and which controls matter when usage moves beyond one developer.

| Need | Start with |
|---|---|
| Understand Claude Code internals | [Architecture](./guide/core/architecture.md) and [Tools Reference](./guide/core/tools-reference.md) |
| Design agent systems | [Agent Harness Engineering](./guide/core/agent-harness.md) and [Loop & Graph Engineering](./guide/core/loop-graph-engineering.md) |
| Structure AI-assisted delivery | [Methodologies](./guide/core/methodologies.md) and [Workflow Guides](./guide/workflows/) |
| Establish a security boundary | [Security Hardening](./guide/security/security-hardening.md) and [Sandbox Isolation](./guide/security/sandbox-isolation.md) |
| Validate understanding | [Knowledge Quiz](https://cc.bruniaux.com/quiz/) and [Recap Cards](https://cc.bruniaux.com/cheatsheets/) |

The guide favors explicit trade-offs and verifiable procedures. Where evidence is incomplete, the relevant page should preserve that limit instead of presenting one workflow as universal.

## Start

### Install Claude Code

Choose one installation method:

```bash
# npm, macOS, Linux, or Windows
npm install -g @anthropic-ai/claude-code

# macOS with Homebrew
brew install claude-code

# macOS or Linux native installer
curl -fsSL https://claude.ai/install.sh | sh
```

Windows PowerShell also supports:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Verify the installation and authenticate:

```bash
claude --version
claude doctor
claude auth login
```

The [Quick Start chapter](./guide/ultimate-guide.md#1-quick-start-day-1) documents installation alternatives, authentication, updates, permission modes, and common first-day failures.

### Complete a first task

Open a small repository with a clean or understood Git state, then start Claude Code:

```bash
cd your-project
claude
```

Give Claude a bounded request that includes the expected result and verification:

```text
Explain how this project runs its tests. Do not modify files.
Name the relevant commands and cite the files that define them.
```

Before asking Claude to edit code, add a project-level `CLAUDE.md` that records the commands and constraints Claude must follow:

```markdown
# Project instructions

## Commands
- Test: `npm test`
- Lint: `npm run lint`

## Boundaries
- Do not edit generated files.
- Do not change dependencies without approval.
- Run the relevant tests before claiming completion.
```

Continue with the [first workflow](./guide/ultimate-guide.md#12-first-workflow) or use the [starter CLAUDE.md templates](./examples/claude-md/).

### Choose a learning path

| Situation | Suggested route |
|---|---|
| New to Claude Code | [Seven-module learning path](./guide/learning-path/README.md) |
| Already using the CLI | [Core Concepts](./guide/ultimate-guide.md#2-core-concepts), then [Context Engineering](./guide/core/context-engineering.md) |
| Senior developer or tech lead | [Methodologies](./guide/core/methodologies.md), [Agent Harness Engineering](./guide/core/agent-harness.md), then [Production Safety](./guide/security/production-safety.md) |
| Engineering manager or CTO | [Adoption Approaches](./guide/roles/adoption-approaches.md), [Team Metrics](./guide/ops/team-metrics.md), then [Subscription Strategy](./guide/ops/subscription-strategy.md) |
| Security or platform role | [Security Hardening](./guide/security/security-hardening.md), [Enterprise Governance](./guide/security/enterprise-governance.md), then [Observability](./guide/ops/observability.md) |
| Product manager or designer | [Product Manager Guide](./docs/for-product-managers.md) or [Design-to-Code Workflow](./guide/workflows/design-to-code.md) |
| Non-developer knowledge worker | [Claude Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide) |

For a personalized route, use the repository onboarding prompt:

```bash
claude "Fetch and follow the onboarding instructions from: https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/tools/onboarding-prompt.md"
```

## Build

### Agent engineering

An agent is one component of a larger system. The surrounding harness controls context, tools, permissions, state, stopping conditions, recovery, and evaluation.

| Resource | Decision it supports |
|---|---|
| [Agent Harness Engineering](./guide/core/agent-harness.md) | Identify the controls required around an agent loop |
| [Loop & Graph Engineering](./guide/core/loop-graph-engineering.md) | Choose bounded feedback loops or explicit workflow graphs |
| [Agent Harness Map](./guide/ecosystem/agent-harness-landscape.md) | Distinguish runtimes, orchestrators, frameworks, control planes, and support tools |
| [Agentic Tools](./guide/ecosystem/agentic-tools.md) | Compare selected coding agents and orchestration products |
| [Agent Evaluation](./guide/roles/agent-evaluation.md) | Test behavior, regressions, and task-level outcomes |
| [Harness Glossary](./guide/core/glossary.md) | Align terminology across design and review |

### Context and memory

Context quality affects every tool call and decision. Start with project instructions, add specialized context only when a recurring task needs it, and test whether the extra material changes behavior.

| Resource | Focus |
|---|---|
| [Context Engineering](./guide/core/context-engineering.md) | Context budget, modular instructions, assembly, and measurement |
| [Memory Systems](./guide/core/memory-systems.md) | Native memory, cross-session systems, team sharing, and retention risks |
| [Context Engineering Tools](./guide/ecosystem/context-engineering-tools.md) | Output compression, retrieval, gateways, and context inspection |
| [Context Audit](./tools/context-audit-prompt.md) | Measure a project's context architecture |
| [Team AI Instructions](./guide/workflows/team-ai-instructions.md) | Maintain shared instructions across a development team |

### Workflows

| Goal | Workflow |
|---|---|
| Implement with tests first | [TDD with Claude](./guide/workflows/tdd-with-claude.md) |
| Define behavior before implementation | [Spec-First Development](./guide/workflows/spec-first.md) |
| Separate planning from execution | [Plan-Driven Development](./guide/workflows/plan-driven.md) |
| Compare independent candidates | [Best-of-N](./guide/workflows/best-of-n.md) |
| Coordinate several agents | [Agent Teams](./guide/workflows/agent-teams.md) |
| Build bounded autonomous loops | [Agentic Software Factories](./guide/workflows/agentic-software-factories.md) |
| Review code systematically | [Code Review](./guide/workflows/code-review.md) |
| Diagnose unfamiliar repositories | [Exploration Workflow](./guide/workflows/exploration-workflow.md) |

[Browse every workflow](./guide/workflows/) for task management, GitHub Actions, production reliability, event-driven agents, design-to-code, PDF generation, search, and team instructions.

### Choose the smallest interface

Claude Code can call local commands, skills, agents, hooks, plugins, and MCP servers. More infrastructure adds setup, permissions, failure modes, and maintenance.

| If the task needs | Prefer |
|---|---|
| A deterministic local command | CLI or script |
| Reusable instructions and supporting files | Skill |
| A separate context and role | Agent |
| A response to a lifecycle event | Hook |
| A packaged collection of capabilities | Plugin |
| A typed interface to a remote service | MCP server |

Use the [MCP or CLI decision guide](./guide/ecosystem/mcp-vs-cli.md) and the [trade-off framework](./guide/ultimate-guide.md#when-to-use-what) before introducing another integration.

## Scale

### Reliability and security

| Concern | Primary resource | Operational companion |
|---|---|---|
| Permissions and prompt injection | [Security Hardening](./guide/security/security-hardening.md) | [Permissions Audit](./tools/permissions-audit-prompt.md) |
| Isolation of untrusted execution | [Sandbox Isolation](./guide/security/sandbox-isolation.md) | [Native Sandbox](./guide/security/sandbox-native.md) |
| Production changes and rollback | [Production Safety](./guide/security/production-safety.md) | [Production Reliability](./guide/workflows/production-reliability.md) |
| Sensitive data and retention | [Data Privacy](./guide/security/data-privacy.md) | [Enterprise Governance](./guide/security/enterprise-governance.md) |
| MCP and extension supply chain | [MCP Ecosystem](./guide/ecosystem/mcp-servers-ecosystem.md) | [Threat Database](./examples/commands/resources/threat-db.yaml) |
| Delegation readiness | [Specification Completeness Audit](./tools/spec-completeness-audit.md) | [Agent Evaluation](./guide/roles/agent-evaluation.md) |

Security claims and threat counts change as sources are added or corrected. Use the linked database and guides as the current source instead of copying their counts into project documentation.

### Evaluation and operations

| Need | Resource |
|---|---|
| Trace agent behavior and failures | [Observability](./guide/ops/observability.md) |
| Attribute AI-assisted changes | [AI Traceability](./guide/ops/ai-traceability.md) |
| Evaluate team outcomes | [Team Metrics](./guide/ops/team-metrics.md) |
| Calculate task-level cost | [AI Unit Economics](./guide/ops/ai-unit-economics.md) |
| Operate infrastructure workflows | [DevOps & SRE](./guide/ops/devops-sre.md) |
| Route governed API traffic | [API Gateways](./guide/ops/api-gateway.md) |

A green structural check proves only what it inspected. Runtime behavior, task acceptance, security boundaries, and business outcomes require separate evidence.

### Organization and economics

| Decision | Resource |
|---|---|
| Roll out Claude Code across a team | [Adoption Approaches](./guide/roles/adoption-approaches.md) |
| Define usage tiers and approvals | [Enterprise Governance](./guide/security/enterprise-governance.md) |
| Preserve team knowledge | [Team Knowledge Base](./guide/ecosystem/team-knowledge-base.md) |
| Compare subscriptions, APIs, and gateways | [Subscription Strategy](./guide/ops/subscription-strategy.md) |
| Compare hosted and local inference | [Local vs Cloud Inference](./guide/ecosystem/local-vs-cloud-inference.md) |
| Map changing AI roles | [AI Roles](./guide/roles/ai-roles.md) |

The economics pages separate observed costs from estimates and scenarios. Recalculate them with your workload, acceptance criteria, review effort, and risk constraints.

## Use the format that fits the task

| Format | Use it for | Read online | Source or download |
|---|---|---|---|
| Complete reference | Deep explanations and linked sections | [Ultimate Guide](https://cc.bruniaux.com/guide/ultimate-guide/) | [Markdown](./guide/ultimate-guide.md) |
| Daily reference | Commands, shortcuts, and checks | [Quick Reference](https://cc.bruniaux.com/cheatsheet/) | [Markdown](./guide/cheatsheet.md) |
| Guided course | Progressive exercises with retained evidence | [Learning Paths](https://cc.bruniaux.com/learning/) | [Course sources](./guide/learning-path/) |
| Runnable material | Agents, skills, hooks, workflows, and scripts | [Examples](https://cc.bruniaux.com/examples/) | [Files](./examples/) |
| Visual explanation | Architecture, context, security, and workflow maps | [Diagrams](https://cc.bruniaux.com/diagrams/) | [Diagram sources](./guide/diagrams/) |
| Knowledge check | Questions with documentation links | [Quiz](https://cc.bruniaux.com/quiz/) | [Question sources](./quiz/) |
| Printable reference | One concept per page in French and English | [Cheat Sheets](https://cc.bruniaux.com/cheatsheets/) | [Card sources](./whitepapers/recap-cards/) |
| Long-form edition | Offline PDF and EPUB | [Ebooks](https://cc.bruniaux.com/whitepapers/) | [Downloads](https://cc.bruniaux.com/downloads/) |
| Machine-readable index | Search and retrieval by an AI assistant | [Guide MCP](https://cc.bruniaux.com/mcp/) | [llms.txt](./machine-readable/llms.txt) and [reference.yaml](./machine-readable/reference.yaml) |

## MCP Server: Use the guide from any coding client

<!-- mcp-product:start -->
Install the guide as a stdio MCP server and query it from Claude Code, Codex, Cursor, VS Code, or another MCP client.

```bash
claude mcp add --scope user claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.3
codex mcp add claude-code-guide -- npx -y claude-code-ultimate-guide-mcp@1.3.3
```

Project-scoped Claude Code configuration belongs in `.mcp.json`:

```json
{
  "mcpServers": {
    "claude-code-guide": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "claude-code-ultimate-guide-mcp@1.3.3"]
    }
  }
}
```

| Capability | Count | Names |
| --- | ---: | --- |
| Tools | 17 | `compare_versions`, `diff_official_docs`, `get_changelog`, `get_cheatsheet`, `get_digest`, `get_example`, `get_release`, `get_threat`, `init_official_docs`, `list_examples`, `list_threats`, `list_topics`, `read_section`, `refresh_official_docs`, `search_examples`, `search_guide`, `search_official_docs` |
| Resources | 6 | `claude-code-guide://agent-harnesses`, `claude-code-guide://distribution-channels`, `claude-code-guide://llms`, `claude-code-guide://reference`, `claude-code-guide://releases`, `claude-code-guide://translations` |
| Prompts | 1 | `claude-code-expert` |
| Companion commands | 5 | `/ccguide:daily`, `/ccguide:diff-docs`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:search-docs` |

The list operations and search index use bundled content. Section, example, cheatsheet, changelog, digest (`get_digest`), and threat tools can fetch GitHub content and write a 24-hour local cache. The official-doc initialization and refresh tools fetch Anthropic documentation and write separate local snapshots.

[Canonical technical guide, installation, privacy, limitations, and dated statistics](./guide/ecosystem/claude-code-guide-mcp.md)

[Package README and diagnostics](./mcp-server/README.md)

Companion commands rendered from the repository: `/ccguide:daily`, `/ccguide:diff-docs`, `/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:search-docs`.
<!-- mcp-product:end -->

### Load the guide into another assistant

Use the small index for discovery:

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/llms.txt
```

Use [reference.yaml](./machine-readable/reference.yaml) when the assistant needs structured topic routes and links into the full guide. Maintenance instructions belong in the [machine-readable documentation](./machine-readable/README.md), not in this README.

## Complementary ecosystem

No single repository needs to cover learning, installation, curation, reference material, and every specialized interface. Choose the resource that matches the current task.

| Need | Resource | What it provides |
|---|---|---|
| Verify Claude Code behavior | [Official Claude Code documentation](https://code.claude.com/docs) | Primary product documentation |
| Learn architecture, trade-offs, security, and workflows | [Claude Code Guide](https://cc.bruniaux.com/guide/) | Explanations, decision guides, operational checks, and examples |
| Discover community projects | [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Curated links across the ecosystem |
| Install a collection of configurations | [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | Packaged agents, skills, hooks, and configurations |
| Browse installable templates | [claude-code-templates](https://github.com/davila7/claude-code-templates) | Template catalog and CLI distribution |
| Start from official skill examples | [anthropics/skills](https://github.com/anthropics/skills) | Anthropic-maintained skill examples |
| Browse the skills marketplace | [skills.sh](https://skills.sh/) | Search and installation routes for published skills |
| Work outside software development | [Claude Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide) | Workflows for knowledge workers |
| Compare coding-agent capabilities | [AI Coding Agents Matrix](https://coding-agents-matrix.dev) | Cross-agent feature comparison |

This short list was reviewed on 2026-08-31. Project activity, installation methods, and scope can change. Browse the public [Ecosystem](https://cc.bruniaux.com/ecosystem/) and [Compare](https://cc.bruniaux.com/compare/) pages first. The [AI Ecosystem source](./guide/ecosystem/ai-ecosystem.md), [Third-Party Tools source](./guide/ecosystem/third-party-tools.md), and [Resource Evaluations](./docs/resource-evaluations/) retain the deeper evidence.

## Updates

Guide changes and Claude Code product releases answer different questions:

| Feed | Tracks | Source |
|---|---|---|
| [Guide Changelog](https://cc.bruniaux.com/changelog/) | New pages, corrections, and major repository revisions | [CHANGELOG.md](./CHANGELOG.md) |
| [Claude Code Releases](https://cc.bruniaux.com/releases/) | Claude Code product versions and operational impact | [Release source](./guide/core/claude-code-releases.md) |
| [RSS Feed](https://cc.bruniaux.com/rss.xml) | Published guide and product updates in a feed reader | Generated by the website |

Recent guide additions include:

- [Loop & Graph Engineering](https://cc.bruniaux.com/guide/loop-graph-engineering/) ([source](./guide/core/loop-graph-engineering.md)): bounded feedback, workflow state, stopping rules, recovery, and judgment allocation.
- [Subscription Strategy](https://cc.bruniaux.com/guide/subscription-strategy/) ([source](./guide/ops/subscription-strategy.md)): seats, APIs, gateways, self-hosting scenarios, and team-scale decision gates.
- [Cross-Session Messaging](https://cc.bruniaux.com/guide/workflows/cross-session-messaging/) ([source](./guide/workflows/cross-session-messaging.md)): peer discovery, delivery, security boundaries, and correlated-drift controls.

Use the changelog for the complete history. The README should expose only a small current selection.

## Languages and translations

English is the canonical edition. French is maintained in this repository. Simplified Chinese, Ukrainian, and Latin American Spanish are independent community editions with separate update schedules.

| Language | Edition |
|---|---|
| English | [Canonical guide](./guide/ultimate-guide.md) |
| Français | [French guide maintained in this repository](./guide/ultimate-guide.fr.md) |
| 简体中文 | [Community edition by JAYcodr](https://github.com/JAYcodr/claude-code-ultimate-guide-zh) |
| Українська | [Community edition by gerasimsergey](https://github.com/gerasimsergey/claude-code-ultimate-guide-ua) |
| Español latinoamericano | [Community edition by Richardls](https://github.com/Richardls/claude-code-ultimate-guide-es) |

The [translation status page](./guide/core/translations.md) records maintainers, source commits, coverage, measured lag, and review status.

## Repository map

```text
guide/
├── ultimate-guide.md       Complete reference
├── learning-path/          Guided course
├── core/                   Architecture, tools, context, methods
├── security/               Hardening, isolation, privacy, governance
├── ecosystem/              Agents, MCP, tools, inference, knowledge
├── roles/                  Adoption, learning, evaluation, careers
├── ops/                    Observability, metrics, economics, gateways
├── workflows/              Task-oriented delivery guides
└── diagrams/               Mermaid diagrams with text fallbacks

examples/                   Reusable agents, skills, hooks, and workflows
machine-readable/           Structured indexes and release data
mcp-server/                 Packaged guide access for MCP clients
quiz/                       Local knowledge validation
docs/resource-evaluations/  Reviewed external resources
whitepapers/                French and English long-form sources
```

The detailed [guide index](./guide/README.md), [examples catalog](./examples/README.md), and [tool index](./tools/README.md) are the canonical navigation pages for those directories.

## Contributing

Corrections, missing evidence, broken links, examples, quiz questions, and documentation improvements are welcome. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.

Useful contribution routes:

- Report an incorrect or outdated claim through [GitHub Issues](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues).
- Submit an external resource through the [resource evaluation process](./docs/resource-evaluations/README.md).
- Propose a focused guide or workflow with its sources, boundaries, and verification method.
- Improve an example without weakening its existing security checks.

## Maintainer

Florian Bruniaux maintains this guide.

[GitHub](https://github.com/FlorianBruniaux) · [LinkedIn](https://www.linkedin.com/in/florian-bruniaux-43408b83/) · [Portfolio](https://florian.bruniaux.com/)

<!-- BEGIN GENERATED RELATED PROJECTS -->
<!-- Source: https://github.com/FlorianBruniaux/FlorianBruniaux/blob/main/ecosystem/projects.json; project: claude-code-guide -->
## Explore the ecosystem

These projects extend the workflow without duplicating this tool:

- **Install with [claude-code-plugins](https://github.com/FlorianBruniaux/claude-code-plugins)**: move from explanations to installable templates.
- **Validate with [ctxharness](https://github.com/FlorianBruniaux/ctxharness)**: test whether documented context and instructions still match the repository.
- **Secure with [agentsec-triage](https://github.com/FlorianBruniaux/agentsec-triage)**: connect security guidance to a versioned operational feed.
- **Continue with [Claude Cowork Guide](https://github.com/FlorianBruniaux/claude-cowork-guide)**: switch to workflows designed for knowledge workers and non-developers.

[Browse the complete open-source galaxy](https://github.com/FlorianBruniaux#open-source-galaxy)
<!-- END GENERATED RELATED PROJECTS -->

## License

The guide uses [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Reusable templates use [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Check the repository license files before redistributing mixed content.

Watch [GitHub Releases](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/releases) or subscribe to the [RSS feed](https://cc.bruniaux.com/rss.xml) for updates.

---

*Version 3.43.0 | Updated daily · Sep 5, 2026*
