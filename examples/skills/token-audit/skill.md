---
name: token-audit
description: "Audit Claude Code configuration to measure fixed-context token overhead and produce a prioritized action plan. Use when hitting rate limits, experiencing early context compression, or after adding significant config files."
effort: medium
allowed-tools: Read Grep Glob Bash
---

# /token-audit: Context Token Audit

**Purpose**: Measure how many tokens your Claude Code configuration consumes before any user task begins. Identify the biggest sources of overhead. Produce a concrete action plan with savings estimates.

**When to use**:
- You're hitting rate limits before end of day
- Sessions feel slow or context compresses early
- You've added a lot of rules files and want to know the real cost
- After a major config change

---

## What You Will Measure

| Component | Loaded when | Typical range |
|-----------|-------------|---------------|
| `~/.claude/CLAUDE.md` + @imports | Always | 5-15K tokens |
| Project `CLAUDE.md` | Always | 2-8K tokens |
| `.claude/rules/*.md` | Always (all files) | 5-40K tokens |
| `MEMORY.md` | Always | 1-3K tokens |
| Claude Code system prompt | Always | ~7,500 tokens |
| Hook stdout | Per tool call | variable |
| Commands, agents, skills | On invocation only | 0 by default |

Key insight: `.claude/rules/` loads every `.md` file at session start, regardless of relevance. Commands and agents are lazy-loaded — they cost zero until invoked. Rules files are the most common source of unexpected overhead.

---

## Step 1 — Run the Measurement

Execute these commands from the project root:

```bash
# Component sizes
echo "=== PROJECT CLAUDE.md ===" && wc -c CLAUDE.md 2>/dev/null || echo "none"

echo ""
echo "=== RULES FILES (sorted by size) ===" && find .claude/rules -name "*.md" 2>/dev/null \
  | xargs wc -c 2>/dev/null | sort -rn | head -20

echo ""
echo "=== GLOBAL ~/.claude ===" && ls -la ~/.claude/*.md 2>/dev/null \
  | awk '{print $5, $9}' | sort -rn
```

Then calculate the full budget:

```bash
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
MEMORY=$(find ~/.claude/projects -name "MEMORY.md" 2>/dev/null \
  | xargs grep -l "$(basename $(pwd))" 2>/dev/null | head -1 \
  | xargs wc -c 2>/dev/null | awk '{print $1}' || echo 0)
TOTAL=$(( GLOBAL + PROJECT + RULES + MEMORY + 30000 ))

echo "Global ~/.claude   : ~$(( GLOBAL / 4 )) tokens ($(( GLOBAL / 1000 ))K chars)"
echo "Project CLAUDE.md  : ~$(( PROJECT / 4 )) tokens"
echo "Rules (auto-loaded): ~$(( RULES / 4 )) tokens"
echo "MEMORY.md          : ~$(( MEMORY / 4 )) tokens"
echo "System prompt      : ~7,500 tokens"
echo "---"
echo "TOTAL fixed context: ~$(( TOTAL / 4 )) tokens"
echo "% of 200K window   : $(( TOTAL / 4 * 100 / 200000 ))%"
```

---

## Step 2 — Classify Rules Files

For each file in `.claude/rules/`, classify it:

| Class | Definition | Action |
|-------|------------|--------|
| **ALWAYS** | Applies to most tasks (conventions, output format, safety) | Keep auto-loaded |
| **SOMETIMES** | Relevant in 20-40% of sessions | Keep if small (<3K chars); lazy-load if large |
| **RARELY** | Relevant in <10% of sessions (Figma, Windows, design system) | Remove from auto-load |
| **NEVER** | Outdated or covered elsewhere | Delete or archive |

Run this classification prompt:

```
Read every file in .claude/rules/. For each file, output a table row:

| File | Size (chars) | Class (ALWAYS/SOMETIMES/RARELY/NEVER) | Reasoning (one sentence) |

Sort by size descending within each class.
At the end, calculate: total chars that would leave the fixed context if all
RARELY and NEVER files were excluded. Convert to tokens (÷ 4).
```

---

