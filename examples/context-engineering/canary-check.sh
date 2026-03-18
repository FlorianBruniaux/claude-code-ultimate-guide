#!/bin/bash
# Context Engineering Canary Check
#
# Runs structural validation tests against your CLAUDE.md configuration.
# Catches common drift issues: missing files, broken imports, bloated size, conflicting rules.
#
# Usage:
#   ./canary-check.sh                   # Check current directory
#   ./canary-check.sh /path/to/project  # Check specific project
#
# Exit codes:
#   0 — all checks passed
#   N — number of issues found
#
# Run this weekly, or add it to your pre-commit hook for critical projects.

set -euo pipefail

PROJECT_DIR="${1:-.}"
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"  # Resolve to absolute path

PASS=0
FAIL=0
WARN=0
RESULTS=()

# ── Result tracking ───────────────────────────────────────────────────────────

log_pass() {
  local test="$1"
  local detail="${2:-}"
  RESULTS+=("PASS  $test${detail:+: $detail}")
  PASS=$((PASS + 1))
}

log_fail() {
  local test="$1"
  local detail="${2:-}"
  RESULTS+=("FAIL  $test${detail:+: $detail}")
  FAIL=$((FAIL + 1))
}

log_warn() {
  local test="$1"
  local detail="${2:-}"
  RESULTS+=("WARN  $test${detail:+: $detail}")
  WARN=$((WARN + 1))
}

# ── Check 1: CLAUDE.md exists and is non-trivial ──────────────────────────────

check_claude_md_exists() {
  local file="$PROJECT_DIR/CLAUDE.md"
  if [ ! -f "$file" ]; then
    log_fail "CLAUDE.md exists" "Not found at $file"
    return 1
  fi
  log_pass "CLAUDE.md exists" "$file"
  return 0
}

check_claude_md_size() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local lines
  lines=$(wc -l < "$file" | tr -d ' ')

  if [ "$lines" -lt 10 ]; then
    log_fail "CLAUDE.md has content" "Only $lines lines — too sparse to be useful"
  elif [ "$lines" -gt 500 ]; then
    log_warn "CLAUDE.md size" "$lines lines exceeds 500 — consider modularizing with @imports"
  else
    log_pass "CLAUDE.md size" "$lines lines (healthy: 10-500)"
  fi
}

# ── Check 2: Broken @imports ──────────────────────────────────────────────────

check_imports() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local broken=0
  local resolved=0

  while IFS= read -r line; do
    if [[ "$line" =~ ^@([^[:space:]].+)$ ]]; then
      local import_path="${BASH_REMATCH[1]}"
      local full_path="$PROJECT_DIR/$import_path"
      if [ ! -f "$full_path" ]; then
        log_fail "Broken @import" "@$import_path — file not found"
        broken=$((broken + 1))
      else
        resolved=$((resolved + 1))
      fi
    fi
  done < "$file"

  if [ "$broken" -eq 0 ]; then
    if [ "$resolved" -gt 0 ]; then
      log_pass "@import resolution" "All $resolved @imports resolve"
    else
      log_pass "@import resolution" "No @imports (not using modular setup)"
    fi
  fi
}

# ── Check 3: Rule count ───────────────────────────────────────────────────────

check_rule_count() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local rules
  rules=$(grep -cE "^[[:space:]]*[-*] |^[[:space:]]*[0-9]+\. " "$file" 2>/dev/null || echo "0")

  if [ "$rules" -gt 150 ]; then
    log_warn "Rule count" "$rules rules (adherence ceiling is ~150 — Claude may drop rules)"
  else
    log_pass "Rule count" "$rules rules"
  fi
}

# ── Check 4: Conflicting always/never rules ───────────────────────────────────

check_conflicts() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local conflicts=0
  local topics=("comments" "tests" "types" "imports" "exports" "logging" "errors")

  for topic in "${topics[@]}"; do
    local always_count never_count
    always_count=$(grep -ciE "always[[:space:]]+[a-z ]*$topic|$topic[a-z ]*[[:space:]]+always" "$file" 2>/dev/null || echo "0")
    never_count=$(grep -ciE "never[[:space:]]+[a-z ]*$topic|$topic[a-z ]*[[:space:]]+never" "$file" 2>/dev/null || echo "0")

    if [ "$always_count" -gt 0 ] && [ "$never_count" -gt 0 ]; then
      log_warn "Potential conflict: $topic" "Both 'always' and 'never' rules found — verify they don't contradict"
      conflicts=$((conflicts + 1))
    fi
  done

  if [ "$conflicts" -eq 0 ]; then
    log_pass "Conflict check" "No obvious always/never contradictions detected"
  fi
}

