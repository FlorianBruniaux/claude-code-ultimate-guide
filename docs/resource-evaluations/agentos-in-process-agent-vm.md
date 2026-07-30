# Resource Evaluation: agentOS (Rivet)

**URL**: https://github.com/rivet-dev (agentOS package: `@rivet-dev/agentos`), site agentos-sdk.dev
**Type**: GitHub repository (Apache 2.0), npm `@rivet-dev/agentos`
**Evaluation date**: 2026-07-29
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1
**Method**: source analysis of a local clone at `~/Sites/divers-test/agentos`, commit `c4e61aa24` (2026-07-29), full `git log` history, code-size counts by language. No install, no build, no benchmark reproduction was run.

---

## Content summary

agentOS is virtualized Linux VMs that run inside your own Node process, positioned as a replacement for cloud code-execution sandboxes (E2B, Daytona, Modal) for agent workloads that do not need a real Linux kernel. `npm install @rivet-dev/agentos` gets you a VM with no microVM to boot, no container to pull, and no provider account.

Architecture: a trusted Rust sidecar process owns a kernel (`crates/kernel`, `crates/vfs`, `crates/execution`) with a layered virtual filesystem (overlay plus mounts for S3, Google Drive, host directories), a virtual process table with `fork`/`exec`/`wait` and real signals, a socket table, pipes, PTY, DNS. No guest syscall touches the host directly; the guest requests, the kernel decides, the kernel executes. The untrusted executor runs guest JavaScript on native V8 with full JIT (not an interpreter), and compiled tools run in WASM.

`software/` (42 packages) compiles real upstream Linux tools (GNU coreutils, grep, sed, gawk, curl, sqlite3, duckdb, vim, git, ripgrep) to `wasm32-wasip1` against a sysroot the team owns entirely, with a patched Rust std and libc. This is not standard WASI; it is Linux-in-WASM, with missing POSIX calls implemented in the libc layer or as host imports.

The differentiator: host **bindings**. A host-defined JS function with a Zod schema appears inside the VM as a shell command (`/usr/local/bin/agentos-weather forecast --city Paris`). The agent calls it like any other CLI tool. API keys never enter the VM; the agent sees an input and an output, never the secret. Agents (Pi, Claude Code, Codex, OpenCode) run as guest processes speaking ACP, with durable sessions (completed ACP events land in SQLite, a VM sleeps after 15 minutes of inactivity and wakes on connection or cron; each VM is a Rivet Actor). Six permission scopes (`fs`, `network`, `childProcess`, `process`, `env`, `binding`), network denied by default, everything else allowed because it is already virtualized; a denial returns `EACCES` before any host resource is touched.

---

## Vendor benchmarks: labeled, not verified

Measured by the team on an i7-12700KF, documented in `benchmarks/`, dated 2026-03-30: 4.8 ms VM creation at p50, roughly 22 MB for a simple shell, roughly 131 MB for a full code agent with MCP. The team cites E2B/Daytona at 440 ms cold start and 1 GB RAM minimum. These are vendor-reported numbers on a single machine, not independently reproduced by this evaluation or, as far as could be found, by any third party. The headline "92x cold-start" comparison is also comparing two different kinds of thing: starting a V8 isolate versus booting a full Linux microVM. Both facts belong in any citation of these numbers.

---

## The honesty caveat, and it matters

"VM" is a marketing choice. There is no KVM, no Firecracker, no hardware virtualization anywhere in this stack. Isolation rests entirely on V8 isolates and the WASM sandbox, enforced by the Rust sidecar. The project's own stated threat model places the security boundary at sidecar/executor, not at a hypervisor. That is solid for ordinary untrusted agent code, and materially weaker than hardware isolation against a motivated attacker hunting a V8 escape. Deliberately out of scope: a browser, a native x86 binary, a heavy dev server, native compilation. For those, the documentation itself points to running a real sandbox on top.

---

## Project health

Measured on `main` at commit `c4e61aa24` (2026-07-29).

