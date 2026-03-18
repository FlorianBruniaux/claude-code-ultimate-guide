---
title: "Agent Vibes - Complete Voice Catalog"
description: "Reference catalog of available TTS voices with quality ratings and language support"
tags: [reference, tts, integration]
---

# Agent Vibes - Complete Voice Catalog

**Total Voices**: 15 installed + 50+ available
**Languages**: French (4 models, 128 speakers), English (12 models)

---

## French Voices (Voix Françaises)

### Overview

| Voice ID | Gender | Quality | Speakers | Size | Recommended |
|----------|--------|---------|----------|------|-------------|
| **fr_FR-tom-medium** | Male | Medium | 1 | 60MB | ⭐️⭐️⭐️⭐️⭐️ Best FR male |
| fr_FR-siwis-medium | Female | Medium | 1 | 60MB | ⭐️⭐️⭐️⭐️ Clear, natural |
| fr_FR-upmc-medium | Neutral | Medium | 1 | 73MB | ⭐️⭐️⭐️ Multi-purpose |
| **fr_FR-mls-medium** | Mixed | Medium | **124** | 73MB | ⭐️⭐️⭐️⭐️⭐️ Maximum variety |

---

### fr_FR-tom-medium ⭐️⭐️⭐️⭐️⭐️

**Gender**: Male
**Quality**: Medium
**Character**: Professional, clear pronunciation, neutral accent
**Best For**: Technical documentation, code reviews, professional context
**Latency**: ~200ms

**Usage**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-tom-medium

# Manual test
echo "Bonjour, je m'appelle Tom. Je suis une voix synthétique française." | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/tom.wav && afplay /tmp/tom.wav
```

**Audio Sample**: Listen at https://rhasspy.github.io/piper-samples/ (search "fr_FR tom")

---

### fr_FR-siwis-medium ⭐️⭐️⭐️⭐️

**Gender**: Female
**Quality**: Medium
**Character**: Warm, natural, slightly Swiss accent
**Best For**: Tutorials, educational content, friendly interactions
**Latency**: ~200ms

**Usage**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-siwis-medium

# Manual test
echo "Bonjour, je suis Siwis. J'ai une voix claire et agréable." | \
  piper -m ~/.claude/piper-voices/fr_FR-siwis-medium.onnx \
  --output-file /tmp/siwis.wav && afplay /tmp/siwis.wav
```

**Audio Sample**: https://rhasspy.github.io/piper-samples/ (search "fr_FR siwis")

---

### fr_FR-upmc-medium ⭐️⭐️⭐️

**Gender**: Neutral (slightly female-leaning)
**Quality**: Medium
**Character**: Technical, precise, academic tone
**Best For**: Scientific content, data analysis, formal presentations
**Latency**: ~220ms (larger model)

**Usage**:
```bash
# In Claude Code
/agent-vibes:switch fr_FR-upmc-medium

# Manual test
echo "Analyse des données en cours. Résultats disponibles dans quelques instants." | \
  piper -m ~/.claude/piper-voices/fr_FR-upmc-medium.onnx \
  --output-file /tmp/upmc.wav && afplay /tmp/upmc.wav
```

**Audio Sample**: https://rhasspy.github.io/piper-samples/ (search "fr_FR upmc")

---

### fr_FR-mls-medium ⭐️⭐️⭐️⭐️⭐️ (Multi-Speaker)

**Gender**: Mixed (49 female, 75 male)
**Quality**: Medium
**Speakers**: **124 different voices**
**Character**: Massive variety (young, old, accents, tones)
**Best For**: Dialogue simulations, variety, character voices
**Latency**: ~200ms + speaker selection

**Usage**:
```bash
# In Claude Code (uses default speaker)
/agent-vibes:switch fr_FR-mls-medium

# Manual test with specific speaker (0-123)
echo "Je suis le speaker numéro 42" | \
  piper -m ~/.claude/piper-voices/fr_FR-mls-medium.onnx -s 42 \
  --output-file /tmp/mls-42.wav && afplay /tmp/mls-42.wav

# Test multiple speakers
for speaker in {0..5}; do
  echo "Bonjour, speaker $speaker" | \
    piper -m ~/.claude/piper-voices/fr_FR-mls-medium.onnx -s $speaker \
    --output-file /tmp/mls-$speaker.wav
  afplay /tmp/mls-$speaker.wav
  sleep 1
done
```

