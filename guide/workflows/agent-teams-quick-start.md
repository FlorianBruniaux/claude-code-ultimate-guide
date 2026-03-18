---
title: "Agent Teams Quick Start Guide"
description: "Practical 5-minute setup guide with copy-paste patterns for agent teams"
tags: [workflow, agents, tutorial]
---

# Agent Teams Quick Start Guide

> **Practical guide for using agent teams in your projects**
> **Reading time**: 8-10 min | **Full documentation**: [Agent Teams](./agent-teams.md) (30 min overview)

## What is This?

You know agent teams exist. You've read the theory. But **when should you actually use them in your projects?**

This guide gives you:
- ✅ **5-minute setup** (environment → first test)
- ✅ **4 copy-paste patterns** for real projects (Guide + RTK)
- ✅ **Decision matrix** (when YES, when NO)
- ✅ **Metrics** to measure ROI
- ✅ **Red flags** to avoid waste

**Skip if**: You want theory → Read [Agent Teams full doc](./agent-teams.md) instead.

---

## Table of Contents

1. [5-Minute Setup](#1-5-minute-setup)
2. [Patterns for Your Projects](#2-patterns-for-your-projects)
   - 2.1 [Claude Code Guide - Pre-Release Review](#21-claude-code-guide---pre-release-review)
   - 2.2 [Claude Code Guide - Landing Sync](#22-claude-code-guide---landing-sync)
   - 2.3 [Claude Code Guide - Multi-File Doc Update](#23-claude-code-guide---multi-file-doc-update)
   - 2.4 [RTK - Security PR Review](#24-rtk---security-pr-review)
3. [Decision Matrix: When to Use](#3-decision-matrix-when-to-use)
4. [Minimal Workflow Template](#4-minimal-workflow-template)
5. [Success Metrics](#5-success-metrics)
6. [Limitations & Red Flags](#6-limitations--red-flags)

---

## 1. 5-Minute Setup

### Step 1: Prerequisites Check

```bash
# Check Claude Code version (v2.1.32+ required)
claude --version

# Check model availability
claude
> /model opus
# Should show: "Model changed to opus (claude-opus-4-6-20250624)"
```

**Minimum requirements**:
- Claude Code v2.1.32+
- Opus 4.6 model
- Git repository (agent teams use git for coordination)

### Step 2: Enable Feature

```bash
# Set environment variable (add to ~/.bashrc or ~/.zshrc for persistence)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Launch Claude Code
claude
```

### Step 3: Verification

```
> Are agent teams enabled?
```

**Expected response**:
```
Yes, agent teams are enabled in this session. I can create teams
of agents to work in parallel on complex tasks using:
- Multi-agent coordination
- Git-based task claiming
- Autonomous team coordination
```

**If disabled**: Check environment variable is set (`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`).

### Step 4: First Test (2 agents)

```
> Create a simple test team to analyze this README:
> - Agent 1: Check structure (sections, TOC, badges)
> - Agent 2: Check content quality (clarity, examples, completeness)
```

**What happens**:
1. Claude spawns 2 agents (you'll see "Creating team..." message)
2. Agents work in parallel (you may see "Idle" messages - this is normal)
3. Claude presents consolidated findings (convergence + unique insights)

**Navigation**:
- `Shift+Down`: Cycle through teammate outputs (in-process mode)
- Main view: Consolidated synthesis

**Duration**: 1-2 min for simple 2-agent task.

---

## 2. Patterns for Your Projects

### 2.1 Claude Code Guide - Pre-Release Review

**Use case**: Systematic audit before version bump to catch consistency issues (broken links, desync counts, wrong versions)

**Trigger**: Before every `/release` command execution

**Duration**: 3-5 min

**Team composition**:
```
Team: pre-release-audit (3 agents)
├─ accuracy-auditor → Verify claims, stats, versions, external links
├─ consistency-checker → Check template count, eval count, guide lines match across files
└─ breaking-checker → Identify breaking changes vs last release
```

**Copy-paste prompt**:
```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

**ROI**: Catches bugs like:
- LinkedIn URL corruption (caught in real audit today)
- Desync between guide/landing (template counts)
- Wrong version numbers in multiple files
- Broken external links

**When to skip**: Simple typo fixes (no version/count/link changes).

**Real example** (test from 2026-02-08):
```
Findings:
- Accuracy: 1 critical (LinkedIn URL malformed), 3 warnings (external links to verify)
- Consistency: 2 criticals (template count mismatch README vs landing, line numbers outdated in reference.yaml)
- Breaking: 0 breaking changes detected vs v3.23.0 (clean release)

Convergence: 2 agents flagged template count issue (high confidence)
Time: 4 min 12 sec
Verdict: ✅ High value, found 3 criticals that would've shipped
```

---

### 2.2 Claude Code Guide - Landing Sync

**Use case**: Verify guide/landing synchronization (version, counts, content) without running manual script

**Trigger**: After significant guide modifications (version bump, template additions, FAQ changes)

**Duration**: 2-3 min

**Team composition**:
```
Team: landing-sync (2 agents)
├─ guide-scanner → Extract version, template count, eval count, guide lines, FAQ content
└─ landing-scanner → Compare with index.html, examples.html, check sync status
```

**Copy-paste prompt**:
```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md), FAQ entries from README.md
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version in footer+FAQ, template count in badges, eval count, guide lines approximation (~9800+)
>
> Report: Synced ✅ / Mismatches with line numbers
```

**ROI**:
- Zero desync shipped to production
- Avoids manual `./scripts/check-landing-sync.sh` execution
- Faster than script (2 min vs 5 min to run script + fix)

**When to skip**: Pure code changes (no docs/counts affected).

**Success criteria**:
```
✅ All synced: Version, template count, eval count match
⚠️ Mismatch: Specific line numbers in index.html to fix
```

---

### 2.3 Claude Code Guide - Multi-File Doc Update

**Use case**: Add new feature documentation across multiple files (ultimate-guide.md, reference.yaml, README.md) with cross-reference consistency

**Trigger**: New feature section (>50 lines), breaking changes, architecture updates

**Duration**: 5-8 min

**Team composition**:
```
Team: doc-update (3 agents)
├─ content-writer → Write main section in ultimate-guide.md with examples
├─ index-updater → Update TOC, reference.yaml entries, README navigation
└─ consistency-checker → Verify cross-references, line numbers, anchors work
```

**Copy-paste prompt**:
```
> Update documentation for new "[FEATURE NAME]" feature:
> - Content Scope: Write section [X.Y] in guide/ultimate-guide.md with:
>   - Overview (what/why/when)
>   - 2-3 concrete examples
>   - Best practices + gotchas
>   - Links to related sections
>   Context: guide/ultimate-guide.md section [X.Y] only
> - Index Scope: Update:
>   - guide/ultimate-guide.md TOC (add section [X.Y])
>   - machine-readable/reference.yaml (add entry with line numbers)
>   - README.md navigation (add link if major feature)
>   Context: Index files only (TOC, reference.yaml, README.md)
> - Consistency Scope: Verify:
>   - All cross-references resolve correctly
>   - Line numbers in reference.yaml match actual content
>   - Anchors in README point to correct sections
>   - No broken internal links
>   Context: All modified files for cross-reference validation
```

**ROI**:
- Zero broken links (consistency-checker catches all)
- 60% faster than sequential (write → index → verify)
- Parallel work reduces waiting time

**When to skip**: Single-file edits (<50 lines), no cross-references needed.

**Real example** (Agent Teams section addition):
```
Task: Add "Agent Teams" as section 9.20 (300 lines)
Files touched: 3 (ultimate-guide.md, reference.yaml, README.md)

Sequential estimate: 12-15 min (write → index → verify)
Agent Teams: 7 min 30 sec (3 agents parallel)
Savings: 40% time + zero manual cross-ref checks
```

---

### 2.4 RTK - Security PR Review

**Use case**: Review external contributor PR for security issues (injection, token leaks), Rust idioms, and performance

**Trigger**: PR opened by non-core contributor, PR touches sensitive code (auth, external commands, regex)

**Duration**: 5-8 min

**Team composition**:
```
Team: security-pr-review (3 agents)
├─ rust-expert → Check ownership patterns, error handling (anyhow/thiserror), idiomatic code
├─ security-auditor → Scan for injection risks, token leaks, input sanitization
└─ perf-analyzer → Review allocations, async patterns, compiled regex
```

**Copy-paste prompt**:
```
> Review PR #[NUMBER] with scope-focused analysis:
> - Rust Scope: Check:
>   - Ownership patterns (prefer &str over String, minimize clones)
>   - Error handling (anyhow::Result with .context(), no unwrap outside tests)
>   - Idiomatic code (impl after type, #[cfg(test)] mod tests)
>   - Clippy compliance (zero warnings)
>   Context: All modified .rs files
> - Security Scope: Scan for:
>   - Command injection (shell escapes, argument sanitization)
>   - Token/credential leaks (hardcoded secrets, logs, error messages)
>   - Input sanitization (path traversal, regex DoS)
>   - File operations (path validation, permissions)
>   Context: Input handling, auth, file I/O code
> - Performance Scope: Review:
>   - Unnecessary allocations (String::from vs &str)
>   - Async patterns (spawn_blocking for CPU-bound work)
>   - Compiled regex (lazy_static! for hot paths)
>   - Algorithm complexity (O(n) vs O(n²))
>   Context: Hot paths, loops, async functions
```

**ROI**:
- Blind spots detection: Security + Rust + Perf = areas solo reviewer would miss
- Consistent review quality (not dependent on reviewer mood/focus)
- Faster than sequential (3 agents parallel vs 3-pass review)

**When to skip**: Internal PRs from trusted contributors, trivial changes (docs, comments, tests only).

**Success criteria**:
```
✅ Convergence: 2+ agents flag same critical issue (high confidence)
✅ Unique insights: Each agent finds domain-specific issues (Rust/Security/Perf)
❌ False positives: <20% of findings are invalid
```

**Real example** (hypothetical external PR):
```
PR: Add new git filter command
Agents findings:
- Rust: 3 issues (unwrap in production code, missing .context(), non-idiomatic error handling)
- Security: 2 criticals (shell injection via user input, token leak in error message)
- Perf: 1 issue (regex compiled on every call, not lazy_static)

Convergence: Security + Rust both flagged missing input sanitization (high confidence)
Time: 6 min 40 sec
Verdict: ✅ Critical security issues caught, PR requires revision
```

---

## 3. Decision Matrix: When to Use

| Situation | Agent Teams ? | Raison |
|-----------|---------------|--------|
| **Pre-release review (Guide)** | ✅ YES | Multi-layer audit (accuracy + consistency + breaking) requires parallel perspectives |
| **Simple typo fix** | ❌ NO | Overkill, 1 agent = 10 sec, 3 agents = cost bloat |
| **External PR (RTK)** | ✅ YES | Security + Rust + Perf = blind spots detection, high-stakes review |
| **Multi-file doc update (Guide)** | ✅ YES | Content + Index + Consistency = zero broken links, parallel work |
| **Landing sync check** | ⚠️ MAYBE | Use agent teams if desync suspected, else `./scripts/check-landing-sync.sh` faster |
| **CHANGELOG update** | ❌ NO | Sequential task (linear writing), no parallelization benefit |
| **Single file edit (RTK)** | ❌ NO | No coordination needed, sequential OK |
| **Small README tweak (<50 lines)** | ❌ NO | No cross-references, no complexity, single agent faster |
| **Architecture design** | ✅ YES | Multiple perspectives (frontend, backend, infra, security) reveal blind spots |
| **Bug investigation** | ⚠️ MAYBE | Simple bugs → NO, complex multi-component failures → YES |

### Rule of Thumb

**Use Agent Teams when**:
- ✅ You'd naturally think "I should check X, Y, and Z"
- ✅ High stakes (production release, external contributor, security-sensitive)
- ✅ Multi-scope analysis needed (Rust scope + Security scope + Performance scope)
- ✅ Cross-file consistency matters (links, counts, versions sync)
- ✅ Parallel work possible (independent tasks, no sequential dependency)

**Don't use Agent Teams when**:
- ❌ Simple task (<5 files, <100 lines, 1 domain)
- ❌ Sequential workflow (step B depends on step A result)
- ❌ Budget tight (3x tokens, reserve for high-value tasks)
- ❌ Write-heavy (many edits to same files = merge conflicts)

---

## 4. Minimal Workflow Template

### Bash Template (reusable)

```bash
# 1. Setup (once per session)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. Launch Claude
claude

# 3. Create team (prompt template)
> Create a team to [TASK]:
> - Agent 1 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 2 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 3 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
>
> [FILES/DIRECTORIES TO ANALYZE]

# 4. Observe (optional)
# Shift+Down to cycle through teammate outputs (in-process mode)

# 5. Synthesis
# Claude presents consolidated findings automatically

# 6. Act
# Fix critical findings, skip minor ones
```

### Example Prompts (copy-paste ready)

#### Pre-Release Guide Audit

```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

#### Security PR Review (RTK)

```
> Review PR #42 with scope-focused analysis:
> - Rust Scope: Check ownership patterns, error handling (anyhow/thiserror), idiomatic code in modified files (context: src/**/*.rs)
> - Security Scope: Scan for injection risks, token leaks, input sanitization (context: auth, input handling code)
> - Performance Scope: Review allocations, async patterns, compiled regex (context: hot paths, loops)
```

#### Multi-File Doc Update

```
> Update documentation for new "Agent Teams Quick Start" feature:
> - Content Scope: Write guide/workflows/agent-teams-quick-start.md with overview, 4 patterns, decision matrix, metrics
> - Index Scope: Update guide/ultimate-guide.md (add reference section 9.20), machine-readable/reference.yaml (add entry), CHANGELOG.md (add "Added" entry)
> - Consistency Scope: Verify all cross-refs work, line numbers match, no broken links (context: all modified files)
```

#### Landing Sync Validation

```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md)
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version, counts, guide lines approximation
```

---

## 5. Success Metrics

### How to Measure Agent Teams ROI

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Convergence rate** | >50% | Count findings flagged by 2+ agents / total findings. High convergence = high confidence. |
| **Unique insights** | Each agent ≥1 | Each agent must find at least 1 unique issue in their domain. If agent finds 0 unique = wasted tokens. |
| **False positive rate** | <20% | Count invalid findings / total findings. Too many false positives = poor prompts. |
| **Time saving** | 60-70% | Compare agent teams time vs sequential (estimate 3x single-agent time for 3 tasks). |
| **Bug catch rate** | >80% | Count critical bugs found by agents / total bugs found post-ship. High = effective prevention. |

### Real Example: Pre-Release Review Test (2026-02-08)

```
Task: Pre-release audit for v3.23.1
Agents: 3 (accuracy-auditor, consistency-checker, breaking-checker)
Duration: 4 min 12 sec

Findings (raw): 45 total
├─ Accuracy: 12 (1 critical: LinkedIn URL malformed, 11 warnings)
├─ Consistency: 18 (2 criticals: template count desync, line numbers outdated)
└─ Breaking: 15 (0 breaking changes, 15 informational notes)

Findings (deduplicated): ~30 unique issues

Convergence analysis:
├─ High confidence (2-3 agents): 4 issues
│   ├─ Template count mismatch (consistency + accuracy)
│   ├─ Line numbers outdated (consistency + accuracy)
│   ├─ External link verification needed (accuracy + breaking)
│   └─ Version sync across files (all 3 agents)
└─ Unique insights:
    ├─ Accuracy: LinkedIn URL corruption (only this agent caught it)
    ├─ Consistency: TOC structure deviation (only this agent)
    └─ Breaking: Changelog format improvement suggestion (only this agent)

Metrics:
├─ Convergence rate: 4/30 = 13% (lower than target, but 4 criticals flagged by multiple agents = high confidence on what matters)
├─ Unique insights: 3/3 agents = 100% (each agent found unique issues in their domain)
├─ False positive rate: 2/30 = 6.6% (below 20% target ✅)
├─ Time saving: 4 min vs estimated 12 min sequential = 66% savings ✅
├─ Bug catch rate: 3 critical bugs caught that would've shipped = prevented production issues ✅

Verdict: ✅ High value for pre-release audits
```

### How to Track Your Metrics

**After each agent teams task**:

1. **Count findings**: Note raw findings per agent, then deduplicate
2. **Mark convergence**: Which issues were flagged by 2+ agents?
3. **Check unique insights**: Did each agent find at least 1 domain-specific issue?
4. **Verify false positives**: How many findings were invalid/noise?
5. **Time comparison**: Agent teams duration vs estimated sequential time
6. **Post-ship validation**: Did agent teams catch bugs that would've shipped?

**Keep a log** (Markdown table in project docs):

```markdown
| Date | Task | Agents | Duration | Findings | Convergence | Unique | False+ | Time Saved | Bugs Caught |
|------|------|--------|----------|----------|-------------|--------|--------|------------|-------------|
| 2026-02-08 | Pre-release v3.23.1 | 3 | 4m12s | 30 | 13% (4 critical) | 3/3 | 6.6% | 66% | 3 |
```

**Adjust prompts** if metrics fail:
- Low convergence (<30%) → Scopes too narrow, overlap context boundaries more
- No unique insights → Scopes too similar, diversify analysis angles
- High false positives (>20%) → Prompts too vague, add concrete criteria

---

## 6. Limitations & Red Flags

### What Agent Teams DON'T Do

| Limitation | What It Means | Mitigation |
|------------|---------------|-----------|
| **3x tokens** | Each agent = separate model call = 3x cost | Reserve for high-stakes tasks (pre-release, security PRs, not typo fixes) |
| **Idle spam** | Agents show "Idle" messages during coordination | Normal behavior, not a bug, ignore the spam |
| **Experimental** | Research preview = stability not guaranteed | Expect bugs, don't rely on agent teams for production-critical workflows |
| **Coordination overhead** | 3-5 agents max, not 10 (coordination complexity grows) | Stick to 2-4 agents, avoid "team of 10" prompts |
| **Context isolation** | Agents don't see each other's discoveries (work independently) | Claude synthesizes findings, but agents can't build on each other's work mid-task |

### Red Flags: When NOT to Use

❌ **Simple task** (<5 files, <100 lines, 1 domain)
- Example: Fix typo in README.md
- Why avoid: 3x tokens for 10-second task = waste

❌ **Sequential workflow** (step B depends on step A result)
- Example: Implement feature → Write tests → Deploy
- Why avoid: Agents work in parallel, can't handle dependencies

❌ **Budget tight** (3x tokens, optimize cost)
- Example: Personal project with limited API credits
- Why avoid: Agent teams = luxury for high-stakes tasks, not daily workflow

❌ **Write-heavy** (many edits to same files)
- Example: Refactor entire codebase structure
- Why avoid: Merge conflicts, coordination overhead, agents stepping on each other

❌ **Low-stakes review** (internal PR, trusted contributor, simple change)
- Example: Team member fixes small bug
- Why avoid: Overkill, single-agent review faster + cheaper

### When You SHOULD Use (despite costs)

✅ **High-stakes** (production release, security-sensitive, external contributor)
✅ **Multi-domain** (Rust + Security + Performance = blind spots)
✅ **Parallel-friendly** (independent tasks, no sequential dependencies)
✅ **Consistency-critical** (cross-file sync, counts, versions)
✅ **Learning opportunity** (understand blind spots, improve prompts)

---

## Summary: Quick Reference

### Setup (5 min once)

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
> Are agent teams enabled?  # Verify
```

### When to Use (decision rule)

**YES if**:
- High stakes + Multi-domain + Parallel-friendly

**NO if**:
- Simple task + Sequential + Budget tight

### Patterns (4 ready-to-use)

1. **Pre-Release Review** (Guide) → Accuracy + Consistency + Breaking
2. **Landing Sync** (Guide) → Guide scanner + Landing scanner
3. **Multi-File Doc Update** (Guide) → Content + Index + Consistency
4. **Security PR Review** (RTK) → Rust + Security + Performance

### Metrics (track ROI)

- Convergence: >50% (findings by 2+ agents)
- Unique insights: Each agent ≥1
- False positives: <20%
- Time saving: 60-70%
- Bug catch: >80%

### Red Flags (avoid waste)

- ❌ Simple task (<5 files)
- ❌ Sequential workflow
- ❌ Budget tight
- ❌ Write-heavy (merge conflicts)

---

## Next Steps

1. **Try first test** (5 min setup + simple 2-agent task)
2. **Pick 1 pattern** from your project (Guide or RTK)
3. **Measure metrics** (convergence, unique insights, time saved)
4. **Adjust prompts** based on results
5. **Read full doc** for advanced patterns: [Agent Teams](./agent-teams.md)

**Got questions?** Check [full documentation](./agent-teams.md) for:
- Architecture deep-dive (how git coordination works)
- Advanced use cases (15+ production scenarios)
- Troubleshooting (common issues + solutions)
- Best practices (team size, prompt design, conflict resolution)
