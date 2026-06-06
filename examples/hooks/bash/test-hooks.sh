#!/bin/bash
# test-hooks.sh — Tests for dangerous-actions-blocker.sh and file-guard.sh
#
# Usage: bash test-hooks.sh
# Exit code: 0 if all pass, 1 if any fail

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLOCKER="$SCRIPT_DIR/dangerous-actions-blocker.sh"
GUARD="$SCRIPT_DIR/file-guard.sh"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

PASS=0
FAIL=0

# ── Payload builders ────────────────────────────────────────────────────────

bash_payload() {
    jq -n --arg cmd "$1" '{"tool_name":"Bash","tool_input":{"command":$cmd}}'
}

file_payload() {
    # $1 = tool (Read/Write/Edit), $2 = file_path
    jq -n --arg tool "$1" --arg path "$2" \
        '{"tool_name":$tool,"tool_input":{"file_path":$path}}'
}

other_payload() {
    jq -n --arg tool "$1" '{"tool_name":$tool,"tool_input":{}}'
}

# ── Assertions ───────────────────────────────────────────────────────────────

section() {
    echo ""
    echo -e "${BOLD}${BLUE}$1${NC}"
}

assert_blocks() {
    local desc="$1" hook="$2" payload="$3" envs="${4:-}"
    local exit_code=0
    echo "$payload" | env $envs bash "$hook" >/dev/null 2>&1 || exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        echo -e "  ${GREEN}✓${NC} blocks: $desc"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} blocks: $desc ${RED}— expected block, got exit 0${NC}"
        FAIL=$((FAIL + 1))
    fi
}

assert_allows() {
    local desc="$1" hook="$2" payload="$3" envs="${4:-}"
    local exit_code=0
    echo "$payload" | env $envs bash "$hook" >/dev/null 2>&1 || exit_code=$?
    if [[ $exit_code -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} allows: $desc"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} allows: $desc ${RED}— expected allow, got exit $exit_code${NC}"
        FAIL=$((FAIL + 1))
    fi
}

assert_warns() {
    # Expects exit 0 AND "Warning" in stdout
    local desc="$1" hook="$2" payload="$3"
    local exit_code=0
    local stdout
    stdout=$(echo "$payload" | bash "$hook" 2>/dev/null) || exit_code=$?
    if [[ $exit_code -eq 0 ]] && echo "$stdout" | grep -qi "warning"; then
        echo -e "  ${GREEN}✓${NC} warns:  $desc"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} warns:  $desc ${RED}— expected warning+exit 0, got exit $exit_code${NC}"
        FAIL=$((FAIL + 1))
    fi
}

# ════════════════════════════════════════════════════════════════════════════
# dangerous-actions-blocker.sh
# ════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo -e "${BOLD}  dangerous-actions-blocker.sh${NC}"
echo -e "${BOLD}═══════════════════════════════════════════${NC}"

section "1. Destructive bash commands"
assert_blocks "rm -rf /"                   "$BLOCKER" "$(bash_payload 'rm -rf /')"
assert_blocks "rm -rf ~"                   "$BLOCKER" "$(bash_payload 'rm -rf ~')"
assert_blocks "dd if= on block device"     "$BLOCKER" "$(bash_payload 'dd if=/dev/zero of=/dev/sda bs=512')"
assert_blocks "mkfs on device"             "$BLOCKER" "$(bash_payload 'mkfs.ext4 /dev/sda1')"
assert_blocks "fork bomb"                  "$BLOCKER" "$(bash_payload ':(){:|:&};:')"
assert_blocks "write to /dev/sda"          "$BLOCKER" "$(bash_payload 'cat backup.img > /dev/sda')"
assert_blocks "chmod -R 777 /"             "$BLOCKER" "$(bash_payload 'chmod -R 777 /')"
assert_blocks "chown -R"                   "$BLOCKER" "$(bash_payload 'chown -R root:root /')"
assert_blocks "sudo rm"                    "$BLOCKER" "$(bash_payload 'sudo rm /etc/passwd')"
assert_blocks "DROP DATABASE"              "$BLOCKER" "$(bash_payload 'psql -c "DROP DATABASE mydb;"')"
assert_blocks "DROP TABLE"                 "$BLOCKER" "$(bash_payload 'psql -c "DROP TABLE users;"')"
assert_blocks "--no-preserve-root"         "$BLOCKER" "$(bash_payload 'rm -rf --no-preserve-root /')"

