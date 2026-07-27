# Evaluation: crit - Human-in-the-Loop Review Interface for AI Agents

**Resource Type**: Open Source CLI Tool
**Author**: Tomasz Tomczyk (@tomasz-tomczyk)
**Date**: 2026-06-09 (v0.16.2)
**URL**: https://github.com/tomasz-tomczyk/crit
**Evaluation Date**: 2026-06-10
**Evaluator**: Claude Sonnet 4.6

---

## 1. Content Summary

`crit` is a local review interface designed to sit between a developer and an AI agent. It provides an adaptive UI for reviewing AI-generated output across four modes:

- **Markdown/plan files**: Rendered with inline line-or-range comments before the agent executes
- **Git diffs**: Split/unified view with round-to-round comparison (delta between agent iterations, not just commits)
- **Live web apps**: Proxies a running local server and injects a DOM-anchoring overlay for spatial comments mapped back to source
- **Static HTML**: Direct render with the same overlay system

The loop: agent produces output → developer opens crit → leaves inline comments → agent reads those comments → crit shows what changed round-to-round.

**Key features**:
- Live threads (continuous back-and-forth conversation attached to a specific line, not one-shot)
- `crit comment src/file.go:42 'message'`: programmatic CLI for agents to inject their own notes
- `POST /api/agent/request`: HTTP endpoint for agents to push review requests to the human
- GitHub PR bidirectional sync (read/write PR comments via `gh` CLI)
- `crit install claude-code`: first-class Claude Code integration (writes project config snippets)
- Async shareable review URLs for remote collaboration

**Tech stack**: Go 1.26+ backend, JS/TS frontend embedded in binary. No database, no cloud, no telemetry.

---

## 2. Initial Scoring: 4/5 (High Value)

| Score | Meaning | Action |
|-------|---------|--------|
| 5 | Critical: integrate immediately | < 24h |
| **4** | **High Value: major improvement** | **< 1 week** |
| 3 | Moderate: useful addition | When time available |
| 2 | Marginal: minimal mention or skip | - |
| 1 | Low: reject | - |

### Justification

**Strengths**:
- Direct Claude Code integration (`crit install claude-code` is a documented first-class command)
- Fills a genuine gap: no existing tool shows round-to-round diffs within an AI session
- DOM-anchored spatial comments for live web apps, with no equivalent in standard PR tooling
- Active maintenance: 477 stars, v0.16.2 shipped June 9 2026, 665 total commits
- MIT license, no telemetry, no cloud dependency
- The CLAUDE.md in the repo is a symlink to AGENTS.md, meaning the maintainer understands Claude Code conventions
- Addresses a friction pattern that shows up in Claude Code sessions: "how do I give structured feedback on a plan before Claude executes it?"

**Why 4/5 and not 5/5**:
- Single maintainer (bus factor), contributor depth unclear
- `live` mode is explicitly marked "feedback wanted", not yet stable
- Go 1.26+ build requirement (may cause issues building from source)
- No visible test suite in README
- Documentation functional but thin (no dedicated docs site)

---

## 3. Technical Analysis

### Round-to-Round Diffing: The Unique Value

Standard diff tools (GitHub PRs, `git diff`, IDE diffs) show delta between commits or branches. `crit` shows delta between agent iterations within the same review session. That specific capability does not exist in any other tooling short of manual bookmarking.

For Claude Code users specifically: when you run Claude multiple times on the same task and want to understand "what did it change from attempt 2 to attempt 3?", `crit` gives a structured answer.

### Plan Review Before Execution

The markdown mode enables reviewing `plan.md` or similar files inline before the agent proceeds. Without `crit`, this requires manually opening the file and passing feedback through the prompt. With `crit`, comments are attached to specific lines and readable by the agent via the CLI comment API.

### GitHub PR Sync

`crit` can read and write GitHub PR review comments bidirectionally via `gh` CLI. This bridges the loop: Claude Code opens a PR, reviewer leaves inline comments in `crit`, those comments sync to the PR, Claude Code reads them via the PR context.

---

## 4. Maturity Signals

| Signal | Value |
|--------|-------|
| Stars | 477 (now 834 as of 2026-07-28) |
| Forks | 36 |
| Open issues | 7 (6 feature requests, 1 bug) |
| Latest release | v0.16.2, 2026-06-09 |
| Total commits | 665 |
| License | MIT |
| Topics | `ai-agents`, `llm`, `agentic-coding`, `code-review`, `cli`, `developer-tools` |

The issue queue is healthy: one recent bug (`@` filename handling, minor), the rest are scoped feature requests with "help wanted" labels. Release cadence is active.

---

## 5. Installation

```bash
# Homebrew (macOS/Linux)
brew install crit

# Go
go install github.com/tomasz-tomczyk/crit@latest

# Binary, Nix, Docker also available
```

**Basic usage**:
```bash
crit                          # Auto-detects uncommitted changes in repo
crit plan.md                  # Review a specific file before agent executes
crit http://localhost:3000    # Proxy and review a running web app
crit landing.html             # Review static HTML with spatial comments

# Claude Code integration setup
crit install claude-code      # Writes config snippets into the project
```

---

## 6. Relevance to Claude Code Users

**Direct and explicit**. The tool is built for this workflow:

- `crit install claude-code` configures it for Claude Code sessions out of the box
- The HTTP API (`/api/agent/request`) is designed for Claude Code to be the receiving agent
- Round-to-round diffs map directly to how Claude Code iterates on the same task across multiple runs
- PR sync bridges the gap between Claude Code-opened PRs and structured human review

For guide readers: `crit` addresses a friction point that comes up in multi-iteration Claude Code sessions. The current guide covers plan review and feedback patterns, but has no tooling recommendation for structured inline review with round-to-round comparison. This fills that gap.

---

## 7. Red Flags

No serious issues. Minor notes:

- **Single maintainer**: Active and engaged, but bus factor is real at 477 stars
- **Go 1.26+ to build from source**: Homebrew/binary installs are unaffected; build-from-source users may hit this
- **Live mode not stable**: Issue #557 explicitly labels it as seeking community feedback
- **One open bug**: `@` in filenames (#656, 2 weeks old, unresolved but scoped)
- **No test suite visible in README**: No CI badge or test command documented
- **`agent_cmd` is global-only**: Deliberate security decision (prevents malicious repos hijacking your agent), but limits per-project agent configuration

No security concerns. No telemetry. No supply chain issues visible.

---

## 8. Integration Decision

**INTEGRATE** at score **4/5**: mention in the guide under human-in-the-loop and review tooling.

**Where to integrate**:
- Section covering agentic workflows and human oversight patterns (the guide section on iteration and review)
- Third-party tools ecosystem section
- Potentially: a callout in the multi-agent / plan review workflow sections

**Format**: Short mention with link and what it uniquely solves (round-to-round diffs, plan review before execution, DOM-anchored web review). No need to document the full feature set, just link to the GitHub repo. One-liner pitch: "structured inline review interface between you and Claude Code, with round-to-round diffs across iterations."

**Not a priority over core guide work**, but a clean addition during the next third-party tools pass.

---

## 9. Final Metadata

**Score**: 4/5
**Decision**: Integrate
**Confidence**: High

**Next action**: Add mention in third-party tools / agentic workflow sections on next guide update pass.

**Archive**: `docs/resource-evaluations/crit-human-in-loop-review.md`
