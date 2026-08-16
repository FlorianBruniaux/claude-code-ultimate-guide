#!/usr/bin/env python3
"""supply-chain-triage.py - Triage a workstation after an npm supply chain incident.

Built for the Shai-Hulud family (keyv/cacheable, August 2026), but the compromised
package list is read from threat-db.yaml rather than hardcoded, so it stays useful
for the next campaign.

What it checks, in the order incident response should run:

  1. Lockfiles           compromised package@version pairs
  2. Installed tree      package.json carrying a preinstall that runs a dropper
  3. Hashes              known payload SHA-256 in node_modules
  4. Startup hooks       .claude/settings*.json and .vscode/tasks.json
  5. Persistence         token-revocation watchers, LaunchAgents, systemd units
  6. Egress              attacker domains pinned in .npmrc or /etc/hosts

Order matters. Checks 4 and 5 run before you rotate anything: these families ship
watchers that fire ON revocation, so rotating first is what triggers them.

Deliberately NOT a filename scan. Payload names are chosen to collide with
legitimate files (Math_Symbol.js ships in regenerate-unicode-properties, setup.mjs
ships in motion-dom). On a normal workstation a filename sweep returns dozens of
benign hits and no signal. The preinstall entry and the hashes are what discriminate.

Usage:
  ./supply-chain-triage.py                      # scan $HOME, human output
  ./supply-chain-triage.py ~/Sites ~/work       # scan specific roots
  ./supply-chain-triage.py --json               # machine-readable
  ./supply-chain-triage.py --threat-db PATH     # custom threat-db.yaml
  ./supply-chain-triage.py --max-depth 6        # limit lockfile/config walk
  ./supply-chain-triage.py --fast               # skip hashing (seconds, not minutes)

Runtime: hashing dominates. Measured on a dev machine with 337 lockfiles and
152,491 installed package.json, a full run took 5m42s and --fast took 1m43s, both
returning the same verdict. Reach for --fast when triaging many machines, then
hash only the ones that flag.

Exit codes: 0 = nothing found, 1 = findings, 2 = error.
"""

import argparse
import hashlib
import json
import os
import re
import sys

DEFAULT_THREAT_DB = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "commands", "resources", "threat-db.yaml",
)

SKIP_DIRS = {".git", "dist", "build", ".next", "target", ".venv", "venv", "__pycache__"}
LOCKFILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "bun.lock", "bun.lockb", "npm-shrinkwrap.json",
}
STARTUP_EVENTS = ("SessionStart", "Setup", "InstructionsLoaded", "DirectoryAdded")

# Dropper entrypoint, matched only inside a preinstall value, never as a filename.
#
# Deliberately narrow. An earlier draft also matched install.js and postinstall,
# which flagged esbuild's entirely legitimate "postinstall": "node install.js".
# Native-binary packages (esbuild, sharp, swc, playwright) all ship postinstall
# fetchers, so postinstall carries no signal. The campaign signature is preinstall
# invoking setup.mjs, on packages that never had any lifecycle script before.
# Variants are caught by the hash check instead.
DROPPER = re.compile(r"\bsetup\.(mjs|cjs)\b", re.I)

WATCHER_PATHS = [
    "~/.local/bin/gh-token-monitor.sh",
    "~/.config/systemd/user/gh-token-monitor.service",
    "~/Library/LaunchAgents/com.user.gh-token-monitor.plist",
]

C = {
    "red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[1;33m",
    "blue": "\033[0;34m", "cyan": "\033[0;36m", "dim": "\033[2m", "off": "\033[0m",
}


def paint(text, color, enabled):
    return f"{C[color]}{text}{C['off']}" if enabled else text


