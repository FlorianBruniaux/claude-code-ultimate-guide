const REQUIRED_CHECKS = ["tests", "security", "package"];

export function verifyRelease(candidate) {
  const problems = [];
  const checksByName = new Map();

  for (const check of candidate.checks ?? []) {
    if (checksByName.has(check.name)) {
      problems.push(`${check.name}: duplicate check`);
    } else {
      checksByName.set(check.name, check);
    }

    if (!check.evidence?.trim()) {
      problems.push(`${check.name}: evidence is required`);
    } else if (
      /\b(?:unknown|failed|not executed|not run|unverified)\b|no retained output/i.test(
        check.evidence,
      )
    ) {
      problems.push(`${check.name}: evidence does not describe a retained result`);
    }
  }

  if (!/^\d+\.\d+\.\d+$/.test(candidate.version ?? "")) {
    problems.push("version: expected MAJOR.MINOR.PATCH");
  }

  for (const name of REQUIRED_CHECKS) {
    const check = checksByName.get(name);
    if (!check) {
      problems.push(`${name}: missing required check`);
    } else if (check.status !== "pass") {
      problems.push(`${name}: expected status pass, received ${check.status}`);
    }
  }

  return {
    name: candidate.name,
    version: candidate.version,
    ready: problems.length === 0,
    problems,
  };
}
