# Resource Evaluation #074 — Ruflo: Multi-Agent Orchestration Platform for Claude Code

**Source:** [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)
**npm package:** `claude-flow` (ancien nom du projet, npm non encore migre)
**Type:** Open source (MIT) — framework d'orchestration multi-agent pour Claude Code
**Author:** ruvnet
**Evaluated:** 2026-03-05
**Traction:** 18,839 stars, 2,096 forks, 452 PRs, 5,900+ commits

---

## Contexte important

Ruflo etait precedemment connu sous le nom **claude-flow** (github.com/ruvnet/claude-flow). Le rebrand recient est une information structurelle a noter: le package npm reste `claude-flow`, l'URL d'install curl pointe encore sur l'ancien repo. Surveiller la stabilite de la transition.

---

## Resume du contenu

- **Multi-agent orchestration framework**: transforme Claude Code en plateforme multi-agent avec reine + workers hierarchiques, mesh topologies, ou swarms
- **Architecture en couches**: CLI + MCP server → Q-Learning router → Mixture of Experts (8) → 60+ agents specialises (coders, testers, reviewers, architects, security auditors...)
- **42+ skills, 17 hooks** integres
- **RuVector**: composant WebAssembly, HNSW vector search, SONA self-optimization, 9 algorithmes de reinforcement learning
- **SQLite persistence** (AgentDB, WAL mode) + 8 types de memoire incluant partage cross-agent
- **Installation**: `npx ruflo@latest init --wizard` (voie recommandee) ou `curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/claude-flow@main/scripts/install.sh | bash` (voie a eviter)
- **Claims de performance** (voir section Fact-Check):
  - 84.8% SWE-Bench solve rate
  - 32.3% reduction de tokens
  - 2.8-4.4x speedup en coordination parallele
  - 352x WASM transforms vs LLM calls
  - 16,400 vector queries/seconde
  - SONA self-optimization <0.05ms

---

## Score de pertinence

| Score | Signification |
|-------|---------------|
| 5 | Essentiel — Gap majeur dans le guide |
| 4 | Tres pertinent — Amelioration significative |
| **3** | **Pertinent — Complement utile** |
| 2 | Marginal — Watch: trop recent, claims non verifies |
| 1 | Hors scope — Non pertinent |

**Score final: 3/5**

**Justification:** 18.9k stars est un signal d'adoption reel pour un outil de niche. Le guide couvre l'orchestration multi-agent native (Task tool, TeammateTool) mais pas les frameworks externes qui remplacent/augmentent cette couche. Gap reel, categorie absente de `guide/third-party-tools.md`. Score abaisse de 4 a 3 suite au challenge: curl|bash install depuis CDN non audite, claims de performance non verifiables, rebrand recent = instabilite potentielle.

---

## Comparatif

| Aspect | Ruflo | Notre guide |
|--------|-------|-------------|
| Orchestration multi-agent native | Architecture supplementaire | Couvre Task tool + TeammateTool nativement |
| Framework externe d'orchestration | Nouveau pattern | Absent de third-party-tools.md |
| Hooks integration Claude Code | 17 hooks integres | Section hooks couverte, pas d'orchestrateur externe |
| MCP server integration | Oui, TypeScript | MCP documente extensivement |
| Performance claims verifiables | Non (voir fact-check) | Stats documentees avec sources |
| Audit securite install | Non effectue | Guide recommande audit avant install |
| Adoption / communaute | 18.9k stars, #42 repos AI | Oui pour les outils recommandes |

---

## Recommandations

**Action: Integrer a moyen terme — apres source audit et clarification claims**

**Ou integrer**: `guide/third-party-tools.md` section "Multi-Agent Orchestration" — pas en entree outil seule, mais comme exemple primaire d'une nouvelle sous-categorie **"External Orchestration Frameworks"** distincte des outils multi-instance actuels (Gas Town, multiclaude).

La distinction est importante: Gas Town / multiclaude = lancer plusieurs Claude Code en parallele. Ruflo = remplacer/augmenter l'orchestration interne de Claude Code avec un framework complet. Ce sont deux niveaux architecturaux differents.

**Ce qui doit se passer avant integration:**

