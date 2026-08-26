'use strict';

const os = require('node:os');
const path = require('node:path');
const { discoverRoots, findRepoRoot, splitRoots } = require('./discovery');
const { computeScopeKey } = require('./cache');

function homeDir() {
  return path.resolve(process.env.SKILL_ROUTER_HOME || os.homedir());
}

function dataRoot() {
  return path.resolve(process.env.SKILL_ROUTER_DATA_DIR || process.env.BM25_DATA_DIR || path.join(__dirname, 'data'));
}

function overlayRoots() {
  const configured = splitRoots(process.env.SKILL_ROUTER_OVERLAY_ROOTS);
  return configured.length ? configured.map((root) => path.resolve(root)) : [path.join(__dirname, '..', 'corpus')];
}

function extraRoots() {
  const roots = splitRoots(process.env.SKILL_ROUTER_EXTRA_ROOTS);
  if (process.env.BM25_SKILLS_ROOT) roots.push(process.env.BM25_SKILLS_ROOT);
  return [...new Set(roots.map((root) => path.resolve(root)))];
}

function resolveContext(cwd) {
  const resolvedCwd = path.resolve(cwd || process.env.SKILL_ROUTER_CWD || process.cwd());
  const roots = discoverRoots({ cwd: resolvedCwd, home: homeDir(), extraRoots: extraRoots() });
  const repoRoot = findRepoRoot(resolvedCwd);
  const scopeKey = computeScopeKey({ cwd: resolvedCwd, repoRoot, roots: roots.map((root) => root.path) });
  return {
    cwd: resolvedCwd,
    repoRoot,
    roots,
    scopeKey,
    cacheDir: path.join(dataRoot(), 'scopes', scopeKey),
  };
}

module.exports = { dataRoot, extraRoots, homeDir, overlayRoots, resolveContext };
