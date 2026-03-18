# Resource Evaluation #073 — Athena Flow: Hook-Based Workflow Runtime for Claude Code

**Source:** [athenaflow.in](https://athenaflow.in) / [github.com/lespaceman/athena-flow](https://github.com/lespaceman/athena-flow)
**Type:** Open source tool (MIT) — workflow runtime wrapping Claude Code via hooks
**Author:** Nadeem M (@lespaceman)
**Evaluated:** 2026-03-05
**Maturity at evaluation:** Published ~same day (LinkedIn post + GitHub, hours old)

---

## Résumé du contenu

- **Workflow runtime for Claude Code**: wraps it via hooks, routes events through a Unix Domain Socket (NDJSON) to a persistent Node.js runtime
- **Architecture**: Claude Code → hook-forwarder (stdin) → UDS → athena-flow runtime → TUI
- **TUI (terminal UI)**: real-time observability of tools, permissions, results, errors; SQLite session persistence; keyboard-driven with color themes
- **Plugin system**: supports commands, hooks, MCP servers, agents; isolation presets (strict/minimal/permissive)
- **First workflow**: autonomous E2E test builder — navigates app like a human, generates structured test cases, produces Playwright CI-ready TypeScript
- **Claimed**: self-healing selectors at 94% success rate (~3s repair time) — unverified, no benchmark in repo
- **Installation**: `npm install -g athena-flow-cli` (Node.js 20+)
- **Roadmap**: visual regression, API testing, Codex support (agent-agnostic positioning)
- **Comparable project discovered via Perplexity**: [Ruflo](https://github.com/ruvnet/ruflo) — multi-agent orchestration platform for Claude Code, a few weeks older and more mature

---

## Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel — Gap majeur dans le guide |
| 4 | Tres pertinent — Amelioration significative |
| 3 | Pertinent — Complement utile |
| **2** | **Marginal — Watch: trop recent, claims non verifies** |
| 1 | Hors scope — Non pertinent |

**Score final: 2/5 (Watch)**

**Justification:** Le pattern "hook-based workflow runtime" est architecturalement distinct de MCP (qui ajoute des outils), des agents (qui delegent des taches), et des hooks basiques. C'est une categorie nouvelle dans l'ecosysteme Claude Code, pas encore documentee dans le guide. La valeur conceptuelle est reelle. Mais a l'evaluation, le projet a quelques heures d'existence: aucune traction mesurable, le claim "94% self-healing selectors" n'a aucune methodologie publiee dans le repo, et l'audit source npm est absent (risque supply chain non evalue). Score 2 maintenu jusqu'a verification de maturite minimale.

---

## Comparatif

| Aspect | Athena Flow | Notre guide |
|--------|-------------|-------------|
| Hook-based workflow runtime (IPC/UDS) | Nouveau pattern non couvert | Absent de third-party-tools.md |
| TUI observabilite Claude Code | Premiere mention de ce pattern | Absent |
| E2E test builder Playwright | Premier dans cette categorie | Playwright MCP couvert (ligne ~11367), pas de generation autonome |
| Plugin/workflow orchestration via hooks | Nouveau pattern | Plugins documentes, pas d'orchestrateur externe |
| Self-healing selectors | Claim 94% non verifie | N/A |
| Maturite / adoption | Heures d'existence | N/A |
| Audit securite (npm install -g) | Non effectue | Guide recommande audit avant install global |

---

## Recommandations

**Action: Watch — Ne pas integrer maintenant, revisiter dans 3-4 semaines**

Ce qui debloquerait une integration a 3/5:
1. **Source audit**: inspecter `athena-flow-cli` sur npm (meme methodologie que Straude: `npm pack`, lire le code compile, verifier l'architecture declaree)
2. **GitHub metrics**: stars, CI actif, issues ouvertes, derniere release stable
3. **94% claim**: soit retire de la doc, soit documente avec une methodologie reproductible
4. **Ruflo comparaison**: evaluer Ruflo (github.com/ruvnet/ruflo) en parallele — plus mature, meme categorie. L'entree du guide devrait couvrir la *categorie* (hook-based runtime), pas juste un outil

Si integration future: creer une section **"Hook-Based Workflow Runtimes"** dans `guide/third-party-tools.md` — categorie inexistante aujourd'hui qui accueillerait Athena Flow + Ruflo + futurs outils du meme type.

**Ne pas faire:**
- Citer le "94% success rate" sans source verifiable
- Recommander `npm install -g athena-flow-cli` sans audit source prealable (voir section securite du guide)
- Integrer une entree outil unique sans la categorie parente

---

## Challenge (technical-writer)

**Score propose initial:** 3/5
**Score apres challenge:** 2/5 (abaisse)

Points souleves par l'agent:

**Pourquoi 3/5 etait trop genereux:**
- Projet de quelques heures = abandonment risk eleve. Roadmap ambitieuse (visual regression, API testing, Codex) sur base d'un seul workflow livre
- `npm install -g` recommande sans audit source = contradiction avec la section securite du guide (ref: snyk-toxicskills-evaluation.md)
- "94% success rate" sans benchmark = erreur factuelle par association si le chiffre entre dans le guide
- Precedent: Rippletide (eval 072) score 2/5 pour "claims non verifiables, pas de traction" — Athena Flow cumule les deux

**Ce qui justifie de ne pas descendre a 1/5:**
- Pattern architecturale genuinement nouveau dans l'ecosysteme (hooks → IPC → runtime persistant)
- Categorie absente du guide = gap reel si le pattern se generalise
- Ruflo confirme que la categorie existe et a de la demande

**Risque de ne pas integrer:** negligeable a court terme. Moyen terme: si Ruflo + Athena Flow + d'autres outils emergent, le guide sera en retard sur une categorie entiere. Surveiller activement.

---

## Fact-Check

| Affirmation | Verifiee | Source |
|-------------|----------|--------|
| Open source MIT | Claimed, non verifie | LinkedIn post (LICENSE file non inspecte) |
| `npm install -g athena-flow-cli` | Vraisemblable | README (non audite) |
| Architecture hooks → UDS → NDJSON | Vraisemblable | README decrit le data flow explicitement |
| TUI avec SQLite session persistence | Vraisemblable | README (feature list) |
| Playwright output CI-ready | Vraisemblable | README + landing site |
| "94% self-healing selector success rate" | Non verifiable | Claim marketing, aucun benchmark dans repo |
| "~3 secondes repair time" | Non verifiable | Idem |
| Codex support "in progress" | Claim roadmap | LinkedIn post, aucun commit visible |
| Free / $0 | Vraisemblable | Landing site + MIT license |
| Ruflo comme projet comparable | Confirme | Perplexity search (github.com/ruvnet/ruflo) |

**Corrections apportees:** Le claim "94%" n'entre pas dans le guide. La mention MIT est en attente de verification du LICENSE file.

---

## Contexte ecosysteme (Perplexity, 2026-03-05)

Projets similaires identifies dans la meme categorie "hook-based runtime / orchestration wrapper":

| Projet | Description | Maturite |
|--------|-------------|----------|
| **[Ruflo](https://github.com/ruvnet/ruflo)** | Multi-agent orchestration platform for Claude Code, governance layer | Quelques semaines, plus mature |
| **Entire CLI** | Gouvernance sequentielle, approval gates, audit trails (SOC2/HIPAA) | ~1 mois, documente dans le guide |
| **oh-my-pi** | Runtime agent terminal alternatif, decouvre hooks/MCP/rules nativement | Recent |

La categorie emerge. Athena Flow n'est pas isole — c'est un signal de tendance.

---

## Decision finale

- **Score final**: 2/5
- **Action**: Watch — revisiter dans 3-4 semaines avec: audit npm source, GitHub metrics, verification claim 94%
- **Confiance**: Haute sur le score, moyenne sur les facts (projet trop recent pour audit complet)
- **Prochaine action**: Evaluer Ruflo (#074) en parallele pour avoir la comparaison de categorie complete avant toute integration