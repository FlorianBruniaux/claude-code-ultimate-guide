---
name: learn-quiz
description: "Test understanding of recently written or accepted code"
---

# Quiz Me

Test understanding of recently written or accepted code.

## Usage

```
/learn:quiz                     # Quiz on last code worked with
/learn:quiz error handling      # Focus on specific aspect
/learn:quiz --hard              # More challenging questions
```

## Instructions

1. Identify the last code I worked with (wrote, edited, or accepted from AI)
2. Generate 3-5 questions that test understanding at different levels:
   - **Recall**: What does this code do?
   - **Understanding**: Why was this approach chosen?
   - **Application**: What would happen if X changed?
   - **Analysis**: What are the trade-offs of this approach?
   - **Synthesis**: How would you extend this?
3. Present questions one at a time
4. Wait for my answer before revealing the correct response
5. Provide explanations with each answer, not just "correct/incorrect"

## Question Types

### Level 1: Recall
- "What does the function X return?"
- "What parameters does Y accept?"
- "What happens when Z is called?"

### Level 2: Understanding
- "Why do we use X instead of Y here?"
- "What problem does this pattern solve?"
- "Why is this line necessary?"

### Level 3: Application
- "What would happen if we removed line X?"
- "How would you add feature Y to this code?"
- "What would break if input Z was provided?"

### Level 4: Analysis
- "What are the performance implications of this approach?"
- "What edge cases might cause issues?"
- "How does this compare to alternative X?"

### Level 5: Synthesis
- "How would you refactor this for better testability?"
- "What would need to change to support X?"
- "Design an extension that adds Y"

## Focus Areas

When focus is specified (e.g., `/learn:quiz error handling`), prioritize questions about:

| Focus | Question Themes |
|-------|-----------------|
| `error handling` | Try/catch, error types, recovery strategies |
| `performance` | Big-O, optimization, bottlenecks |
| `security` | Input validation, XSS, injection |
| `testing` | Test cases, edge cases, mocking |
| `architecture` | Patterns, separation of concerns, SOLID |
| `types` | TypeScript types, inference, generics |

## Difficulty Modes

### Default
- 3 questions
- Mix of Level 1-3
- Focus on understanding current code

### `--hard`
- 5 questions
- Levels 3-5
- Include hypothetical modifications
- Ask about trade-offs and alternatives

## Response Format

For each question:

```
## Question 1 of 3

[Question text]

What's your answer?

---
(After user responds)

### Feedback

[Whether correct and why]

**Key insight**: [The concept this tests]

**Related concept**: [Something to explore further]

Ready for the next question?
```

## After Quiz Complete

Summarize:
- Score: X/Y correct
- Strengths: [Topics understood well]
- Review needed: [Topics to revisit]
- Suggested practice: [Specific exercise]

## Example Session

```
User: /learn:quiz

Claude: Looking at your last code - the useEffect hook for data fetching.

## Question 1 of 3

In your useEffect, you have an empty dependency array [].
What does this mean for when the effect runs?

User: It runs only once when the component mounts

Claude: ### Feedback
Correct! An empty dependency array means the effect runs only on mount
(and cleanup on unmount).

**Key insight**: The dependency array controls WHEN effects re-run.

**Related concept**: What happens with no array vs. [someValue]?

Ready for Question 2?
```

## Tips for Users

1. **Be honest** — Wrong answers are learning opportunities
2. **Explain your reasoning** — Helps identify gaps even in correct answers
3. **Ask follow-ups** — If feedback is unclear, dig deeper
4. **Track weak areas** — Note topics that need more practice

$ARGUMENTS
