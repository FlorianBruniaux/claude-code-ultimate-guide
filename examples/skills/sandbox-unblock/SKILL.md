---
name: sandbox-unblock
description: >
  Diagnostic protocol to run before reporting a sandbox blocker or asking for a
  configuration change. Eleven checks that eliminate false positives, then a
  report template the person holding the settings can act on. On one measured
  day, six of eight reported blockers turned out to be false, all from the same
  handful of method errors.
when_to_use: >
  Whenever a command fails with "operation not permitted", "EPERM", "permission
  denied", "listen EPERM", "ENOTFOUND", "x509: OSStatus", or an unexplained
  network timeout. Also on "I'm blocked by the sandbox", "the sandbox won't let
  me", "sandbox violation", when a command fails right after you read the
  sandbox description in the system prompt, when you hesitate to run git, gh,
  ssh, docker, pnpm, npm, yarn or tsx for fear of a refusal, and before writing
  any blocker report meant for another session.
allowed-tools: Read Grep Bash
effort: medium
---

# Unblock a session slowed by the sandbox

A blocker report is cheap to write and expensive to act on. This skill front-loads
the verification so the report that reaches a maintainer is worth their time.

The measurements quoted below come from a single macOS machine, on Claude Code
2.1.220 (July 2026) through 2.1.302 (October 2026). Treat the numbers as
illustrative and the method as the point.

## Self-diagnosis, all eleven checks, before you complain

Run these in order. Each step says what to run, what to read, and what the result
lets you conclude. Steps 3, 3b, 5b and 5c pay for themselves fastest.

**1. Do not infer anything from the sandbox description in your system prompt.**

It lists `permissions.deny Read(...)` patterns under `read.denyOnly`, things like
`**/*.pem` or `**/.env*`. Whether those patterns reach a Bash subprocess has
changed across versions and still varies by location: on 2.1.302 a sandboxed
`wc -c` read a `.env` outside the project that such a rule covered, while a
September build refused `ls` on a project `.env`. One session concluded an entire
Python pipeline was unrunnable from that list alone; every step of it worked when
measured. Measure the exact read you care about.

**2. Confirm the command you are testing actually ran sandboxed.**

```bash
echo $TMPDIR
```

A path under the sandbox temp root (`/tmp/claude-NNN`) means the measurement
counts. The system temp directory (`/var/folders/.../T/`) means the invocation
escaped, and nothing that follows it proves anything about sandboxed behavior.
Run this in its own call: chaining it to the command under test changes the
answer (step 3).

**3. Test the command alone, nothing before it, nothing after it.**

Since v2.1.277, every command in a call must match an `excludedCommands` entry.
A `cd ... &&`, a `;`, a pipe, a redirect to a file or a `$(...)` substitution keeps
the whole call sandboxed, even when the entry for your tool exists and is correct.

The shell working directory persists between Bash calls inside the project, so
there is no need for a `cd` on the same line. Pass a path as an argument when the
command accepts one.

```bash
# wrong: the call no longer matches any entry, everything stays sandboxed
cd /path/to/project && pnpm exec prisma migrate status
pnpm exec prisma migrate status | head -20
pnpm exec prisma migrate status > out.log 2>&1

# right: one command, bare, read the raw output
pnpm exec prisma migrate status
```

An earlier version of this skill recommended `cd /path && command` as the right
form. Every probe of the diagnosis that followed carried a `| head` or an
`&& echo`, and the session wrongly concluded that `excludedCommands` was inert.

**3b. No inline code in quotes in the measured command.**

`node -e "console.log(require('fs').readdirSync('/path'))"` stayed sandboxed while
`node probe.js`, doing exactly the same thing, escaped. Quotes and parentheses
defeat the analysis of the line. Write the code to a file with the Write tool,
then run it by path.

**3c. Never accept a probe typed by the user at the `!` prompt.**

A command typed with the `!` prefix runs outside the sandbox in most sessions.
It succeeds whatever the state of `excludedCommands`, so its success proves
nothing. Measured: the same probe returned a directory listing when typed with
`!`, and `EPERM scandir` when run by the agent at the same moment.

**4. Check the binary exists before blaming the sandbox.**

Wrappers that compress output often replace a clear message with a bare errno.
A missing binary and a security refusal then look identical on screen.

```bash
command -v <binary>
```

Nothing returned means you have an installation problem, not a policy problem.

**5. Read the real exit code, not a pipe's.**

`cmd | head` returns the exit status of `head`, never of `cmd`. A refused read
earlier in the session also emits a warning on every later command, including
the ones that succeed, so read the last message rather than the first.

This conflicts with step 3: a redirect also keeps the call sandboxed. For a
command that depends on `excludedCommands`, take the bare form and accept the raw
output. Use the redirect below only for a command that is sandboxed anyway.

```bash
cmd > out.log 2>&1
echo "exit: $?"
```

**5b. Check whether a command rewriter sits between you and the matcher.**

This one explained most of the blockers on the day it was found. If a
`PreToolUse` hook rewrites Bash commands, for example a token-compression proxy
that turns `pnpm exec tsx x.ts` into `proxy pnpm exec tsx x.ts`, then an
`excludedCommands` entry written as `pnpm exec *` no longer matches anything.
Only the rewritten form matches.

The tell is an inconsistency: some excluded commands escape the sandbox and
others do not, with no obvious pattern. Look at whether the ones that work happen
to have a prefixed entry in the list. You can also feed the hook a synthetic
payload and read whether it rewrites the command; test a command you know it
rewrites first, so an empty answer is not mistaken for a broken probe.

Any entry you request should be asked for in both forms, bare and prefixed, and
scoped as narrowly in both: a prefixed `proxy git *` covers every git subcommand.

