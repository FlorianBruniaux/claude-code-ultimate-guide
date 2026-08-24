# Team Knowledge Base for Claude Code + Cowork

**Reading time**: 18 minutes
**Skill level**: Month 1+ (team lead deploying both tools)

> **Scope**: This section covers how to set up a shared company knowledge base (KB) that both Claude Code (developer CLI) and Claude Cowork (desktop app for non-developers, research preview) can read. It is the first infrastructure question most teams hit when they roll out both tools. If you only use Claude Code on a single codebase, the repo-as-KB pattern in [§9.25 Harness Engineering](#925-harness-engineering-at-agent-throughput) already covers your needs. This section is for the team-wide case: shared docs, live systems, and reusable workflows across developers and knowledge workers.

## The "One Tool for Three Needs" Trap

A team deploys Claude Code for engineers and Cowork for PMs, ops, and support. Someone asks the obvious question: "Where do we put the company knowledge so both tools can use it?" The instinct is to pick a single answer. A wiki. A Notion workspace. A vector database. One place, one connector, done.

That instinct is the trap. It produces six months of migration work, a half-indexed Confluence space, and an agent that still misses half the answers.

The reason is that "company knowledge" is not one thing. When you look at what teams actually want the agent to access, three distinct shapes appear, and each has a different best-fit storage and access mechanism. Forcing all three into one tool means at least two of them fit badly.

The three shapes:

| Nature of the knowledge | Changes how? | Best-fit tool |
|-------------------------|--------------|---------------|
| **Static docs** (runbooks, ADRs, coding standards, onboarding, policies) | Via file edits, committed | Versioned Markdown repo (Obsidian optional on top) |
| **Live systems** (Jira tickets, Confluence pages, CRM records, internal APIs) | Continuously, by other people and processes | MCP connector / plugin to the source of truth |
| **Reusable team workflows** (slash commands, skills, agents, prompts) | Via team iteration on the workflow itself | Plugin distributed via a marketplace |

The mistake is treating all three as "documents to store somewhere." Static docs want version control and direct file reads. Live systems want a connection to where the data already lives, not a copy that goes stale the moment you sync it. Workflows are not documents at all; they are behavior, and behavior is packaged and distributed differently from content.

Once you classify each piece of knowledge by its nature, the tool choice becomes mechanical. The rest of this section walks through each tier with concrete setup steps, then covers the plugin pattern for workflows, the governance caveat for sensitive data, and a decision table for what to build first.

### Why Claude Projects does not fit

Before the three tiers: one anti-pattern to name first, because teams reach for it before any of the three. Claude Projects (the web feature where you upload files and chat against them) looks like an obvious shared KB. It is not, for a team running Code and Cowork.

| Limitation | Consequence for a team KB |
|------------|---------------------------|
| Web-only | Neither Claude Code nor Cowork can read a Project programmatically |
| Upload-only | No live sync; you re-upload on every change |
| ~20-file practical cap | Does not scale past a small handful of docs |
| No filesystem access | The agent can't navigate, grep, or cross-reference |

Projects are fine for an individual exploring a fixed set of PDFs in the web app. As shared team infrastructure that two agentic tools must both read from, they are a dead end. Use them for ad-hoc analysis, not as the KB backbone.

---

## Tier 1: Versioned Markdown Vault (Static Docs)

Most of what a team calls "the knowledge base" is static documentation. Runbooks, architecture decision records, coding standards, onboarding guides, the "how we deploy" doc, the incident postmortems. These change through deliberate edits, and you want every change reviewed and reversible. That description is the definition of a git repository.

### Why a Markdown repo, not a wiki

The key insight: both Claude Code and Cowork read local files directly. Claude Code clones the repo and has full filesystem access (read, grep, cross-reference across thousands of files). Cowork grants access to the same local folder on the user's machine. Both tools point at the same source. There is no separate "AI copy" to keep in sync, because the source itself is what the agent reads.

A wiki (Confluence, a hosted Notion, an internal portal) puts the content behind an API or a web UI. To make that readable by an agent, you add a connector, and now you maintain a connector and worry about its freshness and its rate limits. A versioned Markdown repo skips that entire layer for static content. The agent reads the file. Git handles history. Pull requests handle review.

| Property | Markdown repo | Hosted wiki |
|----------|---------------|-------------|
| Agent access | Direct file read (no connector) | Requires MCP/API connector |
| Version history | Native (git) | Tool-dependent, often weak |
| Review workflow | Pull requests | Manual or none |
| Offline / local | Yes | No |
| Diff and blame | Native | Limited |
| Migration cost later | Low (plain text) | High (export pain) |

### Setup

Create a dedicated repository for shared knowledge, separate from any codebase. Clone it to a stable shared path on each machine. The convention this guide already uses is a `~/Shared/` directory:

```bash
# On each team member's machine
git clone git@github.com:yourcompany/knowledge-base.git ~/Shared/knowledge-base
```

Give it a structure that mirrors how the team thinks, not how the org chart looks:

```
~/Shared/knowledge-base/
├── CLAUDE.md                  # Root index (the table of contents)
├── engineering/
│   ├── deploy-runbook.md
│   ├── incident-response.md
│   └── adr/                   # Architecture decision records
│       ├── 001-postgres-over-mongo.md
│       └── 002-event-sourcing.md
├── product/
│   ├── roadmap-process.md
│   └── spec-template.md
├── ops/
│   ├── oncall-rotation.md
│   └── vendor-contacts.md
└── policies/
    ├── security-baseline.md
    └── data-handling.md
```

### The root CLAUDE.md as index

The single most useful file is the root `CLAUDE.md`. It acts as the table of contents that tells the agent what exists and where to find it. Claude Code reads `CLAUDE.md` automatically when the directory is in scope. Cowork reads it when granted folder access. A good root index does not contain the knowledge; it points at it, so the agent loads only what the current task needs (progressive disclosure through the filesystem).

```markdown
# Company Knowledge Base

This repo holds shared static documentation for engineering, product, and ops.
Read the file relevant to your task. Do not guess; if it is not written here,
it is not a company convention.

## Engineering
- Deploy procedure: engineering/deploy-runbook.md
- Incident response: engineering/incident-response.md
- Architecture decisions: engineering/adr/ (one file per decision)

## Product
- How we run roadmap: product/roadmap-process.md
- Spec format: product/spec-template.md

## Ops
- On-call rotation and escalation: ops/oncall-rotation.md
- Vendor and account contacts: ops/vendor-contacts.md

## Policies (read before any external-facing or data work)
- Security baseline: policies/security-baseline.md
- Data handling rules: policies/data-handling.md
```

This is the `~/Shared/CLAUDE.md` pattern referenced elsewhere in the guide, expanded into a working structure. The same file serves both tools because both tools read the filesystem.

### Obsidian as an optional human layer

The repo is the source of truth and the machine-readable interface. Humans still want a comfortable way to browse and edit. Obsidian fits cleanly on top because an Obsidian vault is just a folder of Markdown files. Point Obsidian at `~/Shared/knowledge-base/` and you get backlinks, graph view, and a fast editor, while git underneath keeps the version history and the agent keeps reading the raw `.md` files.

Nothing about Obsidian is required. It is a viewer and editor for people who like it. The agent never sees Obsidian; it sees the Markdown. If half your team prefers VS Code or a plain text editor, that works identically. Keep the Obsidian-specific syntax (wikilinks like `[[note]]`, callouts) light if you want the files to read cleanly as standard Markdown for the agent, since deeply nested Obsidian plugins produce syntax the agent has to parse around.

### When direct file reading is enough

For static docs, direct file reading is both the simplest and the most accurate approach, up to a point. The agent opens the file and reads the exact content with no retrieval layer in between. There is no embedding step that might miss a relevant passage, no chunking that splits a procedure across two retrieved fragments. The crossover where this stops scaling is covered in Tier 3. For the typical team KB of dozens to a few hundred documents, Tier 1 alone is the right answer, and you should resist adding retrieval infrastructure before you actually need it.

---

## Tier 2: MCP Connectors for Live Systems

Static docs are the easy half. The harder half is the knowledge that lives in systems other people update all day: the Jira backlog, the Confluence space, the CRM, the internal metrics API. You cannot copy this into a Markdown repo, because it is stale the instant you copy it. A sprint board changes hourly. A customer record changes when support touches it. The right approach is to connect the agent to the system of record, so it reads the current state on demand.

The mechanism is MCP (Model Context Protocol). An MCP server exposes a live system as a set of tools the agent can call. Claude Code adds MCP servers through its config. Cowork ships native connectors and plugins for the common ones. The principle is the same in both: the agent queries the live source rather than a synced copy.

### Atlassian (Jira + Confluence)

Atlassian is the most common case because so many teams run Jira and Confluence together. The good news is that one connection covers both.

For Cowork, there is a native Jira plugin. A non-developer PM can install it and ask Cowork to read tickets, summarize a sprint, or draft a status update from live board state, all without touching a terminal.

For Claude Code, use the Atlassian Remote MCP server, which covers both Jira and Confluence through a single authenticated connection:

```bash
# Add the Atlassian Remote MCP server to Claude Code
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse
```

The first call triggers an OAuth flow in the browser. After authorizing, Claude Code can read Jira issues and Confluence pages with the permissions of the authenticated user.

The important consequence: **if your static docs already live in Confluence, you may not need to migrate them at all.** The same Atlassian MCP connection that reads tickets also reads Confluence pages. That gives the agent live access to the existing KB with zero migration. The tradeoff versus Tier 1 is real (no git history, no pull-request review, connector dependency), so the decision is about whether you value those repo properties enough to move the content. For docs that are already well-maintained in Confluence and change often through the wiki UI, leaving them in place and connecting via MCP is the lower-effort path.

### Notion

Notion offers an official remote MCP server at `mcp.notion.com`, plus a Claude Code plugin that packages Notion-specific skills.

```bash
# Add the official Notion MCP server
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

After the OAuth handshake, the agent can search the workspace, read pages and databases, and (with write scopes) create or update content. If your team runs its KB in Notion, this is the direct equivalent of the Atlassian case: connect to the live workspace rather than exporting it. The plugin layer adds curated skills (for example, a structured "create a project page from this spec" workflow) so the team is not re-describing the same Notion operations every session.

### GitBook

If your published documentation runs on GitBook, you get MCP access with no setup beyond knowing the URL. Every published GitBook site exposes a native MCP endpoint at `/~gitbook/mcp`.

```bash
# Point Claude Code at a GitBook site's native MCP endpoint
claude mcp add --transport http docs https://docs.yourcompany.com/~gitbook/mcp
```

That gives the agent live search over the current published docs, always reflecting what readers actually see. For teams whose external or internal documentation already lives on GitBook, this is the lowest-friction live-docs connection available, because there is nothing to host and nothing to sync.

### Choosing Tier 1 vs Tier 2 for documentation

Both tiers can hold "documentation," and the choice between them is not always obvious. The deciding question is how the docs change and what review you want around them.

| Signal | Lean Tier 1 (Markdown repo) | Lean Tier 2 (MCP to wiki) |
|--------|------------------------------|----------------------------|
| Docs change via deliberate, reviewed edits | ✅ | |
| Docs change constantly through a web UI by many people | | ✅ |
| You want pull-request review on every change | ✅ | |
| Content already lives in Confluence/Notion/GitBook and is maintained | | ✅ |
| You want git history, diff, and blame | ✅ | |
| You want zero migration | | ✅ |
| Same agent must also read tickets/records from that system | | ✅ (one connector covers both) |

Many teams end up with both: engineering standards and ADRs in a Markdown vault (Tier 1), product wiki and tickets via Atlassian or Notion MCP (Tier 2). That is correct. The two tiers are not competitors; they serve content with different change patterns.

---

## Tier 3: RAG at Scale

Tiers 1 and 2 cover almost every team. Tier 3 exists for one specific situation: you have so many documents that the agent cannot read them directly, and search over a connector is too coarse. At that point you add a retrieval layer (RAG, retrieval-augmented generation) that indexes the corpus and returns the most relevant fragments for each query.

### The threshold: when to add RAG

Do not add RAG by default. It is infrastructure, and infrastructure has a maintenance cost. The 2026 benchmark picture is consistent on the tradeoff:

- **Direct file reading is more accurate.** The agent reads the actual document, so nothing is lost to chunking or embedding mismatch.
- **RAG is faster at scale.** It avoids loading large corpora into context, returning only the relevant fragments.

The practical crossover sits at roughly **100 to 1,000 documents**, depending on document size and how much each query needs to span. Below that range, read files directly (Tier 1) or connect to the source (Tier 2); the agent can navigate a few hundred files and you keep the accuracy of direct reads. Above that range, the corpus no longer fits the direct-read model and a RAG layer, exposed to the agent as an MCP server, becomes worth the setup.

| Corpus size | Recommended approach |
|-------------|----------------------|
| < ~100 docs | Direct file reads (Tier 1) or live connector (Tier 2) |
| ~100 to ~1,000 docs | Judgment call; start direct, add RAG if retrieval quality drops |
| > ~1,000 docs | RAG layer as an MCP server (Tier 3) |

The signal that you have crossed the threshold is concrete: the agent starts missing relevant documents that you know exist, because it cannot hold or scan enough of the corpus per task. When that happens repeatedly, add retrieval. Not before.

### Onyx (self-hosted, open source)

[Onyx](https://github.com/onyx-dot-app/onyx) (formerly Danswer) is an open-source enterprise RAG platform you run yourself. It ships as Docker, includes 50+ connectors (Slack, Google Drive, Confluence, GitHub, Notion, and more), does hybrid search (keyword plus vector), and is Anthropic-compatible for the generation side.

```bash
# Onyx runs via Docker Compose (self-hosted)
git clone https://github.com/onyx-dot-app/onyx.git
cd onyx/deployment/docker_compose
docker compose -f docker-compose.dev.yml up -d
```

Onyx is the strong choice when data must stay on your own infrastructure and you want a single index across many sources. One caveat to set expectations correctly: Onyx is primarily its own chat platform. It is not natively wired into Claude Code or Cowork the way the Tier 2 connectors are. To use it from Claude Code, you connect through Onyx's API surface (exposed as an MCP server in front of it). That is more integration work than the managed options below, and you take on running the stack. The payoff is full control and on-premise data residency, which is exactly what some teams require (see the governance section).

### LlamaCloud (managed)

[LlamaCloud](https://cloud.llamaindex.ai/) is a managed RAG service with an official MCP server, which means Claude Code can query it directly without you running a retrieval stack.

```bash
# Connect Claude Code to LlamaCloud's managed RAG via its MCP server
claude mcp add --transport http llamacloud https://mcp.llamaindex.ai/sse
```

You upload and index your corpus in LlamaCloud, and the agent queries the index through the MCP tools. LlamaCloud pairs with LlamaParse for documents that resist naive extraction: complex PDFs with tables, multi-column layouts, scanned forms. If your KB is heavy on that kind of source (financial reports, contracts, technical datasheets), LlamaParse is the part that makes the difference, because clean parsing is what determines whether retrieval returns usable fragments.

### Ragie (fastest managed setup)

[Ragie](https://www.ragie.ai/) is a managed RAG service positioned around getting a working index up quickly. When the goal is "stand up retrieval over our docs this afternoon, not this sprint," Ragie is the lowest-setup managed option. You point it at your sources, it indexes, and you query it from the agent. The tradeoff against LlamaCloud is breadth of parsing and tuning control; the tradeoff against Onyx is that it is managed (no on-premise residency). Pick it when speed to a working index matters more than fine control.

### Tier 3 options compared

| Option | Hosting | Setup effort | Native MCP for Code | Best when |
|--------|---------|--------------|---------------------|-----------|
| **Onyx** | Self-hosted (Docker) | High | No (via its API) | Data must stay on-prem; many sources, one index |
| **LlamaCloud** | Managed | Medium | Yes | Complex PDFs (LlamaParse); want managed but tunable |
| **Ragie** | Managed | Low | Yes | Fastest path to a working index |

---

## The Plugin Pattern: Distributing Team Workflows

The third shape of knowledge from the opening table is not documents at all. It is reusable behavior: the slash commands, skills, agents, and prompts that encode how your team works. A `/deploy-checklist` command, a `incident-summary` skill, a code-review agent tuned to your standards. These are not content to store; they are behavior to distribute, and the distribution mechanism is a plugin.

### Keep content in the vault, behavior in the plugin

The clean separation that holds across all three tiers: **content lives in the vault (Tier 1) or the source system (Tier 2/3); behavior lives in the plugin.** A plugin does not embed the knowledge base. It references it. A skill that summarizes incidents reads the incident docs from `~/Shared/knowledge-base/engineering/`; the skill is the behavior, the docs are the content. This keeps each updatable on its own cycle. You revise a runbook without re-releasing a plugin, and you improve the workflow without touching the docs.

### What a plugin packages

A Claude Code plugin bundles, in a single installable unit:

- **Slash commands** (`commands/`): named workflows the team invokes, like `/release` or `/oncall-handoff`
- **Skills** (`skills/`): structured capabilities the agent loads when relevant
- **Agents** (`agents/`): specialized sub-agents with their own instructions and tools
- **MCP configs**: the Tier 2/3 connector definitions, so installing the plugin also wires up the live-system access

That last point is what makes the plugin the right home for the whole KB access layer. A new team member installs one plugin and gets the team's commands, the team's skills, and the team's MCP connections to Jira, Notion, or the RAG index, all configured. They are not hand-editing MCP config or copying command files.

### Distribution via marketplace.json

Plugins are distributed through a marketplace, a git repository with a `marketplace.json` manifest that lists the available plugins. The team publishes its plugin to an internal (or public) marketplace repo, and members install from it:

```bash
# Add the team's marketplace, then install the KB plugin
claude plugin marketplace add yourcompany/claude-plugins
claude plugin install knowledge-base
```

A minimal `marketplace.json` entry:

```json
{
  "name": "yourcompany-plugins",
  "plugins": [
    {
      "name": "knowledge-base",
      "description": "Team KB access: commands, skills, and live-system MCP connectors",
      "source": "./plugins/knowledge-base"
    }
  ]
}
```

When you improve a command or add a skill, you push to the marketplace repo and the team updates with one command. The workflow knowledge stays versioned and reviewed, the same way the static docs do, and it propagates to everyone without manual file copying. This is exactly the model this guide's own [plugins ecosystem](https://github.com/FlorianBruniaux/claude-code-plugins) uses: templates authored once, distributed as installable plugins.

---

## Governance and Sensitivity Caveat

The architecture above optimizes for access. Before you wire a sensitive corpus into it, weigh the governance side honestly, because the two agentic tools are at different maturity levels here.

### Cowork's current gaps

As of mid-2026, Cowork is a research preview, and its enterprise governance has gaps that matter for regulated or sensitive data. Two in particular:

- **Audit logs**: enterprise-grade, queryable audit trails of what the agent accessed and did are not yet complete. If your compliance posture requires a full record of every document read and every action taken, Cowork does not yet give you that.
- **DLP (data loss prevention)**: integration with enterprise DLP tooling is limited. The controls that prevent sensitive data from leaving approved boundaries are not as mature as in established enterprise software.

The practical reading: Cowork is appropriate for internal-but-not-secret knowledge (process docs, product context, general ops) while these gaps close. It is not yet the tool to point at your most sensitive corpus if you operate under strict audit or DLP requirements. Claude Code, with its more established permission and hook system, gives you more control points, but you should still validate against your specific compliance needs rather than assume coverage.

### When data must stay on-premise

If the data is sensitive enough that it cannot leave your infrastructure at all, the answer is not "connect a cloud RAG service." It is to keep everything inside a boundary you control. The relevant pattern, in research preview as of May 2026, is enterprise self-hosted sandboxes with private MCP tunnels: the agent runs in a sandbox on your infrastructure, and its connection to the internal KB goes through a private MCP tunnel that never exposes the data externally. The Tier 3 self-hosted option (Onyx) fits this model on the retrieval side, because the index and the documents stay on your hardware.

This is more setup than any managed path. The point is that the option exists, so "our data is too sensitive for the cloud" is a configuration question, not a reason to abandon the agentic KB entirely. Match the deployment to the data sensitivity rather than forcing one approach for all of it.

### A documented reference point

Anthropic's own documentation shows the live-KB-via-MCP pattern in action. The example endpoint `https://kb.internal.example.com/mcp`, described as "Internal knowledge base and documentation search," is the canonical shape: an internal KB exposed as an MCP server that the agent queries on demand. That is Tier 2 (or Tier 3 behind it) for a self-hosted KB, and it is the pattern the self-hosted-sandbox approach above secures.

---

## What to Do First

The mistake at the start of this section was reaching for one tool. The correction is to classify each piece of knowledge by its nature, then apply the matching tier. Here is the decision path, from the most common starting point outward.

### Decision table

| If your situation is... | Start with | Why |
|-------------------------|------------|-----|
| Static team docs, dozens to a few hundred files | **Tier 1**: Markdown vault at `~/Shared/`, root `CLAUDE.md` index | Both tools read it directly, full history, no connector |
| Docs already well-maintained in Confluence/Notion/GitBook | **Tier 2**: MCP connector to that system | Zero migration; one connector also covers tickets/records |
| Need live tickets, sprint state, CRM records | **Tier 2**: Atlassian / Notion / source MCP | Live source of truth, never a stale copy |
| More than ~1,000 documents and the agent misses things | **Tier 3**: RAG as MCP (LlamaCloud/Ragie managed, Onyx self-hosted) | Retrieval scales past the direct-read limit |
| Reusable team commands, skills, agents to share | **Plugin** via `marketplace.json` | Behavior distributes as one installable unit, configs included |
| Sensitive data that cannot leave your infrastructure | **Self-hosted** (Onyx + private MCP tunnel / enterprise sandbox) | On-premise residency, agent stays inside your boundary |

### The recommended sequence for a new team

1. **Stand up Tier 1 first.** Create the shared Markdown repo, write the root `CLAUDE.md` index, clone it to `~/Shared/` on every machine. This alone covers most of what both Code and Cowork need, and it is cheap to maintain. Resist adding retrieval infrastructure before you have evidence you need it.

2. **Connect the one or two live systems that matter most.** Usually Jira (Atlassian MCP) for engineering and product, plus whichever wiki holds your existing docs if you choose not to migrate them. Add Tier 2 connectors one at a time, not all at once.

3. **Package your recurring workflows as a plugin** once you notice the team re-describing the same operations every session. Publish it to an internal marketplace so installation is one command. Keep the content in the vault and the behavior in the plugin.

4. **Add a RAG layer only when the corpus outgrows direct reads.** The signal is the agent repeatedly missing documents you know exist. Until that happens, Tier 3 is cost without benefit.

5. **Check governance against your actual data sensitivity** before pointing either tool at a sensitive corpus, with extra care for Cowork's current audit and DLP gaps. For data that cannot leave your infrastructure, go self-hosted from the start rather than retrofitting it later.

The teams that succeed treat these as three separate problems with three separate tools, wired together through MCP and plugins, rather than one storage decision they have to get perfect upfront. Start with the Markdown vault, connect the live systems you actually query, and add scale and packaging as the need shows up.

> **See also**: [§9.25 Harness Engineering](#925-harness-engineering-at-agent-throughput) for the single-repo version of the knowledge-as-files principle. [§9.18.4 Documentation Formats for Agents (llms.txt)](#9184-documentation-formats-for-agents-llmstxt) for making docs discoverable. The [MCP Servers Ecosystem](./mcp-servers-ecosystem.md) for the full connector catalog. The [Third-Party Tools guide](./third-party-tools.md) for the RAG platforms in context. For Cowork specifics, the [AI Ecosystem guide §9](./ai-ecosystem.md#9-claude-cowork-research-preview).
