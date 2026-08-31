# Proofpack verification log

## Scope

| Field | Record |
| --- | --- |
| Work item | [Incomplete release evidence can look ready](../ISSUE.md) |
| Date and owner | 2026-08-31, Codex implementation agent |
| In scope | CLI exit codes, required evidence checks, duplicate checks, hook fixtures, npm package manifest |
| Out of scope | Registry publication, container registry push, remote deployment |
| Runtime | Node.js v24.16.0 on local macOS host; Docker client 29.5.3 |
| Base commit | `e4833e5ee51c4a0539c1d55f2a6e22a5b02b929c` |
| Source fingerprint | [SOURCE-FINGERPRINT.txt](SOURCE-FINGERPRINT.txt), SHA-256 `17584d76f561a8f9153fc60c8e2340563de6a716e6fd57706dd1937cf3f3ece6` |
| Worktree state at verification | Review changes staged on `codex/learning-project`; no unstaged owned files; integration into `main` not performed or verified |

## Executable checks

| Check | Command | Exit status | Result |
| --- | --- | ---: | --- |
| Unit and integration tests | `npm test` | 0 | `PASS`, 11 of 11 tests |
| Hook fixtures | `npm run hook:fixtures` | 0 | `PASS`, 4 of 4 hook tests covering seven inputs |
| Ready candidate | `npm run verify` | 0 | `PASS`, `ready: true` and no problems |
| Package manifest | `npm run package:check` | 0 | `PASS`, five files, dry-run SHA-1 `488681faf85b86e9b4b8cfb51002ffb1c5d3b3e5` |
| Skill frontmatter | `ruby -ryaml` parse plus broad `Bash` grant assertion | 0 | `PASS` for YAML syntax and scoped Bash entries; `skills-ref` not run |
| Markdown links | `node --test test/documentation-links.test.mjs` | 0 | `PASS`, one of one test |
| Docker build | `docker build -t proofpack-learning:local .` | not run | `UNKNOWN`, Docker daemon access denied in this worktree environment |
| Container execution | `docker run --rm proofpack-learning:local` | not run | `UNKNOWN`, no verified image |

## Test-first record

The CLI acceptance test first failed because `src/cli.mjs` did not exist. The incomplete, malformed, duplicate, and invalid-version cases then failed against the initial ready-only implementation. The review cycles failed on `NOT RUN`, `no retained output`, `UNKNOWN`, `failed`, `not executed`, and `unverified` before the corresponding evidence sentinel checks existed. The hook tests first failed because the hook did not exist. The Docker push case and the empty-quote variants failed with an `allow` decision before their deny rules were added. The package negative test accepted invalid JavaScript before `node --check` joined the package gate.

## Final claim

Status: `PASS` for the local Node.js acceptance contract. Docker build and execution remain `UNKNOWN`.

The Node.js checks can prove only the listed local behavior on the recorded revision and runtime. Candidate evidence validation is a sentinel screen over an unstructured string; the proof log, not that field, carries command, exit-status, and checksum evidence. `package:check` validates JavaScript syntax and the npm manifest, but it does not execute the packed CLI. Docker behavior remains `UNKNOWN` until both Docker commands run successfully.
