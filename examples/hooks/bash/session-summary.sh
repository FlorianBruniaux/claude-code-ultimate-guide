#!/bin/bash
# .claude/hooks/session-summary.sh
# Event: SessionEnd
# Auto-display comprehensive session summary when Claude Code session ends
# Inspired by Gemini CLI session summary feature
#
# v3 - Full Analytics + CLI Config
#
# Displays (configurable sections):
#   - Session ID, name, git branch
#   - Duration (wall time, active time, turns count, exit reason)
#   - Tool calls breakdown with success/error rates
#   - Error details (tool name + truncated message)
#   - Files touched (read/edited/created with top edited files)
#   - Features used (MCP servers, agents, skills, teams, plan mode)
#   - Git diff summary (+/- lines, files changed)
#   - Lines of code written (via Edit/Write)
#   - Model usage (requests, tokens, cache hit rate)
#   - Estimated cost (via ccusage or pricing table fallback)
#   - RTK token savings (if RTK installed, delta from session start)
#   - Conversation ratio (interactive vs auto turns, avg time/turn)
#   - Thinking blocks count (off by default)
#   - Context window estimate (off by default)
#
# Requirements:
#   - jq (required for JSON parsing)
#   - ccusage (optional, for accurate cost calculation)
#   - rtk (optional, for token savings tracking)
#
# Configuration priority: env vars > config file > defaults
#   Config file: ~/.config/session-summary/config.sh
#   CLI tool: session-summary-config.sh (show, set, reset, sections, preview, install, log)
#
# Environment variables (SESSION_SUMMARY_*):
#   SKIP=1          - Disable summary entirely
#   LOG=<path>      - Override log directory (default: ~/.claude/logs)
#   FILES=0|1       - Files section (default: 1)
#   RTK=auto|1|0    - RTK savings (default: auto-detect)
#   GIT=0|1         - Git diff summary (default: 1)
#   ERRORS=0|1      - Error details (default: 1)
#   LOC=0|1         - Lines of code (default: 1)
#   RATIO=0|1       - Conversation ratio (default: 1)
#   FEATURES=0|1    - Features used (default: 1)
#   THINKING=0|1    - Thinking blocks (default: 0)
#   CONTEXT=0|1     - Context estimate (default: 0)
#   SECTIONS=<csv>  - Section order (comma-separated)
#
# Place in: .claude/hooks/session-summary.sh
# Register in: .claude/settings.json under SessionEnd event
# NOTE: Do NOT use Stop event - it fires after every assistant turn, not just at exit

set -euo pipefail
export LC_NUMERIC=C  # Ensure consistent decimal separator (bc outputs '.' not ',')

# ═══════════════════════════════════════════════════════════════════════════
# Configuration (priority: env vars > config file > defaults)
# ═══════════════════════════════════════════════════════════════════════════

CONFIG_FILE="${HOME}/.config/session-summary/config.sh"

# Defaults
_DEFAULT_LOG_DIR="$HOME/.claude/logs"
_DEFAULT_SKIP=0
_DEFAULT_FILES=1
_DEFAULT_RTK=auto
_DEFAULT_GIT=1
_DEFAULT_ERRORS=1
_DEFAULT_LOC=1
_DEFAULT_RATIO=1
_DEFAULT_FEATURES=1
_DEFAULT_THINKING=0
_DEFAULT_CONTEXT=0
_DEFAULT_SECTIONS="meta,duration,tools,errors,files,features,git,loc,models,cache,cost,rtk,ratio,thinking,context"

# Load config file (if exists), then overlay env vars
load_config() {
    # Start with defaults
    LOG_DIR="$_DEFAULT_LOG_DIR"
    SKIP="$_DEFAULT_SKIP"
    FILES_ENABLED="$_DEFAULT_FILES"
    RTK_ENABLED="$_DEFAULT_RTK"
    GIT_ENABLED="$_DEFAULT_GIT"
    ERRORS_ENABLED="$_DEFAULT_ERRORS"
    LOC_ENABLED="$_DEFAULT_LOC"
    RATIO_ENABLED="$_DEFAULT_RATIO"
    FEATURES_ENABLED="$_DEFAULT_FEATURES"
    THINKING_ENABLED="$_DEFAULT_THINKING"
    CONTEXT_ENABLED="$_DEFAULT_CONTEXT"
    SECTION_ORDER="$_DEFAULT_SECTIONS"

    # Layer 2: config file
    if [[ -f "$CONFIG_FILE" ]]; then
        local val
        val=$(bash -c "source '$CONFIG_FILE' 2>/dev/null && echo \"\${LOG_DIR:-}|\${SKIP:-}|\${FILES:-}|\${RTK:-}|\${GIT:-}|\${ERRORS:-}|\${LOC:-}|\${RATIO:-}|\${FEATURES:-}|\${THINKING:-}|\${CONTEXT:-}|\${SECTIONS:-}\"")
        IFS='|' read -r _cf_log _cf_skip _cf_files _cf_rtk _cf_git _cf_errors _cf_loc _cf_ratio _cf_features _cf_thinking _cf_context _cf_sections <<< "$val"
        [[ -n "$_cf_log" ]] && LOG_DIR="$_cf_log"
        [[ -n "$_cf_skip" ]] && SKIP="$_cf_skip"
        [[ -n "$_cf_files" ]] && FILES_ENABLED="$_cf_files"
        [[ -n "$_cf_rtk" ]] && RTK_ENABLED="$_cf_rtk"
        [[ -n "$_cf_git" ]] && GIT_ENABLED="$_cf_git"
        [[ -n "$_cf_errors" ]] && ERRORS_ENABLED="$_cf_errors"
        [[ -n "$_cf_loc" ]] && LOC_ENABLED="$_cf_loc"
        [[ -n "$_cf_ratio" ]] && RATIO_ENABLED="$_cf_ratio"
        [[ -n "$_cf_features" ]] && FEATURES_ENABLED="$_cf_features"
        [[ -n "$_cf_thinking" ]] && THINKING_ENABLED="$_cf_thinking"
        [[ -n "$_cf_context" ]] && CONTEXT_ENABLED="$_cf_context"
        [[ -n "$_cf_sections" ]] && SECTION_ORDER="$_cf_sections"
    fi

    # Layer 3: env vars (highest priority)
    [[ -n "${SESSION_SUMMARY_LOG:-}" ]] && LOG_DIR="$SESSION_SUMMARY_LOG"
    [[ -n "${SESSION_SUMMARY_SKIP:-}" ]] && SKIP="$SESSION_SUMMARY_SKIP"
    [[ -n "${SESSION_SUMMARY_FILES:-}" ]] && FILES_ENABLED="$SESSION_SUMMARY_FILES"
    [[ -n "${SESSION_SUMMARY_RTK:-}" ]] && RTK_ENABLED="$SESSION_SUMMARY_RTK"
    [[ -n "${SESSION_SUMMARY_GIT:-}" ]] && GIT_ENABLED="$SESSION_SUMMARY_GIT"
    [[ -n "${SESSION_SUMMARY_ERRORS:-}" ]] && ERRORS_ENABLED="$SESSION_SUMMARY_ERRORS"
    [[ -n "${SESSION_SUMMARY_LOC:-}" ]] && LOC_ENABLED="$SESSION_SUMMARY_LOC"
    [[ -n "${SESSION_SUMMARY_RATIO:-}" ]] && RATIO_ENABLED="$SESSION_SUMMARY_RATIO"
    [[ -n "${SESSION_SUMMARY_FEATURES:-}" ]] && FEATURES_ENABLED="$SESSION_SUMMARY_FEATURES"
    [[ -n "${SESSION_SUMMARY_THINKING:-}" ]] && THINKING_ENABLED="$SESSION_SUMMARY_THINKING"
    [[ -n "${SESSION_SUMMARY_CONTEXT:-}" ]] && CONTEXT_ENABLED="$SESSION_SUMMARY_CONTEXT"
    [[ -n "${SESSION_SUMMARY_SECTIONS:-}" ]] && SECTION_ORDER="$SESSION_SUMMARY_SECTIONS"

    # Auto-detect RTK availability
    if [[ "$RTK_ENABLED" == "auto" ]]; then
        command -v rtk &>/dev/null && RTK_ENABLED=1 || RTK_ENABLED=0
    fi
}

