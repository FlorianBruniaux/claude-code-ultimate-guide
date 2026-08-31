#!/usr/bin/env node

const input = await readStdin();
let decision;

try {
  const event = JSON.parse(input);
  if (event.tool_name !== "Bash" || typeof event.tool_input?.command !== "string") {
    throw new TypeError("expected a Bash command");
  }

  const command = event.tool_input.command
    .replace(/''|""/g, "")
    .replace(/\s+/g, " ")
    .trim();
  const publishesArtifact =
    (/\bnpm\b/i.test(command) && /\bpublish\b/i.test(command)) ||
    (/\bdocker\b/i.test(command) && /\bpush\b/i.test(command));

  decision = publishesArtifact
    ? deny("Run npm run verify and review evidence/PROOF-LOG.md before publishing.")
    : allow("Command does not publish or push an artifact.");
} catch (error) {
  decision = deny(`Hook input is malformed: ${error.message}`);
}

process.stdout.write(`${JSON.stringify(decision)}\n`);

function allow(reason) {
  return hookDecision("allow", reason);
}

function deny(reason) {
  return hookDecision("deny", reason);
}

function hookDecision(permissionDecision, permissionDecisionReason) {
  return {
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision,
      permissionDecisionReason,
    },
  };
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}
