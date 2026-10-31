#!/usr/bin/env python3
"""Read-only archaeology of an AI coding harness in a git repository.

Walks every non-merge commit that touches a harness path, classifies each file
by tool family and element kind, and writes a JSON dataset plus a Markdown
report. Author identities are reduced to salted hashes; no name or e-mail is
written. Usage:

    python3 -I harness_archaeology.py --repo PATH --out DIR [--slug NAME]
        [--since YYYY-MM-DD] [--ref HEAD] [--remotes] [--salt TEXT] [--extra-glob GLOB]... [--exclude-glob GLOB]...
"""
import argparse
import collections
import datetime as dt
import fnmatch
import hashlib
import json
import os
import re
import secrets
import statistics
import subprocess
import sys

PATHSPECS = [
    "**/.github/**", "**/.claude/**", "**/.claude-plugin/**", "**/CLAUDE.md",
    "**/CLAUDE.local.md", "**/AGENTS.md", "**/AGENTS.override.md", "**/.agents/**",
    "**/.codex/**", "**/.cursor/**", "**/.cursorrules", "**/*.mdc", "**/.factory/**",
    "**/mcp.json", "**/.mcp.json", "**/SKILL.md", "**/*.prompt.md", "**/*.agent.md",
    "**/*.chatmode.md", "**/*.instructions.md", "**/plugin.json", "**/marketplace.json",
    "**/hooks.json", "**/docs/ai/**", "**/doc/ai/**", "**/GEMINI.md", "**/.gemini/**",
    "**/.junie/**", "**/.windsurf/**", "**/.windsurfrules", "**/.continue/**",
    "**/.clinerules", "**/.kiro/**", "**/.aider*", "**/agent-ready/**",
    "**/agents/*.md", "**/commands/*.md", "**/skills/**", "**/.copilot/**",
]
EXCLUDE = re.compile(r"(^|/)(node_modules|dist|build|target|\.venv|vendor)/")
GITHUB_NON_AI = re.compile(r"(^|/)\.github/(workflows|ISSUE_TEMPLATE|PULL_REQUEST_TEMPLATE|dependabot|CODEOWNERS|FUNDING|actions)")

FAMILY_RULES = [
    ("copilot", re.compile(r"(^|/)\.github/(copilot-instructions\.md|instructions/|prompts/|chatmodes/|agents/|skills/|hooks/)|\.(prompt|chatmode|agent|instructions)\.md$|(^|/)\.copilot/")),
    ("claude", re.compile(r"(^|/)(CLAUDE(\.local)?\.md$|\.claude/|\.claude-plugin/|\.mcp\.json$)")),
    ("codex-agents", re.compile(r"(^|/)(AGENTS(\.override)?\.md$|\.agents/|\.codex/)")),
    ("factory", re.compile(r"(^|/)\.factory/")),
    ("cursor", re.compile(r"(^|/)(\.cursor/|\.cursorrules$)|\.mdc$")),
    ("other-agent", re.compile(r"(^|/)(GEMINI\.md$|\.gemini/|\.junie/|\.windsurf/|\.windsurfrules$|\.continue/|\.clinerules$|\.kiro/|\.aider)")),
    ("mcp", re.compile(r"(^|/)mcp\.json$")),
    ("plugin", re.compile(r"(^|/)(plugin\.json|marketplace\.json|hooks\.json)$|^(agents|commands)/[^/]+\.md$|(^|/)plugins/[^/]+/(agents|commands)/[^/]+\.md$")),
    ("docs-ai", re.compile(r"(^|/)(docs?/ai/|docs?/agents/|agent-ready/)")),
    ("skills", re.compile(r"(^|/)SKILL\.md$")),
]
KIND_RULES = [
    ("skill", re.compile(r"(^|/)skills?/|SKILL\.md$")),
    ("agent", re.compile(r"\.agent\.md$|(^|/)agents/")),
    ("prompt", re.compile(r"\.prompt\.md$|(^|/)prompts/")),
    ("chatmode", re.compile(r"\.chatmode\.md$|(^|/)chatmodes/")),
    ("command", re.compile(r"(^|/)commands/")),
    ("hook", re.compile(r"(^|/)hooks?/|hooks\.json$")),
    ("rule", re.compile(r"\.instructions\.md$|(^|/)(instructions|rules)/|\.mdc$|\.cursorrules$")),
    ("memory", re.compile(r"(^|/)(AGENTS|CLAUDE|GEMINI)(\.local|\.override)?\.md$|copilot-instructions\.md$")),
    ("mcp", re.compile(r"mcp\.json$")),
    ("settings", re.compile(r"settings(\.local)?\.json$|config\.toml$")),
    ("manifest", re.compile(r"(plugin|marketplace)\.json$")),
    ("doc", re.compile(r"\.md$")),
]
AI_TOOLS = [
    ("Claude", re.compile(r"claude|anthropic", re.I)),
    ("Copilot", re.compile(r"copilot", re.I)),
    ("Codex/OpenAI", re.compile(r"codex|openai|chatgpt|\bgpt", re.I)),
    ("Cursor", re.compile(r"cursor", re.I)),
    ("Gemini", re.compile(r"gemini", re.I)),
    ("Mistral", re.compile(r"mistral|le chat", re.I)),
    ("Autre agent", re.compile(r"windsurf|codeium|devin|aider|junie|kiro|cline|amazon q", re.I)),
]
BODY_AI = re.compile(r"Generated with \[?(Claude Code|Codex|Copilot|Cursor)|🤖 Generated", re.I)
EXTRA = []  # extra glob patterns from --extra-glob, family "custom"
SKIP = []  # glob patterns from --exclude-glob, never classified
SCOPE = re.compile(r"^(\w+)(?:\(([^)]*)\))?!?:")


