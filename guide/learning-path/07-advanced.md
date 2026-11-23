---
title: "Module 07: Advanced Patterns"
description: "Learning Path Module 07: orchestrate multi-agent Claude Code workflows, handle error recovery, and apply production-grade automation patterns for team workflows. 2-3 hours, advanced."
---

# Module 07: Advanced patterns

**Time**: 2-3 hours | **Complexity**: ⭐⭐⭐ Advanced

## Goal

Orchestrate multi-agent workflows. Build complex automation that coordinates multiple specialized agents.

---

## What you'll learn

- Multi-agent architecture patterns
- Orchestration strategies
- Error handling and recovery
- Production-grade automation
- Team workflows
- Real-world scenarios

---

## Multi-agent systems

A **multi-agent system** is when multiple specialized agents work together on one goal.

Before choosing a team pattern, separate the layers: the model produces tokens, a runtime harness owns a session's model-and-tool loop, the repository harness supplies instructions and verification, and an orchestrator coordinates sessions. [Agent Harness Engineering](../core/agent-harness.md) explains that model; the [Agent Harness Map](../ecosystem/agent-harness-landscape.md) compares loop-owning runtimes and keeps the broader directory separate. Use [Agent Tools: Beyond Claude Code](../ecosystem/agentic-tools.md) for frameworks and control planes, the [glossary](../core/glossary.md) for terms, [Agent Evaluation](../roles/agent-evaluation.md) to score the result, [Session Observability](../ops/observability.md) to inspect execution, and [Security Hardening](../security/security-hardening.md) before running work unattended.

### Example: Code release workflow

Instead of one Claude handling everything:

```
You: "Release version 3.5.0"
    ↓
    ├─→ [Version Agent] Updates VERSION file
    │
    ├─→ [Changelog Agent] Creates release notes
    │
    ├─→ [Test Agent] Runs full test suite
    │
    ├─→ [Security Agent] Security audit
    │
    ├─→ [Docs Agent] Updates documentation
    │
    └─→ [Release Agent] Tags, builds, publishes

Result: Complete, tested, documented release
```

Each agent is fast at its specialized task.

---

## Orchestration patterns

### Pattern 1: Sequential (pipeline)

Agents run one after another. Output of agent N becomes input to agent N+1.

```
Input
  ↓
[Agent 1: Parse Requirements] → Output: structured requirements
  ↓
[Agent 2: Design Schema] → Output: database schema
  ↓
[Agent 3: Generate Code] → Output: code skeleton
  ↓
[Agent 4: Write Tests] → Output: test suite
  ↓
Final Result
```

**When to use**: Workflows where each step depends on the previous.

**Example**:
```text
Use the requirements-parser subagent to parse the feature request into specifications

# Later, once we have specifications:
Use the database-designer subagent to design the schema based on these specs

# Once schema is approved:
Use the code-generator subagent to generate models based on the schema
```

### Pattern 2: Parallel (fork-join)

Multiple agents work simultaneously, results combined.

```
         Input
           ↓
    ┌──────┼──────┐
    ↓      ↓      ↓
 [Unit   [Int.  [Sec.
  Tests] Tests] Audit]
    ↓      ↓      ↓
    └──────┼──────┘
           ↓
      Combine Results
           ↓
      Final Report
```

**When to use**: Independent checks or tasks.

**Example**:
```
Request: "Review my code changes using separate subagents for quality, security, test coverage and performance, in parallel"

Parallel tasks:
- Code quality agent reviews
- Security agent scans
- Test coverage agent checks
- Performance agent analyzes

(Claude can start independent subagents at the same time, and each works in its own context window)

Results combined into one report
```

### Pattern 3: Conditional (if-then)

Route to different agents based on conditions.

```
Input: "Fix the bug"
  ↓
[Analyzer: Is it security?]
  ├─ YES → [Security Agent]
  ├─ PERFORMANCE → [Performance Agent]
  └─ LOGIC → [Logic Agent]
  ↓
Result
```

**Example**:
```text
Use the bug-classifier subagent to categorize this bug: security, performance, or logic

# Based on response:
# If security:
Use the security-patcher subagent to fix the security vulnerability

# If performance:
Use the perf-optimizer subagent to optimize this code
```

---

## Building a release workflow

### Scenario

You want to automate your release process. Right now you:
1. Update VERSION file
2. Update CHANGELOG
3. Run tests
4. Run security scan
5. Create git tag
6. Push to origin
7. Deploy to staging

### Solution: Multi-Agent workflow

**Step 1: Create agents** (each specializes in one task)

`.claude/agents/version-manager.md`:
```markdown
---
name: version-manager
description: Manages version files and tags
tools: Read, Edit, Write, Bash
---

# Version Manager

## Purpose
Update VERSION files and create git tags locally. Never push: the release-publisher step owns publishing.

(The `tools` list does not stop `git push`, because `Bash` runs any command. Enforce "no push" outside the prompt: a `permissions.deny` rule such as `Bash(git push *)` in settings, or a `PreToolUse` hook, and scope it to the agents that must not publish.)

## Tasks
- Bump version (patch, minor, major)
- Update VERSION file
- Update version in package.json, pyproject.toml, etc
- Create annotated git tags
```

