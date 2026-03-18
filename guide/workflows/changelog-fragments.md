# Changelog Fragments: Enforced Per-PR Documentation

A 3-layer enforcement pattern that ensures every PR is documented at write time, never at release time.

---

## The Problem

Single `CHANGELOG.md` files break on active teams. Three open feature branches all touching the same file means merge conflicts on every merge. Someone resolves the conflict, drops a line, and release notes are wrong before they're published.

The deeper problem is timing. "Document at release time" sounds reasonable until you're staring at PR #840 three weeks after it merged, trying to reconstruct what changed for users. The commit says `fix session handling`. The developer is in a different timezone. Context is gone.

Enforcement without CI gates means changelogs become a nag job. Someone has to chase people before every release, under time pressure, filling in blanks from git log.

The solution: one YAML fragment per PR, written while implementing, validated by CI, assembled automatically at release.

---

## The 3-Layer Architecture

The system works because enforcement happens at three independent levels. Each layer catches a different failure mode.

### Layer 1: CLAUDE.md Workflow Rule

The first layer is a rule loaded into Claude Code's context at every session. It encodes the entire fragment workflow so Claude can complete it autonomously when asked to create a PR.

```markdown
# git-workflow.md (loaded via CLAUDE.md)

## Changelog Fragment — Required Before Every PR

Before creating a PR, always generate a changelog fragment.

### Steps

1. **Infer from git diff** — analyze `git diff main...HEAD` to determine:
   - `type`: feat | fix | perf | refactor | security | docs | chore
   - `scope`: the functional area affected (auth, sessions, api, etc.)
   - `title`: one-line user-facing summary (< 80 chars)

2. **Create the fragment** — run `pnpm changelog:add` or write directly:
   ```
   changelog/fragments/{PR_NUMBER}-{slug}.yml
   ```

3. **Validate** — run `pnpm changelog:validate changelog/fragments/{file}.yml`

4. **Commit alongside the PR** — include the fragment in the same branch

### Fragment schema

```yaml
pr: 886                    # must match filename prefix
type: fix                  # feat|fix|perf|refactor|security|docs|chore
scope: "visiochat"
title: "Fix empty chat after SSE race condition"   # < 80 chars
description: |             # optional — explain user impact, not implementation
  SSE workplan fires before AI stream completes, causing ChatWrapper
  to mount with 0 messages.
breaking: false
migration: false           # set true if PR adds a DB migration
```

### Bypass

Add label `skip-changelog` for PRs with no user impact (CI config, deps updates, release commits).
```

This rule makes Claude Code a participant in enforcement, not just a coding tool. When a developer says "make the PR," Claude infers the fragment content from the diff and creates it before opening the PR.

### Layer 2: UserPromptSubmit Hook (Behavioral Detection)

The second layer intercepts intent before it becomes action. When the developer types something that signals PR creation intent, the hook checks whether a changelog fragment was mentioned.

```bash
# .claude/hooks/smart-suggest.sh (excerpt — Tier 0 enforcement)

# PR creation intent detected
if echo "$PROMPT_LC" | grep -qE '(create.*pr|open.*pr|make.*pr|pull.?request|push.*pr)'; then
    # Fragment not mentioned → redirect to creation step first
    if ! echo "$PROMPT_LC" | grep -qE '(changelog|fragment|skip-changelog)'; then
        suggest "pnpm changelog:add" \
            "REQUIRED before merge — creates changelog/fragments/{PR}-{slug}.yml"
    else
        # Already mentioned → suggest the PR command normally
        suggest "/pr" "PR creation with structured description"
    fi
fi
```

The hook is `UserPromptSubmit`: non-blocking, max one suggestion per prompt, silent on no match. It runs before Claude Code processes the prompt, so the developer sees the reminder inline before Claude starts doing anything.

The conditional logic (`if X without Y`) is the key pattern here. It's not a blanket blocker — it adapts to context. If the developer already mentioned the fragment, they get the normal suggestion. If they didn't, they get the enforcement reminder.

