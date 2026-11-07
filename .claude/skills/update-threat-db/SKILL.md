---
name: update-threat-db
description: Update the guide's threat intelligence through AgentSec Triage, research new coding-agent and MCP security advisories or researcher IOC lists (malicious repositories, hashes, campaign gists), and synchronize the security feed. Use for threat database refreshes or mise a jour de la base de menaces, not repository security scans or Claude Code release tracking.
---

# Update threat intelligence through AgentSec

Scope: this guide repository and its AgentSec and landing consumers. This skill
does not change global agent configuration. Its canonical source is
`.claude/skills/update-threat-db/`; regenerate the Codex projection with
`python3 scripts/sync-threat-skill.py --write` from the guide root.

## Resolve the workflow

Read `.claude/commands/update-threat-db.md` from the guide root in full. It owns
the delegation contract and consumer checks. Resolve `AGENTSEC_REPO` if set,
otherwise the sibling `../agentsec-triage`. Verify the required files before
continuing. Do not silently substitute the guide's compatibility database.

Read the resolved AgentSec `AGENTS.md` and
`.claude/commands/update-threat-db.md` in full, then execute that workflow.
Preserve unrelated edits in all checkouts. Use the latest recorded update date
through today's date as the research window.

## Evidence and changes

Review primary sources before accepting new records. Keep the evidence sources,
dated events, exact detector inputs and public feed as separate artifacts. Record
affected ranges, fixed versions and uncertainty only when the source supports
them. Deduplicate CVE/GHSA aliases. Keep corrections as dated events.

Add the required regression test before each accepted data change. Distinguish
`detected`, `partial`, `not_detected` and `not_applicable`; a documented CVE does
not prove executable detection. Do not run malicious samples.

## Researcher IOC dumps and repository lures

A campaign report often arrives as a social post plus a CSV or gist of
indicators. Treat the post as context and the indicator file as the evidence
to review row by row.

- Fetch the file through an API or raw URL into a fresh scratch directory. Never
  clone, open or unpack a listed repository or archive.
- Keep each row's own confidence. A hash confirmed on a sandbox run and a C2
  address the author marks campaign-level are different claims.
- Keep repository URLs defanged. Record live or removed status with the date of
  the author's check, and the committed archive path when one is given.
- Judge detector coverage on where the payload lives. A clean `SKILL.md` or
  settings file proves nothing when the README links an archive committed to the
  repository, or when the archive sits under `.claude/`, `.codex/` or a similar
  agent directory.
- Before accepting a "new" campaign, search AgentSec for its family, loader and
  malware names. A slice reported today can belong to a campaign disclosed months
  earlier: backfill that lineage as dated events instead of starting a new one.

Credit the researcher in the guide prose with a public link to the post or the
indicator file.

## Completion checks

1. Pass the AgentSec validation gates and regenerate artifacts twice without drift.
2. Synchronize the approved public feed into the guide and landing; verify byte
   equality and run each consumer's integration checks.
3. Refresh the guide's compatibility database and reader guidance only after the
   canonical records pass. Update each affected repository's changelog.
4. Run `python3 scripts/sync-threat-skill.py --check` after editing this skill or
   its routing scenarios. Validate both host routes with the installed router.
5. Report the research window, accepted and deferred records, detector limits,
   file changes, validation results and synchronization state.

Commit, push, tagging and publication are separate states. Follow AgentSec's
authorization and data-license boundaries; a local update does not authorize a
public release. State any unfinished gate explicitly.
