# Resource Evaluation: Switch (Flint AI / SandboxAQ, agent-human chat bridge)

**URL**: https://github.com/sandbox-quantum/switch
**Type**: GitHub repository (Apache 2.0 + Commons Clause), self-hosted server + Electron desktop console + connectors for Claude Code / Codex / OpenCode
**Evaluation date**: 2026-08-27
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.42.0
**Method**: source analysis of a local clone at `~/Sites/divers-tests/switch`, `main` branch (pushed 2026-08-26), plus `gh api repos/sandbox-quantum/switch` for repository metadata. No install, no server deployment, no live Matrix room was run against it.

---

## Content summary

Switch is infrastructure connecting AI agents and humans in the same conversation, in the chat apps a team already uses (Slack, Microsoft Teams, Discord, Telegram, Mattermost). It uses **Matrix** (server Tuwunel) as the internal message bus: every participant, human, agent, or collaboration bridge, is a Matrix client (`matrix-nio`). A Switch room maps to one external channel via a database row, so the mapping survives a restart.

Three components: `core/switch_core/` (FastAPI server, the Agent Bridge agents register against and authenticate to via API key, plus the collaboration bridges); `gateway/` (React admin UI for agents, rooms, resources, keys); `console/` (an Electron desktop app, forked with upstream attribution, that manages local coding-agent sessions, which rooms an agent belongs to, and auto-starts a Claude Code session when addressed in Slack with none running).

The protocol (`docs/official/internals/agent-protocol.md`): one SSE stream down per connection, HTTP up for every agent action, four connection models (`always_on`, `session_addressable`, `auto_session`, `session_passive`) describing how an agent is actually reachable rather than assuming uniform liveness. Authorization is a single chokepoint (`authz.py`): `can(principal, action, resource)`, an agent-initiated request resolves to its owner's identity and inherits exactly that owner's permissions, public/private visibility per resource.

The Claude Code connector (`connectors/claude-code-plugin/hooks/switch_hook.py`) hooks into Claude Code's pre/post tool-call lifecycle to mediate actions and report events back to the bridge; equivalent connectors exist for Codex and OpenCode.

---

## The core mechanism, verified in code

`core/switch_core/authz.py` is a small, pure module (no DB, no I/O), 89 lines: `Action = Literal["read", "write", "delete"]`, one `can()` function, uniform across References, Documents, Packages, and Rooms. Consolidates what the module's own docstring says was previously scattered as ad-hoc `owner == user or public or admin` checks across call sites, a real simplification if the claim holds across the codebase (not independently traced call-site by call-site in this pass).

`docs/official/internals/collaboration-bridge.md` documents the bridge adapter contract directly: `start`, `stop`, `send_message`, `update_message`, `delete_message`, `send_typing`, `create_channel`, `add_agents_to_channel`, `translate_inbound`/`translate_outbound`. Five adapters ship (Slack Socket Mode, Mattermost WebSocket, Discord Gateway WebSocket, Telegram Bot API polling, Microsoft Teams as a self-hosted HTTP listener, the only one requiring a public address). The bridge itself is a Matrix participant: it joins rooms and only sees what happens after it joins, a real constraint on backfilling history through a newly added bridge, not just a design note.

Distribution is more production-shaped than a single GitHub repo usually is at six weeks old: `docs/official/deploy/self-host.md` documents a Docker Compose artifact (`ghcr.io/sandbox-quantum/standalone-compose`) and a Helm chart (`oci://ghcr.io/sandbox-quantum/charts/switch`), both stamped with the same release version, plus a dedicated `RELEASING.md` at repo root.

---

## Project health

Measured on `main`, pushed 2026-08-26, via local `git log` and `gh api repos/sandbox-quantum/switch`.

| Metric | Value |
|---|---|
| Created | 2026-07-16 (about 6 weeks old at evaluation date) |
| Total commits | 449 |
| Louis Amaudruz (`Louis Amaudruz` + `amaudruz`) | 359 commits (80%) |
| Christian McDermott | 36 commits (8%) |
| Third human, Paul Abbazia | 5 commits (1%) |
| Bot/automation accounts | switch-releaser, switch-worker-louis-remote, socket-fix[bot], github-actions[bot], dependabot[bot], cla-assistant[bot], autofix-pr-bot[bot] |
| GitHub stars | 252 |
| Forks | 13 |
| Open issues | 12 |
| Core package version | `0.21.0` (`core/pyproject.toml`), pre-1.0 |
| License field (GitHub API) | `NOASSERTION` (Commons Clause modification is not an SPDX-recognized license, GitHub cannot classify it) |

**Bus factor close to 1, not exactly 1.** One person at 80%, a second at 8%, both real humans with sustained contribution (not a single-commit drive-by), backed by SandboxAQ (a funded quantum-security company, not a solo side project) under the product name Flint AI. 252 stars in 6 weeks is faster traction than most entries on this repo's watch list crossed at their own evaluation point (fp.dev and ICM were watched at far lower counts). Weigh this against: no independent production-adoption story found in this pass, no second organization's fork or contribution visible in the commit list, and the license's `NOASSERTION` status on GitHub is itself a minor adoption friction (automated license scanners in enterprise pipelines will flag it for manual review).

