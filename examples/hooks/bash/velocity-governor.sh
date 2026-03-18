#!/usr/bin/env bash
# velocity-governor.sh — Claude Code PreToolUse hook
# Limite le débit de tokens pour éviter les rate limits API
#
# Variables d'environnement officielles Claude Code :
#   CLAUDE_PROJECT_DIR  — chemin absolu du projet
#   CLAUDE_VELOCITY_MAX_TPM — override du seuil (défaut : 50000 tokens/min)
#
# Headers API Anthropic pour le rate limiting :
#   anthropic-ratelimit-tokens-remaining
#   anthropic-ratelimit-tokens-reset
#   retry-after (sur 429)
#
# Installation : ajouter dans .claude/settings.json sous hooks.PreToolUse
# {
#   "hooks": {
#     "PreToolUse": [{ "matcher": ".*", "hooks": [{ "type": "command", "command": "bash examples/hooks/bash/velocity-governor.sh" }] }]
#   }
# }

set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────────────────
MAX_TOKENS_PER_MINUTE="${CLAUDE_VELOCITY_MAX_TPM:-50000}"
PROJECT_SLUG="${CLAUDE_PROJECT_DIR//\//-}"
STATE_FILE="/tmp/claude-velocity-${PROJECT_SLUG}.json"

# ── Lecture stdin (JSON fourni par Claude Code) ────────────────────────────────
input=$(cat)
# Contient : session_id, cwd, tool_name, tool_input (selon event PreToolUse)

# ── Récupération ou initialisation de l'état ──────────────────────────────────
now=$(date +%s)

if [[ -f "$STATE_FILE" ]]; then
  window_start=$(jq -r '.window_start // 0' "$STATE_FILE" 2>/dev/null || echo "$now")
  tokens_used=$(jq  -r '.tokens_used  // 0' "$STATE_FILE" 2>/dev/null || echo 0)
else
  window_start=$now
  tokens_used=0
fi

# ── Réinitialisation de la fenêtre glissante (60 secondes) ────────────────────
window_age=$(( now - window_start ))
if (( window_age >= 60 )); then
  window_start=$now
  tokens_used=0
fi

# ── Estimation conservative du coût de l'outil ────────────────────────────────
# 1 appel outil ≈ 500 tokens (lecture + écriture courte)
# Ajuster CLAUDE_VELOCITY_MAX_TPM selon votre tier API
estimated_tokens=500
new_total=$(( tokens_used + estimated_tokens ))

# ── Throttle si seuil dépassé ─────────────────────────────────────────────────
if (( new_total > MAX_TOKENS_PER_MINUTE )); then
  remaining=$(( 60 - window_age ))
  if (( remaining > 0 )); then
    # Attendre la fin de la fenêtre courante
    sleep "$remaining"
    window_start=$(date +%s)
    new_total=$estimated_tokens
  fi
fi

# ── Persistance de l'état ─────────────────────────────────────────────────────
jq -n \
  --argjson ws "$window_start" \
  --argjson tu "$new_total" \
  '{window_start: $ws, tokens_used: $tu}' > "$STATE_FILE"

# ── Laisser passer l'outil ─────────────────────────────────────────────────────
# exit 0 = continuer normalement
# exit 1 = bloquer l'outil (non utilisé ici, préférer le throttle)
exit 0
