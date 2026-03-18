#!/bin/bash
# Check if landing site is in sync with guide
# Usage: ./scripts/check-landing-sync.sh
#
# Verifies: Version, Templates count, Quiz questions, Guide lines, Claude Code version, GitHub stars

set -e

GUIDE_DIR="/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide"
LANDING_DIR="/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=== Landing Site Sync Check ==="
echo ""

ISSUES=0

# Check if landing dir exists
if [ ! -d "$LANDING_DIR" ]; then
    echo -e "${RED}ERROR: Landing directory not found at $LANDING_DIR${NC}"
    exit 1
fi

# ===================
# 1. VERSION CHECK (Guide version, not Claude Code version)
# ===================
GUIDE_VERSION=$(cat "$GUIDE_DIR/VERSION" | tr -d '\n')
# Look for guide version pattern (e.g., "Version 3.8.2" or "v3.8.2" in footer, not "Claude Code vX.Y.Z")
LANDING_VERSION=$(grep -oE 'Version [0-9]+\.[0-9]+\.[0-9]+' "$LANDING_DIR/index.html" | head -1 | sed 's/Version //')
# Fallback: try footer pattern if Version not found
if [ -z "$LANDING_VERSION" ]; then
    LANDING_VERSION=$(grep -E 'footer|Footer' -A5 "$LANDING_DIR/index.html" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
fi

echo -e "${BLUE}1. Version${NC}"
echo "   Guide:   $GUIDE_VERSION"
echo "   Landing: $LANDING_VERSION"
if [ "$GUIDE_VERSION" != "$LANDING_VERSION" ]; then
    echo -e "   ${RED}MISMATCH${NC} → Update index.html (footer + FAQ)"
    ISSUES=$((ISSUES + 1))
else
    echo -e "   ${GREEN}OK${NC}"
fi
echo ""

# ===================
# 2. TEMPLATES COUNT
# ===================
# Count actual templates, excluding README/index documentation files
TEMPLATE_COUNT=$(find "$GUIDE_DIR/examples" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" | wc -l | tr -d ' ')

# Check index.html
LANDING_TEMPLATES_INDEX=$(grep -oE '[0-9]+ Templates' "$LANDING_DIR/index.html" | head -1 | grep -oE '[0-9]+')
# Check examples/index.html
LANDING_TEMPLATES_EXAMPLES=$(grep -oE '[0-9]+ Templates' "$LANDING_DIR/examples/index.html" | head -1 | grep -oE '[0-9]+')

echo -e "${BLUE}2. Templates Count${NC}"
echo "   Guide:         $TEMPLATE_COUNT files"
echo "   index.html:    $LANDING_TEMPLATES_INDEX"
echo "   examples/index.html: $LANDING_TEMPLATES_EXAMPLES"

TEMPLATES_OK=true
if [ "$TEMPLATE_COUNT" != "$LANDING_TEMPLATES_INDEX" ]; then
    echo -e "   ${YELLOW}MISMATCH in index.html${NC}"
    TEMPLATES_OK=false
fi
if [ "$TEMPLATE_COUNT" != "$LANDING_TEMPLATES_EXAMPLES" ]; then
    echo -e "   ${YELLOW}MISMATCH in examples/index.html${NC}"
    TEMPLATES_OK=false
fi
if [ "$TEMPLATES_OK" = true ]; then
    echo -e "   ${GREEN}OK${NC}"
else
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ===================
# 3. QUIZ QUESTIONS
# ===================
# questions.json is in the landing repo (source of truth for quiz)
# Question IDs have format "XX-XXX" (e.g., "01-001"), category IDs are just numbers
QUESTIONS_COUNT=$(grep -cE '"id": "[0-9]+-[0-9]+"' "$LANDING_DIR/questions.json")
# Alternative with jq if available: jq '.questions | length'

# Check what landing pages say
LANDING_QUESTIONS_INDEX=$(grep -oE '[0-9]+ quiz questions' "$LANDING_DIR/index.html" | head -1 | grep -oE '[0-9]+')
LANDING_QUESTIONS_QUIZ=$(grep -oE '[0-9]+ Questions' "$LANDING_DIR/quiz/index.html" | head -1 | grep -oE '[0-9]+')

echo -e "${BLUE}3. Quiz Questions${NC}"
echo "   questions.json: $QUESTIONS_COUNT"
echo "   index.html:     $LANDING_QUESTIONS_INDEX"
echo "   quiz/index.html: $LANDING_QUESTIONS_QUIZ"

QUESTIONS_OK=true
if [ "$QUESTIONS_COUNT" != "$LANDING_QUESTIONS_INDEX" ]; then
    echo -e "   ${YELLOW}MISMATCH in index.html${NC}"
    QUESTIONS_OK=false
fi
if [ "$QUESTIONS_COUNT" != "$LANDING_QUESTIONS_QUIZ" ]; then
    echo -e "   ${YELLOW}MISMATCH in quiz/index.html${NC}"
    QUESTIONS_OK=false
fi
if [ "$QUESTIONS_OK" = true ]; then
    echo -e "   ${GREEN}OK${NC}"
else
    ISSUES=$((ISSUES + 1))
fi
echo ""

# ===================
# 4. GUIDE LINES
# ===================
GUIDE_LINES=$(wc -l < "$GUIDE_DIR/guide/ultimate-guide.md" | tr -d ' ')
# Landing shows approximate (e.g., "9,600+")
LANDING_LINES=$(grep -oE '[0-9,]+\+ lines' "$LANDING_DIR/index.html" | head -1 | grep -oE '[0-9,]+' | tr -d ',')

echo -e "${BLUE}4. Guide Lines${NC}"
echo "   Actual:  $GUIDE_LINES"
echo "   Landing: ${LANDING_LINES}+ (approximate)"

# Check if landing approximation is reasonable (within 500 lines)
LANDING_LINES_NUM=${LANDING_LINES:-0}
DIFF=$((GUIDE_LINES - LANDING_LINES_NUM))
if [ $DIFF -lt -500 ] || [ $DIFF -gt 1000 ]; then
    echo -e "   ${YELLOW}UPDATE RECOMMENDED${NC} - Significant difference"
    # Not counting as hard error, just warning
else
    echo -e "   ${GREEN}OK${NC} (within tolerance)"
fi
echo ""

# ===================
# 5. CLAUDE CODE VERSION
# ===================
CC_VERSION=$(grep "^latest:" "$GUIDE_DIR/machine-readable/claude-code-releases.yaml" | cut -d'"' -f2)
# Landing may show this in a badge or section - check if exists
LANDING_CC_VERSION=$(grep -oE 'Claude Code v[0-9]+\.[0-9]+\.[0-9]+' "$LANDING_DIR/index.html" 2>/dev/null | head -1 | sed 's/Claude Code v//' || echo "N/A")

echo -e "${BLUE}5. Claude Code Version${NC}"
echo "   Releases YAML: $CC_VERSION"
echo "   Landing:       ${LANDING_CC_VERSION:-Not displayed}"
if [ "$LANDING_CC_VERSION" = "N/A" ] || [ -z "$LANDING_CC_VERSION" ]; then
    echo -e "   ${YELLOW}INFO${NC}: Landing doesn't display CC version (optional)"
elif [ "$CC_VERSION" != "$LANDING_CC_VERSION" ]; then
    echo -e "   ${YELLOW}MISMATCH${NC} → Update index.html CC version badge"
    # Not counting as hard error since it's optional
else
    echo -e "   ${GREEN}OK${NC}"
fi
echo ""

# ===================
# 6. GITHUB STARS COUNT
# ===================
# Fetch actual stars count from GitHub API (public, no auth needed)
ACTUAL_STARS=$(curl -s https://api.github.com/repos/FlorianBruniaux/claude-code-ultimate-guide 2>/dev/null | grep -oE '"stargazers_count": [0-9]+' | grep -oE '[0-9]+')

# Extract stars from landing (badge-stars section)
LANDING_STARS=$(grep -A2 'badge badge-stars' "$LANDING_DIR/index.html" | grep 'badge-value' | grep -oE '[0-9]+(\.[0-9]+)?k?' | sed 's/k/000/' | sed 's/\.//g')

echo -e "${BLUE}6. GitHub Stars Count${NC}"
echo "   Actual (GitHub API): ${ACTUAL_STARS:-N/A}"
echo "   Landing (index.html): ${LANDING_STARS:-N/A}"

if [ -z "$ACTUAL_STARS" ]; then
    echo -e "   ${YELLOW}WARNING${NC}: Could not fetch from GitHub API (check connection)"
elif [ -z "$LANDING_STARS" ]; then
    echo -e "   ${RED}ERROR${NC}: Could not extract stars from landing"
    ISSUES=$((ISSUES + 1))
else
    # Allow some tolerance for display format (e.g., 1.2k = 1200, 60 = 60)
    # Compare as integers
    DIFF=$((ACTUAL_STARS - LANDING_STARS))
    DIFF_ABS=${DIFF#-}  # absolute value

    # Tolerance: ±10% or ±10 stars (whichever is larger)
    TOLERANCE=$((ACTUAL_STARS / 10))
    if [ $TOLERANCE -lt 10 ]; then
        TOLERANCE=10
    fi

    if [ $DIFF_ABS -gt $TOLERANCE ]; then
        echo -e "   ${RED}MISMATCH${NC} → Update index.html badge-stars section (line ~281)"
        ISSUES=$((ISSUES + 1))
    else
        echo -e "   ${GREEN}OK${NC} (within tolerance: ±${TOLERANCE})"
    fi
fi
echo ""

# ===================
# 7. MCP VS CLI PAGE SYNC
# ===================
MCP_GUIDE="$GUIDE_DIR/guide/ecosystem/mcp-vs-cli.md"
MCP_LANDING="$LANDING_DIR/src/pages/ecosystem/mcp-vs-cli.astro"

echo -e "${BLUE}7. MCP vs CLI page sync${NC}"

if [ ! -f "$MCP_GUIDE" ]; then
    echo -e "   ${YELLOW}INFO${NC}: guide/ecosystem/mcp-vs-cli.md not found (skip)"
elif [ ! -f "$MCP_LANDING" ]; then
    echo -e "   ${RED}MISSING${NC}: landing page src/pages/ecosystem/mcp-vs-cli.astro not found"
    ISSUES=$((ISSUES + 1))
else
    # Count H2 sections in guide
    GUIDE_H2=$(grep -c '^## ' "$MCP_GUIDE" || true)
    # Count guidance table rows (lines starting with | followed by content, skip header/separator)
    GUIDE_TABLE_ROWS=$(grep -cE '^\| [^-]' "$MCP_GUIDE" || true)
    # Count <tr> rows in landing (approximate — includes header rows)
    LANDING_TR=$(grep -c '<tr>' "$MCP_LANDING" || true)

    echo "   Guide H2 sections: $GUIDE_H2"
    echo "   Guide table rows:  $GUIDE_TABLE_ROWS"
    echo "   Landing <tr> rows: $LANDING_TR"

    # Loose check: if landing has zero <tr>, something is wrong
    if [ "$LANDING_TR" -lt 5 ]; then
        echo -e "   ${RED}ERROR${NC}: Landing page has too few table rows — may be out of sync"
        ISSUES=$((ISSUES + 1))
    else
        echo -e "   ${GREEN}OK${NC} (landing page exists, has table content)"
        echo "   Tip: if you update the guide section, mirror changes in mcp-vs-cli.astro"
    fi
fi
echo ""

# ===================
# SUMMARY
# ===================
echo "=== Summary ==="
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}All synced!${NC}"
else
    echo -e "${RED}$ISSUES issue(s) found${NC}"
    echo ""
    echo "To fix:"
    echo "  1. Edit: $LANDING_DIR/index.html"
    echo "  2. Edit: $LANDING_DIR/examples/index.html (if templates changed)"
    echo "  3. Edit: $LANDING_DIR/quiz/index.html (if questions changed)"
    echo ""
    echo "See: $LANDING_DIR/CLAUDE.md for exact line numbers"
fi

exit $ISSUES
