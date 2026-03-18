---
name: ast-grep-patterns
description: "Skill teaching Claude when and how to use ast-grep for structural code searches"
---

# ast-grep Patterns for Claude Code

> **Skill**: Teach Claude when and how to use ast-grep for structural code searches

## Installation

```bash
# Install ast-grep skill
npx skills add ast-grep/agent-skill

# Or via plugin marketplace
/plugin marketplace add
```

## When to Suggest ast-grep

Suggest ast-grep to the user when:

| Scenario | Signal Words | Why ast-grep? |
|----------|--------------|---------------|
| **Large refactoring** | "rename all calls to...", "change API signature", ">50k lines" | Structural precision needed |
| **Framework migration** | "React 17→18", "Vue 2→3", "upgrade dependencies" | AST-aware transformations |
| **Pattern detection** | "find functions without...", "locate unused...", "identify anti-patterns" | Structural rules |
| **Codebase analysis** | "which components depend on...", "find tightly coupled..." | Dependency graphs |

**Don't suggest for**:
- Simple string searches (function names, imports) → Use Grep
- Small projects (<10k lines) → Grep is sufficient
- One-off searches → Grep is faster
- Semantic searches → Use Serena MCP or grepai

## Decision Tree

```
User request analysis:
├─ "Find string/text" → Grep (native)
├─ "Find by meaning" → Serena MCP or grepai
├─ "Find by structure" → ast-grep (plugin)
└─ Mixed requirements → Start with Grep, escalate if needed
```

## Common Patterns

### 1. Async Functions Without Error Handling

**Use case**: Find async functions missing try/catch blocks

```yaml
# ast-grep rule
rule:
  pattern: |
    async function $FUNC($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: try { $$$TRY } catch
```

**When to use**: Security audits, production readiness checks

### 2. React Components with Specific Hooks

**Use case**: Find all components using `useEffect` without cleanup

```yaml
rule:
  pattern: |
    useEffect(() => {
      $$$BODY
    })
  not:
    has:
      pattern: return () => { $$$CLEANUP }
```

**When to use**: Memory leak detection, React best practices audit

### 3. Functions Exceeding Parameter Threshold

**Use case**: Find functions with >5 parameters (complexity smell)

```yaml
rule:
  pattern: function $NAME($P1, $P2, $P3, $P4, $P5, $P6, $$$REST) { $$$BODY }
```

**When to use**: Code quality improvement, refactoring candidates

### 4. Console.log in Production Code

**Use case**: Remove debug logging from production files

```yaml
rule:
  pattern: console.log($$$ARGS)
  inside:
    pattern: |
      class $CLASS {
        $$$METHODS
      }
```

**When to use**: Production cleanup, pre-release audits

### 5. Unused React Props

**Use case**: Detect props passed but never used

```yaml
rule:
  pattern: |
    function $COMP({ $PROP, $$$OTHER }) {
      $$$BODY
    }
  not:
    has:
      pattern: $PROP
      inside: $$$BODY
```

**When to use**: Dead code elimination, performance optimization

### 6. Deprecated API Usage

**Use case**: Find usage of old API methods

```yaml
rule:
  any:
    - pattern: React.Component
    - pattern: componentWillMount
    - pattern: componentWillReceiveProps
```

**When to use**: Framework migrations, deprecation cleanup

### 7. SQL Injection Risk Patterns

**Use case**: Find potential SQL injection vulnerabilities

```yaml
rule:
  pattern: |
    db.query($TEMPLATE_LITERAL)
  where:
    $TEMPLATE_LITERAL:
      kind: template_string
```

**When to use**: Security audits, vulnerability scanning

### 8. Missing TypeScript Return Types

**Use case**: Enforce explicit return types

```yaml
rule:
  pattern: |
    function $NAME($$$PARAMS) {
      $$$BODY
    }
  not:
    has:
      pattern: ': $TYPE'
```

**When to use**: TypeScript best practices, type safety improvements

### 9. Large Switch Statements (Refactoring Candidates)

**Use case**: Find switch statements with >10 cases

```yaml
rule:
  pattern: |
    switch ($EXPR) {
      $C1: $$$B1
      $C2: $$$B2
      $C3: $$$B3
      $C4: $$$B4
      $C5: $$$B5
      $C6: $$$B6
      $C7: $$$B7
      $C8: $$$B8
      $C9: $$$B9
      $C10: $$$B10
      $C11: $$$B11
    }
```

**When to use**: Complexity reduction, polymorphism refactoring

### 10. Empty Catch Blocks (Swallowed Errors)

**Use case**: Find error handling that silently fails

```yaml
rule:
  pattern: |
    try {
      $$$TRY
    } catch ($ERR) {
      // empty or only comment
    }
```

**When to use**: Debugging mysterious failures, error handling audit

