'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  discoverRoots,
  discoverSkills,
  discoverCorpora,
  findRepoRoot,
} = require('../routing/discovery');

function write(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
}

function skill(root, name, description = name) {
  write(path.join(root, name, 'SKILL.md'), `---\nname: ${name}\ndescription: ${description}\n---\n`);
}

test('discovers nested project and global roots with deterministic precedence', () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'router-discovery-'));
  const home = path.join(base, 'home');
  const repo = path.join(base, 'repo');
  const cwd = path.join(repo, 'packages', 'web');
  fs.mkdirSync(path.join(repo, '.git'), { recursive: true });
  fs.mkdirSync(cwd, { recursive: true });
  skill(path.join(repo, '.agents', 'skills'), 'shared', 'repo version');
  skill(path.join(cwd, '.agents', 'skills'), 'shared', 'nearest version');
  skill(path.join(home, '.agents', 'skills'), 'global-agent');
  skill(path.join(home, '.codex', 'skills'), 'global-codex');

  assert.equal(findRepoRoot(cwd), repo);
  const roots = discoverRoots({ cwd, home, adminRoot: path.join(base, 'missing') });
  const found = discoverSkills(roots);

  assert.deepEqual([...found.skills.keys()].sort(), [
    'global-agent', 'global-codex', 'shared',
  ]);
  assert.match(found.skills.get('shared').skillMd, /packages\/web/);
  assert.equal(found.skills.get('shared').description, 'nearest version');
  assert.ok(found.problems.some((problem) => problem.code === 'shadowed_skill'));
});

test('rejects invalid names, inactive overlay targets, and symlinks escaping authorized roots', () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'router-security-'));
  const root = path.join(base, 'skills');
  const outside = path.join(base, 'outside');
  skill(root, 'valid-skill');
  skill(outside, 'escaped-skill');
  skill(root, 'Bad Name');
  fs.symlinkSync(path.join(outside, 'escaped-skill'), path.join(root, 'linked'));

  const found = discoverSkills([{ path: root, scope: 'extra', precedence: 1 }]);
  assert.deepEqual([...found.skills.keys()], ['valid-skill']);
  assert.ok(found.problems.some((problem) => problem.code === 'invalid_skill_name'));
  assert.ok(found.problems.some((problem) => problem.code === 'escaped_symlink'));

  const overlays = path.join(base, 'overlays');
  write(path.join(overlays, 'valid.json'), JSON.stringify({
    skill: 'valid-skill',
    positive: ['find an agent framework'],
    negative: ['fix a CSS rule'],
  }));
  write(path.join(overlays, 'ghost.json'), JSON.stringify({
    skill: 'ghost-skill',
    positive: ['ghost'],
    negative: ['not a ghost'],
  }));

  const corpora = discoverCorpora({ skills: found.skills, overlayRoots: [overlays] });
  assert.equal(corpora.sources.length, 1);
  assert.equal(corpora.sources[0].skill, 'valid-skill');
  assert.ok(corpora.problems.some((problem) => problem.code === 'inactive_overlay_skill'));
});

test('discovers nested skills below a parent that is itself a skill', () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'router-nested-skills-'));
  const root = path.join(base, 'skills');
  skill(root, 'notion');
  skill(path.join(root, 'notion'), 'notion-find');
  const found = discoverSkills([{ path: root, scope: 'project', precedence: 10 }]);
  assert.deepEqual([...found.skills.keys()].sort(), ['notion', 'notion-find']);
});
