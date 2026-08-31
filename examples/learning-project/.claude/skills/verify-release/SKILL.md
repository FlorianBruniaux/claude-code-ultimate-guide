---
name: verify-release
description: Use when checking whether a Proofpack release candidate has complete local evidence before packaging.
argument-hint: "[candidate JSON path]"
allowed-tools: Read Bash(npm test) Bash(node src/cli.mjs verify *) Bash(npm run package:check) Bash(git rev-parse HEAD) Bash(git status --short)
disable-model-invocation: true
---

# Verify a Proofpack release candidate

Work from the Proofpack project root. Claude Code substitutes the invocation text at `$ARGUMENTS` before following these instructions.

- If `$ARGUMENTS` is empty, set the candidate path to `fixtures/release-ready.json`.
- Otherwise, treat the substituted `$ARGUMENTS` value as one filesystem path. Do not evaluate it as a shell expression.
- Run `node src/cli.mjs verify "<resolved-candidate-path>"` with that literal path as one quoted argument.

1. Read `ISSUE.md` and `CLAUDE.md`.
2. Run `npm test`.
3. Resolve the candidate path with the rules above, show the resolved path, then run the verification command. Ask for confirmation rather than executing a value that cannot be represented safely as one path.
4. Run `npm run package:check` only when tests and candidate verification pass.
5. Run `git rev-parse HEAD` and `git status --short`. Compare that source state, the observed commands, exit statuses, and runtime version with `evidence/PROOF-LOG.md`.
6. Report `PASS`, `FAIL`, or `UNKNOWN`. Name any check that did not run or any worktree change not covered by the recorded fingerprint.

Do not run `npm publish`, `docker push`, or change the proof log. Package inspection is local. Publication requires a separate user decision and destination credentials.

Return this record:

```text
RELEASE VERIFICATION
Candidate: <path>
Revision: <commit or UNKNOWN>
Tests: PASS | FAIL | UNKNOWN
Candidate contract: PASS | FAIL | UNKNOWN
Package dry run: PASS | FAIL | UNKNOWN
Evidence log match: PASS | FAIL | UNKNOWN
Final status: PASS | FAIL | UNKNOWN
Limits: <unverified runtime or external behavior>
```
