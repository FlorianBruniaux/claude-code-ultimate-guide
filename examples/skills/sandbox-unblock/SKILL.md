---
name: sandbox-unblock
description: >
  Diagnostic protocol to run before reporting a sandbox blocker or asking for a
  configuration change. Eight checks that eliminate false positives, then a
  report template the person holding the settings can act on. On one measured
  day, six of eight reported blockers turned out to be false, all from the same
  handful of method errors.
when_to_use: >
  Whenever a command fails with "operation not permitted", "EPERM", "permission
  denied", "listen EPERM", "ENOTFOUND", or an unexplained network timeout. Also
  on "I'm blocked by the sandbox", "the sandbox won't let me", "sandbox
  violation", when a command fails right after you read the sandbox description
  in the system prompt, when you hesitate to run git, gh, ssh, docker, pnpm,
  npm, yarn or tsx for fear of a refusal, and before writing any blocker report
  meant for another session.
allowed-tools: Read Grep Bash
effort: medium
---

# Unblock a session slowed by the sandbox

A blocker report is cheap to write and expensive to act on. This skill front-loads
the verification so the report that reaches a maintainer is worth their time.

The measurements quoted below come from a single macOS machine on Claude Code
2.1.220, July 2026. Treat the numbers as illustrative and the method as the point.

## Self-diagnosis, all eight checks, before you complain

Run these in order. Each step says what to run, what to read, and what the result
lets you conclude. Steps 5b and 5c pay for themselves fastest.

**1. Do not trust the sandbox description in your system prompt.**

It lists the `permissions.deny Read(...)` patterns under `read.denyOnly`, things
like `**/*.pem` or `**/.env*`. Those patterns govern the Read tool and nothing
else. A subprocess launched from Bash reads those files without obstacle. One
session concluded an entire Python pipeline was unrunnable on that basis; every
step of it worked when measured. Never infer a Bash restriction from that list.

**2. Confirm the command you are testing actually ran sandboxed.**

```bash
echo $TMPDIR
```

A path under the sandbox temp root means the measurement counts. The system
temp directory means the invocation escaped, and nothing that follows it proves
anything about sandboxed behavior.

**3. Put the `cd` and the command in the same call.**

The shell working directory resets between Bash calls. A `cd` in one call does
not survive into the next, so the command you meant to test in a project ran
somewhere else entirely. Two independent audits declared a package manager
broken this way; the binary was simply absent from the directory they landed in.

```bash
# wrong: two calls, the cd does not carry over
cd /path/to/project
pnpm exec prisma migrate status

# right: one call
cd /path/to/project && pnpm exec prisma migrate status
```

**4. Check the binary exists before blaming the sandbox.**

Wrappers that compress output often replace a clear message with a bare errno.
A missing binary and a security refusal then look identical on screen.

```bash
command -v <binary>
./node_modules/.bin/<binary> --version
```

Nothing returned means you have an installation problem, not a policy problem.

**5. Read the real exit code, not a pipe's.**

`cmd | head` returns the exit status of `head`, never of `cmd`. A refused read
earlier in the session also emits a warning on every later command, including
the ones that succeed, so read the last message rather than the first.

```bash
cmd > "$TMPDIR/out.log" 2>&1
echo "exit: $?"
cat "$TMPDIR/out.log"
```

**5b. Check whether a command rewriter sits between you and the matcher.**

This one explained most of the blockers on the day it was found. If a
`PreToolUse` hook rewrites Bash commands, for example a token-compression proxy
that turns `pnpm exec tsx x.ts` into `proxy pnpm exec tsx x.ts`, then an
`excludedCommands` entry written as `pnpm exec *` no longer matches anything.
Only the rewritten form matches.

The tell is an inconsistency: some excluded commands escape the sandbox and
others do not, with no obvious pattern. Look at whether the ones that work
happen to have a prefixed entry in the list.

Proof shape, three measurements. A throwaway entry for an otherwise-sandboxed
binary flips a Unix socket `bind()` from failure to success, which shows the
mechanism works at all. The same command under an unprefixed entry stays
sandboxed. Adding the prefixed form releases it immediately.

Any entry you request should be asked for in both forms, bare and prefixed.

**5c. An entry matches the command exactly as written.**

