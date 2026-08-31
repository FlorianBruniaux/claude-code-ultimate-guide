import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync } from "node:fs";
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

test("every relative Markdown link in the project resolves", () => {
  assert.equal(existsSync(readme), true, "README.md is missing");

  const links = markdownFiles(projectRoot).flatMap((source) => {
    const markdown = readFileSync(source, "utf8");
    return [...markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)]
      .map((match) => ({ source, target: match[1] }))
      .filter(({ target }) => !target.includes(":") && !target.startsWith("#"));
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
});
