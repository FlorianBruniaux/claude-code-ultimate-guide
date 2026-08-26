'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  filterEligible,
  formatHint,
  reserveRebuild,
  shouldSkipPrompt,
} = require('../bm25-suggest');

test('Codex hint uses explicit $skill syntax and an exact SKILL.md path', () => {
  const hint = formatHint([
    { skill: 'critique-plan', score: 5, skillMd: '/tmp/skills/critique-plan/SKILL.md' },
  ], 'codex');
  assert.match(hint, /\$critique-plan/);
  assert.match(hint, /\/tmp\/skills\/critique-plan\/SKILL\.md/);
  assert.doesNotMatch(hint, /confidence|%|(?:^|\s)\/critique-plan/);
  assert.ok(hint.length <= 500);
});

test('only one process can request a detached rebuild for a scope', () => {
  const cacheDir = fs.mkdtempSync(path.join(os.tmpdir(), 'router-request-'));
  const first = reserveRebuild(cacheDir);
  const second = reserveRebuild(cacheDir);
  assert.equal(first, path.join(cacheDir, 'rebuild.request'));
  assert.equal(second, null);
  fs.unlinkSync(first);
});

test('only calibrated ok skills with active manifests can fire', () => {
  const scored = [
    { skill: 'ok', score: 4 },
    { skill: 'conflict', score: 9 },
    { skill: 'excluded', score: 10 },
    { skill: 'ghost', score: 20 },
  ];
  const thresholds = {
    ok: { status: 'ok', tau: 3, eligible: true },
    conflict: { status: 'conflict', tau: 1 },
    excluded: { status: 'excluded', tau: 1 },
    ghost: { status: 'ok', tau: 1, eligible: true },
  };
  const activeSkills = { ok: { skillMd: '/tmp/ok/SKILL.md' } };
  assert.deepEqual(filterEligible(scored, thresholds, activeSkills), [
    { skill: 'ok', score: 4, skillMd: '/tmp/ok/SKILL.md' },
  ]);
});

test('a stronger contrastive negative match vetoes a positive lexical overlap', () => {
  const scored = [{ skill: 'finder', score: 4, negativeScore: 5 }];
  const thresholds = { finder: { status: 'ok', tau: 2, eligible: true } };
  const activeSkills = { finder: { skillMd: '/tmp/finder/SKILL.md' } };
  assert.deepEqual(filterEligible(scored, thresholds, activeSkills), []);
});

test('a calibrated skill that fails cross-skill evaluation remains native-only', () => {
  const scored = [{ skill: 'noisy', score: 8, negativeScore: 0 }];
  const thresholds = { noisy: { status: 'ok', tau: 2, eligible: false } };
  const activeSkills = { noisy: { skillMd: '/tmp/noisy/SKILL.md' } };
  assert.deepEqual(filterEligible(scored, thresholds, activeSkills), []);
});

test('normal negation does not disable routing, while explicit invocation and opt-out do', () => {
  assert.equal(shouldSkipPrompt('analyser ce repo sans modifier les fichiers', 'codex', ['review']), false);
  assert.equal(shouldSkipPrompt('ne propose aucune skill pour ce prompt', 'codex', ['review']), true);
  assert.equal(shouldSkipPrompt('$review inspecte ce module', 'codex', ['review']), true);
  assert.equal(shouldSkipPrompt('/review inspecte ce module', 'claude', ['review']), true);
});
