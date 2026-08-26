'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const ALGORITHM_VERSION = 5;

function hashLines(lines) {
  const hash = crypto.createHash('sha256');
  for (const line of lines) hash.update(`${line}\n`);
  return hash.digest('hex');
}

function computeScopeKey({ cwd, repoRoot, roots }) {
  const relativeCwd = repoRoot && cwd.startsWith(repoRoot)
    ? path.relative(repoRoot, cwd) || '.'
    : path.resolve(cwd);
  return hashLines([
    `algorithm=${ALGORITHM_VERSION}`,
    `repo=${repoRoot || '<none>'}`,
    `cwd=${relativeCwd}`,
    ...[...roots].map((root) => path.resolve(root)).sort(),
  ]).slice(0, 24);
}

function fingerprintFiles(files) {
  const lines = [`algorithm=${ALGORITHM_VERSION}`];
  for (const file of [...new Set(files)].sort()) {
    try {
      const stat = fs.statSync(file);
      lines.push(`${path.resolve(file)}|${stat.size}|${stat.mtimeMs}`);
      lines.push(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'));
    } catch {
      lines.push(`${path.resolve(file)}|missing`);
    }
  }
  return hashLines(lines);
}

function fingerprintStats(paths) {
  const lines = [`algorithm=${ALGORITHM_VERSION}`];
  for (const target of [...new Set(paths)].sort()) {
    try {
      const stat = fs.statSync(target);
      lines.push(`${path.resolve(target)}|${stat.isDirectory() ? 'dir' : 'file'}|${stat.size}|${stat.mtimeMs}`);
    } catch {
      lines.push(`${path.resolve(target)}|missing`);
    }
  }
  return hashLines(lines);
}

function writeJsonAtomic(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.tmp.${process.pid}.${Date.now()}`;
  fs.writeFileSync(tmp, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
  fs.renameSync(tmp, file);
}

function acquireBuildLock(lockPath, ttlMs = 30_000) {
  fs.mkdirSync(path.dirname(lockPath), { recursive: true });
  try {
    const fd = fs.openSync(lockPath, 'wx', 0o600);
    fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, createdAt: Date.now() }));
    fs.closeSync(fd);
    return {
      acquired: true,
      release() {
        try { fs.unlinkSync(lockPath); } catch { /* already released */ }
      },
    };
  } catch (error) {
    if (error.code !== 'EEXIST') throw error;
  }

  try {
    const stat = fs.statSync(lockPath);
    if (Date.now() - stat.mtimeMs > ttlMs) {
      fs.unlinkSync(lockPath);
      return acquireBuildLock(lockPath, ttlMs);
    }
  } catch { /* another builder won the race */ }
  return { acquired: false, release() {} };
}

module.exports = {
  ALGORITHM_VERSION,
  acquireBuildLock,
  computeScopeKey,
  fingerprintFiles,
  fingerprintStats,
  writeJsonAtomic,
};
