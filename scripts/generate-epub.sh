#!/bin/bash

# =============================================================================
# EPUB Generator for Claude Code Ultimate Guide
# =============================================================================
# Converts markdown documentation to a properly formatted EPUB book
#
# Dependencies:
#   - pandoc (https://pandoc.org/)
#
# Installation:
#   macOS:   brew install pandoc
#   Ubuntu:  sudo apt-get install pandoc
#   Windows: choco install pandoc
#
# Usage:
#   ./scripts/generate-epub.sh [options]
#
# Options:
#   -o, --output FILE    Output filename (default: claude-code-ultimate-guide.epub)
#   -v, --verbose        Show detailed progress
#   -h, --help           Show this help message
#
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
OUTPUT_FILE="claude-code-ultimate-guide.epub"
VERBOSE=false

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GUIDE_DIR="$REPO_ROOT/guide"
BUILD_DIR="$REPO_ROOT/.build-epub"

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "${BLUE}============================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}→${NC} $1"
    fi
}

show_help() {
    head -30 "$0" | tail -25
    exit 0
}

# =============================================================================
# Parse Arguments
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            ;;
    esac
done

# =============================================================================
# Check Dependencies
# =============================================================================

print_header "EPUB Generator for Claude Code Guide"

echo ""
echo "Checking dependencies..."

if ! command -v pandoc &> /dev/null; then
    print_error "pandoc is not installed"
    echo ""
    echo "Please install pandoc:"
    echo "  macOS:   brew install pandoc"
    echo "  Ubuntu:  sudo apt-get install pandoc"
    echo "  Windows: choco install pandoc"
    echo ""
    exit 1
fi

PANDOC_VERSION=$(pandoc --version | head -1)
print_success "Found $PANDOC_VERSION"

# =============================================================================
# Setup Build Directory
# =============================================================================

echo ""
echo "Setting up build environment..."

# Clean and create build directory
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
print_info "Created build directory: $BUILD_DIR"

# =============================================================================
# Read Version
# =============================================================================

VERSION="unknown"
if [ -f "$REPO_ROOT/VERSION" ]; then
    VERSION=$(cat "$REPO_ROOT/VERSION")
    print_info "Guide version: $VERSION"
fi

# =============================================================================
# Create EPUB Metadata
# =============================================================================

echo ""
echo "Generating metadata..."

cat > "$BUILD_DIR/metadata.yaml" << EOF
---
title: "The Ultimate Claude Code Guide"
subtitle: "From Zero to Power User"
author:
  - "Florian BRUNIAUX"
  - "Claude (Anthropic)"
date: "$(date +%Y-%m-%d)"
lang: en
subject: "Programming, AI, Claude Code, Developer Tools"
description: |
  A comprehensive, self-contained guide to mastering Claude Code -
  Anthropic's AI-powered CLI tool for software development.
  From installation to advanced patterns, this guide covers everything
  you need to become a Claude Code power user.
publisher: "Community Documentation"
rights: "Creative Commons Attribution-ShareAlike 4.0"
version: "$VERSION"
keywords:
  - Claude Code
  - AI Coding
  - Anthropic
  - Developer Tools
  - CLI
  - Software Development
toc: true
toc-depth: 3
number-sections: false
highlight-style: tango
epub-cover-image:
EOF

print_success "Metadata file created"

# =============================================================================
# Process Markdown Files
# =============================================================================

echo ""
echo "Processing markdown files..."

# Create a combined markdown file with proper chapter separation
COMBINED_MD="$BUILD_DIR/combined.md"

# Function to add a file with proper header
add_chapter() {
    local file="$1"
    local title="$2"

    if [ -f "$file" ]; then
        print_info "Adding: $title"

        # Add page break before chapter (except first)
        if [ -s "$COMBINED_MD" ]; then
            echo -e "\n\n<div style=\"page-break-before: always;\"></div>\n" >> "$COMBINED_MD"
        fi

        cat "$file" >> "$COMBINED_MD"
        echo -e "\n" >> "$COMBINED_MD"
        return 0
    else
        print_warning "File not found: $file"
        return 1
    fi
}

# Main guide (introduction and core content)
add_chapter "$GUIDE_DIR/ultimate-guide.md" "Ultimate Guide (Main Content)"

# Additional guides as appendices
echo -e "\n\n<div style=\"page-break-before: always;\"></div>\n" >> "$COMBINED_MD"
echo -e "# Additional Guides\n" >> "$COMBINED_MD"
echo -e "The following sections provide specialized deep-dives into specific topics.\n" >> "$COMBINED_MD"

