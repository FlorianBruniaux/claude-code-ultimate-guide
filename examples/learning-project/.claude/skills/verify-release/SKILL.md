---
name: verify-release
description: Use when checking whether a Proofpack release candidate has complete local evidence before packaging.
argument-hint: "[candidate JSON path]"
allowed-tools: Bash, Read
disable-model-invocation: true
---

# Verify a Proofpack release candidate

Use the supplied candidate path or default to `fixtures/release-ready.json`. Work from the Proofpack project root.

1. Read `ISSUE.md` and `CLAUDE.md`.
2. Run `npm test`.
3. Run `node src/cli.mjs verify <candidate-path>`.
4. Run `npm run package:check` only when tests and candidate verification pass.
5. Compare the observed commands, exit statuses, runtime version, and revision with `evidence/PROOF-LOG.md`.
6. Report `PASS`, `FAIL`, or `UNKNOWN`. Name any check that did not run.

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
