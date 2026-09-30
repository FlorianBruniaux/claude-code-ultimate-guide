---
name: autoresearch
description: "Autonomous improvement loop: scan codebase metrics, scaffold experiment files, run agent-driven iterations until metric improves"
argument-hint: "[--scaffold <loop-name>] [--run <loop-name>] [--status]"
effort: high
disable-model-invocation: true
---

# Autoresearch: Autonomous improvement loop

Scan codebase quality metrics, propose improvement loops, and run autonomous agent iterations. Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch), adapted from ML research to code quality.

**Concept**: The agent proposes a code change, runs the measurement, keeps the change if the metric improved, reverts via `git reset` if not, and repeats until manually stopped.

**Time**: Scan ~30s | Per iteration: depends on scope | Loop: runs indefinitely until you stop it

---

## Mode 1: Scan (default)

Measure current state, detect existing loops, propose next actions.

### Instructions

Run the following metrics and display a prioritized proposal table.

**Step 1: Measure codebase metrics**

Adapt grep patterns to your project's conventions. These are TypeScript defaults, adjust for your stack.

```bash
# M1: Function declarations (prefer arrow functions)
M1=$(grep -r "export function " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M2: Interface declarations (prefer type aliases)
M2=$(grep -r "export interface " src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M3: ESLint disables
M3=$(grep -r "eslint-disable" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M4: Type casts to any
M4=$(grep -r " as any" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')

# M5: TODO comments
M5=$(grep -r "// TODO" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null | wc -l | tr -d ' ')
```

**Step 2: Detect existing loops**

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  LOOP_NAME=$(basename "$dir")
  # Check if loop has results
  if [[ -f "$dir/results.tsv" ]]; then
    ITERS=$(wc -l < "$dir/results.tsv" | tr -d ' ')
    BEST=$(sort -t$'\t' -k2 -n "$dir/results.tsv" | head -1 | cut -f2)
    echo "ACTIVE:$LOOP_NAME:iterations=$ITERS:best=$BEST"
  else
    echo "SCAFFOLDED:$LOOP_NAME"
  fi
done
```

**Step 3: Display**

```
Autoresearch Scan: {date}

Codebase metrics:

| # | Loop              | Metric            | Current | Target | Priority | Risk |
|---|-------------------|-------------------|---------|--------|----------|------|
| A | loop-remove-as-any| `as any` casts    | {M4}    | 0      | P1       | LOW  |
| B | loop-eslint-disable| eslint-disable   | {M3}    | 0      | P2       | MED  |
| C | loop-export-fn    | export function   | {M1}    | 0      | P1       | LOW  |
| D | loop-interface-type| export interface | {M2}    | 0      | P1       | LOW  |
| E | loop-todo-comments| TODO comments     | {M5}    | 0      | P3       | LOW  |

Existing loops: {detected loops or "none yet"}

Recommended next step (P1, LOW risk):
  /autoresearch --scaffold loop-remove-as-any
  Then write program.md, create a worktree, and run the loop.
```

---

## Mode 2: `--scaffold <loop-name>`

Generate the 3 mechanical files for a loop. **Does not generate `program.md`**: write that yourself to encode project-specific constraints.

### Instructions

Create the following files under `scripts/autoresearch/{loop-name}/`:

**`measure.sh`**: the evaluation harness (single metric, returns an integer):

```bash
#!/usr/bin/env bash
# measure.sh: {loop-name}
# Returns an integer. Direction: lower = better (unless loop targets coverage/score).
set -euo pipefail
grep -r "PATTERN" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l | tr -d ' '
```

**`direction.txt`**: improvement direction:

```
lower
```

(Use `higher` for metrics like test coverage or quality score.)

**`files.txt`**: scope the agent should operate on:

```
src/
```

After creating the files, display:

```
Loop scaffolded: scripts/autoresearch/{loop-name}/

  measure.sh  : {pattern} in {scope} -> {N} occurrences today
  direction   : lower (fewer = better)
  files.txt   : src/

Current metric: {N} (target: 0)

Next steps:
  1. Write program.md -- agent behavior, constraints, what it can/cannot touch
     Reference: scripts/autoresearch/loop-remove-as-any/program.md
  2. Create a worktree: /worktree feature/autoresearch-{loop-name}
  3. cd into the worktree
  4. bash scripts/autoresearch/runner.sh {loop-name} 0 15
