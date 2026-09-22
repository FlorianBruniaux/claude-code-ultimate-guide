#!/usr/bin/env bash
# Fresh Context Loop - Ralph Wiggum pattern for Claude Code
#
# Solves context rot by spawning fresh Claude instances per task iteration.
# State persists via TASK.md, PROGRESS.md, and git commits.
#
# Usage: ./fresh-context-loop.sh [max_iterations] [task_file] [progress_file]
#
# Sources:
# - Pattern: https://goose-docs.ai/docs/tutorials/ralph-loop/
# - Research: https://research.trychroma.com/context-rot

set -euo pipefail

MAX_ITERATIONS=${1:-10}
TASK_FILE=${2:-"TASK.md"}
PROGRESS_FILE=${3:-"PROGRESS.md"}

# Validate prerequisites
if [[ ! -f "$TASK_FILE" ]]; then
    echo "❌ Missing $TASK_FILE"
    echo ""
    echo "Create a TASK.md with:"
    echo "  ## Current Focus"
    echo "  [Single atomic task]"
    echo ""
    echo "  ## Acceptance Criteria"
    echo "  - [ ] Tests pass"
    echo "  - [ ] Build succeeds"
    exit 1
fi

# Create progress file if missing
[[ ! -f "$PROGRESS_FILE" ]] && touch "$PROGRESS_FILE"

echo "🔄 Fresh Context Loop"
echo "   Max iterations: $MAX_ITERATIONS"
echo "   Task file: $TASK_FILE"
echo "   Progress file: $PROGRESS_FILE"
echo ""

for i in $(seq 1 "$MAX_ITERATIONS"); do
    echo "═══════════════════════════════════════"
    echo "  Iteration $i/$MAX_ITERATIONS"
    echo "═══════════════════════════════════════"
    echo ""

    # Fresh context each iteration (no -c flag = new session)
    claude -p "$(cat "$TASK_FILE" "$PROGRESS_FILE")

---
INSTRUCTIONS FOR THIS ITERATION:

1. Read the task and progress above carefully
2. Complete the NEXT incomplete task only (one at a time)
3. Run tests/build to verify your changes work
4. Update $PROGRESS_FILE with:
   - What you completed
   - Any blockers encountered
   - What should be done next
5. If ALL tasks are complete and verified, add this exact line to $PROGRESS_FILE:
   LOOP_COMPLETE

IMPORTANT:
- Focus on ONE task per iteration
- Always verify before marking complete
- Commit your changes before the iteration ends"

    echo ""

    # Check completion marker
    if grep -q "LOOP_COMPLETE" "$PROGRESS_FILE" 2>/dev/null; then
        echo ""
        echo "✅ All tasks completed in $i iterations"
        exit 0
    fi

    # Auto-commit progress if changes exist
    if ! git diff --quiet "$PROGRESS_FILE" 2>/dev/null; then
        git add "$PROGRESS_FILE"
        git commit -m "chore: update progress (iteration $i)" --no-verify 2>/dev/null || true
    fi

    # Auto-commit any other staged changes
    if ! git diff --cached --quiet 2>/dev/null; then
        git commit -m "feat: iteration $i progress" --no-verify 2>/dev/null || true
    fi

    echo ""
    echo "─────────────────────────────────────────"
    echo ""
done

echo "⚠️  Max iterations ($MAX_ITERATIONS) reached without completion"
echo "   Check $PROGRESS_FILE for status"
exit 1