def git(repo, *args):
    res = subprocess.run(["git", "-c", "core.quotePath=false", "-C", repo, *args], capture_output=True, text=True, errors="replace")
    if res.returncode != 0:
        raise SystemExit(f"git {' '.join(args[:3])} failed: {res.stderr.strip()[:300]}")
    return res.stdout


def classify(path, skill_dirs):
    if EXCLUDE.search(path) or GITHUB_NON_AI.search(path) or any(fnmatch.fnmatch(path, g) for g in SKIP):
        return None, None
    family = next((f for f, rx in FAMILY_RULES if rx.search(path)), None)
    if family is None and any(path.startswith(d + "/") for d in skill_dirs):
        family = "skills"
    if family is None and any(fnmatch.fnmatch(path, g) for g in EXTRA):
        family = "custom"
    if family is None:
        return None, None
    kind = next((k for k, rx in KIND_RULES if rx.search(path)), "other")
    return family, kind


def module_of(path):
    parts = path.split("/")
    if len(parts) == 1 or parts[0].startswith("."):
        return "(root)"
    return parts[0]


AI_DOMAINS = [("anthropic.com", "Claude"), ("cursor.com", "Cursor"), ("openai.com", "Codex/OpenAI"),
              ("mistral.ai", "Mistral"), ("codeium.com", "Autre agent"), ("devin.ai", "Autre agent")]


def ai_tools(values):
    """A trailer counts when its e-mail domain belongs to a tool vendor, or when the name names a tool and the
    e-mail is a bot or noreply address. A person called Claude with a company e-mail does not count."""
    found = set()
    for v in values:
        m = re.match(r"\s*([^<]*?)\s*(?:<([^>]*)>)?\s*$", v)
        name, email = (m.group(1), (m.group(2) or "").lower()) if m else (v, "")
        hit = next((t for d, t in AI_DOMAINS if email.endswith("@" + d) or email.endswith("." + d)), None)
        if hit is None and (not email or "noreply" in email or "bot" in email.split("@")[0] or email.endswith("@github.com")):
            hit = next((t for t, rx in AI_TOOLS if rx.search(name)), None)
        if hit:
            found.add(hit)
    return found


def parse_log(text):
    """Records separated by \x1e; header fields by \x1f; then --raw and --numstat lines."""
    for rec in text.split("\x1e")[1:]:
        head, _, rest = rec.partition("\x1d\x1d")
        h, date, email, subject, trailers = (head.split("\x1f") + [""] * 5)[:5]
        raw, numstat = [], {}
        for line in rest.splitlines():
            if not line:
                continue
            if line.startswith(":"):
                meta, *paths = line.split("\t")
                fields = meta.split()
                blob = "0" * 40 if fields[1] == "120000" else fields[3]  # symlinks never count as copies
                raw.append((fields[4], blob, paths))
            else:
                parts = line.split("\t")
                if len(parts) >= 3:
                    a, d = parts[0], parts[1]
                    p = parts[-1]
                    if "=>" in p:
                        p = re.sub(r"\{([^{}]*) => ([^{}]*)\}", r"\2", p).replace("//", "/")
                        p = p.split(" => ")[-1]
                    numstat[p] = (0 if a == "-" else int(a), 0 if d == "-" else int(d))
        yield {"hash": h, "date": date, "email": email, "subject": subject,
               "trailers": [t for t in trailers.split(";") if t.strip()], "raw": raw, "numstat": numstat}


