# Greptile Review Rules: Template

<!--
  Copy to .greptile/rules.md at repo root, then replace every placeholder section
  with your project's actual conventions. Greptile's value over Claude Code Action
  is cross-file RAG search: dependency chains, "who else calls this," patterns that
  repeat across distant files. Don't ask it to re-check what Claude/CodeRabbit already
  cover on this repo (see the non-duplication note below), let it specialize instead.
-->

**Non-duplication note**: this rulebook should NOT restate what `.github/prompts/code-review.md`
(Claude Code Action) or `.coderabbit.yaml` (CodeRabbit) already check on this repo. If a rule
appears in more than one config, one of the three has to give it up. Pick whichever tool has
the best vantage point for that specific check (see the architecture doc for the split-rule table).

---

## 1. Architecture conventions

<!-- Example: layering rules, forbidden imports between modules, naming conventions -->

- [ ] Describe your layering pattern here (e.g., "Controller → Service → Repository, no layer skipping")
- [ ] List forbidden cross-module imports
- [ ] Note any codegen boundaries (generated files reviewers should skip)

## 2. Business invariants

<!--
  This is the section that benefits most from Greptile's cross-file search: invariants
  that span multiple files and are easy to violate without noticing (a status enum with
  transition rules enforced in one service but not another, a scoping rule that must apply
  to every new query on a given table, etc).
-->

- [ ] List state machines and their valid transitions
- [ ] List scoping rules that must apply to every query on sensitive tables
- [ ] List fields that must never be exposed to certain roles/endpoints

## 3. Security

<!-- Only list checks NOT already owned by Claude Code Action's prompt or CodeRabbit's path_instructions -->

- [ ] Describe secrets/credentials handling conventions
- [ ] Describe any project-specific auth/permission patterns

## 4. Code conventions

- [ ] Formatting/linting already enforced by CI, do not re-flag (list the tool, e.g. ESLint/Ruff/rustfmt)
- [ ] Project-specific idioms worth flagging when violated

## 5. Accessibility (if applicable)

- [ ] List WCAG-relevant patterns specific to your component library

## 6. Data integrity

- [ ] List invariants a migration or schema change must never break
