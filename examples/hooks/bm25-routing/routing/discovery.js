'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SKILL_NAME_RE = /^[a-z0-9][a-z0-9:_-]{0,127}$/;
const MAX_SKILL_FILE_BYTES = 64 * 1024;

function safeRealpath(target) {
  try { return fs.realpathSync(target); } catch { return null; }
}

function isWithin(target, root) {
  const relative = path.relative(root, target);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function findRepoRoot(start) {
  let current = path.resolve(start || process.cwd());
  while (true) {
    if (fs.existsSync(path.join(current, '.git'))) return current;
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}

function splitRoots(value) {
  return String(value || '').split(path.delimiter).map((item) => item.trim()).filter(Boolean);
}

function discoverRoots(options = {}) {
  const cwd = path.resolve(options.cwd || process.cwd());
  const home = path.resolve(options.home || os.homedir());
  const repoRoot = findRepoRoot(cwd);
  const roots = [];
  let current = cwd;
  let projectPrecedence = 10_000;
  const boundary = repoRoot || path.parse(cwd).root;
  while (true) {
    const candidate = path.join(current, '.agents', 'skills');
    if (fs.existsSync(candidate)) {
      roots.push({ path: candidate, scope: current === repoRoot ? 'project' : 'nested-project', precedence: projectPrecedence-- });
    }
    if (current === boundary) break;
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }

  const globalRoots = [
    { path: path.join(home, '.agents', 'skills'), scope: 'user-agents', precedence: 5_000 },
    { path: path.join(home, '.codex', 'skills'), scope: 'user-codex', precedence: 4_000 },
    { path: options.adminRoot || '/etc/codex/skills', scope: 'admin', precedence: 3_000 },
  ];
  for (const root of globalRoots) if (fs.existsSync(root.path)) roots.push(root);

  const extras = options.extraRoots || splitRoots(process.env.SKILL_ROUTER_EXTRA_ROOTS);
  extras.forEach((root, index) => {
    if (fs.existsSync(root)) roots.push({ path: path.resolve(root), scope: 'extra', precedence: 2_000 - index });
  });

  const unique = [];
  const seen = new Set();
  for (const root of roots.sort((a, b) => b.precedence - a.precedence)) {
    const real = safeRealpath(root.path);
    if (!real || seen.has(real)) continue;
    seen.add(real);
    unique.push({ ...root, path: real });
  }
  return unique;
}

function parseFrontmatter(file) {
  const stat = fs.statSync(file);
  if (stat.size > MAX_SKILL_FILE_BYTES) throw new Error('skill_file_too_large');
  const text = fs.readFileSync(file, 'utf8');
  const block = text.match(/^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/);
  if (!block) return {};
  const metadata = {};
  for (const line of block[1].split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;
    metadata[match[1]] = match[2].trim().replace(/^(['"])(.*)\1$/, '$2');
  }
  return metadata;
}

function discoverSkills(roots) {
  const skills = new Map();
  const problems = [];
  const authorizedRoots = roots.map((root) => ({ ...root, real: safeRealpath(root.path) })).filter((root) => root.real);

  for (const root of authorizedRoots) {
    const stack = [{ dir: root.path, depth: 0 }];
    while (stack.length) {
      const { dir, depth } = stack.pop();
      if (depth > 10) continue;
      let entries;
      try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
      for (const entry of entries) {
        const candidate = path.join(dir, entry.name);
        if (entry.isSymbolicLink()) {
          const resolved = safeRealpath(candidate);
          if (resolved && !authorizedRoots.some((allowed) => isWithin(resolved, allowed.real))) {
            problems.push({ code: 'escaped_symlink', path: candidate });
            continue;
          }
        }
        let stat;
        try { stat = fs.statSync(candidate); } catch { continue; }
        if (!stat.isDirectory()) continue;
        const skillMd = path.join(candidate, 'SKILL.md');
        if (fs.existsSync(skillMd)) {
          try {
            const metadata = parseFrontmatter(skillMd);
            const name = metadata.name || path.basename(candidate);
            if (!SKILL_NAME_RE.test(name)) {
              problems.push({ code: 'invalid_skill_name', path: skillMd, name });
            } else if (skills.has(name)) {
              problems.push({ code: 'shadowed_skill', name, path: skillMd, activePath: skills.get(name).skillMd });
            } else {
              skills.set(name, {
                name,
                description: metadata.description || '',
                skillMd: safeRealpath(skillMd) || skillMd,
                directory: safeRealpath(candidate) || candidate,
                root: root.path,
                scope: root.scope,
                precedence: root.precedence,
              });
            }
          } catch (error) {
            problems.push({ code: error.message, path: skillMd });
          }
        }
        stack.push({ dir: candidate, depth: depth + 1 });
      }
    }
  }
  return { skills, problems };
}

function readCorpus(file, expectedSkill, activeSkills, problems, kind) {
  let data;
  try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch {
    problems.push({ code: 'invalid_corpus_json', path: file });
    return null;
  }
  const name = data && data.skill;
  if (!SKILL_NAME_RE.test(String(name || ''))) {
    problems.push({ code: 'invalid_corpus_skill', path: file, name });
    return null;
  }
  if (expectedSkill && name !== expectedSkill) {
    problems.push({ code: 'mismatched_corpus_skill', path: file, name, expectedSkill });
    return null;
  }
  if (!activeSkills.has(name)) {
    problems.push({ code: kind === 'overlay' ? 'inactive_overlay_skill' : 'inactive_corpus_skill', path: file, name });
    return null;
  }
  if (!Array.isArray(data.positive) || !Array.isArray(data.negative)) {
    problems.push({ code: 'invalid_corpus_shape', path: file, name });
    return null;
  }
  return {
    skill: name,
    positive: data.positive.filter((item) => typeof item === 'string'),
    negative: data.negative.filter((item) => typeof item === 'string'),
    path: safeRealpath(file) || file,
    kind,
  };
}

function findJsonFiles(root) {
  const files = [];
  const stack = [{ dir: root, depth: 0 }];
  while (stack.length) {
    const { dir, depth } = stack.pop();
    if (depth > 8) continue;
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const entry of entries) {
      const candidate = path.join(dir, entry.name);
      if (entry.isDirectory()) stack.push({ dir: candidate, depth: depth + 1 });
      else if (entry.isFile() && entry.name.endsWith('.json')) files.push(candidate);
    }
  }
  return files.sort();
}

function discoverCorpora({ skills, overlayRoots = [] }) {
  const sources = [];
  const problems = [];
  const covered = new Set();
  for (const item of skills.values()) {
    const file = path.join(item.directory, 'evals', 'scenarios.json');
    if (!fs.existsSync(file)) continue;
    const corpus = readCorpus(file, item.name, skills, problems, 'adjacent');
    if (corpus) { sources.push(corpus); covered.add(corpus.skill); }
  }
  for (const root of overlayRoots) {
    for (const file of findJsonFiles(root)) {
      const corpus = readCorpus(file, null, skills, problems, 'overlay');
      if (!corpus) continue;
      if (covered.has(corpus.skill)) {
        problems.push({ code: 'shadowed_overlay_corpus', path: file, name: corpus.skill });
        continue;
      }
      sources.push(corpus);
      covered.add(corpus.skill);
    }
  }
  return { sources, problems };
}

module.exports = {
  SKILL_NAME_RE,
  discoverCorpora,
  discoverRoots,
  discoverSkills,
  findRepoRoot,
  splitRoots,
};
