#!/bin/bash
# session-summary-config.sh
# CLI configuration tool for session-summary.sh hook
# Manages section toggles, section order, and provides utility commands
#
# Compatible with Bash 3.2+ (macOS default) - no associative arrays
#
# Usage:
#   session-summary-config show              # Show current config with section status
#   session-summary-config set KEY=VALUE     # Set a config value (e.g., git=1, errors=0)
#   session-summary-config reset             # Reset to defaults
#   session-summary-config sections          # Show current section order
#   session-summary-config sections "a,b,c"  # Set section order
#   session-summary-config preview           # Show demo output with current config
#   session-summary-config install           # Install hooks in ~/.claude/settings.json
#   session-summary-config log [n]           # Show last n session summaries (default: 5)
#
# Config file: ~/.config/session-summary/config.sh

set -euo pipefail

CONFIG_DIR="${HOME}/.config/session-summary"
CONFIG_FILE="${CONFIG_DIR}/config.sh"
LOG_DIR="${HOME}/.claude/logs"
LOG_FILE="${LOG_DIR}/session-summaries.jsonl"
HOOKS_DIR="${HOME}/.claude/hooks"

# ANSI colors
if [[ -z "${NO_COLOR:-}" ]]; then
    BOLD=$'\033[1m'
    DIM=$'\033[2m'
    CYAN=$'\033[36m'
    GREEN=$'\033[32m'
    YELLOW=$'\033[33m'
    RED=$'\033[31m'
    RESET=$'\033[0m'
else
    BOLD='' DIM='' CYAN='' GREEN='' YELLOW='' RED='' RESET=''
fi

# ═══════════════════════════════════════════════════════════════════════════
# Defaults (must match session-summary.sh) - Bash 3.2 compatible (no declare -A)
# ═══════════════════════════════════════════════════════════════════════════

# Config keys and their defaults
ALL_KEYS="LOG_DIR SKIP FILES RTK GIT ERRORS LOC RATIO FEATURES THINKING CONTEXT SECTIONS"

DEFAULT_LOG_DIR="$HOME/.claude/logs"
DEFAULT_SKIP=0
DEFAULT_FILES=1
DEFAULT_RTK=auto
DEFAULT_GIT=1
DEFAULT_ERRORS=1
DEFAULT_LOC=1
DEFAULT_RATIO=1
DEFAULT_FEATURES=1
DEFAULT_THINKING=0
DEFAULT_CONTEXT=0
DEFAULT_SECTIONS="meta,duration,tools,errors,files,features,git,loc,models,cache,cost,rtk,ratio,thinking,context"

# Current config values (loaded from file, overlaying defaults)
CFG_LOG_DIR=""
CFG_SKIP=""
CFG_FILES=""
CFG_RTK=""
CFG_GIT=""
CFG_ERRORS=""
CFG_LOC=""
CFG_RATIO=""
CFG_FEATURES=""
CFG_THINKING=""
CFG_CONTEXT=""
CFG_SECTIONS=""

get_default() {
    local key="$1"
    case "$key" in
        LOG_DIR)   echo "$DEFAULT_LOG_DIR" ;;
        SKIP)      echo "$DEFAULT_SKIP" ;;
        FILES)     echo "$DEFAULT_FILES" ;;
        RTK)       echo "$DEFAULT_RTK" ;;
        GIT)       echo "$DEFAULT_GIT" ;;
        ERRORS)    echo "$DEFAULT_ERRORS" ;;
        LOC)       echo "$DEFAULT_LOC" ;;
        RATIO)     echo "$DEFAULT_RATIO" ;;
        FEATURES)  echo "$DEFAULT_FEATURES" ;;
        THINKING)  echo "$DEFAULT_THINKING" ;;
        CONTEXT)   echo "$DEFAULT_CONTEXT" ;;
        SECTIONS)  echo "$DEFAULT_SECTIONS" ;;
        *) echo "" ;;
    esac
}

get_cfg() {
    local key="$1"
    local val=""
    case "$key" in
        LOG_DIR)   val="$CFG_LOG_DIR" ;;
        SKIP)      val="$CFG_SKIP" ;;
        FILES)     val="$CFG_FILES" ;;
        RTK)       val="$CFG_RTK" ;;
        GIT)       val="$CFG_GIT" ;;
        ERRORS)    val="$CFG_ERRORS" ;;
        LOC)       val="$CFG_LOC" ;;
        RATIO)     val="$CFG_RATIO" ;;
        FEATURES)  val="$CFG_FEATURES" ;;
        THINKING)  val="$CFG_THINKING" ;;
        CONTEXT)   val="$CFG_CONTEXT" ;;
        SECTIONS)  val="$CFG_SECTIONS" ;;
    esac
    echo "$val"
}

