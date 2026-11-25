# DevOps pipeline plugin

CI/CD automation, deployment, and infrastructure troubleshooting.

## Install

From a clone of this repository:

```bash
bash examples/plugins/devops-pipeline/install.sh
```

## Components

- **devops-sre agent**: infrastructure troubleshooting with the FIRE framework
- **`/ship` skill**: full release workflow (manual invocation only)
- **`/land-and-deploy` skill**: merge and deploy workflow (manual invocation only)
- **claude-code-review workflow**: copied to `.github/workflows/claude-code-review.yml`

## Quick start

```bash
/ship --dry-run
/land-and-deploy --env staging
```

Review `.github/workflows/claude-code-review.yml` before enabling it in GitHub.

These bundles are project-level installers, not plugin packages: the manifest in `.claude-plugin/plugin.json` carries metadata only, and `install.sh` copies the listed components from the sibling `examples/` folders into `.claude/` (existing files are never overwritten). To ship them as a real plugin, copy the components under the plugin root (`skills/<name>/SKILL.md`, `agents/<name>.md`) and run `claude plugin validate`.

See `guide/ops/devops-sre.md` for full documentation.