def load_threat_db(path):
    """Pull the npm IOC set out of threat-db.yaml.

    Falls back to a minimal built-in set if PyYAML or the file is unavailable, so
    the script still runs on a quarantined machine with no pip access.
    """
    fallback = {
        "versions": {
            "keyv": {"6.0.0"}, "flat-cache": {"6.1.24"},
            "file-entry-cache": {"11.1.6"}, "cacheable-request": {"13.0.20"},
            "cacheable": {"2.5.1"}, "cache-manager": {"7.2.10"},
            "@cacheable/memory": {"2.2.1"}, "@cacheable/utils": {"2.5.1"},
            "@cacheable/node-cache": {"3.1.2"}, "@cacheable/net": {"2.1.1"},
            "ecto": {"5.0.1"}, "@deliveroo/reevent": {"1.0.1"},
            "@or-sdk/invitations": {"1.4.9"}, "@picsart/ai-sdk": {"3.32.2"},
            "@qlik/embed-runtime": {"1.6.4"}, "picasso.js": {"2.11.6"},
        },
        "hashes": {
            "54dc7ea54a1317cca0e890a2770630cf7fa6c97813e0cb9d2caa93012b350668":
                "setup.mjs stage 1 dropper",
            "fd3ca4007b225fdf8de7af4345a19179d5efa8c4bb9205f88cda806e5684b1eb":
                "setup.mjs worm-propagation variant",
            "9fc2570b7cef51c1b8df116d144d11ff4096357be7d2c4c6367cfc2509cf1bcc":
                "Math_Symbol.js / math_init.js stage 2 payload",
        },
        "domains": {"npm-cache.com", "pypi-get.com", "js-mirror.com"},
        "source": "built-in fallback",
    }

    try:
        import yaml
    except ImportError:
        fallback["source"] = "built-in fallback (PyYAML not installed)"
        return fallback
    try:
        with open(path, encoding="utf-8") as fh:
            db = yaml.safe_load(fh)
    except Exception:
        fallback["source"] = f"built-in fallback ({path} unreadable)"
        return fallback

    versions = {}
    for entry in db.get("malicious_skills") or []:
        if entry.get("platform") != "npm" or not entry.get("version"):
            continue
        name = entry.get("name", "")
        if name.endswith("/*"):          # wildcard scope, handled separately
            continue
        versions.setdefault(name, set()).add(str(entry["version"]))

    hashes = {
        h["hash"]: h.get("type", "known payload")
        for h in (db.get("iocs", {}).get("malware_hashes") or [])
        if len(h.get("hash", "")) == 64          # skip the abbreviated ones
    }
    domains = {
        d["domain"] for d in (db.get("iocs", {}).get("malicious_domains") or [])
        if d.get("domain")
    }

    if not versions:
        return fallback
    return {
        "versions": versions, "hashes": hashes, "domains": domains,
        "source": f"{path} (v{db.get('version', '?')}, updated {db.get('updated', '?')})",
    }


def walk(roots, max_depth):
    """Yield (dirpath, filenames), pruning noise and honouring a depth budget."""
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        if not os.path.isdir(root):
            continue
        base = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            if dirpath.count(os.sep) - base >= max_depth:
                dirnames[:] = []
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            yield dirpath, filenames


def resolved_pairs(path, name):
    """Yield (package, version) from a lockfile, parsed per format.

    A single regex over the raw text does not work here: npm writes the name and
    version on separate lines ("node_modules/keyv": {\\n "version": "6.0.0"), so a
    proximity match either misses it or, widened enough to catch it, starts pairing
    a name with the neighbouring entry's version.
    """
    if name in ("package-lock.json", "npm-shrinkwrap.json"):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            return
        for key, meta in (data.get("packages") or {}).items():
            if not isinstance(meta, dict) or not meta.get("version"):
                continue
            pkg = meta.get("name") or key.split("node_modules/")[-1]
            if pkg:
                yield pkg, str(meta["version"])
        stack = [data.get("dependencies") or {}]
        while stack:
            deps = stack.pop()
            if not isinstance(deps, dict):
                continue
            for pkg, meta in deps.items():
                if isinstance(meta, dict):
                    if meta.get("version"):
                        yield pkg, str(meta["version"])
                    if meta.get("dependencies"):
                        stack.append(meta["dependencies"])
        return

    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return

    if name == "pnpm-lock.yaml":
        # /keyv@6.0.0: or  keyv@6.0.0:  depending on lockfileVersion
        for match in re.finditer(r"^\s*/?((?:@[^/\s]+/)?[^@/\s:]+)@([0-9][^\s:(]*)",
                                 text, re.M):
            yield match.group(1), match.group(2)
        return

    if name == "yarn.lock":
        # "keyv@^6.0.0":  then  version "6.0.0"  on a later line
        current = []
        for line in text.splitlines():
            if line and not line[0].isspace() and not line.startswith("#"):
                current = re.findall(r'"?((?:@[^/\s]+/)?[^@\s",]+)@', line)
            else:
                match = re.match(r'\s+version:?\s+"?([^"\s]+)"?', line)
                if match and current:
                    for pkg in current:
                        yield pkg, match.group(1)
        return

    # bun.lock and anything else: fall back to the compact name@version form
    for match in re.finditer(r'((?:@[^/\s"]+/)?[a-zA-Z0-9._-]+)@([0-9][0-9A-Za-z.\-+]*)',
                             text):
        yield match.group(1), match.group(2)


