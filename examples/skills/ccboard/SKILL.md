---
name: ccboard
description: "Read Claude Code usage data with the ccboard CLI: token and cost stats, recent or searchable sessions, usage reports, skill invocation counts, and the TUI or web dashboard. Use when asked about token usage, spend, session history, which skills actually ran, or how to launch ccboard. Not for editing Claude Code settings."
allowed-tools: Bash(ccboard *)
effort: low
metadata:
  verified-with: "ccboard 0.25.0"
---

# ccboard

ccboard is a single Rust binary (TUI and web dashboard) that reads Claude Code data from `~/.claude/` without modifying it. Source: https://github.com/FlorianBruniaux/ccboard

## How Claude should use it

The TUI (`ccboard`) is interactive and cannot be driven through the Bash tool. Tell the user to run it in a separate terminal, and answer questions yourself with the non-interactive subcommands below.

Check installation first:

```bash
ccboard --version
```

If the command is missing, give the install options (do not install without being asked):

```bash
brew tap FlorianBruniaux/tap && brew install ccboard   # includes the web frontend
cargo install ccboard                                  # needs Rust 1.85+; `ccboard web` serves no frontend
```

## Non-interactive subcommands

| Goal | Command |
|------|---------|
| Totals for tokens, sessions, models | `ccboard stats` |
| Last N sessions | `ccboard recent 10 --since 7d --json` |
| Find sessions by text, project or branch | `ccboard search "query" --since 30d --limit 20 --json` |
| One session in detail | `ccboard info <session-id>` |
| Usage report with optional CI gates | `ccboard report --format markdown --since 7d` (`--budget <tokens>`, `--error-threshold <pct>` exit 1 when exceeded) |
| Which skills actually ran | `ccboard skills --since 30d --json` |
| Suggestions for skills, commands and CLAUDE.md rules | `ccboard discover` |
| Export data to files | `ccboard export` |

Global options: `--claude-home <path>` (or `CCBOARD_CLAUDE_HOME`), `--project <path>`, `--format json|table`, `--no-color`, `--non-interactive`. Run `ccboard <subcommand> --help` for the exact flags of the installed version.

Prefer `--json` when the output feeds further analysis. Session data can contain prompts and file contents: summarize it, and do not paste raw transcripts into shared places.

Not read-only: `ccboard setup` injects hooks into Claude Code `settings.json`, `ccboard resume` starts a Claude session, and `ccboard summarize` calls an LLM. Run these only when the user asks for them by name.

## Dashboards for the user

```bash
ccboard                    # TUI (default)
ccboard web --port 3333    # web UI, default port 3333
ccboard both --port 3333   # TUI and web server together
```

In the TUI, tabs are reached with the number keys (`1-9`, `0`, `p`), `?` opens contextual help, `:` opens the command palette, `r` refreshes, `e` edits the selected file in `$EDITOR`, `o` reveals it, `q` quits. The tab list and its order change between releases, so point to `?` or the project's `docs/GUIDE.md` instead of quoting a fixed mapping.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| `ccboard: command not found` | Install it, and confirm `~/.cargo/bin` or the Homebrew prefix is on `PATH`. |
| No data | `ls ~/.claude/projects` exists and holds session files; pass `--claude-home` for a custom location. |
| `ccboard web` shows no page | The binary came from `cargo install`, which skips the web frontend. Use the Homebrew or release binary. |
| Stale numbers after a Claude Code upgrade | `ccboard clear-cache`, then rerun. |

## Bundled files

`README.md` and `commands/` describe the original plugin packaging (`/dashboard`, `/costs`, `/sessions`, `/mcp-status`, `/ccboard-web`, `/ccboard-install`). `scripts/` holds the install helpers those commands call.
