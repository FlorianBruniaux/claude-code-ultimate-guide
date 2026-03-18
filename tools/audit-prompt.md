# Audit Your Claude Code Setup

> A self-contained prompt to analyze your Claude Code configuration against best practices.

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Reference**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## 1. What This Does

This prompt instructs Claude to perform a comprehensive audit of your Claude Code setup by:

1. **Scanning** your global and project configuration files using efficient bash commands
2. **Evaluating** each element against best practices from the guide
3. **Generating** a prioritized report with actionable recommendations
4. **Providing** ready-to-use templates tailored to your tech stack

**Performance**: Uses bash/grep for ~80% faster scanning and 90% fewer tokens compared to reading files.

**Important**: Claude will NOT make any changes without your explicit approval.

---

## 2. Who This Is For

| Level | What You'll Get |
|-------|-----------------|
| **Beginner** | Discover what you're missing and get starter templates |
| **Intermediate** | Identify optimization opportunities and advanced patterns |
| **Power User** | Validate your setup and find edge cases to polish |

**Prerequisites**:
- Claude Code installed and working
- A project directory to analyze (or just global config)
- Bash shell (native on macOS/Linux, WSL on Windows)

**Time**: ~2-3 minutes (optimized with bash scanning)

---

## 3. How to Use It

### Step 1: Copy the Prompt

