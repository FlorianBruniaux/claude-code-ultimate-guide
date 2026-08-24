---
title: "Known Issues & Critical Bugs"
description: "Verified critical issues affecting Claude Code users from community reports and official communications"
tags: [reference, security, debugging]
---

# Known Issues & Critical Bugs

This document tracks verified, critical issues affecting Claude Code users based on community reports and official communications.

> **Last Updated**: April 23, 2026
> **Source**: [GitHub Issues](https://github.com/anthropics/claude-code/issues) + [Anthropic Official Communications](https://www.anthropic.com/engineering)

---

## 🚨 Active Critical Issues

### 0. Prompt Cache Bugs: Silent Cost Inflation (Mar 2026 - Present)

**Severity**: 🔴 **HIGH - COST IMPACT**
**Status**: ⚠️ PARTIALLY FIXED (Bug 3 and Bug 2 still active as of v2.1.88)
**Issue**: [#40524](https://github.com/anthropics/claude-code/issues/40524)
**First Reported**: March 2026
**Affected Versions**: v2.1.69+ (Bugs 2 & 3), v2.1.36+ standalone binary (Bug 1)

#### Problem

Three independent bugs break Anthropic's prefix-based prompt caching, causing `cache_creation` charges
(full token cost) instead of `cache_read` (discounted). Measured cost impact depends on usage pattern:

- **Bug 3 alone (attribution header)**: 2-5x inflation on the ~12K-token system prompt per session start and per subagent call
- **Bug 2 active (resume + 10+ skills)**: per-resume rebuild of 87-118K tokens; sessions with 3-4 resumes measured at **4.3-34.6% cache read ratio** (vs 95-99% healthy), translating to **10-20x cost per turn** in the worst sessions
- **Combined effect**: 48% → 99.98% cache hit ratio improvement confirmed with workarounds applied (community measurement, CC#40524)

> **Basis**: Confirmed via community reverse-engineering (CC#40524), source code analysis of the
> leaked npm sourcemap, and independent session JSONL analysis (ArkNill, April 2026). Anthropic shipped
> a partial fix in v2.1.88 (tool schema bytes). Bugs 2 and 3 remain unpatched.

#### Bug 2: Full cache rebuild on --resume / --continue (v2.1.69+), HIGH IMPACT

**Root cause**: The session JSONL writer strips `deferred_tools_delta` attachment records before
writing to disk. On `--resume`, those records are gone, so the deferred tools layer has no prior
announcement history and re-announces all tools from scratch. This shifts every message position in
the restored conversation, breaking the messages-level cache prefix entirely.

**Concrete evidence** (from community session JSONL analysis, sessions with 14 skills):

| Entry | cache_read | cache_creation | Event |
|-------|-----------|----------------|-------|
| 102 | 84,164 | 174 | Normal turn |
| 103 | 0 | 87,176 | **Resume: full rebuild** |
| 105 | 87,176 | 561 | Recovered |
| 166 | 115,989 | 221 | Normal turn |
| 167 | 0 | 118,523 | **Resume: full rebuild** |

Each resume = 87-118K tokens rebuilt as `cache_creation` instead of `cache_read`. 3-4 resumes per
session = 300-400K tokens of avoidable cost. Impact scales with number of skills/deferred tools:
users with 10+ skills (common in framework setups) see the full 0% cache ratio on every resume.

**Workaround**: Avoid `--resume` and `--continue` until a fix ships. Start fresh sessions.
Downgrade option: `npm install -g @anthropic-ai/claude-code@2.1.68` (last version before regression).
Anthropic is tracking this internally (referenced in source telemetry as `inc-4747`).

**Engineering fix**: preserve `deferred_tools_delta` and `mcp_instructions_delta` records when
writing session JSONL, so resume can compute the delta correctly instead of re-announcing everything.

#### Bug 3: Attribution Header (low-to-medium impact, v2.1.69+)

**Root cause**: Claude Code injects a billing header as the **first block** of the system prompt on
every API request. This header contains a 3-character hash derived from characters of your first
user message, making it unique per session, per subagent, and per side query. Since Anthropic's cache
is prefix-based, this unique first block causes a cold miss on the ~12K-token system prompt on every
session start and subagent call.

**Nuance** (per jmarianski, original RE analyst): the per-session system prompt cold miss has
"marginal impact" in practice because the system prompt is small relative to total session context.
The resume bug (Bug 2) has a larger measurable cost for heavy users.

**Empirical measurement**: 48% → 99.98% cache hit ratio with workaround, but this reflects combined
effect with other cache factors; the isolated Bug 3 impact may be smaller.

**Workaround** (apply immediately, low risk):
```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "false"
  }
}
```
Accepted values: `"false"`, `"0"`, `"no"`, `"off"`. No restart needed.

#### Bug 1: Sentinel String Replacement (standalone binary v2.1.36+, edge case)

**Root cause**: Bun's native HTTP stack replaces a `cch=00000` placeholder in the request body
after serialization. If this exact string appears in your message content (e.g., from a CLAUDE.md
that discusses this bug), it may be replaced in the wrong location.

**Workaround**: Do not paste `cch=00000` literally in CLAUDE.md or config files.
Note: this only affects the standalone binary, not npm/npx installs.

#### Audit Tool

Run `/check-cache-bugs` (install from the [examples/commands](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/commands/check-cache-bugs.md) directory) to audit your setup for all three bugs in ~20 seconds.

> **Best practice**: run at the very start of a fresh session, or as a one-shot via `claude -p "$(cat .claude/commands/check-cache-bugs.md)"` to avoid contaminating the current session context with `cch=` strings (potential Bug 1 trigger).

#### Monitoring Cache Health

To verify whether your sessions are healthy, use the official `ANTHROPIC_BASE_URL` environment variable to route through a transparent local proxy and log `cache_creation_input_tokens` / `cache_read_input_tokens` from API responses:

```json
// ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8080"
  }
}
```

Run a pass-through proxy on port 8080 that reads but does not modify requests/responses, parsing the `usage` object from each response. **Healthy sessions** show cache read ratio > 80%; **affected sessions** show < 40%.

Alternatively, inspect session JSONL files directly in `~/.claude/projects/`, and look for `cache_creation_input_tokens` and `cache_read_input_tokens` per turn.

Community tools for monitoring:
- [`cc-diag`](https://github.com/nicobailey/cc-diag): mitmproxy-based Claude Code traffic analysis
- [`claude-code-router`](https://github.com/pathintegral-institute/claude-code-router): transparent proxy with logging

Community patch (applies both Bug 1 and Bug 2 fixes):
- [`cc-cache-fix`](https://github.com/Rangizingo/cc-cache-fix): community-developed patch + test toolkit

#### Official Response

Partial fix in v2.1.88 (tool schema bytes). Bugs 2 and 3 confirmed still active.

**Tracking**: [Issue #40524](https://github.com/anthropics/claude-code/issues/40524) (open since March 2026)

**Related issues**: [#40652](https://github.com/anthropics/claude-code/issues/40652) (cch= billing hash) · [#41663](https://github.com/anthropics/claude-code/issues/41663) (cache token consumption) · [#41607](https://github.com/anthropics/claude-code/issues/41607) (duplicate compaction subagents) · [#41767](https://github.com/anthropics/claude-code/issues/41767) (auto-compact loops v2.1.89) · [#41750](https://github.com/anthropics/claude-code/issues/41750) (context management fires every turn)

---

### 1. GitHub Issue Auto-Creation in Wrong Repository (Dec 2025 - Present)

**Severity**: 🔴 **CRITICAL - SECURITY/PRIVACY RISK**
**Status**: ⚠️ ACTIVE (as of Jan 28, 2026)
**Issue**: [#13797](https://github.com/anthropics/claude-code/issues/13797)
**First Reported**: December 12, 2025
**Affected Versions**: v2.0.65+

#### Problem

Claude Code **systematically creates GitHub issues in the public `anthropics/claude-code` repository** instead of the user's private repository, even when working within a local git repo directory.

#### Impact

**HIGH - PRIVACY/SECURITY**: At least **17+ confirmed cases** of users accidentally exposing sensitive information in the public repository:

- Database schemas
- API credentials and configuration details
- Infrastructure architecture
- Private project roadmaps
- Security configurations

#### Symptoms

- Issue created with unexpected `--repo anthropics/claude-code` flag
- Private project details appear in public anthropics/claude-code issues
- No confirmation prompt before creating issue in public repository
- Occurs when asking Claude to "create an issue" while in local git repo

#### Examples of Accidental Creations

Recent confirmed cases (Jan 2026):
- [#20792](https://github.com/anthropics/claude-code/issues/20792): "Deleted - created in wrong repo"
- [#16483](https://github.com/anthropics/claude-code/issues/16483), [#16476](https://github.com/anthropics/claude-code/issues/16476): "Claude OPENS ISSUES ON THE WRONG REPO"
- [#17899](https://github.com/anthropics/claude-code/issues/17899): "Claude Code suddenly decided to create issue in claude code repo"
- [#16464](https://github.com/anthropics/claude-code/issues/16464): "[Mistaken Post] Please delete"

Full list: [Search "wrong repo" OR "delete this"](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+%22wrong+repo%22+OR+%22delete+this%22)

#### Root Cause (Hypothesis)

Claude Code may confuse:
- **Legitimate feedback** about Claude Code itself → `anthropics/claude-code` (correct)
- **User project issues** → Current repository (should be default)

The tool appears to hardcode or over-prioritize `anthropics/claude-code` as default target.

#### Workarounds

**🛡️ BEFORE creating any GitHub issue via Claude Code:**

1. **Always verify the target repository**:
   ```bash
   # Check current repo
   git remote -v
   ```

2. **Explicitly specify repository**:
   ```bash
   gh issue create --repo YOUR_USERNAME/YOUR_REPO --title "..." --body "..."
   ```

3. **Review the command** before execution:
   - Look for `--repo anthropics/claude-code` flag
   - If present and incorrect, abort and specify correct repo

4. **Use manual approval** for all `gh` commands in Claude settings

5. **Never include sensitive information** in issue creation prompts until bug is fixed

#### If You're Affected

If you accidentally created an issue exposing sensitive information:

1. **Immediately contact GitHub Support** to request issue deletion (not just closing)
2. **Rotate any exposed credentials** (API keys, passwords, tokens)
3. **Report to Anthropic** via [security email](mailto:security@anthropic.com) if security-sensitive
4. **Check for data leaks**: Monitor exposed information usage

#### Official Response

As of Jan 28, 2026: **Issue remains open**, no official fix announced.

**Tracking**: [Issue #13797](https://github.com/anthropics/claude-code/issues/13797) (open since Dec 12, 2025)

---

### 2. Excessive Token Consumption (Jan 2026 - Present)

**Severity**: 🟠 **HIGH - COST IMPACT**
**Status**: ⚠️ REPORTED (Anthropic investigating)
**Issue**: [#16856](https://github.com/anthropics/claude-code/issues/16856)
**First Reported**: January 8, 2026
**Affected Versions**: v2.1.1+ (reported), may affect earlier versions

#### Problem

Multiple users report **4x+ faster token consumption** compared to previous versions, causing:
- Rate limits hit much faster than normal
- Same workflows consuming significantly more tokens
- Unexpected cost increases

#### Symptoms

From Issue #16856:
> "Starting from today's morning with the updated to CC 2.1.1 - the usage is ridiculous. I am working on the same projects for months, same routines, same time. But today it hits 5h limits like 4+ times faster!"

Common reports:
- Weekly limits exhausted in 1-2 days (vs. 5-7 days normally)
- Sessions hitting 90% context after 2-3 messages
- 4x-20x token consumption for identical operations

#### Context

**Holiday Usage Bonus Expiration**: December 25-31, 2025, Anthropic doubled usage limits as a holiday gift. When limits returned to normal on January 1, 2026, users experienced perception of "reduced capacity."

However, **reports persist beyond this timing**, suggesting potential underlying issue.

#### Anthropic Response

From [The Register](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/) (Jan 5, 2026):
> "Anthropic stated it 'takes all such reports seriously but hasn't identified any flaw related to token usage' and indicated it had ruled out bugs in its inference stack."

**Status**: **Not officially confirmed as a bug** by Anthropic as of Jan 28, 2026.

#### Related Issues

20+ reports found (Dec 2025 - Jan 2026):
- [#17687](https://github.com/anthropics/claude-code/issues/17687): "Unexpectedly high token consumption rate since January 2026"
- [#16073](https://github.com/anthropics/claude-code/issues/16073): "[Critical] Claude Code Quality Degradation - Ignoring Instructions, Excessive Token Usage"
- [#17252](https://github.com/anthropics/claude-code/issues/17252): "Excessive token consumption rate in session usage tracking"
- [#13536](https://github.com/anthropics/claude-code/issues/13536): "Excessive token usage on new session initialization"

[Full search](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+excessive+token+created%3A2025-12-01..2026-01-28)

#### Workarounds

While Anthropic investigates:

1. **Monitor token usage actively**:
   ```
   /context
   ```
   Check tokens used vs. capacity regularly

2. **Use shorter sessions**:
   - Restart sessions when approaching 50-60% context
   - Break complex tasks into multiple sessions

3. **Disable auto-compact** (may help):
   ```bash
   claude config set autoCompaction false
   ```

4. **Reduce MCP tools** if not needed:
   - Review `~/.claude.json` (field `"mcpServers"`)
   - Disable unused servers

5. **Use subagents** for isolated tasks:
   - Subagents have separate context windows
   - Use Task tool for complex operations

6. **Track your usage patterns**:
   - Compare before/after version upgrades
   - Document unusual spikes

#### Investigation Tips

If experiencing excessive consumption:

1. Note your **Claude Code version**: `claude --version`
2. **Compare versions**: Test with earlier stable version if available
3. **Document patterns**: Which operations trigger high usage?
4. **Report with data**: Include version, operation type, token counts in issue reports

---

## ✅ Resolved Historical Issues

### Triple Harness Incident: Effort, Thinking Tokens, Verbosity (Mar-Apr 2026)

**Severity**: 🔴 **HIGH**
**Status**: ✅ **RESOLVED** (all three issues resolved by April 20, 2026)
**Timeline**: March 4 – April 20, 2026

#### Problem

Three independent harness and system-prompt changes degraded Claude Code output quality over a six-week period. None were model-level regressions; all were in the Claude Code harness layer. The Anthropic API used directly (without the Claude Code harness) was not affected.

#### Incident 1: Default Effort High to Medium (March 4, reverted April 7)

**Trigger**: Long latency in high effort mode made the UI appear frozen on some sessions.
**Change**: Anthropic changed the default reasoning effort from `high` to `medium` for Sonnet 4.6 and Opus 4.6.
**Impact**: Users who hadn't manually set `/effort high` silently got medium-quality reasoning. The in-product indicator still showed "high", masking the regression for over a month.
**Affected**: Sonnet 4.6, Opus 4.6.
**Resolution**: Reverted April 7. New defaults: xhigh for Opus 4.7, high for all other models. Proper UI iterations (thinking spinners, clearer `/effort` UX) shipped alongside.

#### Incident 2: Thinking Tokens Cleared Per Turn After Idle (March 26, fixed April 10)

**Trigger**: Anthropic shipped a change to clear thinking tokens once when a session had been idle for over an hour (to reduce latency and cache cost on resume).
**Bug**: A code defect caused the clear to trigger on every subsequent turn for the rest of the session, not just once on resume.
**Impact**: Sessions became forgetful and repetitive, with Claude losing context progressively throughout a resumed conversation.
**Affected**: Sonnet 4.6, Opus 4.6.
**Resolution**: Bug fixed April 10, 2026 (v2.1.101). Root cause per Boris Cherny (CC team): large idle sessions caused full cache misses (900K+ tokens), creating significant token cost spikes for Pro users on resume.

#### Incident 3: Verbosity System Prompt Instruction (April 16, reverted April 20)

**Trigger**: Anthropic added a system prompt instruction to reduce response verbosity.
**Impact**: In combination with other prompt changes active at the time, coding quality dropped noticeably.
**Affected**: Sonnet 4.6, Opus 4.6, Opus 4.7.
**Resolution**: Reverted April 20. Four-day exposure, fastest resolution of the three incidents.

#### Community Impact

- Widespread reports of quality degradation across Reddit, HN, X/Twitter (March–April 2026)
- Cancellations among Pro and Max subscribers
- Anthropic employees (including Boris Cherny) initially responded in comment sections without acknowledging the systemic issues
- HN thread reached 250+ comments on day of disclosure

#### Anthropic Response

**Official Update**: [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) (April 23, 2026)

Key commitments from the post:
- Usage limits reset for all subscribers (April 23)
- Larger share of internal staff will use the exact public build (not the feature-test build)
- "Going forward" section promised improved eval and rollout practices

Key quote from Boris Cherny (HN comment):
> "We agree, and will be spending the next few weeks increasing our investment in polish, quality, and reliability."

**Resolution**: All three issues resolved between April 7–20, 2026.

---

### Model Quality Degradation (Aug-Sep 2025)

**Severity**: 🔴 **CRITICAL**
**Status**: ✅ **RESOLVED** (mid-September 2025)
**Timeline**: August 25 - early September 2025

#### Problem

Users reported Claude Code producing:
- Worse outputs than previous versions
- Syntax errors unexpectedly
- Unexpected character insertions (Thai/Chinese text in English responses)
- Failed basic tasks
- Incorrect code edits

#### Root Cause

Anthropic identified **three infrastructure bugs** (not model degradation):

1. **Traffic Misrouting**: ~30% of Claude Code requests routed to wrong server type → degraded responses
2. **Output Corruption**: Misconfiguration deployed Aug 25 caused token generation errors
3. **XLA:TPU Miscompilation**: Performance optimization triggered latent compiler bug affecting token selection

#### Community Impact

- **Mass cancellation campaign** (Aug-Sep 2025)
- Community theories: intentional model degradation (quantization) to reduce costs
- Reddit sentiment dropped sharply

#### Anthropic Response

**Official Postmortem**: [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) (Sept 17, 2025)

Key quote:
> "We never reduce model quality due to demand, time of day, or server load. The problems our users reported were due to infrastructure bugs alone."

**Resolution**: All bugs fixed by mid-September 2025.

---

## 🔄 LLM Day-to-Day Performance Variance

**Type**: Expected behavior (not a bug)
**Severity**: 🟡 **LOW - AWARENESS**
**Status**: Inherent to LLM inference, not specific to any version

### What This Is

Claude's output quality can vary noticeably from session to session, even with identical prompts and a clean context window. That differs from context window degradation, which happens within a session as context fills up. Here the concern is variance between fresh sessions.

Users sometimes report shorter responses, more conservative suggestions, or unexpected refusals on tasks that worked fine the day before. This can feel like a model downgrade, but it is not.

### Root Causes

**Probabilistic inference**: Temperature above 0 means every inference run is non-deterministic. Two runs of the same prompt will produce different token sequences. This is fundamental to how language models work.

**MoE routing variance**: Claude uses a Mixture of Experts architecture. On each forward pass, a routing mechanism selects which expert weights to activate. Different runs activate different combinations, producing different outputs even for semantically identical inputs.

**Infrastructure variance**: In production, requests hit different servers with different load levels, hardware generations, and thermal states. These factors influence numerical precision in floating-point arithmetic during inference, creating subtle but real output differences.

**Context sensitivity**: Even with `/clear`, tiny differences between sessions accumulate. The system prompt, tool list, and session initialization all slightly affect the model's first outputs.

### Observable Signals

| Signal | What You See | What It Means |
|--------|-------------|---------------|
| Response length | Shorter, less detailed than usual | Routing hit a more conservative path |
| Refusals | Edge cases that normally work get refused | Different safety calibration on this run |
| Code style | More verbose or more minimal than expected | Expert mix activated differently |
| Creativity | More conservative, less inventive suggestions | Not a capability loss, a sampling outcome |
| Verbosity | More caveats and disclaimers than usual | Normal variance in token probabilities |

### What This Is NOT

- **Not a model downgrade**: Anthropic versions models deliberately and documents changes. Day-to-day variance happens within the same model version.
- **Not a bug to report**: This behavior is expected and documented in LLM literature. It is inherent to probabilistic inference.
- **Not permanent**: The next session will likely behave differently. A "bad" run does not indicate a lasting change.
- **Not context window degradation**: That is a within-session phenomenon caused by token accumulation. This is between-session variance on fresh starts.

> The Aug-Sep 2025 incident ([see Resolved Issues above](#model-quality-degradation-aug-sep-2025)) was the exception: Anthropic confirmed actual infrastructure bugs causing systematic degradation. True systematic degradation is rare and Anthropic investigates it. Normal session-to-session variance is something else.

### Mitigation Strategies

**Constrain the prompt**: More specific prompts reduce the output space and make variance less noticeable. "Write a function that does X, Y, Z, returns type T, handles edge case E" produces more consistent outputs than "write me something to handle X."

**Fresh context before important work**: Run `/clear` before a high-stakes task. Accumulated session noise from earlier exploratory work can skew subsequent outputs even within the same session.

**Reformulate and retry**: If an output seems off compared to your expectations, try the same request with different framing. A second formulation often routes through different expert paths and produces a better result.

**Compare against a known-good prompt**: If you have a prompt from a previous session that produced excellent output, use it as a reference. If today's version of that prompt produces visibly worse output consistently, that warrants closer investigation (and potentially a GitHub issue if reproducible).

**Calibrate expectations by task type**: Deterministic tasks (regex, simple transforms, well-defined algorithms) show less variance than creative or judgment-heavy tasks. Use Claude Code for the former with high reliability; for the latter, build review steps into your workflow.

---

## 📊 Issue Statistics (as of Jan 28, 2026)

| Metric | Count | Source |
|--------|-------|--------|
| **Open issues** | 5,702 | [GitHub API](https://github.com/anthropics/claude-code) |
| **Issues labeled "invalid"** | 527 | GitHub Issues search |
| **"Wrong repo" issues (confirmed)** | 17+ | Manual search Jan 2026 |
| **Token consumption reports (Dec-Jan)** | 20+ | Issue search |
| **Active releases** | 80+ | GitHub Releases |

---

## 🔍 How to Track Issues

### Check Open Critical Issues

```bash
# Most reacted-to issues (community priority)
gh issue list --repo anthropics/claude-code --state open --sort reactions-+1 --limit 20

# Recent critical bugs
gh search issues --repo anthropics/claude-code "bug" "critical" --sort created --order desc --limit 10
```

### Monitor Specific Topics

- **Token consumption**: [Search](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+excessive+token)
- **Wrong repo creations**: [Search](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+%22wrong+repo%22)
- **Model quality**: [Search](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+quality+degradation)

### Official Channels

- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Anthropic Status**: https://status.anthropic.com/
- **Engineering Blog**: https://www.anthropic.com/engineering
- **Discord**: https://discord.gg/anthropic (invite-only, check website)

---

## 📝 Contributing to This Document

This document tracks **verified, high-impact issues only**. Criteria for inclusion:

- **Verified**: Issue exists in GitHub with multiple reports OR official Anthropic acknowledgment
- **High-impact**: Affects security, privacy, cost, or core functionality
- **Actionable**: Workarounds or official response available

To suggest updates: Open issue in [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues) with:
- Link to GitHub issue
- Evidence of impact (multiple reports, official response)
- Suggested workaround if available

---

**Disclaimer**: This document is community-maintained and not affiliated with Anthropic. Information is provided as-is. Always verify current status via official channels before making decisions.
