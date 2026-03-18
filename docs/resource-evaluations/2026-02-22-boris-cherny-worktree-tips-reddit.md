# Évaluation: "5 Claude Code Worktree Tips from Creator" - Reddit/Twitter

**Date d'évaluation**: 2026-02-22
**Évaluateur**: Claude Code (auto)
**Ressource**: Reddit r/ClaudeAI + Tweet Boris Cherny (@bcherny)

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| **Source primaire** | Tweet @bcherny, 2026-02-21 · 40.2K views |
| **Source secondaire** | Reddit r/ClaudeAI, 164 upvotes |
| **Auteur** | Boris Cherny (créateur et head of Claude Code @ Anthropic) |
| **Catégorie** | Productivity - Worktrees |
| **URL Reddit** | https://www.reddit.com/r/ClaudeAI/comments/1rae05r/ |
| **Tweet original** | https://x.com/bcherny/status/2025007393290272904 |

---

## 📄 Résumé du contenu

- **Annonce officielle**: `claude --worktree` / `-w` flag désormais disponible en CLI (existait en Desktop, maintenant porté en CLI)
- **Modèle concurrent natif**: Chaque agent obtient son propre worktree isolé, pas d'interférence entre sessions parallèles
- **Patterns communautaires validés**: Per-worktree port management (scripts, docker-compose override, ports aléatoires), per-worktree `.claude/settings.json` tuning, "main worktree as integration branch"
- **Ressource externe identifiée**: [claude-worktree-hooks](https://github.com/tfriedel/claude-worktree-hooks) — port isolation automatique pour `claude --worktree`
- **Débat worktrees vs multi-clone**: Worktrees partagent le même objet git (branches, commits, moins de disk), mais multi-clone reste valide pour équipes non-familières

---

## 🎯 Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel - Gap majeur dans le guide |
| **4** | **Très pertinent - Amélioration significative** |
| 3 | Pertinent - Complément utile |
| 2 | Marginal - Info secondaire |
| 1 | Hors scope - Non pertinent |

**Score: 4/5**

**Justification**: Trois facteurs convergents :
1. **Gap documenté**: `claude --worktree` / `-w` est dans `claude-code-releases.md` (v2.1.49) mais **absent du guide principal** (section 13408) qui couvre encore uniquement le `git worktree add` manuel
2. **Patterns actionnables manquants**: port management, per-worktree settings.json tuning, integration branch pattern — rien de cela dans le guide
3. **Source primo-autoritaire**: Boris Cherny est le créateur de Claude Code → contenu directement pertinent, pas de filtre communautaire non vérifié

---

## ⚖️ Comparatif

| Aspect | Cette ressource | Notre guide (section 13408) |
|--------|----------------|------------------------------|
| `claude --worktree` CLI flag | ✅ Annoncé + context | ❌ Absent du guide principal |
| `git worktree add` manuel | ✅ Mentionné (comparaison) | ✅ Documenté avec exemples |
| Port conflict management | ✅ Patterns concrets (docker, scripts, random ports) | ❌ Non couvert |
| Per-worktree `.claude/settings.json` | ✅ Tip BP041 (7 upvotes) | ❌ Non couvert |
| Integration branch pattern | ✅ Tip BP041 | ❌ Non couvert |
| 4 custom commands (/git-worktree, etc.) | ❌ Non mentionné | ✅ Documenté |
| Worktrees vs multi-clone trade-offs | ✅ Débat riche | ❌ Non couvert |

---

## 📍 Recommandations d'intégration

**Score ≥ 3 → Intégrer**

### Action unique recommandée

**Fichier**: `guide/ultimate-guide.md`
**Section**: 13408 - "Git Worktrees for Parallel Development"
**Priorité**: Haute (dans la semaine — le flag date du 2026-02-20)

**Contenu à ajouter** (~30-40 lignes) :

```markdown
#### Using the `--worktree` CLI Flag (v2.1.49+)

Since v2.1.49, Claude Code includes built-in worktree support:

```bash
# Create an isolated worktree automatically
claude --worktree        # or -w (short form)

# Equivalent manual setup
git worktree add ../myproject-feature feature-a && cd ../myproject-feature && claude
```

**What `--worktree` does**: Creates a temporary git worktree, launches Claude in it,
and cleans up on exit if no changes were made.

**Practical patterns:**

**Port isolation** (when services need to run per worktree):
- Use docker-compose override files auto-generated at worktree creation
- Assign random ports dynamically and inject via env variables
- See [claude-worktree-hooks](https://github.com/tfriedel/claude-worktree-hooks) for port automation

**Per-worktree behavior tuning:**
```bash
# In each worktree, create a .claude/settings.json
# Tighter permissions for refactoring worktrees, looser for exploration
```

**Integration branch pattern:**
Keep one 'main' worktree as your integration branch.
Only merge into it from parallel worktrees — never develop directly there.
```

**Ne pas créer** de section séparée pour `claude-worktree-hooks` — juste une note de bas de section.

---

## 🔥 Challenge (technical-writer agent)

> *Score 4/5 justifié, mais pour la mauvaise raison. L'argument "créateur = autorité" est biaisé — c'est la convergence (gap documenté + patterns actionnables vérifiables via release v2.1.49 + communauté) qui justifie le score.*
>
> *Plan d'intégration initial trop dispersé (3 points d'entrée). Bonne simplification : une seule extension de la section 13408.*
>
> *Risque de non-intégration : modéré. Le flag est dans les releases (trouvable), mais la section 13408 devient incohérente si elle n'inclut pas la commande native — elle enseigne encore uniquement le git manuel alors que la feature native existe depuis 2 jours.*

