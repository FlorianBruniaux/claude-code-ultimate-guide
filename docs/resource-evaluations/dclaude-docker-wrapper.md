# Resource Evaluation: dclaude — Dockerized Claude Code Wrapper

| Field | Value |
|-------|-------|
| **Resource** | [github.com/jedi4ever/dclaude](https://github.com/jedi4ever/dclaude) + [LinkedIn post](https://www.linkedin.com/posts/patrickdebois_github-jedi4everdclaude-activity-7423577213188562944-jUE_) |
| **Type** | Open-source tool (bash script) |
| **Author** | Patrick Debois ("father of DevOps", creator of DevOpsDays 2009, co-author DevOps Handbook) |
| **Published** | 2026-02-01 |
| **Score** | **2/5** (Marginal) |
| **Action** | Footnote in `guide/sandbox-isolation.md` (Limitations subsection) |

---

## Summary

1. **dclaude** is a single-file bash script wrapping Claude Code CLI inside a standard Docker container for filesystem isolation. Drop-in replacement: all Claude CLI flags forwarded.
2. **Primary motivation**: Claude Code can navigate entire filesystems, including other git worktree branches, risking accidental edits to production code. dclaude restricts visibility to mounted directories only.
3. **Features**: SSH agent forwarding, GPG signing, Docker-in-Docker (via host socket), automatic port mapping with URL rewriting, persistent named containers, GitHub token forwarding, `.env` auto-loading.
4. **Installation**: Single `curl` download, auto-builds Docker image on first run. Requires Docker Engine only (no Docker Desktop).
5. **Security model**: Standard container isolation (not microVM). Mounts host Docker socket (`/var/run/docker.sock`), `~/.ssh`, `~/.gnupg` into container — expands attack surface vs. Docker Sandboxes' private daemon approach.

## Gap Analysis

| Topic | Guide status | dclaude adds |
|-------|-------------|--------------|
| Sandbox isolation | ✅ Comprehensive (`sandbox-isolation.md`, 6 solutions) | Nothing new |
| Linux + Docker Engine | ⚠️ Gap documented (line 224) but no workaround | ✅ Fills gap |
| Worktree isolation use case | ❌ Not explicitly motivated | ✅ Explicit motivation |
| SSH/GPG forwarding in sandbox | ❌ Not covered | ✅ Built-in (but ⚠️ security tradeoff) |

## Score Justification

**2/5 (Marginal)** because:

- The guide already covers Docker Sandboxes (official, microVM isolation) plus 5 alternatives — no material gap
- dclaude uses standard containers, not microVMs — weaker isolation than Docker Sandboxes. The guide's own anti-patterns (line 377) warn: "Assuming containers = VMs"
- Host Docker socket mount means containerized Claude can control the host Docker daemon — opposite of Docker Sandboxes' private daemon
- Single-maintainer bash script with no lifecycle guarantees
- However: works on Linux with Docker Engine (real gap), and Patrick Debois's standing in the DevOps community gives credibility

**Why not 3/5**: Weaker security model and narrow differentiator (Linux-only gap) don't warrant a dedicated section. The guide documents the Linux limitation already.

**Why not 1/5**: Fills a legitimate gap for Linux Docker Engine users. Debois's contribution merits acknowledgment.

## Challenge (technical-writer)

The technical-writer agent confirmed the 2/5 score with additional analysis:

- **Security under-analyzed**: Host Docker socket mount is a material concern, not just "weaker isolation"
- **Debois credibility understated**: He coined "DevOps" — not just "a known figure"
- **Drop-in claim unverified**: Edge cases (MCP servers, `--resume`, session persistence) likely have friction
- **Placement recommendation refined**: Footnote in Limitations subsection (line 225), NOT in comparison matrix
- **Risk of non-integration**: Minimal — no reader fails to find a sandbox solution without dclaude

## Fact-Check

| Claim | Status | Source |
|-------|--------|--------|
| Author: Patrick Debois | ✅ | LinkedIn profile (17.5K followers) |
| Debois = "father of DevOps" | ✅ | Multiple sources (New Relic, DEV Community, jedi.be) |
| GitHub: jedi4ever | ✅ | Matches jedi.be domain |
| Drop-in replacement for claude CLI | ⚠️ | Claimed by README, not independently tested |
| Single-file install via curl | ✅ | GitHub README |
| SSH/GPG/Docker-in-Docker support | ✅ | GitHub README |
| Auto-builds Docker image | ✅ | GitHub README |
| Persistent container mode | ✅ | GitHub README |
| 60 likes, 7 comments (LinkedIn) | ✅ | LinkedIn post (snapshot at fetch time) |

## Integration Applied

- `guide/sandbox-isolation.md` line 225 — Footnote mention in Limitations subsection with security tradeoff note
- `docs/resource-evaluations/dclaude-docker-wrapper.md` — This file
- `docs/resource-evaluations/README.md` — Index entry added
