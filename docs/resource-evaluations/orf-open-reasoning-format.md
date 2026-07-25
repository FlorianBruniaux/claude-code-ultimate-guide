# ORF (Open Reasoning Format) Evaluation

**Resource**: Open Reasoning Format: file-based cross-session memory for AI coding agents
**Source**: [Guillaume Laforge blog, "Open Reasoning Format"](https://glaforge.dev/posts/2026/07/21/open-reasoning-format/) (2026-07-21)
**Repo**: github.com/glaforge (ORF spec + `manage-experience` skill + eval harness)
**Author**: Guillaume Laforge: Developer Advocate, Google Cloud. Co-founder of Apache Groovy, Java Champion.
**License**: open spec (Markdown + YAML), reference CLI in Python
**Evaluated**: 2026-07-25

---

## Score: 2/5 (Marginal)

**Note (post-challenge revision)**: initial score was 3/5. A skeptical review found the novelty was overstated. `memory-systems.md` §3.1 already documents 3-layer progressive disclosure (claude-mem), and §2.2-2.3 (Auto Memory + Auto Dream) is already a native file-based, no-vector, index-and-prune memory system. So most of what looked novel is covered. Revised down to 2/5.

**Decision**: Minimal mention only. The one genuinely valuable, verified recommendation is independent of ORF: cite the ReasoningBank paper (arXiv 2509.25140) in `memory-systems.md`, since `grep -rli "reasoningbank" guide/` returns zero hits and it is the academic anchor for success-and-failure agent memory. Optionally add a one-paragraph note in §4 on git-committable experience playbooks as a team-sharing path. Do not add a tool entry, do not recommend for production (self-described not-battle-tested POC), cite no benchmark numbers.

---

## What It Is

ORF lets a coding agent record and reload operational learnings across sessions. When an agent resolves a tricky problem, it writes a "playbook" as a Markdown file with YAML frontmatter under `./experiences/`. The next session, an agent facing a similar task retrieves the playbook and skips the dead ends it already paid for once.

Three components:

1. `experiences/INDEX.md`: root catalog. YAML frontmatter defines domain categories; the Markdown body links each playbook with a one-line summary. The helper script auto-appends new entries, so the index stays synced without manual editing.
2. `experiences/<domain>/EXP-<date>-<seq>.md`: one playbook per file, strict 5-section schema (Objective, The Trap, Abstracted Insight, Validated Path, Verification Checklist).
3. `manage-experience/`: an Agent Skill (SKILL.md format) backed by `experiences.py`, a reference Python CLI with `list-categories`, `get-frontmatter`, `read-experience`, and `create-experience`.

Two hard design constraints:

- **Zero server infrastructure.** No vector DB, no embedding API, no sidecar. Just plain files that commit to version control.
- **On-demand loading via progressive disclosure.** Three steps: read the small index (~200 tokens), inspect the frontmatter descriptions of playbooks in the relevant category (~500 tokens), load only the specific matching playbook (~800 tokens).

---

## Foundations (verified)

| Cited source | Status | What ORF takes from it |
|--------------|--------|------------------------|
| **ReasoningBank** (Google, arXiv 2509.25140) | Real, credible. "Scaling Agent Self-Evolving with Reasoning Memory" | The core idea: distill generalizable strategies from *both* successful and failed trajectories into structured memory items, retrieve a few at test time. |
| Open Knowledge Format (OKF) | Community format | Human-readable Markdown + YAML frontmatter. |
| Agent Skills (SKILL.md) | Anthropic spec, documented in this guide | The `manage-experience` skill loads on demand so the base prompt stays clean. |
| Antigravity trajectory analysis | Author's earlier work | The motivation: spot wasted steps in agent trajectories. |

**The key design divergence from ReasoningBank.** ReasoningBank retrieves memory items via embedding search (vector similarity). ORF deliberately drops embeddings and retrieves by filename plus frontmatter descriptions read by the LLM. That is the whole bet: trade semantic-vector recall for zero infrastructure and Git-committable files. The cost is retrieval quality. An LLM scanning one-line descriptions will miss matches a vector index would catch, and the author himself flags this in his open questions ("experiences too specific won't trigger for other cases").

**Closest analogs already in the guide (added post-challenge).** Two existing entries are structurally closer to ORF than the sources ORF itself cites, and both matter for the novelty call:

- **claude-mem (§3.1)** already documents *"Progressive disclosure (3 layers to save tokens)"* with the same index → mid → full staging and token budget. ORF applies it to playbook files instead of session summaries, but the pattern is not new to the guide.
- **Auto Memory + Auto Dream (§2.2-2.3)** is Claude Code's *native* file-based, no-vector, agent-authored memory with a consolidate/prune/index cycle. That is the same "plain files, no embeddings" shape ORF pitches as its differentiator.

What is left as genuinely new, once those are subtracted: git-committable, per-domain, agent-authored experience playbooks with a fixed 5-section failure/fix schema, shared across a team by `git commit experiences/`. That narrow claim is real (Auto Memory is gitignored/per-user, claude-mem is SQLite not versionable files), but it is narrower than "progressive disclosure for memory," which was already covered.

---

## Scoring Breakdown

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Relevance to CC users | 4/5 | Cross-session agent memory is a live problem; the SKILL.md format is directly CC-compatible. |
| Novelty vs. guide | 2/5 | Progressive disclosure for memory is already in §3.1 (claude-mem); native file-based no-vector memory is already in §2.2-2.3 (Auto Memory/Auto Dream). Only the git-committable per-domain 5-section playbook, and the missing ReasoningBank citation, are new. |
| Technical quality | 3/5 | Clean design (progressive disclosure, auto-synced index, strict schema). Reference implementation is a single Python CLI. Very new, author states it is not battle-tested. |
| Evidence quality | 1/5 | Benchmarks are statistical noise (see below), and the author says so plainly. |
| Actionability | 3/5 | Copy one directory, `pip install pyyaml`, done. But no packaging, no consolidation/staleness handling. |

**Overall: 2/5.** Recomputed after the novelty correction: (4+2+3+1+3)/5 = 2.6, rounds to 2. Real relevance, but low novelty against existing guide coverage and near-zero evidence. Matches the README grid's "Marginal, minimal mention or skip".

---

## Patterns Worth Extracting

### Pattern 1: Three-tier progressive disclosure for memory retrieval (already in the guide)

ORF stages retrieval with an explicit token budget: index (~200) → category frontmatter (~500) → single playbook (~800). **Correction after challenge**: this is not new to the guide. `memory-systems.md` §3.1 already documents claude-mem's *"Progressive disclosure (3 layers to save tokens)"* with the same staging (search 50-100 tokens → timeline 500-1000 → full detail). ORF applies it to playbook files rather than session summaries. Nothing to extract; the pattern is covered.

### Pattern 2: Separate the abstract insight from the validated concrete path

The 5-section schema splits "Abstracted Insight" (the reusable principle, e.g. "anchor YAML frontmatter regex to line starts") from "Validated Path" (the concrete fix that worked here). This mirrors ReasoningBank's strategy-level distillation. It is the mechanism meant to fight the over-specific-experience problem: store the principle, not just the one-off fix. Whether it works in practice is unproven, but the schema decision is sound.

### Pattern 3: Auto-synced index on write

`create-experience` appends to `INDEX.md` under the matching category automatically. The index can never drift from the playbook files because writing a playbook writes the index entry in the same operation. Small, but it removes a whole class of stale-index bugs.

---

## Where It Fits the Team Gap

`memory-systems.md` §4.7 argues the team-sharing gap is structural because every leading tool was built single-user-first and depends on per-user infrastructure. ORF is a partial counter-example worth naming: because playbooks are plain files with no server, `git commit experiences/` shares one developer's agent fix with the whole team automatically. It does not solve consolidation or conflict resolution across contributors (the author lists both as open questions), but the distribution mechanism is exactly the Git-native path the guide says is missing. This belongs as a one-paragraph note in §4, not a full section.

---

## Weaknesses (be honest)

- **Benchmarks are meaningless as stated.** SWE-bench Lite "66.7% → 100%" is 3 tasks; one flipped. The "-52% steps" figure is a single scenario (frontmatter-parser). The author explicitly writes "by no means a scientific evaluation... a handful of cases." Read it as a demo, not proof. Cite no numbers from it.
- **Retrieval without embeddings is the unproven core.** The whole zero-infra pitch rests on an LLM reliably matching a task to a one-line description. No evaluation of retrieval precision or recall exists.
- **Open problems are the hard ones, all unsolved.** Consolidation of overlapping or conflicting playbooks, staleness as frameworks evolve, team distribution beyond raw Git. The author names all three and solves none.
- **Not used in production.** "I haven't used the ORF skill in anger yet." Self-reported.

---

## Integration Decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| Cite ReasoningBank (arXiv 2509.25140) in §9 or §10 | **Add (the one real win)** | Verified gap: `grep -rli "reasoningbank" guide/` returns zero. Academic anchor for success-and-failure memory. Valuable independent of ORF. |
| One-paragraph note in §4 (Git-committable playbooks for team sharing) | Add (optional) | Narrow but real: files commit to Git, a partial answer to the §4.7 structural team gap. Name ORF as the example. |
| Full tool entry in `memory-systems.md` §3 | **Skip** | §3 already lists 8+ tools; ORF's core (progressive disclosure, file-based no-vector) is already covered by claude-mem §3.1 and Auto Memory §2.2-2.3. Catalog bloat. |
| Progressive-disclosure-for-retrieval "new pattern" | **Skip** | Already documented in §3.1. The original eval was wrong to call it novel. |
| Recommend the tool for production | Skip | POC maturity, no packaging, unsolved consolidation/staleness, not used in anger. |
| Cite any benchmark number | Skip | Statistically meaningless, author agrees. |
| Entry in `credits.md` | Add (only if the §4 note lands) | Guillaume Laforge, open spec. |

---

## Files to Modify (on integration)

Reduced scope after the 2/5 revision:

- `docs/resource-evaluations/orf-open-reasoning-format.md` (this file)
- `docs/resource-evaluations/README.md`: index row (2/5, minimal mention)
- `guide/core/memory-systems.md`: ReasoningBank citation (the real win) + optional one-paragraph §4 note on git-committable playbooks. No new §3 tool entry.
- `guide/core/credits.md`: only if the §4 note lands
- `CHANGELOG.md`: [Unreleased] entry
