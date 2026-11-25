# ⚠️ Warning: This will delete all Claude Code data and configuration
# Backup your CLAUDE.md files and settings first!

Write-Host "Starting Claude Code clean reinstall..." -ForegroundColor Yellow

# 1. Uninstall
Write-Host "`n[1/5] Uninstalling Claude Code..."
npm uninstall -g @anthropic-ai/claude-code

# 2. Remove shims and binaries
Write-Host "[2/5] Removing npm shims and binaries..."
Remove-Item -Path "$env:APPDATA\npm\claude*" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:APPDATA\npm\node_modules\@anthropic-ai\claude-code" -Recurse -Force -ErrorAction SilentlyContinue

# 3. Delete cache and local data
Write-Host "[3/5] Deleting cache and local data..."
Remove-Item -Path "$env:USERPROFILE\.claude\downloads\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:USERPROFILE\.claude\local" -Recurse -Force -ErrorAction SilentlyContinue

# 4. Backup and remove config (optional - comment out to keep config)
Write-Host "[4/5] Backing up config..."
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item "$env:USERPROFILE\.claude.json" "$env:USERPROFILE\.claude.json.backup-$timestamp" -ErrorAction SilentlyContinue
# Uncomment next line to remove config:
# Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force -ErrorAction SilentlyContinue

# 5. Reinstall
Write-Host "[5/5] Reinstalling Claude Code..."
irm https://claude.ai/install.ps1 | iex

Write-Host "`n✓ Clean reinstall complete!" -ForegroundColor Green
Write-Host "Run 'claude --version' to verify installation"
