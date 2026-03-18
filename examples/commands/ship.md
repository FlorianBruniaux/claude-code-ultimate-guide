---
name: ship
description: "Comprehensive pre-deployment verification to ensure release readiness"
---

# Ship Command - Pre-Deploy Checklist

Comprehensive pre-deployment verification to ensure release readiness.

## Purpose

Run before every production deployment to verify:
- Code quality gates
- Test coverage
- Security checks
- Documentation updates
- Environment readiness

## Pre-Deploy Checklist

### 🔴 Blockers (Must Pass)

```bash
# 1. All tests passing
npm test 2>/dev/null || pnpm test 2>/dev/null || yarn test 2>/dev/null
echo "Exit code: $?"

# 2. No TypeScript/lint errors
npm run typecheck 2>/dev/null || npx tsc --noEmit
npm run lint 2>/dev/null || npx eslint .

# 3. Build succeeds
npm run build 2>/dev/null || pnpm build 2>/dev/null

# 4. No secrets in code
grep -rn "API_KEY=\|SECRET=\|PASSWORD=" --include="*.{ts,js,json}" . 2>/dev/null | grep -v node_modules | grep -v ".env.example"
```

### 🟠 High Priority (Should Pass)

```bash
# 5. Security audit
npm audit --audit-level=high 2>/dev/null || echo "Run manually: npm audit"

# 6. No console.log in production code
grep -rn "console\.log\|console\.debug" --include="*.{ts,js,tsx,jsx}" src/ 2>/dev/null | grep -v "// allowed" | head -10

# 7. No TODO/FIXME in critical paths
grep -rn "TODO\|FIXME\|XXX\|HACK" --include="*.{ts,js}" src/ 2>/dev/null | head -10

# 8. Database migrations ready
[ -d "prisma/migrations" ] && echo "Prisma migrations: $(ls prisma/migrations | wc -l) total"
[ -d "migrations" ] && echo "Migrations: $(ls migrations | wc -l) total"
```

### 🟡 Recommended (Nice to Have)

```bash
# 9. Documentation updated
git diff --name-only HEAD~5 | grep -E "README|CHANGELOG|docs/" | head -10

# 10. Version bumped
cat package.json | jq -r '.version' 2>/dev/null || echo "Check version manually"

# 11. Environment variables documented
[ -f ".env.example" ] && echo "✅ .env.example exists" || echo "⚠️ Missing .env.example"
```

## Output Format

---

### 🚀 Ship Readiness Report

**Branch**: [current branch]
**Commit**: [HEAD short hash]
**Target**: [production/staging]
**Timestamp**: [date/time]

### Blockers (Must Fix Before Deploy)

| Check | Status | Details |
|-------|--------|---------|
| Tests | ✅/❌ | X passed, Y failed |
| TypeScript | ✅/❌ | X errors |
| Lint | ✅/❌ | X warnings, Y errors |
| Build | ✅/❌ | Success/Failed |
| Secrets | ✅/❌ | X potential leaks |

### High Priority

| Check | Status | Action |
|-------|--------|--------|
| Security Audit | ⚠️/✅ | X vulnerabilities |
| Console Logs | ⚠️/✅ | X found in src/ |
| TODOs | ⚠️/✅ | X critical TODOs |
| Migrations | ⚠️/✅ | X pending |

### Recommended

| Check | Status | Note |
|-------|--------|------|
| Docs Updated | ⚠️/✅ | CHANGELOG updated |
| Version Bumped | ⚠️/✅ | Current: X.Y.Z |
| Env Documented | ⚠️/✅ | .env.example present |

### 📊 Summary

```
🔴 Blockers:    X/5 passed
🟠 High:        X/4 passed
🟡 Recommended: X/3 passed
─────────────────────────
Overall:        [READY TO SHIP / NOT READY]
```

### 🎯 Action Items

1. [Most critical fix needed]
2. [Second priority]
3. [Third priority]

---

## Environment-Specific Checks

### Production Deploy

```bash
# Verify production env vars
[ -f ".env.production" ] && echo "Production env exists"

# Check for debug flags
grep -rn "DEBUG=true\|NODE_ENV=development" .env* 2>/dev/null

# Verify API endpoints point to production
grep -rn "localhost\|127\.0\.0\.1" --include="*.{ts,js,json}" src/ 2>/dev/null | grep -v test | head -5
```

### Staging Deploy

```bash
# Staging-specific checks
[ -f ".env.staging" ] && echo "Staging env exists"

# Feature flags for staging
grep -rn "FEATURE_FLAG\|ENABLE_" .env* 2>/dev/null
```

## CI/CD Integration

Add to your pipeline:

```yaml
# GitHub Actions example
ship-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run ship checklist
      run: |
        npm ci
        npm test
        npm run typecheck
        npm run lint
        npm run build
        npm audit --audit-level=high
```

## Post-Deploy Verification

After deployment, verify:

```bash
# 1. Health check
curl -s https://your-app.com/health | jq .

# 2. Version check
curl -s https://your-app.com/version | jq .

# 3. Smoke tests
npm run test:smoke 2>/dev/null || echo "Run smoke tests manually"
```

## Rollback Preparation

Before shipping, ensure you can rollback:

```bash
# Note current production tag
git describe --tags --abbrev=0

# Verify rollback procedure exists
[ -f "docs/runbooks/rollback.md" ] && echo "✅ Rollback docs exist"

# Check database migration reversibility
# Prisma: prisma migrate diff
# Rails: rails db:rollback (dry-run)
```

## Usage

**Full checklist:**
```
/ship
```

**Production deploy:**
```
/ship --production
```

**Quick check (blockers only):**
```
/ship --quick
```

**With specific target:**
```
/ship --target=staging
```

## Tips

1. **Run early, run often**: Don't wait until deploy day
2. **Automate in CI**: Make blockers fail the pipeline
3. **Team agreement**: Define what's a blocker vs warning
4. **Document exceptions**: If skipping a check, note why
5. **Monitor after deploy**: Ship is not done until monitoring confirms success

## Related Commands

- `/release-notes` - Generate changelog and announcements
- `/validate-changes` - LLM-based code review
- `/security` - Deep security audit

$ARGUMENTS
