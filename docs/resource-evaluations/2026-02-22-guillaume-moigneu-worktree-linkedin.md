# Évaluation: "Claude Code built-in git worktree support" - LinkedIn Guillaume Moigneu

**Date d'évaluation**: 2026-02-22
**Évaluateur**: Claude Code (auto)
**Ressource**: LinkedIn post Guillaume Moigneu

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Source** | LinkedIn post de Guillaume Moigneu, 2026-02-22 |
| **Auteur** | Guillaume Moigneu — Solution Architecture/Advocacy @ Upsun, tech speaker |
| **Autorité** | Praticien (pas Anthropic) — Solution Architect avec expertise déploiement |
| **Catégorie** | Productivity - Worktrees + Subagents |
| **Article lié** | https://lnkd.in/gCicQRHP (article personnel sur worktrees) |
| **Relation** | Complément à [2026-02-22-boris-cherny-worktree-tips-reddit.md](./2026-02-22-boris-cherny-worktree-tips-reddit.md) |

---

## 📄 Résumé du contenu

- **Subagent + worktree combinés**: Claude peut créer des worktrees pour ses propres subagents — migrations parallèles massives sans conflits d'écriture
- **`isolation: worktree` déclaratif** (v2.1.50): Dans les agent defs, plus besoin de le spécifier à chaque appel
- **Hooks `WorktreeCreate`/`WorktreeRemove`**: Setup/teardown custom VCS → **non-git SCM supporté** (Perforce, SVN, etc.)
- **Disponible sur**: CLI (`--worktree`), Desktop app, IDE — pas seulement CLI
- **Article détaillé**: Son propre article sur les worktrees (lnkd.in/gCicQRHP)

---

## 🔍 Clarification versions

Guillaume attribue tout à v2.1.50 — c'est légèrement inexact :

| Feature | Version réelle |
|---------|----------------|
| `--worktree` / `-w` CLI flag | **v2.1.49** (2026-02-20) |
| `isolation: "worktree"` pour subagents | **v2.1.49** (2026-02-20) |
| `WorktreeCreate`/`WorktreeRemove` hooks | **v2.1.50** (2026-02-21) |
| `isolation: worktree` déclaratif dans agent defs | **v2.1.50** (2026-02-21) |
| Support Desktop + IDE | **v2.1.50** (confirmé) |

---

## 🎯 Score de pertinence

**Score: 3/5** (complément — ne justifie pas intégration indépendante)

**Justification**: Le post n'apporte pas de contenu standalone suffisant pour une section dédiée. Sa valeur est dans les **deltas** par rapport à l'évaluation principale :
1. Hooks `WorktreeCreate`/`WorktreeRemove` → non-git SCM (non couvert ailleurs)
2. `isolation: worktree` déclaratif dans agent defs (précision v2.1.50 manquante)
3. Confirmation Desktop + IDE (vs CLI-only dans l'autre éval)
4. Article externe à référencer

---

## ⚖️ Delta vs évaluation principale (Boris Cherny Reddit)

| Aspect | Reddit/Tweet | LinkedIn Guillaume | Dans le guide |
|--------|-------------|-------------------|---------------|
| `--worktree` CLI | ✅ | ✅ | ❌ guide principal |
| Subagents + worktrees | Évoqué | **Détaillé (migrations parallèles)** | ❌ |
| `WorktreeCreate`/`WorktreeRemove` hooks | ❌ | **✅ Non-git SCM** | ❌ |
| `isolation: worktree` déclaratif | ❌ | **✅** | ❌ |
| Desktop + IDE (pas que CLI) | ❌ | **✅** | ❌ |
| Article de référence externe | ❌ | **✅** | ❌ |

---

## 📍 Intégration recommandée

**Complète l'intégration définie dans l'éval principale.** Ajouter dans la même section `guide/ultimate-guide.md:13408` :

```markdown
#### Subagents + Worktree Isolation

Claude can spin up worktrees for its own subagents. Declare isolation directly in agent definitions:

```yaml
# .claude/agents/migration-agent.md
---
isolation: worktree   # Each invocation gets its own worktree (v2.1.50+)
background: true
---
```

This enables write-safe parallel migrations: 4 agents refactoring different modules,
no merge conflicts because each works in its own copy.
```

**Aussi**: Ajouter une note sur les hooks `WorktreeCreate`/`WorktreeRemove` dans la section hooks du guide (non-git SCM use case).

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| `WorktreeCreate`/`WorktreeRemove` hooks en v2.1.50 | ✅ | `guide/claude-code-releases.md` ligne 30-31 |
| `isolation: worktree` déclaratif en v2.1.50 | ✅ | `guide/claude-code-releases.md` ligne 32 |
| `--worktree` en v2.1.49 (pas v2.1.50) | ✅ | `guide/claude-code-releases.md` ligne 53 |
| Support Desktop + IDE | ✅ (implicite) | v2.1.50 notes |
| Non-git SCM via hooks | ✅ | `WorktreeCreate`/`WorktreeRemove` hook events |
| Article Guillaume: lnkd.in/gCicQRHP | ⚠️ | URL LinkedIn raccourcie — non vérifié directement |

---

## 🎯 Décision finale

- **Score final**: 3/5
- **Action**: **Intégrer comme complément** — pas de section séparée, enrichit l'intégration de l'éval principale
- **Nouveaux éléments à ajouter au guide**:
  1. `isolation: worktree` déclaratif dans agent defs (YAML example)
  2. `WorktreeCreate`/`WorktreeRemove` hooks → section hooks
  3. Mention Desktop + IDE support
  4. Article Guillaume comme référence externe
