#!/usr/bin/env python3
# Source: https://github.com/FlorianBruniaux/cc-sessions
"""
cc-sessions — Fast CLI to search, browse & resume Claude Code session history

OVERVIEW
--------
Claude Code stores all conversation history locally in ~/.claude/projects/ as JSONL files.
This tool indexes those sessions for fast search and provides a clean CLI interface to:
  - Search by keyword across all conversations
  - Filter by date, branch, or project
  - View recent sessions
  - Resume past sessions with partial ID matching
  - Discover recurring patterns to extract as skills, commands, or CLAUDE.md rules

FEATURES
--------
- ⚡ Incremental indexing: ~200ms search on 1300+ sessions (vs ~5s full scan)
- 📁 Project-scoped by default: auto-detects current project from pwd
- 🔍 Powerful filters: --since 7d, --branch develop, --limit N
- 🎯 Partial ID matching: 'cc-sessions resume 8d472d' finds full session ID
- 🌳 Worktree support: includes git worktree sessions automatically
- 📊 JSON output: pipe to jq/fzf for advanced workflows
- 🔭 Pattern discovery: analyze sessions to suggest skills/commands/rules
- 🐍 Zero dependencies: Python stdlib only (json, argparse, pathlib)

USAGE
-----
# Search in current project
cc-sessions search "notion"

# Search all projects
cc-sessions --all search "stripe"

# Filter by date and branch
cc-sessions search "auth" --since 7d --branch develop --limit 5

# Recent sessions
cc-sessions recent 10

# Session details (partial ID match)
cc-sessions info 8d472d2c

# Resume session (execs: claude --resume <full-id>)
cc-sessions resume 8d472d2c

# Force rebuild index
cc-sessions reindex

# Discover patterns (all projects, last 90 days)
cc-sessions discover

# Discover with custom filters
cc-sessions --all discover --since 60d --min-count 2 --top 15

# JSON output for composition
cc-sessions --json search "prisma" | jq -r '.[].id'

INSTALLATION
------------
1. Save this script to ~/bin/cc-sessions
2. chmod +x ~/bin/cc-sessions
3. Run: cc-sessions recent 5
   (First run builds index ~10s for 1500 sessions, then <200ms)

Or install from GitHub:
  curl -sL https://raw.githubusercontent.com/FlorianBruniaux/cc-sessions/main/cc-sessions \
    -o ~/.local/bin/cc-sessions && chmod +x ~/.local/bin/cc-sessions

INDEX ARCHITECTURE
------------------
- Location: ~/.claude/sessions-index.jsonl (~360KB for 1300 sessions)
- Format: One JSON object per line with session metadata
- Update strategy: Incremental (only re-parses modified files)
- Rebuild: Automatic on search/recent, manual with 'reindex'

Session metadata extracted:
  - id: Full session UUID
  - project: Encoded project path
  - branch: Git branch from JSONL gitBranch field
  - context: First significant user message (60 chars)
  - timestamp: ISO 8601 datetime
  - mtime: File modification time (for incremental updates)

FILTERING RULES
---------------
Significant user message = all 3 conditions:
  1. entry['type'] == 'user'
  2. content is string (not array = tool_result)
  3. content doesn't start with '<' (excludes XML internal tags)

This covers all current and future Claude Code internal messages:
  - <command-name>, <command-message>, <local-command-stdout>
  - <bash-input>, <bash-stdout>, <task-notification>
  - Any future XML-formatted system messages

Subagent sessions (prefix 'agent-') are excluded by default.

PERFORMANCE
-----------
- First run (build index): ~10s for 1500 sessions
- Subsequent searches: ~200ms (reads index)
- Incremental rebuild: <1s if no changes
- Index size: ~280 bytes per session

OUTPUT FORMAT
-------------
2026-02-05 17:15  8d472d2c-128b-4d9b-824d-3944e3409984  develop   "Migration Support Slack → Notion..."
│                 │                                     │         │
Date/Time         Full Session ID (for --resume)      Branch    First user message (60 chars)

ECOSYSTEM
---------
Similar tools:
  - claude-history (Rust): Fuzzy search with fzf
  - cclog (Go): JSONL → HTML/Markdown + TUI
  - claude-code-history-viewer (Tauri): Desktop GUI
  - fast-resume (Rust): Tantivy index + TUI

cc-sessions positioning: Unix-style CLI, fast search, powerful filters, no dependencies.

AUTHOR
------
Created for terminal power users who prefer CLI over GUI.
GitHub: https://github.com/FlorianBruniaux/cc-sessions
Gist: https://gist.github.com/FlorianBruniaux/992d4d1107592d9e98ca9d89838871c6
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

CLAUDE_DIR = Path.home() / ".claude"
INDEX_PATH = CLAUDE_DIR / "sessions-index.jsonl"
DISCOVER_CACHE_PATH = CLAUDE_DIR / "discover-cache.jsonl"

LLM_BATCH_SIZE = 60
LLM_DEFAULT_MODEL = ''  # empty = use claude CLI default model


def parse_duration(duration_str: str) -> datetime:
    """Parse duration string like '7d', '30d' or ISO date."""
    if duration_str.endswith('d'):
        days = int(duration_str[:-1])
        return datetime.now() - timedelta(days=days)
    return datetime.fromisoformat(duration_str)


def encode_project_path(path: Path) -> str:
    """Encode project path to match Claude's format."""
    return str(path).replace('/', '-')  # Keep leading - from root /


