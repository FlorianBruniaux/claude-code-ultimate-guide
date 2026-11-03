#!/bin/bash
# test-private-key-detection.sh - Tests that the secret hooks detect a private key header
#
# Regression: a grep pattern that starts with "-----" was read as an option
# (exit 2, "unrecognized option") when passed without -e, and the error was
# hidden by `|| true` / `2>/dev/null`, so private keys were never reported.
#
# Covers: pre-commit-secrets.sh, output-secrets-scanner.sh, output-validator.sh
# Needs: bash, git, jq
# Usage: bash examples/hooks/bash/test-private-key-detection.sh
# Exit code: 0 if all pass, 1 if any fail
#
# The key material below is a fake header followed by filler text, never a real key.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRE_COMMIT="$SCRIPT_DIR/pre-commit-secrets.sh"
SCANNER="$SCRIPT_DIR/output-secrets-scanner.sh"
VALIDATOR="$SCRIPT_DIR/output-validator.sh"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/private-key-test.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0

check() {
    local desc="$1" ok="$2" detail="${3:-}"
    if [[ "$ok" == "1" ]]; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ${detail:+($detail)}"
        FAIL=$((FAIL + 1))
    fi
}

# Fake key: header line + filler. Not a real key.
FAKE_KEY=$'-----BEGIN RSA PRIVATE KEY-----\nnot-a-real-key-just-filler-text\n-----END RSA PRIVATE KEY-----'

# A grep that always fails with exit 2, to prove a grep error is not read as "clean"
mkdir -p "$WORK/badgrep"
printf '#!/bin/sh\nexit 2\n' > "$WORK/badgrep/grep"
chmod +x "$WORK/badgrep/grep"

echo "pre-commit-secrets.sh"
REPO="$WORK/repo"
git init -q "$REPO"
printf '%s\n' "$FAKE_KEY" > "$REPO/server.conf"
git -C "$REPO" add server.conf
rc=0
out=$(cd "$REPO" && bash "$PRE_COMMIT" 2>&1) || rc=$?
check "blocks a staged private key header" "$([[ $rc -ne 0 && "$out" == *"Private Key"* ]] && echo 1 || echo 0)" "exit $rc"
rc=0
out=$(cd "$REPO" && PATH="$WORK/badgrep:$PATH" bash "$PRE_COMMIT" 2>&1) || rc=$?
check "reports a grep failure instead of staying silent" "$([[ "$out" == *"grep failed"* ]] && echo 1 || echo 0)" "exit $rc"

echo "output-secrets-scanner.sh"
payload=$(jq -n --arg o "$FAKE_KEY" '{"tool_name":"Bash","tool_output":$o}')
rc=0
out=$(echo "$payload" | bash "$SCANNER" 2>/dev/null) || rc=$?
# The "Private Key Inline" pattern also matches this input; require the dedicated
# "Private Key" entry (followed by "," or "." in the message), not that substring.
check "warns on a private key header in tool output" "$([[ "$out" =~ Private\ Key(,|\.) ]] && echo 1 || echo 0)" "stdout: ${out:0:120}"
out=$(echo "$payload" | PATH="$WORK/badgrep:$PATH" bash "$SCANNER" 2>/dev/null) || true
check "reports a grep failure instead of staying silent" "$([[ "$out" == *"SCAN INCOMPLETE"* ]] && echo 1 || echo 0)" "stdout: ${out:0:80}"

echo "output-validator.sh"
payload=$(jq -n --arg o "$FAKE_KEY" '{"tool_name":"Bash","tool_output":$o}')
out=$(echo "$payload" | bash "$VALIDATOR" 2>/dev/null) || true
check "warns on a private key header in tool output" "$([[ "$out" == *"pattern: -----BEGIN"* ]] && echo 1 || echo 0)" "stdout: ${out:0:80}"
out=$(echo "$payload" | PATH="$WORK/badgrep:$PATH" bash "$VALIDATOR" 2>/dev/null) || true
check "reports a grep failure instead of staying silent" "$([[ "$out" == *"Secret scan failed"* ]] && echo 1 || echo 0)" "stdout: ${out:0:80}"

echo ""
echo "$PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
