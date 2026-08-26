# BM25 Skill Router for Codex and Claude Code

This `UserPromptSubmit` hook ranks active skills against curated examples with Okapi BM25. It supports one global Codex installation that discovers both project and user skills from the prompt's `cwd`.

The hook is advisory. It emits `additionalContext` only. It never invokes a skill or approves an action.

## What changed from the first example

The original implementation was project-only and Claude-specific. It also routed `conflict` corpora, treated any negation as an opt-out, displayed a score share as a confidence percentage, and missed some cache invalidations.

This version:

- discovers `.agents/skills` from `cwd` to the Git root;
- then discovers `~/.agents/skills`, `~/.codex/skills`, `/etc/codex/skills`, and `SKILL_ROUTER_EXTRA_ROOTS`;
- lets the nearest project skill shadow a global skill with the same `name`;
- routes only calibrated `status: ok` corpora for active skills;
- stores every cache and optional log outside repositories;
- detects additions, edits, and deletions with an algorithm-versioned SHA-256 fingerprint;
- serializes rebuilds with an expiring lock and writes cache files atomically;
- emits `$skill-name` for Codex and `/skill-name` for Claude Code;
- never logs the raw prompt.

Skills without a valid corpus remain available through native Codex skill matching. The manifest labels them `native-only`.

## Requirements

- Node.js 18 or newer
- no npm dependencies
- a Codex or Claude Code `UserPromptSubmit` hook

## Recommended Codex installation

Preview every destination, checksum, and hook change:

```bash
node install.js --host codex --scope user --dry-run
```

Install after reviewing the preview:

```bash
node install.js --host codex --scope user --apply
```

The installer copies the runtime to `~/.codex/hooks/skill-router/`, stores caches separately in `~/.codex/skill-router-data/`, preserves existing handlers in `~/.codex/hooks.json`, and creates a timestamped backup before replacing anything. A second identical installation makes no changes. Keeping cache data outside the runtime directory also preserves it across router upgrades.

Codex requires non-managed hooks to be reviewed and trusted. Open `/hooks`, inspect the installed command and approve its hash. Until that human step is complete, the files can exist while the hook remains inactive.

Do not also install a project BM25 hook on the same machine. Codex combines matching global and project hooks, so two handlers can inject duplicate context. The global hook already discovers project skills.

## Project-only installation

For a machine without the global router:

```bash
node install.js \
  --host codex \
  --scope project \
  --project-root /absolute/path/to/repo \
  --dry-run
```

Replace `--dry-run` with `--apply` after review. The runtime is installed under `<repo>/.codex/hooks/skill-router/` and uses the same discovery and cache logic. The generated hook sets `SKILL_ROUTER_DATA_DIR` to `~/.codex/skill-router-data`, so prompts never write cache files into the repository.

Claude Code project mode uses `--host claude --scope project`. The hint syntax changes to `/skill-name`. Do not activate both a global Codex router and a project Codex router.

## Corpus format

An adjacent corpus lives at `<skill>/evals/scenarios.json`:

```json
{
  "skill": "my-skill",
  "positive": [
    "run the linter on this file",
    "check code style"
  ],
  "negative": [
    "review this PR for security",
    "deploy the application"
  ]
}
```

The `skill` value must equal the active `name` in `SKILL.md` and match `^[a-z0-9][a-z0-9:_-]{0,127}$`. Calibration requires at least eight positive and two contrastive negative examples.

Use `SKILL_ROUTER_OVERLAY_ROOTS` for a skill whose directory cannot contain `evals/`. The bundled `agentic-project-finder` corpus demonstrates this. An overlay is accepted only when its skill is active in one of the resolved roots.

## Build and inspect

Build the cache for a specific working directory:

```bash
SKILL_ROUTER_CWD=/absolute/path/to/repo \
node routing/build-index.js
```

Inspect without writing:

```bash
SKILL_ROUTER_CWD=/absolute/path/to/repo \
node routing/build-index.js --dry-run
```

Generated files per scope:

- `index.json`: tokenized positive and contrastive negative scenarios;
- `thresholds.json`: calibrated thresholds and `ok`, `conflict`, or `excluded` status;
- `manifest.json`: resolved roots, active skills, paths, coverage, exclusions, and source fingerprint;
- `coverage.json`: `covered`, cross-skill `eligible`, and `native-only` skills;
- `metrics.json`: initial and gated leave-one-out quality, removals, and global F1;
- `verified.json`: timestamp of the last deep source verification.

Only `ok` skills that also pass cross-skill evaluation can appear in a BM25 hint. If the eligible set remains below global F1 0.70, the lowest-quality project corpus stays `native-only`. Acceptance-validated overlay skills are retained while noisy project corpora are removed. `conflict`, `excluded`, malformed, inactive, and `native-only` skills remain silent.

## Evaluation

The acceptance file is independent from the training corpus:

```bash
SKILL_ROUTER_CWD=/absolute/path/to/repo \
node routing/eval.js \
  --acceptance test/acceptance-prompts.json \
  --strict
```

Strict mode requires precision of at least 0.80, F1 of at least 0.70, and zero forbidden matches. The report also includes p50, p95, and maximum in-process scoring latency.

Run all tests:

```bash
node --test test/*.test.js
```

Measure 1,000 warm routing decisions on the target scope:

```bash
SKILL_ROUTER_HOST=codex \
SKILL_ROUTER_DATA_DIR="$HOME/.codex/skill-router-data" \
node routing/benchmark.js --iterations 1000 --cwd /absolute/path/to/repo
```

## Runtime contract

Every hook command must set `SKILL_ROUTER_HOST=codex` or `SKILL_ROUTER_HOST=claude`. The runtime does not infer the host from unstable payload fields.

Example Codex output:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Skill routing candidates:\n- $agentic-project-finder (/absolute/path/SKILL.md)\nUse only if the intent matches."
  }
}
```

The output has at most three candidates and 500 characters. A normal match has no `systemMessage` and no fake confidence percentage.

Ordinary negation does not disable routing. Explicit opt-outs such as `ne suggère aucune skill` and `disable skill routing` do. A prompt that already contains an active `$skill` mention for Codex or `/skill` command for Claude Code also passes through silently.

## Configuration

| Variable | Purpose |
|---|---|
| `SKILL_ROUTER_HOST` | Required adapter: `codex` or `claude` |
| `SKILL_ROUTER_CWD` | Build target working directory |
| `SKILL_ROUTER_HOME` | Home override for tests or isolated installations |
| `SKILL_ROUTER_DATA_DIR` | Cache and optional log root |
| `SKILL_ROUTER_EXTRA_ROOTS` | Additional authorized skill roots, separated by the OS path delimiter |
| `SKILL_ROUTER_OVERLAY_ROOTS` | External corpus roots, separated by the OS path delimiter |
| `SKILL_ROUTER_LOG=1` | Enable metadata-only routing logs |
| `SKILL_ROUTER_DEEP_CHECK_MS` | Interval for a detached content-hash verification, default 60000 ms |

## Rollback

1. Remove only the handler whose command contains `skill-router/bm25-suggest.js` from the relevant hooks file.
2. Restore the timestamped backup printed by the installer.
3. Open `/hooks` in Codex and verify that no modified untrusted hook remains active.
4. Keep the cache temporarily for diagnosis. It contains scenarios and metadata, not user prompts.
