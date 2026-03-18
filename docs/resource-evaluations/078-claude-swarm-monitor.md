# Resource Evaluation: claude-swarm-monitor

**Date**: 2026-03-17
**Evaluator**: Claude (automated via /eval-resource)
**Status**: Watch-list — Re-evaluate at 50+ stars or macOS validation report

---

## 📄 Content Summary

- **TUI dashboard** (Rust + Ratatui) for monitoring multiple Claude Code agents running across git worktrees in parallel
- **One swim lane per agent**: lead repo first, then each worktree — sorted and visually separated
- **Live status streamed from JSONL session files** (`~/.claude/projects/`): Working / Waiting For You / Idle / Done / Error
- **Sub-agent tracking**: agents spawned via the Task tool appear as nested cards within the parent lane (claim unverified — see Fact-check section)
- **Docker stack visibility per worktree**: matches Compose stacks via `COMPOSE_PROJECT_NAME` in `docker/.env`, shows live CPU % and memory

**Source**: [github.com/oinant/claude-swarm-monitor](https://github.com/oinant/claude-swarm-monitor)
**Language**: Rust (≥ 1.80) | **License**: MIT | **Stars**: 10 (March 2026) | **Platform**: Linux tested; Windows/Docker Desktop not yet supported

---

## 🎯 Score: 3/5

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap |
| 4 | High value — Significant improvement |
| **3** | **Pertinent — Useful complement** |
| 2 | Marginal — Secondary info |
| 1 | Out of scope |

**Justification**: claude-swarm-monitor fills two genuine gaps not covered by any tool currently in the guide: (1) monitoring via native JSONL session files rather than SSE/polling, and (2) Docker stack visibility per worktree. The JSONL approach is architecturally distinct from agent-chat (which targets Gas Town/multiclaude). However, at 10 stars (6 weeks old) and Linux-only, the adoption signal is too weak for a high-confidence recommendation. Score capped at 3 pending community validation.

---

## ⚖️ Comparatif

| Aspect | claude-swarm-monitor | Guide actuel |
|--------|---------------------|-------------|
| Monitor agent status across worktrees | ✅ Swim lanes, live status | ⚠️ agent-chat exists but targets Gas Town/multiclaude |
| Status from Claude Code session files (JSONL) | ✅ Unique approach | ❌ No tool reads ~/.claude/projects/ natively |
| Sub-agent (Task tool) tracking | ✅ Claimed | ❌ Not covered by any listed tool |
| Docker stack visibility per worktree | ✅ CPU/mem live | ❌ Gap in current guide |
| Cross-platform | ❌ Linux tested only | ⚠️ multiclaude is Linux/macOS, Conductor is macOS only |
| Adoption signal | ⚠️ 10 stars, 1 maintainer | ✅ multiclaude 383+, Ruflo 18.9k |
| Open source | ✅ MIT | ✅ All listed tools |

---

## 📍 Recommendations

**Current action**: Add to watch-list. Do not integrate into the main guide yet.

**Conditions for promotion to 4/5 and integration**:
1. Re-evaluate at 50+ stars or after a credible community report of production use
2. Verify the sub-agent Task tool tracking claim (how are internal spawns tracked if they don't write separate JSONL files?)
3. Add a security note on `~/.claude/projects/` read scope (session files contain full conversation history including accidentally-typed secrets)
4. Confirm or document macOS compatibility as a hard limitation
5. Measure resource overhead with 10+ worktrees and live Docker polling

**When integrated, placement**: `guide/ecosystem/third-party-tools.md` in the Multi-Agent Orchestration section, with an explicit comparison row against agent-chat noting the key differentiators (JSONL-native vs SSE, Docker visibility, Rust vs JS, Linux vs cross-platform).

---

## 🔥 Challenge (technical-writer agent)

The challenge agent lowered the initial proposed score from 4 to 3, citing:

- **Adoption signal is the weakest in the ecosystem section** — 10 stars vs multiclaude (383+), Ruflo (18.9k); even Athena Flow (explicitly marked "not recommended yet") has more external validation
- **Linux-only limitation is a real constraint** for the target audience (macOS-heavy multi-agent users)
- **Security scope not addressed**: the tool reads `~/.claude/projects/` which contains full session history including sensitive context — consistent with guide's pattern of flagging data access scope (see Straude, Packmind entries)
- **Sub-agent tracking claim unverified**: Task tool spawns are internal to Claude Code's process; it's unclear whether they write separate JSONL files

- **Score adjusted**: 3/5 (from proposed 4/5) — agreed
- **Points missed**: Resource consumption (polling overhead), security implications, macOS support gap, sub-agent tracking verification
- **Risk of non-integration**: Low — agent-chat already covers monitoring; the JSONL/Docker angles are compelling but serve a narrow advanced subset

---

## ✅ Fact-Check

| Claim | Status | Source |
|-------|--------|--------|
| Rust + Ratatui TUI | ✅ | GitHub repo, Cargo.toml |
| Status from JSONL session files | ✅ | README: "streamed directly from Claude Code's JSONL session files" |
| Docker stack matching via COMPOSE_PROJECT_NAME | ✅ | README: `docker/.env` → `COMPOSE_PROJECT_NAME` |
| Sub-agent tracking via Task tool | ⚠️ Unverified | Claimed in README, mechanism unclear |
| MIT license | ✅ | GitHub metadata |
| 10 stars | ✅ | GitHub API (2026-03-17) |
| Linux tested | ✅ | README: "currently tested on Linux only" |
| ~500 lines per file | ✅ | README: "The codebase is small (~500 lines per file, clearly separated modules)" |
| Created Feb 2026 | ✅ | GitHub API: created_at 2026-02-22 |

**Corrections**: None required. All verifiable claims check out. The sub-agent tracking claim needs mechanical verification before being cited as a feature.

---

## 🎯 Final Decision

- **Score**: 3/5
- **Action**: Watch-list (not integrated yet)
- **Re-evaluate trigger**: 50+ stars OR macOS production report OR sub-agent tracking verified
- **Confidence**: Medium (tool is real and functional; uncertainty is on adoption and edge-case claims)

---

*Evaluation file: `docs/resource-evaluations/076-claude-swarm-monitor.md`*
