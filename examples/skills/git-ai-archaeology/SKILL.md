---
name: git-ai-archaeology
description: "Analyze AI config evolution in a git repo. Use when mapping AI adoption history, finding when configs were first introduced, charting commit velocity by month, or identifying maturity phases in a project's AI tooling."
allowed-tools: Write Read Bash
effort: medium
---

# git-ai-archaeology

Produces a complete analysis of AI config evolution in a git repository. Finds when each AI configuration file was created, how AI-config commit velocity evolved month by month, which PRs structured the evolution, and identifies maturity phases.

**Output**: a single file `{output_dir}/{slug}-git-archaeology.md`

## Expected input

```
/git-ai-archaeology repo_path=/path/to/repo [output=./talks/slug] [slug=talk-name] [since=2025-01-01]
```

- `repo_path`: absolute path to the target git repo (required)
- `output`: output directory (default: `./talks`)
- `slug`: output filename (default: repo folder name)
- `since`: analysis start date (default: first repo commit)

## Workflow

1. **Verify the repo**: ensure the path exists and is a git repo
2. **Global metrics**: total commits, releases, contributors, time period
3. **Section 1: First commits**: find creation date for key AI-config paths
4. **Section 2: Monthly distribution**: commits filtered by AI-config keywords
5. **Section 3: Major PRs**: extract and categorize significant AI-config commits
6. **Section 4: CHANGELOG**: if CHANGELOG.md exists, extract releases with AI mentions
7. **Section 5: Phases**: synthesize evolution phases
8. **Save** the output file

---

## Step 1: Verification and global metrics

```bash
# Verify it's a git repo
git -C {repo_path} rev-parse --git-dir

# Global metrics
git -C {repo_path} log --oneline | wc -l                                    # total commits
git -C {repo_path} tag --sort=version:refname | wc -l                       # total releases
git -C {repo_path} shortlog -sn --no-merges | wc -l                         # contributors
git -C {repo_path} log --pretty=format:"%ad" --date=short | tail -1         # first commit
git -C {repo_path} log --pretty=format:"%ad" --date=short | head -1         # last commit
git -C {repo_path} log --merges --oneline | wc -l                           # merged PRs
```

---

## Step 2: Section 1: First commits per AI-config path

For each path, find the origin commit with `--diff-filter=A`:

```bash
# Paths to analyze, adapt based on what exists in the repo
PATHS=(
  "CLAUDE.md"
  ".claude"
  ".claude/commands"
  ".claude/agents"
  ".claude/hooks"
  ".claude/skills"
  ".claude/rules"
  ".agents"
  ".cursor"
  "doc/knowledge-base.md"
  "doc/guides/ai-instructions"
  "doc/guides/ai-review"
)

for path in "${PATHS[@]}"; do
  git -C {repo_path} log --diff-filter=A --follow \
    --format="%ad | %H | %s" --date=short \
    -- "$path" | tail -1
done
```

