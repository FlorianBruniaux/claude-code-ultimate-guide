# Resource Evaluation: Multi-Session Claude Code Management — Landscape Overview

**Date**: 2026-03-19
**Evaluator**: Claude (research session + structured synthesis)
**Status**: Reference — Integrate into guide (ecosystem / third-party tools section)

---

## Summary

This evaluation covers the full landscape of tools for managing multiple Claude Code sessions across multiple projects simultaneously. The research identified 13 tools across 4 categories: monitoring dashboards, remote/browser access, multi-project orchestrators, and sound/notification systems.

No single tool covers all use cases. The space is fragmented, actively evolving (most repos < 6 months old), and missing one obvious feature: per-project audio differentiation.

---

## Score: 4/5 (as a category)

| Score | Meaning |
|-------|---------|
| 5 | Essential (major gap) |
| **4** | **High value (significant improvement)** |
| 3 | Pertinent (useful complement) |
| 2 | Marginal (secondary info) |
| 1 | Out of scope |

**Justification**: Multi-agent, multi-project workflows are increasingly common. The guide covers individual session hooks and notifications but has no consolidated view of the tooling available for running 3-10 parallel Claude Code sessions. vibetunnel (4,276 stars, now 4,607 as of 2026-07-28) and multi-agent-shogun (1,082 stars, now 1,405 as of 2026-07-28) signal strong community demand. Integration would fill a documented gap.

---

## Tool Landscape

### Category 1 — Monitoring Dashboards