load_config

# Section enablement check
# Always-on: meta, duration, tools, models, cache, cost
# Configurable: files, git, errors, loc, rtk, ratio, features (default ON)
# Configurable: thinking, context (default OFF)
is_section_enabled() {
    local section="$1"
    case "$section" in
        meta|duration|tools|models|cache|cost) return 0 ;;  # always on
        files)    [[ "$FILES_ENABLED" == "1" ]] ;;
        git)      [[ "$GIT_ENABLED" == "1" ]] ;;
        errors)   [[ "$ERRORS_ENABLED" == "1" ]] ;;
        loc)      [[ "$LOC_ENABLED" == "1" ]] ;;
        rtk)      [[ "$RTK_ENABLED" == "1" ]] ;;
        ratio)    [[ "$RATIO_ENABLED" == "1" ]] ;;
        features) [[ "$FEATURES_ENABLED" == "1" ]] ;;
        thinking) [[ "$THINKING_ENABLED" == "1" ]] ;;
        context)  [[ "$CONTEXT_ENABLED" == "1" ]] ;;
        *) return 1 ;;
    esac
}

# Output target: /dev/tty bypasses Claude Code's stderr capture for lifecycle hooks
# Falls back to stderr when /dev/tty is unavailable (CI, cron, dry-run in pipes)
if (echo -n "" > /dev/tty) 2>/dev/null; then
    OUTPUT_TARGET="/dev/tty"
else
    OUTPUT_TARGET="/dev/stderr"
fi

# ANSI colors (respect NO_COLOR)
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

# Pricing table (per million tokens, as of 2026-02)
# Used as fallback if ccusage is unavailable
get_pricing() {
    local model="$1"
    local type="$2"  # input or output

    case "$model" in
        claude-opus-4-6)
            [[ "$type" == "input" ]] && echo "15.00" || echo "75.00"
            ;;
        claude-sonnet-4-5)
            [[ "$type" == "input" ]] && echo "3.00" || echo "15.00"
            ;;
        claude-haiku-4-5)
            [[ "$type" == "input" ]] && echo "0.80" || echo "4.00"
            ;;
        *)
            echo "0"
            ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════

check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required but not installed" >&2
        echo "Install: brew install jq (macOS) or apt-get install jq (Linux)" >&2
        exit 0  # Don't block session end
    fi
}

locate_jsonl() {
    local session_id="$1"
    local cwd="$2"

    # Encode project path: /Users/foo/bar -> -Users-foo-bar
    local encoded_path
    encoded_path=$(echo "$cwd" | tr '/' '-')

    local jsonl_path="$HOME/.claude/projects/${encoded_path}/${session_id}.jsonl"

    # Fallback: find if encoding wrong
    if [[ ! -f "$jsonl_path" ]]; then
        jsonl_path=$(find "$HOME/.claude/projects" -name "${session_id}.jsonl" -maxdepth 2 2>/dev/null | head -1)
    fi

    echo "$jsonl_path"
}

format_duration() {
    local ms="$1"
    local seconds=$((ms / 1000))
    local minutes=$((seconds / 60))
    local hours=$((minutes / 60))

    if [[ $hours -gt 0 ]]; then
        printf "%dh %dm" "$hours" "$((minutes % 60))"
    elif [[ $minutes -gt 0 ]]; then
        printf "%dm %ds" "$minutes" "$((seconds % 60))"
    else
        printf "%ds" "$seconds"
    fi
}

format_number() {
    local num="$1"

    if [[ $num -ge 1000000 ]]; then
        printf "%.1fM" "$(bc <<< "scale=1; $num / 1000000")"
    elif [[ $num -ge 1000 ]]; then
        printf "%.1fK" "$(bc <<< "scale=1; $num / 1000")"
    else
        printf "%d" "$num"
    fi
}

shorten_model_name() {
    local model="$1"
    # claude-sonnet-4-5-20250929 -> claude-sonnet-4-5
    echo "$model" | sed -E 's/-(20[0-9]{6})$//'
}

# Parse a numeric value with K/M/B suffix from rtk gain text output
parse_rtk_number() {
    local text="$1"
    local label="$2"

    echo "$text" | awk -v label="$label" '
        $0 ~ label {
            for (i=1; i<=NF; i++) {
                if ($i ~ /^[0-9]/) {
                    val = $i
                    gsub(/,/, "", val)
                    if (val ~ /[Bb]$/) { sub(/[Bb]$/, "", val); printf "%.0f", val * 1000000000 }
                    else if (val ~ /[Mm]$/) { sub(/[Mm]$/, "", val); printf "%.0f", val * 1000000 }
                    else if (val ~ /[Kk]$/) { sub(/[Kk]$/, "", val); printf "%.0f", val * 1000 }
                    else { printf "%.0f", val }
                    exit
                }
            }
        }
    '
}

# Diff "By Command" tables from two rtk gain outputs, return commands with positive delta
# Output: "git status(2), ls(3), git diff(1)"
diff_rtk_commands() {
    local baseline="$1"
    local current="$2"

    { echo "___BASELINE___"; echo "$baseline"; echo "___CURRENT___"; echo "$current"; echo "___END___"; } | awk '
        /^___BASELINE___$/ { section="baseline"; next }
        /^___CURRENT___$/ { section="current"; in_table=0; next }
        /^___END___$/ {
            for (cmd in cur) {
                delta = cur[cmd] - (base[cmd] + 0)
                if (delta > 0) {
                    short = cmd
                    sub(/^rtk /, "", short)
                    # Truncate long commands
                    if (length(short) > 20) short = substr(short, 1, 17) "..."
                    if (length(out) > 0) out = out ", "
                    out = out short "(" delta ")"
                }
            }
            print out
            exit
        }
        /^By Command:/ { in_table=1; next }
        /^─/ { next }
        /^Command/ { next }
        in_table && /^$/ { in_table=0; next }
        in_table && NF >= 5 {
            count = $(NF-3)
            if (count ~ /^[0-9,]+$/) {
                gsub(/,/, "", count)
                cmd = ""
                for (i=1; i<=NF-4; i++) cmd = cmd (i>1?" ":"") $i
                if (section == "baseline") base[cmd] = count + 0
                else cur[cmd] = count + 0
            }
        }
    '
}

