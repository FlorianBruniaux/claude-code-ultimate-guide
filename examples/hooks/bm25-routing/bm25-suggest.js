#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { tokenize } = require('./routing/tokenize');
const { scoreSkills } = require('./routing/bm25');
const { fingerprintStats } = require('./routing/cache');
const { resolveContext } = require('./routing/paths');

const BUILD_SCRIPT = path.join(__dirname, 'routing', 'build-index.js');
const MAX_HINTS = 3;
const MAX_CONTEXT_CHARS = 500;
const DEEP_CHECK_INTERVAL_MS = Number(process.env.SKILL_ROUTER_DEEP_CHECK_MS || 60_000);

function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', () => resolve(''));
  });
}

function shouldSkipPrompt(prompt, host, activeSkillNames) {
  const trimmed = String(prompt || '').trim();
  if (!trimmed) return true;
  const lower = trimmed.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const optOut = [
    'ne propose aucune skill',
    'ne suggere aucune skill',
    'do not suggest a skill',
    "don't suggest a skill",
    'disable skill routing',
  ];
  if (optOut.some((phrase) => lower.includes(phrase))) return true;
  const escaped = activeSkillNames.map((name) => name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (!escaped.length) return false;
  const sigil = host === 'claude' ? '/' : '\\$';
  return new RegExp(`(?:^|\\s)${sigil}(?:${escaped.join('|')})(?:\\s|$)`, 'i').test(trimmed);
}

function filterEligible(scored, thresholds, activeSkills) {
  return scored.flatMap((candidate) => {
    const threshold = thresholds[candidate.skill];
    const active = activeSkills[candidate.skill];
    if (!threshold || threshold.status !== 'ok' || threshold.eligible !== true || !Number.isFinite(threshold.tau)) return [];
    if (Number.isFinite(candidate.negativeScore) && candidate.negativeScore >= candidate.score) return [];
    if (candidate.score < threshold.tau || !active || !active.skillMd) return [];
    return [{ ...candidate, skillMd: active.skillMd }];
  });
}

function formatHint(matches, host) {
  if (!matches.length) return '';
  const sigil = host === 'claude' ? '/' : '$';
  const lines = matches.map((match) => `- ${sigil}${match.skill} (${match.skillMd})`);
  let text = `Skill routing candidates:\n${lines.join('\n')}\nUse only if the intent matches.`;
  if (text.length > MAX_CONTEXT_CHARS) text = `${text.slice(0, MAX_CONTEXT_CHARS - 1)}…`;
  return text;
}

function loadCache(cacheDir) {
  try {
    return {
      index: JSON.parse(fs.readFileSync(path.join(cacheDir, 'index.json'), 'utf8')),
      thresholds: JSON.parse(fs.readFileSync(path.join(cacheDir, 'thresholds.json'), 'utf8')),
      manifest: JSON.parse(fs.readFileSync(path.join(cacheDir, 'manifest.json'), 'utf8')),
      verified: JSON.parse(fs.readFileSync(path.join(cacheDir, 'verified.json'), 'utf8')),
    };
  } catch { return null; }
}

function currentStatFingerprint(manifest) {
  try { return fingerprintStats([...(manifest.source_files || []), ...(manifest.watch_paths || [])]); }
  catch { return null; }
}

function reserveRebuild(cacheDir) {
  const requestFile = path.join(cacheDir, 'rebuild.request');
  fs.mkdirSync(cacheDir, { recursive: true });
  try {
    const fd = fs.openSync(requestFile, 'wx', 0o600);
    fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, requestedAt: Date.now() }));
    fs.closeSync(fd);
    return requestFile;
  } catch (error) {
    if (error.code !== 'EEXIST') return null;
  }
  try {
    if (Date.now() - fs.statSync(requestFile).mtimeMs > 30_000) {
      fs.unlinkSync(requestFile);
      return reserveRebuild(cacheDir);
    }
  } catch { /* another process changed the request */ }
  return null;
}

function spawnDetachedRebuild(cwd, cacheDir) {
  const requestFile = reserveRebuild(cacheDir);
  if (!requestFile) return;
  try {
    const child = spawn(process.execPath, [BUILD_SCRIPT], {
      cwd,
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, SKILL_ROUTER_CWD: cwd, SKILL_ROUTER_REQUEST_FILE: requestFile },
    });
    child.unref();
  } catch {
    try { fs.unlinkSync(requestFile); } catch { /* fail open */ }
  }
}

function appendLog(event) {
  if (process.env.SKILL_ROUTER_LOG !== '1') return;
  try {
    const logRoot = process.env.SKILL_ROUTER_DATA_DIR || path.join(__dirname, 'routing', 'data');
    const logDir = path.join(logRoot, 'logs');
    fs.mkdirSync(logDir, { recursive: true });
    fs.appendFileSync(path.join(logDir, 'routing.jsonl'), `${JSON.stringify(event)}\n`, { mode: 0o600 });
  } catch { /* logging never blocks prompts */ }
}

function routePayload(payload) {
  const prompt = payload && payload.prompt;
  if (typeof prompt !== 'string') return null;
  const host = process.env.SKILL_ROUTER_HOST || 'codex';
  if (!['codex', 'claude'].includes(host)) return null;
  const cwd = typeof payload.cwd === 'string' && payload.cwd ? payload.cwd : process.cwd();
  const context = resolveContext(cwd);
  const loaded = loadCache(context.cacheDir);
  if (!loaded) { spawnDetachedRebuild(cwd, context.cacheDir); return null; }

  const activeNames = Object.keys(loaded.manifest.active_skills || {});
  if (shouldSkipPrompt(prompt, host, activeNames)) return null;
  const statFingerprint = currentStatFingerprint(loaded.manifest);
  const checkedAt = Date.parse(loaded.verified && loaded.verified.checked_at);
  const deepCheckDue = !Number.isFinite(checkedAt) || Date.now() - checkedAt > DEEP_CHECK_INTERVAL_MS;
  if (!statFingerprint || statFingerprint !== loaded.manifest.stat_fingerprint || deepCheckDue) {
    spawnDetachedRebuild(cwd, context.cacheDir);
  }

  const tokens = tokenize(prompt).tokens;
  if (!tokens.length) return null;
  const scored = scoreSkills(tokens, loaded.index.scenarios, loaded.index);
  const matches = filterEligible(scored, loaded.thresholds, loaded.manifest.active_skills || {}).slice(0, MAX_HINTS);
  if (!matches.length) return null;

  const additionalContext = formatHint(matches, host);
  appendLog({
    at: new Date().toISOString(),
    host,
    scopeKey: context.scopeKey,
    matches: matches.map(({ skill, score }) => ({ skill, score })),
  });
  return {
    hookSpecificOutput: { hookEventName: 'UserPromptSubmit', additionalContext },
  };
}

async function main() {
  let payload;
  try { payload = JSON.parse(await readStdin()); } catch { return; }
  const output = routePayload(payload);
  if (output) process.stdout.write(JSON.stringify(output));
}

if (require.main === module) main().catch(() => {});

module.exports = { filterEligible, formatHint, main, reserveRebuild, routePayload, shouldSkipPrompt };