Build the Section 1 table from results. Skip paths with no output (don't exist in this repo).

Also build the ASCII timeline:
```
{date} --- {path} --- {message}
```
Sorted chronologically.

---

## Step 3: Section 2: Monthly distribution of AI-config commits

Filter commits by AI-config-related keywords:

```bash
# All commits with AI-config keywords
git -C {repo_path} log --format="%H %s" | \
  grep -iE "(claude|feat.ai|docs.ai|tech.ai|mcp|skill|hook|agent|llm|prompt)" \
  > /tmp/ai_commits_filtered.txt

# Count AI-config commits per month
git -C {repo_path} log --format="%ad %H" --date=format:"%Y-%m" | \
  while read month hash; do
    if grep -q "$hash" /tmp/ai_commits_filtered.txt; then
      echo "$month"
    fi
  done | sort | uniq -c
```

More direct alternative:

```bash
git -C {repo_path} log --format="%ad %s" --date=format:"%Y-%m" | \
  grep -iE " (feat|fix|docs|tech|chore|refactor)\(ai\)|claude|mcp.*server|\.claude/|skill|hook.*security|guardrail" | \
  awk '{print $1}' | sort | uniq -c
```

Compute per month:
- AI-config commit count
- % of monthly total (cross-reference with all-category monthly total)
- Context (if notable period)

Build ASCII distribution chart (horizontal or vertical bars).

---

## Step 4: Section 3: Major PRs and commits

### 3.1: feat(ai): / docs(ai): / tech(ai): commits

```bash
git -C {repo_path} log --format="%ad | %H | %s" --date=short | \
  grep -iE "\(ai\)|\(mcp\)|\[ai\]"
```

### 3.2: MCP Server integrations

```bash
git -C {repo_path} log --format="%ad | %H | %s" --date=short | \
  grep -iE "mcp|serena|grepai|perplexity|sonar|postgres.*mcp|cursor.*mcp"
```

### 3.3: Skills, commands, hooks, agents

```bash
git -C {repo_path} log --format="%ad | %H | %s" --date=short | \
  grep -iE "feat\(skill|feat\(hook|feat\(agent|feat\(command|feat\(dx\)|feat\(ci\)" | \
  grep -v "^$"
```

### 3.4: Code review automation

```bash
git -C {repo_path} log --format="%ad | %H | %s" --date=short | \
  grep -iE "review|code-review|pr.*auto|ci.*review"
```

---

## Step 5: Section 4: CHANGELOG Analysis (if available)

```bash
# Check if CHANGELOG.md exists
ls {repo_path}/CHANGELOG.md

# Extract releases with AI mentions
grep -n "## \[" {repo_path}/CHANGELOG.md | head -30
```

Read the CHANGELOG and build a table:

| Release | Date | AI-Related Content |
|---------|------|-------------------|

Only list releases with AI-config content (CLAUDE.md, MCP, agents, skills, hooks, guardrails, prompts, etc.).

---

## Step 6: Section 5: Evolution phases

Analyze collected data and identify maturity phases. Typical pattern:

| Phase | Characteristics | Commits | Label |
|-------|-----------------|---------|-------|
| **Phase 1** | Basic config, solo usage, no structure | Low | "Config as Afterthought" |
| **Phase 2** | Documentation, knowledge base, first MCP | Growing | "Config as Documentation" |
| **Phase 3** | Infrastructure: skills/hooks/rules/MCP stack | Spike | "Config as Infrastructure" |
| **Phase 4** | Engineering: tests, CI, guardrails, modules | Dense | "Config as Engineering Practice" |

Adapt phases to what the data actually reveals.

Identify the **main inflection point**: the month where AI-config commit volume spiked.

Compute the "recent vs historical" ratio (e.g., "81% of AI-config commits in the last 2 months").

---

## Output format: {slug}-git-archaeology.md

```markdown
# Git Archaeology: AI Config Evolution: {slug}

**Source**: Git history of repo `{repo_path}` ({total_commits}+ commits, {total_releases}+ releases)
**Method**: `git log --diff-filter=A` for first commits, filtered monthly distribution, major PRs
**Last updated**: {date}

---

## Section 1: First Commit per Key Path

| Path | Creation Date | Commit Message | Hash |
|------|--------------|----------------|------|
{rows}

### Creation Timeline

\```
{ascii_timeline}
\```

---

## Section 2: Monthly Distribution of AI-Config Commits

| Month | AI-Config Commits | % of Total | Context |
|-------|-------------------|-----------|---------|
{rows}

### Visualization

\```
{ascii_chart}
\```

**Inflection**: {insight on the commit spike}

---

## Section 3: Major PRs and Commits Related to AI Tooling

### 3.1 PRs `feat(ai):` / `tech(ai):` / `docs(ai):`

| Date | Hash | Message | Impact |
|------|------|---------|--------|
{rows}

### 3.2 MCP Server Integrations (chronological)

| Date | MCP Server | Hash / PR | Role |
|------|------------|-----------|------|
{rows}

### 3.3 Skills, Commands, Hooks, Agents

| Date | Hash | Message | Category |
|------|------|---------|----------|
{rows}

### 3.4 Code Review Automation

| Date | Hash | Message |
|------|------|---------|
{rows}

---

## Section 4: CHANGELOG AI Mentions by Release

{section if CHANGELOG available, otherwise "Not applicable"}

---

## Section 5: Evolution Phases

### Evidence-Based Timeline

| Milestone | Exact Git Date | Git Evidence |
|-----------|----------------|-------------|
{rows}

### {N} Evolution Phases

#### Phase 1: {Label} ({period}), {n} commits
{description}

#### Phase 2: {Label} ({period}), {n} commits
{description}

#### Phase 3: {Label} ({period}), {n} commits
{description}

#### Phase 4: {Label} ({period}), {n} commits
{description}

### Key Insight

{Summary paragraph: main inflection point, recent/historical ratio, what the data reveals about the project's AI maturity.}

---
*Generated by git-ai-archaeology, {date}*
*Repo: {repo_path} | {total_commits} commits | {total_releases} releases*
```

---

## Important rules

- **Read-only**: no git commands that modify repo state
- **Verify before asserting**: a date not found in git = note "unverified"
- **Adapt paths**: Section 1 paths must be filtered to what actually exists in this repo
- **Extensible keywords**: if the repo uses different conventions (e.g., `feat[ai]` vs `feat(ai)`), adapt grep patterns
- **Section 4 optional**: if no CHANGELOG.md or no AI mentions, note "Not applicable" and skip to Section 5
- **Adaptive phases**: 4 phases is a common pattern, not a rule; 2 phases or 6 phases are equally valid

## Anti-patterns

- Inventing data not found in git
- Rounding numbers without flagging it
- Analyzing paths that don't exist in this repo
- Confusing a rename commit with a creation
- Omitting "flat" months (0 AI-config commits also tells a story)

## Validation checklist

- [ ] Repo verified and readable
- [ ] Section 1: only paths that exist in this repo
- [ ] Section 2: distribution covers the full repo period
- [ ] Section 3: commits sorted chronologically, hash included
- [ ] Section 4: cleanly skipped if no CHANGELOG
- [ ] Section 5: phases based on data, not the template
- [ ] Output file saved
