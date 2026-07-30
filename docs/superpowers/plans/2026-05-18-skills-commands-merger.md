# Skills–Commands Merger — Content Update Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update all educational content (guide, whitepapers, recap cards, landing site, machine-readable) to reflect the CC 2.1.3 commands→skills unification, ensuring FR/EN parity and PDF regeneration.

**Architecture:** The January 2026 merger eliminated `.claude/commands/` as a separate directory. Everything now lives in `.claude/skills/`. Skills can be user-invocable (`/name`, equivalent to old commands), model-invocable (auto-triggered via description), or both. The 3-way comparison Agent/Skill/Command becomes 2-way Agent/Skill with invocation modes. A pedagogical note (`claudedocs/pedagogy-skills-merger.md`) is written first and becomes the single editorial source of truth for all downstream edits.

**Tech Stack:** Quarto + whitepaper-typst, Astro (landing), YAML, Markdown

---

## Scope note

This plan has three natural sub-projects that are sequentially dependent:
1. **Pedagogy** (Task 1) — must be done first; all other tasks read from it
2. **Source edits** (Tasks 2–10) — can run in parallel once Task 1 is done
3. **Build & deploy** (Tasks 11–13) — sequential after source edits

---

## File Map

| File | Action | Task |
|------|--------|------|
| `claudedocs/pedagogy-skills-merger.md` | Create | T1 |
| `guide/cheatsheet.md` L162-165, L261-265, L363-375 | Edit | T2 |
| `guide/ultimate-guide.md` §5 note, §6 header + section reframe, L6149 table, L7439 comparison, L9509-9540 | Edit | T3 |
| `whitepapers/fr/02-personnalisation.qmd` L175, L204, L738-812, L869, L918 | Edit | T4 |
| `whitepapers/en/02-customization.qmd` (EN parity) | Edit | T4 |
| `whitepapers/fr/07-guide-reference.qmd` L368, L407, L545, L574-630 | Edit | T5 |
| `whitepapers/en/07-reference-guide.qmd` (EN parity) | Edit | T5 |
| `whitepapers/fr/04-architecture.qmd` L432 | Edit | T6 |
| `whitepapers/en/04-architecture.qmd` (EN parity) | Edit | T6 |
| `whitepapers/recap-cards/fr/c04-commands-skills-plugins-agents.qmd` | Rewrite | T7 |
| `whitepapers/recap-cards/en/c04-commands-skills-plugins-agents.qmd` | Rewrite | T7 |
| `whitepapers/recap-cards/fr/m09-slash-commands.qmd` | Update (reframe as user-invocable skills) | T8 |
| `whitepapers/recap-cards/en/m09-slash-commands.qmd` | Update | T8 |
| `whitepapers/recap-cards/fr/m10-skills.qmd` | Update (add invocation modes) | T8 |
| `whitepapers/recap-cards/en/m10-skills.qmd` | Update | T8 |
| `whitepapers/recap-cards/fr/01-commandes-essentielles.qmd` | Minor update | T8 |
| `whitepapers/recap-cards/{fr,en}/t01-commandes-essentielles.qmd` | Minor update | T8 |
| Landing `src/content/docs/guide/ultimate-guide/learning-path/05-skills.md` | Edit | T9 |
| Landing `src/content/docs/guide/ultimate-guide/06-commands.md` | Reframe | T9 |
| Landing `src/content/docs/guide/ultimate-guide/learning-path/04-agents.md` | Minor edit | T9 |
| Landing `src/content/docs/learning-path/05-skills.md` | Edit | T9 |
| Landing `src/content/docs/learning-path/04-agents.md` | Minor edit | T9 |
| Landing `src/content/docs/skill-design-patterns.md` | Edit | T9 |
| Landing `src/content/docs/cheatsheet.md` | Edit | T9 |
| Landing `src/content/cheatsheets/m09-slash-commands.md` | Update | T10 |
| Landing `src/content/cheatsheets/m10-skills.md` | Update | T10 |
| Landing `src/content/cheatsheets/c04-commands-skills-plugins-agents.md` | Rewrite | T10 |
| Landing `src/content/cheatsheets/m08-agents-custom.md` | Minor check | T10 |
| Landing `src/content/cheatsheets/t01-commandes-essentielles.md` | Minor update | T10 |
| Landing `src/content/questions/06-commands/` (full dir) | Update Q&A | T10 |
| Landing `src/content/questions/05-skills/` (≥20 files) | Update Q&A | T10 |
| Landing `src/data/examples-data.ts` | Update | T10 |
| Landing `src/data/search-index.ts` | Update | T10 |
| Landing `src/data/guide-search-entries.ts` | Update | T10 |
| Landing `src/data/guide-anchor-map.json` | Update | T10 |
| Landing `src/utils/categories.ts` | Update | T10 |
| Landing `src/components/landing/FeaturesGrid.astro` | Update | T10 |
| Landing `src/components/landing/ExamplesCatalog.astro` | Update | T10 |
| `machine-readable/reference.yaml` L32, L36, L55, L175, L220-221, L279-281, L351 | Update | T11 |
| `llms.txt`, `llms-full.txt`, `machine-readable/llms.txt` | Update | T11 |
| WP PDFs regeneration (02 FR+EN, 04 FR+EN, 07 FR+EN) | Build | T12 |
| Recap card PDFs (c04, m09, m10, 01-commandes, t01 FR+EN) | Build | T12 |
| `whitepapers/CHANGELOG.md` | Bump versions + entries | T12 |
| `florian-portfolio/public/guides/` | Copy PDFs | T13 |
| `florian-portfolio/api/guides.mjs` (GUIDE_MANIFEST) | Update hashes | T13 |
| Landing `src/data/whitepapers-data.ts` | Update `const V` + hashes | T13 |
| Landing `src/components/landing/AnnouncementBanner.astro` | Update message + BANNER_ID | T13 |
| Landing `src/data/rss-entries.ts` | Add `guide_release` entry | T13 |
| `CHANGELOG.md` [Unreleased] | Add entry | T13 |

---

## Task 1 — Pedagogical Note (editorial source of truth)

**Files:**
- Create: `claudedocs/pedagogy-skills-merger.md`

This task MUST complete before any editing task starts. All downstream edits are calibrated to this note.

- [ ] **Step 1: Write the pedagogical note**

Create `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/claudedocs/pedagogy-skills-merger.md` with this exact content:

