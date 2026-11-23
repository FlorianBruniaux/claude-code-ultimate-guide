# Release automation plugin

Release notes generation from git history.

## Install

From a clone of this repository:

```bash
bash examples/plugins/release-automation/install.sh
```

## Components

- **`/release-notes` skill**: generate notes from commits (manual invocation only)
- **release-notes-generator skill**: three output formats (CHANGELOG, PR body, Slack)

Version bumping, tagging, and a version-sync hook are not part of this bundle. The maintainer commands used for this repository's own releases live in `.claude/commands/` and are repository-specific.

## Quick start

```bash
/release-notes --from v1.0.0 --format md
```

These bundles are project-level installers, not plugin packages: the manifest in `.claude-plugin/plugin.json` carries metadata only, and `install.sh` copies the listed components from the sibling `examples/` folders into `.claude/` (existing files are never overwritten). To ship them as a real plugin, copy the components under the plugin root (`skills/<name>/SKILL.md`, `agents/<name>.md`) and run `claude plugin validate`.

See `guide/workflows/` for version management.
