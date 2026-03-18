# Audit Your Context Engineering Setup

> A self-contained prompt to measure and improve your Claude Code context architecture.

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Reference**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. What This Does

This prompt instructs Claude to audit your context engineering setup by:

1. **Measuring** total always-on context size, CLAUDE.md length, and path-scoping ratio
2. **Detecting** skills-to-rules balance, redundancy, and negative vs positive instructions
3. **Flagging** staleness signals (last updated, broken imports, deprecated references)
4. **Scoring** across 8 dimensions for a total of /100 with prioritized recommendations

**Performance**: Uses bash/grep for efficient scanning. Claude reads files only when specific content analysis is needed.

**Important**: Claude will NOT make any changes without your explicit approval.

---

## 2. Who This Is For

| Level | What You Get |
|-------|-------------|
| **Solo developer** | Find quick wins: trim bloat, add missing sections, fix stale imports |
| **Small team (2-10)** | Identify consistency gaps and opportunities for profile-based assembly |
| **Large team (10+)** | Systematic context architecture assessment with maturity scoring |

**Prerequisites**:
- Claude Code installed and working
- A project with at least a CLAUDE.md or `.claude/` directory
- Bash shell (native on macOS/Linux, WSL on Windows)

**Time**: ~3-5 minutes

---

## 3. How to Use It

### Step 1: Copy the Prompt

