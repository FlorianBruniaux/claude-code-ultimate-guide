# Ideas to Dig

> Research topics for future guide improvements. Curated and validated.

## Done

### MCP Security Hardening ✅
Unified security research covering MCP vulnerabilities, prompt injection, and secret detection.

**Completed**: [Security Hardening Guide](./guide/security/security-hardening.md) covers:
- CVE-2025-53109/53110, 54135, 54136 with mitigations
- MCP vetting workflow with 5-minute audit checklist
- MCP Safe List (community vetted)
- Prompt injection evasion techniques (Unicode, ANSI, null bytes)
- Secret detection tool comparison (Gitleaks, TruffleHog, GitGuardian)
- Incident response procedures (secret exposed, MCP compromised)
- 3 new hooks: `unicode-injection-scanner.sh`, `repo-integrity-scanner.sh`, `mcp-config-integrity.sh`

---

## High Priority

### gstack-inspired commands (deferred from 2026-03-26 audit)

Audit of [gstack](https://github.com/garrytan/gstack) (Garry Tan's Claude Code sprint toolkit) identified these gaps. HIGH-priority items were already implemented (`/investigate`, `/qa`, `/canary`, `/land-and-deploy`, `/review-pr` updates). Remaining items deferred here.

**`/autoplan`** — single command that chains CEO → Design → Eng review automatically with encoded decision principles. Classify decisions as Mechanical (auto-decide) vs Taste (surface to user). Prerequisite: our `/plan-ceo-review` and `/plan-eng-review` commands must be stable first. Source: `gstack/autoplan/SKILL.md`.

**`/office-hours`** — YC-style product diagnostic with 6 forcing questions before any planning. Upstream of `/plan-ceo-review`. Writes a design brief to `~/.claude/projects/`. Source: `gstack/office-hours/SKILL.md`.

**`/design-review`** — live-site visual audit + fix loop. Screenshots a URL, audits spacing/typography/color/contrast, detects AI slop patterns (purple gradients, 3-column grids, centered everything). Requires browser tooling standardization first. Source: `gstack/design-review/SKILL.md` + `design-checklist.md`.

**`/benchmark`** — Core Web Vitals regression detection (TTFB, FCP, LCP, DOM load, bundle sizes). Baseline comparison with regression thresholds (>50% OR >500ms = regression). Source: `gstack/benchmark/SKILL.md`.

**`/retro`** — weekly retrospective with git log analysis per contributor. Current vs prior window. Source: `gstack/retro/SKILL.md`.

**`/freeze` + `/unfreeze`** — runtime directory edit lock via PreToolUse hook (hard deny, not warning). State file at `~/.claude/freeze-dir.txt`. Composable with `/careful` into a `/guard` command. Source: `gstack/freeze/SKILL.md`.

**`/document-release`** — post-ship documentation updates. Reads diff since last release, updates README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md, polishes CHANGELOG, cleans TODOS. Source: `gstack/document-release/SKILL.md`.

**Effort compression tables** — add to skill templates: human time vs AI time per task type. Architecture decision for skill format — discuss before implementing across all skills.

**Trigger to implement**: reader requests, or when we do a "workflow completeness" sprint.

---

### Agent Skills — Documentation Gaps (from agentskills.io official docs, 2026-05-14)

Six factual items confirmed missing from the guide's skills chapter after cross-referencing with the official agentskills.io specification and client implementation guide.

**[HIGH] Cross-client directory convention `.agents/skills/`** — The guide only documents `.claude/skills/` (Claude Code-specific). The open standard defines `.agents/skills/` (project) and `~/.agents/skills/` (user) as the cross-client paths. Skills placed there work across all 35+ compatible clients. This distinction directly affects portability claims. Add to the "Where Skills Live" section.

**[HIGH] 4-level skill loading priority** — The guide doesn't document the full hierarchy: Enterprise → Personal → Project → Plugins. Currently the guide implies only Personal vs Project. Enterprise (managed settings, highest priority) and Plugins (lowest) are missing. Add to the priority hierarchy section.

**[MEDIUM] Progressive disclosure token costs** — The spec gives concrete numbers: ~50-100 tokens/skill for catalog (name + description only), <5000 tokens recommended for full SKILL.md body, on-demand for resources. The guide explains the concept but never gives token figures. Useful for readers deciding how many skills to install.

**[MEDIUM] 500-line SKILL.md body limit** — The spec recommends keeping SKILL.md under 500 lines. Not documented anywhere in the guide. Add as a practical rule of thumb in the structure section.

**[MEDIUM] `name` must match parent directory name** — The spec requires this as a structural constraint. The guide documents character/format rules for `name` but omits this requirement. A mismatch causes `skills-ref validate` to fail.

**[LOW] Eval storage convention** — The spec defines a standard file layout: `evals/evals.json` inside the skill folder + `my-skill-workspace/iteration-N/with_skill|without_skill/` for eval runs. Not documented in the guide's evaluation section. Matters for cross-tool compatibility with the `skill-creator` meta-skill.

**Source**: `claudedocs/anthropic-cert/01-agent-skills/agentskills-io-docs.md` (sections 2, 6, 8)

---

## Medium Priority

### CI/CD Workflows Gallery ✅

**Completed**: [GitHub Actions Workflows](./guide/workflows/github-actions.md) — 5 patterns using `anthropics/claude-code-action` (PR review, auto-review, issue triage, security, scheduled maintenance). Includes cost control, fork safety, Bedrock/Vertex auth alternatives. Cross-linked from section 9.3 of the main guide.

### MCP Server Catalog
Exhaustive list of MCP servers with real-world use cases.

**Topics:**
- Available servers by category (dev tools, databases, APIs)
- Performance benchmarks vs native tools
- Security trust levels per server
- Custom server development patterns

**Perplexity Query:**
```
MCP Model Context Protocol servers catalog 2024-2025:
- Most useful servers for developers
- Performance comparison MCP vs native tools
- How to build custom MCP servers
```

---

## Lower Priority

### CLAUDE.md Patterns Library
Stack-specific templates for common project types.

**Topics:**
- React/Next.js optimized configurations
- Python/FastAPI patterns
- Go project conventions
- Monorepo configurations

**Perplexity Query:**
```
CLAUDE.md configuration examples by framework:
- React, Next.js, Vue patterns
- Python, FastAPI, Django patterns
- Best practices from GitHub repositories
```

---

## Watching (Waiting for Demand)

a### prompt-caching MCP Plugin

MCP plugin that automates `cache_control` placement for developers building apps on the Anthropic SDK. Evaluated through a local installation connected to Claude Code.

**Status:** Testing in progress. Real usage data required before any documentation decision.

**What we know:**
- 29 stars, v1.3.0, solo maintainer — maintenance risk
- Author-reported benchmarks (80-92% savings) — unverified, cannot cite
- Fills a real gap: no other MCP tool does this; Spring AI / LiteLLM / Pydantic AI serve different audiences
- Blog post (Mathieu Grenier) independently documents the same pain point + 5 antipatterns — score 3/5, worth integrating in "Strategy 6" regardless

**Open questions:**
- [ ] Do real sessions on this project actually hit the cache? (run `get_cache_stats` after 10+ turns)
- [ ] Is the plugin stable enough to recommend? Any errors, memory leaks, session issues?
- [ ] What are the real savings on a CLAUDE.md-heavy project like this guide?

**If test results are positive (cache hits confirmed, no stability issues):**
- Add to `guide/ecosystem/third-party-tools.md` with verified stats (not README claims)
- Add to landing third-party tools section
- Score upgrade: 3/5 → 4/5

**If test results are inconclusive or plugin is unstable:**
- Move to Discarded Ideas
- Keep the Mathieu Grenier blog post integration (independent value)

**Check again:** After 1 week of real usage

---

### Multi-LLM Consultation Patterns
Using external LLMs (Gemini, GPT-4) as "second opinion" from Claude Code.

**Status:** No proven demand. Add if 3+ reader requests.

**Research done (Jan 2026):**
- Simple approach: Bash script calling Gemini API
- Production approach: [Plano](https://github.com/katanemo/plano) (overkill for solo devs)
- Community adoption: Near zero in Claude Code users

**If implementing:**
- `examples/scripts/gemini-second-opinion.sh`

### Type-Driven API Design for AI Agent Efficiency
Schema-first development impact on Claude Code token consumption.

**Status:** Anecdotal only (no empirical data). Reevaluate if benchmarks emerge.

**Resource evaluated (Feb 2026):**
- [ShipTypes](https://shiptypes.com/) by Boris Tane (Cloudflare)
- **Score:** 2/5 (Marginal) — Claims "types → fewer tokens" unverified
- **Full evaluation:** `docs/resource-evaluations/shiptypes-evaluation.md`

**What's missing:**
- Benchmark comparing token consumption: typed APIs (tRPC/Zod) vs untyped (REST/docs)
- A/B test showing AI agent iterations with/sans types
- Case study with reproducible metrics

**Reevaluation triggers:**
- [ ] Academic paper/blog with empirical data (token consumption metrics)
- [ ] Anthropic official recommendation on schema-first for Claude Code
- [ ] 5+ community discussions/issues requesting this topic

**If validated (score upgrade to 4/5):**
- Add subsection in `guide/core/methodologies.md` (after CDD, line 172)
- Use micro-integration template: `docs/resource-evaluations/shiptypes-evaluation.md` (section "Integration Plan")

**Check again:** August 2026
- 3-line mention in "See Also" section
- No full guide (maintenance burden, scope creep)

**Source:** [daily.dev article](https://app.daily.dev/posts/make-claude-code-opus-talk-to-gemini-pro-b7pyiq394)

### Vibe Coding Discourse

Evolution of the "developer as architect" narrative in AI-assisted development.

**Reference:** [Craig Adam - "Agile is Out, Architecture is Back"](https://medium.com/@craig_32726/agile-is-out-architecture-is-back-7586910ab810)

**Status:** Watching. Term "vibe coding" now mainstream (Collins Word of the Year 2025).

---

## Discarded Ideas

| Idea | Reason Discarded |
|------|------------------|
| LLM Fine-tuning guide | Out of scope - users don't control model training |
| Model architecture internals | Too theoretical, not actionable |
| Token pricing optimization | Changes too frequently, use official docs |
| A2A Protocol (Agent-to-Agent) | Claude Code is single-agent with sub-agents, not true multi-agent |
| AgentOps Enterprise Dashboard | Infrastructure doesn't exist for CLI tool |
| LLM-as-a-Judge evaluation | Overkill for CLI, adds latency without proportional value |
| Decision Trajectory logging | No access to internal traces (black box) |
| 4 Pillars formal framework | Too academic - guide already covers symptoms pragmatically |
| Canary/Blue-Green deployments | Infrastructure patterns, not relevant for CLI |
| Memory Poisoning defenses | Theoretical risk requiring prior system compromise |
| Prompt Engineering for Code Gen | Already well covered (xml_prompting, prompt_formula) |
| Context Window Optimization | Already well covered (context_management, context_triage) |
| Task Decomposition Patterns | Covered via plan_mode, interaction_loop |
| Agent Architecture Comparisons | Out of scope - not multi-agent theory |
| Real-World Case Studies | Non-verifiable metrics, marketing-prone |
| Comparison with Other Tools | Out of scope, rapid obsolescence |

---

## Contributing

Found something interesting? Add it with:
1. Topic name and why it matters
2. Specific research questions
3. Perplexity query to start
