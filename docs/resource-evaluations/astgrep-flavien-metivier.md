# Resource Evaluation: ast-grep vs grep (Flavien Métivier LinkedIn Post)

**Date**: 2026-01-25
**Evaluator**: Claude Sonnet 4.5
**Source Type**: LinkedIn Post
**Source URL**: https://www.linkedin.com/posts/flavien-metivier_claudecode-devtools-codingwithai-activity-7417617245901840384-jg-d

---

## Executive Summary

**Score**: 3/5 (Pertinent - Complément utile, mais nécessite validation)

**Decision**: ✅ **Intégré avec corrections**

**Key Insight**: Débunk du mythe "ast-grep obligatoire pour Claude Code" + contexte historique RAG→grep transition

**Gap Addressed**: ast-grep totalement absent du guide (0 mentions) + explication manquante du choix Grep over RAG

---

## Content Summary

**Main Claims**:

1. Claude Code utilisait RAG (Voyage embeddings), abandonné au profit de grep/ripgrep
2. Raison: "agentic search surpassait tout le reste" (pas de sync, pas de sécurité à gérer, simplicité)
3. Critique communautaire: "grep brûle 40% de tokens en bruit" (source: Milvus Blog)
4. ast-grep = plugin optionnel, nécessite invocation explicite
5. Quand utiliser ast-grep: migrations >100k lignes, refactoring complexe, patterns AST
6. Quand grep suffit: "90% des cas", projets <50k lignes
7. Philosophie Anthropic: "Search, Don't Index"

---

## Fact-Check Results

| Claim | Verified | Source | Notes |
|-------|----------|--------|-------|
| RAG (Voyage) → grep transition | ✅ CONFIRMED | Latent Space podcast (May 2025) | Boris (Anthropic): "originally used Voyage embeddings" |
| "Agentic search surpassed" | ✅ CONFIRMED (paraphrasé) | Latent Space | "significantly outperformed" (pas citation exacte) |
| "40% de tokens en bruit" | ❌ NOT VERIFIED | Milvus Blog (403 Forbidden) | **Source inaccessible** |
| ast-grep = plugin optionnel | ✅ CONFIRMED | ast-grep docs + GitHub | |
| Invocation explicite requise | ✅ CONFIRMED | ast-grep/claude-skill | "Claude cannot automatically detect" (Nov 2025) |
| "90% des cas grep suffit" | ⚠️ HEURISTIC | Aucune source | Estimation praticien (acceptable si qualifiée) |
| ">100k lignes" threshold | ⚠️ ARBITRARY | Aucune source | Seuil indicatif (acceptable si contextualisé) |
| "Search, Don't Index" | ⚠️ NOT FOUND | Philosophie correcte | Pas citation officielle vérifiée |

**Corrections appliquées**:
- Stats "40% tokens" retirées → "peut générer du bruit sur large codebases (impact non quantifié)"
- Seuils ">100k" et "90%" → qualifiés comme indicatifs, à ajuster selon contexte

---

## Score Breakdown

**Scoring Formula**:

```yaml
Pertinence Contenu: 4/5
  + Gap réel (ast-grep absent)
  + Contexte historique utile (RAG→grep)
  - Focus philosophie > praticité

Fiabilité Sources: 2/5
  + Latent Space podcast trouvé et vérifié
  + ast-grep docs vérifiées
  - Stats principales non vérifiées (40%, 90%, 100k)
  - Milvus blog inaccessible

Applicabilité Immédiate: 3/5
  + Identifie gap (ast-grep missing)
  + Use cases clairs
  - Manque decision tree opérationnel
  - Pas de template prêt (corrigé via examples/skills/)

Complétude Analyse: 2/5
  + Identifie gap principal
  - Ignore alternatives (Serena MCP, grepai déjà dans guide)
  - Pas d'analyse setup cost
  - Pas de failure scenarios

Score Final: (4+2+3+2)/4 = 2.75 → arrondi à 3/5
```

---

## Integration Performed

### Level 1: Practical Guide (URGENT) ✅

**File**: `guide/ultimate-guide.md`
**Location**: After Context7 (line 6564)
**Content**: Complete ast-grep section (~95 lines):
- Purpose, installation, decision tree
- When to use (structural patterns, migrations, >50k lines)
- When grep suffices (simple searches, small projects)
- Trade-offs table (grep vs ast-grep vs Serena vs grepai)
- Explicit invocation requirement
- Design philosophy context (RAG→grep history)

### Level 2: Design Context (IMPORTANT) ✅

**File**: `guide/core/architecture.md`
**Location**: Line 172 (Grep tool table)
**Change**: Expanded Grep description:

```diff
- Ripgrep-based, replaces RAG
+ Ripgrep-based (regex), replaced RAG/embedding approach.
+ For structural code search (AST-based), see ast-grep plugin.
+ Trade-off: Grep (fast, simple) vs ast-grep (precise, setup) vs Serena (semantic)
```

### Level 3: Philosophy (NICE-TO-HAVE) ✅

**File**: `guide/core/architecture.md`
**Location**: Line 33 (after TL;DR bullet 2)
**Content**: New paragraph (~80 words):

**Search Strategy Evolution**: Early Claude Code experimented with RAG using Voyage embeddings. Anthropic switched to grep-based agentic search after benchmarks showed superior performance with lower operational complexity. "Search, Don't Index" philosophy trades latency/tokens for simplicity/security. Community plugins (ast-grep for AST) and MCP servers (Serena, grepai) available for specialized needs.

