---
title: "Agent Vibes TTS - Complete Installation Guide"
description: "Step-by-step installation guide for Agent Vibes text-to-speech integration on macOS"
tags: [guide, tts, integration]
---

# Agent Vibes TTS - Complete Installation Guide

**Time Required**: ~18 minutes
**Difficulty**: Intermediate
**System**: macOS (Apple Silicon or Intel)

---

## Prerequisites Check

Before starting, verify you have:

| Requirement | Check Command | Min Version |
|-------------|---------------|-------------|
| **macOS** | `sw_vers` | 10.15+ |
| **Homebrew** | `brew --version` | Any recent |
| **Node.js** | `node --version` | 16.0.0+ |
| **Python** | `python3 --version` | 3.10.0+ |
| **Git** | `git --version` | Any recent |

---

## Installation Overview (5 Phases)

```
Phase 1: System Dependencies     (~5 min)
    ├─ Bash 5.x
    ├─ sox, ffmpeg, util-linux
    └─ espeak-ng

Phase 2: Agent Vibes Install     (~5 min)
    ├─ Interactive installer
    ├─ Provider selection (Piper)
    ├─ Voice selection
    └─ Configuration

Phase 3: Piper TTS + Voices       (~5 min)
    ├─ Piper via pipx
    ├─ Download FR voices (4)
    └─ Download EN voices (12)

Phase 4: Configuration            (~2 min)
    ├─ Set provider: piper
    ├─ Set voice: fr_FR-tom-medium
    └─ Test audio

Phase 5: Verification             (~1 min)
    ├─ Test in Claude Code
    └─ Verify hooks active
```

---

## Phase 1: System Dependencies

### Step 1.1: Install Bash 5.x

Agent Vibes requires Bash 5.x (macOS ships with 3.2).

```bash
# Install Bash 5.x
brew install bash

# Verify installation
/opt/homebrew/bin/bash --version
# Expected: GNU bash, version 5.x
```

**Why**: Agent Vibes scripts use Bash 5.x features (associative arrays, etc.)

### Step 1.2: Install Audio Tools

```bash
# Install audio processing tools
brew install sox ffmpeg util-linux

# Verify sox
sox --version

# Verify ffmpeg
ffmpeg -version

# Verify flock (from util-linux)
/opt/homebrew/opt/util-linux/bin/flock --version
```

**Note**: `util-linux` is "keg-only" (not symlinked), but Agent Vibes finds it automatically.

### Step 1.3: Install espeak-ng (Piper Dependency)

```bash
# Install espeak-ng
brew install espeak-ng

# Verify installation
espeak-ng --version
```

**Why**: Piper TTS requires `libespeak-ng` library for phoneme processing.

### Checkpoint 1: Dependencies Installed ✅

```bash
# Verify all dependencies
command -v /opt/homebrew/bin/bash && \
command -v sox && \
command -v ffmpeg && \
command -v espeak-ng && \
echo "✅ All dependencies installed"
```

---

## Phase 2: Agent Vibes Installation

### Step 2.1: Launch Interactive Installer

```bash
# Navigate to your Claude Code project
cd /path/to/your/project

# Launch installer (interactive, 4 pages)
npx agentvibes install
```

**Expected**: ASCII art banner + welcome screen

### Step 2.2: Navigate Installation Pages

**Page 1/4: System Dependencies**
- Review detected dependencies
- All should show `✓` (green checkmark)
- Click **"Next →"**

**Page 2/4: Provider Selection**
- Options: `macOS Say`, `Piper TTS`, `Termux SSH`
- **Select**: `Piper TTS` (best quality, offline)
- Click **"Next →"**

**Page 3/4: Voice Selection**
- **For French**: Select `fr_FR-tom-medium` (male) or `fr_FR-siwis-medium` (female)
- **For English**: Select `en_US-ryan-high` (best quality)
- Click **"Next →"**

**Page 4/4: Audio Settings**
- **Reverb**: Select `Light` (recommended)
- **Background Music**: Select `Disabled` (avoid distraction)
- **Verbosity**: Select `Low` (less chatty)
- Click **"Start Installation"**

### Step 2.3: Installation Progress

Agent Vibes will install:
- 34 slash commands
- TTS scripts (40 bash scripts)
- Personality templates
- 16 background music tracks
- 7 config files