section "2. Force push to protected branches"
assert_blocks "git push -f main"                 "$BLOCKER" "$(bash_payload 'git push -f main')"
assert_blocks "git push --force master"          "$BLOCKER" "$(bash_payload 'git push --force master')"
assert_blocks "git push origin --force main"     "$BLOCKER" "$(bash_payload 'git push origin --force main')"
assert_blocks "git push -f origin master"        "$BLOCKER" "$(bash_payload 'git push -f origin master')"

section "3. Package publication"
assert_blocks "npm publish"    "$BLOCKER" "$(bash_payload 'npm publish')"
assert_blocks "pnpm publish"   "$BLOCKER" "$(bash_payload 'pnpm publish')"
assert_blocks "yarn publish"   "$BLOCKER" "$(bash_payload 'yarn publish')"

section "4. Credential file references in bash commands (new)"
assert_blocks "cat .env"                   "$BLOCKER" "$(bash_payload 'cat .env')"
assert_blocks "cat .env.local"             "$BLOCKER" "$(bash_payload 'cat .env.local')"
assert_blocks "cat .env.production"        "$BLOCKER" "$(bash_payload 'cat .env.production')"
assert_blocks "vim ~/.aws/credentials"     "$BLOCKER" "$(bash_payload 'vim ~/.aws/credentials')"
assert_blocks "less ~/.ssh/id_rsa"         "$BLOCKER" "$(bash_payload 'less ~/.ssh/id_rsa')"
assert_blocks "less ~/.ssh/id_ed25519"     "$BLOCKER" "$(bash_payload 'less ~/.ssh/id_ed25519')"
assert_blocks "less ~/.ssh/id_ecdsa"       "$BLOCKER" "$(bash_payload 'less ~/.ssh/id_ecdsa')"
assert_blocks "cat credentials.json"       "$BLOCKER" "$(bash_payload 'cat credentials.json')"
assert_blocks "head secrets.yaml"          "$BLOCKER" "$(bash_payload 'head -n 20 secrets.yaml')"
assert_blocks "nano secrets.yml"           "$BLOCKER" "$(bash_payload 'nano secrets.yml')"
assert_blocks "cat serviceAccountKey.json" "$BLOCKER" "$(bash_payload 'cat serviceAccountKey.json')"
assert_blocks "full absolute path to .env" "$BLOCKER" "$(bash_payload 'cat /home/user/project/.env')"

section "5. Secret patterns in commands"
assert_blocks "password= in curl body"     "$BLOCKER" "$(bash_payload 'curl -d "password=mysecret" http://api.example.com')"
assert_blocks "api_key= export"            "$BLOCKER" "$(bash_payload 'export api_key=abc123')"
assert_blocks "aws_access_key in env"      "$BLOCKER" "$(bash_payload 'AWS_ACCESS_KEY=abc ./deploy.sh')"
assert_blocks "aws_secret in command"      "$BLOCKER" "$(bash_payload 'configure --aws_secret mysecret')"
assert_blocks "token= assignment"          "$BLOCKER" "$(bash_payload 'export token=ghp_abc123')"

section "6. Delete operations (warn but allow)"
assert_warns "rm -r directory"    "$BLOCKER" "$(bash_payload 'rm -r ./dist')"
assert_warns "rmdir directory"    "$BLOCKER" "$(bash_payload 'rmdir ./build')"
assert_warns "unlink symlink"     "$BLOCKER" "$(bash_payload 'unlink ./symlink')"

section "7. Allowed bash operations"
assert_allows "git status"                         "$BLOCKER" "$(bash_payload 'git status')"
assert_allows "git push to feature branch"         "$BLOCKER" "$(bash_payload 'git push origin feature-branch')"
assert_allows "git push --force non-main branch"   "$BLOCKER" "$(bash_payload 'git push --force origin feature-branch')"
assert_allows "npm install"                        "$BLOCKER" "$(bash_payload 'npm install')"
assert_allows "npm test"                           "$BLOCKER" "$(bash_payload 'npm test')"
assert_allows "npm install dotenv (no dot in name)" "$BLOCKER" "$(bash_payload 'npm install dotenv')"
assert_allows "cat .env.example (template file)"   "$BLOCKER" "$(bash_payload 'cat .env.example')"
assert_allows "cat README.md"                      "$BLOCKER" "$(bash_payload 'cat README.md')"
assert_allows "make build"                         "$BLOCKER" "$(bash_payload 'make build')"
assert_allows "docker build"                       "$BLOCKER" "$(bash_payload 'docker build -t myapp .')"
assert_allows "ls -la"                             "$BLOCKER" "$(bash_payload 'ls -la')"
assert_allows "grep in source files"               "$BLOCKER" "$(bash_payload 'grep -r "TODO" src/')"