set_cfg() {
    local key="$1"
    local val="$2"
    case "$key" in
        LOG_DIR)   CFG_LOG_DIR="$val" ;;
        SKIP)      CFG_SKIP="$val" ;;
        FILES)     CFG_FILES="$val" ;;
        RTK)       CFG_RTK="$val" ;;
        GIT)       CFG_GIT="$val" ;;
        ERRORS)    CFG_ERRORS="$val" ;;
        LOC)       CFG_LOC="$val" ;;
        RATIO)     CFG_RATIO="$val" ;;
        FEATURES)  CFG_FEATURES="$val" ;;
        THINKING)  CFG_THINKING="$val" ;;
        CONTEXT)   CFG_CONTEXT="$val" ;;
        SECTIONS)  CFG_SECTIONS="$val" ;;
        *) return 1 ;;
    esac
}

is_valid_key() {
    local key="$1"
    case "$key" in
        LOG_DIR|SKIP|FILES|RTK|GIT|ERRORS|LOC|RATIO|FEATURES|THINKING|CONTEXT|SECTIONS) return 0 ;;
        *) return 1 ;;
    esac
}

# Section metadata helpers
get_section_desc() {
    case "$1" in
        meta)     echo "Session ID, name, branch" ;;
        duration) echo "Wall time, active time, turns, exit reason" ;;
        tools)    echo "Tool calls breakdown (OK/ERR)" ;;
        errors)   echo "Error details by tool" ;;
        files)    echo "Files read/edited/created" ;;
        features) echo "MCP servers, agents, skills, teams" ;;
        git)      echo "Git diff summary (+/- lines)" ;;
        loc)      echo "Lines of code via Edit/Write" ;;
        models)   echo "Model usage (reqs, tokens)" ;;
        cache)    echo "Cache hit rate" ;;
        cost)     echo "Estimated session cost" ;;
        rtk)      echo "RTK token savings" ;;
        ratio)    echo "Conversation ratio (interactive/auto)" ;;
        thinking) echo "Thinking blocks count" ;;
        context)  echo "Context window estimate" ;;
        *) echo "" ;;
    esac
}

# Maps section name to its config toggle key (empty = always on)
get_section_key() {
    case "$1" in
        meta|duration|tools|models|cache|cost) echo "" ;;
        files)    echo "FILES" ;;
        git)      echo "GIT" ;;
        errors)   echo "ERRORS" ;;
        loc)      echo "LOC" ;;
        rtk)      echo "RTK" ;;
        ratio)    echo "RATIO" ;;
        features) echo "FEATURES" ;;
        thinking) echo "THINKING" ;;
        context)  echo "CONTEXT" ;;
        *) echo "" ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════
# Config loading/saving
# ═══════════════════════════════════════════════════════════════════════════

