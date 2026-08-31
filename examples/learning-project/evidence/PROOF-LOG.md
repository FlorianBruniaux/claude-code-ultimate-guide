# Proofpack verification log

## Scope

| Field | Record |
| --- | --- |
| Work item | [Incomplete release evidence can look ready](../ISSUE.md) |
| Date and owner | 2026-08-31, Codex implementation agent |
| In scope | CLI exit codes, required evidence checks, duplicate checks, hook fixtures, npm package manifest |
| Out of scope | Registry publication, container registry push, remote deployment |
| Runtime | Node.js v24.16.0 on local macOS host; Docker client 29.5.3 |

## Executable checks

| Check | Command | Exit status | Result |
| --- | --- | ---: | --- |
| Unit and integration tests | `npm test` | 0 | `PASS`, 10 of 10 tests |
| Ready candidate | `npm run verify` | 0 | `PASS`, `ready: true` and no problems |
| Package manifest | `npm run package:check` | 0 | `PASS`, five files, dry-run SHA-1 `1dc9a98ee8a708f8dcd96872e1f5ccb4a0981abd` |
| Markdown links | `node --test test/documentation-links.test.mjs` | 0 | `PASS`, one of one test |
| Docker build | `docker build -t proofpack-learning:local .` | not run | `UNKNOWN`, Docker daemon access denied in this worktree environment |
| Container execution | `docker run --rm proofpack-learning:local` | not run | `UNKNOWN`, no verified image |

## Test-first record

The CLI acceptance test first failed because `src/cli.mjs` did not exist. The incomplete, malformed, duplicate, and invalid-version cases then failed against the initial ready-only implementation. The hook tests first failed because the hook did not exist. The Docker push case failed with an `allow` decision before its deny rule was added.

## Final claim

Status: `PASS` for the local Node.js acceptance contract. Docker build and execution remain `UNKNOWN`.

The Node.js checks can prove only the listed local behavior on the recorded revision and runtime. Docker behavior remains `UNKNOWN` until both Docker commands run successfully.
