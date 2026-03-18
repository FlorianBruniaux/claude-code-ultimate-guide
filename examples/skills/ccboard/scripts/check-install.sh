#!/bin/bash
# Check if ccboard is installed and return status

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Checking ccboard installation..."
echo ""

# Check if ccboard is in PATH
if command -v ccboard &> /dev/null; then
    CCBOARD_PATH=$(which ccboard)
    CCBOARD_VERSION=$(ccboard --version 2>&1 | head -n1 || echo "unknown")

    echo -e "${GREEN}✅ ccboard is installed${NC}"
    echo "   Location: $CCBOARD_PATH"
    echo "   Version: $CCBOARD_VERSION"
    echo ""
    echo "Run with:"
    echo "  ccboard              # Launch TUI"
    echo "  ccboard web          # Launch web UI"
    echo "  ccboard --help       # Show all options"
    exit 0
else
    echo -e "${RED}❌ ccboard is not installed${NC}"
    echo ""
    echo "Install with:"
    echo "  cargo install ccboard"
    echo ""
    echo "Or use Claude Code command:"
    echo "  /ccboard-install"
    exit 1
fi
