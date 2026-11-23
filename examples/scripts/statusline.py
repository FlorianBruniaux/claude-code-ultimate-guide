#!/usr/bin/env python3
"""
Claude Code custom status line script.

Reads session JSON from stdin (piped by Claude Code) and prints a two-line
status bar showing context window usage, git branch, and model name.

Usage (settings.json):
    "statusLine": {"type": "command", "command": "python3 /path/to/statusline.py"}

Output format:
    ####--------------------------------------  18%   (context bar)
    my-project | main | Sonnet 5.5 | 31K/168K

The 32K output buffer subtraction
----------------------------------
Claude Code reports context_window_size as the *total* window (e.g. 200,000
for a 200K-context model, 1,000,000 for a 1M-context model). This script
assumes Claude reserves ~32,000 tokens for its own output. That figure is a
heuristic, not a documented constant. The effective *input* window is then:

    effective_window = total_window - 32_000

If you omit this subtraction, the bar shows 16% when you are actually at
19% of usable space — a meaningful difference when you are approaching the
compact threshold. Packmind chose the 32K figure empirically. Treat it, and
the 200,000 fallback used below when the field is missing, as adjustable
defaults (current models can report a 1M window).

Adapted from Packmind's .claude/statusline.py (Apache 2.0).
See guide/core/skill-design-patterns.md for the full pattern context.
"""

import json
import sys
import subprocess
import os

# ANSI color codes for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# Output buffer Claude reserves for its own response tokens.
# Subtract from total_window to get the effective input window.
OUTPUT_BUFFER = 32_000


def get_color(pct: int) -> str:
    """Return a terminal color based on context usage percentage."""
    if pct < 20:
        return GREEN
    elif pct <= 40:
        return YELLOW
    else:
        return RED


def make_bar(pct: int, width: int = 50) -> str:
    """Render a text progress bar for the given percentage (0-100)."""
    filled = int(pct * width / 100)
    empty = width - filled
    return "#" * filled + "-" * empty


def get_git_branch(cwd: str) -> str:
    """Return the current git branch for the given directory, or 'no-git'."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip() if result.returncode == 0 else "no-git"
    except Exception:
        return "no-git"


def main() -> None:
    try:
        data = json.load(sys.stdin)

        # Folder name from workspace current_dir
        cwd = data.get("workspace", {}).get("current_dir", "")
        folder = os.path.basename(cwd) if cwd else "?"

        git_branch = get_git_branch(cwd)

        # Model display name (e.g. "Sonnet 5.5")
        model = data.get("model", {}).get("display_name", "?")

        # Context window usage
        # context_window_size = total window (including output buffer)
        # We subtract OUTPUT_BUFFER to get the effective input window.
        usage = data.get("context_window", {}).get("current_usage")
        total_window = data.get("context_window", {}).get("context_window_size", 200_000)
        effective_window = total_window - OUTPUT_BUFFER

        if usage and effective_window:
            input_tokens = usage.get("input_tokens", 0)
            cache_creation = usage.get("cache_creation_input_tokens", 0)
            cache_read = usage.get("cache_read_input_tokens", 0)

            # Total tokens currently occupying the input window
            current = input_tokens + cache_creation + cache_read
            pct = int(current * 100 / effective_window) if effective_window else 0

            color = get_color(pct)
            bar = make_bar(pct)
            line1 = f"{color}{bar} {pct}%{RESET}"
            line2 = f"{folder} | {git_branch} | {model} | {current // 1000}K/{effective_window // 1000}K"
        else:
            line1 = f"{GREEN}{make_bar(0)} 0%{RESET}"
            line2 = f"{folder} | {git_branch} | {model}"

        # Claude Code expects a single print to stdout — no trailing newline
        print(f"{line1}\n{line2}", end="")

    except Exception as e:
        print(f"error: {e}", end="")


if __name__ == "__main__":
    main()
