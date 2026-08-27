# Resource Evaluation: Supermemory

**Resource**: supermemoryai/supermemory - Memory API and Context Engine
**URL**: https://supermemory.ai/ | https://github.com/supermemoryai/supermemory
**Type**: MCP server / Cloud API / Self-hostable binary / Claude Code plugin
**Evaluated**: 2026-08-27
**Evaluator**: Florian BRUNIAUX + Claude (Anthropic)

---

## Quick Summary

**Score**: **3/5** (Moderate - integrate when time available)

Supermemory is a VC-backed ($29M seed, Oct 2025) memory API and context engine with three separate integration surfaces for Claude Code: a free, no-login generic MCP endpoint (`mcp.supermemory.ai/mcp`), a paid Claude Code plugin (`claude-supermemory`, Pro plan required at $19/mo minimum), and a self-hostable MIT-licensed local binary that is explicitly single-tenant, even self-hosted. The guide has no coverage gap this closes: single-user cross-session memory is already documented (§3.1-3.8), and Supermemory's team story does not out-perform the guide's existing §4.7 thesis that no tool has solved shared memory cheaply. Its most useful contribution to the guide is not a new capability, it is two concrete, sourced data points: a same-vendor internal contradiction in benchmark numbers (95% vs 85.4% Recall@15 on the same benchmark), and a paid-from-first-use Claude Code integration where every comparable single-user tool already documented (claude-mem, doobidoo, Mem0 Cloud MCP) is free at that tier.

---

## Content Summary

**What Supermemory does**: a hosted memory API (REST + MCP) that ingests documents, conversations, and connector data (Google Drive, Notion, Gmail, OneDrive, cloud-only) and serves them back via semantic retrieval, scoped by "container tags." Three distinct products share the name:

