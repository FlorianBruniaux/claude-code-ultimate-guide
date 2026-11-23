---
name: ast-grep-patterns
description: "Structural code search and refactoring with ast-grep: choose it over Grep, then write tested pattern and YAML rule recipes. Use when renaming calls or changing an API signature across a large codebase, migrating a framework, or finding code by shape (async functions without try/catch, empty catch blocks, long parameter lists). Not for plain text searches, which Grep handles faster."
effort: low
---

# ast-grep patterns

ast-grep matches code by syntax tree, so it survives formatting differences and needs no regex escaping. The patterns below were run against ast-grep 0.51.3 on small TypeScript and TSX samples. Test each one on a small file before running it across a repository.

## Install

```bash
brew install ast-grep            # or: npm install --global @ast-grep/cli
ast-grep --version
```

The binary is `ast-grep` (alias `sg`). An optional agent skill is published at `ast-grep/agent-skill` (install command not verified here).

## When to use it

| Request | Tool |
|---------|------|
| Find a string, a name, an import | Grep |
| Find code by meaning ("where is auth handled") | A semantic search tool such as grepai, or an LSP or symbol-aware MCP server |
| Find or rewrite code by structure | ast-grep |
| Rename every call, change an API signature, migrate a framework | ast-grep |

For a small project or a one-off lookup, Grep is enough. ast-grep pays off when the same structural change touches many files.

## Quick commands

```bash
# One-off pattern ($X = one node, $$$X = zero or more nodes)
ast-grep run -p 'console.log($$$ARGS)' -l ts src/

# Rewrite (preview first, then add --update-all to apply)
ast-grep run -p 'oldApi($A)' -r 'newApi($A)' -l ts src/

# Run a YAML rule file
ast-grep scan -r rules/async-no-try.yml src/

# Machine-readable output
ast-grep run -p 'class $C extends React.Component { $$$ }' -l tsx --json=compact src/

# Print the syntax tree of a pattern when it does not match
ast-grep run --debug-query=ast -p 'foo($A)' -l ts
```

The language is required for `run`; use `ts` for `.ts` files and `tsx` for `.tsx` files, because a rule written for one does not scan the other.

## Rule recipes

Each recipe is saved as a rule file (`id`, `language`, `rule`) and run with `ast-grep scan -r <file> <path>`.

### Async functions without try/catch

```yaml
id: async-no-try
language: tsx
rule:
  pattern: async function $F($$$P) { $$$B }
  not:
    has:
      kind: try_statement
      stopBy: end
```

`stopBy: end` makes `has` search the whole subtree instead of only direct children. Without it the rule reports functions that do have a nested `try`.

### useEffect without a cleanup function

```yaml
id: effect-no-cleanup
language: tsx
rule:
  pattern: useEffect(() => { $$$B })
  not:
    has:
      pattern: return () => { $$$C };
      stopBy: end
```

Only effects with a block body and no dependency array match the pattern. Add a second pattern with `, [$$$D]` for effects that declare dependencies.

### Functions with more than five parameters

```bash
ast-grep run -p 'function $N($A, $B, $C, $D, $E, $F, $$$R) { $$$ }' -l ts src/
```

### Empty catch blocks

```bash
ast-grep run -p 'try { $$$T } catch ($E) {}' -l ts src/
```

A catch block that holds only a comment is also reported, because comments are not statements.

### Deprecated lifecycle methods

```yaml
id: deprecated-lifecycle
language: tsx
rule:
  kind: method_definition
  has:
    field: name
    regex: "^(componentWillMount|componentWillReceiveProps|componentWillUpdate)$"
```

A bare `componentWillMount() { $$$B }` is not a valid pattern (it parses as several nodes), so match the node kind and filter its name instead.

### Template-literal SQL (injection risk)

```yaml
id: sql-template
language: tsx
rule:
  pattern: db.query($Q)
  has:
    kind: template_substitution
    stopBy: end
```

Matches only queries built with `${...}` interpolation, not static template strings.

### Functions without an explicit return type

```yaml
id: no-return-type
language: tsx
rule:
  kind: function_declaration
  not:
    has:
      field: return_type
      kind: type_annotation
```

### innerHTML assignments

```bash
ast-grep run -p '$E.innerHTML = $V' -l ts src/
```

### Hardcoded secret-looking properties

```yaml
id: secret-literal
language: tsx
rule:
  kind: pair
  has:
    field: key
    regex: "(?i)^(password|secret|api_?key|token)$"
  all:
    - has:
        field: value
        kind: string
```

A metavariable must be a whole node: `password: "$P"` does not bind inside the string, which is why this rule filters by key and value kind instead.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Pattern matches nothing | Print the tree with `--debug-query=ast` and compare it with the code. A pattern must be one complete syntax node. |
| "Multiple AST nodes are detected" | The pattern is a fragment. Match the enclosing node by `kind` and add `has` or `regex`. |
| Rule scans nothing | Check `language` against the file extension (`typescript` vs `tsx`). |
| "Rule must have one positive matcher" | A `not` or `has` with only `field` is not enough. Add `kind` or `pattern`. |
| Slow on a large repository | Narrow the path, set `-l`, or use `--globs` to skip generated files. |
| Claude reaches for Grep | Ask explicitly: "use ast-grep to find ...". |

## Prompt templates

Large refactor:

```
Use ast-grep to find every call to [OLD_API] in [DIRECTORY], list the affected files,
and propose a phased rewrite. Analysis only: wait for my approval before applying a rewrite.
```

Framework migration:

```
Use ast-grep to find deprecated [FRAMEWORK] APIs in [DIRECTORY], map each to its
replacement, and order the migration by risk. Do not apply changes.
```

## Resources

- ast-grep documentation: https://ast-grep.github.io/
- Pattern playground: https://ast-grep.github.io/playground.html
- Source: https://github.com/ast-grep/ast-grep
