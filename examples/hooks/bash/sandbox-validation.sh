#!/bin/bash
#
# Sandbox Validation Hook (PreToolUse)
#
# Purpose: Verify native sandbox is active before executing bash commands in production/untrusted environments
# Event: PreToolUse
# Blocking: Yes (exit 2 blocks command execution)
#
# Installation:
#   1. Copy to .claude/hooks/sandbox-validation.sh
#   2. chmod +x .claude/hooks/sandbox-validation.sh
#   3. Configure in settings.json:
#      {
#        "hooks": {
#          "PreToolUse": [{
#            "matcher": "Bash",
#            "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/sandbox-validation.sh" }]
#          }]
#        }
#      }
#
# Input (JSON on stdin, like every hook): tool_name and tool_input. This hook reads
# tool_input.dangerouslyDisableSandbox, the Bash parameter Claude sets to retry a
# command outside the sandbox.
#
# Limit: the hook sees the tool call, not the sandbox state. It checks the request
# flag and whether the platform sandbox binary exists, not that the sandbox is
# running. To enforce the sandbox, set sandbox.enabled and
# sandbox.allowUnsandboxedCommands: false in settings instead.
#
# Exit Codes:
#   0 = Allow (sandbox active or check disabled)
#   2 = Block (sandbox not active in strict mode)

set -euo pipefail

# Configuration
STRICT_MODE="${SANDBOX_VALIDATION_STRICT:-false}"  # Set to "true" to require sandbox in production
PRODUCTION_MARKER="${SANDBOX_VALIDATION_MARKER:-.production}"  # File marker for production environments

# Read the hook input from stdin
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only validate Bash tool
if [ "$TOOL_NAME" != "Bash" ]; then
  exit 0
fi

# Check if production environment
is_production() {
  [ -f "$PRODUCTION_MARKER" ] || [ "${ENVIRONMENT:-}" = "production" ]
}

# Check if sandbox is active
is_sandbox_active() {
  # Parse tool parameters to check for dangerouslyDisableSandbox
  if echo "$INPUT" | jq -e '.tool_input.dangerouslyDisableSandbox == true' >/dev/null 2>&1; then
    return 1  # Sandbox explicitly disabled
  fi

  # Platform-specific checks
  case "$OSTYPE" in
    darwin*)
      # macOS: Check if Seatbelt is available
      if command -v sandbox-exec >/dev/null 2>&1; then
        return 0
      fi
      ;;
    linux*)
      # Linux: Check if bubblewrap is available (the binary is named bwrap)
      if command -v bwrap >/dev/null 2>&1; then
        return 0
      fi
      ;;
  esac

  return 1  # Sandbox not available
}

# Main validation logic
main() {
  # Skip validation if not in strict mode and not production
  if [ "$STRICT_MODE" != "true" ] && ! is_production; then
    exit 0
  fi

  # Check sandbox status
  if ! is_sandbox_active; then
    echo "❌ SANDBOX VALIDATION FAILED" >&2
    echo "" >&2
    echo "Reason: Native sandbox not active for bash command" >&2
    echo "" >&2

    # Platform-specific guidance
    case "$OSTYPE" in
      darwin*)
        echo "macOS: Seatbelt should be built-in. Check Claude Code installation." >&2
        ;;
      linux*)
        echo "Linux: Install bubblewrap and socat:" >&2
        echo "  sudo apt-get install bubblewrap socat  # Ubuntu/Debian" >&2
        echo "  sudo dnf install bubblewrap socat      # Fedora" >&2
        ;;
      *)
        echo "Platform: $OSTYPE (sandbox may not be supported)" >&2
        ;;
    esac

    echo "" >&2
    echo "Options:" >&2
    echo "  1. Enable sandbox: /sandbox command in Claude Code" >&2
    echo "  2. Disable validation: Set SANDBOX_VALIDATION_STRICT=false" >&2
    echo "  3. Remove production marker: rm $PRODUCTION_MARKER" >&2
    echo "" >&2

    if [ "$STRICT_MODE" = "true" ]; then
      echo "⛔ Command BLOCKED (strict mode enabled)" >&2
      exit 2  # Block command execution
    else
      echo "⚠️  Command ALLOWED (production environment detected but strict mode disabled)" >&2
      exit 0  # Allow with warning
    fi
  fi

  # Sandbox active - allow command
  exit 0
}

main
