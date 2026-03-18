---
title: "Agent Vibes - Troubleshooting Guide"
description: "Diagnostic steps and solutions for common Agent Vibes TTS issues"
tags: [guide, tts, debugging, integration]
---

# Agent Vibes - Troubleshooting Guide

**Common Issues**: 7 scenarios with step-by-step solutions
**Diagnostic Tools**: Commands and scripts for problem identification

---

## Issue 1: No Audio Output

### Symptom
```
Claude responds but no TTS audio plays
```

### Diagnostic Steps

```bash
# 1. Check if muted
ls -la .claude/agentvibes-muted ~/.agentvibes-muted
# If file exists → TTS is muted

# 2. Check provider configuration
cat .claude/tts-provider.txt
# Expected: "piper" or "macos"

# 3. Check voice configuration
cat .claude/tts-voice.txt
# Expected: voice name like "fr_FR-tom-medium"

# 4. Test Piper directly
echo "Test audio" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

### Solutions

**If muted**:
```bash
# Unmute
rm .claude/agentvibes-muted
rm ~/.agentvibes-muted 2>/dev/null

# Or in Claude Code
/agent-vibes:unmute
```

**If provider misconfigured**:
```bash
# Set Piper as provider
echo "piper" > .claude/tts-provider.txt

# Verify
cat .claude/tts-provider.txt
```

**If voice missing**:
```bash
# Download missing voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"
```

**If Piper command fails**:
```bash
# Reinstall Piper via pipx
pipx uninstall piper-tts
pipx install piper-tts

# Verify
piper --help
```

---

## Issue 2: libespeak-ng.1.dylib Not Found

### Symptom
```
dyld[xxx]: Library not loaded: @rpath/libespeak-ng.1.dylib
  Referenced from: /Users/.../piper
  Reason: tried: '/usr/local/lib/libespeak-ng.1.dylib' (no such file)
```

### Root Cause
Piper binary requires `espeak-ng` library which is not installed.

### Solution

```bash
# Install espeak-ng
brew install espeak-ng

# Verify installation
espeak-ng --version
# Expected: eSpeak NG text-to-speech: 1.52.0

# Find library location
find /opt/homebrew -name "libespeak-ng*.dylib"
# Expected: /opt/homebrew/lib/libespeak-ng.1.dylib

# If Piper still fails, reinstall via pipx (not binary)
pipx uninstall piper-tts 2>/dev/null
pipx install piper-tts

# Test again
piper --help
```

### Prevention
Always install `espeak-ng` **before** installing Piper TTS.

---

## Issue 3: Voice Sounds Robotic or Low Quality

### Symptom
```
Audio plays but voice quality is poor, robotic, unnatural
```

### Diagnostic

```bash
# Check which voice model is loaded
cat .claude/tts-voice.txt

