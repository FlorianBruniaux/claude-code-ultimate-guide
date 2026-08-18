---
name: update-threat-db
description: Delegate threat-intelligence research and updates to AgentSec, then validate the guide and landing mirrors.
---

# Update Threat Intelligence Through AgentSec

AgentSec Triage owns the technical source of truth. This guide skill is a
delegator and does not carry a private copy of the threat database.

## Workflow

1. Locate the sibling `agentsec-triage` checkout or use `AGENTSEC_REPO`.
2. Read AgentSec's `AGENTS.md` and
   `.claude/commands/update-threat-db.md` completely.
3. Execute the source review, red-first tests, authoring changes, and builders
   inside an isolated AgentSec worktree.
4. Synchronize `exports/security-feed.v1.json` to the guide and landing only
   after AgentSec passes locally.
5. Run the guide and landing mirror checks, then report each repository's
   status separately.

Do not treat the guide's compatibility database as canonical. Do not publish,
tag, or push AgentSec while its license decision blocks public release.

The compatibility database still consumed by the guide commands is
`examples/commands/resources/threat-db.yaml`.
