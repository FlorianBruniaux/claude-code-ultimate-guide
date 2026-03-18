# Resource Evaluation: claude-migrate-session Skill

**Author**: Jim Weller (inspired by Alexis Laporte)
**Type**: Community Skill
**Date Evaluated**: 2026-02-09
**Evaluator**: Claude Code Ultimate Guide Team
**Score**: 3/5 (Pertinent - Complément utile)

---

## Executive Summary

A bash skill that automates cross-folder session migration for Claude Code. Addresses a real gap (GitHub issue #1516) but has zero community adoption. Manual filesystem operations are safer and recommended over this automation tool.

---

## Source Information

| Field | Value |
|-------|-------|
| **LinkedIn Post** | https://www.linkedin.com/posts/jwweller_claude-code-skill-that-clones-a-claude-session-activity-7426010179659309056-ZaUH |
| **GitHub Repository** | https://github.com/jimweller/dotfiles/tree/main/dotfiles/claude-code/skills/claude-migrate-session |
| **Publication Date** | February 2026 |
| **Last Updated** | February 2026 |
| **License** | Not specified (personal dotfiles) |
| **Stars/Forks** | 0/0 (as of 2026-02-09) |
| **Issues/PRs** | 0/0 |

---

## What It Does

**Problem solved**: Native `--resume` command is limited to the current working directory. When you move a project or want to fork a session to a new folder, the session becomes inaccessible.

**Solution provided**:
1. **Global search**: Finds sessions across all projects with keyword filtering
2. **Interactive selection**: Filters results, excludes current directory sessions
3. **Automated migration**: Copies `.jsonl` + subagents directory, generates new UUID
4. **Resume command**: Provides `claude --resume <new-id>` for immediate use

**Technical implementation**:
- Uses ripgrep for performance
- Filtering support (`cleanupPeriodDays: 90` for large histories)
- Bash scripts: `search.sh` + `migrate.sh`
- Command syntax: `/claude-migrate-session <source> <target>`

---

## Evaluation Criteria

### 1. Accuracy (4/5)

**Strengths**:
- ✅ Correctly identifies the architectural limitation (CWD-scoped sessions)
- ✅ Preserves full context (`.jsonl` + subagents)
- ✅ Generates independent copies (new UUID)

**Weaknesses**:
- ⚠️ No explicit handling of hardcoded paths in session context
- ⚠️ No validation of MCP server compatibility
- ⚠️ No warning about secrets in `.jsonl` files

### 2. Relevance (3/5)

**Confirmed gap**: GitHub issue #1516 documents community requests for cross-folder resume.

**But**:
- Niche use case (estimated 1-5% of users)
- Alternative manual approach is trivial (`mv ~/.claude/projects/...`)
- Zero adoption (0 stars/forks) suggests limited real-world demand

### 3. Completeness (2/5)

**Missing critical elements**:
- ❌ No error handling examples
- ❌ No edge case documentation (secrets, paths, MCP mismatches)
- ❌ No testing strategy or test results
- ❌ No security considerations
- ❌ No rollback mechanism

### 4. Quality (3/5)

**Code quality**: Clean bash implementation, uses standard tools (ripgrep).

**Documentation quality**:
- ✅ Clear 4-step workflow explanation
- ⚠️ Minimal usage examples
- ❌ No troubleshooting guide
- ❌ No comparison with manual approach

### 5. Practicality (2/5)

**Barriers to adoption**:
- Requires installation from personal dotfiles (not a standard package)
- No community validation (0 usage stats)
- Manual approach is simpler and safer for most cases

**When it makes sense**:
- Frequent session forking workflows
- Large session histories (ripgrep optimization beneficial)
- Automation preference over manual control

---

## Comparative Analysis

| Aspect | Weller Skill | Manual Approach | Claude Guide |
|--------|--------------|-----------------|--------------|
| **Cross-folder migration** | ✅ Automated | ✅ Manual (30 sec) | ❌ Not documented |
| **Complexity** | ⚠️ Requires skill install | ✅ Zero dependencies | N/A |
| **Safety** | ⚠️ Untested edge cases | ✅ Explicit control | N/A |
| **Adoption** | ❌ 0 stars/forks | ✅ Native filesystem ops | N/A |
| **Maintenance** | ⚠️ Personal repo | ✅ Self-maintained | N/A |

---

## Integration Decision

**Integrated as**: Section addition in `guide/observability.md`

**Rationale**:
1. **Gap confirmed**: GitHub issue #1516 validates the problem
2. **Manual approach prioritized**: Safer, simpler, zero dependencies
3. **Community tool mentioned**: Attribution with honest caveats (0 adoption)
4. **Risks documented**: Secrets, paths, MCP mismatches explicitly warned

**Placement**: `guide/observability.md` § "Session Resume Limitations & Cross-Folder Migration" (40 lines)

**Priority**: P2 (Important, not urgent) - integrate after critical guide updates

---

## Fact-Check Results

| Claim | Verified | Source |
|-------|----------|--------|
| "Clones sessions cross-folder" | ✅ | SKILL.md + LinkedIn post |
| "Inspired by Alexis Laporte" | ✅ | LinkedIn post attribution |
| "Uses ripgrep for performance" | ✅ | LinkedIn post |
| "cleanupPeriodDays: 90" | ✅ | LinkedIn post |
| "14 likes, 3 comments" | ✅ | LinkedIn engagement metrics |
| "GitHub issue #1516 exists" | ✅ | Perplexity search confirmed |
| "0 stars/forks" | ✅ | GitHub repo metadata |
| "Widely adopted" | ❌ | Contradicted by 0 stars/forks |

---

## Risks of Non-Integration

**Low risk**:
- 95%+ users won't need cross-folder migration (based on use case analysis)
- Manual workaround exists and is well-documented in community discussions
- No significant community pressure (minimal GitHub issue activity)

**Opportunity cost of NOT integrating**:
- Users facing this niche issue would discover manual solution via web search anyway
- Guide completeness improved marginally (covers 1-5% more use cases)

---

## Technical Writer Challenge Results

**Initial score**: 4/5
**Challenged score**: 3/5 (adjusted down)

**Key corrections**:
- Adoption metrics (0 stars/forks) reduce score
- Alternative manual approach is simpler → reduces uniqueness value
- Edge cases and risks not addressed by skill → reduces quality score
- Niche use case (1-5%) → reduces overall relevance

**Integration recommendation refined**:
- From: "200-300 line workflow + skill template"
- To: "40-line section with manual approach + skill mention"

---

## Recommendations

### For Guide Maintainers

1. **Document manual approach first** (recommended solution)
2. **Mention community skill** (attribution + honest caveats)
3. **Warn about risks** (secrets, paths, MCP mismatches)
4. **Link GitHub issue #1516** (feature request tracking)

### For Users

1. **Prefer manual approach** for safety and control
2. **Test skill thoroughly** before production use (0 community validation)
3. **Audit `.jsonl` files** for secrets before migration
4. **Verify MCP compatibility** between source and target projects

### For Skill Author (Jim Weller)

1. **Add comprehensive testing** (edge cases, different project types)
2. **Document security considerations** (secrets, credentials handling)
3. **Provide rollback mechanism** (undo failed migrations)
4. **Consider submitting to Claude Code official skills** for broader visibility

---

## Conclusion

**Score: 3/5** - Addresses a real but niche gap with minimal adoption. Manual approach is safer and simpler for most users. Integration as lightweight documentation (40 lines) is appropriate given the use case frequency and lack of community validation.

**Action**: Integrated in `guide/observability.md` with manual approach prioritized and community tool mentioned with caveats.

**Confidence**: High (based on GitHub issue confirmation, Perplexity search validation, and repository inspection)
