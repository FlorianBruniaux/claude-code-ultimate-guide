#!/usr/bin/env python3
"""Record and show an agent's rationale per hunk, stored in git notes.

Notes live under refs/notes/rationale, one JSON document per commit. Each note
anchors to a hunk of that commit's diff by a hash of the hunk's added lines,
with the annotated line's text as a fallback. When neither matches any more,
the note is reported as stale instead of being shown on the wrong line.

Usage, from inside a Git repository:
    rationale.py add --file PATH --line N --intent TEXT [--rejected TEXT]
                     [--risk TEXT] [--evidence TEXT] [--open-question TEXT] [--rev REV]
    rationale.py show [--rev REV] [--json]

Python 3.9 or later, standard library only.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys

NOTES_REF = "refs/notes/rationale"
SCHEMA = "agent-rationale/1"
HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


class RationaleError(Exception):
    pass


def git(*args, stdin=None, check=True):
    result = subprocess.run(["git", *args], input=stdin, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RationaleError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result


def resolve(rev):
    sha = git("rev-parse", "--verify", f"{rev}^{{commit}}").stdout.strip()
    parents = git("rev-list", "--parents", "-n", "1", sha).stdout.split()[1:]
    if len(parents) > 1:
        raise RationaleError(f"{rev} is a merge commit; annotate the commits it merges")
    return sha


def hunks(sha, path):
    """Return the hunks a commit adds to one file: [(start, [added lines])]."""
    diff = git("-c", "core.quotepath=off", "show", "--no-color", "--no-ext-diff",
               "--format=", "-U0", sha, "--", path).stdout
    result = []
    current = None
    for raw in diff.splitlines():
        match = HUNK_HEADER.match(raw)
        if match:
            current = (int(match.group(1)), [])
            result.append(current)
        elif current is not None and raw.startswith("+") and not raw.startswith("+++"):
            current[1].append(raw[1:])
    return [hunk for hunk in result if hunk[1]]


def hunk_hash(lines):
    normalized = "\n".join(line.rstrip() for line in lines)
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def read_note(sha):
    result = git("notes", f"--ref={NOTES_REF}", "show", sha, check=False)
    if result.returncode != 0:
        return {"schema": SCHEMA, "notes": []}
    document = json.loads(result.stdout)
    if document.get("schema") != SCHEMA:
        raise RationaleError(f"unexpected note schema on {sha[:12]}: {document.get('schema')}")
    return document


def add(args):
    sha = resolve(args.rev)
    for start, lines in hunks(sha, args.file):
        if start <= args.line < start + len(lines):
            snippet = lines[args.line - start]
            break
    else:
        raise RationaleError(f"line {args.line} of {args.file} is not in a hunk added by {args.rev}")
    document = read_note(sha)
    document["notes"].append({
        "file": args.file,
        "line": args.line,
        "hunk_hash": hunk_hash(lines),
        "snippet": snippet,
        "intent": args.intent,
        "rejected_alternative": args.rejected,
        "risk": args.risk,
        "evidence": args.evidence,
        "open_question": args.open_question,
    })
    git("notes", f"--ref={NOTES_REF}", "add", "-f", "-F", "-", sha,
        stdin=json.dumps(document, indent=2) + "\n")
    print(f"rationale recorded on {sha[:12]} for {args.file}:{args.line}")


def locate(sha, entry):
    """Anchor by hunk hash, then by the annotated line's text, else stale."""
    file_hunks = hunks(sha, entry["file"])
    for start, lines in file_hunks:
        if hunk_hash(lines) == entry["hunk_hash"]:
            offset = lines.index(entry["snippet"]) if entry["snippet"] in lines else 0
            return "anchored", start + offset
    for start, lines in file_hunks:
        if entry["snippet"] in lines:
            return "reanchored", start + lines.index(entry["snippet"])
    return "stale", None


def show(args):
    sha = resolve(args.rev)
    located = []
    for entry in read_note(sha)["notes"]:
        status, line = locate(sha, entry)
        located.append(dict(entry, status=status, line=line, recorded_line=entry["line"]))
    if args.json:
        print(json.dumps(located, indent=2))
        return
    if not located:
        print(f"no rationale on {sha[:12]}")
    for entry in located:
        where = f"{entry['file']}:{entry['line']}" if entry["line"] else f"{entry['file']} (stale)"
        print(f"[{entry['status']}] {where}")
        if entry["status"] == "stale":
            print(f"  recorded at line {entry['recorded_line']} on: {entry['snippet']!r}; the hunk has changed, re-check before trusting it")
        for label, key in (("intent", "intent"), ("rejected", "rejected_alternative"),
                           ("risk", "risk"), ("evidence", "evidence"), ("open question", "open_question")):
            print(f"  {label}: {entry[key]}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    add_parser = sub.add_parser("add", help="record a rationale for a hunk of a commit")
    add_parser.add_argument("--rev", default="HEAD")
    add_parser.add_argument("--file", required=True)
    add_parser.add_argument("--line", required=True, type=int, help="line number in the commit's version of the file")
    add_parser.add_argument("--intent", required=True)
    for flag in ("--rejected", "--risk", "--evidence", "--open-question"):
        add_parser.add_argument(flag, default="unknown")
    show_parser = sub.add_parser("show", help="show rationales of a commit, re-anchored to its diff")
    show_parser.add_argument("--rev", default="HEAD")
    show_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        (add if args.command == "add" else show)(args)
    except RationaleError as error:
        print(f"rationale: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
