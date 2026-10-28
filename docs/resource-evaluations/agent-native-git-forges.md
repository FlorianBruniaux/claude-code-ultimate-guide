# Agent-native Git forges: Entire, Cursor Origin, Cloudflare Artifacts, Anthropic Scion

**Reviewed:** October 27, 2026. **Trigger:** Entire's launch of a full Git forge on October 26, 2026. **Decision:** integrate a short landscape section in [Third-party tools](../../guide/ecosystem/third-party-tools.md#agent-native-git-forges-2026), and correct every existing Entire CLI passage in the guide against Entire's current documentation.

Scores measure editorial value for this guide, not product quality, security or performance. No product was installed or run for this evaluation. Every claim below was re-read at its primary source on October 27, 2026. A broader secondary scan (press, Hacker News, competitors) was used only to find candidates; claims found only there were left out.

## Sources read

| Source | What it established |
|---|---|
| [Entire launch post](https://entire.com/blog/the-git-forge-for-agent-human-collaboration) (October 26, 2026) | Trails, Gates, distributed hosting, mirror mode, Continuous Memory, Buildkite and Depot CI, ForgeMark figures |
| [entire.com/llms.txt](https://entire.com/llms.txt) and its `.md` pages (trails, code-hosting, cli, sessions, projects) | Product scope, preview and experimental markers, subagent support, redaction |
| [Hosting regions](https://entire.com/regions) (effective October 19, 2026) | Six regions, not the four named in the launch post |
| [Credit Terms](https://entire.com/credit-terms) (effective October 26, 2026) | Prepaid credit billing for Paid Features |
| [Data Processing Agreement](https://entire.com/dpa) | SOC 2 and ISO 27001 cited only for Entire's cloud infrastructure providers |
| [Entire CLI README](https://github.com/entireio/cli) and [CLI reference](https://docs.entire.com/cli-reference) | Real command set (including `blame`, `why`, `checkpoint delete`), install methods, MIT licence, Windows support |
| [Session Storage](https://docs.entire.com/guides/checkpoints/checkpoint-storage) and [Security & Privacy](https://docs.entire.com/security) (verified by Entire against CLI 0.10.2) | Ref-based storage default since 0.10.0, legacy branch storage, shadow branches, redaction layers and limits |
| [Anthropic, Redesigning source control](https://www.anthropic.com/research/redesigning-source-control) (October 13, updated October 15, 2026) | Scion, `scn`, Antique, server-side commits, internal volume figures, merge queue position, "not a suitable replacement for git for general use" |
| [Cloudflare Artifacts](https://blog.cloudflare.com/artifacts-git-for-agents-beta/) (April 16, 2026) | Git-speaking versioned storage for agents, private beta, beta pricing |
| [Cursor Origin announcement](https://forum.cursor.com/t/origin-code-hosting/168670) (August 17, 2026) | Early beta, paid plans only, GitHub as source of truth for synced repos |

## Candidate decisions

| Candidate | Score | Distinct contribution | Decision |
|---|---|---|---|
| Entire forge (Trails, hosting, memory) | 4/5 | First forge that replaces the pull request with agent-scored review and merge Gates; extends the Entire CLI already documented | Landscape section plus corrected CLI coverage |
| Anthropic Scion | 3/5 | Primary data on agent-scale merge volume and on why a classic merge queue breaks; not a product | One paragraph, framed as a lesson, not a tool |
| Cursor Origin | 3/5 | Hosting inside an agent IDE, with GitHub kept as source of truth | One row |
| Cloudflare Artifacts | 3/5 | Programmable Git storage, one repo per agent session | One row; later beta status not re-checked |

## Corrections made to existing guide content

The February 2026 coverage of Entire CLI ([evaluation](./entire-cli.md)) contained claims that the current documentation does not support:

| Previous claim | Current source says | Fix |
|---|---|---|
| "SOC2 Type II certified" | No attestation for Entire found; the DPA cites SOC 2 and ISO 27001 only for infrastructure providers | Removed; stated as not found |
| Commands `entire init`, `capture`, `checkpoint --name`, `log`, `rewind`, `handoff`, `approve --approver`, `review --checkpoint`, `audit-export`, `--compliance-mode` | Absent from the [CLI reference](https://docs.entire.com/cli-reference) | Replaced with `enable`, `checkpoint list/explain`, `session resume`, `search`, `why`, `trail approve/merge` |
| AES-256 encryption at rest, FedRAMP column | Not documented | Removed |
| Checkpoints on the `entire/checkpoints/v1` orphan branch | Ref-based storage under `refs/entire/checkpoints/` is the default since CLI 0.10.0; the branch remains for older repositories | Updated with both backends |
| Written in TypeScript; macOS/Linux only, Windows via WSL | Go CLI; Windows PowerShell installer | Updated |
| Approval gates as a local CLI feature | Gates belong to Trails on the hosted forge | Updated |
| "Path-agnostic" checkpoints with relative paths | Not documented; checkpoints travel because they are Git refs | Reworded, cross-folder resume marked as not verified |
| Storage overhead "~5-10% of project size" | Not documented | Replaced with a measurement procedure |

## What was not verified

- Entire's ForgeMark results (418 pushes per second for Entire against 4.7 for GitHub) and the "up to 71%" token savings of entire-graph: vendor measurements, no independent reproduction found
- Cloudflare Artifacts status after April 2026
- How much of a resumed Claude Code session survives a change of project path
- Competitors seen only in secondary sources (Pierre, GitHub Agent HQ, GitLab Duo Agent Platform, Bitbucket Agentic Pipelines, GitButler, Jujutsu, Graphite, Agent Trace and others) were not re-read and are not cited in the guide from this evaluation

## Tracking

Entire publishes an index at [entire.com/llms.txt](https://entire.com/llms.txt) and a numbered "dispatch" changelog. Re-reading that index and the CLI reference is the cheapest way to keep the guide current. Re-check this evaluation when the Entire CLI reaches 1.0, when Entire publishes a compliance attestation, or when an independent ForgeMark reproduction appears.
