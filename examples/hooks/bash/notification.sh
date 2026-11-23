#!/bin/bash
# Hook: Notification - macOS alerts with contextual sounds
# Plays different sound based on notification type
#
# Place in: .claude/hooks/notification.sh
# Register in: .claude/settings.json under Notification event (optionally with a
# matcher such as "permission_prompt|idle_prompt" to filter by notification type)
#
# Input fields read: message, title (notification_type is also available)
#
# Note: macOS only - requires afplay and osascript

set -e

# Read JSON from stdin
INPUT=$(cat)

# Extract message and title
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude Code Notification"')
TITLE=$(echo "$INPUT" | jq -r '.title // "Claude Code"')

# Select sound based on context
select_sound() {
    local msg="$1"
    local msg_lower
    msg_lower=$(echo "$msg" | tr '[:upper:]' '[:lower:]')

    # Success / Completion
    if echo "$msg_lower" | grep -qE "(completed|terminé|fini|done|success|réussi|validé|finished)"; then
        echo "/System/Library/Sounds/Hero.aiff"
        return
    fi

    # Error / Failure
    if echo "$msg_lower" | grep -qE "(error|erreur|failed|échec|échoué|problem|problème|failure)"; then
        echo "/System/Library/Sounds/Basso.aiff"
        return
    fi

    # Waiting / Permission
    if echo "$msg_lower" | grep -qE "(waiting|attente|permission|approval|input|question|prompt)"; then
        echo "/System/Library/Sounds/Submarine.aiff"
        return
    fi

    # Warning / Attention
    if echo "$msg_lower" | grep -qE "(warning|attention|caution|alert|avertissement)"; then
        echo "/System/Library/Sounds/Sosumi.aiff"
        return
    fi

    # Default
    echo "/System/Library/Sounds/Ping.aiff"
}

SOUND_FILE=$(select_sound "$MESSAGE")

# Play sound (in background to avoid blocking)
if [[ -f "$SOUND_FILE" ]]; then
    afplay "$SOUND_FILE" &
fi

# Display macOS notification. Escape backslashes and double quotes so the text
# cannot break out of the AppleScript string literal.
MESSAGE_ESC=${MESSAGE//\\/\\\\}
MESSAGE_ESC=${MESSAGE_ESC//\"/\\\"}
TITLE_ESC=${TITLE//\\/\\\\}
TITLE_ESC=${TITLE_ESC//\"/\\\"}
osascript -e "display notification \"$MESSAGE_ESC\" with title \"$TITLE_ESC\" sound name \"\"" 2>/dev/null || true

exit 0