section "8. Edit/Write — sensitive file basenames"
assert_blocks "edit .env"              "$BLOCKER" "$(file_payload 'Edit'  '/tmp/.env')"             "CLAUDE_PROJECT_DIR=/tmp"
assert_blocks "write .env.local"       "$BLOCKER" "$(file_payload 'Write' '/tmp/.env.local')"       "CLAUDE_PROJECT_DIR=/tmp"
assert_blocks "write .env.production"  "$BLOCKER" "$(file_payload 'Write' '/tmp/.env.production')"  "CLAUDE_PROJECT_DIR=/tmp"
assert_blocks "edit credentials.json"  "$BLOCKER" "$(file_payload 'Edit'  '/tmp/credentials.json')" "CLAUDE_PROJECT_DIR=/tmp"
assert_blocks "edit id_rsa"            "$BLOCKER" "$(file_payload 'Edit'  '/tmp/id_rsa')"           "CLAUDE_PROJECT_DIR=/tmp"
assert_blocks "edit secrets.yaml"      "$BLOCKER" "$(file_payload 'Edit'  '/tmp/secrets.yaml')"     "CLAUDE_PROJECT_DIR=/tmp"

section "9. Edit/Write — path restriction (outside project)"
assert_blocks "edit /etc/passwd"                  \
    "$BLOCKER" "$(file_payload 'Edit'  '/etc/passwd')"                        "CLAUDE_PROJECT_DIR=/tmp/proj"
assert_blocks "write to unrelated home directory" \
    "$BLOCKER" "$(file_payload 'Write' '/home/user/other-project/app.js')"    "CLAUDE_PROJECT_DIR=/tmp/proj"

section "10. Edit/Write — allowed paths"
assert_allows "edit source file inside project"   \
    "$BLOCKER" "$(file_payload 'Edit'  '/tmp/proj/src/app.js')"               "CLAUDE_PROJECT_DIR=/tmp/proj"
assert_allows "write to ~/.claude (settings etc)" \
    "$BLOCKER" "$(file_payload 'Write' "$HOME/.claude/settings.json")"        "CLAUDE_PROJECT_DIR=/tmp/proj"
assert_allows "write to /tmp"                     \
    "$BLOCKER" "$(file_payload 'Write' '/tmp/output.txt')"                    "CLAUDE_PROJECT_DIR=/tmp/proj"


# ════════════════════════════════════════════════════════════════════════════
# file-guard.sh
# ════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo -e "${BOLD}  file-guard.sh${NC}"
echo -e "${BOLD}═══════════════════════════════════════════${NC}"

section "11. Filename patterns — Read blocked"
assert_blocks "read .env"              "$GUARD" "$(file_payload 'Read' '/project/.env')"
assert_blocks "read .env.local"        "$GUARD" "$(file_payload 'Read' '/project/.env.local')"
assert_blocks "read .env.production"   "$GUARD" "$(file_payload 'Read' '/project/.env.production')"
assert_blocks "read .key file"         "$GUARD" "$(file_payload 'Read' '/project/server.key')"
assert_blocks "read .pem file"         "$GUARD" "$(file_payload 'Read' '/project/cert.pem')"
assert_blocks "read .p12 file"         "$GUARD" "$(file_payload 'Read' '/project/keystore.p12')"
assert_blocks "read credentials.json"  "$GUARD" "$(file_payload 'Read' '/project/credentials.json')"
assert_blocks "read secrets.yaml"      "$GUARD" "$(file_payload 'Read' '/project/secrets.yaml')"

section "12. Filename patterns — Write and Edit blocked"
assert_blocks "write .env"             "$GUARD" "$(file_payload 'Write' '/project/.env')"
assert_blocks "edit .env.local"        "$GUARD" "$(file_payload 'Edit'  '/project/.env.local')"
assert_blocks "write credentials.json" "$GUARD" "$(file_payload 'Write' '/project/credentials.json')"

