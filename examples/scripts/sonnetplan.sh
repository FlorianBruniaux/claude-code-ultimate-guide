#!/usr/bin/env bash
# sonnetplan — Budget hybrid mode: Sonnet 4.6 (plan) + Haiku 4.5 (act)
#
# How it works:
#   Claude Code's `opusplan` alias routes to Opus (plan) + Sonnet (act).
#   By remapping the environment variables that resolve the `opus` and `sonnet`
#   aliases, we effectively create a cheaper Sonnet→Haiku hybrid.
#
# Usage:
#   sonnetplan                    # Start Claude in current directory
#   sonnetplan --project /path    # Start in specific project
#
# Installation:
#   Add this function to your ~/.zshrc or ~/.bashrc:
#
#     source /path/to/sonnetplan.sh
#
#   Or copy the function body directly into your shell config.
#
# Verification:
#   After running `sonnetplan` and typing `/model opusplan`, check the
#   status bar — it should show "Model: Sonnet 4.6" in plan mode.
#   Do NOT rely on asking the model "what model are you?" — that self-report
#   is unreliable. Use the status bar or your billing dashboard instead.
#
# GitHub issue tracking native support: https://github.com/anthropics/claude-code/issues/9749

sonnetplan() {
    ANTHROPIC_DEFAULT_OPUS_MODEL=claude-sonnet-4-6 \
    ANTHROPIC_DEFAULT_SONNET_MODEL=claude-haiku-4-5-20251001 \
    claude "$@"
}