`.claude/agents/changelog-generator.md`:
```markdown
---
name: changelog-generator
description: Generates release notes
---

# Changelog Generator

## Purpose
Create readable release notes from commits

## Output Format
- Version header
- Breaking changes (if any)
- New features
- Bug fixes
- Deprecations
```

`.claude/agents/test-validator.md`:
```markdown
---
name: test-validator
description: Runs full test suite
---

# Test Validator

## Purpose
Execute all tests and verify coverage

## Minimum Requirements
- All tests pass
- Coverage >80%
- No flaky tests
```

`.claude/agents/release-publisher.md`:
```markdown
---
name: release-publisher
description: Publishes and deploys
---

# Release Publisher

## Purpose
Tag and push to origin

## Steps
1. Create git tag
2. Push to origin
3. Trigger CI/CD pipeline
4. Monitor deployment
```

**Step 2: Create a release workflow skill**

Custom commands are now skills: a folder under `.claude/skills/` whose name becomes the slash command. (Existing `.claude/commands/<name>.md` files keep working.)

`.claude/skills/release-workflow/SKILL.md`:
```markdown
---
name: release-workflow
description: Orchestrate a complete release process
disable-model-invocation: true
---

Orchestrate a complete release. The bump type is: $ARGUMENTS (patch, minor or major).

## Process

1. Validate release readiness
2. Update version (version-manager subagent)
3. Generate changelog (changelog-generator subagent)
4. Run tests (test-validator subagent)
5. Security scan (security-auditor subagent)
6. Publish and deploy (release-publisher subagent), only after I confirm

## Requirements
- All tests passing
- No outstanding security issues
- Changelog updated
```

`disable-model-invocation: true` keeps Claude from starting a release on its own: only you can type `/release-workflow`.

**Step 3: Use the workflow**

```bash
/release-workflow patch
```

Claude then:
1. Delegates to version-manager → updates VERSION
2. Delegates to changelog-generator → creates release notes
3. Delegates to test-validator → verifies tests pass
4. Delegates to security-auditor → scans for vulnerabilities
5. Delegates to release-publisher → creates tag, pushes (after your confirmation)
6. You review the result of each step

The step order here is guidance to the model, not a guarantee. If a gate must never be skipped (for example "no push before tests pass"), enforce it in a script, hook or CI job.

---

## Error handling in multi-agent systems

### Pattern: Graceful degradation

If one agent fails, others continue:

```
[Test Agent] ❌ FAILED: 3 test failures
  ↓
[Security Agent] ✅ PASSED: No vulnerabilities
  ↓
[Docs Agent] ✅ PASSED: Docs updated
  ↓
[Aggregate Results]
  ⚠️  Release blocked (tests failed)
  ✅ Security passed
  ✅ Docs ready
  [Instructions to fix tests first]
```

### Pattern: Retry on failure

For transient failures (network, timeouts), retry the real check from a script. Slash commands cannot be called from a bash script; the script runs the actual command (here `npm test`) and uses `claude -p` only when you want Claude's judgment:

```bash
#!/bin/bash
# Release helper script (not a hook)

max_retries=3
retry=0

while [ $retry -lt $max_retries ]; do
  if npm test; then
    echo "✅ Tests passed"
    exit 0
  fi
  
  retry=$((retry + 1))
  if [ $retry -lt $max_retries ]; then
    echo "⚠️  Retry $retry/$max_retries"
    sleep 5
  fi
done

echo "❌ Tests failed after $max_retries attempts"
claude -p "Use the test-validator subagent to summarize why the tests keep failing" || true
exit 1
```

Gate on the real command's exit code. The exit code of `claude -p` says whether Claude ran, not whether your tests passed.

### Pattern: Rollback on error

If something goes wrong, undo only what the release created:

```bash
#!/bin/bash
# Rollback helper (script, not a hook)

START_SHA=$(git rev-parse HEAD)
NEW_TAG=""

cleanup_and_exit() {
  echo "Rolling back..."
  # Discard uncommitted release edits, keep unrelated work intact
  git restore VERSION CHANGELOG.md
  # Remove the tag only if this run created it
  [ -n "$NEW_TAG" ] && git tag -d "$NEW_TAG"
  # Undo a release commit made by this run (history is kept, nothing is force-reset)
  [ "$(git rev-parse HEAD)" != "$START_SHA" ] && git revert --no-edit "$START_SHA"..HEAD
  exit 1
}

# Run release steps (non-interactive Claude call for the bump, real commands for the checks)
if ! claude -p "Use the version-manager subagent to bump the patch version"; then
  cleanup_and_exit
fi

if ! npm test; then
  cleanup_and_exit
fi

# If we get here, release succeeded
exit 0
```

Avoid `git reset --hard` in a rollback helper: it also discards unrelated uncommitted work.