# Check voice quality level
ls -lh ~/.claude/piper-voices/*.onnx | grep $(cat .claude/tts-voice.txt)
# Low quality: ~20-30MB
# Medium quality: ~50-70MB
# High quality: ~100-150MB
```

### Solutions

**Upgrade to high-quality model**:
```bash
# Download high-quality French voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"
curl -L -o fr_FR-siwis-high.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx.json"

# Switch to high-quality voice
/agent-vibes:switch fr_FR-siwis-high
```

**Alternative: Try different voice**:
```bash
# Test multiple voices to find preferred one
/agent-vibes:preview

# Or test manually
for voice in fr_FR-tom-medium fr_FR-siwis-medium fr_FR-upmc-medium; do
  echo "Test voix $voice" | \
    piper -m ~/.claude/piper-voices/${voice}.onnx \
    --output-file /tmp/${voice}.wav
  afplay /tmp/${voice}.wav
  sleep 2
done
```

**Quality Comparison**:
| Quality | Size | Latency | Naturalness |
|---------|------|---------|-------------|
| Low | ~25MB | ~100ms | ⭐️⭐️ |
| Medium | ~60MB | ~200ms | ⭐️⭐️⭐️⭐️ |
| High | ~120MB | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |

---

## Issue 4: High Latency (>500ms)

### Symptom
```
Noticeable delay between Claude response and audio playback
```

### Diagnostic

```bash
# Time audio generation
time (echo "Test rapide" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav > /dev/null 2>&1)
# Expected: ~0.2s for medium quality

# Check if effects are enabled
cat .claude/config/audio-effects.cfg 2>/dev/null
# Look for REVERB_ENABLED=true, ECHO_ENABLED=true

# Check if background music enabled
cat .claude/config/background-music.cfg 2>/dev/null
# Look for ENABLED=true
```

### Solutions

**Switch to low-quality voice** (50% faster):
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-gilles-low.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx"
curl -L -o fr_FR-gilles-low.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx.json"

/agent-vibes:switch fr_FR-gilles-low
```

**Disable audio effects**:
```bash
# In Claude Code
/agent-vibes:effects off

# Or manually
echo "REVERB_ENABLED=false" > .claude/config/audio-effects.cfg
echo "ECHO_ENABLED=false" >> .claude/config/audio-effects.cfg
```

**Disable background music**:
```bash
# In Claude Code
/agent-vibes:background-music off

# Or manually
echo "ENABLED=false" > .claude/config/background-music.cfg
```

**Switch to macOS Say** (instant, lower quality):
```bash
/agent-vibes:provider switch macos
```

**Performance Comparison**:
| Configuration | Latency | Quality |
|---------------|---------|---------|
| Piper High + Effects + Music | ~500ms | ⭐️⭐️⭐️⭐️⭐️ |
| Piper Medium + Effects | ~280ms | ⭐️⭐️⭐️⭐️ |
| Piper Medium (no effects) | ~200ms | ⭐️⭐️⭐️⭐️ |
| Piper Low (no effects) | ~100ms | ⭐️⭐️ |
| macOS Say | ~50ms | ⭐️⭐️⭐️ |

---

## Issue 5: Agent Vibes Commands Clutter Palette

### Symptom
```
34 /agent-vibes:* commands clutter Claude Code command palette
```

### Solution

```bash
# Hide all Agent Vibes commands
/agent-vibes:hide

# Commands still work, just hidden from autocomplete

# Unhide later if needed
/agent-vibes:show
```

### Alternative: Remove Agent Vibes Completely

```bash
npx agentvibes uninstall --yes
```

---

## Issue 6: Audio Plays Multiple Times (Echo/Repeat)

### Symptom
```
Same audio plays 2-3 times in rapid succession
```

### Root Cause
`flock` (file locking) not available, causing race condition with rapid messages.

### Diagnostic

```bash
# Check if flock is available
which flock || /opt/homebrew/opt/util-linux/bin/flock --version
```

### Solution

```bash
# Install util-linux (contains flock)
brew install util-linux

# Add flock to PATH (optional)
echo 'export PATH="/opt/homebrew/opt/util-linux/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
flock --version
```

### Workaround (if flock unavailable)
```bash
# Reduce verbosity to minimize rapid messages
/agent-vibes:verbosity low
```

---

## Issue 7: Installation Hangs or Exits

### Symptom
```
npx agentvibes install exits with:
ExitPromptError: User force closed the prompt
```

### Root Cause
Interactive installer requires terminal input, can't be automated.

### Solution

```bash
# Ensure you're in interactive terminal (not script)
# Run directly in terminal, not via automation

npx agentvibes install

# If still fails, try without cache
npx --yes agentvibes@latest install
```

### Alternative: Manual Installation

```bash
# If installer fails repeatedly, install components manually

# 1. Install Piper TTS
pipx install piper-tts

# 2. Download voices
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices
# ... download voices manually (see voice-catalog.md)

# 3. Create config files
echo "piper" > .claude/tts-provider.txt
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# 4. Download Agent Vibes scripts
# (Contact maintainer or extract from npm package)
```

---

## Diagnostic Script

Create comprehensive diagnostic script:

```bash
cat > /tmp/agent-vibes-diagnostic.sh << 'EOF'
#!/bin/bash
echo "=== Agent Vibes Diagnostic ==="
echo ""

echo "1. System Dependencies"
command -v /opt/homebrew/bin/bash && echo "  ✓ Bash 5.x" || echo "  ✗ Bash 5.x missing"
command -v sox && echo "  ✓ sox" || echo "  ✗ sox missing"
command -v ffmpeg && echo "  ✓ ffmpeg" || echo "  ✗ ffmpeg missing"
command -v espeak-ng && echo "  ✓ espeak-ng" || echo "  ✗ espeak-ng missing"
command -v piper && echo "  ✓ piper" || echo "  ✗ piper missing"
echo ""

echo "2. Configuration Files"
test -f .claude/tts-provider.txt && echo "  ✓ Provider: $(cat .claude/tts-provider.txt)" || echo "  ✗ Provider not configured"
test -f .claude/tts-voice.txt && echo "  ✓ Voice: $(cat .claude/tts-voice.txt)" || echo "  ✗ Voice not configured"
test -f .claude/hooks/play-tts.sh && echo "  ✓ TTS hook installed" || echo "  ✗ TTS hook missing"
echo ""

echo "3. Mute Status"
test -f .claude/agentvibes-muted && echo "  ⚠ Project muted" || echo "  ✓ Project unmuted"
test -f ~/.agentvibes-muted && echo "  ⚠ Global muted" || echo "  ✓ Global unmuted"
echo ""

echo "4. Voice Models"
echo "  Installed voices: $(ls ~/.claude/piper-voices/*.onnx 2>/dev/null | wc -l)"
ls ~/.claude/piper-voices/*.onnx 2>/dev/null | sed 's|.*/||' | sed 's|.onnx||' | sed 's/^/    - /'
echo ""

echo "5. Audio Test"
if command -v piper > /dev/null 2>&1; then
  echo "Test" | piper -m ~/.claude/piper-voices/$(cat .claude/tts-voice.txt).onnx \
    --output-file /tmp/diagnostic-test.wav 2>&1 | grep -q "error" && \
    echo "  ✗ Audio generation failed" || echo "  ✓ Audio generation successful"
  afplay /tmp/diagnostic-test.wav 2>/dev/null && echo "  ✓ Audio playback successful" || echo "  ✗ Audio playback failed"
else
  echo "  ✗ Piper not installed, skipping test"
fi
echo ""

echo "=== End Diagnostic ==="
EOF

chmod +x /tmp/agent-vibes-diagnostic.sh

# Run diagnostic
/tmp/agent-vibes-diagnostic.sh
```

---

## Getting Help

If issues persist:

1. **Run diagnostic script** (above) and share output
2. **Check Agent Vibes GitHub Issues**: https://github.com/paulpreibisch/AgentVibes/issues
3. **Check Claude Code Guide**: [AI Ecosystem](../../../guide/ai-ecosystem.md)
4. **Check logs**: `tail -f ~/.claude/tts-debug.log` (if exists)

---

## Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Bash 3.2 (macOS default) | Scripts fail | Install Bash 5.x via Homebrew |
| No Windows support | Can't run natively | Use WSL2 or macOS |
| flock optional | Audio may overlap | Install util-linux or reduce verbosity |
| Large voice files | ~1GB disk space | Delete unused voices |
| Latency with high-quality | ~400ms delay | Use medium or low quality |

---

*Troubleshooting guide maintained by [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Last updated: 2026-01-22 | Agent Vibes v3.0.0*