```markdown
# Pedagogy Note: Skills–Commands Merger (CC 2.1.3)

Version du changement : Claude Code 2.1.3, released 2026-01-11
Applicable à tout contenu publié après cette date.

---

## 1. Ce qui a changé

**Avant 2.1.3** : deux mécanismes distincts.
- `.claude/commands/` — templates Markdown invoqués via `/nom-command` par l'utilisateur
- `.claude/skills/` — modules de connaissance chargés par le modèle selon le contexte

**Depuis 2.1.3** : un seul mécanisme.
- `.claude/skills/` — tout. Les skills ont deux modes d'invocation :
  1. **User-invocable** : l'utilisateur tape `/nom-skill` (exact comportement des anciennes commands)
  2. **Model-invocable** : le modèle charge la skill automatiquement si la description correspond au contexte
  3. **Les deux** : une skill peut être déclenchée des deux façons (par défaut, sans frontmatter spécial)

Pour restreindre une skill à l'invocation utilisateur uniquement (équivalent d'une ancienne command), ajouter dans le frontmatter :
```yaml
disable-model-invocation: true
```

Le répertoire `.claude/commands/` est déprécié. Les fichiers existants fonctionnent encore (rétrocompatibilité), mais tout nouveau développement doit aller dans `.claude/skills/`.

---

## 2. Comment expliquer la fusion au lecteur

**Ne pas dire** : "commands et skills ont fusionné" (trop technique, peu pédagogique).

**Dire** : "Les skills ont deux modes d'invocation. Quand un utilisateur tape `/nom`, c'est ce qu'on appelait autrefois une command. Quand le modèle charge la skill automatiquement selon le contexte, c'est l'ancien comportement skill. Les deux vivent maintenant dans `.claude/skills/` avec le même frontmatter YAML."

**Conserver le terme "slash command"** : il décrit comment l'utilisateur invoque une skill (via `/`), pas un type de mécanisme distinct. "Slash command" = skill avec invocation utilisateur. Le terme reste pertinent dans les tables de référence des built-in commands (`/clear`, `/compact`, etc.) et dans les explications d'usage.

**Ne pas supprimer "command"** de la terminologie built-in : `/clear`, `/compact`, `/help` restent des "built-in commands". La fusion ne touche que les mécanismes custom.

---

## 3. Nouveau tableau de comparaison Agent vs Skill

Le tableau Agent/Skill/Command (3 colonnes) devient Agent/Skill (2 colonnes) avec une note sur les modes d'invocation de Skill.

| Mécanisme | Déclenchement | Portée | Cas d'usage idéal |
|-----------|--------------|--------|-------------------|
| **Agent** | Task tool / invocation Claude | Session isolée | Audit one-shot, traitement parallèle |
| **Skill** | `/nom` (user) ou auto (modèle) | Partagé entre agents | Connaissance réutilisable, workflow codifié |

**Note d'invocation Skill** :
- User-invocable (`disable-model-invocation: true`) : `/tech:commit`, `/release-notes` — l'utilisateur déclenche manuellement
- Model-invocable : `security-guardian`, `tdd-node` — le modèle charge selon le contexte
- Les deux (défaut) : skills polyvalents, invocables des deux façons

**Règle de sélection rapide** :
- Tâche déléguée avec isolation de contexte → **Agent**
- Connaissance ou workflow à encapsuler → **Skill**
  - L'utilisateur déclenche → `disable-model-invocation: true`
  - Le modèle décide → laisser le défaut (model-invocable)
  - Les deux → laisser le défaut sans l'option

---

## 4. Exemples concrets par mode d'invocation

**User-invocable uniquement** (`disable-model-invocation: true`) :
- `/tech:commit` — l'utilisateur tape manuellement après avoir codé
- `/release-notes` — déclenché en fin de sprint par l'utilisateur
- `/ship` — séquence de deploy déclenchée intentionnellement

**Model-invocable uniquement** (sans frontmatter spécial, description précise) :
- `security-guardian` — chargé quand Claude détecte une auth ou une route sensible
- `tdd-node` — chargé quand Claude commence à écrire des tests
- `silence-framework-expert` — chargé sur les repos avec silence-ws

**Les deux** (défaut, description générale) :
- `pdf-generator` — l'utilisateur peut dire `/pdf-generator` ou Claude le charge sur "génère un PDF"
- `commit-craft` — déclenché par `/commit-craft` ou automatiquement avant un commit

---

## 5. Traitement éditorial par type de contenu

### Comparaison tables (3 mécanismes → 2)
Supprimer la ligne "Command" et ajouter une note sur les modes d'invocation de Skill.

### Exemples de structure de fichiers
```
.claude/
├── skills/       # Slash commands + knowledge modules (unified since CC 2.1.3)
├── agents/
├── hooks/
└── rules/
```
La ligne `commands/` est supprimée des diagrammes d'arborescence.

### Decision trees
Les branches "→ Command" deviennent "→ Skill (user-invocable)".

### Frontmatter examples
Tout exemple de `command` frontmatter dans `.claude/commands/` devient un exemple de skill dans `.claude/skills/` avec `disable-model-invocation: true` si l'ancien exemple était une command pure.

### Callout notes sur la fusion
Dans les whitepapers, remplacer le callout générique "convergence" par un callout factuel :
> **CC 2.1.3 (janvier 2026)** : `.claude/commands/` est désormais fusionné dans `.claude/skills/`. Pour créer l'équivalent d'une ancienne command, placez le fichier dans `.claude/skills/` et ajoutez `disable-model-invocation: true` au frontmatter YAML.

---

## 6. Ce qui ne change PAS

- La terminologie "slash command" pour les built-in commands (`/clear`, `/compact`, `/help`)
- Le concept "Skill Evals" (Capability Uplift vs Encoded Preference) — inchangé
- La structure interne d'un fichier skill (SKILL.md + ressources)
- Le frontmatter `allowed-tools`, `effort`, `name`, `description` — inchangés
- Les agents — inchangés
- Les hooks — inchangés
- Les règles — inchangées

---

## 7. Version et attribution

Changement documenté dans CC 2.1.3 release notes.
Source officielle : https://code.claude.com/docs/fr/skills
Applicable depuis : 2026-01-11
Guide version cible : 3.41.0 (minor bump — changement pédagogique majeur)
```

- [ ] **Step 2: Verify file was created**

```bash
wc -l /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/claudedocs/pedagogy-skills-merger.md
```
Expected: 100+ lines

- [ ] **Step 3: Commit**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
git add claudedocs/pedagogy-skills-merger.md
git commit -m "docs(pedagogy): add skills-commands merger editorial note (CC 2.1.3)"
```

---

## Task 2 — Cheatsheet (`guide/cheatsheet.md`)

**Files:**
- Modify: `guide/cheatsheet.md` at L162-165, L261-265, L363-375

Read the file first: `Read guide/cheatsheet.md lines 155-175` and `Read guide/cheatsheet.md lines 255-275` and `Read guide/cheatsheet.md lines 358-380`.

- [ ] **Step 1: Fix the directory tree (around L162-165)**

Find this exact block (the `.claude/` tree):
```
├── commands/           # Slash commands
├── hooks/              # Event scripts
├── rules/              # Auto-loaded rules
└── skills/             # Knowledge modules
```

Replace with:
```
├── hooks/              # Event scripts
├── rules/              # Auto-loaded rules
└── skills/             # Slash commands + knowledge modules (unified)
```

- [ ] **Step 2: Fix skill effort mention (around L261-265)**

Find the line mentioning `commands/` in context with skills/commands distinction. Read lines 255-270 to locate it exactly, then update any reference to `commands/` as a separate directory.

- [ ] **Step 3: Fix the Command template example (around L363-375)**

Find this block:
```markdown
### Command (`.claude/commands/my-command.md`)
```markdown
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
---
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

Replace with:
```markdown
### Skill — user-invocable (`.claude/skills/my-command/SKILL.md`)
```markdown
---
name: my-command
description: Brief description
argument-hint: "<required_arg> [--flag]"
disable-model-invocation: true
---
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

- [ ] **Step 4: Run verification**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
grep -n "commands/" guide/cheatsheet.md | grep -v "^#\|built-in\|git\|examples/commands"
```
Expected: 0 results (no remaining `.claude/commands/` refs outside examples)

- [ ] **Step 5: Commit**

