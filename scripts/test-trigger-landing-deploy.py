#!/usr/bin/env python3
"""
Regression tests for .github/workflows/trigger-landing-deploy.yml.

Issue #78: the dispatch failed with HTTP 401 Bad credentials and the run gave no
indication of which half was broken — an absent secret and an expired one both
surface as 401, because an empty github-token sends an unauthenticated request.
The workflow now separates those two and maps each API failure to a message that
names the next action.

These tests are written to DISCRIMINATE. Asserting only that the shipped script
produces the right message would also pass against a script that emitted the same
message unconditionally, so every status assertion also checks that the other
branches were NOT taken, and the unknown-status case asserts a rethrow rather
than a swallow. A dispatch failure that exits green is the one outcome worse than
the 401, since the landing would then silently serve stale content.

  python3 scripts/test-trigger-landing-deploy.py

Exit code 0 = all pass, 1 = at least one failure.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "trigger-landing-deploy.yml"

failures = []
passes = 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
        print(f"  PASS  {name}")
    else:
        failures.append(name)
        print(f"  FAIL  {name}  {detail}")


doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
# YAML 1.1 parses a bare `on:` key as boolean True, so accept either spelling.
triggers = doc.get("on", doc.get(True))
steps = doc["jobs"]["trigger"]["steps"]


def find_step(fragment):
    """Locate a step by name fragment, or report a failure instead of crashing.

    The pre-fix workflow has no preflight step at all, so a bare next() raises
    StopIteration and the suite dies with a traceback before running anything.
    A test that cannot report WHICH expectation broke is close to useless when
    it fires in CI, so a missing step is a named failure and the dependent
    assertions are skipped."""
    return next((s for s in steps if fragment in s.get("name", "")), None)


preflight = find_step("Verify")
dispatch = find_step("Dispatch")
script = (dispatch or {}).get("with", {}).get("script", "")

# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------
print("Workflow structure")
check("push trigger on main is preserved",
      triggers.get("push", {}).get("branches") == ["main"])
check("push paths still cover guide/, machine-readable/, examples/",
      triggers.get("push", {}).get("paths")
      == ["guide/**", "machine-readable/**", "examples/**"])
check("workflow_dispatch allows re-verification after a rotation",
      "workflow_dispatch" in triggers)
check("job withholds GITHUB_TOKEN scopes (permissions: {})",
      doc.get("permissions") == {},
      f"(got {doc.get('permissions')!r})")
check("dispatch authenticates with LANDING_DEPLOY_TOKEN",
      (dispatch or {}).get("with", {}).get("github-token")
      == "${{ secrets.LANDING_DEPLOY_TOKEN }}")

# ---------------------------------------------------------------------------
# The secret must never reach the log.
#
# `echo "$TOKEN"`, `echo ${#TOKEN}` and `set -x` have all leaked credentials in
# real workflows. GitHub masks registered secrets, but masking is a backstop and
# does not survive transformations like base64 or per-character printing.
# ---------------------------------------------------------------------------
print("\nSecret hygiene")
check("workflow defines a credential preflight step", preflight is not None)
check("workflow defines a dispatch step", dispatch is not None)
run = preflight["run"] if preflight else ""
check("preflight reads the token from env, not inline interpolation",
      (preflight or {}).get("env", {}).get("LANDING_DEPLOY_TOKEN")
      == "${{ secrets.LANDING_DEPLOY_TOKEN }}")
check("preflight never echoes the token value",
      not re.search(r'echo[^\n]*\$\{?LANDING_DEPLOY_TOKEN', run),
      "(an echo of the token value was found)")
check("preflight never prints the token length",
      "${#LANDING_DEPLOY_TOKEN}" not in run)
check("preflight does not enable shell tracing",
      "set -x" not in run)
check("dispatch script never logs the token",
      "LANDING_DEPLOY_TOKEN" not in script or "core.info(`${" not in script)

# ---------------------------------------------------------------------------
# Preflight guard, executed for real.
# ---------------------------------------------------------------------------
print("\nPreflight guard (executed)")


def run_preflight(token_value):
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as fh:
        fh.write(run)
        path = fh.name
    return subprocess.run(["bash", path], capture_output=True, text=True,
                          env={"PATH": "/usr/bin:/bin", "LANDING_DEPLOY_TOKEN": token_value})


r_empty = run_preflight("")
check("empty secret exits non-zero", r_empty.returncode != 0,
      f"(exit={r_empty.returncode})")
check("empty secret emits a GitHub error annotation",
      "::error" in r_empty.stdout)
check("empty secret names the runbook",
      "landing-sync.md" in r_empty.stdout)

r_set = run_preflight("ghp_exampleTokenValueNotReal")
check("present secret exits zero", r_set.returncode == 0,
      f"(exit={r_set.returncode})")
check("present secret does not leak the value",
      "ghp_exampleTokenValueNotReal" not in r_set.stdout + r_set.stderr,
      "(the token value appeared in output)")

# ---------------------------------------------------------------------------
# Error mapping, executed for real in node against a mocked octokit.
# ---------------------------------------------------------------------------
print("\nDispatch error mapping (executed in node)")

HARNESS = r"""
const fs = require('fs')
const status = process.argv[2] === 'ok' ? null : Number(process.argv[2])
const resultPath = process.argv[3]
const out = { info: [], failed: [], rethrown: null, dispatched: null }
const core = {
  info: (m) => out.info.push(String(m)),
  setFailed: (m) => out.failed.push(String(m)),
}
const github = { rest: { actions: { createWorkflowDispatch: async (args) => {
  if (status !== null) { const e = new Error('mock'); e.status = status; throw e }
  out.dispatched = args
} } } }
const body = process.env.SCRIPT_BODY
const fn = new Function('github', 'core', `return (async () => { ${body} })()`)
fn(github, core)
  .catch((e) => { out.rethrown = { status: e.status, message: e.message } })
  // Written to a file, not stdout: a script under test may print to stdout
  // itself (the pre-fix one calls console.log), which would corrupt the result.
  .finally(() => { fs.writeFileSync(resultPath, JSON.stringify(out)) })
