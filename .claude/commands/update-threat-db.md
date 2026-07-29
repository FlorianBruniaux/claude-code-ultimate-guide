# Update Threat Database

Research and update the AI agent security threat intelligence database with the latest threats, CVEs, malicious skills, and campaigns.

**Time**: 3-8 minutes | **Scope**: `examples/commands/resources/threat-db.yaml`

> Requires Perplexity MCP (or manual web search). Run monthly or after major security advisories.

## Instructions

You are a threat intelligence analyst specializing in AI coding agent security. Research the latest threats and update the threat database.

---

### Phase 1: Current State Assessment

Read the current threat database:

```
Read examples/commands/resources/threat-db.yaml
```

Note:
- Current `version` and `updated` date
- Number of malicious authors, skills, CVEs, campaigns
- Most recent entries to avoid duplicates

---

### Phase 2: Research New Threats

Run **4 targeted Perplexity searches** (parallel when possible):

**Search 1: New malicious skills & campaigns**
```
Query: "malicious AI agent skills ClawHub OpenClaw skills.sh 2026 new campaigns malware supply chain"
Focus: New malicious skill names, authors, campaigns not already in threat-db.yaml
```

**Search 2: New MCP server CVEs**
```
Query: "MCP server CVE vulnerability 2025 2026 model context protocol security advisory"
Focus: New CVEs for MCP servers, SDK vulnerabilities, transport-level flaws
```

**Search 3: New attack techniques**
```
Query: "AI coding agent attack prompt injection Claude Code Cursor supply chain security research 2026"
Focus: New attack vectors, techniques, research papers
```

**Search 4: New defensive tools & blocklists**
```
Query: "MCP security scanner tool mcp-scan alternative AI agent skills security scanning 2026"
Focus: New scanning tools, blocklists, defensive frameworks
```

If Perplexity MCP is unavailable, use WebSearch for each query.

---

### Phase 3: Analyze & Deduplicate

For each finding from Phase 2:

1. **Check if already in threat-db.yaml** — skip duplicates
2. **Verify source credibility** — prefer: CVE databases, security vendor blogs, peer-reviewed research
3. **Categorize** — which section does it belong to?
   - `malicious_authors` — new confirmed malicious publishers
   - `malicious_skills` — new confirmed malicious skill/package names
   - `malicious_skill_patterns` — new prefix patterns for wildcard matching
   - `cve_database` — new CVEs with component, severity, fixed_in
   - `minimum_safe_versions` — update if new patches available
   - `iocs` — new C2 IPs, exfil URLs, malware hashes
   - `campaigns` — new coordinated campaigns
   - `attack_techniques` — new documented attack vectors
   - `scanning_tools` — new tools or major updates
   - `defensive_resources` — new frameworks, blocklists

4. **Assess risk level**:
   - `critical` — confirmed malicious, active exploitation
   - `high` — confirmed vulnerable, exploit available
   - `medium` — theoretical risk, no known exploitation
   - `low` — informational

---

### Phase 4: Update threat-db.yaml

Apply changes following these rules:

1. **Bump version** — increment minor (e.g. 2.0.0 → 2.1.0) for new entries, major for schema changes
2. **Update `updated` date** — set to today
3. **Add new sources** — add any new research sources to the `sources` list
4. **Maintain YAML validity** — use single quotes for patterns containing backslashes
5. **Preserve existing entries** — never remove entries unless confirmed false positive
6. **Follow existing format** — match the structure of existing entries exactly

**Important**: After editing, validate YAML:
```bash
python3 -c "import yaml; yaml.safe_load(open('examples/commands/resources/threat-db.yaml')); print('YAML valid')"
```

---

### Phase 5: Update Dependent Files (if needed)

Check if new CVEs should also be added to the security hardening guide:

```bash
# Count current CVEs in threat-db vs security-hardening
grep -c "id:" examples/commands/resources/threat-db.yaml
grep -c "CVE-" guide/security-hardening.md
```

If major new CVEs found (severity critical/high):
- Consider adding to `guide/security-hardening.md` CVE table
- Update `minimum_safe_versions` if new patches released

---

### Phase 6: Summary Report

## Output Format

```
## Threat Database Update Report

**Date**: [timestamp]
**Previous version**: [old version]
**New version**: [new version]

### Changes Summary

| Category | Added | Updated | Total |
|----------|-------|---------|-------|
| Malicious authors | +X | ~X | XX |
| Malicious skills | +X | ~X | XX |
| CVEs | +X | ~X | XX |
| Campaigns | +X | ~X | XX |
| IOCs | +X | ~X | XX |
| Attack techniques | +X | ~X | XX |
| Scanning tools | +X | ~X | XX |

### New Entries

[List each new entry with source and risk level]

### Notable Findings

[Highlight anything particularly important or urgent]

### No Changes Needed

[If nothing new found, explain what was searched and confirmed up-to-date]

### Next Steps

- [ ] Run `/security-check` to test against updated database
- [ ] Update `guide/security-hardening.md` if new critical CVEs
- [ ] Commit: `docs(security): update threat-db vX.Y.Z — [summary]`
```

$ARGUMENTS