# Calculate RTK token savings for this session (delta between start and end)
calculate_rtk_savings() {
    # Build baseline file path (must match rtk-baseline.sh)
    local baseline_key
    baseline_key=$(echo "${CLAUDE_PROJECT_DIR:-$(pwd)}" | tr '/' '-')
    local baseline_file="/tmp/rtk-baseline${baseline_key}.txt"

    # No baseline = no delta possible
    if [[ ! -f "$baseline_file" ]]; then
        echo ""
        return
    fi

    local baseline_text
    baseline_text=$(<"$baseline_file")

    local current_text
    current_text=$(rtk gain 2>/dev/null) || { echo ""; return; }

    # Parse total commands from both snapshots
    local start_cmds end_cmds
    start_cmds=$(parse_rtk_number "$baseline_text" "Total commands")
    end_cmds=$(parse_rtk_number "$current_text" "Total commands")

    local delta_cmds=$(( ${end_cmds:-0} - ${start_cmds:-0} ))

    # No commands rewritten this session
    if [[ $delta_cmds -le 0 ]]; then
        rm -f "$baseline_file"
        echo ""
        return
    fi

    # Parse all token lines upfront (needed by all 3 approaches + pct calculation)
    local start_saved end_saved start_input end_input start_output end_output
    start_saved=$(parse_rtk_number "$baseline_text" "Tokens saved")
    end_saved=$(parse_rtk_number "$current_text" "Tokens saved")
    start_input=$(parse_rtk_number "$baseline_text" "Input tokens")
    end_input=$(parse_rtk_number "$current_text" "Input tokens")
    start_output=$(parse_rtk_number "$baseline_text" "Output tokens")
    end_output=$(parse_rtk_number "$current_text" "Output tokens")

    # Token savings: 3 approaches (M/K rounding loses precision for small sessions)
    local delta_saved=0 estimated=0

    # Approach 1: Direct delta from "Tokens saved" line
    delta_saved=$(( ${end_saved:-0} - ${start_saved:-0} ))

    # Approach 2: If 0 due to rounding, try (Input - Output) delta
    if [[ $delta_saved -le 0 ]]; then
        delta_saved=$(( (${end_input:-0} - ${start_input:-0}) - (${end_output:-0} - ${start_output:-0}) ))
    fi

    # Approach 3: Estimate from global average per command
    if [[ $delta_saved -le 0 && ${end_cmds:-0} -gt 0 ]]; then
        estimated=1
        delta_saved=$(bc <<< "scale=0; ${end_saved:-0} / ${end_cmds:-1} * $delta_cmds")
    fi

    # Calculate percentage
    local pct="0"
    local delta_input=$(( ${end_input:-0} - ${start_input:-0} ))
    if [[ $estimated -eq 1 ]]; then
        # Use global average percentage
        if [[ ${end_input:-0} -gt 0 ]]; then
            pct=$(bc <<< "scale=0; ${end_saved:-0} * 100 / ${end_input:-1}")
        fi
    elif [[ ${delta_input:-0} -gt 0 ]]; then
        pct=$(bc <<< "scale=0; $delta_saved * 100 / $delta_input")
    fi

    # Parse per-command deltas from "By Command" table
    local cmds_detail
    cmds_detail=$(diff_rtk_commands "$baseline_text" "$current_text")

    # Clean up baseline file
    rm -f "$baseline_file"

    # Return JSON
    jq -cn \
        --argjson cmds "$delta_cmds" \
        --argjson tokens_saved "${delta_saved:-0}" \
        --arg pct "$pct" \
        --argjson estimated "$estimated" \
        --arg commands "${cmds_detail:-}" \
        '{cmds: $cmds, tokens_saved: $tokens_saved, pct: $pct, estimated: ($estimated == 1), commands: $commands}'
}

