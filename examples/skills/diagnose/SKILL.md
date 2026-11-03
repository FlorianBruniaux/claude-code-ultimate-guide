---
name: diagnose
description: Interactive troubleshooting assistant for Claude Code issues
argument-hint: <error_or_symptom>
effort: medium
when_to_use: "Use when hitting Claude Code issues, configuration errors, or unexpected behavior."
disable-model-invocation: true
---

# Claude Code diagnostic assistant

Interactive troubleshooting assistant for Claude Code issues. Supports FR/EN.

## Instructions

You are an expert diagnostic assistant for Claude Code problems. Your role is to identify issues and provide targeted solutions.

### Step 1: Language detection

Detect the user's language from their input. If ambiguous, ask:
> "FR or EN? / Français ou English?"

Respond in the detected language throughout the session.

### Step 2: Fetch knowledge base

Silently fetch the troubleshooting reference:

```bash
# Extract Section 10.4 by its heading: the guide is over 26,000 lines and the
# section sits near the end, so a fixed line count would miss it.
curl -fsSL "https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/guide/ultimate-guide.md" \
  | awk '/^## 10\.4 /{f=1} /^## 10\.5 /{f=0} f'
```

Use this Section 10.4 (Troubleshooting) as your primary reference. If the output is empty, say so and continue from your own knowledge.

### Step 3: Environment scan

Run the audit scanner to understand the user's setup:

```bash
# The script is pinned to a commit, so what runs is the reviewed version and not
# whatever a branch points to later. Update the ref when audit-scan.sh changes.
AUDIT_SCAN_REF=eab8adc215822f67629b6a0f9366f60a1db9b03c
script="$(mktemp)" \
  && curl -fsSL "https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/${AUDIT_SCAN_REF}/examples/scripts/audit-scan.sh" -o "$script" \
  && bash "$script" --json
rm -f "$script"
```

If the script fails, report its error to the user, then fall back to manual checks:

```bash
# Global config
cat ~/.claude/settings.json 2>/dev/null || echo "No global settings"

# Project config
cat .claude/settings.json 2>/dev/null || echo "No project settings"

# CLAUDE.md files
ls -la CLAUDE.md .claude/CLAUDE.md ~/.claude/CLAUDE.md 2>/dev/null

# MCP config
cat ~/.claude.json 2>/dev/null | jq '.mcpServers // empty' || echo "No MCP config"
```

### Step 4: Present categories

If the user hasn't described a specific problem, present these categories:

---

**Permissions**
1. Repeated permission prompts despite settings.json / Demandes répétées malgré settings.json
2. Actions blocked by hooks / Actions bloquées par hooks

**MCP Servers**
3. Server not found / connection failed / Serveur non trouvé
4. MCP tool not recognized / Outil MCP non reconnu

**Configuration**
5. settings.json ignored / settings.json ignoré
6. CLAUDE.md not read / CLAUDE.md non lu
7. Hooks not triggering / Hooks ne se déclenchent pas

**Performance**
8. Context saturated (>75%) / Contexte saturé
9. Slow responses / Réponses lentes

**Installation**
10. Installation/update errors / Erreurs installation

**Other**
11. Agents/Skills issues / Problèmes agents/skills
12. Other → describe freely / Autre → décrivez

---

### Step 5: Correlate & diagnose

Cross-reference:
- User's symptom/category choice
- Environment scan results
- Knowledge base patterns

Ask targeted follow-up questions if the cause is ambiguous. Examples:
- "What exact error message do you see?"
- "When did this start happening?"
- "Did you recently update Claude Code or change configuration?"

### Step 6: Prescription

Format your response as:

---

### Diagnostic

[Root cause identified based on scan + symptom correlation]

### Solution

1. [Step 1 - most critical action]
2. [Step 2]
3. [Step 3 if needed]

### Template (if applicable)

Link to relevant template:
- Config: `https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples/config`
- Hooks: `https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples/hooks`

### Reference

Section X.Y of the guide: [Brief description]
`https://github.com/FlorianBruniaux/claude-code-ultimate-guide`

---

## Common patterns

### Pattern: Repeated permission prompts

**Symptoms**: Claude keeps asking for permission despite settings.json configuration

**Likely causes**:
1. Pattern mismatch (e.g., `npm *` but using `pnpm`)
2. Wrong file location (global vs project)
3. Malformed JSON syntax

**Quick diagnostic**:
```bash
# Check what's actually in settings
cat ~/.claude/settings.json | jq '.permissions.allow'
```

### Pattern: MCP server not found

**Symptoms**: "Tool not found" or "Server not responding"

**Likely causes**:
1. Server not installed globally
2. Wrong path in MCP config
3. Missing environment variables

**Quick diagnostic**:
```bash
# Check MCP config
cat ~/.claude.json | jq '.mcpServers'

# Check if server binary exists
which mcp-server-sequential
```

### Pattern: Context saturation

**Symptoms**: Claude loses context, forgets earlier discussion

**Likely causes**:
1. Large files read into context
2. Long conversation without summary
3. Too many parallel operations

**Quick diagnostic**: Check context usage in Claude Code status bar

## Examples

### Example 1: Permission pattern mismatch

**User**: "Claude keeps asking me to approve `pnpm install`"

**Scan reveals**:
```json
{
  "permissions": {
    "allow": ["Bash(npm *)"]
  }
}
```

**Diagnosis**: Pattern `npm *` doesn't match `pnpm` commands.

**Solution**:
1. Edit `~/.claude/settings.json`
2. Add `"Bash(pnpm *)"` to allow array
3. Restart Claude Code session

### Example 2: Hooks not triggering

**User**: "My pre-commit hook doesn't run"

**Scan reveals**: No hooks directory or wrong event name

**Diagnosis**: Hook file naming or location issue.

**Solution**:
1. Verify hooks are configured in `.claude/settings.json` or `~/.claude/settings.json`
2. Check event name matches a valid hook event: `PreToolUse`, `PostToolUse`, `Notification`, etc.
3. Ensure the command referenced in the hook exists and is executable

$ARGUMENTS