## Setup Complexity vs. Value

| Codebase Size | Setup Worth It? | Alternative |
|---------------|-----------------|-------------|
| <10k lines | ❌ No | Use Grep |
| 10k-50k lines | ⚠️ Maybe | Start with Grep, escalate if needed |
| 50k-200k lines | ✅ Yes | ast-grep for structural, Grep for text |
| >200k lines | ✅ Definitely | ast-grep + Serena MCP combo |

## Troubleshooting

### ast-grep Not Found

```bash
# Verify installation
npx ast-grep --version

# Reinstall skill
npx skills add ast-grep/agent-skill --force
```

### Claude Not Using ast-grep

**Problem**: Claude uses Grep instead of ast-grep

**Solution**: Be explicit in your request
- ❌ "Find async functions"
- ✅ "Use ast-grep to find async functions"

### Performance Issues

**Problem**: ast-grep slow on large codebase

**Solutions**:
1. Narrow search scope: `ast-grep --path src/components/`
2. Use file filters: `ast-grep --lang tsx`
3. Cache results for iterative refinement

### Pattern Not Matching

**Problem**: ast-grep pattern doesn't match expected code

**Debug steps**:
1. Test pattern in isolation: `ast-grep -p 'your-pattern' file.js`
2. Check AST structure: `ast-grep --debug-query`
3. Simplify pattern incrementally
4. Verify language syntax (JS vs TS vs JSX)

## Integration Examples

### Workflow: Pre-Commit Hook with ast-grep

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for console.log in staged files
if ast-grep -p 'console.log($$$)' $(git diff --cached --name-only); then
  echo "❌ Found console.log statements"
  exit 1
fi
```

### Workflow: Migration Script

```bash
#!/bin/bash
# Migrate React class components to hooks

# Find all class components
ast-grep -p 'class $C extends React.Component' --json > components.json

# Process each component
jq -r '.[] | .file' components.json | while read file; do
  echo "Migrating: $file"
  # ... transformation logic
done
```

### Workflow: Security Audit

```bash
#!/bin/bash
# security-audit.sh

echo "=== Security Audit ==="

# SQL injection risks
ast-grep -p 'db.query(`${$VAR}`)' --lang ts

# XSS risks
ast-grep -p 'innerHTML = $VAR' --lang js

# Hardcoded secrets
ast-grep -p 'password: "$PASSWORD"' --lang ts
```

## Claude Prompt Templates

### Template 1: Large Refactoring

```
I need to refactor [FEATURE] across our codebase (~[SIZE] lines).

Use ast-grep to:
1. Find all instances of [OLD_PATTERN]
2. Identify which files will be affected
3. Suggest transformation strategy
4. Create a phased migration plan

Start with analysis only, wait for my approval before making changes.
```

### Template 2: Framework Migration

```
We're migrating from [OLD_FRAMEWORK v1] to [NEW_FRAMEWORK v2].

Use ast-grep to:
1. Find all deprecated API usage
2. Map to new API equivalents
3. Estimate migration effort (files affected)
4. Identify high-risk changes

Provide a dependency graph showing migration order.
```

### Template 3: Code Quality Audit

```
Run a code quality audit on [DIRECTORY] using ast-grep.

Focus on:
- Functions with >5 parameters
- Async functions without error handling
- Empty catch blocks
- Unused function parameters

Rank issues by severity and provide refactoring suggestions.
```

## Advanced: Combining ast-grep with Other Tools

### ast-grep + Serena MCP

```bash
# 1. ast-grep finds structural patterns
ast-grep -p 'async function $F' --json > async-funcs.json

# 2. Serena finds symbols and dependencies
claude mcp call serena find_symbol --name "authenticate"

# 3. Combine insights for full context
# ast-grep: "This is an async function"
# Serena: "Called by 12 other functions"
```

### ast-grep + grepai

```bash
# 1. grepai for semantic search
# "Find authentication-related code"

# 2. ast-grep for structural refinement
# "Among those results, which are async without error handling?"
```

## Best Practices

1. **Start Simple**: Begin with Grep, escalate to ast-grep when needed
2. **Test Patterns**: Verify on small files before running on entire codebase
3. **Document Patterns**: Save successful patterns as reusable rules
4. **Explicit Requests**: Always tell Claude explicitly when to use ast-grep
5. **Combine Tools**: Use ast-grep for structure, Grep for text, Serena for symbols

## Resources

- [ast-grep Documentation](https://ast-grep.github.io/)
- [Pattern Playground](https://ast-grep.github.io/playground.html)
- [ast-grep GitHub](https://github.com/ast-grep/ast-grep)
- [Claude Skill](https://github.com/ast-grep/claude-skill)

---

**Last updated**: January 2026
**Compatible with**: Claude Code 2.1.7+
