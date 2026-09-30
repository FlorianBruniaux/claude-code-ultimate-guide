---
name: check-cache-bugs
description: "Audit Claude Code setup for cache bugs (CC#40524): sentinel, --resume/--continue, attribution header + ArkNill B3/B4/B5"
effort: low
disable-model-invocation: true
---

# Check cache bugs (CC#40524)

Audit your Claude Code setup for cache and cost bugs discovered in March-April 2026.

**Time**: ~30 seconds | **Scope**: version, config files, CLAUDE.md, skills, hooks, shell profiles, all claude binaries

> **Note on cache contamination**: This skill loads content containing `cch=` strings into the current session's message array. For cleanest results, run this command at the very start of a fresh session, or via `claude -p "$(cat .claude/commands/check-cache-bugs.md)"` as a one-shot print-mode invocation.

**Reference**: `anthropics/claude-code#40524` | **Discovered by**: `@jmarianski` + `@whiletrue0x` | **Extended by**: `@ArkNill` (ArkNill/claude-code-cache-analysis, April 2026)

---

## Background

### Fix Status (current as of v2.1.92)

| Bug | Versions affected | Status |
|-----|------------------|--------|
| Bug 1: cch sentinel (standalone binary) | v2.1.36-v2.1.90 | **FIXED in v2.1.91** |
| Bug 2: deferred_tools_delta on --resume | v2.1.69-v2.1.89 | **FIXED in v2.1.90** |
| Bug 3: attribution header per-session hash | v2.1.69+ | **Active** (env var workaround) |
| B4: Microcompact / silent context stripping | all versions through v2.1.92 | **Active** (GrowthBook controlled) |
| B5: Tool result budget cap 200K | all versions through v2.1.92 | **Active** (MCP tools exempted) |

### Original three bugs (CC#40524)

- **Bug 1** (FIXED v2.1.91): Bun's native HTTP layer did a same-length byte replacement of the
  `cch=00000` attestation placeholder after `JSON.stringify` but before TLS. Triggered only if
  `cch=00000` appeared literally in `messages[]` content. Confirmed closed; npm and standalone
  binary are now equivalent on v2.1.91+.

- **Bug 2** (FIXED v2.1.90): The session JSONL writer stripped `deferred_tools_delta` attachment
  records before writing to disk. On `--resume`, those records were absent; the deferred tools
  layer had no prior history and re-announced all tools from scratch, shifting every message
  position and breaking the messages-level cache prefix entirely. Each resume rebuilt 87-118K
  tokens as `cache_creation`. Anthropic tracked internally as inc-4747.

- **Bug 3** (ACTIVE, v2.1.69+): Claude Code injects a billing header as the first block of the
  system prompt. The header contains a 3-character SHA-256 hash derived from characters [4, 7, 20]
  of the first user message + CC version, unique per session, per subagent, per side-query. Since
  the cache is prefix-based, this causes a cold miss on ~12K system prompt tokens on every
  invocation. A session with 5 subagents = 6 cold misses. Empirical: 48% -> 99.98% cache hit with
  env var workaround.

### Additional bugs (ArkNill, April 2026)

- **B4: Microcompact** (all versions): Three mechanisms silently replace tool results with
  `[Old tool result content cleared]` before sending to the API. Controlled by server-side
  GrowthBook flags, bypasses `DISABLE_AUTO_COMPACT`. The `/export` command shows original
  context, NOT what the model received. 327 clearing events measured in one session.

- **B5: Tool result budget cap** (all versions): `applyToolResultBudget()` truncates tool results
  when aggregate chars exceed 200K. Built-in tools (Read, Bash, Grep, Glob, Edit) are affected.
  MCP tools can override via `_meta["anthropic/maxResultSizeChars"]` (v2.1.91+).

Cost impact summary: 2-5x per session start/subagent for Bug 3 in isolation; 10-20x per turn for
Bug 2 with 10+ skills and 3-4 resumes (both estimates are correct in their respective context).

---

## Instructions

You are an auditor. Run all phases in order, collect every result, and produce the final report. Do not skip phases or stop early.

---

### Phase 1: Claude Code version and install method

```bash
# Version check
claude --version

# All installed claude binaries
which -a claude 2>/dev/null

# Check if active binary is standalone or npm
file $(which claude) 2>/dev/null
ls -la $(which claude) 2>/dev/null
```

- Version < 2.1.90 -> flag **BUG 2 RISK** (resume/DTD; fixed in v2.1.90)
- Version < 2.1.91 AND standalone binary -> flag **BUG 1 MECHANISM** (sentinel; fixed in v2.1.91)
- Version >= 2.1.69 -> flag **BUG 3 RISK** (attribution header; no fix yet, check Phase 4)
- Binary is Mach-O / ELF executable -> standalone (relevant for Bug 1 on v2.1.36-v2.1.90)
- Binary is a symlink to `node_modules` or contains `cli.js` -> npm/npx

---

### Phase 2: Sentinel scan (Bug 1)

