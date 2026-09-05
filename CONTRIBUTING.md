# Contributing to Claude Code Ultimate Guide

**Welcome!** Whether you're fixing a typo or adding a new section, every contribution helps developers worldwide master Claude Code.

## Quick Links

- [Report an Issue](../../issues/new)
- [Start a Discussion](../../discussions)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

---

## Ways to Contribute

| Type | Examples | Effort |
|------|----------|--------|
| **Report** | Bugs, outdated info, broken links | 2 min |
| **Improve** | Fix typos, clarify explanations | 5-15 min |
| **Add Examples** | New templates, workflows, hooks | 15-60 min |
| **Translate** | Help reach non-English speakers | Varies |
| **Share** | Your workflows, success stories | 5 min |

**Not sure where to start?** Check [issues labeled `good first issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

---

## Reporting Issues

Found something wrong or have a suggestion?

1. **Search existing issues**: Someone may have reported it
2. **Open a new issue** with:
   - Clear description
   - Location (file, section, line)
   - Your platform (macOS/Linux/Windows)
   - For Windows: PowerShell version

---

## Pull Request Process

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-ultimate-guide.git
cd claude-code-ultimate-guide
```

### 2. Create a Branch

```bash
git checkout -b fix/typo-in-section-3
# or
git checkout -b feature/add-debugging-guide
```

### 2.5. Install Pre-commit Hooks

This repository uses pre-commit hooks to enforce quality gates (markdown lint, YAML validation, version consistency, etc.). Set them up once:

```bash
# macOS/Linux
pip install pre-commit
pre-commit install

# Windows (PowerShell)
pip install pre-commit
pre-commit install
```

Pre-commit will now run automatically on `git commit`. You can also run manually:

```bash
pre-commit run --all-files
```

**What the hooks check:**
- ✓ Markdown formatting consistency
- ✓ YAML syntax validity
- ✓ VERSION file consistency across the repo
- ✓ No broken symlinks or sensitive files

### 3. Make Changes

Follow [Content Guidelines](#content-guidelines) below.

### 4. Test Your Changes

- Preview markdown rendering
- Test code snippets on your platform
- Verify all links work

### 5. Submit PR

Include:
- Clear description of changes
- Why the change is needed
- What you tested

---

## Content Guidelines

### Writing Style

- **Concise**: Bullet points > long paragraphs
- **Practical**: Include examples for every concept
- **Cross-platform**: Support macOS/Linux AND Windows
- **Accurate**: Test all code before submitting

### Documentation Structure

```markdown
## Section Title

Brief intro (1-2 sentences).

### Subsection

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

**Example:**
```bash
code example here
```
```

### Platform-Specific Code

Always provide both when commands differ:

```bash
# macOS/Linux
~/.claude/settings.json

# Windows
%USERPROFILE%\.claude\settings.json
```

---

## Quality Checklist

Before submitting:

- [ ] Markdown renders correctly (preview on GitHub)
- [ ] All links work
- [ ] Code snippets tested on your platform
- [ ] Windows equivalents provided (if applicable)
- [ ] Spell-checked
- [ ] Follows existing style

---

## Windows Contributions (Especially Welcome!)

The maintainer works on macOS. If you're a Windows user:

- Test PowerShell scripts with PS 5.1+
- Verify path handling
- Report Windows-specific issues
- Add batch file alternatives when possible

**Your contributions are especially valuable!**

---

## What We Don't Accept

- Marketing language or promotional content
- Unverified or speculative claims
- Large structural changes without prior discussion
- Breaking changes to existing examples

---

## Recognition

Contributors are recognized through:

- **Git history**: Your commits are permanently attributed
- **GitHub contributors**: Visible on repository page

Significant contributions may be highlighted in release notes.

---

## Questions?

- **General questions**: [GitHub Discussions](../../discussions)
- **Bug reports**: [Issues](../../issues)
- **Direct contact**: [LinkedIn](https://www.linkedin.com/in/florian-bruniaux-43408b83/)

---

**Thank you for helping improve this guide!**
