---
name: ai-assisted-contribution
description: "Record reproduction, verification evidence, author explanation and maintainer follow-up"
complexity: beginner
time: varies
domain: general
status: experimental
keywords: [open-source, contribution, review, evidence]
---

# AI-assisted contribution packet

Copy the fields that the receiving project needs into its own issue or PR template. This packet supplements project policy; it does not override it or certify the patch.

## Need and scope

- Project contribution and AI-assistance policy checked:
- Existing issue or agreed feature proposal:
- Affected version and environment:
- Expected behavior and its source:
- Observed behavior and minimal reproduction:
- Changed files and reason each is needed:
- Deliberately excluded work:

## Evidence

| Check | Revision | Exact command or inspection | Observed result | Limit |
|---|---|---|---|---|
| Reproduction before fix | | | | |
| Regression check after fix | | | | |
| Relevant existing checks | | | | |

Record “not run” and the reason for any missing check. Distinguish expected test failure, unexpected failure, environment failure, and success. Documentation-only changes can use source comparison and link checks instead of artificial tests.

## Author explanation

- Root cause:
- Why this change addresses it:
- Nearby behavior that could regress:
- What I checked myself:
- What remains uncertain:
- Assistance disclosure, if required by project policy:

## Submission and follow-up

- Maintainer feedback I still need before implementation or submission:
- Person responsible for answering review and revising the patch:
- Evidence invalidated by the latest revision:
- Ready for review, or missing evidence:

Do not include credentials, private source, personal data or unrelated agent logs. Route security findings through the project's security policy.
