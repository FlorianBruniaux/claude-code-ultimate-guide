#!/bin/bash
# privacy-warning.sh - Warn users about data sent to Anthropic
#
# Hook type: SessionStart
# Triggers: At the start of a new session (matcher "startup")
#
# Purpose:
#   Reminds users that their prompts, files, and MCP results are sent to Anthropic.
#   Provides link to opt-out of training data (reduces retention from 5 years to 30 days).
#
# Output: a `systemMessage` JSON object, which Claude Code shows to the user.
# Plain stdout from a SessionStart hook is added to Claude's context instead, so it
# would never reach the person this reminder is for.
#
# Installation:
#   1. Copy to ~/.claude/hooks/ and make it executable: chmod +x privacy-warning.sh
#   2. Register in ~/.claude/settings.json:
#      {
#        "hooks": {
#          "SessionStart": [{
#            "matcher": "startup",
#            "hooks": [{ "type": "command", "command": "~/.claude/hooks/privacy-warning.sh" }]
#          }]
#        }
#      }
#
# Reference: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/security/data-privacy.md

cat > /dev/null  # consume stdin

jq -n '{systemMessage: "PRIVACY REMINDER\nYour prompts, files, and MCP results are sent to Anthropic.\nRetention: 5 years (default), 30 days (training opt-out).\nDisable training: claude.ai/settings/data-privacy-controls"}'

exit 0