**Full hook with 3-tier architecture**: [`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)

### Layer 3: CI Enforcement (GitHub Actions)

The third layer is the hard gate. Two independent jobs run on every PR targeting the main branch.

**`check-fragment` job**: checks bypass labels first (closed list), then requires `changelog/fragments/{PR_NUMBER}-*.yml` to exist and pass structural validation.

```yaml
- name: Check fragment exists and is valid
  env:
    PR_NUMBER: ${{ github.event.pull_request.number }}
    PR_LABELS: ${{ toJson(github.event.pull_request.labels.*.name) }}
  run: |
    SKIP_LABELS=("skip-changelog" "dependencies" "release" "chore: deps")
    for LABEL in "${SKIP_LABELS[@]}"; do
      if echo "$PR_LABELS" | grep -q "\"$LABEL\""; then
        echo "Bypass label detected — fragment not required"
        exit 0
      fi
    done

    FRAGMENT=$(ls "changelog/fragments/${PR_NUMBER}-"*.yml 2>/dev/null | head -1)
    if [ -z "$FRAGMENT" ]; then
      echo "Fragment missing. Run: pnpm changelog:add"
      exit 1
    fi

    pnpm tsx changelog/scripts/validate.ts "$FRAGMENT"
```

**`check-migration-flag` job** (runs independently, no bypass): detects new SQL migration files with `git diff --name-only --diff-filter=A`. If migrations are present and `migration: false` in the fragment, it fails. This job cannot be bypassed by labels — a `skip-changelog` PR that adds a migration still triggers the check.

The two jobs are independent by design. A PR can bypass fragment creation (via label) but still fail the migration check.

---

## Fragment Assembly at Release

Fragments accumulate in `changelog/fragments/` as PRs merge. At release time, one command assembles them into a versioned CHANGELOG section.

```bash
pnpm changelog:assemble --version 1.8.0 [--dry-run]
```

What it does:
1. Reads all `changelog/fragments/*.yml`
2. Groups by type in fixed order (feat, fix, perf, refactor, security, docs, chore)
3. Pulls `breaking: true` entries into a dedicated `🔨 Breaking Changes` section
4. Annotates `migration: true` entries inline with `⚠️ Migration DB.`
5. Replaces the `## [Next Release]` placeholder in `CHANGELOG.md`
6. Archives fragments to `changelog/fragments/released/{version}/`

Output:
```markdown
## [1.8.0] - 2026-03-15

### 🔨 Breaking Changes
- **Remove legacy token format (#871)** — Tokens issued before v1.6.0 are invalid.

### ✨ New Features
- **Add real-time presence indicators (#892)**

### 🔧 Bug Fixes
- **Fix empty chat after SSE race condition (#886)** — SSE workplan fires before
  AI stream completes, causing ChatWrapper to mount with 0 messages.
```

---

## Why 3 Layers, Not 1

Each layer catches a different failure mode:

| Layer | Failure caught | When |
|-------|---------------|------|
| CLAUDE.md rule | Claude forgets the workflow | Every session |
| UserPromptSubmit hook | Developer types "make the PR" without thinking | Pre-prompt |
| CI gate | Fragment was skipped or corrupt | Pre-merge |

A single CI gate catches the issue too late — the developer has to context-switch back after their PR is already open. The hook catches it at intent time. The CLAUDE.md rule means Claude handles it autonomously when given the task.

The layers don't conflict. They reinforce each other. A developer who sees the hook suggestion will run `pnpm changelog:add`. Claude will follow the CLAUDE.md rule and validate the output. CI confirms everything before merge.

---

## Adopting This Pattern

The TypeScript scripts (add, validate, assemble, audit) are specific to the Méthode Aristote stack. The 3-layer enforcement pattern is not — it works with any fragment format, any CI system, any assembler.

**Minimum viable setup:**

1. **Define your fragment schema** (YAML, JSON, whatever fits your stack)
2. **Add a CLAUDE.md rule** encoding the creation workflow so Claude can handle it autonomously
3. **Add a `UserPromptSubmit` hook** with the `if PR-intent without fragment-mention → suggest` pattern
4. **Add a CI job** that checks for fragment existence before merge

The hook pattern generalizes to any mandatory workflow step. Substitute "changelog fragment" with "ADR", "migration flag", "test coverage check" — the conditional detection logic is the same.

---

## Related

- Hook example: [`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)
- Hook documentation: [UserPromptSubmit Hooks](../ultimate-guide.md) (search "UserPromptSubmit")
- Fragment validator and assembler scripts: available in the Méthode Aristote repository