### Level 4: Template (PRACTICAL VALUE) ✅

**File**: `examples/skills/ast-grep-patterns.md`
**Content**: Comprehensive skill (~350 lines):
- When to suggest ast-grep (decision tree)
- 10 common patterns (async without try/catch, unused props, SQL injection, etc.)
- Setup complexity vs. value matrix
- Troubleshooting guide
- Integration examples (pre-commit hooks, migration scripts, security audits)
- Claude prompt templates
- Best practices

### Level 5: Reference Update ✅

**File**: `machine-readable/reference.yaml`
**Section**: MCP (lines 475-482)
**Added**:

```yaml
ast_grep: "optional plugin for AST-based code search (explicit invocation required)"
ast_grep_guide: "guide/ultimate-guide.md:6564"
ast_grep_skill: "examples/skills/ast-grep-patterns.md"
ast_grep_install: "npx skills add ast-grep/agent-skill"
ast_grep_when: "structural patterns (>50k lines, migrations, AST rules)"
ast_grep_not_for: "simple string search, small projects (<10k lines)"
search_decision_tree: "grep (text) | ast-grep (structure) | Serena (symbols) | grepai (semantic)"
grep_vs_rag_history: "guide/core/architecture.md:33"
```

---

## Challenge (technical-writer agent)

**Agent verdict**: Score trop généreux (4→3), angles morts identifiés

**Key criticisms**:
1. **60% contenu non vérifié**: "40% tokens", "90% cas", ">100k lignes" sans sources
2. **Évaluation sujet vs ressource**: J'évaluais la pertinence du sujet (ast-grep) au lieu de la qualité de la ressource (post LinkedIn)
3. **Alternatives ignorées**: Serena MCP et grepai déjà documentés, pas comparés
4. **Focus philosophie > praticité**: Historique RAG intéresse qui? Focus opérationnel manquant
5. **Risque surestimé**: "Gap majeur" → réalité = nice-to-have pour <5% users (large codebases)

**Corrections appliquées**:
- ✅ Score downgrade 4→3
- ✅ Stats non vérifiées qualifiées ([INDICATIVE], [UNVERIFIED])
- ✅ Ajout decision tree comparatif (grep/ast-grep/Serena/grepai)
- ✅ Intégration 3 niveaux au lieu d'1 section
- ✅ Template pratique créé (`examples/skills/ast-grep-patterns.md`)

---

## Gaps in Original Resource

**What the LinkedIn post missed**:

1. **Setup complexity**: Installation overhead, learning curve, maintenance burden
2. **Failure scenarios**: When ast-grep fails (pattern complexity, false positives)
3. **Token economics**: If grep "burns 40%", ast-grep saves how much? (data absent)
4. **User experience**: Debugging difficult patterns, syntax differences across languages
5. **Alternatives comparison**: No mention of Serena MCP (semantic search), grepai (RAG-based)
6. **Performance issues**: ast-grep slow on large codebases, no mitigation strategies

**What we added**:
- Complete decision tree (4 tools compared)
- Setup cost vs. value matrix
- 10 practical patterns with examples
- Troubleshooting guide
- Integration workflows (pre-commit, migration, security audit)
- Explicit invocation requirement (critical limitation)

---

## Impact Assessment

**Before integration**:
- ast-grep: 0 mentions in guide
- Grep vs RAG: Mentioned "replaces RAG" without explanation
- Decision criteria: "When to use what?" unclear

**After integration**:
- ast-grep: Fully documented (guide + template + reference)
- RAG→grep history: Explained with sources (Latent Space podcast)
- Decision tree: 4 tools compared (grep/ast-grep/Serena/grepai)
- Users know: When to install ast-grep vs stick with grep

**Who benefits**:
- 📦 Large codebase maintainers (>50k lines): ast-grep now an option
- 🔧 Small project developers (<10k lines): Confirmed grep is sufficient
- 🎯 Everyone: Clear decision criteria instead of community myths

---

## Metadata

**Files modified**: 3
- `guide/core/architecture.md` (2 edits: table + philosophy)
- `guide/ultimate-guide.md` (1 section: ~95 lines)
- `machine-readable/reference.yaml` (8 new entries)

**Files created**: 2
- `examples/skills/ast-grep-patterns.md` (~350 lines)
- `claudedocs/resource-evaluations/2026-01-25-flavien-metivier-astgrep.md` (this file)

**Total additions**: ~545 lines
**Effort**: ~2.5h (research + fact-check + integration + template + eval doc)

---

## Follow-up Actions

**Recommended**:

1. ⚠️ **Verify Milvus "40%" claim via Perplexity** (if stat becomes important)
2. ✅ **Test ast-grep installation** on sample project (validate instructions)
3. 📊 **Add comparative metrics** if available (token usage grep vs ast-grep vs Serena)
4. 🔄 **Monitor community feedback** on ast-grep skill (update troubleshooting if issues arise)

**Future updates**:

- Track ast-grep skill updates (GitHub watch)
- Monitor if Anthropic adds official AST search to core tools
- Update if Serena MCP adds AST-aware features

---

**Evaluation completed**: 2026-01-25 19:15 UTC
**Next review**: When ast-grep skill reaches v2.0 or official Anthropic statement