1. **Source audit `npx ruflo@latest`** via `npm pack ruflo` — verifier absence de preinstall scripts malveillants, confirmer que le package correspond a ce que le README decrit
2. **Clarifier le rebrand**: confirmer que `ruvnet/ruflo` est bien le repo actif et que claude-flow est archive ou redirige
3. **Baliser tous les claims** comme "claim auteur, non verifie" — aucun chiffre (84.8%, 352x, 16,400/s) ne peut entrer dans le guide sans methodologie publiee
4. **Exclure la voie curl|bash** des recommandations (voir section securite)

**Framing correct pour l'entree guide:**
> Ruflo (anciennement claude-flow) est le framework d'orchestration externe le plus adopte pour Claude Code (18.9k stars). Il ajoute une couche multi-agent complete au-dessus de Claude Code: 60+ agents specialises, routing Q-learning, persistance SQLite. A utiliser quand les capacites natives de Claude Code (Task tool, sous-agents) ne suffisent pas pour un use case.

---

## Challenge (technical-writer)

**Score propose initial:** 4/5
**Score apres challenge:** 3/5 (abaisse)

Points cles de l'agent:

**Pourquoi 4/5 etait trop genereux:**
- 18.9k stars avec 830 en un jour = spike de trending, pas adoption soutenue. Besoin de 3-4 semaines de donnees post-spike pour valider la retention
- Rebrand claude-flow → ruflo = evenement non trivial. L'URL curl|bash pointe encore sur l'ancien repo (`ruvnet/claude-flow`) — inconcistance qui indique une transition en cours
- 84.8% SWE-Bench serait SOTA batant les labs fermees. Claim non credible sans paper + reproductibilite. Les autres chiffres (352x, 32.3%, <0.05ms) ont une precision artificielle sans source
- "Byzantine fault tolerance + CRDT" dans un outil pour dev individuels = "architectural theater" (citation agent) si non documente en profondeur

**Pourquoi 3/5 et pas 2:**
- Gap reel dans le guide: la categorie "external orchestration framework" n'existe pas
- Traction verifiee independamment (Perplexity: trending #42 AI repos, communaute chinoise active)
- TypeScript, MIT, npm disponible = plus auditable qu'un projet sans package manager

**Risques de recommander:**
- Complexite elevee: un user qui saute a 60 agents + Q-learning avant de maitriser le Task tool natif prend le mauvais chemin
- Rebrand instable: les conventions de nommage (claude-flow vs ruflo) peuvent changer encore
- Claims agressifs: 84.8% SWE-Bench si cite sans disclaimer emprunte la credibilite du guide

---

## Fact-Check

| Affirmation | Verifiee | Source |
|-------------|----------|--------|
| 18,839 GitHub stars | Confirme | Perplexity (ranktracking #42 AI repos, 2026-03-05) |
| 2,096 forks, 452 PRs | Confirme | Perplexity cross-reference |
| Trending: +830 stars le 3 mars 2026 | Confirme | GitHub ranking chinois (juejin.cn) |
| MIT license | Vraisemblable | README (non inspecte directement) |
| npm package `claude-flow` | Confirme | npmjs.com/package/claude-flow |
| Architecture 60+ agents, 42+ skills, 17 hooks | Vraisemblable | README (non audite) |
| `npx ruflo@latest` disponible | A verifier | npm registry non confirme |
| 84.8% SWE-Bench solve rate | Non verifiable | Claim sans methodologie ni paper |
| 32.3% token reduction | Non verifiable | Precision artificielle, pas de source |
| 352x WASM vs LLM calls | Non verifiable | Baseline de comparaison inconnue |
| 16,400 vector queries/seconde | Non verifiable | Hardware/dataset non specifies |
| SONA <0.05ms adaptation | Non verifiable | Claim marketing |
| Curl CDN pointe sur ancien repo (claude-flow) | Confirme | URL: `cdn.jsdelivr.net/gh/ruvnet/claude-flow` |

**Corrections apportees:** Aucun des chiffres de performance n'entre dans le guide. Rebrand flagge explicitement.

---

## Decision finale

- **Score final**: 3/5
- **Action**: Integrer dans 2-3 semaines, apres source audit et validation post-rebrand
- **Confiance**: Haute sur le score (traction verifiee, claims non verifiables clairement separes), moyenne sur la stabilite du projet (rebrand en cours)
- **Prochaine action**: `npm pack ruflo` ou `npm pack claude-flow` pour identifier le bon package, inspecter le code compile, confirmer absence de preinstall scripts
- **Entree liee**: eval #073 (Athena Flow) — creer section "Hook-Based Runtimes / External Orchestration" dans third-party-tools.md une fois les deux valides