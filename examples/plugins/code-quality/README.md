# Code quality suite plugin

Refactoring, performance optimization, and design-pattern guidance.

## Install

From a clone of this repository:

```bash
bash examples/plugins/code-quality/install.sh
```

## Components

- **refactoring-specialist agent**: SOLID-focused refactoring in an isolated context
- **`/refactor` skill**: safe refactoring with validation
- **`/optimize` skill**: performance optimization
- **`/design-patterns` skill**: design pattern suggestions
- **`/audit-codebase` skill**: codebase quality audit

The two skills that change code or run long analyses (`/refactor`, `/audit-codebase`) set `disable-model-invocation: true`, so Claude runs them only when you type the command.

## Quick start

```bash
/refactor src/auth/
/audit-codebase src/ --focus quality
```

These bundles are project-level installers, not plugin packages: the manifest in `.claude-plugin/plugin.json` carries metadata only, and `install.sh` copies the listed components from the sibling `examples/` folders into `.claude/` (existing files are never overwritten). To ship them as a real plugin, copy the components under the plugin root (`skills/<name>/SKILL.md`, `agents/<name>.md`) and run `claude plugin validate`.

See `guide/workflows/` for methodology documentation.