def detect_project() -> Optional[str]:
    """Detect current project from pwd."""
    pwd = Path.cwd()
    encoded = encode_project_path(pwd)
    project_dir = CLAUDE_DIR / "projects" / encoded

    if not project_dir.exists():
        return None
    return encoded


def get_project_dirs(all_projects: bool = False) -> List[Path]:
    """Get project directories to scan."""
    if all_projects:
        projects_dir = CLAUDE_DIR / "projects"
        if not projects_dir.exists():
            return []
        return [d for d in projects_dir.iterdir() if d.is_dir()]

    current = detect_project()
    if not current:
        return []

    dirs = []
    base = CLAUDE_DIR / "projects" / current
    dirs.append(base)

    # Include worktrees (glob pattern: --worktrees*)
    worktrees = list(base.parent.glob(f"{current}--worktrees*"))
    dirs.extend(worktrees)

    return dirs


def get_first_user_message(filepath: Path) -> Optional[str]:
    """Extract first significant user message from session JSONL."""
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)

                    # Rule 1: Must be user message
                    if entry.get('type') != 'user':
                        continue

                    content = entry.get('message', {}).get('content', '')

                    # Rule 2: Must be string (not array = tool_result)
                    if not isinstance(content, str):
                        continue

                    # Rule 3: Not internal XML message
                    if content.startswith('<'):
                        continue

                    # Found significant user message
                    return content[:60].replace('\n', ' ')
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass
    return None


def extract_all_user_messages(filepath: Path) -> List[str]:
    """Extract all significant user messages from a session JSONL file."""
    messages = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)

                    if entry.get('type') != 'user':
                        continue

                    content = entry.get('message', {}).get('content', '')

                    if not isinstance(content, str):
                        continue

                    if content.startswith('<'):
                        continue

                    stripped = content.strip()

                    # Skip very short messages (likely acknowledgements)
                    if len(stripped) < 10:
                        continue

                    # Skip system-injected messages (compact summaries, reminders)
                    # These are injected as plain-text user messages but aren't real user input
                    if len(stripped) > 800:
                        continue
                    if _is_system_injection(stripped):
                        continue

                    messages.append(stripped)
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass
    return messages


def parse_session(filepath: Path) -> Optional[Dict]:
    """Extract session metadata."""
    session_id = filepath.stem

    # Skip subagent sessions
    if session_id.startswith('agent-'):
        return None

    mtime = filepath.stat().st_mtime
    context = get_first_user_message(filepath)

    if not context:
        return None

    # Extract branch from gitBranch field in JSONL
    branch = "unknown"
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    git_branch = entry.get('gitBranch')
                    if git_branch:
                        branch = git_branch
                        break
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    project = filepath.parent.name

    return {
        "id": session_id,
        "project": project,
        "mtime": mtime,
        "branch": branch,
        "context": context,
        "timestamp": datetime.fromtimestamp(mtime).isoformat()
    }


def build_index(project_dirs: List[Path], existing_index: Dict[str, Dict]) -> Dict[str, Dict]:
    """Build or update index incrementally."""
    index = existing_index.copy()

    for project_dir in project_dirs:
        jsonl_files = list(project_dir.glob("*.jsonl"))

        for filepath in jsonl_files:
            session_id = filepath.stem
            file_mtime = filepath.stat().st_mtime

            # Skip if already indexed and not modified
            if session_id in index and index[session_id]['mtime'] >= file_mtime:
                continue

            # Parse session
            session = parse_session(filepath)
            if session:
                index[session_id] = session

    return index


