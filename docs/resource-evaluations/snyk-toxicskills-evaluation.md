# Resource Evaluation: Snyk ToxicSkills — Malicious AI Agent Skills Audit

| Field | Value |
|-------|-------|
| **Resource** | [Snyk ToxicSkills Blog](https://snyk.io/fr/blog/toxicskills-malicious-ai-agent-skills-clawhub/) |
| **Type** | Security research + open-source tool |
| **Published** | 2026-02-05 |
| **Relayed by** | Victor Langlois (LinkedIn) |
| **Score** | **4/5** (High Value) |
| **Action** | Integrated — enriched security-hardening.md (CVE, stats, new section §1.5) |

---

## Summary

Snyk scanned **3,984 AI agent skills** across ClawHub and skills.sh marketplaces, finding:

1. **36.82%** (1,467 skills) contain security flaws
2. **534 skills** flagged critical (malware, prompt injection, exposed secrets)
3. **76 malicious payloads** identified (credential theft, backdoors, data exfiltration — 8 still active on ClawHub at publication)
4. **10.9%** of ClawHub skills contain hardcoded secrets
5. **2.9%** fetch and execute remote content dynamically
6. **mcp-scan**: open-source tool achieving 90-100% recall on confirmed malicious skills, 0% false positives on top-100 legitimate skills

## Gap Analysis

| Topic | Before (guide) | After |
|-------|----------------|-------|
| Supply chain stats | 8-14% (SafeDep) | 36.82% (Snyk, 3,984 skills corpus) |
| Audit tools | skills-ref validate | + mcp-scan (Snyk) |
| Attack categories | Generic (injection, exfil, privesc) | 8 detailed policies (hardcoded secrets, remote prompt exec, malicious downloads) |
| .claude/ attack vector | 1-line mention (line 199) | Full section §1.5 with checklist |
| Malicious hooks/commands | Not covered | Documented with audit checklist |
| Recent CVEs | 5 CVEs (2025) | + CVE-2026-24052, CVE-2025-66032 |

## Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| 3,984 skills scanned | Yes | Snyk blog |
| 36.82% with flaws (1,467/3,984) | Yes | Snyk blog |
| 534 critical | Yes | Snyk blog (13.4% of total) |
| 76 malicious payloads | Yes | Snyk blog (8 still active on ClawHub) |
| mcp-scan 90-100% recall | Yes | Snyk blog (0% FP on top-100 legit) |
| "91% combine injection + code" | Not verified | LinkedIn post stat, not in Snyk blog. Excluded from integration. |
| CVE-2026-24052 (SSRF Claude Code) | Yes | SentinelOne vulnerability database |
| CVE-2025-66032 (8 bypasses) | Yes | Flatt Security research |

## Score Justification

**4/5 (High Value)** — not 5/5 because:

- The guide already covers ~70% of the scope (security-hardening.md §1.1-1.4)
- This is an enrichment (updated stats, new tool, new section), not a gap-from-scratch
- Snyk stats are more recent and larger corpus than existing SafeDep data
- mcp-scan fills a concrete tooling gap
- The .claude/ attack surface section addresses a real blind spot

## Integration Plan

1. **§1.1 CVE Summary**: +2 CVEs (CVE-2026-24052, CVE-2025-66032)
2. **§1.2 Supply Chain**: Replace SafeDep stats with Snyk (larger corpus), add mcp-scan
3. **MCP Safe List**: Add mcp-scan entry
4. **New §1.5**: Malicious Extensions (.claude/ Attack Surface) with audit checklist
5. **reference.yaml**: Add entries for new sections

## References

- **Snyk ToxicSkills**: [snyk.io/blog/toxicskills](https://snyk.io/fr/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- **mcp-scan**: [github.com/snyk/mcp-scan](https://github.com/snyk/mcp-scan)
- **CVE-2026-24052**: [SentinelOne](https://sentinelone.com/vulnerability-database/)
- **CVE-2025-66032**: [Flatt Security](https://flatt.tech/research/posts/)
- **SafeDep (previous source)**: [safedep.io/agent-skills-threat-model](https://safedep.io/agent-skills-threat-model)
