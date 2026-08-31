# Issue: incomplete release evidence can look ready

## Bounded problem

The release command must not accept a candidate when a required check failed, is missing, has no evidence, or appears twice. Invalid JSON must remain distinguishable from a valid candidate that is not ready.

This reference solution resolves the issue. A learner can use the acceptance contract below to reproduce the work with a fresh branch and a test-first change.

## Acceptance contract

- A candidate with passing `tests`, `security`, and `package` checks exits `0` and reports `ready: true`.
- A valid but incomplete candidate exits `1`, reports `ready: false`, and lists every observed problem.
- Malformed JSON exits `2` and writes the parse error to standard error.
- Duplicate check names fail even if one duplicate contains passing evidence.
- The case-insensitive markers `UNKNOWN`, `failed`, `not executed`, `unverified`, `NOT RUN`, and `no retained output` fail because they do not identify a retained result.
- The tests run through `node:test` without third-party packages or network access.

## Exclusions

The CLI does not authenticate to a registry, execute evidence strings, publish packages, build containers, or prove that an external deployment succeeded. Those actions remain outside this issue.

## Proof locations

- Behavior: [test/cli.test.mjs](test/cli.test.mjs)
- Hook boundary: [test/release-guard.test.mjs](test/release-guard.test.mjs)
- Final record: [evidence/PROOF-LOG.md](evidence/PROOF-LOG.md)
