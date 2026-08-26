'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  acquireBuildLock,
  computeScopeKey,
  fingerprintFiles,
} = require('../routing/cache');

test('scope cache key changes with relative cwd and resolved roots', () => {
  const common = { repoRoot: '/repo', roots: ['/repo/.agents/skills', '/home/u/.agents/skills'] };
  const a = computeScopeKey({ ...common, cwd: '/repo/a' });
  const b = computeScopeKey({ ...common, cwd: '/repo/b' });
  const c = computeScopeKey({ ...common, cwd: '/repo/a', roots: ['/repo/.agents/skills'] });
  assert.notEqual(a, b);
  assert.notEqual(a, c);
  assert.equal(a, computeScopeKey({ ...common, cwd: '/repo/a' }));
});

test('source fingerprint detects edits and deletions', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'router-cache-'));
  const file = path.join(dir, 'scenarios.json');
  fs.writeFileSync(file, '{"a":1}');
  const first = fingerprintFiles([file]);
  fs.writeFileSync(file, '{"a":2,"longer":true}');
  const second = fingerprintFiles([file]);
  fs.unlinkSync(file);
  const deleted = fingerprintFiles([file]);
  assert.notEqual(first, second);
  assert.notEqual(second, deleted);
});

test('source fingerprint detects same-size edits even when mtime is restored', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'router-cache-content-'));
  const file = path.join(dir, 'scenarios.json');
  fs.writeFileSync(file, '{"a":1}');
  const stat = fs.statSync(file);
  const first = fingerprintFiles([file]);
  fs.writeFileSync(file, '{"b":2}');
  fs.utimesSync(file, stat.atime, stat.mtime);
  assert.notEqual(first, fingerprintFiles([file]));
});

test('build lock is exclusive and releasable', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'router-lock-'));
  const lockPath = path.join(dir, 'build.lock');
  const first = acquireBuildLock(lockPath, 60_000);
  const second = acquireBuildLock(lockPath, 60_000);
  assert.equal(first.acquired, true);
  assert.equal(second.acquired, false);
  first.release();
  const third = acquireBuildLock(lockPath, 60_000);
  assert.equal(third.acquired, true);
  third.release();
});
