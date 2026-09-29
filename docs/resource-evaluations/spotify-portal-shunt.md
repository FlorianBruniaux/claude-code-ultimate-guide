# shunt (Spotify Portal): hook-enforced delegation of file reads to a cheaper model

## Evaluation metadata

| Field | Value |
|---|---|
| Resource | [spotify/portal-ai-plugins](https://github.com/spotify/portal-ai-plugins), plugin `plugins/shunt` |
| Article | [Portal by Spotify cut my Claude Code token usage by 90%](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90) (Spotify Engineering blog, also on the Portal blog) |
| Type | Claude Code plugin: two `PreToolUse` hooks, two delegation scripts, two skills |
| License | Apache-2.0 |
| Evaluated | 2026-09-29, at commit [`3c24ca3`](https://github.com/spotify/portal-ai-plugins/tree/3c24ca30ff63e1f5bbad1c43fe5324daff579123), Claude Code 2.1.284 |
| Decision | Integrate as a pattern in `guide/ecosystem/context-engineering-tools.md` §3 and the cost levers table of `guide/ultimate-guide.md` |
| Score | 3/5 |

## Verdict

shunt is not a compressor. It is a delegator: when Claude tries to read a large file, a hook blocks the read and points Claude to a script that sends the files to another model (Gemini 2.5 Flash by default) through Spotify Portal. Claude only receives the worker model's answer. The article's 90% figure measures tokens entering Claude's context on three read scenarios. It does not count the worker model's tokens, answer accuracy, or the extra turn caused by the block.

The tool itself only runs for Portal customers. Portal is Spotify's managed, commercial Backstage offering: a free trial, then pricing through sales, with the AiKA assistant included ([Portal vs Backstage](https://info.backstage.byspotify.com/portal-vs-backstage)). Without a Portal instance, the hooks block reads but the delegation fails.

What earns a place in the guide is the pattern, not the product: a routing rule enforced by a hook instead of an advisory line in `CLAUDE.md`. The author says so directly: the first version was a block of routing rules in `CLAUDE.md`, and "the rules were advisory, not enforced". It also contradicts a sentence in the guide that treated model routing as an API-pipeline technique only.

## Measured facts

GitHub API and a clone of the repository, 2026-09-29.

| Metric | Value |
|---|---|
| Stars / forks / open issues | 2,310 / 190 / 11 |
| Repository created | 2026-07-23 |
| Commits on `main` | 6, last push 2026-08-17 |
| shunt commits | 2, one author, 2026-08-14 |
| shunt version | 0.2.0, Claude Code only (no Codex or Cursor manifest) |
| CI | None (no `.github/` directory) |

## How it works, with sources

1. **Read hook.** [`check-file-size`](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/hooks/check-file-size) runs on every `Read`. A full read (no `offset`, no `limit`) of a file above 350 lines (`SHUNT_MIN_LINES`) is blocked with a reason that names the `/bulk-reader` skill.
2. **Bash hook.** [`check-bash-read`](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/hooks/check-bash-read) applies the same rule to `cat`, `head`, `tail`, `less` and `more`, except when the command contains a pipe or a `>`.
3. **Delegation.** [`bulk-read`](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/scripts/bulk-read) wraps each file in `<file path="...">` tags, appends the question and calls `portal-cli actions aika:invoke-chat` on the `bulk-reader` mode. [`code-write`](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/scripts/code-write) sends a spec and one reference file to the `code-writer` mode and can write the result straight to disk with `--target`.
4. **Transport.** [`aika.sh`](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/scripts/lib/aika.sh) passes the request through argv (ceiling 400 KB on macOS, 120 KB on Linux), resolves the mode by name (own modes first, then the caller's groups, then public ones) and discards any answer where the mode was not applied.

## Claims against evidence

| Claim | What the evidence supports |
|---|---|
| "Spotify cut Claude Code token usage by around 90%" (LinkedIn relays) | The article title says "my": one engineer's benchmark, not an organization-wide measurement |
| 90% mean savings | Mean of three read scenarios (82%, 94%, 94%) on a private 162K-line Java monorepo. Not reproducible. The repository fixtures are three TypeScript files |
| Token counts | Estimated as characters divided by 4, and only for Claude's context. The worker model's tokens are not reported |
| code-write savings | The benchmark script sets the "with shunt" cost to 0 by construction and weights generated tokens 5x |
| "Portal caps a single invocation at 30 seconds" (article) | The shipped script defaults `SHUNT_TIMEOUT_SECONDS` to 180 |

Apply the checklist in [How to read a vendor's cost-reduction claim](../../guide/ops/ai-unit-economics.md#6-how-to-read-a-vendors-cost-reduction-claim) before quoting the figure.

## Defects

Tested live with `claude --plugin-dir` on Claude Code 2.1.284, without a Portal instance, so only the hook behavior was exercised.

| Defect | Status |
|---|---|
| A full `Read` above 350 lines is blocked; a 35-line file reads normally | Confirmed live (works as designed) |
| A PDF is blocked as text: `wc -l` counted 4,471 newline bytes in a PDF, and `bulk-read` would send the binary to the worker model | Confirmed live |
| The Bash hook ignores any path starting with `~`: `head -100 ~/…` passes, the same command with an absolute path is blocked. The hook tests `[ ! -f "$file_path" ]` on the literal string ([line 33](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/hooks/check-bash-read#L33)), and a quoted `~` is not expanded | Confirmed live; not covered by the repository's 51 evals |
| `head -n 5 file` passes because the parser takes `5` for the file name; `head -100 file` (a 100-line read) is blocked | Documented as a known bug in the repository's own evals (`bash-hook-evals.json`, case 17) |
| `offset: 0` or `limit: 0` bypasses the Read hook, and the block message itself suggests re-reading with `offset`/`limit` | Documented in the evals; the hook steers rather than enforces |
| Hooks print the deprecated top-level `decision` field. The [hooks reference](https://code.claude.com/docs/en/hooks) maps only `"approve"` and `"block"`; the `{"decision": "allow"}` the hooks print on every pass-through is not a documented value | No visible error in the live test. Whether it is ignored or treated as an approval was not verified |
| `code-write --target` writes through a Bash call, so hooks and permission rules scoped to `Edit` and `Write` do not see the file, and Claude never reads the generated code by design | Code reading |
| Mode resolution prefers group modes over public ones: a colleague's mode named `code-writer` receives your specs and its output lands in your repository | README and `aika.sh`; not exercised |
| `npx --yes @spotify/portal-cli` runs the latest published CLI with your Portal credentials when no global install exists | Code reading ([`aika.sh` line 37](https://github.com/spotify/portal-ai-plugins/blob/3c24ca30ff63e1f5bbad1c43fe5324daff579123/plugins/shunt/scripts/lib/aika.sh#L37)) |
| The 180-second invocation timeout exceeds the Bash tool's 120,000 ms default (`BASH_DEFAULT_TIMEOUT_MS`), so long delegations are cut on Claude's side first | Code reading; not exercised |
| Without `jq`, both hooks allow everything silently | Code reading |

What is done well: the Portal workflow skills require a dry run and explicit confirmation before any mutation and never ask for credentials in chat, `aika.sh` separates stderr from the JSON envelope and refuses mode-less answers, and the README lists what the plugin does not delegate (debugging, editing, architecture decisions).

## Comparison with existing guide coverage

| Tool in the guide | Layer | Mechanism | Difference with shunt |
|---|---|---|---|
| RTK | Shell output | Deterministic local filters | Different layer: bash output is ~12% of session tokens, file reads ~65% |
| lean-ctx, tilth | File reads | Local structural compression (tree-sitter) | Same layer. They cut tokens without adding a model or sending code off the machine |
| Headroom | Tool outputs, structured data | Local compression with lossless retrieval | Reversible; shunt's summaries are not |
| Edgee | Gateway between client and API | Output brevity, tool catalog reduction, result trimming | The gateway sees all traffic; shunt only sees the files it delegates |
| Subagent with `model: haiku` | File reads, on demand | Native delegation in an isolated context | Same pattern, code stays with Anthropic, no extra vendor. Not enforced unless a hook redirects to it |

## Integration

| Location | Change |
|---|---|
| `guide/ecosystem/context-engineering-tools.md` §3 | New entry "shunt (delegation, not compression)" after tilth, and a row in §10 |
| `guide/ultimate-guide.md`, Cost Optimization Levers | Model routing row and the RouteLLM note: routing can be enforced in interactive sessions by a hook |
| `machine-readable/reference.yaml` and its MCP mirror | Keys for the guide entry and this evaluation |

## Fact-check

| Claim | Verified against |
|---|---|
| Stars, forks, issues, license, creation and push dates | GitHub API, 2026-09-29 |
| Commit count, shunt authorship and dates | `git log` on the clone |
| Hook thresholds, bypass rules, argv ceiling, timeout default, `npx --yes` | Source files at the evaluated commit |
| 51 evals pass | `bash plugins/shunt/evals/run.sh`, run on the clone |
| Read block, PDF block, `~` bypass, absolute-path block | Live session, Claude Code 2.1.284, `claude --plugin-dir` |
| Deprecated `decision` mapping | Claude Code hooks reference, PreToolUse decision control note |
| Portal pricing model | Spotify for Backstage public pages; no list prices published |

Not verified: any real delegation through Portal (no instance available), the token savings themselves, the effect of the undocumented `"allow"` value, and the Bash timeout interaction.
