---
name: handoff-update
description: "Update an existing handoff document with current session progress. Applies section-specific merge rules: append-only for Work Done (never deletes history), replace for Status and Next Steps, merge for Files and Discoveries. Falls back to creating a new handoff if no source file is found."
argument-hint: "[handoff-file-path]"
effort: low
disable-model-invocation: true
---

Update an existing handoff document with this session's progress.

## Step 1: Resolve the Handoff File

Determine which file to update, in this priority order:

1. If `$ARGUMENTS[0]` was provided, use it as the file path.
2. If this session was started via `/handoff:resume`, look in conversation history for the argument that was passed to it.
3. If neither is found, fall back to creating a new file: `claudedocs/handoffs/handoff_YYYYMMDD_HHMMSS.md`. Inform the user that no existing handoff was found.

## Step 2: Read the Existing File

Read the resolved file completely. Parse all sections as the baseline for the merge.

## Step 3: Apply Section Merge Rules

Rewrite the file with updated content using these merge rules:

| Section | Rule | Notes |
|---------|------|-------|
| **Task** | Keep original | Update only if scope fundamentally changed |
| **Scope** | Keep or refine | Narrow it if new understanding emerged |
| **Files** | Merge | Add new files touched in this session. Keep originals. Use `path:line` format |
| **Discoveries** | Append | Add new findings below existing list. Never remove prior discoveries |
| **Work Done** | **Append only** | Add new completed items below existing list. Never remove entries. Include commit hashes |
| **Status** | **Replace** | Write the current state: what is done now, what remains, test status |
| **Next Steps** | **Replace** | Write the updated actionable checklist |
| **Code** | Update | Replace with the most relevant snippets from the current state |

**The append-only rule for Work Done is strict.** Even if a previous entry describes work that was later revised, keep it. The history is the record. Add a new entry describing the revision instead of removing the old one.

## Step 4: Confirm

After saving, confirm:
- File path updated
- How many new Work Done items were added
- The updated Status (one line)
- How many Next Steps remain

---

> This command implements the Handoff Triad pattern documented in this guide's Session Handoff Pattern section.
> Template inspired by [Packmind's handoff commands](https://github.com/PackmindHub/packmind) (Apache 2.0).
