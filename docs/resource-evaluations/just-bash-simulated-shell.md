# Resource Evaluation: just-bash (Vercel Labs)

**URL**: https://github.com/vercel-labs/just-bash
**Type**: GitHub repository (monorepo), npm `just-bash` (core) and `@just-bash/executor` (tool discovery)
**Evaluation date**: 2026-08-04
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1
**Method**: source analysis of a local clone at `~/Sites/divers-test/just-bash`, commit `1e06ce6` (2026-07-26), full `git log` history, `api.github.com` metadata, and a grounded web comparison against seven other agent-sandbox products via Perplexity search (2026-08-04). No install, no build, no benchmark reproduction was run.

---

## Content summary

just-bash is a full bash interpreter written in TypeScript: lexer, recursive-descent parser, AST, and an execution engine, backed by an in-memory virtual filesystem. Nothing spawns. There is no `child_process`, no worker acting as a guest OS, no WASM VM boundary for the shell itself. The interpreter just walks the AST and calls TypeScript functions. Over 90 coreutils-equivalent commands ship built in (`grep`, `sed`, `awk`, `find`, `tar`, `jq`, `xan`, `yq`...), plus optional CPython (via Emscripten), QuickJS (`js-exec`), and sql.js, each gated behind an explicit opt-in flag because each adds real security surface.

Four filesystem backends cover the practical range an embedding app needs: `InMemoryFs` (default, no disk contact), `OverlayFs` (real-disk reads, copy-on-write writes, used by the CLI), `ReadWriteFs` (real disk read-write, for letting an agent actually modify a workspace), and `MountableFs` (composes several backends under one namespace, e.g. a read-only knowledge base mounted next to a writable workspace). A `Sandbox` class mirrors the `@vercel/sandbox` API on purpose, so a project can start on just-bash and swap to a real Vercel Sandbox microVM later without touching call sites.

`THREAT_MODEL.md` (31.5 KB) is the strongest artifact in the repo. It names three threat actors (untrusted script author, malicious data source, compromised dependency), draws explicit trust boundaries, and tabulates the attack surface: token bombs, brace-expansion bombs, command-substitution depth, glob bombs, prototype pollution via IFS/env keys, DNS rebinding on the optional `curl`, each row naming the defense, the limit value, and the source file. Every numeric limit (`maxCallDepth`, `maxSubstitutionDepth: 50`, `maxBraceExpansionResults: 10K`, `maxExecutionTimeMs: 30_000`...) is configurable per instance and overridable per `exec()` call, with a `normal` (liberal) and `hardened` (opt-in tighter) profile.

---

## The isolation model, and the caveat that matters

The README states its own limit without hedging: "All execution happens without VM isolation." There is no process boundary, let alone a hypervisor, between the interpreter and the embedding Node process. Defense rests on JavaScript-level containment: a `DefenseInDepthBox` that monkey-patches `Function`, `eval`, `setTimeout`, `process.*`, and `Module._resolveFilename` inside an `AsyncLocalStorage`-scoped context, reversible proxies over `Reflect`/`JSON`/`Math`, and null-prototype objects for anything a script controls the keys of (env, associative arrays, AWK variables). The docs are honest about where this falls short: reversible proxying cannot revoke a reference a script cached before activation, Node's `resourceLimits` do not reliably cap the WASM linear memory used by CPython or sql.js, and the guidance for anyone needing a hard memory or process guarantee is to use a real worker/process boundary, or Vercel Sandbox, for that piece.

That makes just-bash's isolation weaker in kind than agentOS's (`docs/resource-evaluations/agentos-in-process-agent-vm.md`), which at least puts a Rust sidecar and a V8 isolate between guest code and the host. just-bash puts nothing there beyond disciplined TypeScript. The trade for that is architectural simplicity: no Rust toolchain, no sidecar process to manage, and the entire security model is auditable as ordinary TypeScript plus one markdown file that names every limit.

---

## Project health

Measured 2026-08-04, HEAD at `1e06ce6` (2026-07-26).

| Metric | Value |
|---|---|
| GitHub stars / forks / open issues | 4,037 / 228 / 97 |
| Repo created (GitHub) | 2025-12-23 |
| Total commits (HEAD) | 380 |
| Malte Ubl | 322 commits (84.7%) |
| Next contributor | Lars Trieloff, 6 commits (1.6%) |
| TypeScript LOC (`packages/just-bash/src`) | 273,627 |
| npm version | `just-bash@3.2.0`, `@just-bash/executor@3.0.3` |
| `LICENSE` file at repo root | **Absent.** README claims Apache-2.0; GitHub's own `license` API field reports `null`. |
| Recent cadence | Multiple merged PRs per day through July 2026 (release workflow hardening, grep flag fixes, curl aggregation) |