def load_commits(repo, ref, since, extra):
    fmt = "%x1e%H%x1f%ad%x1f%ae%x1f%s%x1f%(trailers:key=Co-authored-by,valueonly,separator=;)%x1d%x1d"
    args = ["log", *ref, "--no-merges", "-M", "--raw", "--no-abbrev", "--numstat",
            f"--format={fmt}", "--date=short", *extra]
    if since:
        args.append(f"--since={since}")
    args += ["--", *[f":(glob){p}" for p in PATHSPECS + EXTRA]]
    return list(parse_log(git(repo, *args)))


def load_all_commits(repo, ref, since):
    fmt = "%x1e%H%x1f%ad%x1f%ae%x1f%(trailers:key=Co-authored-by,valueonly,separator=;)%x1f%b"
    args = ["log", *ref, "--no-merges", f"--format={fmt}", "--date=format:%Y-%m"]
    if since:
        args.append(f"--since={since}")
    out = []
    for rec in git(repo, *args).split("\x1e")[1:]:
        h, month, email, trailers, body = (rec.split("\x1f") + [""] * 5)[:5]
        tools = ai_tools([t for t in trailers.split(";") if t.strip()])
        m = BODY_AI.search(body)
        if m:
            tools |= ai_tools([m.group(0)])
        out.append((h, month, email, tools))
    return out


def owners(repo):
    """Team groups per module from CODEOWNERS.js (group file names) or CODEOWNERS group handles."""
    res = {}
    for entry in sorted(os.listdir(repo)):
        js = os.path.join(repo, entry, "CODEOWNERS.js")
        if os.path.isfile(js):
            groups = re.findall(r"code-owners-groups/([\w.-]+)\.json", open(js, errors="replace").read())
            if groups:
                res[entry] = sorted(set(groups))
    for cand in ("CODEOWNERS", ".gitlab/CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"):
        p = os.path.join(repo, cand)
        if os.path.isfile(p):
            for line in open(p, errors="replace"):
                line = line.split("#")[0].strip()
                if not line or line.startswith("["):
                    continue
                pat, *handles = line.split()
                groups = [h.lstrip("@") for h in handles if h.startswith("@") and "/" in h]
                mod = pat.strip("/").split("/")[0]
                if groups and mod and mod != "*":
                    res.setdefault(mod, sorted(set(groups)))
    return res


