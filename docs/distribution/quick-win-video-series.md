# Quick-Win Video Series

Four short French videos lead to one result each. Every episode ends on an observable check and points to a canonical guide page. The published description must use the `youtube-fr` attributed URL from [`distribution-channels.yaml`](../../machine-readable/distribution-channels.yaml).

## Episode 1: Your first verified fix

**Outcome:** the viewer completes a small repository change and saves the command that verifies it.

**Target length:** 3 to 5 minutes.

**Sequence:**

1. Open a real repository and state one narrow behavior to change.
2. Ask Claude Code to inspect the relevant files before editing.
3. Apply the smallest coherent change.
4. Run the repository's own test, type check, or linter.
5. Save the command, environment, result, and untested scope in [`TESTING.md`](../../examples/claude-md/TESTING.md).

**Observable check:** the proof record names an exact command and its exit result. A green command with no environment or coverage boundary is incomplete.

**Guide route:** [core workflow](../../guide/learning-path/02-core-loop.md) and [verification evidence](../resource-evaluations/best-of-n-verification-evidence.md).

**Research support:** the [Harness Engineering talk at AI Engineer World's Fair](https://youtube.com/watch?v=D_cw-k0F1DM&t=370s) discusses verification loops in an agent harness. This is practitioner evidence; the talk reports no controlled measurement of this guide.

## Episode 2: Skill, subagent, or MCP server

**Outcome:** the viewer chooses the smallest extension mechanism that matches the task.

**Target length:** 4 to 6 minutes.

**Sequence:**

1. Use a skill when the task needs reusable instructions and local assets.
2. Use a subagent when isolated context or parallel analysis changes the result.
3. Use an MCP server when Claude Code must call a durable external capability.
4. State the permissions, data boundary, and failure mode before installation.
5. Link the chosen component from the project's `CLAUDE.md` or navigation page.

**Observable check:** another contributor can find the component, state why it exists, and identify what it can access.

**Guide route:** [skills](../../guide/learning-path/05-skills.md), [subagents](../../guide/learning-path/04-agents.md), [MCP ecosystem](../../guide/ecosystem/mcp-servers-ecosystem.md), and [plugin distribution](../../guide/ecosystem/plugin-distribution.md).

## Episode 3: One safe hook

**Outcome:** the viewer adds a validation hook that blocks a known failure without hiding an unknown state.

**Target length:** 4 to 6 minutes.

**Sequence:**

1. Choose one event and one failure the hook can detect reliably.
2. Keep the input contract explicit and reject malformed input.
3. Return a distinct result for pass, fail, and unknown coverage.
4. Test a passing fixture, a failing fixture, and malformed input.
5. Record the hook path, hash, test commands, and uncovered runtime behavior.

**Observable check:** all three fixtures produce the documented result and the proof record keeps untested runtime behavior as `UNKNOWN`.

**Guide route:** [hooks module](../../guide/learning-path/06-hooks.md), [hooks examples](../../examples/hooks/README.md), and [production safety](../../guide/security/production-safety.md).

**Research support:** [Never Trust a Monkey](https://youtube.com/watch?v=uvnxEZfSr1g&t=529s) presents circular verification as a practical control. Its examples do not establish that one hook covers a production system.

## Episode 4: Compare candidates without fooling yourself

**Outcome:** the viewer runs a bounded Best-of-3 protocol and keeps evidence for every candidate.

**Target length:** 5 to 7 minutes.

**Sequence:**

1. Freeze the task, mandatory failures, rubric, candidate count, and checks.
2. Generate three candidates from the same contract in isolated contexts.
3. Score every declared candidate against the frozen rubric.
4. Select the highest passing candidate.
5. Verify it outside the generation context and preserve every score in the proof log.

**Observable check:** the record contains C-01, C-02, and C-03, including rejected candidates, plus the selected candidate's executable verification.

**Guide route:** [Best-of-N workflow](../../guide/workflows/best-of-n.md) and [installable Best-of-N skill](../../examples/skills/best-of-n/SKILL.md).

**Research support:** [Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) supports sampling several reasoning paths and selecting the most consistent answer on its evaluated tasks. It does not prove that generic self-review improves software changes. The [Stanford CS221 search lecture](https://youtube.com/watch?v=fPESauMaJYA&t=3076s) provides adjacent teaching material on Best-of-N search.

## Shared production checklist

- Show the real file, command, or check on screen.
- Display the canonical guide page before the closing frame.
- Put the attributed `youtube-fr` URL in the description.
- Add chapters and a transcript before publication.
- Keep claims within the cited paper or video's observed scope.
- After publication, record the date and 30-day measures in [`distribution-channels.yaml`](../../machine-readable/distribution-channels.yaml).

The [learning path slide deck](claude-code-learning-path-slides.pptx) supplies the shared visual narrative. The [distribution workflow](../workflows/guide-distribution.md) defines approval, localization, and measurement boundaries.
