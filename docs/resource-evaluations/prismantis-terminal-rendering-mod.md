# Resource evaluation: prismantis (Claude Code terminal rendering mod)

**URL**: https://github.com/NahumLitvin/prismantis
**Type**: GitHub repository, Claude Code plugin distributed through its own marketplace (`prismantis@prismantis`), a mod (TypeScript function hooks)
**Evaluation date**: 2026-10-31
**Evaluator**: Claude Code Ultimate Guide Team
**Guide version**: 3.44.1
**Method**: README read on the default branch (`main`) through the GitHub API; release list and v0.38.0 notes; issues #209 and #319 with their timestamps; contributor and release counts through the GitHub API; the maintainer's launch post read in full; `claude plugin validate` run on a clone at commit `dc51f35` (v0.38.2); text search of the shipped `hooks/` code for network APIs. The author of this guide uses and recommends the mod, and filed issue #319. No token measurement, no code audit, and no rendering test was run for this evaluation.

---

## Content summary

prismantis redraws what Claude Code shows in the terminal. Replies get colored tables, Prism syntax highlighting in 24 languages, mermaid flowcharts, sequence, state, class and ER diagrams, `xychart-beta` charts, pies, and `figure` blocks drawn as written. Tool rows become one-line summaries and edits become diff cards. Slash-command output and the user's own prompts are restyled too. Each block gets copy buttons, and `/prismantis copy` covers keyboard-only use.

It is built on the mod API that shipped in Claude Code 2.1.287 (October 1, 2026): a `ui.render` hook receives each piece of the transcript before it is drawn and returns what to draw instead. The maintainer's launch post (https://www.catchkill9.dev/posts/prismantis.html) dates the first release to October 2, 2026.

The one thing it sends the model is the optional `diagramHints` note, attached to each prompt, which tells Claude what the terminal can draw. The README gives about 630 tokens per prompt (about 275 for the main part, about 360 for the figure part) and about 80 more while `latex` is on, counted with Claude's tokenizer.

---

## Fact-check results

| Claim (source) | Status | Evidence |
|---|---|---|
| Install: `/plugin marketplace add NahumLitvin/prismantis`, `/plugin install prismantis@prismantis` (README l.34-38) | Verified in README | README on `main`, read 2026-10-31 |
| Requires Claude Code 2.1.287+ (README l.45) | Verified in README | Also the badge at l.9 |
| Update: `claude plugin marketplace update prismantis && claude plugin update prismantis@prismantis`, then `/reload` per session (README l.47-50) | Verified in README | Not executed for this evaluation |
| 17 themes | Verified in README and launch post | README l.29: "16 palettes plus `mono`"; l.69: "17 themes". The GitHub repository description still says 15 |
| `⧉ html` gives "a real Slack table on macOS" (brief for this evaluation) | Not found in README | README l.203: formatted table plus a tab-separated copy; Slack is named for `⧉ art` (l.203) and `▣ png` (l.206). Guide text follows the README |
| About 630 tokens per prompt, about 710 with `latex` | Verified in README, not measured | README l.262 and l.437. Stated in the guide as the maintainer's figure |
| `listMarker: dash` added in 0.38.0 | Verified | Release notes v0.38.0, PR #320 |
| Latest version | 0.38.2 | `gh release list`, published 2026-10-30 14:07 UTC |
| Issue #319 timeline | Verified | Opened 2026-10-30 06:10:02 UTC; v0.38.0 published 08:53:00 UTC; maintainer comment 09:05:10 UTC, closed 09:05:11 UTC |
| Featured in Awesome Claude Code | Verified notification | Issue #209 opened by the list maintainer on 2026-10-18 |
| No network calls (README l.31, l.437) | Partially checked | `claude plugin validate` `calls:` line lists no network API; text search of `hooks/` for `fetch`, `http`, `https`, `net`, `WebSocket` found nothing. Static check of one commit, not an audit |
| 64 releases, 22 contributors besides the maintainer (launch post) | Consistent | API: 64 releases (oldest listed v0.3.1, 2026-10-02), 24 contributors |

---

## Project health

Measured 2026-10-31 through the GitHub API.

