#!/usr/bin/env python3
"""Reject npm package names in npx and npm install commands that are not published.

Readers copy these commands into their shells and MCP configs. A name nobody
published can be registered later by anyone, and the next reader then runs that
code, often with an API key or a cloud credential passed in the same command.
On 2026-11-03 the guide cited @anthropic/mcp-kubernetes, @anthropic/mcp-aws,
@anthropic/mcp-gcp and @anthropic/spec-kit (the npm scope `anthropic` holds
unrelated packages), and @shinzo-labs/hubspot-mcp with a HubSpot key, while the
published package is @shinzolabs/hubspot-mcp.

A published name can still belong to someone else. On 2026-11-04 the guide
credited `npx mcp-scan` to Snyk, but that npm name has an unrelated publisher.
Such names are listed in WRONG_PUBLISHER and fail the check as well.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import http.client
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SCOPED_DIRS = ('guide', 'examples', 'tools', 'quiz', '.claude')
SCOPED_FILES = ('README.md',)
TEXT_TYPES = {'.md', '.txt', '.json', '.yaml', '.yml', '.sh', '.ps1', '.toml', '.qmd'}
# The threat database lists removed malicious packages on purpose, and it is a
# mirror of AgentSec Triage, which owns its corrections.
EXCLUDED_FILES = {'examples/commands/resources/threat-db.yaml', 'scripts/check-npx-packages.py'}
REGISTRY = 'https://registry.npmjs.org/'
# Published npm names whose publisher is not the project the guide credits.
WRONG_PUBLISHER = {
    'mcp-scan': 'published by an unrelated author; the Invariant and Snyk scanner is '
                'the PyPI package snyk-agent-scan (uvx snyk-agent-scan@latest)',
}

NAME = r'@?[A-Za-z0-9][\w.\-]*(?:/[\w.\-]+)?(?:@[\w.\-^~]+)?'
FLAGS = r'(?:(?:-y|--yes|-q|--quiet|-g|--global|-D|--save-dev|--no-install)\s+)*'
COMMAND = re.compile(r'(?<![\w/-])(?:npx|npm\s+(?:install|i|exec)|pnpm\s+(?:add|dlx)|bunx)\s+'
                     + FLAGS + r'(?P<pkg>' + NAME + r')')
JSON_NPX = re.compile(r'"command"\s*:\s*"npx"\s*,\s*"args"\s*:\s*\[(?P<args>[^\]]*)\]', re.S)
PLACEHOLDER = re.compile(r'[<>{}$*]|\.\.\.|^@?(your|my)[-_]|example|^@(org|scope|my|company|your)/|xxx', re.I)
# Words that follow `npx` or `npm i` in prose rather than a package name.
NOT_PACKAGES = {'and', 'or', 'the', 'with', 'to', 'is', 'in', 'a', 'package', 'packages', 'command'}


def bare_name(token):
    token = token.strip().strip('"\'`,;)')
    if token.startswith('@'):
        scope, _, rest = token.partition('/')
        return scope + '/' + rest.split('@', 1)[0] if rest else ''
    return token.split('@', 1)[0]


def is_candidate(name):
    return (name and name.lower() not in NOT_PACKAGES and not PLACEHOLDER.search(name)
            and not name.startswith(('.', '-')) and not name.endswith(('.js', '.ts', '.mjs', '.sh'))
            and name == name.lower())


def extract(text):
    """Return {(name, line)} for every package a command or MCP config would fetch."""
    found = set()
    for m in COMMAND.finditer(text):
        name = bare_name(m.group('pkg'))
        if is_candidate(name):
            found.add((name, text.count('\n', 0, m.start()) + 1))
    for m in JSON_NPX.finditer(text):
        args = re.findall(r'"([^"]*)"', m.group('args'))
        first = next((a for a in args if not a.startswith('-')), '')
        name = bare_name(first)
        if is_candidate(name):
            found.add((name, text.count('\n', 0, m.start()) + 1))
    return found


def scoped_files():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT, text=True).split('\0')
    return [ROOT / n for n in names
            if (n in SCOPED_FILES or any(n.startswith(d + '/') for d in SCOPED_DIRS))
            and n not in EXCLUDED_FILES and Path(n).suffix in TEXT_TYPES and (ROOT / n).is_file()]


def fetch(url, read_body=False):
    # The abbreviated metadata format keeps a published package's answer small.
    headers = {'Accept': 'application/vnd.npm.install-v1+json, application/json'}
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
                return response.status, response.read() if read_body else b''
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return 404, exc.read()
            if exc.code not in (429, 500, 502, 503, 504):
                return exc.code, b''
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException):
            pass
        time.sleep(2 ** attempt)
    return None, b''


def registry_status(name):
    status, _ = fetch(REGISTRY + urllib.parse.quote(name, safe='@'))
    if status == 200:
        return 'published'
    if status == 404:
        if name.startswith('@'):
            scope = name[1:].split('/')[0]
            org_status, body = fetch(f'{REGISTRY}-/org/{urllib.parse.quote(scope)}/package', read_body=True)
            if org_status == 404 or b'Scope not found' in body:
                return 'missing, and no npm organization owns the scope'
            return 'missing in an existing scope'
        return 'missing, and the name is free to register'
    return f'registry did not answer (status {status})'


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('files', nargs='*', type=Path, help='Scan these files instead of the scoped tree')
    parser.add_argument('--self-test', action='store_true', help='Test the extractor offline')
    args = parser.parse_args()
    if args.self_test:
        sample = '\n'.join((
            'claude mcp add hubspot -e K=V -- npx -y @shinzo-labs/hubspot-mcp --api-key X',
            'npx --yes kubernetes-mcp-server@latest',
            'npm install -g @playwright/mcp@0.0.84',
            '"command": "npx",\n  "args": ["-y", "@google-cloud/gcloud-mcp"]',
            'npx <postgres-mcp-package>  npx @org/server  npx @my/server  npx your-package  npx ./local.js',
            'Run npx and then npm i to install.',
        ))
        names = {n for n, _ in extract(sample)}
        expected = {'@shinzo-labs/hubspot-mcp', 'kubernetes-mcp-server', '@playwright/mcp',
                    '@google-cloud/gcloud-mcp'}
        assert names == expected, names
        assert 'mcp-scan' in {n for n, _ in extract('npx mcp-scan ./skill-directory')}
        assert bare_name('@scope/pkg@1.2.3') == '@scope/pkg' and bare_name('pkg@latest') == 'pkg'
        print('npx package extractor self-test passed.')
        return 0

    occurrences = {}
    for path in args.files or scoped_files():
        text = path.read_text(encoding='utf-8', errors='replace')
        resolved = path.resolve()
        shown = resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else path
        for name, line in extract(text):
            occurrences.setdefault(name, []).append(f'{shown}:{line}')
    with ThreadPoolExecutor(max_workers=8) as pool:
        statuses = dict(zip(occurrences, pool.map(registry_status, occurrences)))
    statuses.update({n: WRONG_PUBLISHER[n] for n in statuses if n in WRONG_PUBLISHER})
    failures = {n: s for n, s in statuses.items() if s != 'published'}
    for name in sorted(failures):
        print(f'{name}: {failures[name]}')
        for where in sorted(occurrences[name]):
            print(f'  {where}')
    if failures:
        print(f'\n{len(failures)} of {len(statuses)} npm names are not published by the project the guide '
              'credits. Replace each with the package its maintainer publishes, or with an explicit '
              '<placeholder>.', file=sys.stderr)
        return 1
    print(f'All {len(statuses)} npm package names cited in npx and npm install commands are published.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