# Collect git diff stats (files changed, insertions, deletions)
collect_git_diff() {
    local cwd="$1"
    if ! command -v git &>/dev/null; then
        echo "{}"
        return
    fi

    local stat_line
    stat_line=$(git -C "$cwd" diff --stat HEAD 2>/dev/null | tail -1) || { echo "{}"; return; }

    if [[ -z "$stat_line" ]]; then
        echo "{}"
        return
    fi

    # Parse: " 4 files changed, 142 insertions(+), 37 deletions(-)"
    local files_changed=0 insertions=0 deletions=0
    files_changed=$(echo "$stat_line" | grep -oE '[0-9]+ files? changed' | grep -oE '[0-9]+' || echo "0")
    insertions=$(echo "$stat_line" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
    deletions=$(echo "$stat_line" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")

    jq -cn \
        --argjson files "${files_changed:-0}" \
        --argjson ins "${insertions:-0}" \
        --argjson del "${deletions:-0}" \
        '{files_changed: $files, insertions: $ins, deletions: $del}'
}

extract_session_data() {
    local jsonl_path="$1"
    local loc_enabled="${2:-1}"
    local features_enabled="${3:-1}"
    local errors_enabled="${4:-1}"
    local thinking_enabled="${5:-0}"
    local context_enabled="${6:-0}"

    if [[ ! -f "$jsonl_path" ]]; then
        echo "{}"
        return
    fi

    # Single-pass jq extraction using reduce inputs (streaming, memory-efficient)
    # Pass feature flags to skip expensive operations when disabled
    jq -n --arg jsonl_path "$jsonl_path" \
        --argjson loc_on "$loc_enabled" \
        --argjson feat_on "$features_enabled" \
        --argjson err_on "$errors_enabled" \
        --argjson think_on "$thinking_enabled" \
        --argjson ctx_on "$context_enabled" '
    reduce (inputs | select(. != null and . != "")) as $line (
        {
            models: {},
            tools: {},
            tool_errors: 0,
            turns: 0,
            turn_ms: 0,
            first_ts: null,
            last_ts: null,
            api_requests: 0,
            git_branch: null,
            files_read: {},
            files_edited: {},
            files_created: {},
            # v3 new fields
            pending_tools: {},
            error_details: [],
            loc_added: 0,
            loc_removed: 0,
            user_prompts: 0,
            thinking_blocks: 0,
            peak_input: 0,
            mcp_servers: {},
            agents: {},
            skills: [],
            has_teams: false,
            has_plan_mode: false
        };

        if $line.type == "assistant" and $line.message.usage != null then
            .api_requests += 1 |
            .models[$line.message.model] = {
                requests: ((.models[$line.message.model].requests // 0) + 1),
                input: ((.models[$line.message.model].input // 0) + $line.message.usage.input_tokens),
                output: ((.models[$line.message.model].output // 0) + $line.message.usage.output_tokens),
                cache_read: ((.models[$line.message.model].cache_read // 0) + ($line.message.usage.cache_read_input_tokens // 0)),
                cache_create: ((.models[$line.message.model].cache_create // 0) + ($line.message.usage.cache_creation_input_tokens // 0))
            } |
            # Context window tracking (peak input tokens)
            if $ctx_on == 1 then
                (($line.message.usage.input_tokens + ($line.message.usage.cache_read_input_tokens // 0)) as $ctx |
                if $ctx > .peak_input then .peak_input = $ctx else . end)
            else . end |
            # Thinking blocks count
            if $think_on == 1 then
                .thinking_blocks += ([($line.message.content[]? | select(.type == "thinking"))] | length)
            else . end |
            # Extract tool_use blocks: count tools, track files, features, errors, LOC
            (reduce ($line.message.content[]? | select(.type == "tool_use")) as $block (.;
                .tools[$block.name] = ((.tools[$block.name] // 0) + 1) |
                # Track pending tools for error mapping
                (if $err_on == 1 and ($block.id // null) != null then
                    .pending_tools[$block.id] = $block.name
                else . end) |
                # File tracking
                if ($block.name == "Read") and (($block.input.file_path // null) != null) then
                    .files_read[$block.input.file_path] = true
                elif ($block.name == "Edit" or $block.name == "MultiEdit") and (($block.input.file_path // null) != null) then
                    .files_edited[$block.input.file_path] = ((.files_edited[$block.input.file_path] // 0) + 1) |
                    # LOC tracking for Edit
                    if $loc_on == 1 and $block.name == "Edit" then
                        .loc_removed += (($block.input.old_string // "") | split("\n") | length) |
                        .loc_added += (($block.input.new_string // "") | split("\n") | length)
                    else . end
                elif ($block.name == "Write") and (($block.input.file_path // null) != null) then
                    .files_created[$block.input.file_path] = true |
                    # LOC tracking for Write
                    if $loc_on == 1 then
                        .loc_added += (($block.input.content // "") | split("\n") | length)
                    else . end
                else . end |
                # Features detection
                if $feat_on == 1 then
                    if ($block.name | startswith("mcp__")) then
                        (($block.name | split("__") | .[1]) // "unknown") as $server |
                        .mcp_servers[$server] = ((.mcp_servers[$server] // 0) + 1)
                    elif $block.name == "Task" then
                        (($block.input.subagent_type // "unknown") | tostring) as $atype |
                        .agents[$atype] = ((.agents[$atype] // 0) + 1)
                    elif $block.name == "Skill" then
                        .skills += [(($block.input.skill // "unknown") | tostring)]
                    elif $block.name == "TeamCreate" then
                        .has_teams = true
                    elif $block.name == "EnterPlanMode" then
                        .has_plan_mode = true
                    else . end
                else . end
            )) |
            # Extract git branch from JSONL entries (fallback for session meta)
            (if .git_branch == null and $line.gitBranch != null then .git_branch = $line.gitBranch else . end)
        elif $line.type == "user" then
            # Count tool errors + map to tool names
            (reduce ($line.message.content[]? | select(.type == "tool_result" and .is_error == true)) as $err (.;
                .tool_errors += 1 |
                if $err_on == 1 then
                    ((.pending_tools[$err.tool_use_id] // "unknown") as $tool_name |
                    (($err.content // ($err.output // "")) | tostring | if length > 80 then .[:77] + "..." else . end) as $msg |
                    .error_details += [{tool: $tool_name, message: $msg}])
                else . end
            )) |
            # Count user interactive prompts (messages with text content, not just tool results)
            if ([($line.message.content[]? | select(.type == "text"))] | length) > 0 then
                .user_prompts += 1
            else . end
        elif $line.type == "system" and $line.subtype == "turn_duration" then
            .turns += 1 | .turn_ms += $line.durationMs
        else . end |

        if $line.timestamp != null then
            (if .first_ts == null then .first_ts = $line.timestamp else . end) |
            .last_ts = $line.timestamp
        else . end
    ) |
    # Clean up pending_tools (internal tracking only)
    del(.pending_tools)
    ' "$jsonl_path"
}

get_session_meta() {
    local session_id="$1"
    local cwd="$2"

    local encoded_path
    encoded_path=$(echo "$cwd" | tr '/' '-')
    local index_path="$HOME/.claude/projects/${encoded_path}/sessions-index.json"

    if [[ ! -f "$index_path" ]]; then
        echo "{}"
        return
    fi

    jq --arg sid "$session_id" '
        .entries[]? | select(.sessionId == $sid) | {
            summary: .summary,
            gitBranch: .gitBranch,
            messageCount: .messageCount
        }
    ' "$index_path" 2>/dev/null || echo "{}"
}

calculate_cost() {
    local session_id="$1"
    local session_data="$2"

    # Try ccusage first (with timeout)
    if command -v ccusage &> /dev/null; then
        local cost
        cost=$(timeout 5s ccusage session --id "$session_id" --json --offline 2>/dev/null | jq -r '.totalCost // empty' || echo "")

        if [[ -n "$cost" ]]; then
            echo "$cost"
            return
        fi
    fi

    # Fallback: calculate from pricing table
    local total_cost=0

    while IFS= read -r model_entry; do
        local model
        model=$(echo "$model_entry" | jq -r '.model')
        local input
        input=$(echo "$model_entry" | jq -r '.input')
        local output
        output=$(echo "$model_entry" | jq -r '.output')

        # Shorten model name to match pricing keys
        local model_short
        model_short=$(shorten_model_name "$model")

        local input_price
        input_price=$(get_pricing "$model_short" "input")
        local output_price
        output_price=$(get_pricing "$model_short" "output")

        # Cost = (tokens / 1M) * price_per_M
        local model_cost
        model_cost=$(bc <<< "scale=4; ($input / 1000000) * $input_price + ($output / 1000000) * $output_price")
        total_cost=$(bc <<< "scale=4; $total_cost + $model_cost")
    done < <(echo "$session_data" | jq -c '.models | to_entries[] | {model: .key, input: .value.input, output: .value.output}')

    echo "$total_cost"
}

# ═══════════════════════════════════════════════════════════════════════════
# Section Renderers (each returns a string, empty if no data)
# ═══════════════════════════════════════════════════════════════════════════

# Shared state populated by format_output() before calling renderers
_SD=""          # session_data JSON
_SM=""          # session_meta JSON
_SID=""         # session_id
_BRANCH=""      # git branch
_COST=""        # cost string
_RTK=""         # rtk_data JSON
_GIT_DIFF=""    # git diff JSON
_EXIT_REASON="" # exit reason

# Pre-computed values shared across renderers
_TOOL_CALLS_TOTAL=0
_TOOL_OK=0
_TOOL_ERRORS=0
_TOTAL_INPUT=0
_TOTAL_OUTPUT=0
_TOTAL_CACHE_READ=0
_TOTAL_CACHE_CREATE=0
_TURNS=0
_TURN_MS=0
_WALL_MS=0

render_meta() {
    local session_name
    session_name=$(echo "$_SM" | jq -r '.summary // "Unnamed session"')
    local out=""
    out+="${DIM}ID:${RESET}       ${_SID:0:16}..."$'\n'
    out+="${DIM}Name:${RESET}     $session_name"$'\n'
    out+="${DIM}Branch:${RESET}   $_BRANCH"
    echo "$out"
}

render_duration() {
    local wall_str active_str
    wall_str=$(format_duration "$_WALL_MS")
    active_str=$(format_duration "$_TURN_MS")
    local turn_label="turns"
    [[ $_TURNS -eq 1 ]] && turn_label="turn"

    local line="${DIM}Duration:${RESET} Wall ${wall_str} | Active ${active_str} | ${_TURNS} ${turn_label}"
    [[ -n "$_EXIT_REASON" ]] && line+=" | Exit: ${_EXIT_REASON}"
    echo "$line"
}

render_tools() {
    local tools_line=""
    while IFS= read -r tool_entry; do
        local tool count
        tool=$(echo "$tool_entry" | jq -r '.tool')
        count=$(echo "$tool_entry" | jq -r '.count')
        tools_line+="  ${CYAN}$tool:${RESET} $count"
    done < <(echo "$_SD" | jq -c '.tools | to_entries[] | {tool: .key, count: .value}' | sort -t':' -k2 -rn | head -8)

    local out=""
    out+="${DIM}Tool Calls:${RESET} $_TOOL_CALLS_TOTAL ${GREEN}(OK $_TOOL_OK / ERR $_TOOL_ERRORS)${RESET}"$'\n'
    out+="$tools_line"
    echo "$out"
}

render_errors() {
    local error_count
    error_count=$(echo "$_SD" | jq '.error_details | length')
    [[ "$error_count" == "0" || "$error_count" == "null" ]] && return

    local out=""
    out+="${DIM}Errors:${RESET} ${RED}${error_count}${RESET}"

    # Group errors by tool, show count and first message
    local grouped
    grouped=$(echo "$_SD" | jq -r '
        .error_details | group_by(.tool) | .[] |
        (.[0].tool) as $tool |
        (length) as $count |
        (.[0].message | gsub("\n"; " ")) as $msg |
        "  \($tool): \"\($msg)\" (x\($count))"
    ')
    [[ -n "$grouped" ]] && out+=$'\n'"$grouped"
    echo "$out"
}

render_files() {
    local file_stats
    file_stats=$(echo "$_SD" | jq '
        . as $data |
        {
            read_only: [.files_read | keys[] | . as $p | select(($data.files_edited | has($p)) | not) | select(($data.files_created | has($p)) | not)] | length,
            edited: (.files_edited | length),
            created_only: [.files_created | keys[] | . as $p | select(($data.files_edited | has($p)) | not)] | length,
            top_edited: [.files_edited | to_entries | sort_by(-.value) | .[:5][] | {name: (.key | split("/") | last), count: .value}]
        }
    ')

    local read_only edited created_only
    read_only=$(echo "$file_stats" | jq -r '.read_only')
    edited=$(echo "$file_stats" | jq -r '.edited')
    created_only=$(echo "$file_stats" | jq -r '.created_only')

    local total_files=$((read_only + edited + created_only))
    [[ $total_files -eq 0 ]] && return

    local parts=""
    [[ $read_only -gt 0 ]] && parts+="$read_only read"
    [[ $edited -gt 0 ]] && { [[ -n "$parts" ]] && parts+=" · "; parts+="$edited edited"; }
    [[ $created_only -gt 0 ]] && { [[ -n "$parts" ]] && parts+=" · "; parts+="$created_only created"; }

    local out="${DIM}Files:${RESET} $parts"

    local top_edited
    top_edited=$(echo "$file_stats" | jq -r '.top_edited | map("\(.name) (\(.count) edits)") | join(", ")')
    [[ -n "$top_edited" ]] && out+=$'\n'"  $top_edited"
    echo "$out"
}

render_features() {
    local parts=""

    # MCP servers
    local mcp_count
    mcp_count=$(echo "$_SD" | jq '.mcp_servers | length')
    if [[ "$mcp_count" != "0" && "$mcp_count" != "null" ]]; then
        local mcp_detail
        mcp_detail=$(echo "$_SD" | jq -r '.mcp_servers | to_entries | sort_by(-.value) | map("\(.key) x\(.value)") | join(", ")')
        parts+="MCP ($mcp_detail)"
    fi

    # Agents
    local agent_count
    agent_count=$(echo "$_SD" | jq '.agents | length')
    if [[ "$agent_count" != "0" && "$agent_count" != "null" ]]; then
        local agent_detail
        agent_detail=$(echo "$_SD" | jq -r '.agents | to_entries | sort_by(-.value) | map("\(.key) x\(.value)") | join(", ")')
        [[ -n "$parts" ]] && parts+=" · "
        parts+="Agents ($agent_detail)"
    fi

    # Skills
    local skill_count
    skill_count=$(echo "$_SD" | jq '.skills | unique | length')
    if [[ "$skill_count" != "0" && "$skill_count" != "null" ]]; then
        local skill_list
        skill_list=$(echo "$_SD" | jq -r '.skills | unique | join(", ")')
        [[ -n "$parts" ]] && parts+=" · "
        parts+="Skills ($skill_list)"
    fi

    # Teams
    local has_teams
    has_teams=$(echo "$_SD" | jq -r '.has_teams')
    if [[ "$has_teams" == "true" ]]; then
        [[ -n "$parts" ]] && parts+=" · "
        parts+="Teams"
    fi

    # Plan mode
    local has_plan
    has_plan=$(echo "$_SD" | jq -r '.has_plan_mode')
    if [[ "$has_plan" == "true" ]]; then
        [[ -n "$parts" ]] && parts+=" · "
        parts+="Plan mode"
    fi

    [[ -z "$parts" ]] && return
    echo "${DIM}Features:${RESET} $parts"
}

render_git() {
    [[ -z "$_GIT_DIFF" || "$_GIT_DIFF" == "{}" ]] && return

    local files ins del
    files=$(echo "$_GIT_DIFF" | jq -r '.files_changed')
    ins=$(echo "$_GIT_DIFF" | jq -r '.insertions')
    del=$(echo "$_GIT_DIFF" | jq -r '.deletions')

    [[ "$files" == "0" ]] && return

    local file_label="files"
    [[ "$files" == "1" ]] && file_label="file"
    echo "${DIM}Git:${RESET} ${GREEN}+${ins}${RESET} ${RED}-${del}${RESET} lines · ${files} ${file_label} changed"
}

render_loc() {
    local loc_added loc_removed
    loc_added=$(echo "$_SD" | jq -r '.loc_added // 0')
    loc_removed=$(echo "$_SD" | jq -r '.loc_removed // 0')

    [[ "$loc_added" == "0" && "$loc_removed" == "0" ]] && return
    echo "${DIM}Code:${RESET} ${GREEN}+${loc_added}${RESET} ${RED}-${loc_removed}${RESET} net (via Edit/Write)"
}

render_models() {
    local models_section=""
    while IFS= read -r model_entry; do
        local model requests input output cache_read cache_create
        model=$(echo "$model_entry" | jq -r '.model')
        requests=$(echo "$model_entry" | jq -r '.requests')
        input=$(echo "$model_entry" | jq -r '.input')
        output=$(echo "$model_entry" | jq -r '.output')

        local model_short input_fmt output_fmt
        model_short=$(shorten_model_name "$model")
        input_fmt=$(format_number "$input")
        output_fmt=$(format_number "$output")

        models_section+="$(printf "${CYAN}%-20s${RESET} %4d   %7s   %6s\n" "$model_short" "$requests" "$input_fmt" "$output_fmt")"
    done < <(echo "$_SD" | jq -c '.models | to_entries[] | {model: .key, requests: .value.requests, input: .value.input, output: .value.output}')

    local out=""
    out+="${DIM}Model Usage${RESET}         Reqs    Input    Output"$'\n'
    out+="$models_section"
    echo -n "$out"
}

render_cache() {
    [[ $_TOTAL_CACHE_READ -eq 0 && $_TOTAL_CACHE_CREATE -eq 0 ]] && return

    local cache_hit_rate="0"
    local cache_denominator=$((_TOTAL_CACHE_READ + _TOTAL_INPUT))
    if [[ $cache_denominator -gt 0 ]]; then
        cache_hit_rate=$(bc <<< "scale=0; $_TOTAL_CACHE_READ * 100 / $cache_denominator")
    fi
    echo "Cache: ${cache_hit_rate}% hit rate ($(format_number $_TOTAL_CACHE_READ) read / $(format_number $_TOTAL_CACHE_CREATE) created)"
}

render_cost() {
    [[ -z "$_COST" || "$_COST" == "0" ]] && return
    echo "Est. Cost: ${GREEN}\$$(printf "%.3f" "$_COST")${RESET}"
}

render_rtk() {
    [[ -z "$_RTK" ]] && return

    local rtk_cmds rtk_tokens rtk_pct rtk_estimated rtk_commands
    rtk_cmds=$(echo "$_RTK" | jq -r '.cmds')
    rtk_tokens=$(echo "$_RTK" | jq -r '.tokens_saved')
    rtk_pct=$(echo "$_RTK" | jq -r '.pct')
    rtk_estimated=$(echo "$_RTK" | jq -r '.estimated')
    rtk_commands=$(echo "$_RTK" | jq -r '.commands')

    local est_prefix=""
    [[ "$rtk_estimated" == "true" ]] && est_prefix="est. "

    local out=""
    if [[ $rtk_tokens -gt 0 ]]; then
        out="RTK Savings: $rtk_cmds cmds · ~$(format_number "$rtk_tokens") tokens saved (${est_prefix}${rtk_pct}%)"
    else
        out="RTK Savings: $rtk_cmds cmds rewritten"
    fi
    [[ -n "$rtk_commands" ]] && out+=$'\n'"  $rtk_commands"
    echo "$out"
}

render_ratio() {
    local user_prompts turns
    user_prompts=$(echo "$_SD" | jq -r '.user_prompts // 0')
    turns=$_TURNS

    [[ $turns -eq 0 ]] && return

    local auto_turns=$((turns - user_prompts))
    [[ $auto_turns -lt 0 ]] && auto_turns=0

    local avg_sec=""
    if [[ $_TURN_MS -gt 0 && $turns -gt 0 ]]; then
        avg_sec=$(bc <<< "scale=1; $_TURN_MS / 1000 / $turns")
        avg_sec="${avg_sec}s/turn"
    fi

    local turn_label="turns"
    [[ $turns -eq 1 ]] && turn_label="turn"

    local out="${DIM}Turns:${RESET} ${turns} (${user_prompts} interactive · ${auto_turns} auto)"
    [[ -n "$avg_sec" ]] && out+=" · Avg ${avg_sec}"
    echo "$out"
}

render_thinking() {
    local thinking_blocks
    thinking_blocks=$(echo "$_SD" | jq -r '.thinking_blocks // 0')
    [[ "$thinking_blocks" == "0" ]] && return
    echo "${DIM}Thinking:${RESET} ${thinking_blocks} blocks"
}

render_context() {
    local peak_input
    peak_input=$(echo "$_SD" | jq -r '.peak_input // 0')
    [[ "$peak_input" == "0" ]] && return

    # Estimate context limit based on model (200K default)
    local ctx_limit=200000
    local pct
    pct=$(bc <<< "scale=0; $peak_input * 100 / $ctx_limit")

    echo "${DIM}Context:${RESET} ~${pct}% peak (est.) · Model limit: $(format_number $ctx_limit)"
}

# ═══════════════════════════════════════════════════════════════════════════
# Output Orchestrator
# ═══════════════════════════════════════════════════════════════════════════

format_output() {
    local session_id="$1"
    local session_meta="$2"
    local session_data="$3"
    local cost="$4"
    local git_branch="${5:-unknown}"
    local rtk_data="${6:-}"
    local exit_reason="${7:-}"
    local git_diff_data="${8:-}"

    # Set shared state for renderers
    _SD="$session_data"
    _SM="$session_meta"
    _SID="$session_id"
    _BRANCH="$git_branch"
    _COST="$cost"
    _RTK="$rtk_data"
    _GIT_DIFF="$git_diff_data"
    _EXIT_REASON="$exit_reason"

    # Extract session data
    local api_requests
    api_requests=$(echo "$session_data" | jq -r '.api_requests // 0')

    # Handle empty session
    if [[ $api_requests -eq 0 ]]; then
        local session_name
        session_name=$(echo "$session_meta" | jq -r '.summary // "Unnamed session"')
        local buf=""
        buf+=$'\n'
        buf+="${BOLD}═══ Session Summary ═══════════════════${RESET}"$'\n'
        buf+="${DIM}ID:${RESET}     ${session_id:0:16}..."$'\n'
        buf+="${DIM}Name:${RESET}   $session_name"$'\n'
        buf+="${DIM}Branch:${RESET} $git_branch"$'\n'
        buf+="${DIM}Status:${RESET} ${YELLOW}Empty session (no API requests)${RESET}"$'\n'
        buf+="${BOLD}═══════════════════════════════════════${RESET}"$'\n'
        printf '%s\n' "$buf" > "$OUTPUT_TARGET"
        return
    fi

    # Pre-compute shared values for renderers
    local first_ts last_ts
    first_ts=$(echo "$session_data" | jq -r '.first_ts // 0')
    last_ts=$(echo "$session_data" | jq -r '.last_ts // 0')
    _TURN_MS=$(echo "$session_data" | jq -r '.turn_ms // 0')
    _TURNS=$(echo "$session_data" | jq -r '.turns // 0')

    _WALL_MS=0
    if [[ $first_ts != "null" && $last_ts != "null" && $first_ts != "0" && $last_ts != "0" ]]; then
        _WALL_MS=$(jq -n --arg first "$first_ts" --arg last "$last_ts" '
            (($last | split(".")[0] + "Z" | fromdate) - ($first | split(".")[0] + "Z" | fromdate)) * 1000
        ' 2>/dev/null || echo "0")
    fi

    _TOOL_ERRORS=$(echo "$session_data" | jq -r '.tool_errors // 0')
    _TOOL_CALLS_TOTAL=0
    while IFS= read -r tool_entry; do
        local count
        count=$(echo "$tool_entry" | jq -r '.count')
        _TOOL_CALLS_TOTAL=$((_TOOL_CALLS_TOTAL + count))
    done < <(echo "$session_data" | jq -c '.tools | to_entries[] | {count: .value}')
    _TOOL_OK=$((_TOOL_CALLS_TOTAL > _TOOL_ERRORS ? _TOOL_CALLS_TOTAL - _TOOL_ERRORS : _TOOL_CALLS_TOTAL))

    # Pre-compute token totals for cache/cost renderers
    _TOTAL_INPUT=0 _TOTAL_OUTPUT=0 _TOTAL_CACHE_READ=0 _TOTAL_CACHE_CREATE=0
    while IFS= read -r model_entry; do
        local input output cache_read cache_create
        input=$(echo "$model_entry" | jq -r '.input')
        output=$(echo "$model_entry" | jq -r '.output')
        cache_read=$(echo "$model_entry" | jq -r '.cache_read')
        cache_create=$(echo "$model_entry" | jq -r '.cache_create')
        _TOTAL_INPUT=$((_TOTAL_INPUT + input))
        _TOTAL_OUTPUT=$((_TOTAL_OUTPUT + output))
        _TOTAL_CACHE_READ=$((_TOTAL_CACHE_READ + cache_read))
        _TOTAL_CACHE_CREATE=$((_TOTAL_CACHE_CREATE + cache_create))
    done < <(echo "$session_data" | jq -c '.models | to_entries[] | {input: .value.input, output: .value.output, cache_read: .value.cache_read, cache_create: .value.cache_create}')

    # Render sections in configured order
    local buf=""
    buf+=$'\n'
    buf+="${BOLD}═══ Session Summary ═══════════════════${RESET}"$'\n'

    local section_output
    IFS=',' read -ra sections <<< "$SECTION_ORDER"
    for section in "${sections[@]}"; do
        section=$(echo "$section" | tr -d ' ')  # trim whitespace
        if is_section_enabled "$section" && type "render_${section}" &>/dev/null; then
            section_output=$(render_${section})
            if [[ -n "$section_output" ]]; then
                buf+="$section_output"$'\n'
            fi
        fi
    done

    buf+="${BOLD}═══════════════════════════════════════${RESET}"$'\n'

    printf '%s\n' "$buf" > "$OUTPUT_TARGET"
}

log_summary() {
    local session_id="$1"
    local session_meta="$2"
    local session_data="$3"
    local cost="$4"
    local cwd="$5"
    local git_branch="${6:-unknown}"
    local rtk_data="${7:-}"
    local exit_reason="${8:-}"
    local git_diff_data="${9:-}"

    # Ensure log directory exists
    mkdir -p "$LOG_DIR"

    local log_file="$LOG_DIR/session-summaries.jsonl"

    # Calculate total tokens
    local total_input=0 total_output=0 total_cache_read=0 total_cache_create=0

    while IFS= read -r model_entry; do
        local input output cache_read cache_create
        input=$(echo "$model_entry" | jq -r '.input')
        output=$(echo "$model_entry" | jq -r '.output')
        cache_read=$(echo "$model_entry" | jq -r '.cache_read')
        cache_create=$(echo "$model_entry" | jq -r '.cache_create')

        total_input=$((total_input + input))
        total_output=$((total_output + output))
        total_cache_read=$((total_cache_read + cache_read))
        total_cache_create=$((total_cache_create + cache_create))
    done < <(echo "$session_data" | jq -c '.models | to_entries[] | {input: .value.input, output: .value.output, cache_read: .value.cache_read, cache_create: .value.cache_create}')

    # Calculate wall time for log
    local first_ts last_ts
    first_ts=$(echo "$session_data" | jq -r '.first_ts // "0"')
    last_ts=$(echo "$session_data" | jq -r '.last_ts // "0"')

    local duration_wall_ms=0
    if [[ $first_ts != "null" && $last_ts != "null" && $first_ts != "0" && $last_ts != "0" ]]; then
        duration_wall_ms=$(jq -n --arg first "$first_ts" --arg last "$last_ts" '
            (($last | split(".")[0] + "Z" | fromdate) - ($first | split(".")[0] + "Z" | fromdate)) * 1000
        ' 2>/dev/null || echo "0")
    fi

    # Cache hit rate
    local cache_hit_rate="0"
    local cache_denominator=$((total_cache_read + total_input))
    if [[ $cache_denominator -gt 0 ]]; then
        cache_hit_rate=$(bc <<< "scale=1; $total_cache_read * 100 / $cache_denominator")
        [[ "$cache_hit_rate" == .* ]] && cache_hit_rate="0$cache_hit_rate"
    fi

    # File stats
    local file_stats
    file_stats=$(echo "$session_data" | jq '
        . as $data |
        {
            read_only: [.files_read | keys[] | . as $p | select(($data.files_edited | has($p)) | not) | select(($data.files_created | has($p)) | not)] | length,
            edited: (.files_edited | length),
            created: [.files_created | keys[] | . as $p | select(($data.files_edited | has($p)) | not)] | length,
            top_edited: [.files_edited | to_entries | sort_by(-.value) | .[:5][] | {name: (.key | split("/") | last), count: .value}]
        }
    ')

    # RTK savings for log (JSON or null)
    local rtk_json="${rtk_data:-null}"
    [[ -z "$rtk_json" ]] && rtk_json="null"

    # Git diff for log (JSON or null)
    local git_json="${git_diff_data:-null}"
    [[ -z "$git_json" || "$git_json" == "{}" ]] && git_json="null"

    # v3 new fields from session_data
    local error_details loc_added loc_removed user_prompts thinking_blocks peak_input
    error_details=$(echo "$session_data" | jq -c '.error_details // []')
    loc_added=$(echo "$session_data" | jq -r '.loc_added // 0')
    loc_removed=$(echo "$session_data" | jq -r '.loc_removed // 0')
    user_prompts=$(echo "$session_data" | jq -r '.user_prompts // 0')
    thinking_blocks=$(echo "$session_data" | jq -r '.thinking_blocks // 0')
    peak_input=$(echo "$session_data" | jq -r '.peak_input // 0')

    # Features for log
    local mcp_servers agents skills has_teams has_plan_mode
    mcp_servers=$(echo "$session_data" | jq -c '.mcp_servers // {}')
    agents=$(echo "$session_data" | jq -c '.agents // {}')
    skills=$(echo "$session_data" | jq -c '.skills | unique // []')
    has_teams=$(echo "$session_data" | jq -r '.has_teams // false')
    has_plan_mode=$(echo "$session_data" | jq -r '.has_plan_mode // false')

    # Build log entry
    local log_entry
    log_entry=$(jq -cn \
        --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        --arg session_id "$session_id" \
        --arg session_name "$(echo "$session_meta" | jq -r '.summary // "Unnamed"')" \
        --arg git_branch "$git_branch" \
        --arg project "$cwd" \
        --arg exit_reason "${exit_reason:-unknown}" \
        --argjson duration_wall_ms "$duration_wall_ms" \
        --argjson duration_active_ms "$(echo "$session_data" | jq -r '.turn_ms // 0')" \
        --argjson turns "$(echo "$session_data" | jq -r '.turns // 0')" \
        --argjson user_prompts "$user_prompts" \
        --argjson api_requests "$(echo "$session_data" | jq -r '.api_requests // 0')" \
        --argjson tool_calls "$(echo "$session_data" | jq -c '.tools // {}')" \
        --argjson tool_errors "$(echo "$session_data" | jq -r '.tool_errors // 0')" \
        --argjson error_details "$error_details" \
        --argjson models "$(echo "$session_data" | jq -c '.models // {}')" \
        --argjson total_input "$total_input" \
        --argjson total_output "$total_output" \
        --argjson total_cache_read "$total_cache_read" \
        --argjson total_cache_create "$total_cache_create" \
        --argjson cache_hit_rate "$cache_hit_rate" \
        --argjson files "$file_stats" \
        --argjson loc_added "$loc_added" \
        --argjson loc_removed "$loc_removed" \
        --argjson git_diff "$git_json" \
        --argjson thinking_blocks "$thinking_blocks" \
        --argjson peak_input "$peak_input" \
        --argjson mcp_servers "$mcp_servers" \
        --argjson agents "$agents" \
        --argjson skills "$skills" \
        --argjson has_teams "$has_teams" \
        --argjson has_plan_mode "$has_plan_mode" \
        --argjson rtk_savings "$rtk_json" \
        --arg cost_usd "${cost:-0}" \
        '{
            timestamp: $timestamp,
            session_id: $session_id,
            session_name: $session_name,
            git_branch: $git_branch,
            project: $project,
            exit_reason: $exit_reason,
            duration_wall_ms: $duration_wall_ms,
            duration_active_ms: $duration_active_ms,
            turns: $turns,
            user_prompts: $user_prompts,
            api_requests: $api_requests,
            tool_calls: $tool_calls,
            tool_errors: $tool_errors,
            error_details: $error_details,
            models: $models,
            total_tokens: {
                input: $total_input,
                output: $total_output,
                cache_read: $total_cache_read,
                cache_create: $total_cache_create
            },
            cache_hit_rate: $cache_hit_rate,
            files: $files,
            loc: { added: $loc_added, removed: $loc_removed },
            git_diff: $git_diff,
            thinking_blocks: $thinking_blocks,
            peak_input: $peak_input,
            features: {
                mcp_servers: $mcp_servers,
                agents: $agents,
                skills: $skills,
                has_teams: $has_teams,
                has_plan_mode: $has_plan_mode
            },
            rtk_savings: $rtk_savings,
            cost_usd: ($cost_usd | tonumber)
        }'
    )

    # Append to log file
    echo "$log_entry" >> "$log_file"
}

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

main() {
    # Skip if disabled
    if [[ "$SKIP" == "1" ]]; then
        exit 0
    fi

    # Check dependencies
    check_dependencies

    # Read hook input (SessionEnd receives JSON on stdin with session_id, transcript_path, cwd, reason)
    local input=""
    input=$(cat 2>/dev/null) || true

    # Extract session metadata from stdin JSON
    local session_id=""
    local cwd="${CLAUDE_PROJECT_DIR:-$(pwd)}"
    local exit_reason=""
    local transcript_path=""

    if [[ -n "$input" ]]; then
        session_id=$(echo "$input" | jq -r '.session_id // ""')
        cwd=$(echo "$input" | jq -r '.cwd // "'"$cwd"'"')
        transcript_path=$(echo "$input" | jq -r '.transcript_path // ""')

        # Parse exit reason from stdin
        local raw_reason
        raw_reason=$(echo "$input" | jq -r '.reason // ""')
        case "$raw_reason" in
            prompt_input_exit|user_exit) exit_reason="user" ;;
            clear)                       exit_reason="clear" ;;
            context_limit)               exit_reason="context" ;;
            api_error)                   exit_reason="error" ;;
            "")                          exit_reason="" ;;
            *)                           exit_reason="$raw_reason" ;;
        esac
    fi

    # Locate JSONL file: prefer transcript_path from stdin, then locate by session_id
    local jsonl_path=""

    if [[ -n "$transcript_path" && -f "$transcript_path" ]]; then
        jsonl_path="$transcript_path"
        # Extract session_id from transcript_path if not set
        [[ -z "$session_id" ]] && session_id=$(basename "$jsonl_path" .jsonl)
    fi

    if [[ -z "$jsonl_path" && -n "$session_id" ]]; then
        jsonl_path=$(locate_jsonl "$session_id" "$cwd")
    fi

    # Fallback: find most recently modified JSONL in project dir
    if [[ -z "$jsonl_path" || ! -f "$jsonl_path" ]]; then
        local encoded_path
        encoded_path=$(echo "$cwd" | tr '/' '-')
        local project_dir="$HOME/.claude/projects/${encoded_path}"

        if [[ -d "$project_dir" ]]; then
            # Use subshell to avoid pipefail+SIGPIPE on ls|head with many files
            jsonl_path=$(set +o pipefail; ls -t "$project_dir"/*.jsonl 2>/dev/null | head -1)
        fi

        # Extract session_id from filename
        if [[ -n "$jsonl_path" ]]; then
            session_id=$(basename "$jsonl_path" .jsonl)
        fi
    fi

    # No session data found at all
    if [[ -z "$jsonl_path" || ! -f "$jsonl_path" ]]; then
        exit 0
    fi

    # Extract session data (pass feature flags to skip expensive ops when disabled)
    local session_data
    session_data=$(extract_session_data "$jsonl_path" \
        "$LOC_ENABLED" "$FEATURES_ENABLED" "$ERRORS_ENABLED" \
        "$THINKING_ENABLED" "$CONTEXT_ENABLED")

    # Get session metadata
    local session_meta
    session_meta=$(get_session_meta "$session_id" "$cwd")

    # Resolve git branch (session meta first, then JSONL fallback)
    local git_branch
    git_branch=$(echo "$session_meta" | jq -r '.gitBranch // empty' 2>/dev/null)
    if [[ -z "$git_branch" ]]; then
        git_branch=$(echo "$session_data" | jq -r '.git_branch // "unknown"')
    fi

    # Calculate cost
    local cost
    cost=$(calculate_cost "$session_id" "$session_data")

    # Calculate RTK savings (if enabled)
    local rtk_data=""
    if [[ "$RTK_ENABLED" == "1" ]]; then
        rtk_data=$(calculate_rtk_savings)
    fi

    # Collect git diff (if enabled)
    local git_diff_data=""
    if is_section_enabled "git"; then
        git_diff_data=$(collect_git_diff "$cwd")
    fi

    # Format and display output
    format_output "$session_id" "$session_meta" "$session_data" "$cost" "$git_branch" \
        "$rtk_data" "$exit_reason" "$git_diff_data"

    # Log summary
    log_summary "$session_id" "$session_meta" "$session_data" "$cost" "$cwd" "$git_branch" \
        "$rtk_data" "$exit_reason" "$git_diff_data"

    exit 0
}

main "$@"
