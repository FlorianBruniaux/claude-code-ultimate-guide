# PR workflow plugin

Pull request review and preparation.

## Install

From a clone of this repository:

```bash
bash examples/plugins/pr-workflow/install.sh
```

## Components

- **code-reviewer agent**: read-only code quality and security review
- **`/review-pr` skill**: analyze a PR and report findings
- **`/pr` skill**: prepare and open a PR (manual invocation only)
- **`/validate-changes` skill**: check what will be submitted

## Quick start

```bash
/review-pr 123
/pr --draft
/validate-changes
```

These bundles are project-level installers, not plugin packages: the manifest in `.claude-plugin/plugin.json` carries metadata only, and `install.sh` copies the listed components from the sibling `examples/` folders into `.claude/` (existing files are never overwritten). To ship them as a real plugin, copy the components under the plugin root (`skills/<name>/SKILL.md`, `agents/<name>.md`) and run `claude plugin validate`.

## See also

- `guide/workflows/code-review.md`: full review workflow documentation
- `/security-check`: security-specific review (security-suite plugin)
