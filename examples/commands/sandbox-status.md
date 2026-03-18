---
name: sandbox-status
description: Display native sandbox status, configuration, and recent violations
---

# Sandbox Status Command

Inspect the native Claude Code sandbox state, active configuration, and security events.

## Usage

```
/sandbox-status
```

## What It Does

1. **Check sandbox availability**
   - Verify OS primitives installed (bubblewrap on Linux, Seatbelt on macOS)
   - Display platform support status

2. **Show active configuration**
   - Sandbox mode (Auto-allow vs Regular permissions)
   - Filesystem policies (allowed writes, denied reads)
   - Network policies (domain allowlist/denylist)
   - Excluded commands

3. **List recent sandbox violations**
   - Blocked filesystem access attempts
   - Blocked network connections
   - Escape hatch invocations (`dangerouslyDisableSandbox`)

## Implementation

```bash
#!/bin/bash

echo "=== Native Sandbox Status ==="
echo

# 1. Platform Check
echo "Platform:"
case "$OSTYPE" in
  darwin*)
    echo "  ✅ macOS (Seatbelt built-in)"
    ;;
  linux*)
    if which bubblewrap >/dev/null 2>&1; then
      echo "  ✅ Linux (bubblewrap installed)"
      bubblewrap --version 2>/dev/null | head -1
    else
      echo "  ❌ Linux (bubblewrap NOT installed)"
      echo "     Install: sudo apt-get install bubblewrap socat"
    fi
    if which socat >/dev/null 2>&1; then
      echo "  ✅ socat installed"
    else
      echo "  ❌ socat NOT installed"
    fi
    ;;
  *)
    echo "  ❌ Unsupported platform: $OSTYPE"
    ;;
esac
echo

# 2. Configuration
echo "Configuration (from settings.json):"
if [ -f .claude/settings.json ]; then
  CONFIG=".claude/settings.json"
elif [ -f ~/.claude/settings.json ]; then
  CONFIG="~/.claude/settings.json"
else
  echo "  ⚠️  No settings.json found"
  CONFIG=""
fi

if [ -n "$CONFIG" ]; then
  echo "  Source: $CONFIG"

  # Auto-allow mode
  AUTO_ALLOW=$(jq -r '.sandbox.autoAllowMode // "not set"' "$CONFIG" 2>/dev/null)
  echo "  Auto-allow: $AUTO_ALLOW"

  # Allowed write paths
  WRITE_PATHS=$(jq -r '.sandbox.filesystem.allowedWritePaths[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Allowed writes: ${WRITE_PATHS:-not set}"

  # Denied read paths
  DENIED_READS=$(jq -r '.sandbox.filesystem.deniedReadPaths[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Denied reads: ${DENIED_READS:-not set}"

  # Network policy
  NET_POLICY=$(jq -r '.sandbox.network.policy // "not set"' "$CONFIG" 2>/dev/null)
  echo "  Network policy: $NET_POLICY"

  # Allowed domains
  DOMAINS=$(jq -r '.sandbox.network.allowedDomains[]? // empty' "$CONFIG" 2>/dev/null | head -3 | tr '\n' ', ')
  DOMAINS_COUNT=$(jq -r '.sandbox.network.allowedDomains | length' "$CONFIG" 2>/dev/null)
  if [ -n "$DOMAINS" ]; then
    echo "  Allowed domains: $DOMAINS... ($DOMAINS_COUNT total)"
  else
    echo "  Allowed domains: not set"
  fi

  # Excluded commands
  EXCLUDED=$(jq -r '.sandbox.excludedCommands[]? // empty' "$CONFIG" 2>/dev/null | tr '\n' ', ')
  echo "  Excluded commands: ${EXCLUDED:-not set}"
fi
echo

# 3. Recent Violations (placeholder - actual implementation would read Claude Code logs)
echo "Recent sandbox violations:"
echo "  ℹ️  Log inspection not yet implemented"
echo "  Tip: Check Claude Code session logs for sandbox violation notifications"
echo

# 4. Open-Source Runtime
echo "Open-Source Runtime:"
if which npx >/dev/null 2>&1; then
  echo "  ✅ npx available - can use @anthropic-ai/sandbox-runtime"
  echo "  Usage: npx @anthropic-ai/sandbox-runtime <command>"
else
  echo "  ⚠️  npx not found (install Node.js)"
fi
echo

# 5. Documentation
echo "Documentation:"
echo "  Guide: guide/sandbox-native.md"
echo "  Official: https://code.claude.com/docs/en/sandboxing"
echo "  Runtime: https://github.com/anthropic-experimental/sandbox-runtime"
```

## Example Output

```
=== Native Sandbox Status ===

Platform:
  ✅ macOS (Seatbelt built-in)

Configuration (from settings.json):
  Source: .claude/settings.json
  Auto-allow: true
  Allowed writes: ${CWD}, /tmp
  Denied reads: ${HOME}/.ssh, ${HOME}/.aws, ${HOME}/.kube
  Network policy: deny
  Allowed domains: api.anthropic.com, registry.npmjs.com, github.com... (9 total)
  Excluded commands: docker, kubectl, podman

Recent sandbox violations:
  ℹ️  Log inspection not yet implemented
  Tip: Check Claude Code session logs for sandbox violation notifications

Open-Source Runtime:
  ✅ npx available - can use @anthropic-ai/sandbox-runtime
  Usage: npx @anthropic-ai/sandbox-runtime <command>

Documentation:
  Guide: guide/sandbox-native.md
  Official: https://code.claude.com/docs/en/sandboxing
  Runtime: https://github.com/anthropic-experimental/sandbox-runtime
```

## Use Cases

- **Pre-deployment**: Verify sandbox config before running autonomous workflows
- **Debugging**: Investigate why certain commands are blocked
- **Security audit**: Review allowed domains and filesystem access
- **Onboarding**: Help new team members understand project sandbox policy

## See Also

- [Native Sandboxing Guide](../../guide/sandbox-native.md) - Complete technical reference
- [Sandbox Validation Hook](../hooks/bash/sandbox-validation.sh) - Pre-command validation
- [Sandbox Config Example](../config/sandbox-native.json) - Production-ready settings
