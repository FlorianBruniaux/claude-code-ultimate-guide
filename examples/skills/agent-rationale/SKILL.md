---
name: agent-rationale
description: "Record why each hunk of an agent-written commit looks the way it does (intent, rejected alternative, risk, evidence, open question) in git notes under refs/notes/rationale, anchored by hunk hash, so a reviewer can read it beside the diff and see when a note went stale. Use after committing agent-written code that a human will review. Not for commit messages, PR descriptions or AI attribution metrics."
effort: low
---

# agent-rationale

Writes a short rationale for each hunk you changed into a git note on the commit, so the reviewer reads your reasons next to the code instead of reconstructing them. The note anchors to the hunk by a hash of its added lines; if the hunk changes later, `show` re-anchors the note by the annotated line's text or reports it as stale, never on the wrong line.

This is a template from the [Claude Code Ultimate Guide](https://cc.bruniaux.com/guide/), demonstrated by its own tests, not a measured improvement in review quality.

## Workflow

1. **Commit first.** Notes attach to a commit. Commit the change you want to explain. Done when `git log -1` shows it.

2. **One note per hunk a reviewer would question.** For each such hunk, pick one line inside it (a line number in the committed version of the file) and record:

   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/rationale.py add --file src/cart.py --line 42 \
     --intent "Sum prices, not item objects" \
     --rejected "Give Item an __add__ method" \
     --risk "Items without a price attribute now raise AttributeError" \
     --evidence "tests/test_cart.py::test_total_uses_price" \
     --open-question "unknown"
   ```

   - `--intent` is required. Write what the change is for, not what it does line by line.
   - `--rejected`: the alternative you considered and why you did not take it.
   - `--risk`: what this could break, for whom.
   - `--evidence`: the test, command or output that supports the change. Write `unknown` rather than invent one.
   - `--open-question`: what you could not decide and want the reviewer to answer. `unknown` is a valid answer for any field except intent.

   Done when the command prints `rationale recorded`. A line outside the commit's changes is refused.

3. **Check what the reviewer will see.**

   ```bash
   python3 -I ${CLAUDE_SKILL_DIR}/scripts/rationale.py show
   ```

   Each note is `[anchored]`, `[reanchored]` (the hunk changed but the annotated line is still there) or `[stale]` (the annotated line is gone; re-check before trusting the note). Done when every note you wrote shows as anchored.

## Keep notes through amend and rebase

Git moves notes on `git commit --amend` and `git rebase` only when told to. Once per repository:

```bash
git config notes.rewriteRef refs/notes/rationale
```

A `git merge --squash` and a squash done by the forge's merge button create a new commit without the note. Notes are not pushed by default: `git push origin refs/notes/rationale`.

## Rules

- Write the note from what you actually did and checked. A rationale is a claim the reviewer will check, not evidence by itself.
- Do not put secrets, credentials or customer data in a note: notes are pushed with the repository's refs.
- Never edit a note written by a human reviewer.