```

---

## Mode 3: `--run <loop-name>`

Execute the autonomous loop. The agent runs indefinitely: stop it manually when satisfied.

### Instructions

**Verify prerequisites:**

```bash
[ -f "scripts/autoresearch/{loop-name}/measure.sh" ] || { echo "ERROR: measure.sh missing. Run --scaffold first."; exit 1; }
[ -f "scripts/autoresearch/{loop-name}/program.md" ] || { echo "ERROR: program.md missing. Write it first, this encodes your constraints."; exit 1; }
```

**Run the loop:**

Read `scripts/autoresearch/{loop-name}/program.md` fully before starting. Then enter the following cycle, repeat until stopped:

```
LOOP ITERATION #{N}

1. Current metric: bash scripts/autoresearch/{loop-name}/measure.sh
2. Read program.md constraints
3. Propose ONE targeted change to files in files.txt
4. Apply the change
5. Re-measure: bash scripts/autoresearch/{loop-name}/measure.sh
6. Evaluate:
   - direction=lower AND new < previous -> KEEP (git add -p && git commit -m "autoresearch: {description}")
   - otherwise -> REVERT (git checkout -- .)
7. Log to results.tsv: {timestamp}\t{metric}\t{status}\t{description}
8. Continue to iteration #{N+1}
```

**Stopping criteria** (from program.md):
- Metric reaches target (e.g., 0)
- No more mechanical changes possible
- User manually stops the process

**Display each iteration:**

```
[iter #{N}] metric: {before} -> {after} | {KEPT/REVERTED} | {change description}
```

---

## Mode 4: `--status`

Show status of all loops in the project.

### Instructions

```bash
for dir in scripts/autoresearch/loop-*/; do
  [ -d "$dir" ] || continue
  NAME=$(basename "$dir")
  CURRENT=$(bash "$dir/measure.sh" 2>/dev/null || echo "?")
  ITERS=$([ -f "$dir/results.tsv" ] && wc -l < "$dir/results.tsv" | tr -d ' ' || echo "0")
  KEPT=$([ -f "$dir/results.tsv" ] && grep -c "KEPT" "$dir/results.tsv" || echo "0")
  echo "$NAME | current: $CURRENT | iters: $ITERS | kept: $KEPT"
done
```

Display:

```
Autoresearch Status

| Loop                | Current | Iterations | Kept | Status    |
|---------------------|---------|------------|------|-----------|
| loop-remove-as-any  | {N}     | {N}        | {N}  | ACTIVE    |
| loop-export-fn      | {N}     | 0          | 0    | SCAFFOLDED|
```

---

## Writing `program.md`: The most important file

`program.md` is the agent's behavior contract. Write it yourself, never auto-generate it. It must encode what the agent can/cannot touch for your specific codebase.

**Minimal structure:**

```markdown
# Program: {loop-name}

## Objective
Reduce `{metric}` in `src/` to 0. One mechanical change per iteration.

## Measurement
bash scripts/autoresearch/{loop-name}/measure.sh
Lower = better. Target: 0.

## What you CAN do
- Replace `export function X(` with `export const X = (`
- Keep the function signature identical

## What you CANNOT do
- Modify test files
- Change function signatures
- Touch files outside src/
- Make multiple changes per iteration

## Stop when
- Metric = 0
- No more mechanical replacements exist
```

---

## The pattern (background)

This command implements the **autoresearch loop** pattern from [karpathy/autoresearch](https://github.com/karpathy/autoresearch):

| ML Research (karpathy) | Code Quality (this command) |
|------------------------|----------------------------|
| Modify `train.py` | Modify `src/` files |
| Measure `val_bpb` | Measure grep count |
| 5-minute GPU budget | One atomic change per iteration |
| Keep if val_bpb improves | Keep if count decreases |
| `git reset` if not | `git checkout -- .` if not |
| `program.md` = agent skill | `program.md` = agent skill |

Key insight: a fixed, objective metric + git as rollback mechanism = safe autonomous iteration. The agent never needs human approval per-change because every bad change is automatically reverted.

---

## Usage

**Scan and propose loops:**
```
/autoresearch
```

**Scaffold files for a specific loop:**
```
/autoresearch --scaffold loop-remove-as-any
```

**Run the autonomous loop (after writing program.md):**
```
/autoresearch --run loop-remove-as-any
```

**Check status of all loops:**
```
/autoresearch --status
```

$ARGUMENTS
