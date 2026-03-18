---
name: optimize
description: "Analyze and suggest performance improvements for code, queries, or systems"
---

# Performance Optimizer

Analyze and suggest performance improvements for code, queries, or systems.

## Purpose

Identify optimization opportunities:
- Runtime performance bottlenecks
- Memory usage issues
- Database query inefficiencies
- Bundle size problems
- Algorithm complexity

## Instructions

### Step 1: Scope Identification

Determine optimization target:
- **Function**: Single function performance
- **Module**: Related functions/classes
- **Query**: Database query optimization
- **Bundle**: Frontend bundle analysis
- **System**: Architecture-level optimization

### Step 2: Performance Analysis

#### Runtime Analysis

```bash
# Find potentially slow patterns
grep -rn "forEach\|\.map\|\.filter\|\.reduce" --include="*.{ts,js}" . | head -20

# Find nested loops (O(n²) potential)
grep -rn "for.*for\|\.forEach.*\.forEach\|\.map.*\.map" --include="*.{ts,js}" . | head -10

# Find sync operations that could be async
grep -rn "readFileSync\|writeFileSync\|execSync" --include="*.{ts,js}" . | head -10
```

#### Memory Analysis

```bash
# Large array operations
grep -rn "new Array\|Array\.from\|\.concat\|spread" --include="*.{ts,js}" . | head -10

# Potential memory leaks (event listeners, intervals)
grep -rn "addEventListener\|setInterval\|setTimeout" --include="*.{ts,js}" . | head -10
```

#### Database Query Analysis

```bash
# N+1 query patterns
grep -rn "await.*find\|await.*query" --include="*.{ts,js}" . | head -15

# Missing indexes hints
grep -rn "WHERE\|ORDER BY\|GROUP BY" --include="*.{ts,js,sql}" . | head -15
```

#### Bundle Analysis

```bash
# Check bundle size (if applicable)
[ -f "package.json" ] && npm run build 2>/dev/null && ls -lh dist/*.js 2>/dev/null

# Large dependencies
[ -f "package.json" ] && cat package.json | jq '.dependencies | keys[]' | head -20
```

### Step 3: Prioritization

Rank findings by:
1. **Impact**: How much will this improve performance?
2. **Effort**: How hard is the fix?
3. **Risk**: What could break?

## Output Format

---

### ⚡ Performance Analysis

**Target**: [file/module/system]
**Analysis Date**: [timestamp]

### 📊 Current Metrics (if measurable)

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Response time | Xms | <Yms | -Z% needed |
| Memory usage | XMB | <YMB | -Z% needed |
| Bundle size | XKB | <YKB | -Z% needed |

### 🔴 Critical Issues

#### 1. [Issue Title] - [Location]

**Problem**: [What's slow and why]

**Current**:
```typescript
// O(n²) - nested loops
users.forEach(user => {
  permissions.forEach(perm => {
    if (user.id === perm.userId) { ... }
  });
});
```

**Optimized**:
```typescript
// O(n) - Map lookup
const permMap = new Map(permissions.map(p => [p.userId, p]));
users.forEach(user => {
  const perm = permMap.get(user.id);
  if (perm) { ... }
});
```

**Impact**: ~10x faster for 1000 users
**Effort**: Low (5 min)
**Risk**: Low

### 🟠 High Priority

| Issue | Location | Impact | Effort |
|-------|----------|--------|--------|
| [description] | file:line | [estimate] | [time] |

### 🟡 Medium Priority

| Issue | Location | Impact | Effort |
|-------|----------|--------|--------|
| [description] | file:line | [estimate] | [time] |

### 💡 Quick Wins

1. [Small change with good impact]
2. [Another quick optimization]
3. [Low-hanging fruit]

### 📈 Optimization Roadmap

```
Week 1: Critical fixes (items 1-3)
Week 2: High priority (items 4-6)
Week 3: Measure and validate improvements
```

---

## Common Patterns

### Array Operations

| Pattern | Issue | Fix |
|---------|-------|-----|
| `arr.filter().map()` | Two iterations | Single `reduce()` or `flatMap()` |
| `arr.find()` in loop | O(n²) | Build Map/Set first |
| `[...arr1, ...arr2]` | Memory allocation | `arr1.concat(arr2)` or push |

### Database

| Pattern | Issue | Fix |
|---------|-------|-----|
| Loop with await | N+1 queries | Batch query with `IN` |
| `SELECT *` | Over-fetching | Select only needed columns |
| Missing WHERE index | Full table scan | Add composite index |

### React/Frontend

| Pattern | Issue | Fix |
|---------|-------|-----|
| Inline functions in JSX | Re-renders | `useCallback` |
| Large list rendering | DOM thrashing | Virtualization |
| Unoptimized images | Slow LCP | Next/Image, lazy loading |

### Node.js

| Pattern | Issue | Fix |
|---------|-------|-----|
| Sync file operations | Blocks event loop | Async alternatives |
| JSON.parse large files | Memory spike | Streaming parser |
| No connection pooling | Connection overhead | Pool with pg-pool, etc. |

## Usage

**Analyze specific file:**
```
/optimize src/services/user.ts
```

**Focus on specific area:**
```
/optimize --queries src/repositories/
/optimize --bundle
/optimize --memory src/workers/
```

**With target metrics:**
```
/optimize --target=100ms src/api/search.ts
```

**Quick scan:**
```
/optimize --quick
```

## Notes

- Measurements beat assumptions: profile before optimizing
- Premature optimization is the root of all evil (Knuth)
- Focus on hot paths: optimize what runs often
- Consider trade-offs: speed vs readability vs maintainability

$ARGUMENTS
