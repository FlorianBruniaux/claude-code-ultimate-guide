import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
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
  assert.equal(evidence.tests, "node --test: 10 passed");
  assert.equal(evidence.security, "release guard fixtures: 4 passed");
  assert.equal(
    evidence.package,
    "node --check and npm pack --dry-run: exit 0",
  );
  assert.match(proofLog, /10 of 10 tests/);
  assert.match(proofLog, /4 of 4 hook tests/);
  assert.match(proofLog, /validates JavaScript syntax and the npm manifest/);

  const settings = JSON.parse(
    readFileSync(new URL(".claude/settings.json", projectRoot), "utf8"),
  );
  const hook = settings.hooks.PreToolUse[0].hooks[0];
  assert.equal(hook.command, "node");
  assert.deepEqual(hook.args, [
    "$CLAUDE_PROJECT_DIR/.claude/hooks/release-guard.mjs",
  ]);
  assert.equal(hook.timeout, 5);

  const temporaryRoot = mkdtempSync(join(tmpdir(), "proofpack-package-check-"));
  try {
    const temporaryProject = join(temporaryRoot, "project");
    cpSync(fileURLToPath(projectRoot), temporaryProject, {
      recursive: true,
      filter: (source) => !source.includes("/.cache/"),
    });
    writeFileSync(join(temporaryProject, "src/cli.mjs"), "export const = ;\n");
    const invalidPackage = spawnSync("npm", ["run", "package:check"], {
      cwd: temporaryProject,
      encoding: "utf8",
    });
    assert.notEqual(
      invalidPackage.status,
      0,
      "package:check accepted invalid JavaScript",
    );
  } finally {
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});