# Architecture deep-dive
add_chapter "$GUIDE_DIR/architecture.md" "Architecture Deep-Dive"

# Methodologies
add_chapter "$GUIDE_DIR/methodologies.md" "Development Methodologies"

# Data Privacy
add_chapter "$GUIDE_DIR/data-privacy.md" "Data Privacy"

# Security Hardening
add_chapter "$GUIDE_DIR/security-hardening.md" "Security Hardening"

# DevOps & SRE
add_chapter "$GUIDE_DIR/devops-sre.md" "DevOps & SRE"

# Production Safety
add_chapter "$GUIDE_DIR/production-safety.md" "Production Safety"

# Observability
add_chapter "$GUIDE_DIR/observability.md" "Observability"

# AI Ecosystem
add_chapter "$GUIDE_DIR/ai-ecosystem.md" "AI Ecosystem"

# AI Traceability
add_chapter "$GUIDE_DIR/ai-traceability.md" "AI Traceability"

# Learning with AI
add_chapter "$GUIDE_DIR/learning-with-ai.md" "Learning with AI"

# Adoption Approaches
add_chapter "$GUIDE_DIR/adoption-approaches.md" "Adoption Approaches"

# Claude Code Releases
add_chapter "$GUIDE_DIR/claude-code-releases.md" "Claude Code Releases"

# Workflows section
echo -e "\n\n<div style=\"page-break-before: always;\"></div>\n" >> "$COMBINED_MD"
echo -e "# Workflow Guides\n" >> "$COMBINED_MD"
echo -e "Step-by-step guides for specific workflows and use cases.\n" >> "$COMBINED_MD"

for workflow_file in "$GUIDE_DIR/workflows/"*.md; do
    if [ -f "$workflow_file" ] && [ "$(basename "$workflow_file")" != "README.md" ]; then
        workflow_name=$(basename "$workflow_file" .md | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')
        add_chapter "$workflow_file" "Workflow: $workflow_name"
    fi
done

# Cheatsheet at the end
add_chapter "$GUIDE_DIR/cheatsheet.md" "Cheatsheet"

print_success "Combined $(wc -l < "$COMBINED_MD" | tr -d ' ') lines of content"

# =============================================================================
# Fix Image Paths
# =============================================================================

echo ""
echo "Fixing image paths..."

# Update relative image paths to absolute paths
if [ -d "$GUIDE_DIR/images" ]; then
    # Copy images to build directory
    cp -r "$GUIDE_DIR/images" "$BUILD_DIR/"
    print_info "Copied images directory"

    # Fix paths in the combined markdown
    # Convert paths like ./images/ or images/ to absolute paths
    sed -i.bak "s|\./images/|$BUILD_DIR/images/|g" "$COMBINED_MD"
    sed -i.bak "s|](images/|]($BUILD_DIR/images/|g" "$COMBINED_MD"
    rm -f "$COMBINED_MD.bak"
    print_success "Image paths updated"
else
    print_warning "No images directory found"
fi

# =============================================================================
# Generate EPUB
# =============================================================================

echo ""
echo "Generating EPUB..."

OUTPUT_PATH="$REPO_ROOT/$OUTPUT_FILE"

# Run pandoc with appropriate options
pandoc "$COMBINED_MD" \
    --metadata-file="$BUILD_DIR/metadata.yaml" \
    --from markdown+yaml_metadata_block+smart+emoji+lists_without_preceding_blankline \
    --to epub3 \
    --toc \
    --toc-depth=3 \
    --split-level=2 \
    --epub-chapter-level=2 \
    --standalone \
    --output "$OUTPUT_PATH" \
    2>&1 | while read -r line; do
        print_info "$line"
    done

if [ -f "$OUTPUT_PATH" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
    print_success "Generated: $OUTPUT_FILE ($FILE_SIZE)"
else
    print_error "Failed to generate EPUB"
    exit 1
fi

# =============================================================================
# Cleanup
# =============================================================================

echo ""
echo "Cleaning up..."

rm -rf "$BUILD_DIR"
print_success "Build directory removed"

# =============================================================================
# Summary
# =============================================================================

echo ""
print_header "EPUB Generation Complete!"
echo ""
echo "Output file: $OUTPUT_PATH"
echo "File size:   $FILE_SIZE"
echo ""
echo "You can now:"
echo "  - Open with Apple Books, Calibre, or any EPUB reader"
echo "  - Transfer to your e-reader device"
echo "  - Convert to other formats with Calibre"
echo ""
