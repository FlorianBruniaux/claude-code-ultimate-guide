#!/usr/bin/env bash
#
# File: tts-selective.sh
# Purpose: Selective TTS hook - Speak only specific types of messages
# Event: Notification (reads the `message` field). To read the end of each turn
# aloud instead, register it on Stop and read `last_assistant_message`.
#
# Usage: Replace .claude/hooks/play-tts.sh with this script for selective TTS
#
# Example configurations:
# - Errors only: Speak only when "error" or "failed" detected
# - Success only: Speak only when "success" or "completed" detected
# - Important only: Speak only high-priority notifications
#
# Installation:
#   1. Copy this file to .claude/hooks/
#   2. chmod +x .claude/hooks/tts-selective.sh
#   3. Backup original: cp .claude/hooks/play-tts.sh .claude/hooks/play-tts.sh.backup
#   4. Replace: cp .claude/hooks/tts-selective.sh .claude/hooks/play-tts.sh
#
# Restore original:
#   cp .claude/hooks/play-tts.sh.backup .claude/hooks/play-tts.sh
#

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read input from stdin
INPUT=$(cat)
BODY=$(echo "$INPUT" | jq -r '.message // empty')

# Exit if no body
if [[ -z "$BODY" ]]; then
  exit 0
fi

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION: Customize trigger patterns below
# ═══════════════════════════════════════════════════════════════

# Option 1: Errors Only
# Speak only when message contains error keywords
TRIGGER_PATTERN="(error|Error|ERROR|failed|Failed|FAILED|exception|Exception)"

# Option 2: Success Only (uncomment to use)
# TRIGGER_PATTERN="(success|Success|completed|Completed|done|Done|✓|✅)"

# Option 3: Important Only (uncomment to use)
# TRIGGER_PATTERN="(CRITICAL|WARNING|ERROR|FAILURE|BREAKING)"

# Option 4: Code-related Only (uncomment to use)
# TRIGGER_PATTERN="(test|tests|build|compile|deploy|commit|push|merge)"

# Option 5: Custom Keywords (uncomment and edit)
# TRIGGER_PATTERN="(production|deploy|release|urgent|critical)"

# ═══════════════════════════════════════════════════════════════
# LOGIC: Check if message matches trigger pattern
# ═══════════════════════════════════════════════════════════════

if [[ "$BODY" =~ $TRIGGER_PATTERN ]]; then
  # Message matches trigger - speak it

  # Call original TTS hook (or Agent Vibes play-tts.sh)
  if [[ -f "$SCRIPT_DIR/play-tts.sh.backup" ]]; then
    # Use backup if exists
    "$SCRIPT_DIR/play-tts.sh.backup" "$BODY"
  elif [[ -f ~/.claude/hooks/play-tts.sh ]]; then
    # Use global Agent Vibes hook
    ~/.claude/hooks/play-tts.sh "$BODY"
  else
    # Fallback: macOS Say
    say "$BODY" &
  fi
else
  # Message doesn't match trigger - silent exit
  exit 0
fi

exit 0