| Metric | Value |
|---|---|
| Stars | 266 |
| Contributors | 24 |
| Releases | 64 between 2026-10-02 and 2026-10-30 |
| Latest release | v0.38.2 (2026-10-30) |
| License | MIT (`LICENSE` file present, detected by GitHub) |
| Last push | 2026-10-30 |
| Hand testing | macOS terminal only, per README; CI on macOS, Linux, Windows |

The release cadence is very high (several releases a day at launch). That is good for responsiveness and a reason to read release notes before updating: a session keeps the version it loaded until `/reload`, so different open sessions can run different versions.

---

## Validator output (commit `dc51f35`, v0.38.2)

`claude plugin validate` passed with one plugin-directory warning (no icon). Relevant lines:

- `hooks:` includes `ui.render` on assistant messages, user messages, tool rows and command output, plus `tool.call`, `prompt.submit`, `turn.complete`, `session.start` and `command.run{command=prismantis}`
- `calls:` includes `$.process.run` (through the clipboard helper and LaTeX typesetting), `$.ui.copy`, `$.fs.read`, `$.fs.stat`, `$.config.set`, and `$.session.messages`
- `env writes: nothing`; env reads are terminal detection variables (`TERM_PROGRAM`, `SSH_CONNECTION`, `TMUX`, `KITTY_WINDOW_ID` and similar)
- Five gating hooks without `.catch` (`tool.call`, `prompt.submit`, `ui.focus`, a `ui.scroll` on its setup pane, `prismantis.markdown`). This is a validator notice, not an observed failure

`tool.call` being a gating hook means the mod sits on the tool-call path. Nothing in this evaluation shows it altering tool calls; the README describes only drawing. That is the kind of declaration to re-read on each update.

---

## Where it sits relative to the guide's existing coverage

The guide explains mods in `guide/ultimate-guide.md` (Claude Mods v2.1.287+) with Anthropic's samples but no community example. `guide/ecosystem/third-party-tools.md` lists replacement interfaces under Alternative UIs (Claude chic, Toad, Conductor). prismantis is neither: it keeps Claude Code's own interface and changes how it is drawn. No existing entry covers terminal rendering, copy-to-Slack fidelity, or the token cost of a mod that injects model context.

The `diagramHints` note is also a concrete, documented case of a plugin adding context to every prompt, which connects to the guide's context engineering material: the cost is per prompt, user-level, and invisible in the transcript.

---

## Scoring

| Criterion | Score | Justification |
|---|---|---|
| Technical novelty | 4 | One of the first public mods built on the 2.1.287 `ui.render` API; covers rendering, copying and model nudging together |
| Production reliability | 3 | Fast and responsive maintenance, MIT, CI on three OSes; hand testing on macOS only, very young project (October 2, 2026), high release churn |
| Documentation quality | 5 | README documents every option and default, side effects, programs run, token cost with its breakdown, and a section for LLM agents |
| Adoptability | 5 | Two commands to install, one to update, turned off from `/plugin` |
| Guide value | 4 | Fills the gap of a community mod example and a terminal rendering category; used and recommended by the guide's author |
| **Overall** | **4** | Integrate with the token cost stated as the maintainer's figure and the security check shown |

---

## Decision

**Integrated** in `guide/ecosystem/third-party-tools.md`, new section "Terminal rendering (mods)", with a persona row in "Recommendations by persona". The entry states the `diagramHints` cost as the README's figure, explains when to turn the hints off, shows the validator check and its limit, and dates the maintainer's response to issue #319.

**Not done**: a cross-reference from the mods section of `guide/ultimate-guide.md`. The repository's anti-AI hook evaluates the whole file after an edit, and that file already contains em dashes in prose, so the edit was refused. Add the cross-reference once those are cleaned up.

**Open evidence gaps**: measure the actual per-prompt token cost (`/context` with and without `diagramHints`), and check rendering in the Desktop app and VS Code.

---

## Sources

- Repository and README (default branch `main`): https://github.com/NahumLitvin/prismantis
- Release v0.38.0: https://github.com/NahumLitvin/prismantis/releases/tag/v0.38.0
- Issue #319: https://github.com/NahumLitvin/prismantis/issues/319
- Issue #209 (Awesome Claude Code notification): https://github.com/NahumLitvin/prismantis/issues/209
- Maintainer's launch post: https://www.catchkill9.dev/posts/prismantis.html
- Official mods overview: https://code.claude.com/docs/en/plugins/mods/overview
