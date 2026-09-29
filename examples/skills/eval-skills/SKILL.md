---
name: eval-skills
description: "Audit a project or library of skills for metadata, trigger boundaries, workflow completion criteria, local resource closure, instruction economy, tool scope, effort, and routing evidence. Use before shipping skills, after importing a skill collection, or when a skill triggers too often or not at all."
when_to_use: "Trigger phrases: 'audit my skills', 'check skill quality', 'review skills', 'score skills', 'eval skills'. Also use when a user asks why a skill does not trigger automatically, or whether a skill can ship to Claude Code and Codex."
allowed-tools: Read Glob Grep Bash(find *) Bash(claude plugin validate *)
argument-hint: "[path (default: every discovered skill root)]"
effort: medium
---

# Skill Evaluator

Discover every skill in scope, classify its distribution profile, score it on eight criteria, and keep structural validity separate from routing evidence. Every score states the host and profile it applies to.

## When to Use

- Before committing or publishing a skill
- After bulk-importing skills from another project or library
- When a skill triggers too often, too rarely, or only on one host
- When deciding whether a skill can ship to Claude Code, Codex, or an Agent Skills upload

Read every skill in the selected scope. Do not infer collection-wide quality from a sample. When an argument names a path, audit only that path.

---

## Discovery

### Claude Code locations

| Location | Path | Audit note |
|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` | Skip `.trash/`. `synced/` holds skills downloaded from claude.ai: report them, never edit them |
| Project | `.claude/skills/` in the start directory and every parent up to the repository root | Commit-shared |
| Nested | `<subdir>/.claude/skills/<name>/SKILL.md` | Loads once Claude works on files in `<subdir>`. On a name clash both load and the nested one is `/<subdir>:<name>` |
| Additional directory | `.claude/skills/` in a directory passed with `--add-dir` | Session-scoped |
| Command file | `.claude/commands/**/*.md` | Legacy format. Same frontmatter except `name` and `paths` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` or a plugin-root `SKILL.md` | Namespaced as `/<plugin>:<name>` |
| Enterprise | `.claude/skills/` in the managed settings directory | Report only |

Reserved folder names: a folder named `synced` (any case) is skipped in the enterprise, personal, and project locations. Outside a plugin, a folder or command file named `anthropic-skills` or starting with `anthropic-skills:` does not load.

### Codex locations

| Scope | Path |
|---|---|
| Repository | `.agents/skills` in every directory from the working directory up to the repository root |
| User | `~/.agents/skills` |
| Admin | `/etc/codex/skills` |
| System | Bundled with Codex |

Codex follows symlinked skill folders. A skill disabled with a `[[skills.config]]` entry (`enabled = false`) in `~/.codex/config.toml` is reported as disabled, not scored as broken.

```bash
find .claude/skills .agents/skills -name SKILL.md -not -path '*/.trash/*' 2>/dev/null
find .claude/commands -name '*.md' ! -name 'README*' 2>/dev/null
```

**Done when:** every file in scope is listed with its host, location, and the discovery rule that loads it.

---

## Distribution Profiles

Classify each skill before scoring it. The profile decides which fields are valid.

| Profile | Where it runs | Frontmatter it may use |
|---|---|---|
| Claude Code native | Claude Code at any local level, including plugin skills | Every field in the Claude Code table below |
| Agent Skills spec | claude.ai uploads, the Skills API, packaging with `package_skill.py` | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Any other key fails the upload with a hard error |
| Codex | Codex CLI, IDE extension, ChatGPT desktop app | `name` and `description` are required. Display metadata, invocation policy, and tool dependencies go in `agents/openai.yaml` |

A skill published to several profiles follows their intersection. Keeping host-specific fields inside `metadata` to record provenance is valid for a portable skill and is not a defect.

**Done when:** each skill has one declared or inferred profile, with the evidence for the inference.

---

## Claude Code Frontmatter Reference

Claude Code reads frontmatter only when the opening `---` is the file's first line. It ignores an unknown field without reporting an error. When the YAML does not parse, the skill loads with no fields set: `/name` still works, but Claude cannot match the description. Detect parse failures with `claude plugin validate <skills-dir>` (Claude Code v2.1.233 or later). Boolean fields accept `yes`, `no`, `on`, `off`, `1`, and `0` in any case from v2.1.218.

