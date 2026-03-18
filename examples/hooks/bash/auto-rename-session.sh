#!/bin/bash
# .claude/hooks/auto-rename-session.sh
# Event: SessionEnd
# Automatically generates a descriptive title for each session when it ends.
#
# Strategy:
#   1. Reads the session JSONL from ~/.claude/projects/ (via session_id from stdin or env)
#   2. Extracts the first 3 user messages as context
#   3. Calls claude-haiku-4-5 to generate a 4-6 word title (verb + subject)
#   4. Falls back to a sanitized version of the first message if Haiku fails
#   5. Updates sessions-index.jsonl (custom index) and the JSONL slug (for /resume)
#
# Requirements:
#   - python3 (standard on macOS/Linux)
#   - claude CLI on PATH (for AI title generation; fallback works without it)
#
# Wire up in .claude/settings.json:
#   {
#     "hooks": {
#       "SessionEnd": [
#         {
#           "matcher": "",
#           "hooks": [{ "type": "command", "command": "~/.claude/hooks/auto-rename-session.sh" }]
#         }
#       ]
#     }
#   }
#
# Configuration:
#   SESSION_AUTORENAME=0   Disable this hook for a specific session
#
# Note: Output goes to /dev/tty (or /dev/stderr as fallback) to avoid interfering
# with Claude Code's JSON parsing of hook stdout.

set -uo pipefail

# Route output to tty so it doesn't pollute Claude Code's JSON parsing of stdout
if (echo -n "" > /dev/tty) 2>/dev/null; then
    OUT="/dev/tty"
else
    OUT="/dev/stderr"
fi

# Opt-out mechanism: set SESSION_AUTORENAME=0 in your shell or .env to skip
[[ "${SESSION_AUTORENAME:-1}" == "0" ]] && exit 0

# ---------------------------------------------------------------------------
# Step 1: Resolve session_id and working directory
# ---------------------------------------------------------------------------
# Claude Code passes a JSON payload on stdin with session_id and cwd.
# If stdin was already consumed by a preceding hook, fall back to env vars.

INPUT=$(cat 2>/dev/null || true)

SESSION_ID=""
CWD=""

if [[ -n "$INPUT" ]]; then
    SESSION_ID=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('session_id', ''))
except: pass
" 2>/dev/null || true)

    CWD=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('cwd', ''))
except: pass
" 2>/dev/null || true)
fi

# Fall back to environment variables if stdin parsing yielded nothing
[[ -z "$SESSION_ID" ]] && SESSION_ID="${CLAUDE_SESSION_ID:-}"
[[ -z "$CWD" ]] && CWD="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[[ -z "$CWD" ]] && CWD="$(pwd)"

# ---------------------------------------------------------------------------
# Step 2: Locate the session JSONL file
# ---------------------------------------------------------------------------
# Claude Code stores sessions under ~/.claude/projects/<url-encoded-cwd>/<session_id>.jsonl

PROJECT_SLUG=$(echo "$CWD" | sed 's|/|-|g')
PROJECTS_DIR="$HOME/.claude/projects/$PROJECT_SLUG"

JSONL_FILE=""

if [[ -n "$SESSION_ID" && -f "$PROJECTS_DIR/$SESSION_ID.jsonl" ]]; then
    JSONL_FILE="$PROJECTS_DIR/$SESSION_ID.jsonl"