1. **Supermemory MCP** (github.com/supermemoryai/supermemory-mcp): the generic `mcp.supermemory.ai/mcp` endpoint. Free, no login, usable from any MCP client including Claude Code today.
2. **claude-supermemory plugin** (github.com/supermemoryai/claude-supermemory): a Claude-Code-specific plugin with `memory`/`recall`/`context` tools and a `/context` command. Requires a Supermemory Pro plan or above, $19/mo minimum, not usable on the free tier. Last referenced update: "Claude Supermemory V2," 2026-02-09.
3. **Supermemory local**: a self-hosted single binary, MIT-licensed (confirmed by reading the cloned repo's `LICENSE` file, copyright 2025 supermemory). Single-tenant, single API key, no multi-member team access even self-hosted. Connectors are cloud-only and absent from this mode.

**Multi-tenancy model**: "container tags" (a hard isolation boundary) plus org roles and scoped API keys, functionally closer to Mem0's `user_id` scoping than to Letta's shared memory blocks or Memoria's group branches. No documented merge or conflict-resolution semantics between personal and team memory; that is left to application logic.

**Security posture**: TLS in transit, AES-256-class encryption at rest, SOC 2 Type II certified, GDPR-aligned deletion (container = unit of deletion), HIPAA BAA available. All three compliance items (SOC 2, GDPR workflow guarantees, HIPAA BAA) are gated to Scale/Enterprise plans, not Free/Pro. Two GitHub issues are open and unresolved as of the research date: "Privacy and Security Concerns for Multi-User Application" and "Is end-to-end encryption supported?" No E2E encryption exists today.

**Benchmark claims** (all self-reported, sourced from supermemory.ai/research and supermemory.ai/docs/memorybench): #1 on LongMemEval, LoCoMo, ConvoMem; 95% Recall@15 at 99.4% context reduction; sub-300ms recall; 10x faster than Zep, 25x faster than Mem0; 100B tokens/month across "hundreds of customers." No third-party reproduction was found for any of these. The benchmark harness (MemoryBench) is open source, but every published number is Supermemory's own run.

---

## Relevance Score: 3/5

### Why 3/5 (Moderate)?

**Strengths**:

1. **Real, funded, actively maintained product**: $29M seed (Oct 2025, Browder Capital / Scientifica Venture Capital / Susa Ventures leads, angels including Jeff Dean and Logan Kilpatrick per a third-party profile), MIT-licensed core confirmed by direct file inspection, a genuinely free and login-free MCP entry point usable in Claude Code today.
2. **Readers will ask about it**: given the funding and marketing visibility, silence in a guide that already documents 15+ memory tools is a gap, even a moderate one.
3. **Concrete cross-reference value for two existing sections**: the 95%/85.4% internal benchmark inconsistency is a documented, sourced illustration of the skepticism the guide's §9 already recommends ("numbers reported by tool vendors... should be read skeptically"). The container-tags team model, with no merge semantics and mono-tenant self-hosting, is a fresh, sourced data point for §4.7's "no team taxonomy standard" and "single-tenant DNA" arguments, not a counter-example to them.

**Why not higher (4-5)**:

1. **No new capability class**: Supermemory's single-user surface (MCP-based semantic memory) is a pattern the guide already documents multiple times over (claude-mem, agentmemory, ICM, doobidoo, OpenMemory MCP). It does not fill a gap the way claude-mem's automatic session capture did.
2. **Its team story does not advance the guide's argument, it confirms it**: container tags are architecturally closer to Mem0's existing `user_id` scoping than to anything new, and the self-hosted mode explicitly has no multi-user access at all.
3. **Commercial friction on the one surface with the Claude Code name attached**: the `claude-supermemory` plugin is paid from the first real use ($19/mo minimum), while every single-user tool the guide already recommends (claude-mem, doobidoo, Mem0 Cloud MCP's free tier) is free at that tier. This is a genuine adoption obstacle, not a detail.
4. **Zero independently reproduced benchmark numbers, plus an internal contradiction**: every headline claim is self-reported, and the vendor's own site publishes two different values (95% vs 85.4%) for the same benchmark on two different pages. This is worse verification standing than agentmemory, mem0, or Letta, which at least appear together in a third-party-adjacent harness cited in the guide's existing §9 Representative Results table.
5. **Unresolved open issues on the exact concern a security-conscious reader would check**: multi-user privacy and E2E encryption, both flagged as open on the tracker with no fix at the time of research.

### Comparison to Existing Coverage

| Aspect | Supermemory | Guide's existing coverage (§3-4, v3.42.0) |
|--------|-------------|---------------------------------------------|
| Free, no-login single-user MCP | Yes (`mcp.supermemory.ai/mcp`) | Already covered by claude-mem, doobidoo, OpenMemory MCP |
| Self-hosted, MIT-licensed local binary | Yes, single-tenant only | Already covered by doobidoo (SQLite-vec), ICM |
| Native Claude Code plugin with dedicated tools | Yes, but Pro-gated ($19/mo) | claude-mem is free (AGPL-3.0) and does this natively |
| Team/shared memory | Container tags, cloud-only, no self-host multi-user | Mem0 Cloud MCP (`user_id` wildcards) already covers this pattern; Supermemory does not exceed it |
| Independently reproduced benchmarks | None found; internal inconsistency documented | §9 already has a cross-tool table (agentmemory, BM25 baseline, Letta, mem0) with a reproducibility column; Supermemory would add a "no" row plus a footnote-worthy inconsistency |
| Provenance/source tracking per fact | Not detailed in this research pass | Not a differentiator found |

**Summary**: the guide already has category-level coverage for everything Supermemory does technically. Its incremental value is documentary (two sourced facts that sharpen two existing arguments), not a new capability that changes what a reader should do.

---

## Fact-Check Results

| Claim | Source | Status | Notes |
|-------|--------|--------|-------|
| $29M seed funding, Oct 2025 ($3M + $26M) | startupintros.com/orgs/supermemory | Externally anchored | Third-party profile, not a primary filing (no press release or SEC-equivalent source located) |
| Founder Dhravya Shah, SF-based | Same source | Externally anchored | Started as an open-source side project before the seed rounds |
| MIT license, main repo | LICENSE file, direct inspection of the cloned repo at `/Users/florianbruniaux/Sites/divers-test/supermemory` | Verified directly | Copyright 2025 supermemory |
| SOC 2 Type II, GDPR deletion workflow, HIPAA BAA | supermemory.ai/docs/overview/security | Company-stated | Gated to Scale/Enterprise plans, not Free/Pro; no independent audit report located |
| claude-supermemory plugin requires Pro ($19/mo min.) | github.com/supermemoryai/claude-supermemory | Company-stated, structurally verifiable | Confirmed by the plugin's own stated requirement, not by testing a live signup |
| Supermemory MCP is free, no login, separate from the plugin | github.com/supermemoryai/supermemory-mcp | Company-stated, structurally verifiable | Do not conflate the two integrations; they have different repos, different pricing |
| Self-hosted local binary is single-tenant, no multi-user even self-hosted | supermemory.ai/docs/self-hosting/local-vs-enterprise, supermemory.ai/docs/self-hosting/overview | Company-stated | Consistent with the mono-tenant framing across the docs; no contradicting evidence found |
| Connectors (Drive, Notion, Gmail, OneDrive) are cloud-only | Same self-hosting docs | Company-stated | Not testable without a paid account |
| #1 on LongMemEval/LoCoMo/ConvoMem, 95% Recall@15, 99.4% context reduction, sub-300ms, 10x/25x faster than Zep/Mem0 | supermemory.ai/research, supermemory.ai/research/longmembench | **Unverified, self-reported only** | No third-party reproduction found; MemoryBench harness is open source but all published runs are the vendor's own |
| 85.4% Recall@15 on LongMemEval_s (same benchmark as the 95% claim above) | supermemory.ai/blog/supermemory-vs-pinecone-which-is-better | **Unverified, and internally inconsistent with the 95% claim** | Both numbers are self-published by Supermemory, on different pages, for the same headline claim on the same product |
| Two open GitHub issues on multi-user privacy and missing E2E encryption | github.com/supermemoryai/supermemory/issues | Verified as open at research time | Both unresolved as of the source snippet; no fix timeline stated |
| Direct architecture comparison to Mem0, Zep, Letta | Perplexity Deep Research pass | **Not available in usable, sourced detail** | Only Cognee was covered with enough specificity to cite; do not present a Mem0/Zep/Letta comparison as researched |
| GitHub star count for the main repo | Not captured in this research pass | **Not verified** | Do not state a star count for Supermemory in the guide without a fresh, dated GitHub API check (the pattern claude-mem-evaluation.md and memory-systems.md §3.8/§4.6 already follow for every other tool) |

---

## Limitations & Considerations

1. **Pricing friction on the named Claude Code integration**: `claude-supermemory` is not usable below $19/mo. A reader who wants "the Supermemory Claude Code plugin" specifically, not the generic MCP, hits a paywall on first real use.
2. **No independent benchmark verification, plus a self-published inconsistency**: treat every performance number on supermemory.ai as marketing until reproduced. The 95%/85.4% conflict is worth citing verbatim as a caution, not summarizing away.
3. **Team memory is not more advanced than what the guide already documents**: container tags are a scoping primitive, not a merge or conflict-resolution model. Self-hosting has no multi-user story at all.
4. **Security gaps that matter for a team-shaped feature**: no E2E encryption, two unresolved GitHub issues naming exactly that gap, and the strongest compliance claims (SOC 2, HIPAA BAA) live behind Enterprise pricing.
5. **Research completeness gap**: the source research pass could not produce a sourced, detailed Mem0/Zep/Letta comparison, only Cognee. Any future update that wants that comparison needs a dedicated research pass, not an extrapolation from this file.
6. **No verified star count or independent production-usage evidence** at the time of this evaluation; do not state adoption numbers without a fresh, dated check.

---

## Decision

**Score**: **3/5** (Moderate - integrate when time available)

**Action**:
1. Add Supermemory as an entry in `guide/core/memory-systems.md` §3.8 (Other Notable Tools): a table row plus a short paragraph in the style already used for Memori and codebase-memory-mcp, covering the free MCP endpoint, the paid plugin, and the self-hosted single-tenant binary.
2. Add a row to the §3.9 Master Comparison Table.
3. Add one to two sentences to §4.7 (Why the Team Gap Is Structural), attaching Supermemory's container-tags model and paid-plugin pricing to the existing "no team taxonomy standard" and "no enterprise buyer yet" bullets, as supporting evidence, not a rewrite.
4. Add a short paragraph to §9 (Benchmarks and Evaluation) citing the 95%/85.4% internal inconsistency as a concrete, sourced illustration of the section's existing skepticism guidance.

See `claudedocs/supermemory-integration-plan.md` for exact insertion points and section-by-section content plans.

**Confidence**: Moderate. Company-stated facts about pricing, licensing, and architecture are internally consistent and structurally verifiable (repo files, docs pages). Funding and founder facts rely on a single third-party profile, not a primary source. All performance claims are unverified by design (self-reported, no reproduction found), which the plan treats as the point worth documenting rather than a blocker.

---

**Evaluated**: 2026-08-27
**Next Review**: Before actual integration into memory-systems.md
**Status**: Evaluation complete, integration plan written, guide not yet edited