`git fetch origin` matches `git fetch *`. `git -C /path fetch origin` does not.
`pnpm --dir /path exec tsx x.ts` does not match `pnpm exec *`. A trailing star
requires at least one argument, so bare `git fetch` does not match `git fetch *`
either and stays sandboxed. Rewrite your command in its canonical form before
concluding anything.

**6. If the configuration changed after your session opened, restart first.**

The OS sandbox profile is compiled at session start. Exit and relaunch before
measuring anything on a session that predates a settings change.

Two keys were measured as hot-reloaded, `credentials.files` and
`excludedCommands`, along with the network allowlist. The rest were not tested
that way, so keep the restart as your default.

If all eight checks pass and the blocker holds, move to the report template.

## Network: blocked host or nonexistent host

The domain allowlist filters even when strict mode is off. Do not assume a
permissive default means no filtering; measure with a host you know is outside
both your list and the product's built-in defaults.

Duration tells you which failure you hit. A refusal by the allowlist hangs for
roughly 5 to 7 seconds. A hostname that does not resolve fails in under 30
milliseconds, including when a wildcard in the list already covers it. On one
run, two hosts named in a blocker report failed in about 25 ms while covered by
their wildcards: neither host existed. Verify the apex answers before asking for
a domain to be added.

Raw TCP to an external host is a separate matter. When the sandbox routes HTTP
through a local proxy and cuts direct DNS, anything that is not HTTP has no path
out. Cloud Postgres, MySQL, Redis and raw SSH all fail, and no domain entry can
fix that. The command has to be excluded, or run outside the sandbox.

## Report template

Fill this literally. Do not paraphrase the error: a reworded message cost a full
day of misdirected work on the chantier this skill came from.

```
Exact command typed: <literal copy-paste, every argument included>
Raw error received: <literal copy-paste, not summarized>
$TMPDIR at test time: <exact value>
Sandboxed: <yes if under the sandbox temp root, no otherwise>
Session opened before or after the last config change: <before / after / unknown>
Protocol steps already run: <1, 2, 3, 4, 5, 5b, 5c, 6, with each result>
Workarounds already tried: <list, or "none">
Real impact: <which task is blocked, since when>
```

## Escalation

Hand the filled template to whoever can edit the settings file. Do not edit it
yourself from Bash: writes to it are refused from a sandboxed command, and only
the Edit tool goes through.

The keys worth knowing under `sandbox` are `excludedCommands`,
`credentials.files`, `credentials.envVars`, `filesystem.allowWrite`,
`network.allowedDomains` and `network.strictAllowlist`. Two of them mislead.

`credentials.envVars` in `deny` mode does not remove the variable from Bash
subprocesses. A listed key stays readable in full. Only `credentials.files`
blocks a read, and only for absolute paths, never for a `**/` glob. Moving a
secret out of a denied file and into a denied environment variable therefore
weakens it.

`allowUnsandboxedCommands: false` does not neutralize `excludedCommands`. They
are independent: the first closes the per-invocation escape hatch, the second
excludes named commands regardless of the first.

## Limits with no fix

Verified. Do not reopen an investigation on these.

| Limit | Finding | Known workaround |
|---|---|---|
| Setuid binaries | `ps`, `top`, `su`, `login` cannot exec | `lsof -nP -iTCP -sTCP:LISTEN` |
| `AF_UNIX` sockets | `bind()` refused everywhere, local-binding settings cover TCP only | run the loader directly, or bundle then run plain `node` |
| Direct DNS | cut for everyone, all HTTP goes through the local proxy | exclude the tool if it needs raw sockets |
| `.idea/` and `.vscode/` | creating the directory works, writing a file inside is refused, in the current project only | exclude the install command, in both forms |

On DNS, never propose adding a generic diagnostic tool such as `dig` to the
excluded list. It would return correct resolutions while the rest of the session
stays cut off, which manufactures exactly the kind of false diagnosis this skill
exists to prevent.

The `.idea` scoping matters more than it looks. The refusal applies to the
current project, so an audit run from a neighbouring repository will report that
nothing is blocked, and be wrong.

## See Also

- [Native Sandboxing Guide](../../../guide/security/sandbox-native.md) - configuration keys and measured behavior
- [/sandbox-status](../sandbox-status/SKILL.md) - inspect the active configuration
- [Sandbox Config Example](../../config/sandbox-native.json) - production-ready settings
