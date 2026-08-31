# Module 06: Hooks and Events

**Time:** 1 hour | **Complexity:** Intermediate

**Previous:** [Module 05: Skills and Automation](05-skills.md)

## Goal

Add one Claude Code hook that makes a tool decision from structured input, fails closed on malformed input, and can be tested without starting an interactive session.

Claude Code hooks are not Git hooks. Git hooks respond to repository actions such as `pre-commit`. Claude Code hooks respond to Claude Code lifecycle and tool events such as `PreToolUse`, `PostToolUse`, and `SessionStart`.

## What you will learn

- where Claude Code reads hook configuration;
- how matchers select tool calls;
- what a command hook receives on standard input;
- how a `PreToolUse` hook allows or denies a call;
- what exit codes do and do not prove;
- how to test the decision script with fixed fixtures.

For the complete event matrix, use the [Hooks Events Reference](../core/hooks-events-reference.md). Anthropic maintains the authoritative [hooks documentation](https://code.claude.com/docs/en/hooks).

## The hook boundary

A command hook is a local program launched by Claude Code. It receives one JSON object on standard input. The fields depend on the event. For `PreToolUse`, the useful fields include `tool_name`, `tool_input`, and `tool_use_id`.

The matcher for a tool event filters on `tool_name`:

```text
Claude proposes Write or Edit
             |
             v
PreToolUse matcher selects the hook
             |
             v
Hook reads JSON and returns deny or no decision
             |
             v
Claude Code applies the decision
```

Keep the decision narrow. A path policy can decide whether a proposed file write targets a protected location. It cannot prove that the resulting program is secure or correct.

## Register a `PreToolUse` hook

Project hooks belong in `.claude/settings.json`. The following entry runs one Python command for `Write` and `Edit` calls:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-paths.py"],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

`settings.json` is the supported configuration file in this example. A `settings.yaml` variant is not part of this contract.

## Build the decision script

Save this file as `.claude/hooks/protect-paths.py`:

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import PurePosixPath


def decide(value: str, reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": value,
            "permissionDecisionReason": reason,
        }
    }))


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, UnicodeDecodeError):
    decide("deny", "Hook input was not valid JSON.")
    raise SystemExit(0)

if payload.get("tool_name") not in {"Write", "Edit"}:
    decide("deny", "Unexpected tool for this matcher.")
    raise SystemExit(0)

file_path = payload.get("tool_input", {}).get("file_path")
if not isinstance(file_path, str) or not file_path.strip():
    decide("deny", "Write or Edit input did not contain a file_path.")
    raise SystemExit(0)

path = PurePosixPath(file_path.replace("\\", "/"))
protected = (
    ".git" in path.parts
    or path.name == ".env"
    or path.name.startswith(".env.")
    or path.suffix in {".key", ".pem"}
)

if protected:
    decide("deny", f"Protected path: {file_path}")
else:
    raise SystemExit(0)
```

This example returns a structured decision only when it denies the call. Exit code `0` with no output leaves the normal Claude Code permission flow in place; it does not grant permission. Malformed or incomplete input is denied because the script cannot establish a safe path.

## Test three fixtures

Run the decision script directly:

```bash
printf '%s\n' '{"tool_name":"Write","tool_input":{"file_path":"src/app.py"}}' \
  | python3 .claude/hooks/protect-paths.py

printf '%s\n' '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' \
  | python3 .claude/hooks/protect-paths.py

printf '%s\n' '{bad json' \
  | python3 .claude/hooks/protect-paths.py
```

Expected decisions:

| Fixture | Expected result | Reason |
| --- | --- | --- |
| `src/app.py` | Exit `0`, no output | The path is outside the protected set, so normal permission flow continues |
| `.env` | `deny` | The policy names the path explicitly |
| malformed JSON | `deny` | The hook cannot validate the request |

These fixture tests verify the script's local input and output contract. They do not verify that the project settings were loaded by Claude Code. Confirm runtime loading separately by attempting a harmless write and a protected write in a disposable fixture project.

## Exit codes

Exit codes are event-dependent:

- exit code `0` means the hook command completed; Claude Code then parses any supported JSON output;
- exit code `2` blocks events that support blocking, including `PreToolUse`, and sends standard error back to Claude;
- other non-zero exit codes generally report a non-blocking hook error;
- `WorktreeCreate` is an exception because any non-zero exit fails creation;
- some events ignore exit codes or use a structured JSON decision instead.

Do not import Unix conventions blindly. Exit code `1` does not block a `PreToolUse` call. The [event reference](../core/hooks-events-reference.md#exit-code-2-behavior-per-event) records the behavior for every supported event.

## Safe design rules

- Keep the matcher as narrow as the policy.
- Parse input explicitly and reject unknown shapes when safety depends on them.
- Avoid network calls in a blocking hook.
- Keep secrets out of hook output and debug logs.
- Prefer read-only validation over hidden file mutation.
- Set a timeout.
- Test pass, deny, and malformed fixtures.
- Record what runtime behavior remains untested.

Hooks execute local code with the permissions of the Claude Code process. Review a shared hook before enabling it. For threat modeling and startup execution risks, read [Security Hardening](../security/security-hardening.md#16-startup-hooks-code-execution-before-your-first-prompt) and [Production Safety](../security/production-safety.md).

## Exercise: create a validation hook

1. Add the `PreToolUse` registration to `.claude/settings.json` in a disposable project.
2. Save the decision script at `.claude/hooks/protect-paths.py`.
3. Run the three fixtures and retain their JSON outputs.
4. Start Claude Code in the fixture project.
5. Request a write to `src/app.py` and confirm that the decision permits it.
6. Request a write to `.env` and confirm that the decision denies it.
7. Record the Claude Code version, settings path, command, result, and untested scope.

The exercise is complete when the three direct fixtures match the table and the two disposable runtime probes match the declared decisions. If runtime loading was not tested, record it as `UNKNOWN` rather than inferring it from the direct script tests.

## You are ready when

- you can distinguish Claude Code hooks from Git hooks;
- you can name the event and matcher used by your hook;
- your hook reads JSON from standard input;
- malformed input has an explicit outcome;
- you know that exit code `1` does not block `PreToolUse`;
- your proof separates script tests from Claude Code runtime loading.

## What comes next

[Module 07: Advanced Patterns](07-advanced.md) combines hooks, skills, agents, and verification into larger workflows.
