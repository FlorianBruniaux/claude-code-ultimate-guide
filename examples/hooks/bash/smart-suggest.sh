#!/bin/bash
# .claude/hooks/smart-suggest.sh
# Event: UserPromptSubmit
# Non-blocking behavioral coach: suggests the right command or agent based on detected intent
#
# Architecture: 3-tier priority system
#   Tier 0 — Enforcement: mandatory workflow gates (runs first, exits on match)
#   Tier 1 — Discovery: high-value tools the developer may not know exist
#   Tier 2 — Contextual: opportunistic suggestions for common patterns
#
# Properties:
#   - Max 1 suggestion per prompt (first match wins)
#   - Dedup guard: never suggest a command already in the prompt
#   - ROI logging: records suggestions to ~/.claude/logs/smart-suggest.jsonl
#   - Silent exit on no match (non-blocking, never fails)
#
# Customization: replace patterns with your own commands/agents.
# Keep Tier 0 small and precise — it intercepts before everything else.

set -euo pipefail

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null || true)

# Skip prompts that are too short to match anything meaningful
if [[ -z "$PROMPT" || ${#PROMPT} -lt 8 ]]; then
    exit 0
fi

PROMPT_LC=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Skip slash commands — user already knows what they want
if [[ "$PROMPT_LC" =~ ^/ ]]; then
    exit 0
fi

LABEL_CMD="Command"
LABEL_AGENT="Agent"

# ─── suggest() ────────────────────────────────────────────────────────────────
# Emits one suggestion then exits (guarantees max 1 suggestion per prompt).
# Dedup: if the command/agent name is already in the prompt, exits silently.
suggest() {
    local label="$1" name="$2" reason="$3"

    # Strip leading slash, take first token — prevents matching "pr" in "improve"
    # e.g. "/changelog:add" → "changelog:add", "code-reviewer" → "code-reviewer"
    local check
    check=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's|^/||' | awk '{print $1}')
    if echo "$PROMPT_LC" | grep -qF "$check"; then
        exit 0
    fi

    # Append to JSONL log for ROI measurement (non-blocking — failure is safe)
    local logdir="${HOME}/.claude/logs"
    mkdir -p "$logdir" 2>/dev/null || true
    printf '{"ts":"%s","suggested":"%s","prompt_len":%d}\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$name" "${#PROMPT}" \
        >> "$logdir/smart-suggest.jsonl" 2>/dev/null || true

    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "[Suggestion] $label: $name -- $reason"
  }
}
EOF
    exit 0
}

# ==============================================================================
# TIER 0 — Enforcement
# Intercepts workflow violations before any other suggestion.
# Keep patterns tight: a false positive here is more disruptive than a miss.
# ==============================================================================

# Changelog fragment enforcement
# If the developer signals intent to create a PR without mentioning a changelog
# fragment, redirect to the fragment creation step first.
# When fragment/skip-changelog is already mentioned → suggest the PR command normally.
if echo "$PROMPT_LC" | grep -qE '(create.*pr|open.*pr|make.*pr|pull.?request|push.*pr)'; then
    if ! echo "$PROMPT_LC" | grep -qE '(changelog|fragment|skip-changelog)'; then
        suggest "$LABEL_CMD" "pnpm changelog:add" \
            "REQUIRED before merge — creates changelog/fragments/{PR}-{slug}.yml (or add label 'skip-changelog' for tooling PRs)"
    else
        suggest "$LABEL_CMD" "/pr" \
            "PR creation with structured description and auto-detected scope"
    fi
fi

# Plan-before-code enforcement
# Intercepts implementation intent when no planning context is present.
# Negative lookahead excludes: plan, test, fix, review, explain, refactor.
if echo "$PROMPT_LC" | grep -qE '(implement|add (the|a|an)|create (the|a|an) (service|router|endpoint|feature|component)|write (the )?(code|logic|service))'; then
    if ! echo "$PROMPT_LC" | grep -qE '(plan|test|fix|bug|review|refactor|explain|why|how)'; then
        suggest "$LABEL_CMD" "/plan" \
            "Run /plan BEFORE coding — Research → Spec → Implement reduces rework"
    fi
