---
name: ci-pipeline
description: Push current branch and return the pipeline tracking URL (GitLab or GitHub Actions)
allowed-tools: [Bash]
model: haiku
effort: low
disable-model-invocation: true
---

# /ci-pipeline: Push and trigger pipeline

Pushes the current branch and returns the pipeline tracking link. Never force-push: this skill takes no flags.

## Process

```bash
BRANCH=$(git branch --show-current)

# 1. Safety checks
if echo "$BRANCH" | grep -qE "^(main|master|production)$"; then
  echo "❌ Direct push to $BRANCH is not allowed. Create a feature/fix branch."
  exit 1
fi

# 2. Check for uncommitted changes
UNCOMMITTED=$(git status --porcelain | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "⚠️  $UNCOMMITTED uncommitted file(s):"
  git status --short
  echo ""
  echo "Commit first with /commit or git add + git commit"
  exit 0
fi

# 3. Push
echo "Pushing → origin/$BRANCH"
git push origin "$BRANCH" 2>&1
```

## Pipeline URL

### GitLab CI

```bash
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
WEB_URL=$(echo "$REMOTE" | sed 's/git@gitlab\.com:/https:\/\/gitlab.com\//' | sed 's/\.git$//')
echo ""
echo "✅ Push OK"
echo "   Pipeline: $WEB_URL/-/pipelines?ref=$BRANCH"

# Live status via glab (if installed)
if command -v glab &>/dev/null; then
  sleep 3
  glab ci status --branch "$BRANCH" 2>/dev/null || true
fi
```

### GitHub Actions

```bash
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
WEB_URL=$(echo "$REMOTE" | sed 's/git@github\.com:/https:\/\/github.com\//' | sed 's/\.git$//')
echo ""
echo "✅ Push OK"
echo "   Actions: $WEB_URL/actions?query=branch%3A$BRANCH"

# Live status via gh (if installed)
if command -v gh &>/dev/null; then
  sleep 5
  gh run list --branch "$BRANCH" --limit 3 2>/dev/null || true
fi
```

## Expected output

```
Pushing → origin/feat/add-payment-retry

Enumerating objects: 12, done.
...

✅ Push OK
   Pipeline: https://gitlab.com/org/my-app/-/pipelines?ref=feat/add-payment-retry

Pipeline status (after 3s):
  ⏳ lint       running
  ⏸️  test       waiting
  ⏸️  deploy     waiting
```

## Usage

```
/ci-pipeline
```
