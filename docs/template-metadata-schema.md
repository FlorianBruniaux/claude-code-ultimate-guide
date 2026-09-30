# Template metadata schema

Complete metadata specification for all templates in `examples/`.

---

## Purpose

Template metadata enables:
- **Discovery**: Find templates by complexity, time, domain
- **Automation**: Generate catalogs, indexes, and documentation
- **Quality**: Validate consistency across 181+ templates
- **Learning**: Help users find appropriate templates for their skill level

---

## YAML frontmatter format

All templates (`agents/`, `commands/`, `skills/`, `hooks/`, `workflows/`, `scripts/`) should include metadata in YAML frontmatter:

```yaml
---
name: template-name
description: One-line description of what this template does
complexity: beginner|intermediate|advanced
time: 5 min|15 min|30 min|1 hour|2 hours|4+ hours|varies
domain: security|testing|deployment|performance|architecture|automation|general
prerequisites: []
status: stable|experimental|deprecated
keywords: [tag1, tag2, tag3]
---
```

### File format rules

**Markdown** (`.md`):
```markdown
---
name: code-reviewer
description: Code review agent with security and quality checks
...
---

# Code Reviewer Agent

Content starts here...
```

**Bash/PowerShell** (`.sh`, `.ps1`):
```bash
#!/bin/bash
# ---
# name: pre-commit-validator
# description: Validates code before commit
# ...
# ---

# Script content starts here
```

---

## Field specifications

### `name` (Required)

Unique identifier for the template. Must be URL-safe and kebab-cased.

**Rules:**
- Use only lowercase letters, numbers, hyphens
- No spaces or special characters
- Should match filename (without extension)
- Examples: `code-reviewer`, `unit-test-generator`, `security-auditor`

**Usage:**
- Becomes the catalog link text
- Used in `/agent code-reviewer` commands
- Referenced in documentation

---

### `description` (Required)

One-line summary of what the template does.

**Rules:**
- Keep under 100 characters
- Be specific, not vague
- Start with a verb when possible
- Focus on the outcome, not implementation details

**Examples:**
```yaml
# ✅ Good
description: Automated code review for security and performance issues

# ❌ Bad
description: A tool for reviewing code
description: Code analyzer that checks things
```

---

### `complexity` (Required)

Skill level required to use the template effectively.

**Valid values:**
- `beginner`: No prerequisite knowledge needed
- `intermediate`: Basic Claude Code experience required
- `advanced`: Deep Claude Code knowledge or specialized domain expertise

**Guidelines:**
- **Beginner**: Straightforward agents/skills that don't require customization
  - Examples: Simple testing agents, basic documentation generators
- **Intermediate**: Templates that require some customization or domain knowledge
  - Examples: Code review agents, CI/CD command templates, common workflows
- **Advanced**: Complex orchestration, specialized domains, or multi-component systems
  - Examples: Multi-agent systems, security auditing, performance optimization, cyber defense

**Usage:**
- Helps users filter in learning path and `/self-assessment`
- Guides documentation complexity level
- Informs prerequisite suggestions

---

### `time` (Required)

Estimated time to understand and adapt the template to your project.

**Valid values:**
- `5 min`: Quick reference, minimal setup
- `15 min`: Simple template, light adaptation
- `30 min`: Standard template, some customization needed
- `1 hour`: Moderate complexity or significant learning
- `2 hours`: Complex template or steep learning curve
- `4+ hours`: Very complex systems or multiple components
- `varies`: Depends heavily on context (e.g., domain-specific)

**What "time" includes:**
- Reading/understanding the template
- Adapting to your project
- Testing the template
- Verifying it works

**What "time" does NOT include:**
- Learning Claude Code fundamentals (covered by Module 01-02)
- Domain-specific knowledge (e.g., learning Kubernetes before using DevOps template)

**Examples:**
- `code-reviewer` agent: `30 min` (understand checklist, adapt rules)
- `test-writer` command: `15 min` (pick test framework, light customization)
- Multi-agent cyber defense: `4+ hours` (multiple agents, event schema, pipeline)

---

### `domain` (Optional)

Category/domain the template belongs to.

**Common domains:**
- `security`: Vulnerability scanning, threat detection, security audits
- `testing`: Test generation, test validation, coverage analysis
- `deployment`: CI/CD, release automation, infrastructure
- `performance`: Optimization, profiling, bottleneck detection
- `architecture`: Design review, refactoring, pattern analysis
- `automation`: Workflow orchestration, repetitive task automation
- `general`: No specific domain, broadly applicable

**Rules:**
- Use a single domain (prefer the primary one)
- If template spans multiple domains, pick the strongest fit
- When in doubt, use `general`

**Usage:**
- Enables domain-based filtering in catalogs
- Helps users find expertise-specific tools
- Organizes documentation sections

---

### `prerequisites` (Optional)

What knowledge or setup is required before using the template.

**Format:**
```yaml
prerequisites: [skill-name, agent-name, module-number]
```

