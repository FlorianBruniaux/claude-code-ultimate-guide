# e2e (agentic end-to-end testing framework): documentation review

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [e2e-inc/e2e](https://github.com/e2e-inc/e2e) (the older URL `tester-army/e2e` redirects to it), npm package `e2e` |
| Suggested by | Issue #112, by a contributor to the project who disclosed it. Evaluated as skeptically as any vendor suggestion |
| Type | Open-source test runner and CLI (TypeScript), with a stdio MCP server (`npx e2e mcp`), a Claude Code plugin of skills, and engines for web, iOS and Android |
| License | Apache-2.0 |
| Evaluated | 2026-11-25, `main` at [`d6a7bbc`](https://github.com/e2e-inc/e2e/tree/d6a7bbcf1aab80527728b2f1f48c064a025f0889), npm `latest` 0.24.0 |
| Method | Documentation and repository read through the GitHub API and the npm registry. e2e.com was not reachable from the sandbox, so the docs were read from the repository's `docs/` folder. Nothing was installed or run |
| Decision | Short entry under "Browser automation" in `guide/ecosystem/mcp-servers-ecosystem.md`, with the caveats below. Not scored under that page's server framework |
| Score | 3/5 |

## Verdict

e2e is a real, actively developed project whose design is sound on paper: deterministic locators by default, agent goals only where a selector would break, and a replay cache that records an agent step only after a later check verified it. It fills a gap the [agent-browser evaluation](./2026-03-04-agent-browser-vercel-labs.md) leaves open (that tool is "not a Playwright replacement for traditional E2E suites"), and it is the only mobile-capable tool in this part of the guide. A grep of `guide/` for Detox, Maestro, Appium, XCUITest and simulator or emulator terms found nothing relevant.

It stays at 3/5 and not 4/5 for four reasons. It is pre-1.0 and ships a new minor every one to two weeks. The agent half had no independent exercise: the one hands-on review found did not run agent steps. The suggestion is vendor-authored. And nothing in this review was executed, so every capability below is "per the documentation".

## Claims in the issue, against the source

| Claim in the issue | What the source says |
|---|---|
| Apache-2.0, web, iOS and Android | Confirmed: `LICENSE`, npm `license` field, README package table (`@e2e-dev/web` through Playwright, `@e2e-dev/mobile` through agent-device) |
| Agent flows are kept as test files that run in CI | Confirmed: `*.e2e.ts` files, CI guides for GitHub Actions, GitLab, Bitrise, Codemagic |
| Replay "with no model calls until the app changes" | True for `agent.act` only. `docs/cache.mdx`: "`agent.assert`, `agent.waitFor`, and `agent.extract` always run live". A step is recorded only when a later check passes. `e2e init` gitignores `.e2e/cache/`, so CI starts with no recordings unless they are committed. A stale recording hands the step to the model unless `--strict-cache` is set. Retries never replay |
| Tests without agent steps need no model | Confirmed by the README ("They need no model and no key") |
| `npx e2e mcp` is a stdio MCP server, no model needed | Confirmed in `docs/mcp-server.mdx`. Each action returns the test line that repeats it |
| `claude mcp add --scope project e2e -- npx e2e mcp` | Confirmed verbatim in `docs/mcp-server.mdx` |
| Claude Code plugin with skills | Confirmed, with a limit the issue omits: `plugins/e2e/README.md` says the Claude Code plugin has no MCP server, so the `claude mcp add` step is still required. The plugin is "not listed in any client's public directory" |
| Bring your own model, including Claude Code over the Agent Client Protocol | Confirmed in the README package table (`@e2e-dev/acp`). Not run |
| Pre-1.0, telemetry on by default, opt out with `E2E_TELEMETRY_DISABLED=1` | Confirmed. `docs/telemetry.mdx` also lists `DO_NOT_TRACK=1` and `npx e2e telemetry disable`, and two details the issue omits: a persistent `distinct_id` plus a `project_id` hashed from the repository's root commit, and one `e2e_mcp_session` event per MCP session carrying the client name and tool-call counts. The documentation says test content, URLs and credentials are never sent. That statement was not tested |

Other documented limits worth knowing: secrets typed through `type_secret` are hidden from the agent, but screenshots mask secure fields only and videos from `start_recording` are not masked; typed values other than secrets are stored as typed in the replay cache; agent steps send the redacted screen to the model provider the user configures.

## Notoriety signals, checked at the source (2026-11-25)

| Signal | Value | Reading |
|---|---|---|
| Repository | `e2e-inc/e2e`, created 2026-07-22, renamed from `tester-army/e2e` (the old path resolves to the same repository and creation date) | Young |
| Stars / forks | 14,224 / 796 (REST API) | High for four months. Star history **not verified**: the stargazers REST endpoint returned 404 and the GraphQL `stargazers` connection returned a total of 0 while `stargazerCount` was 14,224, so no distribution over time could be checked |
| Contributors | 117 (page 1 of the API returned 100, page 2 returned 17); top two are `okwasniewski` (729 commits) and the issue author (163) | Real breadth, but the author of the suggestion is the second most active committer |
| Issues and pull requests | 49 open issues, 326 closed issues, 1,447 merged pull requests (search API). The `open_issues_count` field of 111 includes open pull requests | Very active; a bot-assisted workflow is described in `AGENTS.md` |
| Releases | `e2e@0.24.0` on 2026-11-19; 86 versions on npm including nightlies | A minor every one to two weeks, plus nightly builds |
| npm downloads | 1,495,070 in the last week across versions. Only 847 of those are on 0.0.x and 0.1.0, which are the 2014 to 2016 versions of the earlier package with the same name | The name reuse does not explain the volume. It still counts installs from CI runners and nightly pulls, not users, and is not used as adoption evidence in the guide |
| Independent coverage | Show HN, 2026-10-12: 9 points, 2 comments (posted by a maintainer). One third-party review (andrew.ooo, 2026-10-11) that ran the locator-only half and could not verify the agent half | Thin next to 14k stars. No independent test of the agent steps or the replay cache was found |
| Maintainers | npm lists two maintainers, published through GitHub Actions with provenance. The Show HN post says the poster co-founded TesterArmy, a commercial testing platform; a search snippet of the README at tag `e2e@0.21.1` reads "Made by TesterArmy" (not re-read at the source) | Commercial backing, open-source core |

The gap between the star count and the discussion volume is not proof of anything, and no manipulation is claimed. It means stars are not used as the reason for the score.

## Challenge

The review plan called for a second agent to challenge the score. It was not run in this session; the challenge below is the author's own.

- For a higher score: the documentation is unusually specific about its limits (cache reasons, `--strict-cache`, telemetry fields), which is a good sign of a maintained product.
- Against: the guide cannot recommend a tool it has not run. A 4 would need a local run of the MCP server on a web app, one mobile session, and a replayed `agent.act` step in CI.

## Integration

- `guide/ecosystem/mcp-servers-ecosystem.md`: new "e2e (agentic test runner, documentation review)" entry at the end of "Browser automation", with the setup command, what it adds, and the caveats above. No quality score, and the category counts in "Statistics & insights" are unchanged because the entry is not a validated server.
- `machine-readable/reference.yaml` and `mcp-server/content/reference.yaml`: `e2e_mcp_guide`, `e2e_mcp_install`, `e2e_mcp_evaluation` and `e2e_mcp_status`.
- Not edited: `guide/ultimate-guide.md` and `guide/ultimate-guide.fr.md`.

## Not verified

- Star history over time (endpoints failed, see above).
- Anything executed: the MCP server, the Claude Code plugin, a mobile session, the Agent Client Protocol path, replay in CI, and the content of the telemetry payload.
- The e2e.com website itself (blocked in the sandbox); the repository docs were read instead.
- That the npm download volume reflects human use.
