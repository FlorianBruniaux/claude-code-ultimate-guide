---
title: "Known Issues & Critical Bugs"
description: "Verified critical issues affecting Claude Code users from community reports and official communications"
tags: [reference, security, debugging]
---

# Known Issues & Critical Bugs

This document tracks verified, critical issues affecting Claude Code users based on community reports and official communications.

> **Last Updated**: January 28, 2026
> **Source**: [GitHub Issues](https://github.com/anthropics/claude-code/issues) + [Anthropic Official Communications](https://www.anthropic.com/engineering)

---

## 🚨 Active Critical Issues

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

Claude's output quality can vary noticeably from session to session, even with identical prompts and a clean context window. This is distinct from context window degradation (which happens within a session as context fills up). This is about variance between fresh sessions.

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