**Examples:**
```yaml
# Security auditor requires understanding Module 02 (context)
prerequisites: [Module-02-Core-Loop]

# This agent is built on top of code-reviewer
prerequisites: [code-reviewer agent]

# Requires familiarity with testing concepts
prerequisites: [testing-patterns skill]
```

**Rules:**
- List specific modules, skills, or other agents
- Keep it short (max 3 prerequisites)
- If more than 3, consider if template is too advanced
- Should map to actual learning path items

**Usage:**
- Auto-generated prerequisite chains in catalog
- Validation in `/self-assessment` (suggest prereqs)
- Documentation can surface prerequisites

---

### `status` (Optional)

Lifecycle status of the template.

**Valid values:**
- `stable` (default): Tested, documented, ready for production
- `experimental`: New, not yet fully tested, may change
- `deprecated`: No longer recommended, consider alternatives

**Rules:**
- Omit if `stable` (default)
- Mark clearly with warning icon in catalog if `experimental` or `deprecated`
- Experimental templates should include migration path notes

**Examples:**
```yaml
# Experimental new feature
status: experimental
# Consider alternatives: code-reviewer agent

# Deprecated, replaced by newer version
status: deprecated
# Use instead: security-auditor-v2 agent
```

---

### `keywords` (Optional)

Search tags for discoverability.

**Format:**
```yaml
keywords: [keyword1, keyword2, keyword3, ...]
```

**Examples:**
```yaml
# Code reviewer keywords
keywords: [review, quality, security, performance, linting]

# Test generator keywords
keywords: [testing, jest, unit-test, tdd, bdd, coverage]
```

**Rules:**
- Use 3-5 keywords maximum
- Keep keywords short (1-2 words)
- Include common search terms (frameworks, patterns, practices)
- Include domain-specific vocabulary

**Usage:**
- Enables full-text search in extended catalog
- Improves discoverability through tags
- Supports alias mapping (e.g., "reviews" → "code-reviewer")

---

## Validation rules

The `scripts/generate-template-catalog.py --validate` tool enforces:

1. **Required fields** exist: `name`, `description`, `complexity`, `time`
2. **Valid values** for enums: `complexity`, `time`, `status`
3. **Format rules**: `name` is kebab-case, description under 100 chars
4. **File consistency**: Filename matches `name` field
5. **Reference validity**: Prerequisites, domains, keywords are well-formed

---

## Minimal template

Every template MUST include at minimum:

```yaml
---
name: my-template
description: Brief description of what this does
complexity: intermediate
time: 30 min
---
```

---

## Complete example

```yaml
---
name: security-auditor
description: Comprehensive security scan with OWASP Top 10 checks
complexity: advanced
time: 2 hours
domain: security
prerequisites: [Module-02-Core-Loop, code-reviewer agent]
status: stable
keywords: [security, audit, vulnerability, owasp, injection, xss, sqlinjection]
---

# Security Auditor Agent

Agent definition and content follows...
```

---

## Automated generation

The catalog is auto-generated from metadata:

```bash
# Generate CATALOG.md from all template metadata
python3 scripts/generate-template-catalog.py

# Validate all templates have correct metadata
python3 scripts/generate-template-catalog.py --validate

# Generate and save to specific file
python3 scripts/generate-template-catalog.py --output examples/CATALOG.md
```

Integration points:
- **Pre-commit hook**: Validates metadata before commit
- **Release workflow**: Auto-generates catalog during `/release`
- **CI/CD**: Validates metadata on each push

---

## Migration guide

### Existing templates

If updating an existing template:

1. Add frontmatter to the top of the file
2. Run validation: `python3 scripts/generate-template-catalog.py --validate`
3. Commit with message: `docs: add metadata to [template-name]`

### Batch updates

Update multiple templates at once:

```bash
# Find all templates without metadata
find examples -name "*.md" -exec grep -L "^---" {} \;

# Add minimal metadata to all
find examples -name "*.md" | xargs -I {} \
  python3 scripts/add-default-metadata.py {}
```

---

## FAQ

**Q: Should every template have all fields?**  
A: No. Required: `name`, `description`, `complexity`, `time`. Optional fields can be omitted if not applicable.

**Q: Can I add custom fields?**  
A: Yes, but they won't be indexed by the catalog tool. Useful for internal tracking (e.g., `author`, `date_added`).

**Q: How often should metadata be updated?**  
A: Update when: template is significantly modified, status changes, prerequisites change, or domain shifts.

**Q: What if a template covers multiple domains?**  
A: Choose the primary/strongest domain. If truly multi-domain, consider splitting into separate templates or use `general`.

---

## Related files

- `examples/CATALOG.md` — Auto-generated template index
- `scripts/generate-template-catalog.py` — Catalog generation tool
- `.claude/hooks/validate-template-metadata.sh` — Pre-commit validation
- `guide/learning-path/` — Learning path references specific templates

---

**Last updated**: 2026-04-21  
**Version**: 1.0.0
