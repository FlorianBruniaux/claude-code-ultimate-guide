#!/usr/bin/env python3
"""
smart-suggest-roi.py — Analyze acceptance rate of smart-suggest hook suggestions.

Usage:
  ./smart-suggest-roi.py                  # Full report
  ./smart-suggest-roi.py --json           # Machine-readable JSON
  ./smart-suggest-roi.py --since 7d       # Last N days
  ./smart-suggest-roi.py --no-sessions    # Suggestion stats only (fast)
  ./smart-suggest-roi.py --log PATH       # Custom log path

Methodology: "Followed" = the suggested command/agent was used later in the
same session. Proxy metric — user may have used it independently of the
suggestion, or in a different session.
"""

import argparse
import bisect
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Tier classification (extensible mapping)
# ---------------------------------------------------------------------------
TIER_MAP = {
    # Tier 0 — Enforcement (high-stakes, process gates)
    "pnpm changelog:add": 0,
    "/pr": 0,
    "/plan": 0,
    "/tech:plan": 0,
    "/tech:pr": 0,
    "/tech:commit": 0,
    # Tier 1 — Discovery (specialized workflows rarely triggered organically)
    "/test-loop": 1,
    "/retex": 1,
    "/tech:retex": 1,
    "/dupes": 1,
    "/tech:dupes": 1,
    "/loop": 1,
    "security-auditor": 1,
    "/release": 1,
    "/tech:ralph-loop": 1,
    "/tech:scaffold": 1,
    "/tech:sonarqube": 1,
    "complexity-estimator": 1,
    "/tech:diagram": 1,
    "/tech:handoff": 1,
    "/tech:daily": 1,
    "/tech:bilan-hebdo": 1,
    "/tech:worktree": 1,
    "/tech:sentry-triage": 1,
    "skill-creator": 1,
    "/tech:create-release": 1,
    "/tech:tests": 1,
    "/tech:diagnose": 1,
    # Tier 2 — Contextual (common helpers, lower novelty)
    "code-reviewer": 2,
    "debugger": 2,
    "architect-review": 2,
    "/resume": 2,
    "/tech:resume": 2,
    "ui-designer": 2,
    "requirements-analyst": 2,
    "backend-architect": 2,
    "/tech:ship": 2,
    "/critique-plan": 2,
}

