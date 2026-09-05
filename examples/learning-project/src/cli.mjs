#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { verifyRelease } from "./release-verifier.mjs";

const [, , command, candidatePath] = process.argv;

if (command !== "verify" || !candidatePath) {
  console.error("Usage: proofpack verify <candidate.json>");
  process.exitCode = 2;
} else {
  try {
    const candidate = JSON.parse(await readFile(candidatePath, "utf8"));
    const report = verifyRelease(candidate);
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = report.ready ? 0 : 1;
  } catch (error) {
    console.error(`Invalid release candidate JSON: ${error.message}`);
    process.exitCode = 2;
  }
}