**Bus factor 1**, same structural pattern already flagged in the Executor and agentOS evaluations from this same window (2026-07-29). Unlike agentOS's `0.0.1` preview tag, just-bash is past `3.x` on npm with a real changeset-based release pipeline (`@changesets/cli`), a website example deployed publicly, and a companion `bash-tool` package already wrapping it for the AI SDK, so the maturity signal is stronger despite the identical concentration risk. The missing `LICENSE` file is a genuine gap: the README's Apache-2.0 claim is not backed by a file GitHub can detect, worth a direct check before any commercial redistribution decision, not an assumption.

---

## Where it sits relative to the guide's existing coverage

`guide/security/sandbox-isolation.md` §5 already lists agentOS as "the in-process counter-example" to four billed cloud vendors (Fly.io Sprites, Cloudflare Sandbox SDK, Vercel Sandboxes, E2B). just-bash belongs in that same subsection, not as a duplicate of agentOS but as the other end of the in-process spectrum: agentOS runs a real (if hypervisor-less) VM with a Rust kernel and V8 isolate; just-bash runs no VM at all, just a bash-compatible interpreter written directly in the host language. A reader comparing the two needs both data points, since "in-process, no cloud account" spans a much wider range of actual isolation strength than the phrase suggests on its own.

It is also the direct sibling of the guide's existing "Vercel Sandboxes" entry two subsections up (line 435): Vercel ships both ends of the same trade-off under one company, a full Firecracker microVM product for real isolation, and a zero-infrastructure simulated shell for development, testing, and low-stakes embedded use. That relationship is worth stating explicitly since it is not obvious from either product's own docs.

A cross-search of the eight agent-sandbox products commonly compared in this space (Perplexity, 2026-08-04) confirms just-bash and WebContainers (StackBlitz) are the only two "simulation, not isolation" entries; E2B (~150-200ms Firecracker cold start), Daytona (~90ms, Docker/Kata), Modal Sandboxes (gVisor, sub-second to ~3s), Cloudflare Sandboxes, and Fly Machines (~2-3s) all pay real boot latency for a real OS boundary. That two-category split (simulate vs. isolate) is a cleaner mental model for the guide's readers than a flat vendor list, and neither existing guide section states it directly.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 3 | A full bash+coreutils reimplementation in TypeScript is substantial engineering, but "simulate instead of isolate" as a category is already established by WebContainers; the novelty here is applying it thoroughly to the agent-shell-tool use case, not the mechanism itself |
| Production reliability | 3 | Past `3.x` on npm, changeset release pipeline, extensive dedicated security test suite, but bus factor 1 (84.7%) and no `LICENSE` file at the root despite an Apache-2.0 claim |
| Documentation quality | 4 | `THREAT_MODEL.md` names every attack vector, its defense, its limit value, and its source file; README documents every FS backend and option with runnable examples |
| Adoptability | 4 | `npm install just-bash`, zero infra, drop-in `Sandbox` API compatible with `@vercel/sandbox` for a later upgrade path, works in-browser for the core shell |
| Guide value | 4 | Completes the "in-process, no cloud account" category in §5 with a genuinely different mechanism from agentOS, and makes explicit an unstated relationship to the guide's existing Vercel Sandboxes entry |
| **Overall** | **4** | High value. Distinct mechanism from the guide's only existing in-process example, stronger maturity signal than that example, real caveat (no VM isolation, no LICENSE file) worth stating plainly rather than smoothing over |

---

## Decision

**Integrate into `guide/security/sandbox-isolation.md` §5**, as a subsection alongside agentOS, framed explicitly as the "simulate, don't isolate" counterpart with an honest statement that it offers less containment than agentOS, not more, in exchange for zero moving parts. Add one TL;DR row. Skip the §6 Comparison Matrix, same call as agentOS's own integration: most of its columns (Docker-in-Docker, kernel isolation) do not map to an in-process simulator. State the missing `LICENSE` file directly rather than repeating the README's Apache-2.0 claim as fact.

**Revisit trigger**: a `LICENSE` file lands (resolves the flagged gap), a second maintainer crosses 15% of commits over a rolling quarter, or a major version bump changes the isolation model (e.g. an opt-in worker-thread boundary for the core interpreter, not just the WASM runtimes).

---

## Sources

All paths relative to a clone at commit `1e06ce6` (2026-07-26): `README.md`, `CLAUDE.md`, `THREAT_MODEL.md` (§1-3), `package.json` (root and `packages/just-bash/`), `packages/just-bash/src/` directory listing (file count and structure only, not full read), `examples/` directory listing. Git history via `git log --format`, `git shortlog -sn HEAD`, `git rev-list --count HEAD`. Repo metadata via `api.github.com/repos/vercel-labs/just-bash` (stars, forks, license field, created/pushed dates). Eight-product comparison via Perplexity web search, 2026-08-04, cross-referencing Modal, Northflank, and Firecrawl sandbox-comparison posts plus the E2B and Vercel Sandbox docs (see chat transcript for full citation list).
