#!/usr/bin/env python3
"""Reject links to the guide's own repositories under a foreign GitHub owner.

Templates, scripts and commands fetch files from this repository and from the
plugins repository. A wrong owner in such a URL fetches (and sometimes runs)
whatever that other account publishes under the same name. The diagnose skill
piped a script into bash from an unrelated account from v3.0.4 until 3.45.x.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# Places whose files are executed, copied into user configs or served as templates.
SCOPED_DIRS = ('examples', '.claude', 'scripts', 'tools', 'mcp-server/src')
TEXT_TYPES = {'.md', '.txt', '.json', '.yaml', '.yml', '.sh', '.ps1', '.py', '.ts', '.js', '.mjs', '.toml'}
OWN_REPOS = ('claude-code-ultimate-guide', 'claude-code-plugins')
OWNER = 'florianbruniaux'
# Placeholders that tell a reader to substitute their own fork.
PLACEHOLDERS = {'your_username', 'your-username', 'username', 'owner', '<owner>', 'you'}
OWN_REPO_URL = re.compile(
    r'(?:github\.com|raw\.githubusercontent\.com)/([^/\s`"\'()<>]+)/(' + '|'.join(OWN_REPOS) + r')(?![\w-])',
    re.I,
)


def foreign_owners(text):
    return sorted({m.group(1) for m in OWN_REPO_URL.finditer(text)
                   if m.group(1).lower() not in {OWNER} | PLACEHOLDERS})


def scoped_files():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT, text=True).split('\0')
    return [ROOT / n for n in names
            if any(n.startswith(d + '/') for d in SCOPED_DIRS)
            and Path(n).suffix in TEXT_TYPES and (ROOT / n).is_file()
            and n != 'scripts/check-own-repo-urls.py']


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('files', nargs='*', type=Path, help='Scan these files instead of the scoped tree')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        for bad in ('https://raw.githubusercontent.com/flobby41/claude-code-ultimate-guide/main/x.sh',
                    'https://github.com/someone/claude-code-plugins/tree/main'):
            assert foreign_owners(bad), bad
        for good in ('https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main/x.sh',
                     'https://github.com/YOUR_USERNAME/claude-code-ultimate-guide.git',
                     'https://github.com/someone/claude-code-ultimate-guide-zh',
                     'https://github.com/anthropics/claude-code'):
            assert not foreign_owners(good), good
        print('Own-repository URL detector self-test passed.')
        return 0
    failures = []
    for path in args.files or scoped_files():
        for lineno, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
            for owner in foreign_owners(line):
                failures.append(f'{path}:{lineno}: owner "{owner}" is not {OWNER}')
    if failures:
        print('Links to the guide repositories under a foreign owner:', *failures, sep='\n', file=sys.stderr)
        return 1
    print('Own-repository URLs use the canonical owner.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
