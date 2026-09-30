---
name: refactor
description: Analyze code for SOLID violations and suggest targeted improvements
argument-hint: "<file_or_module> [--pattern <name>]"
effort: medium
when_to_use: "Use when a module has SOLID violations, code smells, or duplication to address."
disable-model-invocation: true
---

# SOLID refactoring assistant

Analyze code for SOLID violations and suggest targeted improvements.

## Purpose

Identify refactoring opportunities based on:
- SOLID principle violations
- Code smells and anti-patterns
- Complexity metrics
- Duplication detection

## Instructions

### Step 1: Scope analysis

Determine the refactoring scope from user input:
- Single file: Deep analysis
- Directory: Pattern detection across files
- Function/class: Focused extraction suggestions

```bash
# Get file/directory stats
if [ -f "$TARGET" ]; then
  wc -l "$TARGET"
  echo "Single file analysis"
elif [ -d "$TARGET" ]; then
  find "$TARGET" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) | wc -l
  echo "Directory analysis"
fi
```

### Step 2: SOLID violations detection

#### S - single responsibility

Look for:
- Files > 300 lines
- Functions > 50 lines
- Classes with > 10 methods
- Mixed concerns (data + UI + business logic)

```bash
# Find large files
find . -name "*.{ts,js,py}" -exec wc -l {} + 2>/dev/null | sort -rn | head -10

# Functions with high line count (approximate)
grep -rn "function\|def \|fn " --include="*.{ts,js,py,rs}" . | head -20
```

#### O - open/closed principle

Look for:
- Switch/case statements on types
- Repeated if/else type checking
- Direct modifications vs extensions

#### L - liskov substitution

Look for:
- Overridden methods that throw "not implemented"
- Type checks before method calls
- Empty method overrides

#### I - interface segregation

Look for:
- Large interfaces (> 10 methods)
- Classes implementing unused interface methods
- Fat service classes

#### D - dependency inversion

Look for:
- Direct instantiation of dependencies (`new Service()`)
- Hardcoded class references
- Missing dependency injection

### Step 3: Code smells

```bash
# Duplication patterns
grep -rn --include="*.{ts,js,py}" . 2>/dev/null | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -10

# Long parameter lists (> 4 params)
grep -rn "function.*,.*,.*,.*," --include="*.{ts,js}" . 2>/dev/null | head -10

# Deep nesting (4+ levels)
grep -rn "^\s\{16,\}" --include="*.{ts,js,py}" . 2>/dev/null | head -10
```

### Step 4: Complexity assessment

For each issue found, assess:
- **Impact**: How much code is affected?
- **Risk**: What could break?
- **Effort**: Lines to change, tests needed?

## Output format

---

### 🔧 Refactoring analysis

**Target**: [file/directory]
**Lines Analyzed**: [count]

### 📊 SOLID scorecard

| Principle | Status | Issues Found |
|-----------|--------|--------------|
| Single Responsibility | 🟡 | 3 large classes |
| Open/Closed | 🟢 | OK |
| Liskov Substitution | 🟢 | OK |
| Interface Segregation | 🔴 | 2 fat interfaces |
| Dependency Inversion | 🟡 | 5 direct instantiations |

### 🎯 Priority refactorings

#### 1. [Highest Impact] - Extract class from `UserService`

**Violation**: Single Responsibility
**Current**: 450 lines handling auth + profile + notifications
**Suggested**:
```
UserService.ts (450 lines)
    ↓ Extract
AuthService.ts (~150 lines)
ProfileService.ts (~150 lines)
NotificationService.ts (~100 lines)
```
**Risk**: Medium (update imports)
**Tests Needed**: Update dependency injection in tests

#### 2. [Second Priority] - Replace switch with polymorphism

**Location**: `src/handlers/payment.ts:45`
**Current**:
```typescript
switch (paymentType) {
  case 'card': // 50 lines
  case 'bank': // 50 lines
  case 'crypto': // 50 lines
}
```
**Suggested**: Strategy pattern with `PaymentProcessor` interface
**Risk**: Low (isolated change)

### 📝 Code smells

| Smell | Location | Severity |
|-------|----------|----------|
| Long Method | `api.ts:calculateTotal` (120 lines) | 🟠 High |
| Duplicate Code | `utils/*.ts` (3 similar blocks) | 🟡 Medium |
| Deep Nesting | `parser.ts:parse` (6 levels) | 🟡 Medium |

### 🚀 Quick wins (low risk, high value)

1. Extract `validateEmail()` to shared utils (used in 4 places)
2. Replace magic numbers with named constants
3. Add early returns to reduce nesting in `processOrder()`

### ⚠️ Technical debt notes

- [Item to track for future sprints]

---

## Refactoring safety checklist

Before applying suggestions:

- [ ] Tests exist for affected code
- [ ] Create feature branch
- [ ] Commit current state
- [ ] Apply one refactoring at a time
- [ ] Run tests after each change
- [ ] Review diff before committing

## Usage

**Analyze specific file:**
```
/refactor src/services/user.ts
```

**Analyze directory:**
```
/refactor src/api/
```

**Focus on specific principle:**
```
/refactor --focus=srp src/services/
```

**With complexity threshold:**
```
/refactor --threshold=high
```

## References

- Martin Fowler's Refactoring Catalog
- Clean Code by Robert C. Martin
- SOLID principles by Robert C. Martin

$ARGUMENTS