section "13. Path-based patterns"
assert_blocks "read .aws/credentials (home)"   "$GUARD" "$(file_payload 'Read' "$HOME/.aws/credentials")"
assert_blocks "read .ssh/id_rsa (home)"        "$GUARD" "$(file_payload 'Read' "$HOME/.ssh/id_rsa")"
assert_blocks "read .ssh/id_ed25519"           "$GUARD" "$(file_payload 'Read' "$HOME/.ssh/id_ed25519")"
assert_blocks "read config/secrets/ subtree"   "$GUARD" "$(file_payload 'Read' '/project/config/secrets/db.yaml')"

section "14. Bypass detection"
assert_blocks 'variable expansion: $HOME/.env'          "$GUARD" "$(file_payload 'Read' '$HOME/.env')"
assert_blocks 'brace expansion: ${HOME}/.aws'           "$GUARD" "$(file_payload 'Read' '${HOME}/.aws/credentials')"
assert_blocks 'command substitution: $(pwd)/.env'       "$GUARD" "$(file_payload 'Read' '$(pwd)/.env')"

section "15. False positives — should be allowed (basename fix)"
assert_allows "dotenv.py"              "$GUARD" "$(file_payload 'Read' '/project/dotenv.py')"
assert_allows "dotenv.js"              "$GUARD" "$(file_payload 'Read' '/project/dotenv.js')"
assert_allows ".env.example (template)" "$GUARD" "$(file_payload 'Read' '/project/.env.example')"
assert_allows "my-env-config.py"       "$GUARD" "$(file_payload 'Read' '/project/my-env-config.py')"
assert_allows "README.md"              "$GUARD" "$(file_payload 'Read' '/project/README.md')"
assert_allows "src/app.ts"             "$GUARD" "$(file_payload 'Read' '/project/src/app.ts')"
assert_allows "package.json"           "$GUARD" "$(file_payload 'Read' '/project/package.json')"

section "16. Non-file tools pass through"
assert_allows "Bash tool ignored by file-guard"  "$GUARD" "$(bash_payload 'cat .env')"
assert_allows "arbitrary tool ignored"           "$GUARD" "$(other_payload 'WebSearch')"

section "17. Edge cases"
assert_allows "empty file_path"    "$GUARD" \
    "$(jq -n '{"tool_name":"Read","tool_input":{"file_path":""}}')"
assert_allows "missing file_path"  "$GUARD" \
    "$(jq -n '{"tool_name":"Read","tool_input":{}}')"

section "18. ~/.agentignore global fallback"
AGENTIGNORE_PATH="$HOME/.agentignore"
AGENTIGNORE_BACKUP=""
AGENTIGNORE_EXISTED=false

if [[ -f "$AGENTIGNORE_PATH" ]]; then
    AGENTIGNORE_EXISTED=true
    AGENTIGNORE_BACKUP=$(cat "$AGENTIGNORE_PATH")
fi

# Restore on any exit — crash-safe cleanup
_restore_agentignore() {
    if [[ "$AGENTIGNORE_EXISTED" == true ]]; then
        printf '%s' "$AGENTIGNORE_BACKUP" > "$AGENTIGNORE_PATH"
    else
        rm -f "$AGENTIGNORE_PATH"
    fi
}
trap _restore_agentignore EXIT

printf 'deploy/secrets/\ncustom-secrets.json\n' > "$AGENTIGNORE_PATH"

assert_blocks "path pattern from ~/.agentignore"      \
    "$GUARD" "$(file_payload 'Read' '/project/deploy/secrets/prod.yaml')"
assert_blocks "filename pattern from ~/.agentignore"  \
    "$GUARD" "$(file_payload 'Read' '/project/config/custom-secrets.json')"
assert_allows "non-matching file unaffected"          \
    "$GUARD" "$(file_payload 'Read' '/project/config/app.json')"

# ════════════════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════════════════

TOTAL=$((PASS + FAIL))
echo ""
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
if [[ $FAIL -eq 0 ]]; then
    echo -e "${BOLD}${GREEN}  All $TOTAL tests passed${NC}"
else
    echo -e "${BOLD}  $PASS/$TOTAL passed  ${RED}— $FAIL failed${NC}"
fi
echo -e "${BOLD}═══════════════════════════════════════════${NC}"
echo ""

[[ $FAIL -eq 0 ]]
