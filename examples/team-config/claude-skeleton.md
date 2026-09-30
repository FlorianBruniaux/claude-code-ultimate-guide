# AI instructions: {{DEVELOPER_NAME}}
<!-- Generated: {{GENERATED_DATE}} | OS: {{OS}} | Tool: {{TOOL}} -->
<!-- DO NOT EDIT MANUALLY — auto-generated from profile + modules -->
<!-- To update: edit profiles/{{DEVELOPER_SLUG}}.yaml or modules/, then run: -->
<!-- npx ts-node sync-ai-instructions.ts {{DEVELOPER_SLUG}} -->

---

## Project context

{{MODULE:core-standards}}

---

## Git workflow

{{MODULE:git-workflow}}

---

## Testing

{{MODULE:test-conventions}}

---

{{#if typescript}}
## TypeScript rules

{{MODULE:typescript-rules}}

---
{{/if}}

{{#if python}}
## Python rules

{{MODULE:python-rules}}

---
{{/if}}

## Environment & paths

{{MODULE:{{OS}}-paths}}

---

{{#if cursor}}
## Cursor-specific instructions

{{MODULE:cursor-rules}}

---
{{/if}}

{{#if windsurf}}
## Windsurf-specific instructions

{{MODULE:windsurf-rules}}

---
{{/if}}

## Communication style

{{#if verbose}}
Provide detailed explanations for each decision. Show alternatives considered. Include reasoning.
{{/if}}
{{#if concise}}
Be concise. One sentence per point. Skip obvious details.
{{/if}}
{{#if terse}}
Minimal output. Code only when possible. No explanations unless asked.
{{/if}}