"""

with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
    fh.write(HARNESS)
    harness_path = fh.name


def run_script(status):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        result_path = fh.name
    r = subprocess.run(["node", harness_path, str(status), result_path],
                       capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin:/usr/local/bin",
                            "SCRIPT_BODY": script})
    try:
        return json.loads(Path(result_path).read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return {"info": [], "failed": [], "rethrown": None, "dispatched": None,
                "harness_error": (r.stderr or r.stdout)[:300]}


if not script:
    check("dispatch step exposes an inline script to test", False,
          "(no script found; error-mapping assertions skipped)")
    print(f"\n{passes} passed, {len(failures)} failed")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

def msg(result):
    """First setFailed message, or "" when the script failed to produce one.

    Indexing directly makes every message assertion raise IndexError against a
    script that does not fail the job at all — which is precisely the regression
    these tests exist to catch, so it has to read as a FAIL, not a crash."""
    return (result["failed"] or [""])[0]


ok = run_script("ok")
check("success dispatches deploy.yml on the landing main",
      ok["dispatched"] == {"owner": "FlorianBruniaux",
                           "repo": "claude-code-ultimate-guide-landing",
                           "workflow_id": "deploy.yml", "ref": "main"},
      f"(got {ok['dispatched']!r})")
check("success reports no failure", ok["failed"] == [])
check("success logs where to find the landing run",
      any("actions/workflows/deploy.yml" in m for m in ok["info"]))

r401 = run_script(401)
check("401 fails the job", len(r401["failed"]) == 1)
check("401 says the credential is expired or revoked",
      "expired or revoked" in msg(r401))
check("401 does not misreport a permission problem",
      "Forbidden" not in msg(r401) and "not found" not in msg(r401))
check("401 is not rethrown as an unhandled error", r401["rethrown"] is None)

r403 = run_script(403)
check("403 fails the job", len(r403["failed"]) == 1)
check("403 points at the missing Actions: write scope",
      "Actions: write" in msg(r403))
check("403 is distinguishable from 401",
      msg(r403) != msg(r401))

r404 = run_script(404)
check("404 fails the job", len(r404["failed"]) == 1)
check("404 explains fine-grained tokens report out-of-scope repos as 404",
      "fine-grained" in msg(r404))
check("404 is distinguishable from 403",
      msg(r404) != msg(r403))

r500 = run_script(500)
check("unknown status is rethrown, never swallowed",
      r500["rethrown"] is not None and r500["rethrown"]["status"] == 500,
      f"(got {r500['rethrown']!r})")
check("unknown status does not produce a misleading credential message",
      r500["failed"] == [], f"(got {r500['failed']!r})")

for name, result in (("401", r401), ("403", r403), ("404", r404)):
    check(f"{name} message names the runbook",
          "landing-sync.md" in msg(result))

print(f"\n{passes} passed, {len(failures)} failed")
if failures:
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
sys.exit(0)