def check_lockfiles(roots, iocs, max_depth, stats):
    findings = []
    for dirpath, filenames in walk(roots, max_depth):
        if os.path.basename(dirpath) == "node_modules":
            continue
        for name in filenames:
            if name not in LOCKFILES:
                continue
            path = os.path.join(dirpath, name)
            stats["lockfiles"] += 1
            seen = set()
            for pkg, version in resolved_pairs(path, name):
                if version in iocs["versions"].get(pkg, ()) and (pkg, version) not in seen:
                    seen.add((pkg, version))
                    findings.append({
                        "check": "lockfile", "severity": "critical",
                        "path": path, "detail": f"{pkg}@{version}",
                    })
    return findings


def check_installed(roots, iocs, stats, do_hash=True):
    """The high-signal check: a dependency declaring a dropper as preinstall."""
    findings = []
    wanted = set(iocs["hashes"]) if do_hash else set()
    for dirpath, filenames in walk(roots, 99):
        in_modules = f"{os.sep}node_modules{os.sep}" in dirpath + os.sep
        if not in_modules:
            continue
        if "package.json" in filenames:
            path = os.path.join(dirpath, "package.json")
            stats["package_json"] += 1
            try:
                scripts = (json.load(open(path, encoding="utf-8")) or {}).get("scripts")
            except Exception:
                scripts = None
            if isinstance(scripts, dict):
                value = str(scripts.get("preinstall", ""))
                if value and DROPPER.search(value):
                    findings.append({
                        "check": "lifecycle", "severity": "critical",
                        "path": path, "detail": f"preinstall: {value}",
                    })
        if wanted:
            for name in filenames:
                if not name.endswith((".js", ".mjs", ".cjs")):
                    continue
                path = os.path.join(dirpath, name)
                try:
                    if os.path.getsize(path) > 4_000_000:
                        continue
                    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
                except OSError:
                    continue
                stats["hashed"] += 1
                if digest in wanted:
                    findings.append({
                        "check": "hash", "severity": "critical",
                        "path": path, "detail": f"{iocs['hashes'][digest]} ({digest[:16]}...)",
                    })
    return findings


def check_startup_hooks(roots, max_depth, stats):
    findings = []
    for dirpath, filenames in walk(roots, max_depth):
        if f"{os.sep}node_modules{os.sep}" in dirpath + os.sep:
            continue
        base = os.path.basename(dirpath)
        if base == ".claude":
            for name in filenames:
                if not (name.startswith("settings") and name.endswith(".json")):
                    continue
                path = os.path.join(dirpath, name)
                stats["configs"] += 1
                try:
                    hooks = (json.load(open(path, encoding="utf-8")) or {}).get("hooks") or {}
                except Exception:
                    continue
                for event in STARTUP_EVENTS:
                    for group in hooks.get(event) or []:
                        for hook in group.get("hooks") or []:
                            findings.append({
                                "check": "startup-hook", "severity": "review",
                                "path": path,
                                "detail": f"{event}: {hook.get('command', '(no command)')}",
                            })
        if base == ".vscode" and "tasks.json" in filenames:
            path = os.path.join(dirpath, "tasks.json")
            stats["configs"] += 1
            try:
                tasks = (json.load(open(path, encoding="utf-8")) or {}).get("tasks") or []
            except Exception:
                tasks = []
            for task in tasks:
                run_on = (task.get("runOptions") or {}).get("runOn")
                if run_on == "folderOpen":
                    findings.append({
                        "check": "startup-hook", "severity": "review", "path": path,
                        "detail": f"folderOpen task {task.get('label', '?')}: "
                                  f"{task.get('command', '?')}",
                    })
    return findings


