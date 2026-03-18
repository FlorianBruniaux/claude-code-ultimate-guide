#!/bin/bash
# sync-claude-config.sh - Sync Claude Code global configuration via Git + .env substitution
# Version: 1.0.0
# Inspired by: brianlovin/claude-config + Martin Ratinaud (504 sessions)
#
# Features:
# - Parse .env for MCP secrets
# - Substitute variables in mcp.json from template
# - Validate .gitignore (prevent secret leaks)
# - Backup to cloud storage (optional)
# - Multi-machine sync via Git
#
# Usage:
#   ./sync-claude-config.sh setup      # Initial setup (Git repo + symlinks)
#   ./sync-claude-config.sh sync       # Pull latest from Git, regenerate configs
#   ./sync-claude-config.sh backup     # Push to Git + optional cloud backup
#   ./sync-claude-config.sh restore    # Restore from backup
#   ./sync-claude-config.sh validate   # Verify .gitignore and secrets isolation

set -euo pipefail

# Configuration
CLAUDE_DIR="$HOME/.claude"
BACKUP_DIR="$HOME/claude-config-backup"
ENV_FILE="$CLAUDE_DIR/.env"
MCP_TEMPLATE="$BACKUP_DIR/mcp.json.template"
MCP_CONFIG="$CLAUDE_DIR/mcp.json"
SETTINGS_TEMPLATE="$BACKUP_DIR/settings.template.json"
SETTINGS_CONFIG="$CLAUDE_DIR/settings.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

check_requirements() {
    local missing=()
    command -v git >/dev/null 2>&1 || missing+=("git")
    command -v envsubst >/dev/null 2>&1 || missing+=("envsubst")

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required commands: ${missing[*]}"
        log_info "Install with: brew install gettext (macOS) or apt install gettext-base (Linux)"
        exit 1
    fi
}

# Setup: Create backup repo with symlinks
setup() {
    log_info "Setting up Claude Code configuration backup..."

    # Create backup directory
    if [ -d "$BACKUP_DIR" ]; then
        log_warn "Backup directory already exists: $BACKUP_DIR"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
        rm -rf "$BACKUP_DIR"
    fi

    mkdir -p "$BACKUP_DIR"
    cd "$BACKUP_DIR"
    git init
    log_info "Created Git repository: $BACKUP_DIR"

    # Create symlinks for directories (not files with secrets)
    for dir in agents commands hooks skills rules; do
        if [ -d "$CLAUDE_DIR/$dir" ]; then
            ln -sf "$CLAUDE_DIR/$dir" "$BACKUP_DIR/$dir"
            log_info "Symlinked: ~/.claude/$dir"
        else
            log_warn "Directory not found: ~/.claude/$dir (skipping)"
        fi
    done

    # Create .gitignore
    cat > .gitignore << 'EOF'
# Never commit these (contain secrets)
.env
mcp.json
settings.json
*.local.json

# Session history (large, personal)
projects/

# Backup artifacts
*.tar.gz
*.bak
EOF
    log_info "Created .gitignore"

    # Create template files if they don't exist
    if [ -f "$MCP_CONFIG" ]; then
        # Convert existing mcp.json to template
        sed 's/"[a-zA-Z0-9_-]\{20,\}"/"${env:\U&}"/' "$MCP_CONFIG" > "$MCP_TEMPLATE"
        log_info "Created mcp.json.template from existing config"
    fi

    if [ -f "$SETTINGS_CONFIG" ]; then
        cp "$SETTINGS_CONFIG" "$SETTINGS_TEMPLATE"
        log_info "Created settings.template.json"
    fi

    # Create example .env
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << 'EOF'
# Claude Code MCP Secrets
# Add your API keys here (this file is gitignored)

# GitHub
GITHUB_TOKEN=ghp_your_token_here

# OpenAI
OPENAI_API_KEY=sk_your_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Add more secrets as needed
EOF
        chmod 600 "$ENV_FILE"
        log_info "Created .env template (edit with your secrets)"
    fi

    # Initial commit
    git add .
    git commit -m "Initial Claude Code configuration backup"
    log_info "Initial commit created"

    echo ""
    log_info "Setup complete! Next steps:"
    echo "  1. Edit $ENV_FILE with your secrets"
    echo "  2. Add Git remote: git -C $BACKUP_DIR remote add origin <your-private-repo-url>"
    echo "  3. Run: $0 backup"
}

# Sync: Pull from Git and regenerate configs
sync() {
    log_info "Syncing Claude Code configuration..."

    if [ ! -d "$BACKUP_DIR/.git" ]; then
        log_error "Backup directory not initialized. Run: $0 setup"
        exit 1
    fi

    cd "$BACKUP_DIR"

    # Pull latest from remote
    if git remote get-url origin >/dev/null 2>&1; then
        log_info "Pulling latest from Git..."
        git pull --rebase
    else
        log_warn "No Git remote configured (local only)"
    fi

    # Regenerate configs from templates + .env
    if [ ! -f "$ENV_FILE" ]; then
        log_error ".env file not found: $ENV_FILE"
        log_info "Create it with your secrets, then run sync again"
        exit 1
    fi

    # Export .env variables
    set -a
    source "$ENV_FILE"
    set +a

    # Substitute variables in mcp.json template
    if [ -f "$MCP_TEMPLATE" ]; then
        envsubst < "$MCP_TEMPLATE" > "$MCP_CONFIG"
        log_info "Regenerated mcp.json from template"
    else
        log_warn "mcp.json.template not found (skipping)"
    fi

    # Copy settings (no substitution needed unless you use env vars)
    if [ -f "$SETTINGS_TEMPLATE" ]; then
        cp "$SETTINGS_TEMPLATE" "$SETTINGS_CONFIG"
        log_info "Updated settings.json"
    fi

    log_info "Sync complete! Restart Claude Code to apply changes."
}