**Expected output**:
```
✔ Installed 34 slash commands!
✔ Installed TTS scripts!
✔ Installed personality templates!
✔ Installed 16 background music tracks!
✔ Installed 7 config files!

✅ AgentVibes is Ready!
```

### Checkpoint 2: Agent Vibes Installed ✅

```bash
# Verify installation
ls -la .claude/hooks/play-tts.sh
ls -la .claude/commands/agent-vibes/
ls -la .claude/audio/tracks/

# Check provider config
cat .claude/tts-provider.txt
# Expected: "macos" or "piper"
```

---

## Phase 3: Piper TTS + Voice Models

### Step 3.1: Install Piper TTS via pipx

If you chose Piper provider, Agent Vibes will attempt to install it. If it fails, manual installation:

```bash
# Install Piper via pipx (Python package manager)
pipx install piper-tts

# Verify installation
piper --help
```

**Common Issue**: Precompiled binary fails with `libespeak-ng.1.dylib` error.

**Solution**: `pipx install piper-tts` works reliably (Python version, not binary).

### Step 3.2: Download French Voices

```bash
# Navigate to voice storage
cd ~/.claude/piper-voices

# Download 4 French voice models
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

curl -L -o fr_FR-upmc-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx"
curl -L -o fr_FR-upmc-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json"

curl -L -o fr_FR-mls-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx"
curl -L -o fr_FR-mls-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/mls/medium/fr_FR-mls-medium.onnx.json"
```

**Size**: ~60-73MB per voice (4 voices = ~260MB total)

### Step 3.3: Download English Voices (Optional)

Agent Vibes auto-downloads 12 English voices during installation. Verify:

```bash
ls ~/.claude/piper-voices/en_US-*.onnx
```

**Expected**: 12 files (ryan, amy, lessac, bryce, etc.)

### Checkpoint 3: Voices Downloaded ✅

```bash
# Count voices
ls ~/.claude/piper-voices/*.onnx | wc -l
# Expected: 15+ files (12 EN + 4 FR minimum)

# Test French voice manually
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav
```

---

## Phase 4: Configuration

### Step 4.1: Set Piper as Provider

```bash
# Switch to Piper TTS (if not already set)
echo "piper" > .claude/tts-provider.txt

# Verify
cat .claude/tts-provider.txt
# Expected: "piper"
```

### Step 4.2: Set French Male Voice

```bash
# Set default voice
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# Verify
cat .claude/tts-voice.txt
# Expected: "fr_FR-tom-medium"
```

### Step 4.3: Test Audio Generation

```bash
# Test TTS pipeline manually
~/.claude/hooks/play-tts.sh "Ceci est un test audio"
```

**Expected**: Audio plays with French male voice.

