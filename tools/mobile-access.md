# Claude Code Mobile Access

> **⚠️ STATUS: WIP / UNTESTED**
>
> This guide is a work in progress. The setup has not been fully tested across different environments.
> Use at your own risk. Contributions and feedback welcome.

---

## The Problem

Claude Code CLI is a **local interactive process**, not a service with a session API. Each instance is autonomous. Even `claude --remote` only offloads execution—it doesn't create a relay system.

**What's missing**: A native `claude --serve` mode that exposes a WebSocket API, allows multiple clients, and maintains the same conversation context.

**The workaround**: Expose your terminal via web browser using `ttyd`, accessible from anywhere via `Tailscale` VPN.

---

## Solution: ttyd + Tailscale

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Browser        │
│  (runs here)    │   Tailscale   │  (same session) │
│                 │   (VPN)       │                 │
└─────────────────┘               └─────────────────┘
```

- **ttyd**: Exposes your terminal in a web browser
- **Tailscale**: Free VPN that gives your computer a fixed IP, accessible from anywhere (4G, public WiFi, etc.)
- **tmux**: Keeps session alive even if you close the browser

**Use case**: Follow and continue Claude Code sessions from your phone (commuting, away from desk, etc.)

---

## Architecture Comparison

### ttyd + Tailscale (Self-hosted)

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │◄──────────────│  Browser        │
│  (runs here)    │   Tailscale   │  (same session) │
│  ┌───────────┐  │   VPN         │                 │
│  │   ttyd    │  │               └─────────────────┘
│  └───────────┘  │
└─────────────────┘
✅ ToS-Safe: CLI officiel, pas d'intermédiaire cloud
```

### Happy Coder (App native)

```
YOUR COMPUTER                     YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Claude Code    │               │  Happy App      │
│  (CLI officiel) │◄─────────────►│  (Expo native)  │
│       ▲         │   Local sync  │                 │
│  subprocess     │               └─────────────────┘
│  ┌───────────┐  │
│  │ Happy Hub │  │
│  └───────────┘  │
└─────────────────┘
✅ ToS-Safe: Wrapper local, subprocess Node.js
```

### Remoto.sh (Cloud relay)

```
REMOTO CLOUD                      YOUR PHONE
┌─────────────────┐               ┌─────────────────┐
│  Docker         │◄──────────────│  Browser        │
│  Container      │   WebSocket   │                 │
│  ┌───────────┐  │               └─────────────────┘
│  │ Claude    │  │
│  │ Code CLI  │  │
│  └───────────┘  │
└─────────────────┘
⚠️ ToS Risk: Cloud wrapping = potentiel "proxy non autorisé"
```

---

## Why This Approach?

### ToS Considerations

Some third-party wrappers (like OpenCode) have been blocked by Anthropic for ToS violations. This approach is **ToS-safe** because:

- You're using the **official Claude Code CLI**
- ttyd just exposes your terminal via browser (no wrapper)
- Tailscale is just a VPN for secure access
- No third-party client interacting with Claude's API

---

## Prerequisites

- macOS or Linux
- Claude Code CLI installed and authenticated
- Tailscale account (free tier works)

---

## Installation

### Quick Setup Script

```bash
#!/bin/bash
# claude-mobile-setup.sh

set -e

echo "=== Setup Claude Code Mobile ==="

# 1. Install ttyd + tmux
echo "[1/2] Installing ttyd..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ttyd tmux
else
    sudo apt install -y tmux
    sudo snap install ttyd --classic
fi

# 2. Install Tailscale
echo "[2/2] Installing Tailscale..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install tailscale
else
    curl -fsSL https://tailscale.com/install.sh | sh
fi

# 3. Create launcher script
mkdir -p ~/.local/bin
cat > ~/.local/bin/claude-mobile << 'EOF'
#!/bin/bash
PORT=7681
PASS="${CLAUDE_MOBILE_PASS:-claude123}"

TS_IP=$(tailscale ip -4 2>/dev/null || echo "not connected")

echo "══════════════════════════════════"
echo "  CLAUDE CODE MOBILE"
echo "══════════════════════════════════"
echo "  URL:  http://$TS_IP:$PORT"
echo "  User: claude"
echo "  Pass: $PASS"
echo "══════════════════════════════════"
echo ""
echo "Open this URL on your phone."
echo "Press Ctrl+C to stop."
echo ""

# Kill existing session if any
tmux kill-session -t cc 2>/dev/null || true

# Start Claude in tmux, expose via ttyd
tmux new-session -d -s cc 'claude'
exec ttyd -W -p $PORT -c "claude:$PASS" tmux attach -t cc
EOF

chmod +x ~/.local/bin/claude-mobile

# Add to PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next steps:"
echo "  1. Run: tailscale up"
echo "  2. Run: source ~/.zshrc"
echo "  3. Run: claude-mobile"
echo ""
```

### Manual Installation

```bash
# macOS
brew install ttyd tmux tailscale

# Linux (Debian/Ubuntu)
sudo apt install -y tmux
sudo snap install ttyd --classic
curl -fsSL https://tailscale.com/install.sh | sh
```

---

## Usage

### First Time Setup

```bash
# 1. Connect to Tailscale (one-time)
tailscale up
# Follow the link to authenticate with Google/GitHub/etc.

# 2. Install Tailscale on your phone
# iOS: App Store → Tailscale
# Android: Play Store → Tailscale
# Login with same account

# 3. Start Claude Code Mobile
claude-mobile
```