```bash
git add guide/cheatsheet.md
git commit -m "docs(cheatsheet): update commands→skills unification (CC 2.1.3)"
```

---

## Task 3 — Ultimate Guide (`guide/ultimate-guide.md`)

**Files:**
- Modify: `guide/ultimate-guide.md` at §5 note (L7388+), §6 header (L8903+), comparison table (L6149), 3-way table (L7439), custom commands section (L9509-9540)

Read each section before editing: `Read guide/ultimate-guide.md lines 7388-7400`, `Read guide/ultimate-guide.md lines 8903-8920`, etc.

- [ ] **Step 1: Update §5 Skills intro note (around L7393-7400)**

Find this block:
```
> **Note (January 2026)**: Skills and Commands are being unified. Both now use the same invocation mechanism (`/skill-name` or `/command-name`), share YAML frontmatter syntax, and can be triggered identically. The conceptual distinction (skills = knowledge modules, commands = workflow templates) remains useful for organization, but technically they're converging. Create new ones based on purpose, not mechanism.
```

Replace with:
```
> **CC 2.1.3 (January 2026)**: Skills and Commands are now unified. `.claude/commands/` is merged into `.claude/skills/`. Skills have two invocation modes: user-triggered (`/skill-name`, equivalent to old commands) and model-triggered (auto-loaded by description match). To restrict a skill to user-invocation only, add `disable-model-invocation: true` to its frontmatter. Existing files in `.claude/commands/` remain backward-compatible but all new development belongs in `.claude/skills/`.
```

- [ ] **Step 2: Update §6 Commands header note (around L8910-8916)**

Find the identical "Note (January 2026)" block in §6 Commands and replace it with the same updated text as Step 1.

Then update the §6 section title line to:
```markdown
# 6. Commands (User-Invocable Skills)
```

And update the first paragraph after the note to read:
```
Slash commands are user-invocable skills. Since CC 2.1.3, they live in `.claude/skills/` (not `.claude/commands/`). The `/name` invocation syntax is unchanged. Add `disable-model-invocation: true` to a skill's frontmatter to make it user-only.
```

- [ ] **Step 3: Update Memory Loading Comparison table (around L6149)**

