---
title: "Smart-Suggest Routing: Regex + BM25 Skill Hints"
description: "A Codex and Claude Code UserPromptSubmit routing system using regex rules and calibrated Okapi BM25 skill hints"
tags: [workflow, hooks, guide, reference]
---

# Smart-Suggest Routing: Regex + BM25 Skill Hints

`UserPromptSubmit` hooks can add advisory context before a model handles a prompt. Regex works for fixed enforcement rules. Okapi BM25 works for natural-language variations backed by a reviewed skill corpus.

The runnable implementation in `examples/hooks/bm25-routing/` supports Claude Code and Codex. Its recommended Codex deployment is one global hook that resolves both project and user skills from each prompt's working directory.

## Pick the right engine

| Situation | Regex | BM25 |
|---|---:|---:|
| Fixed command or policy phrase | Strong | Weak |
| Enforcement before an action | Strong | Not appropriate |
| Bilingual natural-language variations | Brittle | Strong with a corpus |
| New skill with fewer than eight positives | Manual rule possible | Native matching only |
| Broad intent with contrastive examples | Large rule set | Strong after evaluation |

Regex and BM25 can both attach to `UserPromptSubmit`, but they solve different problems. A regex reminder can require a changelog check. A BM25 hint can identify a likely review or repository-discovery skill. Neither should auto-approve or auto-run a destructive action.

## Codex architecture

Codex combines matching hooks from global and project configuration. Installing the same BM25 handler at both levels can therefore inject duplicate context. Use one global handler on a configured workstation:

```text
prompt + cwd
    |
    v
~/.codex/hooks/skill-router/bm25-suggest.js
    |
    +-- <cwd>/.agents/skills up to <git-root>/.agents/skills
    +-- ~/.agents/skills
    +-- ~/.codex/skills
    +-- /etc/codex/skills when readable
    +-- SKILL_ROUTER_EXTRA_ROOTS
    +-- external corpus overlays
    |
    v
user-owned cache keyed by repo, relative cwd, and resolved roots
    |
    v
one bounded additionalContext, or silent output
```

The nearest project skill shadows a project-root or global skill with the same frontmatter `name`. This matters in monorepos where a nested `.agents/skills` directory can intentionally override a broader definition.

Skills without a calibrated corpus are marked `native-only`. Codex can still select them from their description or the user can invoke them explicitly with `$skill-name`.

## Claude Code architecture

The same runtime can be installed in project mode with `SKILL_ROUTER_HOST=claude`. Discovery and calibration stay the same. Only the explicit hint syntax changes from Codex `$skill-name` to Claude Code `/skill-name`.

Keep project-specific regex hooks such as `smart-suggest.sh` when they encode separate enforcement rules. Do not duplicate the BM25 handler itself across active Codex configuration layers.

## Corpus format

An adjacent corpus belongs at `<skill>/evals/scenarios.json`:

```json
{
  "skill": "debug-db",
  "positive": [
    "my Prisma client reports connection refused",
    "connexion à la base de données impossible",
    "the database pool is exhausted"
  ],
  "negative": [
    "optimize this slow SQL query",
    "add an index to the users table",
    "export a database backup"
  ]
}
```

The `skill` value must match an active `SKILL.md` name and `^[a-z0-9][a-z0-9:_-]{0,127}$`. At least eight positive and two negative prompts are required for calibration. In practice, use 12 or more varied positives and at least five close negatives.

Negatives need shared vocabulary with the positives. Unrelated negatives make the task artificially easy and set an unsafe threshold. The runtime also scores contrastive negative examples and vetoes a candidate when its strongest negative match is at least as strong as its positive match.

Use an external overlay when a skill directory has a strict file contract. `SKILL_ROUTER_OVERLAY_ROOTS` points to one or more directories containing JSON corpus files. An overlay is ignored unless its `skill` currently resolves to an active skill.

## Discovery and security boundaries

The router parses only `name` and `description` from the first 64 KiB of each `SKILL.md`. It rejects malformed names and scenario files that target inactive or mismatched skills.

Skill symlinks resolve to their real path. A target is accepted only when it stays inside a discovered or explicitly authorized skill root. The emitted hint includes that exact resolved `SKILL.md` path, which gives the model an auditable target.

Precedence is deterministic:

1. nearest `.agents/skills` ancestor of `cwd`;
2. repository-root `.agents/skills`;
3. `~/.agents/skills`;
4. `~/.codex/skills`;
5. `/etc/codex/skills`;
6. explicit extra roots.

## Index and calibration

The scorer uses Okapi BM25 with `K1 = 1.2` and `B = 0.3`. It does not implement BM25+, because there is no delta term. The IDF form is:

```text
IDF(t) = log(1 + (N - n + 0.5) / (n + 0.5))
```

Positive and contrastive negative documents share the same IDF term space. Per-skill positive and negative scores are each the maximum over that skill's matching examples. A maximum avoids favoring skills merely because their corpus has more prompts.