**Speaker Selection**:
- `0-48`: Female voices (49 total)
- `49-123`: Male voices (75 total)

**Recommended Speakers**:
| Speaker ID | Gender | Character |
|------------|--------|-----------|
| 7 | Female | Young, energetic |
| 15 | Female | Mature, professional |
| 23 | Female | Warm, friendly |
| 55 | Male | Deep, authoritative |
| 72 | Male | Clear, technical |
| 99 | Male | Young, casual |

**Audio Samples**: https://rhasspy.github.io/piper-samples/ (search "fr_FR mls")

---

## English Voices (Voix Anglaises)

### Overview

| Voice ID | Gender | Quality | Character | Recommended |
|----------|--------|---------|-----------|-------------|
| **en_US-ryan-high** | Male | High | Professional | ⭐️⭐️⭐️⭐️⭐️ Best EN |
| en_US-amy-medium | Female | Medium | Warm, natural | ⭐️⭐️⭐️⭐️ |
| en_US-lessac-medium | Male | Medium | Authoritative | ⭐️⭐️⭐️⭐️ |
| en_US-libritts-high | Mixed | High | Very natural | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-hfc_female-medium | Female | Medium | Technical | ⭐️⭐️⭐️ |
| en_US-bryce-medium | Male | Medium | Young, dynamic | ⭐️⭐️⭐️ |
| en_US-danny-low | Male | Low | Fast, efficient | ⭐️⭐️ |
| en_US-kathleen-low | Female | Low | Fast, efficient | ⭐️⭐️ |
| en_US-kusal-medium | Male | Medium | Indian accent | ⭐️⭐️⭐️ |
| en_US-kristin-medium | Female | Medium | Clear, neutral | ⭐️⭐️⭐️⭐️ |
| en_US-libritts_r-high | Mixed | High | Very natural | ⭐️⭐️⭐️⭐️⭐️ |
| 16Speakers | Multi | Medium | 16 different | ⭐️⭐️⭐️⭐️ |

---

### en_US-ryan-high ⭐️⭐️⭐️⭐️⭐️

**Gender**: Male
**Quality**: High (best English voice)
**Character**: Professional news anchor, clear pronunciation
**Best For**: Professional presentations, documentation, code reviews
**Latency**: ~400ms (high quality model)

**Usage**:
```bash
/agent-vibes:switch en_US-ryan-high
```

---

### en_US-amy-medium ⭐️⭐️⭐️⭐️

**Gender**: Female
**Quality**: Medium
**Character**: Warm, friendly, conversational
**Best For**: Tutorials, casual interactions, educational content
**Latency**: ~200ms

**Usage**:
```bash
/agent-vibes:switch en_US-amy-medium
```

---

### en_US-libritts-high ⭐️⭐️⭐️⭐️⭐️

**Gender**: Mixed (multi-speaker)
**Quality**: High
**Character**: Very natural, expressive
**Best For**: High-quality audio narration
**Latency**: ~400ms

**Usage**:
```bash
/agent-vibes:switch en_US-libritts-high
```

---

### 16Speakers ⭐️⭐️⭐️⭐️ (Multi-Speaker English)

**Gender**: Mixed (8 female, 8 male)
**Quality**: Medium
**Speakers**: 16 different English voices
**Character**: Variety of ages, accents, tones
**Best For**: Dialogue, variety, character narration
**Latency**: ~200ms + speaker selection

**Usage**:
```bash
# Default speaker
/agent-vibes:switch 16Speakers

# Specific speaker (0-15)
echo "I am speaker number 5" | \
  piper -m ~/.claude/piper-voices/16Speakers.onnx -s 5 \
  --output-file /tmp/16sp-5.wav && afplay /tmp/16sp-5.wav
```

---

## Low-Quality Voices (Faster, Lower Quality)

### When to Use Low-Quality

- Battery optimization (50% faster generation)
- Latency-sensitive applications (<150ms requirement)
- Quick prototyping or testing
- Background notifications (quality less important)

### Available Low-Quality Models

| Voice ID | Gender | Latency | Quality |
|----------|--------|---------|---------|
| en_US-danny-low | Male | ~100ms | ⭐️⭐️ |
| en_US-kathleen-low | Female | ~100ms | ⭐️⭐️ |
| fr_FR-gilles-low | Male | ~100ms | ⭐️⭐️ |
| fr_FR-siwis-low | Female | ~100ms | ⭐️⭐️ |

