# Machine-Readable References

Files optimized for LLM/AI consumption. Sizes below are measured, not targets.

## Contents

| File | Description | Size | Est. tokens |
|------|-------------|------|-------------|
| [reference.yaml](./reference.yaml) | Master index: file paths, section anchors and line numbers into `guide/ultimate-guide.md` and the thematic guides. Also holds decision trees, CLI and env reference, permission and MCP config, agent and skill templates, onboarding question flow. | ~260 KB | ~44K |
| [claude-code-releases.yaml](./claude-code-releases.yaml) | Condensed history of official Claude Code releases: per-version highlights, `breaking_summary` grouped by category, `milestones` quick reference. Source of truth for `guide/core/claude-code-releases.md`. | ~123 KB | ~27K |
| [cowork-reference.yaml](./cowork-reference.yaml) | Index for Claude Cowork (Claude Desktop, non-dev audience). Paths resolve against the dedicated [claude-cowork-guide](https://github.com/FlorianBruniaux/claude-cowork-guide) repo, not this one. | ~21 KB | ~5K |
| [agentsec-security-feed.v1.json](./agentsec-security-feed.v1.json) | AgentSec database metadata, detector coverage, security counters, and reviewed incident fiches consumed by the landing. | ~8 KB | ~2K |
| [agent-harnesses.json](./agent-harnesses.json) | Immutable normalized Agent Harness Map: pinned 160-project upstream snapshot, 32 guide supplements, 42 strict runtimes, 15 adjacent control planes, evidence states, and project URLs. | Generated | Generated |
| `agent-harnesses-github.json` | Optional reviewed GitHub observation sidecar: stars, archive state, language, SPDX signal, branch and push timestamp, bound to the catalog checksum. It is not committed until a complete verified collection is promoted. | Volatile | Volatile |
| [agent-harnesses-github.schema.json](./agent-harnesses-github.schema.json) | JSON Schema for the volatile GitHub observation sidecar. | Generated | N/A |
| [agent-harnesses.schema.json](./agent-harnesses.schema.json) | JSON Schema for validating the normalized harness catalog before publication. | Generated | N/A |
| [translations.json](./translations.json) | Dated registry of canonical, project-maintained, and community editions: URLs, maintainers, status, source commits, attribution, coverage, pinned lag, and bilingual publication roots. | ~10 KB | ~3K |
| [distribution-channels.yaml](./distribution-channels.yaml) | JSON-compatible YAML registry for publication channels, attributed URLs, asset states, dates, and 30-day outcome fields. | ~8 KB | ~2K |
| [navigation.json](./navigation.json) | Shared `Start`, `Build`, `Scale`, `Resources`, and `Updates` navigation contract for the repository README and public landing sitemap. Each public route can point back to its canonical repository source. | Generated | <2K |
| [navigation.schema.json](./navigation.schema.json) | JSON Schema for the shared navigation contract. | Generated | N/A |
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
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/translations.json
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/distribution-channels.yaml
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/machine-readable/navigation.json
```

### Public navigation contract

[`navigation.json`](./navigation.json) keeps the repository summary and the public website aligned without turning either one into the source for guide prose. It owns the curated intent groups, public routes, short descriptions, and source paths. The Markdown files remain canonical for their content.

Validate the manifest and the generated block in `README.md`:

```bash
python3 scripts/sync-navigation.py
```

After editing the manifest, regenerate only the marked README block:

```bash
python3 scripts/sync-navigation.py --write
```

The landing build copies the same manifest into its data directory before Astro renders the readable sitemap. Landing-only pages may use `null` for `source_path`. Every non-null source must exist inside this repository, and a declared source anchor must resolve to a heading.

### Translation status

[`translations.json`](./translations.json) distinguishes the canonical English edition, the maintained French edition, and independently maintained community adaptations. A `stale` state is a truthful published status, not a failed build. Incorrect checksums, source ancestry, pinned lag, attribution fields, missing language pairs, or a state that contradicts the evidence do fail the integrity check.

```bash
python3 scripts/check-translations.py --check
python3 scripts/check-translations.py --check --require-current-maintained
```

The MCP package exposes the same registry as `claude-code-guide://translations`.

### Distribution status

[`distribution-channels.yaml`](./distribution-channels.yaml) separates asset production from external publication. A `ready` asset has passed its local checks but has not been submitted or published. Missing measures remain `null`.

```bash
python3 scripts/check-distribution-channels.py
python3 -m unittest scripts/test-check-distribution-channels.py
```

The MCP package exposes the same registry as `claude-code-guide://distribution-channels`.

### Agent harness landscape

Use the human-readable pages according to the question being asked:

| Need | Entry point |
|---|---|
| Runtime architecture, components, controls, Claude Code implementation, and optimizer evaluation protocol | [Agent Harness Engineering](../guide/core/agent-harness.md) |
| Loop contracts, graph contracts, judgment allocation, durability, observability, and control-structure selection | [Loop & Graph Engineering](../guide/core/loop-graph-engineering.md) |
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

The `interfaces` field uses six values: `cli`, `tui`, `ide`, `desktop`, `web`, and `chat`. Upstream `cli`, `tui`, `ide`, and `browser` tags map deterministically to this vocabulary. Curated exceptions require an official, commit-pinned source in `agent-harnesses-overrides.json`. Interface does not encode execution location or loop ownership.

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

### GitHub metadata sidecar

The scheduled `Collect Agent Harness GitHub Metadata` workflow is read-only. It derives the 179 canonical repository URLs from `agent-harnesses.json`, sends sequential GitHub API requests using the pinned `2022-11-28` API version, and uploads a candidate artifact for 14 days. A checksum-keyed Actions cache preserves verified ETags between runs without crossing catalog revisions. It never commits or opens a pull request.

The collector fails closed on a missing token, incomplete result, HTTP error including 404 or 429, rename, duplicate, cardinality mismatch, or catalog checksum mismatch. It writes atomically only after all repositories have passed validation. `license_spdx` is a GitHub observation and never replaces the editorial `license_signal`; the sidecar never changes `freshness.checked_at`.

To collect a candidate locally, write it outside the repository first:

```bash
GITHUB_TOKEN=... python3 scripts/collect-agent-harnesses-github.py \
  --catalog machine-readable/agent-harnesses.json \
  --output /tmp/agent-harnesses-github.json \
  --captured-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

Promotion is a separate human review. First validate the complete sidecar and render it into a temporary page. This checks the recomputed catalog checksum, schema version, exact fields, timestamps, repository identities, cardinality, ordering, and non-negative stars without changing the published page:

```bash
cp guide/ecosystem/agent-harness-landscape.md /tmp/agent-harness-landscape-candidate.md
python3 scripts/build-agent-harness-page.py \
  --catalog machine-readable/agent-harnesses.json \
  --github-sidecar /tmp/agent-harnesses-github.json \
  --page /tmp/agent-harness-landscape-candidate.md
```

After reviewing the metadata diff, copy the candidate to both `machine-readable/agent-harnesses-github.json` and `mcp-server/content/agent-harnesses-github.json`, then verify the byte-for-byte mirror. The page builder can consume the promoted sidecar explicitly while retaining the catalog fallback:

```bash
python3 scripts/build-agent-harness-page.py \
  --catalog machine-readable/agent-harnesses.json \
  --github-sidecar machine-readable/agent-harnesses-github.json \
  --page guide/ecosystem/agent-harness-landscape.md \
  --check
diff -q machine-readable/agent-harnesses-github.json mcp-server/content/agent-harnesses-github.json
```

## Maintenance

`version` and `updated` at the top of `reference.yaml` must track the root `VERSION` file. Run `./scripts/sync-version.sh --check` before committing.

Anchors and line numbers drift when guide files are restructured. After a large edit to `guide/`, verify that every `path#anchor` in `reference.yaml` still resolves to a real heading, and that every `path:N` stays within its file.

Adding, removing or renaming a `deep_dive` key changes the landing site's Cmd+K palette. Rebuild it from the landing repo with `pnpm build:search`.

Changing a public navigation group, route, label, or source path requires `python3 scripts/sync-navigation.py --write` here and a landing build with the current guide repository available through `GUIDE_REPO_PATH` or the default sibling path.

---

*Back to [main README](../README.md)*