| Field | Notes |
|---|---|
| `name` | In a personal or project skill directory, sets the command shown in `/` and typed to invoke it; the directory name also invokes it. Defaults to the directory name. In a plugin it sets the last segment after the plugin prefix. Command files take their name from the file |
| `description` | What the skill does and when to use it. If omitted, the first non-empty body line is used |
| `when_to_use` | Appended to `description` in the listing and counted in the same cap |
| `argument-hint` | Autocomplete hint such as `[issue-number]` |
| `arguments` | Named positional arguments for `$name` substitution. Space-separated string or YAML list |
| `disable-model-invocation` | `true` removes the description from context: only the user can invoke. Also blocks preloading into subagents and scheduled-task invocation |
| `user-invocable` | `false` hides the skill from `/`; Claude can still invoke it |
| `allowed-tools` | Pre-approves the listed tools for the turn that invokes the skill. It does not restrict tools: every tool stays callable. Space- or comma-separated string, or YAML list. Workspace trust does not gate it |
| `disallowed-tools` | Removes tools from the pool while the skill is active. Cleared on the next message |
| `model` | Model for the rest of the current turn, or `inherit`. A value excluded by `availableModels` is not used |
| `effort` | `low`, `medium`, `high`, `xhigh`, or `max`. Available levels depend on the model |
| `context` | `fork` runs the body as the prompt of a new subagent that does not see the conversation |
| `agent` | Subagent type used with `context: fork` |
| `background` | With `context: fork`, `false` waits for the result in the invoking turn. Default `true` (v2.1.218 or later) |
| `hooks` | Registered when the skill is invoked and kept for the rest of the session. `once: true` removes a hook after its first successful run |
| `paths` | Glob patterns that limit automatic loading. YAML list or comma-separated string |
| `shell` | `bash` (default) or `powershell` for inline command injection |
| `metadata` | Free-form map read by your own tooling. A non-map value is dropped. Do not reuse frontmatter field names as keys |
| `license` | Accepted, not acted on |
| `compatibility` | String up to 500 characters. Accepted, not acted on |

Fields outside this table, such as `tags`, `category`, `keywords`, `usage`, or `args`, have no effect in Claude Code and break an Agent Skills upload. Flag them.

### String Substitutions

