import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

const projectRoot = new URL("../", import.meta.url);
const hookPath = new URL(".claude/hooks/release-guard.mjs", projectRoot);

function runHook(fixtureName) {
  const fixture = new URL(
    `.claude/hooks/fixtures/${fixtureName}`,
    projectRoot,
  );
  return spawnSync(process.execPath, [hookPath.pathname], {
    encoding: "utf8",
    input: readFileSync(fixture, "utf8"),
  });
}

test("the guard allows a local test command", () => {
  const result = runHook("pass.json");

  assert.equal(result.status, 0, result.stderr);
  assert.equal(
    JSON.parse(result.stdout).hookSpecificOutput.permissionDecision,
    "allow",
  );
});

test("the guard denies a publishing command", () => {
  const result = runHook("fail.json");
  const decision = JSON.parse(result.stdout).hookSpecificOutput;

  assert.equal(result.status, 0, result.stderr);
  assert.equal(decision.permissionDecision, "deny");
  assert.match(decision.permissionDecisionReason, /npm run verify/);
});

test("the guard denies a container push", () => {
  const result = runHook("docker-push.json");
  const decision = JSON.parse(result.stdout).hookSpecificOutput;

  assert.equal(result.status, 0, result.stderr);
  assert.equal(decision.permissionDecision, "deny");
});

test("the guard fails closed when hook input is malformed", () => {
  const result = runHook("malformed.json");
  const decision = JSON.parse(result.stdout).hookSpecificOutput;

  assert.equal(result.status, 0, result.stderr);
  assert.equal(decision.permissionDecision, "deny");
  assert.match(decision.permissionDecisionReason, /malformed/i);
});
