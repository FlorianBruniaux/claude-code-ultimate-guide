# Machine-Readable References

Files optimized for LLM/AI consumption. Sizes below are measured, not targets.

## Contents

| File | Description | Size | Est. tokens |
|------|-------------|------|-------------|
| [reference.yaml](./reference.yaml) | Master index: file paths, section anchors and line numbers into `guide/ultimate-guide.md` and the thematic guides. Also holds decision trees, CLI and env reference, permission and MCP config, agent and skill templates, onboarding question flow. | ~174 KB | ~44K |
| [claude-code-releases.yaml](./claude-code-releases.yaml) | Condensed history of official Claude Code releases: per-version highlights, `breaking_summary` grouped by category, `milestones` quick reference. Source of truth for `guide/core/claude-code-releases.md`. | ~104 KB | ~27K |
| [cowork-reference.yaml](./cowork-reference.yaml) | Index for Claude Cowork (Claude Desktop, non-dev audience). Paths resolve against the dedicated [claude-cowork-guide](https://github.com/FlorianBruniaux/claude-cowork-guide) repo, not this one. | ~21 KB | ~5K |
| [llms.txt](./llms.txt) | Standard LLM context file for repository indexation: topic coverage, entry points, key URLs. | ~4 KB | ~1K |

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
```

## Maintenance

`version` and `updated` at the top of `reference.yaml` must track the root `VERSION` file. Run `./scripts/sync-version.sh --check` before committing.

Anchors and line numbers drift when guide files are restructured. After a large edit to `guide/`, verify that every `path#anchor` in `reference.yaml` still resolves to a real heading, and that every `path:N` stays within its file.

Adding, removing or renaming a `deep_dive` key changes the landing site's Cmd+K palette. Rebuild it from the landing repo with `pnpm build:search`.

---

*Back to [main README](../README.md)*
