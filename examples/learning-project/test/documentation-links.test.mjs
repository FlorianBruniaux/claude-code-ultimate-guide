import assert from "node:assert/strict";
import {
  existsSync,
  readFileSync,
  readdirSync,
} from "node:fs";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const projectRoot = new URL("../", import.meta.url);
const readme = new URL("README.md", projectRoot);

function markdownFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const url = new URL(entry.name, directory);
    if (entry.isDirectory()) {
      return markdownFiles(new URL(`${entry.name}/`, directory));
    }
    return entry.name.endsWith(".md") ? [url] : [];
  });
}

function isExternalLink(target) {
  return /^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith("//");
}

test("every relative Markdown link in the project resolves", () => {
  assert.equal(existsSync(readme), true, "README.md is missing");

  const links = markdownFiles(projectRoot).flatMap((source) => {
    const markdown = readFileSync(source, "utf8");
    return [...markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)]
      .map((match) => ({ source, target: match[1] }))
      .filter(({ target }) => !isExternalLink(target) && !target.startsWith("#"));
  });

  assert.ok(links.length >= 12, "README should connect stages to source material");

  for (const { source, target } of links) {
    const [path] = target.split("#", 1);
    const destination = new URL(path, source);
    assert.equal(
      existsSync(destination),
      true,
      `Broken README link: ${fileURLToPath(destination)}`,
    );
  }

  assert.equal(isExternalLink("notes/result:local.md"), false);

  const candidate = JSON.parse(
    readFileSync(new URL("fixtures/release-ready.json", projectRoot), "utf8"),
  );
  const evidence = Object.fromEntries(
    candidate.checks.map((check) => [check.name, check.evidence]),
  );
  const proofLog = readFileSync(
    new URL("evidence/PROOF-LOG.md", projectRoot),
    "utf8",
  );
  assert.equal(evidence.tests, "node --test: 11 passed");
  assert.equal(evidence.security, "release guard fixtures: 4 passed");
  assert.equal(
    evidence.package,
    "node --check and npm pack --dry-run: exit 0",
  );
  assert.match(proofLog, /11 of 11 tests/);
  assert.match(proofLog, /4 of 4 hook tests/);
  assert.match(proofLog, /validates JavaScript syntax and the npm manifest/);

  const settings = JSON.parse(
    readFileSync(new URL(".claude/settings.json", projectRoot), "utf8"),
  );
  const hook = settings.hooks.PreToolUse[0].hooks[0];
  assert.equal(hook.command, "node");
  assert.deepEqual(hook.args, [
    "${CLAUDE_PROJECT_DIR}/.claude/hooks/release-guard.mjs",
  ]);
  assert.equal(hook.timeout, 5);

  const skill = readFileSync(
    new URL(".claude/skills/verify-release/SKILL.md", projectRoot),
    "utf8",
  );
  assert.match(skill, /\$ARGUMENTS/);
  assert.doesNotMatch(skill, /\$\{ARGUMENTS/);
});