Copy everything inside the code block in [Section 4](#4-the-prompt) below.

### Step 2: Run Claude Code

```bash
cd your-project-directory
claude
```

### Step 3: Paste and Execute

Paste the prompt and press Enter. Claude will begin the audit.

### Step 4: Review Results

Claude will present findings, then ask for validation before making any changes.

### Platform Note

| Platform | Global Config Path |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. The Prompt

```markdown
# Audit My Context Engineering Setup

## Context

Perform a comprehensive context engineering audit of my Claude Code configuration.
Focus on context size, structure quality, freshness, and team scalability.

Reference: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md

## Instructions

### Phase 1: Discovery (Bash Scan)

**IMPORTANT**: Use bash commands exclusively in this phase. Do NOT read files yet.

#### 1.1 Size & Structure Scan

```bash
bash -c '
echo "=== GLOBAL CLAUDE.MD ==="
if [ -f ~/.claude/CLAUDE.md ]; then
  lines=$(wc -l < ~/.claude/CLAUDE.md | tr -d " ")
  chars=$(wc -c < ~/.claude/CLAUDE.md | tr -d " ")
  tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
  echo "Lines: $lines"
  echo "Chars: $chars (~$tokens tokens)"
  echo "Imports: $(grep -c "^@" ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Rules count: $(grep -cE "^[-*] |^\d+\. " ~/.claude/CLAUDE.md 2>/dev/null || echo 0)"
  echo "Last commit: $(cd ~/.claude && git log --format="%ar" -- CLAUDE.md 2>/dev/null | head -1 || echo "not tracked")"
else
  echo "NOT FOUND"
fi

echo ""
echo "=== PROJECT CLAUDE.MD ==="
for f in ./CLAUDE.md ./.claude/CLAUDE.md; do
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f" | tr -d " ")
    chars=$(wc -c < "$f" | tr -d " ")
    tokens=$(echo "scale=0; $chars / 4" | bc 2>/dev/null || echo "~$((chars/4))")
    echo "File: $f"
    echo "Lines: $lines"
    echo "Chars: $chars (~$tokens tokens)"
    echo "Imports: $(grep -c "^@" "$f" 2>/dev/null || echo 0)"
    echo "Rules count: $(grep -cE "^[-*] |^\d+\. " "$f" 2>/dev/null || echo 0)"
    echo "Last commit: $(git log --format="%ar" -- "$f" 2>/dev/null | head -1 || echo "not tracked")"
  fi
done

echo ""
echo "=== IMPORTED FILES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  while IFS= read -r line; do
    [[ "$line" =~ ^@ ]] || continue
    import_path="${line#@}"
    import_path="${import_path/ */}"
    resolved="${import_path/#\~/$HOME}"
    resolved="${resolved/#./$PWD}"
    if [ -f "$resolved" ]; then
      sz=$(wc -c < "$resolved" | tr -d " ")
      tk=$(echo "scale=0; $sz / 4" | bc 2>/dev/null || echo "$((sz/4))")
      echo "  FOUND $line (~$tk tokens)"
    else
      echo "  BROKEN $line (file not found)"
    fi
  done < "$f"
done

echo ""
echo "=== RULES & MODULES ==="
for d in ~/.claude ./.claude; do
  [ -d "$d" ] || continue
  for sub in rules skills commands agents hooks; do
    if [ -d "$d/$sub" ]; then
      count=$(find "$d/$sub" -maxdepth 1 -type f | wc -l | tr -d " ")
      total_chars=$(find "$d/$sub" -maxdepth 1 -type f -exec cat {} \; 2>/dev/null | wc -c | tr -d " ")
      tokens=$((total_chars / 4))
      echo "  $d/$sub: $count files (~$tokens tokens)"
    fi
  done
done
'
```

**Store the output** for evaluation.

#### 1.2 Quality Pattern Scan

```bash
bash -c '
echo "=== NEGATIVE VS POSITIVE INSTRUCTIONS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  neg=$(grep -ciE "never|do not|dont|avoid|prohibited|forbidden|not allowed|do NOT" "$f" 2>/dev/null || echo 0)
  pos=$(grep -ciE "always|prefer|use|should|must|recommended|do this" "$f" 2>/dev/null || echo 0)
  echo "$f: negative=$neg positive=$pos"
done

echo ""
echo "=== VAGUE INSTRUCTIONS (red flags) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -inE "be careful|good practice|appropriately|as needed|when necessary|use your judgment|you should know|be smart" "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== DUPLICATE SECTION HEADERS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  dupes=$(grep -E "^#{1,3} " "$f" | sort | uniq -d)
  [ -n "$dupes" ] && echo "$f DUPLICATES: $dupes" || echo "$f: no duplicate headers"
done

echo ""
echo "=== DEPRECATED REFERENCES ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  grep -niE "claude-1|claude-2\.0|claude-3-haiku-|gpt-3\.5|text-davinci|codex|copilot X|cursor pro 1\." "$f" 2>/dev/null | head -5 || echo "  none found"
done

echo ""
echo "=== PATH SCOPING (modular setup) ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  scoped=$(grep -cE "^@.+\.(ts|tsx|js|jsx|py|rs|go|md)$|globs:|path:" "$f" 2>/dev/null || echo 0)
  echo "$f path-scoped entries: $scoped"
done

echo ""
echo "=== SESSION & UPDATE PROTOCOL ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_update=$(grep -ciE "update|review|quarterly|maintenance|how to update|keep.*fresh" "$f" 2>/dev/null || echo 0)
  has_session=$(grep -ciE "session|retro|checkpoint|lesson learned|knowledge loop" "$f" 2>/dev/null || echo 0)
  echo "$f: update-protocol=$has_update session-retro=$has_session"
done

echo ""
echo "=== TEAM/PROFILE READINESS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_profile=$(grep -ciE "profile|role:|junior|senior|lead|persona|persona-" "$f" 2>/dev/null || echo 0)
  has_module=$(grep -cE "^@" "$f" 2>/dev/null || echo 0)
  echo "$f: profile-mentions=$has_profile module-imports=$has_module"
done
'
```

**Store the output** for evaluation.

#### 1.3 Freshness & Conflict Scan

```bash
bash -c '
echo "=== GIT FRESHNESS ==="
for path in ~/.claude ./; do
  if git -C "$path" rev-parse --git-dir &>/dev/null 2>&1; then
    echo "Repo at $path:"
    git -C "$path" log --format="%ar %s" -- CLAUDE.md .claude/CLAUDE.md 2>/dev/null | head -3 || echo "  no commits for CLAUDE.md"
  fi
done

echo ""
echo "=== CONFLICTING RULES PATTERNS ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  echo "$f:"
  # Look for contradictory patterns like "always X" near "never X"
  always_terms=$(grep -ioE "always [a-z ]+" "$f" 2>/dev/null | sed "s/always //i" | sort)
  never_terms=$(grep -ioE "never [a-z ]+" "$f" 2>/dev/null | sed "s/never //i" | sort)
  conflicts=$(comm -12 <(echo "$always_terms") <(echo "$never_terms") 2>/dev/null)
  [ -n "$conflicts" ] && echo "  POTENTIAL CONFLICTS: $conflicts" || echo "  no obvious contradictions"
done

echo ""
echo "=== OVERVIEW / ARCHITECTURE SECTION ==="
for f in ~/.claude/CLAUDE.md ./CLAUDE.md ./.claude/CLAUDE.md; do
  [ -f "$f" ] || continue
  has_overview=$(grep -ciE "^## (overview|purpose|about|architecture|what this|context)" "$f" 2>/dev/null || echo 0)
  has_antip=$(grep -ciE "anti.pattern|bad example|do not do|wrong way|pitfall" "$f" 2>/dev/null || echo 0)
  has_hierarchy=$(grep -cE "^#{1,3} " "$f" 2>/dev/null || echo 0)
  echo "$f: has-overview=$has_overview anti-patterns=$has_antip section-count=$has_hierarchy"
done
'
```

**Store the output** for evaluation.

### Phase 2: Evaluate Across 8 Dimensions

Use the scan outputs from Phase 1. Read specific file sections only if content examples are needed for the report.

#### Dimension 1: Size & Budget (15 pts)

Evaluate based on token estimates from Phase 1:

| Check | Points | Threshold |
|-------|--------|-----------|
| Total always-on context under 8K tokens | 5 | Sum of all CLAUDE.md + imports |
| Rule count under 150 instructions | 5 | global + project combined |
| No single file over 400 lines | 5 | flag if exceeded |

Deduct points proportionally if thresholds are exceeded. A file at 600 lines = 3/5 not 0.

#### Dimension 2: Structure (15 pts)

| Check | Points | Signal |
|-------|--------|--------|
| Has an overview/purpose section | 4 | h2 with "overview", "purpose", "about", "context" |
| Has architecture or project-layout section | 3 | h2 with "architecture", "structure", "layout" |
| Includes anti-patterns or bad examples | 4 | "anti-pattern", "do not", "pitfall" |
| Section count indicates clear hierarchy | 4 | 3+ distinct h2 sections |

#### Dimension 3: Path-Scoping (12 pts)

| Check | Points | Signal |
|-------|--------|--------|
| Uses @imports for modular breakdown | 5 | at least 2 @import lines |
| At least one path-specific or glob-scoped rule | 4 | globs: or file-specific section |
| Not a monolithic file (all instructions in one block) | 3 | multiple files or sections |

#### Dimension 4: Rule Quality (15 pts)

| Check | Points | Signal |
|-------|--------|--------|
| Ratio positive:negative >= 2:1 | 5 | from negative/positive counts |
| No vague instructions detected | 5 | zero "be careful", "as needed", etc. |
| Rules are specific and actionable | 5 | judged from sample during report generation |

#### Dimension 5: Freshness (12 pts)

| Check | Points | Signal |
|-------|--------|--------|
| CLAUDE.md committed within past 6 months | 5 | git log output |
| No deprecated tool/model references | 4 | deprecated scan output |
| No broken @imports | 3 | BROKEN lines in import scan |

#### Dimension 6: Team Readiness (10 pts)

| Check | Points | Signal |
|-------|--------|--------|
| Has profile-based or role-based structure | 4 | profile mentions >= 1 |
| Module imports enable selective assembly | 3 | module-imports >= 3 |
| Documented update protocol for team | 3 | update-protocol >= 1 |

#### Dimension 7: Conflict Detection (11 pts)

| Check | Points | Signal |
|-------|--------|--------|
| No contradictory rules detected | 5 | no conflicts from scan |
| No duplicate section headers | 3 | no duplicates found |
| Session retro or knowledge loop pattern | 3 | session-retro >= 1 |

#### Dimension 8: Knowledge Loop (10 pts)

| Check | Points | Signal |
|-------|--------|--------|
| Has update/review protocol documented | 4 | update-protocol >= 1 |
| Has session retro or lesson-learned pattern | 3 | session-retro >= 1 |
| Context tracked in git (auditable changes) | 3 | git freshness scan shows commits |

#### Calculate Total Score

`Score = sum of earned points across all 8 dimensions`

### Phase 3: Generate Report

Structure your output exactly as:

---

## Context Engineering Audit

### Score: [XX]/100

| Dimension | Score | Notes |
|-----------|-------|-------|
| Size & Budget | X/15 | total ~X tokens, X rules |
| Structure | X/15 | X sections, has/missing overview |
| Path-Scoping | X/12 | X imports, monolithic/modular |
| Rule Quality | X/15 | X% positive, X vague found |
| Freshness | X/12 | last updated X, X broken imports |
| Team Readiness | X/10 | X profiles, update protocol: yes/no |
| Conflict Detection | X/11 | X contradictions, X duplicate headers |
| Knowledge Loop | X/10 | git tracked: yes/no, retro: yes/no |

### Context Budget
- Global CLAUDE.md: ~X tokens
- Project CLAUDE.md: ~X tokens
- @imports combined: ~X tokens
- Total always-on: ~X tokens
- Rule count: X/150 instructions

### Priority Issues (fix these first)
1. [Issue] — [specific fix with example]
2. [Issue] — [specific fix with example]
3. [Issue] — [specific fix with example]

### Quick Wins (< 30 min each)
- [Fix]: [what to do and where]
- [Fix]: [what to do and where]
- [Fix]: [what to do and where]

### Maturity Level
[Choose one and explain why]

**Level 1 — Empty** (0-19): No structured context. Claude operates with zero project knowledge.
**Level 2 — Basic** (20-39): CLAUDE.md exists but is monolithic, stale, or mostly vague rules.
**Level 3 — Structured** (40-59): Clear sections and imports, but missing freshness or team patterns.
**Level 4 — Optimized** (60-79): Modular, scoped, positive-first rules with a known update cadence.
**Level 5 — Engineering-Grade** (80-100): Profile-aware, git-tracked, conflict-free, knowledge loop active.

### Ready-to-use Improvements

Provide 2-3 concrete text blocks that users can paste directly into their CLAUDE.md.
Each block must address a Priority Issue identified above. Format:

**Improvement 1: [name]**
File: `[path]` — add at [top/section X/end]
```
[exact text to paste]
```

**Improvement 2: [name]**
File: `[path]` — add at [top/section X/end]
```
[exact text to paste]
```

---

### Phase 4: Await Validation

**CRITICAL**: Do NOT create or modify any files without explicit approval.

After presenting the report, ask:

"Which improvements would you like me to implement?

Options:
- `all` — Apply all ready-to-use improvements
- `1, 2` — Specific improvements by number
- `priority` — Only Priority Issues fixes
- `none` — Keep the report for reference only

Please specify your choice:"

Wait for explicit user response before taking any action.

## Output Format

Structure your response exactly as:

1. **Score table** with dimension breakdown
2. **Context Budget** summary
3. **Priority Issues** (numbered, fix first)
4. **Quick Wins** (bullet list, < 30 min each)
5. **Maturity Level** with explanation
6. **Ready-to-use Improvements** (paste-ready text blocks)
7. **Validation Request** (ask before implementing)
```

---

## 5. What to Expect

Here's an example of what the audit report looks like:

### Example Score Table

```
## Context Engineering Audit

### Score: 52/100

| Dimension | Score | Notes |
|-----------|-------|-------|
| Size & Budget | 10/15 | ~6,200 tokens total, 182 rules (over limit) |
| Structure | 9/15 | 4 sections, no anti-patterns section |
| Path-Scoping | 4/12 | 1 import, monolithic project CLAUDE.md |
| Rule Quality | 8/15 | 60% positive, 3 vague instructions found |
| Freshness | 9/12 | last commit 4 months ago, 1 broken import |
| Team Readiness | 3/10 | no profiles, no update protocol |
| Conflict Detection | 6/11 | 1 "always/never" contradiction, no duplicate headers |
| Knowledge Loop | 3/10 | not git tracked, no retro pattern |
```

### Example Quick Wins

```
Quick Wins (< 30 min each):
- Fix broken import: @~/.claude/TONE.md not found — update path or remove
- Add overview section: 2-line project description at top of CLAUDE.md
- Trim rule count: merge 3 formatting rules into one compressed block
```

---

## 6. Scoring Guide

| Score | Maturity | Recommended Action |
|-------|----------|--------------------|
| **80-100** | Level 5: Engineering-Grade | Maintain with quarterly review |
| **60-79** | Level 4: Optimized | Address priority issues, reach 80 |
| **40-59** | Level 3: Structured | Dedicate a session to improvement |
| **20-39** | Level 2: Basic | Restructure recommended, use template |
| **0-19** | Level 1: Empty | Start fresh with skeleton template |

---

## 7. Glossary

| Term | Definition |
|------|-----------|
| **Always-on context** | Everything Claude loads before your first message: CLAUDE.md files plus all @imports |
| **@import** | A line starting with `@` in CLAUDE.md that loads another file into context |
| **Path-scoping** | Applying rules only to specific file types or directories, not globally |
| **Rule quality** | Specificity and actionability of instructions — vague rules waste tokens and confuse Claude |
| **Knowledge loop** | The practice of updating context files after sessions based on what worked and what didn't |
| **Profile assembly** | Combining different context modules to create role-specific setups (junior, senior, reviewer) |
| **Staleness signal** | Indicators that context is outdated: broken imports, deprecated model names, no git history |
| **Conflict** | Two rules that contradict each other — Claude will pick one arbitrarily, usually the wrong one |
| **Monolithic CLAUDE.md** | A single large file with all instructions, no imports, no modular breakdown |
| **Maturity level** | A 1-5 scale measuring context engineering sophistication from empty to engineering-grade |

---

## 8. Common Issues

### "Token estimate seems off"

**Cause**: The estimate uses chars/4 as a rough proxy for GPT-style tokens. Claude's tokenizer may differ slightly.

**Fix**: Focus on relative numbers and thresholds rather than absolute token counts. The 8K always-on budget is a heuristic, not a hard limit.

### "Score is low but Claude seems to work fine"

**Cause**: Claude works without context engineering — the score reflects optimization, not basic functionality.

**Fix**: A low score means you're leaving productivity on the table. Each dimension gap adds cognitive overhead per session.

### "Broken import flagged but file exists"

**Cause**: Relative path resolution differs from Claude's actual working directory at startup.

**Fix**: Use absolute paths (`~/.claude/file.md`) for global imports. Use project-relative paths (`./docs/conventions.md`) for project imports.

### "Profile-readiness flagged but I'm solo"

**Cause**: The audit checks for team-scalability patterns regardless of team size.

**Fix**: Profile-based assembly still benefits solo developers when switching contexts (reviewing PRs vs writing features vs debugging). It is optional for solo use.

---

## 9. Related Resources

- [The Ultimate Claude Code Guide](../guide/ultimate-guide.md) - Full reference
- [Audit Your Claude Code Setup](./audit-prompt.md) - Full configuration audit (agents, hooks, MCP, CI)
- [Cheatsheet](../guide/cheatsheet.md) - Quick daily reference
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code) - Anthropic documentation

---

*Last updated: March 2026 | Version 1.0*
