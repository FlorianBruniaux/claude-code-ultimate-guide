# Evaluation: agentskills.io - Agent Skills Open Specification

**Date**: 2026-02-01
**Source**: [agentskills.io](https://agentskills.io/home) | [GitHub: agentskills/agentskills](https://github.com/agentskills/agentskills) (8.2K stars) | [GitHub: anthropics/skills](https://github.com/anthropics/skills) (60.1K stars)
**Maintainer**: Anthropic (open development, community contributions)
**Type**: Open specification + reference implementation + official skill library
**License**: Apache 2.0 (spec + open skills), Source-available (document skills)

---

## Resume du contenu

- **Specification formelle** pour Agent Skills: format SKILL.md, YAML frontmatter, naming rules, directory structure, progressive disclosure model
- **26+ plateformes supportees**: Claude Code, Claude.ai, GitHub, Cursor, VS Code, OpenAI Codex, Gemini CLI, Goose, Roo Code, Amp, Spring AI, Databricks, Factory, Mistral Vibe, TRAE, Firebender, Letta, et plus
- **anthropics/skills** (60.1K stars): repo officiel Anthropic avec skills d'exemple (documents DOCX/PDF/PPTX/XLSX, creative, dev, enterprise) + integration plugin Claude Code
- **skills-ref CLI**: outil officiel de validation et generation de prompt XML (`skills-ref validate`, `skills-ref to-prompt`)
- **Guide d'integration**: documentation pour ajouter le support skills dans n'importe quel agent (filesystem-based ou tool-based)

## Score de pertinence: 4/5

**Justification**:

1. **Gap majeur confirme**: Le guide documente les skills comme une feature Claude Code sans mentionner que c'est un **standard ouvert cross-plateforme** maintenu par Anthropic. C'est une omission significative pour un guide qui se veut reference.
2. **60.1K stars**: `anthropics/skills` est le repo Anthropic le plus starre. Le guide le mentionne en passant (`npx add-skill anthropics/skills` sur 2 lignes) sans documenter son contenu ni son ampleur.
3. **agentskills.io absent**: La specification formelle (naming rules, progressive disclosure, integration guide) n'apparait nulle part dans le guide. Pourtant c'est la source de verite de la feature que le guide documente.
4. **Interoperabilite = argument de poids**: Dire a un utilisateur "vos skills Claude Code fonctionnent aussi dans Cursor, VS Code, Codex, Gemini CLI" est une info a haute valeur ajoutee.
5. **Pas un 5/5 car**: Le guide documente deja bien les skills pour l'usage Claude Code quotidien. L'utilisateur typique n'a pas besoin de la spec formelle pour utiliser des skills. Le gap est conceptuel (manque de contexte) plus que pratique (manque de how-to).

## Comparatif

| Aspect | agentskills.io | Notre guide |
|--------|---------------|-------------|
| Spec SKILL.md formelle | Source de verite (naming rules, constraints precises) | Documentation Claude Code-specific (moins precise) |
| Cross-platform (26+ outils) | Documente + logo carousel | Absent |
| Progressive disclosure model | Documente formellement (3 niveaux) | Mentionne implicitement (quiz) |
| `name` constraints | 1-64 chars, lowercase, no `--`, must match dir | "Kebab-case identifier" (vague) |
| `description` constraints | Max 1024 chars, keywords pour matching | "Activation trigger" (vague) |
| `license` field | Documente | Absent |
| `compatibility` field | Documente (max 500 chars) | Absent |
| `metadata` field | Documente (key-value) | Absent |
| `context` field (fork/inherit) | Absent (Claude Code-specific) | Documente |
| `agent` field (specialist/general) | Absent (Claude Code-specific) | Documente |
| skills-ref CLI (validation) | Outil officiel | Absent |
| `<available_skills>` XML format | Documente (pour integration) | Absent |
| anthropics/skills repo | 60.1K stars, skills officiels | 2 lignes (`npx add-skill`) |
| Security (sandboxing, allowlist) | Section dediee | Mentionne dans validation checklist |
| Integration guide (pour devs) | Guide complet (filesystem vs tool-based) | Hors scope (guide utilisateur) |
| Directory structure | `scripts/`, `references/`, `assets/` | `scripts/`, `reference.md`, `checklists/`, `examples/` |

**Observation critique**: Le guide documente 2 champs (`context`, `agent`) qui ne sont PAS dans la spec officielle agentskills.io. Ce sont des extensions Claude Code-specifiques. Cela devrait etre clarifie pour eviter la confusion.

## Recommandations

**Action: Integrer (priorite haute).**

### 1. Ajout d'un bloc "Open Standard" dans Section 5

**Ou**: `guide/ultimate-guide.md` apres ligne ~5133 (apres la structure de dossier)

**Quoi**: Bloc de 15-20 lignes expliquant:
- Agent Skills = standard ouvert (agentskills.io), cree par Anthropic
- 26+ plateformes supportees (les skills sont portables)
- Claude Code implemente la spec + ajoute des extensions (`context`, `agent`)
- Lien vers spec formelle pour reference

### 2. Clarification des champs frontmatter

**Ou**: `guide/ultimate-guide.md` ligne ~5146 (tableau des champs)

**Quoi**:
- Distinguer champs spec officielle (`name`, `description`, `allowed-tools`, `license`, `compatibility`, `metadata`) des extensions Claude Code (`context`, `agent`)
- Ajouter les contraintes precises du `name` (1-64 chars, pas de `--`, doit matcher le repertoire)
- Ajouter `license`, `compatibility`, `metadata` dans le tableau

### 3. Reference anthropics/skills

**Ou**: `guide/ultimate-guide.md` section Skills Marketplace (~ligne 5873)

**Quoi**:
- Mention du repo officiel (60.1K stars) avec les categories de skills
- Plugin install: `/plugin marketplace add anthropics/skills`
- Distinction: skills open source (Apache 2.0) vs document skills (source-available)

### 4. skills-ref dans reference.yaml

**Ou**: `machine-readable/reference.yaml`

**Quoi**: Ajouter entrees pour agentskills.io, anthropics/skills, skills-ref

### 5. Mention progressive disclosure

**Ou**: Existant implicitement, a rendre explicite dans Section 5.1 ou 5.2

**Quoi**: 3 lignes sur le modele metadata-only → full SKILL.md → resources on demand

## Challenge (auto-critique)

### Arguments pour score +1 (5/5):
- Le guide pretend etre LA reference Claude Code. Ne pas mentionner la spec officielle d'une feature couverte sur 800+ lignes est un trou embarrassant.
- 60.1K stars = ce n'est pas un projet de niche. C'est le repo Anthropic le plus populaire.
- L'interoperabilite (skills portables entre 26+ outils) est un argument selling point majeur que le guide rate completement.
- Les champs `context` et `agent` documentes dans le guide ne sont PAS dans la spec officielle - potentielle source de confusion pour les lecteurs.

### Arguments pour score -1 (3/5):
- L'utilisateur Claude Code moyen ne se soucie pas de la spec formelle. Il veut creer un skill qui marche.
- Le guide documente deja bien le workflow pratique.
- agentskills.io est une spec pour les implementeurs d'agents, pas pour les utilisateurs finaux.
- Les 60.1K stars de anthropics/skills sont gonfles par le buzz initial - beaucoup de stargazers passifs.

### Verdict du challenge:
Score 4/5 maintenu. L'argument "spec pour implementeurs" est valide mais le guide documente deja l'architecture interne (guide/architecture.md), les hooks, le MCP protocol - il ne se limite pas au "how-to utilisateur". L'absence de la spec officielle est un gap reel, pas critique pour l'usage quotidien mais significatif pour la completude. L'interoperabilite et anthropics/skills meritent clairement une mention.

### Points manques:
- Le **threat model SafeDep** (safedep.io/agent-skills-threat-model) documente des vulnerabilites dans la spec (8-14% des skills). Angle securite pertinent pour `guide/security-hardening.md`.
- Le blog Anthropic ["Equipping Agents for the Real World"](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) est la source primaire a referencer.
- Claude.ai supporte aussi les skills directement (pas juste Claude Code) - angle cowork potentiel.

### Risques de non-integration:
**Moderes.** Un lecteur decouvrant la spec agentskills.io realiserait que le guide decrit les skills comme une feature Claude Code isolee, alors qu'elles sont cross-plateforme. Perte de credibilite sur la completude.

## Fact-Check

| Affirmation | Verifiee | Source |
|-------------|----------|--------|
| 26+ plateformes (logo carousel) | ✅ | agentskills.io/home (26 logos comptes) |
| 8.2K stars agentskills/agentskills | ✅ | GitHub repo |
| 60.1K stars anthropics/skills | ✅ | GitHub repo |
| Cree par Anthropic | ✅ | agentskills.io ("originally developed by Anthropic") |
| Standard ouvert | ✅ | agentskills.io ("released as an open standard") |
| skills-ref CLI existe | ✅ | GitHub (agentskills/agentskills/skills-ref/) |
| `name` max 64 chars, lowercase | ✅ | agentskills.io/specification |
| `description` max 1024 chars | ✅ | agentskills.io/specification |
| Progressive disclosure 3 niveaux | ✅ | agentskills.io/what-are-skills |
| Claude Code dans les plateformes | ✅ | Logo carousel sur home page |
| `context`/`agent` absents de la spec | ✅ | agentskills.io/specification (non mentionnes) |
| Document skills = source-available | ✅ | anthropics/skills README |
| Plugin install disponible | ✅ | anthropics/skills README |
| SafeDep threat model | ✅ | Perplexity (safedep.io, jan 2026) |
| Anthropic blog post | ✅ | anthropics/skills README (lien) |

**Corrections apportees**: Aucune. Toutes les claims verifiees.

## Decision finale

- **Score final**: 4/5
- **Action**: Integrer (priorite haute, dans la semaine)
- **Confiance**: Haute
- **Scope d'integration**: 5 modifications ciblees (section open standard, frontmatter, anthropics/skills, reference.yaml, progressive disclosure)
- **Effort estime**: Section additionnelle de ~50-80 lignes dans ultimate-guide.md + mises a jour reference.yaml
- **Note**: Cette evaluation rend le gap encore plus visible - le guide traite les skills sur 800+ lignes sans jamais mentionner la spec officielle qui les definit