| Tool | GitHub | Stars | Stack | Key Features |
|------|--------|-------|-------|-------------|
| **claude-code-monitor (ccm)** | [onikan27/claude-code-monitor](https://github.com/onikan27/claude-code-monitor) | ⭐ 212 (now 269 as of 2026-07-28) | TypeScript / Node | TUI vim-style (j/k, 1-9), session switching via AppleScript, mobile WebUI + QR code pairing, WebSocket real-time |
| **claude-code-dashboard** | [Stargx/claude-code-dashboard](https://github.com/Stargx/claude-code-dashboard) | ⭐ 5 | Node + Express + React | Auto-detects all sessions, token/cost per session, context progress bars, git branch, permission mode badges |
| **sniffly** | [chiphuyen/sniffly](https://github.com/chiphuyen/sniffly) | ⭐ 1,170 (now 1,252 as of 2026-07-28) | Python | Analytics-first: usage patterns, error breakdown, shareable dashboard. Post-hoc, not real-time |
| **ClaudeCode-Dashboard** | [Quriov/ClaudeCode-Dashboard](https://github.com/Quriov/ClaudeCode-Dashboard) | ⭐ 0 | Next.js 16 + ReactFlow | Config topology viewer (hooks, agents, MCP, skills), not session monitoring |

**Best pick**: `ccm` for real-time monitoring on macOS (easiest setup: `npx claude-code-monitor`). `sniffly` for post-session analytics on any platform.

---

### Category 2 — Remote / Browser Access

| Tool | GitHub | Stars | Stack | Key Features |
|------|--------|-------|-------|-------------|
| **vibetunnel** | [amantus-ai/vibetunnel](https://github.com/amantus-ai/vibetunnel) | ⭐ 4,276 (now 4,607 as of 2026-07-28) | TypeScript + Swift | Wraps any terminal in browser tabs, multiple sessions, Git Follow Mode, VibeTunnelTalk voice narration |
| **cc-hub** | [m0a/cc-hub](https://github.com/m0a/cc-hub) | ⭐ 1 | Go + tmux + Tailscale | Split panes + session color themes, file diff tracking (Claude edits vs git), mobile optimized, dashboard with cost stats |

**Best pick**: `vibetunnel` for broad use (4,276 stars, now 4,607 as of 2026-07-28, very active). `cc-hub` if you need session color differentiation and file diffs per project (requires Tailscale).

---

### Category 3 — Multi-Project Orchestrators

| Tool | GitHub | Stars | Stack | Key Features |
|------|--------|-------|-------|-------------|
| **claudio** | [Iron-Ham/claudio](https://github.com/Iron-Ham/claudio) | ⭐ 22 (now 29 as of 2026-07-28) | Go + tmux | Isolated git worktrees, TUI dashboard, 14 color themes, task chaining (`--depends-on`), planning modes: UltraPlan / TripleShot / Adversarial Review, PR automation, cost limits |
| **multi-agent-shogun** | [yohey-w/multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun) | ⭐ 1,082 (now 1,405 as of 2026-07-28) | Shell + tmux | Shogun/Karo/Ashigaru hierarchy, 7 workers + 1 strategist, multi-CLI (Claude, Codex, Copilot, Kimi), zero API coordination cost |
| **zenportal** | [kgang/zenportal](https://github.com/kgang/zenportal) | ⭐ 1 | Python/Textual | Multi-CLI support, git worktrees per session, 3-tier config, session persistence via tmux |
| **praktor** | [mtzanidakis/praktor](https://github.com/mtzanidakis/praktor) | ⭐ 17 (now 40 as of 2026-07-28) | Go + Docker Compose | Telegram I/O (chat from phone), 1 Docker container per agent, cron tasks, swarms, AES-256-GCM secrets vault |

**Best pick**: `claudio` for serious multi-project orchestration (isolated worktrees, color themes, advanced planning). `multi-agent-shogun` (now 1,405 stars as of 2026-07-28) for high-parallelism fan-out patterns with tmux visibility.

---

### Category 4 — Sound / Notification Systems

| Tool | GitHub | Stars | Stack | Per-Project Sound |
|------|--------|-------|-------|------------------|
| **karina-voice-notification** | [t1seo/karina-voice-notification](https://github.com/t1seo/karina-voice-notification) | ⭐ 0 | Python (Qwen3-TTS) | Clone any voice from YouTube → custom `.wav` per project (DIY assembly) |
| **sound-micro-server** | [arc-co/claude-code-notification-sound-micro-server](https://github.com/arc-co/claude-code-notification-sound-micro-server) | ⭐ 0 | Node.js | Browser-based sound via hook `Stop` + `curl POST`. Single sound for all sessions |
| **ccnotify** | [Helmi/ccnotify](https://github.com/Helmi/ccnotify) | n/a | Shell | Voice notifications (spoken text) |
| **claude-session-manager** | [Swarek/claude-session-manager](https://github.com/Swarek/claude-session-manager) | ⭐ 4 (now 6 as of 2026-07-28, note: renamed to blancmathis/claude-session-manager) | Shell | Colored status line per session, session IDs (`cx` command), live description updates |

**Gap**: No tool provides per-project audio differentiation out of the box. The cleanest DIY approach: configure `settings.local.json` per project with a different audio file in the `Stop` hook.

```json
// project-a/.claude/settings.local.json
{
  "hooks": {
    "Stop": [{ "command": "afplay ~/sounds/project-a.wav" }]
  }
}
```

---

## Capability Matrix

| Tool | Multi-session visibility | Session switching | Per-project differentiation | Sound | Platform |
|------|--------------------------|-------------------|-----------------------------|-------|----------|
| ccm | TUI list | AppleScript focus | Status icons | No | macOS only |
| claude-code-dashboard | Web dashboard | No | Git branch / badges | No | All |
| vibetunnel | Browser tabs | Manual tab switch | Terminal titles | No (voice narration optional) | macOS M1+ / Linux |
| cc-hub | Split panes | Click | Color themes per session | No | macOS/Linux + Tailscale |
| claudio | TUI per instance | TUI controls | 14 color themes | No | macOS/Linux |
| multi-agent-shogun | tmux panes | tmux | Pane position | No | macOS/Linux |
| zenportal | TUI list | TUI controls | Session name | No | macOS/Linux |
| praktor | Web + Telegram | @agent_name | Docker container | No | Linux/Docker |
| karina-voice-notification | n/a | n/a | Custom voice per project | YES (DIY) | macOS M1+ / Linux (CUDA) |
| sound-micro-server | n/a | n/a | No | YES (single sound) | All (browser) |
| claude-session-manager | Terminal status line | Manual | Color-coded status | No | macOS/Linux |

---

## Key Findings

**High adoption signal**: vibetunnel (4,276 stars, now 4,607 as of 2026-07-28) and multi-agent-shogun (1,082 stars, now 1,405 as of 2026-07-28) are the two breakout tools. Both are actively maintained and solve real problems at scale.

**Missing feature**: Per-project audio differentiation does not exist as a packaged solution. DIY with `afplay` / `paplay` + `settings.local.json` hooks per project is the only current approach.

**Ecosystem maturity**: The space is 3-6 months old. Most tools are single-maintainer experiments. `claudio`, `ccm`, and `vibetunnel` have the strongest signals for longevity.

**Platform gap**: Most orchestrators require tmux and work only on macOS/Linux. No solid Windows option exists.

---

## Recommendations

**Action**: Integrate a "Multi-Session Management" section into the guide (third-party tools or workflows section).

**Priority picks to document**:

| Use case | Recommended tool |
|----------|-----------------|
| Quick multi-session visibility on macOS | ccm (`npx claude-code-monitor`) |
| Post-session analytics (all platforms) | sniffly (`uvx sniffly@latest init`) |
| Browser/remote access | vibetunnel |
| Serious orchestration with isolation | claudio |
| High-parallelism fan-out | multi-agent-shogun |
| Per-project audio (DIY) | `settings.local.json` + `afplay` |

**Watch list**: cc-hub, zenportal, praktor — interesting architectures but < 20 stars each. Re-evaluate at 100+ stars.

---

## Related Evaluations

- [078-claude-swarm-monitor.md](078-claude-swarm-monitor.md) — TUI for monitoring agents across worktrees (Rust, Linux)
- [074-ruflo-multi-agent-orchestration.md](074-ruflo-multi-agent-orchestration.md) — Ruflo orchestration platform
- [079-fabro-workflow-orchestration.md](079-fabro-workflow-orchestration.md) — Fabro workflow runtime