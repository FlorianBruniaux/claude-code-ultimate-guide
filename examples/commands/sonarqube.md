---
name: sonarqube
description: "Analyze SonarCloud quality issues for a specific PR"
---

# SonarQube Analysis

Analyze SonarCloud quality issues for a specific PR. Generates comprehensive report with metrics, top violators, and action plan.

**Core principle:** Analysis-only = no code changes, pure insight.

## Process

1. **Verify Token**: Check `$SONARQUBE_TOKEN` environment variable
2. **Fetch Issues**: Call SonarCloud API for PR issues
3. **Parse Data**: Group by severity, type, file, rule
4. **Generate Report**: Structured output with action plan
5. **Cleanup**: Remove temporary files

## Prerequisites

### Environment Variable

```bash
# Set SonarQube token (add to ~/.bashrc or ~/.zshrc)
export SONARQUBE_TOKEN="your_token_here"

# Verify token is set
echo $SONARQUBE_TOKEN
```

**To get token:**
1. Go to SonarCloud → My Account → Security
2. Generate new token
3. Copy and export as environment variable

### Project Configuration

Configure your SonarCloud project details:

```bash
# Add to project's CLAUDE.md or as environment variables
SONAR_ORGANIZATION="your-org-name"
SONAR_PROJECT_KEY="your-org_your-project"
SONAR_BASE_URL="https://sonarcloud.io/api"
```

**If not set:** Ask user to provide organization and project key.

## Fetch Issues

**Important:** Direct curl with `-u "$SONARQUBE_TOKEN:"` fails in zsh due to authentication parsing. Use bash script wrapper:

```bash
# Create temporary bash script to handle authentication
cat > /tmp/fetch_sonar.sh << 'SCRIPT'
#!/bin/bash
curl -s -u "${SONARQUBE_TOKEN}:" \
  "https://sonarcloud.io/api/issues/search?componentKeys=${SONAR_PROJECT_KEY}&pullRequest=$1&issueStatuses=OPEN,CONFIRMED&sinceLeakPeriod=true&ps=500"
SCRIPT

chmod +x /tmp/fetch_sonar.sh
/tmp/fetch_sonar.sh $PR_NUMBER > /tmp/sonar_pr_$PR_NUMBER.json
```

**API Parameters:**
- `componentKeys`: Your project key
- `pullRequest`: PR number
- `issueStatuses`: OPEN,CONFIRMED (exclude resolved)
- `sinceLeakPeriod`: Only new issues in this PR
- `ps`: Page size (max 500)

## Analysis Script

Create Node.js analysis script at `/tmp/sonar_analyze.js`:

```javascript
const fs = require('fs');
const prNumber = process.argv[2];
const data = JSON.parse(fs.readFileSync(`/tmp/sonar_pr_${prNumber}.json`, 'utf8'));
const issues = data.issues || [];

// Group by severity
const bySeverity = issues.reduce((acc, i) => {
  acc[i.severity] = (acc[i.severity] || 0) + 1;
  return acc;
}, {});

// Group by type
const byType = issues.reduce((acc, i) => {
  acc[i.type] = (acc[i.type] || 0) + 1;
  return acc;
}, {});

// Group by file
const byFile = issues.reduce((acc, i) => {
  const file = i.component.split(':')[1] || i.component;
  acc[file] = (acc[file] || 0) + 1;
  return acc;
}, {});

// Group by rule
const byRule = issues.reduce((acc, i) => {
  if (!acc[i.rule]) {
    acc[i.rule] = {
      count: 0,
      severity: i.severity,
      message: i.message
    };
  }
  acc[i.rule].count++;
  return acc;
}, {});

// Output structured data
console.log(JSON.stringify({
  total: data.total,
  bySeverity,
  byType,
  topFiles: Object.entries(byFile)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10),
  topRules: Object.entries(byRule)
    .map(([rule, d]) => ({ rule, ...d }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}, null, 2));
```

**Run analysis:**
```bash
node /tmp/sonar_analyze.js $PR_NUMBER > /tmp/sonar_analysis_$PR_NUMBER.json
```

## Report Format

Generate formatted report from analysis:

```
📊 SonarCloud Analysis - PR #XXX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Issues: {TOTAL}

By Severity:
🔴 Blocker/Critical: {COUNT} ({PERCENTAGE}%)
🟡 Major: {COUNT} ({PERCENTAGE}%)
🔵 Minor/Info: {COUNT} ({PERCENTAGE}%)

By Type:
🐛 Bugs: {COUNT}
🛡️ Vulnerabilities: {COUNT}
🧹 Code Smells: {COUNT}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 TOP 10 FILES WITH ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. src/components/UserProfile.tsx - 8 issues
2. src/services/auth.service.ts - 5 issues
3. src/utils/validation.ts - 4 issues
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ TOP 5 VIOLATED RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. typescript:S1854 (MAJOR) - 12 occurrences
   "Dead stores should be removed"

2. typescript:S3776 (CRITICAL) - 8 occurrences
   "Cognitive Complexity of functions should not be too high"

3. typescript:S1186 (MINOR) - 6 occurrences
   "Functions should not be empty"
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ACTION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 1 - CRITICAL/BLOCKER ({COUNT} issues):
  • Fix immediately before merge
  • Focus on: {TOP_FILES}

Priority 2 - MAJOR ({COUNT} issues):
  • Address in this PR if possible
  • Consider technical debt ticket if extensive

Priority 3 - MINOR/INFO ({COUNT} issues):
  • Can be addressed in follow-up PR
  • Add to backlog for refactoring sprint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 LINKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View in SonarCloud:
https://sonarcloud.io/project/pull_requests_list?id={PROJECT_KEY}&pullRequest={PR_NUMBER}
```