Leave-one-out calibration selects a threshold that maximizes F-beta with beta squared equal to four. Status uses plain F1:

| Status | Meaning | Runtime behavior |
|---|---|---|
| `ok` | Calibration F1 is at least 0.60 and cross-skill evaluation passes | Eligible for BM25 |
| `conflict` | A threshold exists but F1 is below 0.60 | Never suggested |
| `excluded` | Fewer than eight positives or two negatives | Never suggested |
| `native-only` | Active skill has no accepted corpus | Native matching only |

The original router filtered only `excluded`, which let `conflict` skills fire. The current runtime requires exactly `status: ok`, a finite threshold, cross-skill eligibility, an active resolved skill, and no stronger contrastive negative match. The combined eligible set must reach global F1 0.70. Lower-quality project corpora stay `native-only`; an overlay that passed its independent holdout remains protected while the project set is trimmed.

## Cache behavior

Each resolved scope gets a separate cache key based on repository root, relative `cwd`, resolved skill roots, and algorithm version. This prevents two nested monorepo workspaces from sharing an incompatible index.

The build fingerprint includes normalized paths, size, modification time, SHA-256 content hash, and algorithm version for every active `SKILL.md` and corpus. The prompt hot path checks a stat fingerprint over known source and watch paths, which detects ordinary additions, edits, and deletions without rereading hundreds of files. Every 60 seconds, a detached deep check recomputes content hashes. This also catches an unusual same-size edit whose modification time was restored manually.

One builder holds an `O_EXCL` lock with a 30-second TTL. Cache files are written to temporary files and renamed atomically. During a rebuild, the current prompt uses the last valid index. Without a valid index, the hook exits silently and schedules the build in the background.

No prompt-time file is written under the current repository. The global installer sets a user-owned data directory. Optional logs contain routing metadata only, never raw prompt text.

## Output contract

The Codex adapter emits:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Skill routing candidates:\n- $agentic-project-finder (/absolute/path/SKILL.md)\nUse only if the intent matches."
  }
}
```

The Claude adapter uses `/agentic-project-finder`. The router emits at most three candidates and 500 characters. It does not display a confidence percentage because `score / sum(top scores)` is not a calibrated probability. Normal suggestions have no `systemMessage`.

Ordinary negation remains routable. For example, `analyse ce dépôt sans modifier les fichiers` can still select a review skill. Explicit opt-outs such as `ne suggère aucune skill` stop routing. An existing active `$skill` mention for Codex or `/skill` command for Claude also stops the router to avoid redundant advice.

## Installation

Preview a global Codex installation:

```bash
cd examples/hooks/bm25-routing
node install.js --host codex --scope user --dry-run
```

The preview lists source, destination, checksum, and hook changes without writing. Apply only after review:

```bash
node install.js --host codex --scope user --apply
```

The installer preserves existing handlers, adds one `UserPromptSubmit` handler, and creates a timestamped backup. Repeating an identical installation is a no-op.

Open `/hooks` in Codex after installation. Non-managed hooks require explicit review and trust. A file copy alone does not make the new handler active.

For a standalone project installation on a machine without the global handler:

```bash
node install.js \
  --host codex \
  --scope project \
  --project-root /absolute/path/to/repo \
  --dry-run
```

The generated project hook still writes caches to a user directory. Do not activate project and global Codex BM25 handlers together.

## Evaluation

Training examples must not double as acceptance evidence. Keep a separate prompt set with expected and forbidden skills:

```json
{
  "prompt": "find repositories implementing shared agent memory",
  "expected": ["agentic-project-finder"],
  "forbidden": ["critique-plan"]
}
```

Run the strict evaluator:

```bash
SKILL_ROUTER_CWD=/absolute/path/to/repo \
node routing/eval.js \
  --acceptance test/acceptance-prompts.json \
  --strict
```

The included gate requires precision of at least 0.80, F1 of at least 0.70, and zero forbidden hits. Extend coverage one reviewed skill at a time. Do not generate production scenarios automatically from descriptions.

## Failure modes to test

- missing, truncated, or invalid cache returns silently;
- project and global duplicate names resolve to the project path;
- `conflict`, `excluded`, and inactive skill names never appear;
- adding, editing, or deleting a corpus invalidates only the relevant scope;
- two simultaneous rebuilds produce one writer;
- optional logs contain no prompt text;
- 30 or more positive, negative, and explicit-invocation prompts pass before deployment;
- warm hook latency stays below 75 ms at p95 on the target machine.

Use `routing/benchmark.js --iterations 1000 --cwd <repo>` for the warm-path latency gate. It measures cache loading, stat invalidation checks, tokenization, scoring, filtering, and output construction in one process, excluding one-time Node startup.

The complete runnable tests use the built-in Node test runner:

```bash
node --test examples/hooks/bm25-routing/test/*.test.js
```

## Related workflows

- [Changelog Fragments](./changelog-fragments.md): regex enforcement patterns for `UserPromptSubmit`
- Runnable implementation: `examples/hooks/bm25-routing/`
