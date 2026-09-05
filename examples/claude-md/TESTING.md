# Verification Proof Log

Copy this file into a work item before testing a change, an agent workflow, or a Best-of-N selection. Fill in fields with evidence. Use `UNKNOWN` when a check has not run, cannot run, or has incomplete coverage. Do not replace it with a passing conclusion.

Method reference: [Best-of-N: Generate, Select, and Verify](../../guide/workflows/best-of-n.md). For a reusable generation and selection procedure, see the [Best-of-N skill](../skills/best-of-n/SKILL.md).

## 1. Scope and acceptance contract

| Field | Record |
| --- | --- |
| Work item | `<issue, task, or request>` |
| Date and owner | `<ISO date, person or agent>` |
| Repository and revision | `<remote or path, commit SHA>` |
| In scope | `<behavior, files, and environments>` |
| Out of scope | `<explicit exclusions>` |
| Acceptance criteria | `<observable requirements>` |
| Mandatory failures | `<conditions that disqualify delivery>` |
| Authorization boundary | `<permissions, external actions, and approvals>` |

## 2. Environment and inputs

| Field | Record |
| --- | --- |
| OS and runtime | `<OS, language/runtime versions>` |
| Dependency or lockfile state | `<lockfile revision and install state>` |
| Configuration and secrets | `<redacted names only; never paste secrets>` |
| Data or fixture version | `<source, hash, retention boundary>` |
| Tool and model versions | `<tool, model, harness, and prompt version>` |
| Time and cost budget | `<limit and actual if available>` |

## 3. Candidate and selection record

Use this section only when more than one candidate was generated. Candidate identifiers should be opaque during scoring where practical. Add one table row for every generated candidate. Do not omit rejected candidates or candidates generated in a later batch.

| Field | Record |
| --- | --- |
| Frozen rubric version | `<path, hash, or dated identifier>` |
| Candidate count, batch schedule, and stop rule | `<N, every declared batch, and between-batch trigger>` |
| Isolation controls | `<separate prompts, worktrees, models, or fresh contexts>` |
| Known correlation | `<shared model, prompt, tools, state, or none known>` |
| Selected candidate | `<ID and artifact link>` |
| Tie-breaker or synthesis record | `<rule used, or new synthesized ID>` |

| Candidate | Mandatory criteria | Rubric score and evidence | Artifact link | Status |
| --- | --- | --- | --- | --- |
| `<generated candidate ID>` | `<pass/fail>` | `<score, criterion evidence>` | `<path, diff, or URL>` | `<selected/rejected>` |

## 4. Executable checks

Record every command actually run. A command not listed here was not verified by this log.

| Check | Command | Environment | Exit status | Result | Artifact link |
| --- | --- | --- | ---: | --- | --- |
| Unit tests | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Type or schema check | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Lint or static analysis | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<output path>` |
| Build or package | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail>` | `<artifact path/hash>` |
| Integration or end-to-end | `<exact command>` | `<environment ID>` | `<0/nonzero>` | `<pass/fail/UNKNOWN>` | `<output path>` |

## 5. Independent review

| Field | Record |
| --- | --- |
| Reviewer | `<person, agent, or service>` |
| Reviewer role | `<human, fresh-context agent, different model, deterministic system>` |
| Generation separation | `<what the reviewer did not receive>` |
| Shared context and incentives | `<model, repository, tools, prompt, or access overlap>` |
| Review scope | `<requirements and artifacts examined>` |
| Verdict and findings | `<accept/reject/needs changes; links>` |

## 6. Failures, unknowns, and final claim

| Category | Record |
| --- | --- |
| Failures observed | `<failed command, symptom, and disposition>` |
| Checks not run | `<reason and impact>` |
| Unknowns | `<uncovered behavior, environment, or external state>` |
| Artifact retention | `<paths, hashes, access boundary, and expiry if applicable>` |
| Final status | `PASS`, `FAIL`, or `UNKNOWN` |
| Claim justified by this log | `<bounded statement only>` |

`PASS` means the listed acceptance criteria passed in the listed environment. It does not prove behavior outside that scope. `FAIL` means a mandatory criterion or declared check failed. `UNKNOWN` means the available evidence cannot support the requested claim.