def build(args):
    repo = os.path.realpath(args.repo)
    git(repo, "rev-parse", "--git-dir")
    ref = [args.ref]
    head_date = git(repo, "log", "-1", "--format=%ad", "--date=short", args.ref).strip()
    first_date = git(repo, "log", "--reverse", "--format=%ad", "--date=short", args.ref).split("\n", 1)[0]
    salt = args.salt or secrets.token_hex(16)  # random by default: hashes cannot be recomputed from e-mails
    anon = lambda e: hashlib.sha256((salt + e.lower()).encode()).hexdigest()[:12]

    commits = load_commits(repo, ref, args.since, [])
    commits.reverse()  # chronological
    skill_dirs = set()
    for c in commits:
        for _, _, paths in c["raw"]:
            for p in paths:
                if p.endswith("SKILL.md"):
                    skill_dirs.add(p.rsplit("/", 1)[0] if "/" in p else "")
    skill_dirs.discard("")

    head_tree = {}
    for line in git(repo, "ls-tree", "-r", "--full-tree", "-z", args.ref).split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            mode, _, blob = meta.split()
            head_tree[path] = (mode, blob)
    head_files = set(head_tree)
    files = {}
    harness_commits = []
    blob_first = {}
    propagation = []
    for c in commits:
        touched = []
        for status, blob, paths in c["raw"]:
            st = status[0]
            path = paths[-1]
            fam, kind = classify(path, skill_dirs)
            old = paths[0] if st in "RC" and len(paths) == 2 else None
            if fam is None and old:
                fam, kind = classify(old, skill_dirs)
            if fam is None:
                continue
            a, d = c["numstat"].get(path, (0, 0))
            touched.append((st, path, fam, kind, a, d, old))
            rec = files.get(old) if st == "R" and old in files else None
            if rec is not None:
                del files[old]
                rec["renamed_from"].append(old)
                rec["path"] = path
                files[path] = rec
            rec = files.setdefault(path, {"path": path, "family": fam, "kind": kind, "module": module_of(path),
                                          "created": None, "created_hash": None, "last": None, "deleted": None,
                                          "commits": 0, "authors": set(), "added": 0, "removed": 0,
                                          "renamed_from": [], "events": collections.Counter()})
            rec["family"], rec["kind"], rec["module"] = fam, kind, module_of(path)
            if rec["created"] is None and st in "ACR":
                rec["created"], rec["created_hash"] = c["date"], c["hash"][:11]
            if rec["created"] is None:
                rec["created"], rec["created_hash"] = c["date"], c["hash"][:11]
                rec["events"]["pre-existing"] += 1
            rec["last"] = c["date"]
            rec["commits"] += 1
            rec["authors"].add(anon(c["email"]))
            rec["added"] += a
            rec["removed"] += d
            rec["events"][st] += 1
            rec["deleted"] = c["date"] if st == "D" else None
            if st in "ACM" and blob != "0" * 40:
                if blob in blob_first and blob_first[blob][0] != path and st in "AC":
                    propagation.append({"date": c["date"], "hash": c["hash"][:11], "from": blob_first[blob][0],
                                        "to": path, "from_date": blob_first[blob][1]})
                blob_first.setdefault(blob, (path, c["date"]))
        if touched:
            scope_m = SCOPE.match(c["subject"])
            harness_commits.append({
                "hash": c["hash"][:11], "date": c["date"], "author": anon(c["email"]),
                "subject": c["subject"][:160], "type": scope_m.group(1) if scope_m else None,
                "scope": scope_m.group(2) if scope_m and scope_m.group(2) else None,
                "ai_tools": sorted(ai_tools(c["trailers"])),
                "files": [{"status": t[0], "path": t[1], "family": t[2], "kind": t[3], "added": t[4], "removed": t[5],
                           "old": t[6]} for t in touched],
                "families": sorted({t[2] for t in touched}),
                "modules": sorted({module_of(t[1]) for t in touched}),
            })

    all_commits = load_all_commits(repo, ref, args.since)
    ai_by_hash = {h[:11]: tools for h, _, _, tools in all_commits if tools}
    for hc in harness_commits:  # same usage definition as the monthly table: trailers or "Generated with"
        hc["ai_tools"] = sorted(ai_by_hash.get(hc["hash"], set()))
    monthly = collections.defaultdict(lambda: {"commits": 0, "ai": 0, "authors": set(), "ai_authors": set(),
                                               "harness": 0, "harness_ai": 0,
                                               "tools": collections.Counter(), "families": collections.Counter()})
    for h, month, email, tools in all_commits:
        m = monthly[month]
        m["commits"] += 1
        m["authors"].add(anon(email))
        if tools:
            m["ai"] += 1
            m["ai_authors"].add(anon(email))
            for t in tools:
                m["tools"][t] += 1
    for hc in harness_commits:
        m = monthly[hc["date"][:7]]
        m["harness"] += 1
        m["harness_ai"] += 1 if hc["ai_tools"] else 0
        for f in hc["families"]:
            m["families"][f] += 1

    if monthly:  # show months without any commit too
        y, mo = map(int, min(monthly).split("-"))
        last = max(monthly)
        while f"{y:04d}-{mo:02d}" <= last:
            monthly[f"{y:04d}-{mo:02d}"]
            y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)

    unmerged = []
    if args.remotes:
        un = load_commits(repo, ["--remotes"], args.since, ["--not", args.ref])
        for c in un:
            paths = [p[-1] for _, _, p in c["raw"] if classify(p[-1], skill_dirs)[0]]
            if paths:
                unmerged.append({"hash": c["hash"][:11], "date": c["date"], "subject": c["subject"][:160],
                                 "files": len(paths), "families": sorted({classify(p, skill_dirs)[0] for p in paths}),
                                 "modules": sorted({module_of(p) for p in paths})})

    for rec in files.values():
        rec["present"] = rec["path"] in head_files
        rec["authors"] = len(rec["authors"])
        rec["events"] = dict(rec["events"])

    head_blobs = collections.defaultdict(list)
    for path, (mode, blob) in head_tree.items():
        if path in files and files[path]["present"] and mode != "120000":  # symlinks are not copies
            head_blobs[blob].append(path)
    duplicates = sorted(([p for p in v] for v in head_blobs.values() if len(v) > 1), key=len, reverse=True)

    return {
        "repo": os.path.basename(repo), "ref": args.ref, "head_date": head_date, "first_date": first_date,
        "since": args.since, "generated": dt.date.today().isoformat(),
        "total_commits": len(all_commits), "harness_commits": harness_commits, "files": list(files.values()),
        "monthly": {k: {**v, "authors": len(v["authors"]), "ai_authors": len(v["ai_authors"]),
                        "tools": dict(v["tools"]), "families": dict(v["families"])} for k, v in sorted(monthly.items())},
        "propagation": propagation, "duplicates_at_head": duplicates, "owners": owners(repo),
        "unmerged": unmerged, "remotes_scanned": args.remotes,
    }