**5c. An entry matches the command exactly as written.**

`git fetch origin` matches `git fetch *`. `git -C /path fetch origin` and
`git -c key=value fetch origin` do not, because the option sits before the verb.
`pnpm --dir /path exec tsx x.ts` does not match `pnpm exec *`. Calling the binary
by absolute path does not match either. A trailing star requires at least one
argument, so bare `git fetch` does not match `git fetch *` and stays sandboxed.
Rewrite your command in its canonical form before concluding anything.

**5d. Matching does not traverse scripts or loops.**

An entry for `ps *` releases `ps` typed directly, not a script that calls `ps`
internally: the line submitted to the matcher is `bash script.sh`. A diagnostic
script needs its own entry, on its own path, in both forms (with and without
` *`). Likewise, `for c in "top -l 1" "pgrep -x zsh"; do eval "$c"; done` stays
sandboxed even when both tools are excluded. Grouping probes to save time
produces false negatives.

**6. If the configuration changed after your session opened, restart unless you know the key reloads.**

Filesystem lists, `credentials.files`, `excludedCommands` and the network
allowlist were measured as applying to the next command without a restart.
Keep the restart as your default for any other key.

If all eleven checks pass and the blocker holds, move to the report template.

## Network: blocked host or nonexistent host

The domain allowlist filters even when strict mode is off. Measure with a host you
know is outside both your list and the product's built-in defaults.

In auto mode on v2.1.271 and later, a host the command did not declare is refused
and named in the command result; read the name before asking for anything. In
other modes, duration tells you which failure you hit: a refusal by the allowlist
hung for roughly 5 to 7 seconds on 2.1.220, while a hostname that does not resolve
failed in under 30 milliseconds, including when a wildcard in the list already
covered it. Verify the apex answers before asking for a domain to be added.

Raw TCP to an external host is a separate matter. Anything that ignores the proxy
variables has no path out: cloud Postgres, MySQL, Redis and plain SSH all fail,
and no domain entry can fix that. On macOS, git over SSH fails too, even with the
host allowed. The command has to be excluded, or run outside the sandbox.

## Report template

Fill this literally. Do not paraphrase the error: a reworded message cost a full
day of misdirected work on the project this skill came from.

```
Exact command typed: <literal copy-paste, every argument included>
Raw error received: <literal copy-paste, not summarized>
$TMPDIR at test time: <exact value, from a separate call>
Sandboxed: <yes if under the sandbox temp root, no otherwise>
Claude Code version: <claude --version>
Session opened before or after the last config change: <before / after / unknown>
Protocol steps already run: <1, 2, 3, 3b, 3c, 4, 5, 5b, 5c, 5d, 6, with each result>
Workarounds already tried: <list, or "none">
Real impact: <which task is blocked, since when>
```

## Escalation

Hand the filled template to whoever can edit the settings file. Do not edit it
yourself from Bash: writes to settings files are refused from a sandboxed
command. In auto mode, the classifier may also refuse an Edit to your own
settings as self-modification; prepare a candidate file elsewhere, show the diff,
and let the person apply it.

The keys worth knowing under `sandbox` are `excludedCommands`,
`credentials.files`, `credentials.envVars`, `filesystem.allowWrite`,
`filesystem.denyRead`, `network.allowedDomains` and `network.strictAllowlist`.
Two of them mislead.

`credentials.envVars` in `deny` mode unsets the variable before each sandboxed
command, but measure before trusting it. On 2.1.302, a denied variable present
only in Claude Code's launch environment was gone inside the sandbox, while two
denied variables exported by the user's shell profile were still set. The shell
the Bash tool starts is initialized from that profile; whether that re-exports
them is the likely mechanism, not a verified one. Check with a probe that prints
only `set` or `unset`, never the value.

`allowUnsandboxedCommands: false` does not neutralize `excludedCommands` from
your own settings. The first closes the per-invocation escape hatch, the second
excludes named commands. When the `false` comes from managed settings or
`--settings`, the sandbox becomes admin-required and a repository's
`excludedCommands` are ignored (v2.1.282 and later).

## Limits with no settings fix inside the sandbox

Verified. Do not reopen an investigation on these. Each one disappears when the
command runs outside the sandbox through a bare `excludedCommands` match, at the
cost of full access for that command.

| Limit | Finding | Known workaround |
|---|---|---|
| Setuid binaries | `ps`, `top`, `su`, `login` cannot exec sandboxed | exclude the bare command (`ps *`), or `lsof -nP -iTCP -sTCP:LISTEN` without touching the config |
| `AF_UNIX` sockets | `bind()` refused while sandboxed, local-binding settings cover TCP only | run the bare command under its exclusion, or bundle then run plain `node` |
| Direct DNS | cut for everyone, all HTTP goes through the local proxy | exclude the tool if it needs raw sockets |
| `.idea/` and `.vscode/` | writing a file inside is refused in the current project (protected paths) | exclude the install command, in both forms |

A setuid binary or a socket failure is therefore often a step 3 problem: the
command was excluded, but chained to something else.

On DNS, never propose adding a generic diagnostic tool such as `dig` to the
excluded list. It would return correct resolutions while the rest of the session
stays cut off, which manufactures exactly the kind of false diagnosis this skill
exists to prevent.

The `.idea` scoping matters more than it looks. The refusal applies to the
current project, so an audit run from a neighbouring repository will report that
nothing is blocked, and be wrong.

## See also

- [Native Sandboxing Guide](../../../guide/security/sandbox-native.md) - configuration keys and measured behavior
- [/sandbox-status](../sandbox-status/SKILL.md) - inspect the active configuration
- [Sandbox Config Example](../../config/sandbox-native.json) - production-ready settings
