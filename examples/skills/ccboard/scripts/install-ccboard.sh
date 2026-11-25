#!/bin/bash
# Install ccboard via cargo

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}📦 ccboard Installation${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if cargo is installed
if ! command -v cargo &> /dev/null; then
    echo -e "${RED}❌ Error: cargo is not installed${NC}"
    echo ""
    echo "Install Rust and cargo from: https://rustup.rs"
    echo ""
    echo "Run:"
    echo "  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

echo -e "${GREEN}✅ cargo found${NC}"
echo ""

# Check if ccboard is already installed
if command -v ccboard &> /dev/null; then
    CURRENT_VERSION=$(ccboard --version 2>&1 | head -n1 || echo "unknown")
    echo -e "${YELLOW}⚠️  ccboard is already installed: $CURRENT_VERSION${NC}"
    echo ""
    read -p "Do you want to update to the latest version? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo ""
fi

# Install ccboard
echo -e "${CYAN}Installing ccboard...${NC}"
echo ""

if cargo install ccboard --force; then
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ ccboard installed successfully!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Get installed version
    INSTALLED_VERSION=$(ccboard --version 2>&1 | head -n1 || echo "unknown")
    echo "Version: $INSTALLED_VERSION"
    echo "Location: $(which ccboard)"
    echo ""

    echo "Quick start:"
    echo "  ccboard              # Launch TUI dashboard"
    echo "  ccboard web          # Launch web interface"
    echo "  ccboard --help       # Show all options"
    echo ""
    echo "Or use Claude Code commands:"
    echo "  /dashboard           # Launch TUI"
    echo "  /mcp-status          # Open MCP tab"
    echo "  /costs               # Open costs analysis"
else
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ Installation failed${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Ensure cargo is up to date: rustup update"
    echo "  2. Check network connection"
    echo "  3. Try manual installation from source:"
    echo "     git clone https://github.com/FlorianBruniaux/ccboard"
    echo "     cd ccboard"
    echo "     cargo install --path crates/ccboard"
    exit 1
fi