load_current_config() {
    # Start with defaults
    for key in $ALL_KEYS; do
        set_cfg "$key" "$(get_default "$key")"
    done

    # Overlay from config file
    if [[ -f "$CONFIG_FILE" ]]; then
        while IFS='=' read -r key value; do
            key=$(echo "$key" | tr -d '[:space:]')
            value=$(echo "$value" | tr -d '[:space:]' | sed 's/^"//;s/"$//')
            [[ -z "$key" || "$key" == \#* ]] && continue
            if is_valid_key "$key"; then
                set_cfg "$key" "$value"
            fi
        done < "$CONFIG_FILE"
    fi
}

write_config() {
    mkdir -p "$CONFIG_DIR"
    {
        echo "# Session Summary Configuration"
        echo "# Generated by session-summary-config.sh"
        echo "# $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        echo ""
        for key in $ALL_KEYS; do
            local val
            val=$(get_cfg "$key")
            if [[ "$key" == "SECTIONS" || "$key" == "LOG_DIR" ]]; then
                echo "${key}=\"${val}\""
            else
                echo "${key}=${val}"
            fi
        done
    } > "$CONFIG_FILE"
}

# ═══════════════════════════════════════════════════════════════════════════
# Subcommands
# ═══════════════════════════════════════════════════════════════════════════

cmd_show() {
    load_current_config

    echo "${BOLD}Session Summary Configuration${RESET}"
    echo ""
    echo "${DIM}Config file:${RESET} $CONFIG_FILE"
    [[ -f "$CONFIG_FILE" ]] && echo "${DIM}Status:${RESET} ${GREEN}exists${RESET}" || echo "${DIM}Status:${RESET} ${YELLOW}not created (using defaults)${RESET}"
    echo ""

    echo "${BOLD}Sections:${RESET}"
    echo ""

    # Parse current section order
    local sections_str
    sections_str=$(get_cfg "SECTIONS")
    IFS=',' read -ra ordered_sections <<< "$sections_str"
    for section in "${ordered_sections[@]}"; do
        section=$(echo "$section" | tr -d ' ')
        local key desc status
        key=$(get_section_key "$section")
        desc=$(get_section_desc "$section")

        if [[ -z "$key" ]]; then
            status="${GREEN}always on${RESET}"
        else
            local val
            val=$(get_cfg "$key")
            if [[ "$val" == "1" ]]; then
                status="${GREEN}on${RESET}"
            elif [[ "$val" == "auto" ]]; then
                status="${CYAN}auto${RESET}"
            else
                status="${DIM}off${RESET}"
            fi
        fi

        printf "  %-12s %-8s %s\n" "$section" "[$status]" "${DIM}${desc}${RESET}"
    done

    echo ""
    echo "${BOLD}Settings:${RESET}"
    echo "  ${DIM}LOG_DIR:${RESET}  $(get_cfg LOG_DIR)"
    echo "  ${DIM}SKIP:${RESET}     $(get_cfg SKIP)"
    echo ""
    echo "${DIM}Priority: env vars (SESSION_SUMMARY_*) > config file > defaults${RESET}"
}

cmd_set() {
    load_current_config

    for arg in "$@"; do
        if [[ "$arg" != *"="* ]]; then
            echo "${RED}Error: Invalid format '$arg'. Use KEY=VALUE (e.g., git=1, errors=0)${RESET}" >&2
            exit 1
        fi

        local key="${arg%%=*}"
        local value="${arg#*=}"

        # Normalize key to uppercase
        key=$(echo "$key" | tr '[:lower:]' '[:upper:]')

        # Validate key
        if ! is_valid_key "$key"; then
            echo "${RED}Error: Unknown key '$key'. Valid keys: $ALL_KEYS${RESET}" >&2
            exit 1
        fi

        set_cfg "$key" "$value"
        echo "${GREEN}Set${RESET} $key=$value"
    done

    write_config
    echo ""
    echo "${DIM}Config saved to $CONFIG_FILE${RESET}"
}

cmd_reset() {
    load_current_config
    for key in $ALL_KEYS; do
        set_cfg "$key" "$(get_default "$key")"
    done
    write_config
    echo "${GREEN}Config reset to defaults${RESET}"
    echo "${DIM}Saved to $CONFIG_FILE${RESET}"
}

cmd_sections() {
    load_current_config

    if [[ $# -eq 0 ]]; then
        # Show current order
        echo "${BOLD}Current section order:${RESET}"
        echo "  $(get_cfg SECTIONS)"
        echo ""
        echo "${DIM}Available sections:${RESET}"
        echo "  cache,context,cost,duration,errors,features,files,git,loc,meta,models,ratio,rtk,thinking,tools"
        echo ""
        echo "${DIM}Usage: session-summary-config sections \"meta,duration,tools,files,...\"${RESET}"
    else
        # Set new order
        set_cfg "SECTIONS" "$1"
        write_config
        echo "${GREEN}Section order updated:${RESET} $1"
    fi
}

cmd_preview() {
    load_current_config

    echo ""
    echo "${BOLD}═══ Session Summary (Preview) ═════════${RESET}"

    local sections_str
    sections_str=$(get_cfg "SECTIONS")
    IFS=',' read -ra sections <<< "$sections_str"
    for section in "${sections[@]}"; do
        section=$(echo "$section" | tr -d ' ')
        local key
        key=$(get_section_key "$section")
        local enabled=true

        if [[ -n "$key" ]]; then
            local val
            val=$(get_cfg "$key")
            [[ "$val" != "1" && "$val" != "auto" ]] && enabled=false
        fi

        $enabled || continue

        case "$section" in
            meta)
                echo "${DIM}ID:${RESET}       a1b2c3d4-e5f6-78..."
                echo "${DIM}Name:${RESET}     Example session"
                echo "${DIM}Branch:${RESET}   main"
                ;;
            duration)
                echo "${DIM}Duration:${RESET} Wall 5m 28s | Active 1m 33s | 12 turns | Exit: user"
                ;;
            tools)
                echo "${DIM}Tool Calls:${RESET} 29 ${GREEN}(OK 27 / ERR 2)${RESET}"
                echo "  ${CYAN}Edit:${RESET} 13  ${CYAN}Bash:${RESET} 8  ${CYAN}Read:${RESET} 6  ${CYAN}Grep:${RESET} 1  ${CYAN}Glob:${RESET} 1"
                ;;
            errors)
                echo "${DIM}Errors:${RESET} ${RED}2${RESET}"
                echo "  Bash: \"command not found: rtk\" (x1)"
                echo "  Edit: \"old_string not unique\" (x1)"
                ;;
            files)
                echo "${DIM}Files:${RESET} 3 read · 2 edited · 1 created"
                echo "  session-summary.sh (8 edits), settings.json (3 edits)"
                ;;
            features)
                echo "${DIM}Features:${RESET} MCP (perplexity x4, chrome x12) · Agents (Explore x3, Plan x1) · Skills (commit)"
                ;;
            git)
                echo "${DIM}Git:${RESET} ${GREEN}+142${RESET} ${RED}-37${RESET} lines · 4 files changed"
                ;;
            loc)
                echo "${DIM}Code:${RESET} ${GREEN}+87${RESET} ${RED}-12${RESET} net (via Edit/Write)"
                ;;
            models)
                echo "${DIM}Model Usage${RESET}         Reqs    Input    Output"
                printf "${CYAN}%-20s${RESET} %4d   %7s   %6s\n" "claude-opus-4-6" 59 "93K" "628"
                ;;
            cache)
                echo "Cache: 85% hit rate (3.9M read / 322K created)"
                ;;
            cost)
                echo "Est. Cost: ${GREEN}\$0.045${RESET}"
                ;;
            rtk)
                echo "RTK Savings: 24 cmds · ~12.4K tokens saved (73%)"
                echo "  git status(8), git diff(5), ls(4)"
                ;;
            ratio)
                echo "${DIM}Turns:${RESET} 12 (8 interactive · 4 auto) · Avg 6.7s/turn"
                ;;
            thinking)
                echo "${DIM}Thinking:${RESET} 12 blocks"
                ;;
            context)
                echo "${DIM}Context:${RESET} ~78% peak (est.) · Model limit: 200K"
                ;;
        esac
    done

    echo "${BOLD}═══════════════════════════════════════${RESET}"
}

