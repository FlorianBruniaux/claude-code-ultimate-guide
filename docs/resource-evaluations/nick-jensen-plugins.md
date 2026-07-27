# Resource Evaluation: Claude Code Plugins Developer Productivity

**URL**: https://www.nickjensen.co/posts/claude-code-plugins-developer-productivity
**Author**: Nick Jensen (Product Engineering)
**Date article**: © 2026 NickJensen.co (no explicit publication date)
**Evaluated**: 2026-01-24
**Evaluator**: Claude (via /eval-resource skill)

---

## Executive Summary

| Criterion | Value |
|-----------|-------|
| **Initial Score** | 3/5 |
| **Score after challenge** | 4/5 |
| **Score after Perplexity verification** | **2/5** (Marginal) |
| **Final Decision** | Do NOT integrate directly |
| **Reason** | Outdated stats, unverified claims, better primary sources exist |

---

## Content Summary

Article covering Claude Code plugins:
- Plugin architecture (`.claude-plugin/` structure with manifest.json)
- Marketplaces (cited `wshobson/agents` with stats)
- Workflow installation/management
- Concrete examples: /test-report, /deploy, /review
- Business use cases: team standards, onboarding acceleration

---

## Fact-Check Results

### Claims Verified Against Article Source

| Claim | In Article | Status |
|-------|-----------|--------|
| Nick Jensen, Product Engineering | ✅ | Verified |
| © 2026 | ✅ | Verified |
| wshobson/agents: 63 plugins, 85 agents, 47 skills | ✅ | **OUTDATED** |
| Onboarding 4-6w → 1-2w | ✅ | **UNVERIFIED externally** |
| 47 progressive disclosure skills | ✅ | Verified |
| 44 tools across 23 categories | ✅ | Verified |

### Perplexity Deep Verification

| Claim | Reality (Jan 2026) | Source |
|-------|-------------------|--------|
| wshobson/agents stats | **67 plugins, 99 agents, 107 skills** | GitHub README |
| Onboarding improvement | **Only appears in this article** - no independent citation | Multiple searches |
| Marketplace existence | ✅ Confirmed, actively maintained (Dec 2025 commits) | GitHub activity |

---

## Why Score Dropped from 4/5 to 2/5

1. **Stats are outdated**: 63/85/47 was an earlier version, now 67/99/107
2. **Onboarding claim is anecdotal**: "4-6 weeks → 1-2 weeks" appears nowhere else
3. **Better primary sources exist**:
   - Official Anthropic docs: code.claude.com/docs/en/plugins
   - wshobson/agents README (current stats)
   - claude-plugins.dev registry (11,989 plugins, 63,065 skills)
   - Firecrawl analysis with actual install counts

---

## Primary Sources Discovered (Better Alternatives)

| Source | Value | URL |
|--------|-------|-----|
| **Anthropic Official Docs** | Authoritative plugin structure, manifest schema | code.claude.com/docs/en/plugins |
| **wshobson/agents** | 67 plugins, 99 agents, 107 skills (current as of 2026-01-24), 38,296 GitHub stars as of 2026-07-28 | github.com/wshobson/agents |
| **claude-plugins.dev** | 11,989 plugins, 63,065 skills indexed | claude-plugins.dev |
| **claudemarketplaces.com** | Auto-scans GitHub for marketplaces | claudemarketplaces.com |
| **Firecrawl analysis** | Actual install counts (Context7: 72k, Ralph: 57k) | firecrawl.dev/blog/best-claude-code-plugins |
| **awesome-claude-code** | 20k+ stars, curated list | github.com/hesreallyhim/awesome-claude-code |

---

## Integration Actions Taken

Instead of integrating Nick Jensen's article, we integrated **primary sources**:

### 1. Fixed Section 8.5 "Creating Custom Plugins" (guide/ultimate-guide.md)

**Before** (incorrect):
```
my-plugin/
├── plugin.json           # Plugin manifest
```

**After** (correct per Anthropic docs):
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (ONLY file in this dir)
├── agents/
├── skills/
├── commands/
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
└── README.md
```

### 2. Added "Community Marketplaces" subsection (~line 7245)

- wshobson/agents (67 plugins, 99 agents, 107 skills)
- claude-plugins.dev (11,989 plugins, 63,065 skills)
- claudemarketplaces.com
- Popular plugins with install counts
- Links to awesome-claude-code

### 3. Updated reference.yaml

- Added official Anthropic doc links
- Added community marketplace resources
- Added popular plugins with install counts
- Added awesome list reference

---

## Lessons Learned

1. **Always verify stats against primary sources** - blog posts often cite outdated data
2. **Productivity claims need external validation** - anecdotal improvements are not generalizable
3. **Perplexity research revealed better sources** - registry data > blog commentary
4. **Official docs should be checked first** - Anthropic has comprehensive plugin documentation

---

## Related Evaluations

- [se-cove-plugin.md](./se-cove-plugin.md) - First plugin example integrated

---

## Metadata

```yaml
evaluated_by: Claude (Opus 4.5)
skill_used: /eval-resource
time_spent: ~30 minutes
perplexity_used: Yes (user-provided research)
changes_made:
  - guide/ultimate-guide.md (Section 8.5)
  - machine-readable/reference.yaml
integration_decision: Rejected article, integrated primary sources instead
```