| Metric | Value |
|---|---|
| Total commits | 353 |
| Span | 2026-03 to 2026-07 |
| Nathan Flurry | 322 commits (91%) |
| Rust (23 crates) | 362,029 LOC |
| TypeScript (23 packages) | 185,545 LOC |
| Software packages (`software/`) | 42 |
| Monthly cadence, recent | 118 (Jun) → 181 (Jul), rising |
| Version | `0.0.1`, explicitly preview, API declared unstable |

**Bus factor 1**, same structural risk as Executor, but with a rising rather than declining commit trend over the two most recent months measured. That is a weak signal on its own (two data points), not evidence of a stable trajectory, but it is the opposite direction from Executor's 76% cadence decline from April to July measured in the companion evaluation.

---

## Where it sits relative to the guide's existing coverage

`guide/security/sandbox-isolation.md` §5, titled with the words "cloud sandboxes" (Fly.io Sprites, Cloudflare Sandbox SDK, Vercel Sandboxes, E2B), lists four vendors and every one bills through a cloud provider. agentOS is the missing counter-example: no provider, no account, runs inside the host's own Node process. That is a real gap in the section as it stands, not an incremental addition to an existing list.

Technically, it also goes deeper than what `sandbox-isolation.md` §7b ("WebAssembly-based MCP Tool Sandboxing, Experimental") currently covers. That section is scoped to sandboxing individual MCP tool calls at the OS-access level (tools like Wassette). agentOS's WASM sysroot compiles a substantial slice of userland Linux (42 packages, including git, ripgrep, sqlite3, duckdb) against an owned libc, which is a materially larger scope than per-tool capability grants.

One independent, unrelated data point from the guide's own YouTube-transcript research corpus (`yt-insights`, 2026-07-29): Rene Brandel's "How we hacked YC Spring 2025 batch's AI agents" (DevCon Fall 2025, 2025-11-21) recommends the opposite default, using an existing sandbox provider (E2B, Daytona) rather than building your own. agentOS is exactly the kind of project that advice would normally warn against building, from a team that appears to have built it anyway. Worth naming as the live counter-example when this advice is cited.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 4 | Rust kernel plus an owned WASM sysroot compiling real upstream Linux tools is deeper than anything currently in the guide's sandboxing coverage |
| Production reliability | 2 | `0.0.1` preview, bus factor 1, vendor-only benchmarks |
| Documentation quality | 3 | The threat model is stated plainly and honestly (sidecar/executor boundary, not hypervisor), which is unusual candor for a pre-1.0 project |
| Adoptability | 3 | `npm install` simplicity for the basic case; permission scopes and bindings are well-specified |
| Guide value | 4 | Fills a documented, explicit gap in `sandbox-isolation.md` §5 |
| **Overall** | **4** | High value. Fills a real gap, rising cadence, deeper technical content than the guide currently covers on this axis. |

---

## Decision

**Integrate into `guide/security/sandbox-isolation.md` §5, as the explicit in-process counter-example to the section's four cloud vendors, plus one new TL;DR row.**

Frame every benchmark figure as vendor-reported, dated, and single-machine, per this evaluation's own findings. State the "no hypervisor" caveat directly rather than letting the word "VM" imply hardware isolation it does not have. Cross-reference §7b so a reader comparing agentOS to Wassette-style MCP tool sandboxing understands they solve overlapping but differently-scoped problems.

**Revisit trigger**: a tagged `1.0.0` release, an independently reproduced benchmark, or a second maintainer crossing 20% of commits over a rolling quarter.

---

## Sources

All paths relative to a clone at commit `c4e61aa24` (2026-07-29): repository root listing (`crates/`, `packages/`, `software/`), `crates/kernel/`, `crates/vfs/`, `crates/execution/`, `benchmarks/` (figures only, methodology not independently reproduced), `LICENSE`. Git history via `git log --format` and `git shortlog -sn` on the full clone. Cross-reference: `/Users/florianbruniaux/Sites/perso/yt-insights/output/aidevcon/insights/20251121 - Rene Brandel - How we hacked YC Spring 2025 batch's AI agents ｜ DevCon Fall 2025 [o_bVqT_5yGM].en.md`.
