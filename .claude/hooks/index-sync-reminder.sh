#!/usr/bin/env bash
# Stop hook. Fires when a turn ends.
#
# Catches the failure this repo keeps hitting: guide/ content changes, the
# machine-readable index does not, and nobody notices until an anchor audit
# months later. The index feeds the MCP server and the landing's Cmd+K palette,
# so a missing entry is invisible content, not a cosmetic gap.
#
# Non-blocking by design. It reports, it does not veto: a turn can legitimately
# end mid-edit, and a hook that blocks on that becomes a hook people disable.

set -uo pipefail

REPO="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$REPO" ] && [ -d "$REPO/.git" ] || exit 0
cd "$REPO" || exit 0

changed() { git status --porcelain -- "$@" 2>/dev/null | grep -q .; }

# Nothing touched in guide/, nothing to say.
changed guide/ || exit 0

MISSING=""
INDEX_STALE=""

# 1. New or renamed guide files that reference.yaml has never heard of.
if [ -x scripts/check-index-coverage.py ] || [ -f scripts/check-index-coverage.py ]; then
  if ! python3 scripts/check-index-coverage.py --check --quiet >/dev/null 2>&1; then
    MISSING=$(python3 scripts/check-index-coverage.py 2>/dev/null | grep "unindexed" | head -5)
  fi
fi

# 2. Guide content edited while every index file stayed untouched. New sections
#    inside an already-indexed file are the common case here, and no automated
#    check can tell a typo fix from a new concept, so this is a prompt to look.
if ! changed machine-readable/reference.yaml llms.txt llms-full.txt machine-readable/llms.txt; then
  INDEX_STALE="yes"
fi

[ -z "$MISSING" ] && [ -z "$INDEX_STALE" ] && exit 0

echo "── index sync ─────────────────────────────────────────────"
if [ -n "$MISSING" ]; then
  echo "Guide files with no entry in machine-readable/reference.yaml:"
  echo "$MISSING"
fi
if [ -n "$INDEX_STALE" ]; then
  echo "guide/ changed, no index file did. If this added a page, a section,"
  echo "a concept, or a named tool, it needs an entry:"
  echo "  machine-readable/reference.yaml   deep_dive key -> path#anchor"
  echo "  llms-full.txt                     only for guide-level structure"
  echo "  mcp-server/content/reference.yaml manual copy, no resync script"
fi
echo "Then: python3 scripts/validate-reference-yaml.py --ci"
echo "A deep_dive key change also needs \`pnpm build:search\` on the landing."
echo "───────────────────────────────────────────────────────────"
exit 0