Search for the literal string `cch=` in all static config files. Exclude `.jsonl` files (ephemeral conversation history) and this command file itself.

```bash
# Global config files
grep -r "cch=" \
  ~/.claude/CLAUDE.md \
  ~/.claude/MEMORY.md \
  ~/.claude/TONE.md \
  ~/.claude/FLAGS.md \
  ~/.claude/RULES.md \
  ~/.claude/RTK.md \
  ~/.claude/ANTI_AI.md \
  2>/dev/null

# Global skills, commands, agents, hooks (excluding this command file)
grep -rl "cch=" ~/.claude/skills/ 2>/dev/null
grep -rl "cch=" ~/.claude/commands/ --exclude="check-cache-bugs.md" 2>/dev/null
grep -rl "cch=" ~/.claude/agents/ 2>/dev/null
grep -rl "cch=" ~/.claude/hooks/ 2>/dev/null

# Project-level config
grep -r "cch=" CLAUDE.md .claude/CLAUDE.md .claude/MEMORY.md 2>/dev/null
grep -rl "cch=" .claude/skills/ 2>/dev/null
grep -rl "cch=" .claude/commands/ --exclude="check-cache-bugs.md" 2>/dev/null
grep -rl "cch=" .claude/agents/ 2>/dev/null
grep -rl "cch=" .claude/hooks/ 2>/dev/null

# Broader scan: all CLAUDE.md files across projects
find ~ -name "CLAUDE.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  2>/dev/null | xargs grep -l "cch=" 2>/dev/null
```

Flag as **BUG 1 RISK** if any match found outside `.jsonl` files AND version < v2.1.91.
On v2.1.91+: sentinel mechanism is fixed, no risk regardless of config content.

---

### Phase 3: Resume/continue usage (Bug 2)

```bash
# settings.json
grep -i -- "--resume\|--continue" ~/.claude/settings.json 2>/dev/null
grep -i -- "--resume\|--continue" .claude/settings.json 2>/dev/null

# Hooks
grep -rn -- "--resume\|--continue" ~/.claude/hooks/ 2>/dev/null
grep -rn -- "--resume\|--continue" .claude/hooks/ 2>/dev/null

# Commands and skills
grep -rn -- "--resume\|--continue" ~/.claude/commands/ 2>/dev/null
grep -rn -- "--resume\|--continue" .claude/commands/ 2>/dev/null

# Shell profiles (aliases, functions)
grep -n -- "--resume\|--continue" ~/.zshrc ~/.bashrc ~/.bash_profile ~/.zprofile 2>/dev/null

# Project scripts
find . -name "*.sh" -o -name "Makefile" 2>/dev/null | \
  xargs grep -l -- "--resume\|--continue" 2>/dev/null
```

- Version >= v2.1.90: Bug 2 is **FIXED**, flag hits as informational only (no active cost risk)
- Version < v2.1.90 AND any hit in hooks/settings -> flag **BUG 2 AUTOMATED** (constant exposure)
- Version < v2.1.90 AND any hit in commands/skills/scripts -> flag **BUG 2 MANUAL** (exposure when invoked)

---

### Phase 4: Attribution header check (Bug 3)

Check whether the billing header env var is already disabled.

```bash
# Global settings
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER\|ENABLE_TOOL_SEARCH" \
  ~/.claude/settings.json 2>/dev/null

# Project settings
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER\|ENABLE_TOOL_SEARCH" \
  .claude/settings.json 2>/dev/null

# Shell profiles
grep -i "CLAUDE_CODE_ATTRIBUTION_HEADER" \
  ~/.zshrc ~/.bashrc ~/.bash_profile ~/.zprofile 2>/dev/null
```

- `CLAUDE_CODE_ATTRIBUTION_HEADER` not set to `false` AND version >= 2.1.69 -> flag **BUG 3 ACTIVE**
- Already set to `false` -> **BUG 3 MITIGATED**

---

### Phase 5: Multiple binaries check

```bash
for b in $(which -a claude 2>/dev/null | sort -u); do
  echo "=== $b ==="
  $b --version 2>/dev/null || echo "unavailable"
  file $b 2>/dev/null
  ls -la $b 2>/dev/null
done
```

Flag any standalone binary < v2.1.91 as at risk for Bug 1.
Flag any binary < v2.1.90 as at risk for Bug 2.
Flag any binary >= v2.1.69 as at risk for Bug 3 (unless attribution header env var already set).
Note stale binaries that could be mistakenly invoked.

---

## Output format

