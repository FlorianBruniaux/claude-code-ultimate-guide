# AI Instructions — {{DEVELOPER_NAME}}
<!-- Generated: {{GENERATED_DATE}} | OS: {{OS}} | Tool: {{TOOL}} -->
<!-- DO NOT EDIT MANUALLY — auto-generated from profile + modules -->
<!-- To update: edit profiles/{{DEVELOPER_SLUG}}.yaml or modules/, then run: -->
<!-- npx ts-node sync-ai-instructions.ts {{DEVELOPER_SLUG}} -->

---

## Project Context

{{MODULE:core-standards}}

---

## Git Workflow

{{MODULE:git-workflow}}

---

## Testing

{{MODULE:test-conventions}}

---

{{#if typescript}}
## TypeScript Rules

{{MODULE:typescript-rules}}

---
{{/if}}

{{#if python}}
## Python Rules

{{MODULE:python-rules}}

---
{{/if}}

## Environment & Paths

{{MODULE:{{OS}}-paths}}

---

{{#if cursor}}
## Cursor-Specific Instructions

{{MODULE:cursor-rules}}

---
{{/if}}

{{#if windsurf}}
## Windsurf-Specific Instructions

{{MODULE:windsurf-rules}}

---
{{/if}}

## Communication Style

{{#if verbose}}
Provide detailed explanations for each decision. Show alternatives considered. Include reasoning.
{{/if}}
{{#if concise}}
Be concise. One sentence per point. Skip obvious details.
{{/if}}
{{#if terse}}
Minimal output. Code only when possible. No explanations unless asked.
{{/if}}
