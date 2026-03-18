# Resource Evaluation: Context7 CLI (ctx7)

**URL**: https://context7.com/docs/clients/cli
**Date**: 2026-03-17
**Evaluator**: Claude Sonnet 4.6
**Score**: 4/5

## Summary

CLI companion to the Context7 MCP server (Upstash). Covers three functions: fetch library docs in terminal, manage skills (install/search/suggest/generate), configure Context7 for Claude Code.

Key commands:
- `npx ctx7 skills suggest` — auto-detects project deps, recommends matching skills
- `npx ctx7 skills install owner/repo` — install from any GitHub repository
- `npx ctx7 setup --claude` — wizard for MCP or CLI+Skills mode configuration
- `npx ctx7 library [name]` / `ctx7 docs [id] [query]` — doc lookup without browser

## Decision

**Integrated** into `guide/ultimate-guide.md` §5.5 as new subsection "Registry-based Discovery: ctx7 CLI" (~60 lines) and a cross-reference note in `guide/ecosystem/mcp-servers-ecosystem.md` Context7 section.

## Key Finding

The existing workflow (curl/unzip from GitHub) is replaced by `ctx7 skills suggest` + `ctx7 skills install`, which adds dependency-awareness and trust scores. The guide was documenting a 2024 manual workflow for a 2025 ecosystem.

## Fact-Check Note

First WebFetch call hallucinated "Built by Anthropic" for Context7 — this is false. Context7 is an Upstash product (confirmed via mcp-servers-ecosystem.md: `@upstash/context7-mcp`). Corrected before integration.

## Registry Relationship

- `agentskills.io` = open spec (30+ platforms, defined skill format) — guide §5.1
- `context7.com/skills` = hosted registry of conforming skills with trust scores
- These are complementary, not competing. Documented in the guide integration.
