# Machine-Readable References

Files optimized for LLM/AI consumption. Sizes below are measured, not targets.

## Contents

| File | Description | Size | Est. tokens |
|------|-------------|------|-------------|
| [reference.yaml](./reference.yaml) | Master index: file paths, section anchors and line numbers into `guide/ultimate-guide.md` and the thematic guides. Also holds decision trees, CLI and env reference, permission and MCP config, agent and skill templates, onboarding question flow. | ~260 KB | ~44K |
| [claude-code-releases.yaml](./claude-code-releases.yaml) | Condensed history of official Claude Code releases: per-version highlights, `breaking_summary` grouped by category, `milestones` quick reference. Source of truth for `guide/core/claude-code-releases.md`. | ~123 KB | ~27K |
| [cowork-reference.yaml](./cowork-reference.yaml) | Index for Claude Cowork (Claude Desktop, non-dev audience). Paths resolve against the dedicated [claude-cowork-guide](https://github.com/FlorianBruniaux/claude-cowork-guide) repo, not this one. | ~21 KB | ~5K |
| [agentsec-security-feed.v1.json](./agentsec-security-feed.v1.json) | AgentSec database metadata, detector coverage, security counters, and reviewed incident fiches consumed by the landing. | ~8 KB | ~2K |
| [agent-harnesses.json](./agent-harnesses.json) | Normalized Agent Harness Map: pinned 160-project upstream snapshot, 31 guide supplements, 42 strict runtimes, 14 adjacent control planes, evidence states, project URLs, and dated GitHub metadata. Research harness optimizers remain in the cited guide layer rather than this runtime catalog. | Generated | Generated |
| [agent-harnesses.schema.json](./agent-harnesses.schema.json) | JSON Schema for validating the normalized harness catalog before publication. | Generated | N/A |
| [llms.txt](./llms.txt) | Standard LLM context file for repository indexation: topic coverage, entry points, key URLs. | ~5 KB | ~1K |

`reference.yaml` is a full index, not a summary. Loading it whole costs roughly 44K tokens, so prefer grepping it for the topic you need and following the resulting path or line number, rather than pasting the entire file into context.

Root-level `llms.txt` and `llms-full.txt` cover the same AI-indexation role for crawlers. Keep `machine-readable/llms.txt` and the root `llms.txt` identical.

## Usage

### Look up a topic without loading the whole guide

```bash
# Find where a topic lives, then read only that file or line range
grep -i "memory_systems" machine-readable/reference.yaml
grep -i "hooks_events" machine-readable/reference.yaml
```

### Reference in Claude Code

```
@machine-readable/reference.yaml
```

### Fetch remotely

```bash
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/reference.yaml
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/agent-harnesses.json
```

### Agent harness landscape

Use the human-readable pages according to the question being asked:

| Need | Entry point |
|---|---|
| Runtime architecture, components, controls, Claude Code implementation, and optimizer evaluation protocol | [Agent Harness Engineering](../guide/core/agent-harness.md) |
| Dated cross-product map, classification, selection, test-drive protocol, and meta-harness research layer | [Agent Harness Landscape](../guide/ecosystem/agent-harness-landscape.md) |
| Detailed profiles of selected coding agents | [Agent Tools: Beyond Claude Code](../guide/ecosystem/agentic-tools.md) |
| Runtime, repository, evaluation harness, and orchestrator terminology | [Glossary](../guide/core/glossary.md) |
| Version-level Claude Code behavior | [claude-code-releases.yaml](./claude-code-releases.yaml) |
| Stable topic and section routes | [reference.yaml](./reference.yaml) |

`agent-harnesses.json` is generated from the committed snapshot at `best-of-Agent-Harnesses@ece314654d2c23fe7bd69fc6ef7088f093207e49` and curated manual overrides. The raw source is verified against `best-of-agent-harnesses-ece314654d2c.manifest.json` and SHA-256 `4c02e547e11b056aa4d7e519305b7f4ca4f02550c27018d70757a59d26ace65f` before parsing. The upstream-derived records retain the source's CC-BY-SA-4.0 attribution and its 2026-08-23 star snapshot.

The file keeps four sets separate:

- `upstream_snapshot`: the 160 source projects across 12 categories;
- `guide_supplement`: official products and reviewed repositories absent from that snapshot;
- `strict_runtime_map`: projects whose evidence says they own an agent loop;
- `adjacent_control_planes`: wrappers, fleet managers, task controllers, and execution layers that call another runtime.

Evidence uses `confirmed`, `claimed`, `unknown`, or `not_applicable`. `unknown` does not mean the feature is absent. `owns_loop` uses `confirmed`, `claimed`, `unknown`, or `no`. The extractor never launches an agent or sends README text to a model. It emits deterministic `unknown` proposals for manual review. External proposals remain review input and are never published automatically.

Each extraction proposal binds its input to the canonical GitHub repository URL, the repository-relative README path, and the SHA-256 of the bytes actually read. Raw README content and local filesystem paths are not copied into the proposal.

Rebuild and verify without network access:

```bash
python3 scripts/build-agent-harnesses.py \
  --source machine-readable/sources/best-of-agent-harnesses-ece314654d2c.json \
  --overrides machine-readable/agent-harnesses-overrides.json \
  --output machine-readable/agent-harnesses.json
python3 scripts/build-agent-harnesses.py \
  --source machine-readable/sources/best-of-agent-harnesses-ece314654d2c.json \
  --overrides machine-readable/agent-harnesses-overrides.json \
  --output machine-readable/agent-harnesses.json \
  --check
uv run --offline --with jsonschema python scripts/test-agent-harnesses.py
```

The `uv` test command is the required validation gate. It always loads `jsonschema` and checks both the committed catalog and hostile schema witnesses; the runner exits immediately if `jsonschema` is unavailable.

Refresh the upstream source deliberately with `scripts/collect-agent-harnesses.py`. The collector rejects any initial snapshot that no longer has exactly 160 projects, 12 categories, and the required licence. A new upstream commit requires a reviewed contract update rather than a silent count change.

## Maintenance

`version` and `updated` at the top of `reference.yaml` must track the root `VERSION` file. Run `./scripts/sync-version.sh --check` before committing.

Anchors and line numbers drift when guide files are restructured. After a large edit to `guide/`, verify that every `path#anchor` in `reference.yaml` still resolves to a real heading, and that every `path:N` stays within its file.

Adding, removing or renaming a `deep_dive` key changes the landing site's Cmd+K palette. Rebuild it from the landing repo with `pnpm build:search`.

---

*Back to [main README](../README.md)*