TIER_LABELS = {0: "Tier 0 (Enforcement)", 1: "Tier 1 (Discovery)", 2: "Tier 2 (Contextual)", -1: "Custom"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_ts(ts_str: str) -> float:
    """Parse ISO 8601 timestamp to Unix epoch float."""
    if not ts_str:
        return 0.0
    ts_str = ts_str.rstrip("Z")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(ts_str, fmt).replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except ValueError:
            continue
    return 0.0


def first_token(cmd: str) -> str:
    """Return first whitespace-delimited token (for commands like '/loop [interval]')."""
    return cmd.split()[0] if cmd else cmd


def get_tier(cmd: str) -> int:
    """Classify a command into a tier. Returns -1 for unknown (Custom)."""
    return TIER_MAP.get(cmd, TIER_MAP.get(first_token(cmd), -1))


def parse_since(since_str: str) -> float:
    """Parse '7d', '24h', '30m' into a Unix timestamp cutoff."""
    unit = since_str[-1]
    value = int(since_str[:-1])
    now = datetime.now(tz=timezone.utc).timestamp()
    if unit == "d":
        return now - value * 86400
    if unit == "h":
        return now - value * 3600
    if unit == "m":
        return now - value * 60
    raise ValueError(f"Unsupported time unit: {unit}. Use d/h/m (e.g. 7d, 24h).")


# ---------------------------------------------------------------------------
# Phase 1 — Parse suggestions log
# ---------------------------------------------------------------------------

def parse_suggestions(log_path: Path, since_ts: float = 0.0):
    """
    Returns list of suggestion dicts and skip count.
    Each dict: {ts, suggested, prompt_len, cmd (first token)}
    """
    suggestions = []
    skip_count = 0

    if not log_path.exists():
        return suggestions, skip_count

    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = parse_ts(entry.get("ts", ""))
                if ts == 0.0:
                    skip_count += 1
                    continue
                if ts < since_ts:
                    continue
                suggested = entry.get("suggested", "")
                if not suggested:
                    skip_count += 1
                    continue
                suggestions.append({
                    "ts": ts,
                    "suggested": suggested,
                    "cmd": first_token(suggested),
                    "prompt_len": entry.get("prompt_len", 0),
                })
            except (json.JSONDecodeError, KeyError, TypeError):
                skip_count += 1

    suggestions.sort(key=lambda x: x["ts"])
    return suggestions, skip_count


# ---------------------------------------------------------------------------
# Phase 2 — Build session index & detect acceptance
# ---------------------------------------------------------------------------

def _read_first_last_ts(path: Path):
    """Read first and last timestamp from a session JSONL file efficiently."""
    first_ts = None
    last_ts = None
    session_id = None

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = parse_ts(entry.get("timestamp", ""))
                    if ts == 0.0:
                        continue
                    if first_ts is None:
                        first_ts = ts
                        session_id = entry.get("sessionId", "")
                    last_ts = ts
                except (json.JSONDecodeError, TypeError):
                    continue
    except (PermissionError, OSError):
        pass

    return first_ts, last_ts, session_id


def build_session_index(projects_dir: Path):
    """
    Walk all project JSONL session files and build a sorted index for lookup.

    Returns:
      - sessions: list of {start_ts, end_ts, session_id, path} sorted by start_ts
      - start_ts_list: just start timestamps for bisect
    """
    sessions = []

    if not projects_dir.exists():
        return sessions, []

    for jsonl_file in projects_dir.glob("*/*.jsonl"):
        # Skip activity logs and smart-suggest logs (not session files)
        if "activity-" in jsonl_file.name or "smart-suggest" in jsonl_file.name:
            continue
        first_ts, last_ts, session_id = _read_first_last_ts(jsonl_file)
        if first_ts is None:
            continue
        sessions.append({
            "start_ts": first_ts,
            "end_ts": last_ts or first_ts,
            "session_id": session_id,
            "path": jsonl_file,
        })

    sessions.sort(key=lambda x: x["start_ts"])
    start_ts_list = [s["start_ts"] for s in sessions]
    return sessions, start_ts_list


def find_sessions_for_ts(ts: float, sessions: list, start_ts_list: list, window_before: float = 120.0):
    """
    Find sessions that were active at timestamp ts.
    A session is "active" if ts is between start and end (+ small buffer).
    """
    if not sessions:
        return []

    # Binary search: find sessions that started before ts + window_before
    hi = bisect.bisect_right(start_ts_list, ts + window_before)
    candidates = sessions[:hi]

    active = []
    for s in candidates:
        if s["start_ts"] <= ts + window_before and s["end_ts"] >= ts - 30:
            active.append(s)
    return active


def _check_acceptance_in_session(path: Path, cmd_token: str, suggestion_ts: float, time_window: float = 600.0):
    """
    Scan a session JSONL file for evidence the suggested command was followed.

    Acceptance signals (in priority order):
      1. <command-name>cmd</command-name> in user message content
      2. Skill tool use with skill = cmd
      3. Agent tool use with subagent_type = cmd
      4. cmd appears in next 5 user messages within time_window seconds
    """
    entries_after = []

    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = parse_ts(entry.get("timestamp", ""))
                    if ts >= suggestion_ts:
                        entries_after.append((ts, entry))
                except (json.JSONDecodeError, TypeError):
                    continue
    except (PermissionError, OSError):
        return None  # Cannot read file

    if not entries_after:
        return None  # No entries after suggestion — cannot determine

    user_message_count = 0

    for ts, entry in entries_after:
        msg_type = entry.get("type", "")
        msg = entry.get("message", {})
        if not isinstance(msg, dict):
            continue

        role = msg.get("role", "")
        content = msg.get("content", "")

        # Signal 1: slash command invocation in user message
        if msg_type == "user" or role == "user":
            user_message_count += 1
            content_str = content if isinstance(content, str) else json.dumps(content)
            # Check for <command-name> tag
            if f"<command-name>{cmd_token}</command-name>" in content_str:
                return True
            # Check for skill invocation pattern
            if f'"skill": "{cmd_token}"' in content_str or f"'skill': '{cmd_token}'" in content_str:
                return True
            # Text mention in first 5 user messages within window
            if user_message_count <= 5 and ts - suggestion_ts <= time_window:
                if cmd_token in content_str:
                    return True

        # Signal 2 & 3: tool use in assistant messages
        if msg_type == "assistant" or role == "assistant":
            content_list = content if isinstance(content, list) else []
            for block in content_list:
                if not isinstance(block, dict):
                    continue
                if block.get("type") != "tool_use":
                    continue
                tool_name = block.get("name", "")
                tool_input = block.get("input", {}) or {}
                # Signal 2: Skill tool
                if tool_name == "Skill" and tool_input.get("skill") == cmd_token:
                    return True
                # Signal 3: Agent tool
                if tool_name == "Agent" and tool_input.get("subagent_type") == cmd_token:
                    return True

    return False  # No signals found


def compute_acceptance(suggestions: list, sessions: list, start_ts_list: list):
    """
    For each suggestion, find matching sessions and check acceptance.
    Mutates each suggestion dict in-place, adding 'followed' key.
    """
    for s in suggestions:
        active = find_sessions_for_ts(s["ts"], sessions, start_ts_list)
        if not active:
            s["followed"] = None  # No session context
            continue

        # Check all active sessions — accepted if ANY matches
        result = False
        any_data = False
        for sess in active:
            check = _check_acceptance_in_session(sess["path"], s["cmd"], s["ts"])
            if check is True:
                result = True
                any_data = True
                break
            if check is False:
                any_data = True
            # check is None: no data in this file

        if not any_data:
            s["followed"] = None
        else:
            s["followed"] = result


# ---------------------------------------------------------------------------
# Phase 3 — Compute stats
# ---------------------------------------------------------------------------

def compute_stats(suggestions: list):
    """Build stats dict from annotated suggestions."""
    stats = {
        "total": len(suggestions),
        "sessions_matched": sum(1 for s in suggestions if s.get("followed") is not None),
        "followed": sum(1 for s in suggestions if s.get("followed") is True),
        "by_cmd": defaultdict(lambda: {"total": 0, "followed": 0, "unmatched": 0}),
        "by_tier": defaultdict(lambda: {"total": 0, "followed": 0}),
        "by_day": defaultdict(lambda: {"total": 0, "followed": 0}),
    }

    for s in suggestions:
        cmd = s["cmd"]
        tier = get_tier(s["suggested"])
        day = datetime.fromtimestamp(s["ts"], tz=timezone.utc).strftime("%b %d")

        stats["by_cmd"][cmd]["total"] += 1
        stats["by_tier"][tier]["total"] += 1
        stats["by_day"][day]["total"] += 1

        if s.get("followed") is True:
            stats["by_cmd"][cmd]["followed"] += 1
            stats["by_tier"][tier]["followed"] += 1
            stats["by_day"][day]["followed"] += 1
        elif s.get("followed") is None:
            stats["by_cmd"][cmd]["unmatched"] += 1

    # Compute unique commands
    stats["unique_cmds"] = len(stats["by_cmd"])

    return stats


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def pct(num: int, den: int) -> str:
    if den == 0:
        return "n/a"
    return f"{round(100 * num / den)}%"


def bar(count: int, max_count: int, width: int = 16) -> str:
    if max_count == 0:
        return ""
    filled = round(width * count / max_count)
    return "█" * filled + " " * (width - filled)


def print_report(stats: dict, suggestions: list, skip_count: int,
                 log_path: Path, projects_dir: Path, no_sessions: bool, since_str: str | None):
    sep = "═" * 51
    print(sep)
    since_label = f" ({since_str})" if since_str else f" ({_date_range(suggestions)})"
    print(f"  Smart-Suggest ROI Report{since_label}")
    print(sep)

    print()
    print("Summary")
    print(f"  Suggestions emitted:   {stats['total']}")
    print(f"  Unique commands:       {stats['unique_cmds']}")

    if not no_sessions:
        matched = stats["sessions_matched"]
        total = stats["total"]
        followed = stats["followed"]
        print(f"  Sessions matched:      {matched} / {total} ({pct(matched, total)})")
        print(f"  Followed:              {followed} / {matched} ({pct(followed, matched)})")

    # By tier
    if not no_sessions:
        print()
        print(f"{'By Tier':<38} {'followed / total'}")
        for tier_id in sorted(stats["by_tier"].keys()):
            t = stats["by_tier"][tier_id]
            label = TIER_LABELS.get(tier_id, "Custom")
            rate = pct(t["followed"], t["total"])
            print(f"  {label + ':':34} {rate:<8} {t['followed']:>4} / {t['total']}")

    # Top 10 most suggested
    by_cmd = stats["by_cmd"]
    sorted_by_total = sorted(by_cmd.items(), key=lambda x: x[1]["total"], reverse=True)
    print()
    print("Top 10 Most Suggested")
    for cmd, data in sorted_by_total[:10]:
        rate = f"{pct(data['followed'], data['total'])} followed" if not no_sessions else ""
        print(f"  {data['total']:>4}  {cmd:<34} {rate}")

    # Top 10 most followed (only if session data available)
    if not no_sessions and stats["followed"] > 0:
        sorted_by_followed = sorted(
            [(cmd, d) for cmd, d in by_cmd.items() if d["followed"] > 0],
            key=lambda x: x[1]["followed"],
            reverse=True,
        )
        print()
        print("Top 10 Most Followed")
        for cmd, data in sorted_by_followed[:10]:
            rate = pct(data["followed"], data["total"])
            print(f"  {data['followed']:>4}  {cmd:<34} {rate} of {data['total']}")

        # Never followed
        never = [(cmd, d) for cmd, d in by_cmd.items()
                 if d["followed"] == 0 and d["total"] - d["unmatched"] > 0]
        if never:
            print()
            print("Never Followed (always ignored)")
            for cmd, data in sorted(never, key=lambda x: x[1]["total"], reverse=True)[:10]:
                print(f"  {cmd:<36} ({data['total']} suggestions)")

    # Daily trend
    by_day = stats["by_day"]
    if by_day:
        print()
        print("Daily Trend")
        max_day_total = max(d["total"] for d in by_day.values())
        for day in sorted(by_day.keys()):
            d = by_day[day]
            b = bar(d["total"], max_day_total)
            followed_str = f"  ({d['followed']} followed)" if not no_sessions else ""
            print(f"  {day}  {b}  {d['total']}{followed_str}")

    print()
    if not no_sessions:
        print("Note: \"Followed\" means the suggested command/agent was used later in the")
        print("same session. Proxy metric — the user may have used it independently of")
        print("the suggestion, or followed it in a different session.")
        print()

    if skip_count > 0:
        print(f"  [{skip_count} malformed lines skipped]")

    print(sep)
    print(f"  Log: {log_path}")
    if not no_sessions:
        from pathlib import Path as _P
        project_count = sum(1 for _ in projects_dir.glob("*/"))
        print(f"  Sessions: {projects_dir} ({project_count} projects)")
    print(sep)


def _date_range(suggestions: list) -> str:
    if not suggestions:
        return "no data"
    first = datetime.fromtimestamp(suggestions[0]["ts"], tz=timezone.utc)
    last = datetime.fromtimestamp(suggestions[-1]["ts"], tz=timezone.utc)
    delta = last - first
    days = max(1, delta.days + 1)
    return f"{days} days"


def print_json(stats: dict, suggestions: list, skip_count: int):
    output = {
        "summary": {
            "total": stats["total"],
            "unique_cmds": stats["unique_cmds"],
            "sessions_matched": stats["sessions_matched"],
            "followed": stats["followed"],
            "follow_rate": round(stats["followed"] / stats["sessions_matched"], 3)
            if stats["sessions_matched"] > 0 else None,
        },
        "by_cmd": {
            cmd: {
                "total": d["total"],
                "followed": d["followed"],
                "unmatched": d["unmatched"],
                "follow_rate": round(d["followed"] / (d["total"] - d["unmatched"]), 3)
                if (d["total"] - d["unmatched"]) > 0 else None,
            }
            for cmd, d in stats["by_cmd"].items()
        },
        "by_tier": {
            TIER_LABELS.get(t, "Custom"): {
                "total": d["total"],
                "followed": d["followed"],
                "follow_rate": round(d["followed"] / d["total"], 3) if d["total"] > 0 else None,
            }
            for t, d in stats["by_tier"].items()
        },
        "by_day": dict(stats["by_day"]),
        "skip_count": skip_count,
    }
    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyze smart-suggest hook ROI from suggestion and session logs."
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path.home() / ".claude" / "logs" / "smart-suggest.jsonl",
        help="Path to smart-suggest.jsonl log (default: ~/.claude/logs/smart-suggest.jsonl)",
    )
    parser.add_argument(
        "--projects-dir",
        type=Path,
        default=Path.home() / ".claude" / "projects",
        help="Path to Claude projects directory (default: ~/.claude/projects)",
    )
    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Filter to last N days/hours/minutes (e.g. 7d, 24h, 30m)",
    )
    parser.add_argument(
        "--no-sessions",
        action="store_true",
        help="Skip session scanning — show suggestion stats only (fast mode)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON",
    )
    args = parser.parse_args()

    # Resolve since cutoff
    since_ts = 0.0
    if args.since:
        try:
            since_ts = parse_since(args.since)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Phase 1: parse suggestions
    suggestions, skip_count = parse_suggestions(args.log, since_ts)

    if not suggestions:
        print(f"No suggestions found in {args.log}", file=sys.stderr)
        if since_ts > 0:
            print(f"(filtered to last {args.since})", file=sys.stderr)
        sys.exit(0)

    # Phase 2: session index + acceptance (unless --no-sessions)
    if not args.no_sessions:
        sessions, start_ts_list = build_session_index(args.projects_dir)
        compute_acceptance(suggestions, sessions, start_ts_list)
    else:
        # Mark all as unmatched so stats are computed correctly
        for s in suggestions:
            s["followed"] = None

    # Phase 3: stats
    stats = compute_stats(suggestions)

    # Output
    if args.json:
        print_json(stats, suggestions, skip_count)
    else:
        print_report(
            stats, suggestions, skip_count,
            args.log, args.projects_dir, args.no_sessions, args.since
        )


if __name__ == "__main__":
    main()
