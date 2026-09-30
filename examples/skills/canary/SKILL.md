---
name: canary
description: "Post-deploy monitoring: watch production after a deploy and alert on regressions"
argument-hint: "[--baseline]"
effort: medium
disable-model-invocation: true
---

# Canary: Post-Deploy monitoring

Watch a live application after deployment. Alert on errors and regressions. Compare against a pre-deploy baseline.

**Two modes:**
- `--baseline`: capture the current state BEFORE deploying
- *(default)*: monitor AFTER deploying and compare against baseline

## Instructions

### Phase 1: Setup

Parse the user's arguments and detect the deployment context.

```bash
# Detect current branch and recent deploy commit
git branch --show-current
git log --oneline -5

# Auto-detect platform from config files
[ -f fly.toml ]         && echo "PLATFORM: fly"
[ -f render.yaml ]      && echo "PLATFORM: render"
[ -f vercel.json ]      && echo "PLATFORM: vercel"
[ -f netlify.toml ]     && echo "PLATFORM: netlify"
[ -f Procfile ]         && echo "PLATFORM: heroku"
[ -f railway.toml ]     && echo "PLATFORM: railway"

# Check for health endpoint
curl -sf "${URL}/health" -w "\n%{http_code}" 2>/dev/null | tail -1
curl -sf "${URL}/api/health" -w "\n%{http_code}" 2>/dev/null | tail -1
```

Create the working directory:

```bash
mkdir -p .canary/baselines .canary/reports .canary/screenshots
```

---

### Phase 2: Baseline Capture (`--baseline` mode)

Run this BEFORE deploying to capture the current healthy state.

For each page to monitor, record:

1. **HTTP status**: is the page returning 200?
2. **Response time**: how long does it take to load?
3. **Content snapshot**: key text content to detect blank pages later

```bash
# For each page URL
for PAGE_PATH in "/" "/dashboard" "/settings" "/api/health"; do
  SLUG=$(echo "$PAGE_PATH" | tr '/' '_' | tr -d '?&=')
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" "${BASE_URL}${PAGE_PATH}" 2>/dev/null)
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')
  echo "  ${PAGE_PATH}: HTTP ${STATUS}, ${TIME_MS}ms"
done
```

Save baseline to `.canary/baselines/baseline.json`:

```json
{
  "url": "<base-url>",
  "timestamp": "<ISO-8601>",
  "branch": "<branch-name>",
  "commit": "<git-SHA>",
  "pages": {
    "/": { "status": 200, "time_ms": 450 },
    "/dashboard": { "status": 200, "time_ms": 680 },
    "/api/health": { "status": 200, "time_ms": 45 }
  }
}
```

Then **STOP** and tell the user: "Baseline captured. Deploy your changes, then run `/canary <url>` to monitor."

---

### Phase 3: Page discovery

If no pages were specified, auto-discover pages to monitor.

**From the application:**

```bash
# Check sitemap if available
curl -sf "${URL}/sitemap.xml" 2>/dev/null | grep -oP '(?<=<loc>)[^<]+' | head -10

# Check robots.txt for known paths
curl -sf "${URL}/robots.txt" 2>/dev/null | grep -i "allow\|disallow" | head -10

# Common paths to always check
echo "Always check: / /login /dashboard /settings /api/health"
```

Default pages to monitor if nothing found: `/`, and the homepage only.

---

### Phase 4: Monitoring loop

Monitor for the specified duration (default: 10 minutes). Run a check every 60 seconds.

**Each check cycle:**

```bash
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CHECK_NUM=$((CHECK_NUM + 1))

for PAGE_PATH in "${PAGES[@]}"; do
  # Check HTTP status and response time
  RESULT=$(curl -sf -o /dev/null -w "%{http_code}|%{time_total}" \
    --max-time 10 "${BASE_URL}${PAGE_PATH}" 2>/dev/null || echo "0|0")
  STATUS=$(echo "$RESULT" | cut -d'|' -f1)
  TIME_MS=$(echo "$RESULT" | awk -F'|' '{printf "%.0f", $2 * 1000}')

  # Compare against baseline
  BASELINE_STATUS=$(jq -r ".pages[\"${PAGE_PATH}\"].status // 200" .canary/baselines/baseline.json 2>/dev/null)
  BASELINE_TIME=$(jq -r ".pages[\"${PAGE_PATH}\"].time_ms // 1000" .canary/baselines/baseline.json 2>/dev/null)

  echo "  [Check #${CHECK_NUM}] ${PAGE_PATH}: HTTP ${STATUS} (${TIME_MS}ms)"
done
```

