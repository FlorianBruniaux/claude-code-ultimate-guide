# Resource Evaluation: ClaudeKit

**Resource**: [carlrannaberg/claudekit](https://github.com/carlrannaberg/claudekit)
**Type**: npm package / CLI wrapper
**Evaluation Date**: 2026-02-02
**Evaluator**: Automated analysis + manual review
**Decision**: Patterns extracted, tool not mentioned

---

## Quick Facts

| Metric | Value |
|--------|-------|
| Stars | 571 |
| Forks | 94 |
| License | MIT |
| Language | TypeScript |
| Created | July 2025 |
| Last Activity | January 2026 |
| npm Package | `claudekit` |
| Requirements | Node 20+ |

---

## Score Summary

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| **Accuracy** | 4/5 | 30% | 1.20 |
| **Depth** | 2/5 | 25% | 0.50 |
| **Practicality** | 3/5 | 20% | 0.60 |
| **Uniqueness** | 2/5 | 15% | 0.30 |
| **Maintainability** | 2/5 | 10% | 0.20 |
| **TOTAL** | **2.8/5** | 100% | **2.8** |

**Final Score**: **3/5** (Moderate Value - rounded up for actionable patterns)

---

## What ClaudeKit Is

ClaudeKit is an npm wrapper around Claude Code that:
- Provides 32 pre-built subagent templates
- Implements checkpoint management via git stash
- Adds validation pipeline hooks (typecheck, lint, test)
- Implements file protection via `.agentignore`
- Adds spec-driven development commands
- Provides codebase-map DSL for static context injection
- Includes "thinking-level" hook (megathink/ultrathink keywords)

**Core idea**: Automate common patterns that Claude Code supports but doesn't configure by default.

---

## Scoring Breakdown

### Accuracy: 4/5

**What's correct**:
- Git stash as checkpoint mechanism ✅
- PreToolUse/PostToolUse hook patterns ✅
- File protection concept ✅
- Validation pipeline concept ✅

**What's incorrect**:
- The "thinking-level" hook is **factually obsolete** since Opus 4.5 (thinking is always-on, keywords are cosmetic)
- Codebase-map contradicts Claude Code's "Search Don't Index" architecture

**Verdict**: Mostly accurate concepts, but 2 significant errors.

### Depth: 2/5

**Shallow areas**:
- 32 subagents are one-liners ("You are a Rust expert")
- No discussion of hook failure modes, performance, or edge cases
- No explanation of when to use checkpoints vs branches
- No async vs sync hook guidance

**Verdict**: Breadth over depth. Useful patterns but superficial explanations.

### Practicality: 3/5

**Practical**:
- Checkpoint workflow is immediately usable ✅
- Hooks are functional templates ✅
- npm install makes setup easy ✅

**Impractical**:
- Requires npm global install (dependency)
- Breaks if package is abandoned or has breaking changes
- Codebase-map adds 9K+ static context (token waste)

**Verdict**: Good for rapid prototyping, risky for long-term use.

### Uniqueness: 2/5

**Not unique**:
- Hooks are documented in our guide (Section 7)
- Subagents are covered in Section 9.18
- Spec-driven dev is in methodologies.md

**Unique**:
- Automated checkpoint on Stop event (we didn't have this)
- Unified file-guard with bypass detection (we had pieces, not unified)
- Test-on-change with smart detection (we didn't automate this)

**Verdict**: 70% overlap with existing guide, 30% novel automation.

### Maintainability: 2/5

**Concerns**:
- Last activity: January 2026 (recent but slowing?)
- Thinking-level hook already obsolete (shows maintenance lag)
- npm wrapper creates dependency on third-party package
- Breaking changes in Claude Code could break ClaudeKit

**Verdict**: Maintenance risk for long-term projects.

---

## What We Already Cover Better

| Topic | Our Guide | ClaudeKit | Winner |
|-------|-----------|-----------|--------|
| Hooks (all events) | Section 7 (775 lines, 25 templates) | Wrapper with JSON config | **Guide** |
| Subagents | Section 9.18 (650 lines, 6 deep templates) | 32 shallow templates | **Guide** |
| Spec-driven dev | methodologies.md (824 lines) | 4 commands (spec:create/validate/decompose/execute) | **Guide** |
| Multi-agent review | Pat Cullen workflow + convergence loop | 6 parallel agents (basic) | **Guide** |
| Architecture | architecture.md (complete) | None | **Guide** |
| Thinking levels | Accurate post-Opus 4.5 (line 9303) | Obsolete megathink hook | **Guide** |

**Takeaway**: ClaudeKit is a shortcuts layer over concepts we already document more thoroughly.

---

## 3 Gaps Identified (Actionable)

### Gap 1: Auto-Checkpoint Workflow ⭐ HIGH PRIORITY

**What ClaudeKit does**:
- Stop hook that auto-creates git stash on session end
- Naming: `claude-checkpoint-{branch}-{timestamp}`
- Slash commands: `/checkpoint:create`, `/checkpoint:restore`, `/checkpoint:list`

**What we were missing**:
- Hook template for auto-checkpoint
- Structured workflow: create → experiment → restore
- Checkpoint vs branching guidance

**Action taken**:
- ✅ Created `examples/hooks/bash/auto-checkpoint.sh`
- ✅ Added Section 2.4 "Checkpoint Pattern" (~40 lines)
- ✅ Documented when to use checkpoints vs branches

**Impact**: Enables safe experimentation without branch overhead.

---

### Gap 2: Validation Pipeline Hook ⭐ MEDIUM PRIORITY

**What ClaudeKit does**:
- Separate PostToolUse hooks for typecheck, lint, test
- Run automatically after each Edit/Write

**What we were missing**:
- Hook template for `typecheck-on-save.sh`
- Hook template for `test-on-change.sh` (with smart test file detection)
- Pattern for chaining validation steps

**Action taken**:
- ✅ Created `examples/hooks/bash/typecheck-on-save.sh`
- ✅ Created `examples/hooks/bash/test-on-change.sh`
- ✅ Added Section 7.5 "Validation Pipeline Pattern" (~80 lines)

**Impact**: Immediate feedback loop for code quality without manual test runs.

---

### Gap 3: File Protection Unified ⭐ MEDIUM PRIORITY

**What ClaudeKit does**:
- `.agentignore` file with gitignore syntax
- 195 default patterns
- Bash variable expansion detection

**What we were missing**:
- Unified strategy combining permissions.deny + hooks + .agentignore
- Sophisticated bypass detection (variable expansion, command substitution)
- Complete template with all 3 layers

**Action taken**:
- ✅ Created `examples/hooks/bash/file-guard.sh`
- ✅ Added Section 7.4 "File Protection Strategy" (~90 lines)
- ✅ Cross-referenced security-hardening.md

**Impact**: Defense-in-depth file protection with bypass detection.

---

## What We're Ignoring (Deliberately)

| ClaudeKit Feature | Why We Skip |
|-------------------|-------------|
| Codebase-map (DSL/tree inject) | Anti-pattern for Claude Code's "Search Don't Index" architecture. Static 9K context is token waste. |
| AGENTS.md migration tool | Already covered in ai-ecosystem.md:1260. Simple `ln -s` suffices. npm tooling is overkill. |
| 32 pre-built subagents | Shallow one-liners. Our 6 templates (Section 9.18) are deeper and more pedagogical. |
| Oracle (GPT-5 integration) | Out of scope - we document Claude Code, not bridges to other LLMs. |
| STM (Simple Task Master) | Claude Code has TodoWrite/TaskCreate natively. STM is redundant layer. |
| Dev cleanup command | Trivial - `find . -name "*.tmp" -delete` doesn't need a section. |
| npm install global | We document patterns, not packages. Survives tool abandonment. |

**Rationale**: Extract patterns, ignore implementation details that couple to a specific package.

---

## Recommendation: Patterns Not Package

**Do NOT mention ClaudeKit in the guide**. Reasons:

1. **Maintenance risk**: Package can become abandonware (last activity: Jan 2026)
2. **Obsolete features**: Thinking-level hook already outdated (proves shaky maintenance)
3. **Anti-patterns**: Codebase-map contradicts Claude Code architecture
4. **Dependency coupling**: npm package creates fragile dependency
5. **We're better**: Our docs survive package deprecation

**Instead**: Implement the 3 gaps as **original content** inspired by patterns (not by tool).

---

## Integration Strategy

### Files Modified

| File | Change | Lines | Status |
|------|--------|-------|--------|
| `examples/hooks/bash/auto-checkpoint.sh` | CREATE | 40 | ✅ Done |
| `examples/hooks/bash/typecheck-on-save.sh` | CREATE | 35 | ✅ Done |
| `examples/hooks/bash/test-on-change.sh` | CREATE | 45 | ✅ Done |
| `examples/hooks/bash/file-guard.sh` | CREATE | 60 | ✅ Done |
| `guide/ultimate-guide.md` Section 2.4 | EDIT +40 | +40 | ✅ Done |
| `guide/ultimate-guide.md` Section 7.4 | EDIT +90 | +90 | ✅ Done |
| `guide/ultimate-guide.md` Section 7.5 | EDIT +80 | +80 | ✅ Done |
| `docs/resource-evaluations/claudekit-evaluation.md` | CREATE | 90 | ✅ Done (this file) |

**Total impact**: +4 hook templates, +210 lines guide content, structured evaluation.

---

## Verification Checklist

- [x] 4 new hook scripts created
- [x] All scripts are executable (`chmod +x`)
- [x] Section numbering preserved (2.4, 7.4, 7.5)
- [x] Cross-references added (security-hardening.md)
- [x] Templates count increased by 4
- [ ] Landing sync check (if template count matters)
- [ ] Version bump check (if content change warrants)

---

## References

- **Source**: https://github.com/carlrannaberg/claudekit
- **npm**: https://www.npmjs.com/package/claudekit
- **License**: MIT
- **Related Guide Sections**:
  - Section 2.4: Rewind & Checkpoint
  - Section 7.4: Security Hooks (File Protection)
  - Section 7.5: Hook Examples (Validation Pipeline)
  - security-hardening.md: Full security hardening guide

---

## Changelog

**2026-02-02**: Initial evaluation
- Scored 3/5 (Moderate Value)
- Identified 3 actionable gaps
- Implemented all 3 gaps as original content
- Decision: Extract patterns, don't mention tool
