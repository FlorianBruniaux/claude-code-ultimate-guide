#!/bin/bash
# governance-enforcement-hook.sh
# Event: SessionStart
#
# Validates active Claude Code MCP configuration against the org's approved registry.
# Warns about unapproved MCPs and checks that security deny rules are in place.
#
# Related: guide/security/enterprise-governance.md §3.3 and §5
#
# Installation:
#   cp governance-enforcement-hook.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/governance-enforcement-hook.sh
#
#   Then add to ~/.claude/settings.json:
#   {
#     "hooks": {
#       "SessionStart": ["~/.claude/hooks/governance-enforcement-hook.sh"]
#     }
#   }
#
# Or in project .claude/settings.json:
#   {
#     "hooks": {
#       "SessionStart": [".claude/hooks/governance-enforcement-hook.sh"]
#     }
#   }

set -euo pipefail

SETTINGS_FILE="${HOME}/.claude.json"
REGISTRY_FILE="${PWD}/.claude/mcp-registry.yaml"
PROJECT_SETTINGS="${PWD}/.claude/settings.json"

# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────

warn() { echo "GOVERNANCE WARNING: $*" >&2; }
info() { echo "GOVERNANCE: $*" >&2; }

has_command() { command -v "$1" &>/dev/null; }

# ─────────────────────────────────────────────────────────────────
# Check 1: Project governance config present
# ─────────────────────────────────────────────────────────────────

check_project_config() {
  if [[ ! -f "$PROJECT_SETTINGS" ]]; then
    warn "No .claude/settings.json in project. Governance not applied to this repo."
    warn "Set up governance: see guide/security/enterprise-governance.md"
    return
  fi

  # Check that deny rules exist for secrets
  if has_command jq; then
    local has_deny
    has_deny=$(jq -e '.permissions.deny // [] | length' "$PROJECT_SETTINGS" 2>/dev/null || echo "0")
    if [[ "$has_deny" == "0" ]]; then
      warn "No permissions.deny rules in .claude/settings.json."
      warn "Add deny rules for .env, *.key, *.pem files."
    fi

    # Check for dangerous allow rules
    local dangerous_allows
    dangerous_allows=$(jq -r '.permissions.allow[]? // ""' "$PROJECT_SETTINGS" 2>/dev/null | \
      grep -iE '(env|secret|credential|password|token|key)' || true)
    if [[ -n "$dangerous_allows" ]]; then
      warn "DANGEROUS: permissions.allow contains sensitive patterns:"
      echo "$dangerous_allows" | while read -r line; do
        warn "  Allowed: $line"
      done
    fi
  fi
}

# ─────────────────────────────────────────────────────────────────
# Check 2: MCP registry compliance
# ─────────────────────────────────────────────────────────────────

check_mcp_registry() {
  if [[ ! -f "$REGISTRY_FILE" ]]; then
    # No registry = no enforcement (opt-in)
    return
  fi

  if ! has_command jq || ! has_command yq; then
    warn "jq or yq not installed — cannot check MCP registry compliance."
    warn "Install: brew install jq yq"
    return
  fi

  if [[ ! -f "$SETTINGS_FILE" ]]; then
    return
  fi

  # Get active MCPs
  local active_mcps
  active_mcps=$(jq -r '.mcpServers // {} | keys[]' "$SETTINGS_FILE" 2>/dev/null || true)

  if [[ -z "$active_mcps" ]]; then
    return
  fi

  # Get approved MCPs from registry
  local approved_mcps
  approved_mcps=$(yq e '.approved[].name' "$REGISTRY_FILE" 2>/dev/null || true)

  # Compare
  local unapproved=()
  while IFS= read -r mcp; do
    if [[ -n "$mcp" ]] && ! echo "$approved_mcps" | grep -q "^${mcp}$"; then
      unapproved+=("$mcp")
    fi
  done <<< "$active_mcps"

  if [[ ${#unapproved[@]} -gt 0 ]]; then
    warn "Unapproved MCP servers detected:"
    for mcp in "${unapproved[@]}"; do
      warn "  - $mcp (not in .claude/mcp-registry.yaml)"
    done
    warn "Submit approval request per your org's AI usage charter."
    warn "Session continues — remediate within 48 hours per policy."
  else
    info "MCP registry check passed. All MCPs approved."
  fi

  # Check for expired approvals
  local today
  today=$(date +%Y-%m-%d)
  while IFS= read -r name; do
    local expires
    expires=$(yq e ".approved[] | select(.name == \"$name\") | .expires" "$REGISTRY_FILE" 2>/dev/null || true)
    if [[ -n "$expires" && "$expires" < "$today" ]]; then
      warn "MCP '$name' approval expired on $expires. Re-approval required."
    fi
  done <<< "$approved_mcps"
}

# ─────────────────────────────────────────────────────────────────
# Check 3: Data classification context
# ─────────────────────────────────────────────────────────────────

check_data_classification() {
  # Detect sensitive files in working directory
  local sensitive_patterns=(".env" "*.pem" "*.key" "secrets/" "credentials")
  local found_sensitive=()

  for pattern in "${sensitive_patterns[@]}"; do
    if compgen -G "${PWD}/${pattern}" &>/dev/null 2>/dev/null; then
      found_sensitive+=("$pattern")
    fi
  done

  if [[ ${#found_sensitive[@]} -gt 0 ]]; then
    info "Sensitive file patterns detected in working directory:"
    for f in "${found_sensitive[@]}"; do
      info "  - $f"
    done
    info "Verify .claude/settings.json deny rules cover these files."
  fi
}

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

main() {
  check_project_config
  check_mcp_registry
  check_data_classification

  # Always exit 0 — governance hook warns but does not block session start
  # Blocking at SessionStart creates too much friction; use periodic audits instead
  exit 0
}

main