fi

# ==============================================================================
# TIER 1 — Discovery
# High-value tools the developer may not know about.
# Use multi-word patterns to reduce false positives.
# ==============================================================================

# Failing tests — suggest auto-fix loop before generic debug
if echo "$PROMPT_LC" | grep -qE '(tests? (fail|broken|red)|fix (the |these )?tests?|tests? (are )?failing)'; then
    if ! echo "$PROMPT_LC" | grep -qE '(api|server|endpoint|500|404)'; then
        suggest "$LABEL_CMD" "/test-loop" \
            "Auto-fix loop: 1 test per cycle with convergence stats"
    fi
fi

# Lesson learned / rollback scenario
if echo "$PROMPT_LC" | grep -qE '(wrong approach|bad approach|should have|dead end|root cause was|lesson learned|introduced.*bug|regression)'; then
    suggest "$LABEL_CMD" "/retex" \
        "Capture this lesson in persistent memory (searchable across sessions)"
fi

# Code duplication detected
if echo "$PROMPT_LC" | grep -qE '(duplicat|copy.?past|same code|repeated (code|logic)|identical (code|function))'; then
    suggest "$LABEL_CMD" "/dupes" \
        "Detect copy-paste code with jscpd before the refactor"
fi

# Monitoring / polling intent — suggest background loop
if echo "$PROMPT_LC" | grep -qE '(check (every|each|all)|wait (until|for)|poll|monitor|watch.*for|when (it.?s |it is )?done|once (the )?deploy|once (the )?ci)'; then
    suggest "$LABEL_CMD" "/loop [interval] [prompt]" \
        "Run in background while you work: /loop 5m check the deploy status"
fi

# Security-sensitive keywords
if echo "$PROMPT_LC" | grep -qE '(sql injection|xss|owasp|vulnerability|security audit|auth bypass)'; then
    suggest "$LABEL_AGENT" "security-auditor" \
        "Read-only OWASP audit — detects injection, auth, and data exposure issues"
fi

# Release assembly — suggest structured release command
if echo "$PROMPT_LC" | grep -qE '(cut.*release|prepare.*release|new (version|release)|release.*[0-9]+\.[0-9]|tag.*version|deploy.*main|merge.*main)'; then
    suggest "$LABEL_CMD" "/release" \
        "Assembles fragments → CHANGELOG section, bumps version, creates release branch"
fi

# ==============================================================================
# TIER 2 — Contextual
# General patterns, lower priority, regex kept tight to avoid noise.
# ==============================================================================

# Code review before merge
if echo "$PROMPT_LC" | grep -qE '(review (the |this )?(code|pr|file)|code review|before (merge|merging))'; then
    suggest "$LABEL_AGENT" "code-reviewer" \
        "Quality + security + performance review"
fi

# Debugging — generic
if echo "$PROMPT_LC" | grep -qE '(debug (this|the)|fix (this |the )?(bug|crash|error)|stack trace|not (working|loading))'; then
    suggest "$LABEL_AGENT" "debugger" \
        "Systematic root cause analysis"
fi

# Architecture decision
if echo "$PROMPT_LC" | grep -qE '(architecture (decision|review)|system design|big refactor|large.*refactor)'; then
    suggest "$LABEL_AGENT" "architect-review" \
        "Validates architectural decisions across scalability, coupling, and tradeoffs"
fi

# Resume previous session
if echo "$PROMPT_LC" | grep -qE '(resume (session|work)|pick up (where|from)|continue (from )?(yesterday|last session))'; then
    suggest "$LABEL_CMD" "/resume" \
        "Restores session context from persistent memory"
fi

# No match — silent exit (never blocks the user)
exit 0
