'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { execFileSync, spawnSync } = require('node:child_process');

const exampleRoot = path.resolve(__dirname, '..');
const buildScript = path.join(exampleRoot, 'routing', 'build-index.js');
const hookScript = path.join(exampleRoot, 'bm25-suggest.js');

function write(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content);
}

test('builds a scoped cache and emits a bounded Codex hook response', () => {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'router-e2e-'));
  const repo = path.join(base, 'repo');
  const home = path.join(base, 'home');
  const data = path.join(base, 'data');
  const overlays = path.join(base, 'overlays');
  const skillDir = path.join(repo, '.agents', 'skills', 'repo-finder');
  fs.mkdirSync(path.join(repo, '.git'), { recursive: true });
  fs.mkdirSync(overlays, { recursive: true });
  write(path.join(skillDir, 'SKILL.md'), '---\nname: repo-finder\ndescription: Find relevant repositories\n---\n');
  write(path.join(skillDir, 'evals', 'scenarios.json'), JSON.stringify({
    skill: 'repo-finder',
    positive: [
      'find an open source agent repository',
      'search github for agent frameworks',
      'discover a coding agent project',
      'locate repositories for autonomous agents',
      'find me an agentic software project',
      'look for open source multi agent tools',
      'which github repo implements coding agents',
      'identify an agent framework repository',
    ],
    negative: [
      'fix the CSS in this repository',
      'review the security of this project',
      'write unit tests for the current module',
      'deploy this application to production',
    ],
  }));
  const env = {
    ...process.env,
    SKILL_ROUTER_CWD: repo,
    SKILL_ROUTER_HOME: home,
    SKILL_ROUTER_DATA_DIR: data,
    SKILL_ROUTER_OVERLAY_ROOTS: overlays,
    SKILL_ROUTER_HOST: 'codex',
  };

  execFileSync(process.execPath, [buildScript], { cwd: repo, env, stdio: 'pipe' });
  const scopes = fs.readdirSync(path.join(data, 'scopes'));
  assert.equal(scopes.length, 1);
  const cacheDir = path.join(data, 'scopes', scopes[0]);
  const manifest = JSON.parse(fs.readFileSync(path.join(cacheDir, 'manifest.json')));
  assert.equal(manifest.active_skills['repo-finder'].scope, 'project');
  assert.equal(manifest.coverage.covered, 1);
  assert.equal(manifest.coverage.uncovered, 0);

  fs.mkdirSync(path.join(skillDir, 'empty-directory'));
  execFileSync(process.execPath, [buildScript], { cwd: repo, env, stdio: 'pipe' });
  const refreshedManifest = JSON.parse(fs.readFileSync(path.join(cacheDir, 'manifest.json')));
  assert.notEqual(refreshedManifest.stat_fingerprint, manifest.stat_fingerprint);
  assert.equal(refreshedManifest.source_fingerprint, manifest.source_fingerprint);

  const hook = spawnSync(process.execPath, [hookScript], {
    cwd: repo,
    env,
    input: JSON.stringify({ prompt: 'find an open source agent repository', cwd: repo }),
    encoding: 'utf8',
  });
  assert.equal(hook.status, 0);
  const response = JSON.parse(hook.stdout);
  assert.equal(response.hookSpecificOutput.hookEventName, 'UserPromptSubmit');
  assert.match(response.hookSpecificOutput.additionalContext, /\$repo-finder/);
  assert.ok(response.hookSpecificOutput.additionalContext.length <= 500);

  const logged = spawnSync(process.execPath, [hookScript], {
    cwd: repo,
    env: { ...env, SKILL_ROUTER_LOG: '1' },
    input: JSON.stringify({ prompt: 'find an open source agent repository', cwd: repo, session_id: 's1', turn_id: 't1' }),
    encoding: 'utf8',
  });
  assert.equal(logged.status, 0);
  const log = fs.readFileSync(path.join(data, 'logs', 'routing.jsonl'), 'utf8');
  assert.doesNotMatch(log, /find an open source agent repository/);
  assert.match(log, /repo-finder/);
});
