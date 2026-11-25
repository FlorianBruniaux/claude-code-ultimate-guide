---
name: version
description: Display current guide and Claude Code versions
---

# Version Information

Display current version information for the guide and tracked Claude Code version.

## What to Display

```
Claude Code Ultimate Guide
├─ Guide Version:        X.Y.Z (from VERSION file)
├─ Claude Code Tracked:  vA.B.C (from claude-code-releases.yaml)
├─ Last CC Update:       YYYY-MM-DD
├─ Templates:            N files
├─ Quiz Questions:       N questions
├─ Guide Lines:          ~N lines
└─ Landing Synced:       ✅ Yes / ❌ No

Recent Guide Updates:
- [Date]: Version X.Y.Z-1 → X.Y.Z (reason)
- [Date]: Version X.Y.Z-2 → X.Y.Z-1 (reason)
- [Date]: Version X.Y.Z-3 → X.Y.Z-2 (reason)

Recent Claude Code Releases:
- vA.B.C (YYYY-MM-DD): [2-3 highlights]
- vA.B.C-1 (YYYY-MM-DD): [2-3 highlights]
- vA.B.C-2 (YYYY-MM-DD): [2-3 highlights]
```

## Files to Read

1. `VERSION` - Guide version
2. `machine-readable/claude-code-releases.yaml` - CC version + date
3. `CHANGELOG.md` - Last 3 guide updates
4. `machine-readable/claude-code-releases.yaml` - Last 3 CC releases
5. Run `find examples/ -type f \( -name "*.md" -o -name "*.sh" -o -name "*.ps1" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) -not -name README.md -not -name index.md -not -path '*/commands/*' | wc -l` - Templates count (same definition as `scripts/check-landing-sync.sh`)
6. Run `grep -r '  - id:' quiz/questions/ | wc -l` - Quiz count
7. Run `wc -l guide/ultimate-guide.md | awk '{print $1}'` - Guide lines
8. Run `./scripts/check-landing-sync.sh` - Sync status

## Output Format

Use clean, readable formatting with emojis for visual clarity:

```
📊 Claude Code Ultimate Guide - Version Info

📦 Guide Version: 3.9.11
🔧 Claude Code: v2.1.14 (2026-01-21)

📈 Content Stats:
   • Templates:      65 files
   • Quiz Questions: 227 questions
   • Guide Lines:    ~11,560 lines

🔄 Landing Sync: ✅ Synchronized

📝 Recent Guide Updates:
   • 2026-01-20 - v3.9.10 → v3.9.11: Production Safety Rules
   • 2026-01-19 - v3.9.9 → v3.9.10: DevOps & SRE Guide (FIRE)
   • 2026-01-18 - v3.9.8 → v3.9.9: Documentation improvements

🚀 Recent Claude Code Releases:
   • v2.1.14 (2026-01-21)
     - History-based autocomplete in bash mode
     - Plugin search and SHA pinning
     - Context window + memory fixes

   • v2.1.12 (2026-01-18)
     - Message rendering bugfix

   • v2.1.11 (2026-01-17)
     - MCP connection optimization
```

## Implementation

1. Read all required files
2. Execute shell commands for counts
3. Parse YAML for CC releases
4. Parse CHANGELOG for guide updates
5. Format output with proper alignment
6. Display with clear visual hierarchy
