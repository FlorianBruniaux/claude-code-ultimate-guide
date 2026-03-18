# Resource Evaluation: mcp2cli (knowsuchagency)

**Date**: 2026-03-17
**Evaluator**: Claude Sonnet 4.6
**Resource URL**: https://github.com/knowsuchagency/mcp2cli
**Resource Type**: Open-source CLI tool (GitHub)
**Author**: knowsuchagency (Stephan Fitzpatrick)
**Published**: 2026-03-09
**Stars**: 1,261 | **License**: MIT | **Language**: Python

---

## Executive Summary

mcp2cli converts MCP servers, OpenAPI specs, and GraphQL schemas into runtime CLI commands, eliminating tool schema injection from LLM prompts. The project claims 96-99% token savings by removing schema overhead, with an additional 40-60% via TOON encoding on array output. Created 8 days ago, it has 1,261 stars and a Claude Code skill integration. The architectural insight is real — MCP tool schema injection is a documented cost driver in agentic workflows — but the tool is too new for production recommendation. There is also a structural mismatch with Claude Code's internal MCP architecture: Claude Code manages MCP connections natively, so mcp2cli's schema-elimination approach doesn't map cleanly onto the standard Claude Code workflow.

---

## Content Summary

- **Core mechanic**: converts MCP server definitions, OpenAPI specs, and GraphQL schemas into runtime CLI tools with zero codegen, calling the underlying server on invocation
- **Token savings claims**: 96-99% reduction by removing tool schema injection from prompts; 40-60% additional via TOON (Tree-Optimized Output Notation) on array output
- **Features**: OAuth support, spec caching, secrets management, `bake` mode (batch commands), jq integration for filtering
- **Claude Code skill**: `npx skills add knowsuchagency/mcp2cli --skill mcp2cli` — installs as a skill for direct use in sessions
- **Supported sources**: MCP servers (stdio, HTTP/SSE), OpenAPI 2.x/3.x, GraphQL schemas
- **Contributors**: 3 | **Open issues**: 0 | **Last commit**: 2026-03-17

---

## Gap Analysis vs. Guide

| Area | mcp2cli | Guide coverage |
|------|---------|----------------|
| MCP schema overhead documentation | ✅ Addresses directly | ❌ Not documented anywhere |
| Token cost of MCP tool injection | ✅ Core value prop | ❌ Gap — not mentioned in cost section |
| CLI vs MCP tradeoff pattern | ✅ Practical tool for this | ⚠️ Mentioned at concept level, no concrete tooling |
| RTK-style output filtering | ❌ Different mechanism (schema removal, not output filtering) | ✅ RTK covered |
| Claude Code MCP integration | ⚠️ Structural mismatch (see Risk) | ✅ Covered in mcp-servers-ecosystem.md |
| OpenAPI/GraphQL → CLI conversion | ✅ | ❌ Not covered |

**Real gap**: the guide does not document MCP tool schema overhead as a cost driver. This is worth adding to the cost optimization or MCP ecosystem sections, independent of whether this specific tool is recommended.

---

## Risk Assessment

**Structural mismatch with Claude Code**: Claude Code manages MCP connections internally via its own runtime. mcp2cli's primary value proposition — replacing MCP tool injection with CLI calls — does not apply to the standard Claude Code workflow where tool schemas are injected by the host. The Claude Code skill (`npx skills add`) is the intended integration path, but it positions mcp2cli as a complementary tool rather than a replacement for native MCP. Users expecting "install mcp2cli, save 96% tokens in Claude Code" will be disappointed. The actual use case is closer to: use mcp2cli in scripts, hooks, or non-Claude Code contexts where you control the tool injection.

**Maturity**: 8 days old. No production track record. 0 open issues could mean the tool is solid or could mean it hasn't been stress-tested yet. The Python dependency stack (typer, httpx, pydantic) is mature, but the integration surface with arbitrary MCP servers is wide.

**Token savings claims**: the 96-99% figure references an external blog post and does not include a controlled benchmark against a defined baseline. TOON encoding savings are plausible for array-heavy output but not independently verified.

---

## Score

**Score: 3/5** (Moderate — Watch list)

Real problem, real approach, credible engineering (MIT, active dev, 1K+ stars in one week). The structural mismatch with Claude Code's architecture and the 8-day maturity are the limiting factors. The architectural insight about schema overhead is worth documenting in the guide even if the tool itself isn't ready for a primary recommendation.

---

## Challenge

**Challenge**: "1,261 stars in 8 days is a recency bubble. The guide has a track record problem with early hype. Score should be 2/5."

**Response**: The concern is valid for production recommendation. However, 3/5 here reflects "watch list + document the insight," not "integrate now." The architectural gap (MCP schema overhead is not mentioned anywhere in the guide) is real and independent of mcp2cli's maturity. If the tool were 2/5, the insight would still be worth documenting. Score stays at 3/5 with explicit maturity caveat.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| 1,261 stars | ✅ | GitHub API — created 2026-03-09, checked 2026-03-17 |
| MIT license | ✅ | LICENSE file in repo |
| Claude Code skill integration | ✅ | `npx skills add knowsuchagency/mcp2cli --skill mcp2cli` in README |
| 96-99% token savings | ⚠️ | Claimed in README, references external blog — not independently verified |
| TOON encoding | ⚠️ | Described in README, no independent benchmark |
| 3 contributors, 0 open issues | ✅ | GitHub API |
| Python, typer, httpx | ✅ | pyproject.toml |

---

## Decision

**Score: 3/5 — Watch list. Document the architectural insight now, revisit the tool recommendation in 3 months.**

**Immediate action (guide)**: Add a note in `guide/ecosystem/mcp-servers-ecosystem.md` (or the cost optimization section of the ultimate guide) documenting MCP tool schema overhead as a token cost driver. This insight exists independently of mcp2cli.

**Deferred action**: If mcp2cli reaches 200+ stars sustained after the initial wave, has 10+ contributors, and has documented real-world usage with Claude Code specifically, revisit for mention in `guide/ecosystem/third-party-tools.md`.

**What NOT to do**: Do not mention mcp2cli as a production tool for Claude Code token savings without clarifying the structural mismatch with Claude Code's native MCP architecture.

**Confidence**: High on architecture analysis. Medium on token savings claims (unverified externally). High on maturity assessment.
