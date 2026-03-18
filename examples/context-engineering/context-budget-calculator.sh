#!/bin/bash
# Context Budget Calculator
#
# Measures the always-on token cost of your CLAUDE.md configuration.
# Accounts for: global CLAUDE.md, project CLAUDE.md, and all @imported modules.
#
# Usage:
#   ./context-budget-calculator.sh                   # Check current directory
#   ./context-budget-calculator.sh /path/to/project  # Check specific project
#
# Token estimation: ~4 chars per token (approximate, varies by content type)
#
# Budget guide:
#   < 2K  tokens — lean (excellent)
#   2K-10K tokens — healthy (good range for most projects)
#   10K-25K tokens — heavy (review for trimming opportunities)
#   > 25K tokens  — overloaded (Claude will likely deprioritize some rules)

set -euo pipefail

PROJECT_DIR="${1:-.}"
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
GLOBAL_CLAUDE="$HOME/.claude/CLAUDE.md"
PROJECT_CLAUDE="$PROJECT_DIR/CLAUDE.md"

# ── Helpers ───────────────────────────────────────────────────────────────────

estimate_tokens() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "0"
    return
  fi
  local chars
  chars=$(wc -c < "$file" | tr -d ' ')
  echo $((chars / 4))
}

count_lines() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "0"
    return
  fi
  wc -l < "$file" | tr -d ' '
}

count_rules() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "0"
    return
  fi
  grep -cE "^[[:space:]]*[-*] |^[[:space:]]*[0-9]+\. " "$file" 2>/dev/null || echo "0"
}

format_assessment() {
  local tokens="$1"
  if [ "$tokens" -lt 2000 ]; then
    echo "LEAN         — well under budget, headroom available"
  elif [ "$tokens" -lt 10000 ]; then
    echo "HEALTHY      — good range for most projects"
  elif [ "$tokens" -lt 25000 ]; then
    echo "HEAVY        — consider trimming or deferring to @imports"
  else
    echo "OVERLOADED   — Claude will likely deprioritize some rules"
  fi
}

# ── Collect @imports from a file ──────────────────────────────────────────────

collect_imports() {
  local file="$1"
  local base_dir="$2"
  local -n imports_ref="$3"  # nameref to array

  [ ! -f "$file" ] && return

  while IFS= read -r line; do
    if [[ "$line" =~ ^@([^[:space:]].+)$ ]]; then
      local import_path="${BASH_REMATCH[1]}"
      local full_path="$base_dir/$import_path"
      imports_ref+=("$import_path|$full_path")
    fi
  done < "$file"
}

# ── Main ──────────────────────────────────────────────────────────────────────

echo "Context Budget Calculator"
echo "========================="
echo "Project: $PROJECT_DIR"
echo ""

GRAND_TOTAL_TOKENS=0
GRAND_TOTAL_RULES=0

# Global CLAUDE.md
echo "Global CLAUDE.md (~/.claude/CLAUDE.md)"
echo "----------------------------------------"
if [ -f "$GLOBAL_CLAUDE" ]; then
  G_TOKENS=$(estimate_tokens "$GLOBAL_CLAUDE")
  G_LINES=$(count_lines "$GLOBAL_CLAUDE")
  G_RULES=$(count_rules "$GLOBAL_CLAUDE")
  echo "  Lines:   $G_LINES"
  echo "  Rules:   $G_RULES"
  echo "  Tokens:  ~$G_TOKENS"
  GRAND_TOTAL_TOKENS=$((GRAND_TOTAL_TOKENS + G_TOKENS))
  GRAND_TOTAL_RULES=$((GRAND_TOTAL_RULES + G_RULES))
else
  echo "  (not found — no global config)"
fi
echo ""

# Project CLAUDE.md
echo "Project CLAUDE.md ($PROJECT_CLAUDE)"
echo "----------------------------------------"
if [ -f "$PROJECT_CLAUDE" ]; then
  P_TOKENS=$(estimate_tokens "$PROJECT_CLAUDE")
  P_LINES=$(count_lines "$PROJECT_CLAUDE")
  P_RULES=$(count_rules "$PROJECT_CLAUDE")
  echo "  Lines:   $P_LINES"
  echo "  Rules:   $P_RULES"
  echo "  Tokens:  ~$P_TOKENS"
  GRAND_TOTAL_TOKENS=$((GRAND_TOTAL_TOKENS + P_TOKENS))
  GRAND_TOTAL_RULES=$((GRAND_TOTAL_RULES + P_RULES))
else
  echo "  (not found)"
fi
echo ""

# @imports from project CLAUDE.md
declare -a IMPORTS=()
collect_imports "$PROJECT_CLAUDE" "$PROJECT_DIR" IMPORTS

IMPORT_TOTAL_TOKENS=0
if [ "${#IMPORTS[@]}" -gt 0 ]; then
  echo "@imports (always-loaded modules)"
  echo "----------------------------------------"
  for entry in "${IMPORTS[@]}"; do
    local_path="${entry%%|*}"
    full_path="${entry##*|}"
    if [ -f "$full_path" ]; then
      I_TOKENS=$(estimate_tokens "$full_path")
      I_LINES=$(count_lines "$full_path")
      IMPORT_TOTAL_TOKENS=$((IMPORT_TOTAL_TOKENS + I_TOKENS))
      printf "  %-45s %5d lines  ~%d tokens\n" "@$local_path" "$I_LINES" "$I_TOKENS"
    else
      printf "  %-45s %s\n" "@$local_path" "NOT FOUND"
    fi
  done
  echo ""
  echo "  Import total: ~$IMPORT_TOTAL_TOKENS tokens"
  GRAND_TOTAL_TOKENS=$((GRAND_TOTAL_TOKENS + IMPORT_TOTAL_TOKENS))
  echo ""
fi

# Summary
echo "Summary"
echo "======="
echo ""
echo "  Total always-on tokens:  ~$GRAND_TOTAL_TOKENS"
echo "  Total rules/instructions: $GRAND_TOTAL_RULES"
echo ""

ASSESSMENT=$(format_assessment "$GRAND_TOTAL_TOKENS")
echo "  Budget assessment: $ASSESSMENT"

if [ "$GRAND_TOTAL_RULES" -gt 150 ]; then
  echo ""
  echo "  Rule count warning: $GRAND_TOTAL_RULES rules exceeds ~150"
  echo "  Claude's adherence decreases as rule count grows."
  echo "  Consider consolidating redundant rules or moving to task-scoped @imports."
fi

echo ""
echo "Optimization Tips"
echo "-----------------"
if [ "$GRAND_TOTAL_TOKENS" -gt 10000 ]; then
  echo "  1. Move reference material to @imports and load only when needed"
  echo "  2. Trim verbose explanations — rules, not documentation"
  echo "  3. Remove rules about deprecated tech that's been removed"
  echo "  4. Consolidate duplicate rules across sections"
  echo "  5. Global CLAUDE.md: keep to framework-level defaults, not project specifics"
else
  echo "  Budget is healthy. Maintain this range as the project grows."
  echo "  Set an alert when you approach $((GRAND_TOTAL_TOKENS + 3000)) tokens."
fi
