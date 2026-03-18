#!/usr/bin/env bash
# detect-new-onboarding-topics.sh
# Detects CRITICAL/HIGH VALUE topics from resource evaluations not covered in onboarding_matrix
# Part of adaptive onboarding maintenance automation (v2.0.0, guide v3.23.0+)
# Usage: Run monthly or before releases to ensure new important topics are discoverable

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REFERENCE_YAML="$REPO_ROOT/machine-readable/reference.yaml"
EVALUATIONS_DIR="$REPO_ROOT/docs/resource-evaluations"

# Helper functions
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

gap() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

critical_gap() {
    echo -e "${RED}🚨 $1${NC}"
}

# Main scan
scan_evaluations() {
    info "Scanning resource evaluations for CRITICAL (5/5) and HIGH VALUE (4/5) topics..."
    echo ""

    # Extract all keys referenced in onboarding_matrix
    local matrix_keys
    matrix_keys=$(python3 <<'EOF'
import yaml
import sys

with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)

matrix = data.get('onboarding_matrix', {})

# Collect all keys
referenced = set()
for goal, levels in matrix.items():
    for level, profile in levels.items():
        if isinstance(profile, dict):
            if 'core' in profile:
                referenced.update(profile['core'])
            if 'adaptive' in profile:
                for item in profile['adaptive']:
                    if isinstance(item, dict) and 'topics' in item:
                        topics = item['topics']
                        if isinstance(topics, list):
                            referenced.update(topics)
                        else:
                            referenced.add(topics)
        elif isinstance(profile, list):
            referenced.update(profile)

print('|'.join(sorted(referenced)))
EOF
"$REFERENCE_YAML")

    # Check deep_dive keys
    local deep_dive_keys
    deep_dive_keys=$(python3 -c "import yaml; print('|'.join(yaml.safe_load(open('$REFERENCE_YAML')).get('deep_dive', {}).keys()))")

    # Scan evaluation files
    local critical_topics=()
    local high_topics=()
    local gaps=()
    local critical_gaps=()

    if [ ! -d "$EVALUATIONS_DIR" ]; then
        info "No evaluations directory found at $EVALUATIONS_DIR"
        return 0
    fi

    for eval_file in "$EVALUATIONS_DIR"/*.md; do
        if [ ! -f "$eval_file" ]; then
            continue
        fi

        # Extract score (look for "**Score**: X/5" or "Score: X/5")
        local score
        score=$(grep -oE '\*\*Score\*\*:?\s*[0-9]/5|Score:?\s*[0-9]/5' "$eval_file" | head -1 | grep -oE '[0-9]' || echo "0")

        # Extract topic/key (look for deep_dive references in evaluation)
        local topic_key
        topic_key=$(basename "$eval_file" .md | sed 's/-evaluation$//' | sed 's/-/_/g')

        # Check if it's CRITICAL or HIGH VALUE
        if [ "$score" -eq 5 ]; then
            critical_topics+=("$topic_key")
            # Check if in deep_dive
            if [[ "$deep_dive_keys" == *"$topic_key"* ]]; then
                # Check if in matrix
                if [[ "$matrix_keys" != *"$topic_key"* ]]; then
                    critical_gaps+=("$topic_key (5/5 CRITICAL, file: $(basename "$eval_file"))")
                fi
            fi
        elif [ "$score" -eq 4 ]; then
            high_topics+=("$topic_key")
            # Check if in deep_dive
            if [[ "$deep_dive_keys" == *"$topic_key"* ]]; then
                # Check if in matrix
                if [[ "$matrix_keys" != *"$topic_key"* ]]; then
                    gaps+=("$topic_key (4/5 HIGH VALUE, file: $(basename "$eval_file"))")
                fi
            fi
        fi
    done

    # Report
    echo "📊 Summary:"
    echo "  - CRITICAL (5/5) topics found: ${#critical_topics[@]}"
    echo "  - HIGH VALUE (4/5) topics found: ${#high_topics[@]}"
    echo ""

    if [ ${#critical_gaps[@]} -gt 0 ]; then
        critical_gap "Found ${#critical_gaps[@]} CRITICAL topics NOT in any onboarding profile:"
        for gap_item in "${critical_gaps[@]}"; do
            echo "    - $gap_item"
        done
        echo ""
    fi

    if [ ${#gaps[@]} -gt 0 ]; then
        gap "Found ${#gaps[@]} HIGH VALUE topics NOT in any onboarding profile:"
        for gap_item in "${gaps[@]}"; do
            echo "    - $gap_item"
        done
        echo ""
    fi

    if [ ${#critical_gaps[@]} -eq 0 ] && [ ${#gaps[@]} -eq 0 ]; then
        success "All CRITICAL and HIGH VALUE topics are covered in onboarding_matrix!"
        echo ""
        info "Covered topics:"
        for topic in "${critical_topics[@]}"; do
            if [[ "$matrix_keys" == *"$topic"* ]]; then
                echo "    ✅ $topic (5/5 CRITICAL)"
            fi
        done
        for topic in "${high_topics[@]}"; do
            if [[ "$matrix_keys" == *"$topic"* ]]; then
                echo "    ✅ $topic (4/5 HIGH VALUE)"
            fi
        done
        return 0
    else
        echo "💡 Action required:"
        echo "   Review the gaps above and consider adding them to relevant profiles in:"
        echo "   $REFERENCE_YAML (onboarding_matrix section)"
        echo ""
        echo "   See design doc: claudedocs/adaptive-onboarding-design.md"
        return 1
    fi
}

# Main
main() {
    echo "════════════════════════════════════════════════════════════════"
    echo "  Onboarding Topics Gap Detection (v2.0.0)"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    scan_evaluations
    local exit_code=$?

    echo ""
    echo "════════════════════════════════════════════════════════════════"
    if [ $exit_code -eq 0 ]; then
        success "No gaps detected - onboarding is up-to-date!"
    else
        gap "Gaps detected - review and update onboarding_matrix"
    fi
    echo "════════════════════════════════════════════════════════════════"

    exit $exit_code
}

main "$@"
