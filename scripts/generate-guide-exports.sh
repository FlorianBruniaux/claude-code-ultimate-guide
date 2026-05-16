#!/bin/bash

# =============================================================================
# Guide Export Generator — EPUB + PDF
# =============================================================================
# Generates the full guide/ultimate-guide.md as EPUB and/or PDF.
#
# Dependencies:
#   - pandoc (https://pandoc.org/)
#
# Installation:
#   macOS:   brew install pandoc
#   Ubuntu:  sudo apt-get install pandoc
#
# Usage:
#   ./scripts/generate-guide-exports.sh [options]
#
# Options:
#   --epub               Generate EPUB only (default: both)
#   --pdf                Generate PDF only (default: both)
#   -o, --output DIR     Output directory (default: dist/)
#   -v, --verbose        Show detailed progress
#   -h, --help           Show this help message
#
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GUIDE_FILE="$REPO_ROOT/guide/ultimate-guide.md"
BUILD_DIR="$REPO_ROOT/.build-exports"
OUTPUT_DIR="$REPO_ROOT/dist"
VERBOSE=false
DO_EPUB=true
DO_PDF=true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}→${NC} $1"; }
ok()     { echo -e "${GREEN}✓${NC} $1"; }
warn()   { echo -e "${YELLOW}⚠${NC} $1"; }
err()    { echo -e "${RED}✗${NC} $1"; exit 1; }
verbose(){ [ "$VERBOSE" = true ] && log "$1" || true; }

show_help() { sed -n '4,24p' "$0"; exit 0; }

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --epub) DO_PDF=false; shift ;;
        --pdf) DO_EPUB=false; shift ;;
        -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -h|--help) show_help ;;
        *) err "Unknown option: $1" ;;
    esac
done

VERSION="$(cat "$REPO_ROOT/VERSION" 2>/dev/null || echo "unknown")"
EPUB_OUT="$OUTPUT_DIR/claude-code-ultimate-guide.epub"
PDF_OUT="$OUTPUT_DIR/claude-code-ultimate-guide.pdf"

echo ""
echo -e "${BLUE}Claude Code Ultimate Guide — Export Generator${NC}"
echo ""

# Check dependency
if ! command -v pandoc &>/dev/null; then
    err "pandoc not found. Install with: brew install pandoc"
fi
verbose "$(pandoc --version | head -1)"

# Check source file
[ -f "$GUIDE_FILE" ] || err "Guide file not found: $GUIDE_FILE"
GUIDE_LINES=$(wc -l < "$GUIDE_FILE")
log "Source: guide/ultimate-guide.md ($GUIDE_LINES lines, v$VERSION)"

# Create output and build dirs
mkdir -p "$OUTPUT_DIR" "$BUILD_DIR"

# Pre-process guide for PDF: strip internal anchor links and disable citations
# Internal links (#anchor) cause Typst label errors; @word patterns cause citation errors
if [ "$DO_PDF" = true ]; then
    verbose "Pre-processing guide for PDF (stripping internal links)..."
    python3 -c "
import re
content = open('$GUIDE_FILE').read()
content = re.sub(r'\[([^\]]+)\]\(#[^)]+\)', r'\1', content)
open('$BUILD_DIR/guide-pdf.md', 'w').write(content)
"
fi

# ---- EPUB ----
if [ "$DO_EPUB" = true ]; then
    log "Generating EPUB..."
    pandoc \
        --from markdown \
        --to epub3 \
        --output "$EPUB_OUT" \
        --metadata title="Claude Code Ultimate Guide" \
        --metadata author="Florian Bruniaux" \
        --metadata lang="en" \
        --toc \
        --toc-depth=2 \
        --split-level=1 \
        "$GUIDE_FILE" 2>/dev/null

    if [ -f "$EPUB_OUT" ]; then
        SIZE=$(du -sh "$EPUB_OUT" | cut -f1)
        ok "EPUB → $EPUB_OUT ($SIZE)"
    else
        warn "EPUB generation failed"
    fi
fi

# ---- PDF ----
if [ "$DO_PDF" = true ]; then
    # Find Typst — try system first, fall back to Quarto's bundled binary
    TYPST_BIN=""
    if command -v typst &>/dev/null; then
        TYPST_BIN="typst"
    else
        ARCH=$(uname -m)
        # Quarto uses 'aarch64' on Apple Silicon, not 'arm64'
        [ "$ARCH" = "arm64" ] && ARCH="aarch64"
        QUARTO_TYPST="/Applications/quarto/bin/tools/${ARCH}/typst"
        [ -f "$QUARTO_TYPST" ] && TYPST_BIN="$QUARTO_TYPST"
    fi

    if [ -z "$TYPST_BIN" ]; then
        warn "Typst not found — skipping PDF. Install: brew install typst"
    else
        log "Generating PDF (via Typst)..."
        # Typst 0.14+ requires a non-empty font fallback list; pandoc's default
        # Typst template leaves `mainfont`/`monofont` empty unless set. Pass
        # widely-available fonts so the build works on Linux/macOS alike.
        pandoc \
            --from markdown-citations \
            --to pdf \
            --output "$PDF_OUT" \
            --metadata title="Claude Code Ultimate Guide" \
            --metadata author="Florian Bruniaux" \
            --metadata lang="en" \
            -V mainfont="Libertinus Serif" \
            -V monofont="DejaVu Sans Mono" \
            --toc \
            --toc-depth=2 \
            --pdf-engine="$TYPST_BIN" \
            "$BUILD_DIR/guide-pdf.md" 2>/dev/null

        if [ -f "$PDF_OUT" ]; then
            SIZE=$(du -sh "$PDF_OUT" | cut -f1)
            ok "PDF  → $PDF_OUT ($SIZE)"
        else
            warn "PDF generation failed"
        fi
    fi
fi

# Cleanup
rm -rf "$BUILD_DIR"

echo ""
echo "Open EPUB in: Calibre, Apple Books, Kindle, or any EPUB reader."
echo "Open PDF in:  any PDF viewer."
