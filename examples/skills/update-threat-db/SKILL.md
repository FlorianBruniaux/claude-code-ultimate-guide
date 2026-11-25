---
name: update-threat-db
description: "Refresh the guide's threat intelligence by delegating research and updates to AgentSec Triage, then validate the guide and landing mirrors. Use when asked to update the threat database, pull new coding-agent or MCP security advisories, or sync the security feed. Not for scanning a repository (use security-check or security-audit) or tracking Claude Code releases."
effort: high
disable-model-invocation: true
---

# Update threat intelligence through AgentSec

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
5. Follow the guide's `.claude/commands/update-threat-db.md` for compatibility
   database updates and the landing's searchable catalogue sync/check command.
   A current feed badge does not prove the catalogue contains the new records.
6. Run the guide and landing mirror checks, then report each repository's
   status separately.

Do not treat the guide's compatibility database as canonical. Do not publish,
tag, or push AgentSec while its license decision blocks public release.

The compatibility database still consumed by the guide commands is
`examples/commands/resources/threat-db.yaml`.
