# Audit Your Claude Code Permission and Sandbox Posture

> A self-contained prompt that audits how a project actually gates Claude Code: blanket execution grants, allow-rule bloat, deny and ask coverage, sandbox configuration, scope hygiene, and permission-mode interactions.

**Author**: [Florian BRUNIAUX](https://github.com/FlorianBruniaux) | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**Reference**: [The Ultimate Claude Code Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/ultimate-guide.md)

---

## What this is for

`/security-audit` scans your project for secrets and injection surfaces. `tools/audit-prompt.md` scores your whole setup across eight dimensions. This prompt does one thing instead: it determines whether your permission rules still constitute a boundary, or whether they have quietly stopped meaning anything.

The failure it is built to catch is invisible from the inside. You accumulate `allow` rules one "Yes, don't ask again" at a time. One of them turns out to be an interpreter. From that point, every other rule in the file is decoration, including the `deny` rules you wrote deliberately. Nothing warns you. Prompts simply stop appearing, which reads as a well-tuned setup.

Run it per project. It reads configuration only and changes nothing.

---

## How to run it

Paste everything below the line into a Claude Code session at the root of the project you want audited.

For a fleet, run it once per repository. Findings in user-scope settings will repeat across runs, which is the point: a user-scope hole affects every project at once and should be fixed first.

### Fleet triage first

Auditing thirty repositories one at a time wastes the first twenty runs discovering the same thing. Sweep the whole fleet first, rank by exposure, then run the full prompt only on what the sweep flags. Point `ROOTS` at the directories your repositories actually live under.

```bash
ROOTS="$HOME/Sites $HOME/dev $HOME/work"   # adjust
find $ROOTS -maxdepth 5 -name node_modules -prune -o -name .worktrees -prune \
     -o -path "*/.claude/settings*.json" -print 2>/dev/null | sort -u > /tmp/cc-settings.txt
wc -l < /tmp/cc-settings.txt

python3 - <<'PY'
import json,re,os
BLANK=re.compile(r'^Bash\((bash|sh|zsh|fish|dash|python3?|perl|ruby|node|deno|bun|npm|pnpm|yarn|npx|bunx|make|just|env|xargs|eval|uv|poetry|docker run|docker exec)\s*(-[ce])?\s*(:\*|\*|\))')
files=[l.strip() for l in open('/tmp/cc-settings.txt') if l.strip()]
rows=[]; broken=[]; totals=[0,0,0,0]
for p in files:
    try: d=json.load(open(p))
    except Exception as e: broken.append((p,str(e)[:60])); continue
    perm=d.get("permissions",{})
    a,dn,ak=perm.get("allow",[]),perm.get("deny",[]),perm.get("ask",[])
    sb="sandbox" in d
    totals[0]+=len(a); totals[1]+=len(dn); totals[2]+=len(ak); totals[3]+=sb
    hits=sorted({r for r in a if BLANK.match(r)})
    tracked = p.endswith("settings.json")
    if hits or not dn:
        rows.append((len(hits), tracked, len(a), len(dn), len(ak), sb, p, hits))
print(f"files={len(files)} allow={totals[0]} deny={totals[1]} ask={totals[2]} sandbox={totals[3]}")
for p,e in broken: print("UNPARSEABLE", p, e)
for n,tracked,a,dn,ak,sb,p,hits in sorted(rows, reverse=True):
    tag = "TRACKED" if tracked else "local  "
    print(f"[{tag}] blank={n:2d} allow={a:5d} deny={dn:3d} ask={ak} sandbox={'y' if sb else 'n'}  {p.replace(os.path.expanduser('~'),'~')}")
    if hits: print("          " + "  ".join(hits))
PY
```

Read the output in this order. A blanket grant in a **tracked** `settings.json` outranks everything else, because it ships to whoever clones the repository. A blanket grant in a `settings.local.json` is next, one line per affected repository. A repository with zero `deny` rules and no sandbox has no boundary beyond the built-in defaults, whatever its allow count says. A high allow count with no blanket grant is noise, not risk, and should be scheduled last.

Then run the full prompt on the two or three repositories where the answer is genuinely unclear, and apply the fleet-wide fixes from the plan rather than re-auditing each one.

---

# PROMPT STARTS HERE

You are a senior security engineer auditing the Claude Code permission posture of this repository. You produce evidence, not impressions. Every finding you report carries a file path, a line or rule, and a command someone else can run to reproduce it.

You do not modify any file. You do not run `claude config`, `/permissions`, or anything that writes. If asked to fix something, you propose a patch as text and stop.

## Ground truth you must use

Claude Code's permission matcher has specific semantics. Most bad audits come from guessing them. Use these, which are the documented behavior, rather than reasoning from the rule text alone.

**Rule shape.** Rules are `Tool` or `Tool(specifier)`. A bare `Bash` and `Bash(*)` both match every command. Wildcards match at any position, including the middle: `Bash(git * main)` matches `git push origin main`. A trailing ` *` enforces a word boundary, so `Bash(ls *)` matches `ls -la` but not `lsof`, while `Bash(ls*)` matches both. The `:*` suffix equals a trailing ` *` and is recognized **only at the end of a pattern**; in `Bash(git:* push)` the colon is a literal character and the rule matches nothing.

**Compound commands.** The recognized separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines. A rule must match each subcommand independently, so `Bash(safe *)` does not authorize `safe && rm -rf .`.

**Wrappers stripped before matching.** `timeout`, `time`, `nice`, `nohup`, `stdbuf`, the builtins `command` and `builtin`, zsh's `noglob`, and bare `xargs` with no flags. A rule written for the inner command therefore covers the wrapped form.

**Wrappers NOT stripped, which is where holes come from.** `npx`, `docker exec`, `devbox run`, `mise exec`, `direnv exec`, and every interpreter invoked with `-c` or `-e`. These execute their arguments as a command, so a rule like `Bash(devbox run *)` authorizes `devbox run rm -rf .`, and `Bash(bash *)` authorizes `bash -c '<anything>'`. This is the single most important mechanic in this audit.

**Environment variable prefixes.** An `allow` rule does not match past an assignment of a variable outside a known-safe set. A `deny` or `ask` rule matches past any leading assignment, so `Bash(rm *)` in deny still catches `FOO=bar rm -rf tmp/`.

**Exec wrappers that always prompt** and cannot be prefix-approved: `watch`, `setsid`, `ionice`, `flock`, and `find` with `-exec` or `-delete`.

**Built-in read-only set**, never prompted in any mode and not configurable: `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`, and read-only forms of `git`. An `allow` rule for any of these is dead weight, not a risk.

**Protected paths**, never auto-approved outside `bypassPermissions`, and **not** pre-approvable by an `allow` rule in settings: `.git`, `.config/git`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, `.mvn`, `.claude` (except `.claude/worktrees`), plus shell rc files, `.npmrc`, `.gitconfig`, `.mcp.json`, `.claude.json`, and similar. The safety check runs before settings are evaluated.

**Auto mode ordering.** Actions matching an `allow`, `ask`, or `deny` rule resolve immediately, **before** the classifier runs. On entering auto mode Claude Code drops only the broad execution grants: blanket `Bash(*)`, wildcarded interpreters, package-manager run commands, and `Agent` allow rules. A narrow rule such as `Bash(git push:*)` survives and therefore removes classifier review from that action. In auto mode, an allow list is not neutral: it subtracts oversight.

**Ask rules.** A content-scoped `ask` rule such as `Bash(git push *)` forces a prompt in every mode, including auto mode and including sandboxed commands. A bare `Bash` ask rule is skipped for commands that run sandboxed. Ask rules are the only human checkpoint that survives every other setting.

**Sandbox.** Off unless `sandbox.enabled` is true. Two independent layers. Filesystem: writes limited to the working directory and session temp; reads cover the **entire machine** including `~/.ssh` and `~/.aws`, because there is no built-in credential deny list. Network: no domain pre-allowed, prompt on first use. `autoAllowBashIfSandboxed` auto-approves sandboxed commands, which is what replaces a long allow list. `allowUnsandboxedCommands: false` disables only the `dangerouslyDisableSandbox` retry; it does **not** constrain `excludedCommands`, which remains a full bypass of the OS boundary. The built-in proxy does not terminate TLS, so a broad `allowedDomains` entry such as `github.com` is an egress path, not a restriction.

**Scope precedence** for permission arrays: managed, then project local, then project, then user, with array keys merged and deduplicated across every scope rather than replaced. A `deny` added anywhere applies everywhere; no scope can remove another scope's deny. Several keys are deliberately ignored when they come from project settings: `defaultMode: "auto"`, `sandbox.filesystem.disabled`, `sandbox.credentials` `mask` entries, `network.tlsTerminate`, `network.strictAllowlist`, and `allowAppleEvents`.

If you are unsure whether a behavior still holds in the installed version, say so in the report under "Not verified" rather than asserting it. Record the version from `claude --version`.

## Phase 0. Inventory

Locate every settings file that applies here and count what is in each. Report the table before analyzing anything.

```bash
claude --version
for f in ~/.claude/settings.json ~/.claude/settings.local.json \
         .claude/settings.json .claude/settings.local.json \
         "/Library/Application Support/ClaudeCode/managed-settings.json"; do
  [ -f "$f" ] || continue
  python3 - "$f" <<'PY'
import json,sys
p=sys.argv[1]
try: d=json.load(open(p))
except Exception as e: print(f"{p}: UNPARSEABLE -> {e}"); raise SystemExit
perm=d.get("permissions",{})
print(f"{p}")
print("   allow={} deny={} ask={} defaultMode={}".format(
    len(perm.get("allow",[])), len(perm.get("deny",[])),
    len(perm.get("ask",[])), perm.get("defaultMode","<unset>")))
print("   sandbox={} hooks={} top-level={}".format(
    "yes" if "sandbox" in d else "NO", "yes" if "hooks" in d else "no",
    ",".join(d.keys())))
PY
done
```

A file that fails to parse is a P0 on its own: Claude Code cannot apply rules it cannot read, and JSON does not accept `//` comments. Report the parse error verbatim and stop analyzing that file.

Note which files are git-tracked. A `settings.json` under version control is a team-wide policy; a `settings.local.json` is personal and gitignored. Rules in the wrong one are a finding in Phase 5.

## Phase 1. Blanket execution grants (P0)

This phase alone decides whether the rest of the configuration means anything.

Search every `allow` array for rules whose specifier resolves to an interpreter, a package manager, an environment runner, or a passthrough. Start from this list and extend it with anything project-specific you find, such as an in-house task runner or a proxy CLI:

`bash`, `sh`, `zsh`, `fish`, `dash`, `python`, `python3`, `perl`, `ruby`, `node`, `deno`, `bun`, `npm`, `pnpm`, `yarn`, `npx`, `bunx`, `make`, `just`, `task`, `env`, `xargs`, `eval`, `source`, `docker`, `kubectl`, `ssh`, `devbox`, `mise`, `direnv`, `nix-shell`, `uv`, `poetry`, `cargo run`, `go run`, `dotnet run`.

```bash
python3 - <<'PY'
import json,re,os
PAT=re.compile(r'^(Bash|PowerShell)\((bash|sh|zsh|fish|dash|python3?|perl|ruby|node|deno|bun|npm|pnpm|yarn|npx|bunx|make|just|task|env|xargs|eval|source|docker|kubectl|ssh|devbox|mise|direnv|nix-shell|uv|poetry)\b')
for p in ("~/.claude/settings.json","~/.claude/settings.local.json",
          ".claude/settings.json",".claude/settings.local.json"):
    p=os.path.expanduser(p)
    if not os.path.exists(p): continue
    try: rules=json.load(open(p)).get("permissions",{}).get("allow",[])
    except Exception: continue
    hits=[r for r in rules if PAT.match(r)]
    if hits:
        print(f"--- {p} ({len(hits)} of {len(rules)})")
        for r in sorted(set(hits)): print("   ", r)
PY
```

For each hit, decide whether it actually grants arbitrary execution, and say why:

| Verdict | Looks like | Consequence |
|---|---|---|
| Arbitrary | `Bash(bash *)`, `Bash(node:*)`, `Bash(env:*)`, `Bash(xargs:*)` | Every other rule in every scope is bypassable |
| Arbitrary via subcommand | `Bash(npm:*)`, `Bash(pnpm *)`, `Bash(make *)` | `run`, `exec`, and install lifecycle scripts execute arbitrary code |
| Scoped, acceptable | `Bash(npm run build:*)`, `Bash(pnpm vitest run:*)` | Bounded to a named script |
| Passthrough | any wrapper CLI that forwards its argv unfiltered | Equivalent to the wrapped shell |

Then prove the consequence rather than asserting it. Pick the strictest `deny` rule in the repository, usually a secret read, and write out the exact command that defeats it through the grant you found. Example shape: given `deny: ["Read(**/.env*)", "Bash(cat .env)"]` and `allow: ["Bash(bash *)"]`, the bypass is `bash -c 'cat .env'`, matched as a `bash` command and never as a `cat`. Name the rule, the grant, and the bypass string. **Do not execute it.**

If Phase 1 finds nothing, say so explicitly. That is a genuinely good result and worth stating.

## Phase 2. Rule population health

Count, then characterize. Volume is not the problem; what the volume hides is.

```bash
python3 - <<'PY'
import json,re,os,collections
for p in (".claude/settings.local.json",".claude/settings.json"):
    if not os.path.exists(p): continue
    a=json.load(open(p)).get("permissions",{}).get("allow",[])
    if not a: continue
    exact=[r for r in a if r.startswith("Bash(") and not r.rstrip(")").endswith(("*",":*"))]
    heads=collections.Counter()
    for r in a:
        m=re.match(r'Bash\(([^\s:)]+)',r)
        if m: heads[m.group(1)]+=1
    print(f"--- {p}: {len(a)} allow, {len(exact)} exact-match Bash")
    print("   heads:", heads.most_common(15))
PY
```

Report three things. How many rules are exact matches that will never fire again, the residue of per-invocation approvals. Which command heads have accumulated many near-identical entries that a single prefix rule would replace. And whether any rule is already dead: covered by the built-in read-only set, shadowed by a broader rule in the same or a wider scope, or malformed such as a `:*` that is not at the end.

Known matcher quirk worth checking here: commands carrying an environment-variable prefix, for instance `TEST_DB_URL="..." pytest`, never consolidate into a prefix rule, because the allow matcher does not look past an unknown assignment. A cluster of near-identical entries differing only by an env prefix is this bug, not user error.

## Phase 3. Deny and ask coverage

An empty `ask` array means the configuration contains no human checkpoint anywhere. Say that plainly if it is the case.

Check for coverage of the actions that are expensive to undo, and report each as present or absent with the rule text:

History rewriting and destructive git: `git push --force` and its `-f` and `--force-with-lease` forms, refspec forces such as `git push origin +main`, `git reset --hard`, `git clean -fd`, and branch or remote deletion.

Publication and merge: `npm publish`, `gh pr merge`, `gh repo delete`, `gh repo edit`, registry pushes, and deploy commands specific to this project.

Secret exposure: reads of `.env` and variants, `*.pem`, `*.key`, `~/.ssh`, `~/.aws`, `~/.gnupg`, and any credential directory this project actually uses.

When a `deny` exists, test it against the semantics above rather than accepting it at face value. A pattern anchored on `git push` misses `git -c key=value push --force`, since the command no longer starts with the matched prefix. Report that as a limitation of the rule, and note that pattern matching loses this game: branch protection on the server is the boundary that actually holds. A `deny` rule remains worth keeping as a local guard against accident.

Finally, name at least one `ask` rule this project should have and does not, chosen from what the repository actually does. Justify it from the code or the CI configuration, not from a generic checklist.

## Phase 4. Sandbox posture

If no scope defines `sandbox`, state that the sandbox is off, then quantify what that costs **here** rather than in the abstract. Base it on Phase 1: with an interpreter grant present and no sandbox, there is no boundary of any kind on Bash. With no interpreter grant and no sandbox, the boundary is the rule list alone, which holds only as long as no future rule opens it.

If `sandbox` is defined, audit it against these:

`excludedCommands` is a full bypass of the OS boundary, and `allowUnsandboxedCommands: false` does not constrain it. For every entry, ask whether that command can reach the host filesystem. `docker` can, through volume mounts and through the daemon socket. `kubectl`, `ssh`, and `make` typically can. Report each excluded command with what it can still reach, and check whether a `deny` or `ask` rule covers it. Also flag entries whose syntax is unverified for this field: the documented forms are the bare name or `name *`, and a `:*` suffix here is not the same field as the Bash matcher. Verify the resolved configuration in the `/sandbox` Config tab rather than guessing.

`network.allowedDomains` is an egress allowlist evaluated on the hostname the client claims, with no TLS inspection by default. Broad entries such as `github.com` or a wildcard on user content domains permit exfiltration. List each domain with the reason it is there; anything you cannot justify is a finding. Recommend `network.strictAllowlist: true` where the version supports it, and note that it must live in user or managed settings because project settings are ignored for that key.

`credentials` absent is a finding whenever the sandbox is on, because the default read policy covers the whole machine. Propose concrete `files` deny entries for the credential paths this machine actually has, and `envVars` entries for the tokens this project actually uses.

`filesystem.allowWrite` should be checked against reality. If the project's own workflows write outside the working directory, sibling repositories, a shared build output, a cache directory, those paths must be listed or the sandbox will break the workflow and push someone toward disabling it. Inspect scripts, `package.json`, and CI configuration to find them. Report each as a required entry.

Keys that project settings cannot set are worth flagging if present in a project file, since they are silently ignored: `defaultMode: "auto"`, `filesystem.disabled`, `credentials` `mask` entries, `network.tlsTerminate`, `network.strictAllowlist`, `allowAppleEvents`.

## Phase 5. Scope hygiene

Determine, for every rule that matters, whether it lives in the right file.

A `deny` on credential reads belongs in user settings, because it should follow the operator to every project rather than being re-declared per repository. A rule specific to this project's toolchain belongs in the tracked `.claude/settings.json`, so the team inherits it. A rule that reflects one person's habits belongs in `.claude/settings.local.json`.

Flag misplacement in both directions. A credential deny that exists only in this project leaves every other project uncovered. A machine-specific absolute path in a tracked file breaks for everyone else. A blanket grant in user settings is the worst case, since it applies to every repository including untrusted ones.

Note whether `settings.local.json` is actually gitignored here, and say so if it is not.

## Phase 6. Mode interaction

Determine the effective permission mode: `permissions.defaultMode` in the nearest scope that is allowed to set it, otherwise Manual. Remember that `defaultMode: "auto"` is ignored from project and local settings.

Then evaluate the allow list **against that mode**, because the same list has opposite effects in different modes.

In Manual or `acceptEdits`, an allow rule removes a prompt you would otherwise have answered. Broad grants are the risk.

In auto mode, an allow rule removes the classifier from the decision entirely, since allow, ask, and deny resolve before the classifier runs. Rules such as `Bash(git push:*)`, `Bash(git commit:*)`, or `Bash(gh pr:*)` therefore disable exactly the checks the classifier is best at, including whether a push carries secrets outside the repository. If the project runs in auto mode, list every allow rule that suppresses classifier review and recommend moving it to `ask` or deleting it. Note also which broad grants auto mode drops on entry, so the reader knows which Phase 1 findings are neutralized in that mode and which are not.

If hooks are configured, check whether a `PreToolUse` hook exits non-zero to block anything. A hook that inspects the resolved command is a harder boundary than a pattern, and it is worth confirming it catches the interpreter forms found in Phase 1 rather than only the literal command names.

## Output

Produce, in this order.

**Posture score out of 100**, with the breakdown visible so the reader can argue with it:

| Dimension | Points | Basis |
|---|---:|---|
| No blanket execution grant | 30 | Any arbitrary grant scores 0 here, whatever else is right |
| Deny coverage on destructive and secret actions | 20 | Presence and robustness against the documented semantics |
| At least one meaningful `ask` rule | 10 | An empty `ask` array scores 0 |
| Sandbox enabled and coherently configured | 20 | Off scores 0; on with an unjustified bypass scores partial |
| Scope hygiene | 10 | Right rule, right file, gitignore correct |
| Rule population health | 10 | Dead, shadowed, and malformed rules |

**Ranked findings**, worst first. Each one carries: severity, the file and rule, what an attacker or an accident does with it, the reproduction command, and the fix. No finding without a reproduction step.

**A ready-to-apply patch**, as a JSON block per file, showing only what changes and stating which scope it belongs in. Do not apply it.

**Not verified**, listing everything you could not confirm: version-dependent behavior, fields whose syntax you could not check, anything requiring the `/sandbox` or `/permissions` panel. Being explicit here is worth more than a complete-looking report.

**One sentence** naming the single change with the highest ratio of risk removed to effort spent.

## Rules for your report

Be specific or say nothing. "Consider tightening permissions" is not a finding; "`Bash(node:*)` in `.claude/settings.local.json` line 412 makes the `Read(**/.env*)` deny in `.claude/settings.json` line 5 bypassable via `node -e 'console.log(require("fs").readFileSync(".env","utf8"))'`" is.

Do not pad the report to look thorough. If a phase finds nothing, one line saying so is the correct output.

Do not recommend `bypassPermissions` or `--dangerously-skip-permissions` as a remedy for prompt fatigue. The sandbox with `autoAllowBashIfSandboxed` is the mechanism that removes prompts while keeping a boundary.

State plainly when a configuration is good. An audit that manufactures findings to justify itself is worse than no audit.

# PROMPT ENDS HERE

---

## Reading the score

A score above 80 with the sandbox off is possible and means the rule list is genuinely disciplined. It also means the boundary depends on that discipline holding for every future rule someone adds.

A score below 40 almost always traces to a single line. Phase 1 usually finds it, and removing it moves the score more than anything else in the report.

The dimension weights are deliberately lopsided. An arbitrary execution grant zeroes 30 points on its own, because a configuration containing one is not a weaker boundary than a configuration without it: it is not a boundary.

## Related

| Tool | Scope |
|---|---|
| `tools/audit-prompt.md` | Whole setup, eight dimensions, memory and skills and agents included |
| `/security-audit` | Project secrets, injection surface, dependencies |
| `/security-check` | Fast config check against the threat database |
| `/fewer-permission-prompts` | Built-in skill that proposes a read-only allowlist from your transcripts |

Run this one after `/fewer-permission-prompts`, not before. That skill adds rules; this prompt tells you whether the rules you now have still form a boundary.