cmd_install() {
    local settings_file="${HOME}/.claude/settings.json"

    echo "${BOLD}Installing session-summary hooks...${RESET}"
    echo ""

    # Copy hook files
    mkdir -p "$HOOKS_DIR"

    local script_dir
    script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

    local src_summary="${script_dir}/session-summary.sh"
    local src_baseline="${script_dir}/rtk-baseline.sh"
    local src_config="${script_dir}/session-summary-config.sh"

    if [[ -f "$src_summary" ]]; then
        cp "$src_summary" "$HOOKS_DIR/session-summary.sh"
        chmod +x "$HOOKS_DIR/session-summary.sh"
        echo "  ${GREEN}Copied${RESET} session-summary.sh -> $HOOKS_DIR/"
    else
        echo "  ${YELLOW}Skipped${RESET} session-summary.sh (not found at $src_summary)"
    fi

    if [[ -f "$src_baseline" ]]; then
        cp "$src_baseline" "$HOOKS_DIR/rtk-baseline.sh"
        chmod +x "$HOOKS_DIR/rtk-baseline.sh"
        echo "  ${GREEN}Copied${RESET} rtk-baseline.sh -> $HOOKS_DIR/"
    fi

    if [[ -f "$src_config" ]]; then
        cp "$src_config" "$HOOKS_DIR/session-summary-config.sh"
        chmod +x "$HOOKS_DIR/session-summary-config.sh"
        echo "  ${GREEN}Copied${RESET} session-summary-config.sh -> $HOOKS_DIR/"
    fi

    echo ""

    # Update settings.json
    if ! command -v jq &>/dev/null; then
        echo "${RED}Error: jq required for settings.json update. Install: brew install jq${RESET}" >&2
        exit 1
    fi

    local hook_session_end='{
        "hooks": [{
            "type": "command",
            "command": "~/.claude/hooks/session-summary.sh"
        }]
    }'
    local hook_session_start='{
        "hooks": [{
            "type": "command",
            "command": "~/.claude/hooks/rtk-baseline.sh",
            "timeout": 5000
        }]
    }'

    if [[ -f "$settings_file" ]]; then
        local tmp
        tmp=$(mktemp)

        # Add/update SessionEnd hook
        jq --argjson hook "$hook_session_end" '
            .hooks.SessionEnd = (
                [(.hooks.SessionEnd // [])[] | select(.hooks[0].command | test("session-summary") | not)] + [$hook]
            )
        ' "$settings_file" > "$tmp"

        # Add/update SessionStart hook (rtk-baseline) if RTK available
        if command -v rtk &>/dev/null; then
            jq --argjson hook "$hook_session_start" '
                .hooks.SessionStart = (
                    [(.hooks.SessionStart // [])[] | select(.hooks[0].command | test("rtk-baseline") | not)] + [$hook]
                )
            ' "$tmp" > "${tmp}.2" && mv "${tmp}.2" "$tmp"
        fi

        mv "$tmp" "$settings_file"
        echo "  ${GREEN}Updated${RESET} $settings_file"
    else
        # Create new settings.json
        local hooks_obj="{\"SessionEnd\": [$hook_session_end]"
        if command -v rtk &>/dev/null; then
            hooks_obj+=", \"SessionStart\": [$hook_session_start]"
        fi
        hooks_obj+="}"

        echo "{\"hooks\": $hooks_obj}" | jq '.' > "$settings_file"
        echo "  ${GREEN}Created${RESET} $settings_file"
    fi

    echo ""
    echo "${GREEN}Installation complete.${RESET}"
    echo "${DIM}Session summary will appear on next session exit.${RESET}"
}

cmd_log() {
    local count="${1:-5}"

    if [[ ! -f "$LOG_FILE" ]]; then
        echo "${YELLOW}No session summaries found at $LOG_FILE${RESET}"
        exit 0
    fi

    echo "${BOLD}Last $count session summaries:${RESET}"
    echo ""

    tail -n "$count" "$LOG_FILE" | jq -r '
        "=== \(.session_name // "Unnamed") ===",
        "  ID: \(.session_id[:16])...  Branch: \(.git_branch)  Exit: \(.exit_reason // "unknown")",
        "  Duration: \((.duration_wall_ms / 1000 / 60) | floor)m  Turns: \(.turns)  Cost: $\(.cost_usd | tostring[:5])",
        "  Tools: \(.tool_calls | to_entries | map("\(.key):\(.value)") | join(", "))",
        "  Errors: \(.tool_errors)  Cache: \(.cache_hit_rate)%",
        ""
    ' 2>/dev/null || echo "${RED}Error parsing log file${RESET}"
}

cmd_help() {
    echo "${BOLD}session-summary-config${RESET} - Configure session-summary.sh hook"
    echo ""
    echo "${BOLD}Usage:${RESET}"
    echo "  session-summary-config ${CYAN}show${RESET}              Show current config"
    echo "  session-summary-config ${CYAN}set${RESET} KEY=VALUE     Set a config value"
    echo "  session-summary-config ${CYAN}reset${RESET}             Reset to defaults"
    echo "  session-summary-config ${CYAN}sections${RESET}          Show section order"
    echo "  session-summary-config ${CYAN}sections${RESET} \"a,b,c\"  Set section order"
    echo "  session-summary-config ${CYAN}preview${RESET}           Demo output with current config"
    echo "  session-summary-config ${CYAN}install${RESET}           Install hooks + settings.json"
    echo "  session-summary-config ${CYAN}log${RESET} [n]           Show last n summaries (default: 5)"
    echo ""
    echo "${BOLD}Config keys:${RESET}"
    echo "  files, git, errors, loc, rtk, ratio, features, thinking, context"
    echo "  skip, log_dir, sections"
    echo ""
    echo "${BOLD}Examples:${RESET}"
    echo "  session-summary-config set git=0          # Disable git diff"
    echo "  session-summary-config set thinking=1     # Enable thinking blocks"
    echo "  session-summary-config set rtk=auto       # Auto-detect RTK"
    echo "  session-summary-config sections \"meta,duration,tools,cost\"  # Minimal output"
}

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

case "${1:-help}" in
    show)     cmd_show ;;
    set)      shift; cmd_set "$@" ;;
    reset)    cmd_reset ;;
    sections) shift; cmd_sections "$@" ;;
    preview)  cmd_preview ;;
    install)  cmd_install ;;
    log)      shift; cmd_log "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
        echo "${RED}Unknown command: $1${RESET}" >&2
        echo ""
        cmd_help
        exit 1
        ;;
esac
