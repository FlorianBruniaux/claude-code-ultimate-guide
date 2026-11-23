---
description: Install or update ccboard
disable-model-invocation: true
---

# Install ccboard

Install the binary with one of these methods. Ask which one the user prefers before running anything.

```bash
brew tap FlorianBruniaux/tap && brew install ccboard    # includes the web frontend
cargo install ccboard                                   # needs Rust 1.85+, no web frontend
bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-ccboard.sh" # cargo install with an update prompt
```

If Rust is missing, install it from https://rustup.rs first. After installing, check with `ccboard --version`.

Troubleshooting:

- `cargo: command not found`: install Rust, then `source "$HOME/.cargo/env"`.
- Build fails: `rustup update`, then retry.
- `ccboard: command not found` after install: add `$HOME/.cargo/bin` to `PATH`.

Remove with `cargo uninstall ccboard` or `brew uninstall ccboard`.