## Severity Mapping

| SonarCloud | Symbol | Priority | Action |
|------------|--------|----------|--------|
| BLOCKER | 🔴 | P0 | Fix immediately |
| CRITICAL | 🔴 | P0 | Fix immediately |
| MAJOR | 🟡 | P1 | Fix in this PR |
| MINOR | 🔵 | P2 | Consider for follow-up |
| INFO | 🔵 | P3 | Optional improvement |

## Issue Types

| Type | Symbol | Description |
|------|--------|-------------|
| BUG | 🐛 | Code that is demonstrably wrong |
| VULNERABILITY | 🛡️ | Security issues |
| CODE_SMELL | 🧹 | Maintainability issue |
| SECURITY_HOTSPOT | 🔒 | Security-sensitive code to review |

## Cleanup

Always clean up temporary files after execution:

```bash
rm -f /tmp/fetch_sonar.sh
rm -f /tmp/sonar_pr_$PR_NUMBER.json
rm -f /tmp/sonar_analyze.js
rm -f /tmp/sonar_analysis_$PR_NUMBER.json
```

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Token not set | `$SONARQUBE_TOKEN` missing | Ask user to export token |
| 401 Unauthorized | Invalid or expired token | Request new token from SonarCloud |
| 404 Not Found | PR doesn't exist in SonarCloud | Verify PR number and project key |
| Empty response | No issues found | Report clean PR, congratulate team |
| >500 issues | Pagination limit reached | Warn about incomplete data, suggest filtering |
| Network error | API unreachable | Check internet connection, retry |

## Configuration Options

### Project-Level Configuration

Create `.sonarcloud.properties` or add to `CLAUDE.md`:

```properties
# SonarCloud Configuration
SONAR_ORGANIZATION=your-org
SONAR_PROJECT_KEY=your-org_your-project
SONAR_EXCLUSIONS=**/*.test.ts,**/*.spec.ts,**/migrations/**
SONAR_COVERAGE_EXCLUSIONS=**/*.test.ts,src/test/**
```

### API Rate Limits

SonarCloud API limits:
- Free tier: 10,000 requests/day
- Paid tier: Unlimited

**Tip:** Cache results for repeated queries to same PR.

## Integration Examples

### GitHub Actions

```yaml
- name: SonarQube Analysis
  run: |
    export SONARQUBE_TOKEN=${{ secrets.SONAR_TOKEN }}
    export SONAR_PROJECT_KEY="${{ secrets.SONAR_PROJECT }}"
    claude -p "/sonarqube ${{ github.event.pull_request.number }}"
```

### Pre-merge Hook

Add to `.claude/hooks/pre-merge.sh`:

```bash
#!/bin/bash
PR_NUMBER=$(gh pr view --json number -q .number)
claude -p "/sonarqube $PR_NUMBER"
```

## Red Flags - NEVER Do

**Never:**
- ❌ Modify code or auto-fix issues (analysis-only command)
- ❌ Skip token verification (security risk)
- ❌ Leave temp files in `/tmp` (cleanup required)
- ❌ Commit SonarQube token to repository (use env vars)
- ❌ Run without checking token expiration

**Always:**
- ✅ Generate structured, actionable report
- ✅ Clean up after execution
- ✅ Handle API errors gracefully
- ✅ Verify token is valid before API calls
- ✅ Parse and present data clearly

## Advanced Usage

### Custom Filters

```bash
# Only show critical/blocker issues
/sonarqube 123 --severity BLOCKER,CRITICAL

# Only show bugs and vulnerabilities
/sonarqube 123 --types BUG,VULNERABILITY

# Specific file pattern
/sonarqube 123 --files "src/services/**"
```

### Multiple PRs

```bash
# Compare issues across PRs
/sonarqube 123,124,125 --compare
```

## Troubleshooting

### Issue: "curl: (22) The requested URL returned error: 401"

**Cause:** Invalid or missing token

**Fix:**
```bash
# Regenerate token in SonarCloud
# Export new token
export SONARQUBE_TOKEN="new_token_here"
```

### Issue: "Empty response or no issues"

**Cause:** Analysis not yet complete or PR not analyzed

**Fix:** Wait for SonarCloud analysis to complete (~2-5 minutes after PR creation)

### Issue: "componentKeys not found"

**Cause:** Wrong project key

**Fix:** Verify project key in SonarCloud URL:
```
https://sonarcloud.io/project/overview?id=YOUR_PROJECT_KEY
```

## Usage Examples

```bash
# Basic usage
/sonarqube 170

# With PR prefix
/sonarqube PR #234

# Using PR URL
/sonarqube https://github.com/org/repo/pull/170

# Custom severity filter (if implemented)
/sonarqube 170 --critical-only
```

PR Number: $ARGUMENTS
