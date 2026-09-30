---
title: "AI Assistance Disclosure (CONTRIBUTING.md Template)"
description: "CONTRIBUTING.md template section for disclosing AI tool usage in pull requests"
tags: [template, config, ai-ecosystem]
---

# AI assistance disclosure (CONTRIBUTING.md template)

> Copy this section into your project's CONTRIBUTING.md

---

## AI assistance disclosure

If you use any AI tools to help with your contribution, please disclose this
in your pull request description.

### What to disclose

| AI Usage | Example Disclosure |
|----------|-------------------|
| **AI-generated code** | "This PR was written primarily by Claude Code" |
| **AI-assisted research** | "I consulted ChatGPT to understand the codebase" |
| **AI-suggested approach** | "Copilot suggested the algorithm structure" |
| **AI-drafted docs** | "Documentation was drafted with Claude assistance" |

### What doesn't need disclosure

- Trivial autocomplete (single keywords, short phrases)
- IDE syntax helpers (formatting, auto-imports)
- Grammar/spell checking
- Code formatting tools (prettier, black)

### Why we ask

AI-generated code often requires more careful review:

- May use patterns unfamiliar to the codebase
- Could introduce subtle bugs humans wouldn't make
- Might miss project-specific conventions
- Sometimes "looks right" but has logical issues

Disclosure helps maintainers:
- Allocate review time appropriately
- Know where to look more carefully
- Provide better feedback on AI usage

This is a **courtesy to reviewers**, not a judgment on AI use.

### Suggested disclosure format

In your PR description:

```markdown
## AI Assistance

This PR was developed with assistance from [Tool Name].
Specifically:
- [What AI helped with]
- [What you did manually]

All code has been reviewed and understood by the author.
```

---

## Attribution

Based on policies from:
- [Ghostty](https://github.com/ghostty-org/ghostty/blob/main/CONTRIBUTING.md)
- [LLVM](https://llvm.org/docs/DeveloperPolicy.html)
- [Fedora](https://docs.fedoraproject.org/en-US/council/policy/ai-contribution-policy/)

For more context, see [AI Traceability Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ops/ai-traceability.md).
