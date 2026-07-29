#!/bin/bash
# Hook: UserPromptSubmit - Concierge: suggère agents/commandes pertinents
# Non-bloquant, pure bash, max 1 suggestion par prompt
# 22 patterns en 2 tiers : découverte (Tier 1) et contextuel (Tier 2)
# Logs ROI : ~/.claude/logs/smart-suggest.jsonl

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null || true)

# Exit early si prompt trop court
if [[ -z "$PROMPT" || ${#PROMPT} -lt 8 ]]; then
    exit 0
fi

PROMPT_LC=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Skip si déjà une slash command
if [[ "$PROMPT_LC" =~ ^/ ]]; then
    exit 0
fi

suggest() {
    local label="$1" name="$2" reason="$3"

    # Dedup : skip si le nom de la commande/agent est déjà dans le prompt
    local check
    check=$(echo "$name" | tr '[:upper:]' '[:lower:]' | sed 's|/||g; s|:||g; s| ||g')
    if echo "$PROMPT_LC" | grep -qF "$check"; then
        exit 0
    fi

    # Log pour mesure ROI (append, non-bloquant) — inclut le pattern suggéré
    local logdir="${HOME}/.claude/logs"
    mkdir -p "$logdir" 2>/dev/null || true
    printf '{"ts":"%s","suggested":"%s","label":"%s","prompt_len":%d}\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$name" "$label" "${#PROMPT}" \
        >> "$logdir/smart-suggest.jsonl" 2>/dev/null || true

    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "[Suggestion] $label : $name -- $reason"
  }
}
EOF
    exit 0
}

# ===========================================================================
# TIER 1 : Outils méconnus, haute valeur de découverte
# Regex multi-mots pour éviter les faux positifs
# ===========================================================================

# Retex / Lesson learned
if echo "$PROMPT_LC" | grep -qE '(rollback|revert|fausse piste|mauvaise approche|j.aurais d[uû]|bug introduit|regression|erreur de ma part|wrong approach|lesson learned|dead end|finalement c.etait|le vrai (probleme|souci)|root cause.*(etait|est))'; then
    suggest "Commande" "/retex" "Capture cette lesson dans memory (persistance cross-session)"
fi

# Whitepaper density / padding
if echo "$PROMPT_LC" | grep -qE '(padding|rempli|rhetoric|bullshit.*wp|whitepaper.*(creux|vide|remplissage|qualite)|densite.*whitepaper|substance.*wp)'; then
    suggest "Agent" "whitepaper-density" "Analyse ratio valeur/remplissage du whitepaper"
fi

# Whitepaper journalist review
if echo "$PROMPT_LC" | grep -qE '(regard.*(extern|journal)|critique.*(whitepaper|wp)|journali.*review|editorial.*(whitepaper|wp)|wp.*publication)'; then
    suggest "Agent" "whitepaper-journalist" "Review style journaliste avant publication"
fi

# Whitepaper coherence
if echo "$PROMPT_LC" | grep -qE '(coheren.*(whitepaper|wp)|contradiction.*(wp|whitepaper)|logique.*(wp|whitepaper)|rupture.*narrativ)'; then
    suggest "Agent" "whitepaper-coherence" "Audit cohérence globale du whitepaper"
fi

# PDF generation
if echo "$PROMPT_LC" | grep -qE '(genere.*(pdf|epub)|render.*(pdf|whitepaper)|build.*(pdf|wp)|quarto.*(render|build)|typst)'; then
    suggest "Skill" "/pdf-generator" "Aide contextuelle Quarto/Typst pour la génération PDF"
fi

# Landing sync
if echo "$PROMPT_LC" | grep -qE '(landing.*(sync|desync|desynchro)|sync.*(landing|site)|site.*(a jour|version|badge)|(badge|version).*(site|landing)|version.*landing|retard.*(site|badge|landing))'; then
    suggest "Commande" "/sync" "Vérifie la synchronisation guide ↔ landing"
fi

# Security audit complet
if echo "$PROMPT_LC" | grep -qE '(audit.*securit|securit.*audit|score.*securit|posture.*securit|owasp|vulnerabilit)'; then
    suggest "Commande" "/security-audit" "Audit sécurité complet 6 phases avec score /100"
fi

# Documentation audit
if echo "$PROMPT_LC" | grep -qE '(audit.*(doc|readme|guide)|qualite.*(doc|readme)|best.practice.*(doc|readme)|manque.*(doc|readme))'; then
    suggest "Commande" "/audit-repo-docs" "Audit documentation contre 85+ best practices"
fi

# LinkedIn post / guide reference
if echo "$PROMPT_LC" | grep -qE '(linkedin.*(post|comment|reponse)|repondr.*(linkedin|post)|commente.*(linkedin|article))'; then
    suggest "Commande" "/boldguy-linkedin-answer" "Draft commentaire LinkedIn avec référence guide"
fi

# Guide recap / social content
if echo "$PROMPT_LC" | grep -qE '(recap.*(semaine|week|guide)|social.*(content|post.*guide)|newsletter.*guide|post.*changelog)'; then
    suggest "Skill" "/guide-recap" "Transforme les CHANGELOG en posts LinkedIn/Twitter/Newsletter"
fi

# Park session
if echo "$PROMPT_LC" | grep -qE '(park.*(session|travail)|sauvegarder.*(session|contexte|progression)|fin de session|reprendre.*(demain|plus tard))'; then
    suggest "Commande" "/park" "Sauvegarde la session pour la reprendre plus tard"
fi

# Update whitepapers
if echo "$PROMPT_LC" | grep -qE '(mise a jour.*(whitepaper|wp)|update.*(whitepaper|wp)|synchroni.*(whitepaper|wp).*(changelog|release))'; then
    suggest "Skill" "/update-whitepapers" "Met à jour les whitepapers FR+EN depuis le CHANGELOG (équipe parallèle)"
fi

# ===========================================================================
# TIER 2 : Suggestion contextuelle (regex resserrées)
# ===========================================================================

# Release
if echo "$PROMPT_LC" | grep -qE '(faire.*(release|version)|bump.*(version|patch|minor|major)|nouvelle.*(version|release))'; then
    suggest "Commande" "/release" "Release complète : CHANGELOG + VERSION + sync + commit + push"
fi

# Changelog
if echo "$PROMPT_LC" | grep -qE '(voir.*(changelog|changement)|quoi de neuf|dernier.*(changement|commit|release))'; then
    suggest "Commande" "/changelog" "Affiche les dernières entrées CHANGELOG"
fi

# Version check
if echo "$PROMPT_LC" | grep -qE '(version.*(courante|actuelle|check)|stats.*(guide|repo)|combien.*(template|ligne))'; then
    suggest "Commande" "/version" "Affiche versions + stats (lignes, templates, agents)"
fi

# Code/config review
if echo "$PROMPT_LC" | grep -qE '(review.*(hook|script|config|command)|revue.*(code|config)|avant.*(commit|push|merge))'; then
    suggest "Agent" "code-reviewer" "Review qualité + sécurité + performance"
fi

# Debug hook/script
if echo "$PROMPT_LC" | grep -qE '(hook.*(marche pas|bug|error|ne fonctionne)|script.*(crash|error|bug|echec))'; then
    suggest "Agent" "debugger" "Debug méthodique avec root cause analysis"
fi

# Audit agents/skills config
if echo "$PROMPT_LC" | grep -qE '(audit.*(agent|skill|command|hook)|qualite.*(agent|skill)|config.*(claude|\.claude))'; then
    suggest "Commande" "/audit-agents-skills" "Audit qualité des agents, skills, commands"
fi

# Update threat DB
if echo "$PROMPT_LC" | grep -qE '(threat|menace.*(securit|nouveau)|base.*(securit|threat)|vuln.*(nouveau|recente))'; then
    suggest "Commande" "/update-threat-db" "Met à jour la base de données de menaces"
fi

# Audit prose whitepapers
if echo "$PROMPT_LC" | grep -qE '(prose.*(whitepaper|wp)|section.*(vide|bare|bare)|ajouter.*(contenu|prose).*(wp|whitepaper))'; then
    suggest "Skill" "/audit-prose" "Enrichit les sections vides des whitepapers (9 agents parallèles)"
fi

# Release notes
if echo "$PROMPT_LC" | grep -qE '(release.*(note|notes|announcement)|note.*(release|version)|slack.*(annonce|release))'; then
    suggest "Skill" "/release-notes-generator" "Génère release notes (CHANGELOG + PR body + Slack)"
fi

# Security quick check
if echo "$PROMPT_LC" | grep -qE '(verif.*(securit|config)|check.*(securit|threat|hook)|scan.*(config|securit))'; then
    suggest "Commande" "/security-check" "Vérifie la config contre les menaces connues (~30s)"
fi

# llms.txt / AI indexing sync
if echo "$PROMPT_LC" | grep -qE '(llms\.(txt|full)|ai.index|geo.*(guide|site)|indexing.*(llm|ai)|llm.*(index|sync)|update.*(llms|ai.index)|llms.*(a jour|sync|version|desync))'; then
    suggest "Action" "llms.txt + llms-full.txt + machine-readable/llms.txt" "Ces 3 fichiers doivent être mis à jour (version, stats) — voir Step 4 du /release"
fi

# reference.yaml sync
if echo "$PROMPT_LC" | grep -qE '(reference\.(yaml|yml)|reference.*yaml.*(a jour|sync|version)|yaml.*(index|reference).*(a jour|sync))'; then
    suggest "Fichier" "machine-readable/reference.yaml" "Vérifier version + updated + entrées manquantes (cf. CHANGELOG)"
fi

# Aucun match - sortie silencieuse
exit 0
