#!/bin/bash
# Fetch latest Claude Code releases and show diff
# Usage: ./scripts/update-cc-releases.sh
#
# Sources tracked:
#   1. GitHub CHANGELOG (CLI/npm releases) — github.com/anthropics/claude-code/CHANGELOG.md
#   2. Weekly docs digest (Desktop/Web features) — code.claude.com/docs/en/whats-new/2026-wN.md
#   3. Help Center release notes — support.claude.com/en/articles/12138966-release-notes
#
# You then manually add the condensed entries to claude-code-releases.yaml

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
RELEASES_FILE="$REPO_DIR/machine-readable/claude-code-releases.yaml"
CHANGELOG_URL="https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
WEEKLY_DOCS_BASE="https://code.claude.com/docs/en/whats-new"
TMP_DIR="${TMPDIR:-/tmp}"
TMP_FILE="${TMP_DIR%/}/claude-code-changelog.md"
TMP_WEEKLY="${TMP_DIR%/}/claude-code-weekly.md"
TMP_WEEKLY_PAGE="${TMP_DIR%/}/claude-code-weekly-page.md"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "=== Claude Code Releases Update ==="
echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 1: GitHub CHANGELOG (CLI releases)
# ─────────────────────────────────────────────────────────────────────────────

# Get current version from our YAML
CURRENT_VERSION=$(grep "^latest:" "$RELEASES_FILE" | cut -d'"' -f2)
echo -e "${BLUE}Current tracked version:${NC} $CURRENT_VERSION"

# Fetch latest CHANGELOG
echo -e "${BLUE}[Source 1] Fetching GitHub CHANGELOG (CLI releases)...${NC}"
curl -sL "$CHANGELOG_URL" -o "$TMP_FILE"

if [ ! -s "$TMP_FILE" ]; then
    echo "ERROR: Failed to fetch CHANGELOG"
    exit 1
fi

# Extract latest version from CHANGELOG (format: "## X.Y.Z")
LATEST_VERSION=$(grep -oE "^## [0-9]+\.[0-9]+\.[0-9]+" "$TMP_FILE" | head -1 | sed 's/## //')
echo -e "${BLUE}Latest CLI version:${NC} $LATEST_VERSION"
echo ""

# Compare versions
if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
    echo -e "${GREEN}✓ CLI releases up to date!${NC}"
else
    echo -e "${YELLOW}⚠ New CLI versions available!${NC}"
    echo ""
    echo -e "${BLUE}New releases since $CURRENT_VERSION:${NC}"
    echo "────────────────────────────────────────"

    awk -v current="$CURRENT_VERSION" '
        /^## [0-9]+\.[0-9]+\.[0-9]+/ {
            match($0, /[0-9]+\.[0-9]+\.[0-9]+/)
            ver = substr($0, RSTART, RLENGTH)
            if (ver == current) exit
            in_version = 1
            print ""
            print $0
            next
        }
        in_version { print }
    ' "$TMP_FILE" | head -100

    echo ""
    echo "────────────────────────────────────────"
fi

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 2: Weekly docs digest (Desktop/Web/Cloud features)
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}[Source 2] Fetching weekly docs digest (Desktop/Web/Cloud features)...${NC}"
echo -e "${CYAN}These cover features NOT in the GitHub CHANGELOG (scheduled tasks, cloud features, web UI).${NC}"
echo ""

# Calculate current week number (ISO 8601)
CURRENT_YEAR=$(date +%Y)
CURRENT_WEEK=$(date +%V | sed 's/^0//')

# Fetch last 3 weeks to catch anything recent
> "$TMP_WEEKLY"
FOUND_WEEKLY=0
for OFFSET in 0 1 2; do
    WEEK=$((CURRENT_WEEK - OFFSET))
    YEAR=$CURRENT_YEAR
    # Handle year boundary
    if [ "$WEEK" -le 0 ]; then
        WEEK=$((52 + WEEK))
        YEAR=$((YEAR - 1))
    fi
    WEEK_STR=$(printf "%02d" "$WEEK")
    WEEKLY_URL="${WEEKLY_DOCS_BASE}/${YEAR}-w${WEEK_STR}.md"

    HTTP_CODE=$(curl -sL -o "$TMP_WEEKLY_PAGE" -w "%{http_code}" "$WEEKLY_URL")
    if [ "$HTTP_CODE" = "200" ] && [ -s "$TMP_WEEKLY_PAGE" ]; then
        echo -e "${GREEN}  ✓ Week ${WEEK} (${YEAR}) found${NC}"
        echo "" >> "$TMP_WEEKLY"
        echo "## Week ${WEEK} — ${YEAR}" >> "$TMP_WEEKLY"
        cat "$TMP_WEEKLY_PAGE" >> "$TMP_WEEKLY"
        FOUND_WEEKLY=$((FOUND_WEEKLY + 1))
    else
        echo -e "  · Week ${WEEK} (${YEAR}): not published yet"
    fi
done

if [ "$FOUND_WEEKLY" -gt 0 ]; then
    echo ""
    echo -e "${CYAN}Weekly digest content (last ${FOUND_WEEKLY} week(s)):${NC}"
    echo "────────────────────────────────────────"
    # Show a trimmed version (key features only, skip boilerplate)
    grep -E "^#|^\*\*|^- \*\*|^> " "$TMP_WEEKLY" | grep -v "^> ##" | head -60
    echo ""
    echo "────────────────────────────────────────"
    echo -e "${CYAN}Full weekly digest saved to:${NC} $TMP_WEEKLY"
else
    echo -e "  ${YELLOW}No weekly digest pages found for recent weeks.${NC}"
fi

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 3: Reference links for manual check
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}[Source 3] Additional sources to check manually:${NC}"
echo "  Help Center release notes: https://support.claude.com/en/articles/12138966-release-notes"
echo "  Weekly digest index:       ${WEEKLY_DOCS_BASE}"
echo "  GitHub releases:           https://github.com/anthropics/claude-code/releases"

# ─────────────────────────────────────────────────────────────────────────────
# Next steps
# ─────────────────────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════"
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review CLI changes above (Source 1)"
echo "2. Review weekly digest above (Source 2) for Desktop/Web/Cloud features"
echo "3. Add condensed entries to: machine-readable/claude-code-releases.yaml"
echo "4. Update: guide/core/claude-code-releases.md"
echo "5. Update 'latest' and 'updated' fields in the YAML"
echo "6. Run: ./scripts/check-landing-sync.sh"
echo ""
echo -e "${BLUE}Files saved:${NC}"
echo "  CLI CHANGELOG: $TMP_FILE"
[ "$FOUND_WEEKLY" -gt 0 ] && echo "  Weekly digest: $TMP_WEEKLY"
echo ""
echo "Tip: Use Claude to condense entries:"
echo "  claude -p \"Condense these Claude Code release notes for claude-code-releases.yaml format: \$(cat $TMP_FILE | head -200)\""