def check_persistence():
    findings = []
    for raw in WATCHER_PATHS:
        path = os.path.expanduser(raw)
        if os.path.exists(path):
            findings.append({
                "check": "persistence", "severity": "critical", "path": path,
                "detail": "known token-revocation watcher path. Remove BEFORE rotating.",
            })
    agents = os.path.expanduser("~/Library/LaunchAgents")
    if os.path.isdir(agents):
        for name in os.listdir(agents):
            if re.search(r"token|monitor|npm-cache", name, re.I):
                findings.append({
                    "check": "persistence", "severity": "review",
                    "path": os.path.join(agents, name),
                    "detail": "LaunchAgent name matches watcher naming patterns",
                })
    return findings


def check_egress(iocs):
    findings = []
    for raw in ("~/.npmrc", "/etc/hosts", "~/.yarnrc.yml", "~/.bunfig.toml"):
        path = os.path.expanduser(raw)
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for domain in iocs["domains"]:
            if domain in text:
                findings.append({
                    "check": "egress", "severity": "critical", "path": path,
                    "detail": f"attacker domain {domain} present",
                })
    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Triage a workstation after an npm supply chain incident.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("roots", nargs="*", default=[os.path.expanduser("~")],
                        help="directories to scan (default: $HOME)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--threat-db", default=DEFAULT_THREAT_DB,
                        help="path to threat-db.yaml")
    parser.add_argument("--max-depth", type=int, default=6,
                        help="depth budget for the lockfile and config walk (default: 6)")
    parser.add_argument("--fast", action="store_true",
                        help="skip payload hashing (seconds instead of minutes)")
    args = parser.parse_args()

    color = sys.stdout.isatty() and not args.json
    iocs = load_threat_db(args.threat_db)
    stats = {"lockfiles": 0, "package_json": 0, "configs": 0, "hashed": 0}

    findings = []
    findings += check_lockfiles(args.roots, iocs, args.max_depth, stats)
    findings += check_installed(args.roots, iocs, stats, do_hash=not args.fast)
    findings += check_startup_hooks(args.roots, args.max_depth, stats)
    findings += check_persistence()
    findings += check_egress(iocs)

    critical = [f for f in findings if f["severity"] == "critical"]
    review = [f for f in findings if f["severity"] == "review"]

    if args.json:
        json.dump({
            "ioc_source": iocs["source"], "stats": stats,
            "critical": critical, "review": review,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1 if findings else 0

    print(paint("npm supply chain triage", "cyan", color))
    print(paint(f"  IOC source: {iocs['source']}", "dim", color))
    print(paint(f"  scanned: {stats['lockfiles']} lockfiles, "
                f"{stats['package_json']} installed package.json, "
                f"{stats['configs']} agent/editor configs, "
                + ("hashing skipped (--fast)" if args.fast
                   else f"{stats['hashed']} scripts hashed"), "dim", color))
    print()

    if critical:
        print(paint(f"CRITICAL ({len(critical)})", "red", color))
        for f in critical:
            print(f"  [{f['check']}] {f['path']}")
            print(paint(f"      {f['detail']}", "dim", color))
        print()
    if review:
        print(paint(f"REVIEW ({len(review)})", "yellow", color))
        print(paint("  Startup hooks are legitimate in many projects. Confirm each one "
                    "belongs to that repo.", "dim", color))
        for f in review:
            print(f"  [{f['check']}] {f['path']}")
            print(paint(f"      {f['detail']}", "dim", color))
        print()

    if not findings:
        print(paint("No indicators found.", "green", color))
        print(paint("  A clean result covers this IOC set only. It is not a "
                    "guarantee of a clean machine.", "dim", color))
        return 0

    if critical:
        print(paint("Next steps, in this order:", "blue", color))
        print("  1. Isolate the host. Do NOT rotate credentials yet.")
        print("  2. Remove persistence and watcher entries found above.")
        print("  3. Block egress to the attacker domains.")
        print("  4. Rotate from a clean machine: npm, GitHub, cloud, k8s, Vault, SSH, CI, .env.")
        print("  5. Rebuild runners and workstations from clean images.")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
