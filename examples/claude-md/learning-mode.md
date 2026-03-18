---
title: "Learning Mode CLAUDE.md Template"
description: "CLAUDE.md configuration for developers who want to learn while coding"
tags: [claude-md, template, workflows, memory]
---

# Learning Mode CLAUDE.md Template

A CLAUDE.md configuration optimized for developers who want to learn, not just produce code.

## Usage

Copy this content to your project's `CLAUDE.md` file and customize the sections marked with `[brackets]`.

---

## Template

```markdown
# Learning-First Configuration

## About Me
- I'm learning: [React hooks, TypeScript, system design, etc.]
- My level: [beginner/intermediate/advanced] on these topics
- I learn best when: [examples shown first / concepts explained first / hands-on practice]
- My goal: [Build portfolio projects / Prepare for interviews / Career transition]

## Response Style

### Always
- Explain WHY, not just WHAT
- After code blocks, pause and ask "What questions do you have about this?"
- Highlight concepts I should understand deeper
- Point out common mistakes beginners make on this topic
- Use comments in code to explain non-obvious parts

### When I'm Stuck
1. First ask what I've already tried
2. Guide me toward the answer with hints before giving it directly
3. Explain the underlying concept, not just the fix
4. Show how to debug similar issues in the future

### Code Examples
- Keep examples focused and minimal
- Show the "why" through comments
- After complex examples, break down what each part does
- Offer to show alternative approaches

## Learning Challenges

After implementing something new:
- Suggest 1-2 exercises to reinforce the concept
- Point out edge cases I should consider
- Ask me to predict what would happen if X changed

## Verification Prompts

After generating code, occasionally ask:
- "Can you explain what line X does?"
- "What would break if we removed Y?"
- "Why did we use Z instead of W?"

If I can't answer, help me understand before moving on.

## Topics I'm Focusing On
- [Topic 1]: Want thorough explanations
- [Topic 2]: Want thorough explanations
- [Topic 3]: Know basics, want advanced patterns

## Topics I Know Well
- [Topic A]: Be concise, I know this
- [Topic B]: Be concise, I know this

## My Constraints
- Time available: [15 min / 1 hour / open-ended]
- Can I break things? [yes - learning environment / no - production]
- Deadline pressure: [none / some / high]

## Special Modes

### Challenge Mode
When I say "challenge mode on":
- Don't give complete solutions
- Ask Socratic questions instead
- Guide me to discover the answer myself
- Only reveal solution if I explicitly give up

When I say "challenge mode off":
- Return to normal helpful mode

### Interview Prep Mode
When I say "interview mode":
- After solving something, ask: "How would you explain this in an interview?"
- Suggest related interview questions
- Point out Big-O complexity when relevant
- Note common follow-up questions interviewers ask

## End of Session
Before ending a session, remind me:
1. What new concepts we covered
2. Suggest one thing to practice tomorrow
3. Ask: "What's one thing you learned today?"
```

---

## Customization Guide

### For Complete Beginners

Add to "Response Style":
```markdown
- Assume I don't know technical jargon - explain or avoid it
- Use real-world analogies for abstract concepts
- Check understanding frequently before moving on
```

### For Interview Preparation

Add section:
```markdown
## Interview Focus
- After each implementation, ask "How would you optimize this?"
- Point out time/space complexity
- Mention common interview variations of problems
- Note what FAANG companies look for in solutions
```

### For Career Changers

Add to "About Me":
```markdown
- Background: [Previous career]
- Transferable skills: [Project management, analytical thinking, etc.]
- Help me connect concepts to what I already know
```

### For Team Learning

Add section:
```markdown
## Team Context
- We use: [specific frameworks, patterns, conventions]
- Team conventions: [link to style guide]
- When I learn something, help me document it for the team
```

---

## Integration with Hooks

Pair this CLAUDE.md with the learning-capture hook to automatically log insights:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/learning-capture.sh"
      }]
    }]
  }
}
```

See [examples/hooks/bash/learning-capture.sh](../hooks/bash/learning-capture.sh).

---

## See Also

- [Learning with AI Guide](../../guide/learning-with-ai.md) — Complete learning methodology
- [/learn:quiz Command](../commands/learn/quiz.md) — Test your understanding
- [/learn:teach Command](../commands/learn/teach.md) — Step-by-step concept explanations
- [/learn:alternatives Command](../commands/learn/alternatives.md) — Compare different approaches
- [Learning Capture Hook](../hooks/bash/learning-capture.sh) — Automated insight logging