elif [[ -d "$PROJECTS_DIR" ]]; then
    # No explicit session_id: pick the most recently modified JSONL (excluding agent files)
    JSONL_FILE=$(ls -t "$PROJECTS_DIR"/*.jsonl 2>/dev/null | grep -v '/agent-' | head -1 || true)
    [[ -n "$JSONL_FILE" ]] && SESSION_ID=$(basename "$JSONL_FILE" .jsonl)
fi

[[ -z "$JSONL_FILE" || ! -f "$JSONL_FILE" ]] && exit 0

# Read the current slug so we can detect whether it changed later
CURRENT_SLUG=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    for line in f:
        try:
            obj = json.loads(line)
            s = obj.get('slug', '')
            if s: print(s); break
        except: pass
" "$JSONL_FILE" 2>/dev/null || true)

# ---------------------------------------------------------------------------
# Step 3: Extract the first 3 user messages as context
# ---------------------------------------------------------------------------
# Skips tool result blobs (<...), slash commands (/...), and messages longer
# than 250 characters to keep the prompt tight.

CONTEXT=$(python3 -c "
import json, sys

jsonl_file = sys.argv[1]
messages = []

with open(jsonl_file) as f:
    for line in f:
        try:
            obj = json.loads(line)
            if obj.get('type') != 'user':
                continue
            content = obj.get('message', {}).get('content', '')
            if not isinstance(content, str):
                continue
            content = content.strip()
            if content.startswith('<') or content.startswith('/'):
                continue
            messages.append(content[:250])
            if len(messages) >= 3:
                break
        except:
            continue

print('\n---\n'.join(messages))
" "$JSONL_FILE" 2>/dev/null || true)

[[ -z "$CONTEXT" ]] && exit 0

FIRST_MSG=$(echo "$CONTEXT" | head -1 | head -c 60)

# ---------------------------------------------------------------------------
# Step 4: Generate a title via Haiku (with plaintext fallback)
# ---------------------------------------------------------------------------

TITLE=""
TITLE_SOURCE="fallback"

PROMPT="Generate a 4-6 word lowercase English title summarizing this Claude Code session. Format: verb + subject (e.g. 'fix auth bug postgres', 'add stripe webhook handler', 'eval session labels tool'). Reply with ONLY the title, nothing else.

Session messages:
$CONTEXT"

if command -v claude &>/dev/null; then
    # CLAUDECODE is unset to prevent the subprocess from inheriting hook context,
    # which could cause unexpected behaviour or infinite loops.
    TITLE=$(printf '%s' "$PROMPT" \
        | env -u CLAUDECODE timeout 12 claude -p --model claude-haiku-4-5-20251001 2>/dev/null \
        | head -1 \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[^a-z0-9 ]//g' \
        | sed 's/  */ /g' \
        | sed 's/^ //;s/ $//' \
        | head -c 60 \
        || true)
    [[ -n "$TITLE" ]] && TITLE_SOURCE="haiku"
fi

# Fallback: sanitize the first user message into a slug-friendly string
if [[ -z "$TITLE" ]]; then
    TITLE=$(echo "$FIRST_MSG" \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/[^a-z0-9 ]/ /g' \
        | sed 's/  */ /g' \
        | sed 's/^ //;s/ $//' \
        | head -c 55 \
        || true)
fi

[[ -z "$TITLE" ]] && exit 0

SLUG=$(echo "$TITLE" | sed 's/ /-/g' | sed 's/[^a-z0-9-]//g')

# ---------------------------------------------------------------------------
# Step 5: Persist the title
# ---------------------------------------------------------------------------

# 5a. Update sessions-index.jsonl (used by custom session browsers / tooling)
python3 -c "
import json, os, sys

index_path = os.path.expanduser('~/.claude/sessions-index.jsonl')
session_id = sys.argv[1]
title = sys.argv[2]

try:
    with open(index_path) as f:
        entries = [json.loads(line) for line in f if line.strip()]
    for entry in entries:
        if entry['id'] == session_id:
            entry['context'] = title
            break
    with open(index_path, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')
except:
    pass
" "$SESSION_ID" "$TITLE" 2>/dev/null || true

# 5b. Update the slug field inside the JSONL so /resume shows the new title
if [[ -n "$CURRENT_SLUG" && -n "$SLUG" && "$CURRENT_SLUG" != "$SLUG" ]]; then
    TMPFILE=$(mktemp)
    python3 -c "
import json, sys

jsonl_file, old_slug, new_slug = sys.argv[1], sys.argv[2], sys.argv[3]

with open(jsonl_file) as f:
    lines = f.readlines()

out = []
for line in lines:
    try:
        obj = json.loads(line)
        if obj.get('slug') == old_slug:
            obj['slug'] = new_slug
        out.append(json.dumps(obj, separators=(',', ':')))
    except:
        out.append(line.rstrip())

print('\n'.join(out))
" "$JSONL_FILE" "$CURRENT_SLUG" "$SLUG" > "$TMPFILE" 2>/dev/null

    [[ -s "$TMPFILE" ]] && mv "$TMPFILE" "$JSONL_FILE" || rm -f "$TMPFILE"
fi

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo "" > "$OUT"
echo "Session renamed: \"$TITLE\" ($TITLE_SOURCE)" > "$OUT"
echo "" > "$OUT"

exit 0
