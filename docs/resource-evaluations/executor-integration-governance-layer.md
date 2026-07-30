# Resource Evaluation: Executor (integration governance layer)

**URL**: https://github.com/UsefulSoftwareCo/executor
**Type**: GitHub repository (MIT), npm/CLI `executor`, site executor.sh
**Evaluation date**: 2026-07-29
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.41.1
**Method**: source analysis of a local clone at `~/Sites/divers-test/executor`, commit `2f09b13e0` (2026-07-28), full `git log` history, file-count concept mapping between `vision.md` and shipped source. No install, no build, no live MCP session was run against it.

---

## Content summary

Executor is an integration layer between AI agents and external APIs: MIT-licensed, Bun + Turborepo monorepo, version `1.4.0-beta.0`. The pitch: declare an integration once (an API's auth and rules), and every MCP-compatible agent (Claude Code, Cursor, ChatGPT) shares the same catalog instead of each carrying its own copy of the same credentials and tool wiring.

Four concepts, in dependency order:

1. **Integration** (a spec: OpenAPI, GraphQL, an existing MCP server, Google Discovery) indexed into a tool catalog.
2. **Connection**, a configured, authenticated instance of an integration, identified by `(scope, integration, name)`. One integration can hold many connections (two GitHub orgs, `work` and `perso`).
3. **Policy**, per tool, one of `allowed` / `require_approval` / `blocked`, with defaults derived from the spec (a write is not treated like a read).
4. **MCP exposure**, a single endpoint (`/mcp?toolkit=...`); agents see the whole catalog through meta-tools (`search` + `describe` + `execute`) rather than every schema loaded upfront.

The mechanism worth taking seriously: a Connection never stores the raw credential, only a `SecretRef` (`op://`, `keychain://`, `env://`, `vault://`), resolved by a provider at call time behind a tool-proxy. `vision.md` states there is no escape hatch: a `SecretRef` never appears in a tool's input/output schema or any MCP response. Execution is pausable, since a call blocked on missing auth or a pending approval returns a paused Run, resumed with `executor resume --execution-id exec_123`.

Four ways to run it, same functionality: Executor Cloud (hosted), CLI + daemon (`apps/cli` + `apps/local`), Desktop app, self-host (Docker or Cloudflare Worker).

---

## The core mechanism, verified in code

The `SecretRef` claim is the one that matters most, since the whole value proposition rests on it. `packages/core/sdk/src/` holds `connection.ts`, `integration.ts`, and the full OAuth surface (`oauth-flow.ts`, `oauth-client.ts`, `oauth-discovery.ts`, `oauth-callback-state.ts`, `oauth-gc.ts`, `migration-oauth-metadata.ts`). `packages/hosts/mcp/src/tool-server.ts` (41.9 KB, with a 63.3 KB test file, the largest test-to-source ratio of any file checked) is the actual MCP surface. Secret-backend plugins exist separately per provider: `packages/plugins/onepassword/`, `keychain/`, `workos-vault/`, `encrypted-secrets/`, `file-secrets/`.

This evaluation did not trace every call site that touches a `SecretRef` to confirm it never leaks into a serialized response; that would require running the test suite and instrumenting the proxy path, which was out of scope for a read-only source pass. What is confirmed: the pattern is architecturally consistent (separate secret-backend plugins, a dedicated OAuth module, a large MCP-surface test file), and `vision.md` states the invariant explicitly as a design rule rather than an implementation detail discovered after the fact. Treat the "never reaches the agent" claim as architecturally well-supported, not independently proven by this pass.

---

## Vision versus shipped code

Counting source filenames per concept across `packages/`:

| Concept | Files (shipped) |
|---|---|
| execution | 31 |
| scope | 15 |
| toolkit | 10 |
| policy | 8 |
| approval | 4 |
| kernel (code-mode runtimes) | 4 runtimes (`quickjs`, `deno-subprocess`, `dynamic-worker`, `workerd-subprocess`), roughly 200 KB of TS combined |

| Concept in `vision.md`, zero files built | |
|---|---|
| workflow | 0 |
| audit / Run model | 0 |
| triggers (cron/event) | 0 |
| storage | 2 |
| skills | 2 |
| generative UI | 0 |
| user-authored plugins (sandboxed) | 0 |

`vision.md` (391 lines) states the discipline directly: "in build mode, every 'and then you'd want X' is a YAGNI to defer." The gap between a 391-line vision document and what is actually built matches that stated discipline rather than contradicting it. This is the strongest positive signal in the repository: most projects that write a vision this large build past what they need. This one has not, yet.

---

## Project health

Measured on `main` at commit `2f09b13e0` (2026-07-28).

| Metric | Value |
|---|---|
| Total commits | 2,532 |
| Span | 2026-02 to 2026-07 |
| Rhys Sullivan | 2,359 commits (93%) |
| Second contributor | 43 commits (1.7%) |
| Monthly cadence | 408 (Feb) → 479 (Mar) → 605 (Apr, peak) → 564 (May) → 333 (Jun) → 143 (Jul) |
| Remote branches | 358 |
| Source (TS/TSX) | 227,626 LOC across 1,232 files |
| Test files | 451 (37% of files) |
| Files importing `effect` | 436 of 1,232 (35%) |
| Files mentioning `cloudflare` | 106 |

**Bus factor 1.** Cadence down 76% from the April peak to July. Two readings are equally plausible from outside the project and neither can be settled by reading the repo: pre-1.0 hardening ahead of a stable release, or the founder's attention shifting to Executor Cloud and go-to-market. A second maintainer or a tagged `1.0.0` would resolve this; neither exists yet.

**Effect coupling.** The SDK exposes a Promise-based API (`@executor-js/sdk/promise`) alongside an Effect-native one, so consuming it does not require learning Effect. Contributing to it, or wrapping it more deeply than the documented Promise surface, does: 35% of source files import `effect` directly, and `AGENTS.md` mandates Effect Vitest for all tests (`bun test` explicitly forbidden). A production user who reported using it as their MCP core for external agent harnesses independently flagged this exact tension: "velocity is very high, something to constantly stay on top of, especially if you run wrappers around it."

---

## Agentic-engineering configuration in the repo itself

Separate from the product, the repository's own configuration for working with AI coding agents is worth naming, because it generalizes past this one codebase. Three skill directories coexist: `.claude/skills/` (3 skills), `.agents/skills/`, and `.skills/` (6, including `effect-atom-optimistic-updates`, `warden-security-review`, `effect-http-testing`, `cli-release`, `effect-use-pattern`, `graphite`), plus `.codex/environments/`. `AGENTS.md` is a 58-line contributor contract with hard rules (Effect Vitest required, `bun test` forbidden, e2e run last and sparingly, never re-vendor the `@executor-js/emulate` package). Three agent-memory files are deliberately gitignored: `MISTAKES.md`, `DESIRES.md`, `LEARNINGS.md`, private working memory rather than shared team memory. `warden.toml` scopes Sentry's warden-skills security scans by path. The README's "References" section names the codebases fed to the agent as patterns: FumaDB, Effect, OpenCode, OpenClaw, Emdash, Pi.

This is treated separately from the product evaluation because it survives independently of whether Executor itself succeeds. See the guide integration decision below for where each piece lands.

---

## Where it sits relative to the guide's existing coverage

`guide/security/enterprise-governance.md` §3 ("MCP Governance Workflow") already documents this exact category by hand: an approval workflow (§3.1), a YAML registry with per-tool `risk`/`restrictions` fields (§3.2), a hook that enforces it (§3.3). Executor is a productized version of the same pattern, not a new category: its four concepts map onto that registry's fields (Integration ≈ a registry entry's `source` + `config`, Connection ≈ a named authenticated instance of that entry, Policy ≈ the registry's `risk` field generalized to per-tool allow/approval/block, MCP exposure ≈ one endpoint replacing one entry per server).

`guide/ecosystem/mcp-vs-cli.md`'s "Tooling in this space" table (RTK, mcporter, mcp2cli, Klavis AI/Strata, Arcade.dev) is the wrong table for it: that table's shared axis is token cost, and Executor does not compete on token cost. Its axis is access governance, closest to Klavis's OAuth/catalog side, not to mcp2cli's schema-elimination trick.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 3 | The four-concept model and `SecretRef` indirection are clean, but generalize a pattern the guide already documents by hand in `enterprise-governance.md` §3 |
| Production reliability | 2 | Pre-1.0 beta (`1.4.0-beta.0`), bus factor 1, cadence down 76% from peak |
| Documentation quality | 4 | `vision.md` is unusually disciplined about scope, and the vision-vs-shipped gap it names matches what the code shows |
| Adoptability | 3 | Promise SDK avoids Effect for basic use; contributing or deep-wrapping does not |
| Guide value | 3 | Fills no missing category; provides a well-documented, productized example of a pattern the guide already covers |
| **Overall** | **3** | Useful addition, not urgent. No gap-filler. |

---

## Decision

**Integrate as a cross-reference in `enterprise-governance.md` §3, framed as comparison, not as a replacement recommendation. Do not create a standalone integration-governance page.**

`enterprise-governance.md` §3.2's YAML registry is actively copied by teams reading the guide into their own `.claude/mcp-registry.yaml`. A new subsection reading as "use Executor instead" would push readers toward a beta product with a bus factor of one, for a workflow the guide currently documents as a dependency-free YAML file plus a hook. The subsection should read as "here is what automating this registry pattern by hand eventually looks like as a product," with the pre-1.0/bus-factor-1 caveat stated plainly, not implied.

The agentic-engineering configuration (three skill directories, gitignored agent-memory files) is real and reusable independent of Executor's own fate. It is documented separately: the gitignored `MISTAKES.md`/`DESIRES.md`/`LEARNINGS.md` as a fourth data point in `guide/core/memory-systems.md` §3.7's file-based-memory comparison, and the three coexisting skill directories as a new pattern entry in `guide/core/skill-design-patterns.md`. `warden.toml` and the README "References" list are left out of this pass: no existing section fits either cleanly, and forcing one on the evidence of a single repository is premature.

**Revisit trigger**: a tagged `1.0.0` release, or a second maintainer crossing 20% of commits over a rolling quarter, whichever comes first.

---

## Sources

All paths relative to a clone of `github.com/UsefulSoftwareCo/executor` at commit `2f09b13e0` (2026-07-28): `README.md`, `vision.md`, `AGENTS.md`, `RUNNING.md`, `design.md` (visual design system only, not architecture), `package.json`, `packages/core/sdk/src/`, `packages/hosts/mcp/src/tool-server.ts`, `packages/core/execution/`, `packages/plugins/{openapi,graphql,mcp,onepassword,keychain,workos-vault,encrypted-secrets,file-secrets}/`, `packages/kernel/{core,ir,runtime-quickjs,runtime-deno-subprocess,runtime-dynamic-worker,runtime-workerd-subprocess}/`, `apps/cli/src/main.ts`, `.claude/skills/`, `.agents/skills/`, `.skills/`, `.codex/environments/`, `warden.toml`. Git history via `git log --format` and `git shortlog -sn` on the full clone (not truncated by any output-compressing proxy).