# ── Check 5: Git tracking and freshness ───────────────────────────────────────

check_git_tracking() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  if ! command -v git &>/dev/null; then
    log_warn "Git tracking" "git not available — skipping"
    return
  fi

  if ! git -C "$PROJECT_DIR" rev-parse --git-dir &>/dev/null 2>&1; then
    log_warn "Git tracking" "Not a git repo — skipping"
    return
  fi

  # Check if tracked
  if ! git -C "$PROJECT_DIR" ls-files --error-unmatch CLAUDE.md &>/dev/null 2>&1; then
    log_fail "CLAUDE.md in git" "File exists but is not tracked — run: git add CLAUDE.md"
    return
  fi

  # Check freshness
  local last_updated
  last_updated=$(git -C "$PROJECT_DIR" log --format="%ar" -- CLAUDE.md 2>/dev/null | head -1)

  if [ -z "$last_updated" ]; then
    log_warn "CLAUDE.md freshness" "No git history for this file"
  else
    log_pass "CLAUDE.md freshness" "Last updated: $last_updated"
  fi
}

# ── Check 6: Required sections ────────────────────────────────────────────────

check_required_sections() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local missing=0
  local -a required_sections=("Overview\|Purpose\|Description" "Architecture\|Stack\|Tech" "Standards\|Conventions\|Style")

  for pattern in "${required_sections[@]}"; do
    if ! grep -qiE "^#+ ($pattern)" "$file" 2>/dev/null; then
      local display="${pattern//\\|/ or }"
      log_warn "Missing section" "No heading matching: $display"
      missing=$((missing + 1))
    fi
  done

  if [ "$missing" -eq 0 ]; then
    log_pass "Required sections" "Overview, Architecture, and Standards sections found"
  fi
}

# ── Check 7: Token budget estimate ───────────────────────────────────────────

check_token_budget() {
  local file="$PROJECT_DIR/CLAUDE.md"
  [ ! -f "$file" ] && return

  local chars
  chars=$(wc -c < "$file" | tr -d ' ')
  local tokens=$((chars / 4))

  # Sum up @imports too
  local import_tokens=0
  while IFS= read -r line; do
    if [[ "$line" =~ ^@([^[:space:]].+)$ ]]; then
      local import_path="${BASH_REMATCH[1]}"
      local full_path="$PROJECT_DIR/$import_path"
      if [ -f "$full_path" ]; then
        local import_chars
        import_chars=$(wc -c < "$full_path" | tr -d ' ')
        import_tokens=$((import_tokens + import_chars / 4))
      fi
    fi
  done < "$file"

  local total=$((tokens + import_tokens))

  if [ "$total" -lt 2000 ]; then
    log_pass "Token budget" "~$total tokens (lean)"
  elif [ "$total" -lt 10000 ]; then
    log_pass "Token budget" "~$total tokens (healthy)"
  elif [ "$total" -lt 25000 ]; then
    log_warn "Token budget" "~$total tokens (heavy — consider trimming)"
  else
    log_fail "Token budget" "~$total tokens (overloaded — Claude will likely ignore some rules)"
  fi
}

# ── Run all checks ────────────────────────────────────────────────────────────

echo "Context Engineering Canary Check"
echo "================================="
echo "Project: $PROJECT_DIR"
echo ""

check_claude_md_exists || true
check_claude_md_size
check_imports
check_rule_count
check_conflicts
check_git_tracking
check_required_sections
check_token_budget

# ── Summary ───────────────────────────────────────────────────────────────────

echo ""
echo "Results:"
echo "--------"
for result in "${RESULTS[@]}"; do
  echo "  $result"
done

echo ""
echo "Score: $PASS passed, $WARN warnings, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  echo "Status: ISSUES FOUND"
  echo ""
  echo "Next steps:"
  echo "  - Fix failing checks above"
  echo "  - Run ./eval-questions.yaml audit for deeper analysis"
  echo "  - See guide/core/context-engineering.md for remediation guidance"
  exit "$FAIL"
elif [ "$WARN" -gt 0 ]; then
  echo "Status: PASSED WITH WARNINGS"
  echo "        Address warnings to improve context quality"
  exit 0
else
  echo "Status: ALL CHECKS PASSED"
  exit 0
fi
