# Resource Evaluation: AgentsView — Local Session Analytics for Claude Code

**Evaluated**: 2026-02-23
**Evaluator**: Claude Sonnet 4.6 + technical-writer agent challenge
**Target Guide**: Claude Code Ultimate Guide

---

## Executive Summary

**Resource**: AgentsView — Local web app for browsing, searching, and analyzing AI coding sessions
**URL**: https://www.agentsview.io/
**GitHub**: https://github.com/wesm/agentsview
**Author**: Wes McKinney (creator of pandas)

**Initial Score**: 4/5
**Challenged Score**: 3/5
**Final Score**: **3/5 (Pertinent — Complement utile)**

**Decision**: **Integrate in `guide/observability.md` (External Monitoring Tools section). Cross-reference in `guide/third-party-tools.md` (Session Management).** Wait 2-4 weeks for adoption to consolidate before publishing (target: ~200+ stars).

---

## 📄 Resource Summary

**Type**: Local-first web application (Go + Svelte 5 + SQLite FTS5)

**Key Points**:
1. **Full-text search** across months of sessions via SQLite FTS5 — find specific discussions instantly
2. **Usage analytics**: activity heatmaps, velocity metrics, tool usage breakdowns, per-project stats
3. **Real-time monitoring**: watches session directories via Server-Sent Events, streams live messages
4. **Multi-CLI support**: Claude Code + Codex + Gemini CLI (unique in the space)
5. **Local-first**: single Go binary, MIT license, no accounts, no cloud; session export as HTML or GitHub Gist

**Technical Stack**:
- Backend: Go (56.8% of codebase)
- Frontend: Svelte 5 + Vite + TypeScript
- Storage: SQLite with FTS5 full-text search
- Real-time: Server-Sent Events (embedded web server)

---

## 🎯 Score: 3/5

**Justification**: Real gap in the guide — no existing documented tool combines full-text search + visual analytics (heatmaps, velocity) in a local web UI.

- `claude-code-viewer`: basic session viewer, no search, no analytics
- `session-search.sh`: CLI search only, zero UI, no analytics
- `ccboard`: cost-centric dashboard, full-text search not confirmed

AgentsView fills this gap. However, the repo was created on February 19, 2026 (4 days before this evaluation), has 49 stars, and only 2 contributors. Too recent for a 4/5 (High Value) without established adoption. Wes McKinney's credibility (pandas creator) is a strong positive signal.

---

## ⚖️ Comparative Analysis

| Feature | AgentsView | Guide (current) |
|---------|-----------|-----------------|
| Full-text search sessions | ✅ SQLite FTS5 | ⚠️ CLI only (`session-search.sh`) |
| Activity heatmaps | ✅ Yes | ❌ Missing |
| Velocity metrics | ✅ Yes | ❌ Missing |
| Tool usage breakdown | ✅ Yes | ⚠️ Partial (ccboard) |
| Local web UI | ✅ Go embedded server | ⚠️ claude-code-viewer (viewer only) |
| Real-time monitoring | ✅ SSE | ⚠️ claude-code-viewer (SSE too) |
| Multi-CLI support | ✅ Claude + Codex + Gemini | ❌ Claude Code only |
| Cost tracking | ❌ Not mentioned | ✅ ccusage, ccboard |
| Session replay/rewind | ❌ No | ✅ Entire CLI |
| Keyboard navigation | ✅ Vim-style shortcuts | N/A |

**vs ccboard distinction**: ccboard = cost-centric with session view. AgentsView = behavior-analytics-centric with FTS search. Different primary use case, ~40% feature overlap.

---

## 📍 Integration Recommendations

### Primary: `guide/observability.md` — External Monitoring Tools

Add row to the comparison table (after ccboard):

```markdown
| **AgentsView** | Local web app | FTS search + activity heatmaps + velocity metrics + real-time monitoring. Multi-CLI (Claude/Codex/Gemini). No cost tracking. | `github.com/wesm/agentsview` |
```

Add to Decision Guide:
```
Want search + visual analytics in one local UI?  → AgentsView
```

### Secondary: `guide/third-party-tools.md` — Session Management

Add short entry after `claude-code-viewer` with explicit differentiation:

| Tool | Focus | Search | Analytics |
|------|-------|--------|-----------|
| claude-code-viewer | UI viewer | No | No |
| AgentsView | Search + analytics | ✅ FTS5 | ✅ Heatmaps, velocity |
| session-search.sh | CLI search | ✅ Fast | No |

### Priority

**Low-Medium** — Integrate in 2-4 weeks once repo reaches ~200 stars. The gap is real but not critical; users can currently combine session-search.sh (CLI) + ccboard (stats).

---

## 🔥 Challenge (technical-writer)

The challenge agent recommended **3/5** (vs initial 4/5) for the following reasons:

1. **Score**: 4/5 requires verifiable adoption signals. Repo is 4 days old, 49 stars → 3/5 correct.
2. **Placement corrected**: `observability.md` (analytics/monitoring) is the right location, not `third-party-tools.md`. The guide explicitly states third-party-tools.md is "not DIY monitoring scripts (see Observability)". AgentsView is an analytics dashboard.
3. **ccboard overlap**: More significant than initially assessed. Must document the distinction explicitly: ccboard = cost + session view; AgentsView = FTS search + behavior analytics.
4. **Missing in initial evaluation**: Model type (now confirmed MIT open source), exact stack (confirmed Go, not Rust), "nothing leaves your machine" claim is marketing (unaudited via traffic analysis).

**Adopted**: Score adjusted to 3/5. Placement changed to `observability.md`.

---

## ✅ Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Author = Wes McKinney | ✅ | github.com/wesm/agentsview |
| MIT License, open source | ✅ | GitHub repo |
| Stack Go + Svelte 5 + SQLite FTS5 | ✅ | GitHub (56.8% Go) |
| Full-text search via SQLite | ✅ | README + codebase |
| Activity heatmaps | ✅ | agentsview.io documentation |
| Real-time via SSE | ✅ | GitHub description |
| Multi-agent: Claude + Codex + Gemini | ✅ | GitHub README |
| Single binary, local-first | ✅ | agentsview.io |
| "Nothing leaves your machine" | ⚠️ | Marketing claim — credible given architecture, but not verified via traffic analysis |
| 49 stars, created Feb 19 2026 | ✅ | GitHub (verified Feb 23 2026) |
| v0.3.2, 7 releases in 4 days | ✅ | GitHub Releases |
| Session export HTML/GitHub Gist | ✅ | GitHub README |

**Correction**: Initial WebFetch described a "Rust backend" — incorrect. GitHub shows Go (56.8%). Corrected.

**Note on LinkedIn post**: https://www.linkedin.com/posts/wesmckinn_agentsview-activity-7431693909841309696-paBN — could not be fetched (requires authentication). Not factored into scoring.

---

## 🎯 Final Decision

- **Final score**: **3/5**
- **Action**: **Integrate** — `observability.md` + mention in `third-party-tools.md`
- **Timing**: 2-4 weeks (wait for repo to reach ~200+ stars)
- **Confidence**: **Medium** — real gap confirmed, tool verified functional, but adoption too recent for high confidence. Wes McKinney's credibility (pandas) is a strong positive signal. 