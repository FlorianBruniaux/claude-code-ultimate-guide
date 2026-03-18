# Evaluation: Kairn — Knowledge Graph Memory MCP

**Date**: 2026-02-25
**Evaluator**: Claude (eval-resource skill)
**Score**: 4/5 — Intégré

---

## Sources évaluées

1. **LinkedIn post** — Robin Lorenz, "Context Engineering for Claude Code", 24 fév. 2026
   - Score: 2/5 — Watch list (claims invérifiables, pas de code source)
2. **GitHub repo** — [kairn-ai/kairn](https://github.com/kairn-ai/kairn) (MIT, Python 100%)
   - Score: 4/5 — **Intégré**

---

## Résumé Kairn

MCP server Python offrant une mémoire organisée en knowledge graph avec 18 outils.

**Différenciateurs clés vs Serena/doobidoo**:
- Typed relationships (`depends-on`, `resolves`, `causes`)
- Biological decay model : solutions ~200j, workarounds ~50j (auto-pruning)
- Full-text search + confidence routing
- Cross-session et cross-IDE

---

## Décision d'intégration

| Élément modifié | Description |
|-----------------|-------------|
| `guide/ultimate-guide.md` ~10233 | Nouvelle section "Kairn: Knowledge Graph Memory with Biological Decay" |
| `guide/ultimate-guide.md` | Comparison Matrix + "When to use" table — colonne Kairn ajoutée |
| `guide/ultimate-guide.md` | Doobidoo limitation "No expiration" → pointe vers Kairn |
| `examples/config/mcp.json` | Entrée `kairn` ajoutée |

---

## Watch list — LinkedIn Lorenz

**Score: 2/5** — Réévaluer si un repo/article technique accompagne le post.

Raison du rejet : post LinkedIn sans code source, stats non vérifiables (93% réduction tokens), Perplexity n'a trouvé aucune trace indépendante. La philosophie "infrastructure outlives prompts" est déjà couverte dans `guide/methodologies.md`.

**Réévaluation trigger** : publication d'un repo GitHub accompagnant le post.
