# MCP Server — Future Ideas

Tracked ideas that didn't make it into the current release. Implementation complexity varies; all are technically feasible with existing data.

---

## Tools

### `get_quiz(topic?, count?)`

Interactive quiz from `machine-readable/questions.json` (274 questions, already used by the landing site).

- `topic` (optional string): filter by topic (e.g. "hooks", "agents", "mcp")
- `count` (optional number, default 5, max 20): number of questions to return
- Returns questions with options, correct answer, and explanation
- Useful for learning validation, onboarding, and teaching workflows

**Data**: `machine-readable/questions.json` — not currently bundled in the package; would need bundling or GitHub fetch.

---

### `get_methodology(name)`

Step-by-step workflows for TDD, SDD, BDD from `guide/methodologies.md`.

- `name` (string): `tdd | sdd | bdd | all`
- Returns the workflow steps, when to use it, and example commands
- Useful for agents doing test-driven development or spec-driven design

**Data**: `guide/methodologies.md` — fetched on demand (already in section-reader infrastructure).

---

### `get_workflow(name)`

Step-by-step workflows from `guide/workflows/` directory.

- `name` (string): partial name match (e.g. "code-review", "refactor", "debug")
- Returns the workflow with steps, triggers, and example prompts
- Could list available workflows when no name provided

**Data**: `guide/workflows/*.md` — fetched on demand.

---

## Resources

### `claude-code-guide://diff`

Shows what changed between the bundled YAML index version and the live GitHub version.

- Fetch live `machine-readable/reference.yaml` from GitHub
- Diff against bundled version (entry count, new keys, changed values)
- Helps users know when the package is stale vs. the guide

**Complexity**: Medium — requires async resource handler + structured diffing.

---

## Prompts

### `security-review`

Dedicated security audit workflow prompt using the threat database.

- Guides the model through: check CVEs → check authors → check skills → check techniques
- Returns a structured security posture report
- Reuses `list_threats` and `get_threat` tools internally

**Dependency**: Requires `threats.ts` tools (already implemented in v1.1.0).

---

## Notes

- All ideas use data already in the repo — no new data sources needed
- `get_quiz` requires bundling `questions.json` (currently not in npm package)
- `get_methodology` and `get_workflow` are low-effort since section-reader already handles arbitrary file fetching
