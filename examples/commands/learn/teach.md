---
name: learn-teach
description: "Step-by-step explanation of a concept with progressive depth"
---

# Teach Me

Step-by-step explanation of a concept with progressive depth.

## Usage

```
/learn:teach React hooks         # Learn about React hooks
/learn:teach async/await         # Understand async patterns
/learn:teach SOLID principles    # Learn design principles
/learn:teach --deep SQL joins    # In-depth explanation
```

## Instructions

1. Start with a **one-sentence definition** of the concept
2. Explain **why it matters** (real-world problem it solves)
3. Show a **minimal example** (simplest possible code)
4. Break down **each part** of the example with comments
5. Show a **practical example** (real-world use case)
6. Highlight **common mistakes** beginners make
7. Suggest **next concepts** to learn

## Response Format

```markdown
## [Concept Name]

**In one sentence**: [Clear, simple definition]

### Why It Matters

[1-2 sentences on the problem this solves]

### Minimal Example

\`\`\`[language]
// Simplest possible demonstration
[code]
\`\`\`

**Line by line**:
- Line 1: [explanation]
- Line 2: [explanation]
...

### Practical Example

\`\`\`[language]
// Real-world scenario
[code]
\`\`\`

### Common Mistakes

1. **[Mistake]**: [Why it's wrong and what to do instead]
2. **[Mistake]**: [Why it's wrong and what to do instead]

### Key Takeaways

- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

### Learn Next

- [Related concept 1] — [why it connects]
- [Related concept 2] — [why it connects]

---

**Practice challenge**: [Small exercise to reinforce the concept]
```

## Depth Modes

### Default
- One-sentence definition
- One minimal example
- One practical example
- 2-3 common mistakes

### `--deep`
- Extended explanation with history/context
- Multiple examples of increasing complexity
- Edge cases and gotchas
- Performance considerations
- Comparison with alternatives
- Interview-relevant details

### `--quick`
- Definition only
- Single example
- No extras

## Adaptation Rules

### For Beginners
- Use analogies from everyday life
- Avoid jargon (or explain it immediately)
- More comments in code
- Smaller code examples

### For Intermediates
- Assume basic syntax knowledge
- Focus on "why" over "what"
- Include trade-offs
- Show idiomatic patterns

### For Advanced Topics
- Reference official documentation
- Discuss internal implementation when relevant
- Include performance implications
- Mention related patterns

## Example Session

```
User: /learn:teach useEffect

Claude: ## useEffect

**In one sentence**: useEffect lets you run side effects (data fetching, subscriptions, DOM changes) after React renders a component.

### Why It Matters

React components are pure functions that render UI. But real apps need to interact with the outside world—APIs, browser events, timers. useEffect is the bridge between React's declarative world and imperative side effects.

### Minimal Example

\`\`\`jsx
import { useEffect, useState } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setSeconds(s => s + 1);
    }, 1000);

    return () => clearInterval(id);  // Cleanup
  }, []);  // Empty array = run once

  return <div>{seconds}s</div>;
}
\`\`\`

**Line by line**:
- `useEffect(() => {...}, [])`: Run this function after first render
- `setInterval(...)`: Start a timer (side effect)
- `return () => clearInterval(id)`: Cleanup when component unmounts
- `[]`: Empty dependency array = only run on mount

### Common Mistakes

1. **Missing dependency array**: Without `[]`, effect runs on EVERY render
2. **Forgetting cleanup**: Intervals/subscriptions leak without return function
3. **Stale closures**: Using old state values instead of functional updates

---

**Practice challenge**: Add a pause button that stops and resumes the timer.
```

## Topics Well-Suited for /learn:teach

| Category | Examples |
|----------|----------|
| **React** | hooks, context, suspense, server components |
| **JavaScript** | closures, promises, event loop, prototypes |
| **TypeScript** | generics, mapped types, utility types |
| **Patterns** | SOLID, DI, composition, factories |
| **Backend** | REST, GraphQL, authentication, caching |
| **Database** | indexes, joins, transactions, normalization |
| **DevOps** | containers, CI/CD, infrastructure as code |

$ARGUMENTS