## Step 3 — Audit Hook Overhead

Hooks on `PreToolUse` and `PostToolUse` fire on every tool call. Each invocation injects its stdout into context. A hook outputting 500 chars on 150 tool calls per session = 75K chars ≈ 19K extra tokens.

Check what you have:

```bash
# List hooks by event type
python3 - << 'EOF'
import json, os
for path in [os.path.expanduser("~/.claude/settings.json"), ".claude/settings.json"]:
    if not os.path.exists(path): continue
    print(f"\n--- {path} ---")
    data = json.load(open(path))
    for event, hooks in data.get("hooks", {}).items():
        for h in hooks:
            cmd = h.get("command", "?")
            matcher = h.get("matcher", "*")
            print(f"  [{event}] matcher={matcher} → {cmd[:80]}")
EOF
```

For each `PreToolUse` or `PostToolUse` hook, estimate its stdout size by running it manually. Multiply by your average tool call count per session (visible in `/cost` after a session).

**Red flags**:
- Hooks that `cat` files unconditionally
- `git status` or `git log` on every call
- Multi-line echo output for debugging that was never removed
- JSON blobs injected as context

---

## Step 4 — Build the Action Plan

Produce a prioritized table. Rule of thumb: only include actions achievable without external infrastructure (no RAG, no vector databases, no custom MCP servers).

| Action | Estimated token savings | Effort | Risk |
|--------|------------------------|--------|------|
| Remove RARELY files from auto-load | varies | 30 min | Low |
| Split large rules into core + detail | varies | 1-2h | Low |
| Trim hook stdout to essential fields | varies | 1h | Low |
| Compress verbose rules (see §8 context-engineering.md) | 20-30% of rules | 1-2h | Low |
| Archive outdated MEMORY.md entries | 500-1K tokens | 30 min | Low |

---

## Step 5 — The RAG Question

Lazy-loading via a vector database (RAG) is sometimes pitched as the solution. Assess it honestly before committing:

1. What fixed-context tokens remain after Steps 1-4? (Measure this first.)
2. Is RAG justified? A pgvector + custom MCP setup is a 1-2 week project.
3. Break-even: if you have 10 rules files averaging 3K chars each, classification (30 min) saves as much as RAG would. RAG earns its cost at 50+ rule files where intent-based routing is the only scalable solution.

---

## Output Format

After running the audit, produce this report:

```markdown
## Token Audit — [PROJECT] — [DATE]

### Budget Summary

| Component | Tokens | % of total |
|-----------|--------|------------|
| Global ~/.claude | X | Y% |
| Project CLAUDE.md | X | Y% |
| Rules (auto-loaded) | X | Y% |
| MEMORY.md | X | Y% |
| System prompt | 7,500 | Y% |
| **TOTAL** | **X** | **100%** |

Context window used before any task: X% of 200K

### Rules Classification

| File | Chars | Class | Action |
|------|-------|-------|--------|
| ... | ... | ALWAYS/SOMETIMES/RARELY | keep/lazy-load/remove |

### Hook Overhead

| Hook | Event | Est. stdout | Calls/session | Total tokens/session |
|------|-------|-------------|---------------|----------------------|
| ... | PreToolUse | X chars | ~Y | ~Z tokens |

### Action Plan

| Action | Savings | Effort | Risk |
|--------|---------|--------|------|
| ... | -X tokens | 30 min | Low |

**Total achievable without infrastructure**: -X tokens → from Y to Z (N% reduction)

### RAG Verdict

[One paragraph: remaining overhead after action plan, whether RAG is justified,
estimated setup cost vs savings.]
```

---

## Interpreting Results

| Fixed context | Assessment |
|---------------|------------|
| < 20K tokens | Healthy — no urgent action needed |
| 20-40K tokens | Moderate — run the classification pass, grab easy wins |
| 40-60K tokens | High — rules audit is worth an afternoon |
| > 60K tokens | Critical — you are burning 30%+ of your window before any task |

A 48% reduction is typical after a first-pass audit on a heavily configured project, with no infrastructure changes — just removing the RARELY-used files from auto-load.
