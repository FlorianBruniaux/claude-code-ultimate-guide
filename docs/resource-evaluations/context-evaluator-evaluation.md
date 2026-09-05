# context-evaluator Evaluation

**Resource**: context-evaluator — AI-powered CLAUDE.md / AGENTS.md quality analyzer
**Source**: [github.com/PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator)
**Web app**: [context-evaluator.ai](https://context-evaluator.ai)
**Author**: Packmind engineering team
**License**: MIT
**Evaluated**: 2026-04-16

---

## Score: 4/5 (High Value)

**Decision**: Integrate — add to `guide/ecosystem/third-party-tools.md` (Configuration Quality section) and extract 2 patterns to `guide/core/skill-design-patterns.md`.

---

## What It Is

context-evaluator analyzes CLAUDE.md and AGENTS.md files using 17 specialized AI evaluators (13 error + 4 suggestion categories). Available as:

- Zero-install web app at context-evaluator.ai (paste a GitHub URL or upload a file)
- Pre-compiled binary for macOS/Linux/Windows (no runtime dependencies)
- Source install (Bun/TypeScript)

Evaluation takes 1-3 minutes. Outputs a scored report with severity levels (Critical/High/Medium/Low) and specific fix recommendations. An automated remediation feature produces a `.patch` file for AI-generated improvements.

---

## Scoring Breakdown

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Relevance to CC users | 5/5 | Directly evaluates the primary Claude Code config artifact (CLAUDE.md) |
| Novelty vs. guide | 4/5 | LLM-based CLAUDE.md evaluation not covered; Caliber is deterministic only |
| Technical quality | 4/5 | MIT, Bun/TypeScript, test coverage, pre-built binaries, 37KB CLAUDE.md |
| Actionability | 5/5 | Zero-install web version + automated patch generation |
| Engineering patterns | 4/5 | 2 new patterns not in guide: Runtime Prompt Logging, Adaptive Unified/Parallel Mode |

**Overall: 4/5**

---

## Technical Patterns Identified (Source Read)

### Pattern 1: Runtime Prompt Logging (`runtime-prompt-logger.ts`)

**Always-on blocking write to disk BEFORE the AI provider call.** Not a debug flag — every prompt is saved to `prompts/debug/` with an ISO-8601 timestamp filename, regardless of `--debug` flag state. The write is `await writeFile()` (blocking). If the provider call crashes or times out, the exact prompt is already on disk.

Key design decisions:
- Blocking write (not fire-and-forget): ensures the file exists before the AI call starts
- Never throws: logging failures log a warning and return `null` but do not break evaluations
- Separate from `--debug` (which saves to `{workingDir}/debug-output/`): this persists forever and is always active

**Not in guide currently.** The guide covers `--debug` flag usage but does not name "write-before-invoke" as a design pattern for evaluator skills.

### Pattern 2: Adaptive Unified/Parallel Mode (`runner.ts:764-775`)

**Token-threshold switching between single-agent and parallel-agent execution.** Before launching evaluators, the system estimates the combined token count of all input files. If below 100K tokens (`DEFAULT_MAX_UNIFIED_TOKENS`), all files are evaluated in a single unified agent call that can detect cross-file contradictions. If above, each file is evaluated by independent parallel agents.

```typescript
export function canUseUnifiedMode(
  context: MultiFileContext,
  maxTokens: number = DEFAULT_MAX_UNIFIED_TOKENS,
): { viable: boolean; reason?: string } {
  if (context.totalTokenEstimate > maxTokens) {
    return {
      viable: false,
      reason: `Combined file content (~${context.totalTokenEstimate} tokens) exceeds limit (${maxTokens} tokens)`,
    };
  }
  return { viable: true };
}
```

**Not explicitly named in guide.** The guide discusses parallel sub-agents and multi-file evaluation but does not document the "check token count, choose 1-agent vs N-agent" switching pattern with a concrete threshold.

### Pattern 3: Technical Inventory Injection (`context-identifier.ts`)

CLOC + folder structure + `ls -la` analysis are collected first, then injected as structured context into all 17 evaluator prompts. Similar to Shared Ground Truth Injection (already documented in v3.39.0 `skill-design-patterns.md`). **No new documentation needed**: this is a variant of a pattern already covered.

### Pattern 4: Multi-layer deduplication

Three-phase pipeline: rule-based clustering (location tolerance + text similarity) → AI semantic deduplication → impact curation. Interesting but specific to evaluation systems. Low value to general CC users, skip.

---

## Integration Decisions

| Item | Decision | Rationale |
|------|----------|-----------|
| Tool mention in `third-party-tools.md` | Add | Directly useful, zero-install, higher value than Caliber for LLM-based review |
| Runtime Prompt Logging in `skill-design-patterns.md` | Add | New pattern, 1 concrete implementation point |
| Adaptive Unified/Parallel Mode in `skill-design-patterns.md` | Add | Concrete threshold-based decision not documented elsewhere |
| Technical Inventory Injection | Skip | Variant of Shared Ground Truth (already in guide v3.39.0) |
| Multi-layer deduplication | Skip | Too specific to evaluation pipelines |
| Entry in `credits.md` | Add | Packmind repo, MIT license |

---

## Delta vs Caliber (in guide)

| Feature | Caliber | context-evaluator |
|---------|---------|-------------------|
| No AI provider required | Yes | No |
| Scoring rubric (0-100) | Yes | No |
| Git drift detection | Yes | No |
| LLM-based content review | No | Yes (17 evaluators) |
| Cross-file analysis | No | Yes |
| Automated remediation (patch) | No | Yes |
| Zero-install (web) | No | Yes |

context-evaluator and Caliber are complementary, not competitive. The guide should present them as options for different needs.

---

## Limitations

- Requires AI provider (Claude Code, Cursor, OpenCode, GitHub Copilot, Codex)
- Processing takes 1-3 minutes per run
- No deterministic scoring rubric for CI gates
- No git-based drift detection
- Very new tool (launched 2026, Packmind experimental project)

---

## Files Modified

- `docs/resource-evaluations/context-evaluator-evaluation.md` (this file)
- `guide/ecosystem/third-party-tools.md` — new context-evaluator entry (Configuration Quality section)
- `guide/core/skill-design-patterns.md` — 2 new patterns: Runtime Prompt Logging, Adaptive Unified/Parallel Mode
- `guide/core/credits.md` — new entry for context-evaluator (MIT, Packmind)
- `machine-readable/reference.yaml` — new entries
- `CHANGELOG.md` — [Unreleased] entry