| Placeholder | Meaning |
|---|---|
| `$ARGUMENTS` | Full argument string. When no placeholder receives the arguments, Claude Code appends `ARGUMENTS: <value>` |
| `$ARGUMENTS[N]` | Argument at 0-based index N |
| `$N` | Shorthand for `$ARGUMENTS[N]`. Valid without an `arguments:` field |
| `$name` | Named argument declared in `arguments:`. Expands to an empty string when the argument is missing |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_EFFORT}` | Active effort level |
| `${CLAUDE_SKILL_DIR}` | Directory containing this `SKILL.md`. Also substituted in `allowed-tools` Bash rules |
| `${CLAUDE_PROJECT_DIR}` | Project root (v2.1.196 or later). Also substituted in `allowed-tools` Bash rules |
| `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` | Plugin installation and persistent data directories. Plugin skills only |

An indexed placeholder with no matching argument stays in the text unchanged. Escape a literal `$` before a digit, `ARGUMENTS`, or a declared name with a single backslash, as in `\$1.00`. Placeholders such as `${ARGS}` or `%ARGUMENTS%` are passed as literal text. The Codex skills documentation does not describe argument substitution: record Codex behavior for these placeholders as `UNKNOWN` rather than assuming it.

### Listing Budget

- **Claude Code:** the skill listing gets 1% of the model's context window. Each entry's combined `description` and `when_to_use` is capped at 1,536 characters, configurable with `skillListingMaxDescChars`. `skillListingBudgetFraction` or `SLASH_COMMAND_TOOL_CHAR_BUDGET` raise the budget. On overflow, descriptions of the least-invoked skills are dropped first. `skillOverrides` set to `"name-only"` frees budget. `/skill-doctor` (v2.1.252 or later) reports cost and usage per skill.
- **Codex:** the initial list uses at most 2% of the context window, or 8,000 characters when the window is unknown. Codex shortens descriptions first and may omit skills with a warning.

On both hosts, front-load the key use case so a shortened description still matches.

---

## Scoring Criteria (25 points per skill)

| # | Criterion | Max | What is checked |
|---|-----------|-----|-----------------|
| 1 | **identity** | 2 | `name` present with lowercase letters, digits, and hyphens (1), required by Codex; no unresolved name collision on the same host (1) |
| 2 | **context pointer** | 4 | Description identifies the capability (1), names distinct trigger branches (1), leads with discriminating terms (1), and fits the listing cap without synonym stuffing (1) |
| 3 | **profile fit** | 3 | Profile declared or inferable (1); every field valid for that profile (1); tool grants proportionate to the workflow (1) |
| 4 | **invocation and effort** | 2 | Invocation control matches side effects (1); `effort`, when declared, matches the inferred level and the target model supports it (1) |
| 5 | **workflow contract** | 4 | Purpose or boundary is explicit (1), ordered work is actionable (1), each step has an observable completion criterion (1), and no placeholder text remains (1) |
| 6 | **resource closure** | 3 | Required local links resolve (1), required scripts and templates exist (1), and no resource escapes the skill root without an explicit portable contract (1) |
| 7 | **instruction economy** | 3 | One source of truth per rule (1), no instruction merely restates model defaults (1), and branch-only material is disclosed instead of always loaded (1) |
| 8 | **routing evidence** | 4 | Corpus has at least 8 positives and 2 close negatives (1), uses realistic language and boundary cases (1), Claude Code evidence recorded (1), Codex evidence recorded (1) |

**Thresholds**, as a share of applicable points:

- ✅ Good: 80% or more (20 to 25 of 25)
- ⚠️ Needs work: 60% to 79% (15 to 19 of 25)
- ❌ Fix: under 60% (14 or fewer of 25)

An explicitly invoked command wrapper may omit automatic routing evidence. Record it as `explicit-only`, verify that each requested host can discover it, and score it out of 21: Good 17 or more, Needs work 13 to 16, Fix 12 or fewer.

### Identity review

Resolve collisions with each host's rule. Claude Code: enterprise over personal over project; a skill over a command file; a local skill replaces a bundled command but not its aliases; a nested skill and a root skill both load; plugin skills are namespaced. Codex does not merge skills that share a `name`: both can appear in selectors, which is a collision to report.

### Context pointer review

Treat the description and `when_to_use` text as the pointer that decides whether the skill loads. List branches, not synonym piles. A branch is a different kind of request handled by different instructions. If two descriptions can both claim the same prompt, record the collision as a correctness defect.

### Profile fit review

- **Claude Code native:** `allowed-tools` is a pre-approval, so an unscoped `Bash` entry lets every shell command run without a prompt during that turn, even in an untrusted repository. For a read-only workflow, pre-approve only the commands it runs, such as `Bash(git status *)` or `Bash(${CLAUDE_SKILL_DIR}/scripts/check.sh *)`. Use `disallowed-tools` when an autonomous skill must never call a tool, such as `AskUserQuestion` in a background loop. A native skill with no `allowed-tools` is not penalized: the user's permission settings apply.
- **Agent Skills spec:** any field outside the six allowed keys fails the criterion.
- **Codex:** `name` and `description` present; `agents/openai.yaml`, when present, parses and its `dependencies.tools` entries name available tools.
- **Portable across hosts:** host-enforcement fields are absent or kept inside `metadata`. Do not recommend adding `allowed-tools` or `effort` to the frontmatter of a portable skill.

### Invocation and effort review

A workflow with side effects, such as deploy, publish, send, or delete, sets `disable-model-invocation: true` for Claude Code and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex, or states why automatic invocation is safe. Missing `effort` is not a defect. A declared `effort` must match the inference below and be supported by the target model: for example, the guide lists no effort parameter for Haiku 4.5.

### Workflow completion review

For each ordered step, identify the condition that permits the next step to begin. Accept commands run, files produced, checks passed, decisions recorded, or explicit reports of blocked evidence. Reject criteria such as "analysis complete" or "understanding reached" when the agent cannot test them.

### Resource closure review

Resolve local Markdown links relative to the file containing them. Also verify scripts, templates, fixtures, and references declared in prose or code examples when execution depends on them. Bundled scripts should be referenced through `${CLAUDE_SKILL_DIR}` in Claude Code rather than a path that depends on the working directory. A missing required resource is a blocker even when the frontmatter and prose score well.

### Instruction economy review

Apply three checks sentence by sentence:

1. Would removing this instruction change likely behavior? If not, flag a no-op.
2. Is the same rule authoritative elsewhere? If yes, keep one source and point to it.
3. Does every invocation need this material? If not, move it behind a branch-specific pointer.

---

## Producing Routing Evidence

Never award a routing point without a recorded run. Record `UNKNOWN` for a host that was not tested.

- **Baseline comparison (both hosts):** run each prompt in a fresh session with the skill available and again with it disabled (`skillOverrides` set to `"off"` in Claude Code, `[[skills.config]]` with `enabled = false` in Codex). A fresh session matters because context left from authoring the skill masks gaps.
- **Claude Code plugin skills:** `claude plugin eval` runs each prompt in an isolated session with and without the plugin; a `tool_used: Skill` grader measures triggering and the command exits non-zero below its threshold.
- **Claude Code description tuning:** the official `skill-creator` plugin from `claude-plugins-official` generates should-trigger and should-not-trigger prompts and measures the hit rate.
- **Codex:** the Codex skills documentation describes no dedicated evaluation command. Replay each prompt in a fresh Codex session and record whether the skill was selected.

**Done when:** each routed skill has a result per host, or `UNKNOWN` with the reason.

---

## Effort Level Inference

Infer a level from the description and body. Report it as a recommendation for Claude Code native skills only.

- **`low`:** mechanical execution with no design decision. Template instantiation, formatting, syncing, fetching. Short sequential workflow, no subagents.
- **`medium`:** bounded analysis and categorization. Reviewing one diff, triaging issues, producing a structured table. At most one or two scoped subagents.
- **`high`:** design decisions, adversarial or cross-system reasoning. Security audits, architecture reviews, scoring against trade-offs. Several subagents or explicit uncertainty sections.
- **`xhigh` or `max`:** exhaustive long-running synthesis. Fan-out across many parallel agents, dynamic workflows, multi-repository scope.

Ultracode is a separate toggle in `/effort` since Claude Code v2.1.284 and no longer implies an effort level. Do not treat the word `ultracode` in a skill body as an effort signal.

If a declared `effort` differs from the inference, flag it:

> ⚠️ Effort mismatch: declared `low`, inferred `high`. Skill spawns four subagents and performs security analysis.

---

## Execution Instructions

### Step 1: Discover

List every skill file in scope with its host and location, using the discovery tables above. **Done when:** the inventory is complete and each entry names its discovery rule.

### Step 2: Classify and parse

For each skill:

1. Read the full file and extract the frontmatter between the first two `---` lines.
2. Record a parse failure when the YAML does not parse, and confirm it with `claude plugin validate <skills-dir>` when Claude Code v2.1.233 or later is available.
3. Assign the distribution profile.
4. Flag fields that are unknown or invalid for that profile.
5. Check substitution placeholders against the table.
6. Resolve required local links, scripts, templates, fixtures, and references.
7. Record ordered steps and the observable completion criterion for each one.
8. Read `evals/scenarios.json` when present and count positives and negatives.

**Done when:** every skill has a parsed record, a profile, and a resource list with each item resolved or missing.

### Step 3: Score and infer

Apply the eight criteria, infer effort, and compare it with any declared value. Check `context: fork` skills for an actionable task body and an `agent` field, and note that a backgrounded fork runs with the narrower background tool set. **Done when:** every criterion has a score and a one-line reason.

### Step 4: Report

```
# Skills Audit: [project name or path]
Date: [today] | Scanned: N skills | Hosts: Claude Code, Codex

