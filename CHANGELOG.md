# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- **New guide section §5.5 — Registry-based Discovery: ctx7 CLI** (`guide/ultimate-guide.md`): Context7's CLI companion (`npx ctx7`) for automated skill discovery and MCP setup. Documents `ctx7 skills suggest` (dependency-aware skill recommendations), `ctx7 skills install owner/repo`, `ctx7 setup --claude` wizard, and `ctx7 docs` terminal lookup. Clarifies agentskills.io (open spec) vs context7.com/skills (registry) relationship. Cross-reference note added to `guide/ecosystem/mcp-servers-ecosystem.md` Context7 section. Resource evaluation: `docs/resource-evaluations/2026-03-17-context7-cli.md` (score 4/5).

- **Doc audit — stats sync**: corrected stale counts across guide + landing. Templates: 204/216/217/218/222/232 → unified to 217 (per `check-landing-sync.sh` logic). Guide lines: "22K" → "23K+" (actual: 23,422). Quiz: reference.yaml `quiz_count` and llms*.txt had 311 → corrected to 271 (actual count). Version in llms.txt / llms-full.txt / machine-readable/llms.txt bumped 3.36.0 → 3.37.0. Landing updated: FeaturesGrid, GuideComparison, WhyGuide, McpDemo, cheatsheet page, index.astro, compare page, and guide content files (00-introduction, index, 09-advanced-patterns, 12-appendices).

## [3.37.0] - 2026-03-17

- **ICM v0.5.0 — setup guide + session starter template**: corrected `icm init` documentation (3 explicit modes: `--mode mcp`, `--mode hook`, `--mode skill` — not a single interactive command); fixed CLI syntax (`--importance` is an enum `critical|high|medium|low`, not a float; no `memory` subcommand); added `examples/memory/icm-session-starter.md` ready-to-use onboarding prompt to paste at the start of any session.

- **New guide section — MCP vs CLI Decision Guide** (`guide/ecosystem/mcp-vs-cli.md`): full comparison of MCP servers vs CLI tools across 4 decision dimensions (user type, model capability, observability needs, schema stability), decision matrix by situation, token cost analysis, tooling overview (RTK, MCPorter, mcp2cli), and practitioner quotes. Cross-linked from `mcp-servers-ecosystem.md`. Landing page published at `cc.bruniaux.com/ecosystem/mcp-vs-cli/` with 4 decision cards, 15-row collapsible guidance table, practitioner quotes section, and tooling micro-section. `check-landing-sync.sh` extended with section 7 for MCP vs CLI sync tracking.

- **Resource evaluations (3)**: mcp2cli (3/5, MCP/OpenAPI/GraphQL to runtime CLI, 96-99% token savings claim, 8-day-old tool with structural mismatch against Claude Code native MCP architecture — watch list + document schema overhead insight); MCPorter by Steinberger (3/5, TypeScript MCP toolkit with auto-discovery, CLI generation and TS codegen — useful companion for testing MCP servers and hook scripts); CircleCI MCP vs CLI blog (3/5, inner loop / outer loop decision framework, 6-question guide, directional browser automation benchmark — worth borrowing the vocabulary, not the benchmark numbers).

- **WP10 v1.2.0 — Marc Sélince feedback (DAF/finance)**: 6 corrections FR+EN on `10-budget-ia.qmd` / `10-ai-budget.qmd`. New `## Pour le DAF/CFO` section (ROI + OpEx/CapEx framing, replaces placeholder callout). New `## Freins COMEX au-delà du coût` Q&A section (vendor dependency, IP risk, lock-in pricing). §3.1 reframed "Attraction et rétention des top performers" (market tight for seniors/experts, not all profiles). §3.2 CTO: new "ROI des heures d'ingénieur" sub-point (LLMs on mechanical code free engineering time for architecture). §4.1 Budget: option 4 added (replace paid tool with OS equivalent for net-zero pilot), "200-500$/mois" figure removed from discretionary budget.

- **Recap cards — EN translations created + FR fixes**: 57 EN recap cards created from scratch (`whitepapers/recap-cards/en/`) by translating all FR cards. FR cards batch-updated: `guide-version` and `version` fields bumped `3.32.1` → `3.36.0` across all 57 FR cards. Factual fixes: T19 (context window) corrected "1M beta, API only" → "1M GA for Max/Team/Enterprise CC plans (v2.1.75, no header needed)"; T01 (essential commands) updated with `/plan`, `/effort`, `/branch`, `/rename`, `/loop`, `/voice`, `/fast`, removed non-existent `/cost`, corrected keyboard shortcuts. `docs/for-cto.md` updated: "whitepapers coming soon" → links to `florian.bruniaux.com/guides` in all 4 occurrences.

- **Fix dead link** (`guide/ultimate-guide.md` §3.5): Packmind anchor `../ecosystem/third-party-tools.md#packmind` corrected to `ecosystem/third-party-tools.md#packmind` (wrong `../` prefix was resolving outside `guide/`).

- **Whitepapers v2.2 — Guide content sync (7 WPs updated)**: synced WP content with guide v3.27.6 → v3.36.0 delta.
  - **WP00** (v1.2.0): 1M context corrected "beta" → GA (v2.1.75); 7 major features table added (Tasks API, Auto-memories, Agent Teams, LSP Tool, Remote Control, MCP Elicitation)
  - **WP03** (v1.1.0): PreToolUse security fix callout (v2.1.77 — `"allow"` bypassed enterprise `deny`); `allowRead` sandbox parameter added
  - **WP05** (v1.2.0): Native Code Review section (Research Preview, Teams/Enterprise) — multi-agent, 3 trigger modes, `REVIEW.md`, ~$15-25/PR pricing
  - **WP07** (v1.1.0): 12 new slash commands, 7 new hook events, extended CLI flags, Remote Control section, 1M GA correction
  - **WP08** (v1.2.0): Identity drift after compaction pattern added (UserPromptSubmit hook + agent-identity.txt re-injection)
  - **WP09** (v1.1.0): Review bottleneck inversion section; Regulatory Exposure section (EU AI Act GPAI/high-risk, FDA AI/ML Guidance)
  - WP02: no hook events section in scope; WP01/WP04/WP06/WP10: no gaps identified

- **Cheatsheet + reference.yaml maintenance**: date updated February → March 2026 in `guide/cheatsheet.md`; "Command not found" fix updated to use native installer (`curl | sh`); `machine-readable/reference.yaml` `updated` field bumped to 2026-03-17.

- **Whitepapers v2 — Reviewer corrections** (6 relecteurs: Edouard, Mat, Nicolas, Marc, Anthony, Emmanuel): 8-phase correction plan applied across 10 whitepapers (WP00–WP10) FR+EN.
  - **Phase 1 — Factual errors**: npm "deprecated" → "not recommended" (WP00), native installer added as primary install method (WP00 EN), context window 200K vs 1M clarified (WP00 FR+EN), Claude Max ratio corrected to range 1.5-3% FR / 1-1.6% EN (WP10), sub-agents vs agent teams difference correctly stated as P2P messaging + coordination tools, not context isolation (WP08 EN)
  - **Phase 2 — Accents + articles + typos**: ~200+ accent corrections across WP08 FR (977 lines); anglicisms corrected in WP02 FR (on-demand, per-project, Memories, Feature opt-in); table row reformulated in WP00 FR; accents restored in WP02 FR (~10 passages)
  - **Phase 3 — Malformed sentences**: "chez dans une fintech" fixed, meta-sentence "This is the single definition..." removed (WP08 FR+EN); "Multiple Claude instances..." rewritten as complete sentence (WP05 FR+EN); Turnkey Quickstart explained (WP05 FR+EN)
  - **Phase 4 — Anglicisms + clarifications**: tmux noted as external tool, not built-in (WP08 FR+EN); "OUI →" residue fixed in WP05 EN; user-level/project-level translated (WP05 FR)
  - **Phase 6 — WP08 structural corrections**: "~30K lines" clarified as "~30K lines ≈ 1M tokens"; continuous merge definition improved; note added that solo Claude Code agent is a full autonomous agent, not a chatbot
  - **Phase 7 — WP10 restructuration**: executive summary added (5 key metrics); learning curve duplication removed; BCG 2025 source improved; pricing note "March 2026" added; "5-10 people in 2020" reformulated without unsourced claim; "Beyond engineering teams" section expanded with 3 concrete use cases; CFO/DAF and change management placeholder callouts added

- **Resource Evaluation #078 + integration** (`guide/ultimate-guide.md`): HumanLayer — "Skill Issue: Harness Engineering for Coding Agents" (March 12, 2026). Score 3/5. "Harness Engineer" concept already covered in `guide/roles/ai-roles.md §10` (Martin Fowler source); ETH Zürich study already integrated. Two genuine gaps filled: (1) **Silent Success hook pattern** — asymmetric hook behavior (exit 0 = silence, exit 2 = re-engage agent) named and documented with example before §7.3; (2) **CLI vs MCP training-data argument** — familiar CLIs (git/grep/jq) are already in model weights, CLAUDE.md usage examples often beat a verbose MCP server for standard tools; added after MCP Tool Search section.

## [3.36.0] - 2026-03-17

### Documentation

- **Resource Evaluation #076**: Addy Osmani — "Stop Using /init for AGENTS.md" (Feb 23, 2026). Score 3/5. Secondary synthesis of ETH Zürich paper (already evaluated). Verified: ETH Zürich claims confirmed. Unverified: Lulla et al. (ICSE JAWs 2026) and ACE framework (ICLR 2026) — no findable academic source. Arize AI concept verified, specific numbers uncorroborated. Integration: added discoverability filter + anchoring risk concepts to §3.1, added research note (ETH Zürich), added `/init` warning in commands table.

- **Resource Evaluation #077 + integration** (`guide/roles/learning-with-ai.md`): "Comprehension Debt" article (LinkedIn, March 14, 2026). Score 3/5. Integrated: (1) "comprehension debt" as emerging term after Vibe Coding section, (2) review bottleneck inversion framing — juniors can now generate code faster than seniors can audit, (3) new "Regulatory Exposure" subsection for tech leads covering EU AI Act active dates (GPAI Aug 2025, high-risk Aug 2026) and FDA AI guidance (Jan + Jun 2025). Confirmed by Perplexity research.

- **Claude Code Releases**: Updated tracking to v2.1.77
  - Opus 4.6 default max output raised to 64k tokens; upper bound for Opus 4.6 and Sonnet 4.6 raised to 128k tokens
  - Security fix: `PreToolUse` hooks returning `"allow"` could bypass enterprise `deny` permission rules
  - `allowRead` sandbox setting; `/branch` replaces `/fork`; `/copy N` for Nth-latest response
  - Breaking: `Agent` tool `resume` parameter removed — use `SendMessage({to: agentId})` instead
  - Fixed auto-updater GBs memory leak; fixed `--resume` truncating recent history

- **Claude Code Releases**: Updated tracking to v2.1.76
  - MCP elicitation support — servers request structured input mid-task via interactive dialog
  - New hooks: `Elicitation`, `ElicitationResult`, `PostCompact`
  - `-n`/`--name` CLI flag for session display name; `worktree.sparsePaths` for monorepo sparse checkout
  - `/effort` slash command; fixed ToolSearch deferred tools losing schemas after compaction
  - Auto-compact circuit breaker (stops after 3 failures); fixed `Bash(cmd:*)` rules with `#` in args

- **Resource evaluation** (rejected, no file): LinkedIn post "Five Levels of Context Engineering" by Matthew Alverson (via Addy Osmani) — score 1/5, rejected. Content is a pedagogical reformulation of concepts already covered with more rigor in `guide/core/context-engineering.md`. Alverson's 5-level taxonomy is not empirically grounded and not widely cited in the literature. Evaluation surfaced 3 real gaps now addressed (see Added section). Better primary sources identified: Anthropic Engineering Blog (Sept 2025), MCP Maturity Model (Mitra, Nov 2025).

- **Resource evaluation** (no file — text digest): Anthropic weekly recap March 9-15, 2026 (5 Claude Code releases, Code Review launch, 1M GA, Spring Break promo, corporate news) — score 4/5. Two gaps actioned: (1) Code Review product feature added as `guide/workflows/code-review.md`; (2) 1M context status updated from beta to GA in `guide/ultimate-guide.md` lines 2021-2070. Source reliability note: digest incorrectly attributes Claude Code changelog to `anthropics/anthropic-sdk-python` (correct repo: `anthropics/claude-code`); Code Review pricing ($15-25/PR) verified against official docs.

- **Resource evaluation** (`docs/resource-evaluations/eval-claude-1m-context-window-jp-caparas.md`): JP Caparas article on 1M token context window — score 2/5, do not integrate. Central claim (flat pricing, no surcharge above 200K tokens) is factually wrong; invalidates the competitive pricing analysis. Fact-check table, comparative analysis vs guide, and independent action items (verify 1M GA status, potential update to guide lines 2028-2070 on beta/GA status).

### Changed

- **External support section — clarified positioning** (`docs/for-cto.md`, `docs/for-tech-leads.md`, `docs/for-cio-ceo.md`): Brown Bag Lunch, talks, and speaker/panelist slots (1-3h) explicitly marked as free and done for networking/challenge purposes. Training/consulting missions framed as open-but-not-actively-sought with "contact for availability and potentially pricing" wording. Contact link updated to `florian.bruniaux.com` across all three files.

### Fixed

- **`/release` skill — 3 correctness gaps** (`.claude/commands/release.md` Step 4): (1) Quiz count command fixed: `grep -c '  - id:'` was returning per-file counts and taking only the last file's value — replaced with `grep -r '  - id:' quiz/questions/ | wc -l` to sum across the entire directory. (2) `llms-full.txt` now documents all 4 occurrences requiring update (Metadata block, "For Learning" URL text, "Template Library" section heading, repo tree comment) — previously only Metadata fields were listed, causing silent drift. (3) Verification gate added after Step 4: bash block prints all three llms files' key fields side-by-side against expected values before the commit, making any mismatch visible immediately.

### Added

- **Resource evaluation #078: claude-swarm-monitor** (`docs/resource-evaluations/078-claude-swarm-monitor.md`): TUI dashboard (Rust + Ratatui) for monitoring multi-agent Claude Code workflows across git worktrees. Score 3/5 — watch-list. Unique angles: JSONL-native session file monitoring (distinct from agent-chat's SSE approach) and Docker stack visibility per worktree. Not integrated into guide yet — 10 stars, Linux-only, sub-agent tracking claim unverified. Re-evaluate at 50+ stars or confirmed macOS production use.

- **Packmind — Engineering Standards Distribution** (`guide/ecosystem/third-party-tools.md`, `guide/ultimate-guide.md`, `guide/ecosystem/mcp-servers-ecosystem.md`): Added Packmind (score 4/5, eval #076) as a new "Engineering Standards Distribution" section in third-party-tools. Tool distributes CLAUDE.md + slash commands + skills across repos and agents (Claude Code, Cursor, Copilot, Windsurf) from a single playbook, ships an MCP server, Apache-2.0 CLI self-hostable. Added cross-reference paragraph at end of ultimate-guide.md §3.5 (Team Configuration at Scale) linking the per-project `.claude/rules/` pattern to org-scale tooling. Added Packmind MCP server entry in mcp-servers-ecosystem.md Orchestration section.

- **3 new AI roles** (`guide/roles/ai-roles.md`): Added MLOps Engineer (§14), AI Developer Advocate (§15), and AI Orchestration Engineer (§16) as full role profiles. Includes responsibilities, required skills, salary benchmarks, entry paths, and key distinctions from adjacent roles. Sections 14→17 renumbered accordingly. Removed "Orchestration engineer" from "What's Not a Role Yet" — job postings at Vista Equity, Zapier, Heidi Health, and Adobe confirm it's now a real title. Career Decision Matrix and Salary Benchmarks updated with all 3 roles. Based on Perplexity market research (March 2026).

- **Failure-triggered context drift pattern** (`guide/core/architecture.md` §Session Degradation Limits): New subsection documenting a distinct degradation mode from compaction drift — repeated tool failures accumulate error noise that dilutes the original intent without filling the context window. Pattern: re-inject core task instructions on every command failure via `PostToolUse` hook, not just after `/compact`. Source: Nick Tune (2026-03-01). Resource evaluation: `docs/resource-evaluations/2026-03-16-nick-tune-workflow-dsl-ddd.md` (score 3/5 — 1 of 3 patterns integrated).

- **Identity re-injection after compaction** (`guide/ultimate-guide.md` §7.5 + `examples/hooks/bash/identity-reinjection.sh`): New hook pattern from Nick Tune (Feb 2026). Solves agent identity drift after context compaction in long sessions — `UserPromptSubmit` hook reads transcript, detects missing identity marker in last assistant message, re-injects `.claude/agent-identity.txt` as `additionalContext`. Configurable via `CLAUDE_IDENTITY_FILE` and `CLAUDE_IDENTITY_MARKER` env vars. `reference.yaml` updated with `identity_reinjection_hook` + `identity_reinjection_example` keys.

- **Security audit hardening — 3 patterns** (`examples/commands/security-audit.md`, `examples/agents/security-auditor.md`): (1) Pre-step added to `/security-audit`: asks dev/staging/prod before running — avoids false positives on debug flags and CORS `*` in local dev. (2) Anti-false-positive rule in Phase 2 (secrets scan): mandates running `git log --all -p` and checking `.gitignore` before raising any secret finding — no more findings based on pattern matching alone. (3) Paywall/billing checklist added to `security-auditor.md` under A04 Insecure Design: server-side limit enforcement, subscription status from DB, webhook signature verification, billing bypass endpoints, race conditions on resource creation.

- **Resource evaluation: VicKayro — claude-security-audit** (`docs/resource-evaluations/2026-03-16-vickairo-claude-security-audit.md`): Score 2/5. Single-file `/security-audit` command, OWASP Top 10 (2021) + 16 sections, MIT, 60 stars (18 days old). Substantial overlap with existing `security-audit.md`, `security-auditor.md`, and `security-hardening.md`. Genuine gaps: paywall/billing audit section (not covered anywhere), environment context pre-step (dev/staging/prod before auditing), and stricter anti-false-positive pattern for secrets (mandate `git log --all -p` proof before raising finding). Decision: extract 3 patterns into existing commands silently, no guide mention, revisit at 200+ stars.

- **Resource evaluation: Nick Tune — Hook-Driven Dev Workflows** (`docs/resource-evaluations/2026-03-16-nick-tune-hook-driven-workflows.md`): Score 3/5. Covers hooks-as-workflow-engine pattern: typed state machine (Zod), per-state SubagentStart context injection, agent respawn for fresh context windows, identity re-injection after compaction, JSON workflow persistence. Key gap confirmed: guide lacks identity re-injection after compaction + per-state SubagentStart injection. Tiered integration: identity re-injection → §7.5 now; SubagentStart injection → agent-teams.md (3-4 weeks); full state machine guide deferred 60-90 days (1 week of author testing, needs community validation). Prerequisites: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1, Opus 4.6, Node.js + TypeScript.

- **1M context window status update** (`guide/ultimate-guide.md` lines ~2021-2070): Updated from "beta" to GA for Max/Team/Enterprise Claude Code plans (v2.1.75, March 13 2026). Preserved distinction: direct API use still requires tier 4 / custom rate limits. Pricing table updated to reflect standard rates for plan users.

- **Code Review feature** (`guide/workflows/code-review.md` + cross-reference in `guide/ultimate-guide.md`): New workflow guide for Anthropic's Code Review research preview (Teams/Enterprise). Covers: multi-agent architecture and severity levels (🔴/🟡/🟣), full setup flow (admin URL `claude.ai/admin-settings/claude-code`, GitHub App permissions, 3 trigger modes — once/every push/manual), `@claude review` manual trigger, `REVIEW.md` schema with example, pricing model ($15-25 avg, billed via extra usage outside plan, spend cap at `claude.ai/admin-settings/usage`), analytics dashboard, and cross-links to manual CLI workflows + GitLab CI/CD. Verified against official docs at `code.claude.com/docs/en/code-review`.

- **Context engineering guide — 3 additions** (`guide/core/context-engineering.md`):
  - **"Most failures are context failures"** framing added to §1 Why It Matters — reframes troubleshooting from "the AI is bad" to "what's missing from context"
  - **Static vs. Dynamic context** — new subsection distinguishing CLAUDE.md (static) from runtime tool outputs and agent context (dynamic); includes reference to Anthropic's September 2025 engineering post on agent context engineering
  - **Maturity assessment §9** — Level 0-5 self-assessment grid grounded in Claude Code patterns (no CLAUDE.md → flat config → structured → modular → measured → full system); includes "what to do at each level" action table

- **Spring Break promotion note** (guide line ~2395): Documented Anthropic's March 13-27, 2026 promotion — 2x usage limits outside 5-11am PT (peak hours) and all weekends, bonus usage doesn't count against weekly limits, applies to Free/Pro/Max/Team. Includes CET timezone conversion for European users (2x from midnight-13h and 19h-24h France time). Source: Anthropic support article.

- **Smart-Suggest ROI script** (`examples/scripts/smart-suggest-roi.py`): Python stdlib-only analyzer for the `smart-suggest` UserPromptSubmit hook. Correlates suggestion log (`~/.claude/logs/smart-suggest.jsonl`) with session JSONL files to estimate command acceptance rate. Detects 4 acceptance signals: slash command tags, Skill tool use, Agent tool use, and text mention in next 5 user messages. Reports: summary, tier breakdown (Enforcement/Discovery/Contextual/Custom), top suggested/followed commands, never-followed list, and daily trend chart. CLI: `--since Nd`, `--no-sessions` (fast mode), `--json`, `--log PATH`.
- **ICM (Infinite Context Memory)**: New MCP memory server section after Kairn (~line 11365) — Rust single binary, zero deps, Homebrew install, dual architecture (episodic decay Memories + permanent knowledge graph Memoirs), 9 typed relation types, auto-extraction 3 layers, 14 editor clients. Score 3/5 — recommended as Rust-native alternative when Python dependency management is a friction point. Includes explicit license callout (Source-Available, free ≤20 people) and vendor-reported benchmark flags.
- **Comparison matrix update**: Added ICM column to MCP memory stack matrix (Runtime + License rows added for all tools)

## [3.35.0] - 2026-03-13

### Added

- **`guide/workflows/github-actions.md`** — 5 production-ready patterns for GitHub Actions CI/CD with `anthropics/claude-code-action` (6.2k stars, v1.0): on-demand PR review via `@claude` mention, automatic review on every push, issue triage and labeling, security-focused review on sensitive paths (`auth/**`, `payments/**`), scheduled weekly repo health check. Includes cost control table (Haiku vs Sonnet per pattern), concurrency setup, fork safety (`pull_request_target` guard), Bedrock/Vertex auth alternatives. Cross-linked from guide §9.3 and `guide/workflows/README.md`.

- **`guide/workflows/rpi.md`** — RPI: Research → Plan → Implement. 3-phase feature development with explicit GO gates: Research → `RESEARCH.md`, Plan → `PLAN.md`, Implement → working code. Slash command templates (`/rpi:research`, `/rpi:plan`, `/rpi:implement`), worked example (rate limiting on Express API), and comparison matrix vs Plan-Driven, TDD, Spec-First. Best for features where discovering a wrong assumption late is expensive.

- **`guide/workflows/changelog-fragments.md`** — Changelog Fragments workflow: one YAML fragment per PR, written at implementation time, validated by CI, assembled at release. 3-layer enforcement: CLAUDE.md workflow rule + `UserPromptSubmit` hook (3-tier: enforcement → discovery → contextual) + independent CI migration check. Documents the `UserPromptSubmit` tier pattern as a reusable architecture for any mandatory workflow step.

- **`examples/hooks/bash/smart-suggest.sh`** — `UserPromptSubmit` behavioral coach hook: Tier 0 enforcement (changelog fragment required before PR, plan-before-code), Tier 1 discovery (test-loop, retex, dupes, monitoring loop, security audit, release), Tier 2 contextual (code review, debugging, architecture, session resume). Max 1 suggestion per prompt, dedup guard, ROI logging to `~/.claude/logs/smart-suggest.jsonl`, silent exit on no match.

- **`guide/core/known-issues.md`** — "LLM Day-to-Day Performance Variance" section: session-to-session quality variance (shorter responses, conservative suggestions, edge-case refusals) documented as expected behavior, not a bug. 4 root causes: probabilistic inference, MoE routing variance, infrastructure variance, context sensitivity. Observable signals table and ruling-out checklist.

- **`examples/scripts/test-prompt-caching.ts`** — Standalone TypeScript script (zero deps, native fetch) to verify Anthropic prompt caching on any API key. Runs 3 identical calls, checks write/read metrics. Documents 4 undocumented production gotchas: `anthropic-beta: prompt-caching-2024-07-31` header required for Claude 4.x, effective threshold ~2048+ tokens, cached tokens excluded from `input_tokens`, new nested `cache_creation` object format.

- **`cc-sessions discover` documentation** — "Session Pattern Discovery" subsection in §2.x: `discover` subcommand n-gram mode (local, ~3s) vs `--llm` mode (semantic via `claude --print`), 20% rule decision framework (CLAUDE.md rule / skill / command), install instructions. Cross-reference added after the 20% rule callout in §5.1.

- **`examples/scripts/cc-sessions.py`** — Synced from 498-line stale copy to full 1225-line version from `~/bin/cc-sessions`: complete `discover` subcommand, incremental cache, Jaccard deduplication, all filtering logic. GitHub source header added.

- **GitHub repo [FlorianBruniaux/cc-sessions](https://github.com/FlorianBruniaux/cc-sessions)** — v1.0.0 published with curl install instructions.

### Updated

- **`guide/ultimate-guide.md`** — Two additions: cross-reference callout to `github-actions.md` in CI/CD section; "Fighting Vibe Code Degradation" subsection covering desloppify ([peteromallet/desloppify](https://github.com/peteromallet/desloppify)) — scan → next → fix → resolve loop as a Claude Code skill, early-stage (Feb 2026, ~2K stars), token cost caveat.

- **`examples/commands/resources/threat-db.yaml`** — v2.7.0 (2026-03-13). +5 threat sources: CVE-2026-26118 Azure MCP Server SSRF (THN/Tenable), OpenClaw agentic AI risk (ReversingLabs), Taskflow Agent scanner (GitHub Security Lab), OpenAI Codex Security research preview, DryRun Security 87% vulnerability rate in AI-built PRs.

- **`CLAUDE.md`** — "Behavioral Rules" section: 5 rules from observed session friction: always update CHANGELOG.md, exhaustive first pass, absolute paths, closing checklist, bias toward action.

- **`examples/scripts/README.md`** — cc-sessions entry updated with `discover` subcommand examples, GitHub repo link, curl install instructions.

- **`machine-readable/reference.yaml`** — Added `cc_sessions_github`, `cc_sessions_discover`, `changelog_fragments_*`, `smart_suggest_hook`, `rpi_*` entries.

## [3.34.11] - 2026-03-13

### Updated

- **`guide/ultimate-guide.md`** (§ Cost Optimization → Strategy 6): Added `#### How Claude Code Handles Caching Automatically` subsection (~75 lines) covering the mechanics that were previously a single undocumented footnote. New content: (1) **Cache prefix hierarchy** — `tools → system → messages` ordering and why the first two layers almost always hit; (2) **20-block lookback** — the long-session cache degradation trap and why `/compact` restores hit rates; (3) **Minimum token thresholds by model** — eligibility table for Opus/Sonnet/Haiku families (1,024–4,096 tokens), correcting the previously circulating false "32,000 token maximum" claim; (4) **Tool result size and cache economics** — why compact tool outputs reduce both cache write and read costs proportionally across the entire session; (5) **Monitoring in custom pipelines** — `cache_creation_input_tokens` / `cache_read_input_tokens` response fields, hit rate calculation formula, and why no dedicated CC cache monitoring tool currently exists; (6) **Practical rules** — CLAUDE.md stability, pre-emptive `/compact` timing, avoiding dynamic content in stable sections.

## [3.34.10] - 2026-03-13

### Added

- **Quiz expanded: 277 → 311 questions (+34)** — 33 new questions covering topics added since the last quiz audit, across 9 categories: `modelOverrides`/`autoMemoryDirectory` settings (v2.1.73-74), tool-qualified deny format `Read(file_path:*.env*)`, CLAUDE.md HTML comment hiding (v2.1.72), `spinnerVerbs`/`spinnerTipsOverride` terminal personalization, team config at scale (N×M×P fragmentation, 59% token reduction), `/loop`/`/simplify`/`/batch`/`/stats`/`/rename` commands (v2.1.63-71), `WorktreeCreate`/`WorktreeRemove`/`TeammateIdle`/`TaskCompleted` hook events (v2.1.50 + v2.1.32+), auto-rename-session hook pattern, Git MCP vs GitHub MCP (12 local tools vs remote Copilot-required), Context Engineering 150% ceiling + ACE pipeline, Plan-Validate-Execute 3-command workflow, dual-instance planning (Jon Williams, $100-200/month), `isolation: "worktree"` in agent frontmatter, simplified effort levels ○◐● (v2.1.72, max removed), Fast mode (2.5x faster/6x price), `model` parameter restored on Agent tool (v2.1.72), `/context` actionable suggestions (v2.1.74), METR RCT 2025 (19% slower on large codebases), Borg "Echoes of AI" RCT 2025 (30.7% faster, no maintainability regression), Contribution Metrics platform feature (+67% PRs/day), enterprise governance 4 guardrail tiers (Starter/Standard/Strict/Regulated), MCP governance workflow + YAML registry, native sandbox OS primitives (macOS Seatbelt vs Linux bubblewrap), `dangerouslyDisableSandbox` escape hatch, RTK (60-92% token reduction, TOML Filter DSL), Google Antigravity (agent-first IDE). 1 question corrected: `12-architecture-internals/002` updated to reflect Tasks API replacing TodoWrite (v2.1.16+).
- **Quiz counters synced**: `machine-readable/reference.yaml` (`quiz_count: 311`), `llms.txt` + `llms-full.txt` + `machine-readable/llms.txt` (`Quiz Questions: 311`).

## [3.34.9] - 2026-03-13

### Added

- **`guide/workflows/gstack-workflow.md`** — New workflow guide (140 lines) documenting the "Cognitive Mode Switching" pattern: switching between specialist roles across the ship cycle (strategic gate → architecture → paranoid review → release → browser QA → retrospective). Reference implementation: [gstack](https://github.com/garrytan/gstack) by Garry Tan (YC CEO). Covers the 6 gears table, the pre-implementation strategic gate concept ("are we building the right thing?"), `/browse` non-MCP native browser architecture (persistent Chromium daemon, ~100ms/cmd vs MCP), full cycle demo, and when to use vs Plan Pipeline.

- **`examples/commands/plan-ceo-review.md`** — New command template for the strategic product gate. Three modes: SCOPE EXPANSION (find the 10-star product), HOLD SCOPE (make the plan bulletproof), SCOPE REDUCTION (strip to MVP). Includes full prompt template, concrete example (photo upload → smart listing creation), and integration notes. Inspired by gstack's `/plan-ceo-review` skill.

- **`examples/commands/plan-eng-review.md`** — New command template for the engineering architecture gate. Forces diagram generation (architecture, sequence, state machine), sync/async boundary decisions, failure mode inventory, trust boundary map, and test matrix before implementation. Includes Mermaid diagram examples and integration notes. Inspired by gstack's `/plan-eng-review` skill.

### Updated

- **`guide/workflows/README.md`**: Added Cognitive Mode Switching entry to Development Workflows section. Added two rows to Quick Selection Guide: "Strategic gate before coding" and "Non-MCP browser automation".

- **`guide/ecosystem/third-party-tools.md`** (Plugin Ecosystem section): Added gstack as the first entry under a new "Notable skill packs" subsection, with cross-reference to the workflow guide.

## [3.34.8] - 2026-03-12

### Added

- **`examples/hooks/bash/smart-suggest.sh`** — Production-ready `UserPromptSubmit` hook implementing a 3-tier behavioral coaching architecture (Tier 0: enforcement, Tier 1: discovery, Tier 2: contextual). Features: max 1 suggestion per prompt, dedup guard (never suggests a command already in the prompt), JSONL ROI logging to `~/.claude/logs/smart-suggest.jsonl`, and silent exit on no match. Includes changelog fragment enforcement as the canonical Tier 0 example (conditional "if PR-intent without fragment-mention" pattern), plus 10 additional patterns across all three tiers. Directly reusable as a starting point for any project-level behavioral enforcement hook.

- **`guide/workflows/changelog-fragments.md`** — New workflow guide documenting the 3-layer changelog fragment enforcement pattern: (1) CLAUDE.md workflow rule for autonomous fragment creation by Claude, (2) `UserPromptSubmit` hook with tier-priority system for pre-prompt interception, (3) CI gate with two independent jobs (fragment validation + migration flag check). Explains why each layer is necessary, how they compose without conflicting, and how to adopt the pattern independent of the TypeScript implementation.

### Updated

- **`guide/ultimate-guide.md`** (§ Release Notes Generation): Added `### Changelog Fragments: Per-PR Enforcement Pattern` subsection covering the 3-layer approach with fragment YAML example, hook snippet, and assembly command. Positioned as an alternative to commit-based release notes generation, with links to the workflow guide and hook example.

- **`guide/workflows/README.md`**: Added Changelog Fragments entry to Development Workflows section with key topics (CLAUDE.md rule, UserPromptSubmit 3-tier hook, conditional suggestion pattern, independent CI migration check). Added to Quick Selection Guide under "Enforce mandatory workflow steps".

## [3.34.7] - 2026-03-12

### Added

- **`guide/diagrams/11-context-engineering.md`** — 4 new Mermaid diagrams covering context engineering: 3-layer context system (global/project/session scopes), context budget and adherence degradation curve (95%→45% zones + path-scoping fix), monolithic vs modular CLAUDE.md architecture (anti-pattern vs path-scoped approach), and rule placement decision tree.

- **`guide/diagrams/12-enterprise-governance.md`** — 3 new Mermaid diagrams covering enterprise governance: 4-tier risk model (Starter/Team/Production/Regulated with controls per tier), MCP governance approval workflow (sequenceDiagram: submit → audit → classify → registry → deploy → monitor), and data classification matrix (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED with access rules).

### Updated

- **`guide/diagrams/01-foundations.md`**: Added Plan Mode and dontAsk as two new permission mode subgraphs (was showing 3/5 modes, now all 5 CLI permission modes are documented).

- **`guide/diagrams/04-architecture-internals.md`**: Added Control Flow Tools as a 6th tool category (EnterPlanMode/ExitPlanMode, EnterWorktree/ExitWorktree, AskUserQuestion). Count updated 5→6.

- **`guide/diagrams/05-mcp-ecosystem.md`**: Added clarifying note that local + user scopes both live in `~/.claude.json` (separate configuration keys), not in separate files. Description updated "4 different locations" → "4 priority levels (3 actual files)".

- **`guide/diagrams/07-multi-agent-patterns.md`**: Fixed disconnected B2 node — now properly connected as a third branch off the pattern-selection flow.

- **`guide/diagrams/09-cost-and-optimization.md`**: Replaced hardcoded USD prices with relative ratios (Haiku ~5x cheaper than Sonnet, Opus ~5x more than Sonnet) and added disclaimer pointing to anthropic.com/pricing.

- **`guide/diagrams/README.md`**: Updated diagram count 41→48, extended navigation table with files 11 and 12, added two new use-case navigation sections ("govern Claude Code across my team", "improve Claude's context adherence").

## [3.34.6] - 2026-03-12

### Added

- **`guide/workflows/rpi.md`** — New RPI (Research → Plan → Implement) workflow guide (560 lines). 3-phase feature development pattern with explicit validation gates: GO/NO-GO gate after Research, plan approval gate before any code is written, and per-step test gates during implementation. Includes full RESEARCH.md and PLAN.md templates, 3 slash command templates (`/rpi:research`, `/rpi:plan`, `/rpi:implement`), worked example (API rate limiting), comparison table vs dual-instance/spec-first/TDD/direct, and troubleshooting section. Inspired by community patterns from claude-code-best-practice.

- **LLM Day-to-Day Performance Variance** (`guide/core/known-issues.md`): New section documenting session-to-session output variance as expected behavior (not a bug). Covers root causes (MoE routing variance, infrastructure variance, probabilistic inference, context sensitivity), observable signals table (response length, refusals, code style, creativity, verbosity), clear distinction from the Aug-Sep 2025 infrastructure bugs, and 5 mitigation strategies (constrain prompts, fresh context, reformulate and retry, compare against known-good prompt, calibrate by task type).

### Updated

- **`guide/ultimate-guide.md`** (§ Quick Decision Tree): Added RPI entry — "Feasibility is unknown → workflows/rpi.md"
- **`machine-readable/reference.yaml`**: Added 8 new entries — `rpi_workflow`, `rpi_when_to_use`, `rpi_phase1_research`, `rpi_phase2_plan`, `rpi_phase3_implement`, `rpi_slash_commands`, `rpi_vs_other_workflows`, `known_issues_llm_variance`

## [3.34.5] - 2026-03-12

### Added

- **Blast-Radius Pattern** (grepai section, §8.2): Named pre-refactoring workflow using `grepai trace callers/callees` to enumerate all affected call sites before touching a widely-used function. Run before the refactor, not after compile errors. Includes 3-step bash example.

- **Pre-structural indexing** (§9.13 Token-Saving Techniques): New technique #6 documenting the concept of building a codebase structural index before starting a session. Replaces 5-10 sequential file reads with 1 graph query (~75% fewer tool calls for discovery tasks). Includes CodeXRay setup example (`npx codexray`, `cxr watch`).

- **Dead code & circular dependency detection** (§9.13): Documents three structural analysis patterns — dead code detection (`grepai trace callers` returning zero results), circular dependency identification, and hotspot analysis — as token optimization strategies. References CodeXRay and Claudette as alpha-stage community implementations with grepai as the stable alternative.

## [3.34.4] - 2026-03-12

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.74 (2026-03-12)
  - v2.1.74: `/context` actionable suggestions, `autoMemoryDirectory` setting, memory leak fix in streaming buffers, managed policy `ask` rules bypass fix, `SessionEnd` hook timeout fix
  - v2.1.73: `modelOverrides` setting, deadlock fix for skill hot-reload, subagent model downgrade fix on Bedrock/Vertex/Foundry, Opus 4.6 as default on 3P providers, `/output-style` deprecated

## [3.34.3] - 2026-03-11

### Added

- **MCP Server v1.1.0**: 4 new tools for tracking official Anthropic Claude Code docs
  - `init_official_docs()` — fetch and store a local baseline snapshot (runs once)
  - `refresh_official_docs()` — update the "current" snapshot without touching the baseline
  - `diff_official_docs()` — compare baseline vs current at section level, zero network calls
  - `search_official_docs(query)` — search official docs, loads only matching sections
- **Local cache architecture**: 4 files in `~/.cache/claude-code-guide/` (index + content, baseline + current). Diff reads only lightweight index files (~50KB), never the full 1.2MB doc. Atomic writes via `.tmp` + rename to prevent corruption.
- **5 new slash commands** (`/ccguide:init-docs`, `/ccguide:refresh-docs`, `/ccguide:diff-docs`, `/ccguide:search-docs`, `/ccguide:daily`) — documented in `ultimate-guide.md` and added to `.claude/commands/ccguide/`
- **`/ccguide:daily`** orchestrates the full daily workflow: refresh → diff official docs → guide/CC digest in one shot

## [3.34.2] - 2026-03-11

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.72 (2026-03-09)
  - Restored `model` parameter on Agent tool for per-invocation model overrides
  - Fixed SDK `query()` prompt cache invalidation — up to 12x input token cost reduction
  - CLAUDE.md HTML comments now hidden from Claude when auto-injected
  - Simplified effort levels: low/medium/high (removed max), new symbols ○ ◐ ●
  - `ExitWorktree` tool added; `CLAUDE_CODE_DISABLE_CRON` env var; `/plan` optional description

## [3.34.1] - 2026-03-11

### Added

- **`guide/workflows/og-image-generation.md`** — New workflow guide for generating dynamic OG images at build time using Satori and resvg in Astro 5. Covers setup, font format requirements (woff1 only), static file shadowing gotcha, dynamic stat counting from content directories, testing with opengraph.xyz / LinkedIn Post Inspector, and three design variants (stats grid, personal branding, terminal badge). Includes CI size check pattern.

- **`examples/scripts/og-image-astro.ts`** — Production-ready template for `src/pages/og-image.png.ts`. Drop into any Astro 5 project. Auto-serves at `/og-image.png`, counts content files dynamically, includes stat card component, author signature, and inline comments on every gotcha.

## [3.34.0] - 2026-03-11

### Added

- **Context Engineering Configurator** (`cc.bruniaux.com/context/`) — Interactive multi-step configurator that generates a personalized CLAUDE.md starter kit. 5-screen flow: profile (team size, AI tools), current state (existing CLAUDE.md, rules files), stack (language, frontend), results (generated artifacts + maturity assessment). Features: generated CLAUDE.md preview with copy-to-clipboard, Profile YAML for team setups, maturity badge (Level 1-5), personalized next-steps roadmap, localStorage persistence. Vanilla JS, no framework. Nav: added "Context" to landing header dropdown.

- **`guide/core/context-engineering.md`** — New consolidated reference (1,188 lines) covering all context engineering concepts. 8 sections: (1) What is Context Engineering (Karpathy's definition, prompt vs. context engineering distinction, three-layer model); (2) The Context Budget (token math, 150-instruction ceiling, HumanLayer 15-25% adherence data, path-scoping efficiency, overload signs); (3) Configuration Hierarchy (global/project/session split, decision tree for rule placement, override semantics); (4) Modular Architecture (path-scoping, skills vs. rules distinction, progressive disclosure, anti-pattern: monolithic CLAUDE.md); (5) Team Assembly (N×M×P problem, profile YAML, assembly workflow, CI drift detection, module library structure); (6) Context Lifecycle (instruction debt, update loop, knowledge feeding, ACE pipeline, session retrospective); (7) Quality Measurement (self-evaluation questions, canary checks, adherence tracking, context debt score formula); (8) Context Reduction Techniques (path-scoping -40-50%, negative constraints +15-25%, rule compression, deduplication, archive pattern).

- **`examples/context-engineering/`** — 10 production-ready templates: `README.md` (overview + quick start), `profile-template.yaml` (developer profile for context assembly), `skeleton-template.md` (CLAUDE.md skeleton with filled placeholders), `assembler.ts` (~240-line TypeScript script for profile-based assembly with @import resolution, dry-run support, token estimation), `eval-questions.yaml` (20 self-evaluation questions across 4 dimensions), `canary-check.sh` (5-check behavioral regression script), `ci-drift-check.yml` (weekly GitHub Actions drift detection with auto-issue creation), `context-budget-calculator.sh` (measures always-on token cost), `rules/knowledge-feeding.md` (proactive context update protocol), `rules/update-loop-retro.md` (session retrospective template).

- **`tools/context-audit-prompt.md`** — Self-contained context audit prompt (543 lines) following `audit-prompt.md` pattern. Scores context engineering setup /100 across 8 dimensions: Size & Budget (15 pts), Structure (15 pts), Path-Scoping (12 pts), Rule Quality (15 pts), Freshness (12 pts), Team Readiness (10 pts), Conflict Detection (11 pts), Knowledge Loop (10 pts). Includes 3 bash scan phases, report format with context budget breakdown, 5-level maturity ladder, and ready-to-use paste improvements.

- **`src/data/context-data.ts`** (landing) — TypeScript data file with all configurator types, option arrays (team size, AI tools, stack, frontend), maturity level definitions (5 levels: Starter/Modular/Team-Ready/Measured/Adaptive), and template generators (`generateClaudeMd`, `generateProfileYaml`, `calculateMaturityLevel`).

### Updated

- **`guide/README.md`** — Added `core/context-engineering.md` row to Core Reference table.
- **`machine-readable/reference.yaml`** — Added 24 context engineering entries with paths to guide, examples, tools, and landing configurator.
- **`src/components/global/Header.astro`** (landing) — Added "Context" to moreLinks dropdown.

## [3.33.1] - 2026-03-10

### Updated

- **RTK documentation updated to v0.28.0** — Synced RTK coverage across `guide/ultimate-guide.md`, `guide/ecosystem/third-party-tools.md`, `machine-readable/reference.yaml`, and global `~/.claude/{CLAUDE.md,RTK.md}`. New content: TOML Filter DSL (declarative filters without Rust, 33+ built-in filters, `.rtk/filters.toml` project-local and `~/.config/rtk/filters.toml` global lookup chain); `rtk rewrite` command (v0.25.0 single source of truth for hook rewrites, migration note: `rtk init --global` required after upgrade); new modules — `rtk docker compose`, `rtk mypy`, `rtk aws`, `rtk psql`, `rtk cargo nextest`, `rtk gt` (Graphite CLI), `rtk wc`; `rtk gain -p` per-project savings; `rtk init --global` with settings.json auto-patch; `exclude_commands` config; SHA-256 hook integrity verification; hook outdated warning.

## [3.33.0] - 2026-03-10

### Fixed

- **`guide/security/enterprise-governance.md` — Accuracy review pass** — 6 correctness issues fixed after adversarial critique: (1) Non-existent hooks removed from all tier `settings.json` configs (`dependency-guard.sh`, `compliance-pre-check.sh`, `pii-detector.sh`, `compliance-session-init.sh` were referenced but never existed in `examples/hooks/bash/`); (2) `compliance-audit-logger.sh` in Regulated tier replaced with real `session-logger.sh`; (3) Fabricated Claude Code API removed — `CLAUDE_SETTINGS` env var and `claude run-headless` subcommand don't exist; replaced with an honest CI pipeline validation pattern; (4) `date -d '30 days ago'` (GNU coreutils only) fixed to cross-platform with macOS/Linux `$OSTYPE` check; (5) Customer PII reclassified from CONFIDENTIAL to RESTRICTED — Enterprise plan (ZDR) alone doesn't satisfy GDPR/CCPA; (6) All `// comment` lines inside JSON code blocks removed (invalid JSON, breaks copy-paste).

### Added

- **Enterprise AI Governance section** (`guide/security/enterprise-governance.md`) — New guide covering org-level governance for teams deploying Claude Code at scale. 6 sections: (1) Local vs Shared governance split (risk matrix, decision framework); (2) AI Usage Charter — lean template covering approved tools, data classification, use case boundaries, approval matrix; (3) MCP Governance Workflow — approval pipeline (request → review → approve → deploy), YAML registry format, enforcement hook; (4) Guardrail Tiers — 4 pre-configured tiers (Starter/Standard/Strict/Regulated) with ready-to-copy `settings.json` and `CLAUDE.md` additions; (5) Policy Enforcement at Scale — config distribution, onboarding checklist, compliance audit script, role-based guardrails, CI/CD gates; (6) Audit & Compliance — what SOC2/ISO27001 auditors actually ask, audit trail setup, AI Governance Committee minimal structure. Audience: tech leads, engineering managers, security officers. Complements security-hardening.md (individual dev security) and production-safety.md (6 prod rules).

- **MCP Registry Template** (`examples/scripts/mcp-registry-template.yaml`) — Ready-to-use YAML format for tracking approved MCP servers at org level. Includes approved/pending/denied sections, version bump policy, risk classification (LOW/MEDIUM/HIGH), data scope classification (PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED), and expiry dates.

- **Governance Enforcement Hook** (`examples/hooks/bash/governance-enforcement-hook.sh`) — SessionStart hook validating active MCP configuration against org's approved registry, checking deny rules for secret files, and detecting dangerous `permissions.allow` overrides. Warns without blocking (governance-first, not friction-first).

- **AI Usage Charter Template** (`examples/scripts/ai-usage-charter-template.md`) — Org-level charter template covering approved tools, data classification (4 levels), approved/prohibited use cases, MCP server governance, code review and attribution requirements, accountability roles, incident response, and compliance mapping (SOC2/ISO27001/HIPAA/PCI DSS/GDPR).

### Documentation

- **`guide/roles/adoption-approaches.md`** — Added "Enterprise Rollout (50+ developers)" section with 3-phase rollout approach (Foundation/Adoption/Optimization), common rollout mistakes at scale, and pointer to enterprise-governance.md for compliance programs.

- **`guide/ops/observability.md`** — Added "Manager Audit Checklist" section with weekly spot-check bash queries (files accessed outside project scope, destructive commands run) and a monthly compliance report script.

- **`guide/ops/ai-traceability.md`** — Added "Evidence Collection for Auditors" subsection under §7.3 Enterprise/Compliance — practical table mapping auditor questions to evidence sources and generation commands.

- **`guide/security/production-safety.md`** — Added cross-reference to enterprise-governance.md in See Also section.

- **`guide/security/security-hardening.md`** — Added cross-reference to enterprise-governance.md with explicit scope boundary ("this guide = individual MCP vetting; that guide = org-level policy"), plus MCP registry template reference.

- **`guide/README.md`** — Added enterprise-governance.md entry in Security section.

- **`machine-readable/reference.yaml`** — Added 22 entries for enterprise governance guide, templates, and hooks.

### Changed

- **GEO/SEO optimization — llms.txt, llms-full.txt, guide meta descriptions** — Phase 1 (repo): `machine-readable/llms.txt` updated (v3.8.0→3.32.2, 87→238 templates, 9.6K→22.7K lines); `llms.txt` created at repo root (convention llmstxt.org — AI crawlers expect root); `llms-full.txt` created (~20KB: full cheatsheet, 238-template catalog, 10 Q&A FAQ); `mcp-server/content/llms.txt` synced. Phase 2 (landing): `public/llms.txt` synced, `public/llms-full.txt` created; stale root `robots.txt` (wrong sitemap URL, missing 6 AI bots) and `sitemap.xml` (6 URLs only) deleted — `public/` versions are canonical. Phase 3 (landing): JSON-LD counts fixed (113→238 in `examples/index.astro`, description sync in `index.astro`); `twitter:site` + `twitter:creator` added to `Layout.astro`; CVE stat 19→24 in security page; `lastmod` added to all sitemap entries in `astro.config.mjs`. Phase 4 (README): invisible HTML keyword comment replaced with visible 5 Q&A mini-FAQ (GEO crawlers + humans). Phase 5 (guide section): 13 `CHAPTERS` descriptions rewritten in `scripts/prepare-guide-content.mjs` (source of truth for Starlight frontmatter) — avg 40→150 chars, now include specific agent names, hook event types, MCP server names, pattern names.

### Documentation

- **README navigation indexes synced with disk** (11 files) — Full audit revealed 40+ missing entries accumulated over time. `examples/README.md`: agents 9→16 (+2 collections), commands 26→31, hooks 31→34, skills 15→17, config 5→8, claude-md 6→7, scripts 13→16, integrations 4→1; 3 new sections: Rules (5), Team Config (3), Templates (1). `guide/README.md`: diagrams 40→41, +5 missing guide files (ai-roles, production-safety, remarkable-ai, sandbox-native, search-tools-cheatsheet), workflows 6→18. `guide/workflows/README.md`: new "Multi-Agent & Advanced" section (agent-teams, agent-teams-quick-start, dual-instance-planning, event-driven-agents, plan-pipeline, task-management), Quick Selection Guide extended, date updated. `examples/hooks/README.md`: +3 hooks (auto-rename-session, security-gate, velocity-governor). `examples/scripts/README.md`: +6 scripts (bridge-plan-schema.json, migrate-arguments-syntax.sh/.ps1, rtk-benchmark, sync-claude-config, sonnetplan). `guide/diagrams/README.md`: frontmatter 40→41. `docs/resource-evaluations/README.md`: 72→115. `README.md` root: resource evals 84→115.

### Changed

- **`tools/onboarding-prompt.md` updated for guide v3.32.2** — 7 changes: (1) "Who This Is For" table enriched (sandbox modes, Plan-Validate-Execute, Skills 2.0 taxonomy, threat DB mentioned by goal); (2) version refs `v3.23.0+` and `v3.21-3.22` updated to `v3.32.2+` / `v3.21-3.32` (6 occurrences); (3) 5 new adaptive triggers documented (`permission|allow|deny → permission_modes`, `memory|persist|session → memory_files`, `template|structure|format → skill_template`, `validation|checklist|deploy → agent_validation_checklist`, `plan|pipeline → plan_pipeline_workflow`); (4) time option "📖 2+ hours" added to the time profile question; (5) fallback roadmap `learn_security` enriched with `permission_modes`; (6) quiz count 274 → 271, per-profile subtotals removed (inconsistent), guide lines 11K+ → 22K+; (7) localization status updated (v3.23.0 → v3.32.2, `plan_pipeline` added in topics, quiz 274 → 271).

- **`tools/audit-prompt.md` updated — Version 3.0** (`tools/audit-prompt.md`) — 6 changes: (1) Opus 4.5 → Opus 4.6 (3 occurrences: intro note, Thinking Mode checklist, glossary); (2) Context Zones corrected: `Green (0-50%) / Yellow (50-70%) / Red (70%+)` → precise thresholds `< 70% optimal, 75% auto-compact, 85% handoff, 95% force handoff`; (3) `sed` line numbers updated with values from `reference.yaml` (deep_dive keys) + maintenance comment; (4) 4 new checklist categories added before "2.2 Calculate Health Score": **Rules Templates** (`.claude/rules/`, auto-loaded), **Sandbox & Permissions** (modes, `permissions.deny`), **Security Commands** (`/security-check`, `/security-audit`, threat-db), **Plan-Validate-Execute Pipeline** (`/plan-start`, `/plan-validate`, `/plan-execute`, ADR loop); (5) 4 new glossary entries: **Rules**, **Permission Modes**, **Sandbox**, **Plugins**; (6) footer `January 2026 | Version 2.9` → `March 2026 | Version 3.0`.

- **`machine-readable/reference.yaml` — Onboarding Matrix v2.1.0** (`machine-readable/reference.yaml`) — 5 changes: (1) metadata `version 2.0.0 → 2.1.0`, `last_updated → 2026-03-09`, new changelog entry v2.1.0; (2) 3 new deep_dive keys: `skills_taxonomy: 6718` (§5.0 Two Kinds of Skills), `skills_evals: 6954` (§5.Y Skill Evals), `session_auto_rename: 859` (distinct from `session_naming_guide: 815`); (3) quiz count `264 → 271` (4 occurrences: `quiz_count`, `unique` array, `code_landing.features`, comment); (4) adaptive triggers `plan|pipeline[|validate|execute]` added in 3 profiles: `optimize.power_60min`, `build_agents.power_60min`, `learn_everything.power_120min` → topic `plan_pipeline_workflow`; (5) version refs `v3.21-3.22 → v3.21-3.32` in profile notes (4 occurrences).

### Documentation

- **`/loop` command added to Commands Table §10.1** (`guide/ultimate-guide.md`) — `/loop [interval] [prompt]` runs a prompt or slash command on a recurring interval (e.g. `/loop 5m check the deploy`). v2.1.71+. Was already in cheatsheet (v3.32.2), now present in the reference table.

- **Voice keybindings documented §10.2** (`guide/ultimate-guide.md`) — new "Voice Input" subsection in Keyboard Shortcuts: push-to-talk default binding (`Space`), `voice:pushToTalk` rebindable in `~/.claude/keybindings.json` (v2.1.71+), example config included.

- **Claude Code Security note enriched §7.4** (`guide/ultimate-guide.md`) — added Mozilla Firefox validation context (March 2026): Opus 4.6 scanned ~6,000 C++ files in Firefox's JS engine, surfaced 22 confirmed vulnerabilities (14 high severity) in two weeks. Reinforces the "limited research preview" note with production evidence.

- **Pipelex + MTHDS added** (`guide/ecosystem/third-party-tools.md`) — new entry in "External Orchestration Frameworks" for Pipelex, Python runtime of the open MTHDS standard. Declarative DSL (`.mthds` files) for creating typed, git-versionable, multi-LLM AI methods. Integrates natively with Claude Code via `/plugin marketplace add mthds-ai/skills`. 623 stars (MIT, created May 2025). Status "Watch" — MTHDS standard not yet validated at scale. Architectural note distinguishing Pipelex (DSL for pipelines) from Ruflo/AthenaFlow (agent orchestration).

- **Diagrams updated — 3 files** (`guide/diagrams/`) — Mermaid diagrams updated following releases v2.1.59–v2.1.69 and documentation corrections v3.29–v3.31. (1) `02-context-and-sessions.md`: Memory Hierarchy goes from 5 to 6 types — addition of **Native Auto-Memory** (`~/.claude/projects/*/memory/MEMORY.md`, v2.1.59+) between Subdirectory CLAUDE.md and In-Conversation Context, cross-session scope, distinct green style from ephemeral types. (2) `03-configuration-system.md`: Hooks Event Pipeline enriched with 3 new events — `InstructionsLoaded` (v2.1.69+, session start), `UserPromptSubmit` (before PreToolUse, exit 2 = feedback), `Stop / SessionEnd` (renamed) — and a note on the HTTP type (POST JSON, v2.1.63+). (3) `05-mcp-ecosystem.md`: Official Servers goes from 3 to 5 entries — added `git-mcp` (official Anthropic, 12 git tools) and `github-mcp` (official GitHub, full platform).

### Changed

- **`/pr-triage` skill — Phase 4 Worktree Setup** (`examples/skills/pr-triage/SKILL.md`) — porting the worktree pattern developed on Méthode Aristote to the guide's generic template. The skill goes from 3 to 4 phases: Phase 4 is opt-in, accessible from a navigation menu after Phase 1 (without going through Phase 2/3). Integrated content: 30min cache-check on Phase 1 data, automatic filtering of draft PRs and bots (Dependabot, renovate, snyk), grouped display by author, multiSelect selection via AskUserQuestion, sequential execution per PR with structured status codes (CREATED / EXISTING / FETCH_FAILED / GITIGNORE_MISSING / ALREADY_CHECKED_OUT / CREATE_FAILED), automatic `node_modules` symlink if present (Node.js), `.worktreeinclude` convention to copy local config files into each worktree, git pull `--ff-only` for existing worktrees with guided rebase fallback, final summary with next steps `cd .worktrees/<branch> && claude`. Phase 4 edge cases added (5 cases). Related table and frontmatter description updated (3-phase → 4-phase, `worktree` tag).

## [3.32.2] - 2026-03-09

### Documentation

- **Cheatsheet updated** (`guide/cheatsheet.md` + landing `cheatsheet/index.astro`) — 4 new commands from releases v2.1.59–v2.1.71: `/loop [interval] [prompt]` (recurring scheduler, e.g. `/loop 5m check the deploy`), `/stats` (usage chart + streak), `/rename [name]` (name a session), `/copy` (interactive picker to copy a code block). New shortcut `Ctrl+F` (kills all background agents, double press). `/loop` added to "Hidden Features" with version v2.1.71. Landing version synced 3.29.2 → 3.32.0.

## [3.32.1] - 2026-03-08

### Added

- **`auto-rename-session.sh` hook template** (`examples/hooks/bash/auto-rename-session.sh`) — SessionEnd hook that automatically generates a descriptive title for each session. Reads the session JSONL directly, extracts the first 3 user messages, calls `claude -p --model claude-haiku-4-5-20251001` to generate a 4-6 word title (`verb + subject` format), falls back to the cleaned first message if Haiku is unavailable. Updates the slug in the native JSONL (for `/resume`) and in `sessions-index.jsonl`. Output via `/dev/tty` to bypass Claude Code's JSON parsing.

### Documentation

- **"Session Auto-Rename" section updated** (`guide/ultimate-guide.md`) — now presents two complementary approaches: Approach A (CLAUDE.md instruction, mid-session renaming via `/rename`, zero tooling) and Approach B (SessionEnd hook, title generated by Haiku post-session, direct JSONL reading). Removed the "Why not a hook?" paragraph which was incorrect since the introduction of session data access via JSONL.

## [3.32.0] - 2026-03-06

### Added

- **Plan-Validate-Execute Pipeline** (`guide/workflows/plan-pipeline.md`) — new complete 3-command workflow for AI-first teams: `/plan-start` (5 phases: PRD analysis, design, technical decisions, dynamic research team, metrics), `/plan-validate` (2 layers: inline structural checks + specialist agents triggered by triggers), `/plan-execute` (isolated worktree, TDD scaffolding, parallel execution by levels, quality gate with smoke test, PR creation and merge, cleanup). Includes: "non-prescriptive" philosophy (say what, never how), first principles "No Bandaids, No Workarounds" (state-of-the-art always, build time irrelevant, zero workaround), ADR learning loop (Watching → Emerging → Confirmed → CLAUDE.md promotion), CLAUDE.md discipline (120-line limit, pointer strategy to sub-files, dynamic loading), context management (`/clear` between each command). Cost profile: $2-10 for a typical Tier 2 feature with compounding over time.

- **`/plan-start` command** (`examples/commands/plan-start.md`) — 5-phase slash command with dynamic agent pool (12 roles, trigger-based selection). Includes: interactive PRD analysis with 3 buckets (missing/ambiguous/compliance), design analysis (screen inventory, states catalog, animation specs, ARIA accessibility), technical analysis with automatic resolution of ADR-confirmed decisions, scope assessment (Tier 0 Solo → Tier 4 Full Spectrum), parallel multi-agent research monitored via TaskOutput, synthesis by `planning-coordinator`, commit plan + ADRs + metrics. Auto-transition to `/plan-validate` if no ambiguities.

- **`/plan-validate` command** (`examples/commands/plan-validate.md`) — independent validation in 2 layers. Layer 1 inline structural (format, dependencies, file existence, ADR consistency, CLAUDE.md compliance). Layer 2 specialists triggered by triggers (security-reviewer Opus, db-migration-reviewer Opus, performance-reviewer, design-system-reviewer, ux-reviewer, cross-platform-reviewer, integration-reviewer Opus — 0 to 8 agents depending on the plan). ADR-aware auto-fix phase: Bucket A (auto-resolution via ADR/PATTERNS/first principles, ~95%), Bucket B (human input → new rule → future auto-resolution). Structured persistence of issues in metrics JSON. Auto-transition to `/plan-execute` if everything auto-resolved.

- **`/plan-execute` command** (`examples/commands/plan-execute.md`) — complete execution through to merged PR. Isolated worktree → TDD scaffolding (failing tests first) → parallel execution by levels (one agent per task, commit per task) → drift detection → quality gate (lint + types + tests) → integration smoke test (probe GraphQL, scan container logs, plan-defined commands) → PRD reconciliation + plan archival → PR squash merge → post-merge metrics → worktree cleanup. Up to 3 auto-fix attempts by debug agent before human escalation.

- **`planning-coordinator` agent** (`examples/agents/planning-coordinator.md`) — Opus synthesis agent, read-only. Receives reports from all research agents, reads existing ADRs, resolves conflicts between agents (ADR precedence → agent stake → human escalation), builds the task graph (layers, TDD markers, atomic granularity), verifies plan completeness (PRD coverage, security findings addressed, acyclicity). Spawned automatically when 2+ research agents are selected. Does not research — synthesizes.

- **`integration-reviewer` agent** (`examples/agents/integration-reviewer.md`) — Opus runtime validation agent, read-only + WebFetch. Validates what compiles but fails at runtime: connection parameters (ports, protocols, hostnames across environments), async/sync consistency (missing awaits, sync call in async context), env var completeness (`.env.example`, CI/CD, k8s manifests, startup validation), API library correctness (installed version vs API used via WebFetch), OTEL pipeline (configured exporter, cross-service context propagation, sampling). Triggered in `/plan-validate` when new services, libraries, or OTEL config are in scope.

## [3.31.0] - 2026-03-06

### Added

- **Skills 2.0 — Taxonomy, Evals and Lifecycle** (`guide/ultimate-guide.md` §5.0, §5.X, §5.Y) — 3 new blocks: Capability Uplift vs Encoded Preference taxonomy, Skill Lifecycle (Catch Regressions + Spot Outgrowth + retirement checklist), Skill Evals (Benchmark Mode / A/B Testing / Trigger Tuning). "What Makes a Good Skill?" table enriched (Expected Lifespan column). `guide/cheatsheet.md` + `machine-readable/llms.txt` updated. 3 new landing quiz questions (019-021). Sources: ainews.com, mexc.co, claudecode.jp — March 2026.

- **Featured Community Plugins — Vitals + SE-CoVe** (`guide/ultimate-guide.md` §8.5) — Vitals (chopratejas/vitals, v0.1 alpha): hotspot detection using `git churn × structural complexity × coupling centrality` formula, Claude semantic diagnostics, zero dependencies. SE-CoVe (vertti/se-cove-claude-plugin, v1.1.1): 5-step Chain-of-Verification pipeline (Baseline → Planner → Executor → Synthesizer → Output), verifier without access to the initial solution. Evaluation: `docs/resource-evaluations/vitals-codebase-health-plugin.md` (3/5). `machine-readable/reference.yaml` entries updated.

### Documentation

- **Memory system — 3 corrections** (`guide/ultimate-guide.md`): Auto-Memories version corrected (v2.1.32+ → v2.1.59+, confirmed 2026-02-26), context thresholds unified (<70% optimal / 75% auto-compact / 85% handoff / 95% force), WHAT/WHY/HOW framework added (§3.1 Minimum Viable CLAUDE.md) with Next.js example and anti-pattern "do not auto-generate your CLAUDE.md".

## [3.30.2] - 2026-03-05

### Documentation

- **Conductor section enriched** (`guide/ecosystem/third-party-tools.md:376`) — section rewritten from 5 generic bullets to 6 structured subsections, verified against official changelog (conductor.build). Added: workspace status system (backlog → done, v0.35.0), Next Workspace button for agent queue navigation (v0.36.4), turn-by-turn diff viewer (v0.22.0), Manual Mode built-in editor replacing VSCode for quick edits (v0.37.0), full GitHub/CI integration details (Actions tab v0.33.2, failing CI → Claude auto-fix v0.12.0, PR workflow with `⌘⇧P`), Linear deeplinks, Codex support alongside Claude, Melty Labs attribution. Community workflow pattern added: 5+ parallel features across multiple repos, BMAD + Conductor combo for spec-driven development (user-reported, unverified claim clearly marked).

- **Claude Code Releases tracking**: Updated to v2.1.69 (from v2.1.66)
  - v2.1.69: InstructionsLoaded hook, 4 security fixes (nested skills/symlink bypass/trust dialog/sandbox), 15+ memory leak fixes, Voice STT 20 languages, ${CLAUDE_SKILL_DIR}, /reload-plugins
  - v2.1.68: ultrathink keyword re-introduced, Opus 4.6 medium effort default, Opus 4/4.1 removed from first-party API


### Added

- **OpenClaw security hardening — personal documentation (boldguy/obsidian)** — 4 files created after security audit (score 5/10 → target 8+/10). (1) `securisation-openclaw.md`: complete 5-level guide — gateway bind loopback + 32-char token, exec allowlist + filesystem denied paths, memory-lancedb reconfigured with local Ollama (nomic-embed-text, `dimensions: 768` required because `config.ts:66-72` throws for non-OpenAI model without this field), Cloudflare Access Zero Trust on `webhook.bruniaux.com`, iMessage DM Policy (pairing or allowlist), hardened docker-compose. (2) `checklist-openclaw.md`: 5 checkable sections (pre-install, network, sandbox, memory/data, channels) + monthly monitoring. (3) `scripts/verify-openclaw-security.sh`: bash script with 8 automated checks (port binding, JSON config, Ollama, active OpenAI connections, injection session scan, built-in audit, FileVault). (4) `rapport-audit-openclaw.md`: Addendum section with additional findings (Ollama local support verified in `config.ts:10,147`, community 3-tier guide, DM Policy modes). Key audit finding: `memory-lancedb` sends embeddings to OpenAI by default — reconfigure with `baseUrl: "http://localhost:11434/v1"` + `dimensions: 768` to stay 100% local.

### Fixed

- **Remote Control §9.22 — iOS bugs documented and workarounds** (`guide/ultimate-guide.md:20075`) — troubleshooting enriched following field testing (iPhone, March 2026). Confirmed bug: QR code scan opens the Claude app but the session does not appear in the list (Research Preview, reproducible on iOS, documented by MacStories). Two reliable workarounds added: (1) `claude.ai/code` in Safari — session visible directly, (2) URL copied from terminal and pasted in Safari. Explanatory note added in troubleshooting table with MacStories reference.

### Added

- **Entire CLI enrichment (6 sections, 4 files)** — integration of production analysis issue #802 (Méthode Aristote) into the guide. Content added: (1) `guide/ops/ai-traceability.md` — complete "workflow without vs with Entire" diagram showing the 7 hooks and what they capture (UserPromptSubmit, PreToolUse, PostToolUse, Stop...), actual checkpoint structure (`entire/checkpoints/v1/` with metadata.json + full.jsonl + prompt.txt + context.md), orphan branch diagram (no common ancestor = zero merge conflict), Go/No-Go table with measurable thresholds (< 10 MB/session, push < 5s, < 100 MB/week) and 2h spike commands. (2) `guide/ecosystem/ai-ecosystem.md` — Claude → Gemini agent handoffs diagram with context preservation (reasoning trace, touched files, decisions, rejected approaches), "no cold start" explanation. (3) `guide/ecosystem/third-party-tools.md` — delta table vs existing setups (7-day JSONL vs permanent checkpoints, absent human/AI attribution vs % per line, silent handoffs vs auto-passed context). (4) `guide/security/security-hardening.md` — approval gate flow diagram (policy check → low risk auto-OK / high risk → reviewer transcript + diffs → approve/reject → immutable audit trail). Source: [github.com/methode-aristote/app/issues/802](https://github.com/methode-aristote/app/issues/802).

- **`issue-triage` skill** (`examples/skills/issue-triage/`) — 3-phase issue backlog management for maintainers: automated audit of all open issues (categorization, Jaccard duplicate detection against open + 20 recent closed, risk classification Red/Yellow/Green, staleness 30/90-day thresholds, cross-reference to open PRs), opt-in deep analysis via parallel agents (full body + comments, duplicate verification, missing-info detection, effort estimate), and validated triage actions with mandatory `AskUserQuestion` gate (comment / label / close with close-reason). Jaccard algorithm is self-contained at runtime (no external library: normalize → tokenize → set intersection/union → threshold 0.60). Cross-referenced with `/pr-triage` for PR-side backlog management.

- **`pr-triage` skill** (`examples/skills/pr-triage/`) — 3-phase PR backlog management for maintainers: automated audit of all open PRs (size classification, overlap detection, cluster analysis, staleness, CI status, PR-issue linking), opt-in deep review via parallel `code-reviewer` agents, and validated comment posting with mandatory `AskUserQuestion` gate. Stack-agnostic (Node/TS, Python, Rust, Go checklists included), cross-platform clipboard (pbcopy/xclip/wl-copy/clip.exe), and cross-referenced with `/review-pr` for single-PR use cases.

- **External Orchestration Frameworks** (`guide/ecosystem/third-party-tools.md`, new section) — new category architecturally distinct from existing multi-instance tools (Gas Town, multiclaude). Documented distinction: launching multiple Claude Code instances in parallel vs. replacing/augmenting the internal orchestration layer with a full runtime. Two tools covered: (1) **Ruflo** (formerly claude-flow, 18.9k stars) — most adopted framework, hierarchical queen + workers swarms, 60+ specialized agents, Q-Learning router, 42+ skills, 17 hooks, SQLite persistence. Install recommendation via `npx ruflo@latest` (not curl|bash). Performance claims (84.8% SWE-Bench, 352x WASM) marked unverified, ongoing rebrand documented. (2) **Athena Flow** — different architecture (hooks → UDS → NDJSON → Node.js runtime → TUI), intercepts hook events rather than augmenting the agent layer. First workflow: autonomous Playwright E2E test builder. Status "Watch — not recommended yet" (project too recent, source audit missing). Complete evaluations: `docs/resource-evaluations/073-athena-flow-workflow-runtime.md` (2/5 Watch) and `074-ruflo-multi-agent-orchestration.md` (3/5 Pertinent).

- **For Tech Leads & Engineering Managers** (`guide/roles/learning-with-ai.md`, new §12) — dedicated section for tech leads and engineering managers, a blind spot identified through resource evaluation (Mathieu Eveillard, "Génération LLM"). The guide only covered the individual perspective; this section addresses organizational responsibility. Content: 4-week onboarding model (week 1 without AI for calibration before the tool masks gaps, validated by Create Future 2025: structured training → 14-42% → 35-65% time savings), 5 real growth metrics vs. velocity, 3 scalable mentoring models (pair rotations, 15min/week architecture hot seat, collective CLAUDE.md), AI team policy template for shared `CLAUDE.md`, 6 team-level warning signs with specific responses, quick checklist. New "Team & Organizational Research" section in sources (Create Future 2025, Stanford Digital Economy 2025, LeadDev, Stack Overflow Gen Z). Evaluation file created: `docs/resource-evaluations/2026-03-04-eveillard-generation-llm.md`.

- **Compound Engineering patterns** (`guide/ultimate-guide.md`, 4 insertions) — portable patterns from Every.to's compound-engineering plugin (Kieran Klaassen, prod-tested on Cora), previously absent from the guide. (1) **Named Perspective Agents**: distinction between persona roleplay (anti-pattern, prohibited §3.x) and named perspective (DHH = fat models + thin controllers + pragmatic REST condensed into one token), with caveat on drift between Claude versions. (2) **Swarm vs Sequential**: comparison table of the two multi-agent coordination modes, decision rule (Swarm = independent + thoroughness, Teams = sequential dependencies). (3) **Skill Quality Gates**: 9-criteria checklist going beyond frontmatter validation (`/audit-agents-skills`). (4) **Brainstorm-before-planning + documentary hierarchy**: `docs/brainstorms/ → docs/plans/` workflow before coding, table of 5 directories with their distinct roles (CLAUDE.md = rules, solutions/ = solved problems, brainstorms/ = thinking, plans/ = active plans, todos/ = ephemeral tasks). Formal evaluation: `docs/resource-evaluations/2026-03-04-compound-engineering-every-to.md` (4/5 HIGH VALUE).

- **Session Auto-Rename pattern** — behavioral instruction in `~/.claude/CLAUDE.md` that makes Claude automatically rename sessions after 2-3 exchanges, without any hook or script. Format `[action] [subject]` (e.g. "fix auth middleware", "refactor hook system"), max 50 chars, action verb first. Useful for finding sessions via `/resume` when multiple are running in parallel. Documented limitation: the WebStorm terminal tab cannot be renamed (ANSI sequences filtered by JetBrains). Template: `examples/claude-md/session-naming.md`. Guide: new "Session Auto-Rename" subsection in §1.3 Session Continuation. Template counter 175→176.

- **Design Reference File pattern** (`examples/claude-md/design-reference-file.md`) — field pattern from Boris Paillard / mixt.care evaluation (March 2026). Principle: keep `brand-book.html` and `ui-kit.html` at the project root as permanent context files — Claude Code reads them before any UI generation, ensuring design system consistency across sessions without re-prompting. Content: CLAUDE.md activation snippet, 4 complete prompts (brand-book with integrated WCAG, Tailwind ui-kit, WCAG 2.1 color audit + color blindness simulation, vanilla JS Intersection Observer scroll animations), palette example with CSS semantic roles (mixt.care), WCAG correction notes (e.g. copper #B87333 fails for normal text → fix to #9B5F20). Evaluation: `docs/resource-evaluations/075-paillard-design-system-first-website.md` (3/5).

- **Straude** (`guide/ecosystem/third-party-tools.md`, Token & Cost Tracking section) — complete entry for straude.com, a social dashboard for tracking Claude Code usage with leaderboard and streaks. Includes: functional description, table of data transmitted to the server (costs, tokens, models, hostname), security analysis based on direct source code inspection (`npm pack straude@0.1.9`), verdict (no malware, reservations about maturity and lack of privacy policy), `--dry-run` recommendation on first use. Complete evaluation: `docs/resource-evaluations/straude-evaluation.md`. Entries added in `machine-readable/reference.yaml`.

## [3.30.1] - 2026-03-04

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.66
  - v2.1.66: Reduced spurious error logging
  - v2.1.63: HTTP hooks (POST JSON to URL), project configs shared across git worktrees, `/simplify` & `/batch` bundled commands, major memory leak wave fixed
  - v2.1.62: Prompt suggestion cache fix
  - v2.1.61: Windows config file corruption fix

### Added

- **Native LSP documented** (`guide/ultimate-guide.md`, `guide/cheatsheet.md`, landing cheatsheet) — complete section on Claude Code's native LSP support (v2.0.74+, December 2025). Content: performance gain explanation (50ms vs 45s for codebase navigation, 900x), activation via `ENABLE_LSP_TOOL=1` or `~/.claude/settings.json`, table of 11 supported languages with install commands (`tsserver`, `pylsp`, `gopls`, `rust-analyzer`, `kotlin-language-server`, `sourcekit-lsp`...), `.lsp.json` configuration for timeouts. Enriched cheatsheet: LSP line with perf stat + activation note. Sources: [aifreeapi.com/en/posts/claude-code-lsp](https://aifreeapi.com/en/posts/claude-code-lsp), Perplexity fact-check March 2026.

- **`docs/solutions/` pattern documented** (`guide/ultimate-guide.md` §CLAUDE.md as Compounding Memory) — complementary pattern to CLAUDE.md for capturing solved problems between PRs, inspired by the [Compound Engineering (Every.to)](https://every.to/guides/compound-engineering) framework. Clear distinction: CLAUDE.md = behavioral rules, `docs/solutions/` = solved problems with full context. Includes example structure with 3 illustrative files (auth, iOS StoreKit, Kotlin coroutines).

- **Voice Mode documented** (`guide/ultimate-guide.md`, `guide/cheatsheet.md`) — native feature rolling out (~5% of Pro/Max/Team/Enterprise users). `/voice` to activate, hold `Space` to speak, release to send. Can be mixed with text input in the same prompt. Free transcription, does not count toward rate limits. 4 places updated: quick commands table §1.3, built-in commands table §6.1, voice workarounds section §11 (switching from superwhisper/MacWhisper workaround to native feature), cheatsheet (commands + shortcuts + hidden features). Source: [Charly Wargnier / LinkedIn](https://www.linkedin.com/posts/charlywargnier_voice-mode-is-officially-coming-to-claude-ugcPost-7434514836211863552-JvKw).

- **Smart Concierge + Retex system** — porting the system developed on Méthode Aristote to this project. `UserPromptSubmit` hook (`smart-suggest.sh`) that analyzes each prompt in natural language and suggests 0 or 1 relevant tool (max 1 per prompt, silent on slash commands, dedup if the tool is already in the prompt, ROI log in `~/.claude/logs/smart-suggest.jsonl`). 22 patterns in 2 tiers adapted to this project's tools: Tier 1 discovery (retex, whitepaper-density/journalist/coherence, pdf-generator, sync, security-audit, audit-repo-docs, boldguy-linkedin-answer, guide-recap, park, update-whitepapers), Tier 2 contextual (release, changelog, version, code-reviewer, debugger, audit-agents-skills, update-threat-db, audit-prose, release-notes-generator, security-check).
- **`/retex` command** — captures lessons learned (dead ends, bugs, rollbacks) in `.claude/memories/retex-*.md` with global index `retex-index.md`. Structure: what happened, root cause, prevention rule, tags, severity, scope. Direct mode (`/retex "description"`) and interactive mode.
- **`retex-review.md` rule** — auto-loaded at each session, displays the 3 most recent retex at startup, inline contextual surfacing if a pattern matches an existing prevention rule (max 1 warning per type per session).

## [3.30.0] - 2026-03-03

### Added

- **10 advanced patterns documented** — systematic audit of 10 patterns identified from expert practitioners, fact-checked via 9 Perplexity searches (March 2026). 5 new files created, 4 existing files enriched, 3 sections added to the main guide.

  **New files**:
  - `examples/agents/plan-challenger.md` — adversarial agent for challenging plans before implementation (+52.8% security, +80% bug detection, sources: DrillAgent/nsfocusglobal.com, milvus.io)
  - `examples/agents/adr-writer.md` — automatic ADR generation agent with C1/C2/C3 criticality matrix, `mcp-adr-analysis-server` MCP reference (tosin2013/GitHub)
  - `examples/commands/audit-codebase.md` — codebase scoring command in 7 categories (Secrets, Security, Dependencies, Structure, Tests, Imports, AI Patterns), 3 severity levels, progression plan by tiers 5→8→10 (inspired by Variant Systems open-source plugin)
  - `examples/rules/first-principles.md` — session invariants template: Contract/Working Set/Noise model, measurable thresholds ("80% minimum" > "good coverage"), context decay mitigation
  - `guide/workflows/event-driven-agents.md` — complete "event → agent" workflow: Linear-Driven Agent Loop (Galarza, Feb 2026), generic webhook pattern, events×agents table, guardrails (idempotency, rate limiting, circuit breaker)

  **Main guide modifications** (`guide/ultimate-guide.md`):
  - §3.1 — new "Modular Context Architecture" subsection: CLAUDE.md-as-index (<100 lines), `paths:` frontmatter for conditional loading, 3-tier architecture root→rules/→skills/ (undocumented official feature)
  - §9.3 — new "Deployment Automation" subsection: Vercel building blocks (3 required variables), Infisical as open-source Vault alternative, deploy skill, non-negotiable guardrails (staging-first, confirmation hook, rollback)
  - §9.12 (worktrees) — new "Coordinating Parallel Worktrees: Task Dependencies" subsection: manual analysis of touched files, explicit `blockedBy`, decision matrix, `coderabbitai/git-worktree-runner` reference, clarification: auto-detection does not exist

  **Workflow modifications**:
  - `guide/workflows/iterative-refinement.md` — "Community Patterns & Known Limitations" section: Ralph Loop (nathanonn.com), Auto-Continue Skill (mcpmarket.com), Stop Hooks integration, post-3-iterations escalation strategy, caveats GitHub issues #28489 and #28843
  - `guide/workflows/agent-teams.md` — nuance of >5 agents anti-pattern: context window table 10K/50K/100K+, model-per-role (desired feature, not supported by API March 2026), Gartner 40% enterprise prediction 2026

- **SonnetPlan hack documented** (`guide/ultimate-guide.md` §OpusPlan Mode) — budget Sonnet→Haiku variant via `ANTHROPIC_DEFAULT_OPUS_MODEL` + `ANTHROPIC_DEFAULT_SONNET_MODEL` remap: `sonnetplan()` shell function, Plan/Act routing, unreliable self-report caveat, GitHub issue link [#9749](https://github.com/anthropics/claude-code/issues/9749). New template `examples/scripts/sonnetplan.sh` with installation instructions and verification note (status bar vs self-report).

- **Auto-memory documented as 3rd native memory system** (`guide/ultimate-guide.md` §Session vs Persistent Memory) — transition from 2 to 3 systems (session / native auto-memory / Serena MCP), new 5×4 table, dedicated "Auto-Memory (native, v2.1.59+)" section with MEMORY.md path and `/memory` management. Correction: the old description linked `/memory` to CLAUDE.md (inaccurate) and ignored the native system. "When to use which" guidance updated.
- **`/memory` and `/copy` — command descriptions updated** (`guide/ultimate-guide.md` §Command Reference) — `/memory`: corrected to auto-memory + MEMORY.md (v2.1.59+). `/copy`: enriched with interactive code block picker and "Always copy full response" option (v2.1.59+).

- **`/batch` highlighted** (`guide/cheatsheet.md`, `whitepapers/fr/07`, `whitepapers/fr/08`, `whitepapers/en/07`, `whitepapers/en/08`) — `/batch` = 5-30 parallel agents in isolated Git worktrees, each opens a PR. Dedicated sections in whitepapers 07 (table /batch vs manual agent teams) and 08 (native alternative). Cheatsheet updated with `/simplify` + `/batch`.

- **skills.sh security audits** (`guide/ultimate-guide.md` §Skills Marketplace) — new "Security Audits (February 2026)" subsection: 3 independent partners (Socket static analysis 97% F1, Snyk mcp-scan 0% false positives, Gen Agent Trust Hub continuous monitoring), 4 risk levels (Safe/Low/High/Critical), post-install monitoring, mental model "skill = executable dependency". Trade-offs updated: removed "Early stage" warning, added ✅ automated audits + continuous monitoring. 3 source references added (Vercel changelog, Snyk blog, Gen/PRNewswire). Source: [Vercel, Feb 17 2026](https://vercel.com/changelog/automated-security-audits-now-available-for-skills-sh).

## [3.29.2] - 2026-03-02

### Added
- **`/simplify` command documentation** (`guide/ultimate-guide.md` §6.1) — dedicated section for the v2.1.63 bundled command: official description (over-engineering, redundant abstractions), 3 analyzed dimensions (reuse/quality/efficiency), targeted usage examples (`/simplify focus on error handling`), positioning table vs linters/formatters.
- **`/batch` command documentation** (`guide/ultimate-guide.md` §6.1) — dedicated section for the v2.1.63 bundled command: processing multiple items in a single invocation.
- **Built-in Commands table updated** — `/simplify` and `/batch` added §6.1 and §1.3. Sources: official GitHub release notes + Perplexity.

## [3.29.1] - 2026-03-02

### Added

- **Git MCP Server + GitHub MCP Server** (`guide/ultimate-guide.md` §8.2 MCP Server Catalog) — Git MCP Server (official Anthropic): 12 tools for local Git operations (git_status, git_diff, git_commit, git_log, git_create_branch…), `uvx` setup, multi-repo config, comparison vs Bash, typical workflows. GitHub MCP Server (official GitHub): Issues, PRs, Projects, Code search, Enterprise — remote mode via `api.githubcopilot.com/mcp/` (Copilot required) + self-hosted PAT-only. Fix documented for the `Incompatible auth server: does not support dynamic client registration` error: `gh auth token` + `Authorization: Bearer` header in `~/.claude.json`, expired token maintenance note.
- **Resource evaluation: MCP servers watch** (`docs/resource-evaluations/2026-03-02-mcp-servers-veille.md`) — 3 servers evaluated post-challenge + fact-check: GitHub MCP 4/5 (integrated), Exa 2/5 (rejected, unverifiable stars), Graphiti 2/5 (rejected, Kairn already covers the need).
- **Tool comparison table extended to 5 tools** (`guide/ultimate-guide.md` §Migration from Other Tools) — added Windsurf and Zed, fixed Cursor pricing.
- **Subscription quotas: "Claude Code prompts / 5h" column** (`guide/ultimate-guide.md` §Subscription Plans & Limits) — Pro ~10-40, Max 5x ~50-200, Max 20x ~200-800.
- **Resource evaluation: benchmark AI coding tools Feb 2026** (`docs/resource-evaluations/benchmark-ai-coding-tools-feb2026.md`) — score 3/5, 2 items integrated.
- **Claude Code v2.1.63 release tracking** — `machine-readable/claude-code-releases.yaml` + `guide/core/claude-code-releases.md`: v2.1.61–v2.1.63 (HTTP hooks, worktree config sharing, `/simplify` + `/batch`, `ENABLE_CLAUDEAI_MCP_SERVERS`).
- **HTTP hooks documentation** (`guide/ultimate-guide.md` §7.2) — `"http"` type (v2.1.63+): POST JSON → JSON response, config example with `allowedEnvVars`.
- **Resource evaluation W09-2026** (`docs/resource-evaluations/weekly-intel-2026-W09.md`) — score 4/5, 3 items integrated.
- **Section 9.23 — Configuration Lifecycle & The Update Loop** (`guide/ultimate-guide.md`) — continuous improvement loop, `detect-friction.sh` script, skills lifecycle, "The Update Loop" pattern.
- **Observability: Reading for Quality, Not Just Quantity** (`guide/ops/observability.md`) — 3 qualitative patterns with `jq` commands.
- **MCP Server: 3 new tools** — `compare_versions`, `get_threat`/`list_threats`, `search_examples` (8 → 12 tools total).
- **Terminal Personalization Settings** (`guide/ultimate-guide.md` §3.3) — `spinnerVerbs`, `spinnerTipsOverride`, complete example `examples/config/settings-personalization.json`.

### Added

- **Tool comparison table extended to 5 tools** (`guide/ultimate-guide.md` §Migration from Other Tools) — comparison table extended from 3 to 5 tools: added Windsurf (Cascade multi-agents, Wave 13, credit-based $15/mo) and Zed (native Rust, Ollama offline, token-based $10/mo + list price +10%). New rows: inline autocomplete, offline/local models, best for. Factual fix: Cursor pricing corrected from "$20/month flat" → credit-based (since June 2025, $20 included + overages).

- **Subscription quotas: "Claude Code prompts / 5h" column** (`guide/ultimate-guide.md` §Subscription Plans & Limits) — token budgets table enriched with a practical "Claude Code prompts/5h" column: Pro ~10-40, Max 5x ~50-200, Max 20x ~200-800. Warning note completed: ~50 active windows monthly cap + sub-agents/1M context impact on consumption.

- **Resource evaluation: benchmark AI coding tools Feb 2026** (`docs/resource-evaluations/benchmark-ai-coding-tools-feb2026.md`) — evaluation of a comparative 5-tool benchmark (Claude Code, Cursor, Windsurf, Zed, Copilot Workspace), text copied without source URL. Score 3/5 (relevant, selective integration). 2 net items integrated: prompts/5h quotas + comparison table extension. 4 recommendations rejected (already covered).

- **Claude Code v2.1.63 release tracking** — `machine-readable/claude-code-releases.yaml` + `guide/core/claude-code-releases.md` updated with v2.1.61, v2.1.62, v2.1.63 (HTTP hooks, worktree config sharing, `/simplify` + `/batch` bundled commands, `ENABLE_CLAUDEAI_MCP_SERVERS` env var, wave of memory leak fixes)

- **HTTP hooks documentation** (`guide/ultimate-guide.md` §7.2 Creating Hooks) — new hook type `"http"` (v2.1.63+): POST JSON to a URL, receives JSON in return. Added to the Configuration Fields table, descriptive bullet point, and complete config example with `allowedEnvVars`

- **Resource evaluation W09-2026** (`docs/resource-evaluations/weekly-intel-2026-W09.md`) — evaluation of the Anthropic/Claude Code weekly watch report (Feb 24 – Mar 1, 2026): score 4/5, 3 items integrated (v2.1.63 releases, HTTP hooks, Haiku 3 deadline note already present), 3 items rejected (Cowork, DoW, Vercept)

- **Section 9.23 — Configuration Lifecycle & The Update Loop** (`guide/ultimate-guide.md`) — continuous improvement loop for Claude Code configurations: friction detection from JSONL logs (`detect-friction.sh` script), skills lifecycle management (semantic versioning, deprecation, CI staleness check GitHub Actions), "The Update Loop" pattern (observe → analyze → delta update → canary test), handoff integration, DSPy/TextGrad mentions
- **Observability: Reading for Quality, Not Just Quantity** (`guide/ops/observability.md`) — new subsection in "Analyzing Session Data": 3 qualitative patterns (repeated reads, tool failures, high edit frequency) with ready-to-use `jq` commands, linked to §9.23

- **Git MCP Server + GitHub MCP Server** (`guide/ultimate-guide.md` §8.2 MCP Server Catalog) — two new servers documented in the MCP catalog:
  - **Git MCP Server** (official Anthropic, `mcp-server-git`): 12 tools for local Git operations (git_status, git_diff, git_commit, git_log, git_create_branch, etc.), `uvx` setup, multi-repo config, Git MCP vs Bash comparison, typical workflows. Status: early dev.
  - **GitHub MCP Server** (official GitHub, `github/github-mcp-server`): full GitHub platform access (Issues, PRs, Projects, Code search, Enterprise), remote MCP via `api.githubcopilot.com/mcp/` (Copilot required) + self-hosted PAT-only. Documented fix for the `Incompatible auth server: does not support dynamic client registration` error: inject token via `gh auth token` + manual header in `~/.claude.json`. Expired maintenance token note included.

- **Resource evaluation: MCP servers watch** (`docs/resource-evaluations/2026-03-02-mcp-servers-veille.md`) — evaluation of a watch report on 3 MCP servers (GitHub MCP, Exa, Graphiti). Final post-challenge scores: GitHub MCP 4/5 (integrated), Exa 2/5 (rejected, unverifiable stars 220 vs claim 3.1k), Graphiti 2/5 (rejected, heavy stack, Kairn already covers the need). Git MCP 5/5 (CRITICAL, previous evaluation) integrated simultaneously.

- **MCP Server: 3 new tools** — compare_versions, get_threat/list_threats, search_examples
  - `compare_versions(from, to?)` — diff between two Claude Code CLI versions: all releases in the range, aggregated highlights, aggregated breaking changes
  - `get_threat(id)` — lookup CVE (e.g. `CVE-2025-53109`) or attack technique (e.g. `T001`) from the threat database v2.4.0
  - `list_threats(category?)` — browse the threat-db: global summary with counts (no category) or detailed list by section (`cves`, `authors`, `skills`, `techniques`, `mitigations`, `sources`)
  - `search_examples(query, limit?)` — semantic search across 175 templates by intent (e.g. `"hook lint"`, `"agent code review"`) — complementary to `get_example` (exact name) and `list_examples` (category)
  - `mcp-server/IDEAS.md` — future ideas documented: `get_quiz`, `get_methodology`, `get_workflow`, resource `diff`, prompt `security-review`
  - Total: 8 tools → 12 tools (+ 3 resources + 1 prompt)

- **Terminal Personalization Settings** — documentation `spinnerVerbs` + `spinnerTipsOverride` in `guide/ultimate-guide.md` §3.3 Settings & Permissions
  - New section "Terminal Personalization Settings" (line 4978): JSON examples for `spinnerVerbs` (replace/add mode) and `spinnerTipsOverride` (with `excludeDefault: true`)
  - `settings.json` available keys enriched: added `spinnerVerbs`, `spinnerTipsOverride`, `plansDirectory`, `enableAllProjectMcpServers`
  - Link to complete example in the guide section
  - New file `examples/config/settings-personalization.json` — 183 lines, 19 custom verbs, 113+ tips in 13 categories (Context, Shortcuts, Prompting, Models, Plan Mode, Memory, Golden Rules, MCP, Tasks, CI/CD, Cost, Debug, Remote, Worktrees, Security, Hooks, Agents, Resources)
  - `machine-readable/reference.yaml`: new entry `spinner_personalization` + line number fix `permissions_deny_tool_qualified` (4978→5008)
  - Source: LinkedIn post on spinner verbs (evaluation score 3/5, gap confirmed from eval #070)

- **Tool-qualified deny format documentation** — new section in §3.3 Settings & Permissions (`guide/ultimate-guide.md`)
  - Permission Patterns table enriched: `Read(file_path:*.env*)`, `Edit(file_path:*.pem)`, `Write(file_path:*.key)`, `Bash(command:*rm -rf*)`
  - New section "Tool-qualified deny format" with complete example inspired by real production configs (strangebee, aristote): `Read(file_path:...)` syntax vs simple `".env"` format, glob patterns, note on known `permissions.deny` limitation (GitHub #4160)
  - Reference section §10.3 Permission Patterns updated with the 3 new lines
  - Source: comparative analysis of 3 production `.claude/` configs (StrangeBee/TheHive, Méthode Aristote, ccboard)

- **Resource evaluations** — 2 new evaluations in `docs/resource-evaluations/`
  - `069-claude-code-best-practice-repo-eval.md` — Evaluation of repo `shanraisshan/claude-code-best-practice` (score 4/5): bug fixed line 5646 (official agent fields misclassified as "community patterns"), interesting patterns identified
  - `070-claude-code-best-practice-dot-claude-eval.md` — Evaluation of `.claude/` config from the same repo (score 4/5): self-evolving agent pattern, Command→Agent→Skills architecture, `allowed-tools` wildcard scoping

### Fixed

- **MCP Server v1.0.3 — content path bug** (`mcp-server/src/lib/content.ts`)
  - ENOENT at production startup: `CONTENT_DIR` resolved `../../content` from `dist/` (2 levels), landing in `node_modules/` instead of the package root
  - Fix: `../content` (1 level) — tsup bundles everything flat in `dist/`, so 1 level is sufficient
  - Published on npm: `claude-code-ultimate-guide-mcp@1.0.3`

- **Bug line 5646 `guide/ultimate-guide.md`** — agent frontmatter fields `skills`, `background`, `isolation`, `memory` were incorrectly labeled "community patterns / not official spec". Replaced by complete official table verified against `code.claude.com/docs/en/sub-agents`. Fields concerned: `model`, `tools`, `disallowedTools`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation`, `color` — all official.

### Changed

- **`ccboard/.claude/settings.json`** — added `permissions.deny` with tool-qualified format (14 rules): protection for sensitive files (`.env*`, `.pem`, `.key`, `credentials`, `secrets`) and destructive commands (`rm -rf`, force-push, reset --hard). Config went from `budget`-only to complete security config.

- **Boris Cherny / Lenny's Newsletter integration** — 3 insights from Head of Claude Code interview (Feb 19, 2026, Lenny's Newsletter)
  - `guide/ultimate-guide.md` l. 2350 — Empirical "80% Plan Mode" ratio: Boris Cherny starts ~80% of his tasks in Plan Mode, blockquote in the "When to Use Plan Mode" table
  - `guide/ultimate-guide.md` l. 4285 — New section "Build for the Model 6 Months Out" in CLAUDE.md compounding memory: strategic principle for designing workflows in anticipation of future models
  - `guide/ultimate-guide.md` l. 5492 — New section "Boris Cherny's 3 Principles for AI Teams" (end of §3.5): underfund projects, unlimited tokens first, go faster — management advice verified Business Insider
  - `docs/resource-evaluations/2026-02-25-boris-cherny-lenny-newsletter-podcast.md` — Complete evaluation (4/5, technical-writer challenge, Perplexity fact-check)

- **Remote Control (Mobile Access) — Section 9.22** — New section in `guide/ultimate-guide.md` documenting the Remote Control feature (Research Preview, v2.1.51+, Pro/Max only)
  - Two activation modes: `claude remote-control` CLI subcommand and `/rc` slash command
  - QR code + session URL connection workflow, `/mobile` command for app download
  - Community-sourced limitations: slash commands (`/new`, `/compact`) don't work in remote UI (undocumented in official Anthropic docs)
  - Advanced patterns: tmux multi-session workaround (bypass 1-session limit), VM/cloud persistent architecture
  - Security considerations, alternatives comparison (happy.engineering, OpenClaw, SSH, ngrok)
  - Section 9 Recap updated with Remote Control checklist item
  - TOC entry added: `[9.22 Remote Control (Mobile Access)]`

- **`guide/cheatsheet.md`** — Dedicated "Remote Control" section + Hidden Features entry
  - New section with full workflow: commands, QR/URL/app connection, limitations table, tmux pattern, auto-enable
  - Added to Hidden Features: v2.1.51 Remote Control
  - CLI flags table: `remote-control` subcommand
  - Slash commands table: `/remote-control`, `/rc`, `/mobile`

- **`guide/security/security-hardening.md`** — Part 7: Remote Control Security
  - Architecture diagram (outbound-only HTTPS relay model)
  - Threat model: session URL leak, RCE surface, corporate policy, persistent exposure
  - Community perspective (senior dev security concerns)
  - Best practices + enterprise considerations
  - Comparison table: Remote Control vs SSH, ngrok, VPN+SSH

- **`machine-readable/reference.yaml`** — Remote Control entries
  - Slash commands: `/remote-control`, `/rc`, `/mobile`
  - CLI: `remote-control` subcommand
  - Deep dive: `remote_control: 18843` line reference

- **`docs/resource-evaluations/2026-02-25-claude-code-remote-control.md`** — Resource evaluation (score 4/5)
  - Full fact-check, community feedback (FR Slack), 9 press articles found
  - Challenge section with risk analysis
  - Original insights: slash command limitation, tmux pattern, security concerns

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.56 (v2.1.52 → v2.1.56)
  - v2.1.56: VSCode extension crash fix on Windows
  - v2.1.55: BashTool EINVAL fix on Windows
  - v2.1.53: Stability release — Windows panics/crashes, WebAssembly crashes (Linux x64/Windows x64/ARM64), Remote Control shutdown fix

## [3.29.0] - 2026-02-24

### Changed

- **docs/resource-evaluations/agents-md-empirical-study-2602-11988.md** — Added "Community Reception" section
  - Key nuance: the `/init` command generates an LLM-generated context file → -3% performance (not "delete your CLAUDE.md")
  - Link to Charly Wargnier's post (LinkedIn, 72 reactions) as an example of community simplification
  - Note on posts paraphrasing the study without added value (do not cite as independent sources)

## [3.29.0] - 2026-02-24

### Added

- **guide/ultimate-guide.md §5.5** — Design Intelligence: UI UX Pro Max skill
  - Most popular repository in the ecosystem (33.7k stars, 3.3k forks, MIT, v2.2.1)
  - BM25 offline design reasoning engine on ~400 local JSON rules (67 UI styles, 96 palettes, 57 typographies)
  - Compatible with 14 AI assistants (Claude Code, Cursor, Copilot, Windsurf…)
  - Installation guide, workflows, usage examples

- **guide/ops/observability.md** — Complete MLflow Tracing section (~120 lines)
  - CLI mode (zero Python) + SDK mode with API wrapping
  - LLM-as-judge for automatic quality regression
  - Exact token counts vs ~15-25% variance from hooks
  - Complete setup: tracking URI, auto-tracing, evaluation with GPT-4o judge
  - Decision guide: when MLflow vs ccusage vs OpenTelemetry

- **guide/diagrams/06-development-workflows.md** — "AI Fluency — High vs Low Fluency Paths" diagram
  - 41st Mermaid diagram in the guide
  - Based on Anthropic AI Fluency Index (9,830 conversations analyzed)
  - Visualizes the gap between 30% high-fluency vs 70% low-fluency users

- **guide/ultimate-guide.md** — 3 empirical callouts from Anthropic AI Fluency Index
  - Rev the Engine pattern: users who challenge reasoning are 5.6× more likely to catch errors
  - CLAUDE.md: only 30% explicitly define collaboration terms before starting
  - Source: Swanson et al., "The AI Fluency Index", Anthropic (2026-02-23)

- **guide/ultimate-guide.md** — New docs v2.1.47-v2.1.50
  - `WorktreeCreate`, `WorktreeRemove`, `ConfigChange` hook events with bash examples
  - `last_assistant_message` field in Stop/SubagentStop hooks
  - `--from-pr` flag documentation + auto-link sessions PR
  - Repo-Level Plugin Policy via `--add-dir` (settings.json `extraKnownMarketplaces`, `enabledPlugins`)
  - LSP `startupTimeout` configuration (v2.1.50+)

- **docs/resource-evaluations/** — 4 new evaluations (83 → 84 files)
  - `2026-02-23-agentsview-session-analytics.md` — AgentsView score 3/5
  - `2026-02-23-anthropic-ai-fluency-index.md` — AI Fluency Index score 4/5
  - `2026-02-23-veille-cc-releases-2144-2150.md` — CC releases watch
  - `ui-ux-pro-max-skill.md` — UI UX Pro Max skill score 4/5

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.52
  - v2.1.51: `claude remote-control` subcommand, BashTool login shell perf, SDK account env vars, /model human-readable labels
  - v2.1.52: VSCode crash fix on Windows

### Changed

- **README.md** — 41 diagrams (was 40), 84 evaluations (was 78)
- **machine-readable/reference.yaml** — Entries added for new content
- **guide/diagrams/README.md** — Added the 41st AI Fluency diagram

### Version Bump

- Bumped guide version: 3.28.1 → 3.29.0
- Reason: new MLflow observability section, UI UX Pro Max, AI Fluency diagram + empirical callouts, 4 resource evaluations

### Added

- **guide/ultimate-guide.md §9.21** — New section "Legacy Codebase Modernization" (4-step workflow validated by independent research)
  - Trigger: Anthropic COBOL article (Feb 23, 2026) + IBM -13% drop same day (worst day since Oct. 2000)
  - Workflow: Discovery → Risk Analysis → Strategic Planning → Incremental Implementation
  - Concrete prompt patterns for each phase, realistic expectations table (-25% to -88% depending on context)
  - Stats verified via Perplexity: 220B COBOL lines (IBM), ~95% ATM (Reuters/industry), 93% accuracy COBOL→Java (arXiv Apr. 2025)
  - Documented anti-patterns: big bang migration, no parallel run, skip discovery, blind trust on business logic
  - Sources: arXiv 2504.11335, AWS EKS case study (Jul. 2025), WJAETS 2025, Airbnb case (6 weeks vs 1.5 years)
  - Resource evaluation: score 2/5 maintained (marketing article without technical depth) — workflow integrated via independent research

- **Anthropic AI Fluency Index (Feb 23, 2026)** — Integration of official Anthropic research (9,830 conversations analyzed) in 3 targeted points + diagram
  - **§2.3 Rev the Engine** — Empirical callout: 5.6× more error catches for users who question reasoning (justifies plan review)
  - **§3.1 CLAUDE.md Best Practices** — 30% callout: only 30% of users explicitly define collaboration terms → CLAUDE.md structurally fills this gap
  - **§9.11 Common Pitfalls** — "⚠️ Artifact Paradox" callout: polished artifacts (code, files) → −5.2pp gap identification, −3.7pp fact-checking, −3.1pp questioning (with 5 concrete countermeasures)
  - **guide/diagrams/06-development-workflows.md** — 5th diagram: "AI Fluency — High vs Low Fluency Paths" (Bold Guy flowchart, standard palette, click hrefs + ASCII fallback), total diagrams: 40 → **41**
  - **docs/resource-evaluations/2026-02-23-anthropic-ai-fluency-index.md** — Evaluation file (score 4/5, complete fact-check with exact article citations)
  - **machine-readable/reference.yaml** — 16 `ai_fluency_*` entries + `ai_fluency_diagram`, `resource_evaluations_count` 83→84, `mermaid_diagrams.description` updated

- **docs/resource-evaluations/2026-02-23-agentsview-session-analytics.md** — AgentsView evaluation (score 3/5, to integrate in 2-4 weeks)
  - Local web app (Go + Svelte 5 + SQLite FTS5) for search + analytics of Claude Code, Codex, Gemini CLI sessions
  - Confirmed gap: no existing tool in the guide combines FTS + visual analytics (heatmaps, velocity) in a local web UI
  - Barriers: 4-day-old repo (created Feb 19, 2026), 49 stars at time of evaluation
  - Author credibility: Wes McKinney (creator of pandas)
  - Integration plan: `guide/ops/observability.md` External Monitoring Tools section + mention in `guide/ecosystem/third-party-tools.md`
  - Initial score 4/5 → challenged to 3/5 (adoption not established) + placement corrected to `observability.md`

- **guide/ultimate-guide.md §5.5** — New entry "Design Intelligence: UI UX Pro Max" in Community Skill Repositories
  - Most popular design skill in the ecosystem (33.7k stars, 3.3k forks, MIT, v2.2.1)
  - Covers: 67 UI styles, 96 palettes, 57 typographies, 99 UX guidelines, 100 industry rules
  - Documentation of the Design System Generator (BM25 Python engine, offline) with exact commands
  - Master + Override pattern for multi-page projects documented with end-to-end workflow
  - 3 installation options (Claude Marketplace, CLI `uipro-cli`, manual git clone)
  - Security note updated post-source-audit (Feb 2026): no npm preinstall/postinstall scripts, Python engine 100% offline (stdlib + local CSV/JSON, zero network calls)
  - Evaluation: `docs/resource-evaluations/ui-ux-pro-max-skill.md` (score 4/5, traction verified via gh CLI, clean source audit)

- **machine-readable/reference.yaml** — Entry `ui_ux_pro_max` with URL, line number, stats

- **guide/ultimate-guide.md** — 7 sections added following Anthropic weekly watch Feb 17-23, 2026 (eval: `docs/resource-evaluations/2026-02-22-veille-hebdo-anthropic-17-23-fev.md`, score 3/5)

  **P1 — Prompt caching + missing env vars**
  - §1.7 Cost Optimization — Strategy 6: prompt caching API (`cache_control`, cache write/read pricing, break-even, 4 max breakpoints)
  - §Appendix Environment Variables — `CLAUDE_CODE_DISABLE_1M_CONTEXT` (v2.1.50+) and `CLAUDE_CODE_SIMPLE` (v2.1.50+) added to the main table

  **P2 — Model deprecations + agents**
  - §1.7 Pricing Model — Warning box: `claude-3-haiku-20240307` deprecated Feb 19, 2026, retirement April 20, 2026, migration to `claude-haiku-4-5-20251001`
  - §4.2 Frontmatter Fields — `background: true` (non-blocking, v2.1.49+) and `isolation: "worktree"` (isolated spawn, v2.1.50+) added to table
  - §4.4 Best Practices — New section "Background Agents": behavior, management (ctrl+f, double ESC/ctrl+C), default vs background mode comparison
  - §4.4 Best Practices — New section "`claude agents` CLI": command + annotated output example (v2.1.50+)

  **P3 — Native worktree isolation + security cross-ref**
  - §9.11 Git Worktrees — New subsection "Claude Code Native Worktree Features": `--worktree`/`-w` flag, declarative `isolation: "worktree"`, `WorktreeCreate`/`WorktreeRemove` hooks with complete `settings.json` example
  - §7.4 Security Hooks — Cross-ref callout to `security-hardening.md#claude-code-as-security-scanner-research-preview`

- **docs/resource-evaluations/2026-02-22-veille-hebdo-anthropic-17-23-fev.md** — Anthropic weekly watch evaluation file Feb 17-23, 2026 (score 3/5, partial integration)

- **README.md + CLAUDE.md** — Guide stats update: `~19K lines` → `~20K lines` (20,440 lines)

- **guide/diagrams/09-cost-and-optimization.md + guide/ultimate-guide.md §2.5** — Budget modifier for model selection decision flow
  - The "Model Selection Decision Flow" diagram implicitly assumed unlimited budget (Max/API) — blind spot flagged by the community
  - Added a **Budget modifier table**: Max/API → Opus plan + Sonnet impl; Pro/Teams Standard → Sonnet plan + Haiku impl (mechanical tasks)
  - Community pattern documented: *Sonnet for Plan → Haiku for Implementation* on Teams Standard $25/mo
  - ASCII version updated with the budget modifier
  - Note added in Decision Table §2.5 for the same modifier
  - Source: Frédéric Camblor feedback (community)

- **guide/ultimate-guide.md — §2.7 Configuration Decision Guide** (new section, ~73 lines)
  - Unified view "which mechanism for what?" for the 7 configuration mechanisms (CLAUDE.md, rules, commands, hooks, agents, skills, MCP)
  - **Semantic Roles table** — conceptual role → mechanism mapping in 6 lines
  - **Mechanism Comparison table** — 7 mechanisms with loading timing, optimal usage, token cost, reliability
  - **Decision Tree** — binary tree covering all 7 mechanisms in priority order
  - **56% Reliability Warning** — Gao 2026 stat + practical implications + safe CLAUDE.md/skill pattern
  - **Common Mistakes table** — 4 common anti-patterns with corrections
  - Sections 2.7→2.11 renumbered (Structured Prompting, Semantic Anchors, Data Flow, Under the Hood)
  - TOC, quick-jump bar, and 3 backlinks (§2.6, §3.4, §5.1) updated
  - `reference.yaml`: 4 new entries with anchors and line numbers

### Research

- **Resource Evaluation: fp.dev** (score 2/5 — watchlist)
  - fp.dev = agent-native local-first issue tracker for Claude Code (issues as git-committable `.md`, skills `/fp-plan` `/fp-implement` `/fp-review`, diff viewer)
  - Real differentiator vs Tasks API: committable issues in the repo. But insufficient adoption + Apple Silicon only + partial overlap with native Tasks API
  - File: `docs/resource-evaluations/2026-02-22-fp-dev-issue-tracker.md`
  - **Known Gap added** in `guide/ecosystem/third-party-tools.md`: "Agent-native issue tracking (markdown-based, git-committable)"
  - **Watch List**: re-evaluate when GitHub stars visible + release cadence + practitioner prod write-up

## [3.28.1] - 2026-02-22 (security patch)

### Security

- **Threat Database v2.1.0 → v2.2.0** — 2 new CVEs, 5 new scanning tools, 1 new attack technique
  - **CVE-2026-0755** (Critical, CVSS 9.8) — gemini-mcp-tool RCE via command injection; LLM-generated args passed to shell without validation; no auth, network-reachable; **no fix as of 2026-02-22**
  - **SNYK-PYTHON-MCPRUNPYTHON-15250607** (High) — mcp-run-python SSRF via overly permissive Deno sandbox allowing localhost access
  - **T010 Attack Technique** — Agent-to-Agent Communication Injection: attacker injects malicious instructions into Slack/GitHub/ticketing channels monitored autonomously by AI agents
  - **5 new scanning tools catalogued**: Proximity (open-source), Enkrypt AI MCP Scanner, Cisco MCP Scanner (behavioral analysis), NeuralTrust MCP Scanner, MCPScan.ai
  - **Defensive resource**: Anthropic Claude Code Security (AI-powered codebase scanner, launched 2026-02-21)
  - **4 new sources**: Lakera "Agent Skill Ecosystem" audit (4310 OpenClaw skills), Penligent AI CVE-2026-0755, Snyk mcp-run-python SSRF, THN Anthropic CC Security
- **guide/security/security-hardening.md** — CVE table updated with CVE-2026-0755 and mcp-run-python SSRF entries + critical warning note (no patch available)

## [3.28.1] - 2026-02-22

### Added

- **Visual Diagrams Series** — 40 Mermaid interactive diagrams in new `guide/diagrams/` directory (10 thematic files)
  - Files: 01-foundations, 02-context-and-sessions, 03-configuration-system, 04-architecture-internals, 05-mcp-ecosystem, 06-development-workflows, 07-multi-agent-patterns, 08-security-and-production, 09-cost-and-optimization, 10-adoption-and-learning
  - Each diagram: Mermaid (GitHub-native rendering) + ASCII fallback in `<details>` + source link
  - Consistent Bold Guy palette across all diagrams (6-color system)
  - Cross-linked from `visual-reference.md`, `guide/README.md`, and `reference.yaml`
  - Covers: 4-layer model, master loop, memory hierarchy, model selection, MCP rug pull attack, 3-layer defense, multi-agent topologies, TDD/spec-first/plan-driven workflows, UVAL protocol, trust calibration

- **guide/ultimate-guide.md — Managing Large MCP Server Sets** (section 8.3)
  - Documented problem: loading too many servers globally degrades Claude's tool selection
  - Recommended pattern: minimal global config (2-3 servers) + per-project `.mcp.json`
  - Mention of community tool cc-setup (TUI registry with health checks)
- **guide/workflows/plan-driven.md — Section "Advanced: Custom Markdown Plans (Boris Tane Pattern)"** (+169 lines)
  - 3-phase workflow: Emphatic Research → Annotation Cycle → Mechanical Implementation
  - Comparison table `/plan` native vs custom `.md` (selection criteria)
  - Annotation Cycle diagram with loop, guard prompt and exit criteria
  - Phase 1: why emphatic language changes Claude's behavior
  - Phase 2: Aristote-ready plan.md structure, exit criteria, Boris Tane quote
  - Phase 3: mechanical mindset, terse feedback
  - Complementary techniques table (cherry-picking, scope trimming, revert & re-scope)
  - Source: Boris Tane (Engineering Lead @ Cloudflare), Feb 2026
- **guide/ultimate-guide.md — AI Code Disclosure Policy** (section 3.5)
  - Threshold >10 consecutive lines = mandatory declaration
  - PR template: "What the AI did / What I did"
  - Graduated enforcement by level (junior → senior)
  - "Hidden vibe coding" anti-pattern documented
- **guide/ultimate-guide.md — claude-mem with Gemini** (section claude-mem)
  - Gemini 2.5 Flash alternative: $14/month vs Haiku $102/month (-86%)
  - Configuration instructions via localhost:37777 dashboard
  - Model comparison table with measured monthly cost (400 sessions/month)
- **guide/ultimate-guide.md — critical claude-mem gotchas** (section claude-mem)
  - Hooks coexistence: before/after JSON, silent overwrite risk documented
  - Fail-open v9.1.0+: worker down doesn't block Claude Code, restart instructions
- **guide/core/methodologies.md**: cross-reference to Boris Tane Pattern from Plan-First section
- **machine-readable/reference.yaml**: 4 new entries (`annotation_cycle_pattern`, `custom_markdown_plans`, `boris_tane_source`, `boris_tane_author`)
- **docs/resource-evaluations/boris-tane-how-i-use-claude-code.md**: formal evaluation (score 4/5, fact-check, integration decision)
- **docs/resource-evaluations/aristote-ai-instructions-patterns.md**: Méthode Aristote production patterns analysis (24 ai-instructions files)
- **guide/security/security-hardening.md — Part 4: Integration** (+104 lines)
  - **4.1 PR Security Review Workflow**: 3-agent pipeline (security-auditor → data flow trace → security-patcher), ready-to-use prompts
  - Table by change type (API endpoint, DB query, auth, file upload, third-party lib) with risk levels
  - Git `pre-push` hook to alert on sensitive files (auth, payment, token, session)
  - **Claude Code Security (Research Preview)**: presentation of Anthropic feature on waitlist, comparison with Security Auditor Agent
- **examples/agents/security-patcher.md**: new agent (companion to security-auditor)
  - Limited scope: applies patches identified by security-auditor, never autonomously
  - Explicit separation of responsibilities: auditor detects, patcher fixes
  - Proposes patches for human review, applies nothing without approval
- **examples/hooks/bash/security-gate.sh**: new PreToolUse hook
  - Detects application security anti-patterns before writing to source files
  - Complements `dangerous-actions-blocker.sh` (system ops) — focuses on application code
  - Exit 0 = allow, Exit 2 = block with contextual message
- **guide/workflows/pdf-generation.md**: "Output Formats & Commands" diagram (+48 lines)
  - 3-column ASCII table (format / command / output) with distinction between standard vs styled PDF
  - EPUB commands, live preview, batch loop with error summary
- **examples/skills/pdf-generator.md**: generation pipeline diagram (+28 lines)
  - ASCII diagram SOURCE → Quarto → template → Typst → PDF with output size annotations
- **docs/resource-evaluations/2026-02-22-boris-cherny-worktree-tips-reddit.md**: evaluation of Boris Cherny Reddit/Twitter (Claude Code creator) — 5 worktree tips, 40.2K views
- **docs/resource-evaluations/2026-02-22-guillaume-moigneu-worktree-linkedin.md**: evaluation of Guillaume Moigneu LinkedIn (Solution Architect @ Upsun) — built-in git worktree support

- **guide/ops/observability.md — 3 new monitoring sections** (+214 lines)
  - **Activity Monitoring**: audit of Claude Code actions via session JSONL — which files were read, commands executed, URLs fetched. Ready-to-use `jq` queries. Table of sensitive patterns (.env, rm -rf, external WebFetch)
  - **External Monitoring Tools**: comparison table ccusage / claude-code-otel / Akto / MLflow / ccboard with decision guide and install examples
  - **Proxying Claude Code**: why Proxyman/Charles fail (Node.js ignores system proxies), 4 solutions: `NODE_EXTRA_CA_CERTS`, `ANTHROPIC_API_URL`, mitmproxy (recommended), minimal Python proxy
- **docs/resource-evaluations/ccboard-activity-module-plan.md**: complete plan for the ccboard Activity module (Tab 10)
  - Rust data models (`ToolCall`, `FileAccess`, `BashCommand`, `NetworkCall`, `Alert`)
  - JSONL stream parser with destructive/sensitive detection
  - SQLite schema + lazy cache strategy (invalidation by mtime)
  - TUI layout with 5 sub-tabs (Files/Commands/Network/Alerts/Timeline)
  - Web API endpoints (`GET /api/activity/:session_id/...`)
  - 7 alert rules with severities
  - 5 implementation phases with checklists
- **machine-readable/reference.yaml**: 6 new entries (`activity_monitoring`, `external_monitoring_tools`, `proxying_claude_code`, `ccboard_activity_plan`...)

## [3.28.0] - 2026-02-21

### Added

- **Section 2.5 — Model Selection & Thinking Guide**: canonical section consolidated in `guide/ultimate-guide.md`
  - 4-column decision table (Task / Model / Effort / Estimated cost per task)
  - Effort levels with concrete examples of calibrated prompts (low/medium/high/max)
  - Model-per-agent patterns: planner (Opus), implementer (Haiku), architecture-reviewer (Opus)
  - "When Thinking Helps vs. Wastes Tokens" table
  - Cross-refs to OpusPlan, Rev the Engine, Cost Awareness
- **3 new agent templates** (`examples/agents/`)
  - `planner.md` — Opus, read-only, strategy before implementation
  - `implementer.md` — Haiku, mechanical execution, escalation note to Sonnet for business logic
  - `architecture-reviewer.md` — Opus, critical read-only review, verification protocol before assertion
- **7 new quiz questions** (09-037 → 09-043) in `quiz/questions/09-advanced-patterns.yaml`
  - Covers: model selection by task, `model:` frontmatter, `effort` parameter, Adaptive Thinking Opus 4.6

### Changed

- **3 redundant tables replaced** by cross-refs to Section 2.5:
  - Tactical Model Selection Matrix (Section 4)
  - Cost-Effective Model Selection (Section 12)
  - Model Selection Matrix (Section 9.13)
- **Effort levels enriched** (Section 9 Adaptive Thinking): concrete prompt examples added + cross-ref to 2.5
- **Sections 2.6→2.10 renumbered** to make room for new 2.5 (former Mental Model 2.5 → 2.6, etc.)
- **Cheatsheet**: condensed Quick Model Selection table added (3 lines + cross-ref)
- **`examples/README.md`**: agents count 6 → 9, 3 new lines in table
- **`machine-readable/reference.yaml`**: stale line numbers fixed, 4 new entries

## [3.27.9] - 2026-02-21

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.50
  - `WorktreeCreate`/`WorktreeRemove` hook events; `isolation: worktree` in agent definitions
  - `claude agents` CLI command; `CLAUDE_CODE_DISABLE_1M_CONTEXT` env var
  - Opus 4.6 fast mode now has full 1M context window
  - Major memory leak fixes + headless mode startup performance improvements

### Added

- **Talk Preparation Pipeline** — 6-stage skill pipeline: raw material → conference talk → Kimi slides
  - New workflow guide: `guide/workflows/talk-pipeline.md` (REX vs Concept modes, stage-by-stage guide, design patterns, real-world example)
  - New skill templates: `examples/skills/talk-pipeline/` (7 SKILL.md files + 2 templates)
    - Stage 1: Extract (source → structured summary, type auto-detection)
    - Stage 2: Research (REX only — git archaeology, changelog analysis, verified timeline)
    - Stage 3: Concepts (numbered, scored catalogue — HIGH/MEDIUM/LOW)
    - Stage 4: Position (angles, titles, descriptions, peer feedback draft + mandatory CHECKPOINT)
    - Stage 5: Script (5-act pitch, slide spec, Kimi prompt for AI slide generation)
    - Stage 6: Revision (master concept table, Q&A cheat-sheet, glossary)
    - Orchestrator (runs full pipeline from one invocation, routes by mode)
  - Generic Kimi template: `stage-5-script/templates/kimi-prompt-template.md` (dark theme, orange accent, WCAG AA)
  - Peer feedback template: `stage-4-position/templates/feedback-draft.md` (3 formats: Slack, email, LinkedIn)
  - Design patterns documented: skill chaining + file-based state, tool permission scoping, human-in-the-loop gate, AI-to-AI handoff (Claude → Kimi), dual execution modes
  - `reference.yaml`: 16 entries for talk pipeline components
  - `guide/workflows/README.md`: Talk Pipeline entry under Design & Content + Quick Selection Table

- **Resource evaluation**: Mergify "Cross-System Support Investigator" (score 4/5)
  - Production case study: Claude Code + 5 MCP servers (Datadog, Sentry, PostgreSQL, Linear, GitHub) for support ticket triage
  - Architecture pattern: Claude Code as operational orchestrator with parallel fan-out across MCP adapters
  - Results (self-reported): triage 15 min → <5 min; 75% first-pass accuracy
  - Integrated in `guide/ultimate-guide.md` §8.4 → new "Production Case Study" subsection with architecture diagram
  - Evaluation archived: `docs/resource-evaluations/2026-02-20-mergify-cross-system-support-investigator.md`

/- **Resource evaluation**: "Evaluating AGENTS.md" — ETH Zürich arXiv 2602.11988 (score 4/5)
  - First empirical study on repository-level context files (AGENTS.md/CLAUDE.md) effectiveness
  - Developer-written context files: **+4% agent success rate**; LLM-generated: **-3%** vs no context file
  - Inference cost penalty: **+20-23% in all cases** when file contains non-essential information
  - Mechanism: agents follow all instructions faithfully, even irrelevant ones → broader exploration, longer reasoning chains
  - Recommendation: include only build/test commands + project-specific tooling; style guides → separate docs
  - Benchmark: AGENTbench (138 instances, 12 repos) + SWE-bench Lite; 4 coding agents (Claude Code, Codex, Qwen Code)
  - Source: Gloaguen, Mündler, Müller, Raychev, Vechev — ETH Zürich, February 2026
  - Evaluation archived: `docs/resource-evaluations/agents-md-empirical-study-2602-11988.md`

### Changed

- `guide/ultimate-guide.md`: Added empirical research backing to CLAUDE.md Token-Saving Techniques section (~l.13393-13411)
  - New callout: context files with non-essential info add +20-23% inference cost regardless of line count (Gloaguen et al., 2026)
  - New research note after "Keep CLAUDE.md concise" best practice: +4% (dev-written) / -3% (LLM-generated) with mechanism explanation and tooling recommendation

- `guide/workflows/spec-first.md`: New "Task Granularity" section — vertical slices + PRD quality checklist
  - Vertical slice definition: thin, end-to-end unit for exactly one user behavior; one agent session = one slice
  - 6-dimension PRD quality checklist (Problem Clarity, Testable Criteria, Scope Boundaries, Observable Done, Requirements Clarity, Terminology)
  - Concrete example: over-scoped task vs properly-sized vertical slice
  - Inspired by Allan Hill (Fractional CTO) — [evaluation](docs/resource-evaluations/2026-02-19-allanhillgeek-decomposition-agentic-dev.md) (3/5)

- `guide/core/methodologies.md`: Expanded ATDD section with agentic application
  - Added 3-step agent workflow: Gherkin → failing tests → implementation
  - Gherkin example for "password reset" feature
  - Practical note: how to pass Gherkin file to Claude Code as task contract

- `machine-readable/reference.yaml`: 3 new index entries (`spec_task_granularity`, `spec_prd_checklist`, `atdd_with_agents`)

- **Resource evaluation**: Sylvain Chabaud — Spec-to-Code Factory (score 3/5)
  - Multi-agent pipeline BREAK→MODEL→ACT→DEBRIEF with 6 tooled validation gates (Node.js)
  - "No Spec No Code" + "No Task No Commit" invariants enforced via hooks — enforcement pattern not documented in the guide
  - Transparent token budget per phase (~900K total) — unique concrete estimate in the ecosystem
  - Mention added in `guide/core/methodologies.md` (SDD Tools table) and `guide/workflows/spec-first.md` (See Also)
  - Evaluation archived: `docs/resource-evaluations/sylvain-chabaud-spec-to-code-factory.md`

- **New Section 3.5**: Team Configuration at Scale — Profile-Based Module Assembly pattern
  - Covers N×M×P fragmentation problem (N devs × M tools × P OS) with modular solution
  - Architecture: profiles YAML + shared modules + skeleton template + TypeScript assembler script
  - Measured results: 59% context token reduction (380 → 185 lines avg, 5-dev production team)
  - CI drift detection via GitHub Actions daily check
  - 5-step replication guide + trade-offs table (when NOT to use)
  - Inserted between Section 3.4 (Precedence Rules) and Section 4 (Agents)

- **New workflow**: `guide/workflows/team-ai-instructions.md` — step-by-step setup guide
  - 6 phases: Audit → Extract Modules → Create Profiles → Assembler Script → CI Integration → Onboarding
  - Scaling thresholds: 1-2 devs (shared CLAUDE.md) → 3-5 (modules only) → 5+ (full profile assembly)
  - Troubleshooting table for common issues

- **New templates**: `examples/team-config/` — ready-to-use Profile-Based Assembly templates
  - `profile-template.yaml`: developer profile with core + conditional modules
  - `claude-skeleton.md`: CLAUDE.md template with `{{MODULE:*}}` and `{{#if}}` placeholders
  - `sync-script.ts`: TypeScript assembler with module resolution, conditional blocks, drift detection

- **reference.yaml**: 9 new entries for `team_ai_instructions_*` (section, workflow, templates, pattern, token savings)

## [3.27.8] - 2026-02-19

### Added

- **New GitHub Actions workflow**: `examples/github-actions/claude-code-review.yml` — prompt-based code review pattern
  - Uses `anthropics/claude-code-action@v1` with OAuth token support (API key as fallback)
  - Triggers on PR open/sync/ready + `/claude-review` on-demand comment
  - Scoped `allowed_tools`: read-only (Read, Glob, Grep + GitHub PR inspection/review tools)
  - Externalized prompt via `prompt_file:` — iterate on criteria without touching workflow YAML
- **New prompt template**: `examples/github-actions/prompts/code-review.md`
  - Anti-hallucination protocol: verify before reporting, no invented line numbers
  - Structured severity tiers: 🔴 MUST FIX / 🟡 SHOULD FIX / 🟢 CAN SKIP
  - 4-step workflow: gather context → analyze → verify → structured review output
  - Stack-agnostic with explicit "Stack Context" customization hook

- **Resource evaluation**: SKILLMIND/Boris Cherny workflow practices (score 2/5)
  - LinkedIn post by @stasbel (64K followers) sharing SKILL.md file attributed to Boris Cherny (Claude Code creator)
  - 6 workflow orchestration practices + 6 task management items + 3 core principles
  - Key concept: `tasks/lessons.md` self-improvement loop (Claude captures corrections as rules, reviewed each session)
  - Score 2/5: majority of content already covered in guide; novel delta = lessons.md naming convention vs PROGRESS.md
  - Evaluation file: `docs/resource-evaluations/2026-02-19-stasbel-skillmind-boris-cherny-workflow.md`

- **Resource evaluation**: Augment Context Engine MCP (score 3/5)
  - Cloud-hosted semantic code search MCP (launched Feb 6, 2026); indexes up to 500K files across repos/wikis
  - Self-published benchmark: 80% quality improvement on 300 Elasticsearch PRs (Claude Opus 4.5, not 4.6 as stated on product page)
  - Relevant as cloud alternative to grepai: managed, multi-repo, no local setup, but paid ($20+/month) and cloud-hosted
  - Evaluation file: `docs/resource-evaluations/2026-02-19-augment-context-engine-mcp.md`

- **Resource evaluation**: LinkedIn "Context Engineering" post (score 2/5)
  - Promotional LinkedIn post on "prompt engineering is dead, context engineering is king" — marginal relevance
  - Evaluation file: `docs/resource-evaluations/2026-02-19-linkedin-context-engineering-augment.md`

- **Resource evaluation**: LinkedIn activity-7428930570451083264 (inaccessible)
  - Could not fetch — LinkedIn authentication required
  - Evaluation file: `docs/resource-evaluations/2026-02-19-linkedin-activity-7428930570451083264.md`

### Changed

- `examples/github-actions/README.md`: added entry for prompt-based workflow (⭐ Recommended), updated directory tree
- `guide/ultimate-guide.md`: Added `tasks/lessons.md` variant to Fresh Context Pattern (Ralph Loop) section
  - Lightweight alternative for interactive sessions: Claude updates lessons.md with behavioral rules after each user correction
  - Reviewed at session start for compounding improvement effect
  - Clarifies distinction from PROGRESS.md (task state) vs lessons.md (behavioral rules)
- `CLAUDE.md`: Added Whitepaper Generation section (PDF + EPUB commands, stack documentation)

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.47 (from v2.1.45)
  - v2.1.47: VS Code plan preview auto-updates, `ctrl+f` kills all background agents, `last_assistant_message` hook field, 70+ bug fixes
  - v2.1.46: claude.ai MCP connectors support, orphaned process fix on macOS

## [3.27.7] - 2026-02-19

### Added

- **Resource evaluation**: Borg et al. "Echoes of AI" RCT (arXiv:2507.00788)
  - 2-phase blind controlled experiment, 151 participants (95% professional developers)
  - AI users 30.7% faster (median), habitual users ~55.9% faster
  - No significant maintainability impact for downstream developers — first RCT to explicitly target this question
  - Fact-checked against primary source; v2 (Dec 2025) confirmed via Perplexity
  - Co-authored by Dave Farley ("Continuous Delivery")
  - Evaluation file: `docs/resource-evaluations/2026-02-19-echoes-of-ai-maintainability-study.md`

### Changed

- `guide/roles/learning-with-ai.md`: Added Borg et al. 2025 RCT citation in Productivity Research bibliography (revised to factual/neutral wording after technical-writer audit)
- `guide/roles/learning-with-ai.md`: Added "On maintainability fear" note in "Why Some Teams Get Results" section — the real risks are skill atrophy and over-delegation, not downstream quality degradation
- `guide/ultimate-guide.md`: Added downstream maintainability nuance blockquote in §1.7 Trust Calibration — defect rates ≠ maintenance burden (Borg et al. 2025 blind RCT)
- `machine-readable/reference.yaml`: Added 4 entries — `productivity_rct_metr`, `productivity_rct_echoes`, `productivity_maintainability_empirical`, `trust_calibration_maintainability_nuance`
- Landing `faq/index.astro`: Updated "How much should I trust AI-generated code?" — added maintainability nuance (HTML visible answer + JSON-LD structured data)

## [3.27.6] - 2026-02-18

### Added
- New subsection "200K vs 1M Context: Performance, Cost & Use Cases" with MRCR benchmark table, cost-per-session table, decision guide, and key facts
- Community findings from Reddit/HN/blogs: Gemini comparison, "70% context → new session" workaround, real-world use case limits
- HN community validation reference: Opus 4.6 retrieves 49/50 spells across ~733K tokens (Harry Potter test)
- `machine-readable/reference.yaml`: 5 new entries for Sonnet 4.6 + context window comparison

### Changed
- Pricing table: Sonnet 4.6 now listed as default model (replaced Sonnet 4.5)
- Context Management section: updated to mention 1M beta with link to comparison subsection
- `threat-db.yaml` v2.1.0: added CVE-2026-23744 (MCPJam RCE), hightower6eu publisher (314+ malicious skills), Slopsquatting technique T009, Mcpwn scanner, OWASP Agentic AI Top 10 2026, new sources (VirusTotal, SentinelOne, Immersive Labs, arXiv)
- `cheatsheet.pdf`: updated binary

### Fixed
- Beta header corrected: `interleaved-thinking-2025-05-14` → `context-1m-2025-08-07` (different feature, deprecated on Opus 4.6)
- Sonnet 4.6 long-context pricing: added premium tier ($3→$6 / $15→$22.50 above 200K — applies to all models)
- Cost estimates recalculated: Sonnet 4.6 @ 1M ~$4.13 (was $2.25), Opus 4.6 @ 1M ~$6.88 (was $8.75)
- Restored Opus 4.6 MRCR 93% @ 256K with confirmed source (independent analysis of Anthropic data)
- Added usage tier 4 requirement (1M context not available on tiers 1–3)
- Clarified premium pricing applies to all tokens in request once input exceeds 200K (not just excess)

## [3.27.5] - 2026-02-17

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.45
  - Claude Sonnet 4.6 model support
  - `spinnerTipsOverride` setting for customizable spinner tips
  - SDK `SDKRateLimitInfo` / `SDKRateLimitEvent` for rate limit tracking
  - Fixed Agent Teams on Bedrock/Vertex/Foundry; memory improvements for large outputs

## [3.27.4] - 2026-02-17

### Added

- **Review Plan command template** (`examples/commands/review-plan.md`)
  - Structured plan review across 4 axes: architecture, code quality, tests, performance
  - Inspired by Garry Tan's (YC CEO) Plan Mode prompt, adapted for Claude Code's native config system
  - Includes BIG CHANGE / SMALL CHANGE modes, numbered issues with lettered options, "do nothing" option
  - Uses AskUserQuestion for structured interaction
- **Rules templates** (`examples/rules/`) — new directory
  - `architecture-review.md`: system design, dependencies, data flow, scaling, security
  - `code-quality-review.md`: organization, DRY violations, error handling, tech debt, engineering balance
  - `test-review.md`: coverage gaps, test quality, edge cases, failure modes
  - `performance-review.md`: database access, memory, caching, complexity

- **AI Kill Switch & Containment Architecture** (`guide/security/security-hardening.md` §3.5)
  - Three-level kill switch mapped to Claude Code mechanisms (scoped revocation → velocity governor → global hard stop)
  - Ready-to-use `velocity-governor.sh` hook example (rate-limiter for runaway agents)
  - Regulatory context: EU AI Act (Aug 2025), CoSAI AI Incident Response Framework V1.0, governance-containment gap stats
  - Sources: Fortune Dec 2025, CDOTrends Jan 2026, OASIS/CoSAI Nov 2025
- **AI-specific incident cross-reference** (`guide/ops/devops-sre.md`)
  - Added pointer from "When NOT to Use Claude" to security-hardening.md for AI incidents (prompt injection, MCP compromise, agent exfiltration)

- **Git Worktree command suite** (`examples/commands/`)
  - `git-worktree.md`: Overhauled — symlink `node_modules` by default, background verification, `--fast`/`--isolated` flags, companion command links
  - `git-worktree-status.md`: New — check background verification tasks (type check, tests, build)
  - `git-worktree-remove.md`: New — safe removal with branch cleanup, merge verification, DB teardown
  - `git-worktree-clean.md`: New — batch cleanup of stale/merged worktrees

### Updated

- **Claude Code Releases**: Updated tracking v2.1.42 → v2.1.44
  - v2.1.44: Auth refresh error fix
  - v2.1.43: AWS auth refresh timeout (3min), structured-outputs beta header fix on Vertex/Bedrock, non-agent markdown warnings fix
- **`reference.yaml`**: Added 12 new entries (review-plan, rules templates, git-worktree suite, security kill switch), updated resource evaluations count 67 → 74
- **Template count**: 113 → 116 (review-plan command, git-worktree-status/remove/clean commands, rules templates) — updated across README, CLAUDE.md, reference badges
- **Commands count**: 23 → 26 (git-worktree-status, git-worktree-remove, git-worktree-clean)

## [3.27.3] - 2026-02-16

### Updated

- **Claude Code Releases**: Updated tracking v2.1.41 → v2.1.42
  - v2.1.42: Startup optimization (deferred Zod schema), prompt cache hit rate improvement (date outside system prompt), Opus 4.6 effort callout, `/resume` and image error UX fixes

## [3.27.2] - 2026-02-15

### Added

- **YAML frontmatter on 90 markdown files** across `guide/` and `examples/`
  - Schema A (title, description, tags): 24 guide top-level + 15 workflow files
  - Schema B (name, description): 20 command templates (matches existing convention)
  - Schema C (title, description, tags with claude-md): 5 claude-md templates
  - Schema D (title, description, tags): 7 READMEs + 19 miscellaneous example files
  - Controlled tag vocabulary: 15 domains, 11 content types, 9 features
  - 18 files with existing frontmatter correctly skipped
  - Enables machine-readable metadata for navigation, SSG, SEO, and LLM consumption

## [3.27.1] - 2026-02-15

### Added

- **Grepai MCP documentation** (`guide/ecosystem/mcp-servers-ecosystem.md`)
  - New "Code Search & Analysis" section (~130 lines): semantic search, call graph tracing, setup guide
  - Privacy: fully local (Ollama + nomic-embed-text), zero data exfiltration
  - Token efficiency comparison: grepai 2-3K tokens vs Grep+Read 15K for same results
  - Cross-referenced from `reference.yaml`

- **2 new resource evaluations** (both scored 2/5 — not integrated)
  - `system-prompts-opus-4-6-update.md`: Re-evaluation of x1xhlol system prompts repo (Opus 4.6 update), still redundant
  - `2026-02-14-simone-ruggiero-qmd-token-savings-medium.md`: qmd token savings tool (Medium article), claims unverifiable, redundant with grepai

- **2 new hook templates** (`examples/hooks/bash/`)
  - `rtk-baseline.sh`: SessionStart hook — saves RTK gain baseline for delta tracking
  - `session-summary.sh`: SessionEnd hook — auto-displays session summary (inspired by Gemini CLI)

- **Watch list entry**: o16g (Outcome Engineering) — emerging framework by Cory Ondrejka (ex-VP Google/Meta)

### Changed

- **RTK documentation overhaul** (v0.7.0 → v0.16.0, 446 stars, rtk-ai org)
  - Updated 15+ files across guide + landing: org migration (rtk-ai/rtk), removed fork distinction
  - Added: Python, Go, Homebrew, hook-first install, `rtk init`, `rtk tree`, `rtk learn`
  - Removed outdated ls/grep warnings (bugs resolved in v0.16.0)
  - Evaluation score: 4.5/5 → 5/5 (446 stars, [700+ Reddit upvotes](https://www.reddit.com/r/ClaudeAI/comments/1r2tt7q/))
  - Landing site updated: Homebrew install, new command grid (cargo/python/go), removed name collision warning
  - `~/.claude/CLAUDE.md`: replaced fork install with cargo/Homebrew

- **Exports deprecated** — Moved `kimi.pdf` and `notebooklm.pdf` to `exports/deprecated/` (generated from ~9K line v1.x era, guide now ~19K lines)

### Fixed

- **Fact-check corrections across 22 files** (866 insertions, 308 deletions)
  - CVEs: 22→18 (7 files: README, CHANGELOG, SECURITY, competitive-analysis, etc.)
  - Resource evaluations: 56→67 (README), 55→67 (reference.yaml), 14→68 (CLAUDE.md)
  - Templates: 111→120 (badges), breakdown 22 commands→23, 18 hooks→30
  - Quiz questions: 257→264 (README, CLAUDE.md, reference.yaml, ai-ecosystem)
  - Guide lines: 11K→19K (competitive-analysis, CLAUDE.md, ai-ecosystem, audit-cheatsheet-prompt)
  - CLAUDE.md: version 3.9.9→3.27.0, evaluations 14→68, quiz 257→264
  - MCP ecosystem: updated date Jan→Feb 2026, added Code Search TOC entry

- **README positioning fact-check** (4 files, 21 edits)
  - Template count: 120/123 → **108** (ground truth recount: hooks 30→31, workflows 2→3, multi-provider removed)
  - Ratio: 14× → **24×** (19,000 ÷ 784 = 24.2×, added "16 specialized guides" context)
  - everything-claude-code stars: 31.9k → **45k+** (verified 2026-02-15)
  - Commands count in README: 20→23 (aligned with examples/README.md)
  - Added missing entries to `examples/README.md`: `session-summary-config.sh` (hook), `memory-stack-integration.md` (workflow)

## [3.27.0] - 2026-02-12

### Added

- **Watch List** (`docs/resource-evaluations/watch-list.md`)
  - Public tracker for resources monitored but not yet integrated (tools, MCP servers, articles, libraries)
  - Event-driven re-evaluation (trigger-based, not time-based) to avoid stale dates
  - 3 sections: Active Watch, Graduated, Dropped
  - Initial entries: ICM (MCP, pre-v1), System Prompts (x1xhlol, redundant with official sources)
  - Cross-referenced from `mcp-servers-ecosystem.md` (Monitor workflow) and `resource-evaluations/README.md`
  - Added to `reference.yaml` as `resource_evaluations_watchlist`
  - Replaces private `claudedocs/` watch list (deleted)

- **Entire CLI Integration** (launched Feb 2026 by Thomas Dohmke, ex-GitHub CEO, $60M funding)
  - Comprehensive coverage across 7 guide files: ai-traceability, third-party-tools, observability, ai-ecosystem, ultimate-guide, security-hardening, cheatsheet
  - **Replaces deprecated git-ai** (404 repo) in AI Traceability Guide with production-ready alternative
  - **Fills "Session replay" gap** documented in Known Gaps with rewindable checkpoints
  - Governance layer documentation for compliance use cases (SOC2, HIPAA, FedRAMP)
  - Agent handoff workflows for multi-agent orchestration (Claude → Gemini)
  - Session portability alternative to native `--resume` limitations
  - Quick reference added to community tools section
  - Formal resource evaluation created (docs/resource-evaluations/entire-cli.md) with 5/5 critical scoring

### Fixed

- **Corrected git-ai references** (ai-traceability.md section 5.1) - repo is 404, replaced with Entire CLI

## [3.26.0] - 2026-02-11

### Added

- **Security Threat Intelligence Database** (`examples/commands/resources/threat-db.yaml` v2.0.0)
  - Comprehensive threat DB compiled from Perplexity Deep Research across 15 sources
  - **63 malicious skills** catalogued (ClawHavoc 341 skills, Snyk ToxicSkills, PyPI supply chain)
  - **18 CVEs** tracked with component, severity, fixed_in version, and mitigation
  - **4 campaigns** documented: ClawHavoc (AMOS), ToxicSkills, PyPI MCP reverse shell, Postmark npm squatter
  - **IOCs**: 6 C2 IPs, exfiltration endpoints, malicious GitHub repos, malware hashes
  - **17 malicious skill patterns** for wildcard matching (prefix-based scanning)
  - **10 minimum safe versions** quick reference for MCP servers
  - **8 attack techniques** taxonomy (T001-T008) mapped to campaigns
  - **6 scanning tools** documented (mcp-scan, skills-ref, Garak, MCP Fortress, SafeDep vet, Koi Clawdex)
  - **5 defensive resources** (SAFE-MCP framework, VirusTotal integration, Docker MCP Gateway, Snyk AI-BOM, Bitsight TRACE)
  - Sources: Koi Security, Snyk, JFrog, Flatt Security, SentinelOne, Cymulate, Checkpoint, Bitsight, SafeDep, SAFE-MCP

- **New Slash Command**: `/security-check` (`examples/commands/security-check.md`)
  - Quick (~30s) configuration security check against known threats database
  - 7 phases: Load threat DB → MCP audit → Skills/agents audit → Hook security → Memory poisoning → Permissions → Exposed secrets
  - Outputs CRITICAL/HIGH/MEDIUM/LOW findings with exact fix commands

- **New Slash Command**: `/security-audit` (`examples/commands/security-audit.md`)
  - Full 6-phase security audit with scored posture assessment (/100, grades A-F)
  - Phases: Config (via /security-check) → Secrets scan → Injection surface → Dependencies → Hook security → Posture score
  - Includes benchmark against security-hardening.md recommendations

- **New Slash Command**: `/update-threat-db` (`examples/commands/update-threat-db.md`)
  - Research & update the threat intelligence database via Perplexity searches
  - 6 phases: Assess current state → 4 targeted searches → Deduplicate → Update YAML → Cascade to guides → Summary report
  - Designed for monthly maintenance or post-advisory updates

- **Threat DB Badge** in README: red badge linking to security-hardening.md showing CVE and malicious skill counts

- **Resource Evaluation**: "AI Fatigue is Real" by Siddhant Khare (`docs/resource-evaluations/siddhant-khare-ai-fatigue.md`)
  - Score: 3/5 — Time-boxing tactics, nondeterminism stress recognition

### Changed

- **README**: Commands count updated 18→22, 3 new security commands listed in examples library
- **CLAUDE.md**: Slash commands table updated with `/security-check`, `/security-audit`, `/update-threat-db`
- **reference.yaml**: 4 new entries (security_check_command, security_audit_command, security_threat_db, security_update_threat_db)
- **Learning Guide Enhancement**: AI fatigue symptom recognition integrated into `guide/roles/learning-with-ai.md`
  - Red Flags Checklist, Productivity Reality, UVAL Protocol sections updated

### Fixed

- **Extended Thinking Documentation**: Corrected `effort` parameter documentation based on [official Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/effort)
  - API syntax, scope clarification, official descriptions, control table, effort and tool use subsection

## [3.25.0] - 2026-02-10

### Added

- **New Mental Model Section**: "From Chatbot to Context System" (§2.5)
  - Addresses critical gap identified by [Robin Lorenz](https://www.linkedin.com/in/robin-lorenz-54055412a/) ([comment](https://www.linkedin.com/feed/update/urn:li:activity:7426936437746352128?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7426936437746352128%2C7426941635306987520%29))
  - AI Engineer, 17-agent orchestration in production
  - Four-layer framework unifying CLAUDE.md, skills, hooks, and project memory
  - Comparison table: What each layer does, when to set up (Week 1-3 + Ongoing)
  - Before/After examples: Chatbot mode vs Context system mode
  - Cross-references to §3.1 (Memory Files), §5 (Skills), §7 (Hooks), §9.10 (Continuous Improvement)
  - Location: guide/ultimate-guide.md line 2636 (after "You Are the Main Thread", before "Communicating Effectively")
  - **Impact**: Presents CLAUDE.md/skills/hooks/memory not as independent features but as layers of a unified context system
  - **Concept**: "Stop treating it like a chatbot. Give it structured context. Changes everything." — Robin Lorenz

### Changed

- **Mistake #8 Rewritten**: "Not Using CLAUDE.md" → "Treating Claude Code Like a Chatbot" (§1.8)
  - Expanded scope: From single-feature warning to systematic context building approach
  - Fix now includes: CLAUDE.md + Skills + Hooks (3-layer solution instead of 1)
  - Cross-reference to new §2.5 section for full framework
  - Location: guide/ultimate-guide.md line 1274

- **Key Mindset Shift Updated**: Section 1.6 comparison table
  - Before: "conversational coding partner, not an autocomplete tool"
  - After: "structured context system, not a chatbot or autocomplete tool"
  - Added cross-reference to §2.5 for context system framework
  - Location: guide/ultimate-guide.md line 849

- **Quick Self-Check Enhanced**: Added cross-reference to CLAUDE.md checklist item
  - Checklist item now links to §2.5 for context on why CLAUDE.md matters
  - Location: guide/ultimate-guide.md line 1290

- **Continuous Improvement Mindset**: Added cross-reference to new §2.5 section
  - Links the "fix the system that produces the code" philosophy to the 4-layer framework
  - Location: guide/ultimate-guide.md line 12086 (after Nick Tune quote, before §9.11)

## [3.24.0] - 2026-02-10

### Added

- **Resource Evaluation**: nao framework (`docs/resource-evaluations/nao-framework.md`)
  - Evaluated open-source framework for building analytics agents
  - Score: 3/5 (Moderate - Useful Complement)
  - Identified critical gap: Agent evaluation not documented in guide
  - Technical challenge by technical-writer agent adjusted score from 2/5 to 3/5
  - All technical claims fact-checked (TypeScript 58.9%, Python 38.5%, stack verified)

- **New Guide Section**: Agent Evaluation (`guide/roles/agent-evaluation.md`, ~3000 tokens)
  - **Why Evaluate Agents**: Quantify quality, compare configurations, build feedback loops
  - **Metrics to Track**: Response quality, tool usage, performance, user satisfaction
  - **Implementation Patterns**: Logging hooks, unit tests, A/B testing, feedback loops
  - **Example**: Analytics agent with built-in metrics collection
  - **Tools & References**: nao framework as reference, Claude Code hooks integration
  - Addresses critical gap identified in nao evaluation
  - Navigation: After `guide/ultimate-guide.md` Section 4 (Agents)

- **AI Ecosystem Update**: Section 8.2 Domain-Specific Agent Frameworks (`guide/ecosystem/ai-ecosystem.md`)
  - New subsection after "Multi-Agent Orchestration Systems"
  - **nao (Analytics Agents)**: Database-agnostic framework with built-in evaluation
  - Transposable patterns: Context builder architecture, evaluation hooks, database integrations
  - Links to new `guide/roles/agent-evaluation.md` for implementation details
  - Location: guide/ecosystem/ai-ecosystem.md lines 1612-1638

- **Template**: Analytics Agent with Evaluation (`examples/agents/analytics-with-eval/`, 5 files)
  - **README.md**: Complete setup, usage, troubleshooting (production-ready)
  - **analytics-agent.md**: SQL query generator with evaluation criteria and safety rules
  - **hooks/post-response-metrics.sh**: Automated metrics logging (safety, performance, errors)
  - **eval/metrics.sh**: Analysis script for aggregating collected metrics
  - **eval/report-template.md**: Monthly evaluation report template
  - Demonstrates patterns from `guide/roles/agent-evaluation.md` in complete implementation
  - Includes safety checks (destructive operations), performance monitoring, feedback loops

### Changed

- **Agent Evaluation Guide**: Updated template reference (line 434)
  - Changed "(coming soon)" to "with hooks, scripts, and report template"
  - Added reference to complete template in "Example" section (line 277)
  - All links verified and functional

- **Landing Site**: Templates count synchronized
  - Updated index.html: 110 → 114 templates
  - Updated examples/index.html: 110 → 114 templates
  - Reflects addition of analytics-with-eval template (5 new files)

## [3.23.5] - 2026-02-10

### Added

- **Prompt Template**: `claudedocs/prompts/analyze-claude-mem-integration.md`
  - Comprehensive 6-phase analysis framework for claude-mem integration
  - Designed for Aristote project (EdTech, Next.js/tRPC/Prisma)
  - Audit current memory stack (Serena, grepai, 9 hooks)
  - Cost/ROI estimation ($3.75/month API, 50-100x ROI factor)
  - Integration plan with hooks synergy (activity-logger, serena-sync)
  - Go/No-Go decision criteria

## [3.23.4] - 2026-02-09

### Added

- **Agent Anti-Patterns Section** (§9.17): Critical guidance on proper agent usage
  - Citation from Dex Horty: "Subagents are not for anthropomorphizing roles, they are for controlling context"
  - Wrong vs Right table: Anthropomorphizing (Frontend Agent) vs Context Control (scope-focused agents)
  - When to use agents (good reasons): Context isolation, parallel processing, scope limitation
  - When NOT to use agents (bad reasons): Fake teams, roleplaying, mimicking human org structure
  - Section location: guide/ultimate-guide.md line 3662

### Changed

- **Agent Terminology Refactoring** (Breaking conceptual change): Systematic replacement of role-based language with scope-focused terminology
  - **Section renames**: "Split-Role Sub-Agents" → "Scope-Focused Agents" (line 3709)
  - **Agent definitions**: "Specialized role" → "Context isolation tool" (Skills vs Agents table, line 5490)
  - **Custom agent examples** (3 refactored):
    - code-reviewer: "You are a senior code reviewer" → "Perform comprehensive code reviews with isolated context"
    - debugger: "You are a systematic debugger" → "Perform systematic debugging with isolated context"
    - backend-architect: "You are a senior backend architect" → "Analyze backend architecture with isolated context"
  - **Prompt examples** (8+ refactored): All agent prompts now specify scope boundaries with explicit context
    - Before: "Security Agent: Check for vulnerabilities"
    - After: "Security Scope: Check for vulnerabilities (context: auth, input validation code)"
  - **Production examples**: Pat Cullen's Multi-Agent Code Review, Fountain case study (line 5335, 16623)
  - **Workflow files**: agent-teams-quick-start.md, agent-teams.md, tdd-with-claude.md, iterative-refinement.md
  - **Terminology replacements**:
    - "Specialized agents" → "Scope-focused agents"
    - "Expert personas" → "Context boundaries"
    - "Multi-domain expertise" → "Multi-scope analysis"
    - "Diversify expertise" → "Diversify analysis angles"
  - **Example agents** (5 files in examples/agents/): All refactored to use functional language instead of role-based personas

### Fixed

- **Methodologies**: Added clarification note to BMAD description about role-based naming (guide/core/methodologies.md line 49)

## [3.23.3] - 2026-02-09

### Added

- **Opus 4.6 Integration**: Comprehensive documentation update for Claude Opus 4.6 features (Feb 2026)
  - **Adaptive Thinking**: Replaced budget-based thinking with dynamic depth calibration
    - Effort parameter: `low|medium|high|max` (API only, default: high)
    - API syntax: `thinking: {"type": "adaptive", "effort": "high"}`
    - CLI: Same Alt+T toggle (no per-request control)
    - Deprecation: `budget_tokens` no longer functional on Opus 4.6
    - Section: Extended Thinking (line 9911), API Breaking Changes (line 10044)
  - **Fast Mode** (`/fast` command, v2.1.36+): 2.5x faster responses, 6x price
    - CLI: `/fast` command (toggle, persists across sessions)
    - API: `speed: "fast"` + beta header `fast-mode-2026-02-01`
    - Pricing: $30/$150 per 1M tokens (vs $5/$25 standard)
    - Added to Commands Table (line 16279), Pricing Model (line 1722)
  - **Pricing Tiers**: Updated pricing table with Opus 4.6 three-tier model
    - Standard: $5/$25 per 1M tokens (200K context)
    - 1M Context Beta: $10/$37.50 per 1M tokens (requests >200K)
    - Fast Mode: $30/$150 per 1M tokens (2.5x speed)
  - **API Breaking Changes**: Documented removed and deprecated features
    - `assistant-prefill` removed (use system prompts instead)
    - `budget_tokens` deprecated (use adaptive thinking)
- **Auto-Memories** (v2.1.32+): Automatic context capture across sessions
  - Opt-in feature, per-project storage
  - Automatically identifies: decisions, preferences, patterns, known issues
  - Separate from CLAUDE.md (personal vs team-level)
  - Comparative table: CLAUDE.md vs auto-memories (line 3999)
  - Section: Memory Files (line 3986)
- **Context Management**: "Summarize from here" feature (v2.1.32+)
  - Right-click message → summarize from that point forward
  - More precise than full `/compact`
  - Added to Context Recovery Strategies (line 1470)
- **Debug Command** (`/debug`, v2.1.30+): Systematic troubleshooting
  - Added to Commands Table (line 16280)
  - Purpose: Error investigation and debugging workflows
- **Agent Teams Enhancements** (v2.1.32+)
  - Hook events: `TeammateIdle` and `TaskCompleted` in events table (line 6972)
  - Agent frontmatter: `memory` field for pre-populated context (line 4849)
  - Enables persistent agent context without repeating project details
- **Xcode Integration** (Feb 2026): Native Claude Agent SDK support
  - Xcode 26.3 RC+ includes built-in Claude assistant
  - Same harness as Claude Code CLI
  - Section: IDE Integration (line 10834)
- **Session Cross-Folder Migration** (Feb 2026): Documentation for resume limitations and workarounds
  - **Architecture explanation**: Why `--resume` is limited to current working directory
  - **Manual migration workflow**: Filesystem operations for moving/forking sessions
  - **Risk documentation**: Secrets, paths, MCP mismatches explicitly warned
  - **Community tool mention**: Jim Weller's claude-migrate-session skill (with 0 adoption caveat)
  - **GitHub issue tracking**: Issue #1516 for native cross-folder support
  - Section: Session Resume Limitations & Cross-Folder Migration (observability.md:117)
  - FAQ entry: "Can I continue a session from a different project folder?" (ultimate-guide.md:~18312)
  - Resource evaluation: docs/resource-evaluations/weller-session-migration-skill.md
  - Reference: machine-readable/reference.yaml (session_resume_limitations, session_migration_*)
  - Clarified: Claude Agent SDK ≠ Claude Code (shared framework, different products)
- **machine-readable/reference.yaml**: 24 new entries
  - Auto-memories, fast mode, debug command, Opus 4.6 features
  - Hook events (TeammateIdle, TaskCompleted)
  - Agent memory field, Xcode integration, adaptive thinking
  - Updated: 2026-02-09
- **llms.txt Standard Documentation** (Section 9.18.4): AI-optimized documentation indexing
  - **Concept explanation**: llms.txt as documentation discovery standard for LLMs
  - **Format and structure**: Plain text index at `/llms.txt` or `/machine-readable/llms.txt`
  - **Complementarity with MCP**: Clarifies llms.txt (static index) vs Context7 MCP (runtime lookup)
  - **Implementation examples**: Minimal and advanced patterns with line numbers
  - **CLAUDE.md integration**: How llms.txt and CLAUDE.md serve different purposes
  - **Repository example**: References this guide's own `machine-readable/llms.txt` implementation
  - Section: Documentation Formats for Agents (line 14544)
  - Resource: docs/resource-evaluations/wasp-fullstack-essentials-eval.md (score 3/5)
  - Source: llmstxt.org specification (official standard)
  - Gap addressed: Repository had llms.txt file without conceptual documentation
- **Background Tasks Workflow** (Section 9.5): Fullstack development patterns with Ctrl+B
  - **When to background**: 5 scenarios (dev server, test watcher, build, migration, docker)
  - **Fullstack workflow pattern**: Dev server backgrounded while iterating on frontend
  - **Real-world example**: API + frontend iteration maintaining tight feedback loops
  - **Context rot prevention**: `/tasks` monitoring strategies
  - **Limitations**: No foreground command, session-scoped tasks, output visibility
  - **Teleportation integration**: Background tasks not transferred, restart required
  - **Disable flag**: `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable (v2.1.4+)
  - Section: Background Tasks for Fullstack Development (line 11057)
  - Resource: docs/resource-evaluations/wasp-fullstack-essentials-eval.md (score 3/5)
  - Gap addressed: Ctrl+B documented as feature, now complete workflow strategy
- **Chrome DevTools MCP Server** (mcp-servers-ecosystem.md): Debugging and inspection capabilities
  - **Official Anthropic server**: Chrome DevTools Protocol integration
  - **Use case**: Debugging web apps, runtime inspection, complements Playwright MCP
  - **Key features**: Console access, network monitoring, DOM inspection, JS execution, profiling
  - **Comparison table**: Chrome DevTools (debugging) vs Playwright (testing)
  - **Setup and limitations**: Manual Chrome launch with remote debugging port
  - Section: Browser Automation (line 418)
  - Statistics: 3 browser servers (was 2), 6 official servers (was 5)
  - Resource: docs/resource-evaluations/wasp-fullstack-essentials-eval.md (score 3/5)
  - npm: @modelcontextprotocol/server-chrome-devtools
- **Convention-Over-Configuration for AI** (Section 9.18.1): Framework selection impact
  - **Problem**: Custom architectures require extensive CLAUDE.md documentation
  - **Solution**: Opinionated frameworks reduce agent cognitive load through conventions
  - **Comparison table**: Custom vs opinionated architectures (file organization, routing, testing)
  - **Framework examples**: Next.js, Rails, Phoenix, Django with convention benefits
  - **Real-world impact**: Fewer mistakes, faster boilerplate, smaller CLAUDE.md files
  - **Trade-offs**: Faster onboarding vs architectural flexibility
  - **CLAUDE.md connection**: Convention-over-config directly reduces token requirements
  - Section: Convention-Over-Configuration for AI Agents (line 14380)
  - Resource: docs/resource-evaluations/wasp-fullstack-essentials-eval.md (score 3/5)
  - Gap addressed: Existing AX framework concept reinforced with framework angle

### Changed

- **Pricing Model**: Updated default model from "Sonnet 3.5" to "Sonnet 4.5" (line 1720)
- **Model References**: 8 mentions "Opus 4.5" updated to "Opus 4.6" or context-appropriate version
  - Status line example, Trinity pattern description, TDD workflow, benchmarks
- **Comparative Tools Table**: Corrected PowerPoint capability
  - Before: "No PPTX output capability"
  - After: "Limited PPTX (via Claude in PowerPoint add-in, research preview)"
  - Note: Claude in PowerPoint exists but limited to add-in (line 17251)

### Security

- **CVE Update**: Added Claude Code v2.1.34 security fix to security-hardening.md
  - Critical sandbox bypass vulnerability patched
  - Recommendation: **Upgrade to v2.1.34+ immediately**
  - Details undisclosed pending broader adoption
  - Added to CVE Summary table (guide/security/security-hardening.md)

### Documentation

- **Fact-Checking**: All Opus 4.6 details verified via Perplexity Pro
  - Pricing confirmed: $5/$25 (standard), $10/$37.50 (1M), $30/$150 (fast)
  - Adaptive thinking syntax validated: effort parameter, API examples
  - Fast mode behavior confirmed: 2.5x speed, 6x cost, persistent toggle
  - Auto-memories verified: opt-in, per-project, cross-session recall
  - Sources: Anthropic official docs, pricepertoken.com, eesel.ai, help.apiyi.com

- **Templates**: Session handoff template based on Robin Lorenz's context engineering approach
  - Structured handoff at 85% context to prevent auto-compact degradation
  - Research-backed rationale (LLM performance drop 50-70% at high context)
  - Complete workflow: metadata, completed work, pending tasks, blockers, next steps, essential context
  - File: `examples/templates/session-handoff-lorenz.md`

### Changed

- **Architecture**: Auto-compaction confidence upgraded 50% → 75% (Tier 3 → Tier 2)
  - Added platform-specific thresholds: VS Code (~75% usage), CLI (1-5% remaining)
  - Added performance impact research section with 6+ sources
  - Performance benchmarks: 50-70% accuracy drop on complex tasks (1K → 32K tokens)
  - Research sources: Context Rot (Chroma), Beyond Prompts (UseAI), Claude Saves Tokens (Golev)
  - Added Lorenz's proactive thresholds: 70% warning, 85% handoff, 95% force handoff
  - File: `guide/core/architecture.md` Section 3.2
- **Context Management**: Added research-backed proactive thresholds
  - Replaced generic "Check context before resuming (>75%)" with specific 70%/85%/95% ladder
  - Added performance degradation warnings with research links
  - Clarified auto-compact triggers: ~75% (VS Code), ~95% (CLI) with quality impact
  - File: `guide/ultimate-guide.md` (lines ~734, ~3582)

### Documentation

- **Resource Evaluation**: Lorenz session handoffs post (score 4/5)
  - Initial score 2/5 → upgraded to 4/5 after Perplexity validation
  - 3 research queries validated core claims (auto-compact degradation, LLM performance, handoff best practices)
  - Technical-writer challenge identified 4 critical gaps in initial assessment
  - Integration: architecture.md + ultimate-guide.md + template created
  - File: `docs/resource-evaluations/lorenz-session-handoffs-2026.md`
- **Ecosystem**: Added awesome-claude-skills (BehiSecc) to curated lists
  - 62 skills taxonomy across 12 categories (Development, Design, Documentation, Testing, DevOps, Security, Data, AI/ML, Productivity, Content, Integration, Fun)
  - Positioned as complementary to awesome-claude-code (skills-only focus vs full ecosystem)
  - Distinct from ComposioHQ/awesome-claude-skills (different maintainer, taxonomy approach)
  - Referenced in guide section 8.5 (line 9721), Further Reading (line 17520), README.md, reference.yaml
  - Evaluation: `docs/resource-evaluations/awesome-claude-skills-github.md` (score 3/5)

## [3.23.2] - 2026-02-08

### Documentation

- **Claude Code Releases**: Updated tracking v2.1.33 → v2.1.37
  - v2.1.37: Fixed /fast availability after /extra-usage
  - v2.1.36: Fast mode now available for Opus 4.6
  - v2.1.34: Security fix for sandbox-excluded commands bypass + agent teams crash fix

### Added

- **Workflows**: Agent Teams Quick Start Guide (`guide/workflows/agent-teams-quick-start.md`)
  - Practical 8-10 min guide vs 30 min full documentation
  - 5-minute setup walkthrough (prerequisites → first test)
  - 4 copy-paste patterns for real projects (Guide pre-release review, landing sync, multi-file doc updates, RTK security PR review)
  - Decision matrix with 10+ scenarios (when YES, when NO, when MAYBE)
  - Success metrics framework (convergence rate, unique insights, false positive rate, time saving, bug catch rate)
  - Minimal workflow template (bash + prompt examples)
  - Red flags section (when NOT to use agent teams to avoid waste)

- **Slash Commands**: `/audit-agents-skills` command for quality auditing of agents, skills, and commands
  - 16-criteria framework (Identity 3x, Prompt 2x, Validation 1x, Design 2x)
  - Weighted scoring: 32 points max for agents/skills, 20 points for commands
  - Production readiness grading (A-F scale, 80% threshold for production)
  - Fix mode with actionable suggestions for failing criteria
  - Project-level command (`.claude/commands/`) + distributable template (`examples/commands/`)
- **Skills**: `audit-agents-skills` advanced skill with 3 audit modes
  - Quick Audit: Top-5 critical criteria (fast pass/fail)
  - Full Audit: All 16 criteria per file with detailed scores
  - Comparative: Full + benchmark analysis vs reference templates
  - JSON + Markdown dual output for CI/CD integration
  - Externalized scoring grids in `scoring/criteria.yaml` for programmatic reuse
- **Templates**: Added 3 audit infrastructure files
  - Command template: `examples/commands/audit-agents-skills.md` (~350 lines)
  - Skill template: `examples/skills/audit-agents-skills/SKILL.md` (~400 lines)
  - Scoring grids: `examples/skills/audit-agents-skills/scoring/criteria.yaml` (~120 lines, 16 criteria × 3 types)

### Documentation

- **Resource Evaluations**: Added Gur Sannikov "Claude Code as Embedded OS" evaluation (4/5 - High Value)
  - Score: 4/5 (ADR workflow gap + native capabilities checklist + community validation)
  - Decision: Integrate 4 sections across 3 guide files
  - Gap addressed: ADR-driven development pattern, capabilities onboarding checklist, dynamic model switching
  - Integration: ADR workflow (methodologies.md), Native Capabilities Audit (architecture.md), Dynamic Model Switching (cheatsheet.md), Community Validation (architecture.md)
  - Community validation: Cursor power user adopting Agent Skills standard (validates "less scaffolding, more model" philosophy)
  - Source: [LinkedIn post](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb) (2026-02-01)
- **Resource Evaluations Index**: Updated count from 24 to 55 evaluations
- **Slash Commands**: Added comprehensive documentation for `/insights` command (Section 6.1) with architecture deep dive
  - **Architecture Overview** subsection (7-stage pipeline: session filtering, transcript summarization, facet extraction, aggregated analysis, executive summary, report generation, facet caching)
  - **Facets Classification System**: 6 dimensions documented (13 goal types, 12 friction categories, 6 satisfaction levels, 4 outcome states, 7 success categories, 5 session types)
  - **Performance optimization**: Caching system explanation (facets/<session-id>.json for incremental analysis)
  - **Interpretation guidance**: How facets categories help understand report recommendations
  - **Source attribution**: Zolkos Technical Deep Dive (2026-02-04) as architecture reference
- **Agent/Skill Quality**: Added 2 strategic references in ultimate-guide.md
  - After Agent Validation Checklist (line 4951): Automated audit call-out with methodology reference
  - After Skill Validation (line 5495): Beyond spec validation note explaining quality scoring extension
- **Resource Evaluations**: Added Mathieu Grenier agent/skill quality evaluation (3/5 - Moderate Value)
  - Score: 3/5 (real-world observations, identifies automation gap, aligns with LangChain 2026 data)
  - Decision: Integrate selectively via audit tooling creation
  - Gap addressed: Guide had conceptual best practices but no automated enforcement
  - Industry context: 29.5% deploy agents without evaluation (LangChain Agent Report 2026)
  - Integration: Created `/audit-agents-skills` command + skill + criteria YAML
- **Resource Evaluations**: Added Zolkos /insights deep dive evaluation (4/5 - High Value)
  - Score: 4/5 (comprehensive technical architecture, fills guide gap, complementary with usage documentation)
  - Decision: Integrate architecture + facets classification system
  - Integration: Architecture overview added to Section 6.1 (~800 tokens)
  - Complementarity: Zolkos (internal architecture) + Guide (external usage) = complete documentation
- **Resource Evaluations Index**: Updated count from 23 to 24 evaluations (added Grenier entry)

## [3.23.1] - 2026-02-06

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.33 (2026-02-06)
  - Agent teams fixes (tmux sessions, availability warnings)
  - `TeammateIdle` and `TaskCompleted` hook events for multi-agent workflows
  - Agent frontmatter: `memory` field (user/project/local scope), `Task(agent_type)` sub-agent restriction
  - Plugin name in skill descriptions and `/skills` menu
  - VSCode: Remote sessions, branch/message count in session picker
  - Multiple stability fixes and improved error messages

## [3.23.0] - 2026-02-06

### Changed

- **Adaptive Onboarding Architecture v2.0.0** — Major redesign of interactive onboarding system addressing 8 critical gaps identified by technical-writer challenge (~2,100 lines modified, 2 validation scripts, metrics plan)
  - **Adaptive topic selection**: Each profile now has **core topics** (always shown) + **adaptive topics** (context-based via keyword triggers). Claude analyzes user messages (e.g., "I work in a team and use git") to surface relevant v3.21-3.22 content (config_hierarchy, git_mcp_guide, mcp_secrets_management, dual_instance_planning, sandbox_native_guide) based on relevance, not chronology
  - **Security-first fix**: Moved `sandbox_native_guide` from `beginner_30min` → `beginner_5min` (CRITICAL fix). New users now learn sandboxing security **BEFORE** running commands, addressing technical-writer's "security gap HIGH RISK" finding
  - **Time budget validation**: All 18 profiles validated (6-8 min/topic average), respects `topics_max` limits. Prevents overwhelming users (e.g., power_30min: 4 topics max, not 6). Addresses "time budget impossible" challenge finding
  - **New learn_security goal**: Dedicated security-focused learning path with 2 profiles (intermediate_30min, power_60min) covering sandbox_native, mcp_secrets, security_hardening, production_safety, sandbox_isolation_guide. Fills gap for security-conscious users
  - **V3.21-3.22 comprehensive coverage**: All CRITICAL (5/5) and HIGH VALUE (4/5) topics now discoverable via adaptive triggers: git_mcp_guide (v3.22.0), config_hierarchy (v3.21.0), mcp_secrets_management (v3.21.0), dual_instance_planning (v3.22.0), sandbox_native_guide (v3.21.1)
  - **Quiz integration as exit activity**: Phase 4 wrap-up now recommends quiz by profile level (beginner: 60 questions ~15 min, intermediate: 100 questions ~25 min, advanced: 97 questions ~30 min). Addresses "quiz = testing mechanism, not learning content" challenge finding. 13 new deep_dive entries for quiz system
  - **Fallback minimal by design**: Kept graceful degradation pattern (3-5 topics if fetch fails), rejected proposal to enrich fallback per technical-writer recommendation. Improved fetch reliability strategy over content expansion
  - **Portability warnings added**: Documents AskUserQuestion Claude Code-specific limitation, localization status (English only for v3.21-3.22 topics, on-the-fly translation for FR/ES with accuracy warnings), simplification steps for ChatGPT/Gemini compatibility
  - **Maintenance automation**: 2 validation scripts created
    - `validate-onboarding.sh` (6 checks): YAML syntax, deep_dive key existence, time budget compliance, topics_max constraints, question_flow completeness, version alignment with VERSION file
    - `detect-new-onboarding-topics.sh`: Scans resource evaluations for CRITICAL/HIGH VALUE topics not in any profile, run monthly to prevent future drift
  - **Version metadata system**: `onboarding_matrix_meta` section added with version tracking (v2.0.0), changelog, maintenance guidelines (review trigger: every CRITICAL/HIGH feature), automation pointer (detect-new-topics script), responsible party (quarterly reviews)
  - **Files modified**: `reference.yaml` (+150 lines: onboarding_matrix_meta, adaptive matrix, learn_security goal, quiz deep_dive entries), `onboarding-prompt.md` (+80 lines: adaptive logic Phase 1/2, learn_security in Phase 1.5, quiz recommendations Phase 4, portability warnings), `scripts/validate-onboarding.sh` (350 lines), `scripts/detect-new-onboarding-topics.sh` (200 lines), `claudedocs/adaptive-onboarding-design.md` (1,100 lines design doc with 12 sections + 2 appendices)
  - **Impact**: Adoption improvement (30% of users use onboarding → 30% now discover v3.21-3.22 features), Security enhancement (beginners learn sandbox FIRST, not eventually), Support reduction (users following updated paths avoid "Why wasn't I told about X?" issues), Maintenance automation (gap detection prevents future drift), Portability transparency (users know AskUserQuestion limitation, localization accuracy warnings)
  - **Challenge validation**: Technical-writer agent challenged initial analysis, identified 8 missing angles (severity underestimation, sandbox placement wrong, quiz integration superficial, time budget violations, fallback design misunderstanding, user flow continuity gaps, maintenance burden unquantified, metrics plan missing). All 8 addressed in v2.0.0 design
  - **Effort**: 95 min actual (85 min estimated, +10 min for comprehensive testing/localization check)
  - **Credits**: Technical-writer agent (challenge phase identifying 8 critical gaps, adaptive architecture recommendation, time budget validation requirement, quiz UX correction, fallback graceful degradation insight), user request for onboarding sync verification

## [3.22.1] - 2026-02-05

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.32 (2026-02-05)
  - ⭐ **Opus 4.6 is now available**
  - ⭐ **Agent teams research preview** — Multi-agent collaboration for complex tasks (experimental, token-intensive)
  - ⭐ **Automatic memory recording and recall** — Claude now automatically records and recalls memories as it works
  - **"Summarize from here"** — Message selector allows partial conversation summarization
  - Skills from `.claude/skills/` in `--add-dir` directories now auto-load
  - Multiple fixes: `@` file completion paths, bash heredoc JS template literals, Thai/Lao vowel rendering
  - [VSCode] Fixed slash commands executing incorrectly, added conversation loading spinner

## [3.22.0] - 2026-02-04

### Documentation

- **Claude Code Releases**: Updated tracking to v2.1.31 (2026-02-04)
  - v2.1.31 (2026-02-03): Session resume hint, PDF/bash/LSP fixes, system improvements
  - v2.1.30 (2026-02-02): PDF page range support (`pages` parameter), pre-configured OAuth for MCP (Slack), `/debug` command, git log/show flags, task tool metrics
  - Notable features: PDF pages parameter for large documents (>10 pages), built-in OAuth for servers without Dynamic Client Registration, new troubleshooting command, reduced motion accessibility mode

### Added

- **Dual-Instance Planning Pattern (Jon Williams)** — Vertical separation workflow (planner/implementer) as complement to horizontal scaling (Boris pattern), addressing solo dev and budget-conscious audience gap (~1,100 lines, scored 4/5 High Value after technical-writer challenge)
  - **New section: Alternative Pattern: Dual-Instance Planning** (`guide/ultimate-guide.md:12884-13230`, ~350 lines) — Comprehensive documentation covering when to use dual-instance pattern (solo devs, spec-heavy work, $100-200/month vs $500-1K Boris pattern), setup instructions (2 Claude instances with distinct roles: Claude Zero planner/reviewer never touches code, Claude One implementer executes approved plans), complete 5-phase workflow (planning with interview-based requirements clarification → human review checkpoint → implementation → verification by planner → archive), Plans/ directory structure (Review/Active/Completed as Kanban-style workflow), comparison table Boris horizontal scaling vs Jon vertical separation (8 dimensions: scaling axis, primary goal, monthly cost, entry barrier, audience, context pollution, accountability, tooling, coordination, best for), cost analysis (2 instances sequential vs 1 instance with correction loops, breakeven at ≥2 corrections), agent-ready plan best practices (file paths + line numbers reduce implementation time), limitations and tips (when not to use, overhead management), see also links
  - **New workflow file: dual-instance-planning.md** (`guide/workflows/dual-instance-planning.md`, ~750 lines) — Complete workflow guide with TL;DR, when-to-use checklist, detailed setup (directory structure, role enforcement in first messages), 5-phase workflow with concrete JWT authentication example (~500 lines showing plan structure, human approval, implementation, verification, archival), ready-to-use plan template (Summary, Requirements Clarified, Files to Create with line numbers, Files to Modify with before/after, Implementation Steps, Success Criteria, Security Checklist, Risks & Mitigation, Questions for Implementer, Estimated Effort Breakdown), cost analysis breakdown (simple/medium/complex features, monthly budget estimates for light/moderate/heavy users, breakeven calculations), tips and troubleshooting (role enforcement via CLAUDE.md, context pollution prevention, plan drift solutions, bash aliases for directory movement automation)
  - **Resource evaluation** (`docs/resource-evaluations/jon-williams-dual-instance-pattern.md`, ~300 lines) — Scored 4/5 (High Value, initially 2-3/5 corrected after technical-writer challenge), fact-check 100% (10 claims verified: author role/date, transition context, model used, workflow steps, directory structure, all verified via primary LinkedIn source), challenge results documented (score underestimation due to LinkedIn origin bias, gap identification for vertical vs horizontal scaling, audience gap for $100-200/month budget, pattern recognition of two-phase commit engineering principle, cost analysis gap filled), risk assessment if not integrated (80% probability audience gap, 90% probability pattern missing, quantified impact), lessons learned (don't undervalue practitioner sources, pattern orthogonality matters, challenge agents catch bias)
  - **Machine-readable index** (`reference.yaml`, +15 entries) — Added: dual_instance_planning (12884), dual_instance_workflow, dual_instance_overview, dual_instance_setup, dual_instance_complete_workflow, dual_instance_plan_template, dual_instance_cost_analysis, dual_instance_comparison (13074 Boris vs Jon table), dual_instance_source (LinkedIn URL), dual_instance_author (Jon Williams Product Designer UK), dual_instance_date (2026-02-03), dual_instance_pattern (vertical separation description), dual_instance_cost ($100-200/month), dual_instance_audience (solo devs spec-heavy quality over speed); Updated: resource_evaluations_count (46→47)
  - **References updated**: `guide/workflows/plan-driven.md` See Also section (+1 link to dual-instance-planning.md with description "Advanced: Use two Claude instances planner + implementer for quality-focused workflows"), `README.md` evaluation count harmonized (46/45/44 inconsistencies → 47 across 4 locations)
  - **Gap filled**: Vertical separation (planner ↔ implementer) pattern — 0% documented, only Boris horizontal scaling (5-15 parallel instances) → 100% comprehensive with workflow/template/cost analysis; Solo dev budget ($100-200/month) — underserved by $500-1K Boris pattern → complete alternative with lower entry barrier; Agent-ready plan structure — implicit in /plan mode → explicit best practice teaching (file paths, line numbers, acceptance criteria); Human-in-the-loop persistent planning approval — single /plan approval → persistent review checkpoint workflow (Review/Active/Completed directories); Cost analysis 2 instances vs correction loops — not documented → breakeven calculations, monthly budget estimates, decision criteria
  - **Impact**: Audience expansion (solo devs, product designers, spec-heavy workflows now served), Cost accessibility (lower barrier $100-200 vs $500-1K enables adoption), Quality improvement (separation of concerns reduces implementation errors via two-phase commit pattern), Pattern complementarity (vertical + horizontal scaling strategies documented, not competing choices), Practical tooling (bash aliases, directory structure, plan template ready to use)
  - **Source**: [Jon Williams LinkedIn post](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) (Product Designer UK, Feb 3 2026, transition from Cursor 6 months to Claude Code with Opus 4.5)
  - **Credits**: Jon Williams (pattern practitioner), technical-writer agent (challenge phase: 2-3/5 → 4/5 score revision, identified undervaluation due to source bias, gap analysis for vertical separation, audience gap quantification, engineering pattern recognition two-phase commit), fact-check validation (100% verified via primary source)


- **Git MCP Server (Official) Documentation** — Integration of Anthropic's official Git MCP server addressing version control automation gap (~1600 words, scored 5/5 CRITICAL after technical-writer challenge)
  - **New section: Version Control (Official Servers)** (`guide/ecosystem/mcp-servers-ecosystem.md:102-255`) — Comprehensive documentation covering official Git MCP server (12 tools: git_status, git_log, git_diff, git_commit, git_add, git_reset, git_branch, git_create_branch, git_checkout, git_show, git_diff_unstaged, git_diff_staged), 3 installation methods (uvx one-liner, pip, Docker), multi-repo configuration, advanced log filtering (ISO 8601, relative dates "2 weeks ago", absolute dates), context_lines parameter for token efficiency, IDE integrations (Claude Desktop, VS Code, Zed, Zencoder with one-click install buttons), quality score 8.5/10, limitations & workarounds (early development API changes, no interactive rebase/reflog/bisect)
  - **Decision Matrix: Git MCP vs GitHub MCP vs Bash Tool** (`guide/ecosystem/mcp-servers-ecosystem.md:212-255`) — Comprehensive comparison table (11 operations: local commits, branch management, diff/log analysis, PR creation, issue management, CI/CD checks, interactive rebase, reflog recovery, git bisect, multi-tool pipelines), decision tree workflow, 7 workflow examples with justifications (feature development, commit history analysis, code review preparation, cleanup commits, recover lost commits, bug hunting, automated release flow)
  - **Machine-readable index** (`reference.yaml`, +11 entries) — Added: git_mcp (description), git_mcp_guide (line pointer), git_mcp_tools (12 tools list), git_mcp_install (uvx command), git_mcp_decision_matrix (line pointer), git_mcp_repo (GitHub URL), git_mcp_score (8.5/10), git_mcp_status (early development), git_mcp_advanced_filtering (date formats), git_mcp_use_cases (5 use cases); Updated: reference.yaml updated timestamp (2026-02-03)
  - **Gap filled**: Official Git server documentation — mentioned in official servers table (line 29) but 0% documented → 100% comprehensive with use cases/config/decision matrix; Git vs GitHub vs Bash tool clarity — confusion not addressed → decision tree + comparison table + 7 workflow examples; Multi-repo workflows — not documented → configuration example with multiple instances; Token efficiency strategies — general advice → specific git_diff context_lines parameter, structured output benefits quantified
  - **Impact**: Workflow automation (AI-assisted commits, branch creation, log analysis without Bash tool), Token efficiency (structured output, context_lines control vs parsing text), Cross-platform safety (MCP vs direct Bash Git commands), Multi-tool composition (Git MCP + GitHub MCP pipelines documented), Developer experience (decision tree prevents tool selection confusion)
  - **Source**: [Official Git MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git) (MIT License, 77,908+ stars parent repo), Anthropic MCP ecosystem
  - **Credits**: Anthropic (official server), technical-writer agent (challenge phase: 3/5 → 5/5 score revision, placement critique, decision matrix requirement), fact-check validation (100% verified: 12 tools, installation methods, date filtering, IDE integrations, early development status, MIT license)

### Fixed

- **Ctrl+R Keybinding Documentation** — Corrected incorrect "Retry" label to accurate "Search command history" in 5 locations
  - **Guide corrections** (`guide/cheatsheet.md:39`, `guide/ultimate-guide.md:358,15508,15521,16032`) — Updated from "Retry last operation"/"Retry last"/"Retry" to "Search command history"/"Search history"/"Search" reflecting official `history:search` action (Global context) and `historySearch:next` (HistorySearch context)
  - **Verification method** — Tested against official keybindings documentation (`~/.claude/keybindings.json` schema) and CLI behavior confirmation
  - **Resource evaluation** (`docs/resource-evaluations/sankalp-claude-code-experience.md`) — Sankalp's blog (Dec 27, 2025) correctly identified guide error, scored 2/5 (marginal overlap but accurate Ctrl+R identification), evaluation documents correction workflow + CLI test results
  - **Impact** — Users now have accurate keybinding documentation matching actual behavior (search command history similar to shell Ctrl+R reverse-i-search)
  - **Credits** — Sankalp (@dejavucoder) for identifying error in [blog post](https://sankalp.bearblog.dev/my-experience-with-claude-code-20-and-how-to-get-better-at-using-coding-agents/), verification via official keybindings schema

## [3.21.1] - 2026-02-02

### Added

- **Native Sandboxing Comprehensive Documentation** — Integration of official Anthropic sandboxing documentation (v2.1.0+) addressing critical security gap (~1800 words missing content, scored 5/5 CRITICAL)
  - **New guide: sandbox-native.md** (`guide/security/sandbox-native.md`, ~3000 lines) — Complete technical reference covering OS primitives (Seatbelt for macOS, bubblewrap for Linux/WSL2), filesystem isolation (read all/write CWD), network isolation (SOCKS5 proxy with domain filtering), sandbox modes (Auto-allow vs Regular permissions), escape hatch (`dangerouslyDisableSandbox`), security limitations (domain fronting, Unix sockets privilege escalation, filesystem permission escalation), open-source runtime (`@anthropic-ai/sandbox-runtime`), platform support (macOS ✅, Linux ✅, WSL2 ✅, WSL1 ❌, Windows planned), decision tree (Native vs Docker vs Cloud), configuration examples (Strict/Balanced/Development), best practices, troubleshooting
  - **Enhanced: sandbox-isolation.md** (`guide/security/sandbox-isolation.md`, +800 lines) — Added Section 4 "Native Claude Code Sandbox" with architecture diagram, OS primitives comparison, quick start guide, configuration example, Native vs Docker decision tree, security limitations summary, deep dive reference; Updated TL;DR table (Native CC repositioned #2 with enriched details); Updated Comparison Matrix (Native CC enriched with kernel isolation, overhead, setup details); Sections renumbered (4→5 Cloud Sandboxes, 5→6 Comparison Matrix, 6→7 Safe Autonomy, 7→8 Anti-Patterns)
  - **Enhanced: architecture.md** (`guide/core/architecture.md:523`, +80 lines) — Added Section 5.1 "Native Sandbox (v2.1.0+)" in Permission & Security Model with architecture diagram (sandbox wrapper flow), OS primitives table, isolation model (filesystem/network/process), sandbox modes, security trade-offs table (Native vs Docker), security limitations, when-to-use guide, deep dive reference
  - **Resource evaluation** (`docs/resource-evaluations/native-sandbox-official-docs.md`, ~600 lines) — Scored 5/5 (CRITICAL), official Anthropic documentation, gap analysis quantified (~1800 words missing), fact-check 100% (11 claims verified), technical-writer agent challenge (3/5 → 5/5 score revision), risks of non-integration documented (security incidents, adoption friction, configuration errors)
  - **Production templates** (3 files):
    - `examples/config/sandbox-native.json` — Native sandbox configuration (denylist mode, domain allowlist, denied credentials paths, excluded commands)
    - `examples/commands/sandbox-status.md` — `/sandbox-status` command for sandbox inspection (platform check, config display, recent violations, open-source runtime)
    - `examples/hooks/bash/sandbox-validation.sh` — PreToolUse hook for production sandbox validation (strict mode, platform-specific checks, exit 2 blocking)
  - **Machine-readable index** (`reference.yaml`, +24 entries) — Added: sandbox_native_guide, sandbox_native_why, sandbox_native_os_primitives, sandbox_native_filesystem, sandbox_native_network, sandbox_native_modes, sandbox_native_escape_hatch, sandbox_native_security_limits, sandbox_native_opensource, sandbox_native_platforms, sandbox_native_decision_tree, sandbox_native_config_examples, sandbox_native_best_practices, sandbox_native_troubleshooting, sandbox_runtime_oss, sandbox_runtime_npm, sandbox_official_docs, sandbox_comparison_native_docker, sandbox_native_evaluation, sandbox_native_score, sandbox_native_config_template, sandbox_status_command, sandbox_validation_hook; Updated: sandbox_safe_autonomy (320→486), sandbox_anti_patterns (372→538), sandbox_comparison_matrix (306→469)
  - **Gap filled**: Native sandbox technical details (OS primitives, network proxy, security limitations) — 0% documented → 100% comprehensive; Trade-off Docker microVM vs Native process-level — not quantified → detailed comparison matrix; Open-source runtime — 0% mentioned → complete walkthrough with GitHub/npm links; Platform incompatibility (WSL1, Windows) — not documented → explicit status + migration guidance
  - **Impact**: Security (domain fronting/Unix sockets/filesystem attacks documented with mitigations), Production readiness (templates enable safe autonomous workflows), Developer experience (decision tree helps choose Native vs Docker vs Cloud), Community (open-source runtime enables audits/contributions)
  - **Source**: [Official Anthropic Documentation](https://code.claude.com/docs/en/sandboxing), [Open-source runtime](https://github.com/anthropic-experimental/sandbox-runtime), Claude Code v2.1.0+ feature
  - **Credits**: Anthropic (official documentation), technical-writer agent (challenge phase identified under-scoring), fact-check validation (100% verified claims)

## [3.21.0] - 2026-02-02

### Added

- **Configuration Management & Backup** — Two major new sections addressing critical gap in Claude Code configuration strategy (1,591 lines added, 3 templates, 22 reference entries)
  - **Section 3.2.1 "Version Control & Backup"** (`guide/ultimate-guide.md:4085`) — 611 lines covering configuration hierarchy (global → project → local), Git strategies for both project `.claude/` and global `~/.claude/`, backup strategies comparison (Git remote, cloud sync, cron, third-party tools), multi-machine sync workflows (Git, cloud storage, hybrid), security considerations, disaster recovery procedures, community solutions (brianlovin/claude-config + Martin Ratinaud approach)
  - **Documented `.claude/settings.local.json`** — Previously undocumented feature for machine-specific overrides (gitignored) now explained with hierarchy precedence rules and use cases
  - **Section 8.3.1 "MCP Secrets Management"** (`guide/ultimate-guide.md:8113`) — 293 lines covering security principles, three practical approaches (OS Keychain with encryption at rest, .env + .gitignore with template substitution, Secret Vaults for enterprise), secrets rotation workflow, pre-commit detection hook, verification checklist, best practices summary
  - **Template: sync-claude-config.sh** (`examples/scripts/sync-claude-config.sh`) — 350-line automation script with 5 commands (setup, sync, backup, restore, validate), .env parsing + envsubst for variable substitution, Git repo creation with symlinks, validation checks (secrets not in Git, file permissions), optional cloud backup support
  - **Template: pre-commit-secrets.sh** (`examples/hooks/bash/pre-commit-secrets.sh`) — 163-line Git hook detecting 10+ secret patterns (OpenAI, GitHub, AWS, Anthropic, JWT, etc.), whitelist system for false positives, skip files (*.md, *example*, *template*), clear error messages with remediation steps, blocks commits if secrets detected
  - **Template: settings.local.json.example** (`examples/config/settings.local.json.example`) — 145-line template for machine-specific overrides with examples (skip expensive checks on laptop, local MCP endpoints, personal permissions, machine-specific hooks)
  - **Resource Evaluation: Martin Ratinaud Configuration Management** (`docs/resource-evaluations/ratinaud-config-management-evaluation.md`) — Scored 5/5 (CRITICAL), 294-line evaluation with content summary, comparative analysis, 3× Perplexity fact-checks, technical-writer agent challenge, integration plan. Source: [LinkedIn post](https://www.linkedin.com/posts/martinratinaud_claudecode-devtools-buildinpublic-activity-7424055660247629824-hBsL) by Martin Ratinaud (11 years experience, "Claude Code Max Addict", 504 sessions validation)
  - **Community Validation**: GitHub Issue [#16204](https://github.com/anthropics/claude-code/issues/16204) "Proactive migration guidance for backup/restore workflows", brianlovin/claude-config repo with sync.sh script, claudebot backup tool (third-party)
  - **Machine-readable index**: 22 new entries in `reference.yaml` (config_hierarchy, config_git_strategy_project, config_git_strategy_global, config_backup_strategies, config_multi_machine_sync, config_security_considerations, config_disaster_recovery, config_community_solutions, config_github_issue, config_brianlovin_repo, config_ratinaud_approach, config_ratinaud_evaluation, mcp_secrets_management, mcp_secrets_principles, mcp_secrets_os_keychain, mcp_secrets_env_file, mcp_secrets_vaults, mcp_secrets_rotation, mcp_secrets_pre_commit, mcp_secrets_verification, mcp_secrets_best_practices, sync_claude_config_script, pre_commit_secrets_hook, settings_local_example)
  - **Gap filled**: Version control strategy for `~/.claude/` (previously undocumented), MCP secrets storage workflows (theory → practice), multi-machine sync (project-level documented, global-level missing), disaster recovery procedures (0 → complete coverage), team onboarding for `~/.claude/` setup
  - **Impact**: Security (pre-commit hook prevents secret leaks), Productivity (multi-machine sync saves 80% reconfiguration time), Team coordination (onboarding workflow for consistent setup), Disaster recovery (backup strategies protect against config loss)
  - **Credits**: Martin Ratinaud (504 sessions, symlinks approach), brianlovin/claude-config (community sync.sh example), GitHub community (Issue #16204 request), Perplexity (3× fact-check searches validating gap and community demand)
- **Resource Evaluation: Alan Engineering "Tour Eiffel Paradigm"** (scored 5/5, CRITICAL) — Integration of paradigm shift framework from Alan Engineering team (Charles Gorintin, CTO + Maxime Le Bras, Talent Lead) validating production-scale AI transformation (`docs/resource-evaluations/alan-tour-eiffel-paradigm.md`)
  - **Source**: LinkedIn Newsletter "Intelligence Humaine" (Feb 2, 2026, 3,897 followers), French healthtech company (15K+ companies, 300K+ members, €500M raised, heavily regulated industry)
  - **Key frameworks**: (1) Eiffel Tower Principle — AI tools transform what's architecturally possible (like elevators enabled Eiffel Tower shape), not just acceleration, (2) Ralph Wiggum Programming — agentic loops where engineers become architects/editors, (3) **Verification Paradox** — 99% AI success makes human vigilance fragile for 1% errors, need automated guardrails, (4) Precision as Currency — clear spec definition (WHAT/WHERE/HOW) is new engineer superpower, (5) Ambition Scaling — pursue previously impossible goals enabled by tools
  - **Production Safety Rule 7** added (`guide/security/production-safety.md:639-791`): "The Verification Paradox" — when AI reliability crosses 95%, shift from manual review to automated guardrails (tests, types, lints, CI/CD gates). Anti-patterns vs Better Approaches table, 3 implementation options (automated stack, verification contracts, pre-merge checklist), integration with Rules 2/3/6
  - **Practitioner Insight** added (`guide/ecosystem/ai-ecosystem.md:2133-2168`): Alan Engineering section after Addy Osmani, following existing format (credentials, content summary, alignment table with guide references, production-scale context). Interview mention of Stanislas Polu (Dust co-founder) citing Mirakl achievement (75% employees → agent builders)
  - **Machine-readable index** updated (`reference.yaml`): Added `practitioner_alan`, `practitioner_alan_source`, `verification_paradox`, `verification_paradox_source` entries
  - **README.md counters harmonized**: Fixed evaluation count inconsistencies (37/35/38 → 41 across 5 locations: line 18 intro, line 74 mermaid diagram, line 118 structure, line 163 features, line 427 details)
  - **Challenge phase**: Technical-writer agent reviewed 6 proposed integrations, rejected 4 (Quick Start paradigm shift, Mental Model refactoring, methodologies.md deep dive, XML Prompting precision) for dilution/duplication concerns, approved 3 (production-safety, ai-ecosystem, reference.yaml)
  - **Language note**: Original article in French, concepts and Henri Bergson quote ("L'intelligence est la faculté de fabriquer des outils à faire des outils") translated for guide
- **Multi-IDE Configuration Sync Pattern** — Documented strategies for maintaining consistent AI instructions across multiple coding tools (Claude Code, Cursor, Copilot) in `guide/ecosystem/ai-ecosystem.md:1256-1329`
  - **Problem statement**: Table comparing config files (CLAUDE.md, .cursorrules, AGENTS.md, .github/copilot-instructions.md) — without sync, each drifts independently causing inconsistent AI behavior
  - **Solution 1**: Native @import (recommended for Claude Code solo usage) — no build step, maintained by Anthropic, but Cursor doesn't support it
  - **Solution 2**: Script-based generation for multi-IDE teams — source of truth in `docs/ai-instructions/` compiled into tool-specific configs via bash/node sync scripts
  - **AGENTS.md Support Status**: Clarified Claude Code does NOT natively support AGENTS.md ([GitHub issue #6235](https://github.com/anthropics/claude-code/issues/6235), 171 comments, open as of Feb 2026) — workaround via symlink documented
  - **Compatibility matrix**: AGENTS.md standard supported by Cursor, Windsurf, Cline, GitHub Copilot (see [AI Coding Agents Matrix](https://coding-agents-matrix.dev))
  - **Machine-readable index**: Added `ai_ecosystem_multi_ide_sync` and `agents_md_support_status` entries to `reference.yaml`
- **Resource Evaluation: Addy Osmani LinkedIn Post** (scored 2/5, Marginal - Tracking mention only) — Post about Anthropic study (17% comprehension gap) evaluated but not integrated due to 100% overlap with primary source already documented (`docs/resource-evaluations/addy-osmani-linkedin-anthropic-study.md`)
  - **Content**: LinkedIn post (Feb 1, 2026, 246K reach) citing Shen & Tamkin 2026 study on AI-assisted learning
  - **Key claims verified**: 17% comprehension gap, 2-minute productivity gain, "thinking partner vs code vending machine" framing
  - **Overlap**: 100% with arXiv:2601.20245 already cited 3× in `guide/roles/learning-with-ai.md` (lines 114, 868, 890)
  - **Decision**: Minimal integration (1-2 line tracking mention) to document mainstream diffusion timeline without content duplication
  - **Challenge phase**: Technical-writer agent confirmed score 2/5 content but noted 3/5 ecosystem context (authority messager + diffusion milestone)
  - **New criterion documented**: "Influencer Amplification" pattern for future evaluations (reach >100K + timeline awareness)
- **Resource Evaluation: "Beyond Vibe Coding" Book** (scored 3/5, Pertinent - Minimal integration) — Comprehensive O'Reilly book by Addy Osmani evaluated for 90%+ overlap with existing guide content (`docs/resource-evaluations/beyond-vibe-coding.md`)
  - **Content**: 6-chapter book (Intro/Principles/Advanced Techniques/CLI Agents/Production/Future Trends) published 2025, paid format ($B0F6S5425Y Amazon), freemium web content at beyond.addy.ie
  - **Key frameworks**: The 70% Problem (AI accelerates 70%, final 30% needs rigor), Context Engineering as RAM metaphor, Critique-Driven Development, MCP as "USB-C for AI", Multi-Agent Orchestration
  - **Overlap analysis**: 14 aspects compared — 10/14 already covered 100% (Vibe Coding, Context Engineering, MCP, Multi-Agent, Plan Mode, TDD, Spec-First, Visual Context, Production Safety)
  - **Gap identified**: Critique-Driven Development framework not explicitly documented (conceptually covered via code review workflows), Few-Shot Prompting technique, Cost-Benefit Analysis Framework
  - **Cross-validation**: Osmani's "80% Problem" article already evaluated 3/5 (ai-ecosystem.md:2024), "Good Spec" article already integrated 4/5 (workflows/spec-first.md)
  - **Decision**: Tracking mention (3-5 lines in ai-ecosystem.md:2024) + cross-ref citations (1-2 lines in 4-5 overlapping sections) + "Context as RAM" metaphor note (methodologies.md:192)
  - **Rationale**: Book = external validation/synthesis, but guide already more comprehensive (11K lines vs paid book). Rejected full integration (paid resource, 90% duplication, 2 Osmani articles already integrated)

## [3.20.8] - 2026-02-01

### Updated

- **RTK (Rust Token Killer) Evaluation** — Major update from v0.2.0 to v0.7.0 (score upgraded from 4/5 to 4.5/5, +0.43 points) (`docs/resource-evaluations/rtk-evaluation.md`)
  - **All critical gaps resolved**: pnpm support (v0.6.0), npm/vitest (v0.6.0), git arg parsing bug fixed (v0.7.0), grep/ls broken commands fixed (v0.7.0), GitHub CLI support (v0.6.0), Cargo commands (v0.6.0), analytics system (`rtk gain` v0.4.0, `rtk discover` v0.7.0), auto-rewrite hook for Claude Code PreToolUse (v0.7.0)
  - **Evolution**: 5 major releases in 9 days (2026-01-23 → 2026-02-01) with 10+ community PRs merged (FlorianBruniaux contributions integrated upstream)
  - **Architecture maturity**: 24 command modules (was 12), 9 filtering strategies (50-99% reduction), SQLite token tracking (`~/.local/share/rtk/history.db`), configuration system (`~/.config/rtk/config.toml`), ARCHITECTURE.md documentation
  - **Community growth**: 17 stars (+113% from 8), 2 forks (+200% from 0), 1 open issue, 2+ contributors (active development)
  - **Score breakdown**: Accuracy +1 (3→4, bugs fixed), Comprehensiveness +1 (4→5, full stack coverage), Production Readiness +1 (3→4, architecture docs), Community +1 (2→3, growth trajectory)
  - **Token reduction**: 72.6% (git only, v0.2.0) → 89.4% (full stack estimate, v0.7.0) with 85% command coverage (was 40%)
  - **Recommendation updated**: "GOOD (4/5) - git-only, bugs, experimental" → "EXCELLENT (4.5/5) - production-ready for early adopters, full modern dev stack (git, pnpm, npm, cargo, gh)"
  - **Fork status**: Fork (FlorianBruniaux/rtk) no longer needed — all features merged upstream, use `pszymkowiak/rtk` v0.7.0 directly

## [3.20.7] - 2026-02-01

### Added

- **Addy Osmani Spec-Writing Evaluation** (scored 4/5, High Value) — Integration of ["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/) by Addy Osmani (former Head of Chrome Developer Experience at Google, 14 years Chrome team, O'Reilly author)
  - **Resource evaluation**: Systematic 5-point assessment with fact-checking (Perplexity verified credentials, all claims sourced) and technical-writer agent challenge phase (corrected initial 3/5 → 4/5 score) (`docs/resource-evaluations/addy-osmani-good-spec.md`)
  - **Gaps filled**: Modular prompts strategy, operational boundaries framework (Always/Ask First/Never), command spec templates, anti-pattern documentation for monolithic CLAUDE.md
  - **Integration priority**: High (within 1 week) — addresses daily user pain points (context pollution, spec clarity, operational decision-making)
- **Spec-First Workflow: 4 New Sections** (~180 lines added to `guide/workflows/spec-first.md`, 327 → 507 lines total)
  - **"Modular Spec Design"** (line 322): Pattern for splitting large CLAUDE.md files into focused domain files (CLAUDE-auth.md, CLAUDE-api.md, etc.). When to split (>200 lines threshold), 3 split strategies (feature-based, role-based, workflow-based), implementation pattern with @file references
  - **"Operational Boundaries"** (line 372): Three-tier boundary system (Always/Ask First/Never) mapped to Claude Code permission modes (auto-accept/default/plan mode). Decision framework table, API development example, quarterly review guidelines
  - **"Command Spec Template"** (line 432): Template for executable command specifications (testing, build, deployment, database commands) with expected outputs and error handling. Examples: `pnpm test`, `pnpm build`, `pnpm db:migrate` with safety checks
  - **"Anti-Pattern: Monolithic CLAUDE.md"** (line 472): Explains cognitive load problem (>200 lines = context pollution), real-world before/after example (387 lines → 7 focused files, 61% context reduction), migration checklist
- **Reference Index**: 8 new entries in `machine-readable/reference.yaml` (spec_first_workflow, spec_modular_design, spec_operational_boundaries, spec_command_template, spec_anti_monolithic, spec_osmani_source, spec_osmani_evaluation, spec_osmani_score)
- **README.md**: Incremented resource evaluations count (35 → 36 assessments)
- **Fresh Context Pattern**: New "Session-per-Concern Pipeline" variant — dedicates a fresh session to each quality dimension (plan → test → implement → security review → perf → code review) instead of looping the same task. References OpusPlan and TDD. (`guide/ultimate-guide.md:1595`)
- **Resource Evaluation #19: dclaude** (Patrick Debois) — Dockerized Claude Code wrapper evaluated at 2/5 (Marginal). Fills a narrow gap (Linux + Docker Engine without Docker Desktop) but uses standard containers with host Docker socket mount — weaker isolation than Docker Sandboxes' microVMs. Footnote added in `guide/security/sandbox-isolation.md` Limitations subsection. (`docs/resource-evaluations/dclaude-docker-wrapper.md`)
- **Resource Evaluation #20: 10 Tips from Inside the Claude Code Team** (paddo.dev / Boris Cherny thread) — Scored 4/5 (High Value). 4 integrations in ultimate-guide.md:
  - **Prompting as Provocation** (section 2.6.1): 3 challenge patterns — Gatekeeper, Proof Demand, Reset — treating Claude as a peer to convince rather than an assistant to direct (`guide/ultimate-guide.md:3029`)
  - **Model-as-Security-Gate** hook pattern: Route permission requests to Opus 4.5 via PreToolUse hook for intelligent security screening beyond static rules (`guide/ultimate-guide.md:6907`)
  - **Boris Cherny team patterns**: Skills as institutional knowledge (/techdebt, context dumps, BigQuery agents), CLI-over-MCP rationale, re-plan when stuck, Claude writes its own rules (`guide/ultimate-guide.md:11822`)
  - **Worktree shell aliases**: za/zb/zc navigation + dedicated analysis worktree tip (`guide/ultimate-guide.md:10717`)

## [3.20.6] - 2026-02-01

### Added

- **agentskills.io Open Standard integration** (scored 4/5) — Agent Skills follow the [agentskills.io](https://agentskills.io) specification, created by Anthropic, supported by 26+ platforms (Cursor, VS Code, GitHub, Codex, Gemini CLI, Goose, Roo Code, etc.)
  - SKILL.md frontmatter table now distinguishes spec fields (`name`, `description`, `allowed-tools`, `license`, `compatibility`, `metadata`) from Claude Code-only extensions (`context`, `agent`) (`guide/ultimate-guide.md:5180`)
  - `skills-ref validate` / `skills-ref to-prompt` CLI tool added to skill creation workflow (`guide/ultimate-guide.md:5188`)
  - Skill Portability section in Goose comparison (`guide/ecosystem/ai-ecosystem.md:1876`)
  - 16 new reference.yaml entries (spec, CLI, anthropics/skills repo, SafeDep threat model, blog)
- **Agent Skills Supply Chain Risks** — New section 1.2 in security-hardening.md based on SafeDep threat model (8-14% of public skills have vulnerabilities). 4 mitigations: review SKILL.md, validate with skills-ref, pin versions, audit scripts/ (`guide/security/security-hardening.md:121`)
- **anthropics/skills** (60K+⭐) added to README Complementary Resources table
- **Resource Evaluations**: Skill Doctor GitHub Action (2/5, marginal), agentskills.io specification (4/5, high value) (`docs/resource-evaluations/skill-doctor-github-action.md`, `docs/resource-evaluations/agentskills-io-specification.md`)

## [3.20.5] - 2026-01-31

### Added

- **Visual Reference**: 4 new high-value ASCII diagrams (16 → 20 total)
  - **#17 TDD Red-Green-Refactor Cycle** — Cyclic loop showing the iterative nature of TDD
  - **#18 UVAL Protocol Flow** — 4-step learning framework (Understand → Verify → Apply → Learn) with failure backtrack paths
  - **#19 Security 3-Layer Defense** — Prevention/Detection/Response overview with adoption path by team size
  - **#20 Secret Exposure Timeline** — Emergency response actions by time window (15min/1h/24h) with severity guide
- **README.md**: Added Visual Reference to Core Documentation table

## [3.20.4] - 2026-01-31

### Added

- **30 New Quiz Questions** (227 → 257 total) across 11 categories
  - **Advanced Patterns** (+8): Mechanic Stacking, Permutation Frameworks, "You Are the Main Thread", Task Lists as Diagnostic, Anti-hallucination occurrence rule, Multi-Agent PR Review, Comprehension Debt, CLAUDE.md compounding memory
  - **MCP Servers** (+3): MCP Apps (SEP-1865), `auto:N` lazy loading, Semgrep top score (9.0/10)
  - **Architecture** (+3): Tasks API (replaces TodoWrite), Tasks API N+1 overhead, TeammateTool experimental status
  - **Reference** (+3): `--from-pr` flag, `$ARGUMENTS` bracket syntax breaking change, Myths vs Reality
  - **Hooks** (+2): Async hook `async: true` config, async hook limitations
  - **Learning with AI** (+2): Addy Osmani's 80% Problem failure modes, vibe coding context overload symptoms
  - **Security** (+2): Docker sandbox isolation, GitHub Issue Auto-Creation Bug (#13797)
  - **AI Ecosystem** (+3): LM Studio bridge cost savings, external orchestrators (Gas Town/multiclaude/agent-chat), skeleton project audit areas
  - **Memory & Settings** (+2): 8 verification domains, Fresh Context Pattern
  - **Agents** (+1): AGENTS.md vs Skills invocation reliability (100% vs 53-79%)
  - **Privacy** (+1): Co-Authored-By vs Assisted-By traceability
  - Difficulty distribution: 4 junior, 4 intermediate, 14 senior, 8 power
  - Also fixed pre-existing "14 categories" → "15 categories" in landing quiz page

### Changed

- **README.md**: Quiz badge updated (227 → 257), quiz section updated
- **Landing site**: All quiz counts updated (index.html, quiz/index.html, learning/index.html, CLAUDE.md)

## [3.20.3] - 2026-01-31

### Added

- **Competitive Analysis: 9 Gaps Filled from claudelog.com** — Systematic veille against claudelog.com (313 pages, InventorBlack/r/ClaudeAI)
  - **Section 9.19: Permutation Frameworks** (~180 lines, `guide/ultimate-guide.md`)
    - CLAUDE.md-driven systematic variation testing (define dimensions → generate variants → implement → evaluate)
    - Step-by-step implementation with practical API design example (REST vs GraphQL vs tRPC)
    - Anti-patterns table, integration with TDD/Plan Mode/Skeleton Projects
  - **Skeleton Projects Workflow** — `guide/workflows/skeleton-projects.md` (NEW, 208 lines)
    - 4-phase workflow: Find & Evaluate → Fork & Customize → Expand to MVP → Document
    - Sub-agent evaluation pattern for skeleton auditing (Security + Architecture + DX)
    - Expansion timeline (Day 1 → Week 1 → Month 1) with common pitfalls
  - **Task Lists as Diagnostic Tool** (~50 lines, `guide/ultimate-guide.md`)
    - Divergence patterns table: too broad, too narrow, wrong priorities, missing/extra tasks
    - Diagnostic workflow using TaskList as instruction clarity sanity check
  - **Rev the Engine** (~45 lines, `guide/ultimate-guide.md`)
    - Multi-round planning pattern (3 rounds: initial → challenge → finalize → execute)
    - Integrated after OpusPlan in Plan Mode section
  - **Mechanic Stacking** (~30 lines, `guide/ultimate-guide.md`)
    - 5-layer intelligence stack: Plan Mode → Extended Thinking → Rev → Split-Role → Permutation
    - Decision matrix matching stack depth to decision impact (Low → Critical)
  - **Split-Role Sub-Agents** (~60 lines, `guide/ultimate-guide.md`)
    - Multi-perspective analysis pattern with custom agent YAML templates
    - Security Expert + Performance Analyst + UX/API Reviewer example
  - **"You Are the Main Thread" Mental Model** (~30 lines, `guide/ultimate-guide.md`)
    - CPU scheduler analogy: developer as orchestrator, Claude instances as worker threads
    - ASCII diagram with 4 practical implications
  - **Continuous Context Update** (~40 lines, `guide/ultimate-guide.md`)
    - Proactive CLAUDE.md enrichment during dev sessions (not just reactive error capture)
    - Discovery type → CLAUDE.md section mapping table
  - **Smart Hook Dispatching** (~80 lines, `guide/ultimate-guide.md`)
    - Single dispatcher routing events by file type and tool to specialized handlers
    - Handler directory structure with language-specific hooks (TypeScript, Python, Rust, SQL)
  - **Reference updates**: `machine-readable/reference.yaml` (+17 entries)
    - `permutation_frameworks`, `rev_the_engine`, `mechanic_stacking`, `split_role_sub_agents`,
      `task_lists_diagnostic`, `main_thread_orchestrator`, `continuous_context_update`,
      `smart_hook_dispatching`, `skeleton_projects_workflow`
  - **Workflows README**: Updated `guide/workflows/README.md` with Skeleton Projects entry + Quick Selection Guide

### Changed

- **README.md**: Guide line count updated (15K → 16K), version bumped to 3.20.3
- **Guide line count**: 15,771 → 16,293 (+522 lines)

---

- **Sandbox Isolation for Coding Agents** — `guide/security/sandbox-isolation.md` (NEW), `machine-readable/reference.yaml`, `guide/ultimate-guide.md`
  - Score: 4/5 (High Value — official Docker docs + verified vendor documentation)
  - Source: [docs.docker.com/ai/sandboxes/](https://docs.docker.com/ai/sandboxes/) (Docker Desktop 4.58+, Jan 2026)
  - New guide file: Docker Sandboxes (microVM isolation, network policies, custom templates, supported agents)
  - Alternatives landscape: Fly.io Sprites, Cloudflare Sandbox SDK, E2B, Vercel Sandboxes, native CC sandbox
  - Comparison matrix (6 solutions, 7 criteria) + decision tree (Mermaid flowchart)
  - Safe autonomy workflows: Docker Sandbox + `--dangerously-skip-permissions` pattern, CI/CD sketch
  - Anti-patterns table (6 entries)
  - Cross-reference added after `--dangerously-skip-permissions` warning (ultimate-guide.md:3953)
  - 18 new `sandbox_*` entries in reference.yaml
  - Evaluation: `docs/resource-evaluations/docker-sandboxes-isolation.md`

- **Claude Code releases tracking: v2.1.27** — `machine-readable/claude-code-releases.yaml`, `guide/core/claude-code-releases.md`
  - `--from-pr` flag to resume sessions linked to GitHub PR number/URL
  - Sessions auto-linked to PRs when created via `gh pr create`
  - Context management fixes for Bedrock/Vertex gateway users
  - Landing synced: banner + timeline card in index.html

- **Contribution Metrics (Anthropic blog, Jan 29 2026)** — `guide/ultimate-guide.md`, `machine-readable/reference.yaml`
  - Score: 4/5 (High Value — official source with harder metrics superseding Aug 2025 data)
  - Source: [claude.com/blog/contribution-metrics](https://claude.com/blog/contribution-metrics)
  - New subsection after Anthropic Internal Study: +67% PRs merged/engineer/day, 70-90% AI-assisted code
  - Contribution Metrics dashboard: public beta, Team & Enterprise plans (GitHub integration)
  - Methodological note: PR-based measurement vs Aug 2025 self-reported surveys
  - ROI cross-reference added in cost optimization section
  - Evaluation: `docs/resource-evaluations/026-contribution-metrics-blog.md`

- **Learning guide: Shen & Tamkin RCT integration** — `guide/roles/learning-with-ai.md`
  - Source: [arXiv:2601.20245](https://arxiv.org/abs/2601.20245) (Shen & Tamkin, Anthropic Fellows, Jan 2026)
  - Score: 3/5 (Relevant - Useful complement, high overlap with existing content)
  - Added RCT data point in §3 "Reality of AI Productivity": 17% skill reduction (n=52, Cohen's d=0.738, p=0.01), no significant speed gain, only ~20% delegation users finished faster
  - Added new Red Flag: "Perception gap" — AI users rate tasks easier while scoring lower
  - Added full reference in §12 Sources (Academic Research) with 6 interaction patterns summary
  - Also added METR RCT (arXiv:2507.09089) in Productivity Research sources

## [3.20.1] - 2026-01-30

### Added

- **Resource Evaluation: Vercel AGENTS.md vs Skills Eval** — `docs/resource-evaluations/025-vercel-agents-md-vs-skills-eval.md`
  - Score: 3/5 (Pertinent — confirms existing CLAUDE.md architecture)
  - Source: [Jude Gao (Vercel), Jan 27 2026](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  - First quantified benchmark: eager context (AGENTS.md) 100% vs lazy invocation (skills) 53-79%
  - Key finding: skills auto-invoked only 56% of the time by coding agents
  - Compression benchmark: 40KB → 8KB docs index with zero performance loss
  - Double challenge: technical-writer + system-architect agents (unanimous 3/5)
  - Fact-check: 13/13 claims verified
  - Conflict of interest noted: Vercel operates both skills.sh and the AGENTS.md codemod

### Changed

- **CLAUDE.md sizing** (ultimate-guide.md:3527): Added Vercel 8KB compression benchmark as evidence for 4-8KB target
- **Memory Loading insight** (ultimate-guide.md:4082): Added warning about 56% skill invocation rate — critical instructions should use CLAUDE.md/rules, not skills
- **Skills trade-offs** (ultimate-guide.md:5652): Added invocation reliability caveat with source

## [3.20.0] - 2026-01-30

### Added

- **Code Review Automation: Multi-Agent PR Review** — Production-grade review patterns from Pat Cullen & Méthode Aristote
  - **Resource evaluation**: `docs/resource-evaluations/017-pat-cullen-final-review.md`
    - Score: 5/5 (Critical - Must integrate immediately)
    - Source: [Pat Cullen's Final Review Gist](https://gist.github.com/patyearone/c9a091b97e756f5ed361f7514d88ef0b) (Jan 28, 2026)
    - Multi-agent workflow with 3 specialized agents: Consistency Auditor, SOLID Analyst, Defensive Code Auditor
    - Anti-hallucination safeguards: pre-flight check (git log Co-Authored-By detection), verification protocol, occurrence rule
    - Production patterns: reconciliation step, severity classification (🔴🟡🟢), auto-fix convergence loop
    - Fact-checked: All claims verified, workflow production-ready (used regularly by author)
  - **Enhanced `/review-pr` command**: `examples/commands/review-pr.md` (+150 lines: 80 → 230)
    - Simple template PRESERVED (lines 1-80) for beginners
    - NEW "Advanced: Multi-Agent Review" section (line 81+)
    - Pre-flight check: `git log --oneline -10 | grep "Co-Authored-By: Claude"` to avoid repeating suggestions
    - Multi-agent specialization: 3 parallel agents (Consistency, SOLID, Defensive)
    - Anti-hallucination rules: verify patterns with Grep/Glob before recommending (occurrence rule: >10 = established)
    - Reconciliation: prioritize existing project patterns, skip with documented reasoning
    - Severity classification: 🔴 Must Fix (blockers) / 🟡 Should Fix / 🟢 Can Skip
    - Auto-fix loop: review → fix → re-review → converge (max 3 iterations)
    - Conditional context loading: stack-agnostic table (DB queries → check indexes, API routes → check auth, etc.)
  - **Enhanced `code-reviewer` agent**: `examples/agents/code-reviewer.md` (+219 lines: 72 → 291)
    - NEW "Anti-Hallucination Rules" section (line 75)
      - Verification protocol: Use Grep/Glob before claiming patterns exist
      - Occurrence rule: >10 occurrences = established, 3-10 = emerging, <3 = not established
      - Read full file context (not just diff lines)
      - Uncertainty markers: ❓ To verify / 💡 Consider / 🔴 Must fix
    - NEW "Conditional Context Loading" section
      - Detailed table: if diff contains X → load context Y → use tools Z
      - Stack-agnostic patterns (imports → check package.json, DB queries → check schema, etc.)
    - NEW "Defensive Code Audit" section
      - Silent catches detection: empty catch blocks, console-only catches
      - Hidden fallbacks detection: chained fallbacks (a || b || c), optional chaining with fallback
      - Unchecked nulls detection: property access without validation
      - Ignored promise rejections: async calls without .catch()
    - NEW "Severity Classification System" with justification requirements
    - Enhanced output format with evidence-based findings
    - Attribution: Méthode Aristote production code review patterns
  - **Enhanced iterative refinement workflow**: `guide/workflows/iterative-refinement.md` (+133 lines: 389 → 522)
    - NEW "Review Auto-Correction Loop" section (line 347)
    - Pattern: review → fix → re-review → converge (with visual diagram)
    - Safeguards: max iterations, quality gates (tsc/lint), protected files, change threshold, rollback capability
    - Example session: 3 iterations with 🔴 Must Fix → 🟡 Should Fix → 🟢 Can Skip convergence
    - Comparison: one-pass review vs convergence loop (when to use each)
    - Integration with multi-agent review
    - Convergence criteria: 5 conditions (no issues, max iterations, change threshold, quality gate failure, manual stop)
    - Anti-patterns table: infinite loop, scope creep, breaking fixes, protected file changes, context loss
  - **Enhanced ultimate guide**: `guide/ultimate-guide.md` (+28 lines, ~line 4623)
    - NEW "Production Example: Multi-Agent Code Review" after existing Code Review Prompt
    - 3 specialized agent roles: Consistency, SOLID, Defensive Code Auditor
    - Key patterns beyond generic Split Role: pre-flight check, anti-hallucination (Grep/Glob verification), reconciliation, severity classification, convergence loop
    - Production safeguards: full file context, conditional loading, protected files, quality gates
    - Attribution: Pat Cullen's Final Review Gist + implementation references
  - **Reference updates**: `machine-readable/reference.yaml` (+3 entries)
    - `review_pr_advanced: "examples/commands/review-pr.md:81"`
    - `review_anti_hallucination: "examples/agents/code-reviewer.md:75"`
    - `review_auto_fix_loop: "guide/workflows/iterative-refinement.md:347"`
  - **Impact**: Transforms basic `/review-pr` template into production-grade multi-agent system
    - Beginner-friendly: simple template preserved (lines 1-80)
    - Advanced users: comprehensive patterns for critical code review
    - Anti-hallucination safeguards prevent false suggestions
    - Defensive code audit catches silent failures (empty catches, hidden fallbacks, unchecked nulls)
    - Convergence loop ensures quality through iterative refinement
  - **Design principles**: Enrich existing files (no fragmentation), no breaking changes (review-pr.md not renamed), complete attribution (Pat Cullen + Méthode Aristote), audience-aware (simple → advanced progression)

## [3.19.0] - 2026-01-30

### Added

- **Practitioner Insight: Addy Osmani (Google Chrome Team)** — Added to AI Ecosystem Practitioner Insights
  - **New entry**: `guide/ecosystem/ai-ecosystem.md` line ~2024 "Addy Osmani (Google Chrome Team)" (~32 lines)
    - "The 80% Problem in Agentic Coding" synthesis (January 28, 2026)
    - Three new failure modes: overengineering, assumption propagation, sycophantic agreement
    - Comprehension debt concept (distinct from technical debt)
    - Productivity paradox data: +98% PRs, +91% review time, no workload reduction
    - Alignment table mapping Osmani concepts to existing guide sections
  - **Reference updates**: `machine-readable/reference.yaml` — 4 new entries
    - `practitioner_addy_osmani: "guide/ecosystem/ai-ecosystem.md:2024"`
    - `practitioner_osmani_source: "https://addyo.substack.com/p/the-80-problem-in-agentic-coding"`
    - `eighty_percent_problem`, `comprehension_debt_secondary`
  - **Resource evaluation**: `docs/resource-evaluations/024-addy-osmani-80-percent-problem.md`
    - Score: 3/5 (Pertinent) — Useful synthesis, but 90% overlap with existing content
    - Minimal integration approach (32 lines vs rejected 250 lines proposal)
    - Fact-check: 6 stats verified, 1 Stack Overflow stat found incorrect
    - Challenge by technical-writer agent validated downgrade from 4/5 to 3/5
    - Transparent note: "secondary synthesis, primary sources already documented"

- **Hook Execution Model Documentation** — New comprehensive section documenting async vs sync hooks (v2.1.0+)
  - **New section**: `guide/ultimate-guide.md` line ~6075 "Hook Execution Model (v2.1.0+)" (~97 lines)
    - Synchronous vs Asynchronous execution explained
    - Configuration examples with `async: true` parameter
    - **Decision matrix**: 15 use cases (formatting, linting, type checking, security, logging, notifications, etc.)
    - Performance impact analysis (example: -5-10s per session with async formatting)
    - Limitations of async hooks (no exit code feedback, no additionalContext, no blocking)
    - Version history (v2.1.0 introduction, v2.1.23 cancellation fix)
  - **Reference updates**: `machine-readable/reference.yaml` — 7 new entries
    - `hooks_execution_model: 6075` (section pointer)
    - `hooks_async_support`, `hooks_async_use_cases`, `hooks_sync_use_cases`
    - `hooks_decision_matrix: 6091`, `hooks_async_limitations`, `hooks_async_bug_fix`
  - **Resource evaluation**: `docs/resource-evaluations/melvyn-malherbe-async-hooks-linkedin.md`
    - Score: 1/5 (Low - Reject) — Marketing post without technical value
    - **Gap identified**: Async hooks behavior not explicitly documented in guide
    - Fact-checked via Perplexity Deep Research (comprehensive 5K+ token report)
    - Challenge by technical-writer agent validated rejection + gap discovery
    - LinkedIn post (Jan 30, 2026) from Melvyn Malherbe redirects to commercial product (mlv.sh/ccli → codelynx.dev)
  - **Practical migration guide**: `claudedocs/aristote-hooks-migration-prompt.md` (400+ lines)
    - Real-world example: Méthode Aristote project with 7 hooks analyzed
    - 3 hooks migrated to async (auto-format, activity-logger, notification) for -12.75s/session gain
    - 4 hooks kept sync (dangerous-actions-blocker, typecheck-feedback, post-release-doc-update, git-context)
    - Step-by-step migration plan with verification checklist
    - Complete modified configuration in `claudedocs/aristote-hooks-migration.json`
  - **Impact**: Critical documentation gap filled — async hooks introduced in v2.1.0 but execution model never explicitly documented
    - Users can now optimize hook performance by migrating non-critical hooks to async
    - Decision matrix provides clear guidance on when to use sync vs async
    - Real-world case study demonstrates 30-40% reduction in blocked time per session
  - **Discovery method**: Resource evaluation workflow successfully identified gap through:
    1. LinkedIn post analysis (low technical value)
    2. Perplexity Deep Research confirming async hooks exist
    3. Guide audit revealing missing documentation
    4. Technical-writer agent challenge validating findings

## [3.18.2] - 2026-01-30

### Added

- **Practitioner Insights** — Peter Steinberger (PSPDFKit Founder, Moltbot Creator)
  - Added new practitioner insight in `guide/ecosystem/ai-ecosystem.md` documenting model-agnostic workflow patterns
  - **Patterns documented**: Stream monitoring, multi-project juggling (3-8 concurrent projects), fresh context validation, iterative exploration
  - **Source**: [Shipping at Inference-Speed](https://steipete.me/posts/2025/shipping-at-inference-speed) (Dec 2025 blog post)
  - **Evaluation**: Score 3/5 (Relevant - Useful complement)
    - Complete evaluation in `docs/resource-evaluations/steinberger-inference-speed.md`
    - Fact-checked GPT-5.2 claims (confirmed real, Dec 2024 release)
    - Validated PSPDFKit credentials (60+ employees, Dropbox/DocuSign/SAP clients)
  - **Alignment with guide**: Validates existing patterns (Fresh Context Section 2.2, Multi-Instance Section 9.13, Iterative Refinement workflows)
  - **Scope**: Model-agnostic patterns only, zero model comparisons (Codex/Opus excluded as per evaluation decision)
  - **Note**: Patterns originate from non-Claude workflow (Moltbot/GPT-5.2); validation in Claude Code context recommended
  - **Files modified**:
    - `guide/ecosystem/ai-ecosystem.md`: New entry after Matteo Collina (~26 lines, H3 format with alignment table)
    - `docs/resource-evaluations/steinberger-inference-speed.md`: Complete evaluation with challenge agent review
    - `docs/resource-evaluations/README.md`: Index updated (15→16 evaluations)
    - `machine-readable/reference.yaml`: Added `practitioner_steinberger` references (line 1997)

## [3.18.1] - 2026-01-30

### Changed

- **Claude Code Releases Tracking** — Updated to v2.1.25
  - **v2.1.25** (2026-01-30): Fixed beta header validation for Bedrock/Vertex gateway users
  - **v2.1.23** (2026-01-29): Customizable spinner verbs, mTLS/proxy fixes, terminal performance improvements
  - **Files updated**:
    - `machine-readable/claude-code-releases.yaml`: Updated latest version, added 2 new releases
    - `guide/core/claude-code-releases.md`: Synchronized with YAML, added detailed release notes
  - **Landing sync**: Updated Claude Code version badge v2.1.22 → v2.1.25

## [3.18.0] - 2026-01-28

### Added

- **MCP Servers Ecosystem Documentation** — New `guide/ecosystem/mcp-servers-ecosystem.md` (893 lines) documenting validated community MCP servers
  - **8 validated production-ready servers**:
    - **Playwright MCP** (Microsoft): Browser automation with accessibility trees (Quality: 8.8/10)
    - **Semgrep MCP** (Semgrep Inc.): Security scanning SAST/secrets/supply chain (Quality: 9.0/10)
    - **Kubernetes MCP** (Red Hat): Cluster management in natural language (Quality: 8.4/10)
    - **Context7 MCP**: Official framework documentation lookup (Quality: 7.2/10)
    - **Linear MCP**: Project management integration (Quality: 8.6/10)
    - **Vercel MCP**: Deployment and logs integration (Quality: 8.0/10)
    - **Browserbase MCP**: Headless browser infrastructure (Quality: 7.8/10)
    - **MCP-Compose**: Multi-server orchestration (Quality: 7.0/10)
  - **Evaluation framework**: 5 criteria (GitHub stars ≥50, release <3 months, docs, tests, unique use case)
  - **Production deployment guide**: Security checklist, quick start stack, performance metrics
  - **Ecosystem evolution**: Linux Foundation standardization, MCPB format, Advanced MCP Tool Use, MCP Apps
  - **Monthly watch methodology**: Template for maintaining guide with ecosystem updates
  - **Quality scoring system**: 5 dimensions (Maintenance, Documentation, Tests, Performance, Adoption) normalized to /10
  - **Files modified**:
    - `guide/ultimate-guide.md`: Added Community MCP Servers section with comparison table and quick start
    - `guide/README.md`: Added mcp-servers-ecosystem.md to docs table
  - **Impact**: Fills critical gap in guide - community MCP servers were previously undocumented

## [3.18.0] - 2026-01-28

### Added

- **Known Issues Tracker** — New `guide/core/known-issues.md` (285 lines) documenting verified critical bugs
  - **GitHub Issue Auto-Creation Bug**: Verified Issue #13797 (Dec 2025), 17+ confirmed accidental public disclosures
    - Security/privacy risk: Private project details exposed in public anthropics/claude-code repo
    - Affected versions: v2.0.65+
    - Status: ACTIVE as of Jan 28, 2026
    - Workarounds documented: Explicit repo specification, manual approval, pre-execution verification
    - Examples: #20792, #16483, #16476, #17899, #16464 ("wrong repo", "delete this")
  - **Excessive Token Consumption**: Issue #16856 (Jan 2026), 20+ reports of 4x+ faster consumption
    - Affected versions: v2.1.1+ (reported, published Jan 7, 2026)
    - Corrected version: Report claimed v2.0.61 (doesn't exist), real bug is v2.1.1
    - Anthropic status: "Not officially confirmed as bug" (investigating)
    - Possible causes: Holiday bonus expiration (Dec 25-31) + potential underlying issues
    - Workarounds: Monitor with /context, shorter sessions, disable auto-compact, reduce MCP tools
  - **Model Quality Degradation** (Aug-Sep 2025): ✅ RESOLVED
    - Official Anthropic postmortem: 3 infrastructure bugs (traffic misrouting, output corruption, XLA:TPU miscompilation)
    - Not intentional model degradation (community theories debunked)
    - All bugs fixed by mid-September 2025
    - Source: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues
  - **Stats verified via GitHub API** (Jan 28, 2026): 5,702 open issues (not 4,697 reported), 527 invalid labels (not 263), 80+ releases
  - **Fact-checking methodology**: Perplexity Pro (4 searches) + direct GitHub API queries (gh api, gh search issues, gh issue view)
  - **References**: Official links to GitHub issues, Anthropic postmortem, The Register article
  - **Impact**: Critical security awareness for users, actionable workarounds, transparent issue tracking
  - **Files modified**:
    - `guide/README.md`: Added known-issues.md to docs table
    - `machine-readable/reference.yaml`: 4 new entries (known_issues, github_bug:16, token_consumption:136, model_quality:231)
    - `docs/resource-evaluations/023-community-discussions-report-jan2026.md`: Full evaluation process (score 2/5, partial integration)

- **RTK (Rust Token Killer) integration** — Command output optimization tool for 72.6% token reduction
  - **New documentation**: `docs/resource-evaluations/rtk-evaluation.md` (comprehensive evaluation, score 4/5)
  - **Guide integration**: Section 9.13 Cost Optimization → new "Command Output Optimization with RTK" subsection
  - **Benchmarks verified**:
    - `rtk git log`: 92.3% reduction (13,994 → 1,076 chars)
    - `rtk git status`: 76.0% reduction (100 → 24 chars)
    - `rtk find`: 76.3% reduction (780 → 185 chars)
    - Average across working commands: 72.6% reduction
  - **Integration templates**:
    - `examples/claude-md/rtk-optimized.md`: CLAUDE.md template for manual RTK usage
    - `examples/skills/rtk-optimizer/SKILL.md`: Auto-suggestion skill for high-verbosity commands
    - `examples/hooks/bash/rtk-auto-wrapper.sh`: PreToolUse hook for automatic RTK wrapping
  - **Upstream contributions**: `claudedocs/rtk-pr-proposals.md` with 7 PR proposals (grep fix, ls fix, npm support)
  - **Limitations documented**: grep broken (v0.2.0), ls worse (-274%), low adoption (8 stars), early-stage
  - **Use cases**: Git workflows, file finding, large file reading (avoid: ls, grep, small outputs)
  - **Impact**: Proven 72.6% token reduction for git operations, validates preprocessing optimization strategy
  - **Reference**: https://github.com/pszymkowiak/rtk

### Fixed

- **Corrected "mgrep" misattribution in Everything Claude Code evaluation**
  - **Issue**: Incorrectly claimed Everything Claude Code contained "mgrep (50% token reduction)" tool
  - **Reality**: No such tool exists in affaan-m/everything-claude-code repository (verified via WebFetch)
  - **Confusion**: Mixed up mgrep (mixedbread-ai semantic search) with non-existent token reduction tool
  - **Files corrected**:
    - `docs/resource-evaluations/015-everything-claude-code-github-repo.md`: Removed 14 erroneous mgrep mentions
    - `machine-readable/reference.yaml:724`: Removed "mgrep (50% token reduction)" from unique patterns
    - `guide/ultimate-guide.md:14821`: Replaced with verified patterns (hookify, strategic compaction)
    - `CHANGELOG.md`: Updated v3.17.0 and v3.15.0 entries
  - **Verified patterns now documented**: hookify, pass@k metrics, sandboxed subagents, strategic compaction skills
  - **Impact**: Maintains guide credibility, prevents user confusion, ensures accuracy of ecosystem documentation

## [3.17.1] - 2026-01-27

### Added

- **Repository Structure diagram** in README.md
  - Interactive Mermaid diagram (graph LR layout) with 6 main directories
  - High-contrast colors (dark backgrounds + white text) for readability
  - ASCII art fallback in collapsible section for detailed structure
  - Shows key metrics: 15K lines guide, 86 templates, 227 questions, 22 evaluations

### Changed

- **README V3** — Merged best elements from two versions (README.md + README-new.md)
  - Kept "WHY vs HOW" positioning and quiz prominence from new version
  - Restored cc-copilot-bridge, Learning Paths by role, AI Assistants section from old version
  - Removed excessive competitor references (8 mentions → 2-3 in Ecosystem only)
  - Complementary positioning instead of "graduate to everything-claude-code"
  - Final size: 491 lines (vs 474 original)

- **Quiz links** — Now points to online version first
  - Primary: https://florianbruniaux.github.io/claude-code-ultimate-guide-landing/quiz/
  - Secondary: Local ./quiz/ for offline use

- **Core Documentation table** — Added 4 missing guides
  - AI Ecosystem (Complementary AI tools & integration patterns)
  - AI Traceability (Code attribution & provenance tracking)
  - Search Tools Cheatsheet (Grep, Serena, ast-grep, grepai comparison)
  - Learning with AI (Use AI without becoming dependent)

- **Ecosystem section** — Added direct link to AI Ecosystem Guide for integration patterns

### Removed

- **README-new.md** — No longer needed after V3 merge

## [3.17.0] - 2026-01-27

### Added

- **Tasks API field visibility limitations** (Gang Rui analysis, 2026-01-27)
  - **guide/ultimate-guide.md:3133**: Added 3 rows to comparison table (description visibility, metadata visibility, multi-call overhead)
  - **guide/ultimate-guide.md:3195**: New subsection "⚠️ Tasks API Limitations (Critical)" (~40 lines)
    - Field visibility constraint table (TaskList vs TaskGet)
    - Impact analysis: 11x API overhead for 10 tasks, no metadata scanning, session resumption friction
    - Cost example with bash code block
    - 3 workaround patterns: Hybrid approach (recommended), subject-as-summary, selective fetching
    - Source attribution: Community practitioner feedback (Gang Rui, Jan 2026)
  - **guide/workflows/task-management.md:223**: New subsection "⚠️ Field Visibility Limitations" (~35 lines)
    - TaskList field visibility details (id, subject, status, owner, blockedBy only)
    - Workflow adjustment examples (DON'T vs DO patterns)
    - Cost awareness: quantified overhead for N tasks
    - Mitigation strategies: subject field usage, concise descriptions, markdown files for plans
  - **guide/cheatsheet.md:398**: Added limitation note (~3 lines)
    - Warning: TaskList shows limited fields
    - Workaround pointer: use TaskGet per task for descriptions/metadata
    - Actionable tip: store key info in subject field
  - **machine-readable/reference.yaml:143-146**: Added 4 new entries
    - tasks_api_limitations: 3195 (line reference to new subsection)
    - tasks_api_field_visibility: inline summary
    - tasks_api_cost_overhead: formula for overhead calculation
    - tasks_api_workarounds: 3210 (line reference to workaround patterns)
  - **docs/resource-evaluations/016-gang-rui-tasks-api-limitations.md**: New evaluation (score 5/5 CRITICAL)
    - Comprehensive fact-check (8/8 claims verified)
    - Challenge phase with technical-writer agent (score adjusted 4→5)
    - Integration details with exact line numbers for all 6 modified files
  - **Score justification**: Breaks recommended workflow, 11x-51x cost overhead, metadata invisibility affects all custom fields
  - **Impact**: Prevents user frustration, maintains guide credibility, transparent cost implications

### Changed

- **everything-claude-code stats update** (31.9k stars, 2026-01-27)
  - Updated star count from 16k → 31.9k across all files (`CHANGELOG.md`, `machine-readable/reference.yaml`, `guide/ultimate-guide.md`)
  - Added unique patterns documentation: hookify (conversational hooks), pass@k metrics, sandboxed subagents, strategic compaction
  - Created comprehensive evaluation: `docs/resource-evaluations/015-everything-claude-code-github-repo.md` (Score 5/5 CRITICAL)
  - Added new "Production Config Collections" section in guide (line ~14768)
  - Positioning clarified: Complementary to Ultimate Guide (production configs vs educational content)

## [3.16.0] - 2026-01-27

### Added

- **TeammateTool & Myths vs Reality Documentation** (`guide/ultimate-guide.md`, `guide/cheatsheet.md`, `machine-readable/reference.yaml`, `docs/resource-evaluations/`)
  - **guide/ultimate-guide.md:3294**: New section "TeammateTool (Experimental)" (~60 lines)
    - Capabilities: Multi-agent coordination, team messaging, swarm patterns
    - Operations table: spawnTeam, discoverTeams, requestJoin, approveJoin
    - Execution backends (in-process, tmux, iTerm2) with auto-detection
    - Pattern examples: Parallel Specialists, Swarm Pattern
    - Limitations: 5-minute heartbeat timeout, feature flags non-documented, experimental status
    - When to use vs when NOT to use guidance
    - 3 community sources cited (kieranklaassen gist, GitHub Issue #3013, claude-sneakpeek)
    - Warning: Unstable, no official Anthropic support
  - **guide/ultimate-guide.md:15257**: New appendix "Appendix D: Myths vs Reality" (~160 lines)
    - Myth #1: "Hidden features with secret flags" → Reality: Progressive rollout, not secrets
    - Myth #2: "Tasks API = autonomous agents" → Reality: Coordination, not autonomy
    - Myth #3: "100x faster than competitors" → Reality: Honest comparison, no marketing hyperbole
    - Section: "What Makes Claude Code Actually Special" (documented strengths with sources)
    - Section: "How to Spot Reliable Information" (red flags checklist, trusted sources)
    - Contribution process for new myths
  - **guide/cheatsheet.md**: New section "Hidden Features (But Official!)" (~15 lines)
    - Lists 5 under-utilized features: Tasks API, Background Agents, TeammateTool, Session Forking, LSP Tool
    - Pro tip: "Read the CHANGELOG—these aren't secrets!"
    - Placed after "File References" for visibility
  - **machine-readable/reference.yaml**: 12 new entries
    - teammatetool: 3294 (line reference)
    - teammatetool_status, teammatetool_capabilities, teammatetool_sources (4 entries)
    - appendix_c_resource_evaluation: 15214
    - appendix_d_myths_vs_reality: 15257
    - myths_hidden_features, myths_tasks_api_autonomous, myths_100x_faster, myths_reliable_sources (4 line references)
  - **docs/resource-evaluations/2026-01-27-claude-code-hidden-feature-social-post.md**: New evaluation (307 lines)
    - Score: 1/5 (Reject - Marketing misinformation)
    - Fact-check: 5 claims verified (3 false, 2 partially true)
    - Technical writer challenge: 3/5 → 1/5 (score revised down after critique)
    - Decision: Reject source, but document real gaps (TeammateTool, Myths section) with official sources only
    - 12 sources consulted (official CHANGELOG, community gists, Perplexity search, GitHub Issues)
  - **Total documentation**: ~235 lines across guide files
  - **Resources evaluated**: Social media post (rejected), community gists (validated)
  - **Key facts verified**:
    - TeammateTool: Real feature, partially feature-flagged, community-discovered
    - Tasks API (v2.1.16+): Official, public, documented in CHANGELOG
    - CLAUDE_CODE_ENABLE_TASKS: Migration flag (revert to old system), not activation flag
    - No "hidden features": All public features documented in official CHANGELOG
- **MCP Apps (SEP-1865) Documentation** (`guide/core/architecture.md`, `guide/ultimate-guide.md`, `machine-readable/reference.yaml`)
  - **guide/core/architecture.md:656**: New section "MCP Extensions: Apps (SEP-1865)" (~150 lines)
    - Technical architecture (2 primitives: tools with UI metadata + UI resources via `ui://` scheme)
    - Communication flow diagram (MCP Client → Server → Sandboxed Iframe)
    - Multi-layered security model (sandbox, pre-declared templates, auditable JSON-RPC, user consent, content blocking)
    - Complete SDK documentation (`@modelcontextprotocol/ext-apps`): connect, ontoolresult, callServerTool, updateModelContext
    - Platform support matrix (6 clients: Claude Desktop, Cowork, VS Code, ChatGPT, Goose, CLI)
    - CLI relevance analysis (indirect: ecosystem understanding, MCP server dev, hybrid workflows)
    - 5 official example servers (threejs, map, pdf, system-monitor, sheet-music)
    - Production adoption table (9 tools at launch: Asana, Slack, Figma, Amplitude, Box, Canva, Clay, Hex, monday.com)
    - Relationship to prior work (MCP-UI, OpenAI Apps SDK)
    - Decision tree for MCP server developers (when to use Apps vs traditional tools)
    - 6 resource links (spec, SDK, blogs, VS Code announcement)
  - **guide/ultimate-guide.md:6509**: New section "MCP Evolution: Apps Extension" (~90 lines)
    - Context gap problem (before/after comparison)
    - What are MCP Apps (4 interface types: dashboards, wizards, viewers, monitors)
    - Available interactive tools table (9 tools with capabilities)
    - Platform support matrix with access instructions
    - CLI relevance (indirect benefits + hybrid workflow example)
    - Technical foundation (co-authoring, SDK, "build once deploy everywhere")
    - Cross-reference to architecture.md for deep dive
    - 3 resource links (MCP blog, Claude blog, spec)
  - **guide/ultimate-guide.md:7522**: Table update "Plugin vs. MCP Server"
    - Added "Interactive UI" row: Plugin (No) | MCP Server (Yes via MCP Apps)
    - Extended rule of thumb: MCP Apps = "What Claude can show"
    - Note clarifying CLI relevance and cross-reference to 8.1
  - **machine-readable/reference.yaml**: 8 new entries
    - mcp_apps_architecture, mcp_apps_evolution (line references)
    - mcp_apps_spec, mcp_apps_blog_mcp, mcp_apps_blog_claude, mcp_apps_sdk (external links)
    - mcp_apps_announcement_date: "2026-01-26"
    - mcp_apps_cli_relevance: "Indirect (ecosystem understanding, MCP server dev, hybrid workflows)"
  - **docs/resource-evaluations/mcp-apps-announcement.md**: New evaluation (159 lines)
    - Score: 4/5 (High Value - Integrate within 1 week)
    - 4 criteria evaluated (Relevance: 4/5, Reliability: 5/5, Applicability: 3/5, Completeness: 4/5)
    - Technical review challenge (2/5 initial → 4/5 revised after ecosystem analysis)
    - Fact-check with Perplexity (9 claims verified)
    - Decision justification and integration tracking
  - **Total documentation**: ~240 lines across 3 guide files
  - **Resources evaluated**:
    - https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
    - https://claude.com/blog/interactive-tools-in-claude
  - **Key facts verified**:
    - First official MCP extension (co-authored OpenAI + Anthropic + MCP-UI creators)
    - SDK stable 2026-01-26
    - 9 interactive tools at launch (Asana, Slack, Figma, Amplitude, Box, Canva, Clay, Hex, monday.com)
    - Platform support: Claude Desktop (claude.ai/directory, Pro/Max/Team/Enterprise), VS Code Insiders, ChatGPT rolling out, Goose
    - Claude Code CLI: Not applicable (text-only terminal, no iframe rendering)
    - Indirect CLI benefits: Ecosystem understanding, MCP server development option, hybrid Desktop→CLI workflows
- **Migration Scripts for v2.1.19 Breaking Change** (`examples/scripts/`)
  - `migrate-arguments-syntax.sh`: Bash migration script for macOS/Linux users
  - `migrate-arguments-syntax.ps1`: PowerShell migration script for Windows users
  - Automated detection and conversion of `$ARGUMENTS.0` → `$ARGUMENTS[0]` in custom commands
  - Dry-run mode with preview, automatic backups, safe batch processing

### Changed

- **Updated $ARGUMENTS Syntax Documentation** (Claude Code v2.1.19 breaking change)
  - `guide/ultimate-guide.md` (7 occurrences): Updated all custom command examples to use bracket syntax `$ARGUMENTS[0]` or shorthand `$0`, `$1`
  - Added migration note in § 6.2 Variable Interpolation explaining breaking change and migration path
  - `guide/cheatsheet.md`: Updated command template to show new syntax
  - All examples now demonstrate both bracket notation and shorthand alternatives

## [3.14.0] - 2026-01-26

### Added

- **NotebookLM MCP Integration Documentation** (`guide/ecosystem/ai-ecosystem.md`, `guide/ultimate-guide.md`)
  - **§ 4.1 NotebookLM MCP Integration** (~240 lines): Complete installation and usage guide
    - Detailed tool breakdown table: 16 tools across 3 profiles (minimal/standard/full)
    - Multi-account authentication workflow (authuser parameter for secondary Google accounts)
    - Share links library building pattern (isolated Chrome profile, no auto-sync)
    - Query notebooks with persistent conversation context (session_id)
    - Comparison table: MCP integration vs Web UI
    - Troubleshooting guide and example onboarding workflow
  - **§ 4.2 Advanced Features (Full Profile)** (~110 lines)
    - `remove_notebook`: Clean up library, fix duplicates
    - `re_auth`: Switch Google accounts without full cleanup
    - `cleanup_data`: Complete MCP reset with preserve_library option
    - Manual browser control: state inspection, actions, element waiting
  - **§ 4.3 Browser Options** (~70 lines)
    - Complete options reference: headless, timeout, viewport, stealth mode
    - Stealth mode configuration: typing speed (160-240 WPM), random delays, mouse movements
    - Usage examples: debug visually, custom timeouts, disable stealth for speed
  - **§ 4.4 Session Management** (~60 lines)
    - Session lifecycle: automatic creation, 15min timeout, 10 max concurrent
    - Manual session control: resume specific sessions, force new sessions
    - List active sessions with message counts and age
  - **§ 4.5 Library Management Best Practices** (~90 lines)
    - Naming conventions and topics strategy (specific vs broad)
    - Metadata refinement workflow: add → use → refine → archive
    - Search and discovery patterns (keyword search, smart selection)
    - Notebook lifecycle management
  - **guide/ultimate-guide.md**: Updated Complementary Tools table with "MCP integration" mention
  - **Total**: ~630 lines of comprehensive MCP documentation covering all 16 tools
- **Resource Evaluations Public Documentation** (`docs/resource-evaluations/`)
  - New tracked directory with 14 community resource evaluations (gsd, worktrunk, boris-cowork-video, astgrep, etc.)
  - Standardized filenames (removed date prefixes for stable linking)
  - Comprehensive methodology documentation with scoring grid (1-5 scale)
  - Index table with all evaluations, scores, and integration decisions
  - Working documents (prompts, private audits) remain in `claudedocs/` (gitignored)
  - New workflow section in CLAUDE.md documenting evaluation process
  - Transparency: Contributors can now see why resources were integrated/rejected
- **Task Management Workflow** (`guide/workflows/task-management.md`)
  - Comprehensive 775-line guide for Claude Code's task management system
  - Complete API reference: TaskCreate, TaskUpdate, TaskGet, TaskList, TaskDelete
  - 5 practical workflows: startup → feature work → bug fixing → code review → cleanup
  - Best practices: when to use tasks, granularity guidelines, status lifecycle
  - Anti-patterns section: over-tasking, status confusion, orphaned tasks
  - Integration with other workflows (TDD, Plan-Driven, GSD)
  - Quick reference added to cheatsheet
- **Ultimate Guide Task Management Integration** (`guide/ultimate-guide.md:10786-10930`)
  - New §9.18 "Task Management System" section (145 lines)
  - Core concepts, tool reference, practical patterns
  - Links to full workflow guide for details
- **Appendix C: Resource Evaluation Process** (`guide/ultimate-guide.md:15034`)
  - New appendix section documenting systematic evaluation methodology
  - 5-point scoring system (Critical → Low) with decision criteria and timelines
  - List of 14 documented assessments organized by categories (methodologies, tools, content, research)
  - Transparency explanation: why resources are integrated (3+), mentioned (2), or rejected (1)
  - Links to full methodology in `docs/resource-evaluations/README.md`
  - Browse all evaluations link to `docs/resource-evaluations/` directory

### Changed

- **guide/core/methodologies.md:55**: Corrected GSD evaluation link
  - Old: `../claudedocs/resource-evaluations/gsd-evaluation.md` (private)
  - New: `../docs/resource-evaluations/gsd-evaluation.md` (public)
- **machine-readable/reference.yaml**: Added resource evaluations metadata
  - New section: resource_evaluations_directory, count (14), methodology link
  - Added references: appendix (line 15034), README section (line 278)
  - Corrected gsd_evaluation path from private claudedocs to public docs
- **README.md**: Updated documentation metrics for accuracy and landing site synchronization
  - Guide length: ~10K → ~15K lines (actual: 15,053 lines)
  - Reading time: ~3 hours → ~4 hours (reflects actual guide size)
  - Security hooks: 15+ → 18 (precise count)
  - Templates count: maintained at 86 (consistent with check-landing-sync.sh logic)
  - Repository Structure section: updated ultimate-guide.md from "~13,425 lines" to "~15K lines"
  - Added **Resource Evaluations** section (14 assessments) with methodology links
  - All changes verified with `./scripts/check-landing-sync.sh` for full synchronization

## [3.13.0] - 2026-01-26

### Added

- **Boris Cherny mental models integration** (from YouTube interview analysis)
  - **CLAUDE.md as Compounding Memory** (`guide/ultimate-guide.md:3254`)
    - New philosophy section: "You should never have to correct Claude twice for the same mistake"
    - 4-step cycle: error → rule → read → never repeated
    - Compounding effect visualization (5 → 20 → 50 rules over time)
    - Boris's practical example: 2.5K tokens grown over months
    - Anti-pattern warning: no preemptive documentation
    - Mental model shift: configuration file → organizational learning system
  - **Plan-First Discipline** (`guide/core/methodologies.md:61`)
    - New "Foundational Discipline" section (between Tier 1 and Tier 2)
    - Core principle: "Once the plan is good, the code is good" (Boris quote)
    - Decision table: when to plan first vs when to skip
    - 3-phase workflow: exploration → validation → execution
    - Benefits quantified vs "just start coding"
    - CLAUDE.md integration example for team planning policy
  - **Verification Loops architectural pattern** (`guide/core/methodologies.md:214`)
    - Extended beyond TDD to general architectural principle
    - 8 verification domains table (frontend, backend, types, style, performance, accessibility, security, UX)
    - Boris quote: "An agent that can 'see' what it has done produces better results"
    - Implementation patterns: hooks, browser extensions, test watchers, CI/CD gates
    - Anti-pattern: blind iteration without feedback mechanism
  - **Boris direct quotes in case study** (`guide/ultimate-guide.md:10743`)
    - 4 key insights: multi-clauding, CLAUDE.md compounding, plan-first, verification loops
    - Opus 4.5 ROI explanation: higher per-token cost but fewer corrections = net savings
    - Supervision model description: "tending to multiple agents" vs sequential execution
    - YouTube source citation added alongside InfoQ article
  - Resource evaluation saved in `claudedocs/resource-evaluations/boris-cowork-video-eval.md` (score: 3/5 - relevant, moderate improvement)
  - Source: [YouTube - I got a private lesson on Claude Cowork & Claude Code](https://www.youtube.com/watch?v=DW4a1Cm8nG4)
- **Advanced Worktree Tooling section** (`guide/ultimate-guide.md:10748`)
  - New section "Advanced Tooling for Worktree Management (Optional)" in §9.17 Multi-Instance Workflows
  - Pattern validation: 3 independent teams created worktree wrappers (incident.io, GitHub #1052, Worktrunk)
  - **"Do I Need Worktrunk?" self-assessment** (`guide/ultimate-guide.md:10762`)
    - 3 quick questions (volume, multi-instance, team context)
    - Decision matrix: 4 user profiles (Beginner, Casual, Power user, Boris scale)
    - Quick alias alternative for "Casual user" profile (2 min setup, -79% typing vs vanilla git)
    - Bottom line guidance: "80% of readers should start with vanilla git or alias"
    - Prevents tool adoption without need assessment (YAGNI principle applied to tooling)
  - Benchmark table: Worktrunk vs vanilla git vs custom wrappers (6 operations compared)
  - Option 1: Worktrunk CLI (1.6K stars, Rust, multi-platform, CI/LLM integration, project hooks)
  - Option 2: DIY custom wrappers (bash/fish examples from production teams)
  - Progressive recommendation: Learn fundamentals → Add wrapper → Scale to multi-instance
  - Philosophy: "Tools amplify knowledge. Master git patterns before adding convenience layers."
  - ROI evidence: incident.io measured 18% improvement (30s) on API generation time with worktree workflow
  - Fact-checked analysis: 4 sources analyzed (Worktrunk GitHub, incident.io blog, Anthropic best practices, GitHub issue #1052)
  - Resource evaluation saved in `claudedocs/resource-evaluations/worktrunk-evaluation.md` (score: 3/5 - relevant, useful complement)
  - Total additions: ~260 lines (121 original + 139 self-assessment)
- **machine-readable/reference.yaml**: Added `advanced_worktree_tooling: 10748`, `worktree_tooling_self_assessment: 10762`, and updated line references for all sections after worktrees
- **GSD (Get Shit Done) methodology mention** (`guide/core/methodologies.md:47-55`)
  - Added to Tier 1: Strategic Orchestration alongside BMAD
  - Meta-prompting 6-phase workflow (Initialize → Discuss → Plan → Execute → Verify → Complete)
  - Fresh 200k-token contexts per task to avoid context rot
  - Note: Core concepts overlap with existing patterns (Ralph Loop, Gas Town, BMAD)
  - Resource evaluation saved in `claudedocs/resource-evaluations/gsd-evaluation.md` (score: 2/5 - marginal/redundant)
  - Source: https://github.com/glittercowboy/get-shit-done (7.5k stars, created Dec 2025)
- **ClawdBot FAQ enrichment** (`guide/ultimate-guide.md:14375,14385`)
  - Added community adoption analysis link (5,600+ social mentions on X/Twitter)
  - Updated final note with adoption metrics and real-world use case examples
  - Link to comprehensive community analysis: https://docs.google.com/document/d/1Mz4xt1yAqb2gDxjr0Vs_YOu9EeO-6JYQMSx4WWI8KUA/preview
  - Resource evaluation saved in `claudedocs/resource-evaluations/2026-01-25-clawdbot-twitter-analysis.md` (score: 2/5 - marginal, partial integration)
- **MCP architecture visual diagram** (`guide/core/architecture.md:513`, SVG)
  - 7-layer security model showing LLM/MCP Server/Tools separation
  - Visual representation of "No Data Access" (LLM layer) and "Hidden From AI" (Real Systems layer)
  - Beginner-friendly introduction to MCP architecture with color-coded security boundaries
  - Design inspired by Dinesh Kumar's LinkedIn visualization, recreated as original work under Apache-2.0
  - Includes workflow diagram (5 steps: User Asks → LLM Thinks → MCP Controls → Tools Execute → Safe Result)
  - Golden rule banner: "LLM Thinks → MCP Controls → Tools Execute → Data Locked"
- **machine-readable/reference.yaml**: Added `architecture_mcp_visual` (SVG diagram reference)

### Changed

- **README.md**: Updated templates count from 83 to 86 (badge and description text)
  - Reflects addition of 3 new evaluation documents in `claudedocs/resource-evaluations/`
  - Actual template count: 86 files in `examples/` directory

## [3.12.1] - 2026-01-25

### Added

- **Bridge Script: Claude Code → doobidoo → LM Studio** (`examples/scripts/bridge.py`)
  - Python CLI for executing Claude Code plans locally via LM Studio
  - Cost optimization: Plan with Opus (~$0.50-2), execute free locally (80-90% savings)
  - Architecture: Claude Code stores plans in doobidoo SQLite → bridge reads → LM Studio executes
  - 5 components: DoobidooReader, LMStudioClient, Validator, StepExecutor, PlanExecutor
  - JSON Schema for plan validation (`examples/scripts/bridge-plan-schema.json`)
  - 4 validation types: json, syntax_check, contains_keys, non_empty
  - Failure handling: retry_with_context, skip, halt strategies
  - CLI: `--health`, `--list`, `--plan ID`, `-v` verbose mode
  - Documentation in ultimate-guide.md §11.2 "Local Execution Bridge" (line 14079)
- **examples/scripts/README.md**: New documentation for all utility scripts
- **machine-readable/reference.yaml**: Added bridge_script, bridge_schema, bridge_guide entries

### Changed

- **.gitignore**: Added `__pycache__/` and `*.pyc` for Python artifacts

## [3.12.0] - 2026-01-25

### Added

- **External orchestration systems documentation** (`guide/ecosystem/ai-ecosystem.md:808`)
  - Gas Town (Steve Yegge): Multi-agent workspace manager using Claude Code instances
  - multiclaude (dlorenc): Self-hosted multi-agent Claude Code spawner (383 stars, active development)
  - agent-chat (Justin Abrahms): Real-time monitoring UI for orchestrator communications (v0.2.0)
  - Architecture patterns for transposing monitoring to native Claude Code workflows
  - Security and cost warnings for experimental orchestration systems
  - Decision matrix: when to use orchestrators vs single Claude Code sessions
- **machine-readable/reference.yaml**: Added `external_orchestrators` section with structured data
  - Programmatic access to Gas Town, multiclaude, agent-chat metadata
  - Links to guide sections, GitHub repos, author attribution
- **guide/ops/observability.md:117**: Cross-reference to multi-agent orchestration monitoring
  - Architecture pattern for custom implementations (hooks + SQLite + SSE)
  - Comparison table: external orchestrator monitoring vs native Claude Code monitoring

## [3.11.7] - 2026-01-25

### Added

- **Vibe Coding: Context Overload Anti-Pattern** (`guide/ultimate-guide.md:8746`)
  - New subsection in §9.8 Vibe Coding documenting the "context overload" anti-pattern
  - Identifies symptoms: big-bang context dumps, 5K+ line prompts, performance degradation
  - Phased context strategy: Exploration (plan mode) → Implementation (focused) → Fresh start (handoffs)
  - Unifies 3 existing patterns (plan mode, fresh context, session handoffs) under explicit framework
  - Attribution to Jens Rusitschka ("Vibe Coding, Level 2", Jan 2026)
  - Practical workflow examples with bash commands
  - Cross-references to §2.2 (Fresh Context Pattern, line 1525), §2.3 (Plan Mode, line 2100)
  - Total additions: ~60 lines
- **machine-readable/reference.yaml**: Added `vibe_coding_context_overload`, `vibe_coding_context_overload_source`, `vibe_coding_phased_strategy`
- **guide/roles/learning-with-ai.md:96**: Added cross-reference from "Vibe Coding Trap" to new anti-pattern section

- **Product Manager FAQ entry** (`guide/ultimate-guide.md:14335`)
  - Minimal FAQ entry (28 lines) addressing PM workflows with Claude Code
  - Distinction between code-adjacent PMs (technical validation) and non-coding PMs (strategy/research)
  - Tool stack example from Stilyan Mitrev (Head of Product, StableLab): Granola, Wispr Flow, ChatPRD, v0
  - Reality check: "emerging area with limited community validation" (1 practitioner report, tool not adopted long-term)
  - Guidance: CLI appropriate for technical PMs, Claude Desktop better for non-technical workflows
  - Cross-references: AI Ecosystem Guide, Cowork Guide, Design-to-Code Workflow
  - Source: [LinkedIn article (Jan 23, 2026)](https://www.linkedin.com/pulse/how-i-currently-ai-product-manager-stilyan-mitrev-ycvvf/)
  - Decision: Minimal integration (proportional to source), invite community contribution
  - Reference YAML: Added `faq_product_managers: 14335`

- **MCP architecture visual diagram** (`guide/core/architecture.md:513`, SVG)
  - 7-layer security model showing LLM/MCP Server/Tools separation
  - Visual representation of "No Data Access" (LLM layer) and "Hidden From AI" (Real Systems layer)
  - Beginner-friendly introduction to MCP architecture with color-coded security boundaries
  - Design inspired by Dinesh Kumar's LinkedIn visualization, recreated as original work under Apache-2.0
  - Includes workflow diagram (5 steps: User Asks → LLM Thinks → MCP Controls → Tools Execute → Safe Result)
  - Golden rule banner: "LLM Thinks → MCP Controls → Tools Execute → Data Locked"
- **External orchestration systems documentation** (`guide/ecosystem/ai-ecosystem.md:808`)
  - Gas Town (Steve Yegge): Multi-agent workspace manager using Claude Code instances
  - multiclaude (dlorenc): Self-hosted multi-agent Claude Code spawner
  - agent-chat (Justin Abrahms): Real-time monitoring UI for orchestrator communications
  - Architecture patterns for transposing monitoring to native Claude Code workflows
  - Security and cost warnings for experimental orchestration systems
- **machine-readable/reference.yaml**: Added `external_orchestrators` section with Gas Town, multiclaude, agent-chat
- **machine-readable/reference.yaml**: Added `architecture_mcp_visual` (SVG diagram reference)
- **guide/ops/observability.md**: Cross-reference to multi-agent orchestration monitoring

## [3.11.7] - 2026-01-25

### Added

- **ClawdBot vs Claude Code FAQ** (`guide/ultimate-guide.md:14263`)
  - New Appendix B: FAQ section addressing community confusion between ClawdBot and Claude Code
  - Comprehensive comparison table (9 dimensions): interface, audience, use cases, pricing, architecture
  - Decision tree: when to choose each tool, when to use both together
  - Early warning note in "Before You Start" section (line 33) to alert readers immediately
  - Community misconceptions addressed: different architectures, complementary not competitive
  - Resources: ClawdBot website, GitHub repo, setup guides
  - Context: Jan 2026 buzz on X/Reddit created confusion ("dominated X timeline over 1-2 months")
  - Related: ClawdBot is self-hosted chatbot for messaging apps (personal automation, smart home); Claude Code is CLI for developers (terminal/IDE, code generation)
  - Total additions: +76 lines in guide, +3 lines in reference.yaml

- **Architecture Diagrams as Context (Advanced Pattern)** (`guide/ecosystem/ai-ecosystem.md:1379`)
  - Pattern documentation for using architecture diagrams in OOP codebases
  - MCP tools reference: Archy MCP, Mermaid MCP, Blueprint MCP (ArcadeAI)
  - ACM 2024 research validation for LLM OOP limitations
  - Recommended workflow: Serena → Archy MCP → Manual inline Mermaid
  - Use cases: OOP codebases >20 modules, Java/Spring projects with deep polymorphism
  - Source: [LinkedIn discussion (Jan 2026)](https://www.linkedin.com/posts/tigraff_uml-claude-wibecoding-activity-7420595633826258944-gGO5)
  - Evaluation report: `claudedocs/resource-evaluations/uml-oop-diagrams-eval.md`

- **AI Traceability & Attribution Guide** (`guide/ops/ai-traceability.md`)
  - Comprehensive documentation on AI code attribution and disclosure (~500 lines)
  - LLVM "Human-in-the-Loop" policy (January 2026): `Assisted-by:` trailer standard
  - Ghostty mandatory disclosure pattern (August 2025)
  - Fedora contributor accountability framework (RFC 2119 language)
  - git-ai tool: checkpoint tracking, AI Code Halflife metric (3.33 years median)
  - PromptPwnd security vulnerability documentation
  - Four-level disclosure spectrum: None → Minimal → Standard → Full
  - Policy comparison matrix across LLVM, Ghostty, Fedora
  - Implementation guides for solo dev, team, and enterprise contexts
  - Source: [Vibe coding needs git blame](https://quesma.com/blog/vibe-code-git-blame/) (Piotr Migdał)

- **AI Disclosure Templates** (`examples/config/`)
  - `CONTRIBUTING-ai-disclosure.md`: Section template for CONTRIBUTING.md
  - `PULL_REQUEST_TEMPLATE-ai.md`: PR template with AI disclosure checkboxes
  - Based on Ghostty, LLVM, and Fedora policies

- **Cross-references added**
  - `guide/ultimate-guide.md:9256`: Link to AI Traceability Guide after Co-Authored-By section
  - `guide/roles/learning-with-ai.md:85`: Related note after Vibe Coding Trap
  - `guide/security/security-hardening.md:476`: PromptPwnd reference in See Also
  - `guide/README.md`: New entry in contents table

- **Reference YAML expansion** (`machine-readable/reference.yaml`)
  - 14 new entries for AI traceability topics
  - Template locations for disclosure files

- **Architecture Diagrams as Context (Advanced Pattern)** (`guide/ecosystem/ai-ecosystem.md:1379`)
  - Pattern documentation for using architecture diagrams in OOP codebases
  - MCP tools reference: Archy MCP, Mermaid MCP, Blueprint MCP (ArcadeAI)
  - ACM 2024 research validation for LLM OOP limitations
  - Recommended workflow: Serena → Archy MCP → Manual inline Mermaid
  - Use cases: OOP codebases >20 modules, Java/Spring projects with deep polymorphism
  - Source: [LinkedIn discussion (Jan 2026)](https://www.linkedin.com/posts/tigraff_uml-claude-wibecoding-activity-7420595633826258944-gGO5)
  - Evaluation report: `claudedocs/resource-evaluations/uml-oop-diagrams-eval.md`

## [3.11.6] - 2026-01-24

### Added

- **Plugin System Section 8.5 major update** (`guide/ultimate-guide.md:7092-7280`)
  - **CRITICAL FIX**: Corrected plugin structure (`.claude-plugin/plugin.json` not root `plugin.json`)
  - Added `.mcp.json`, `.lsp.json`, `hooks/hooks.json` to directory structure
  - Added skill namespacing documentation (`/plugin-name:skill`)
  - Added warning about common mistake (components outside `.claude-plugin/`)
  - Added link to official Anthropic docs: code.claude.com/docs/en/plugins
  - Source: [Anthropic Official Plugin Docs](https://code.claude.com/docs/en/plugins)

- **Community Marketplaces subsection** (`guide/ultimate-guide.md:7246`)
  - **wshobson/agents**: 67 plugins, 99 agents, 107 skills (verified Jan 2026)
  - **claude-plugins.dev**: 11,989 plugins, 63,065 skills indexed
  - **claudemarketplaces.com**: Auto-scan GitHub for marketplaces
  - Popular plugins with install counts: Context7 (~72k), Ralph Wiggum (~57k), Figma MCP (~18k), Linear MCP (~9.5k)
  - Curated lists: awesome-claude-code (20k+ stars)
  - Installation examples for wshobson/agents
  - Sources: [wshobson/agents](https://github.com/wshobson/agents), [claude-plugins.dev](https://claude-plugins.dev), [Firecrawl analysis](https://www.firecrawl.dev/blog/best-claude-code-plugins)

- **Plugin ecosystem YAML index expansion** (`machine-readable/reference.yaml:137-164`)
  - `plugins_official_docs`: Official Anthropic plugin documentation URL
  - `plugins_official_reference`: Plugin reference docs URL
  - `plugins_official_marketplaces`: Marketplace docs URL
  - `plugins_wshobson_agents`: Stats and URL (67/99/107)
  - `plugins_registry_claude_plugins_dev`: Registry stats (11,989/63,065)
  - `plugins_registry_claudemarketplaces`: Auto-scan description
  - `plugins_popular`: Top 4 plugins with install counts
  - `plugins_awesome_list`: 20k+ stars curated list
  - `plugins_community_marketplaces: 7246`: New section line number

- **Resource evaluation: Nick Jensen plugins article** (`claudedocs/resource-evaluations/2026-01-24-nick-jensen-plugins.md`)
  - Initial score 3/5 → Challenge 4/5 → Perplexity verification 2/5 (Marginal)
  - Rejected as direct source: outdated stats (63/85/47 vs 67/99/107), unverified onboarding claim
  - Perplexity research revealed better primary sources (Anthropic docs, wshobson README, claude-plugins.dev)
  - Lesson: Blog posts often cite outdated data; verify against primary sources
  - Decision: Integrate primary sources instead of article

- **First plugin example: SE-CoVe (Chain-of-Verification)** (`examples/plugins/se-cove.md`)
  - Software Engineering adaptation of Meta's Chain-of-Verification methodology for Claude Code
  - Research foundation: Meta AI paper (arXiv:2309.11495), ACL 2024 Findings
  - 5-stage pipeline: Baseline → Planner → Executor → Synthesizer → Output
  - Critical innovation: Verifier operates without draft code access (prevents confirmation bias)
  - Performance metrics from research (Llama 65B): +23-112% accuracy depending on task, ~2x token cost
  - When to use: Critical code review, architectural decisions, complex debugging (when correctness > speed)
  - When NOT to use: Trivial changes, tight token budgets, exploratory coding
  - Installation via `/plugin marketplace add vertti/se-cove-claude-plugin` then `/plugin install chain-of-verification`
  - Limitations documented: Reduces hallucinations (not eliminates), model-specific (Llama 65B tested), task-dependent performance
  - Plugin System gap filled: First concrete example for Section 8.5 (previously theoretical docs only)
  - Sources: [GitHub repo](https://github.com/vertti/se-cove-claude-plugin) v1.1.1, [arXiv paper](https://arxiv.org/abs/2309.11495), [ACL Anthology](https://aclanthology.org/2024.findings-acl.212/)

- **Plugin system YAML index entries** (`machine-readable/reference.yaml:124-132`)
  - `plugins_system: 6863` (existing section reference)
  - `plugins_commands: 6876` (command table reference)
  - `plugins_marketplace: 6890` (marketplace management reference)
  - `plugins_recommended: "examples/plugins/"` (new directory)
  - `plugins_se_cove: "examples/plugins/se-cove.md"`
  - `chain_of_verification: "guide/core/methodologies.md:165"` (methodology reference)
  - `chain_of_verification_paper: "https://arxiv.org/abs/2309.11495"`
  - `chain_of_verification_acl: "https://aclanthology.org/2024.findings-acl.212/"`

- **Resource evaluation documentation** (`claudedocs/resource-evaluations/2026-01-24-se-cove-plugin.md`)
  - Complete evaluation workflow: Fetch → Gap Analysis → Technical Writer Challenge → Fact-Check (Perplexity) → Documentation
  - Fact-check findings: Marketing claim "28% improvement" contextualized (task-specific: 23-112%, omitted 2x cost and -26% output)
  - Curation policy established: Academic validation + Claims fact-checked + Trade-offs disclosed
  - Approach B (Neutral Academic) validated: Cite paper metrics, not marketing claims
  - Template for future plugin evaluations (reusable workflow)
  - Tools used: WebFetch (LinkedIn, GitHub, arXiv), Perplexity Pro (paper verification), Task (technical-writer challenge)
  - Confidence assessment: High (methodology), Medium (generalization), Low (marketing accuracy)

- **Claude Reflect System documentation** (`guide/ultimate-guide.md:5161`, ~135 lines)
  - New subsection: "Automatic Skill Improvement: Claude Reflect System"
  - Repository: [haddock-development/claude-reflect-system](https://github.com/haddock-development/claude-reflect-system)
  - Marketplace: [Agent Skills Index](https://agent-skills.md/skills/haddock-development/claude-reflect-system/reflect)
  - Pattern documented: Self-improving skills via feedback analysis (complementary to Claudeception)
  - Two modes: Manual (`/reflect [skill-name]`) + Automatic (Stop hook)
  - 8-step workflow: Monitor → Parse → Classify → Propose → Review → Backup → Apply → Commit
  - Safety features table: User review gate, Git backups, syntax validation, confidence levels, locking
  - Security warnings table: 4 risks (Feedback Poisoning, Memory Poisoning, Prompt Injection, Skill Bloat) with mitigations
  - Installation instructions: Git clone + Stop hook configuration (Bash/PowerShell)
  - Use case example: Terraform validation skill evolution
  - Activation commands: `/reflect-on`, `/reflect-off`, `/reflect [skill]`, `/reflect status`
  - Comparison table: Claudeception (generation) vs Reflect System (improvement)
  - Recommended combined workflow: Bootstrap → Iterate → Refine → Curate
  - Timeline example: 8-week skill evolution (80% → 95% accuracy)
  - Resources: GitHub, Agent Skills, YouTube tutorial, Anthropic Memory Cookbook
  - Academic sources: Anthropic Memory Cookbook, adversarial attacks research

- **Skill lifecycle YAML index entries** (`machine-readable/reference.yaml:113-123`)
  - `skill_lifecycle: 5118` (section start)
  - `claude_reflect_system: 5161` (main section)
  - `claude_reflect_system_repo: https://github.com/haddock-development/claude-reflect-system`
  - `claude_reflect_system_agent_skills: https://agent-skills.md/skills/...`
  - `skill_improvement_pattern: 5161`
  - `skill_improvement_how_it_works: 5169`
  - `skill_improvement_safety: 5188`
  - `skill_improvement_security_warnings: 5237`
  - `skill_improvement_comparison: 5263` (Claudeception vs Reflect)
  - `skill_improvement_workflow: 5275` (combined workflow)

- **Resource evaluation: Self-improve skill pattern** (`claudedocs/resource-evaluations/2026-01-24_self-improve-skill.md`)
  - Investigation workflow: Repository search (failed) → Pattern validation via Perplexity (success)
  - Findings: Announced plugin unavailable, but pattern validated by Claude Reflect System
  - Score: 2/5 (announced resource) → REJECT with REDIRECT to proven alternative
  - Decision rationale: Availability > Announcement, Verification > Claims, Alternatives > Gaps
  - Tools used: GitHub search (failed), Perplexity Pro (found alternative), WebSearch (baseline)
  - Curation policy reinforced: Only document publicly accessible resources with verified functionality
  - Research foundation: Anthropic Memory Cookbook, Agent Skills Index
  - Evaluation status: COMPLETE with HIGH confidence

### Changed

- **README.md**: Templates count 82 → 83 (added SE-CoVe plugin)
  - Badge updated: `Templates-82` → `Templates-83`
  - "Examples Library" section updated (line 228)
  - Ecosystem table updated (line 377)
  - New **Plugins** subsection added after Skills (line 238)

## [3.11.5] - 2026-01-23

### Added

- **skills.sh marketplace documentation** (`guide/ultimate-guide.md:5172`, `guide/ecosystem/ai-ecosystem.md:1284`)
  - New subsection in Section 5.5: "Skills Marketplace: skills.sh"
  - Vercel Labs project (launched Jan 21, 2026): centralized skill discovery + one-command install
  - 200+ skills, leaderboard with 35K+ installs (vercel-react-best-practices top skill)
  - Format 100% compatible with `.claude/skills/` structure
  - Installation: `npx add-skill <owner/repo>` → copies to `~/.claude/skills/`
  - Supported agents: 20+ (Claude Code, Cursor, GitHub Copilot, Windsurf, etc.)
  - Top skills by category: Frontend (vercel-react, web-design), Database (supabase-postgres), Auth (better-auth), Testing (TDD)
  - Status documented: Community project (Vercel Labs, not official Anthropic), early stage
  - Trade-offs: Centralized discovery vs GitHub distribution, multi-agent focus vs Claude Code specific
  - Cross-reference added to `guide/ecosystem/ai-ecosystem.md` Section 11.3 (Skills Distribution Platforms)
  - Complementary resources table updated in README.md
  - YAML index entries:
    - `skills_marketplace: 5172`
    - `skills_marketplace_url: https://skills.sh/`
    - `skills_marketplace_github: vercel-labs/agent-skills`
    - `skills_marketplace_install: npx add-skill <owner/repo>`
    - `skills_marketplace_top_skills` (5 entries with install counts)
    - `skills_marketplace_status: Community (Vercel Labs), launched Jan 21, 2026`

## [3.11.4] - 2026-01-23

### Added

- **Matteo Collina practitioner insight** (`guide/ecosystem/ai-ecosystem.md:1243`)
  - Node.js TSC Chair's perspective on AI-assisted development
  - "Bottleneck shift" thesis: judgment becomes the limiting factor, not typing speed
  - Key quote: "The human in the loop isn't a limitation. It's the point."
  - Context: Response to Arnaldi's "The Death of Software Development" (January 2026)
  - Data points: Review time +91% (CodeRabbit), 96% devs don't trust AI code (Sonar 2026)
  - Cross-reference added to `guide/roles/learning-with-ai.md` Practitioner Perspectives
  - YAML index entries: `practitioner_matteo_collina`, `practitioner_collina_source`

- **Claude Code releases tracking update** (`machine-readable/claude-code-releases.yaml`, `guide/core/claude-code-releases.md`)
  - Added v2.1.17: Fix for crashes on processors without AVX instruction support
  - Added v2.1.16: ⭐ New task management system with dependency tracking, VSCode native plugin management, OAuth remote session browsing
  - Added v2.1.15: npm installations deprecated (migrate to native installer), React Compiler performance improvements
  - New milestone: v2.1.16 (task management system)
  - New breaking change: npm installations deprecated

### Changed

- Updated landing site releases section with 3 new versions (v2.1.15-v2.1.17)
- Fixed landing release descriptions to match official CHANGELOG (v2.1.12, v2.1.11 corrections)
- Release count: 39 → 42

## [3.11.3] - 2026-01-23

### Added

- **Verification Loops pattern** (`guide/core/methodologies.md:145`)
  - Formalized pattern for autonomous iteration with tests as termination condition
  - Official Anthropic guidance: "Tell Claude to keep going until all tests pass"
  - Implementation options: Stop hooks, multi-Claude verification, explicit "DONE" markers

- **Eval Harness documentation** (`guide/core/methodologies.md:161`)
  - Definition: Infrastructure running evaluations end-to-end
  - Link to Anthropic source: "Demystifying Evals for AI Agents"

- **everything-claude-code ecosystem entry** (`machine-readable/reference.yaml`)
  - Added affaan-m/everything-claude-code (31.9k stars as of 2026-01-27, created 2026-01-18)
  - Author: Affaan Mustafa (Anthropic hackathon winner - Zenith project)
  - Unique patterns: hookify (conversational hooks), pass@k metrics, sandboxed subagents, strategic compaction
  - Plugin ecosystem: One-command installation, skill creator from git history
  - Comprehensive evaluation (Score 5/5): `docs/resource-evaluations/015-everything-claude-code-github-repo.md`
  - Caveats documented: hackathon win was indirect, Node.js hooks not officially recommended

- **deep_dive index entries** (`machine-readable/reference.yaml`)
  - `verification_loops`: guide/core/methodologies.md:145
  - `verification_loops_source`: Anthropic Best Practices link
  - `eval_harness`: guide/core/methodologies.md:161
  - `eval_harness_source`: Demystifying Evals link

- **Subscription Token Limits documentation** (`guide/ultimate-guide.md:1933-1995`)
  - Detailed token budgets by plan: Pro ~44K, Max 5x ~88-220K, Max 20x ~220K+ per 5-hour window
  - Opus/Sonnet consumption ratio (8-10×) explicitly documented
  - Clarification that "hours" = processing time, not direct token conversion
  - Link to `ccusage` community monitoring tool
  - Historical note on October 2025 undocumented limit reductions
  - **Sources**: Perplexity research (Jan 2026), Anthropic support docs, Reddit/GitHub community reports

- **Goose comparison section** (`guide/ecosystem/ai-ecosystem.md:1116-1204`)
  - New section "11.1 Goose: Open-Source Alternative (Block)"
  - Technical comparison table: Claude Code vs Goose on 7 criteria
  - GitHub stats: 15,400+ stars, 350+ contributors, Apache 2.0 license
  - Use cases and trade-offs with honest advantages/limitations
  - Hardware requirements by LLM type (cloud vs local models)
  - Quick start installation commands
  - Updated Table of Contents

- **machine-readable/reference.yaml**: Additional entries
  - `subscription_token_budgets: 1948`
  - `subscription_opus_ratio: 1946`
  - `subscription_monitoring: 1985`
  - `ai_ecosystem_goose: "guide/ecosystem/ai-ecosystem.md:1116"`
  - `ai_ecosystem_goose_comparison: "guide/ecosystem/ai-ecosystem.md:1132"`

- **Practitioner Insights section** (`guide/ecosystem/ai-ecosystem.md:1209-1241`)
  - New section "11.2 Practitioner Insights" for external validation
  - Dave Van Veen (PhD Stanford, Principal AI Scientist @ HOPPR)
  - Validates guide patterns: TDD, git worktrees, manual commits, planning phase
  - Academic credential: Co-author "Agentic Systems in Radiology" (ArXiv 2025)
  - Clarification: "English is the new programming language" attributed to Karpathy/Reddy, not Van Veen
  - Updated Table of Contents with new section

- **machine-readable/reference.yaml**: Practitioner insights entries
  - `practitioner_insights: "guide/ecosystem/ai-ecosystem.md:1209"`
  - `practitioner_dave_van_veen: "guide/ecosystem/ai-ecosystem.md:1213"`
  - `ecosystem.practitioner_insights.dave_van_veen` with full metadata

- **OCTO Technology reference** (`guide/roles/learning-with-ai.md:907`)
  - Added to "Practitioner Perspectives" section in Sources & Research
  - Article: "Le développement logiciel à l'ère des agents IA"
  - Key insights: pairs as minimal team unit (bus factor), bottleneck shifts to functional requirements
  - Caveat: managerial focus, useful context for team leads

### Changed

- **Subscription limits section** (`guide/ultimate-guide.md`) rewritten with concrete data
- **reference.yaml**: Updated line numbers for `subscription_limits` (1914 → 1933) and `ai_ecosystem_context_packing` (1114 → 1208)

### Research

- **Comprehensive fact-check** of everything-claude-code repository
  - Verified "Anthropic hackathon winner" claim (true for Zenith project, indirect for this repo)
  - Confirmed 16k+ stars growth in 5 days via GitCharts
  - Validated technical concepts (eval-harness, verification-loops) exist in Anthropic docs
  - Found "strategic-compact" term not in official sources (not adopted)
  - Confirmed Node.js hooks not recommended vs native shell

---

## [3.11.2] - 2026-01-22

### Added

- **Context Packing Tools section** (`guide/ecosystem/ai-ecosystem.md:1114`)
  - New section "12. Context Packing Tools" documenting gitingest, repo2txt usage patterns
  - Clarifies when to use external context extraction vs native Claude Code file access
  - Updated Table of Contents with sections 11 (AI Coding Agents Matrix) and 12
  - **machine-readable/reference.yaml**: Added `ai_ecosystem_context_packing` entry

- **Addy Osmani AI Coding Workflow reference** (`guide/core/methodologies.md:313`)
  - Added "My AI Coding Workflow in 2026" article to SDD & Spec-First sources
  - Validates spec-first, TDD, git checkpoints workflow patterns

- **MCP Tool Search documentation** (`guide/core/architecture.md`)
  - New section "MCP Tool Search (Lazy Loading)" with complete technical details
  - Explains how Claude Code uses Anthropic's Advanced Tool Use API feature (v2.1.7+)
  - Includes ASCII diagram of Tool Search flow
  - Documents 85% token reduction benchmark and accuracy improvements
  - Configuration guide for `ENABLE_TOOL_SEARCH=auto:N` syntax
  - Simon Willison quote on context pollution resolution
  - **Sources**: Anthropic Engineering blog, Scott Spence documentation, Perplexity verification
  - **machine-readable/reference.yaml**: Added `tool_search`, `tool_search_config`, `tool_search_deep_dive` entries

### Changed

- **Release notes enrichment** (`guide/core/claude-code-releases.md`)
  - v2.1.7: Added 85% token reduction stats, accuracy improvements, Anthropic blog link
  - v2.1.9: Added `auto:N` configuration examples and cross-reference to architecture.md

### Fixed

- **Template count**: Corrected from 83 to 82 (actual count in examples/)

---

## [3.11.1] - 2026-01-22

### Added

- **Agent Vibes TTS Integration** (`examples/integrations/agent-vibes/`)
  - **8 documentation files, 2,400+ lines**: Complete text-to-speech integration guide
  - **Integration guide** (`README.md`): Quick start with decision matrix, 30-second overview, architecture diagram, essential commands
  - **Installation guide** (`installation.md`): 18-minute step-by-step procedure across 5 phases (bash 5.x, dependencies, Agent Vibes, Piper TTS, French voices)
  - **Voice catalog** (`voice-catalog.md`): Detailed catalog of 15 voices (4 French models with 128 total speakers via multi-speaker models)
  - **Troubleshooting guide** (`troubleshooting.md`): Solutions for 7 common issues with diagnostic script
  - **Workflow** (`guide/workflows/tts-setup.md`): 18-minute guided workflow with decision scoring system and 5 checkpointed phases
  - **Custom hook example** (`examples/hooks/bash/tts-selective.sh`): Selective TTS activation (errors only) with pattern matching
  - **Project template** (`examples/claude-md/tts-enabled.md`): CLAUDE.md template for TTS-enabled projects with team guidelines
  - **Key features**:
    - Offline TTS with Piper (no cloud dependency)
    - French voice support (4 models: tom, siwis, upmc, mls-124speakers)
    - Mute hierarchy system (project override → project mute → global mute)
    - Provider auto-detection (macOS Say, Piper TTS)
    - Audio effects pipeline (reverb, echo, background music)
  - **Documentation**: Added section 5.1 "Text-to-Speech Tools" in `guide/ecosystem/ai-ecosystem.md` (80+ lines with tables, quick start, recommendations)

### Changed

- **Template count**: 71 → 83 (+12 templates including integration docs, hook, workflow, CLAUDE.md template)
- **README.md**: Updated badges (71→83), template counts (66→83, 74→83), version footer (3.11.0→3.11.1)
- **guide/README.md**: Added TTS workflow reference and ai-ecosystem.md section update
- **machine-readable/reference.yaml**: Added 8 TTS-related entries (tts_integration_guide, tts_installation, tts_voice_catalog, tts_troubleshooting, tts_workflow, tts_ai_ecosystem, tts_hook_example, tts_claude_md_template)
- **.gitignore**: Added audio file exclusions (*.wav, *.mp3, *.onnx)

### Context

- **Use case**: Add audible narration to Claude Code for multitasking during code reviews, debugging, or long-running operations
- **Target audience**: Developers wanting TTS feedback without cloud dependencies, preference for high-quality French voices
- **Methodology**: Community MCP server (Agent Vibes v3.0.0) + Piper TTS + offline voice models from Hugging Face

---

## [3.11.0] - 2026-01-21

### Added

- **Skill: Design Patterns Analyzer** (`examples/skills/design-patterns/`)
  - **9 files, 5,690 lines**: Comprehensive GoF design patterns analyzer with stack-aware suggestions
  - **SKILL.md** (450 lines): Main instructions with 3 operating modes (Detection, Suggestion, Evaluation)
  - **reference/** (2,140 lines): Complete documentation for 23 GoF patterns
    - `patterns-index.yaml`: Machine-readable index with metadata (difficulty, frequency, confidence)
    - `creational.md`: 5 patterns (Singleton, Factory Method, Abstract Factory, Builder, Prototype)
    - `structural.md`: 7 patterns (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy)
    - `behavioral.md`: 11 patterns (Observer, Strategy, State, Command, etc.)
  - **signatures/** (1,420 lines): Detection and suggestion rules
    - `stack-patterns.yaml`: 8 stacks detection + native alternatives (React, Angular, NestJS, Vue, Express, RxJS, Redux, ORMs)
    - `detection-rules.yaml`: Grep patterns and heuristics for 23 patterns
    - `code-smells.yaml`: Mapping from 15+ code smells to suggested patterns
  - **checklists/** (450 lines): Quality evaluation system (5 criteria: Correctness, Testability, SRP, Open/Closed, Documentation)
  - **Key features**:
    - Detects 23 Gang of Four design patterns in TypeScript/JavaScript codebases
    - Stack-aware detection (analyzes package.json, tsconfig.json, config files)
    - Prefers stack-native alternatives (e.g., React Context over Singleton, RxJS over manual Observer)
    - Code smell detection with refactoring suggestions
    - Quality scoring (0-10 with weighted criteria)
  - **Documentation**: Added comprehensive example in guide section 5.4 (149 lines) with usage patterns, stack-native recommendations table, detection methodology, and integration examples
  - **Tested on**: Méthode Aristote codebase (Next.js 15.5 + React 19 + tRPC + Prisma)
    - Found: Factory Method (8.2/10), Observer via EventSource (9.1/10), Strategy-like patterns, Repository via Prisma
    - Suggested: React Context instead of Singleton, Strategy pattern for switch statements
    - Identified: Large service files (2,396 and 2,221 lines) requiring extraction

### Changed

- **Template count**: 65 → 66 (added design-patterns skill)
- **examples/README.md**: Added design-patterns entry with ⭐ marker
- **machine-readable/reference.yaml**: Added design_patterns_skill entries (line numbers, location, modes, coverage)

### Context

- **Use case**: Analyze existing patterns, suggest refactoring with stack-native patterns, evaluate pattern implementation quality
- **Target audience**: Developers working on TypeScript/JavaScript projects wanting to detect anti-patterns and improve architecture
- **Methodology**: Glob → Grep → Read pipeline for detection, stack-aware suggestions prioritizing framework idioms

---

## [3.10.0] - 2026-01-21

### Added

- **Section 9.18: Codebase Design for Agent Productivity** (~1809 lines)
  - **Based on**: [Agent Experience Best Practices](https://marmelab.com/blog/2026/01/21/agent-experience.html) by François Zaninotto (Marmelab, Jan 21, 2026)
  - **Additional validation**: Netlify AX framework (2025), Speakeasy implementation guide, ArXiv papers on agent context engineering
  - **9.18.1 Paradigm Shift**: Traditional vs AI-native codebase design, Agent Experience (AX) framework, when to invest in AX
  - **9.18.2 Domain Knowledge Embedding**: CLAUDE.md advanced patterns, code comments (what vs how), Architecture Decision Records (ADRs)
  - **9.18.3 Code Discoverability**: Complete terms vs abbreviations, synonyms in comments, JSDoc tags, directory READMEs
  - **9.18.4 Token Efficiency**: Split large files (500 line guideline), remove obvious comments, verbose flags for debug output
  - **9.18.5 Testing for Autonomy**: Why TDD is more critical for agents, tests written manually (not delegated), browser automation, coverage as guardrail
  - **9.18.6 Conventions & Patterns**: Standard design patterns agents know, "boring tech" advantage, ADRs for custom architectures
  - **9.18.7 Guardrails & Validation**: Hooks as anti-pattern validators, "tainted code" philosophy, PR reviews, validation layers
  - **9.18.8 Serendipity & Cross-References**: Module cross-references, self-documenting commands, embedded technical docs
  - **9.18.9 Usage Instructions**: Doc blocks with examples, Context7 MCP for official docs, sensible defaults
  - **9.18.10 Decision Matrix**: When to optimize for agents vs humans, agent-friendly codebase checklist (33-point), quick wins
- **Section 3.1 enrichment**: Added cross-reference to Section 9.18 for advanced domain knowledge patterns
- **Section 9.11 new subsection**: "Codebase Structure Pitfalls" with ❌/✅ patterns and cross-reference to Section 9.18
- **Table of Contents**: Added Section 9.18 entry
- **Section 9 Recap**: Added "Codebase Design for Agents" item to quality awareness checklist
- **machine-readable/reference.yaml**: Added `codebase_design_agents` entry with line number and source attribution

### Changed

- **VERSION**: Bumped from 3.9.11 to 3.10.0 (minor version bump for major new section)
- **Guide size**: Increased from ~11,560 lines to 13,425 lines (+1,865 lines, +16.1%)

### Context

- **Gap identified**: Guide lacked comprehensive codebase design patterns for agent productivity
- **Timing**: Article published 2 days ago (Jan 21, 2026), validated by Netlify AX research and ArXiv papers
- **Target audience**: Teams extensively using Claude Code (>50% commits by agents), greenfield projects
- **Complementary sources**: Netlify "Agent Experience" research, Speakeasy API DX guide (includes AX patterns)

---

## [3.9.11] - 2026-01-21

### Added
- **Production Safety Rules Guide** (`guide/security/production-safety.md`): Comprehensive production safety rules for teams deploying Claude Code in production environments
  - Port Stability: Prevent accidental port changes breaking local dev/Docker/deployed configs
  - Database Safety: Backup enforcement via PreToolUse hooks to prevent data loss
  - Feature Completeness: No TODOs for core functionality rules
  - Infrastructure Lock: Protect docker-compose.yml, Dockerfile, .env.example, terraform/
  - Dependency Safety: Block unapproved npm packages with permission deny rules
  - Pattern Following: Enforce codebase conventions via CLAUDE.md and automated validation
- Cross-references to production-safety.md in `ultimate-guide.md` section 3.1 and `adoption-approaches.md` (Medium/Large teams)
- New deep_dive entry in `machine-readable/reference.yaml` for production safety topics

### Context
- Adapted from community "10 non-negotiable CLAUDE.md rules" (6/10 rules integrated, 4/10 already covered in existing guide)
- Verified gaps using grepai searches: Rule #5 (ports) genuinely absent, Rule #6 (DB) partially covered
- Target audience: 20% production teams (vs 80% learners in main guide)

---

## [3.9.10] - 2026-01-21

### Added

- **Section 9.17: Scaling Patterns - Multi-Instance Workflows** (~390 lines)
  - **Boris Cherny case study**: 259 PRs/30 days with 5-15 parallel Claude instances (InfoQ interview, Jan 2026)
  - **Anthropic internal study**: 132 engineers, +50% productivity, 21.2 consecutive autonomous actions (Aug 2025)
  - **Decision matrix by team size**: Solo (❌) → Startup (⚠️) → Scale-up (✅) → Enterprise (✅)
  - **Cost-benefit analysis**: $240-1000/month with ROI thresholds (3-5% productivity gain to justify)
  - **Git worktrees foundation**: Critical prerequisite for multi-instance isolation (non-negotiable)
  - **Orchestration frameworks**: Headless PM (open-source REST API), Cursor, Windsurf
  - **Progressive implementation**: 3-phase guide (single mastery → dual testing → multi-instance)
  - **Monitoring guidelines**: Merge conflicts, PRs/month, test pass rates, skill atrophy
  - **Anti-patterns**: When NOT to use (legacy monoliths, solo devs, <$500/mo budget, <5 PRs/week)
  - **Primary sources**: InfoQ "Claude Code Creator Workflow" (2026-01-09), Anthropic Research "How AI is Transforming Work" (2025-08)
- **machine-readable/reference.yaml**: 10 new entries for multi-instance topics
  - `multi_instance_workflows`, `boris_cherny_case_study`, `anthropic_study_metrics`
  - `git_worktrees_multi_instance`, `multi_instance_costs`, `orchestration_frameworks`
  - `headless_pm_framework`, `multi_instance_implementation`, `multi_instance_monitoring`
  - `multi_instance_decision_matrix`

### Fixed

- **Table of Contents**: Added missing sections 9.12-9.17 (git, cost, methodologies, prompts, teleportation, multi-instance)
- **Section 9 checklist**: Added multi-instance scaling item to advanced workflows recap

## [3.9.9] - 2026-01-20

### Changed

- **README.md: Ecosystem cross-reference** — Added bidirectional link to Claude Cowork Guide
  - New section "Not a Developer?" (lines 75-81) linking to Cowork Guide for non-technical users
  - Improves ecosystem discovery and audience routing between dev and non-dev guides
  - Cowork Guide also received reciprocal cross-reference (commit ceadd82 in Cowork repo)
- **CLAUDE.md: Version reference update** — Updated current version from 3.9.7 to 3.9.9

### Fixed

- **README.md: Template count correction** — Fixed template count from 69 to accurate count of 65
  - Badge (line 9): 69 → 65
  - Examples Library summary (line 198): 66 → 65
  - Ecosystem table (line 341): 66 → 65
  - Verified with `find examples/ -type f \( -name "*.md" -o -name "*.sh" ... \) ! -name "README.md" | wc -l`
  - Original count of 69 in v3.9.9 release was overcounted by 4 templates

## [3.9.9] - 2026-01-20

### Added

- **DevOps & SRE Guide** — Comprehensive infrastructure diagnosis guide (~900 lines)
  - **New file**: `guide/ops/devops-sre.md` — The FIRE Framework for infrastructure troubleshooting
    - **F**irst Response → **I**nvestigate → **R**emediate → **E**valuate
    - Kubernetes troubleshooting with copy-paste prompts by symptom (CrashLoopBackOff, OOMKilled, ImagePullBackOff, etc.)
    - Solo incident response workflow (designed for 3 AM scenarios)
    - Multi-agent pattern for post-incident analysis
    - IaC patterns: Terraform, Ansible, GitOps workflows
    - Guardrails & team adoption checklist
    - Claude limitations table (what Claude can't do for DevOps)
    - Case studies: Production outage root cause, OpsWorker.ai MTTR reduction
  - **New file**: `examples/agents/devops-sre.md` — DevOps/SRE agent persona (~130 lines)
    - FIRE framework implementation
    - Kubernetes, network, and resource debugging checklists
    - Response templates (assessment, root cause, remediation)
    - Safety rules for production environments
  - **New file**: `examples/claude-md/devops-sre.md` — CLAUDE.md template for DevOps teams (~170 lines)
    - Infrastructure context configuration
    - Environment, service map, access patterns
    - Team conventions and runbook format
    - Customization guides (K8s-heavy, Terraform-heavy, multi-cloud)
  - **Updated**: `guide/ultimate-guide.md` — Added DevOps & SRE Guide reference after Section 5.4
  - **Updated**: `machine-readable/reference.yaml` — Added 11 DevOps/SRE entries
  - **Updated**: `examples/README.md` — Added agent and CLAUDE.md template to indexes
  - **Updated**: `README.md` — Added DevOps/SRE learning path, updated templates count (69)

## [3.9.8] - 2026-01-20

### Added

- **AI Ecosystem: AI Coding Agents Matrix integration** — Comprehensive ecosystem resource
  - **New Section 11** in `guide/ecosystem/ai-ecosystem.md` (~60 lines): "AI Coding Agents Matrix"
    - Interactive comparison of 23 AI coding agents across 11 technical criteria
    - What Is It, Why It's Useful, Complementarity table, Interactive Features, Limitations
    - Positioning: Discovery (Matrix) → Mastery (This Guide)
    - Maintainers: Packmind (Cédric Teyton, Arthur Magne)
  - **Enhanced `machine-readable/reference.yaml`** (lines 397-412):
    - Added: GitHub repo, maintainers, license (Apache-2.0), tech stack (React, Vite, Tailwind)
    - Added: 4 features (11 criteria, sortable/filterable, community-driven, JSON-based)
    - Added: positioning note, data freshness warning
  - **Updated `README.md`** (Section 8: Ecosystem):
    - Converted complementary resources to comparison table (4 projects)
    - Added dedicated paragraph for AI Coding Agents Matrix with use case
    - Positioning: "Use Matrix to discover/compare → Choose Claude Code → Use this guide to master it"
  - Cross-promotion with [coding-agents-matrix.dev](https://coding-agents-matrix.dev/) (updated Jan 19, 2026)

## [3.9.7] - 2026-01-20

### Changed

- **CLAUDE.md: Model Configuration** — OpusPlan workflow recommendation (replaces thinking mode disable)
  - Hybrid intelligence: Opus (planning) → Sonnet (execution)
  - Task breakdown table: doc edits, version sync, restructuring, research, consistency checks
  - Cost optimization: 10-20% Opus planning, 80-90% Sonnet execution
  - Workflow: `/model opusplan` → `Shift+Tab × 2` (plan) → `Shift+Tab` (execute)

## [3.9.6] - 2026-01-20

### Added

- **ultimate-guide.md: Section 5.5 "Infrastructure as Code Skills"** — New community skill repository (~50 lines)
  - Anton Babenko's terraform-skill (creator of terraform-aws-modules, 1B+ downloads)
  - Covers testing, module development, CI/CD, security, patterns
  - Notable for marketplace distribution (.claude-plugin/), structured references, test coverage
  - Source: [GitHub repo](https://github.com/antonbabenko/terraform-skill)

- **ultimate-guide.md: Section 1.7 "Trust Calibration: When and How Much to Verify"** — New section (~155 lines)
  - Research-backed stats table (ACM, Veracode, CodeRabbit, Cortex.io sources)
  - Verification spectrum (boilerplate → security-critical)
  - Solo vs Team verification strategies with workflow diagrams
  - "Prove It Works" checklist (functional, security, integration, quality)
  - Anti-patterns table (6 common mistakes)
  - Attribution to Addy Osmani's "AI Code Review" (Jan 2026)

- **ultimate-guide.md: New pitfall** — "Trust AI output without proportional verification"

- **learning-with-ai.md: Section 3 "The Reality of AI Productivity"** — New section (~55 lines)
  - Productivity curve phases (Wow Effect → Targeted Gains → Sustainable Plateau)
  - High-gain vs low/negative-gain task categorization
  - Team success factors (guidelines, code review, mentorship)

- **reference.yaml**: `trust_calibration` (line 1039), `community_skills_cybersec` (4786), `community_skills_iac` (4871), `vibe_coding_trap` (81)

- **learning-with-ai.md: "The Vibe Coding Trap" section** — New anti-pattern documentation (~15 lines)
  - Term coined by Andrej Karpathy (Feb 2025, Collins Word of the Year 2025)
  - Symptoms checklist + Karpathy's caveat ("throwaway projects" vs production)
  - Links to UVAL Protocol as antidote

- **IDEAS.md: "Vibe Coding Discourse"** — New Watching entry
  - Tracks "developer as architect" narrative evolution
  - Source: Craig Adam "Agile is Out, Architecture is Back" (Medium)

- **learning-with-ai.md: External Resources** — Added [leerob.com/ai](https://leerob.com/ai) link
  - AI fundamentals for engineers (ML, neural networks, transformers, tokenization)
  - Score 3/5 eval: complement utile, not deep integration
  - Source: Lee Robinson (Nov 2024)

### Changed

- **reference.yaml**: Complete line number synchronization (~55 entries updated)
  - Guide grew from ~9900 to 11154 lines; all deep_dive references now accurate
  - Added "Updated 2026-01-20" comment for tracking
  - Major corrections: cost_optimization (8047→8833), interaction_loop (1063→1299), etc.

- **ultimate-guide.md**: Section renumbering — "Eight Beginner Mistakes" moved 1.7 → 1.8
- **learning-with-ai.md**: Three Patterns productivity trajectory table, 70/30 Split research callout, Sources section (+5 sources)
- **learning-with-ai.md**: ToC renumbered (14 sections, was 13)

## [3.9.5] - 2026-01-19

### Added

- **IDEAS.md "Watching" section** — New category for tracking ideas awaiting demand
  - Multi-LLM Consultation Patterns (Gemini/GPT-4 as second opinion)
  - Research done: bash scripts vs Plano (overkill for solo devs)
  - Criteria: implement if 3+ reader requests

### Changed

- **README.md restructuration** — Reduced cognitive load by ~40% (benchmarked)
  - Removed duplicate "5 Rules to Remember" section (content already in "Golden Rules")
  - Added collapsible Table of Contents with 4 learning paths:
    - Beginner Path (TL;DR, Get Started, Golden Rules)
    - Developer Path (By Role, Guide Navigation, Examples)
    - Advanced Path (Audit, Quiz, Ecosystem)
    - Reference (Toolkit, About, Contributing)
  - Simplified "Choose Your Path" section (4 rows → 3, references ToC)
  - Updated TL;DR link from `#5-rules-to-remember` → `#-golden-rules`
  - Net change: +19 lines (757 total), improved navigation

## [3.9.4] - 2026-01-19

### Added

- **Session Teleportation documentation** — New Section 9.16 in Ultimate Guide (~105 lines)
  - Evolution timeline (2.0.24 → 2.1.0)
  - Commands reference (`%`, `--teleport`, `/teleport`, `/tasks`, `/remote-env`, `Ctrl+B`)
  - Prerequisites (GitHub App, clean git state, same account)
  - Workflow example with step-by-step
  - Environment support table (CLI, VS Code, Cursor, Web, iOS)
  - Current limitations (research preview, unidirectional, GitHub only)
  - Troubleshooting table
  - Best practices
  - Environment variables (`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`)
- Updated Section 9 Recap with "Advanced Workflows" category
- Updated `guide/cheatsheet.md` with teleportation commands
  - Essential Commands: `/teleport`, `/tasks`, `/remote-env`
  - Keyboard Shortcuts: `Ctrl+B`
  - CLI Flags: `--teleport`
- Updated `machine-readable/reference.yaml`
  - New `session_teleportation` deep_dive entry
  - Commands: `/teleport`, `/tasks`, `/remote-env`
  - Shortcuts: `Ctrl+B`
  - CLI: `--teleport`
  - Line numbers updated for sections after 9.15

## [3.9.3] - 2026-01-19

### Added

- **Claude Cowork documentation** — Complete guide for the new agentic desktop feature
  - `guide/cowork.md` (NEW, ~460 lines) — Full documentation
    - Architecture overview (local-first, sub-agents, no code execution)
    - Comparison: Claude Code vs Cowork vs Projects
    - 5 detailed use cases (file org, expenses, reports, travel, meetings)
    - Security best practices (no official docs exist yet)
    - Developer ↔ Non-Developer workflow patterns
    - Known issues & troubleshooting
    - Availability & roadmap
  - `guide/ecosystem/ai-ecosystem.md` Section 9 (~90 lines) — Condensed integration guide
    - Quick comparison table
    - When to use what decision flow
    - Security considerations summary
    - Cross-reference to full guide
  - `guide/ultimate-guide.md` — Cowork subsection in Section 11
    - Comparison table and collaboration pattern
    - Table of Contents updated
  - `machine-readable/reference.yaml` — 8 new deep_dive entries for Cowork
  - Updated `guide/README.md` navigation table
  - Updated main `README.md` AI Ecosystem entry

## [3.9.2] - 2026-01-19

### Added

- **Alternative Providers section** in `guide/ecosystem/ai-ecosystem.md` (~55 lines)
  - Documents existence of community workarounds (ANTHROPIC_BASE_URL, etc.)
  - Clear disclaimer: not tested, not recommended, not supported
  - Reasons to avoid: feature degradation, ToS risks, no support
  - Better alternatives table: Aider for local models, Continue.dev for multi-provider
  - External reading pointers (no step-by-step instructions intentionally)
  - Updated Table of Contents
  - Added `ai_ecosystem_alternative_providers` reference in `reference.yaml`

## [3.9.1] - 2026-01-19

### Added

- **AI Ecosystem: Complementary Tools** — New Section 11 documenting tool complementarity
  - `guide/ultimate-guide.md` Section 11 (~250 lines)
    - 11.1 Why Complementarity Matters — Claude Code strengths vs gaps
    - 11.2 Tool Matrix — Decision guide for when to use which tool
    - 11.3 Practical Workflows — 4 pipelines (Research→Code, Visual→Code, Documentation, Presentation)
    - 11.4 Integration Patterns — Full workflows with budget recommendations
  - `guide/ecosystem/ai-ecosystem.md` (NEW, ~750 lines)
    - Detailed guide for each complementary tool
    - Perplexity AI (research with verified sources)
    - Google Gemini (image understanding → code)
    - Kimi/Moonshot (PPTX generation, 128K context)
    - NotebookLM (doc synthesis + audio overviews)
    - IDE tools (Cursor, Windsurf, Cline)
    - UI Prototypers (v0, Bolt, Lovable)
    - Ready-to-use prompts appendix
    - Cost optimization strategies
  - Updated `guide/README.md` with navigation link
  - Updated main `README.md` navigation table
  - Updated `machine-readable/reference.yaml` with 6 new line number references

### Changed

- **tools/mobile-access.md** - Enhanced with verified data and alternatives
  - Added Architecture Comparison section with 3 ASCII diagrams (ttyd, Happy Coder, Remoto.sh)
  - Restructured comparison table with Type/Pros/Cons/ToS/Stars columns
  - Added Happy Coder section: 7.8K ⭐ (verified 2026-01-19), MIT, Tauri/Expo stack, ToS-safe
  - Added Remoto.sh warning: ToS risk documented (Anthropic §4.2 proxy policy)
  - Added Sources section with all referenced projects
  - Updated footer with data verification date
  - File expanded from 300 to 385 lines

## [3.9.0] - 2026-01-19

### Added

- **Semantic Anchors** — New concept integrated for better LLM prompting
  - Section 2.7 "Semantic Anchors" in `guide/ultimate-guide.md` (~93 lines)
    - Explains how precise vocabulary helps LLMs activate correct patterns
    - Common anchors table (vague → precise) with explanations
    - Integration examples with CLAUDE.md and XML tags
  - `examples/semantic-anchors/anchor-catalog.md` (NEW, ~320 lines)
    - Comprehensive catalog organized by domain (Testing, Architecture, Design, etc.)
    - Before/after examples showing prompt improvement
    - CLAUDE.md template with anchors integrated
  - Source attribution: Alexandre Soyer, [github.com/LLM-Coding/Semantic-Anchors](https://github.com/LLM-Coding/Semantic-Anchors) (Apache-2.0)
  - Section numbering fixed: 2.6 Data Flow → 2.8, 2.7 Under the Hood → 2.9

- **Subscription Plans & Limits** — New section documenting subscription concepts
  - Section "#### Subscription Plans & Limits" in `guide/ultimate-guide.md` (~42 lines)
    - Explains message windows, hybrid counting, weekly caps, model weighting
    - Tier-specific strategies (limited → unlimited quota)
    - Links to official pricing page (concepts only, no volatile numbers)
  - Updated `machine-readable/reference.yaml` with `subscription_limits: 1750`
  - Fixed drifted line numbers in reference.yaml (commands_table, shortcuts_table, etc.)

- **6 new slash commands** (Sprint 1 + Sprint 2 implementation)
  - `examples/commands/catchup.md` - Restore context after `/clear` (137 lines)
    - Git history analysis (last 10 commits, recent diffs)
    - TODO/FIXME scanning across codebase
    - Project state summary with actionable next steps
  - `examples/commands/security.md` - Quick OWASP security audit (149 lines)
    - Secrets detection (API keys, tokens, passwords)
    - Injection vulnerability scanning (SQL, XSS, command)
    - Dependency audit integration
    - Severity-based output (Critical/High/Medium/Low)
  - `examples/commands/refactor.md` - SOLID-based code improvements (195 lines)
    - SOLID violation detection with examples
    - Risk level assessment for each suggestion
    - Atomic commit recommendations
  - `examples/commands/explain.md` - Code explanations with 3 depth levels (174 lines)
    - Simple (TL;DR), Standard, Deep modes
    - Supports files, functions, concepts, flows
    - Example outputs at each level
  - `examples/commands/optimize.md` - Performance analysis and roadmap (195 lines)
    - Runtime, memory, database, bundle analysis
    - Profiling commands per language
    - Prioritized optimization roadmap
  - `examples/commands/ship.md` - Pre-deploy checklist (189 lines)
    - Blocker/High/Recommended categorization
    - Tests, lint, build, secrets, security audit
    - Migration and rollback verification

- **Named Prompting Patterns** section in `guide/ultimate-guide.md` (Section 9.15, ~155 lines)
  - **"As If" Pattern**: Set quality expectations ("Implement as if senior engineer at Google")
  - **Constraint Pattern**: Force creative solutions ("Solve without new dependencies")
  - **"Explain First" Pattern**: Force planning before implementation
  - **"Rubber Duck" Pattern**: Collaborative debugging through questions
  - **Incremental Pattern**: Gradual complexity building
  - **Boundary Pattern**: Define scope and constraints explicitly
  - Combination examples and anti-patterns

- **Mermaid Diagram Generation** section in `guide/ultimate-guide.md` (Section 9.7, ~90 lines)
  - 6 diagram types: Flowchart, Sequence, Class, ER, State, Gantt
  - Prompt templates for each type
  - Visualization tools reference (GitHub, mermaid.live, VS Code)

- **Eight Beginner Mistakes** checklist in `guide/ultimate-guide.md` (Section 1.7, ~70 lines)
  - Based on competitive analysis vs Jo Vinkenroye's Mastery series
  - 8 common mistakes with symptoms and solutions
  - Prevention patterns for each mistake

- **Commands vs Skills vs Agents** enhanced comparison table (Section 5.1, ~50 lines)
  - Detailed comparison across 8 aspects
  - When to use each type with decision criteria
  - Combination patterns for complex workflows

- **Learning with AI guide** for junior developers (`guide/roles/learning-with-ai.md`, ~900 lines)
  - **Quick Self-Check** (L31-81): 5 diagnostic questions to assess AI dependency
  - **Three Developer Patterns** (L82-126): Dependent, Avoidant, Augmented profiles with action paths
  - **UVAL Protocol** (L127-352): Understand → Verify → Apply → Learn framework
  - **Claude Code for Learning** (L353-469): CLAUDE.md configuration, slash commands, hooks
  - **Breaking Dependency** (L470-517): Recovery plan for over-reliant developers
  - **Embracing AI** (L518-709): Onboarding for AI-skeptical developers
  - **30-Day Progression Plan** (L710-769): Week-by-week AI ratio progression
  - **Red Flags Checklist** (L770-850): Warning signs and corrective actions

- **Learning mode templates** (3 new files)
  - `examples/claude-md/learning-mode.md`: CLAUDE.md template for learning-focused development
  - `examples/commands/quiz.md`: /quiz slash command for self-testing
  - `examples/hooks/bash/learning-capture.sh`: Stop event hook for daily learning capture

- **Wireframing & Figma MCP documentation** in `guide/ultimate-guide.md` (+143 lines)
  - Wireframing tools comparison (Excalidraw, tldraw, Frame0, Paper+Photo)
  - Figma MCP Integration with official Anthropic server
  - Image Optimization for Claude Vision with resolution guidelines

### Changed

- **README.md** updates:
  - Lines badge: 9,800+ → 10,500+
  - Templates badge: 56 → 63
  - Commands table: Added 6 new commands
  - Version: 3.8.2 → 3.9.0
  - Added prominent "Visit Website" badge linking to landing page

- **examples/README.md**: Added 6 new commands to Commands table

- **scripts/install-templates.sh**: Updated commands list with new templates

- **guide/ultimate-guide.md**:
  - Table of Contents updated with sections 1.6, 1.7
  - Section 9 Recap enhanced with Communication Patterns checklist
  - Guide expanded by ~385 lines (9,881 → 10,266)

- **Semantic search tools priority**: grepai now recommended over mgrep
  - Sections reordered (grepai first as "Recommended", mgrep as "Alternative")
  - `guide/cheatsheet.md`: MCP Servers table updated
  - Rationale: grepai is fully open-source, runs locally (privacy)

### Stats

- 6 new command files created (~1,039 lines total)
- ~385 lines added to ultimate-guide.md
- Templates count: 56 → 63
- Focus on competitive analysis gaps vs community resources
- Named patterns and beginner-friendly content added

---

## [3.8.2] - 2026-01-17

### Added

- **Landing Site Synchronization System**
  - New script `scripts/check-landing-sync.sh` verifying 4 metrics:
    - Version (`VERSION` vs landing index.html)
    - Templates count (`find examples/` vs landing badges)
    - Quiz questions (`questions.json` vs index.html + quiz.html)
    - Guide lines (with ±500 tolerance)
  - CLAUDE.md updated with sync documentation and expected output
  - Landing site CLAUDE.md created with sync workflow and line numbers

### Fixed

- **Templates count corrected**: 87 → 49 in README.md badges and text
  - Badge count was wrong since original creation
  - Actual count verified with `find examples/ -type f`

---

## [3.8.1] - 2026-01-16

### Added

- **PDF Generation documentation**
  - New workflow guide: `guide/workflows/pdf-generation.md`
  - New skill template: `examples/skills/pdf-generator.md`
  - Covers Quarto + Typst stack, YAML frontmatter, design system, troubleshooting
  - Updated `machine-readable/reference.yaml` with deep_dive entries

### Changed

- **Whitepapers PDF template modernized** (internal)
  - New color palette: Slate + Indigo (WCAG AA compliant)
  - Typography: Inter font, JetBrains Mono for code
  - Cover page redesign: Claude Code logo, minimal white design
  - Fixed nested markdown code blocks (42 blocks using `````markdown`)
  - Added clickable GitHub links for all script references

---

## [3.8.0] - 2026-01-16

### Added

- **TL;DR Quick Start section** in README.md
  - Quick reference table: Cheat Sheet (2 min), Starter CLAUDE.md (30 sec), 5 Rules (1 min)
  - Copy-paste CLAUDE.md template directly in README
  - Optimized for TTFV (Time-to-First-Value) < 5 minutes
  - Prominent badges at top: version, license, Claude Code support

- **French Whitepapers documentation** in README.md
  - New section documenting 8 whitepapers in French (~185 pages total)
  - Learning paths by profile: Junior (25 min), Senior (1h15), Tech Lead (1h15)
  - Files in `whitepapers/` directory using Quarto (.qmd) format

- **CODE_OF_CONDUCT.md** (new file)
  - Contributor Covenant v2.1
  - Standard OSS community guidelines

- **Distribution playbooks** (internal, gitignored)
  - `claudedocs/distribution-playbook.md`: Ready-to-use content for awesome-claude-code PR, Reddit, dev.to, Twitter
  - `claudedocs/github-discussions-setup.md`: Step-by-step GitHub Discussions setup
  - French distribution strategy: Dev With AI Slack, LinkedIn FR

### Changed

- **CONTRIBUTING.md completely rewritten**
  - Added welcome message and contribution types table
  - Clear PR process with checklist
  - Quality checklist before submitting
  - References to GitHub Discussions and Code of Conduct

- **README.md restructured**
  - "Why This Guide" section rewritten for clarity
  - Repository structure updated to include whitepapers/
  - Dev With AI community reference added

### Internal

- Added `claudedocs/` and `whitepapers/` to `.gitignore` (internal docs)

---

## [3.7.1] - 2026-01-15

### Added

- **Intellectual Property Considerations** section in `guide/security/data-privacy.md`
  - Disclaimer about legal advice limitations
  - Key considerations: ownership, license contamination, vendor indemnification, sector compliance
  - Guidance to consult legal counsel for specific situations

---

## [3.7.0] - 2026-01-15

### Added - Session Search v2.1

Major upgrade to the session search utility (`cs`) with new features and bug fixes.

#### New Features

| Feature | Description | Example |
|---------|-------------|---------|
| **Multi-word AND search** | All words must match (was broken in v1) | `cs "prisma migration"` |
| **Project filter** | Filter by project name (substring) | `cs -p myproject "bug"` |
| **Date filter** | Filter by date (today, 7d, YYYY-MM-DD) | `cs --since 7d` |
| **JSON output** | Machine-readable output for scripting | `cs --json "api" \| jq .` |
| **Timeout** | 3-second timeout prevents long searches | Automatic |
| **Clean previews** | XML tags stripped, unicode filtered | No more `<local-command-caveat>` |

#### Performance

| Operation | Time |
|-----------|------|
| Cache lookup | ~16ms |
| Index rebuild | ~6s (239 sessions) |
| Fulltext search | 3-4s (timeout-bounded) |

#### Usage Examples

```bash
cs                          # 10 most recent sessions
cs "Prisma migration"       # Multi-word AND search
cs -p MethodeAristote "api" # Filter by project + keyword
cs --since 7d               # Last 7 days
cs --since today -n 20      # Today's sessions
cs --json "test" | jq .     # JSON for scripting
```

#### Files Modified

- `examples/scripts/session-search.sh` - Script v2.1 (367 lines)
- `guide/ops/observability.md` - Documentation updated with new options

#### Quality Score Progression

| Version | Score | Key Improvements |
|---------|-------|------------------|
| v1.0 | 6/10 | Basic functionality |
| v2.0 | 8/10 | +AND search, +filters, +JSON |
| v2.1 | **9.3/10** | +JSON fix, +clean previews |

---

## [3.6.1] - 2026-01-15

### Fixed - Critical Factual Corrections

Major audit identifying and correcting factual errors that could mislead users about Claude Code's actual behavior.

#### 1. `--add-dir` Flag (Wrong Description → Permissions, Not Context Loading)

**Before**: Documented as "loading directories into context" / "focused context"
**Reality**: Grants tool access to directories outside CWD (permissions only, no token impact)

| File | Correction |
|------|------------|
| guide/ultimate-guide.md | "focused context" → "allow tool access outside CWD" |
| guide/cheatsheet.md | "Add directory" → "Allow access outside CWD" |
| machine-readable/reference.yaml | "limit loaded dirs" → "access dirs outside CWD" |
| quiz/questions/10-reference.yaml | Question + explanation corrected |

#### 2. `excludePatterns` → `permissions.deny` (Never Existed)

**Before**: Documented `excludePatterns` as a valid settings key
**Reality**: Never existed - the correct syntax is `permissions.deny`

| File | Correction |
|------|------------|
| guide/ultimate-guide.md | New syntax + warning |
| guide/security/data-privacy.md | New syntax + deprecation note |
| examples/scripts/audit-scan.sh | Detection + message fixed |
| tools/audit-prompt.md | 3 references corrected |

#### 3. `.claudeignore` Removed (Does Not Exist)

**Before**: Documented as a file exclusion mechanism like `.gitignore`
**Reality**: Not an official feature - use `permissions.deny` instead

| File | Correction |
|------|------------|
| guide/ultimate-guide.md | References → `permissions.deny` |
| guide/security/data-privacy.md | Section removed |
| CHANGELOG.md:1244 | Historical reference corrected |

#### 4. "Selective Context Loading" Myth → Lazy Loading Reality

**Before**: Implied Claude loads entire codebase or selectively loads directories
**Reality**: Claude uses lazy loading - reads files on-demand via Read/Grep tools

| File | Correction |
|------|------------|
| guide/ultimate-guide.md | New section explaining lazy loading |
| guide/cheatsheet.md | "Giant context loads" → "Vague prompts" |
| machine-readable/reference.yaml | "load giant context" → "bloated CLAUDE.md" |

#### 5. Invented CLI Flags (SuperClaude Extension Confusion)

**Before**: `--think`, `--think-hard`, `--ultrathink`, `--headless`, `--learn`, `--uc`, `--web` documented as official CLI flags
**Reality**: These are SuperClaude framework extensions (prompt injection), NOT official Claude Code flags

| Correction Type | Details |
|-----------------|---------|
| `--headless` | Replaced with `-p` (the actual flag for non-interactive mode) |
| `--think` variants | Clarified as "prompt keywords", not CLI flags |
| SuperClaude section | Added warning: "Non-official Extension" |
| Cheatsheet | Think flags table reformatted as prompt keywords |
| Decision tree | "Use --think" → "Use extended thinking prompts" |

#### 6. `@` File Reference Behavior

**Before**: "Claude loads file content automatically"
**After**: "Signals Claude to read files on-demand via tools"

### Added - Session Search Tool (`cs`)

**Problem solved**: After weeks of Claude Code usage, finding past conversations becomes painful:
- `claude --resume` is interactive (no search)
- Sessions accumulate in `~/.claude/projects/`
- No quick way to search "that session where I talked about auth"

**Solution**: `cs` — Zero-dependency bash script for searching and resuming sessions.

```bash
cs                    # List 10 recent sessions (15ms)
cs "authentication"   # Full-text search (400ms)
cs -n 20              # More results

# Output:
# 2026-01-15 08:32 │ my-project │ Implement OAuth flow for...
#   claude --resume 84287c0d-8778-4a8d-abf1-eb2807e327a8
```

**Performance comparison**:

| Tool | List | Search | Deps | Resume cmd |
|------|------|--------|------|------------|
| `cs` (this script) | 15ms | 400ms | None | ✅ Shown |
| claude-conversation-extractor | 230ms | 1.7s | Python | ❌ |
| `claude --resume` native | 500ms+ | ❌ | None | Interactive |

**Files created/modified**:

| File | Description |
|------|-------------|
| `examples/scripts/session-search.sh` | Script in repo (source) |
| `examples/README.md` | Entry in Scripts table |
| `guide/ops/observability.md` | Section "Session Search & Resume" |
| `guide/ultimate-guide.md:505-524` | Examples in "Finding session IDs" |
| `README.md:398-403` | Section "Utility Scripts" |
| `machine-readable/reference.yaml` | `deep_dive.session_search` entry |

**Installation** (local):
```bash
# Copy script
cp examples/scripts/session-search.sh ~/.claude/scripts/cs
chmod +x ~/.claude/scripts/cs

# Add alias to shell
echo 'alias cs="~/.claude/scripts/cs"' >> ~/.zshrc
source ~/.zshrc
```

### Added - Security Documentation

| File | Addition |
|------|----------|
| guide/security/security-hardening.md | Section 1.2 "Known Limitations of permissions.deny" |

**Content**:
- Blocking matrix (Read/Edit/Write/Bash)
- Security gaps documented (GitHub #4160)
- Recommended exhaustive config
- Defense-in-depth strategy

### Files Modified (15 total)

```
guide/ultimate-guide.md
guide/cheatsheet.md
guide/security/data-privacy.md
guide/security/security-hardening.md
guide/ops/observability.md
machine-readable/reference.yaml
examples/scripts/audit-scan.sh
examples/scripts/session-search.sh (NEW)
examples/README.md
tools/audit-prompt.md
quiz/questions/01-quick-start.yaml
quiz/questions/10-reference.yaml
CHANGELOG.md
```

### Root Cause Analysis

The factual errors originated from:
1. **SuperClaude framework confusion**: User had `~/.claude/FLAGS.md` with custom flags that were documented as if official
2. **Assumption propagation**: "selective loading" concept was assumed from other AI tools
3. **Outdated syntax**: `excludePatterns` may have been planned but never implemented

---

## [3.6.0] - 2026-01-15

### Added - Version Sync Infrastructure

Single source of truth for versioning across all documentation.

#### New Files
- **VERSION** - Canonical version file (single source of truth)
- **scripts/sync-version.sh** - Automated version synchronization script
  - `--check` mode for CI validation (exit 1 if mismatch)
  - Auto-fixes all 3.x.x versions across docs
  - macOS/Linux compatible

#### Fixed
- **Version inconsistencies resolved**:
  - guide/cheatsheet.md: 3.5.0 → 3.6.0
  - guide/ultimate-guide.md: 3.0.7, 3.5.0 → 3.6.0
  - machine-readable/reference.yaml: 3.5.0 → 3.6.0

---

### Improved - README.md Navigation & Structure

Documentation alignment and navigation improvements.

#### README.md Updates
- **Repository Structure**: Added guide/workflows/, examples/modes/, examples/config/, examples/memory/
- **Core Documentation**: Added 5 entries (methodologies.md, workflows/, data-privacy.md, security-hardening.md, observability.md)
- **Slash Commands**: Added 4 commands (generate-tests, review-pr, git-worktree, validate-changes)
- **Security Hooks**: Added 2 hooks + link to complete catalog
- **🧭 Not Sure Where to Start?**: Added 6 navigation entries (Workflows, Methodologies, Architecture, Data Privacy, Security Hardening, Observability)
- **By Role Paths**: Enhanced all 4 paths with new resources (Power User +1: Security Hardening)
- **SEO Keywords**: Added 9 keywords (tdd ai, sdd, bdd, methodologies, architecture, workflows, data privacy, ai coding workflows)

#### guide/README.md Updates
- Added security-hardening.md to Contents table

---

## [3.5.0] - 2026-01-14

### Added - Development Methodologies & Workflows

Comprehensive documentation covering 15 structured development methodologies for AI-assisted development (2025-2026), with practical workflow guides.

#### New Files
- **guide/core/methodologies.md** (NEW, ~400 lines) - Complete methodology reference:
  - 15 methodologies organized in 6-tier pyramid (Orchestration → Optimization)
  - BMAD, SDD, TDD, BDD, DDD, ATDD, CDD, FDD, Context Engineering, Eval-Driven, Multi-Agent, Iterative Loops, Prompt Engineering
  - Decision tree for choosing the right approach
  - SDD tools reference (Spec Kit, OpenSpec, Specmatic)
  - Combination patterns by project type
  - Claude Fit ratings for each methodology

- **guide/workflows/** (NEW directory, 4 files, ~700 lines total):
  - **tdd-with-claude.md** - Test-Driven Development workflow with Claude-specific prompting patterns
  - **spec-first.md** - Spec-First Development (SDD) adapted for CLAUDE.md
  - **plan-driven.md** - Effective use of /plan mode
  - **iterative-refinement.md** - Prompt → Observe → Reprompt loops

#### Guide Updates
- **guide/ultimate-guide.md** - Section 9.14 "Development Methodologies" (NEW, ~60 lines):
  - Quick decision tree for workflow selection
  - 4 core workflows summary table
  - 15 methodologies reference table
  - SDD tools overview
  - Combination patterns by situation

#### Navigation Updates
- **guide/README.md** - Contents table updated with methodologies.md and workflows/

### Sources
- Anthropic Engineering Blog (claude-code-best-practices, context-engineering)
- GitHub (Spec Kit official announcement)
- Martin Fowler (SDD essays)
- Fission AI (OpenSpec)
- Specmatic.io
- Community production reports (2025-2026)

### Stats
- 5 new files created (~1,100 lines total)
- 2 files modified (ultimate-guide.md, guide/README.md)
- Focus on practical, actionable workflows over theory

---

## [3.4.0] - 2026-01-14

### Added - Architecture & Internals Documentation

New comprehensive documentation explaining how Claude Code works internally, based on official Anthropic sources and verified community analysis.

#### New Files
- **guide/core/architecture.md** (NEW, ~800 lines) - Complete technical deep-dive:
  - The Master Loop (`while(tool_call)` architecture)
  - The Tool Arsenal (8 core tools: Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite)
  - Context Management Internals (~200K token budget, auto-compaction)
  - Sub-Agent Architecture (isolated context, max depth=1)
  - Permission & Security Model (interactive prompts + allow/deny + hooks)
  - MCP Integration (JSON-RPC 2.0, treated as native tools)
  - The Edit Tool internals (exact match → fuzzy matching)
  - Session Persistence (--resume, --continue)
  - Philosophy: "Less Scaffolding, More Model"
  - Claude Code vs Alternatives comparison table
  - Sources with explicit confidence levels (Tier 1/2/3)
  - Appendix: What We Don't Know (transparency about gaps)
  - 5 ASCII diagrams (Master Loop, Context Budget, Sub-Agent, Permission Layers, MCP)

#### Guide Updates
- **guide/ultimate-guide.md** - Section 2.7 "Under the Hood" (NEW, ~100 lines):
  - Summary of architecture concepts with ASCII diagram
  - Links to full architecture.md for deep dives
  - Cross-references to existing sections (7-Hooks, 8.6-MCP Security)
  - Updated Table of Contents

- **guide/cheatsheet.md** - "Under the Hood (Quick Facts)" section (NEW):
  - 5-row table with key architecture concepts
  - Link to architecture.md for deep dive

#### Navigation Updates
- **README.md** - Core Documentation table + Repository Structure updated
- **guide/README.md** - Contents table updated with architecture.md
- **machine-readable/reference.yaml** - New `architecture:` section + deep_dive refs
- **machine-readable/llms.txt** - Guide structure + file list updated
- **tools/audit-prompt.md** - Related Resources updated
- **tools/onboarding-prompt.md** - Related Resources updated
- **examples/README.md** - Footer reference added

### Sources
- Tier 1 (Official): anthropic.com/engineering/claude-code-best-practices, code.claude.com/docs
- Tier 2 (Verified): PromptLayer analysis, community observations
- Tier 3 (Inferred): Marked with confidence levels

### Stats
- 1 new file created (architecture.md, ~800 lines)
- 10 files modified (navigation, versioning)
- Focus on transparency about Claude Code internals with source citations

---

## [3.3.1] - 2026-01-14

### Changed
- **IDEAS.md** - Consolidated and curated research topics
  - High Priority: Unified "MCP Security Hardening" (merged 3 overlapping topics)
  - Medium Priority: Kept CI/CD Workflows Gallery + MCP Server Catalog
  - Lower Priority: CLAUDE.md Patterns Library (templates by stack)
  - Discarded: Added 6 topics already covered in guide (prompt engineering, context optimization, task decomposition, agent architecture, case studies, tool comparisons)
  - Technical writer agent validation of all ideas against reference.yaml

### Stats
- IDEAS.md reduced from 12 research topics to 4 actionable items
- Discarded section expanded from 3 to 16 entries with clear justifications
- Focus on actionable research vs theoretical exploration

---

## [3.3.0] - 2026-01-14

### Added - LLM Handbook Integration + Google Agent Whitepaper

This release combines learnings from the LLM Engineers Handbook (guardrails, observability, evaluation) and Google's Agent Whitepaper (context triage, security patterns, validation checklists).

#### Advanced Guardrails
- **examples/hooks/bash/prompt-injection-detector.sh** - PreToolUse hook detecting:
  - Role override attempts ("ignore previous instructions", "you are now")
  - Jailbreak patterns ("DAN mode", "developer mode")
  - Delimiter injection (`</system>`, `[INST]`, `<<SYS>>`)
  - Authority impersonation and base64-encoded payloads
- **examples/hooks/bash/output-validator.sh** - PostToolUse heuristic validation:
  - Placeholder content detection (`/path/to/`, `TODO:`, `example.com`)
  - Potential secrets in output (regex patterns)
  - Uncertainty indicators and incomplete implementations
- **examples/hooks/bash/claudemd-scanner.sh** - SessionStart hook (NEW):
  - Scans CLAUDE.md files for prompt injection attacks before session
  - Detects: "ignore previous instructions", shell injection (`curl | bash`), base64 obfuscation
  - Warns about suspicious patterns in repository memory files
- **examples/hooks/bash/output-secrets-scanner.sh** - PostToolUse hook (NEW):
  - Scans tool outputs for leaked secrets (API keys, tokens, private keys)
  - Catches secrets before they appear in responses or commits
  - Detects: OpenAI/Anthropic/AWS keys, GitHub tokens, database URLs

#### Observability & Monitoring
- **examples/hooks/bash/session-logger.sh** - PostToolUse operation logging:
  - JSONL format to `~/.claude/logs/activity-YYYY-MM-DD.jsonl`
  - Token estimation, project tracking, session IDs
- **examples/scripts/session-stats.sh** - Log analysis script:
  - Daily/weekly/monthly summaries
  - Cost estimation with configurable rates
  - Tool usage and project breakdowns
- **guide/ops/observability.md** - Full observability documentation (~180 lines):
  - Setup instructions, cost tracking, patterns
  - Limitations clearly documented

#### LLM-as-a-Judge Evaluation
- **examples/agents/output-evaluator.md** - Quality gate agent (Haiku):
  - Scores: Correctness, Completeness, Safety (0-10)
  - Verdicts: APPROVE, NEEDS_REVIEW, REJECT
  - JSON output format for automation
- **examples/commands/validate-changes.md** - `/validate-changes` command:
  - Pre-commit validation workflow
  - Integrates with output-evaluator agent
- **examples/hooks/bash/pre-commit-evaluator.sh** - Git pre-commit hook:
  - Opt-in LLM evaluation before commits
  - Cost: ~$0.01-0.05/commit (Haiku)
  - Bypass with `--no-verify` or `CLAUDE_SKIP_EVAL=1`

#### Google Agent Whitepaper Integration
- **guide/ultimate-guide.md Section 2.2.4** - Context Triage Guide (NEW):
  - What to keep vs evacuate when approaching context limits
  - Priority matrix: Critical (current task) → Important (recent decisions) → Evacuate (old context)
  - Recovery patterns for session continuation
- **guide/ultimate-guide.md Section 3.1.3** - CLAUDE.md Injection Warning (NEW):
  - Security risks when cloning unfamiliar repositories
  - Recommendation to use `claudemd-scanner.sh` hook
  - Examples of malicious patterns to watch for
- **guide/ultimate-guide.md Section 4.2.4** - Agent Validation Checklist (NEW):
  - 12-point checklist before deploying custom agents
  - Covers: tool restrictions, output validation, error handling, cost control
  - Based on Google's agent validation framework
- **guide/ultimate-guide.md Section 8.6** - MCP Security (NEW):
  - Tool Shadowing attacks: malicious MCP tools mimicking legitimate ones
  - Confused Deputy attacks: MCP servers tricked into unauthorized actions
  - Mitigation strategies and trust verification patterns
- **guide/ultimate-guide.md Section 3.3.3** - Session vs Memory (NEW):
  - Clarifies session context (ephemeral) vs persistent memory (Serena write_memory)
  - When to use each for long-running projects
  - Recovery patterns after context limits

### Changed
- **examples/hooks/README.md** - Added "Advanced Guardrails" section with all new hooks
- **examples/README.md** - Updated index with all new files
- **guide/README.md** - Added observability.md to contents

### Stats
- 10 new files created
- 8 files modified
- 5 new guide sections added
- Focus: Production LLM patterns + Security hardening + Context management

---

## [3.2.0] - 2026-01-14

### Added
- **guide/security/data-privacy.md** - Comprehensive data privacy documentation (NEW, ~200 lines)
  - TL;DR retention table: 5 years (default) | 30 days (opt-out) | 0 (Enterprise ZDR)
  - Data flow diagram showing what leaves your machine
  - Known risks with MCP database connections
  - Protection measures (excludePatterns, hooks, MCP safety)
  - Quick checklist for immediate action

- **README.md** - Privacy notice encart (3 lines after transparency note)
  - Retention summary with action link
  - Direct link to opt-out and full guide

- **guide/ultimate-guide.md** - Section 2.6 "Data Flow & Privacy" (~45 lines)
  - Data types sent table
  - Retention policies table
  - Link to dedicated guide
  - Updated TOC and quick jump navigation

- **tools/onboarding-prompt.md** - Phase 0.5 Privacy Awareness
  - Privacy notice shown after level assessment
  - Asks user about privacy settings configuration

- **tools/audit-prompt.md** - Privacy configuration checks
  - Phase 1.2: PRIVACY CONFIGURATION bash checks
  - Phase 2.1: Privacy Configuration checklist
  - Glossary: "Data Retention" and "excludePatterns" terms

- **examples/scripts/audit-scan.sh** - PRIVACY CHECK section
  - Human output: .env exclusion check, DB MCP warning, opt-out link
  - JSON output: `"privacy"` object with env_excluded, has_db_mcp, opt_out_link, guide_link

- **examples/scripts/check-claude.sh** - Privacy reminder section
  - Shows retention info and opt-out link during health check

- **examples/hooks/bash/privacy-warning.sh** - SessionStart hook (NEW)
  - Displays privacy reminder box once per terminal session
  - Suppresses with `PRIVACY_WARNING_SHOWN=1` env var

- **guide/cheatsheet.md** - Golden Rule #7 added
  - "Know what's sent — prompts, files, MCP results → Anthropic"

### Stats
- 2 new files created (data-privacy.md, privacy-warning.sh)
- 8 files modified (README, guide, cheatsheet, audit-scan, check-claude, onboarding, audit-prompt)
- Focus on user awareness of data retention and actionable opt-out

## [3.1.0] - 2026-01-13

### Changed
- **Major repository restructuring** - Reorganized 15 root files into 4 thematic directories
  - `guide/` - Core documentation (ultimate-guide.md, cheatsheet.md, adoption-approaches.md)
  - `tools/` - Interactive utilities (audit-prompt.md, onboarding-prompt.md, mobile-access.md)
  - `machine-readable/` - LLM/AI consumption (reference.yaml, llms.txt)
  - `exports/` - Generated outputs (notebooklm.pdf, kimi.pdf)
- **File renaming** for cleaner paths:
  - `english-ultimate-claude-code-guide.md` → `guide/ultimate-guide.md`
  - `cheatsheet-en.md` → `guide/cheatsheet.md`
  - `claude-setup-audit-prompt.md` → `tools/audit-prompt.md`
  - `personalized-onboarding-prompt.md` → `tools/onboarding-prompt.md`
  - `mobile-access-setup.md` → `tools/mobile-access.md`
  - `claude-code-reference.yaml` → `machine-readable/reference.yaml`
- **README.md** - Added "Repository Structure" section with visual tree
- **150+ internal links updated** across all documentation files
- **Deleted** empty `to-ignore/` directory

### Added
- `guide/README.md` - Index for core documentation folder
- `tools/README.md` - Index for interactive utilities folder
- `machine-readable/README.md` - Index for LLM consumption folder
- `exports/README.md` - Index for generated outputs folder

### Stats
- 10 files moved to new locations
- 4 new README.md files created
- 150+ links updated
- Navigation significantly improved

## [3.0.7] - 2026-01-13

### Added
- **mobile-access-setup.md** - Mobile access guide for Claude Code (NEW, WIP/UNTESTED)
  - Problem statement: Claude Code lacks native session relay/sync across devices
  - Solution: ttyd + Tailscale for ToS-safe mobile access
  - Complete setup script with tmux for persistent sessions
  - Security considerations and ToS compliance notes
  - Alternatives comparison (Happy Coder, Claude Code Web, tmux+SSH)
  - Troubleshooting guide
  - Marked as WIP/UNTESTED - community feedback welcome

- **README.md** - Added mobile access guide to navigation table
  - New row: "Want mobile access to Claude Code" → Mobile Access Setup → WIP

### Stats
- 1 new file created (mobile-access-setup.md, ~300 lines)
- 2 files modified (README.md, cheatsheet-en.md version bump)
- Focus on ToS-safe remote access without third-party wrappers

## [3.0.6] - 2026-01-13

### Changed
- **Documentation honesty overhaul** - Removed marketing language and unverified claims
  - **README.md** (~12 edits):
    - Added transparency disclaimer after badges
    - Changed "Transform...superpower" → factual description of content
    - Changed "Our Solution: in hours, not weeks" → honest framing
    - Replaced time estimates with depth categories (Essentials, Foundation, Intermediate, Comprehensive)
    - Fixed "2 seconds" claims → "Quick (~30 seconds)"
    - Corrected privacy claim ("Everything runs locally" → accurate API explanation)
    - Changed "mentor for Claude Code mastery" → "structured learning companion"
  - **english-ultimate-claude-code-guide.md** (~15 edits):
    - Added "Before You Start" disclaimer section at top
    - Removed "Guide Status 100% Complete" table (false certainty)
    - Added qualifying note after context thresholds table
    - "90% of daily usage" → "the ones I use most frequently"
    - "20-30% faster" → subjective productivity indicators
    - "Saves 30-40%" → "Frees significant context space"
    - Removed invented ROI table with fake calculations
    - "Never guesses - always verifies" → with LLM hallucination warning
    - Removed "12,400% ROI" ridiculous claim
    - "90% of tasks" → "most common tasks"
    - "80-90% savings" → "significant (varies by project)"
  - **adoption-approaches.md** (already in 3.0.5):
    - Added disclaimer about Claude Code being young (~1 year)
    - Added "What We Don't Know Yet" section
    - Changed prescriptive language to tentative observations

### Stats
- 3 files modified (README.md, english-ultimate-claude-code-guide.md, cheatsheet-en.md)
- ~30 edits removing invented percentages, times, and marketing claims
- Focus on honest, qualified observations over false authority

## [3.0.5] - 2026-01-13

### Added
- **adoption-approaches.md** - Comprehensive adoption philosophy guide (NEW, ~355 lines)
  - Addresses community feedback: "turnkey setup" vs "autonomous learning" approaches
  - **Decision Tree** for immediate routing based on context (time, team size, uniqueness)
  - **Turnkey Quickstart** (15 min) with 3 verifiable steps
  - **Autonomous Learning Path** with 4 phases + time estimates + line references
  - **Adoption Checkpoints** with pass/fail criteria (Day 1, Week 1, Week 2, Month 1)
  - **Anti-patterns** table with symptoms and solutions
  - **Team Size Guidelines** with config structures for solo/4-10/10+ developers
  - **Scenario Decisions**: CTO evaluation, team disagreements, inherited configs, upgrade triggers
  - **Quick Reference**: daily commands table + cost-conscious model selection
  - Aligns with `claude-code-reference.yaml` patterns (decision trees, line refs, context zones)

### Changed
- **README.md** - Added adoption guide to "Not Sure Where to Start?" navigation table
  - New row: "Choosing turnkey vs. autonomous approach" → Adoption Guide → 5 min

### Stats
- 1 new file created (adoption-approaches.md, ~355 lines)
- 1 file modified (README.md, +1 line)
- Focus on helping users choose the right adoption strategy for their context

## [3.0.4] - 2026-01-13

### Added
- **examples/commands/diagnose.md** - Interactive troubleshooting assistant (NEW)
  - Bilingual support (FR/EN) with automatic language detection
  - 12 problem categories: permissions, MCP servers, config, performance, installation, agents/skills
  - Auto-fetches latest guide from GitHub for up-to-date troubleshooting data
  - Integrates with `audit-scan.sh --json` for environment scanning
  - Structured diagnostic output: root cause → solution → template → reference
  - Common patterns documented: repeated permission prompts, MCP not found, context saturation
  - Usage: Copy to `~/.claude/commands/` then invoke with `/diagnose`

### Changed
- **README.md** - Added `/diagnose` to commands table and navigation
- **examples/README.md** - Added `/diagnose` to commands index
- **cheatsheet-en.md** - Version bump to 3.0.4

### Stats
- 1 new file created (diagnose.md, ~210 lines)
- 3 files modified (README.md, examples/README.md, cheatsheet-en.md)
- Focus on self-service troubleshooting for common Claude Code issues

## [3.0.3] - 2026-01-13

### Enhanced
- **audit-scan.sh v2.0** - Major improvements based on community feedback (2 test projects)
  - **P0.1: MCP Detection globale** - Now detects both project-specific AND global MCPs from `~/.claude.json`
    - Previously only checked `projects[path].mcpServers`, now also checks top-level `mcpServers`
    - Shows separate counts: project MCPs vs global MCPs with their sources
  - **P0.2: MCP documented vs configured** - New feature detecting MCPs mentioned in CLAUDE.md but not actually configured
    - Scans CLAUDE.md files for known MCPs (serena, context7, sequential, playwright, morphllm, magic, filesystem)
    - Warns when MCP is documented but missing from config: "Documented but NOT configured: serena"
    - Helps catch configuration drift
  - **P1.1: +35 integrations detected** - Expanded from ~25 to ~60 packages
    - Chat/Communication: TalkJS, Knock, Stream
    - Maps: MapLibre, Mapbox, Google Maps
    - File Upload: Bytescale, UploadThing, Cloudinary
    - Admin: Forest Admin, Refine
    - Validation: Zod, Yup, Valibot
    - UI Libraries: Chakra UI, Material UI, DaisyUI, Mantine
    - Database providers: Neon, PlanetScale, Vercel Postgres, Upstash, Turso
    - Analytics: Vercel Analytics, Mixpanel, Hotjar, Amplitude
    - Feature flags: Vercel Flags, LaunchDarkly
    - Forms: React Hook Form, Formik
    - Auth: Kinde
    - Payments: LemonSqueezy
    - AI: Vercel AI SDK
    - CMS: Payload CMS
    - State: Jotai
  - **P1.2: Test framework warning** - Now explicitly warns when no test framework detected
    - Checks package.json deps, config files (jest.config.*, vitest.config.*), and test file patterns
    - Shows ❌ "No test framework detected" in quality patterns
  - **P1.3: MCP Recommendations** - Context-aware suggestions based on detected stack
    - context7 recommended for modern frameworks (Next.js, React, Vue, etc.)
    - sequential-thinking for complex architectures (with DB or NestJS/Next.js)
    - playwright for projects without E2E testing
    - serena for TypeScript projects
  - **P2.1: Extended SSoT detection** - Now searches for @refs in codebase even without CLAUDE.md
    - If >5 files contain `@*.md` references, considers SSoT pattern adopted
  - **P2.2: shadcn/ui detection** - Special case handling (not in package.json)
    - Detects presence of `components/ui/` or `src/components/ui/` folders
  - **JSON output enhanced** with new fields:
    - `quality.has_test_framework` (boolean)
    - `mcp.project_servers`, `mcp.global_servers` (separated)
    - `mcp.documented`, `mcp.missing` (doc vs config gap)
    - `mcp.recommendations` (stack-based suggestions)
  - **Human output enhanced**:
    - New "🔌 MCP SERVERS" section with project/global breakdown
    - Warning for documented but unconfigured MCPs
    - Recommendations displayed with 💡 icon

### Fixed
- **audit-scan.sh** - `ALL_DEPS` unbound variable error when running outside Node.js projects
  - Initialized `ALL_DEPS=""` before conditional blocks

### Stats
- 1 file modified (audit-scan.sh, ~200 lines added/modified)
- Integration detection improved from ~25 to ~60 packages
- MCP detection now covers all configuration locations
- Based on feedback from Native Spaces (venue booking) and Méthode Aristote (EdTech) projects

## [3.0.2] - 2026-01-12

### Added
- **personalized-onboarding-prompt.md** - Interactive onboarding prompt (~200 lines)
  - Multilingual support: User chooses preferred language first
  - 3 experience levels: Beginner (🟢), Intermediate (🟡), Power User (🔴)
  - Progressive exploration with deeper/next/skip controls
  - Tailored learning paths per level
  - Optional practical exercises
  - Self-paced interactive Q&A format

- **README.md** - Added onboarding prompt to "Not Sure Where to Start?" table
  - New row: "Want a guided tour" → Personalized Onboarding → ~15 min

### Stats
- 1 new file created (personalized-onboarding-prompt.md, ~200 lines)
- 1 file modified (README.md)
- Focus on accessible, multilingual onboarding experience

## [3.0.1] - 2026-01-12

### Added
- **Custom Statusline Setup** documentation
  - New section in `english-ultimate-claude-code-guide.md` (lines 990-1027)
  - [ccstatusline](https://github.com/sirmalloc/ccstatusline) as recommended solution
  - Enhanced statusline displays: model, git branch, file changes (+/-), context metrics
  - Custom script option with JSON stdin format
  - `/statusline` command reference for auto-generation
  - Added to `cheatsheet-en.md` (lines 130-133)

### Stats
- 2 files modified (english-ultimate-claude-code-guide.md ~38 lines, cheatsheet-en.md ~4 lines)
- Focus on developer experience and terminal customization

## [3.0.0] - 2026-01-12

### Added
- **quiz/** - Interactive CLI quiz to test Claude Code knowledge (MAJOR FEATURE)
  - 159 curated questions across 10 categories (matching guide sections)
  - 4 user profiles: Junior (15q), Senior (20q), Power User (25q), PM (10q)
  - Immediate feedback with explanations and documentation links
  - Score tracking with category breakdown and weak area identification
  - Session persistence to `~/.claude-quiz/` for progress history
  - Replay options: retry wrong questions or start fresh quiz
  - Optional dynamic question generation via `claude -p`
  - Cross-platform: Node.js (works on macOS, Linux, Windows)

- **README.md** - New "Knowledge Quiz" section in navigation
  - Added quiz to "Not Sure Where to Start?" table
  - Collapsible example session showing quiz flow
  - Links to quiz documentation and contribution template

### Files Created
```
quiz/
├── package.json           # Node.js config
├── README.md              # Full documentation with examples
├── src/
│   ├── index.js           # Entry point + CLI args
│   ├── ui.js              # Terminal display
│   ├── prompts.js         # User prompts (inquirer)
│   ├── questions.js       # YAML loading + filtering
│   ├── quiz.js            # Quiz engine
│   ├── score.js           # Score tracking
│   ├── session.js         # Persistence
│   └── dynamic.js         # claude -p generation
├── questions/             # 10 YAML files (159 questions)
└── templates/
    └── question-template.yaml
```

### Stats
- 20+ new files
- 159 questions covering all guide sections
- New learning tool for the community

## [2.9.9] - 2026-01-12

### Enhanced
- **audit-scan.sh** - SSoT refactor warning
  - New `needs_ssot_refactor` flag: true if CLAUDE.md >100 lines with 0 @references
  - Human output shows red warning suggesting SSoT pattern (split into @docs/)
  - JSON output includes `needs_ssot_refactor` in quality section

- **README.md** - Improved Full Audit prompt for incremental suggestions
  - Added IMPORTANT instruction to focus on incremental improvements, not generic advice
  - Health score now penalizes large CLAUDE.md without @refs
  - Quick wins must be domain-specific, not generic
  - If CLAUDE.md exists: suggest 3-5 improvements instead of full template
  - Agents/commands suggestions must not duplicate existing ones

### Stats
- 2 files modified
- Audit now provides targeted, incremental recommendations

## [2.9.8] - 2026-01-12

### Enhanced
- **audit-scan.sh** - Enhanced stack detection with detailed breakdown
  - Now detects: runtime, framework, test runner, bundler, database/ORM
  - Generic integration detection from package.json (auth, payments, AI, monitoring, etc.)
  - Works without jq (grep-based fallback for all JSON parsing)
  - Stack recap shown at top of human output
  - JSON output includes full `stack` object with all detected components

- **README.md** - Updated Full Audit prompt
  - Now requests Stack Recap as first output item
  - CLAUDE.md template increased from ~60 to ~100 lines
  - Added integration-aware suggestions in output description

### Fixed
- **audit-scan.sh** - jq fallback now works for MCP detection in ~/.claude.json

### Stats
- 2 files modified (audit-scan.sh ~150 lines added, README.md prompt updated)
- Detects 25+ common integrations (Clerk, Stripe, OpenAI, Sentry, etc.)

## [2.9.7] - 2026-01-12

### Enhanced
- **README.md** - Deep Audit now context-aware
  - Full Audit command now reads project's README.md, CLAUDE.md, and .claude/CLAUDE.md
  - Claude analyzes business domain to provide tailored recommendations
  - Domain-specific suggestions (EdTech → session agents, E-commerce → inventory commands)
  - Privacy notice: all data stays local, nothing sent back to repo

### Stats
- 1 file modified (README.md)
- Deep Audit now provides personalized, domain-aware recommendations

## [2.9.6] - 2026-01-12

### Fixed
- **audit-scan.sh** - Count files recursively in subfolders
  - Commands in subfolders (e.g., `commands/tech/`, `commands/product/`) now counted
  - Split into `count_md_files()` for .md and `count_script_files()` for hooks (.sh/.js/.py/.ts)
  - Excludes README.md from counts
  - Bug found: Was reporting 0 commands when 10 existed in subfolders

### Stats
- 1 file modified (audit-scan.sh, ~15 lines)
- Critical fix for accurate extension counting

## [2.9.5] - 2026-01-12

### Added
- **README.md** - Deep Audit section with one-liner commands
  - New row in "Not Sure Where to Start?" table
  - `🔬 Deep Audit` section with two options:
    - Quick Version (~10 sec): Single curl pipe to Claude
    - Full Audit (~30 sec): Downloads YAML reference + scan for comprehensive analysis
  - Outputs: Health score, prioritized findings, CLAUDE.md template, suggested extensions

### Stats
- 1 file modified (README.md, ~35 lines added)
- Focus on one-command personalized audit experience

## [2.9.4] - 2026-01-12

### Added
- **examples/modes/** - New folder for behavioral modes
  - `MODE_Learning.md` - Complete Learning Mode ready to copy to `~/.claude/`
  - `README.md` - Installation guide with SuperClaude framework reference
- **examples/README.md** - Updated with modes folder and templates

### Stats
- 2 new files created (MODE_Learning.md, modes/README.md)
- 1 file modified (examples/README.md)
- Focus on making SuperClaude Learning Mode plug-and-play

## [2.9.3] - 2026-01-12

### Added
- **README.md** - LLM Reference section with curl one-liner
  - New row in "Not Sure Where to Start?" table
  - `🤖 LLM Reference` section with instant curl command
  - Use cases: ChatGPT/Claude/Gemini context, system prompts, `@` reference
  - Clarification that YAML points to line numbers in full guide for deep dives
- **english-ultimate-claude-code-guide.md** - Learning Mode documentation (~136 lines)
  - SuperClaude Behavioral Modes overview table
  - Complete Learning Mode installation guide (4 steps)
  - Usage examples with `--learn`, `--learn focus:X`, `--learn batch` flags
  - Offer format examples (standard and token-efficient)
  - Integration matrix with other modes
  - Priority rules and example session
- **claude-code-reference.yaml** - Learning mode additions
  - `deep_dive` refs: superclaude_modes, learning_mode
  - `decide` section: learning flag
  - `cli` section: --learn, --learn focus:X, --no-learn flags

### Stats
- 3 files modified (README.md, english-ultimate-claude-code-guide.md, claude-code-reference.yaml)
- ~150 lines added across files
- Focus on LLM context sharing and SuperClaude Learning Mode documentation

## [2.9.2] - 2026-01-12

### Added
- **claude-code-reference.yaml** - Machine-optimized LLM index (~2K tokens)
  - **Decision tree** as first section (most used lookup)
  - **Prompting formula** (WHAT/WHERE/HOW/VERIFY pattern)
  - **38 deep_dive line references** to english-ultimate-claude-code-guide.md
  - 22 sections covering: commands, shortcuts, CLI flags, context management, memory files, MCP servers, think levels, cost optimization, anti-patterns, troubleshooting
  - Flat YAML structure (max 1 level nesting) for optimal LLM parsing
  - ~97% token reduction vs full guide (2K vs 70K tokens)
- **README.md** - Added LLM Reference row in Core Documentation table
- **llms.txt** - Added Machine-Optimized Reference section with YAML file description

### Stats
- 1 new file created (claude-code-reference.yaml, 282 lines)
- 2 files modified (README.md, llms.txt)
- Use case: Claude Code self-reference for fast user question answering

## [2.9.1] - 2026-01-12

### Fixed
- **Cheatsheet completeness audit** (cheatsheet-en.md, ~15 lines modified)
  - **Missing commands added**:
    - `/execute` - Exit Plan Mode (counterpart to `/plan`)
    - `/model` - Switch model (sonnet/opus/opusplan)
  - **Missing keyboard shortcuts added**:
    - `Ctrl+R` - Retry last operation
    - `Ctrl+L` - Clear screen (keeps context)
  - **Missing CLI flags added**:
    - `-c` / `--continue` - Continue last session
    - `-r` / `--resume <id>` - Resume specific session
    - `--headless` - Non-interactive (CI/CD)
  - **Missing maintenance command added**:
    - `claude update` - Check/install updates
  - **Inconsistency fixed**:
    - Removed false `/resume` slash command from Context Recovery Commands
    - Replaced with correct CLI flags (`claude -c`, `claude -r <id>`)
  - **Clarification**:
    - `/status` vs `/context` descriptions clarified (session state vs detailed token breakdown)
  - Cheatsheet version: 2.8 → 2.8.1

### Stats
- 1 file modified (cheatsheet-en.md)
- Audit coverage improved from ~36% to ~85% of documented commands
- Format preserved: 377 lines, 1-page printable maintained

## [2.9.0] - 2026-01-12

### Fixed
- **MCP detection bug in audit-scan.sh** (~60 lines modified)
  - **Root cause**: Script searched for `~/.claude/mcp.json` which doesn't exist
  - **Actual location**: Claude Code stores MCP config in `~/.claude.json` under `projects.<path>.mcpServers`
  - **Solution**: Multi-source detection with priority:
    1. `~/.claude.json` → `projects.<cwd>.mcpServers` (most common)
    2. `./.claude/mcp.json` (project-level)
    3. `~/.claude/mcp.json` (legacy global)
  - JSON output now includes detailed `mcp` section (configured, count, servers, source)
  - Human output shows server count and source location
- **Bug `0\n0` in `claude_md_refs`** (~8 lines)
  - **Root cause**: `grep -c ... || echo "0"` could produce double output
  - **Solution**: Rewritten `count_pattern()` function to properly capture and return count

### Changed
- **audit-scan.sh** enhanced (~50 lines)
  - Added `MCP_SOURCE` variable to track where MCP config was found
  - Added `MCP_COUNT` variable for server count
  - Global `mcp.json` message changed from error to info (not required)
  - JSON output restructured with separate `mcp` object
- **claude-setup-audit-prompt.md** updated (~40 lines)
  - Phase 1.1: Now checks `~/.claude.json` instead of `~/.claude/mcp.json`
  - Phase 1.2: Complete MCP detection rewrite covering all 3 locations
  - Glossary: Updated MCP definition to explain config locations
  - Version: 2.8 → 2.9

### Stats
- 2 files modified (audit-scan.sh, claude-setup-audit-prompt.md)
- Bug impact: Scripts now correctly detect MCP servers (was showing "No MCP" even when configured)
- Tested: Verified on Méthode Aristote project with 9 MCP servers

## [2.8.0] - 2026-01-11

### Added
- **Verified CLI commands and flags from Medium article analysis** (~61 lines)
  - **Section 1.1 "Updating Claude Code"** (lines 210-241)
    - `claude update` command - Check and install available updates
    - `claude doctor` command - Verify auto-updater health and system integrity
    - Maintenance commands reference table with usage guidance
    - Update frequency recommendations (weekly, before major work, after system changes)
    - Alternative npm update method documented
  - **Section 10.1 Built-in Commands** (line 7746)
    - `/output-style` - Change response format (concise/detailed/code)
    - `/feedback` - Report bugs or send feedback to Anthropic (renamed from `/bug`)
  - **Section 10.3 CLI Flags Reference** (lines 7837, 7848)
    - `--json-schema <schema>` - JSON Schema for structured output validation
    - `--max-budget-usd <amount>` - Maximum API spend limit (with `--print` only)
  - **Section 10.4 Quick Diagnostic Guide** (lines 7893-7913)
    - Symptom-based troubleshooting table with 8 common scenarios
    - Quick Fix + Prevention columns for rapid issue resolution
    - 5-step diagnosis flow (context → connectivity → configuration → permissions → doctor)
    - Covers: context overflow, rate limits, MCP issues, permission prompts, session corruption

- **README.md navigation improvements** (~50 lines)
  - Decision Helper table after Quick Start (6 user personas with direct links)
  - Moved Audit section to prominent position after Quick Start
  - Reframed AI admission from apologetic to professional tone
  - Added Prerequisites section (Node.js, API key, cost estimate)
  - Outcome-based Guide Navigation ("After this, you can...")
  - Consolidated PDFs/DeepWiki into collapsible `<details>` section
  - Shortened Windows disclaimer (5 lines → 1 line)
  - Added GitHub Actions section to Production-Ready Examples
- **examples/README.md catalog completion**
  - Added `github-actions/` folder to Structure table (3 CI/CD workflows)
  - Added `workflows/` folder to Structure table (database branch setup)
  - Complete Templates Index with all 9 example categories

### Changed
- **Verification methodology improvements**
  - All additions verified via `claude --help` output or direct user testing
  - Rejected 6+ unverified elements from Medium article (false positives and non-existent commands)
  - Avoided documenting 16 already-present elements (prevented redundancy)
  - Maintained guide credibility by only adding 100% confirmed features
- **README.md restructured** for better first-time user experience
  - Clear decision support for new users ("Not Sure Where to Start?")
  - Audit tool more discoverable (moved from buried position)
  - Professional AI disclosure without being apologetic

### Stats
- Guide expanded from 8,787 to 8,848 lines (+61 lines, +0.7%)
- 6 sections modified (Installation, Commands Table, CLI Flags, Troubleshooting, README, examples/README)
- Focus on maintenance commands, structured output, rapid diagnostics, and navigation UX
- Verification ratio: 7 confirmed additions / 22 rejected claims (~32% valid from source article)
- README improvements: Decision Helper, Audit visibility, GitHub Actions showcase

## [2.7.0] - 2026-01-11

### Added
- **Audit optimization with bash scanning** (~350 lines across 4 files)
  - **examples/scripts/audit-scan.sh** (NEW, ~230 lines)
    - Fast Claude Code setup scanner with dual output modes
    - JSON output (`--json`) for Claude processing
    - Human-readable output (default) with color-coded results (✅/❌/⚠️)
    - Scans: global config (~/.claude/), project config (./CLAUDE.md, .claude/), extensions (agents/commands/skills/hooks/rules)
    - Tech stack auto-detection (Node.js, Python, Go, Rust, PHP via manifest files)
    - Quality pattern checks: security hooks (PreToolUse), SSoT references (@refs), MCP servers
    - Performance: ~80% faster than file-reading approach (~2s vs ~30s)
    - Token efficiency: ~90% reduction (~500 tokens vs ~5000 tokens)
  - **claude-setup-audit-prompt.md Phase 1-2 rewrite** (~120 lines modified)
    - Phase 1.1 "Quick Configuration Scan" replaced file reads with bash commands
    - Phase 1.2 "Quality Pattern Checks" uses grep/wc/find for targeted validation
    - Phase 1.3 references external audit-scan.sh for comprehensive scanning
    - Added "Efficient Guide Reference Lookup" with sed line range extraction
    - Reduced audit time estimate from ~5-10 minutes to ~2-3 minutes
    - Version updated: 2.1 → 2.2
  - **examples/README.md scripts section** (~20 lines)
    - Added `scripts/` folder to structure table
    - Scripts table documenting 3 utility scripts (audit-scan.sh, check-claude.sh, clean-reinstall-claude.sh)
    - Usage examples for both JSON and human-readable output modes
  - **README.md "Audit Your Setup" section rewrite** (~60 lines)
    - Two-option approach: Quick Bash Scan (2 seconds) vs Claude-powered audit (2-3 minutes)
    - Performance comparison: "~80% faster scanning and 90% fewer tokens"
    - Option 1: Direct script execution with curl download example
    - Option 2: Claude-powered analysis referencing audit prompt
    - Clear usage instructions for both `--json` and default modes

### Changed
- **Version alignment** across documentation
  - README.md: Version 2.6 → 2.7
  - english-ultimate-claude-code-guide.md: Already at 2.7
  - claude-setup-audit-prompt.md: Version 2.1 → 2.2

### Stats
- 1 new file created (audit-scan.sh, ~230 lines)
- 4 files modified (claude-setup-audit-prompt.md, examples/README.md, README.md, CHANGELOG.md)
- Performance improvement: 80% faster scanning, 90% token reduction
- Focus on efficiency, developer experience, and programmatic auditing
- Script supports both human-readable and machine-readable (JSON) output

## [2.6.0] - 2026-01-11

### Added
- **Section 8.5: Plugin System** (~245 lines, comprehensive documentation)
  - **Plugin System fundamentals** (lines 4836-5073)
    - What are plugins: packaged agents, skills, commands, domain-specific tooling
    - Plugin commands table: install, enable, disable, uninstall, update, validate
    - Marketplace management: add, list, update, remove marketplaces
    - Using plugins workflow from marketplace to session usage
    - Plugin session loading with `--plugin-dir` flag for testing
  - **When to Use Plugins** decision matrix
    - Team workflows: Share standardized agents/skills via private marketplace
    - Domain expertise: Pre-built security, accessibility, performance plugins
    - Repeating patterns: Package custom workflows for reuse
    - Community solutions: Leverage community expertise
  - **Creating Custom Plugins** guide
    - Directory structure with manifest (plugin.json)
    - Example security-audit plugin manifest
    - Validation command: `claude plugin validate ./my-plugin`
  - **Plugin vs. MCP Server** comparison table
    - Plugin = "How Claude thinks" (workflows, specialized agents)
    - MCP Server = "What Claude can do" (tools, external systems)
    - Clear guidance on when to use which
  - **Security Considerations** section
    - Before installing: trust source, review manifest, test in isolation
    - Red flags: network access without reason, obfuscated code, no documentation
  - **Example Use Cases** with real workflows
    - Team Code Standards Plugin (private marketplace)
    - Security Audit Suite (community plugin)
    - Accessibility Testing (a11y plugin with WCAG compliance)
  - **Troubleshooting** guide
    - Plugin not found after install
    - Plugin conflicts resolution
    - Plugin not loading in session
- **Keyboard Shortcut: `Esc×2` double-tap** (line 7487)
  - Added to Section 10.2 Keyboard Shortcuts table
  - Clarifies double-tap pattern: Rewind to previous checkpoint (same as `/rewind`)
  - Resolves inconsistency between TL;DR mention and shortcuts table
- **Plugin command** in Section 10.1 Commands Table (line 7696)
  - `/plugin` command: Manage Claude Code plugins (Config category)
- **Plugin flag** in Section 10.3 CLI Flags Reference (line 7782)
  - `--plugin-dir`: Load plugins from directory (repeatable flag)

### Changed
- **Table of Contents updated** (line 147)
  - Added [8.5 Plugin System](#85-plugin-system) entry
- **Section 8 Quick Jump navigation enhanced** (line 4530)
  - Added Plugin System link to quick navigation bar
- **TL;DR Power Features table** (line 80)
  - Added "Plugins: Community-created extension packages" row
- **Version alignment** across documentation
  - english-ultimate-claude-code-guide.md: Version 2.5 → 2.6
  - README.md: Version 2.5 → 2.6

### Stats
- Guide expanded from 8,545 to 8,787 lines (+242 lines, +2.8%)
- Plugin System section: ~245 lines of comprehensive documentation
- 1 keyboard shortcut clarified (Esc×2)
- 2 command/flag additions (/plugin, --plugin-dir)
- Focus on extensibility and community-driven functionality
- Zero loss of existing functionality

## [2.5.0] - 2026-01-11

### Removed
- **Content cleanup and optimization** (~1048 lines removed, -10.9%)
  - **DeepSeek Integration section** (~200 lines, lines 9123-9321)
    - Third-party provider documentation not specific to Claude Code
    - Replaced reference in configuration table with generic "Alternative auth token"
  - **Git Archaeology Pattern** (~250 lines, lines 8834-9081)
    - General Git technique, not Claude Code-specific
  - **Emergency Hotfix Checklist** (~140 lines, lines 8695-8832)
    - Generic development workflow, not specific to Claude Code
  - **Maturity Model & Success Metrics** (~95 lines, lines 8544-8691)
    - Gamification content that added weight without Claude Code value
  - **Prompt Templates** (~105 lines, lines 8437-8542)
    - Generic prompt templates not specific to Claude Code
  - **Task-specific checklists** (Bug Fix, Feature, Code Review, Refactoring)
    - General development checklists, not Claude Code workflows
  - **Community Resources fictional dates** (table column removed)
    - Removed "Last Updated" column with fictional future dates (Apr 2025, Oct 2025, Jul 2025, Aug 2025)
    - Reduced from 5 to 3 essential awesome-lists

### Changed
- **Health Check Scripts externalized** to `examples/scripts/`
  - Replaced ~90 lines of inline PowerShell/Bash scripts with links
  - Created `examples/scripts/check-claude.sh` (macOS/Linux health check)
  - Created `examples/scripts/check-claude.ps1` (Windows health check)
  - Main guide now references external scripts for maintainability
- **Clean Reinstall Scripts externalized** to `examples/scripts/`
  - Replaced ~75 lines of inline reinstall procedures with links
  - Created `examples/scripts/clean-reinstall-claude.sh` (macOS/Linux reinstall)
  - Created `examples/scripts/clean-reinstall-claude.ps1` (Windows reinstall)
  - Improves separation of concerns (guide vs utilities)
- **Nick Tune reference condensed**
  - Reduced from ~40 lines to 3 lines with link only
  - Kept attribution but removed excessive detail
- **Daily Workflow & Checklists streamlined**
  - Removed generic checklists (Bug Fix, Feature, Code Review, Refactoring)
  - Kept only Claude Code-specific parts (Daily Workflow, Prompt Quality)
- **Table of Contents cleaned**
  - Removed obsolete references to A.8 (Prompt Templates) and A.9 (Success Metrics)
  - Fixed document structure coherence

### Fixed
- Version consistency across documentation (2.4 aligned)
- Code block balance verification (673 markers, properly balanced)
- Removed broken internal references to deleted sections

### Stats
- Document reduced from 9,593 to 8,545 lines (-1,048 lines, -10.9%)
- 4 new script files created in examples/scripts/ (~350 lines externalized)
- Focus shifted to Claude Code-specific content only
- Improved maintainability through script externalization
- Zero loss of essential Claude Code functionality

## [2.4.0] - 2026-01-10

### Added
- **Database Branch Isolation with Git Worktrees** (~540 lines across 3 files)
  - **examples/commands/git-worktree.md** enhanced (~90 lines added)
    - Database provider auto-detection (Neon, PlanetScale, Local Postgres, Supabase)
    - Suggested commands for DB branch creation per provider
    - `.worktreeinclude` setup documentation for .env copying
    - "When to Create Database Branch" decision table
    - Cleanup commands including DB branch deletion
    - Common mistakes section expanded with DB-related pitfalls
  - **examples/workflows/database-branch-setup.md** (NEW, ~350 lines)
    - Complete provider-specific setup guides (Neon, PlanetScale, Local Postgres)
    - TL;DR section for 90% use case (Neon quick start)
    - Provider comparison table with branching capabilities
    - 3 isolation patterns: Cloud branching, Local schema, Shared DB
    - Decision tree for choosing DB isolation strategy
    - Real-world workflow examples with commands
    - Troubleshooting section with common issues
    - Prerequisites and CLI installation per provider
  - **english-ultimate-claude-code-guide.md** Section 9.12 enhanced (~95 lines)
    - "Database Branch Isolation with Worktrees" new subsection
    - Problem/Solution framing for schema conflicts
    - Provider detection explanation
    - "When to create DB branch" decision table
    - Complete workflow example with Neon
    - Prerequisites for all major providers
    - Links to detailed workflow guide
  - **Source attribution**: [Neon database branching](https://neon.tech/docs/guides/branching) and [PlanetScale branching workflows](https://planetscale.com/docs/concepts/branching)

### Changed
- **Guide statistics updated**
  - Guide expanded from 9,700+ to 9,592 lines (optimized structure, net -108 lines)
  - Content reorganized for better progressive disclosure
  - Reduced redundancy through single source of truth pattern
- **Documentation architecture improved**
  - Command reference (git-worktree.md) kept concise and scannable
  - Detailed workflows separated into dedicated guide
  - Clear separation: Quick Reference → Complete Tutorial

### Stats
- 1 new file created (workflows/database-branch-setup.md, ~350 lines)
- 3 files modified (git-worktree.md +90, guide +95, examples/README.md)
- Focus on database isolation patterns for modern dev workflows
- Maintenance-friendly: Single source of truth for provider commands

## [2.3.0] - 2026-01-10

### Added
- **DeepTo Claude Code Guide integration** (~800 lines across 5 sections)
  - **Image Processing** (Section 2.3.2, lines 377-445)
    - Direct image input via paste/drag-drop in terminal
    - Screenshot analysis, UI debugging, error message analysis
    - Best practices for image-based workflows
    - Supported formats: PNG, JPG, GIF, WebP, screenshots
  - **Session Continuation and Resume** (Section 2.3.4, lines 447-560)
    - `claude --continue` / `-c` to resume last session
    - `claude --resume <id>` / `-r <id>` for specific sessions
    - Use cases table: long-term projects, research, interrupted work, daily workflows
    - Context preservation across terminal sessions
    - Integration with MCP Serena for persistent memory
  - **XML-Structured Prompts** (Section 2.6, lines 1582-2148)
    - Semantic organization using `<instruction>`, `<context>`, `<code_example>`, `<constraints>`, `<output>` tags
    - Benefits table: disambiguation, role clarity, example isolation, constraint definition
    - 3 practical examples: code review, feature implementation, bug investigation
    - Advanced patterns: nested tags, multiple examples, conditional instructions
    - Integration with CLAUDE.md and Plan Mode
    - Template library for common scenarios
  - **ccusage CLI Tool** (Section 3.5.3, around line 970)
    - Detailed cost analytics and tracking
    - Model-specific breakdowns (Haiku/Sonnet/Opus)
    - Token usage analysis and optimization insights
    - Installation and usage instructions
  - **Unix Piping Workflows** (Section 9.3.3, line 4490)
    - Feeding content to Claude via stdin pipes
    - Output format options (text, json, markdown)
    - Build script integration patterns
    - CI/CD pipeline examples (linting, testing, security)
    - Automated analysis and report generation
  - **DeepTo Guide reference** added to README.md Resources section
    - Listed alongside zebbern, Claudelog, and ykdojo guides
    - Brief description covering all integrated concepts
  - **Source attribution** included in all new sections
    - Proper credit to https://cc.deeptoai.com/docs/en/best-practices/claude-code-comprehensive-guide
    - Following same attribution format used for other community guides

### Changed
- **Guide statistics updated**
  - Guide expanded to approximately 9,700+ lines (+800 lines from DeepTo integration)
  - Enhanced coverage of context management, structured prompting, and automation
- **README.md Resources section enhanced**
  - Added DeepTo Claude Code Guide to Related Guides

### Stats
- 0 new files created (documentation enhancement only)
- 3 files modified (README.md, english-ultimate-claude-code-guide.md, CHANGELOG.md)
- Focus on advanced prompting techniques, cost optimization, and automation workflows
- Integration of community best practices from DeepTo guide

## [2.2.0] - 2026-01-10

### Added
- **ykdojo/claude-code-tips reference integration** (~300 lines, 6 tips)
  - Added to References section in README.md (2 locations: Key inspirations + Related Guides)
  - Added to Learning Sites table in guide (Section 10.3.3, lines 8277, 8500)
  - Listed as peer guide alongside Claudelog and zebbern
  - **Tip 1: Undocumented Commands** integrated in Section 10.1 Commands Table
    - `/usage` - Check rate limits and token allocation
    - `/stats` - View usage statistics with activity graphs
    - `/chrome` - Toggle native browser integration
    - `/mcp` - Manage Model Context Protocol servers
  - **Tips 3+4+8: Keyboard Shortcuts** integrated in Section 10.2
    - Restructured with 2 categories: "Session Control" + "Input & Navigation"
    - `Ctrl+A` - Jump to beginning of line
    - `Ctrl+E` - Jump to end of line
    - `Ctrl+W` - Delete previous word
    - `Ctrl+G` - Open external editor for long text
    - `Ctrl+B` - Run command in background
  - **Tip 5: Session Handoff Pattern** new subsection in Section 2.2 (lines 1252-1308)
    - Complete template with 5 sections (Accomplished, Current State, Decisions, Next Steps, Context)
    - When-to-use table with 5 scenarios (end of day, context limit, switching focus, interruption, debugging)
    - Storage location: `claudedocs/handoffs/handoff-YYYY-MM-DD.md`
    - Pro tip: Ask Claude to generate handoff automatically
  - **Tip 12: GitHub Actions CLI Debugging** new subsection in Section 9.3 (lines 4445-4500)
    - Quick investigation workflow with `gh run` commands
    - Common commands table: list, view, view logs, watch, rerun
    - Practical example combining `gh` with Claude Code
    - Pro tip: Pipe failed logs directly to Claude for analysis
  - **Additional topics worth exploring** section added (lines 8516-8522)
    - 6 non-integrated but pertinent topics from ykdojo listed
    - Voice transcription workflows (superwhisper/MacWhisper)
    - Tmux for autonomous testing
    - cc-safe security tool
    - Cascade multitasking method
    - Container experimentation with Docker
    - Half-clone technique for context trimming

### Changed
- **Guide statistics updated**
  - Guide expanded from 8,505 to 8,929 lines (+424 lines, +5.0%)
  - Word count increased from ~31,280 to 33,219 words (+1,939 words, +6.2%)
  - Reading time updated: "~3 hours" → "~2h15min" (more precise estimate)
- **Version alignment** across documentation
  - english-ultimate-claude-code-guide.md: Version 2.1 → 2.2
  - README.md: Version 2.1 → 2.2
  - CHANGELOG.md: New release 2.2.0 documented

### Stats
- 0 new files created (documentation enhancement only)
- 3 files modified (README.md, english-ultimate-claude-code-guide.md, CHANGELOG.md)
- Guide grew by 424 lines (5.0% growth from v2.1.0)
- Focus on productivity techniques and terminal efficiency
- Integration of battle-tested workflows from Y.K. Dojo

## [2.1.0] - 2026-01-10

### Added
- **Production-ready slash commands** in examples/commands/ (~25 KB)
  - **pr.md** (5.8 KB) - PR creation with scope analysis
    - Complexity scoring algorithm (code files × 2 + tests × 0.5 + directories × 3 + commits)
    - Scope coherence detection (related vs unrelated changes)
    - Semi-automatic split suggestions with git commands
    - Conventional commit format enforcement
    - Complete PR template with TLDR + description + test checklist
  - **release-notes.md** (7.2 KB) - Generate release notes in 3 formats
    - CHANGELOG.md format (Keep a Changelog standard)
    - GitHub Release / PR body format
    - User announcement format (tech-to-product language transformation)
    - Database migration detection (Prisma, Sequelize, Django, Alembic)
    - Semantic versioning determination from commit types
  - **sonarqube.md** (11.3 KB) - Analyze SonarCloud quality issues for PRs
    - Environment variable configuration ($SONARQUBE_TOKEN, $SONAR_PROJECT_KEY)
    - Bash script wrapper to handle zsh authentication issues
    - Node.js analysis script for grouping issues by rule and severity
    - Executive summary with top violators and action plan
    - Severity mapping (BLOCKER/CRITICAL → 🔴, MAJOR → 🟡, MINOR/INFO → 🔵)
- **Production-ready hooks** in examples/hooks/bash/ (~6.5 KB)
  - **dangerous-actions-blocker.sh** (5.2 KB) - PreToolUse security hook
    - Blocks destructive commands (rm -rf /, fork bombs, dd if=, mkfs)
    - Blocks git force push to main/master branches
    - Blocks npm/pnpm/yarn publish without confirmation
    - Detects secrets in commands (password=, api_key=, token= patterns)
    - Protects sensitive files (.env, credentials.json, SSH keys, .npmrc)
    - Path validation with $ALLOWED_PATHS environment variable
    - Generic implementation using $CLAUDE_PROJECT_DIR with fallback to pwd
  - **notification.sh** (1.3 KB) - Notification hook with contextual macOS alerts
    - 5 contextual sound mappings (success, error, waiting, warning, default)
    - Keyword-based context detection (completed/done → Hero.aiff, error/failed → Basso.aiff)
    - Non-blocking background execution
    - Native macOS notifications with osascript
    - Multi-language support (English/French keywords)
- **Comprehensive hooks documentation**
  - **examples/hooks/README.md** (12.4 KB) - Complete hook system guide
    - Available hooks table with 6 hook examples across events
    - Hook events reference (PreToolUse, PostToolUse, UserPromptSubmit, Notification, SessionStart, SessionEnd, Stop)
    - Configuration guide with settings.json examples and matcher patterns
    - Creating custom hooks template with environment variables
    - Best practices (short timeout, fail gracefully, minimal logging)
    - Advanced examples (git context enrichment, activity logger, migration detector)
    - Troubleshooting section (permission issues, timeout errors, jq installation)
- **README.md improvements** for better discoverability
  - Moved "What's Inside" section to line 24 (immediately after intro, before "About This Guide")
  - Added examples/ row to table: "Production-ready commands, hooks, agents | Browse as needed"
  - **DeepWiki interactive documentation explorer** section
    - Link to https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/1-overview
    - 4 bullet points explaining features (natural language queries, contextual navigation, semantic search, on-demand summaries)
    - Tagline: "Perfect for quick lookups when you don't want to read the full 7500+ lines"
  - **Ready-to-Use Examples** section with comprehensive tables
    - Commands table: 6 commands with purpose and highlights (/pr, /release-notes, /sonarqube, /commit, /review-pr, /git-worktree)
    - Hooks table: 4 hooks with events and purposes (dangerous-actions-blocker, notification, security-check, auto-format)
    - Link to examples/README.md for full catalog
- **Guide documentation extensions** (english-ultimate-claude-code-guide.md)
  - **Section 1.3 "Quick Actions & Shortcuts"** expanded (~80 lines)
    - New subsection "Shell Commands with `!`" with 9 concrete examples
      - Quick status checks (!git status, !npm run test, !docker ps)
      - View logs (!tail -f, !cat package.json)
      - Quick searches (!grep -r "TODO", !find . -name "*.test.ts")
    - Comparison table: when to use `!` vs asking Claude
    - Example workflow showing both approaches
    - New subsection "File References with `@`" with usage patterns
      - Single file, multiple files, wildcards, relative paths
      - "Why use `@`" section: precision, speed, context, clarity
      - Comparative example showing with/without `@`
  - Section 10 TL;DR updated with "Copy ready-to-use templates → examples/ directory"
  - Appendix updated with note redirecting to examples/ for production-ready templates

### Changed
- **examples/README.md** updated with new entries
  - Commands table: Added /pr, /release-notes, /sonarqube rows
  - Hooks table: Added dangerous-actions-blocker.sh, notification.sh rows
  - Added note: "See hooks/README.md for complete documentation"
- **README.md restructured** for immediate content comprehension
  - "What's Inside" moved from line 72 to line 24 (48 lines higher)
  - Removed duplicate "What's Inside" section (was at old location)
  - Removed duplicate DeepWiki reference from Resources section
  - Optimal information architecture: Title → Author → What's Inside → About
- **Guide statistics updated**
  - Guide expanded from 7,668 to 8,505 lines (+837 lines, +10.9%)
  - Word count updated to approximately 31,280 words
  - Reading time remains 3 hours (comprehensive read-through)

### Stats
- 6 new files created (~43 KB total)
  - 3 slash commands (pr.md, release-notes.md, sonarqube.md)
  - 2 bash hooks (dangerous-actions-blocker.sh, notification.sh)
  - 1 comprehensive documentation (hooks/README.md)
- 3 files modified (README.md, english-ultimate-claude-code-guide.md, examples/README.md)
- Guide grew by 837 lines (10.9% growth from v2.0.0)
- Focus on production-ready templates and improved documentation discoverability
- All commands and hooks fully generic (no project-specific references)

## [2.0.0] - 2026-01-10

### Added
- **Section 9.12: Git Best Practices & Workflows** (~400 lines)
  - Commit message best practices with Conventional Commits format
  - Git amend workflow with safety rules and verification process
  - Branch management patterns and naming conventions
  - Rewind vs Revert decision tree for different scenarios
  - **Git Worktrees comprehensive documentation**
    - Parallel branch development without context switching
    - Setup process and directory structure
    - Claude Code integration patterns
    - CLAUDE.md memory file strategies for worktrees
    - Best practices and troubleshooting guide
    - Cleanup procedures
- **Section 9.13: Cost Optimization Strategies** (~350 lines)
  - Model selection matrix (Haiku/Sonnet/Opus use cases and costs)
  - OpusPlan mode (Opus for planning, Sonnet for execution)
  - Token-saving techniques (concise CLAUDE.md, targeted @references, proactive compacting)
  - Agent specialization for efficiency
  - Cost tracking with /status command and budget alerts
  - Economic workflows (Haiku for tests, Sonnet for implementation)
  - Token calculation reference with real pricing examples
  - Cost vs productivity trade-offs analysis
  - ROI calculations and cost-effectiveness metrics
- **examples/commands/git-worktree.md** - Slash command template
  - Systematic worktree setup workflow
  - Directory selection priority logic (.worktrees/ vs worktrees/)
  - Safety verification (.gitignore checks)
  - Auto-detection of package managers (pnpm, cargo, poetry, go)
  - Baseline test verification
  - Complete quick reference table
- **8 TL;DR/Recap sections** for improved navigation and learning journey
  - Section 2 TL;DR (Core Concepts) - 2 minute overview of mental model
  - Section 3 TL;DR (Memory & Settings) - 90 second memory hierarchy guide
  - Section 4 TL;DR (Agents) - 60 second quick start guide
  - Section 7 TL;DR (Hooks) - 60 second event system overview
  - Section 9 TL;DR (Advanced Patterns) - 3 minute pattern categories breakdown
  - Section 10 TL;DR (Reference) - 1 minute navigation table
  - Subsection 2.2 Quick Reference (Context Management zones)
  - Section 9 Recap Checklist (Pattern mastery verification before Section 10)
- **Format Enhancements** for better readability
  - Collapsible tables using `<details>` tags for dense content (MCP Server Catalog)
  - C-style comment format (`/*──────*/`) for multi-OS installation commands
  - Quick navigation anchor links at top of all 10 major sections
- **zebbern/claude-code-guide reference** in README Resources
  - New "Related Guides" section grouping zebbern and Claudelog as peer guides
  - Positioned prominently after Official docs section
  - Added context: "Comprehensive reference & troubleshooting guide with cybersecurity focus"

### Changed
- **Updated statistics** throughout documentation
  - Guide expanded from 7,481 to 7,668 lines (+187 lines, +2.5%)
  - Word count: 27,471 words (27K+)
  - Reading time estimate: 2.5 hours → 3 hours (more accurate for full guide)
  - README: "4000+ lines" → "7500+ lines, 27K+ words"
  - PDF Kimi reading time: 2.5 hours → 3 hours
- **Version alignment** across all files to 2.0
  - english-ultimate-claude-code-guide.md: Version 1.0 → 2.0
  - README.md: Version 1.0 → 2.0
  - claude-setup-audit-prompt.md: Version 1.0 → 2.0
  - cheatsheet-en.md: Already 2.0
- **Date updates** to January 2026
  - All "Last updated" fields across documentation
  - Status Overview Table dates (Jan 2025 → Jan 2026)
  - Pricing model reference date (January 2026)
  - Footer timestamps in all major files

### Fixed
- Removed duplicate Claudelog reference from "Frameworks & Tools" section (was in both Key inspirations and Resources)
- Improved organization of Resources section with clearer categorization

### Stats
- Guide now 7,668 lines (from 6,250 lines in v1.2.0)
- Added 187 lines of TL;DR/navigation content
- ~23% growth from v1.2.0
- Focus on user experience optimization and learning journey enhancement
- Major version bump reflects structural documentation paradigm shift (learning-focused TL;DRs throughout)

## [1.2.0] - 2025-01-10

### Added
- **Section 1.6: Migration Patterns** (~230 lines)
  - Complete guide for transitioning from GitHub Copilot to Claude Code
  - Cursor to Claude Code migration strategies
  - Hybrid workflow recommendations (when to use which tool)
  - Week-by-week migration checklist
  - Common migration issues and solutions
  - Success metrics and productivity indicators
- **Section 2.2: Cost Awareness & Optimization** (~220 lines)
  - Detailed pricing model breakdown (Sonnet/Opus/Haiku)
  - Cost optimization strategies (5 actionable patterns)
  - Real-world cost examples and ROI calculations
  - Budget tracking and cost-conscious workflows
  - Cost vs. value analysis (when to optimize, when not to)
  - Red flags for cost waste indicators
- **Section 9.3: Release Notes Generation** (~280 lines)
  - Command-based release notes automation
  - CI/CD integration for automated changelog
  - Interactive workflow for manual control
  - Three output formats (CHANGELOG.md, GitHub Release, User Announcement)
  - Best practices and common issues
  - Complete examples with real commit history
- **Section 10.4: Enhanced Troubleshooting** (~170 lines added)
  - MCP server connection issues (Serena, Context7, Sequential)
  - Permission pattern matching problems
  - Timeout handling strategies
  - Platform-specific installation issues (Windows, macOS, Linux)
- **Appendix A.10: Emergency Hotfix Checklist** (~140 lines)
  - Step-by-step hotfix protocol (8 phases)
  - Time-based decision matrix (<5 min to >30 min)
  - Claude Code hotfix-specific commands
  - Hotfix anti-patterns and best practices
  - Communication templates for incident updates
- **Appendix A.11: Git Archaeology Pattern** (~250 lines)
  - 6 archaeology patterns (mysterious code, feature evolution, bug introduction)
  - Claude-optimized git commands for investigation
  - Real-world examples (workarounds, breaking changes, dead code)
  - Archaeology prompt template
  - Finding domain experts via git history
- Enhanced Windows disclaimer in README (more visible, actionable)
- Updated `claude-setup-audit-prompt.md` with new checklist items
  - Cost Awareness evaluation criteria
  - Migration Patterns assessment
  - Release Notes automation check
  - Emergency procedures documentation
  - Git archaeology usage patterns

### Changed
- Improved Windows support visibility in README
  - Changed from small note to prominent callout box
  - Added specific areas of concern (PowerShell, paths, batch files)
  - Clear call-to-action for Windows contributors
  - Status indicator for platform support

### Stats
- Guide expanded from ~4955 lines to ~6250 lines (~26% growth)
- Added ~1300 lines of high-value, practical content
- 6 major new sections addressing real-world developer needs
- Focus on cost optimization, migration, and production scenarios

## [1.1.0] - 2025-01-10

### Added
- Comprehensive Windows compatibility support
  - PowerShell hook templates
  - Windows-specific paths throughout documentation
  - PowerShell profile setup instructions
  - Batch file alternatives where applicable
- Windows disclaimer in README (author on macOS, Windows untested)
- DeepWiki exploration link for interactive repository discovery
- `llms.txt` file for AI indexation

### Changed
- Installation instructions now prioritize npm (cross-platform)
- Cheatsheet updated with dual-platform paths (macOS/Linux + Windows)
- Audit prompt includes Windows paths

## [1.0.0] - 2025-01-09

### Added
- Complete Claude Code guide (4700+ lines)
  - Section 1: Quick Start
  - Section 2: Core Concepts (Context Management, Plan Mode, Rewind)
  - Section 3: Memory & Settings (CLAUDE.md, .claude/ folder)
  - Section 4: Agents (Custom AI personas, Tool SEO)
  - Section 5: Skills (Reusable knowledge modules)
  - Section 6: Commands (Custom slash commands)
  - Section 7: Hooks (Event-driven automation)
  - Section 8: MCP Servers (Serena, Context7, Sequential, Playwright)
  - Section 9: Advanced Patterns (Trinity, CI/CD, Vibe Coding)
  - Section 10: Reference (Commands, Troubleshooting, Checklists)
  - Appendix: Templates Collection
- 1-page printable cheatsheet (`cheatsheet-en.md`)
- Setup audit prompt (`claude-setup-audit-prompt.md`)
- PDF versions for offline reading
- NotebookLM audio deep dive

### Documentation
- README with quick start guide
- Table of contents with anchor links
- Quick links by topic
- Who Is This For section

## [0.1.0] - 2025-01-08

### Added
- Initial repository structure
- License (CC BY-SA 4.0)
- .gitignore for common patterns
