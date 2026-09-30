# Evaluation: "Claude Code Hidden Feature" social media post

**Date**: 2026-01-27
**Evaluator**: Claude Sonnet 4.5
**Source Type**: Copied text (unsourced social media post)
**Verdict**: ❌ **REJECTED** (Score: 1/5)

---

## Summary

Social media post claiming Claude Code has a "hidden feature" for parallel agent execution, using aggressive marketing language and creating artificial FOMO. Post lacks citations and presents publicly documented features as "secrets."

---

## Content summary

- **Main claim**: "Hidden feature" enables automatic spawning of parallel agents like a "team"
- **Mechanism described**: Feature flag that automatically creates agents for each task
- **Tone**: Marketing hyperbole ("retourne internet", "tu passes à côté d'un truc énorme")
- **Call to action**: "Find the flag with Perplexity"
- **Sources cited**: None

---

## Fact-check results

| Claim | Verified | Official Source | Verdict |
|-------|----------|-----------------|---------|
| "Hidden feature" | ❌ **FALSE** | [CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2116---2026-01-22) | **Public** since Jan 2026 |
| "Tasks → auto-spawn agents" | ⚠️ **PARTIALLY TRUE** | [Tasks API docs](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | Sub-agents exist, not automatic |
| "CLAUDE_CODE_ENABLE_TASKS flag" | ✅ **TRUE** | [v2.1.19 release](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2119---2026-01-25) | Migration flag (revert), not activation |
| "Team coordination" | ⚠️ **PARTIALLY TRUE** | [TeammateTool gist](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea) | Real but experimental, not "hidden" |
| "Retourne internet" / "Prendre de l'avance" | ❌ **MARKETING LIES** | N/A | Unverifiable hyperbole |

### Factual corrections

**What is TRUE (and already officially documented):**

1. **Tasks API** (v2.1.16+): Task management with dependencies - [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2116---2026-01-22)
2. **Parallel sub-agents**: `Task` tool spawns independent agents - [Docs](https://code.claude.com/docs/en/sub-agents)
3. **TeammateTool**: Multi-agent orchestration (real, not hidden) - [Community gist](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea)
4. **CLAUDE_CODE_ENABLE_TASKS=false**: Migration flag to **disable** new system - [v2.1.19](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2119---2026-01-25)

**What is FALSE:**

- ❌ Not "hidden" → Documented since v2.1.16 (Jan 22, 2026)
- ❌ Not recent → Released 5 days ago at evaluation time
- ❌ Flag doesn't "unlock" → It reverts to old system
- ❌ Not exclusive → Available to all Claude Code users

---

## Scoring & decision

### Score: 1/5 ❌ - REJECT

**Rationale:**

1. **Fundamental dishonesty**: Presents public features as "hidden"
2. **FOMO creation**: Manipulative language designed to create urgency
3. **Zero sources**: No official citations = massive red flag
4. **Contradicts guide principles**: "Accuracy over marketing" (RULES.md line ~350)
5. **Zero documentary value**: All true facts already in CHANGELOG

**Why rejection is important:**

This guide has 15K+ lines and 66+ templates built on rigorous sourcing. **One low-quality source can contaminate credibility.** Readers must trust 100% of cited sources.

### What would have justified score 3+:

- ✅ Cite official CHANGELOG
- ✅ Professional, factual tone
- ✅ Pedagogical explanation (how/why use feature)
- ✅ Mention limitations and use cases
- ✅ Distinguish "experimental" from "stable" features

---

## Comparative analysis

| Aspect | This Source | Our Guide (v3.15.0) | Gap? |
|--------|-------------|---------------------|------|
| **Tasks API (v2.1.16+)** | ⚠️ "Hidden" (false) | ✅ Documented (line 3200-3500) | No |
| **CLAUDE_CODE_ENABLE_TASKS** | ⚠️ Presented as "activation" | ✅ Documented (line 3213) | No |
| **Sub-agents parallel** | ⚠️ "Feature flag" | ✅ Documented (Task tool) | No |
| **TeammateTool** | ❌ Not mentioned | ❌ **GAP IDENTIFIED** | ✅ **YES** |
| **Swarm mode** | ❌ Not mentioned | ❌ **GAP IDENTIFIED** | ✅ **YES** |
| **Professional tone** | ❌ Marketing hyperbole | ✅ Factual & sourced | - |

### Real gaps identified (independent of source)

Despite this source's low quality, it revealed two real gaps in our guide:

1. **TeammateTool**: Real experimental feature not yet documented
   - Confirmed by: [Community gist](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea), [GitHub Issue #3013](https://github.com/anthropics/claude-code/issues/3013)
   - Status: Partially feature-flagged, usable but unstable

2. **Swarm mode / claude-sneakpeek**: Parallel build enabling unreleased features
   - Source: [GitHub mikekelly/claude-sneakpeek](https://github.com/mikekelly/claude-sneakpeek)
   - Status: Unofficial method, unknown risks

---

## Technical writer agent challenge

**Score adjustment**: 3/5 → 1/5 (challenge accepted)

**Key arguments from technical-writer agent:**

1. **"Score 3/5 too generous"** → "Fundamentally dishonest. Reject."
2. **"Negative pedagogical value"** → "Teaches bad practices: seek secrets vs read docs"
3. **"Zero documentary value"** → "All facts already in CHANGELOG. Adds nothing."
4. **"Test: remove marketing → what remains?"** → "Public facts. Value = 0."
5. **"Risk of precedent"** → "Next step: integrate unsourced Reddit threads?"

**Question returned**: *"Why hesitate to reject? Pressure to 'cover everything' even low quality?"*

**Answer**: No pressure. Standard applied: accuracy over coverage. This source fails quality bar.

---

## Actions taken

### ❌ Not integrated

- Did NOT cite this source in guide
- Did NOT create "Hidden Features" section (reinforces myth)
- Did NOT legitimize low-quality social media content

### ✅ Improvements made (independent of source)

1. **Added TeammateTool documentation**
   - Location: `guide/ultimate-guide.md` line 3294
   - Content: Experimental status, capabilities, limitations, official sources
   - Warning: Unstable, no official support

2. **Created "Myths vs Reality" appendix**
   - Location: `guide/ultimate-guide.md` line 15257 (Appendix D)
   - Sections:
     - ❌ Myth: "Hidden features unlockable with flags"
     - ❌ Myth: "Tasks API = autonomous agents"
     - ❌ Myth: "100x faster than competitors"
     - ✅ Reality: What makes Claude Code actually special
     - How to spot reliable information

3. **Enhanced cheatsheet visibility**
   - Location: `guide/cheatsheet.md` after "File References"
   - Section: "Features Méconnues (But Official!)"
   - Lists: Tasks API, Background Agents, TeammateTool, Session Forking, LSP Tool
   - Pro tip: "Read the CHANGELOG—these aren't secrets!"

4. **Updated machine-readable index**
   - Location: `machine-readable/reference.yaml`
   - Added: TeammateTool (line 3294), Appendix D (line 15257)
   - Added: Myths sections with line numbers

---

## Research sources used

### Official

- [Claude Code CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2116---2026-01-22)
- [Claude Code CHANGELOG v2.1.19](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md#2119---2026-01-25)
- [Claude Code Docs - Sub-Agents](https://code.claude.com/docs/en/sub-agents)

### Community (reliable)

- [kieranklaassen - TeammateTool Complete Guide (Gist)](https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea)
- [GitHub Issue #3013 - Parallel Agent Execution](https://github.com/anthropics/claude-code/issues/3013)
- [mikekelly/claude-sneakpeek (GitHub)](https://github.com/mikekelly/claude-sneakpeek)
- [Tim Dietrich - Parallel Subagents](https://timdietrich.me/blog/claude-code-parallel-subagents/)
- [Medium - Multi-agent parallel coding](https://medium.com/@codecentrevibe/claude-code-multi-agent-parallel-coding-83271c4675fa)

### Search engines used

- **Perplexity Search**: "Claude Code CLAUDE_CODE_ENABLE_TASKS feature flag parallel agents 2026"
- **Google WebSearch**: "site:github.com anthropics/claude-code TeammateTool"
- **WebFetch**: Official CHANGELOG, TeammateTool gist, claude-sneakpeek repo

---

## Final decision

- **Score**: 1/5 ❌
- **Action**: **REJECT** - Do not integrate
- **Confidence**: Very High (rigorous fact-check completed)
- **Documentary value**: Zero
- **Gaps identified**: TeammateTool + Swarm mode (worth documenting with **official sources only**)

### Principle applied

From RULES.md line ~350:

> **No Marketing Language**: Never use "blazingly fast", "100% secure", "magnificent", "excellent"

This source violates our core editorial principle. Rejection maintains guide integrity.

---

## Recommendation for future

**Red flags checklist** (signs of misinformation):

- ❌ "Hidden feature that will blow your mind!"
- ❌ "Secret trick devs don't want you to know"
- ❌ No official source citations
- ❌ FOMO language: "falling behind if not using"
- ❌ Dramatic claims without evidence

**Trusted sources checklist**:

- ✅ Official [Claude Code docs](https://code.claude.com/docs)
- ✅ [GitHub CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- ✅ GitHub Issues with Anthropic staff responses
- ✅ Community resources citing official sources
- ✅ This guide (14+ evaluated resources, clear sourcing)

**Moral**: Truth > Hype. Accuracy > Coverage. Official sources > Rumors.

---

**Evaluation completed**: 2026-01-27
**Result**: Improved guide quality by rejecting low-quality source while documenting real gaps with proper sources.
