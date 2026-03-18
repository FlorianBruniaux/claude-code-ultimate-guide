---
title: "Agent Vibes TTS - Text-to-Speech for Claude Code"
description: "Community MCP server adding text-to-speech capabilities to Claude Code"
tags: [mcp, integration, plugin]
---

# Agent Vibes TTS - Text-to-Speech for Claude Code

**Status**: Community MCP Server (optional)
**Version**: 3.0.0
**Maintainer**: [Paul Preibisch](https://github.com/paulpreibisch/AgentVibes)
**License**: Apache 2.0

---

## Quick Decision Matrix

Should you install Agent Vibes? Use this matrix:

| Use Case | Recommendation | Reason |
|----------|----------------|--------|
| Code reviews (listen while multitasking) | ⭐️⭐️⭐️⭐️⭐️ | Audio narration frees your eyes |
| Long debugging sessions | ⭐️⭐️⭐️⭐️ | Audio notifications keep you informed |
| Focus-intensive work | ⚠️ Can be distracting | Consider mute during deep work |
| Offline TTS (no internet) | ✅ Perfect fit | Piper TTS is 100% offline |
| Premium voice quality | ❌ Use ElevenLabs | Agent Vibes = free, good quality |
| French language | ⭐️⭐️⭐️⭐️ | 4 FR voices (128 speakers) |
| English language | ⭐️⭐️⭐️⭐️⭐️ | 12 EN voices (high quality) |

---

## 30-Second Overview

Agent Vibes adds **audible narration** to Claude Code responses using:

- **15 voices** (12 English, 4 French including 124 speakers)
- **100% free** (Piper TTS + macOS Say)
- **100% offline** (no cloud dependency)
- **18-minute installation** (5 phases with checkpoints)
- **34 slash commands** for voice control

**Installation**: [Complete Guide](./installation.md) | [Quick Workflow](../../../guide/workflows/tts-setup.md)
**Usage**: [Voice Catalog](./voice-catalog.md) | [Troubleshooting](./troubleshooting.md)

---

## How It Works

### Architecture

```
Claude Code Response
    ↓
.claude/hooks/play-tts.sh (Router)
    ↓
[Mute Check] → Exit if muted
    ↓
[Provider Manager]
    ├─ piper   → Piper TTS (offline, neural voices)
    ├─ macos   → macOS Say (native, instant)
    └─ termux  → Android via SSH
    ↓
[Voice Processing]
    ├─ Load voice model (~60MB)
    ├─ Generate audio (~200ms)
    ├─ Apply effects (reverb, echo)
    └─ Mix background music (optional)
    ↓
[Audio Output] → afplay (macOS) / speaker
```

**Performance (M1 Mac)**:
- Audio generation: ~200ms
- Total latency: ~280ms (generation + effects + playback)
- RAM usage: ~50MB
- CPU: ~80% burst (200ms), then idle

---

## Quick Start (5 Minutes)

### Prerequisites

- macOS with Homebrew
- Bash 5.x (Agent Vibes will help install)
- Node.js 16+ (for installation)

### Installation

```bash
# 1. Install Agent Vibes (interactive, 4 pages)
npx agentvibes install

# 2. Choose Piper TTS provider (recommended)
# Select: Piper > fr_FR-tom-medium > Light reverb > Low verbosity

# 3. Verify installation
ls -la .claude/hooks/play-tts.sh
ls -la ~/.claude/piper-voices/
```

**Stuck?** See [Full Installation Guide](./installation.md) or [Troubleshooting](./troubleshooting.md)

### First Test

```bash
# Launch Claude Code
claude

# In Claude, test TTS
/agent-vibes:whoami
/agent-vibes:list
> "Say hello in French"
```

You should hear audio narration!

---

## Activation & Deactivation

### Quick Mute/Unmute

```bash
# In Claude Code
/agent-vibes:mute      # Mute (persists across sessions)
/agent-vibes:unmute    # Unmute

# Or manually
touch .claude/agentvibes-muted      # Project mute
touch ~/.agentvibes-muted           # Global mute
rm .claude/agentvibes-muted         # Project unmute
```

### Mute Hierarchy

```
Priority 1: .claude/agentvibes-unmuted  (project override)
Priority 2: .claude/agentvibes-muted    (project mute)
Priority 3: ~/.agentvibes-muted         (global mute)
Priority 4: Active by default
```

**Example**: Mute globally, unmute specific project:
```bash
touch ~/.agentvibes-muted                 # All projects muted
touch .claude/agentvibes-unmuted          # This project unmuted
```

### Complete Uninstall

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

## Essential Commands

### Provider Management

```bash
/agent-vibes:provider list              # List available providers
/agent-vibes:provider switch piper      # Switch to Piper TTS
/agent-vibes:provider switch macos      # Switch to macOS Say
/agent-vibes:provider info              # Current provider details
```

### Voice Management

```bash
/agent-vibes:list                       # List all voices
/agent-vibes:list first 5               # Show first 5 voices
/agent-vibes:switch fr_FR-tom-medium    # Switch to French male voice
/agent-vibes:whoami                     # Current voice & provider
/agent-vibes:preview                    # Preview first 3 voices
/agent-vibes:sample fr_FR-tom-medium    # Test specific voice
```

### Audio Control

```bash
/agent-vibes:mute                       # Mute all TTS
/agent-vibes:unmute                     # Unmute TTS
/agent-vibes:replay                     # Replay last audio
/agent-vibes:replay 2                   # Replay second-to-last
/agent-vibes:verbosity low              # Speak less (recommended)
/agent-vibes:verbosity medium           # Speak more
```

### Effects & Personalization

```bash
/agent-vibes:effects reverb light       # Add light reverb
/agent-vibes:effects off                # Disable all effects
/agent-vibes:background-music on        # Enable background music
/agent-vibes:background-music off       # Disable background music
/agent-vibes:personality sarcastic      # Change personality
/agent-vibes:personality professional   # Professional mode
```

### Utility Commands

```bash
/agent-vibes:hide                       # Hide all 34 commands
/agent-vibes:show                       # Show commands again
/agent-vibes:version                    # Agent Vibes version
/agent-vibes:update                     # Update Agent Vibes
```

**Full command reference**: 34 commands available. Use `/agent-vibes:hide` if they clutter your command palette.

---

## Voice Catalog Quick Reference

### French Voices (4 models, 128 speakers)

| Voice | Gender | Quality | Speakers | Use Case |
|-------|--------|---------|----------|----------|
| **fr_FR-tom-medium** | Male | Medium | 1 | ⭐️⭐️⭐️⭐️⭐️ Best FR male |
| fr_FR-siwis-medium | Female | Medium | 1 | Clear, natural |
| fr_FR-upmc-medium | Neutral | Medium | 1 | Multi-purpose |
| **fr_FR-mls-medium** | Mixed | Medium | 124 | ⭐️⭐️⭐️⭐️⭐️ Maximum variety |

**Multi-speakers**: `fr_FR-mls-medium` has 124 different voices (49 female, 75 male). Use `-s 0-123` flag to select specific speaker.

### English Voices (12 models)

| Voice | Gender | Quality | Character |
|-------|--------|---------|-----------|
| **en_US-ryan-high** | Male | High | ⭐️⭐️⭐️⭐️⭐️ Professional |
| en_US-amy-medium | Female | Medium | Warm, natural |
| en_US-lessac-medium | Male | Medium | Authoritative |
| en_US-libritts-high | Mixed | High | Very natural |
| ... | ... | ... | 8 more voices |

**Full catalog with audio samples**: [Voice Catalog](./voice-catalog.md)

---

## Common Use Cases

### 1. Listen During Code Reviews

```bash
# Enable TTS with low verbosity
/agent-vibes:verbosity low

# Work on other tasks while listening to Claude's analysis
> "Review the authentication middleware for security issues"
```

### 2. Audio Notifications for Long Tasks

```bash
# Run long test suite, get notified when done
> "Run the full test suite and report failures"
# → Audio alert when tests complete
```

### 3. Language Learning Mode

```bash
# Enable dual-language TTS
/agent-vibes:learn on
/agent-vibes:target es_ES
/agent-vibes:target-voice es_ES-davefx-medium

# Responses spoken in both English and Spanish
> "Explain dependency injection"
```

### 4. Custom Hooks (Errors Only)

```bash
# Create selective TTS hook
cat > .claude/hooks/speak-errors-only.sh << 'EOF'
#!/opt/homebrew/bin/bash
INPUT=$(cat)
BODY=$(echo "$INPUT" | jq -r '.notification.body // empty')

# Speak only if contains "error" or "failed"
if [[ "$BODY" =~ (error|failed|Error|Failed) ]]; then
  ~/.claude/hooks/play-tts.sh "$BODY"
fi
exit 0
EOF

chmod +x .claude/hooks/speak-errors-only.sh
```

---

## Performance Tips

### Reduce Latency

```bash
# Use low-quality voice (faster generation)
/agent-vibes:switch fr_FR-siwis-low  # If available

# Disable effects
/agent-vibes:effects off

# Disable background music
/agent-vibes:background-music off

# Result: ~150ms latency instead of ~280ms
```

### Optimize for Battery

```bash
# macOS Say (instant, no CPU burst)
/agent-vibes:provider switch macos

# Trade-off: Lower quality, but 0ms generation time
```

### Reduce Distraction

```bash
# Minimum verbosity
/agent-vibes:verbosity low

# Professional personality (less chatty)
/agent-vibes:personality professional

# Or mute during focus work
/agent-vibes:mute
```

---

## Troubleshooting

### No Audio

```bash
# 1. Check mute status
ls -la .claude/agentvibes-muted ~/.agentvibes-muted

# 2. Verify provider
cat .claude/tts-provider.txt

# 3. Test Piper manually
echo "Test" | piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test.wav && afplay /tmp/test.wav
```

**Solution**: See [Troubleshooting Guide](./troubleshooting.md) for detailed diagnostics.

### Voice Sounds Robotic

**Solution**: Switch to high-quality model:
```bash
# Download high-quality voice
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"

/agent-vibes:switch fr_FR-siwis-high
```

### 34 Commands Clutter Command Palette

**Solution**: Hide them:
```bash
/agent-vibes:hide

# Unhide later if needed
/agent-vibes:show
```

**More issues?** Check [Troubleshooting Guide](./troubleshooting.md)

---

## Configuration Files

| File | Purpose | Format |
|------|---------|--------|
| `.claude/tts-provider.txt` | Active provider | `piper` or `macos` or `termux` |
| `.claude/tts-voice.txt` | Active voice | `fr_FR-tom-medium` |
| `.claude/agentvibes-muted` | Project mute status | Existence = muted |
| `~/.agentvibes-muted` | Global mute status | Existence = muted |
| `.claude/config/audio-effects.cfg` | Audio effects config | Key=Value format |
| `~/.claude/piper-voices/*.onnx` | Voice models | Neural network models |

---

## Related Documentation

- **[Installation Guide](./installation.md)** - Complete 18-minute setup procedure
- **[Voice Catalog](./voice-catalog.md)** - All 15 voices with audio samples
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions
- **[TTS Setup Workflow](../../../guide/workflows/tts-setup.md)** - Step-by-step installation
- **[AI Ecosystem](../../../guide/ai-ecosystem.md#47-voice-interfaces)** - TTS in AI context

---

## Resources

- **GitHub**: https://github.com/paulpreibisch/AgentVibes
- **Website**: https://agentvibes.org
- **Demo Video**: https://youtu.be/ngLiA_KQtTA
- **Piper Voices**: https://huggingface.co/rhasspy/piper-voices
- **Piper Samples**: https://rhasspy.github.io/piper-samples/

---

## Contributing

Agent Vibes is a community project. Report issues or contribute:
- **Issues**: https://github.com/paulpreibisch/AgentVibes/issues
- **License**: Apache 2.0

---

*Integration guide maintained by [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Last updated: 2026-01-22 | Agent Vibes v3.0.0 | Piper TTS v1.3.0*