def load_index() -> Dict[str, Dict]:
    """Load existing index."""
    if not INDEX_PATH.exists():
        return {}

    index = {}
    try:
        with open(INDEX_PATH, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                index[entry['id']] = entry
    except Exception as e:
        print(f"Warning: Failed to load index: {e}", file=sys.stderr)
        return {}

    return index


def save_index(index: Dict[str, Dict]):
    """Save index to disk."""
    CLAUDE_DIR.mkdir(exist_ok=True)

    with open(INDEX_PATH, 'w') as f:
        for entry in index.values():
            f.write(json.dumps(entry) + '\n')


def cmd_search(keyword: str, project_dirs: List[Path], limit: int = 10,
               since: Optional[str] = None, branch: Optional[str] = None,
               json_output: bool = False):
    """Search sessions by keyword."""
    # Build/update index
    existing = load_index()
    index = build_index(project_dirs, existing)
    save_index(index)

    # Filter
    matches = []
    since_dt = parse_duration(since) if since else None

    for entry in index.values():
        # Filter by project
        if not any(entry['project'] == d.name for d in project_dirs):
            continue

        # Filter by keyword (case-insensitive in context)
        if keyword.lower() not in entry['context'].lower():
            continue

        # Filter by date
        if since_dt:
            entry_dt = datetime.fromisoformat(entry['timestamp'])
            if entry_dt < since_dt:
                continue

        # Filter by branch
        if branch and entry['branch'] != branch:
            continue

        matches.append(entry)

    # Sort by timestamp desc
    matches.sort(key=lambda x: x['timestamp'], reverse=True)
    matches = matches[:limit]

    # Output
    if json_output:
        print(json.dumps(matches, indent=2))
    else:
        for m in matches:
            dt = datetime.fromisoformat(m['timestamp'])
            print(f"{dt.strftime('%Y-%m-%d %H:%M')}  {m['id']}  {m['branch']:12}  \"{m['context']}\"")


def cmd_recent(project_dirs: List[Path], limit: int = 10, json_output: bool = False):
    """Show recent sessions."""
    # Build/update index
    existing = load_index()
    index = build_index(project_dirs, existing)
    save_index(index)

    # Filter by project
    sessions = [e for e in index.values()
                if any(e['project'] == d.name for d in project_dirs)]

    # Sort by timestamp desc
    sessions.sort(key=lambda x: x['timestamp'], reverse=True)
    sessions = sessions[:limit]

    # Output
    if json_output:
        print(json.dumps(sessions, indent=2))
    else:
        for s in sessions:
            dt = datetime.fromisoformat(s['timestamp'])
            print(f"{dt.strftime('%Y-%m-%d %H:%M')}  {s['id']}  {s['branch']:12}  \"{s['context']}\"")


def cmd_info(session_id: str):
    """Show session details."""
    # Match partial ID
    index = load_index()

    matches = [s for s in index.values() if s['id'].startswith(session_id)]

    if not matches:
        print(f"Error: Session not found: {session_id}", file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1:
        print(f"Error: Ambiguous ID, multiple matches:", file=sys.stderr)
        for m in matches:
            print(f"  {m['id']}", file=sys.stderr)
        sys.exit(1)

    session = matches[0]
    dt = datetime.fromisoformat(session['timestamp'])

    print(f"Session: {session['id']}")
    print(f"Date:    {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project: {session['project']}")
    print(f"Branch:  {session['branch']}")
    print(f"Context: {session['context']}")


def cmd_resume(session_id: str):
    """Resume a session."""
    # Match partial ID
    index = load_index()

    matches = [s for s in index.values() if s['id'].startswith(session_id)]

    if not matches:
        print(f"Error: Session not found: {session_id}", file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1:
        print(f"Error: Ambiguous ID, multiple matches:", file=sys.stderr)
        for m in matches:
            print(f"  {m['id']}", file=sys.stderr)
        sys.exit(1)

    full_id = matches[0]['id']

    # exec claude --resume
    os.execvp('claude', ['claude', '--resume', full_id])


def cmd_reindex():
    """Force rebuild of entire index."""
    print("Rebuilding index...", file=sys.stderr)

    projects_dir = CLAUDE_DIR / "projects"
    if not projects_dir.exists():
        print("Error: No projects directory found", file=sys.stderr)
        sys.exit(1)

    all_dirs = [d for d in projects_dir.iterdir() if d.is_dir()]

    index = build_index(all_dirs, {})
    save_index(index)

    print(f"Indexed {len(index)} sessions", file=sys.stderr)


# ─── DISCOVER subcommand ──────────────────────────────────────────────────────

# Boilerplate phrases that identify system-injected messages (compact summaries,
# system-reminder injections, plan mode prompts, task tool notifications...).
# These appear as plain-text user messages in JSONL but are not real user input.
_SYSTEM_INJECTION_MARKERS = (
    'this session is being continued',
    'read the full transcript',
    'context summary below covers',
    'exact snippets error messages content',
    'exiting plan mode',
    'task tools haven',
    'teamcreate tool team parallelize',
    'florianbruniaux/.claude/projects',   # path fragments in compact prompts
    'florianbruniaux/sites/',              # project path fragments
    '-users-florianbruniaux-',            # encoded path in compact messages
)


def _is_system_injection(text: str) -> bool:
    """Return True if this looks like a Claude Code system message, not real user input."""
    lower = text.lower()
    return any(marker in lower for marker in _SYSTEM_INJECTION_MARKERS)


# Stop words to exclude from n-gram analysis
_STOP_WORDS = frozenset({
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'it', 'its', 'be', 'as', 'was',
    'are', 'were', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall',
    'this', 'that', 'these', 'those', 'i', 'you', 'we', 'they', 'he',
    'she', 'my', 'your', 'our', 'their', 'his', 'her', 'me', 'us', 'them',
    'so', 'if', 'then', 'than', 'when', 'what', 'how', 'why', 'where',
    'who', 'which', 'not', 'no', 'also', 'just', 'now', 'up', 'out',
    'about', 'into', 'after', 'before', 'all', 'any', 'some', 'more',
    'new', 'add', 'use', 'make', 'get', 'go', 'run', 'see', 'here',
    'there', 'need', 'want', 'please', 'ok', 'okay', 'yes', 'yeah',
    'let', 'can', 'help', 'look', 'check', 'same', 'like', 'very',
    'much', 'only', 'other', 'also', 'each', 'file', 'code', 'create',
    'update', 'change', 'think', 'know', 'give', 'take', 'put', 'keep',
})


def normalize_text(text: str) -> List[str]:
    """Lowercase, strip punctuation, tokenize, remove stop words."""
    text = text.lower()
    # Replace punctuation/special chars with spaces (keep alphanumeric and hyphens)
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    # Collapse whitespace
    tokens = text.split()
    # Filter stop words and very short tokens
    return [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]


def extract_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    """Extract n-grams from a token list."""
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def token_overlap(tokens_a: List[str], tokens_b: List[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not tokens_a or not tokens_b:
        return 0.0
    set_a, set_b = set(tokens_a), set(tokens_b)
    return len(set_a & set_b) / len(set_a | set_b)


def load_discover_cache() -> Dict[str, Dict]:
    """Load the discover cache (session_id -> {mtime, messages[]})."""
    if not DISCOVER_CACHE_PATH.exists():
        return {}
    cache = {}
    try:
        with open(DISCOVER_CACHE_PATH, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                cache[entry['id']] = entry
    except Exception:
        return {}
    return cache


def save_discover_cache(cache: Dict[str, Dict]):
    """Persist the discover cache to disk."""
    CLAUDE_DIR.mkdir(exist_ok=True)
    with open(DISCOVER_CACHE_PATH, 'w') as f:
        for entry in cache.values():
            f.write(json.dumps(entry) + '\n')


def collect_sessions_data(
    project_dirs: List[Path],
    since_dt: Optional[datetime],
) -> List[Dict]:
    """
    Collect {session_id, project, mtime, messages[]} for all sessions.

    Uses mtime-based cache to avoid re-reading unchanged files.
    Returns one dict per session that has at least one user message.
    """
    cache = load_discover_cache()
    updated_cache = {}
    sessions_data = []

    for project_dir in project_dirs:
        project_name = project_dir.name
        jsonl_files = list(project_dir.glob("*.jsonl"))

        for filepath in jsonl_files:
            session_id = filepath.stem

            # Skip subagent sessions
            if session_id.startswith('agent-'):
                continue

            try:
                file_mtime = filepath.stat().st_mtime
            except OSError:
                continue

            # Apply date filter: skip if file is older than since_dt
            if since_dt:
                file_dt = datetime.fromtimestamp(file_mtime)
                if file_dt < since_dt:
                    continue

            # Cache hit: file unchanged since last analysis
            if session_id in cache and cache[session_id].get('mtime', 0) >= file_mtime:
                entry = cache[session_id]
                if entry.get('messages'):
                    sessions_data.append({
                        'session_id': session_id,
                        'project': project_name,
                        'mtime': file_mtime,
                        'messages': entry['messages'],
                    })
                updated_cache[session_id] = entry
                continue

            # Cache miss: parse file
            messages = extract_all_user_messages(filepath)
            cache_entry = {
                'id': session_id,
                'mtime': file_mtime,
                'messages': messages,
            }
            updated_cache[session_id] = cache_entry

            if messages:
                sessions_data.append({
                    'session_id': session_id,
                    'project': project_name,
                    'mtime': file_mtime,
                    'messages': messages,
                })

    save_discover_cache(updated_cache)
    return sessions_data


def discover_patterns(
    sessions_data: List[Dict],
    min_count: int = 3,
    top: int = 20,
) -> List[Dict]:
    """
    Analyze sessions data and return pattern suggestions.

    Each suggestion has:
      - pattern: human-readable phrase
      - count: number of occurrences
      - session_count: number of distinct sessions
      - project_count: number of distinct projects
      - cross_project: bool
      - category: 'CLAUDE.md rule' | 'skill' | 'command'
      - score: float (frequency × cross-project bonus)
      - example_sessions: list of up to 2 session_ids
    """
    total_sessions = len(sessions_data)
    if total_sessions == 0:
        return []

    # ── Step 1: Build per-session token lists and n-gram index ────────────────
    # ngram_index: ngram_tuple -> list of {session_id, project, original_message}
    ngram_index: Dict[Tuple, List[Dict]] = defaultdict(list)

    for sd in sessions_data:
        session_id = sd['session_id']
        project = sd['project']
        for msg in sd['messages']:
            tokens = normalize_text(msg)
            if len(tokens) < 3:
                continue
            for n in range(3, 7):  # 3-6 word n-grams
                for ngram in extract_ngrams(tokens, n):
                    # Filter n-grams that are all stop words (shouldn't happen after normalize)
                    if all(t in _STOP_WORDS for t in ngram):
                        continue
                    ngram_index[ngram].append({
                        'session_id': session_id,
                        'project': project,
                        'msg': msg[:80],
                    })

    # ── Step 2: Filter n-grams below min_count ────────────────────────────────
    frequent_ngrams = {
        ng: occurrences
        for ng, occurrences in ngram_index.items()
        if len(occurrences) >= min_count
    }

    # ── Step 3: Deduplicate — prefer longer n-gram if it subsumes shorter ─────
    # Sort by length desc, then count desc
    sorted_ngrams = sorted(
        frequent_ngrams.items(),
        key=lambda x: (len(x[0]), len(x[1])),
        reverse=True,
    )

    kept_ngrams: List[Tuple[Tuple, List[Dict]]] = []
    subsumed: set = set()

    for ngram, occurrences in sorted_ngrams:
        if ngram in subsumed:
            continue
        kept_ngrams.append((ngram, occurrences))
        # Mark all sub-ngrams of this ngram as subsumed
        for n in range(3, len(ngram)):
            for i in range(len(ngram) - n + 1):
                sub = ngram[i:i+n]
                subsumed.add(sub)

    # ── Step 4: Similarity clustering — merge near-duplicate phrases ──────────
    # Group kept_ngrams by token overlap > 60%
    clusters: List[List[int]] = []
    assigned = set()

    for i, (ng_i, _) in enumerate(kept_ngrams):
        if i in assigned:
            continue
        cluster = [i]
        for j, (ng_j, _) in enumerate(kept_ngrams):
            if j <= i or j in assigned:
                continue
            overlap = token_overlap(list(ng_i), list(ng_j))
            if overlap > 0.6:
                cluster.append(j)
                assigned.add(j)
        clusters.append(cluster)
        assigned.add(i)

    # ── Step 5: Build suggestion per cluster (representative = highest count) ──
    suggestions = []
    for cluster in clusters:
        # Pick representative: longest ngram with most occurrences
        best_idx = max(cluster, key=lambda i: (len(kept_ngrams[i][0]), len(kept_ngrams[i][1])))
        ngram, occurrences = kept_ngrams[best_idx]

        # Aggregate across cluster members
        all_occurrences = []
        for idx in cluster:
            all_occurrences.extend(kept_ngrams[idx][1])

        distinct_sessions = list({o['session_id'] for o in all_occurrences})
        distinct_projects = list({o['project'] for o in all_occurrences})
        count = len(all_occurrences)
        session_count = len(distinct_sessions)
        project_count = len(distinct_projects)
        cross_project = project_count >= 2

        if session_count < min_count:
            continue

        session_pct = session_count / total_sessions

        # Categorize
        if session_pct > 0.20:
            category = 'CLAUDE.md rule'
        elif session_pct >= 0.05:
            category = 'skill'
        else:
            category = 'command'

        # Score: base = session_pct, bonus × 1.5 if cross-project
        score = session_pct * (1.5 if cross_project else 1.0)

        phrase = ' '.join(ngram)

        suggestions.append({
            'pattern': phrase,
            'count': count,
            'session_count': session_count,
            'project_count': project_count,
            'cross_project': cross_project,
            'category': category,
            'score': round(score, 4),
            'example_sessions': distinct_sessions[:2],
        })

    # ── Step 6: Sort by score desc, truncate ──────────────────────────────────
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions[:top]


def cmd_discover(
    project_dirs: List[Path],
    since: str = '90d',
    min_count: int = 3,
    top: int = 20,
    json_output: bool = False,
):
    """Analyze sessions and surface patterns worth extracting as skills/commands/rules."""
    since_dt = parse_duration(since)

    print(f"Scanning sessions since {since_dt.strftime('%Y-%m-%d')}...", file=sys.stderr)

    sessions_data = collect_sessions_data(project_dirs, since_dt)

    if not sessions_data:
        print("No sessions found in the given time range.", file=sys.stderr)
        return

    print(f"Analyzing {len(sessions_data)} sessions across "
          f"{len({sd['project'] for sd in sessions_data})} project(s)...", file=sys.stderr)

    suggestions = discover_patterns(sessions_data, min_count=min_count, top=top)

    if not suggestions:
        print("No recurring patterns found (try --min-count 2 or --since 180d).", file=sys.stderr)
        return

    if json_output:
        print(json.dumps(suggestions, indent=2))
        return

    # ── Human-readable output ─────────────────────────────────────────────────
    by_category: Dict[str, List[Dict]] = defaultdict(list)
    for s in suggestions:
        by_category[s['category']].append(s)

    category_order = ['CLAUDE.md rule', 'skill', 'command']
    category_icons = {
        'CLAUDE.md rule': '📋',
        'skill': '🧩',
        'command': '⚡',
    }

    total_sessions = len(sessions_data)
    total_projects = len({sd['project'] for sd in sessions_data})

    print()
    print(f"  cc-sessions discover — {total_sessions} sessions · {total_projects} project(s) · since {since}")
    print()

    for cat in category_order:
        items = by_category.get(cat, [])
        if not items:
            continue

        icon = category_icons[cat]
        print(f"  {icon}  {cat.upper()}")
        print(f"  {'─' * 60}")

        for item in items:
            tag = ' [cross-project]' if item['cross_project'] else ''
            pct = item['session_count'] / total_sessions * 100
            print(
                f"  {item['pattern']}"
                f"{tag}"
            )
            print(
                f"    {item['session_count']} sessions ({pct:.0f}%) · "
                f"{item['count']} occurrences · "
                f"score {item['score']:.3f}"
            )
            for ex in item['example_sessions']:
                print(f"    → {ex[:36]}")
            print()

        print()

    print(f"  Run with --json to pipe to jq for further processing.")
    print()


# ─── DISCOVER --llm subcommand ────────────────────────────────────────────────

def deduplicate_messages_for_llm(sessions_data: List[Dict], max_messages: int = 300) -> List[Dict]:
    """
    Deduplicate semantically similar messages using Jaccard similarity.
    Returns list of {text, count, projects} sorted by frequency desc.
    """
    all_msgs = []
    for sd in sessions_data:
        for msg in sd.get('messages', []):
            all_msgs.append({
                'text': msg[:500],
                'project': sd['project'],
                'tokens': normalize_text(msg),
            })

    if not all_msgs:
        return []

    clusters: List[List[int]] = []
    assigned = set()

    for i, m in enumerate(all_msgs):
        if i in assigned:
            continue
        cluster = [i]
        # Limit comparison window for performance on large sets
        window_end = min(i + 300, len(all_msgs))
        for j in range(i + 1, window_end):
            if j in assigned:
                continue
            if token_overlap(m['tokens'], all_msgs[j]['tokens']) > 0.65:
                cluster.append(j)
                assigned.add(j)
        clusters.append(cluster)
        assigned.add(i)

    deduped = []
    for cluster in clusters:
        representative = all_msgs[cluster[0]]
        projects = list({all_msgs[i]['project'] for i in cluster})
        deduped.append({
            'text': representative['text'],
            'count': len(cluster),
            'projects': projects,
        })

    deduped.sort(key=lambda x: x['count'], reverse=True)
    return deduped[:max_messages]


def build_analysis_prompt(messages: List[Dict]) -> str:
    lines = []
    for i, m in enumerate(messages, 1):
        count_info = f" (x{m['count']})" if m['count'] > 1 else ""
        cross = " [multi-project]" if len(m['projects']) > 1 else ""
        text = m['text'][:200].replace('\n', ' ')
        lines.append(f"{i}. {text}{count_info}{cross}")

    messages_block = '\n'.join(lines)

    return f"""You are analyzing a developer's Claude Code session history to find recurring patterns worth extracting as reusable configurations.

Below are user messages (deduplicated). Numbers in parentheses show how many times a similar message appeared. [multi-project] means it appeared across different codebases.

MESSAGES:
{messages_block}

Identify recurring patterns and suggest what to extract. For each suggestion, choose the category:
- CLAUDE.md rule: a behavioral instruction that should always be active (broad constraint or guideline)
- skill: specialized expertise loaded on-demand (domain-specific, not always needed)
- command: a repeatable step-by-step workflow with clear inputs/outputs

Return ONLY a JSON array, no prose outside it:
[
  {{
    "pattern": "short description of the recurring intent (max 60 chars)",
    "category": "CLAUDE.md rule",
    "suggested_name": "kebab-case-name",
    "rationale": "one sentence explaining why this should be extracted",
    "frequency": "high",
    "example_messages": ["example 1", "example 2"],
    "suggested_content": "what the skill/command/rule would contain (2-3 sentences)"
  }}
]

Rules:
- Only include genuinely recurring patterns (at least 2 messages with similar intent)
- Prefer specific, actionable suggestions over generic ones
- Maximum 15 suggestions, sorted by impact (most valuable first)"""


def call_claude_cli(messages_batch: List[Dict], model: str) -> List[Dict]:
    """
    Call the local `claude --print` CLI (uses your existing subscription).
    No API key required.
    """
    import subprocess
    import tempfile

    prompt = build_analysis_prompt(messages_batch)

    # claude --print accepts the prompt as a positional argument
    cmd = ['claude', '--print', prompt]
    if model:
        cmd += ['--model', model]

    # Remove CLAUDECODE so the subprocess isn't blocked by nested-session detection
    env = os.environ.copy()
    env.pop('CLAUDECODE', None)
    env.pop('CLAUDE_CODE_ENTRYPOINT', None)

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        raise RuntimeError("'claude' CLI not found. Make sure Claude Code is installed and in PATH.")
    except subprocess.TimeoutExpired:
        raise RuntimeError("claude CLI timed out after 120s.")

    if result.returncode != 0:
        detail = (result.stderr or result.stdout)[:500]
        raise RuntimeError(f"claude CLI error (exit {result.returncode}):\n{detail}")

    text = result.stdout.strip()

    # Catch runtime errors reported on stdout (returncode 0 but failed)
    if text.lower().startswith('execution error') or text.lower().startswith('error:'):
        stderr_hint = f"\nstderr: {result.stderr[:300]}" if result.stderr.strip() else ""
        raise RuntimeError(f"claude CLI reported an error:\n{text[:300]}{stderr_hint}")

    # Strip markdown code fences if present
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\n?', '', text)
        text = re.sub(r'\n?```$', '', text)

    # Extract JSON array if surrounded by prose
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        text = match.group(0)

    try:
        suggestions = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse CLI response as JSON: {e}\nRaw: {text[:500]}") from e

    if not isinstance(suggestions, list):
        raise RuntimeError(f"Expected JSON array, got: {type(suggestions)}")

    return suggestions


def cmd_discover_llm(
    project_dirs: List[Path],
    since: str = '90d',
    top: int = 15,
    model: str = LLM_DEFAULT_MODEL,
    json_output: bool = False,
):
    """LLM-powered pattern discovery via `claude --print` (uses your subscription)."""
    since_dt = parse_duration(since)
    print(f"Scanning sessions since {since_dt.strftime('%Y-%m-%d')}...", file=sys.stderr)

    sessions_data = collect_sessions_data(project_dirs, since_dt)
    if not sessions_data:
        print("No sessions found in the given time range.", file=sys.stderr)
        return

    print(f"Collected {len(sessions_data)} sessions — deduplicating messages...", file=sys.stderr)
    deduped = deduplicate_messages_for_llm(sessions_data, max_messages=300)
    if not deduped:
        print("No user messages found.", file=sys.stderr)
        return

    batch = deduped[:LLM_BATCH_SIZE]
    print(f"Sending {len(batch)} unique messages to claude --print ({model})...", file=sys.stderr)

    try:
        suggestions = call_claude_cli(batch, model)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    suggestions = suggestions[:top]

    if json_output:
        print(json.dumps(suggestions, indent=2))
        return

    total_sessions = len(sessions_data)
    total_projects = len({sd['project'] for sd in sessions_data})

    print()
    print(f"  cc-sessions discover --llm — {total_sessions} sessions · {total_projects} project(s) · {model}")
    print()

    by_category: Dict[str, List[Dict]] = defaultdict(list)
    for s in suggestions:
        by_category[s.get('category', 'command')].append(s)

    category_order = ['CLAUDE.md rule', 'skill', 'command']
    category_icons = {'CLAUDE.md rule': '📋', 'skill': '🧩', 'command': '⚡'}

    for cat in category_order:
        items = by_category.get(cat, [])
        if not items:
            continue

        icon = category_icons.get(cat, '•')
        print(f"  {icon}  {cat.upper()}")
        print(f"  {'─' * 70}")

        for item in items:
            freq = item.get('frequency', '')
            freq_tag = f" [{freq}]" if freq else ""
            print(f"  {item.get('pattern', '?')}{freq_tag}")
            print(f"    -> /{item.get('suggested_name', '?')}")
            print(f"    {item.get('rationale', '')}")
            if item.get('suggested_content'):
                print(f"    Content: {item['suggested_content']}")
            for ex in item.get('example_messages', [])[:2]:
                print(f"    e.g. \"{ex[:100].replace(chr(10), ' ')}\"")
            print()

        print()

    print(f"  Run with --json to pipe to jq.")
    print()


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Search Claude Code session history")
    parser.add_argument('--all', action='store_true', help="Search all projects")
    parser.add_argument('--json', action='store_true', help="JSON output")

    subparsers = parser.add_subparsers(dest='command', required=True)

    # search
    search_parser = subparsers.add_parser('search', help="Search sessions by keyword")
    search_parser.add_argument('keyword', help="Search keyword")
    search_parser.add_argument('--limit', type=int, default=10, help="Max results")
    search_parser.add_argument('--since', help="Filter by date (7d, 30d, or ISO date)")
    search_parser.add_argument('--branch', help="Filter by git branch")

    # recent
    recent_parser = subparsers.add_parser('recent', help="Show recent sessions")
    recent_parser.add_argument('limit', nargs='?', type=int, default=10, help="Number of sessions")

    # info
    info_parser = subparsers.add_parser('info', help="Show session details")
    info_parser.add_argument('session_id', help="Session ID (partial match)")

    # resume
    resume_parser = subparsers.add_parser('resume', help="Resume a session")
    resume_parser.add_argument('session_id', help="Session ID (partial match)")

    # reindex
    subparsers.add_parser('reindex', help="Force rebuild index")

    # discover
    discover_parser = subparsers.add_parser(
        'discover',
        help="Analyze sessions to suggest skills, commands, and CLAUDE.md rules",
    )
    discover_parser.add_argument(
        '--since', default='90d',
        help="Time window to analyze (default: 90d)",
    )
    discover_parser.add_argument(
        '--min-count', type=int, default=3,
        help="Minimum occurrences to surface a pattern (default: 3)",
    )
    discover_parser.add_argument(
        '--top', type=int, default=20,
        help="Maximum number of suggestions to show (default: 20)",
    )
    discover_parser.add_argument(
        '--llm', action='store_true',
        help="Use 'claude --print' for semantic analysis (uses your subscription)",
    )
    discover_parser.add_argument(
        '--model', default=LLM_DEFAULT_MODEL,
        help="Claude model to use with --llm, e.g. 'haiku' or 'sonnet' (default: CLI default)",
    )

    args = parser.parse_args()

    # Get project dirs
    if args.command in ['search', 'recent', 'discover']:
        project_dirs = get_project_dirs(args.all)

        if not project_dirs:
            if args.all:
                print("Error: No projects found", file=sys.stderr)
            else:
                print("Error: Not in a Claude project directory", file=sys.stderr)
                print("Hint: Use --all to search all projects", file=sys.stderr)
            sys.exit(1)

    # Execute command
    if args.command == 'search':
        cmd_search(args.keyword, project_dirs, args.limit, args.since, args.branch, args.json)
    elif args.command == 'recent':
        cmd_recent(project_dirs, args.limit, args.json)
    elif args.command == 'info':
        cmd_info(args.session_id)
    elif args.command == 'resume':
        cmd_resume(args.session_id)
    elif args.command == 'reindex':
        cmd_reindex()
    elif args.command == 'discover':
        if args.llm:
            cmd_discover_llm(
                project_dirs,
                since=args.since,
                top=args.top,
                model=args.model,
                json_output=args.json,
            )
        else:
            cmd_discover(
                project_dirs,
                since=args.since,
                min_count=args.min_count,
                top=args.top,
                json_output=args.json,
            )


if __name__ == '__main__':
    main()