---

## Production patterns

### Pattern 1: Staged rollout

Release to different environments progressively:

```
/release major
  ↓
[Dev] Deploy and test
  ✅ Verified
  ↓
[Staging] Deploy and test
  ✅ Verified
  ↓
[Prod] Deploy with monitoring
  ✅ Monitoring green
  ↓
Release Complete
```

### Pattern 2: Approval gates

Block advancement until reviewed. A hook cannot prompt in the terminal: its standard input carries JSON, not your keyboard. Use a `PreToolUse` hook to make Claude Code ask you instead.

`.claude/hooks/pre-prod-deploy.sh`:
```bash
#!/bin/bash
# Ask for confirmation before any production deploy command
input=$(cat)
command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')

case "$command" in
  *"deploy --env prod"*)
    jq -n '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask", permissionDecisionReason: "Production deploy: confirm tests and security checks passed"}}'
    ;;
esac
exit 0
```

Register it in `.claude/settings.json` under `hooks.PreToolUse` with `"matcher": "Bash"` and `"command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-prod-deploy.sh"` (see Module 06 for the registration shape). Claude Code then shows its normal permission prompt with your reason. Use `"deny"` instead of `"ask"` to block outright.

### Pattern 3: Monitoring & rollback

After deployment, verify health with a script that your release workflow runs:

```bash
#!/bin/bash
# post-deploy-check.sh (called by the release workflow, not a Claude Code hook event)

sleep 10  # Let services start

# Health checks
if ! curl -f https://api.example.com/health; then
  echo "❌ Health check failed"
  echo "Rolling back..."
  git revert -n HEAD
  git commit -m "Rollback: deployment health check failed"
  exit 1
fi

echo "✅ Deployment successful and healthy"
exit 0
```

---

## Exercise: Build your first multi-agent workflow

### Scenario

You have a data science project. Release checklist:
1. Update model version
2. Run validation tests
3. Generate performance report
4. Update documentation
5. Create release tag

### Step 1: Create agents

Create `.claude/agents/` with (each file needs `name`, `description` and, ideally, a `tools` list):
- `model-versioner.md` - Updates VERSION, model metadata
- `validator.md` - Runs validation tests
- `report-generator.md` - Creates performance metrics
- `doc-updater.md` - Updates README, API docs
- `release-tagger.md` - Creates git tag

### Step 2: Create the orchestration skill

`.claude/skills/ml-release/SKILL.md`:
```markdown
---
name: ml-release
description: Release a new model version
disable-model-invocation: true
---

Release a new model version. Bump type: $ARGUMENTS (major, minor or patch).

## Workflow
1. model-versioner subagent bumps version
2. validator subagent runs test suite
3. report-generator subagent generates metrics
4. doc-updater subagent updates documentation
5. release-tagger subagent creates release tag
```

### Step 3: Test it

```bash
/ml-release patch
```

Watch as Claude delegates each step to its subagent. Review each result before the tag step.

---

## Best practices for advanced systems

### DO

✅ Design agents to be **composable** (outputs fit into next agent)

✅ **Log everything** (helps debug failures)

✅ Test workflows on **small changes first**

✅ **Document the orchestration flow** (so others understand)

✅ Build in **approval gates** for risky operations

✅ **Monitor after automation** (verify success)

### DON'T

❌ Chain too many agents (>7 becomes hard to debug)

❌ Make agents **interdependent** (prefer loose coupling)

❌ Skip **error handling** (things will fail)

❌ Deploy automated releases **without testing** workflow first

❌ Assume agents will **always agree** (build conflict resolution)

---

## Validation: You're ready if...

✓ You can explain multi-agent orchestration patterns

✓ You've created at least 2-3 cooperating agents

✓ You understand error handling strategies

✓ You know how to design workflows with approval gates

✓ You could build a release automation for your project

---

## What's next?

You've completed the 7-module learning path! You now understand:

- ✅ Installation and setup
- ✅ Core loop and context
- ✅ Memory and configuration
- ✅ Agent specialization
- ✅ Skills and knowledge
- ✅ Hooks and automation
- ✅ Advanced orchestration

### Next steps

**Option A: Deep Dive into a Domain**
- Go deeper into security: `guide/security/`
- Go deeper into DevOps: `guide/ops/`
- Go deeper into architecture: `guide/core/architecture.md`

**Option B: Build Something**
- Create a multi-agent workflow for your project
- Implement one of the exercises from this path
- Build a plugin bundle and share with team

**Option C: Learn from Examples**
- Review production agents in `examples/agents/`
- Study plugin bundles in `examples/plugins/`
- Explore skills in `guide/core/skill-design-patterns.md`

**Option D: Self-Assess**
- Take `/self-assessment comprehensive` to find gaps
- Get personalized recommendations
- Create a learning plan for weak areas

---

**Completed Module 07?** → You're a Claude Code power user.

Explore the full guide at `guide/ultimate-guide.md` for depth, or teach others what you've learned.
