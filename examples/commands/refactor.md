---
name: refactor
description: "Analyze code for SOLID violations and suggest targeted improvements"
---

# SOLID Refactoring Assistant

Analyze code for SOLID violations and suggest targeted improvements.

## Purpose

Identify refactoring opportunities based on:
- SOLID principle violations
- Code smells and anti-patterns
- Complexity metrics
- Duplication detection

## Instructions

### Step 1: Scope Analysis

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

### Step 2: SOLID Violations Detection

#### S - Single Responsibility

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

#### O - Open/Closed Principle

Look for:
- Switch/case statements on types
- Repeated if/else type checking
- Direct modifications vs extensions

#### L - Liskov Substitution

Look for:
- Overridden methods that throw "not implemented"
- Type checks before method calls
- Empty method overrides

#### I - Interface Segregation

Look for:
- Large interfaces (> 10 methods)
- Classes implementing unused interface methods
- Fat service classes

#### D - Dependency Inversion

Look for:
- Direct instantiation of dependencies (`new Service()`)
- Hardcoded class references
- Missing dependency injection

### Step 3: Code Smells

```bash
# Duplication patterns
grep -rn --include="*.{ts,js,py}" . 2>/dev/null | \
  awk -F: '{print $3}' | sort | uniq -c | sort -rn | head -10

# Long parameter lists (> 4 params)
grep -rn "function.*,.*,.*,.*," --include="*.{ts,js}" . 2>/dev/null | head -10

# Deep nesting (4+ levels)
grep -rn "^\s\{16,\}" --include="*.{ts,js,py}" . 2>/dev/null | head -10
```

### Step 4: Complexity Assessment

For each issue found, assess:
- **Impact**: How much code is affected?
- **Risk**: What could break?
- **Effort**: Lines to change, tests needed?

## Output Format

---

### 🔧 Refactoring Analysis

**Target**: [file/directory]
**Lines Analyzed**: [count]

### 📊 SOLID Scorecard

| Principle | Status | Issues Found |
|-----------|--------|--------------|
| Single Responsibility | 🟡 | 3 large classes |
| Open/Closed | 🟢 | OK |
| Liskov Substitution | 🟢 | OK |
| Interface Segregation | 🔴 | 2 fat interfaces |
| Dependency Inversion | 🟡 | 5 direct instantiations |

### 🎯 Priority Refactorings

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

### 📝 Code Smells

| Smell | Location | Severity |
|-------|----------|----------|
| Long Method | `api.ts:calculateTotal` (120 lines) | 🟠 High |
| Duplicate Code | `utils/*.ts` (3 similar blocks) | 🟡 Medium |
| Deep Nesting | `parser.ts:parse` (6 levels) | 🟡 Medium |

### 🚀 Quick Wins (Low Risk, High Value)

1. Extract `validateEmail()` to shared utils (used in 4 places)
2. Replace magic numbers with named constants
3. Add early returns to reduce nesting in `processOrder()`

### ⚠️ Technical Debt Notes

- [Item to track for future sprints]

---

## Refactoring Safety Checklist

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
