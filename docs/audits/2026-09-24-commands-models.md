# Commands and models audit, September 24, 2026

The operational references were checked against the official documentation fetched on September 24 and the Claude Code changelog through v2.1.281. This is a documentation and example-code audit, not a live test of every plan, provider, or model API.

## Sources

- [Claude Code model configuration](https://code.claude.com/docs/en/model-config): aliases, provider differences, account defaults, effort, persistence, and thinking controls.
- [Command reference](https://code.claude.com/docs/en/commands), [CLI reference](https://code.claude.com/docs/en/cli-reference), and [interactive controls](https://code.claude.com/docs/en/interactive-mode): commands, flags, and shortcuts.
- [Model specifications](https://platform.claude.com/docs/en/models/overview) and [API pricing](https://platform.claude.com/docs/en/about-claude/pricing): model IDs, context, output limits, and standard rates.
- [Fast mode](https://code.claude.com/docs/en/fast-mode), [Remote Control](https://code.claude.com/docs/en/remote-control), [Agent Teams](https://code.claude.com/docs/en/agent-teams), and [settings](https://code.claude.com/docs/en/settings-reference): feature-specific behavior.
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): current JSON-schema and strict-tool syntax.
- [Upstream changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md): version boundaries, including removal of TaskOutput in v2.1.278. The tool-reference page still describes it as deprecated; the later explicit removal takes precedence here.

## Current reference

Standard direct-API prices in USD per million input/output tokens:

| Model | ID | Input / output | Context | Claude Code default effort |
|-------|----|----------------|---------|----------------------------|
| Opus 5.5 | `claude-opus-5-5` | $4 / $20 | 1M | medium |
| Sonnet 5 | `claude-sonnet-5` | $2 / $10 | 1M | high |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5 | 200K | Unsupported |
| Fable 5.1 | `claude-fable-5-1` | $10 / $50 | 1M | high |

Opus 5.5 fast mode costs $8/$40. Native 1M models do not inherit the old premium above 200K or the beta-header requirement. Provider aliases can resolve to older models, so a cloud alias is not a universal version identifier.

## Coverage and decisions

| Surface | Action |
|---------|--------|
| Main English guide and daily cheatsheet | Refresh model selection, pricing, thinking, settings, command inventory, shortcuts, Remote Control, and task-tool guidance |
| French full guide | Correct affected model, pricing, thinking, and command sections; retain the declared stale translation status because this is not a complete retranslation |
| Architecture, context, operations, ecosystem, and Agent Teams pages | Correct active examples and claims; keep measurements tied to the model actually measured |
| English/French cheatsheets and print sources | Refresh model/command sections in WP02, WP04, WP07, WP08 and affected recap cards; increment document revisions |
| Quiz | Correct model inheritance, thinking toggles, team requirements, MCP debugging, and fast-mode questions in the canonical web bank and generated CLI bank |
| Examples | Correct fallback model pricing, configured logger rates, structured outputs, and background-agent output reading |
| Machine-readable and MCP indexes | Synchronize descriptions, command additions, links, and positional references |
| Historical releases, security advisories, resource evaluations, and benchmarks | Preserve original model names, dates, affected versions, and measured costs |
| Third-party model pins and sample historical transcripts | Preserve the documented upstream choice or sample; do not claim untested compatibility with a newer model |
| Installed personal skills and global model configuration | Outside this audit; distributed examples are edited without installing them |

All 114 command names represented by rows in the fetched official reference are present in the main English guide. That count includes removed commands and feature-gated entries; it is not a claim that one installation exposes 114 commands.

The distributed `plan-pipeline` skill examples only change output-reading instructions. Their frontmatter, discovery names, and routing descriptions remain unchanged. They are portable templates, not installed host projections; no live router activation is claimed.

## Verification boundaries

The fallback-pricing regression exercises ten model IDs, including a dated Haiku ID. Seven cases failed before correction and all pass afterward. The estimates use standard token rates; they are not provider invoices and do not include fast-mode premiums.

Syntax, index, mirror, quiz, and rendering checks are recorded with the change. No paid model requests, organization settings, or global skills are modified to validate documentation. A successful static build does not establish live availability on every provider.

Translation provenance must be refreshed from the committed English source. Updating selected French sections does not mark the complete French translation current.

## Checks completed before publication

- Positional index: 906 references checked, zero broken; all 793 linked anchors and 61 declared positional anchors resolve. All 106 tracked guide pages are indexed.
- CLI quiz: all 17 categories match the canonical web bank; three CLI tests pass.
- Landing: 258 tests pass, including the localhost HTTP fixtures. The static build produces 462 pages; the link inventory checks 583 HTML documents and validates 1,782 local targets. External URLs are outside that offline result. Forty-six diagrams render as SVG; three retain their text fallback.
- Fallback pricing: ten model cases pass; both changed shell scripts pass syntax checks. The session summary now reports peak input tokens without assuming every model has a 200K window.
- Print exports: 22 PDFs regenerated. The twelve recap cards remain one page each; the two daily cheatsheets are five pages each. Eight affected whitepapers also have rebuilt EPUBs. Four series archives retain 22 cards each.
- MCP package: all 37 tests and the complete release check pass, including the regenerated product manifest, documentation, registry metadata, and package contents.
- Public-content scan: zero workstation-path violations across 1,438 source and rendered files. Source and bundled MCP reference files are byte-identical.

## Changed guide files

The companion landing carries the corresponding web quiz, cheatsheet, reader/search data and downloads. The portfolio carries the versioned PDF/ZIP assets and their download allowlist.

- `CHANGELOG.md`
- `README.md`
- `docs/audits/2026-09-24-commands-models.md`
- `examples/config/settings-personalization.json`
- `examples/hooks/bash/session-summary.sh`
- `examples/modes/README.md`
- `examples/scripts/session-stats.sh`
- `examples/skills/plan-pipeline/execute/SKILL.md`
- `examples/skills/plan-pipeline/start/SKILL.md`
- `examples/skills/plan-pipeline/validate/SKILL.md`
- `examples/styles/custom-style-template.md`
- `guide/cheatsheet.md`
- `guide/core/architecture.md`
- `guide/core/community-patterns.md`
- `guide/core/context-engineering.md`
- `guide/core/known-issues.md`
- `guide/core/settings-reference.md`
- `guide/core/tools-reference.md`
- `guide/diagrams/09-cost-and-optimization.md`
- `guide/ecosystem/agentic-tools.md`
- `guide/ecosystem/ai-ecosystem.md`
- `guide/ecosystem/local-vs-cloud-inference.md`
- `guide/learning-path/03-memory.md`
- `guide/ops/ai-unit-economics.md`
- `guide/ops/api-gateway.md`
- `guide/ops/devops-sre.md`
- `guide/ops/observability.md`
- `guide/ops/subscription-strategy.md`
- `guide/roles/agent-evaluation.md`
- `guide/ultimate-guide.fr.md`
- `guide/ultimate-guide.md`
- `guide/workflows/agent-teams-quick-start.md`
- `guide/workflows/agent-teams.md`
- `guide/workflows/dual-instance-planning.md`
- `guide/workflows/iterative-refinement.md`
- `guide/workflows/plan-pipeline.md`
- `llms.txt`
- `machine-readable/llms.txt`
- `machine-readable/mcp-product.json`
- `machine-readable/reference.yaml`
- `machine-readable/translations.json`
- `mcp-server/content/llms.txt`
- `mcp-server/content/reference.yaml`
- `mcp-server/content/translations.json`
- `quiz/questions/01-quick-start.yaml`
- `quiz/questions/02-core-concepts.yaml`
- `quiz/questions/03-memory-settings.yaml`
- `quiz/questions/04-agents.yaml`
- `quiz/questions/05-skills.yaml`
- `quiz/questions/06-commands.yaml`
- `quiz/questions/07-hooks.yaml`
- `quiz/questions/08-mcp-servers.yaml`
- `quiz/questions/09-advanced-patterns.yaml`
- `quiz/questions/10-reference.yaml`
- `quiz/questions/11-learning-with-ai.yaml`
- `quiz/questions/12-architecture.yaml`
- `quiz/questions/13-security.yaml`
- `quiz/questions/14-privacy-observability.yaml`
- `quiz/questions/15-ai-ecosystem.yaml`
- `quiz/questions/16-agent-harness-context.yaml`
- `quiz/questions/17-team-metrics.yaml`
- `scripts/test-session-summary-pricing.py`
- `whitepapers/CHANGELOG.md`
- `whitepapers/en/02-customization.qmd`
- `whitepapers/en/04-architecture.qmd`
- `whitepapers/en/07-reference-guide.qmd`
- `whitepapers/en/08-agent-teams.qmd`
- `whitepapers/en/cheatsheet.pdf`
- `whitepapers/en/cheatsheet.qmd`
- `whitepapers/fr/02-personnalisation.qmd`
- `whitepapers/fr/04-architecture.qmd`
- `whitepapers/fr/07-guide-reference.qmd`
- `whitepapers/fr/08-agent-teams.qmd`
- `whitepapers/fr/cheatsheet.pdf`
- `whitepapers/fr/cheatsheet.qmd`
- `whitepapers/recap-cards/en/01-commandes-essentielles.qmd`
- `whitepapers/recap-cards/en/m08-agents-custom.qmd`
- `whitepapers/recap-cards/en/m16-multi-agent-topologie.qmd`
- `whitepapers/recap-cards/en/t18-modeles-thinking-modes.qmd`
- `whitepapers/recap-cards/en/t19-context-window-200k-1m.qmd`
- `whitepapers/recap-cards/en/t21-fast-mode-api.qmd`
- `whitepapers/recap-cards/fr/01-commandes-essentielles.qmd`
- `whitepapers/recap-cards/fr/m08-agents-custom.qmd`
- `whitepapers/recap-cards/fr/m16-multi-agent-topologie.qmd`
- `whitepapers/recap-cards/fr/t18-modeles-thinking-modes.qmd`
- `whitepapers/recap-cards/fr/t19-context-window-200k-1m.qmd`
- `whitepapers/recap-cards/fr/t21-fast-mode-api.qmd`
