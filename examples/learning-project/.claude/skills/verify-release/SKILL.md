---
name: verify-release
description: Use when checking whether a Proofpack release candidate has complete local evidence before packaging.
argument-hint: "[candidate JSON path]"
allowed-tools: Read Bash(npm test) Bash(node src/cli.mjs verify *) Bash(npm run package:check) Bash(git rev-parse HEAD) Bash(git status --short)
disable-model-invocation: true
---

# Verify a Proofpack release candidate

Use the supplied candidate path or default to `fixtures/release-ready.json`. Work from the Proofpack project root. The verification command consumes the skill argument directly:

```bash
node src/cli.mjs verify "${ARGUMENTS:-fixtures/release-ready.json}"
```

1. Read `ISSUE.md` and `CLAUDE.md`.
2. Run `npm test`.
3. Run the command above. Do not substitute an unreviewed shell expression for `$ARGUMENTS`.
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