- **Score ajusté**: 4/5 (confirmé)
- **Points manqués**: Source primaire = changelog v2.1.49, pas le tweet (le tweet disparaît, le changelog reste)
- **Risques de non-intégration**: Incohérence interne (section 13408 outdated vs releases.md à jour)

---

## ✅ Fact-Check

| Affirmation | Vérifiée | Source |
|-------------|----------|--------|
| `claude --worktree` / `-w` existe en v2.1.49 | ✅ | `guide/claude-code-releases.md` ligne 53 |
| Boris Cherny = créateur de Claude Code | ✅ | Perplexity (ITPro, Lenny's Newsletter, YouTube) |
| Tweet date: 21 Feb 2026 | ✅ | Screenshot utilisateur |
| 40.2K views sur le tweet | ✅ | Screenshot utilisateur |
| Reddit: 164 upvotes | ✅ | Screenshot utilisateur |
| `claude-worktree-hooks` existe sur GitHub | ⚠️ | Mentionné par u/cygn — non vérifié directement |
| `workmux` existe sur GitHub | ⚠️ | Mentionné par u/philosophical_lens — non vérifié directement |

**Corrections apportées**: Aucune (aucune stat inventée)

**Stats nécessitant vérification externe avant intégration**: Les repos GitHub (`claude-worktree-hooks`, `workmux`) — vérifier existence + activité avant de les mentionner dans le guide.

---

## 🔗 Sources complémentaires

| Source | Apport principal |
|--------|-----------------|
| [LinkedIn Guillaume Moigneu (2026-02-22)](./2026-02-22-guillaume-moigneu-worktree-linkedin.md) | `WorktreeCreate`/`WorktreeRemove` hooks, `isolation: worktree` déclaratif (v2.1.50), support Desktop + IDE, article externe |

**Clarification versions** (Guillaume attribue tout à v2.1.50, incorrect) :
- `--worktree` CLI + `isolation: "worktree"` subagents → **v2.1.49**
- `WorktreeCreate`/`WorktreeRemove` hooks + déclaratif agent defs → **v2.1.50**

---

## 🎯 Décision finale

- **Score final**: 4/5
- **Action**: **Intégrer**
- **Délai recommandé**: Dans la semaine (feature sortie le 2026-02-20)
- **Effort estimé**: ~50-60 lignes dans la section 13408 + ~10 lignes section hooks
- **Confiance**: Haute (confirmé dans nos propres release notes v2.1.49 + v2.1.50)

### Périmètre d'intégration complet (après les deux évals)

1. Section `13408` — ajouter :
   - `claude --worktree` / `-w` native flag avec exemple
   - `isolation: worktree` déclaratif dans agent defs (YAML)
   - Subagents + worktrees pour migrations parallèles
   - Port management patterns (docker-compose override, random ports)
   - Per-worktree `.claude/settings.json` tuning
   - Integration branch pattern
   - Note Desktop + IDE support
2. Section hooks — ajouter `WorktreeCreate`/`WorktreeRemove` (non-git SCM use case)
3. Références externes : `claude-worktree-hooks` + article Guillaume Moigneu (à vérifier avant publication)
