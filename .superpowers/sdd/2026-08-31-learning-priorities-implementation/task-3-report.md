# Task 3 report: executable learning-path prototype

## Delivered

The implementation series on `codex/priority-learning` is:

1. `23be055`: initial dependency-free learning-path prototype.
2. `a491b3c`: independent-review remediation for state validation, atomic-save failure, third-party invocation, track mapping, and validator boundary.
3. `8e251e5`: exclusive concurrent `init`, revised self-assessment mapping, and exact `quick_validate.py` boundary.

Owned files committed:

- `examples/skills/learning-path/SKILL.md`
- `examples/skills/learning-path/README.md`
- `examples/skills/learning-path/assets/path.yaml`
- `examples/skills/learning-path/scripts/progress.py`
- `examples/skills/learning-path/tests/test_progress.py`

The skill exposes four tracks: Beginner, Practitioner, Production, and Maintainer. Its seven module definitions point to the existing learning-path guide pages and their exercise headings. `path.yaml` uses JSON syntax, a valid YAML subset, so the Python standard library can parse it without PyYAML.

The state is stored under the target project at `.claude/learning/claude-code-guide-progress.json`. The engine creates a profile without overwriting an existing state file, atomically persists JSON through a same-directory temporary file and `os.replace`, rejects corrupt JSON or invalid state shape, enforces prerequisites, and requires a non-empty evidence note for completion.

Review dates are exactly J+1, J+3, J+7, J+14, J+30, J+60, and J+90. The CLI provides `init`, `status`, `next`, `complete`, and `due` commands.

## Test-first evidence

The initial focused test run failed because `scripts/progress.py` did not exist. The failing error was `FileNotFoundError` for that file. The implementation was then added to satisfy the tests.

Focused test suite after implementation:

```text
python3 -m unittest -v examples/skills/learning-path/tests/test_progress.py

Ran 11 tests in 0.029s
OK
```

Covered behaviours:

1. New Beginner profile writes state outside the installed skill.
2. Atomic save leaves valid complete JSON and no temporary file.
3. An injected `os.replace` failure leaves the old state bytes intact and removes the temporary file.
4. Incomplete prerequisites block completion.
5. Blank evidence blocks completion.
6. Next-module selection returns the first unlocked module.
7. Review scheduling returns the seven required dates.
8. Corrupt JSON state fails closed.
9. Boolean version values, unknown tracks, unknown modules, and modules outside the selected track fail closed.
10. `status`, `next`, `due`, and `complete` reject corrupt state before executing.
11. Sixteen concurrent `init` attempts produce exactly one successful profile and fifteen rejected attempts.

## Independent-review remediation

- `_validate_state` now receives the trusted `path_data`. It requires `version` to be an actual integer, recognises only defined tracks, and accepts only known modules that belong to the selected track. It also rejects a completion record whose prerequisites are absent.
- Every state-reading CLI command loads and validates state against `path_data` before selecting, scheduling, completing, or reporting work.
- Skill commands now run through `${CLAUDE_SKILL_DIR}/scripts/progress.py` with `--root "$PWD"` before the subcommand. They therefore target the learner's third-party project rather than assuming this guide checkout.
- The self-assessment mapping initially made Maintainer a governance-only option; the final remediation removes it from assessment results entirely.
- The wording now says that completion requires a non-empty evidence note. It no longer implies that arbitrary evidence can be judged incomplete.
- The initial validator note is superseded below by the exact `quick_validate.py` frontmatter-validation boundary.

## Final-review remediation

- `init` no longer checks for an existing target before writing. It writes and fsyncs a same-directory temporary file, then publishes it with `os.link`. That primitive succeeds for exactly one contender and never overwrites an existing target. Every losing contender removes only its own temporary file.
- The concurrent test starts sixteen callers at a barrier and verifies one winner, fifteen rejected calls, and a readable final state.
- The self-assessment mapping now contains only Beginner, Intermediate, and Advanced. Maintainer is documented separately as a manual choice for a shared-governance objective.
- The validation boundary now names the actual `quick_validate.py` behaviour: it imports PyYAML before parsing the `SKILL.md` frontmatter. The system Python lacks PyYAML and raises `ModuleNotFoundError`, but the available pyenv Python runs this validator successfully.

## Additional verification

- Normal focused unit suite passed after the final commit: 11 tests in 0.029s.
- Isolated focused unit suite passed after the final commit with `python3 -I -B`: 11 tests in 0.029s.
- Python compilation passed with a temporary bytecode cache outside the worktree during the earlier remediation run.
- Relative Markdown links in the new SKILL and README resolved successfully.
- All seven exercise fragments resolve to headings in the existing guide pages.
- Third-party CLI smoke test passed with `CLAUDE_SKILL_DIR`: create profile, fetch the first module, record evidence, and list the first due review.
- `rg` found no em dash in the new prototype files.
- `git diff --check` passed before and after the final commit.
- `/Users/florianbruniaux/.pyenv/shims/python3 /Users/florianbruniaux/.codex/skills/.system/skill-creator/scripts/quick_validate.py examples/skills/learning-path` passed with `Skill is valid!`. The system Python invocation still exits at `import yaml` with `ModuleNotFoundError: No module named 'yaml'`. The dependency-free runtime also loaded the shipped JSON-compatible YAML definition during the test suite.

## Boundary and concern

The prototype intentionally records completion evidence but does not judge evidence quality or mark reviews as completed. Due reviews remain visible once their date has passed. Human or future product logic must decide whether a review was substantively performed. No network, package installation, guide edit, navigation update, catalog update, changelog update, version change, or external write was performed by the prototype.
