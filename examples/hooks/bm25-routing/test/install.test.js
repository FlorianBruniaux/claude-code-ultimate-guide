'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const installer = path.resolve(__dirname, '..', 'install.js');

test('dry-run is read-only and apply is idempotent while preserving existing hooks', () => {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'router-install-'));
  const hooksFile = path.join(home, '.codex', 'hooks.json');
  fs.mkdirSync(path.dirname(hooksFile), { recursive: true });
  fs.writeFileSync(hooksFile, JSON.stringify({
    hooks: {
      UserPromptSubmit: [{
        hooks: [{ type: 'command', command: 'bash /existing/status.sh' }],
      }],
    },
  }));
  const before = fs.readFileSync(hooksFile, 'utf8');

  const dry = spawnSync(process.execPath, [installer, '--host', 'codex', '--scope', 'user', '--home', home, '--dry-run'], { encoding: 'utf8' });
  assert.equal(dry.status, 0, dry.stderr);
  assert.equal(fs.readFileSync(hooksFile, 'utf8'), before);
  assert.equal(fs.existsSync(path.join(home, '.codex', 'hooks', 'skill-router')), false);
  assert.match(dry.stdout, /DRY RUN/);

  const apply = spawnSync(process.execPath, [installer, '--host', 'codex', '--scope', 'user', '--home', home, '--apply'], { encoding: 'utf8' });
  assert.equal(apply.status, 0, apply.stderr);
  const installed = JSON.parse(fs.readFileSync(hooksFile, 'utf8'));
  assert.equal(installed.hooks.UserPromptSubmit.length, 2);
  assert.equal(installed.hooks.UserPromptSubmit[0].hooks[0].command, 'bash /existing/status.sh');
  assert.match(installed.hooks.UserPromptSubmit[1].hooks[0].command, /SKILL_ROUTER_HOST=codex/);
  assert.ok(fs.existsSync(path.join(home, '.codex', 'hooks', 'skill-router', 'routing', 'discovery.js')));

  const hooksAfterFirst = fs.readFileSync(hooksFile, 'utf8');
  const second = spawnSync(process.execPath, [installer, '--host', 'codex', '--scope', 'user', '--home', home, '--apply'], { encoding: 'utf8' });
  assert.equal(second.status, 0, second.stderr);
  assert.equal(fs.readFileSync(hooksFile, 'utf8'), hooksAfterFirst);
  assert.match(second.stdout, /already current/);
});

