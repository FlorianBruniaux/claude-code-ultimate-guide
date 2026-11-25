#!/bin/bash
# Install the Release Automation bundle into a project's .claude/ directory.
# Run from a clone of the repository: components are copied from the sibling
# examples/ directories (agents/, skills/, hooks/bash/, github-actions/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXAMPLES_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_CLAUDE_DIR="${CLAUDE_PROJECT_DIR:-.claude}"

AGENTS=()
SKILLS=(release-notes release-notes-generator)
HOOKS=()
WORKFLOWS=()

copy_item() {
  local src="$1" dest="$2" label="$3"
  if [ ! -e "$src" ]; then
    echo "  missing: $src" >&2
    return 1
  fi
  if [ -e "$dest" ]; then
    echo "  skipped (already exists): $dest"
    return 0
  fi
  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$dest"
  echo "  installed $label: $dest"
}

echo "Installing Release Automation into $PROJECT_CLAUDE_DIR"

for a in "${AGENTS[@]+"${AGENTS[@]}"}"; do
  copy_item "$EXAMPLES_DIR/agents/$a.md" "$PROJECT_CLAUDE_DIR/agents/$a.md" agent
done

# Skills are folders (<name>/SKILL.md), copied whole so bundled files come along
for s in "${SKILLS[@]+"${SKILLS[@]}"}"; do
  copy_item "$EXAMPLES_DIR/skills/$s" "$PROJECT_CLAUDE_DIR/skills/$s" skill
done

for h in "${HOOKS[@]+"${HOOKS[@]}"}"; do
  copy_item "$EXAMPLES_DIR/hooks/bash/$h.sh" "$PROJECT_CLAUDE_DIR/hooks/bash/$h.sh" hook
  chmod +x "$PROJECT_CLAUDE_DIR/hooks/bash/$h.sh"
done

# GitHub Actions workflows go to the repository root, not into .claude/
for w in "${WORKFLOWS[@]+"${WORKFLOWS[@]}"}"; do
  copy_item "$EXAMPLES_DIR/github-actions/$w.yml" ".github/workflows/$w.yml" workflow
done

echo "Done. Hooks are not active until registered in settings.json: see README.md."