Find this table row:
```
| `.claude/commands/*.md` | Invocation only | Only when invoked | Workflow templates |
```

Replace with:
```
| `.claude/skills/*.md` (user-invocable) | Invocation only | Only when invoked `/name` | Workflow templates (old "commands") |
```

Note: the `.claude/skills/*.md` (model-invocable) row likely already exists in the table — do not duplicate it. If both rows need to be reconciled into one, merge them:
```
| `.claude/skills/*.md` | Invocation only | When invoked (`/name`) or auto-loaded by model | Workflow templates + knowledge modules |
```

- [ ] **Step 4: Update the 3-way comparison table (around L7435-7450)**

Find this table:
```markdown
| Aspect | Commands | Skills | Agents |
|--------|----------|--------|--------|
| **What it is** | Prompt template | Knowledge module | Context isolation tool |
| **Location** | `.claude/commands/` | `.claude/skills/` | `.claude/agents/` |
| **Invocation** | `/command-name` | `/skill-name` or auto-loaded | Task tool delegation |
...
```

Replace with:
```markdown
| Aspect | Skills (user-invocable) | Skills (model-invocable) | Agents |
|--------|------------------------|--------------------------|--------|
| **What it is** | Workflow template | Knowledge module | Context isolation tool |
| **Location** | `.claude/skills/` | `.claude/skills/` | `.claude/agents/` |
| **Invocation** | `/skill-name` (user types) | Auto-loaded by model | Task tool delegation |
| **Frontmatter** | `disable-model-invocation: true` | Default (no flag needed) | n/a |
| **Execution** | In main conversation | Loaded into context | Separate subprocess |
| **Context** | Shares main context | Adds to agent context | Isolated context |
| **Best for** | Repeatable manual workflows | Reusable knowledge | Scope-limited analysis |
| **Token cost** | Low (template only) | Medium (knowledge loaded) | High (full agent) |
| **Examples** | `/commit`, `/pr`, `/ship` | TDD, security-guardian | security-audit, perf-audit |
```

Also update the Quick Reference table just above (around L7430):
```markdown
| **Agent** | Context isolation tool | Task tool delegation |
| **Skill** | Knowledge module or workflow | `/skill-name` (user) or auto-loaded (model) |
```
(Remove the `| **Command** |` row entirely.)

- [ ] **Step 5: Update Decision Tree**

Find the decision tree block that starts "Is this a repeatable workflow with steps?" (around L7460+). Update the first branch:

Old:
```
├─ Yes → Use a COMMAND
│        Example: /commit, /release-notes, /ship
```

New:
```
├─ Yes → Use a SKILL (user-invocable, disable-model-invocation: true)
│        Example: /commit, /release-notes, /ship
```

- [ ] **Step 6: Update Custom Commands section (around L9509-9540)**

Find:
```
### Custom Commands

You can create your own commands in `.claude/commands/`:

```
/tech:commit    → .claude/commands/tech/commit.md
/tech:pr        → .claude/commands/tech/pr.md
/product:scope  → .claude/commands/product/scope.md
```
```

Replace with:
```
### User-Invocable Skills (formerly "Custom Commands")

Since CC 2.1.3, user-invocable skills live in `.claude/skills/`:

```
/tech:commit    → .claude/skills/tech/commit/SKILL.md
/tech:pr        → .claude/skills/tech/pr/SKILL.md
/product:scope  → .claude/skills/product/scope/SKILL.md
```

Add `disable-model-invocation: true` to the frontmatter to prevent the model from auto-loading the skill when not explicitly invoked.
```

Also update the directory tree example in §6.2 Creating Custom Commands:
```
.claude/skills/
├── tech/           # Development workflows
│   ├── commit/SKILL.md
│   └── pr/SKILL.md
├── product/        # Product workflows
│   └── problem-framer/SKILL.md
└── support/        # Support workflows
    └── ticket-analyzer/SKILL.md
```

- [ ] **Step 7: Verify no stray `.claude/commands/` references remain in non-example context**

```bash
grep -n "\.claude/commands/" guide/ultimate-guide.md | grep -v "examples/\|# \|backward-compat\|rétrocompat\|symlink\|ln -s"
```
Expected: only references that explicitly discuss the deprecated path or examples.

- [ ] **Step 8: Commit**

```bash
git add guide/ultimate-guide.md
git commit -m "docs(guide): reframe commands as user-invocable skills (CC 2.1.3)"
```

---

## Task 4 — WP02 FR+EN (`02-personnalisation.qmd` / `02-customization.qmd`)

**Files:**
- Modify: `whitepapers/fr/02-personnalisation.qmd`
- Modify: `whitepapers/en/02-customization.qmd`

This is the most impacted whitepaper. Edit FR first, then mirror every change to EN.

Read the following sections before editing:
- `Read whitepapers/fr/02-personnalisation.qmd lines 170-215`
- `Read whitepapers/fr/02-personnalisation.qmd lines 60-75` (decision table row 3)
- `Read whitepapers/fr/02-personnalisation.qmd lines 735-815`
- `Read whitepapers/fr/02-personnalisation.qmd lines 860-930`

- [ ] **Step 1: Update persona table row (around L55)**

Find the level table row:
```
| **3** | Skills + Commands | Modules + Automatisation | Avancé |
```

Replace with:
```
| **3** | Skills avancés | Modules réutilisables + Workflows codifiés | Avancé |
```

- [ ] **Step 2: Update decision tree entry (around L68-70)**

Find:
```
└─ Workflow automatisé → Command
```

Replace with:
```
└─ Workflow automatisé → Skill (user-invocable)
```

- [ ] **Step 3: Update CLAUDE.md `## Commands` sections (around L175, L204)**

These two sections show a CLAUDE.md template with a heading `## Commands`. This is fine — "Commands" in CLAUDE.md refers to build/test/lint commands, not slash commands. No change needed here unless the context implies `.claude/commands/` directory. Read the lines to verify and add an inline comment if ambiguous.

- [ ] **Step 4: Update Agent vs Skill vs Command table (around L742)**

Find the table:
```markdown
| Mécanisme | Déclenchement | Portée | Persiste entre sessions | Cas d'usage idéal | Exemple concret |
|-----------|--------------|--------|------------------------|-------------------|-----------------|
| **Agent** | ... |
| **Skill** | ... |
| **Command** | `/namespace:nom` par l'utilisateur | Projet ou global | Non (template) | Workflow répétitif avec arguments | `/tech:commit "feat: login"` |
```

Replace the entire table with the 2-row version from the pedagogy note:
```markdown
| Mécanisme | Déclenchement | Portée | Cas d'usage idéal | Exemple concret |
|-----------|--------------|--------|-------------------|-----------------|
| **Agent** | Task tool / invocation Claude | Session isolée | Audit one-shot, traitement parallèle | `dep-auditor` sur package.json |
| **Skill** | `/nom` (user) ou auto (modèle) | Partagé entre agents | Connaissance ou workflow réutilisable | `security-guardian` OWASP |
```

- [ ] **Step 5: Update Règle de sélection rapide (around L762)**

Find the three-bullet rule:
```
- Une même tâche revient plusieurs fois par semaine avec le même périmètre de fichiers → **Agent**
- Plusieurs agents ont besoin des mêmes connaissances spécialisées → **Skill**
- Un humain déclenche manuellement une séquence d'actions prévisible → **Command**
```

Replace with:
```
- Une même tâche requiert un contexte isolé ou du traitement parallèle → **Agent**
- Un savoir-faire ou workflow doit être réutilisable → **Skill**
  - L'utilisateur déclenche manuellement → `disable-model-invocation: true`
  - Le modèle détecte le besoin → laisser le défaut (model-invocable)
```

- [ ] **Step 6: Update anti-pattern callout (around L765)**

Find:
```
::: {.callout-note title="Anti-pattern courant : le skill-command mix"}
Créer une command quand il faut un skill (ou vice versa) est l'erreur la plus fréquente. Signal : si vous copiez-collez les mêmes instructions dans plusieurs agents → c'est un skill. Si un humain tape un slash pour déclencher → c'est une command.
:::
```

Replace with:
```
::: {.callout-note title="Anti-pattern courant : mauvaise configuration d'invocation"}
La confusion entre skill user-invocable et model-invocable est l'erreur la plus fréquente depuis la fusion CC 2.1.3. Signal : si un humain tape le slash manuellement à chaque fois → ajoutez `disable-model-invocation: true`. Si vous voulez que le modèle charge la skill automatiquement selon le contexte → laissez le défaut.
:::
```

- [ ] **Step 7: Update `# Commands` chapter header and intro (around L918)**

Find the `# Commands : Slash Commands Custom` section header and the intro paragraph explaining "Contrairement aux agents (qui isolent le contexte) et aux skills (qui partagent des connaissances), les commands encapsulent une séquence d'actions..."

Update the header:
```
# Skills User-Invocables : Slash Commands
```

Update the intro paragraph to read:
```
Depuis CC 2.1.3, les "commands" custom vivent dans `.claude/skills/` et non plus `.claude/commands/`. Un skill user-invocable s'utilise exactement comme une ancienne command — l'utilisateur tape `/nom-skill` — mais il bénéficie de la même syntaxe frontmatter que tous les autres skills. Pour restreindre l'invocation à l'utilisateur uniquement, ajoutez `disable-model-invocation: true`.
```

- [ ] **Step 8: Update structure example in Commands chapter**

Find any `.claude/commands/` directory tree in this chapter:
```
.claude/commands/
├── release.md
└── ...
```

Replace with:
```
.claude/skills/
├── release/
│   └── SKILL.md    # /release — disable-model-invocation: true
└── ...
```

- [ ] **Step 9: Update frontmatter examples**

Find any Command frontmatter example like:
```yaml
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
---
```
(in `.claude/commands/` context)

Replace with:
```yaml
---
name: my-workflow
description: Brief description
argument-hint: "<required_arg> [--flag]"
disable-model-invocation: true
---
```

- [ ] **Step 10: Mirror all changes to EN file**

For each change made to `whitepapers/fr/02-personnalisation.qmd`, apply the equivalent change to `whitepapers/en/02-customization.qmd`. The EN file has the same structure but in English. Read each equivalent section before editing.

- [ ] **Step 11: Commit FR**

```bash
git add whitepapers/fr/02-personnalisation.qmd
git commit -m "docs(wp02-fr): update commands→skills unification (CC 2.1.3)"
```

- [ ] **Step 12: Commit EN**

```bash
git add whitepapers/en/02-customization.qmd
git commit -m "docs(wp02-en): parity update commands→skills unification (CC 2.1.3)"
```

---

## Task 5 — WP07 FR+EN (`07-guide-reference.qmd`)

**Files:**
- Modify: `whitepapers/fr/07-guide-reference.qmd`
- Modify: `whitepapers/en/07-reference-guide.qmd`

Read these sections first:
- `Read whitepapers/fr/07-guide-reference.qmd lines 50-60`
- `Read whitepapers/fr/07-guide-reference.qmd lines 300-310`
- `Read whitepapers/fr/07-guide-reference.qmd lines 540-550`
- `Read whitepapers/fr/07-guide-reference.qmd lines 574-640`

- [ ] **Step 1: Update marketing bullet (around L54)**

Find:
```
| **Personnalisable** | Agents, Skills, Commands, Hooks pour adapter à vos workflows |
```

Replace with:
```
| **Personnalisable** | Agents, Skills (user-invocable + model-invocable), Hooks |
```

- [ ] **Step 2: Update "Configurer 1-2 commandes custom" (around L305)**

Find:
```
□ Configurer 1-2 commandes custom pour tâches fréquentes
```

Replace with:
```
□ Créer 1-2 skills user-invocables pour tâches fréquentes (`.claude/skills/`, `disable-model-invocation: true`)
```

- [ ] **Step 3: Update "Commandes Utiles" section (around L545)**

Read lines 540-560 to check context. If this section discusses custom commands (not built-in), update the path reference. Built-in commands (`/clear`, `/compact`) keep their terminology unchanged.

- [ ] **Step 4: Update Chapter 5 header and comparison table (around L574-630)**

Find the chapter header:
```
# Chapitre 5 : Agents, Skills, Commands
```

Replace with:
```
# Chapitre 5 : Agents, Skills
```

Find the comparison table:
```markdown
| Extension | Quand | Exemple |
|-----------|-------|---------|
| **Command** | Action rapide, pas de state | `/format`, `/test` |
| **Skill** | Module réutilisable avec ressources | `/review`, `/deploy` |
| **Agent** | Persona spécialisé pour un domaine | Security Auditor, DBA Expert |
```

Replace with:
```markdown
| Extension | Quand | Exemple |
|-----------|-------|---------|
| **Skill (user-invocable)** | Workflow déclenché manuellement | `/format`, `/test`, `/commit` |
| **Skill (model-invocable)** | Connaissance chargée selon le contexte | `security-guardian`, TDD |
| **Agent** | Persona spécialisé pour un domaine | Security Auditor, DBA Expert |
```

- [ ] **Step 5: Update Slash Commands section (around L590-630)**

Find:
```
## Slash Commands

### Anatomie d'une Command

````markdown
---
name: test
description: Run tests for modified files
...
### Placement

```
.claude/commands/
├── test.md
...
```
```

Replace the placement section:
```
### Placement (depuis CC 2.1.3)

```
.claude/skills/
├── test/SKILL.md    # /test → disable-model-invocation: true
├── format/SKILL.md
└── deploy/SKILL.md
```
```

And update the frontmatter example to include `disable-model-invocation: true`.

- [ ] **Step 6: Update Skills section — remove distinction paragraph**

Find:
```
Les skills sont des modules de connaissance réutilisables, distincts des Commands qui sont des prompts réutilisables.
```

Replace with:
```
Les skills sont des modules réutilisables qui couvrent deux cas d'usage : connaissance partagée (chargée par le modèle) et workflows manuels (invoqués par l'utilisateur via `/nom`). Depuis CC 2.1.3, ils vivent tous dans `.claude/skills/`.
```

- [ ] **Step 7: Mirror to EN + commit both**

Apply equivalent changes to `whitepapers/en/07-reference-guide.qmd`.

```bash
git add whitepapers/fr/07-guide-reference.qmd whitepapers/en/07-reference-guide.qmd
git commit -m "docs(wp07): update commands→skills unification (CC 2.1.3)"
```

---

## Task 6 — WP04 FR+EN (`04-architecture.qmd`)

**Files:**
- Modify: `whitepapers/fr/04-architecture.qmd` L432, L785
- Modify: `whitepapers/en/04-architecture.qmd`

Read first: `Read whitepapers/fr/04-architecture.qmd lines 425-440` and `Read whitepapers/fr/04-architecture.qmd lines 780-792`.

- [ ] **Step 1: Update decision tree branch (around L432)**

Find:
```
├─ Oui → Skill / Slash Command (.claude/commands/)
```

Replace with:
```
├─ Oui → Skill user-invocable (.claude/skills/, disable-model-invocation: true)
```

- [ ] **Step 2: Update extension comparison row (around L785)**

Find:
```
| **Skills** | Faible | Nulle | Global | Workflows récurrents, slash commands |
```

Replace with:
```
| **Skills** | Faible | Nulle | Global | Workflows récurrents (user-invocable) + modules de connaissance (model-invocable) |
```

- [ ] **Step 3: Mirror to EN + commit**

```bash
git add whitepapers/fr/04-architecture.qmd whitepapers/en/04-architecture.qmd
git commit -m "docs(wp04): update commands reference (CC 2.1.3)"
```

---

## Task 7 — Recap Card c04 FR+EN (full rewrite)

**Files:**
- Rewrite: `whitepapers/recap-cards/fr/c04-commands-skills-plugins-agents.qmd`
- Rewrite: `whitepapers/recap-cards/en/c04-commands-skills-plugins-agents.qmd`

Read the current files first to understand the structure: `Read whitepapers/recap-cards/fr/c04-commands-skills-plugins-agents.qmd`.

- [ ] **Step 1: Rewrite FR c04**

Replace the full content of `whitepapers/recap-cards/fr/c04-commands-skills-plugins-agents.qmd` with:

```qmd
---
title: "Skills, Plugins & Agents"
subtitle: "Choisir le bon mécanisme d'extension selon le besoin"
card-number: "C04"
category: "Conception"
difficulty: "intermediate"
guide-version: "3.41.0"
author: "Florian BRUNIAUX"
version: "3.41.0"
date: "Mai 2026"
layout: "two-col"
lang: fr
format:
  recap-card-typst: default
---

## Tableau de comparaison

| Mécanisme | Scope | Invocation | Ressources | Cas d'usage |
|-----------|-------|-----------|-----------|-------------|
| **Skill (user)** | Workflow codifié | `/nom` (utilisateur) | Oui | Tâche répétable déclenchée manuellement |
| **Skill (auto)** | Connaissance réutilisable | Auto par le modèle | Oui | Expertise partagée entre agents |
| **Plugin** | Marketplace | Global | Oui | Intégration tierce |
| **Agent** | Spécialiste autonome | Task tool | Via memory | Délégation complexe |

> **CC 2.1.3** : `.claude/commands/` est fusionné dans `.claude/skills/`. Ajoutez `disable-model-invocation: true` pour une skill déclenchée uniquement par l'utilisateur.

## Skills user-invocables (ex-commands)

Depuis CC 2.1.3, les workflows déclenchés manuellement par `/nom` sont des skills dans `.claude/skills/` avec `disable-model-invocation: true`.

```yaml
# .claude/skills/release/SKILL.md
---
name: release
description: Prépare une release (bump version, CHANGELOG, tag)
allowed-tools: [Read, Write, Bash]
disable-model-invocation: true
---
1. Lire la version courante dans package.json
2. Bumper selon semver (patch/minor/major)
3. Mettre à jour CHANGELOG.md
4. Créer un tag git
```

**Quand choisir :** vous avez une séquence d'instructions que vous déclenchez intentionnellement plusieurs fois par semaine.

## Skills model-invocables

Un skill sans `disable-model-invocation` est chargé automatiquement par le modèle quand la description correspond au contexte.

```yaml
# .claude/skills/security-guardian/SKILL.md
---
name: security-guardian
description: OWASP security review — use when reviewing auth, routes, or user input
allowed-tools: [Read, Grep, Glob]
---
Analyser le code pour les vulnérabilités OWASP Top 10...
```

**Quand choisir :** plusieurs agents ont besoin des mêmes connaissances spécialisées, ou vous voulez que Claude charge automatiquement l'expertise appropriée.

## Plugins : intégrations tierces

Les plugins proviennent du marketplace et ajoutent des capacités externes. Ils s'installent via `/plugin marketplace add`.

**Quand choisir :** une intégration avec un service tiers existant couvre exactement votre besoin.

`${CLAUDE_PLUGIN_DATA}` (v2.1.78+) : répertoire persistant pour stocker l'état entre sessions.

## Agents : délégation de tâches complexes

Un agent est un Claude spécialisé avec ses propres outils et son propre scope. Il sert à isoler le contexte, pas à simuler un rôle humain.

```yaml
# .claude/agents/security-audit.md
---
name: security-audit
model: opus
tools: Read, Grep, Glob
---
Analyser le code pour les vulnérabilités OWASP...
```

**Quand choisir :** tâche longue qui polluerait le contexte principal, ou travail parallélisable.

## Règle de décision rapide

Workflow déclenché manuellement = **Skill user-invocable**. Connaissance à partager entre agents = **Skill model-invocable**. Intégration tierce = **Plugin**. Tâche à déléguer avec contexte isolé = **Agent**.
```

- [ ] **Step 2: Write EN c04**

Read `whitepapers/recap-cards/en/c04-commands-skills-plugins-agents.qmd` then create the English equivalent with:
- Same structure, English language
- `title: "Skills, Plugins & Agents"` (remove "Commands" from title)
- `lang: en`
- Same version `3.41.0`
- All French text translated faithfully

- [ ] **Step 3: Commit**

```bash
git add whitepapers/recap-cards/fr/c04-commands-skills-plugins-agents.qmd \
        whitepapers/recap-cards/en/c04-commands-skills-plugins-agents.qmd
git commit -m "docs(c04): rewrite recap card — skills unified model (CC 2.1.3)"
```

---

## Task 8 — Recap Cards m09, m10, t01 FR+EN

**Files:**
- Modify: `whitepapers/recap-cards/fr/m09-slash-commands.qmd`
- Modify: `whitepapers/recap-cards/en/m09-slash-commands.qmd`
- Modify: `whitepapers/recap-cards/fr/m10-skills.qmd`
- Modify: `whitepapers/recap-cards/en/m10-skills.qmd`
- Modify: `whitepapers/recap-cards/fr/01-commandes-essentielles.qmd`
- Modify: `whitepapers/recap-cards/{fr,en}/t01-commandes-essentielles.qmd`

Decision on m09 vs m10: **Keep both** but reframe. m09 becomes "User-Invocable Skills" (slash-triggered), m10 keeps "Skills" with emphasis on both invocation modes.

Read all six files before editing.

- [ ] **Step 1: Update m09 FR — reframe as user-invocable skills**

- Update `subtitle` to: `"Skills déclenchés manuellement via /nom (CC 2.1.3)"`
- Add a callout box at the top: `> **CC 2.1.3** : Les "commands" custom vivent désormais dans `.claude/skills/` avec `disable-model-invocation: true`. La syntaxe `/nom` et le comportement sont identiques.`
- Update any `.claude/commands/` path to `.claude/skills/`
- Add `disable-model-invocation: true` to all frontmatter examples
- Update `guide-version` and `version` to `3.41.0`

- [ ] **Step 2: Update m09 EN**

Apply EN equivalent of Step 1.

- [ ] **Step 3: Update m10 FR — add invocation modes**

- Update intro paragraph to mention both invocation modes
- Add a small table showing user-invocable vs model-invocable distinction
- Add `disable-model-invocation: true` note for user-only skills
- Update `guide-version` and `version` to `3.41.0`

- [ ] **Step 4: Update m10 EN**

Apply EN equivalent of Step 3.

- [ ] **Step 5: Update 01-commandes-essentielles FR and t01 FR+EN**

Read the files. Check if they reference `.claude/commands/`. If yes, update to `.claude/skills/`. These cards focus on built-in commands (`/clear`, `/compact`) so changes are likely minor — just any directory tree showing `.claude/commands/`.

- [ ] **Step 6: Commit**

```bash
git add whitepapers/recap-cards/fr/m09-slash-commands.qmd \
        whitepapers/recap-cards/en/m09-slash-commands.qmd \
        whitepapers/recap-cards/fr/m10-skills.qmd \
        whitepapers/recap-cards/en/m10-skills.qmd \
        whitepapers/recap-cards/fr/01-commandes-essentielles.qmd \
        whitepapers/recap-cards/fr/t01-commandes-essentielles.qmd \
        whitepapers/recap-cards/en/t01-commandes-essentielles.qmd
git commit -m "docs(recap-cards): update m09/m10/t01 for skills unification (CC 2.1.3)"
```

---

## Task 9 — Landing Docs Mirrors

**Files (all in `/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/`):**
- `src/content/docs/guide/ultimate-guide/learning-path/05-skills.md`
- `src/content/docs/guide/ultimate-guide/06-commands.md`
- `src/content/docs/guide/ultimate-guide/learning-path/04-agents.md`
- `src/content/docs/learning-path/05-skills.md`
- `src/content/docs/learning-path/04-agents.md`
- `src/content/docs/skill-design-patterns.md`
- `src/content/docs/cheatsheet.md`

These mirror the guide. Apply the same changes as Tasks 2–5 but in the landing format (Astro MDX or Markdown).

For each file: read it first to understand the format, then apply changes using the pedagogy note as reference.

- [ ] **Step 1: Update `06-commands.md`**

This page maps to guide §6. Apply changes from Task 3 Steps 2, 5, 6. Update title to "Commands (User-Invocable Skills)". Add a notice box: "Since CC 2.1.3, user-invocable skills live in `.claude/skills/`. See Skills."

- [ ] **Step 2: Update `05-skills.md`**

Apply changes from Task 3 Step 1. Add invocation modes section.

- [ ] **Step 3: Update `04-agents.md`**

Minor: remove Command row from any Agent/Skill/Command comparison table.

- [ ] **Step 4: Update learning-path files**

Apply equivalent reframing. Read each file first.

- [ ] **Step 5: Update `skill-design-patterns.md`**

Read file. Update any patterns that show `.claude/commands/` context.

- [ ] **Step 6: Update `cheatsheet.md`**

Apply same changes as Task 2 (cheatsheet in guide).

- [ ] **Step 7: Commit**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing
git add src/content/docs/
git commit -m "docs: sync skills-commands unification from guide (CC 2.1.3)"
```

---

## Task 10 — Landing Cheatsheets, Questions, Data & Components

**Files (landing repo):**
- `src/content/cheatsheets/m09-slash-commands.md`
- `src/content/cheatsheets/m10-skills.md`
- `src/content/cheatsheets/c04-commands-skills-plugins-agents.md`
- `src/content/cheatsheets/m08-agents-custom.md`
- `src/content/cheatsheets/t01-commandes-essentielles.md`
- `src/content/questions/06-commands/` (full dir)
- `src/content/questions/05-skills/` (≥20 files)
- `src/data/examples-data.ts`
- `src/data/search-index.ts`
- `src/data/guide-search-entries.ts`
- `src/data/guide-anchor-map.json`
- `src/utils/categories.ts`
- `src/components/landing/FeaturesGrid.astro`
- `src/components/landing/ExamplesCatalog.astro`

- [ ] **Step 1: Update landing cheatsheets**

For `c04-commands-skills-plugins-agents.md`: replace with content mirroring the rewritten recap card (Task 7). Remove "Commands" section, add "User-invocable Skills" and "Model-invocable Skills".

For `m09-slash-commands.md` and `m10-skills.md`: mirror Task 8 changes.

For `m08-agents-custom.md`: read file, check for Command/Skill comparison — update if found.

For `t01-commandes-essentielles.md`: read file, check for `.claude/commands/` reference — update if found.

- [ ] **Step 2: Audit questions/06-commands/ directory**

```bash
ls src/content/questions/06-commands/
```

For each .md file: read it, check if the answer references `.claude/commands/` as a path, or describes commands as a separate mechanism from skills. Update any outdated Q&A to reflect the unified model. Key Q&As that certainly need updating:
- "Où placer mes commands custom ?" → answer: `.claude/skills/`
- "Quelle est la différence entre command et skill ?" → answer: invocation mode, not separate mechanisms
- "Comment créer une command ?" → answer: create skill with `disable-model-invocation: true`

- [ ] **Step 3: Audit questions/05-skills/ directory**

```bash
ls src/content/questions/05-skills/
```

For each file referencing "command vs skill" as separate types: update to reflect unified model.

- [ ] **Step 4: Update data files**

Read `src/data/examples-data.ts` and search for `commands/` references in skill/command categories. Update category labels if needed.

Read `src/utils/categories.ts` and check if "commands" is a separate category from "skills". If yes, merge or rename.

Read `src/data/search-index.ts` and `guide-search-entries.ts` for stale anchor refs pointing to `#62-creating-custom-commands` — these may still be valid as section anchors but check for outdated descriptions.

Update `guide-anchor-map.json` if section 6 anchor description reads "Creating Custom Commands" — update to "User-Invocable Skills".

- [ ] **Step 5: Update components**

Read `src/components/landing/FeaturesGrid.astro` — check for "Commands" as a listed feature separate from "Skills". Update to reflect unified model.

Read `src/components/landing/ExamplesCatalog.astro` — check for "commands" filter/category. If commands examples are listed separately from skills, add a unification note or merge the categories.

- [ ] **Step 6: Commit**

```bash
git add src/content/cheatsheets/ src/content/questions/ src/data/ src/utils/ src/components/
git commit -m "docs(landing): update cheatsheets, FAQ, data for skills unification (CC 2.1.3)"
```

---

## Task 11 — Machine-readable files

**Files (guide repo):**
- `machine-readable/reference.yaml`
- `llms.txt`
- `llms-full.txt`
- `machine-readable/llms.txt`

- [ ] **Step 1: Update reference.yaml**

Read `machine-readable/reference.yaml` lines 30-40 and lines 170-180 and lines 215-225 and lines 275-285 and lines 345-360.

For each entry that points to `examples/commands/` where the example is a custom workflow (not a built-in command reference), add a sibling `_note: "Equivalent skill: examples/skills/..."` or update to the skills path if the example has been migrated.

Update the description fields where they say "slash commands in .claude/commands/" to "user-invocable skills in .claude/skills/".

Add a new entry for the CC 2.1.3 skills-commands merger:
```yaml
skills_commands_merger:
  version: "2.1.3"
  date: "2026-01-11"
  summary: ".claude/commands/ merged into .claude/skills/. Add disable-model-invocation: true for user-only skills."
  docs: "https://code.claude.com/docs/en/skills"
  guide_section: "guide/ultimate-guide.md:8903"
```

- [ ] **Step 2: Update llms.txt**

Read `llms.txt`. Find any bullet or section describing the CC project structure that lists `commands/` and `skills/` as separate directories. Update to show `skills/` as the unified directory.

Update the version reference to `3.41.0`.

- [ ] **Step 3: Update llms-full.txt**

Read `llms-full.txt`. Apply the same directory structure fix as Step 2. Update the skills/commands section to describe the unified model with invocation modes. Update version.

- [ ] **Step 4: Update machine-readable/llms.txt**

Apply same changes as Step 2.

- [ ] **Step 5: Commit**

```bash
git add machine-readable/reference.yaml llms.txt llms-full.txt machine-readable/llms.txt
git commit -m "docs(machine-readable): update for skills-commands unification v3.41.0"
```

---

## Task 12 — PDF Generation

**Prerequisites:** Tasks 4, 5, 6, 7, 8 must be complete.

**Files:**
- `whitepapers/fr/02-personnalisation.qmd` → PDF
- `whitepapers/en/02-customization.qmd` → PDF
- `whitepapers/fr/04-architecture.qmd` → PDF
- `whitepapers/en/04-architecture.qmd` → PDF
- `whitepapers/fr/07-guide-reference.qmd` → PDF
- `whitepapers/en/07-reference-guide.qmd` → PDF
- Recap cards: c04, m09, m10, 01-commandes, t01 (FR+EN)
- `whitepapers/CHANGELOG.md`

**IMPORTANT**: Always use `--to whitepaper-typst`. Never `--to pdf`.

- [ ] **Step 1: Bump wp-version in WP02 frontmatters**

In `whitepapers/fr/02-personnalisation.qmd`, find the `wp-version` frontmatter field and increment it. Read the current value first.

Apply same bump to `whitepapers/en/02-customization.qmd`.

Apply same to WP04 and WP07 (FR+EN).

- [ ] **Step 2: Bump guide-version in recap card frontmatters**

In each modified recap card, set `guide-version: "3.41.0"` and `version: "3.41.0"`.

- [ ] **Step 3: Render WP02 FR+EN**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/fr
quarto render 02-personnalisation.qmd --to whitepaper-typst
```

Expected: generates `02-personnalisation.pdf` with no Quarto errors.

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/en
quarto render 02-customization.qmd --to whitepaper-typst
```

- [ ] **Step 4: Render WP04 FR+EN**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/fr
quarto render 04-architecture.qmd --to whitepaper-typst

cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/en
quarto render 04-architecture.qmd --to whitepaper-typst
```

- [ ] **Step 5: Render WP07 FR+EN**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/fr
quarto render 07-guide-reference.qmd --to whitepaper-typst

cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/en
quarto render 07-reference-guide.qmd --to whitepaper-typst
```

- [ ] **Step 6: Render recap cards**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers/recap-cards
./render-recap-cards.sh fr
./render-recap-cards.sh en
```

If the script doesn't exist or errors, render individually:
```bash
cd whitepapers/recap-cards/fr
for f in c04-commands-skills-plugins-agents.qmd m09-slash-commands.qmd m10-skills.qmd 01-commandes-essentielles.qmd t01-commandes-essentielles.qmd; do
  quarto render "$f" --to whitepaper-typst
done
```

- [ ] **Step 7: Update whitepapers/CHANGELOG.md**

Add an entry at the top of `whitepapers/CHANGELOG.md`:
```markdown
## [2026-05-18] Skills–Commands Merger Update

### Changed (CC 2.1.3 — January 2026)
- **WP02 FR/EN** (Personnalisation/Customization): Unified Agent/Skill/Command → Agent/Skill table. Removed "Command" as separate mechanism. Updated `.claude/commands/` → `.claude/skills/` throughout.
- **WP04 FR/EN** (Architecture): Updated decision tree and extension comparison row.
- **WP07 FR/EN** (Guide Référence): Updated Chapter 5 header and comparison table.
- **Recap card C04 FR/EN**: Full rewrite — title "Skills, Plugins & Agents", new 4-row table with user-invocable and model-invocable skills.
- **Recap cards M09/M10 FR/EN**: M09 reframed as user-invocable skills, M10 updated with invocation modes.
- **T01 FR/EN**: Minor update — `.claude/commands/` path removed.
```

- [ ] **Step 8: Commit versions + CHANGELOG**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
git add whitepapers/
git commit -m "docs(whitepapers): regenerate PDFs + CHANGELOG for CC 2.1.3 skills merger"
```

---

## Task 13 — Deploy & Announce

**Files:**
- `florian-portfolio/public/guides/` (copy PDFs)
- `florian-portfolio/api/guides.mjs` (GUIDE_MANIFEST update)
- Landing `src/data/whitepapers-data.ts`
- Landing `src/components/landing/AnnouncementBanner.astro`
- Landing `src/data/rss-entries.ts`
- Guide `CHANGELOG.md` [Unreleased]
- Guide `VERSION`

**IMPORTANT**: Do not forget `florian-portfolio/api/guides.mjs`. Without this update, existing email subscribers receive the old PDF on download.

- [ ] **Step 1: Copy PDFs to portfolio**

```bash
PORTFOLIO=/Users/florianbruniaux/Sites/perso/florian-portfolio/public/guides
WHITEPAPERS=/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/whitepapers

# WP02 FR+EN
cp "$WHITEPAPERS/fr/02-personnalisation.pdf" "$PORTFOLIO/"
cp "$WHITEPAPERS/en/02-customization.pdf" "$PORTFOLIO/"

# WP04 FR+EN
cp "$WHITEPAPERS/fr/04-architecture.pdf" "$PORTFOLIO/"
cp "$WHITEPAPERS/en/04-architecture.pdf" "$PORTFOLIO/"

# WP07 FR+EN
cp "$WHITEPAPERS/fr/07-guide-reference.pdf" "$PORTFOLIO/"
cp "$WHITEPAPERS/en/07-reference-guide.pdf" "$PORTFOLIO/"

# Recap cards
for f in c04-commands-skills-plugins-agents m09-slash-commands m10-skills 01-commandes-essentielles t01-commandes-essentielles; do
  cp "$WHITEPAPERS/recap-cards/fr/${f}.pdf" "$PORTFOLIO/" 2>/dev/null || true
  cp "$WHITEPAPERS/recap-cards/en/${f}.pdf" "$PORTFOLIO/" 2>/dev/null || true
done
```

- [ ] **Step 2: Get PDF hashes**

```bash
md5 /Users/florianbruniaux/Sites/perso/florian-portfolio/public/guides/02-personnalisation.pdf
md5 /Users/florianbruniaux/Sites/perso/florian-portfolio/public/guides/02-customization.pdf
md5 /Users/florianbruniaux/Sites/perso/florian-portfolio/public/guides/07-guide-reference.pdf
md5 /Users/florianbruniaux/Sites/perso/florian-portfolio/public/guides/07-reference-guide.pdf
```

Note the hashes — they go into guides.mjs and whitepapers-data.ts.

- [ ] **Step 3: Update florian-portfolio/api/guides.mjs**

Read the file first: `Read /Users/florianbruniaux/Sites/perso/florian-portfolio/api/guides.mjs`.

Find the `GUIDE_MANIFEST` array entries for each updated whitepaper. Update the `hashedFileFr` and `hashedFileEn` fields (or equivalent) with the new MD5 hashes from Step 2.

Also update any `version` field in these entries to `3.41.0`.

- [ ] **Step 4: Update landing whitepapers-data.ts**

Read `src/data/whitepapers-data.ts` in the landing repo.

Find `const V` or the version constant and update to `"3.41.0"`.

Update the `hashedFileFr` and `hashedFileEn` (or equivalent fields) for the updated whitepapers using the MD5 hashes from Step 2.

- [ ] **Step 5: Update AnnouncementBanner.astro**

Read `src/components/landing/AnnouncementBanner.astro`.

Find the `BANNER_ID` constant and increment it by 1.

Update the banner message to:
```
🔄 Mise à jour CC 2.1.3 : Skills et Commands unifiés — Whitepapers 02, 04, 07 + Recap Cards mis à jour
```

(EN version if there's a separate one):
```
🔄 CC 2.1.3 Update: Skills and Commands unified — Whitepapers 02, 04, 07 + Recap Cards updated
```

- [ ] **Step 6: Update rss-entries.ts**

Read `src/data/rss-entries.ts`.

Add a new entry to the array (at the top, most recent first):
```typescript
{
  id: "guide_release_3_41_0",
  type: "guide_release",
  date: "2026-05-18",
  title: "v3.41.0 — Skills & Commands unifiés (CC 2.1.3)",
  titleEn: "v3.41.0 — Skills & Commands Unified (CC 2.1.3)",
  description: "Mise à jour pédagogique majeure : .claude/commands/ fusionné dans .claude/skills/. Whitepapers 02, 04, 07 (FR+EN) + Recap Cards c04, m09, m10 mis à jour.",
  descriptionEn: "Major pedagogical update: .claude/commands/ merged into .claude/skills/. Whitepapers 02, 04, 07 (FR+EN) + Recap Cards c04, m09, m10 updated.",
  link: "/changelog#v3410",
},
```

- [ ] **Step 7: Update guide CHANGELOG.md [Unreleased]**

Add under `## [Unreleased]` in `CHANGELOG.md`:

```markdown
### Changed

- **Skills–Commands unification (CC 2.1.3)**: All educational content updated to reflect that `.claude/commands/` is merged into `.claude/skills/`. The 3-way Agent/Skill/Command comparison is now a 2-way Agent/Skill model with invocation modes (user-invocable via `disable-model-invocation: true`, model-invocable by default). Affected files: `guide/cheatsheet.md`, `guide/ultimate-guide.md` §5 and §6, `whitepapers/fr+en/02`, `04`, `07`, recap cards `c04`, `m09`, `m10`, `01-commandes-essentielles`, `t01`, all landing mirrors and Q&A, machine-readable index. New pedagogical reference: `claudedocs/pedagogy-skills-merger.md`.
```

- [ ] **Step 8: Bump VERSION to 3.41.0**

```bash
echo "3.41.0" > /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide/VERSION
```

- [ ] **Step 9: Commit and push guide repo**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide
git add VERSION CHANGELOG.md
git commit -m "chore(release): bump to v3.41.0 — skills-commands merger (CC 2.1.3)"
```

- [ ] **Step 10: Commit and push portfolio repo**

```bash
cd /Users/florianbruniaux/Sites/perso/florian-portfolio
git add public/guides/ api/guides.mjs
git commit -m "chore: update guides v3.41.0 — skills-commands merger PDFs"
```

- [ ] **Step 11: Commit and push landing repo**

```bash
cd /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing
git add src/data/whitepapers-data.ts \
        src/components/landing/AnnouncementBanner.astro \
        src/data/rss-entries.ts
git commit -m "chore(release): v3.41.0 — skills-commands merger, banner + RSS"
```

---

## Self-Review

### Spec coverage check

| Spec requirement | Task |
|-----------------|------|
| Note pédagogique avant toute édition | T1 |
| Recap card c04 FR+EN refonte complète | T7 |
| Whitepaper 02 FR+EN | T4 |
| Guide ultimate-guide.md | T3 |
| Cheatsheet | T2 |
| Recap cards m09+m10 | T8 |
| Whitepaper 07 | T5 |
| Whitepaper 04 | T6 |
| Landing docs miroirs | T9 |
| Landing cheatsheets | T10 |
| Landing questions FAQ | T10 |
| machine-readable + llms.txt | T11 |
| PDFs régénérés --to whitepaper-typst | T12 |
| Versions bumpées + CHANGELOG ebooks | T12 |
| 3 fichiers PDF deployment sync (portfolio + landing + guides.mjs) | T13 |
| Landing rebuild + AnnouncementBanner BANNER_ID | T13 |
| RSS entry | T13 |
| CHANGELOG guide [Unreleased] | T13 |

All criteria accounted for. ✓

### Placeholder check

No TBD, TODO, or "implement later" in this plan. ✓

### Consistency check

- `disable-model-invocation: true` used consistently throughout ✓
- `.claude/skills/` used consistently as target path ✓
- `3.41.0` used consistently as target version ✓
- `2026-01-11` used consistently as change date ✓
