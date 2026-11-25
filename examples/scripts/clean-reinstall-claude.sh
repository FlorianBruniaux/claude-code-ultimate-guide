#!/bin/bash
# ⚠️ Warning: This will delete all Claude Code data and configuration
# Backup your CLAUDE.md files and settings first!

echo "Starting Claude Code clean reinstall..."

# 1. Uninstall
echo -e "\n[1/5] Uninstalling Claude Code..."
npm uninstall -g @anthropic-ai/claude-code

# 2. Remove global bin files
echo "[2/5] Removing npm global files..."
rm -f "$(npm config get prefix)/bin/claude"
rm -rf "$(npm config get prefix)/lib/node_modules/@anthropic-ai/claude-code"

# 3. Delete cache and local data
echo "[3/5] Deleting cache and local data..."
rm -rf ~/.claude/downloads/*
rm -rf ~/.claude/local

# 4. Backup and remove config (optional)
echo "[4/5] Backing up config..."
timestamp=$(date +%Y%m%d-%H%M%S)
cp ~/.claude.json ~/.claude.json.backup-$timestamp 2>/dev/null || true
# Uncomment next line to remove config:
# rm -f ~/.claude.json

# 5. Reinstall
echo "[5/5] Reinstalling Claude Code..."
curl -fsSL https://claude.ai/install.sh | bash

echo -e "\n✓ Clean reinstall complete!"
echo "Run 'claude --version' to verify installation"
