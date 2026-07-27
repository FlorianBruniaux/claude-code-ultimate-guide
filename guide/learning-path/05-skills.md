---
title: "Module 05: Skills & Automation"
description: "Learning Path Module 05: build reusable Claude Code skills with SKILL.md, from frontmatter and metadata to auto-invocation, and package them into a shared knowledge base. 1.5 hours, intermediate."
---

# Module 05: Skills & Automation

**Time**: 1.5 hours | **Complexity**: ⭐⭐ Intermediate

## Goal

Create reusable skills that give Claude domain-specific knowledge. Package solutions for repeated problems.

---

## What You'll Learn

- What skills are and why they're powerful
- Creating skills with SKILL.md
- Skill frontmatter and metadata
- Auto-invoking skills
- Building a knowledge base
- Bundling skills with your projects

---

## What Are Skills?

A **skill** is a reusable knowledge module. It teaches Claude how to do something specific.

### Example: Testing Skill

Instead of explaining your testing approach every session, you create a skill:

```markdown
# Testing Best Practices for Our Project

## Framework: Jest

## Style
- Descriptive names: "should validate email with + symbols"
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test behavior, not implementation

## Coverage Target
Minimum 80%
```

Now, whenever Claude helps with testing, it reads this skill and follows your approach.

### Skills vs Agents

| Aspect | Skill | Agent |
|--------|-------|-------|
| Purpose | Teach knowledge | Execute tasks |
| Scope | Domain knowledge | Specialized workflow |
| Persistence | Remembered each session | Called explicitly |
| Auto-invoke | Yes (optional) | Manual only |
| Example | "How we test code" | "The test-writer agent" |

---

## Creating Your First Skill

Skills are markdown files in `.claude/skills/`.

### Basic Structure

```markdown
---
name: testing-standards
description: Our project's testing practices and conventions
triggers: [test, testing, jest, spec]
auto_invoke: false
keywords: [jest, unit-test, integration-test, mocking]
version: 1.0.0
---

# Testing Standards

## Framework
Jest with @testing-library/react

## File Organization
- Tests live next to source code
- Naming: `[Component].test.tsx`
- Fixtures in `__fixtures__/`
- Mocks in `__mocks__/`

## Test Structure (AAA)
1. **Arrange**: Set up test data
2. **Act**: Call the function/component
3. **Assert**: Check results

## Example

```typescript
describe('validateEmail', () => {
  it('should accept valid email addresses', () => {
    // Arrange
    const email = 'user@example.com';
    
    // Act
    const result = validateEmail(email);
    
    // Assert
    expect(result).toBe(true);
  });
});
```

## Coverage Requirements
- Target: 80% minimum
- Critical paths: 100%
- Types of coverage: line, branch, function

## Mocking Strategy
- External APIs: use jest.mock()
- Database: use test fixtures
- Timers: use jest.useFakeTimers()

## Running Tests
```bash
npm test                 # Run all tests
npm test -- --coverage   # With coverage report
npm test -- --watch      # Watch mode
```
```

### File Location

```
my-project/
└── .claude/
    └── skills/
        └── testing-standards.md
```

---

## Skill Features

### Triggers

Automatically invoke the skill when Claude sees certain keywords:

```markdown
---
triggers: [test, jest, spec, coverage, mock]
---
```

If Claude sees "add tests to this function", it automatically reads the testing skill.

### Auto-Invoke

```markdown
---
auto_invoke: true
---
```

When `true`, Claude loads the skill at session start (without you asking). Use for critical rules.

### Keywords

Help Claude's search find the skill:

```markdown
---
keywords: [testing, jest, unit-test, mocking, assertions]
---
```

### Version

Track skill versions:

```markdown
---
version: 1.0.0
---
```

Update when the skill changes significantly.

---

## Common Skill Patterns

### Pattern 1: Coding Standards

```markdown
---
name: python-standards
triggers: [python, flask, django]
---

# Python Coding Standards

## Style
- PEP 8 compliance (max 100 chars)
- Type hints on all functions
- Docstrings in Google format

## Testing
- pytest for unit tests
- 80% minimum coverage
- Mock external dependencies

## File Organization
src/
├── models/
├── services/
├── controllers/
└── tests/

## Imports
```python
# ✅ Good: specific imports
from models import User
from services.auth import authenticate

# ❌ Bad: wildcard imports
from models import *
```
```

### Pattern 2: Domain Knowledge

```markdown
---
name: payment-processing
description: Payment system rules and edge cases
auto_invoke: true
---

# Payment Processing Rules

## PCI Compliance
- Never log card numbers
- Use tokenization (Stripe)
- Encrypt sensitive data
- Audit all transactions

## Common Issues
1. Partial charges: Retry with exponential backoff
2. Currency conversion: Always round to 2 decimals
3. Timezone handling: Store all times in UTC

## Edge Cases
- Declined cards: Provide clear error message
- Expired cards: Suggest updating payment method
- 3D Secure: Handle verification flow
```

