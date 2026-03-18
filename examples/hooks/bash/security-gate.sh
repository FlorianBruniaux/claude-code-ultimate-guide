#!/bin/bash
# Hook: PreToolUse - Security Gate
# Detects vulnerable code patterns before writing to source files.
#
# Complements dangerous-actions-blocker.sh (system-level ops).
# This hook focuses on APPLICATION security anti-patterns in code.
#
# Place in: .claude/hooks/security-gate.sh
# Register in: .claude/settings.json under PreToolUse event (Write, Edit tools)
#
# Exit 0 = allow, Exit 2 = block (stderr message shown to Claude)

set -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only check Write and Edit operations on source files
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')

# Skip non-source files (tests, docs, configs)
EXTENSION="${FILE_PATH##*.}"
SOURCE_EXTENSIONS="js ts jsx tsx py go java rb php cs"
is_source=false
for ext in $SOURCE_EXTENSIONS; do
    [[ "$EXTENSION" == "$ext" ]] && is_source=true && break
done

if [[ "$is_source" == "false" ]]; then
    exit 0
fi

# Extract content being written
if [[ "$TOOL_NAME" == "Write" ]]; then
    CONTENT=$(echo "$INPUT" | jq -r '.content // empty')
else
    # Edit: check both old and new strings
    CONTENT=$(echo "$INPUT" | jq -r '.new_string // empty')
fi

# ── PATTERN 1: Hardcoded secrets ──────────────────────────────────────────────
# Detect API keys, passwords, tokens assigned as string literals
if echo "$CONTENT" | grep -qiE '(api[_-]?key|password|secret|token|bearer)\s*=\s*["'"'"'][^"'"'"'$\{][^"'"'"']{8,}["'"'"']'; then
    echo "SECURITY-GATE: Potential hardcoded secret detected in $FILE_PATH" >&2
    echo "Use environment variables instead: process.env.MY_SECRET or os.getenv('MY_SECRET')" >&2
    exit 2
fi

# Known provider key patterns
if echo "$CONTENT" | grep -qE '(sk-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|xox[bps]-[a-zA-Z0-9\-]{20,})'; then
    echo "SECURITY-GATE: Provider API key pattern detected in source file $FILE_PATH" >&2
    echo "Move to .env and reference via environment variable." >&2
    exit 2
fi

# ── PATTERN 2: SQL injection via string interpolation ─────────────────────────
# Detect template literals or string concat in SQL context
if echo "$CONTENT" | grep -qiE '(SELECT|INSERT|UPDATE|DELETE|DROP).{0,60}(\$\{|'"'"'\s*\+\s*|"\s*\+\s*)'; then
    echo "SECURITY-GATE: Potential SQL injection pattern in $FILE_PATH" >&2
    echo "Use parameterized queries: db.query('SELECT * WHERE id = \$1', [id])" >&2
    exit 2
fi

# ── PATTERN 3: XSS via innerHTML / document.write ────────────────────────────
if echo "$CONTENT" | grep -qE '\.innerHTML\s*=\s*[^"'"'"'`]|document\.write\s*\('; then
    echo "SECURITY-GATE: Potential XSS pattern in $FILE_PATH" >&2
    echo "Use textContent instead of innerHTML, or sanitize input with DOMPurify." >&2
    exit 2
fi

# ── PATTERN 4: eval() with dynamic content ───────────────────────────────────
if echo "$CONTENT" | grep -qE 'eval\s*\(\s*[^"'"'"'`]|new\s+Function\s*\(\s*[^"'"'"'`]'; then
    echo "SECURITY-GATE: eval() or new Function() with dynamic content in $FILE_PATH" >&2
    echo "Avoid eval() with user input. Use JSON.parse() for data, or refactor logic." >&2
    exit 2
fi

# ── PATTERN 5: Weak hashing for passwords ────────────────────────────────────
if echo "$CONTENT" | grep -qiE '(md5|sha1|sha256)\s*\(.*password|hashlib\.(md5|sha1)\s*\(.*password'; then
    echo "SECURITY-GATE: Weak hash algorithm for password in $FILE_PATH" >&2
    echo "Use bcrypt, argon2, or scrypt for password hashing." >&2
    exit 2
fi

# ── PATTERN 6: Command injection via exec/shell ───────────────────────────────
if echo "$CONTENT" | grep -qE '(exec|shell_exec|system|popen|subprocess\.call)\s*\([^"'"'"'`].*(\$\{|'"'"'\s*\+|"\s*\+)'; then
    echo "SECURITY-GATE: Potential command injection in $FILE_PATH" >&2
    echo "Use parameterized subprocess calls, never interpolate user input into shell commands." >&2
    exit 2
fi

# ── PATTERN 7: Path traversal via user input ─────────────────────────────────
if echo "$CONTENT" | grep -qE '(readFile|open|fopen|path\.join)\s*\([^)]*req\.(params|query|body)'; then
    echo "SECURITY-GATE: Potential path traversal — user input in file path operation ($FILE_PATH)" >&2
    echo "Validate and sanitize file paths. Use path.resolve() + check against allowed base directory." >&2
    exit 2
fi

# Allow by default
exit 0
