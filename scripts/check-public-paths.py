#!/usr/bin/env python3
"""Reject workstation-specific paths in reader-facing sources and built pages."""
import argparse
import html
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = ('guide', 'docs', 'examples', 'whitepapers', 'machine-readable', 'mcp-server/content')
PUBLIC_FILES = ('README.md', 'CHANGELOG.md', 'IDEAS.md', 'llms.txt', 'llms-full.txt')
TEXT_TYPES = {'.md', '.mdx', '.txt', '.qmd', '.json', '.yaml', '.yml', '.html'}
# Generic example usernames and macOS system-path explanations remain useful.
EXAMPLE_USERS = {'user', 'username', 'yourname', 'you', 'me', 'example', 'foo', '...', '…', 'mcp', 'root'}
USER_PATH = re.compile(r'''(?<![\w/])/(?:Users|home)/([^/\s`"'<>|]+)''', re.I)
TEMP_PATH = re.compile(r'(?<![\w/])/private/(?:tmp|var/folders)/[\w.-]+', re.I)
SITE_PATH = re.compile(r'~/Sites/', re.I)


def has_workstation_path(text):
    text = html.unescape(unquote(text))
    return bool(TEMP_PATH.search(text) or SITE_PATH.search(text) or any(
        match.group(1).lower() not in EXAMPLE_USERS for match in USER_PATH.finditer(text)
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist', type=Path, help='Also scan the complete rendered site')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        for value in ('/Users/alice/project', '/home/alice/repo', '/private/tmp/review',
                      '%2FUsers%2Falice%2Frepo', '&#47;Users/alice/repo', '~/Sites/repo'):
            assert has_workstation_path(value), value
        for value in ('./mcp/src', '/Users/you/project', '/home/user/private/**',
                      '/private/{etc,var,tmp,home}', '/private/tmp', 'https://example.org/en/users/features'):
            assert not has_workstation_path(value), value
        print('Public-path detector self-test passed.')
        return 0
    paths = {ROOT / name for name in PUBLIC_FILES if (ROOT / name).is_file()}
    for name in PUBLIC_DIRS:
        paths.update(p for p in (ROOT / name).rglob('*') if p.is_file() and p.suffix in TEXT_TYPES)
    if args.dist:
        if not args.dist.is_dir():
            parser.error('--dist must name an existing build directory')
        paths.update(p for p in args.dist.rglob('*') if p.is_file() and p.suffix in TEXT_TYPES | {'.js'})
    failures = []
    for path in sorted(paths):
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if has_workstation_path(line):
                failures.append(f'{path}:{number}')
    print(f'Public-path check: {len(paths)} files, {len(failures)} offending lines.')
    for failure in failures:
        print(failure)
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
