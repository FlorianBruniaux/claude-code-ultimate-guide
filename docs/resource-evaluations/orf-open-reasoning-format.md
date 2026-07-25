# ORF (Open Reasoning Format) Evaluation

**Resource**: Open Reasoning Format: file-based cross-session memory for AI coding agents
**Source**: [Guillaume Laforge blog, "Open Reasoning Format"](https://glaforge.dev/posts/2026/07/21/open-reasoning-format/) (2026-07-21)
**Repo**: github.com/glaforge (ORF spec + `manage-experience` skill + eval harness)
**Author**: Guillaume Laforge: Developer Advocate, Google Cloud. Co-founder of Apache Groovy, Java Champion.
**License**: open spec (Markdown + YAML), reference CLI in Python
**Evaluated**: 2026-07-25

---

## Score: 3/5 (Moderate)

**Decision**: Integrate as a mention in `guide/core/memory-systems.md` (new file-based experience-playbook entry under §3) plus cite the ReasoningBank paper as the academic anchor for failure-and-success memory. Extract one documented pattern: 3-tier progressive disclosure applied to memory retrieval. Do not recommend the tool for production; it is a well-designed POC the author has not yet used in anger.

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

---

## Scoring Breakdown

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Relevance to CC users | 4/5 | Cross-session agent memory is a live problem; the SKILL.md format is directly CC-compatible. |
| Novelty vs. guide | 4/5 | `memory-systems.md` lists mostly vector/semantic tools (SQLite-vec, ChromaDB). The file-based, no-embedding, Git-committable experience-playbook angle is not covered, and ReasoningBank is cited nowhere. |
| Technical quality | 3/5 | Clean design (progressive disclosure, auto-synced index, strict schema). Reference implementation is a single Python CLI. Very new, author states it is not battle-tested. |
| Evidence quality | 1/5 | Benchmarks are statistical noise (see below), and the author says so plainly. |
| Actionability | 3/5 | Copy one directory, `pip install pyyaml`, done. But no packaging, no consolidation/staleness handling. |

**Overall: 3/5.** High novelty and relevance, dragged down by near-zero evidence and POC maturity.

---

## Patterns Worth Extracting

### Pattern 1: Three-tier progressive disclosure for memory retrieval

Most memory tools inject recalled context in one shot. ORF stages it with an explicit token budget: index (~200) → category frontmatter (~500) → single playbook (~800). The agent only pays for the playbook it actually needs. This is the SKILL.md progressive-disclosure idea applied to a memory index rather than a skill body. Concrete, cheap, and not named as a memory pattern in the guide today.

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
| Entry in `memory-systems.md` §3 (file-based experience track) | Add | Fills a real gap: the no-vector, Git-committable playbook approach. |
| Cite ReasoningBank (arXiv 2509.25140) in §3 or §9 | Add | Academic anchor for success-and-failure memory; currently absent from the guide. |
| Progressive-disclosure-for-retrieval note | Add | Concrete token-budgeted pattern, applied to memory rather than skills. |
| One-paragraph note in §4 (Git-native team sharing) | Add | Partial answer to the structural team gap the guide flags. |
| Recommend the tool for production | Skip | POC maturity, no packaging, unsolved consolidation/staleness. |
| Cite any benchmark number | Skip | Statistically meaningless, author agrees. |
| Entry in `credits.md` | Add | Guillaume Laforge, open spec. |

---

## Files to Modify (on integration)

- `docs/resource-evaluations/orf-open-reasoning-format.md` (this file)
- `docs/resource-evaluations/README.md`: index row
- `guide/core/memory-systems.md`: §3 file-based experience entry + ReasoningBank citation + §4 Git-sharing note + progressive-disclosure pattern
- `guide/core/credits.md`: Guillaume Laforge / ORF entry
- `machine-readable/reference.yaml`: new entries if section added
- `CHANGELOG.md`: [Unreleased] entry
