# Evaluation: agent-trace (Siddhant-K-code/agent-trace)

**Date**: 2026-03-16
**Source**: https://github.com/Siddhant-K-code/agent-trace
**Type**: GitHub repository (Python tool)
**Evaluator**: Claude (eval-resource skill)

---

## Summary

`agent-trace` (pip package: `agent-strace`) is a Python tool — zero dependencies, stdlib only — that captures every tool call, user prompt, and assistant response in Claude Code via hooks, then lets you replay sessions in the terminal or export as OpenTelemetry spans. Created 2026-03-15. 7 stars at time of evaluation.

The "strace for AI agents" framing is apt: it solves the "my agent modified 47 files and I have no idea why" problem by giving you a time-stamped, replayable record of every decision point.

---

## Key Points

- **Claude Code hooks**: Setup via `agent-strace setup`. Registers PreToolUse, PostToolUse, PostToolUseFailure, UserPromptSubmit, Stop, SessionStart, SessionEnd in `.claude/settings.json`
- **Session replay**: `agent-strace replay` shows full session with timestamps, durations, tool inputs, errors — the missing layer between JSONL and understanding
- **MCP proxy**: Wraps any MCP server (stdio or HTTP/SSE). Works with Cursor, Windsurf, any MCP client
- **OpenTelemetry export**: OTLP output → Datadog, Honeycomb, New Relic, Splunk
- **Python decorator API**: `@trace_tool`, `@trace_llm_call`, `log_decision()` for custom agents
- **Secret redaction**: `--redact` flag strips OpenAI, GitHub, AWS, Anthropic, Slack, JWTs, Bearer tokens, connection strings

---

## Relevance Score: 2/5

**Pertinent but too immature for immediate integration.**

The session replay angle is real and not covered by existing tools in the guide. But `claude-code-otel` already handles the OTel export use case, and the manual jq queries at `guide/ops/observability.md:519-550` cover most of the audit use case. The unique differentiator — interactive replay — needs production validation before being recommended to readers.

---

## Comparison vs Current Guide Coverage

| Aspect | agent-trace | Guide coverage |
|--------|-------------|----------------|
| Manual JSONL audit (jq) | ✅ Abstracted as CLI | ✅ observability.md:520 |
| Session replay (visual) | ✅ Unique differentiator | ❌ Not covered |
| OpenTelemetry export | ✅ OTLP | ✅ claude-code-otel already in table |
| Hook setup automation | ✅ `agent-strace setup` | ✅ Documented manually |
| MCP proxy (Cursor/Windsurf) | ✅ stdio + HTTP/SSE | ❌ Not covered |
| Python decorator API | ✅ Custom agents | ❌ Not covered |
| Maturity | ❌ 1 day old, 7 stars | ✅ Table tools have 100-10K stars |

---

## Challenge Notes (technical-writer review)

**Score should be 2/5, not 3/5.** Reasons:

1. `claude-code-otel` already exports to Datadog/Honeycomb. The OTel angle is not additive.
2. The jq queries at observability.md:519-550 cover most of the audit use case already. The "replay niche" is thinner than it appears.
3. ICM (1 star) was put on watch list. Agent-trace at 7 stars deserves the same treatment.

**Missing aspects not in initial analysis**:

- **MCP proxy = MITM risk**: Routing all MCP traffic through an unaudited HTTP/SSE proxy is a security surface. The guide has a full hardening section — adding this to the monitoring table without flagging would be inconsistent.
- **Secret redaction unverified**: Base64-encoded tokens, multi-line .env values, AWS temporary credentials — edge cases not tested. Could create false confidence.
- **Python decorator API vs MLflow SDK**: MLflow has versioning + experiment tracking + LLM-as-judge. Agent-trace has lower friction. Real trade-off not mentioned.

**On placement**: If integrated, not in the External Monitoring Tools table (that's monitoring, not debugging). Better as a footnote in the JSONL section (~observability.md:565) as "a higher-level wrapper for session replay."

**Risk of NOT integrating**: Near zero. The jq queries + claude-code-otel cover the primary use cases. Real risk runs the other direction: adding a 1-day-old tool that goes unmaintained = dead link in a table readers use for tooling decisions.

---

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Zero dependencies, Python stdlib only | ✅ | pyproject.toml + README |
| Created 2026-03-15 | ✅ | GitHub API: `created_at: 2026-03-15T08:09:45Z` |
| MIT licensed | ✅ | GitHub API: `license: MIT License` |
| Captures all CC hook events | ✅ | README hooks JSON: all 7 event types |
| Export to Datadog, Honeycomb, Splunk | ✅ | README: `export --to otlp` (OTLP compatible) |
| 7 stars at evaluation | ✅ | GitHub API 2026-03-16 |

No hallucinations detected. All stats confirmed against source.

---

## Decision

**Action: Watch list**
**Integration trigger**: 100+ stars AND at least one practitioner write-up showing real production use.

**If triggered**: Add as footnote in observability.md ~line 565 (JSONL section), not in the External Monitoring Tools table. Frame as "higher-level wrapper for session replay/debug" distinct from the monitoring tools.

**Why watch list and not reject**: Session replay is a real gap. Zero-deps Python is a genuine adoption differentiator. The engineering quality looks solid (automated setup, secret redaction, HTTP/SSE proxy). Just needs time to prove reliability on real sessions.
