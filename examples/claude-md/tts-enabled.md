---
title: "TTS-Enabled Project Template"
description: "CLAUDE.md configuration for projects using Agent Vibes text-to-speech"
tags: [claude-md, template, tts]
---

# Project with TTS Enabled

This is a template `CLAUDE.md` file for projects using Agent Vibes TTS.

## TTS Configuration

**Provider**: Piper TTS
**Voice**: fr_FR-tom-medium (French male)
**Verbosity**: Low (recommended)
**Effects**: Light reverb
**Background Music**: Disabled

## Project-Specific TTS Settings

### Mute During Focus Work

When working on tasks requiring deep concentration, mute TTS:

```bash
# Mute for this session
/agent-vibes:mute

# Unmute when done
/agent-vibes:unmute
```

### Selective TTS (Errors Only)

For this project, TTS speaks only error messages:

- ✅ Errors, failures, exceptions
- ❌ Regular responses, confirmations
- ❌ Informational messages

**Reason**: This is a critical production system where audio alerts for errors are valuable, but constant narration is distracting.

## Voice Preferences

| Task Type | Recommended Voice | Reason |
|-----------|-------------------|--------|
| Code reviews | fr_FR-tom-medium | Professional, clear |
| Documentation | fr_FR-siwis-medium | Warm, educational tone |
| Debugging | fr_FR-tom-medium (low verbosity) | Critical alerts only |

## Commands Reference

Quick reference for team members:

```bash
# Check current voice
/agent-vibes:whoami

# Switch voice
/agent-vibes:switch fr_FR-tom-medium

# Mute/unmute
/agent-vibes:mute
/agent-vibes:unmute

# Adjust verbosity
/agent-vibes:verbosity low

# Disable effects (faster)
/agent-vibes:effects off
```

## Team Guidelines

### When to Mute

- Pair programming sessions (speaker explains, TTS distracts)
- Video meetings (avoid audio conflicts)
- Deep focus work (flow state priority)
- Public spaces (avoid disturbing others)

### When to Enable

- Solo code reviews (listen while reviewing diffs)
- Long-running tasks (audio completion notifications)
- Background monitoring (alerts for errors)
- Learning mode (dual-language practice)

## Installation for Team Members

New team members should follow:

1. **Installation Guide**: [Agent Vibes Installation](../../integrations/agent-vibes/installation.md)
2. **Voice Selection**: Use `fr_FR-tom-medium` for consistency
3. **Configuration**: Copy settings from this file

## Troubleshooting

Common issues:

- **No audio**: Check `cat .claude/tts-provider.txt` → should be `piper`
- **Wrong voice**: Run `/agent-vibes:switch fr_FR-tom-medium`
- **Too verbose**: Run `/agent-vibes:verbosity low`

**Full troubleshooting**: [Agent Vibes Troubleshooting](../../integrations/agent-vibes/troubleshooting.md)

## Notes

- TTS is **optional** - not required for project contribution
- Mute status is **project-specific** (`.claude/agentvibes-muted`)
- Voice models are **shared globally** (`~/.claude/piper-voices/`)

---

*For more information about Agent Vibes TTS, see [Integration Guide](../../integrations/agent-vibes/README.md)*
