---
name: park
description: Park current session for later resume (append to Markdown file)
argument-hint: "[session description]"
---

# Park Session

Save the current session info so you can resume it after a reboot.

## Usage

```
/park fix du bug auth JWT     # description inline
/park                          # will ask for description
```

## Step 1: Get Description

If `$ARGUMENTS` is non-empty → use it as the session description.
Otherwise → ask:

> "Comment décrire cette session ? (ex: fix bug auth JWT, refacto pricing page, migration DB)"

## Step 2: Choose Destination File

Ask the user where to save:

> "Fichier destination ?"

Options:
1. `~/Desktop/parked-sessions.md` (default, recommended)
2. `~/.claude/parked-sessions.md` (hidden, always available)
3. Other (free text input)

If the user just presses Enter → use option 1.

## Step 3: Detect Session ID

Run these commands to find the current session:

```bash
# Get current directory encoded path (/ → -, prefixed with -)
PWD_ENCODED=$(pwd | sed 's|/|-|g' | sed 's|^|projects-|' | sed 's|^projects-||')
SESSIONS_FILE="$HOME/.claude/projects/-$(echo "$PWD" | sed 's|/|-|g' | sed 's|^-||')/sessions-index.json"
```

More precisely, the Claude sessions index path is:
```
~/.claude/projects/<encoded-pwd>/sessions-index.json
```

Where `<encoded-pwd>` is the current directory path with every `/` replaced by `-` (and the leading `/` becomes the start of the encoded path, so `/Users/flo/myproject` → `-Users-flo-myproject`).

**To detect the session ID:**

1. Run: `ls -t ~/.claude/projects/ | head -5` to find the most likely project folder
2. Read the `sessions-index.json` from the matching folder
3. The sessions-index.json contains an array of session objects — take the most recent one (last in array or highest timestamp)
4. Extract the session `id` field (UUID format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

**Fallback if detection fails**: Use `claude --continue` instead of `claude --resume <id>` in the output.

## Step 4: Collect Context

Run in parallel:
```bash
pwd                         # → repo path
git branch --show-current   # → active branch (or "no git" if not a repo)
date "+%Y-%m-%d %H:%M"     # → timestamp
```

## Step 5: Write to File

**Check if file exists:**
- If it does NOT exist → create it with header: `# Parked Sessions\n\n`
- If it exists → append to the end (NEVER overwrite existing content)

**Append this Markdown block:**

```markdown
## <description>
- **Date** : <YYYY-MM-DD HH:MM>
- **Repo** : <pwd output>
- **Branch** : <git branch or "N/A">
- **Resume** : `cd <pwd> && claude --resume <session-id>`

---
```

If session ID was not detected, use:
```markdown
- **Resume** : `cd <pwd> && claude --continue`
```

## Step 6: Display Summary

Output in terminal:

```
Session parkée dans <destination-file>

Pour reprendre :
  cd <pwd> && claude --resume <session-id>
```

If multiple sessions were parked before, remind: "Ce fichier contient maintenant N sessions. Pour voir toutes vos sessions : cat <destination-file>"

## Error Handling

| Error | Action |
|-------|--------|
| Not a git repo | Use `N/A` for branch, continue |
| sessions-index.json not found | Use `claude --continue` as fallback |
| File write permission denied | Try `~/.claude/parked-sessions.md` as fallback |
| sessions-index.json malformed | Use `claude --continue` as fallback |

## Example Output (success)

```
Session parkée dans ~/Desktop/parked-sessions.md

Pour reprendre :
  cd /Users/flo/Sites/perso/mon-projet && claude --resume 84287c0d-8778-4a8d-abf1-eb2807e327a8
```
