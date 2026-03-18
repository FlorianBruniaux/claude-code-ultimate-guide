---
title: "TTS Setup Workflow - Agent Vibes Installation"
description: "Add text-to-speech narration to Claude Code on macOS"
tags: [workflow, tts, tutorial]
---

# TTS Setup Workflow - Agent Vibes Installation

**Goal**: Add text-to-speech narration to Claude Code
**Time**: 18 minutes
**Difficulty**: Intermediate
**System**: macOS (Homebrew required)

---

## Decision Point: Should You Install TTS?

Use this quick assessment:

| Question | Answer | Score |
|----------|--------|-------|
| Do you work on long code reviews? | Yes | +2 |
| Do you multitask during debugging? | Yes | +2 |
| Do you prefer audio notifications? | Yes | +1 |
| Do you need offline TTS (no cloud)? | Yes | +2 |
| Is latency critical (<100ms required)? | Yes | -2 |
| Do you work in public spaces (no audio)? | Yes | -3 |
| Do you prefer silent work environment? | Yes | -2 |

**Score**:
- **≥3**: Install TTS (good fit)
- **0-2**: Optional (try it, can uninstall)
- **<0**: Skip TTS (not a good fit)

---

## Workflow Overview

```
Phase 1: Prerequisites (5 min)
    ↓
Phase 2: Agent Vibes Install (5 min)
    ↓
Phase 3: Piper TTS + Voices (5 min)
    ↓
Phase 4: Test & Configure (3 min)
    ↓
Phase 5: Verify (1 min)
```

---

## Phase 1: Prerequisites (5 minutes)

### Checkpoint 1.1: System Requirements

```bash
# Verify macOS version
sw_vers
# Required: macOS 10.15+

# Verify Homebrew
brew --version
# If missing: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify Node.js
node --version
# Required: 16.0.0+
```

### Checkpoint 1.2: Install Bash 5.x

```bash
# Install
brew install bash

# Verify
/opt/homebrew/bin/bash --version
# Expected: GNU bash, version 5.x

# ✅ Checkpoint: Bash 5.x installed
```

### Checkpoint 1.3: Install Dependencies

```bash
# Install audio tools
brew install sox ffmpeg util-linux espeak-ng

# Verify all installed
command -v sox && command -v ffmpeg && command -v espeak-ng && echo "✅ Dependencies OK"

# ✅ Checkpoint: Dependencies installed
```

**Total time Phase 1**: ~5 minutes

---

## Phase 2: Agent Vibes Installation (5 minutes)

### Step 2.1: Launch Installer

```bash
# Navigate to your project
cd /path/to/your/claude-project

# Launch interactive installer
npx agentvibes install
```

**Expected**: ASCII banner + 4-page interactive installer

### Step 2.2: Navigate Pages

**Page 1/4 - Dependencies**:
- Review: Should show all ✓ green checkmarks
- Action: Click "Next →"

**Page 2/4 - Provider**:
- **Select**: `Piper TTS` (best quality, offline)
- Action: Click "Next →"

**Page 3/4 - Voice**:
- **French**: Select `fr_FR-tom-medium` (male, professional)
- **English**: Select `en_US-ryan-high` (best quality)
- Action: Click "Next →"

**Page 4/4 - Settings**:
- **Reverb**: `Light` (recommended)
- **Background Music**: `Disabled` (avoid distraction)
- **Verbosity**: `Low` (less chatty)
- Action: Click "Start Installation"

### Checkpoint 2.3: Verify Installation

```bash
# Check installed files
ls .claude/hooks/play-tts.sh
ls .claude/commands/agent-vibes/
cat .claude/tts-provider.txt
# Expected: Files exist, provider shows "macos" or "piper"

# ✅ Checkpoint: Agent Vibes installed
```

**Total time Phase 2**: ~5 minutes

---

## Phase 3: Piper TTS + French Voices (5 minutes)

### Step 3.1: Install Piper via pipx

```bash
# Install Piper TTS
pipx install piper-tts

# Verify
piper --help
# Expected: Piper usage instructions

# ✅ Checkpoint: Piper installed
```

### Step 3.2: Download French Voices

```bash
# Create voice directory
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices

# Download French male voice (recommended)
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

# Download French female voice (optional)
curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

# ✅ Checkpoint: Voices downloaded (~120MB)
```

**Total time Phase 3**: ~5 minutes

---

## Phase 4: Configuration & Testing (3 minutes)

### Step 4.1: Configure Provider & Voice

```bash
# Set Piper as provider
echo "piper" > .claude/tts-provider.txt

# Set French male voice
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# Verify configuration
cat .claude/tts-provider.txt  # Expected: piper
cat .claude/tts-voice.txt     # Expected: fr_FR-tom-medium

# ✅ Checkpoint: Configuration set
```

### Step 4.2: Test Audio Pipeline

```bash
# Test Piper directly
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav

# Test TTS hook
~/.claude/hooks/play-tts.sh "Ceci est un test audio"

# ✅ Checkpoint: Audio works
```

**Expected**: You should hear French male voice.

**Total time Phase 4**: ~3 minutes

---

## Phase 5: Verification in Claude Code (1 minute)

### Step 5.1: Launch & Test

```bash
# Start Claude Code
claude

# In Claude, run:
/agent-vibes:whoami
# Expected: Shows "piper" provider and "fr_FR-tom-medium" voice

# Test simple request
> "Dis-moi bonjour en français"
# Expected: Audio response in French male voice

# ✅ Checkpoint: TTS active in Claude Code
```

### Step 5.2: Configure Preferences

```bash
# Reduce verbosity (recommended)
/agent-vibes:verbosity low

# Hide 34 commands if cluttered
/agent-vibes:hide

# ✅ Checkpoint: Preferences set
```

**Total time Phase 5**: ~1 minute

---

## Total Time: ~18 Minutes ✅

---

## Post-Setup Recommendations

### Optimize for Your Workflow

**For code reviews**:
```bash
/agent-vibes:verbosity low
/agent-vibes:effects off
```

**For focus work**:
```bash
/agent-vibes:mute  # Mute temporarily
# Work without audio
/agent-vibes:unmute  # Re-enable when done
```

**For battery optimization**:
```bash
# Switch to macOS Say (instant, no CPU burst)
/agent-vibes:provider switch macos
```

### Add to .gitignore

```bash
# Prevent committing large audio files
echo ".claude/audio/" >> .gitignore
echo ".claude/piper-voices/" >> .gitignore
echo "*.wav" >> .gitignore
echo "*.onnx" >> .gitignore
```

---

## Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| No audio | Check `cat .claude/tts-provider.txt` |
| Wrong voice | Run `/agent-vibes:switch fr_FR-tom-medium` |
| Too verbose | Run `/agent-vibes:verbosity low` |
| Commands clutter | Run `/agent-vibes:hide` |

**Full troubleshooting**: [Agent Vibes Troubleshooting](../../examples/integrations/agent-vibes/troubleshooting.md)

---

## Next Steps

- **[Voice Catalog](../../examples/integrations/agent-vibes/voice-catalog.md)** - Explore 15 voices
- **[Integration Guide](../../examples/integrations/agent-vibes/README.md)** - Learn commands
- **[Installation Details](../../examples/integrations/agent-vibes/installation.md)** - Deep dive

---

## Uninstall Instructions

To remove Agent Vibes completely:

```bash
# Automated uninstall
npx agentvibes uninstall --yes

# Manual cleanup (if needed)
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/
rm -rf ~/.claude/piper-voices/
pipx uninstall piper-tts
```

---

*Workflow guide maintained by [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Last updated: 2026-01-22 | Agent Vibes v3.0.0*
