# Delegate Threat Database Updates to AgentSec

AgentSec Triage is the canonical technical source for threat evidence, dated
fiches, detector inputs, and the public security feed. Do not research or edit
the guide database first.

## Locate AgentSec

Use `AGENTSEC_REPO` when it is already set. Otherwise look for the sibling
checkout `../agentsec-triage` from this repository root. Stop if neither path is
available or if it does not contain all of these files:

- `AGENTS.md`
- `.claude/commands/update-threat-db.md`
- `data/intelligence/sources.yaml`
- `data/intelligence/events.yaml`
- `data/threat-db.yaml`

Do not clone, pull, install, publish, or push without explicit authorization.

## Execute the canonical workflow

Read AgentSec's `AGENTS.md`, then execute its
`.claude/commands/update-threat-db.md` from the AgentSec repository. AgentSec
owns source review, uncertainty, detector coverage, regression tests, generated
artifacts, and the publication boundary.

After AgentSec passes locally, synchronize its generated feed into this guide
and the landing with `scripts/sync_security_feed.py --write`. Run the same
command with `--check`, then run:

```bash
python3 scripts/test-check-agentsec-security-feed.py
python3 scripts/check-agentsec-security-feed.py \
  --agentsec-feed "$AGENTSEC_REPO/exports/security-feed.v1.json"
```

The guide keeps `examples/commands/resources/threat-db.yaml` temporarily because
`/security-check` and `/security-audit` still consume it. It is a compatibility
consumer, not the place to start a new intelligence update.

## Guide follow-up

Only after the AgentSec record is reviewed:

- add reader-facing context to `guide/security/security-hardening.md` when the
  finding materially changes guidance;
- update the compatibility database without claiming detector coverage that
  AgentSec does not implement;
- update `CHANGELOG.md` under `[Unreleased]`;
- keep the AgentSec feed mirror byte-identical to its canonical artifact.

Report AgentSec, guide, and landing validation separately. State commit, push,
tag, and publication status explicitly.
