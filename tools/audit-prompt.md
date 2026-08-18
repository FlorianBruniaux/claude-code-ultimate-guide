# Audit Your Claude Code Setup

> A self-contained prompt that audits your Claude Code configuration — project memory, rules hygiene, skills, agents/commands, security, MCP, workflow commands, and freshness — in one pass.

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Reference**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. What This Does

This prompt turns Claude into an **audit orchestrator** across 8 weighted dimensions (100 pts total). It runs a fast bash inventory, then delegates each domain to a specialized skill or command if one is installed, falling back to inline checks when not.

| What it audits | How |
|---|---|
| Memory & Context (CLAUDE.md, rules, token budget) | Delegates to `/token-audit` if installed, otherwise bash estimate |
| Rules Hygiene (`.claude/rules/`, `paths:` validity) | Delegates to `/eval-rules` if installed, otherwise bash scan |
| Skills Quality (frontmatter, effort, allowed-tools) | Delegates to `/eval-skills` if installed, otherwise quick check |
| Agents/Commands Quality (16 criteria, grades A-F) | Delegates to `/audit-agents-skills` if installed, otherwise check |
| Security Posture (permissions, hooks, sandbox) | Delegates to `/security-check` if installed, otherwise bash check |
| MCP Ecosystem (servers, DB risk, version safety) | Inline bash (no dedicated skill needed) |
| Workflow Commands (/investigate, /qa, /canary…) | Inline bash scan |
| Freshness & Best Practices (stale refs, cache bugs) | Inline bash + pattern checks |

**What this does NOT do**: replace the deep-dive tools it delegates to. Use `/security-audit`, `/token-audit`, `/eval-rules` directly when you want full detail on a specific dimension.

**Time**: ~5-8 min if all audit skills are installed, ~3-4 min in fallback mode.

**Important**: Claude will NOT make any changes without your explicit approval.

---

## 2. Who This Is For

| Level | What You'll Get |
|-------|-----------------|
| **Beginner** | Discover what you're missing and get starter templates |
| **Intermediate** | Identify optimization opportunities and advanced patterns |
| **Power User** | Validate your setup and find edge cases to polish |

**Prerequisites**:
- Claude Code installed and working
- A project directory to analyze (or just global config)
- Bash shell (native on macOS/Linux, WSL on Windows)

**Optional** (richer results): `/token-audit`, `/eval-rules`, `/eval-skills`, `/audit-agents-skills`, `/security-check` installed. See Section 8 for install commands.

---

## 3. How to Use It

### Step 1: Copy the Prompt

