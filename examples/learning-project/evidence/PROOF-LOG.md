# Proofpack verification log

## Scope

| Field | Record |
| --- | --- |
| Work item | [Incomplete release evidence can look ready](../ISSUE.md) |
| Date and owner | 2026-08-31, Codex implementation agent |
| In scope | CLI exit codes, required evidence checks, duplicate checks, hook fixtures, npm package manifest |
| Out of scope | Registry publication, container registry push, remote deployment |
| Runtime | Node.js v24.16.0 on local macOS host; Docker client 29.5.3 |
| Base commit | `95cc28591bcdaa75a5b254e81b08e8c413384651` |
| Source fingerprint | [SOURCE-FINGERPRINT.txt](SOURCE-FINGERPRINT.txt), SHA-256 `880ae07d00e1b8f3ef448f5104a2b6763116f69bfc38e1a04e6ade79397d6432` |
| Worktree state at verification | Review changes staged on `codex/learning-project`; no unstaged owned files; integration into `main` not performed or verified |

## Executable checks

| Check | Command | Exit status | Result |
| --- | --- | ---: | --- |
| Unit and integration tests | `npm test` | 0 | `PASS`, 10 of 10 tests |
| Hook fixtures | `npm run hook:fixtures` | 0 | `PASS`, 4 of 4 hook tests covering seven inputs |
| Ready candidate | `npm run verify` | 0 | `PASS`, `ready: true` and no problems |
| Package manifest | `npm run package:check` | 0 | `PASS`, five files, dry-run SHA-1 `738bf21297bf361c469490ec6535166fb2ff4500` |
| Skill frontmatter | `ruby -ryaml` parse plus broad `Bash` grant assertion | 0 | `PASS` for YAML syntax and scoped Bash entries; `skills-ref` not run |
| Markdown links | `node --test test/documentation-links.test.mjs` | 0 | `PASS`, one of one test |
| Docker build | `docker build -t proofpack-learning:local .` | not run | `UNKNOWN`, Docker daemon access denied in this worktree environment |
| Container execution | `docker run --rm proofpack-learning:local` | not run | `UNKNOWN`, no verified image |

## Test-first record

The CLI acceptance test first failed because `src/cli.mjs` did not exist. The incomplete, malformed, duplicate, and invalid-version cases then failed against the initial ready-only implementation. The review cycle also failed on `NOT RUN` and `no retained output` before the evidence sentinel check existed. The hook tests first failed because the hook did not exist. The Docker push case and the empty-quote variants failed with an `allow` decision before their deny rules were added. The package negative test accepted invalid JavaScript before `node --check` joined the package gate.

## Final claim

Status: `PASS` for the local Node.js acceptance contract. Docker build and execution remain `UNKNOWN`.

The Node.js checks can prove only the listed local behavior on the recorded revision and runtime. `package:check` validates JavaScript syntax and the npm manifest, but it does not execute the packed CLI. Docker behavior remains `UNKNOWN` until both Docker commands run successfully.
