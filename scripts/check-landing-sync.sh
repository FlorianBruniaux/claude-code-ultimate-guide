#!/bin/bash
# Check if landing site (Astro) is in sync with guide
# Usage: ./scripts/check-landing-sync.sh
#
# Verifies: Version, Templates count, Quiz questions, Guide lines, Claude Code version, MCP vs CLI page
# Note: GitHub stars are fetched live client-side by HeroBanner.astro — no static value to sync.

GUIDE_DIR="/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide"
LANDING_DIR="/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=== Landing Site Sync Check (Astro) ==="
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
GUIDE_VERSION=$(tr -d '\n' < "$GUIDE_DIR/VERSION")
# Guide version is displayed in the announcement banner (badge + link)
BANNER_FILE="$LANDING_DIR/src/components/global/AnnouncementBanner.astro"
LANDING_VERSION=$(grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' "$BANNER_FILE" 2>/dev/null | head -1 | sed 's/^v//')

echo -e "${BLUE}1. Version${NC}"
echo "   Guide:   $GUIDE_VERSION"
echo "   Landing: ${LANDING_VERSION:-not found}"
if [ "$GUIDE_VERSION" != "$LANDING_VERSION" ]; then
    echo -e "   ${RED}MISMATCH${NC} → Update src/components/global/AnnouncementBanner.astro"
    ISSUES=$((ISSUES + 1))
else
    echo -e "   ${GREEN}OK${NC}"
fi
echo ""

# ===================
# 2. TEMPLATES COUNT
# ===================
# Count actual templates, excluding README/index documentation files
TEMPLATE_COUNT=$(find "$GUIDE_DIR/examples" -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name "README.md" -not -name "index.md" -not -path '*/commands/*' | wc -l | tr -d ' ')

# Check examples-data.ts for indexed path count
LANDING_TEMPLATES_DATA=$(grep -c 'path:' "$LANDING_DIR/src/data/examples-data.ts" 2>/dev/null || echo 0)
# Check examples index.astro tagline for display count
LANDING_TEMPLATES_ASTRO=$(grep -oE '[0-9]+ production-ready templates' "$LANDING_DIR/src/pages/examples/index.astro" 2>/dev/null | head -1 | grep -oE '[0-9]+' || echo "")
# Check hero badge count
LANDING_TEMPLATES_HERO=$(grep -A2 'badge badge-templates' "$LANDING_DIR/src/components/landing/HeroBanner.astro" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "")

echo -e "${BLUE}2. Templates Count${NC}"
echo "   Guide files (find): $TEMPLATE_COUNT"
echo "   Catalog indexed:    $LANDING_TEMPLATES_DATA (path: entries in examples-data.ts)"
echo "   Examples page:      ${LANDING_TEMPLATES_ASTRO:-not found} (examples/index.astro tagline)"
echo "   Hero badge:         ${LANDING_TEMPLATES_HERO:-not found} (HeroBanner.astro)"

TEMPLATES_OK=true
if [ "${LANDING_TEMPLATES_DATA:-0}" -lt 200 ] 2>/dev/null; then
    echo -e "   ${YELLOW}LOW: examples-data.ts has fewer than 200 indexed entries${NC}"
    TEMPLATES_OK=false
fi
if [ -n "$LANDING_TEMPLATES_ASTRO" ] && [ -n "$LANDING_TEMPLATES_HERO" ] && [ "$LANDING_TEMPLATES_ASTRO" != "$LANDING_TEMPLATES_HERO" ]; then
    echo -e "   ${YELLOW}MISMATCH between examples page and hero badge${NC}"
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
# Source of truth: src/content/questions/*/*.md in the landing repo (questions.json is generated at build via astro:content)
QUESTIONS_COUNT=$(find "$LANDING_DIR/src/content/questions" -name '*.md' -not -name 'README*' 2>/dev/null | wc -l | tr -d ' ')
LANDING_QUESTIONS_QUIZ=$(grep -oE '"numberOfQuestions": [0-9]+' "$LANDING_DIR/src/pages/quiz/index.astro" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "")
LANDING_QUESTIONS_HERO=$(grep -oE '[0-9]+ questions' "$LANDING_DIR/src/components/landing/HeroBanner.astro" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "")
LANDING_QUESTIONS_INDEX=$(grep -oE '[0-9]+-question quiz' "$LANDING_DIR/src/pages/index.astro" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "")

echo -e "${BLUE}3. Quiz Questions${NC}"
echo "   src/content/questions/ (md files): $QUESTIONS_COUNT"
echo "   quiz/index.astro:      ${LANDING_QUESTIONS_QUIZ:-not found} (numberOfQuestions schema)"
echo "   HeroBanner badge:      ${LANDING_QUESTIONS_HERO:-not found}"
echo "   index.astro meta:      ${LANDING_QUESTIONS_INDEX:-not found} (description \"N-question quiz\")"

QUESTIONS_OK=true
if [ "$QUESTIONS_COUNT" != "$LANDING_QUESTIONS_QUIZ" ]; then
    echo -e "   ${YELLOW}MISMATCH in quiz/index.astro${NC}"
    QUESTIONS_OK=false
fi
if [ -n "$LANDING_QUESTIONS_HERO" ] && [ "$QUESTIONS_COUNT" != "$LANDING_QUESTIONS_HERO" ]; then
    echo -e "   ${YELLOW}MISMATCH in HeroBanner.astro${NC}"
    QUESTIONS_OK=false
fi
if [ "$QUESTIONS_COUNT" != "$LANDING_QUESTIONS_INDEX" ]; then
    echo -e "   ${YELLOW}MISMATCH in index.astro meta description${NC}"
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
# Landing shows a rounded claim like "25K+ lines" in index.astro meta description
LANDING_LINES_K=$(grep -oE '[0-9]+K\+ lines' "$LANDING_DIR/src/pages/index.astro" 2>/dev/null | head -1 | grep -oE '[0-9]+' || echo "")

echo -e "${BLUE}4. Guide Lines${NC}"
echo "   Actual:  $GUIDE_LINES"
echo "   Landing: ${LANDING_LINES_K:-?}K+ (index.astro meta description)"

if [ -z "$LANDING_LINES_K" ]; then
    echo -e "   ${YELLOW}INFO${NC}: No \"NK+ lines\" claim found in index.astro"
else
    LOWER=$((LANDING_LINES_K * 1000))
    UPPER=$(((LANDING_LINES_K + 2) * 1000))
    if [ "$GUIDE_LINES" -lt "$LOWER" ] || [ "$GUIDE_LINES" -ge "$UPPER" ]; then
        echo -e "   ${YELLOW}UPDATE RECOMMENDED${NC}: claim \"${LANDING_LINES_K}K+\" drifted from actual $GUIDE_LINES"
        # Soft warning, not counted as hard error
    else
        echo -e "   ${GREEN}OK${NC} (within tolerance)"
    fi
fi
echo ""

# ===================
# 5. CLAUDE CODE VERSION
# ===================
CC_VERSION=$(grep "^latest:" "$GUIDE_DIR/machine-readable/claude-code-releases.yaml" | cut -d'"' -f2)
# releases.ts is newest-first; the first version entry must carry latest: true
RELEASES_TS="$LANDING_DIR/src/data/releases.ts"
LANDING_CC_VERSION=$(grep -oE "version: 'v[0-9]+\.[0-9]+\.[0-9]+'" "$RELEASES_TS" 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "")
LATEST_FLAG_COUNT=$(grep -c 'latest: true' "$RELEASES_TS" 2>/dev/null || echo 0)

echo -e "${BLUE}5. Claude Code Version${NC}"
echo "   Releases YAML:      $CC_VERSION"
echo "   Landing releases.ts: ${LANDING_CC_VERSION:-not found} (first entry)"
if [ "$CC_VERSION" != "$LANDING_CC_VERSION" ]; then
    echo -e "   ${RED}MISMATCH${NC} → Add v$CC_VERSION to src/data/releases.ts"
    ISSUES=$((ISSUES + 1))
elif [ "$LATEST_FLAG_COUNT" -ne 1 ]; then
    echo -e "   ${RED}FLAG ERROR${NC}: expected exactly one 'latest: true' in releases.ts, found $LATEST_FLAG_COUNT"
    ISSUES=$((ISSUES + 1))
else
    echo -e "   ${GREEN}OK${NC}"
fi
echo ""

# ===================
# 6. MCP VS CLI PAGE SYNC
# ===================
MCP_GUIDE="$GUIDE_DIR/guide/ecosystem/mcp-vs-cli.md"
MCP_LANDING="$LANDING_DIR/src/pages/ecosystem/mcp-vs-cli.astro"

echo -e "${BLUE}6. MCP vs CLI page sync${NC}"

if [ ! -f "$MCP_GUIDE" ]; then
    echo -e "   ${YELLOW}INFO${NC}: guide/ecosystem/mcp-vs-cli.md not found (skip)"
elif [ ! -f "$MCP_LANDING" ]; then
    echo -e "   ${RED}MISSING${NC}: landing page src/pages/ecosystem/mcp-vs-cli.astro not found"
    ISSUES=$((ISSUES + 1))
else
    GUIDE_H2=$(grep -c '^## ' "$MCP_GUIDE" || true)
    GUIDE_TABLE_ROWS=$(grep -cE '^\| [^-]' "$MCP_GUIDE" || true)
    LANDING_TR=$(grep -c '<tr>' "$MCP_LANDING" || true)

    echo "   Guide H2 sections: $GUIDE_H2"
    echo "   Guide table rows:  $GUIDE_TABLE_ROWS"
    echo "   Landing <tr> rows: $LANDING_TR"

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
    echo "Files to check (Astro landing):"
    echo "  - src/components/global/AnnouncementBanner.astro (guide version)"
    echo "  - src/components/landing/HeroBanner.astro (badges: templates, quiz)"
    echo "  - src/pages/index.astro (meta description: lines, quiz)"
    echo "  - src/pages/quiz/index.astro (numberOfQuestions schema)"
    echo "  - src/data/releases.ts (Claude Code versions)"
    echo ""
    echo "See: $LANDING_DIR/CLAUDE.md for workflows"
fi

exit $ISSUES
