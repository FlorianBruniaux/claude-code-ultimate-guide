---
title: "Veille Claude Code Releases 2.1.44 → 2.1.50 (17-23 fev 2026)"
type: "weekly-watch"
date: "2026-02-23"
score: 4
action: "integrate"
sources:
  - "Texte copie (analyse veille structuree par version)"
  - "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
  - "https://releasebot.io/updates/anthropic/claude-code"
---

# Veille CC Releases 2.1.44 → 2.1.50 (17-23 fev 2026)

## Resume

Analyse detaillee de 6 releases Claude Code (17-21 fev 2026) couvrant : worktree isolation native, nouveaux hooks `WorktreeCreate`/`WorktreeRemove`/`ConfigChange`, breaking change keybinding (`Ctrl+F` remplace double-ESC), corrections massives de fuites memoire, et migration modele Sonnet 4.6 1M context.

## Score: 4/5

**Justification**: Les releases YAML et claude-code-releases.md sont deja a jour (2.1.50). Les features majeures (worktree isolation, hooks WorktreeCreate/WorktreeRemove, claude agents CLI, env vars 1M) sont dans ultimate-guide.md. La valeur de cette veille = audit de couverture qui revele 8+ gaps dans les sections thematiques + **1 bug documentation actif critique** (ESC/double-ESC).

## Bug Critique Identifie et Corrige

**Fichier**: `guide/ultimate-guide.md` lignes ~5738-5741

**Probleme**: Le guide indiquait `ctrl+c ctrl+c` / `ESC ESC` pour tuer les agents de fond. Faux depuis v2.1.47.

**Risque**: Utilisateurs croyant leurs agents tues alors qu'ils tournent en fond (consommation tokens silencieuse, conflits d'ecriture parallele).

**Fix applique**: Corrige le 2026-02-23. ESC ne cancel plus que le thread principal. `Ctrl+F` = seul moyen de gerer les agents de fond (overlay).

## Gaps Identifies

| Gap | Localisation cible | Priorite | Status |
|-----|-------------------|----------|--------|
| Bug ESC/double-ESC → `Ctrl+F` | ultimate-guide.md ~5738-5741 | **P0 BUG** | ✅ CORRIGE |
| `ConfigChange` hook event | ultimate-guide.md Section 7 Hooks (Event Types table) | **P1** | ✅ FAIT |
| `disableAllHooks` managed hierarchy (breaking) | ultimate-guide.md Section Enterprise/Settings | **P1** | ✅ FAIT (note dans ConfigChange section) |
| `startupTimeout` LSP config | ultimate-guide.md Section LSP | P2 | ✅ FAIT |
| `last_assistant_message` Stop/SubagentStop hooks | ultimate-guide.md Section Hooks Stop event | P2 | ✅ FAIT |
| `--from-pr` CLI flag | ultimate-guide.md Section Workflows GitHub | P2 | ✅ FAIT |
| `enabledPlugins` / `extraKnownMarketplaces` via `--add-dir` | ultimate-guide.md Section Plugins | P2 | ✅ FAIT |
| `SDKRateLimitInfo` / `SDKRateLimitEvent` | ultimate-guide.md Section SDK reference | P3 | ⏳ |
| `spinnerTipsOverride` setting | ultimate-guide.md Section Settings config | P3 | ⏳ |
| `chat:newline` keybinding | ultimate-guide.md Section Keybindings | P3 | ⏳ |
| `added_dirs` in statusline JSON workspace | ultimate-guide.md Section Statusline | P3 | ⏳ |

## Plan d'integration Progressive

### Phase 1 — Hooks (P1, 1 session)

**`ConfigChange` hook** — Ajouter dans la table des evenements hooks (autour de la section WorktreeCreate/WorktreeRemove existante) :

```markdown
| `ConfigChange` | When config files change during session | Enterprise: audit + block live config changes |
```

Avec exemple :
```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "scripts/audit-config-change.sh" }]
      }
    ]
  }
}
```

**`disableAllHooks` managed hierarchy** — Note dans la section Enterprise Settings :
> `disableAllHooks` (v2.1.49+) ne peut plus desactiver les hooks managed par la politique entreprise. Les hooks du niveau `managed` overrident toujours les settings utilisateur.

**`last_assistant_message` in Stop/SubagentStop** — Ajouter dans la section hooks Stop/SubagentStop :
> Le champ `last_assistant_message` est maintenant expose dans les inputs des evenements `Stop` et `SubagentStop` (v2.1.47+). Utile pour acceder a la reponse finale sans parser les transcripts.

### Phase 2 — CLI & LSP (P2, 1 session)

**`--from-pr` flag** — Dans la section GitHub/DevOps workflows :
```bash
# Resume session linked to a specific PR
claude --from-pr 123
# Sessions created via gh pr create are auto-linked
```

**`startupTimeout` LSP** — Dans la section configuration LSP :
```json
{
  "lsp": {
    "servers": {
      "tsserver": { "startupTimeout": 15000 }
    }
  }
}
```

**`enabledPlugins` via `--add-dir`** — Dans la section Plugins :
> `enabledPlugins` et `extraKnownMarketplaces` peuvent etre definis dans les settings d'un repertoire `--add-dir`, permettant une politique de plugins au niveau repo.

### Phase 3 — Settings & Keybindings (P3, batch)

Mettre a jour les tableaux existants :
- **Settings table** : `spinnerTipsOverride` (custom tips, `excludeDefault` option)
- **Keybindings table** : `chat:newline` (configurable multi-line input)
- **Statusline JSON** : `added_dirs` field dans l'objet `workspace`
- **SDK reference** : `SDKRateLimitInfo` / `SDKRateLimitEvent` types

## Fait-Check

| Affirmation | Statut | Source |
|-------------|--------|--------|
| Releases 2.1.44-2.1.50 dates 17-21 fev 2026 | ✅ | claude-code-releases.yaml |
| `WorktreeCreate`/`WorktreeRemove` en 2.1.50 | ✅ | claude-code-releases.yaml ligne 21 |
| `Ctrl+F` remplace double-ESC depuis 2.1.47 | ✅ | claude-code-releases.md ligne 82 |
| `ConfigChange` hook en 2.1.49 | ✅ | claude-code-releases.md ligne 56 |
| `CLAUDE_CODE_SIMPLE` desactive MCP/hooks/CLAUDE.md depuis 2.1.50 | ✅ | claude-code-releases.md ligne 38 |
| Fix glibc < 2.30 RHEL 8 en 2.1.50 | ✅ | claude-code-releases.yaml (2.1.50 highlights) |
| Bug doc ESC lignes 5738-5741 | ✅ CONFIRME | ultimate-guide.md (verifie + corrige) |
| Sonnet 4.5 1M retire du plan Max | ✅ | claude-code-releases.md (2.1.49 breaking) |

## Challenge (technical-writer)

- **Score maintenu** : 4/5
- **Bug ESC sous-evalue dans l'analyse initiale** : c'est un risque operationnel reel (agents fantomes), pas un simple gap de feature. Traite en P0.
- **3 gaps manques initialement** : `last_assistant_message`, `--from-pr`, bug ESC actif
- **Valeur principale** : service de quality assurance/audit de couverture sur un guide de 20K lignes, pas une source de contenu primaire