Copy everything inside the code block in [Section 4](#4-the-prompt) below.

### Step 2: Run Claude Code

```bash
cd your-project-directory
claude
```

> **Note**: With Opus 4.6, thinking mode is enabled by default at maximum depth. Use Alt+T to toggle if needed.

### Step 3: Paste and Execute

Paste the prompt and press Enter. Claude will begin the audit.

### Step 4: Review Results

Claude will present findings and ask for validation before making any changes.

### Platform Note

| Platform | Global Config Path |
|----------|-------------------|
| **macOS/Linux** | `~/.claude/` |
| **Windows** | `%USERPROFILE%\.claude\` |

---

## 4. The Prompt

```markdown
# Audit My Claude Code Setup

## Context

Perform a comprehensive audit of my Claude Code configuration against best practices from "The Ultimate Claude Code Guide":
https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md

## Instructions

### Phase 1: Discovery (Bash Scan)

**IMPORTANT**: Use efficient bash commands. Do NOT read files unnecessarily.

#### 1.1 Quick Configuration Scan

**Run this bash command to get all config status at once:**

```bash
bash -c '
echo "=== GLOBAL CONFIG ==="
for f in ~/.claude/CLAUDE.md ~/.claude/settings.json; do
  [ -f "$f" ] && echo "✅ $(basename $f)" || echo "❌ $(basename $f)"
done
# Note: MCP config is now in ~/.claude.json, not ~/.claude/mcp.json
[ -f ~/.claude.json ] && echo "✅ ~/.claude.json (contains MCP config)" || echo "❌ ~/.claude.json"

echo -e "\n=== PROJECT CONFIG ==="
for f in ./CLAUDE.md ./.claude/CLAUDE.md ./.claude/settings.json ./.claude/settings.local.json; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ $f"
done

echo -e "\n=== EXTENSIONS ==="
for d in agents commands skills hooks rules; do
  if [ -d "./.claude/$d" ]; then
    count=$(find "./.claude/$d" -maxdepth 1 -type f | wc -l | tr -d " ")
    echo "✅ $d: $count files"
  else
    echo "❌ $d/"
  fi
done

echo -e "\n=== TECH STACK ==="
[ -f package.json ] && echo "nodejs: $(grep -oP "\"name\":\s*\"\K[^\"]*" package.json 2>/dev/null || echo "detected")"
[ -f pyproject.toml ] && echo "python: $(grep "^name" pyproject.toml | head -1)"
[ -f requirements.txt ] && echo "python: requirements.txt"
[ -f go.mod ] && echo "go: $(head -1 go.mod)"
[ -f Cargo.toml ] && echo "rust: $(grep "^name" Cargo.toml | head -1)"
[ -f composer.json ] && echo "php: detected"
[ -f Gemfile ] && echo "ruby: detected"
'
```

**Store the output** for evaluation phase.

#### 1.2 Quality Pattern Checks

**Run these targeted grep commands:**

```bash
bash -c '
# Security hooks
echo "=== SECURITY HOOKS ==="
if [ -d "./.claude/hooks" ]; then
  grep -l "PreToolUse" ./.claude/hooks/* 2>/dev/null || echo "❌ None found"
else
  echo "❌ No hooks directory"
fi

# MCP servers (check all locations)
echo -e "\n=== MCP SERVERS ==="
CURRENT_DIR=$(pwd)

# Check 1: Project-specific MCP in ~/.claude.json (most common)
if [ -f ~/.claude.json ] && command -v jq &> /dev/null; then
  MCP=$(jq -r --arg path "$CURRENT_DIR" ".projects[\$path].mcpServers // {} | keys[]" ~/.claude.json 2>/dev/null)
  if [ -n "$MCP" ]; then
    echo "Source: ~/.claude.json (project)"
    echo "$MCP"
  fi
fi

# Check 2: Project-level .claude/mcp.json
if [ -z "$MCP" ] && [ -f ./.claude/mcp.json ]; then
  echo "Source: .claude/mcp.json"
  if command -v jq &> /dev/null; then
    jq -r ".mcpServers // {} | keys[]" ./.claude/mcp.json 2>/dev/null
  else
    grep -oE "\"[a-zA-Z0-9_-]+\"[[:space:]]*:" ./.claude/mcp.json | sed "s/\"//g;s/://g"
  fi
fi

# Check 3: Legacy global ~/.claude/mcp.json
if [ -z "$MCP" ] && [ -f ~/.claude/mcp.json ]; then
  echo "Source: ~/.claude/mcp.json (global)"
  if command -v jq &> /dev/null; then
    jq -r ".mcpServers // {} | keys[]" ~/.claude/mcp.json 2>/dev/null
  else
    grep -oE "\"[a-zA-Z0-9_-]+\"[[:space:]]*:" ~/.claude/mcp.json | sed "s/\"//g;s/://g"
  fi
fi

[ -z "$MCP" ] && echo "❌ No MCP servers configured for this project"

# CLAUDE.md quality
echo -e "\n=== MEMORY FILE QUALITY ==="
if [ -f ./CLAUDE.md ]; then
  lines=$(wc -l < ./CLAUDE.md | tr -d " ")
  refs=$(grep -c "@" ./CLAUDE.md 2>/dev/null || echo 0)
  examples=$(grep -ci "example" ./CLAUDE.md 2>/dev/null || echo 0)
  echo "Lines: $lines"
  echo "@references: $refs"
  echo "Examples: $examples"
  [ $lines -gt 200 ] && echo "⚠️  Consider shortening (>200 lines)"
else
  echo "❌ No CLAUDE.md"
fi

# Single Source of Truth pattern
echo -e "\n=== SSOT PATTERN ==="
if [ -f ./CLAUDE.md ]; then
  grep -E "^@|/docs/|/conventions/" ./CLAUDE.md 2>/dev/null | head -5 || echo "❌ No @references found"
else
  echo "❌ No CLAUDE.md"
fi

# Documentation folders
echo -e "\n=== DOCUMENTATION ==="
for d in docs/ docs/conventions/ documentation/; do
  [ -d "$d" ] && echo "✅ $d exists"
done

# Privacy configuration
echo -e "\n=== PRIVACY CONFIGURATION ==="
if [ -f "./.claude/settings.json" ]; then
  if grep -q "\.env" ./.claude/settings.json 2>/dev/null; then
    echo "✅ .env excluded in settings"
  else
    echo "⚠️  .env NOT blocked in permissions.deny"
  fi
else
  echo "⚠️  No settings.json - .env files may be read"
fi

# Check for database MCP servers (privacy risk)
if command -v jq &> /dev/null && [ -f ~/.claude.json ]; then
  DB_MCP=$(jq -r --arg path "$CURRENT_DIR" ".projects[\$path].mcpServers // {} | keys[]" ~/.claude.json 2>/dev/null | grep -iE "postgres|neon|supabase|mysql|database" || true)
  if [ -n "$DB_MCP" ]; then
    echo "⚠️  Database MCP detected: $DB_MCP"
    echo "   → Ensure NOT connected to production data"
  fi
fi

echo "💡 Opt-out training: https://claude.ai/settings/data-privacy-controls"
'
```

**Store the output** for evaluation phase.

#### 1.3 Optional: Full Script

For a comprehensive JSON report, use the audit script from the repository:

```bash
# Download and run the official audit script
curl -sL https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/examples/scripts/audit-scan.sh | bash

# Or if you have the repo locally:
# ./examples/scripts/audit-scan.sh --json
```

### Phase 2: Evaluate & Report

**IMPORTANT**: Use the bash scan outputs from Phase 1 as your primary data source. Only read files when you need specific content examples or template generation.

#### 2.1 Evaluation Checklist

For each category, evaluate against these criteria based on Phase 1 scan results:

**Memory Files (Guide Section 3.1)**
- [ ] Global CLAUDE.md exists with personal preferences
- [ ] Project CLAUDE.md exists with team conventions
- [ ] Memory files are concise (not essays)
- [ ] Includes concrete examples
- [ ] References external docs instead of duplicating

**Single Source of Truth (Guide Section 3.1)**
- [ ] Conventions documented in `/docs/conventions/` or similar
- [ ] CLAUDE.md references these docs with `@path`
- [ ] Same conventions used across tools (CodeRabbit, SonarQube, etc.)

**Folder Structure (Guide Section 3.2)**
- [ ] `.claude/` folder properly organized
- [ ] Appropriate gitignore (settings.local.json, local CLAUDE.md)

**Context Management (Guide Section 2.2)**
- [ ] Awareness of context zones (green/yellow/red)
- [ ] Sanity markers strategy documented
- [ ] Context poisoning prevention considered

**Plan Mode Usage (Guide Section 2.3)**
- [ ] Plan mode mentioned for complex/risky tasks
- [ ] Auto Plan Mode configured if needed

**Agents (Guide Section 4)**
- [ ] Custom agents for repetitive specialized tasks
- [ ] Agents have clear descriptions (Tool SEO principle)
- [ ] Appropriate model selection per agent (haiku/sonnet/opus)

**Skills (Guide Section 5)**
- [ ] Reusable knowledge modules for complex domains
- [ ] Properly structured with frontmatter

**Commands (Guide Section 6)**
- [ ] Custom commands for frequent workflows
- [ ] Use $ARGUMENTS for flexibility

**Hooks (Guide Section 7)**
- [ ] Security hooks (PreToolUse) for sensitive operations
- [ ] Auto-formatting hooks (PostToolUse) if needed
- [ ] Context enrichment (UserPromptSubmit) if useful

**Privacy Configuration (Guide Section 2.6)**
- [ ] Training opt-out verified at claude.ai/settings
- [ ] `permissions.deny` blocks `.env*`, `credentials*`, `*.pem`
- [ ] MCP database servers NOT connected to production
- [ ] Team aware data is sent to Anthropic (5 years default, 30 days opt-out)

**MCP Servers (Guide Section 8)**
- [ ] Serena configured if large codebase (indexation + memory)
- [ ] Context7 configured if using external libraries
- [ ] Other relevant MCPs for the project needs

**Thinking Mode & Trinity (Guide Section 9.1)**
- [ ] Understanding of thinking mode (enabled by default in Opus 4.6, Alt+T to toggle)
- [ ] Trinity pattern documented for complex workflows

**CI/CD Integration (Guide Section 9.3)**
- [ ] Verify Gate pattern implemented (build → lint → test → typecheck)
- [ ] Autonomous retry loop considered

**Continuous Improvement (Guide Section 9.10)**
- [ ] Meta-rules for fixing system, not just code
- [ ] Learning from repeated issues

**Cost Awareness (Guide Section 2.2)**
- [ ] Understanding of pricing model (Sonnet/Opus/Haiku costs)
- [ ] Using /compact proactively to manage costs
- [ ] Being specific in queries to reduce token usage
- [ ] Tracking costs via Anthropic Console

**Migration Patterns (Guide Section 1.6)**
- [ ] Understanding differences vs Copilot/Cursor
- [ ] Hybrid workflow defined (when to use which tool)
- [ ] Successfully transitioned from previous AI tools

**Release Notes Automation (Guide Section 9.3)**
- [ ] Using Claude for changelog generation
- [ ] Automated release notes in CI/CD
- [ ] User-facing vs technical release notes

**Emergency Procedures (Guide Appendix A.10)**
- [ ] Hotfix checklist available for production issues
- [ ] Plan Mode usage during critical fixes
- [ ] Post-mortem process documented

**Git Archaeology (Guide Appendix A.11)**
- [ ] Using git blame/log for code understanding
- [ ] Finding domain experts via git history
- [ ] Understanding code evolution patterns

**Rules Templates (Guide Section 3.2)**
- [ ] `.claude/rules/` directory exists with auto-loaded rule files
- [ ] Rules cover relevant domains (architecture, code quality, testing)
- [ ] Rules are concise and actionable (not duplicating CLAUDE.md content)

**Sandbox & Permissions (Guide Section 1.4)**
- [ ] Understanding of sandbox modes (Docker container vs native process-level)
- [ ] Permission modes configured appropriately for the project
- [ ] Sensitive file patterns blocked via `permissions.deny` (`.env*`, `*.pem`, `credentials*`)

**Security Commands (Guide: security-hardening.md)**
- [ ] `/security-check` available for quick config scans (~30s)
- [ ] `/security-audit` available for comprehensive audits (2-5min, scored /100)
- [ ] Awareness of threat database (`threat-db.yaml`) for known attack patterns

**Plan-Validate-Execute Pipeline (Guide: workflows/plan-pipeline.md)**
- [ ] Awareness of pipeline workflow for complex features (power users)
- [ ] `/plan-start`, `/plan-validate`, `/plan-execute` commands installed if applicable
- [ ] ADR learning loop understood for accumulating architectural decisions

#### 2.2 Calculate Health Score

**Formula**: `Score = (earned_points / max_points) × 100`

| Priority | Points per ✅ | Weight Rationale |
|----------|--------------|------------------|
| 🔴 High | 3 points | Fundamentals, security, major productivity |
| 🟡 Medium | 2 points | Best practices, recommended patterns |
| 🟢 Low | 1 point | Polish, optimization, nice-to-have |

**Priority Assignment Rules**:
- 🔴 **High**: Missing CLAUDE.md (any), no security hooks, no permissions config, no context management awareness
- 🟡 **Medium**: No custom agents for repeated tasks, incomplete MCP setup, missing Single Source of Truth, no CI integration
- 🟢 **Low**: Tool SEO optimization, optional skills, advanced patterns like Trinity

#### 2.3 Generate Report

**Executive Summary** (5-10 lines):
- Health Score: X/100 (with color indicator)
- Top 3 Quick Wins (< 5 min each)
- Top 3 Important Gaps
- Detected tech stack

**Quick Wins Section**:
List 3-5 high-impact actions that take less than 5 minutes:
```
⚡ Quick Win 1: [action] → [impact]
⚡ Quick Win 2: [action] → [impact]
⚡ Quick Win 3: [action] → [impact]
```

**Findings Table** (4 columns):

| Priority | Element | Status | Action |
|----------|---------|--------|--------|
| 🔴 | ... | ❌/⚠️/✅ | ... |

**Detailed Findings** (expandable per item):
For each ❌ or ⚠️ item, provide:
```
### [Element Name]
**Current State**: [what exists or doesn't]
**Why It Matters**: [impact on workflow]
**Guide Reference**: [Section X.X](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md#section-anchor)
```

**Efficient Guide Reference Lookup**:
Instead of reading the entire guide, use these line ranges for targeted extraction:

```bash
# Line numbers from reference.yaml (deep_dive keys) — verify with:
# grep "memory_files\|hooks\|mcp_servers\|context_management\|plan_mode" machine-readable/reference.yaml

# Memory Files best practices (deep_dive: memory_files)
sed -n '3054,3254p' guide/ultimate-guide.md

# Hooks section (deep_dive: hooks)
sed -n '8300,8800p' guide/ultimate-guide.md

# MCP Servers section (deep_dive: mcp_servers)
sed -n '9500,10000p' guide/ultimate-guide.md

# Context Management (deep_dive: context_management)
sed -n '1000,1500p' guide/ultimate-guide.md

# Plan Mode (deep_dive: plan_mode)
sed -n '1500,1700p' guide/ultimate-guide.md
```

**Suggested Templates**:
For each High/Medium priority gap, provide a STACK-SPECIFIC template:
```
### Template: [Element Name]

**File**: `path/to/file`
**Stack**: [detected stack]

**Suggested content**:
\`\`\`
[template content customized for the detected tech stack]
\`\`\`
```

### Phase 3: Await Validation

**CRITICAL**: Do NOT create or modify any files without explicit approval.

After presenting the report, ask:

"Which of these suggestions would you like me to implement?

Options:
- `all` - Implement all templates
- `high` - Only 🔴 High priority items
- `1, 3, 5` - Specific items by number
- `none` - Just keep the report for reference

Please specify your choice:"

Wait for explicit user response before taking any action.

## Output Format

Structure your response exactly as:

1. **Executive Summary** (health score, quick wins, gaps, stack)
2. **Quick Wins** (3-5 immediate actions)
3. **Findings Table** (4-column overview)
4. **Detailed Findings** (expanded per item)
5. **Suggested Templates** (stack-specific, ready to use)
6. **Validation Request** (ask before implementing)
```

---

## 5. What to Expect

Here's an example of what the audit report looks like:

### Example Executive Summary

```
## Executive Summary

**Health Score**: 45/100 🟡

**Detected Stack**: TypeScript + Next.js + Prisma

**Quick Wins** (< 5 min each):
⚡ Create project CLAUDE.md → Immediate context for Claude
⚡ Add .claude/ to .gitignore patterns → Prevent accidental commits
⚡ Enable Context7 MCP → Better library documentation

**Top 3 Gaps**:
1. 🔴 No project CLAUDE.md - Claude lacks project context
2. 🔴 No security hooks - Sensitive operations unprotected
3. 🟡 No custom agents - Repetitive tasks done manually
```

### Example Findings Table

| Priority | Element | Status | Action |
|----------|---------|--------|--------|
| 🔴 High | Project CLAUDE.md | ❌ Missing | Create with stack conventions |
| 🔴 High | Security hooks | ❌ Missing | Add PreToolUse for secrets |
| 🟡 Medium | Custom agents | ❌ Missing | Create for code review, testing |
| 🟡 Medium | MCP Serena | ⚠️ Partial | Add memory configuration |
| 🟢 Low | Tool SEO | ⚠️ Partial | Improve agent descriptions |

---

## 6. Understanding Results

### Glossary

| Term | Definition |
|------|------------|
| **Memory Files** | CLAUDE.md files that provide persistent context to Claude across sessions |
| **Single Source of Truth** | Pattern where conventions are documented once and referenced everywhere |
| **Tool SEO** | Writing agent/command descriptions so Claude selects the right tool automatically |
| **MCP Servers** | Model Context Protocol - external tools that extend Claude's capabilities. Config stored in `~/.claude.json` per project, or `.claude/mcp.json` at project level |
| **Serena** | MCP server for codebase indexation and session memory persistence |
| **Context7** | MCP server for official library documentation lookup |
| **Hooks** | Scripts that run automatically on Claude events (PreToolUse, PostToolUse, etc.) |
| **PreToolUse** | Hook that runs BEFORE Claude executes a tool - great for security checks |
| **PostToolUse** | Hook that runs AFTER Claude executes a tool - great for formatting |
| **Plan Mode** | Read-only exploration mode for safe analysis before making changes |
| **Thinking Mode** | Extended thinking (Opus 4.6: ON by default). Toggle with Alt+T, configure in /config |
| **Trinity Pattern** | Combining Plan Mode + Extended Thinking + MCP for complex tasks |
| **Verify Gate** | CI/CD pattern: build → lint → test → typecheck before merge |
| **Context Zones** | < 70% optimal, 75% auto-compact trigger, 85% handoff recommended, 95% force handoff |
| **Data Retention** | Anthropic stores conversations: 5 years (default), 30 days (opt-out), 0 days (Enterprise ZDR) |
| **permissions.deny** | Settings to block Claude from reading sensitive files like `.env`, credentials |
| **Rules** | Auto-loaded `.claude/rules/*.md` files providing contextual instructions every session |
| **Permission Modes** | Trust levels for Claude's tool access: default deny, allowlist, or prompt-on-use |
| **Sandbox** | OS-level isolation (Docker container or native process-level). Toggle with `/sandbox` |
| **Plugins** | Community extensions installable via `/install-plugin owner/repo` |

### Priority Levels Explained

| Level | Meaning | Examples |
|-------|---------|----------|
| 🔴 **High** | Missing fundamentals, security risks, major productivity loss | No CLAUDE.md, no security hooks |
| 🟡 **Medium** | Recommended best practices, significant improvements | No agents, incomplete MCP |
| 🟢 **Low** | Nice-to-have optimizations, polish | Tool SEO, advanced patterns |

### Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Good - meets best practices |
| ⚠️ | Partial - exists but needs improvement |
| ❌ | Missing - doesn't exist or broken |

---

## 7. Common Issues

### "Claude didn't find my files"

**Cause**: Wrong working directory or platform path differences.

**Fix**:
- Ensure you run `claude` from your project root
- On Windows, paths use `%USERPROFILE%\.claude\` not `~/.claude/`

### "Health score seems wrong"

**Cause**: The weighted formula may not match your priorities.

**Fix**: Focus on the specific findings rather than the score. The score is indicative, not absolute.

### "Templates don't match my stack"

**Cause**: Stack detection failed or project uses uncommon setup.

**Fix**: Tell Claude your stack explicitly: "My project uses [X]. Regenerate templates for this stack."

### "Too many recommendations"

**Cause**: First-time audit on a project without Claude Code configuration.

**Fix**:
1. Start with Quick Wins only
2. Implement High priority items first
3. Add Medium/Low items incrementally

### "Claude made changes without asking"

**Cause**: This shouldn't happen if using the prompt correctly.

**Fix**:
- Ensure you copied the entire prompt including Phase 3
- Use Plan Mode (`Shift+Tab` twice) for extra safety
- Report this as a bug if it persists

---

## 8. Related Resources

- [The Ultimate Claude Code Guide](../guide/ultimate-guide.md) - Full reference
- [Architecture & Internals](../guide/core/architecture.md) - How Claude Code works
- [Cheatsheet](../guide/cheatsheet.md) - Quick daily reference
- [Claude Code Official Docs](https://docs.anthropic.com/en/docs/claude-code) - Anthropic documentation

---

*Last updated: March 2026 | Version 3.0 - Updated for guide v3.32.2 (Opus 4.6, new checklist categories, glossary, context zones)*
