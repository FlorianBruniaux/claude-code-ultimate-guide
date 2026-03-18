# Resource Evaluation: `shanraisshan/claude-code-best-practice` — Claude Code Best Practices Repo

**Date**: 2026-02-26
**Evaluator**: Claude (Sonnet 4.6)
**URL**: https://github.com/shanraisshan/claude-code-best-practice
**Source**: LinkedIn post by Jean-Christophe Cherid (99% of devs are using Claude wrong)
**Author**: Shan Rais Shan
**Last Updated**: Feb 26, 2026

---

## Summary

Reference repository for Claude Code best practices. Continuously updated as Claude Code evolves. Key content:

- Complete frontmatter references for agents (15 fields), skills (10 fields), and commands
- Global vs project-level settings taxonomy (Tasks system v2.1.16, Agent Teams experimental)
- Boris Cherny 12 customization tips (Feb 12, 2026, official source)
- "My Experience" sections with practical advice (CLAUDE.md < 150 lines, /compact at 50%, etc.)
- Command → Agent → Skills architecture pattern with working example
- CLI startup flags complete reference
- MCP servers for daily use (Context7, Playwright, Claude in Chrome, DeepWiki, Excalidraw)
- Agent memory scopes (user/project/local) with cross-session learning patterns
- Self-evolving agent pattern (agent updates its own skills after execution)

---

## Evaluation Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Relevance** | 5/5 | Direct Claude Code content, frequently updated |
| **Originality** | 4/5 | Practical field-level reference rarely found elsewhere |
| **Authority** | 4/5 | Links to official docs (code.claude.com) for every claim, verified |
| **Accuracy** | 5/5 | All major claims verified against official docs (code.claude.com/docs/en/sub-agents) |
| **Actionability** | 4/5 | Direct corrections and additions needed in guide |

**Overall Score**: **4/5 (High Value)**

---

## Gap Analysis — Critical Finding

### CRITICAL BUG in our guide (line 5646)

Current text in `guide/ultimate-guide.md:5646`:
> "Community patterns: Some users add extra fields like skills, background, isolation, or memory in their agent definitions. These are not part of the official documented spec..."

**This is factually wrong.** The official Claude Code docs (`code.claude.com/docs/en/sub-agents`) explicitly document ALL these fields in the "Supported frontmatter fields" table:

| Field | Official Status | Our Guide Says |
|-------|----------------|----------------|
| `skills` | ✅ OFFICIAL | "community pattern" |
| `background` | ✅ OFFICIAL | "community pattern" |
| `isolation` | ✅ OFFICIAL | "community pattern" |
| `memory` | ✅ OFFICIAL (user/project/local) | "community pattern" |
| `disallowedTools` | ✅ OFFICIAL | Partially covered |
| `permissionMode` | ✅ OFFICIAL | Partially covered |
| `maxTurns` | ✅ OFFICIAL | Partially covered |
| `mcpServers` | ✅ OFFICIAL | Partially covered |
| `hooks` | ✅ OFFICIAL | Partially covered |
| `color` | ✅ OFFICIAL | Not mentioned |

### Already Covered in Guide

| Resource Topic | Guide Coverage | Location |
|----------------|----------------|----------|
| `isolation: worktree` for agents | ✅ Covered | ultimate-guide.md:14277 |
| `$ARGUMENTS[N]` syntax | ✅ Covered | ultimate-guide.md:7601 |
| Background subagents | ✅ Covered | ultimate-guide.md:5798 |
| Skills context:fork | ✅ Covered | quiz/questions/05-skills.yaml |
| Boris Cherny tips | ✅ Integrated | (previous session) |

### Not Well Covered

| Topic | Gap Level | Notes |
|-------|-----------|-------|
| Agent memory scopes (user/project/local) | HIGH | Mislabeled "community pattern" |
| `background: true` frontmatter field | HIGH | Mislabeled "community pattern" |
| Command → Agent → Skills architecture (explicit) | MEDIUM | Pattern exists but not named |
| Self-evolving agents (agent updates its own skills) | LOW | Novel pattern |
| `!`command`` dynamic injection in skills | MEDIUM | Covered for `!` shell but not for skill frontmatter context |

---

## Recommendations

**Priorité 1 — Critique**: Corriger `guide/ultimate-guide.md:5646`
- Remplacer le warning "community patterns" par la liste complète des champs officiels
- Ajouter tableau complet des frontmatter fields avec descriptions (cf. rapport du repo)

**Priorité 2 — Haute**: Documenter les memory scopes (user/project/local)
- Ajouter section dans `guide/ultimate-guide.md` section agents
- Avec exemples de cas d'usage pour chaque scope

**Priorité 3 — Moyenne**: Command → Agent → Skills architecture
- Nommer et documenter ce pattern explicitement
- Le repo a un exemple concret (weather orchestration) à référencer

---

## Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| `background`, `isolation`, `memory`, `skills` sont des champs officiels | ✅ Confirmé | code.claude.com/docs/en/sub-agents |
| `memory` a 3 scopes : user, project, local | ✅ Confirmé | code.claude.com/docs/en/sub-agents#enable-persistent-memory |
| `isolation: worktree` isole dans un git worktree temp | ✅ Confirmé | code.claude.com/docs/en/sub-agents |
| Boris Cherny = créateur de Claude Code, tips datés Feb 12, 2026 | ✅ Confirmé | X/@bcherny |
| 37 settings et 84 env vars | ✅ Confirmé | code.claude.com/docs/en/settings |

**Corrections apportées**: Aucune (toutes les claims du repo sont vérifiées)

---

## Decision

- **Score final**: 4/5 (High Value)
- **Action**: Intégrer — correction critique de la ligne 5646 en priorité
- **Confiance**: Haute (toutes les claims vérifiées contre doc officielle)

### Actions concrètes

1. **[URGENT]** Corriger `guide/ultimate-guide.md:5646` — supprimer le warning "community patterns", remplacer par tableau officiel des frontmatter fields
2. **[HIGH]** Ajouter section "Agent Memory Scopes" avec user/project/local
3. **[MEDIUM]** Nommer le pattern Command → Agent → Skills dans le guide