### Output

```
══════════════════════════════════
  CLAUDE CODE MOBILE
══════════════════════════════════
  URL:  http://100.78.42.15:7681
  User: claude
  Pass: claude123
══════════════════════════════════
```

### On Your Phone

1. Open Safari/Chrome
2. Go to `http://100.78.42.15:7681` (use your actual Tailscale IP)
3. Login with `claude` / `claude123`
4. You now have Claude Code in your browser

---

## Configuration

### Change Password

```bash
export CLAUDE_MOBILE_PASS="your-secure-password"
claude-mobile
```

Or add to your shell config:

```bash
echo 'export CLAUDE_MOBILE_PASS="your-secure-password"' >> ~/.zshrc
```

### Change Port

Edit `~/.local/bin/claude-mobile` and change `PORT=7681` to your preferred port.

---

## Security

| Layer | Protection |
|-------|------------|
| **Network** | Tailscale uses WireGuard encryption |
| **Authentication** | Basic auth (username:password) via ttyd |
| **Access** | Only accessible from your Tailscale network |

**Recommendations**:
- Use a strong password (not the default `claude123`)
- Don't expose ttyd directly to the internet without Tailscale
- Keep Tailscale client updated on all devices

---

## Troubleshooting

### "not connected" instead of IP

```bash
# Check Tailscale status
tailscale status

# If disconnected, reconnect
tailscale up
```

### Can't access from phone

1. Ensure Tailscale app is installed on phone and connected to same account
2. Check firewall isn't blocking port 7681
3. Try accessing locally first: `http://localhost:7681`

### Session not persisting

The tmux session should persist. To manually reattach:

```bash
tmux attach -t cc
```

### ttyd command not found

```bash
# macOS
brew reinstall ttyd

# Linux
sudo snap install ttyd --classic
```

---

## Alternatives Comparison

| Solution | Type | Pros | Cons | ToS | Stars |
|----------|------|------|------|-----|-------|
| **ttyd + Tailscale** ✅ | Self-hosted | Gratuit, max contrôle, CLI officiel | Setup manuel, UX terminal | ✅ Safe | N/A |
| [Happy Coder](https://github.com/slopus/happy) | App native | Voice, encryption, multi-instances, mobile-first | Dépendance projet tiers | ✅ Safe | 7.8K |
| [Remoto.sh](https://remoto.sh) | Cloud relay | Setup rapide, browser only | Cloud wrapping, latence, coût | ⚠️ Risk | N/A |
| tmux + SSH | Self-hosted | Zero deps, CLI officiel | Besoin client SSH mobile | ✅ Safe | N/A |
| [swe-mux](https://github.com/jatoran/swe-mux) | Self-hosted (PWA over Tailscale) | Official CLI in real PTYs, same live sessions on desktop and phone, per-session status, push notifications, dev-server previews, sessions survive restarts, no relay | Windows desktop app; macOS/Linux via browser; young project | ✅ Safe | N/A |

We chose ttyd + Tailscale because:
- It's just your terminal exposed via browser
- No third-party wrapper around Claude Code
- Zero ToS risk—you're using the official CLI

---

### Happy Coder - Alternative Recommandée

Si vous préférez une **app native** plutôt qu'un terminal web :

- **Repo** : [github.com/slopus/happy](https://github.com/slopus/happy)
- **Stars** : 7.8K (janvier 2026)
- **License** : MIT
- **Stack** : Tauri (desktop) + Expo (mobile)
- **Providers** : Claude Code, Codex, Gemini

**Pourquoi ToS-safe** : Happy Coder est un wrapper local qui exécute le CLI officiel via subprocess Node.js. Pas d'appels API directs, pas de proxy cloud.

**Installation** :
```bash
npm i -g happy-coder && happy
```

---

### Remoto.sh - Alternative Cloud (avec risques)

**Pourquoi risqué** : Remoto.sh utilise des conteneurs Docker cloud comme relay. Selon les ToS Anthropic (§4.2), les "proxies non autorisés qui masquent l'origine des requêtes" sont interdits. Des suspensions ont été signalées sur Reddit/HN pour usage similaire.

> **Recommandation** : Préférer Happy Coder ou ttyd+Tailscale pour éviter les risques ToS.

---

## Related Resources

- [ttyd GitHub](https://github.com/tsl0922/ttyd) - Terminal web server
- [Tailscale](https://tailscale.com/) - Zero-config VPN
- [ttyd + Claude Code Guide](https://aiengineerguide.com/blog/agentic-cli-browser-ttyd/) - Community tutorial
- [VPS Setup Guide](https://joshualent.com/snippets/claude-phone/) - Alternative: run on VPS

---

## Sources

- [Happy Coder GitHub](https://github.com/slopus/happy) - 7.8K ⭐, MIT license
- [ttyd GitHub](https://github.com/tsl0922/ttyd) - Terminal web server
- [Tailscale](https://tailscale.com/) - Zero-config VPN
- [Remoto.sh](https://remoto.sh) - Cloud terminal (ToS risk noted)
- ToS Anthropic §4.2 - Proxies non autorisés

---

## Contributing

This doc is **WIP/UNTESTED**. If you test this setup, please share:
- Your OS/environment
- Any issues encountered
- Suggested improvements

Open an issue or PR on this repo.

---

*Last updated: January 2026 | Status: WIP/UNTESTED | Data verified: Happy Coder 7.8K ⭐ (2026-01-19)*
