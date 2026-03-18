# Resource Evaluation: Docker Sandboxes & Sandbox Isolation Landscape

| Field | Value |
|-------|-------|
| **Resource** | Docker Sandboxes blog + [docs.docker.com/ai/sandboxes/](https://docs.docker.com/ai/sandboxes/) |
| **Type** | Product launch + official documentation |
| **Published** | 2026-01-30 |
| **Score** | **4/5** (High Value) |
| **Action** | Integrated — new guide file + reference.yaml + cross-references |

---

## Summary

1. **Docker Sandboxes** (Docker Desktop 4.58+) provide microVM-based isolation for AI coding agents, replacing the older container-based approach. Claude Code runs with `--dangerously-skip-permissions` inside the sandbox since the VM itself is the security boundary.
2. **Network policies** offer allowlist/denylist modes with domain-level filtering, per-sandbox config, and built-in monitoring via `docker sandbox network log`. Private CIDR ranges blocked by default.
3. **Custom templates** use standard Dockerfiles extending `docker/sandbox-templates:claude-code`. Base image includes Ubuntu, Node.js, Python 3, Go, Git, Docker CLI, GitHub CLI, ripgrep, jq.
4. **The broader landscape** includes Fly.io Sprites (Firecracker microVMs, ~300ms checkpoint/restore), Cloudflare Sandbox SDK (container-based, Workers integration), E2B (open-source Firecracker, 150ms cold boot), and Vercel Sandboxes (GA 2026-01-30, Firecracker microVMs).
5. **Gap in the guide**: No existing documentation on running Claude Code in isolated environments. The `--dangerously-skip-permissions` warning (ultimate-guide.md:3943) lacks a safe alternative path.

## Gap Analysis

| Topic | Before | After |
|-------|--------|-------|
| Safe autonomous execution | Warning only ("never use --dsp") | Documented pattern: sandbox + --dsp |
| Docker Sandboxes | Not mentioned | Full guide with commands, network, templates |
| Cloud sandbox alternatives | Not mentioned | 4 alternatives with comparison matrix |
| Isolation decision tree | Missing | Flowchart: local vs cloud vs serverless |
| Network policy configuration | Missing | Allowlist/denylist modes documented |
| Custom template creation | Missing | Dockerfile pattern documented |

## Integration Decision

**Score justification**: 4/5 (High Value) rather than 5/5 because:
- Docker Sandboxes are genuinely useful and fill a real gap (safe autonomy)
- Official Docker documentation is reliable (Tier 1 source)
- However, the feature is Docker Desktop-only (no standalone Docker Engine support)
- Linux support limited to legacy container mode (not microVM)
- MCP Gateway not yet supported inside sandboxes
- Cloud alternatives are supplementary context, not Claude Code-specific features

**Action**: Create dedicated guide file (`guide/sandbox-isolation.md`) covering Docker Sandboxes as the primary solution with alternatives for cloud/CI scenarios.

## Fact-Check

| Claim | Verification | Status |
|-------|-------------|--------|
| Docker Sandboxes use microVMs, not containers | docs.docker.com/ai/sandboxes/ | Verified |
| Claude Code runs with --dsp inside sandbox | docs.docker.com/ai/sandboxes/claude-code/ | Verified |
| Supported agents: Claude Code, Codex, Gemini, cagent, Kiro | docs.docker.com/ai/sandboxes/ | Verified |
| Network allowlist/denylist modes | docs.docker.com/ai/sandboxes/network-policies/ | Verified |
| macOS + Windows only for microVM mode | docs.docker.com/ai/sandboxes/ | Verified |
| Fly.io Sprites use Firecracker microVMs | sprites.dev | Verified |
| E2B cold boot ~150ms | e2b.dev | Claimed by vendor |
| Vercel Sandboxes GA 2026-01-30 | vercel.com announcement | Verified |
| Cloudflare uses containers, not microVMs | developers.cloudflare.com/sandbox/ | Verified |

## Integration Applied

- `guide/sandbox-isolation.md` — New guide file (~10 min read)
- `machine-readable/reference.yaml` — 13 new sandbox_* index entries
- `guide/ultimate-guide.md:3943` — Cross-reference added after --dsp warning
- `guide/README.md` — Navigation entry added
- `docs/resource-evaluations/README.md` — Index entry added
