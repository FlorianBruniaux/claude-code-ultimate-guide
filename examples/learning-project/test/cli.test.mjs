import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

const projectRoot = new URL("../", import.meta.url);
const cliPath = new URL("src/cli.mjs", projectRoot);
const readyFixture = new URL("fixtures/release-ready.json", projectRoot);
const incompleteFixture = new URL("fixtures/release-incomplete.json", projectRoot);
const malformedFixture = new URL("fixtures/release-malformed.json", projectRoot);

function runVerify(fixture) {
  return spawnSync(
    process.execPath,
    [cliPath.pathname, "verify", fixture.pathname],
    { encoding: "utf8" },
  );
}

test("verify exits successfully for a release with complete evidence", () => {
  const result = runVerify(readyFixture);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /"ready": true/);
});

test("verify reports every missing or failed required check", () => {
  const result = runVerify(incompleteFixture);

  assert.equal(result.status, 1, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), {
    name: "proofpack",
    version: "1.0.0",
    ready: false,
    problems: [
      "tests: evidence does not describe a retained result",
      "security: evidence does not describe a retained result",
      "security: expected status pass, received fail",
      "package: missing required check",
    ],
  });
});

test("verify rejects malformed JSON with a distinct input error", () => {
  const result = runVerify(malformedFixture);

  assert.equal(result.status, 2);
  assert.equal(result.stdout, "");
  assert.match(result.stderr, /^Invalid release candidate JSON:/);
});

test("verify rejects duplicate checks instead of accepting shadow evidence", () => {
  const duplicateFixture = new URL("fixtures/release-duplicate.json", projectRoot);
  const result = runVerify(duplicateFixture);

  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /tests: duplicate check/);
  assert.match(result.stdout, /tests: evidence is required/);
});

test("verify rejects a non-semantic release version", () => {
  const invalidVersionFixture = new URL(
    "fixtures/release-invalid-version.json",
    projectRoot,
  );
  const result = runVerify(invalidVersionFixture);

  assert.equal(result.status, 1, result.stderr);
  assert.match(result.stdout, /version: expected MAJOR\.MINOR\.PATCH/);
});
