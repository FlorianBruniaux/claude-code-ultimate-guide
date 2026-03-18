---
name: learn-alternatives
description: "Compare different approaches to solve the same problem"
---

# Show Alternatives

Compare different approaches to solve the same problem.

## Usage

```
/learn:alternatives              # Compare approaches for current code
/learn:alternatives auth         # Compare authentication methods
/learn:alternatives state        # Compare state management options
/learn:alternatives --detailed   # Include code examples for each
```

## Instructions

1. Identify the **problem being solved** (from context or argument)
2. Present **3-5 alternative approaches**
3. For each approach, explain:
   - What it is (one sentence)
   - When to use it
   - Trade-offs (pros/cons)
4. Provide a **recommendation** based on context
5. Optionally show code examples for top choices

## Response Format

```markdown
## Problem: [What we're trying to solve]

### Approach 1: [Name]

**What**: [One-sentence description]

**When to use**:
- [Scenario 1]
- [Scenario 2]

**Pros**: [List]
**Cons**: [List]

---

### Approach 2: [Name]
...

---

## Comparison Table

| Criteria | Approach 1 | Approach 2 | Approach 3 |
|----------|------------|------------|------------|
| Complexity | Low | Medium | High |
| Performance | ★★☆ | ★★★ | ★★☆ |
| Bundle size | Small | Medium | Large |
| Learning curve | Easy | Medium | Steep |

## Recommendation

**For your case**: [Recommended approach] because [reason based on context]

**Consider instead if**: [Alternative scenarios]
```

## Comparison Criteria

Standard criteria to evaluate (adjust based on problem):

| Criteria | Description |
|----------|-------------|
| **Complexity** | How hard to implement and maintain |
| **Performance** | Runtime speed, memory usage |
| **Bundle size** | Impact on frontend bundle |
| **Learning curve** | Time to understand and use correctly |
| **Flexibility** | Ease of extending or modifying |
| **Community** | Documentation, ecosystem, support |
| **Testing** | How easy to test |
| **Type safety** | TypeScript support quality |

## Depth Modes

### Default
- 3-4 alternatives
- Brief description each
- Comparison table
- Recommendation

### `--detailed`
- 4-5 alternatives
- Code example for each
- Detailed trade-offs
- Migration considerations
- Real-world case studies

### `--quick`
- 2-3 alternatives
- One-line each
- Quick recommendation

## Example Session

```
User: I'm using useState for form state. /learn:alternatives

Claude: ## Problem: Managing Form State in React

### Approach 1: Multiple useState

**What**: Separate useState for each field

**When to use**:
- Simple forms (< 5 fields)
- No complex validation
- No cross-field dependencies

**Pros**: Simple, no dependencies, easy to understand
**Cons**: Verbose with many fields, scattered state

---

### Approach 2: Single useState with Object

**What**: One useState holding all fields as object

**When to use**:
- Medium forms (5-10 fields)
- Need to reset entire form
- Want cleaner code

**Pros**: Grouped state, easy reset, cleaner
**Cons**: Need spread operator, can cause unnecessary re-renders

---

### Approach 3: useReducer

**What**: Reducer pattern for complex state transitions

**When to use**:
- Complex validation logic
- Multi-step forms
- Undo/redo functionality

**Pros**: Predictable updates, handles complex logic, testable
**Cons**: More boilerplate, learning curve

---

### Approach 4: Form Library (React Hook Form, Formik)

**What**: Dedicated form state management library

**When to use**:
- Large forms (10+ fields)
- Complex validation (async, cross-field)
- Performance critical (many fields)

**Pros**: Optimized re-renders, validation built-in, less code
**Cons**: Dependency, learning curve, bundle size

---

## Comparison Table

| Criteria | useState | useReducer | React Hook Form |
|----------|----------|------------|-----------------|
| Complexity | Low | Medium | Medium |
| Performance | ★★☆ | ★★☆ | ★★★ |
| Bundle size | 0kb | 0kb | ~8kb |
| Validation | Manual | Manual | Built-in |
| Best for | Simple | Complex logic | Large forms |

## Recommendation

**For your case**: If this is a simple login/contact form, stick with **useState**. If you're building a multi-step checkout or admin form, consider **React Hook Form** for the validation and performance benefits.

**Consider useReducer if**: You need undo/redo, complex state machines, or want reducer-style testing.
```

## Common Alternative Comparisons

| Topic | Typical Alternatives |
|-------|---------------------|
| **State** | useState, useReducer, Zustand, Redux, Jotai |
| **Styling** | CSS Modules, Tailwind, styled-components, CSS-in-JS |
| **Data fetching** | fetch, axios, React Query, SWR |
| **Forms** | useState, React Hook Form, Formik |
| **Auth** | JWT, sessions, OAuth, magic links |
| **API design** | REST, GraphQL, tRPC, gRPC |
| **Testing** | Jest, Vitest, Testing Library, Cypress |
| **Databases** | PostgreSQL, MySQL, MongoDB, SQLite |

$ARGUMENTS