### Pattern 3: Process Documentation

```markdown
---
name: code-review-checklist
triggers: [review, pull request, pr]
---

# Code Review Checklist

## Before Requesting Review
- [ ] Tests pass locally
- [ ] No console.log statements
- [ ] No secrets in code
- [ ] Commit messages are clear

## Security Checks
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No exposed API keys
- [ ] Input is validated

## Performance
- [ ] No N+1 queries
- [ ] No infinite loops
- [ ] Load times acceptable

## Testing
- [ ] Unit tests added
- [ ] Integration tests updated
- [ ] Coverage >80%
```

---

## Bundling Skills

You can package multiple related skills together.

### Project Skill Bundle

```
my-project/
└── .claude/
    └── skills/
        ├── testing-standards.md
        ├── api-design.md
        ├── database-patterns.md
        └── security-checklist.md
```

In CLAUDE.md, reference them:

```markdown
## Available Skills
Our custom skills are loaded automatically:
- **testing-standards**: How we write tests
- **api-design**: REST API conventions
- **database-patterns**: Common queries and migrations
- **security-checklist**: Security review process
```

### Distributing Skills

To share skills with your team, version control them in git:

```bash
git add .claude/skills/
git commit -m "Add testing and API design skills"
git push
```

Teammates checkout the project and get the skills automatically.

---

## Exercise: Create a Domain Skill

### Scenario

You're building an e-commerce site. You want Claude to understand your product data model.

### Step 1: Create the Skill

```bash
cat > .claude/skills/product-data-model.md << 'EOF'
---
name: product-data-model
description: E-commerce product data structure and rules
triggers: [product, catalog, sku, price, inventory]
auto_invoke: false
version: 1.0.0
---

# Product Data Model

## Core Entities

### Product
```
{
  id: UUID,
  name: string,
  slug: string,  // URL-friendly
  description: string,
  category_id: UUID,
  created_at: timestamp,
  updated_at: timestamp
}
```

### SKU (Stock Keeping Unit)
```
{
  id: UUID,
  product_id: UUID,
  sku: string,  // e.g., "BLUE-XL-001"
  price: decimal,  // Always 2 decimals
  cost: decimal,
  inventory: integer,
  weight: float,  // In kg
}
```

### Inventory Rules
- Decrement on order placement
- Increment on return
- Low stock alert: <5 units
- Reorder level: Set per product

## Common Queries

### Get product with all SKUs
```sql
SELECT p.*, s.* 
FROM products p 
JOIN skus s ON p.id = s.product_id 
WHERE p.slug = ?
```

### Check inventory
```sql
SELECT sum(inventory) FROM skus WHERE product_id = ?
```

## Edge Cases
1. Out of stock: Return 404 or "unavailable"
2. Variant selection: Show price per SKU
3. Price changes: Update in SKU, not Product
EOF
```

### Step 2: Reference in CLAUDE.md

```markdown
## Skills
- **product-data-model**: Understanding our product structure
```

### Step 3: Use It

In a session:

```
Add a query to find all products with low inventory (< 5 units)
```

Claude will:
1. Read the product-data-model skill
2. Understand your schema
3. Write the correct SQL

---

## Best Practices

### DO

✅ Create skills for things you repeat

✅ Keep skills focused (one domain per skill)

✅ Version control your skills

✅ Include examples in skills

✅ Update skills when requirements change

✅ Share skills with your team

### DON'T

❌ Create skills for one-time knowledge (use CLAUDE.md instead)

❌ Make skills too long (>500 lines = break into multiple skills)

❌ Use skills for temporary instructions (use CLAUDE.md or AGENT.md)

❌ Assume skills are comprehensive documentation

---

## Skill Lifecycle

1. **Create**: Identify repeated pattern or domain knowledge
2. **Document**: Write the skill with examples
3. **Test**: Use it in a session and verify Claude follows it
4. **Refine**: Update based on feedback
5. **Share**: Commit to git for team access
6. **Maintain**: Update as your practices evolve

---

## Validation: You're Ready If...

✓ You've created at least one custom skill

✓ You understand triggers and auto-invoke

✓ You know the difference between skills and agents

✓ You can explain when to use a skill vs CLAUDE.md

✓ Your skill has been tested in a real session

---

## What's Next?

**Module 06: Hooks & Events** covers:
- Automating responses to system events
- Pre-commit validation
- Post-action notifications
- Building safe automation

This teaches you how to automate repetitive tasks without manual intervention.

---

**Completed Module 05?** → Ready for Module 06: Hooks & Events
