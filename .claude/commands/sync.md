---
name: sync
description: Check guide/landing synchronization status
---

# Synchronization Check

Run comprehensive sync verification between guide repository and landing site.

## What to Check

Execute `./scripts/check-landing-sync.sh` and display results with enhanced formatting.

## Output Format

```
🔄 Guide ↔ Landing Synchronization Check

═══════════════════════════════════════════════════════════

1️⃣ Guide Version
   Guide:   3.9.11
   Landing: 3.9.11
   Status:  ✅ Synchronized

2️⃣ Templates Count
   Guide Files:      65
   Landing (index):  65
   Landing (examples): 65
   Status:  ✅ Synchronized

3️⃣ Quiz Questions
   Source (JSON):     227
   Landing (index):   227
   Landing (quiz):    227
   Status:  ✅ Synchronized

4️⃣ Guide Lines
   Actual Count:      11,560
   Landing Display:   11,000+ (approximate)
   Status:  ✅ Within Tolerance

5️⃣ Claude Code Version
   Releases YAML:     v2.1.14
   Landing Badge:     v2.1.14
   Status:  ✅ Synchronized

═══════════════════════════════════════════════════════════

✅ All Components Synchronized

No action required. Guide and landing site are in sync.
```

## If Mismatches Detected

```
🔄 Guide ↔ Landing Synchronization Check

═══════════════════════════════════════════════════════════

1️⃣ Guide Version
   [... as above ...]

2️⃣ Templates Count
   Guide Files:      65
   Landing (index):  63
   Landing (examples): 65
   Status:  ⚠️ MISMATCH

3️⃣ Quiz Questions
   [... etc ...]

═══════════════════════════════════════════════════════════

❌ Synchronization Issues Detected (1 issue)

Issues to Fix:

1. Templates Count Mismatch
   Location: claude-code-ultimate-guide-landing/src/data/examples-data.ts
             (HeroBanner.astro and src/pages/examples/index.astro render
             {stats.templateCount}, computed from this catalog)
   Current:  63
   Expected: 65
   Action:   Add or remove the catalog entries in examples-data.ts

Quick Fixes:
   # Update landing templates count
   cd ../claude-code-ultimate-guide-landing
   # Add the missing entries to src/data/examples-data.ts (no literal count to edit)
   git add src/data/examples-data.ts
   git commit -m "fix: sync templates count (63 → 65)"
   git push

Recommended:
   Run /update-infos-release to automate synchronization
```

## Implementation

1. Execute sync check script
2. Capture output and parse status codes
3. Format results with clear visual hierarchy
4. If issues detected:
   - List each mismatch
   - Provide file locations
   - Suggest exact fixes
   - Recommend automation commands
5. Color-code status indicators
6. Add actionable next steps

## Related Commands

- `/update-infos-release` - Automated sync + version management
- `/version` - View current versions
- `/changelog` - View recent CHANGELOG entries