## Summary
| Status | Count |
|--------|-------|
| ✅ Good (>=80%) | N |
| ⚠️ Needs work (60-79%) | N |
| ❌ Fix (<60%) | N |
| explicit-only | N |

Profiles: N Claude Code native · N portable · N Codex only
Routing evidence: N both hosts · N one host · N UNKNOWN

---

## Per-Skill Results

### [skill-name] ([score]/25) [✅/⚠️/❌] [profile]

| Criterion | Score | Notes |
|-----------|-------|-------|
| identity | ✅ 2/2 | ok |
| context pointer | ⚠️ 2/4 | Overlaps a neighboring skill |
| profile fit | ⚠️ 2/3 | Unscoped Bash pre-approval for a read-only workflow |
| invocation and effort | ✅ 2/2 | No side effects, no effort declared |
| workflow contract | ⚠️ 2/4 | Two steps have no observable completion criterion |
| resource closure | ❌ 0/3 | Required template does not exist |
| instruction economy | ⚠️ 2/3 | One branch-only reference is always loaded |
| routing evidence | ❌ 0/4 | No corpus; Claude Code and Codex UNKNOWN |

**Effort inference**: `high`. Security analysis with adversarial reasoning.

**Priority fixes** (ordered by impact):
1. Restore the missing required template
2. Separate the overlapping trigger branch from the neighboring skill
3. Scope `allowed-tools` to the commands the workflow runs
4. Add a corpus and record results for both hosts
```

**Done when:** every scanned skill appears once, and the summary counts match the per-skill results.

---

## Fix Summary Format

End with a copy-paste block of recommended `effort` values for Claude Code native skills only, then one count line:

```
## Recommended effort fields (Claude Code native skills)

skill-name-1: effort: low     # mechanical scaffold
skill-name-2: effort: high    # security analysis, spawns agents
```

`N broken resources · N name collisions · N trigger collisions · N invalid fields for profile · N steps without completion criteria · N routing gaps · N effort mismatches`
