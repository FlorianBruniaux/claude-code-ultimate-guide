# Proofpack: one project for the seven-module learning path

Proofpack is a dependency-free Node.js CLI that decides whether a release candidate has enough evidence to ship. Its final state is a reference solution. A learner can rebuild the same result across modules 01 to 07 without switching projects or inventing a new exercise each time.

The bounded work item is recorded in [ISSUE.md](ISSUE.md). The CLI accepts a JSON candidate, checks the required `tests`, `security`, and `package` evidence, prints a machine-readable report, and returns a distinct exit code for incomplete evidence or invalid input.

## Run it without installing packages

Node.js 20 or later is the only test dependency.

```bash
node --version
npm test
npm run verify
```

`npm run verify` should exit `0`. Compare it with the intentional failure fixture:

```bash
npm run verify:incomplete
```

That command should exit `1` and name the failed and missing checks. Invalid JSON exits `2`.

## Carry the project through modules 01 to 07

| Stage | Guide module | Work in this project | Evidence to retain |
| --- | --- | --- | --- |
| 01 | [Installation and setup](../../guide/learning-path/01-installation.md) | Confirm Node.js, inspect the repository, and run the ready fixture. | Runtime version and the `npm run verify` exit status. |
| 02 | [Core loop](../../guide/learning-path/02-core-loop.md) | Read [ISSUE.md](ISSUE.md), reproduce the incomplete case, write a failing test, then change the validator. | The red failure, green test run, and reviewed diff. |
| 03 | [Memory and config](../../guide/learning-path/03-memory.md) | Read [CLAUDE.md](CLAUDE.md) and ask Claude Code to explain which rules constrain a change. | The rule cited before editing and the command selected for verification. |
| 04 | [Agents and specialization](../../guide/learning-path/04-agents.md) | Use the read-only [evidence reviewer](.claude/agents/evidence-reviewer.md) after the implementation is green. | Findings tied to a file, check, or missing artifact. |
| 05 | [Skills and automation](../../guide/learning-path/05-skills.md) | Run the focused [verify-release skill](.claude/skills/verify-release/SKILL.md). | Its bounded `PASS`, `FAIL`, or `UNKNOWN` record. |
| 06 | [Hooks and events](../../guide/learning-path/06-hooks.md) | Inspect the [PreToolUse hook](.claude/hooks/release-guard.mjs), its [configuration](.claude/settings.json), and the pass, fail, obfuscation, and malformed fixtures. | `npm run hook:fixtures` with four tests covering seven inputs. |
| 07 | [Advanced patterns](../../guide/learning-path/07-advanced.md) | Compare candidates only when the decision warrants [Best-of-N](../../guide/workflows/best-of-n.md), complete the [proof log](evidence/PROOF-LOG.md), check the npm package, then review the [Dockerfile](Dockerfile). | Test output, package manifest, selected-candidate record if used, and remaining runtime unknowns. |

The executable [learning-path skill](../skills/learning-path/README.md) can record module completion and scheduled reviews. Use its state file for learning progress. Keep product evidence in this project's proof log so a course-completion note cannot substitute for a test result.

## Evidence contract

The validator requires one unique check for each of these names:

- `tests`
- `security`
- `package`

Every check needs `status: "pass"` and a retained-result description. Empty evidence and the case-insensitive markers `UNKNOWN`, `failed`, `not executed`, `unverified`, `NOT RUN`, and `no retained output` all fail. This is a conservative string screen, so text such as `0 failed` also fails. The candidate schema does not parse a command, exit status, or checksum from this string. Put those structured facts in [evidence/PROOF-LOG.md](evidence/PROOF-LOG.md). The version must use `MAJOR.MINOR.PATCH`. A duplicate name is a failure because later evidence must not shadow an earlier result.

[fixtures/release-ready.json](fixtures/release-ready.json) demonstrates the accepted schema. [fixtures/release-incomplete.json](fixtures/release-incomplete.json) demonstrates a failed security check and missing package evidence. The CLI does not contact a registry, execute the evidence strings, or infer that a cited command really ran.

## Verification and packaging

Run the complete local gate before claiming the reference solution passes:

```bash
npm test
npm run verify
npm run package:check
```

The package gate checks both JavaScript files with `node --check`, then builds an npm manifest without downloading dependencies or publishing an artifact. The named [package-check test](test/package-check.test.mjs) injects invalid JavaScript into a temporary copy and requires a nonzero exit. This proves the syntax boundary, not execution of the packed CLI. The [Dockerfile](Dockerfile) supplies an additional deployable form. Building it may require the `node:22-alpine` base image from a registry, so a passing Node.js test run does not prove the image builds or runs on another host.

The repository's [TESTING.md proof-log template](../claude-md/TESTING.md) explains the full evidence format. This example keeps a filled, project-specific [proof log](evidence/PROOF-LOG.md). For higher-cost choices, follow the [Best-of-N workflow](../../guide/workflows/best-of-n.md) and preserve rejected candidates as well as the selected one.

## Safety boundary

The release guard blocks direct, flag-bearing, and empty-quote-obfuscated `npm publish` and `docker push` tool calls. It also denies any command where `npm` appears with `publish`, or `docker` appears with `push`, even when the words are only printed or discussed. Those conservative false positives are intentional. The hook does not catch aliases, encoded commands, variable expansion, other registry clients, or shell constructions that split words with non-empty quoted text. It never auto-unblocks after a passing check. Treat it as a teaching control, not a shell parser or a general command firewall. Apply the repository's [security hardening guidance](../../guide/security/security-hardening.md) before adapting hooks to production.

Publishing also needs a channel owner, destination credentials, and an explicit decision. The [guide distribution workflow](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/workflows/guide-distribution.md) separates those external actions from local packaging checks. That page is supplied by the parent integration on `main`; this isolated branch keeps an external repository link until both commits are combined.

## Project map

```text
examples/learning-project/
├── .claude/
│   ├── agents/evidence-reviewer.md
│   ├── hooks/release-guard.mjs
│   ├── hooks/fixtures/
│   ├── settings.json
│   └── skills/verify-release/SKILL.md
├── evidence/PROOF-LOG.md
├── fixtures/
├── src/
├── test/
├── CLAUDE.md
├── Dockerfile
├── ISSUE.md
└── package.json
```
