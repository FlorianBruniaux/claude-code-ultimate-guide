import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  cpSync,
  mkdtempSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const projectRoot = new URL("../", import.meta.url);

test("package:check rejects a package containing invalid JavaScript", () => {
  const temporaryRoot = mkdtempSync(join(tmpdir(), "proofpack-package-check-"));
  try {
    const temporaryProject = join(temporaryRoot, "project");
    cpSync(fileURLToPath(projectRoot), temporaryProject, {
      recursive: true,
      filter: (source) => !source.includes("/.cache/"),
    });
    writeFileSync(join(temporaryProject, "src/cli.mjs"), "export const = ;\n");

    const result = spawnSync("npm", ["run", "package:check"], {
      cwd: temporaryProject,
      encoding: "utf8",
    });

    assert.notEqual(result.status, 0, "package:check accepted invalid JavaScript");
    assert.match(result.stderr, /SyntaxError/);
  } finally {
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});