---

## Where it sits relative to the guide's existing coverage

Three sections were checked as candidate homes before concluding this is a genuine gap, not a placement failure:

`guide/core/memory-systems.md` §4.7 ("Why the Team Gap Is Structural") documents six barriers to *semantic* team memory (single-tenant storage, OAuth cost, taxonomy standards, enterprise buyers). Switch has no embedding store and no retrieval layer; it is a real-time bus, not a memory system. `authz.py`'s owner-inheritance model is a relevant data point on the OAuth-cost barrier specifically, but placing Switch itself in this section would misclassify what it is.

`guide/ecosystem/third-party-tools.md` "Multi-Agent Orchestration" (abtop, Conductor, Agent Orchestrator, lines 1409-1536) and "External Orchestration Frameworks" (Ruflo, Athena Flow, Pipelex + MTHDS) share one axis: multiple instances of the same coding agent, on one machine, coordinated through git worktrees and PR/CI feedback. Switch's axis is different: heterogeneous agents (Claude Code, Codex, LangChain, anything speaking the protocol) reaching humans on five *external* chat platforms, mediated through a governed identity model. Not a variation of the existing entries, a different category.

`guide/ecosystem/ai-ecosystem.md` §8.1 "agent-chat" (lines 1655-1666) is tagged "Slack-like" in the guide's own prose, which reads as coverage of the same space until the code is checked: it is a read-only SSE dashboard over Gas Town's `beads.db` and multiclaude's JSON logs, no live external platform connection, no auth model, explicitly incompatible with standalone Claude Code. Structurally a monitoring tool, not a bridge.

`third-party-tools.md` "Known Gaps" (lines 1850-1866), the section that already names capability holes the guide has identified but not filled (Sandcastle, fp.dev, and others), has no entry for "cross-platform agent-human chat bridge with governance." That confirms the gap rather than resolving it.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 4 | No comparable entry exists anywhere in the guide's current coverage; a formalized agent-liveness protocol (four connection models) and an owner-inheritance authz model are both real design decisions, not marketing claims |
| Production reliability | 2 | Pre-1.0 (`0.21.0`), 6 weeks old, bus factor close to 1 (80% one author), no independently confirmed production deployment found outside the vendor's own demo videos |
| Documentation quality | 4 | Full published docs site (`docs/official/`), an explicit agent-protocol spec, a collaboration-bridge adapter contract, self-host instructions with pinned versioned artifacts |
| Adoptability | 2 | Requires operating a Matrix homeserver plus N bridge processes; heavier operational footprint than most tools this guide covers for individual Claude Code users, though Switch Console lowers the bar for a first trial without self-hosting |
| Guide value | 3 | Fills a real, previously unfilled category gap, but as a single-vendor early example with no comparable peer yet, not a category with enough breadth for a dedicated comparison page |
| **Overall** | **3** | Useful addition, not urgent. Real category gap-filler, but too young and too single-vendor for more than a pointer. |

This overall score is one point above the 2/5 a prior assessment estimated from a summary alone, without access to the clone's git history or `gh api` metrics. The 252-star, 6-week traction and the Docker Compose/Helm release engineering found in this pass are stronger production-shape signals than "cloned today, zero recul terrain" assumed; the bus-factor and pre-1.0 concerns that assessment raised hold up and are reflected in the Production reliability and Adoptability scores.

---

## Decision

**Do not integrate a dedicated guide section. Add one line to `third-party-tools.md` "Known Gaps" naming the category and citing Switch as the first observed candidate, plus a watch-list entry.**

The guide's precedent for a dedicated file (`ai-executive-agents.md`, `agent-harness-landscape.md`) is a comparison of many peer projects with a routing table, not a write-up of a single vendor. No peer to Switch (a governed, multi-platform, multi-framework agent-human chat bridge) was found anywhere in this evaluation's research; writing a standalone section now would read as a product page for one company's OSS release, not guide-neutral coverage.

**Revisit trigger**: a second, independent chat-bridge tool with comparable scope appears (making a comparison table possible), or Switch reaches a tagged `1.0.0` release, or an independently documented production deployment (not from SandboxAQ/Flint AI) surfaces.

---

## Sources

All paths relative to a clone of `github.com/sandbox-quantum/switch` at `main` (pushed 2026-08-26): `README.md`, `CLAUDE.md`, `LICENSE`, `RELEASING.md`, `core/switch_core/authz.py`, `core/switch_core/matrix_admin.py`, `core/pyproject.toml`, `connectors/claude-code-plugin/hooks/switch_hook.py`, `connectors/{codex-plugin,opencode-plugin}/`, `docs/official/internals/{agent-protocol,collaboration-bridge,matrix-substrate}.md`, `docs/official/deploy/self-host.md`, `console/CLAUDE.md`. Repository metadata via `gh api repos/sandbox-quantum/switch` (2026-08-27). Git history via local `git log --format` and manual author aggregation (not truncated by any output-compressing proxy).
