# Evaluation: liza-mas token-saving CLI tools

**Source**: GitHub org [liza-mas](https://github.com/liza-mas) (Tangi Vass)
**Context**: Mentioned in a LinkedIn comment on Soufiane Keli's series on LLM token-cost optimization for technical teams
**Initially evaluated**: 2026-06-10
**Initial evaluator**: Claude Opus 4.8
**Reassessed**: 2026-10-13, against public documentation and selected implementation and test files

## Revised decision

The original evaluation confused Markdown navigation with TOC generation and mistook an npm distribution wrapper for Stacklit's implementation language. It also missed the value of independently addressable artifacts in concurrent worktrees. Those errors invalidate the original blanket rejection and the runtime-based comparison.

| Tool | Initial score | Revised score | Decision |
|------|---------------|---------------|----------|
| scip-search | 1/5 | 2/5 | Specialized candidate for worktree-local symbol navigation |
| mdtoc | 1/5 | 3/5 | Eligible for a bounded Markdown-navigation example |
| functional-clusters | 1/5 | 2/5 | Specialized advisory clustering pipeline |
| stacklit-cli | 2/5 | 3/5 | Eligible for a CLI-first comparison with upstream Stacklit |

These scores assess relevance to the guide, not production readiness. This correction updates evaluations, their index, and watch entries; it does not add new guide sections. mdtoc and stacklit-cli qualify for consideration under the score-3 policy. Representative agent tasks should determine their practical benefit, rather than a GitHub-star threshold.

The 2026-09-01 framework correction still applies: Liza's [toolchain profiles](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/support-docs/TOOLCHAIN.md) expose optional utilities, and its [agent tool contract](https://github.com/liza-mas/liza/blob/a22c12381c5d884d2586a48aaaa517bca184f9cf/contracts/AGENT_TOOLS.md) provides fallbacks. Standalone value and optionality are separate questions.

## Worktree support and index freshness

These tools use files or explicitly selected artifacts rather than requiring one mutable index for all checkouts. The mechanism differs by tool:

| Tool | Documented mechanism | Boundary |
|------|----------------------|----------|
| scip-search | Explicit `--index` path; `reroot` copies an existing SCIP index with a new project root | Re-rooting suits a checkout of the same tree. It does not re-index changed source files |
| mdtoc | Reads supplied Markdown files directly | No persistent index to synchronize; ranges describe the file read |
| stacklit-cli | Generates a checkout's JSON artifact and accepts explicit input/output paths | Regeneration remains necessary after changes. The optional post-commit recipe skips paths under `.worktrees`, so it does not refresh those worktrees automatically |
| functional-clusters | Takes explicit SCIP graph and Stacklit architecture export paths | Artifacts must describe the intended checkout; independent files do not establish freshness |

Sources: [SCIP concurrent indexes and re-rooting](https://github.com/liza-mas/scip-search/blob/16384a7564ec9b5cf93580c26e4a76618242ee53/README.md), [mdtoc behavior](https://github.com/liza-mas/mdtoc/blob/37712275e36b5aef9c9651e633b1896e22d917f3/README.md), [Stacklit CLI refresh recipe](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/USAGE.md), [Functional Clusters inputs](https://github.com/liza-mas/functional-clusters/blob/f1ac506508752660214d4a6d35fd33113177a482/README.md).

Semble's [cache key implementation](https://github.com/MinishLab/semble/blob/0e5e02832ae0340c0feb637d2b7213fe065571fd/src/semble/cache.py) hashes the resolved project path. Distinct worktree directories therefore select distinct index caches. A shared cache directory is not a single shared project index. See the corrected [Semble evaluation](./semble-code-search.md).

No comparative survey was performed to establish that most competing indexers require a centralized index. Worktree compatibility, index reuse, freshness, and concurrent writes need separate evidence.

## Tool-by-tool analysis

### scip-search

**Repository**: [liza-mas/scip-search](https://github.com/liza-mas/scip-search)
**Language / license**: Go / Apache-2.0

SCIP Search queries prebuilt SCIP artifacts for definitions, references, implementations, and graph-derived navigation. Its [command interface](https://github.com/liza-mas/scip-search/blob/16384a7564ec9b5cf93580c26e4a76618242ee53/README.md) supports independently selected indexes and worktree re-rooting. Language indexers are separate dependencies.

The original evaluation grouped it too loosely with semantic search and live LSP navigation. A SCIP artifact can be selected and copied independently of a running editor or service. Conversely, an index can be stale, and static graph/impact results do not establish a complete runtime call graph.

**Score: 2/5.** The artifact model provides a concrete specialized use case. A broader recommendation needs a representative comparison of indexing effort, freshness handling, and navigation accuracy. The historical day-one star count does not decide technical merit.

### mdtoc

**Repository**: [liza-mas/mdtoc](https://github.com/liza-mas/mdtoc)
**Language / license**: Go / Apache-2.0

mdtoc emits source ranges and hierarchical `mdq` selectors for Markdown ATX headings. Its [parser](https://github.com/liza-mas/mdtoc/blob/37712275e36b5aef9c9651e633b1896e22d917f3/internal/mdtoc/toc.go) tracks fenced blocks, computes section ends using heading levels, constructs ancestor paths, and flags duplicate selector paths. Its [tests](https://github.com/liza-mas/mdtoc/blob/37712275e36b5aef9c9651e633b1896e22d917f3/internal/mdtoc/toc_test.go) cover fenced-code exclusion, parent ranges, duplicate paths, and escaping. These files were inspected, not executed here.

A raw heading regex can match shell comments inside fenced examples and leaves section-end calculation and parent-path reconstruction to the caller. Claude Code's [tools reference](https://code.claude.com/docs/en/tools-reference) documents file reads, pattern search, and language-server operations. Those primitives do not by themselves supply mdtoc's Markdown section contract. An agent can script equivalent parsing or read the whole file, but that does not establish that the utility has no value.

The same CLI output can be consumed by Claude Code, Codex, or another agent. Its relevance comes from targeted document navigation, not from requiring a Claude-specific hook. Setext headings are outside the documented scope, and selector compatibility depends on `mdq`. Token savings and agent error reduction were not measured here.

**Score: 3/5.** A concrete addition for agents navigating long specifications. Replace the original rejection with consideration of a short example comparing regex matches, parsed ranges, and targeted reads.

### functional-clusters

**Repository**: [liza-mas/functional-clusters](https://github.com/liza-mas/functional-clusters)
**Language / license**: Go / Apache-2.0

The [current contract](https://github.com/liza-mas/functional-clusters/blob/f1ac506508752660214d4a6d35fd33113177a482/README.md) consumes one or more `scip.graph-export.v1` JSON files and a `stacklit.architecture-export.v1` JSON file, then produces advisory clusters. The [CLI](https://github.com/liza-mas/functional-clusters/blob/f1ac506508752660214d4a6d35fd33113177a482/internal/cli/root.go) exposes `build`, `list`, and `explain`.

The dependency is on artifacts with defined schemas. Consumers do not need upstream tools running during every query. Source and fixtures make isolated evaluation possible, contrary to the original assertion that it cannot be evaluated independently. Generating fresh inputs remains part of an end-to-end assessment.

**Score: 2/5.** An inspectable specialized pipeline, with more preparation than direct search. The reviewed material does not establish whether its clusters improve agent navigation or identify functional boundaries on representative repositories.

### stacklit-cli

**Repository**: [liza-mas/stacklit-cli](https://github.com/liza-mas/stacklit-cli)
**Language / license**: Go / MIT

stacklit-cli is a fork of [glincker/stacklit](https://github.com/glincker/stacklit), whose [implementation is already Go](https://github.com/glincker/stacklit/blob/master/go.mod). Upstream's npm package distributes the binary. The distinction is the CLI interface and extensions, not a Go port of a Node implementation.

The [fork documentation](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/README.md) and [command registration](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/internal/cli/root.go) support these differences:

- Former MCP queries are CLI commands such as `find-module` and `get-dependencies`. The fork removed the MCP/setup surface. Claude Code integration is a manual instruction to read the index, not automatic configuration.
- `init-insights` and `ai-summary` maintain curated metadata incorporated by `generate-json`. `derive --ai-summary` reads the stored summary. The documented workflow drafts fresh insights before reconciling existing ones in one agent session; the ordering is prompt-directed, not an access barrier.
- Parsing uses a configurable worker pool, with a default of 3 and a command-level override. The [engine tests](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/internal/engine/engine_test.go) compare normalized output across worker counts. They were inspected, not run here. The [dependency file](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/go.mod) uses gotreesitter v0.53.0.
- `export-architecture` reads an existing index and writes the schema used by Functional Clusters. `diff` distinguishes a current index (0), stale sources (1), and command failure (2).

The [published worker benchmark](https://github.com/liza-mas/stacklit-cli/blob/3c0e04153fe10dde2eeb4ddff72417c7621d5436/specs/benchmarks/map-reduce/benchmark-report.md) documents an earlier implementation and a private workload. It does not establish the current fork's indexing performance after the parser upgrade. Later performance improvements reported by the maintainer lack a matching public benchmark in the inspected material and were not independently reproduced here. Headline token-reduction claims also remain unverified. Worker tuning and the parser upgrade should not be conflated into one measured cause.

**Score: 3/5.** The interface, insights workflow, and architecture export provide distinct value for a bounded comparison. Prior integration gives upstream no exemption from the same evidence standard. A full recommendation needs representative navigation tasks and reproducible measurements, not 50 stars.

## Challenge and evidence limits

The original challenge accepted upstream Stacklit because it had already been integrated and dismissed the fork for low traction. That was inconsistent. This reassessment asks what each utility supplies, what an agent must still do, and which improvements have been measured.

Source inspection supports corrected interfaces and artifact boundaries. It does not prove concurrent correctness, agent adoption, production suitability, or token savings. Go was unavailable in this review environment, so no Go tests or CLI behavior checks were run. Test definitions document intended coverage, not a passing result from this review.

| Candidate | Next comparison needed |
|-----------|------------------------|
| mdtoc | Long Markdown with fenced comments, nested headings, and duplicates; compare correctness and total agent tokens against regex plus targeted reads |
| stacklit-cli | Upstream and fork on the same public repositories; compare extraction, freshness handling, wall time, peak memory, and successful agent navigation |
| scip-search / functional-clusters | Two divergent worktrees with separately regenerated artifacts; verify paths, freshness, and usefulness of navigation or clustering |

The [watch list](./watch-list.md) tracks mdtoc and stacklit-cli pending these comparisons. No new guide section or production recommendation is implied by this correction.
