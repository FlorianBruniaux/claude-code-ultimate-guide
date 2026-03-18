# Audit Your Landing Cheatsheet

> A self-contained prompt to evaluate if your project needs a cheatsheet and audit existing ones against the gold standard.

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Methode Aristote](https://methode-aristote.fr)

**Reference**: [Claude Code Ultimate Guide Cheatsheet](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/cheatsheet.md) (gold standard)

---

## 1. What This Does

This prompt instructs Claude to perform a systematic cheatsheet audit in 4 phases:

1. **Discovery** — Explore the project source + landing to understand scope
2. **Evaluation** — Score whether the project needs a cheatsheet (objective criteria)
3. **Audit** — If a cheatsheet exists, grade it against 13 quality checkpoints
4. **Recommendation** — Go/no-go decision with actionable plan

**Covers 3 scenarios**:
- No cheatsheet exists → need assessment + go/no-go
- Partial cheatsheet (HTML only, or MD only) → gap analysis
- Complete cheatsheet (MD + PDF + HTML) → quality audit

**Time**: ~3-5 minutes depending on project size

---

## 2. Who This Is For

| Audience | What You'll Get |
|----------|-----------------|
| **Project maintainer** | Clear go/no-go on creating a cheatsheet |
| **Landing page builder** | Quality checklist for cheatsheet pages |
| **Documentation lead** | Gap analysis and prioritized improvements |

**Prerequisites**:
- Claude Code installed and working
- Access to the project source code (repo with docs/README)
- Access to the landing site (if exists)
- Bash shell (native on macOS/Linux, WSL on Windows)

---

## 3. How to Use It

### Step 1: Copy the Prompt

Copy everything inside the code block in [Section 4](#4-the-prompt) below.

### Step 2: Navigate to your project

```bash
cd your-project-directory
claude
```

### Step 3: Paste and Execute

Paste the prompt and press Enter. Claude will begin the 4-phase audit.

### Step 4: Review Results

Claude will present findings per phase and a final summary with actionable recommendations.

---

## 4. The Prompt

````markdown
# Cheatsheet Audit

## Context

You are a documentation quality auditor. Your job is to evaluate whether this project needs a cheatsheet, and if one exists, audit its quality against a proven gold standard.

**Gold standard reference**: The Claude Code Ultimate Guide cheatsheet — a 527-line Markdown file that condenses a 11K-line guide into 1 printable page, with matching PDF and HTML landing page versions.

## Instructions

Run all 4 phases sequentially. Report findings after each phase before proceeding.

---

### Phase 1: Discovery

**Goal**: Understand the project scope, audience, and existing documentation assets.

#### 1.1 Project Source Scan

```bash
bash -c '
echo "=== PROJECT IDENTITY ==="
[ -f "package.json" ] && echo "Name: $(grep -m1 \"name\" package.json | cut -d\" -f4)"
[ -f "Cargo.toml" ] && echo "Name: $(grep -m1 "name" Cargo.toml | cut -d\" -f2)"
[ -f "VERSION" ] && echo "Version: $(cat VERSION)" || echo "Version: not found"
echo ""

echo "=== DOCUMENTATION ==="
for f in README.md CLAUDE.md CHANGELOG.md; do
  [ -f "$f" ] && echo "✅ $f ($(wc -l < "$f") lines)" || echo "❌ $f"
done
echo ""

echo "=== GUIDE/DOCS DIRECTORY ==="
for d in guide docs doc documentation; do
  [ -d "$d" ] && echo "✅ $d/ ($(find "$d" -name "*.md" | wc -l | tr -d " ") md files)" || echo "— $d/ not found"
done
echo ""

echo "=== CHEATSHEET FILES ==="
find . -maxdepth 3 -iname "*cheatsheet*" -o -iname "*cheat-sheet*" -o -iname "*quick-ref*" -o -iname "*quickref*" 2>/dev/null | head -20
echo ""

echo "=== EXAMPLES/TEMPLATES ==="
for d in examples templates; do
  [ -d "$d" ] && echo "✅ $d/ ($(find "$d" -type f | wc -l | tr -d " ") files)"
done
'
```

#### 1.2 Landing Site Scan

If the project has an associated landing site, scan it:

```bash
bash -c '
echo "=== LANDING SEARCH ==="
# Check common landing locations relative to project
PROJECT_NAME=$(basename "$PWD")
for suffix in "-landing" "-site" "-web" "-docs"; do
  LANDING="../${PROJECT_NAME}${suffix}"
  [ -d "$LANDING" ] && echo "✅ Found: $LANDING" && ls "$LANDING"/*.html 2>/dev/null | head -5
done

# Check for cheatsheet in landing
echo ""
echo "=== LANDING CHEATSHEET ==="
find .. -maxdepth 3 -path "*landing*" -name "*cheatsheet*" 2>/dev/null | head -10
'
```

#### 1.3 Content Complexity Assessment

```bash
bash -c '
echo "=== COMPLEXITY INDICATORS ==="

# Commands/CLI
echo "--- Commands ---"
grep -rh "^\`[a-z]" README.md guide/*.md docs/*.md 2>/dev/null | sort -u | wc -l | xargs echo "CLI commands found:"
grep -rhi "slash command\|/command\|custom command" README.md guide/*.md docs/*.md 2>/dev/null | wc -l | xargs echo "Slash command refs:"

# Keyboard shortcuts
echo "--- Shortcuts ---"
grep -rhi "ctrl\|alt\|shift\|cmd\|⌘\|shortcut" README.md guide/*.md docs/*.md 2>/dev/null | wc -l | xargs echo "Shortcut references:"

# Config files
echo "--- Configuration ---"
grep -rhi "config\|settings\|\.env\|\.json\|\.yaml\|\.toml" README.md guide/*.md docs/*.md 2>/dev/null | wc -l | xargs echo "Config references:"

# API surface
echo "--- API/Features ---"
grep -rhi "endpoint\|api\|route\|feature\|flag" README.md guide/*.md docs/*.md 2>/dev/null | wc -l | xargs echo "API/feature refs:"

# Total doc volume
echo "--- Volume ---"
find . -name "*.md" -not -path "./.git/*" -not -path "*/node_modules/*" | xargs wc -l 2>/dev/null | tail -1 | xargs echo "Total MD lines:"
'
```

**After running Phase 1, report:**
- Project name, version, type (CLI tool / library / app / framework)
- Target audience (developers / non-devs / mixed)
- Documentation volume (lines, files)
- Existing cheatsheet assets found (MD, PDF, HTML, none)
- Complexity indicators summary

---

### Phase 2: Need Evaluation

**Goal**: Determine objectively whether this project warrants a cheatsheet.

Score each criterion 0-2 (0 = no, 1 = partial, 2 = yes):

| # | Criterion | Score Guide | Score |
|---|-----------|-------------|-------|
| 1 | **Command surface** | 2 = 10+ commands, 1 = 5-9, 0 = <5 | |
| 2 | **Keyboard shortcuts** | 2 = 5+ shortcuts, 1 = 2-4, 0 = 0-1 | |
| 3 | **Configuration complexity** | 2 = multiple config files/levels, 1 = single config, 0 = minimal | |
| 4 | **Multi-step workflows** | 2 = documented workflows, 1 = implicit workflows, 0 = none | |
| 5 | **Decision points** | 2 = multiple modes/options to choose from, 1 = some, 0 = linear | |
| 6 | **Reference frequency** | 2 = users look up daily, 1 = weekly, 0 = once then done | |
| 7 | **Documentation volume** | 2 = >2000 lines docs, 1 = 500-2000, 0 = <500 | |
| 8 | **Audience breadth** | 2 = beginners + advanced, 1 = single level, 0 = niche experts | |

**Scoring**:
- **12-16**: Strong need — cheatsheet is high value
- **8-11**: Moderate need — cheatsheet adds value
- **4-7**: Low need — consider a "Quick Start" section instead
- **0-3**: No need — a good README suffices

**Report**: Table with scores, total, and verdict (Strong/Moderate/Low/None).

---

### Phase 3: Quality Audit (if cheatsheet exists)

**Goal**: Grade the existing cheatsheet against the gold standard's 13 quality checkpoints.

If no cheatsheet was found in Phase 1, skip to Phase 4.

For each checkpoint, grade: Pass / Partial / Fail / N/A.

#### A. Version & Date Sync

Check that version numbers match the project's source of truth:
- Header/footer version matches `VERSION` file or `package.json`
- "Last updated" date is current (within 1 month of latest release)
- HTML: schema.org `dateModified` matches
- HTML: Open Graph metadata matches

#### B. Factual Accuracy

Spot-check 3-5 factual claims against the source documentation:
- Are described features still current? (no deprecated items listed as active)
- Are version requirements accurate?
- Are any "keywords" or "magic strings" documented that don't actually work?

#### C. Commands Completeness

Compare commands listed vs. actual available commands:
- Count commands in cheatsheet vs. source docs
- Flag any missing essential commands
- Flag any deprecated commands still listed

#### D. Keyboard Shortcuts Completeness

Compare shortcuts listed vs. actual shortcuts:
- Cross-reference with source documentation
- Check platform-specific variants (macOS vs Windows/Linux)
- Verify no deprecated shortcuts

#### E. Feature Tables Accuracy

For each feature table in the cheatsheet:
- Verify column values against source docs
- Check for outdated entries
- Verify links still work

#### F. Decision Trees / Quick Reference

If the cheatsheet includes decision trees or flowcharts:
- Verify all paths lead to valid recommendations
- Check that referenced features/commands exist
- Ensure no dead-end paths

#### G. Folder Structure / Config

If folder structure or config layout is documented:
- Compare against actual project structure
- Verify all listed files/dirs exist
- Flag any missing important paths

#### H. Installation Correctness

If installation instructions are included:
- Verify package name is correct
- Check version constraints
- Test install command mentally against current ecosystem

#### I. Section Coverage (cross-format)

Compare coverage across available formats:

| Section | MD | PDF | HTML |
|---------|:--:|:---:|:----:|
| Commands | ? | ? | ? |
| Shortcuts | ? | ? | ? |
| Config | ? | ? | ? |
| Workflows | ? | ? | ? |
| Troubleshooting | ? | ? | ? |

Flag sections present in one format but missing in another.

#### J. Cost / Pricing Accuracy

If pricing or cost information is included:
- Verify against current official pricing
- Check that model names are current
- Verify any "free tier" claims

#### K. CLI Flags Completeness

If CLI flags are documented:
- Compare against `--help` output or source docs
- Flag missing commonly-used flags
- Flag deprecated flags still listed

#### L. SEO / Schema.org (HTML landing only)

For HTML cheatsheet pages:
- Verify `<script type="application/ld+json">` schema exists
- Check `dateModified` is current
- Verify canonical URL
- Check Open Graph tags (title, description, image)
- Check meta description accuracy
- Verify print CSS exists (cheatsheets get printed)

#### M. PDF Rendering Quality

For PDF cheatsheets:
- Tables render correctly (no broken columns)
- Special characters display properly (checkmarks, arrows, emojis)
- Code blocks are readable (monospace font, syntax highlighting)
- Fits intended page count (1 page for quick ref, 2-4 for detailed)
- Print-friendly (no dark backgrounds eating ink)

**Report**: Table with all 13 checkpoints graded, plus notes on critical failures.

---

### Phase 4: Recommendation

**Goal**: Deliver a clear, actionable verdict.

#### If no cheatsheet exists (Phase 2 result)

Based on the need score:

**Score 12-16 (Strong need)**:
```
VERDICT: GO — Create cheatsheet
Priority: HIGH
Estimated effort: [S/M/L based on complexity]
Recommended formats: [MD only / MD+PDF / MD+PDF+HTML]
Suggested sections (based on Phase 1 findings):
1. [section] — [why]
2. [section] — [why]
...
```

**Score 8-11 (Moderate need)**:
```
VERDICT: CONDITIONAL GO — Create if [condition]
Priority: MEDIUM
Condition: [e.g., "if landing site targets beginners"]
Lighter alternative: [e.g., "expanded Quick Start in README"]
```

**Score 4-7 (Low need)**:
```
VERDICT: NO-GO — Quick Start section recommended instead
Reason: [specific reasons]
Alternative: Add a "Quick Start" or "TL;DR" section to README
```

**Score 0-3 (No need)**:
```
VERDICT: NO-GO — README is sufficient
Reason: [specific reasons]
```

#### If cheatsheet exists (Phase 3 result)

```
AUDIT SCORE: [X/13 passing]
Critical failures: [list]
Priority fixes:
1. [fix] — [impact]
2. [fix] — [impact]
...
Missing formats: [list needed: MD / PDF / HTML]
Estimated effort to reach gold standard: [S/M/L]
```

---

## Gold Standard Reference

The Claude Code cheatsheet serves as the benchmark. Here's what makes it the gold standard:

### Structure (527 lines, 17 sections)

```
1. Essential Commands (15 commands, table format)
2. Keyboard Shortcuts (9 shortcuts, table format)
3. File References (syntax + IDE shortcuts)
4. Hidden Features (versioned feature table)
5. Permission Modes (3-mode matrix)
6. Memory & Settings (2-level config with paths)
7. .claude/ Folder Structure (tree diagram)
8. Typical Workflow (numbered step-by-step)
9. Context Management (thresholds + symptoms + recovery)
10. Under the Hood (quick facts table)
11. Plan Mode & Thinking (controls + cost + model switching)
12. MCP Servers (7 servers, table format)
13. Creating Custom Components (agent/command/hook templates)
14. Anti-patterns (do/don't table)
15. Quick Prompting Formula (template + example)
16. CLI Flags Quick Reference (13 flags)
17. Golden Rules (7 rules, numbered)
```

### Quality Characteristics

- **Density**: 527 lines condenses 19,000+ lines (36:1 ratio)
- **Scannability**: Every section uses tables, code blocks, or numbered lists
- **Actionability**: Every entry answers "what do I type?" not "what is this?"
- **Cross-format**: MD (source) + PDF (print) + HTML (landing, with dark theme + print CSS)
- **Version-synced**: Header, footer, schema.org all match VERSION file
- **Platform-aware**: macOS + Windows paths where relevant
- **Anti-pattern section**: Shows what NOT to do (high value for beginners)
- **Decision tree**: "What should I do?" quick routing

### HTML Landing Patterns

When evaluating HTML cheatsheet pages, the gold standard includes:
- Dark theme with syntax highlighting
- Print-optimized CSS (`@media print`)
- Schema.org `TechArticle` markup with `dateModified`
- Open Graph tags for social sharing
- Responsive design (mobile-friendly tables)
- Navigation integration (linked from main landing)
- Download CTA for PDF version
````

---

## 5. Example Output

Here's what the audit looks like when run against a real project:

### Example: Project with no cheatsheet

```
=== PHASE 1: DISCOVERY ===
Project: cc-copilot-bridge v1.5.3 (CLI tool)
Audience: Developers (VS Code users)
Docs: README.md (450 lines), 3 guide files (1200 lines total)
Cheatsheet: None found
Complexity: 12 commands, 6 config options, 3 workflows

=== PHASE 2: NEED EVALUATION ===
| # | Criterion              | Score |
|---|------------------------|-------|
| 1 | Command surface        | 2     |
| 2 | Keyboard shortcuts     | 1     |
| 3 | Config complexity      | 1     |
| 4 | Multi-step workflows   | 2     |
| 5 | Decision points        | 1     |
| 6 | Reference frequency    | 2     |
| 7 | Documentation volume   | 1     |
| 8 | Audience breadth       | 1     |
|   | **TOTAL**              | **11** |

VERDICT: CONDITIONAL GO
Priority: MEDIUM
Condition: If landing site is created for broader audience
Lighter alternative: "Quick Reference" section in README

=== PHASE 3: SKIPPED (no cheatsheet) ===

=== PHASE 4: RECOMMENDATION ===
If you decide to create a cheatsheet:
- Start with MD format (1-2 hours)
- Sections: Commands, Config, Workflows, Troubleshooting
- Skip PDF/HTML until landing site exists
```

---

**Version**: 1.0.0 | **Last Updated**: February 2026