def pct(a, b):
    return f"{100 * a / b:.1f} %" if b else "-"


def bar(n, scale):
    return "█" * max(1 if n else 0, round(n / scale)) if scale else ""


def report(data):
    hc, files, monthly = data["harness_commits"], data["files"], data["monthly"]
    L = []
    w = L.append
    present = [f for f in files if f["present"]]
    w(f"# AI harness archaeology: {data['repo']}\n")
    w(f"Ref `{data['ref']}`, from {data['first_date']} to {data['head_date']}. Generated on {data['generated']} by `harness_archaeology.py`, read-only. Authors reduced to a salted hash.\n")
    if not hc:
        w("No commit touches a known AI harness path.\n")
        return "\n".join(L)
    authors = collections.Counter(c["author"] for c in hc)
    top = authors.most_common()
    w("## Key figures\n")
    w("| Measure | Value |\n| --- | --- |")
    w(f"| Repository commits (no merges) | {data['total_commits']} |")
    w(f"| Commits touching the harness | {len(hc)} ({pct(len(hc), data['total_commits'])}) |")
    w(f"| First harness commit | {hc[0]['date']} `{hc[0]['hash']}` |")
    w(f"| Harness files seen in history | {len(files)}, {len(present)} present at ref |")
    w(f"| Harness contributors | {len(authors)}; top one signs {pct(top[0][1], len(hc))}, top three {pct(sum(n for _, n in top[:3]), len(hc))} |")
    w(f"| One-commit harness contributors | {sum(1 for _, n in top if n == 1)} |")
    w(f"| Harness commits with an AI trailer | {sum(1 for c in hc if c['ai_tools'])} ({pct(sum(1 for c in hc if c['ai_tools']), len(hc))}) |")
    never = sum(1 for f in present if f["commits"] == 1)
    w(f"| Present files never edited after creation | {never} ({pct(never, len(present))}) |")
    ref = dt.date.fromisoformat(data["head_date"])
    stale = sum(1 for f in present if (ref - dt.date.fromisoformat(f["last"])).days > 180)
    w(f"| Present files untouched for over 180 days | {stale} ({pct(stale, len(present))}) |")
    w(f"| Identical copies at ref | {sum(len(d) for d in data['duplicates_at_head'])} files in {len(data['duplicates_at_head'])} groups |")
    w(f"| Copy propagations (same content added elsewhere) | {len(data['propagation'])} |")
    if data["remotes_scanned"]:
        w(f"| Harness commits on unmerged remote branches | {len(data['unmerged'])} |")
    w("")

    w("## By tool family\n")
    fam = collections.defaultdict(lambda: {"files": 0, "present": 0, "commits": set(), "first": None, "last": None, "authors": set()})
    for c in hc:
        for f in c["files"]:
            x = fam[f["family"]]
            x["commits"].add(c["hash"])
            x["authors"].add(c["author"])
            x["first"] = x["first"] or c["date"]
            x["last"] = c["date"]
    for f in files:
        fam[f["family"]]["files"] += 1
        fam[f["family"]]["present"] += f["present"]
    w("| Family | First commit | Last | Commits | Contributors | Files seen | Present |\n| --- | --- | --- | --- | --- | --- | --- |")
    for k, x in sorted(fam.items(), key=lambda kv: kv[1]["first"] or ""):
        w(f"| {k} | {x['first']} | {x['last']} | {len(x['commits'])} | {len(x['authors'])} | {x['files']} | {x['present']} |")
    w("")

    w("## By element kind (present files)\n")
    kinds = collections.Counter((f["family"], f["kind"]) for f in present)
    w("| Family | Kind | Files |\n| --- | --- | --- |")
    for (f, k), n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        w(f"| {f} | {k} | {n} |")
    w("")

    w("## Monthly distribution\n")
    w("Usage: commits with a `Co-authored-by` trailer or a 'Generated with' line naming an AI tool, across the whole repository. This is a lower bound.\n")
    w("| Month | Commits | Harness | AI usage | % usage | AI contributors | Tools (usage) | Families touched |\n| --- | --- | --- | --- | --- | --- | --- | --- |")
    start = hc[0]["date"][:7]
    for month, m in monthly.items():
        if month < start:
            continue
        tools = ", ".join(f"{t} {n}" for t, n in sorted(m["tools"].items(), key=lambda kv: -kv[1])) or "-"
        fams = ", ".join(f"{t} {n}" for t, n in sorted(m["families"].items(), key=lambda kv: -kv[1])) or "-"
        w(f"| {month} | {m['commits']} | {m['harness']} | {m['ai']} | {pct(m['ai'], m['commits'])} | {m['ai_authors']}/{m['authors']} | {tools} | {fams} |")
    w("")
    peak = max(m["harness"] for k, m in monthly.items() if k >= start) or 1
    w("```text")
    for month, m in monthly.items():
        if month >= start:
            w(f"{month} {bar(m['harness'], peak / 40):<40} {m['harness']}")
    w("```\n")

    w("## By module\n")
    mods = collections.defaultdict(lambda: {"commits": set(), "files": 0, "present": 0, "first": None, "last": None, "families": collections.Counter(), "authors": set()})
    for c in hc:
        for f in c["files"]:
            x = mods[module_of(f["path"])]
            x["commits"].add(c["hash"])
            x["authors"].add(c["author"])
            x["first"] = x["first"] or c["date"]
            x["last"] = c["date"]
    for f in files:
        mods[f["module"]]["files"] += 1
        mods[f["module"]]["present"] += f["present"]
        mods[f["module"]]["families"][f["family"]] += f["present"]
    w("| Module | Teams (CODEOWNERS) | First | Last | Commits | Contributors | Present | Present families |\n| --- | --- | --- | --- | --- | --- | --- | --- |")
    for k, x in sorted(mods.items(), key=lambda kv: -len(kv[1]["commits"])):
        fams = ", ".join(f"{a} {n}" for a, n in x["families"].most_common() if n) or "none"
        teams = ", ".join(data["owners"].get(k, [])) or "-"
        w(f"| {k} | {teams} | {x['first']} | {x['last']} | {len(x['commits'])} | {len(x['authors'])} | {x['present']} | {fams} |")
    w("")

    w("## Most frequent commit scopes\n")
    scopes = collections.Counter(c["scope"] or "(no scope)" for c in hc)
    w("| Scope | Commits |\n| --- | --- |")
    for s, n in scopes.most_common(25):
        w(f"| `{s}` | {n} |")
    w("")

    w("## Milestones: structuring commits (10 harness files or more)\n")
    w("| Date | Hash | Files | A/M/D/R | Families | Subject |\n| --- | --- | --- | --- | --- | --- |")
    for c in hc:
        if len(c["files"]) >= 10:
            st = collections.Counter(f["status"][0] for f in c["files"])
            w(f"| {c['date']} | `{c['hash']}` | {len(c['files'])} | {st.get('A',0)}/{st.get('M',0)}/{st.get('D',0)}/{st.get('R',0)} | {', '.join(c['families'])} | {c['subject'].replace('|', '/')} |")
    w("")

    w("## Most edited files\n")
    w("| File | Family | Created | Last | Commits | Contributors | +/- | Present |\n| --- | --- | --- | --- | --- | --- | --- | --- |")
    for f in sorted(files, key=lambda f: -f["commits"])[:30]:
        w(f"| `{f['path']}` | {f['family']} | {f['created']} | {f['last']} | {f['commits']} | {f['authors']} | +{f['added']}/-{f['removed']} | {'yes' if f['present'] else 'no'} |")
    w("")

    deleted = [f for f in files if not f["present"]]
    w(f"## Deleted files ({len(deleted)})\n")
    if deleted:
        lives = [(dt.date.fromisoformat(f["last"]) - dt.date.fromisoformat(f["created"])).days for f in deleted]
        w(f"Median lifetime: {statistics.median(lives)} days. By family: " + ", ".join(f"{k} {n}" for k, n in collections.Counter(f['family'] for f in deleted).most_common()) + ".\n")
        w("| File | Family | Created | Last commit | Commits |\n| --- | --- | --- | --- | --- |")
        for f in sorted(deleted, key=lambda f: f["last"])[-25:]:
            w(f"| `{f['path']}` | {f['family']} | {f['created']} | {f['last']} | {f['commits']} |")
    w("")

    if data["duplicates_at_head"]:
        w("## Identical copies at ref (10 largest groups)\n")
        for g in data["duplicates_at_head"][:10]:
            w(f"- {len(g)} copies: " + ", ".join(f"`{p}`" for p in sorted(g)[:6]) + (" ..." if len(g) > 6 else ""))
        w("")
    if data["propagation"]:
        w("## Copy propagations (last 20)\n")
        w("| Date | Hash | Copied from | To |\n| --- | --- | --- | --- |")
        for p in data["propagation"][-20:]:
            w(f"| {p['date']} | `{p['hash']}` | `{p['from']}` ({p['from_date']}) | `{p['to']}` |")
        w("")
    if data["remotes_scanned"]:
        w(f"## Unmerged remote branches ({len(data['unmerged'])} harness commits)\n")
        mods = collections.Counter(m for u in data["unmerged"] for m in u["modules"])
        w("Modules: " + (", ".join(f"{k} {n}" for k, n in mods.most_common(15)) or "none") + ".\n")
        w("| Date | Hash | Files | Families | Subject |\n| --- | --- | --- | --- | --- |")
        for u in sorted(data["unmerged"], key=lambda u: u["date"])[-25:]:
            w(f"| {u['date']} | `{u['hash']}` | {u['files']} | {', '.join(u['families'])} | {u['subject'].replace('|', '/')} |")
        w("")

    w("## Limits\n")
    w("- Merges are excluded: a change counts once, at its commit's author date.")
    w("- Only the analysed ref counts, except the remote-branch section when requested.")
    w("- An AI trailer is a lower bound of usage and does not say which tool feature was used.")
    w("- Classification is path-based. A harness file outside the known patterns is not seen.")
    w("- Authors are counted by e-mail: one person with two e-mails counts twice.")
    if data["since"]:
        pre = sum(1 for f in files if f["events"].get("pre-existing"))
        w(f"- Window opened on {data['since']}: {pre} files existed before; their creation date is their first commit in the window.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--slug")
    ap.add_argument("--since")
    ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--remotes", action="store_true", help="also scan remote branches not merged into --ref")
    ap.add_argument("--salt", help="salt for author hashes (default: repository name)")
    ap.add_argument("--extra-glob", action="append", default=[],
                    help="extra harness glob, repeatable, e.g. 'tools/ai/**'; classified as family custom")
    ap.add_argument("--exclude-glob", action="append", default=[],
                    help="glob to ignore, repeatable, e.g. 'examples/**' when skills are product content")
    args = ap.parse_args()
    ap_skip = args.exclude_glob
    EXTRA.extend(args.extra_glob)
    SKIP.extend(ap_skip)
    if not os.path.isdir(args.repo):
        sys.exit(f"not a directory: {args.repo}")
    data = build(args)
    slug = args.slug or data["repo"]
    os.makedirs(args.out, exist_ok=True)
    jp = os.path.join(args.out, f"{slug}-harness.json")
    mp = os.path.join(args.out, f"{slug}-harness.md")
    with open(jp, "w") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    with open(mp, "w") as fh:
        fh.write(report(data))
    print(json.dumps({"repo": data["repo"], "harness_commits": len(data["harness_commits"]),
                      "files": len(data["files"]), "json": jp, "md": mp}, ensure_ascii=False))


if __name__ == "__main__":
    main()