**Download Low-Quality Voice**:
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-gilles-low.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx"
curl -L -o fr_FR-gilles-low.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/gilles/low/fr_FR-gilles-low.onnx.json"
```

---

## High-Quality Voices (Slower, Better Quality)

### When to Use High-Quality

- Professional presentations
- Content creation (videos, podcasts)
- Demos or public showcases
- When latency is not critical

### Available High-Quality Models

| Voice ID | Gender | Latency | Quality |
|----------|--------|---------|---------|
| en_US-ryan-high | Male | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-libritts-high | Mixed | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| en_US-libritts_r-high | Mixed | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |
| fr_FR-siwis-high | Female | ~400ms | ⭐️⭐️⭐️⭐️⭐️ |

**Download High-Quality Voice**:
```bash
cd ~/.claude/piper-voices
curl -L -o fr_FR-siwis-high.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx"
curl -L -o fr_FR-siwis-high.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/high/fr_FR-siwis-high.onnx.json"
```

---

## Additional Languages

Piper TTS supports **50+ languages**. Download additional voices from Hugging Face.

### Popular Languages Available

| Language | Voices Available | Repository |
|----------|------------------|------------|
| Spanish (es_ES) | 10+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES) |
| German (de_DE) | 8+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/de/de_DE) |
| Italian (it_IT) | 6+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/it/it_IT) |
| Portuguese (pt_BR) | 5+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/pt/pt_BR) |
| Russian (ru_RU) | 4+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU) |
| Chinese (zh_CN) | 3+ voices | [Link](https://huggingface.co/rhasspy/piper-voices/tree/main/zh/zh_CN) |

### Download Spanish Voice Example

```bash
cd ~/.claude/piper-voices

# Spanish male voice (Davefx - high quality)
curl -L -o es_ES-davefx-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx"
curl -L -o es_ES-davefx-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json"

# Test
echo "Hola, soy Claude y hablo español" | \
  piper -m es_ES-davefx-medium.onnx \
  --output-file /tmp/es.wav && afplay /tmp/es.wav
```

---

## Voice Selection Recommendations

### By Use Case

| Use Case | Recommended Voice | Reason |
|----------|-------------------|--------|
| **Technical Documentation** | fr_FR-tom-medium | Clear, professional, technical tone |
| **Code Reviews** | en_US-ryan-high | Authoritative, clear pronunciation |
| **Tutorials** | fr_FR-siwis-medium | Warm, friendly, educational |
| **Background Notifications** | fr_FR-gilles-low | Fast, efficient, low latency |
| **Professional Presentations** | en_US-ryan-high | Best quality, professional |
| **Variety/Dialogue** | fr_FR-mls-medium | 124 different voices |
| **Battery Optimization** | Any "-low" voice | 50% faster generation |

### By Language

| Primary Language | Best Voice | Alternative |
|------------------|------------|-------------|
| **French** | fr_FR-tom-medium | fr_FR-mls-medium (variety) |
| **English** | en_US-ryan-high | en_US-libritts-high |
| **Spanish** | es_ES-davefx-medium | es_ES-carlfm-medium |
| **German** | de_DE-thorsten-high | de_DE-kerstin-low |

---

## Voice Comparison Tool

Compare voices side-by-side:

```bash
# Create comparison script
cat > /tmp/compare-voices.sh << 'EOF'
#!/bin/bash
TEXT="$1"
VOICES=("fr_FR-tom-medium" "fr_FR-siwis-medium" "fr_FR-upmc-medium")

for voice in "${VOICES[@]}"; do
  echo "Testing $voice..."
  echo "$TEXT" | piper -m ~/.claude/piper-voices/${voice}.onnx \
    --output-file /tmp/${voice}.wav
  afplay /tmp/${voice}.wav
  sleep 2
done
EOF

chmod +x /tmp/compare-voices.sh

# Compare voices
/tmp/compare-voices.sh "Bonjour, ceci est un test de comparaison"
```

---

## Resources

- **Piper Voice Repository**: https://huggingface.co/rhasspy/piper-voices
- **Audio Samples**: https://rhasspy.github.io/piper-samples/
- **Voice Training**: https://github.com/rhasspy/piper/blob/master/TRAINING.md
- **Custom Voices**: https://community.rhasspy.org/c/piper/

---

*Voice catalog maintained by [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide)*
*Last updated: 2026-01-22 | Piper TTS v1.3.0*