Copy everything inside the code block in [Section 4](#4-the-prompt) below.

### Step 2: Run Claude Code

```bash
cd your-project-directory
claude
```

### Step 3: Paste and Execute

Paste the prompt and press Enter. To also audit your global `~/.claude/` config, append `--include-global` after the paste.

### Step 4: Review Results

Claude presents the 8-dimension scorecard and asks for validation before making any changes.

### Platform Note

| Platform | Global Config Path |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. The Prompt

````markdown
# Audit My Claude Code Setup — v5.0

## Scope Detection

Check if the user appended `--include-global` to this prompt.
- **Default (project only)**: audit `.` + `.claude/` in the current directory.
- **With `--include-global`**: also audit `~/.claude/` and `~/.claude.json`.

Set SCOPE accordingly. All bash blocks below note which paths apply per scope.

## Instructions

Do NOT modify any files. Do NOT make any changes. Audit and report only.

Use efficient bash commands for discovery. Only read file content when needed for scoring.

---

## Phase 1 — Inventory (30 seconds, bash-only)

Run this single block to gather all structural data at once:

```bash
bash -c '
echo "=== SCOPE ==="
SCOPE="project"
[[ "$*" == *"--include-global"* ]] && SCOPE="project+global"
echo "Audit scope: $SCOPE"
CURRENT_DIR=$(pwd)

echo ""
echo "=== CONFIG FILES ==="
# Project
for f in ./CLAUDE.md ./.claude/CLAUDE.md ./.claude/settings.json ./.claude/settings.local.json; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f"
done
# Global (always check for context, even in project-only scope)
[ -f ~/.claude/CLAUDE.md ] && echo "✅ ~/.claude/CLAUDE.md (global)" || echo "❌ ~/.claude/CLAUDE.md (global)"
[ -f ~/.claude.json ] && echo "✅ ~/.claude.json (MCP config)" || echo "❌ ~/.claude.json"

echo ""
echo "=== FOLDER STRUCTURE ==="
for d in agents commands skills hooks rules styles; do
  if [ -d "./.claude/$d" ]; then
    count=$(find "./.claude/$d" -maxdepth 2 -type f | wc -l | tr -d " ")
    echo "✅ .claude/$d/ ($count files)"
  else
    echo "❌ .claude/$d/"
  fi
done

echo ""
echo "=== TECH STACK ==="
[ -f package.json ] && grep -o '"name": *"[^"]*"' package.json | head -1 | sed "s/\"name\": /nodejs: /"
[ -f pyproject.toml ] && grep "^name" pyproject.toml | head -1 | sed "s/name/python:/"
[ -f requirements.txt ] && echo "python: requirements.txt"
[ -f go.mod ] && head -1 go.mod | sed "s/module /go: /"
[ -f Cargo.toml ] && grep "^name" Cargo.toml | head -1 | sed "s/name/rust:/"
[ -f composer.json ] && echo "php: detected"
[ -f Gemfile ] && echo "ruby: detected"

echo ""
echo "=== MCP SERVERS ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  MCP=$(jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null)
  [ -n "$MCP" ] && echo "$MCP" | sed "s/^/  /" || echo "  (none for this project)"
  DB_MCP=$(echo "$MCP" | grep -iE "postgres|neon|supabase|mysql|database" || true)
  [ -n "$DB_MCP" ] && echo "  ⚠️  DB MCPs detected: $DB_MCP (verify not production)"
else
  echo "  (jq not installed or ~/.claude.json absent)"
fi

echo ""
echo "=== RULES INVENTORY ==="
RULES_DIR="./.claude/rules"
if [ -d "$RULES_DIR" ]; then
  count=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
  size=$(find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | tail -1 | awk "{print \$1}")
  echo "  $count rules files, ~$size total chars"
  echo "  Top 3 by size:"
  find "$RULES_DIR" -name "*.md" | xargs wc -c 2>/dev/null | sort -rn | head -4 | grep -v "total" | awk "{print \"    \" \$0}"
  with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
  always_on=$(( count - with_paths ))
  echo "  path-scoped: $with_paths | always-on: $always_on"
else
  echo "  No .claude/rules/ directory"
fi

echo ""
echo "=== AUDIT SKILLS AVAILABLE ==="
for skill in token-audit eval-rules eval-skills audit-agents-skills; do
  found=false
  [ -f "$HOME/.claude/skills/$skill/SKILL.md" ] && found=true
  [ -f ".claude/skills/$skill/SKILL.md" ] && found=true
  $found && echo "  ✅ /$skill" || echo "  ❌ /$skill (fallback mode)"
done
for cmd in security-check security-audit; do
  found=false
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd (fallback mode)"
done

echo ""
echo "=== CACHE BUG INDICATORS ==="
grep -rl "disableSkillShellExecution\|--resume" .claude/ ~/.claude/ 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No cache bug workarounds found"
' "$@"
```

Store this full output. Use it for all dimension scoring below.

---

## Phase 2 — Dimension Audit

Score each dimension. For dimensions with a delegated skill, check if that skill is available (per Phase 1 output). If ✅: invoke the skill and use its output for scoring. If ❌: run the inline fallback bash and apply the simplified heuristic.

### Dimension 1 — Memory & Context (20 pts)

**Full audit** (if `/token-audit` is available):
Invoke: `/token-audit`
Use the Token Audit output:
- Fixed context <20K tokens → 18-20 pts
- 20-40K tokens → 12-17 pts
- 40-60K tokens → 6-11 pts
- >60K tokens → 0-5 pts. Deduct 2 pts if CLAUDE.md is missing, 3 pts if global CLAUDE.md is missing.

**Fallback** (if `/token-audit` is not installed):

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c || echo 0)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
TOTAL=$(( (GLOBAL + PROJECT + RULES) / 4 + 7500 ))
echo "Estimated fixed context: ~$TOTAL tokens (~$(( TOTAL * 100 / 200000 ))% of 200K window)"
```

Fallback scoring (max 14 pts):
- Global CLAUDE.md exists and non-empty: 3 pts
- Project CLAUDE.md exists: 3 pts
- Rules count reasonable (<15 files): 2 pts
- Token estimate <20K: 6 pts | 20-40K: 3 pts | >40K: 0 pts

### Dimension 2 — Rules Hygiene (10 pts)

**Full audit** (if `/eval-rules` is available):
Invoke: `/eval-rules`
Take the average score across all rules files (12 pts each). Map to 10 pts proportionally.

**Fallback** (if `/eval-rules` is not installed):

```bash
RULES_DIR=".claude/rules"
[ -d "$RULES_DIR" ] || { echo "No rules dir"; exit 0; }
total=$(find "$RULES_DIR" -name "*.md" | wc -l | tr -d " ")
with_front=$(grep -rl "^---" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
with_paths=$(grep -rl "^paths:" "$RULES_DIR"/*.md 2>/dev/null | wc -l | tr -d " ")
valid_patterns=0
for f in "$RULES_DIR"/*.md; do
  pattern=$(grep -A1 "^paths:" "$f" 2>/dev/null | grep "^\s*-" | head -1 | sed "s/.*- //;s/['\"]//g")
  [ -n "$pattern" ] && ls $pattern 2>/dev/null | head -1 | grep -q . && valid_patterns=$(( valid_patterns + 1 ))
done
echo "Total: $total | With frontmatter: $with_front | With paths: $with_paths | Valid patterns: $valid_patterns"
```

Fallback scoring (max 8 pts):
- Rules directory exists: 1 pt
- All files have YAML frontmatter: 2 pts
- At least half have `paths:` field: 3 pts
- No file >150 lines (check with `wc -l`): 2 pts

### Dimension 3 — Skills Quality (10 pts)

**Full audit** (if `/eval-skills` is available):
Invoke: `/eval-skills`
Take the average score across all skill files (14 pts each). Map to 10 pts proportionally.

**Fallback** (if `/eval-skills` is not installed):

```bash
SKILLS_DIR=".claude/skills"
[ -d "$SKILLS_DIR" ] || { echo "No skills dir (0 pts)"; exit 0; }
total=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d " ")
with_effort=$(grep -rl "^effort:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_tools=$(grep -rl "^allowed-tools:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
with_desc=$(grep -rl "^description:" "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d " ")
echo "Skills: $total | effort field: $with_effort | allowed-tools: $with_tools | description: $with_desc"
```

Fallback scoring (max 8 pts):
- Skills directory exists: 1 pt
- All SKILL.md have `description:` field: 2 pts
- All SKILL.md have `effort:` field: 3 pts
- All SKILL.md have `allowed-tools:` field: 2 pts

### Dimension 4 — Agents/Commands Quality (10 pts)

**Full audit** (if `/audit-agents-skills` is available):
Invoke: `/audit-agents-skills`
Take the overall score from its report (score/100). Multiply by 0.10 to get pts on 10.

**Fallback** (if `/audit-agents-skills` is not installed):

```bash
agents=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l | tr -d " ")
commands=$(find .claude/commands -name "*.md" 2>/dev/null | wc -l | tr -d " ")
skills=$(find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l | tr -d " ")
with_front=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^---" 2>/dev/null | wc -l | tr -d " ")
with_desc=$(find .claude/agents .claude/commands .claude/skills -name "*.md" 2>/dev/null | xargs grep -l "^description:" 2>/dev/null | wc -l | tr -d " ")
# Check argument-hint on legacy commands still using $ARGUMENTS
uses_args=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l '\$ARGUMENTS' 2>/dev/null | wc -l | tr -d " ")
with_hint=$(find .claude/commands -name "*.md" 2>/dev/null | xargs grep -l 'argument-hint' 2>/dev/null | wc -l | tr -d " ")
echo "Agents: $agents | Commands: $commands | Skills: $skills | With frontmatter: $with_front | With description: $with_desc"
echo "Commands using \$ARGUMENTS: $uses_args | With argument-hint: $with_hint"
```

Fallback scoring (max 8 pts):
- Has agents, commands, or skills: 2 pts
- All have YAML frontmatter: 2 pts
- All have `description:` field: 2 pts
- `argument-hint:` present in all legacy commands that use `$ARGUMENTS`: 2 pts

### Dimension 5 — Security Posture (20 pts)

**Full audit** (if `/security-check` is available):
Invoke: `/security-check`
Map its findings to 20 pts:
- No critical findings: 18-20 pts
- 1-2 medium findings: 12-17 pts
- 3+ findings or any critical: 0-11 pts

**Fallback** (if `/security-check` is not installed):

```bash
# permissions.deny check
echo "=== Permissions Deny ==="
for setting in ".claude/settings.json" "~/.claude/settings.json"; do
  [ -f "$setting" ] && {
    echo "File: $setting"
    grep -E "\.env|\.pem|credentials|secrets" "$setting" 2>/dev/null && echo "  ✅ Sensitive patterns found" || echo "  ❌ No .env/.pem/credentials blocked"
    grep -i "sandbox\|failIfUnavailable" "$setting" 2>/dev/null | head -3 | sed "s/^/  /"
  }
done

echo ""
echo "=== Hooks ==="
if [ -d ".claude/hooks" ]; then
  hooks=$(ls .claude/hooks/*.sh 2>/dev/null | wc -l | tr -d " ")
  pretool=$(grep -rl "PreToolUse" .claude/hooks/ 2>/dev/null | wc -l | tr -d " ")
  echo "  Hooks: $hooks | PreToolUse: $pretool"
else
  echo "  ❌ No hooks directory"
fi

echo ""
echo "=== Dangerous Patterns ==="
# Check for hardcoded tokens/keys in config
grep -rn "sk-\|ghp_\|xox[baprs]-\|AKIA" .claude/ CLAUDE.md 2>/dev/null | grep -v "example\|sample\|template" | head -5 || echo "  No obvious secrets found"
```

Fallback scoring (max 17 pts):
- `.env*` blocked in `permissions.deny`: 4 pts
- `*.pem` and `credentials*` also blocked: 3 pts
- At least one `PreToolUse` hook exists: 4 pts
- Sandbox configured (`failIfUnavailable`): 3 pts
- No hardcoded secrets in config: 3 pts

### Dimension 6 — MCP Ecosystem (10 pts)

Inline bash only (no dedicated skill for this dimension):

```bash
CURRENT_DIR=$(pwd)
echo "=== MCP Servers for this project ==="
if command -v jq &>/dev/null && [ -f ~/.claude.json ]; then
  jq -r --arg p "$CURRENT_DIR" '
    .projects[$p].mcpServers // {} | to_entries[] |
    "\(.key): \(.value.command // .value.url // "configured")"
  ' ~/.claude.json 2>/dev/null || echo "  No project-specific MCPs"

  echo ""
  echo "=== DB MCP Risk ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "postgres|neon|supabase|mysql|database|mongo" \
    | sed "s/^/  ⚠️  /" || echo "  No DB MCPs found"

  echo ""
  echo "=== Guide MCP ==="
  jq -r --arg p "$CURRENT_DIR" '.projects[$p].mcpServers // {} | keys[]' ~/.claude.json 2>/dev/null \
    | grep -iE "claude-code-ultimate-guide|ccguide" \
    | sed "s/^/  ✅ /" || echo "  ❌ Guide MCP not installed"
else
  echo "  (install jq for MCP analysis)"
fi
```

Scoring (max 10 pts):
- At least 1 MCP configured: 3 pts
- Documentation MCP present (Context7 or similar): 2 pts
- No DB MCP, or DB MCP is clearly scoped to dev/staging: 3 pts
- Guide MCP installed: 2 pts

### Dimension 7 — Workflow Commands (10 pts)

```bash
echo "=== Core Workflow Skills/Commands ==="
for cmd in investigate qa canary land-and-deploy review-pr; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done

echo ""
echo "=== Additional Debug/Deploy Skills/Commands ==="
for cmd in ship commit release-notes diagnose; do
  found=false
  [ -f ".claude/commands/$cmd.md" ] && found=true
  [ -f "$HOME/.claude/commands/$cmd.md" ] && found=true
  [ -f ".claude/skills/$cmd/SKILL.md" ] && found=true
  [ -f "$HOME/.claude/skills/$cmd/SKILL.md" ] && found=true
  $found && echo "  ✅ /$cmd" || echo "  ❌ /$cmd"
done
```

Scoring: 2 pts per core command present (`/investigate`, `/qa`, `/canary`, `/land-and-deploy`, `/review-pr`). Max 10 pts.

### Dimension 8 — Freshness & Best Practices (10 pts)

```bash
echo "=== Deprecated Model References ==="
grep -rn "claude-3-haiku\|gpt-3.5\|claude-2\b\|claude-instant\|claude-3-5-sonnet\b" \
  .claude/ CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null | grep -v ".git" | head -8 \
  || echo "  No deprecated model names found"

echo ""
echo "=== Config Freshness ==="
git log --oneline -1 --format="  Last commit: %ar (%h)" 2>/dev/null || echo "  (not a git repo)"

echo ""
echo "=== Cache Bug Workarounds ==="
# Bug 2 HIGH: --resume causes 87-118K token re-announcement
grep -rn "disableSkillShellExecution" ~/.claude/settings.json .claude/settings.json 2>/dev/null \
  | sed "s/^/  /" || echo "  disableSkillShellExecution: not set"

echo ""
echo "=== argument-hint Coverage (legacy commands) ==="
missing=0
for f in $(find .claude/commands -name "*.md" 2>/dev/null); do
  grep -q '\$ARGUMENTS' "$f" && ! grep -q "argument-hint" "$f" && {
    echo "  ⚠️  Missing argument-hint: $f"
    missing=$(( missing + 1 ))
  }
done
[ $missing -eq 0 ] && echo "  ✅ All commands using \$ARGUMENTS have argument-hint (skills use effort: field instead)"

echo ""
echo "=== Hook Profiles (env vars) ==="
grep -rn "CLAUDE_HOOK_PROFILE\|HOOK_PROFILE" .claude/ CLAUDE.md 2>/dev/null | head -3 | sed "s/^/  /" || echo "  No hook profiles configured"
```

Scoring (max 10 pts):
- No deprecated model names: 3 pts
- Git activity in last 90 days (or not a git repo): 2 pts
- `disableSkillShellExecution: false` OR not using `--resume` pattern: 3 pts
- All commands using `$ARGUMENTS` have `argument-hint:`: 2 pts

---

## Phase 3 — Unified Report

Produce the report in this exact structure:

### Executive Summary

State:
- **Total Score**: X/100
- **Maturity Tier**: Starter (<40) | Growing (40-59) | Established (60-79) | Optimized (80+)
- **Detected Stack**: [from Phase 1]
- **Top 3 Quick Wins**: highest-ROI gaps that can be fixed in <15 min each
- **Top 3 Critical Gaps**: highest-severity missing items

### Dimension Scorecard

| # | Dimension | Score | Max | Status | Key Finding |
|---|-----------|-------|-----|--------|-------------|
| 1 | Memory & Context | X | 20 | ✅/⚠️/❌ | one-line finding |
| 2 | Rules Hygiene | X | 10 | ✅/⚠️/❌ | one-line finding |
| 3 | Skills Quality | X | 10 | ✅/⚠️/❌ | one-line finding |
| 4 | Agents/Commands Quality | X | 10 | ✅/⚠️/❌ | one-line finding |
| 5 | Security Posture | X | 20 | ✅/⚠️/❌ | one-line finding |
| 6 | MCP Ecosystem | X | 10 | ✅/⚠️/❌ | one-line finding |
| 7 | Workflow Commands | X | 10 | ✅/⚠️/❌ | one-line finding |
| 8 | Freshness & Best Practices | X | 10 | ✅/⚠️/❌ | one-line finding |
| | **TOTAL** | **X** | **100** | | |

Status thresholds: ✅ ≥80% of max, ⚠️ 50-79%, ❌ <50%.

### Detailed Findings

Group by dimension. For each gap (❌ or ⚠️):

```
**[Dimension N — Name]**
Gap: [what is missing or suboptimal]
Impact: [what breaks or degrades without it]
Fix: [concrete action with file path]
```

### Stack-Specific Templates

Propose at most 3 templates, chosen for the highest-impact gaps on the detected stack. Include only file path + starter content. Do not repeat existing content.

### Deepen Your Audit

List which audit skills are not installed and what they would unlock:

```
Skills not installed — install for deeper analysis:

# token-audit (Dimension 1 — adds rule classification, hook overhead analysis)
mkdir -p ~/.claude/skills/token-audit
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/token-audit/SKILL.md \
  > ~/.claude/skills/token-audit/SKILL.md

# eval-rules (Dimension 2 — adds glob validation, interactive review)
mkdir -p ~/.claude/skills/eval-rules
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-rules/SKILL.md \
  > ~/.claude/skills/eval-rules/SKILL.md

# eval-skills (Dimension 3 — adds 14-pt scoring per skill)
mkdir -p ~/.claude/skills/eval-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/eval-skills/SKILL.md \
  > ~/.claude/skills/eval-skills/SKILL.md

# audit-agents-skills (Dimension 4 — adds grades A-F, comparative analysis)
mkdir -p ~/.claude/skills/audit-agents-skills
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/audit-agents-skills/SKILL.md \
  > ~/.claude/skills/audit-agents-skills/SKILL.md

# security-check (Dimension 5 — scans against threat-db, 55 CVEs, 24 techniques)
mkdir -p ~/.claude/skills/security-check
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/skills/security-check/SKILL.md \
  > ~/.claude/skills/security-check/SKILL.md

# Alternative for Dimension 1 — context-evaluator.ai
# Zero-install LLM-native audit: 17 AI evaluators for CLAUDE.md/AGENTS.md,
# automated .patch remediation. Complements /token-audit with deeper rule analysis.
# Visit: https://context-evaluator.ai
```

---

## Phase 4 — Validation Request

After presenting the report, ask:

"Implement the top 3 quick wins? Reply:
- **yes** → I'll implement all three
- **high** → only critical gaps (Dimensions 5 and 1 if ❌)
- **1, 3** → specific items by number from findings
- **none** → keep the report, no changes"

Wait for explicit user response before taking any action.
````

---

## 5. What to Expect

### Example Executive Summary

```
## Executive Summary

Total Score: 52/100 — Growing

Detected Stack: TypeScript + Next.js + Prisma

Top 3 Quick Wins:
- Add permissions.deny for .env* (15 min) → fixes Dimension 5 critical gap
- Install /investigate and /qa commands (5 min) → +4 pts on Dimension 7
- Add paths: frontmatter to 3 always-on rules (20 min) → reduces fixed context ~3K tokens

Top 3 Critical Gaps:
1. ❌ Security — no permissions.deny, no PreToolUse hooks (0/20)
2. ⚠️ Memory — project CLAUDE.md missing, global is 22K tokens (8/20)
3. ❌ Workflow — 3/5 core commands absent (4/10)
```

### Example Dimension Scorecard

| # | Dimension | Score | Max | Status | Key Finding |
|---|-----------|-------|-----|--------|-------------|
| 1 | Memory & Context | 8 | 20 | ⚠️ | 22K fixed tokens, no project CLAUDE.md |
| 2 | Rules Hygiene | 7 | 10 | ⚠️ | 4 rules, none have paths: field |
| 3 | Skills Quality | 8 | 10 | ✅ | 3 skills, all have effort + allowed-tools |
| 4 | Agents/Commands Quality | 6 | 10 | ⚠️ | 8 commands, 2 missing argument-hint |
| 5 | Security Posture | 0 | 20 | ❌ | No deny rules, no hooks |
| 6 | MCP Ecosystem | 7 | 10 | ✅ | Context7 + Sequential configured |
| 7 | Workflow Commands | 4 | 10 | ⚠️ | /investigate ✅ /qa ❌ /canary ❌ |
| 8 | Freshness & Best Practices | 12 | 10 | — | capped at max |
| | **TOTAL** | **52** | **100** | ⚠️ | |

---

## 6. Understanding Results

### Glossary

| Term | Definition |
|------|------------|
| **Memory Files** | CLAUDE.md files that provide persistent context to Claude across sessions |
| **Context Budget** | Total always-on token cost before any task begins. Seuils: green <20K, yellow 20-40K, red >40K |
| **Rules (auto-loaded)** | `.claude/rules/*.md` files that load at every session start. Files with `paths:` only load when a matching file is read |
| **paths: frontmatter** | Field in rule YAML that scopes a rule to specific file patterns — reduces always-on overhead |
| **Eval Skill** | Specialized skill that audits one domain: `eval-skills`, `eval-rules`, `token-audit`, `audit-agents-skills` |
| **Single Source of Truth** | Pattern where conventions are documented once and referenced via `@path` |
| **Tool SEO** | Writing agent/command descriptions so Claude selects the right tool automatically |
| **MCP Servers** | Model Context Protocol — external tools that extend Claude's capabilities. Config stored in `~/.claude.json` per project |
| **Hook Profiles** | minimal/standard/strict security levels for hooks, switched via env var (added v3.38.0) |
| **PreToolUse** | Hook that fires BEFORE Claude executes a tool — used for security checks and approval gates |
| **effort: field** | Skill frontmatter for low/medium/high complexity signal — used by Claude to allocate thinking budget |
| **argument-hint** | Frontmatter field showing placeholder text in slash command menu for commands using `$ARGUMENTS` |
| **Threat Database** | `examples/commands/resources/threat-db.yaml` — versioned CVEs, attack techniques, IOC records, and minimum safe versions |
| **Cache Bug #40524** | Bug 2 (HIGH): `--resume` causes full context re-announcement (87-118K tokens rebuilt per resume) |
| **Scope Drift** | When a PR changes files outside the stated plan intent. Detected by comparing `~/.claude/plans/` vs `git diff --stat` |
| **Fix-First Heuristic** | Review pattern: auto-fix mechanical issues, ask for judgment calls on security/design decisions |
| **LLM Output Trust Boundary** | Review category for AI-generated values written to DB without format validation |
| **managed-settings.d/** | Enterprise drop-in directory for governance rules that override user settings (added v2.1.83) |
| **Routines** | Cloud-hosted scheduled tasks with 3 trigger types: schedule, API, GitHub events (launched April 2026) |
| **Context Zones** | <70% optimal, 75% auto-compact trigger, 85% handoff recommended |
| **Sandbox** | OS-level isolation (Docker container or native process-level). Configured in settings.json |
| **Iron Law** | Debugging principle: no fixes without root cause investigation first. See `/investigate` |

### Score Thresholds

| Score | Tier | What it means |
|-------|------|----------------|
| 80-100 | Optimized | Config is solid. Focus on Freshness and edge cases |
| 60-79 | Established | Good foundation. Fill the ⚠️ dimensions |
| 40-59 | Growing | Core pieces exist but several gaps. Follow Quick Wins |
| <40 | Starter | Start with Dimension 5 (Security) and 1 (Memory) |

### Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | ≥80% of max pts for this dimension |
| ⚠️ | 50-79% of max pts |
| ❌ | <50% of max pts |

---

## 7. Common Issues

### "Audit skills not installed"

**Cause**: The specialized skills are optional and not globally available by default.

**What happens**: The prompt runs in fallback mode for that dimension. Scores are capped lower (8 pts instead of 10 for some dimensions). Results are still actionable, just less detailed.

**Fix**: Use the install commands in the "Deepen Your Audit" section of the report. Each skill takes ~1 min to install and immediately improves future audits.

### "Claude didn't find my files"

**Cause**: Wrong working directory or platform path differences.

**Fix**:
- Ensure you run `claude` from your project root
- On Windows, paths use `%USERPROFILE%\.claude\` not `~/.claude/`

### "Score seems off"

**Cause**: Fallback mode scoring is simplified — it can't verify glob validity, run 14-pt skill checks, or scan against the threat database.

**Fix**: Install the relevant audit skills (see "Deepen Your Audit"). Re-run to get accurate dimension scores.

### "Too many recommendations"

**Cause**: First-time audit on a project without Claude Code config.

**Fix**: Use the Quick Wins from the Executive Summary. Implement those three. Re-audit. Build incrementally.

### "Claude made changes without asking"

**Cause**: Phase 4 validation wasn't reached or was skipped.

**Fix**: Ensure you copied the complete prompt including Phase 4. Use Plan Mode (`Shift+Tab` twice) for extra safety before pasting.

---

## 8. Related Resources

**Complementary audit tools** (go deeper on specific dimensions):

| Tool | Dimension | Install |
|------|-----------|---------|
| `/token-audit` | Memory & Context | `mkdir -p ~/.claude/skills/token-audit && curl -sL .../examples/skills/token-audit/SKILL.md > ...` |
| `/eval-rules` | Rules Hygiene | Same pattern |
| `/eval-skills` | Skills Quality | Same pattern |
| `/audit-agents-skills` | Agents/Commands | Same pattern |
| `/security-check` | Security Posture (quick, ~30s) | `mkdir -p ~/.claude/skills/security-check && curl -sL ...` |
| `/security-audit` | Security Posture (full, 2-5 min, scored /100) | Same pattern |
| [`tools/context-audit-prompt.md`](context-audit-prompt.md) | Deep-dive on context engineering | Self-contained prompt, no install needed |
| [`tools/onboarding-prompt.md`](onboarding-prompt.md) | Setup from scratch | Self-contained prompt, no install needed |
| [context-evaluator.ai](https://context-evaluator.ai) | Memory & Context (alternative) — LLM-native, 17 evaluators, auto `.patch` | Zero-install web tool |

**Reference docs**:
- [The Ultimate Claude Code Guide](../guide/ultimate-guide.md) — full reference
- [Cheatsheet](../guide/cheatsheet.md) — quick daily reference
- [Security Hardening](../guide/security/security-hardening.md) — production security patterns
- [Context Engineering](../guide/core/architecture.md) — token budget strategies
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code) — Anthropic documentation

**For CI/CD integration** (JSON output, batch mode): [`examples/scripts/audit-scan.sh`](../examples/scripts/audit-scan.sh)

---

*Version 5.2 (guide v3.41.0+) | v5.2: skill detection updated for CC 2.1.3 skills-commands unification — Dimension 4/7/8 bash now checks both `.claude/skills/` and `.claude/commands/`; security-check install path fixed to canonical SKILL.md. v5.1: context-evaluator.ai added. v5.0: refactored from checklist to orchestrator with 8 weighted dimensions.*
