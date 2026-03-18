#!/usr/bin/env bash
# validate-onboarding.sh
# Validates onboarding system integrity: YAML syntax, deep_dive keys, time budgets, etc.
# Part of adaptive onboarding architecture v2.0.0 (guide v3.23.0+)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REFERENCE_YAML="$REPO_ROOT/machine-readable/reference.yaml"
VERSION_FILE="$REPO_ROOT/VERSION"

# Counters
CHECKS_TOTAL=0
CHECKS_PASSED=0
CHECKS_FAILED=0

# Helper functions
pass() {
    ((CHECKS_PASSED++))
    ((CHECKS_TOTAL++))
    echo -e "${GREEN}✅ $1${NC}"
}

fail() {
    ((CHECKS_FAILED++))
    ((CHECKS_TOTAL++))
    echo -e "${RED}❌ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

info() {
    echo -e "${NC}ℹ️  $1${NC}"
}

# Check 1: YAML syntax valid
check_yaml_syntax() {
    info "Check 1: YAML syntax validation"
    if python3 -c "import yaml; yaml.safe_load(open('$REFERENCE_YAML'))" 2>/dev/null; then
        pass "YAML syntax valid"
    else
        fail "YAML syntax invalid - cannot parse reference.yaml"
        return 1
    fi
}

# Check 2: All deep_dive keys in onboarding_matrix exist
check_deep_dive_keys() {
    info "Check 2: Verifying all deep_dive keys exist"

    # Extract all keys referenced in onboarding_matrix (both core and adaptive)
    local matrix_keys
    export REFERENCE_YAML
    matrix_keys=$(python3 <<'EOF'
import yaml
import sys
import os

with open(os.environ['REFERENCE_YAML']) as f:
    data = yaml.safe_load(f)

matrix = data.get('onboarding_matrix', {})
deep_dive = data.get('deep_dive', {})

# Collect all keys from core and adaptive
referenced_keys = set()
for goal, levels in matrix.items():
    for level, profile in levels.items():
        # Handle both old format (list) and new format (dict with core/adaptive)
        if isinstance(profile, dict):
            # New adaptive format
            if 'core' in profile:
                referenced_keys.update(profile['core'])
            if 'adaptive' in profile:
                for item in profile['adaptive']:
                    if isinstance(item, dict) and 'topics' in item:
                        topics = item['topics']
                        if isinstance(topics, list):
                            referenced_keys.update(topics)
                        else:
                            referenced_keys.add(topics)
                    elif item != 'default':  # Skip 'default' keyword
                        continue
        elif isinstance(profile, list):
            # Old static format
            referenced_keys.update(profile)

# Check all keys exist in deep_dive
missing = []
for key in sorted(referenced_keys):
    if key not in deep_dive and '.' not in key:  # Allow context.zones style keys
        missing.append(key)

if missing:
    print(f"MISSING: {', '.join(missing)}")
    sys.exit(1)
else:
    print(f"OK: All {len(referenced_keys)} keys exist")
    sys.exit(0)
EOF
"$REFERENCE_YAML")

    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        pass "Deep_dive keys: $matrix_keys"
    else
        fail "Deep_dive keys: $matrix_keys"
        return 1
    fi
}

# Check 3: Time budgets respected
check_time_budgets() {
    info "Check 3: Validating time budgets"

    local validation_result
    validation_result=$(python3 <<'EOF'
import yaml
import sys
import os

with open(os.environ['REFERENCE_YAML']) as f:
    data = yaml.safe_load(f)

matrix = data.get('onboarding_matrix', {})

# Time budget rules (min per topic)
MIN_PER_TOPIC = {
    '5min': 2,
    '15min': 4,
    '30min': 6,
    '60min': 8,
    '120min': 10
}

violations = []
checks = 0

for goal, levels in matrix.items():
    for level, profile in levels.items():
        if not isinstance(profile, dict):
            continue  # Skip old format or fix_problem.any_any

        time_budget = profile.get('time_budget', 'N/A')
        topics_max = profile.get('topics_max', 0)

        if time_budget == 'N/A':
            continue

        # Extract numeric time
        time_key = time_budget.split()[0]  # "30 min" -> "30"

        # Calculate required time
        if time_key in MIN_PER_TOPIC:
            min_per_topic = MIN_PER_TOPIC[time_key]
            required_time = topics_max * min_per_topic
            actual_time = int(time_key.replace('min', ''))

            checks += 1
            if required_time > actual_time * 1.1:  # Allow 10% tolerance
                violations.append(
                    f"{goal}.{level}: {topics_max} topics × {min_per_topic} min = {required_time} min > {actual_time} min budget"
                )

if violations:
    print(f"VIOLATIONS ({len(violations)}):")
    for v in violations:
        print(f"  - {v}")
    sys.exit(1)
else:
    print(f"OK: {checks} profiles checked, all time budgets respected")
    sys.exit(0)
EOF
"$REFERENCE_YAML")

    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        pass "Time budgets: $validation_result"
    else
        fail "Time budgets: $validation_result"
        return 1
    fi
}

# Check 4: topics_max constraints not violated
check_topics_max() {
    info "Check 4: Verifying topics_max constraints"

    local result
    result=$(python3 <<'EOF'
import yaml
import sys
import os

with open(os.environ['REFERENCE_YAML']) as f:
    data = yaml.safe_load(f)

matrix = data.get('onboarding_matrix', {})
violations = []
checks = 0

for goal, levels in matrix.items():
    for level, profile in levels.items():
        if not isinstance(profile, dict):
            continue

        topics_max = profile.get('topics_max', 0)

        # Count core topics
        core_count = len(profile.get('core', []))

        # Determine max adaptive topics based on adaptive section existence and note
        adaptive_section = profile.get('adaptive', [])
        if not adaptive_section:
            # No adaptive section = no adaptive topics
            max_adaptive = 0
        else:
            # Has adaptive section - check note for "picks up to 2"
            note = profile.get('note', '')
            if 'picks up to 2' in note or 'up to 2' in note:
                max_adaptive = 2
            else:
                max_adaptive = 1  # Either 1 trigger OR default

        # Max possible topics: core + max_adaptive
        max_possible = core_count + max_adaptive

        checks += 1
        if max_possible > topics_max:
            violations.append(
                f"{goal}.{level}: max_possible={max_possible} (core={core_count} + adaptive/default) > topics_max={topics_max}"
            )

if violations:
    print(f"VIOLATIONS ({len(violations)}):")
    for v in violations:
        print(f"  - {v}")
    sys.exit(1)
else:
    print(f"OK: {checks} profiles checked")
    sys.exit(0)
EOF
"$REFERENCE_YAML")

    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        pass "Topics_max constraints: $result"
    else
        fail "Topics_max: $result"
        return 1
    fi
}

# Check 5: question_flow references all goals
check_question_flow() {
    info "Check 5: Verifying question_flow completeness"

    local result
    result=$(python3 <<'EOF'
import yaml
import sys
import os

with open(os.environ['REFERENCE_YAML']) as f:
    data = yaml.safe_load(f)

matrix = data.get('onboarding_matrix', {})
questions = data.get('onboarding_questions', {})
question_flow = questions.get('question_flow', {})

matrix_goals = set(matrix.keys())
flow_goals = set(question_flow.keys())

missing = matrix_goals - flow_goals
extra = flow_goals - matrix_goals

if missing or extra:
    if missing:
        print(f"MISSING in question_flow: {', '.join(sorted(missing))}")
    if extra:
        print(f"EXTRA in question_flow: {', '.join(sorted(extra))}")
    sys.exit(1)
else:
    print(f"OK: All {len(matrix_goals)} goals present")
    sys.exit(0)
EOF
"$REFERENCE_YAML")

    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        pass "Question_flow: $result"
    else
        fail "Question_flow: $result"
        return 1
    fi
}

# Check 6: Version alignment
check_version_alignment() {
    info "Check 6: Verifying version alignment"

    local guide_version
    guide_version=$(cat "$VERSION_FILE")

    local yaml_version meta_aligned
    yaml_version=$(python3 -c "import yaml; print(yaml.safe_load(open('$REFERENCE_YAML'))['version'])")
    meta_aligned=$(python3 -c "import yaml; data=yaml.safe_load(open('$REFERENCE_YAML')); print(data.get('onboarding_matrix_meta', {}).get('aligned_with_guide', 'N/A'))")

    if [ "$guide_version" = "$yaml_version" ] && [ "$guide_version" = "$meta_aligned" ]; then
        pass "Version aligned: $guide_version (VERSION = reference.yaml = onboarding_matrix_meta)"
    else
        fail "Version mismatch: VERSION=$guide_version, reference.yaml=$yaml_version, meta=$meta_aligned"
        return 1
    fi
}

# Main execution
main() {
    echo "════════════════════════════════════════════════════════════════"
    echo "  Onboarding System Validation (v2.0.0)"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    check_yaml_syntax || true
    check_deep_dive_keys || true
    check_time_budgets || true
    check_topics_max || true
    check_question_flow || true
    check_version_alignment || true

    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  Summary"
    echo "════════════════════════════════════════════════════════════════"
    echo -e "Total checks: $CHECKS_TOTAL"
    echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"

    if [ $CHECKS_FAILED -gt 0 ]; then
        echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
        echo ""
        echo -e "${RED}❌ Validation FAILED${NC}"
        exit 1
    else
        echo -e "${GREEN}Failed: 0${NC}"
        echo ""
        echo -e "${GREEN}✅ All checks passed!${NC}"
        exit 0
    fi
}

main "$@"
