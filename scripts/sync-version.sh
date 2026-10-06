#!/bin/bash
# sync-version.sh - Sync version from VERSION file to all documentation
# Usage: ./scripts/sync-version.sh [--check]
#   --check : Only check, don't modify (exit 1 if mismatch)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Read source of truth
if [[ ! -f VERSION ]]; then
  echo "❌ VERSION file not found"
  exit 1
fi

VERSION=$(cat VERSION | tr -d '[:space:]')
CHECK_ONLY=false
ERRORS=0

if [[ "${1:-}" == "--check" ]]; then
  CHECK_ONLY=true
fi

echo "=== Version Sync ==="
echo "Source: VERSION → $VERSION"
echo ""

# Function to check/update a file
check_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    echo "⚠️  $file not found"
    return
  fi

  # Match edition metadata only. A section number or historical release
  # reference may have the same shape as a version and must stay unchanged.
  local status=0
  python3 - "$file" "$VERSION" "$CHECK_ONLY" <<'PY' || status=$?
import re
import sys
from pathlib import Path

path, version, check = Path(sys.argv[1]), sys.argv[2], sys.argv[3] == "true"
source = path.read_text(encoding="utf-8")
pattern = re.compile(
    r'(^\*\*Version\*\*:\s*|Guide-v|(?:Guide|guide) version\s+|'
    r'Updated-[^\n"<]*_·_v|\*Version\s+|'
    r'\| (?:\*\*)?Version(?:\*\*)?:?\s+|'
    r'^version:\s*"|^\s+aligned_with_guide:\s*")'
    r'(\d+\.\d+\.\d+)', re.MULTILINE,
)
matches = list(pattern.finditer(source))
old = sorted({match[2] for match in matches if match[2] != version})
if old:
    print(f"📍 {path}: outdated edition metadata: {', '.join(old)} → {version}")
    if check:
        sys.exit(1)
    path.write_text(pattern.sub(lambda match: match[1] + version, source), encoding="utf-8")
    print(f"✅ {path}: updated")
elif matches:
    print(f"✅ {path}: OK ({version})")
else:
    print(f"⚠️ {path}: no edition version found")
PY
  if [[ $status -eq 1 ]]; then
    ERRORS=$((ERRORS + 1))
  elif [[ $status -ne 0 ]]; then
    return "$status"
  fi
}

# Function to update date in README
update_readme_date() {
  local file="README.md"

  if [[ ! -f "$file" ]]; then
    echo "⚠️  $file not found"
    return
  fi

  # Get current date in format: Feb 10, 2026 (locale-pinned so the month
  # abbreviation is always English, regardless of the machine's locale)
  local current_date=$(LC_ALL=C date +"%b %-d, %Y")
  # Format for badge: Feb_10,_2026
  local badge_date=$(echo "$current_date" | sed 's/ /_/g')

  if $CHECK_ONLY; then
    # In check mode, date drift is informational only: it changes every
    # day that isn't release day and must not fail the pre-commit gate.
    # Only VERSION mismatches (see check_file) drive the exit code.
    if ! grep -q "Updated-${badge_date}_·_v${VERSION}-brightgreen" "$file" 2>/dev/null; then
      echo "📍 $file: date badge needs update (→ $current_date)"
    fi
    if ! grep -q "Updated daily · ${current_date}" "$file" 2>/dev/null; then
      echo "📍 $file: footer date needs update (→ $current_date)"
    fi
  else
    # Update badge date pattern: Updated-XXX-brightgreen
    sed -i '' "s|Updated-[^-]*-brightgreen|Updated-${badge_date}_·_v${VERSION}-brightgreen|g" "$file"

    # Update footer date pattern and preserve the closing Markdown asterisk.
    sed -i '' "s|Updated daily · [^*]*|Updated daily · ${current_date}|g" "$file"

    echo "✅ $file: date updated (→ $current_date)"
  fi
}

# Check main files
check_file "README.md"
check_file "guide/cheatsheet.md"
check_file "guide/ultimate-guide.md"
check_file "machine-readable/reference.yaml"

# Update README date (version and date in badge + footer)
update_readme_date

# Keep translation provenance truthful. A declared stale translation is valid
# in the default gate; missing pairs, wrong hashes, and contradictory status are not.
if $CHECK_ONLY; then
  if ! python3 scripts/check-translations.py --check; then
    ERRORS=$((ERRORS + 1))
  fi
else
  python3 scripts/check-translations.py --update-local
  python3 scripts/check-translations.py --check
fi

echo ""

if $CHECK_ONLY && [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS file(s) need version update"
  echo "Run: ./scripts/sync-version.sh"
  exit 1
fi

echo "✅ Done"