# Backup: Push to Git + optional cloud storage
backup() {
    log_info "Backing up Claude Code configuration..."

    if [ ! -d "$BACKUP_DIR/.git" ]; then
        log_error "Backup directory not initialized. Run: $0 setup"
        exit 1
    fi

    cd "$BACKUP_DIR"

    # Check for changes
    if git diff-index --quiet HEAD --; then
        log_info "No changes to backup"
        return 0
    fi

    # Commit changes
    git add agents/ commands/ hooks/ skills/ rules/ *.template.json .gitignore 2>/dev/null || true
    git commit -m "Backup Claude Code config - $(date +%Y-%m-%d\ %H:%M:%S)"
    log_info "Changes committed"

    # Push to remote if configured
    if git remote get-url origin >/dev/null 2>&1; then
        git push
        log_info "Pushed to remote Git repository"
    else
        log_warn "No Git remote configured. Add with:"
        echo "  git remote add origin git@github.com:yourusername/claude-config-private.git"
    fi

    # Optional: Backup to cloud storage (Box, Dropbox, etc.)
    # Uncomment and customize:
    # if command -v rclone >/dev/null 2>&1; then
    #     rclone sync "$BACKUP_DIR" remote:claude-config-backup
    #     log_info "Synced to cloud storage (rclone)"
    # fi
}

# Restore: Restore from backup
restore() {
    log_info "Restoring Claude Code configuration..."

    if [ ! -d "$BACKUP_DIR/.git" ]; then
        log_error "Backup directory not found. Clone your backup repo to: $BACKUP_DIR"
        exit 1
    fi

    cd "$BACKUP_DIR"

    # Recreate symlinks
    for dir in agents commands hooks skills rules; do
        if [ -d "$BACKUP_DIR/$dir" ]; then
            rm -f "$BACKUP_DIR/$dir"
            ln -sf "$CLAUDE_DIR/$dir" "$BACKUP_DIR/$dir"
            log_info "Recreated symlink: ~/.claude/$dir"
        fi
    done

    # Regenerate configs
    sync

    log_info "Restore complete!"
}

# Validate: Check .gitignore and secrets isolation
validate() {
    log_info "Validating Claude Code configuration..."

    local issues=0

    # Check .env not in Git
    if [ -f "$ENV_FILE" ] && git -C "$BACKUP_DIR" ls-files --error-unmatch "$ENV_FILE" >/dev/null 2>&1; then
        log_error ".env is tracked by Git (CRITICAL SECURITY ISSUE)"
        issues=$((issues + 1))
    else
        log_info ".env is not tracked by Git"
    fi

    # Check file permissions
    if [ -f "$ENV_FILE" ]; then
        perm=$(stat -f "%A" "$ENV_FILE" 2>/dev/null || stat -c "%a" "$ENV_FILE" 2>/dev/null)
        if [ "$perm" != "600" ]; then
            log_warn ".env permissions are $perm (should be 600)"
            chmod 600 "$ENV_FILE"
            log_info "Fixed permissions to 600"
        else
            log_info ".env permissions are correct (600)"
        fi
    fi

    # Check secrets in staged files
    if git -C "$BACKUP_DIR" diff --cached --name-only | xargs grep -E "(sk-[A-Za-z0-9]{48}|ghp_[A-Za-z0-9]{36}|AKIA[A-Z0-9]{16})" >/dev/null 2>&1; then
        log_error "Secrets detected in staged files (DO NOT COMMIT)"
        issues=$((issues + 1))
    else
        log_info "No secrets detected in staged files"
    fi

    # Check .gitignore exists
    if [ ! -f "$BACKUP_DIR/.gitignore" ]; then
        log_error ".gitignore missing (create one to prevent secret leaks)"
        issues=$((issues + 1))
    else
        log_info ".gitignore exists"

        # Verify critical patterns
        for pattern in ".env" "mcp.json" "*.local.json"; do
            if ! grep -q "^$pattern" "$BACKUP_DIR/.gitignore"; then
                log_warn ".gitignore missing pattern: $pattern"
                issues=$((issues + 1))
            fi
        done
    fi

    if [ $issues -eq 0 ]; then
        log_info "Validation passed! Configuration is secure."
        return 0
    else
        log_error "Validation failed with $issues issues"
        return 1
    fi
}

# Main command dispatcher
main() {
    check_requirements

    case "${1:-}" in
        setup)
            setup
            ;;
        sync)
            sync
            ;;
        backup)
            backup
            ;;
        restore)
            restore
            ;;
        validate)
            validate
            ;;
        *)
            echo "Usage: $0 {setup|sync|backup|restore|validate}"
            echo ""
            echo "Commands:"
            echo "  setup    - Initial setup (Git repo + symlinks)"
            echo "  sync     - Pull latest from Git, regenerate configs"
            echo "  backup   - Push to Git + optional cloud backup"
            echo "  restore  - Restore from backup"
            echo "  validate - Verify .gitignore and secrets isolation"
            exit 1
            ;;
    esac
}

main "$@"
