---
title: "Module 07: Advanced Patterns"
description: "Learning Path Module 07: orchestrate multi-agent Claude Code workflows, handle error recovery, and apply production-grade automation patterns for team workflows. 2-3 hours, advanced."
---

# Module 07: Advanced Patterns

**Time**: 2-3 hours | **Complexity**: ⭐⭐⭐ Advanced

## Goal

Orchestrate multi-agent workflows. Build complex automation that coordinates multiple specialized agents.

---

## What You'll Learn

- Multi-agent architecture patterns
- Orchestration strategies
- Error handling and recovery
- Production-grade automation
- Team workflows
- Real-world scenarios

---

## Multi-Agent Systems

A **multi-agent system** is when multiple specialized agents work together on one goal.

### Example: Code Release Workflow

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

## Orchestration Patterns

### Pattern 1: Sequential (Pipeline)

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
```bash
/agent requirements-parser
Parse the feature request into specifications

# Later, once we have specifications:
/agent database-designer
Design the schema based on these specs

# Once schema is approved:
/agent code-generator
Generate models based on the schema
```

### Pattern 2: Parallel (Fork-Join)

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
Request: "Review my code changes"

Parallel tasks:
- Code quality agent reviews
- Security agent scans
- Test coverage agent checks
- Performance agent analyzes

(All run at the same time)

Results combined into one report
```

### Pattern 3: Conditional (If-Then)

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
```bash
/agent bug-classifier
Categorize this bug: security, performance, or logic

# Based on response:
# If security:
/agent security-patcher
Fix the security vulnerability

# If performance:
/agent perf-optimizer
Optimize this code
```

---

## Building a Release Workflow

### Scenario

You want to automate your release process. Right now you:
1. Update VERSION file
2. Update CHANGELOG
3. Run tests
4. Run security scan
5. Create git tag
6. Push to origin
7. Deploy to staging

### Solution: Multi-Agent Workflow

**Step 1: Create agents** (each specializes in one task)

`.claude/agents/version-manager.md`:
```markdown
---
name: version-manager
description: Manages version files and tags
capabilities:
  - read_files
  - write_files
  - NO: push
---

# Version Manager

## Purpose
Update VERSION files and create git tags

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

**Step 2: Create a release workflow command**

`.claude/commands/release-workflow.md`:
```markdown
# /release-workflow

Orchestrate a complete release process.

Usage:
```
/release-workflow patch|minor|major
```

## Process

1. Validate release readiness
2. Update version (version-manager agent)
3. Generate changelog (changelog-generator agent)
4. Run tests (test-validator agent)
5. Security scan (security-auditor agent)
6. Publish and deploy (release-publisher agent)

## Requirements
- All tests passing
- No outstanding security issues
- Changelog updated
```

**Step 3: Use the workflow**

```bash
/release-workflow patch
```

Claude then:
1. Calls version-manager → updates VERSION
2. Calls changelog-generator → creates release notes
3. Calls test-validator → verifies tests pass
4. Calls security-auditor → scans for vulnerabilities
5. Calls release-publisher → creates tag, pushes
6. You review, then approve each step

---

## Error Handling in Multi-Agent Systems

### Pattern: Graceful Degradation

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

### Pattern: Retry on Failure

For transient failures (network, timeouts):

```bash
#!/bin/bash
# In a hook or skill

max_retries=3
retry=0

while [ $retry -lt $max_retries ]; do
  if /agent test-validator run-tests; then
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
exit 1
```

### Pattern: Rollback on Error

If something goes wrong, undo changes:

```bash
#!/bin/bash
# Rollback helper

ORIGINAL_VERSION=$(git rev-parse HEAD:VERSION)
ORIGINAL_TAG=$(git describe --tags --abbrev=0)

cleanup_and_exit() {
  echo "Rolling back..."
  git reset --hard HEAD~1
  git tag -d "$NEW_TAG"
  echo "VERSION restored to: $ORIGINAL_VERSION"
  exit 1
}

# Run release steps
if ! /agent version-manager bump-version patch; then
  cleanup_and_exit
fi

if ! /agent test-validator validate-all; then
  cleanup_and_exit
fi

# If we get here, release succeeded
exit 0
```

---

## Production Patterns

### Pattern 1: Staged Rollout

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

### Pattern 2: Approval Gates

Block advancement until reviewed:

```bash
# In .claude/hooks/pre-prod-deploy.sh

echo "🚨 PRODUCTION DEPLOY"
echo "Changes: $CHANGES"
echo "Tests: PASSING"
echo "Security: PASSING"
echo ""
read -p "Type 'I approve' to deploy to production: " approval

if [ "$approval" != "I approve" ]; then
  echo "❌ Deploy cancelled"
  exit 1
fi

exit 0
```

### Pattern 3: Monitoring & Rollback

After deployment, verify health:

```bash
#!/bin/bash
# Post-deploy hook

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

## Exercise: Build Your First Multi-Agent Workflow

### Scenario

You have a data science project. Release checklist:
1. Update model version
2. Run validation tests
3. Generate performance report
4. Update documentation
5. Create release tag

### Step 1: Create Agents

Create `.claude/agents/` with:
- `model-versioner.md` - Updates VERSION, model metadata
- `validator.md` - Runs validation tests
- `report-generator.md` - Creates performance metrics
- `doc-updater.md` - Updates README, API docs
- `release-tagger.md` - Creates git tag

### Step 2: Create the Orchestration Command

`.claude/commands/ml-release.md`:
```markdown
# /ml-release

Release a new model version.

Usage:
```
/ml-release [major|minor|patch]
```

## Workflow
1. Version agent bumps version
2. Validator runs test suite
3. Report agent generates metrics
4. Doc agent updates documentation
5. Tagger creates release tag
```

### Step 3: Test It

```bash
/ml-release patch
```

Watch as agents coordinate the full release.

---

## Best Practices for Advanced Systems

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

## Validation: You're Ready If...

✓ You can explain multi-agent orchestration patterns

✓ You've created at least 2-3 cooperating agents

✓ You understand error handling strategies

✓ You know how to design workflows with approval gates

✓ You could build a release automation for your project

---

## What's Next?

You've completed the 7-module learning path! You now understand:

- ✅ Installation and setup
- ✅ Core loop and context
- ✅ Memory and configuration
- ✅ Agent specialization
- ✅ Skills and knowledge
- ✅ Hooks and automation
- ✅ Advanced orchestration

### Next Steps

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

**Completed Module 07?** → You're a Claude Code power user! 🚀

Explore the full guide at `guide/ultimate-guide.md` for depth, or teach others what you've learned.