```
## Claude Code Cache Bug Audit: CC#40524

**Date**: [today]
**Active claude version**: [version]
**Install method**: [standalone binary | npm/npx | mixed]

---

### Bug 1: Sentinel replacement (standalone binary v2.1.36-v2.1.90)
**Status**: [FIXED (v2.1.91+) / SAFE / AT RISK / NOT APPLICABLE]

**Version >= v2.1.91**: [YES -> FIXED | NO -> check below]
**Mechanism active (standalone binary, v2.1.36-v2.1.90)**: [YES / NO]
**Trigger sentinel found in static config**: [YES (locations) | NO]

[If FIXED] Running v2.1.91+. Sentinel mechanism patched; npm and standalone are equivalent. No action needed.
[If AT RISK (v < 2.1.91 AND standalone AND sentinel found)]
-> Update to v2.1.91+: `npm install -g @anthropic-ai/claude-code@latest`
-> Temporary: remove `cch=00000` string from the flagged files, or use npm instead.
[If SAFE] Mechanism present in binary but no trigger in static config. Update to v2.1.91 still recommended.
[If NOT APPLICABLE] npm/npx install: Bug 1 mechanism absent.

---

### Bug 2: Cache prefix mismatch on --resume / --continue (v2.1.69-v2.1.89)
**Status**: [FIXED (v2.1.90+) / AT RISK (automated) / AT RISK (manual) / NOT APPLICABLE]

**Version >= v2.1.90**: [YES -> FIXED | NO -> check below]
**Automated usage found (hooks/settings)**: [YES (locations) | NO]
**Manual usage found (commands/skills/scripts)**: [YES (locations) | NO]

**Root cause**: JSONL writer stripped `deferred_tools_delta` records before writing to disk. On `--resume`,
the deferred tools layer had no announcement history and re-announced all tools from scratch, shifting every
message position and breaking messages-level cache prefix. Each resume rebuilt 87-118K tokens as cache_creation.
Anthropic tracked as inc-4747. Fixed in v2.1.90.

[If FIXED] Running v2.1.90+. Bug resolved. `--resume` usage found in config is now safe at the cache level.
[If AT RISK]
-> Update to v2.1.90+: `npm install -g @anthropic-ai/claude-code@latest`
-> Immediate: avoid `--resume` and `--continue` until updated.
[If NOT APPLICABLE] Version < 2.1.69: not affected.

---

### Bug 3: Attribution header per-session hash (v2.1.69+, no fix yet)
**Status**: [ACTIVE / MITIGATED / NOT APPLICABLE]

**Version in affected range (>= v2.1.69)**: [YES / NO]
**CLAUDE_CODE_ATTRIBUTION_HEADER set to false/0/no/off**: [YES -> MITIGATED | NO -> ACTIVE]

[If ACTIVE] Every session start and every subagent call misses the system prompt cache (~12K tokens
rebuilt at cache_creation rate). A session with 5 subagents = 6 cold misses.
-> Fix (immediate, no restart needed): add to ~/.claude/settings.json:
  {
    "env": {
      "CLAUDE_CODE_ATTRIBUTION_HEADER": "false"
    }
  }
-> Expected impact: cache hit ratio 48% -> ~99.98% (measured, source: @whiletrue0x CC#40524)

[If MITIGATED] Header already disabled. No action needed.
[If NOT APPLICABLE] Version < 2.1.69: not affected.

---

### B4/B5: Context mutation (informational, all versions)

These bugs are controlled by server-side GrowthBook flags and cannot be mitigated client-side.
No config check is possible; report as informational.

**B4: Microcompact**: Three mechanisms silently replace tool results with `[Old tool result content cleared]`
before sending to the API. The `/export` command shows original context, NOT what the model received.
Workaround: start fresh sessions periodically to reset the tool result pool.

**B5: Tool result budget cap (200K chars aggregate)**: Built-in tools (Read, Bash, Grep, Glob, Edit)
hit a 200K character cap on aggregate tool results per session. Results are truncated beyond this threshold.
MCP tools can partially override via `_meta["anthropic/maxResultSizeChars"]` (v2.1.91+, up to 500K).

---

### Multiple binaries
[List each binary found, version, type (standalone/npm), and per-bug status]

---

### Summary

| Bug | Versions | Status | Action |
|-----|----------|--------|--------|
| Bug 1: sentinel (standalone) | v2.1.36-v2.1.90 | [FIXED / SAFE / AT RISK / N/A] | [update to v2.1.91+ or "none"] |
| Bug 2: --resume/--continue | v2.1.69-v2.1.89 | [FIXED / AT RISK / N/A] | [update to v2.1.90+ or "none"] |
| Bug 3: attribution header | v2.1.69+ | [ACTIVE / MITIGATED / N/A] | [add env var or "none"] |
| B4: microcompact | all versions | INFORMATIONAL | start fresh sessions |
| B5: tool result budget 200K | all versions | INFORMATIONAL | use MCP tools for large reads |
| Stale binaries | -- | [CLEAN / PRESENT] | [remove or none] |

[If Bug 3 ACTIVE (always show this)]
Quick win: add CLAUDE_CODE_ATTRIBUTION_HEADER=false to settings.json, immediate effect, no restart needed.

[If all SAFE/MITIGATED/FIXED/N/A on Bugs 1-3]
No active cache exposure on the original CC#40524 bugs. B4/B5 are informational, monitor session length.

Track: github.com/anthropics/claude-code/issues/40524 | github.com/ArkNill/claude-code-cache-analysis
```