**Troubleshooting**: If no audio, see [Troubleshooting Guide](./troubleshooting.md#no-audio).

### Checkpoint 4: Configuration Complete ✅

```bash
# Verify config files
test -f .claude/tts-provider.txt && \
test -f .claude/tts-voice.txt && \
test -f .claude/hooks/play-tts.sh && \
echo "✅ Configuration complete"
```

---

## Phase 5: Verification in Claude Code

### Step 5.1: Launch Claude Code

```bash
# Start Claude Code session
claude
```

### Step 5.2: Test TTS Commands

```bash
# In Claude, run:
/agent-vibes:whoami
# Expected: Shows current voice and provider

/agent-vibes:list
# Expected: Lists all 15+ voices

# Test TTS with simple request
> "Dis-moi bonjour en français"
# Expected: Audio response in French
```

### Step 5.3: Verify Hooks Active

```bash
# Exit Claude, check hook was triggered
ls -la /tmp/tts-*.wav
# Expected: Temporary audio files

# Check last played audio
ls -la ~/.claude/tts-last-played.wav
# Expected: File exists
```

### Checkpoint 5: Verification Complete ✅

```bash
# Final verification
cat .claude/tts-provider.txt && \
cat .claude/tts-voice.txt && \
piper --help > /dev/null 2>&1 && \
ls ~/.claude/piper-voices/*.onnx | wc -l && \
echo "✅ Installation successful!"
```

---

## Post-Installation Configuration

### Reduce Verbosity (Recommended)

```bash
# In Claude Code
/agent-vibes:verbosity low
```

**Why**: Reduces audio narration frequency, less distracting.

### Hide 34 Commands (Optional)

```bash
# In Claude Code
/agent-vibes:hide
```

**Why**: Declutters command palette. Use `/agent-vibes:show` to unhide.

### Disable Background Music

```bash
# In Claude Code
/agent-vibes:background-music off
```

**Why**: Background music can be distracting during focus work.

### Set Project Mute (Optional)

```bash
# Mute TTS for this project only
touch .claude/agentvibes-muted
```

**Why**: Some projects don't need audio (e.g., documentation-only repos).

---

## Performance Benchmarks

**System**: M1 MacBook Pro, 16GB RAM, macOS Sequoia 24.6.0

| Metric | Piper Medium | Piper High | macOS Say |
|--------|--------------|------------|-----------|
| **Audio Generation** | ~200ms | ~400ms | Instant |
| **Total Latency** | ~280ms | ~480ms | ~50ms |
| **RAM Usage** | ~50MB | ~70MB | ~10MB |
| **CPU Burst** | 80% (200ms) | 90% (400ms) | 5% (50ms) |
| **Voice Quality** | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ |
| **Offline** | ✅ | ✅ | ✅ |

**Recommendation**: Piper Medium = best quality/speed trade-off.

---

## Disk Usage

| Component | Size | Location |
|-----------|------|----------|
| **Piper TTS** | ~5MB | `~/.local/pipx/venvs/piper-tts/` |
| **Voice Models** | ~1GB | `~/.claude/piper-voices/` (15 voices × 60MB) |
| **Background Music** | ~300MB | `.claude/audio/tracks/` (16 tracks) |
| **Scripts** | ~2MB | `.claude/hooks/` (40 bash scripts) |
| **Total** | **~1.3GB** | - |

**Cleanup Tip**: Delete unused voices to save space.

---

## Uninstall Instructions

### Automated Uninstall

```bash
# Uninstall Agent Vibes completely
npx agentvibes uninstall --yes
```

### Manual Cleanup

```bash
# Remove Agent Vibes files
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/

# Remove Piper TTS
pipx uninstall piper-tts

# Remove voice models
rm -rf ~/.claude/piper-voices/

# Remove config files
rm .claude/tts-provider.txt
rm .claude/tts-voice.txt
rm .claude/agentvibes-muted 2>/dev/null
rm ~/.agentvibes-muted 2>/dev/null
```

---

## Common Installation Issues

### Issue 1: `libespeak-ng.1.dylib` Not Found

**Symptom**:
```
dyld[xxx]: Library not loaded: @rpath/libespeak-ng.1.dylib
```

**Solution**:
```bash
# Install espeak-ng
brew install espeak-ng

# Reinstall Piper via pipx (not binary)
pipx uninstall piper-tts
pipx install piper-tts
```

### Issue 2: `flock` Warning (Optional Tool)

**Symptom**:
```
⚠ flock - TTS queue locking
```

**Impact**: Minor. TTS works without `flock`, may have audio collision with rapid messages.

**Solution** (optional):
```bash
# flock is in util-linux, already installed
# Add to PATH if needed
export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"
```

### Issue 3: Agent Vibes Installer Exits

**Symptom**:
```
ExitPromptError: User force closed the prompt
```

**Cause**: Interactive installer requires user input (can't be automated).

**Solution**: Run `npx agentvibes install` in interactive terminal (not via script).

### Issue 4: No Audio After Installation

**Diagnostic**:
```bash
# 1. Check mute status
ls .claude/agentvibes-muted ~/.agentvibes-muted

# 2. Check provider
cat .claude/tts-provider.txt

# 3. Test Piper manually
echo "Test" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

**Solutions**: See [Troubleshooting Guide](./troubleshooting.md).

---

## Next Steps

After installation:

1. **[Voice Catalog](./voice-catalog.md)** - Explore 15 voices and choose your favorite
2. **[README](./README.md)** - Learn essential commands and use cases
3. **[Troubleshooting](./troubleshooting.md)** - Solve common issues
4. **[AI Ecosystem](../../../guide/ai-ecosystem.md#47-voice-interfaces)** - TTS in broader AI context

---

## Resources

- **Agent Vibes GitHub**: https://github.com/paulpreibisch/AgentVibes
- **Piper Voices Repository**: https://huggingface.co/rhasspy/piper-voices
- **Piper Voice Samples**: https://rhasspy.github.io/piper-samples/
- **Agent Vibes Website**: https://agentvibes.org

---

*Installation guide maintained by [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Last updated: 2026-01-22 | Tested on: macOS Sequoia 24.6.0 (Apple Silicon)*
