#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SOURCE_ROOT = __dirname;
const RUNTIME_FILES = [
  'bm25-suggest.js',
  'routing/bm25.js',
  'routing/benchmark.js',
  'routing/build-index.js',
  'routing/cache.js',
  'routing/discovery.js',
  'routing/package.json',
  'routing/paths.js',
  'routing/tokenize.js',
  'corpus/agentic-project-finder/scenarios.json',
];

function parseArgs(argv) {
  const args = { dryRun: false, apply: false };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--dry-run') args.dryRun = true;
    else if (token === '--apply') args.apply = true;
    else if (token.startsWith('--')) args[token.slice(2).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] = argv[++index];
  }
  if (args.dryRun === args.apply) throw new Error('choose exactly one of --dry-run or --apply');
  if (!['codex', 'claude'].includes(args.host)) throw new Error('--host must be codex or claude');
  if (!['user', 'project'].includes(args.scope)) throw new Error('--scope must be user or project');
  if (args.scope === 'project' && !args.projectRoot) throw new Error('--project-root is required for project scope');
  return args;
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function destinationFor(args) {
  const home = path.resolve(args.home || os.homedir());
  if (args.scope === 'user') {
    if (args.host !== 'codex') throw new Error('Claude user installation is intentionally unsupported; use project scope');
    return {
      target: path.join(home, '.codex', 'hooks', 'skill-router'),
      hooksFile: path.join(home, '.codex', 'hooks.json'),
      backupBase: path.join(home, '.codex', 'backups', 'skill-router'),
      dataDir: path.join(home, '.codex', 'skill-router-data'),
    };
  }
  const project = path.resolve(args.projectRoot);
  const configDir = args.host === 'codex' ? '.codex' : '.claude';
  return {
    target: path.join(project, configDir, 'hooks', 'skill-router'),
    hooksFile: path.join(project, configDir, args.host === 'codex' ? 'hooks.json' : 'settings.json'),
    backupBase: path.join(project, configDir, 'backups', 'skill-router'),
    dataDir: path.join(home, '.codex', 'skill-router-data'),
  };
}

function desiredHandler(target, host, dataDir) {
  return {
    hooks: [{
      type: 'command',
      command: `env SKILL_ROUTER_HOST=${host} SKILL_ROUTER_DATA_DIR=${JSON.stringify(dataDir)} node ${JSON.stringify(path.join(target, 'bm25-suggest.js'))}`,
      timeout: 2,
      additionalContextLimit: 300,
    }],
  };
}

function readHooks(file) {
  if (!fs.existsSync(file)) return { hooks: {} };
  const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error(`invalid hooks object: ${file}`);
  if (!parsed.hooks || typeof parsed.hooks !== 'object' || Array.isArray(parsed.hooks)) parsed.hooks = {};
  return parsed;
}

function mergeHandler(config, handler) {
  const list = Array.isArray(config.hooks.UserPromptSubmit) ? [...config.hooks.UserPromptSubmit] : [];
  const indexes = [];
  list.forEach((entry, index) => {
    const commands = Array.isArray(entry && entry.hooks) ? entry.hooks.map((hook) => String(hook.command || '')) : [];
    if (commands.some((command) => command.includes('skill-router/bm25-suggest.js'))) indexes.push(index);
  });
  if (!indexes.length) list.push(handler);
  else {
    list[indexes[0]] = handler;
    for (let index = indexes.length - 1; index >= 1; index -= 1) list.splice(indexes[index], 1);
  }
  config.hooks.UserPromptSubmit = list;
  return config;
}

function sourcePlan(target) {
  return RUNTIME_FILES.map((relative) => {
    const source = path.join(SOURCE_ROOT, relative);
    if (!fs.existsSync(source)) throw new Error(`missing runtime source: ${source}`);
    const destination = path.join(target, relative);
    return {
      relative,
      source,
      destination,
      checksum: sha256(source),
      currentChecksum: fs.existsSync(destination) ? sha256(destination) : null,
    };
  });
}

function copyRuntime(plan, target) {
  const staging = `${target}.staging-${process.pid}`;
  fs.rmSync(staging, { recursive: true, force: true });
  for (const item of plan) {
    const destination = path.join(staging, item.relative);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.copyFileSync(item.source, destination);
  }
  fs.chmodSync(path.join(staging, 'bm25-suggest.js'), 0o755);
  fs.chmodSync(path.join(staging, 'routing', 'build-index.js'), 0o755);
  if (fs.existsSync(target)) fs.rmSync(target, { recursive: true });
  fs.renameSync(staging, target);
}

function install(args) {
  const destination = destinationFor(args);
  const plan = sourcePlan(destination.target);
  const originalHooks = readHooks(destination.hooksFile);
  const desiredHooks = mergeHandler(structuredClone(originalHooks), desiredHandler(destination.target, args.host, destination.dataDir));
  const hooksBefore = `${JSON.stringify(originalHooks, null, 2)}\n`;
  const hooksAfter = `${JSON.stringify(desiredHooks, null, 2)}\n`;
  const runtimeCurrent = plan.every((item) => item.checksum === item.currentChecksum);
  const hooksCurrent = hooksBefore === hooksAfter;

  process.stdout.write(`${args.dryRun ? 'DRY RUN' : 'APPLY'} ${args.host}/${args.scope}\n`);
  for (const item of plan) {
    process.stdout.write(`${item.source} -> ${item.destination} sha256=${item.checksum}\n`);
  }
  process.stdout.write(`${destination.hooksFile}: ${hooksCurrent ? 'unchanged' : 'merge UserPromptSubmit handler'}\n`);
  if (runtimeCurrent && hooksCurrent) {
    process.stdout.write('already current\n');
    return { changed: false };
  }
  if (args.dryRun) return { changed: true };

  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backup = path.join(destination.backupBase, stamp);
  fs.mkdirSync(backup, { recursive: true });
  if (!runtimeCurrent) {
    if (fs.existsSync(destination.target)) fs.cpSync(destination.target, path.join(backup, 'skill-router'), { recursive: true });
    fs.mkdirSync(path.dirname(destination.target), { recursive: true });
    copyRuntime(plan, destination.target);
  }
  if (!hooksCurrent) {
    if (fs.existsSync(destination.hooksFile)) fs.copyFileSync(destination.hooksFile, path.join(backup, path.basename(destination.hooksFile)));
    fs.mkdirSync(path.dirname(destination.hooksFile), { recursive: true });
    const tmp = `${destination.hooksFile}.tmp.${process.pid}`;
    fs.writeFileSync(tmp, hooksAfter, { mode: 0o600 });
    fs.renameSync(tmp, destination.hooksFile);
  }
  process.stdout.write(`backup=${backup}\n`);
  return { changed: true, backup };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  install(args);
}

if (require.main === module) {
  try { main(); } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = { install, mergeHandler, parseArgs };