**Alert levels:**

| Level | Condition | Trigger |
|-------|-----------|---------|
| **CRITICAL** | Page load failure | HTTP status is not 2xx, curl timeout, DNS failure |
| **HIGH** | New errors | Error rate increased vs baseline (console errors, 5xx responses) |
| **MEDIUM** | Performance regression | Response time exceeds 2x baseline |
| **LOW** | New broken links | Previously-working routes now return 404 |

**Key principles:**
- **Alert on changes, not absolutes.** A page with 3 errors in baseline is fine if still 3. One NEW error is an alert.
- **Transient tolerance.** Only alert on patterns persisting across 2+ consecutive checks. A single network blip is not an alert.

**When a CRITICAL or HIGH alert fires (2 consecutive checks):**

```
CANARY ALERT
=====================================
Time:     [check #N at Xs elapsed]
Page:     [URL]
Level:    [CRITICAL / HIGH / MEDIUM / LOW]
Finding:  [what changed, be specific]
Baseline: [baseline value]
Current:  [current value]
=====================================
Options:
  A) Investigate now: stop monitoring, focus on this issue
  B) Continue monitoring: wait for next check to confirm
  C) Rollback: revert the deploy
  D) Dismiss: known issue, continue monitoring
```

---

### Phase 5: Health report

After monitoring completes (or user stops), produce a summary.

```
CANARY REPORT: [url]
=========================================
Duration:    [X minutes]
Checks:      [N total per page]
Pages:       [N pages monitored]
Commit:      [deployed SHA]
Status:      [HEALTHY / DEGRADED / BROKEN]

Per-Page Results:
-----------------------------------------
  Page           Status      Avg Time   Alerts
  /              HEALTHY     450ms      0
  /dashboard     DEGRADED    1100ms     1 medium (was 450ms)
  /settings      HEALTHY     380ms      0
  /api/health    HEALTHY     45ms       0

Alerts Fired: [N] (X critical, Y high, Z medium, W low)

VERDICT: [DEPLOY HEALTHY / DEPLOY HAS ISSUES (see alerts above)]
=========================================
```

Save report to `.canary/reports/<date>-canary.md`.

---

### Phase 6: Baseline update

If the deploy is healthy and the user wants to update the baseline:

```bash
cp .canary/reports/latest-snapshot.json .canary/baselines/baseline.json
echo "Baseline updated to commit $(git rev-parse --short HEAD)"
```

---

## Output format

See Phase 5 above for the full CANARY REPORT template.

Inline alert format (during monitoring):
```
[08:42:15] Check #3: /dashboard: ALERT HIGH, response time 1250ms (baseline: 420ms)
[08:43:15] Check #4: /dashboard: ALERT HIGH, response time 1180ms (baseline: 420ms)
-> Consistent across 2 checks. Firing alert.
```

## Usage

```
/canary https://app.example.com                # Monitor homepage for 10 min
/canary https://app.example.com --baseline     # Capture baseline before deploying
/canary https://app.example.com --duration 5m  # Monitor for 5 minutes
/canary https://app.example.com --quick        # Single-pass health check (no loop)
/canary https://app.example.com --pages /,/dashboard,/api/health
```

## Tips

1. **Always capture a baseline** before deploying to production: run `/canary <url> --baseline`
2. **Start monitoring immediately** after deploy; the first 5 minutes catch 90% of regressions
3. **CRITICAL alerts** require immediate investigation; don't wait for the monitoring to finish
4. **MEDIUM alerts (performance)** may be cache warming; give it 2-3 more checks before acting
5. **Keep `.canary/baselines/` in git** so any team member can run canary against the same baseline

## Related commands

- `/ship`: pre-deploy checklist (run before deploying)
- `/land-and-deploy`: full merge-to-verify pipeline (runs canary automatically)
- `/qa`: interactive QA testing before shipping

$ARGUMENTS
