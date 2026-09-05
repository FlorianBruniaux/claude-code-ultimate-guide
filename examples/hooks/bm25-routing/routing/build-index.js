#!/usr/bin/env node
'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { tokenize } = require('./tokenize');
const { buildIndex, scoreDoc, scoreSkills } = require('./bm25');
const { discoverCorpora, discoverSkills } = require('./discovery');
const { overlayRoots, resolveContext } = require('./paths');
const {
  ALGORITHM_VERSION,
  acquireBuildLock,
  fingerprintFiles,
  fingerprintStats,
  writeJsonAtomic,
} = require('./cache');

const MIN_POS = 8;
const MIN_NEG = 2;
const MIN_F1 = 0.60;
const MIN_EVAL_F1 = 0.55;
const MIN_GLOBAL_F1 = 0.70;

function tokenizeScenarios(corpora) {
  const scenarios = [];
  for (const corpus of corpora) {
    for (const prompt of corpus.positive) {
      scenarios.push({ skill: corpus.skill, prompt, polarity: 'pos', tokens: tokenize(prompt).tokens });
    }
    for (const prompt of corpus.negative) {
      scenarios.push({ skill: corpus.skill, prompt, polarity: 'neg', tokens: tokenize(prompt).tokens });
    }
  }
  return scenarios;
}

function maxScoreAgainstPositives(probe, positives, index, excluded) {
  let best = 0;
  for (const document of positives) {
    if (document === excluded) continue;
    best = Math.max(best, scoreDoc(probe.tokens, document, index.idf, index.avgdl));
  }
  return best;
}

function metricsAt(posScores, negScores, tau) {
  const TP = posScores.filter((score) => score >= tau).length;
  const FP = negScores.filter((score) => score >= tau).length;
  const FN = posScores.length - TP;
  const precision = TP + FP ? TP / (TP + FP) : 0;
  const recall = TP + FN ? TP / (TP + FN) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  const beta2 = 4;
  const fbeta2 = beta2 * precision + recall
    ? ((1 + beta2) * precision * recall) / (beta2 * precision + recall)
    : 0;
  return { TP, FP, FN, precision, recall, f1, fbeta2 };
}

function calibrateThresholds(scenarios, index) {
  const thresholds = {};
  for (const skill of [...new Set(scenarios.map((scenario) => scenario.skill))].sort()) {
    const positives = scenarios.filter((scenario) => scenario.skill === skill && scenario.polarity === 'pos');
    const negatives = scenarios.filter((scenario) => scenario.skill === skill && scenario.polarity === 'neg');
    if (positives.length < MIN_POS || negatives.length < MIN_NEG) {
      thresholds[skill] = {
        status: 'excluded', tau: null, f1: null,
        n_pos: positives.length, n_neg: negatives.length,
      };
      continue;
    }
    const posScores = positives.map((probe) => maxScoreAgainstPositives(probe, positives, index, probe));
    const negScores = negatives.map((probe) => maxScoreAgainstPositives(probe, positives, index));
    const observed = [...new Set([...posScores, ...negScores].filter((score) => score > 0))].sort((a, b) => a - b);
    if (!observed.length) {
      thresholds[skill] = {
        status: 'conflict', tau: null, f1: 0,
        n_pos: positives.length, n_neg: negatives.length,
      };
      continue;
    }
    const candidates = observed.map((score, indexValue) => (
      indexValue === 0 ? Math.max(Number.EPSILON, score - 0.001) : (observed[indexValue - 1] + score) / 2
    ));
    let best = null;
    for (const tau of candidates) {
      const metrics = metricsAt(posScores, negScores, tau);
      if (!best || metrics.fbeta2 > best.fbeta2 || (metrics.fbeta2 === best.fbeta2 && metrics.f1 > best.f1)) {
        best = { tau, ...metrics };
      }
    }
    thresholds[skill] = {
      ...best,
      n_pos: positives.length,
      n_neg: negatives.length,
      status: best.f1 >= MIN_F1 ? 'ok' : 'conflict',
    };
  }
  return thresholds;
}

function candidateMatches(probe, scenarios, index, thresholds, allowedSkills) {
  return scoreSkills(probe.tokens, scenarios.filter((scenario) => scenario !== probe), index)
    .filter((candidate) => {
      const threshold = thresholds[candidate.skill];
      if (!threshold || threshold.status !== 'ok' || !Number.isFinite(threshold.tau)) return false;
      if (allowedSkills && !allowedSkills.has(candidate.skill)) return false;
      if (candidate.score < threshold.tau) return false;
      return !Number.isFinite(candidate.negativeScore) || candidate.negativeScore < candidate.score;
    })
    .slice(0, 3)
    .map((candidate) => candidate.skill);
}

function crossSkillEvaluation(scenarios, index, thresholds, allowedSkills = null) {
  const perSkill = {};
  for (const skill of Object.keys(thresholds)) {
    perSkill[skill] = { TP: 0, FP: 0, FN: 0, TN: 0, n_pos: 0, n_neg: 0 };
  }
  for (const probe of scenarios) {
    const matches = new Set(candidateMatches(probe, scenarios, index, thresholds, allowedSkills));
    const owner = perSkill[probe.skill];
    if (!owner) continue;
    if (probe.polarity === 'pos') {
      owner.n_pos += 1;
      if (matches.has(probe.skill)) owner.TP += 1;
      else owner.FN += 1;
      for (const match of matches) if (match !== probe.skill && perSkill[match]) perSkill[match].FP += 1;
    } else {
      owner.n_neg += 1;
      if (matches.has(probe.skill)) owner.FP += 1;
      else owner.TN += 1;
    }
  }
  let TP = 0;
  let FP = 0;
  let FN = 0;
  for (const [skill, metrics] of Object.entries(perSkill)) {
    const precision = metrics.TP + metrics.FP ? metrics.TP / (metrics.TP + metrics.FP) : 0;
    const recall = metrics.TP + metrics.FN ? metrics.TP / (metrics.TP + metrics.FN) : 0;
    const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
    perSkill[skill] = { ...metrics, precision, recall, f1 };
    if (!allowedSkills || allowedSkills.has(skill)) {
      TP += metrics.TP;
      FP += metrics.FP;
      FN += metrics.FN;
    }
  }
  const precision = TP + FP ? TP / (TP + FP) : 0;
  const recall = TP + FN ? TP / (TP + FN) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return { perSkill, global: { TP, FP, FN, precision, recall, f1 } };
}

function selectEligibleSkills(scenarios, index, thresholds, protectedSkills = new Set()) {
  const initial = crossSkillEvaluation(scenarios, index, thresholds);
  const eligible = new Set(Object.entries(initial.perSkill)
    .filter(([skill, metrics]) => thresholds[skill].status === 'ok' && metrics.f1 >= MIN_EVAL_F1)
    .map(([skill]) => skill));
  const removedForGlobalGate = [];
  let final = crossSkillEvaluation(scenarios, index, thresholds, eligible);
  while (eligible.size && final.global.f1 < MIN_GLOBAL_F1) {
    const removable = [...eligible].filter((skill) => !protectedSkills.has(skill));
    if (!removable.length) break;
    const worst = removable.sort((left, right) => {
      const difference = final.perSkill[left].f1 - final.perSkill[right].f1;
      return difference || left.localeCompare(right);
    })[0];
    eligible.delete(worst);
    removedForGlobalGate.push(worst);
    final = crossSkillEvaluation(scenarios, index, thresholds, eligible);
  }
  for (const [skill, threshold] of Object.entries(thresholds)) {
    threshold.eligible = eligible.has(skill);
    threshold.evaluation = initial.perSkill[skill];
  }
  return {
    initial,
    final,
    eligible: [...eligible].sort(),
    protected: [...protectedSkills].filter((skill) => eligible.has(skill)).sort(),
    removedForGlobalGate,
    globalGatePassed: final.global.f1 >= MIN_GLOBAL_F1,
  };
}

function buildHash(scenarios, index) {
  const hash = crypto.createHash('sha256');
  hash.update(`algorithm=${ALGORITHM_VERSION}\n`);
  for (const scenario of [...scenarios].sort((a, b) => `${a.skill}|${a.prompt}`.localeCompare(`${b.skill}|${b.prompt}`))) {
    hash.update(`${scenario.skill}|${scenario.polarity}|${scenario.prompt}\n`);
  }
  hash.update(JSON.stringify({ K1: index.K1, B: index.B }));
  return hash.digest('hex');
}

function serializableSkills(skills, thresholds, coveredSkills) {
  return Object.fromEntries([...skills.entries()].map(([name, skill]) => [name, {
    description: skill.description,
    skillMd: skill.skillMd,
    scope: skill.scope,
    root: skill.root,
    precedence: skill.precedence,
    scenarioStatus: coveredSkills.has(name) && thresholds[name].eligible ? 'ok' : 'native-only',
  }]));
}

function build(options = {}) {
  const dryRun = options.dryRun || process.argv.includes('--dry-run');
  const context = resolveContext(options.cwd || process.env.SKILL_ROUTER_CWD || process.cwd());
  const discovered = discoverSkills(context.roots);
  const corpora = discoverCorpora({ skills: discovered.skills, overlayRoots: overlayRoots() });
  const sourceFiles = [
    ...[...discovered.skills.values()].map((skill) => skill.skillMd),
    ...corpora.sources.map((source) => source.path),
  ];
  const sourceFingerprint = fingerprintFiles(sourceFiles);
  const watchPaths = [
    ...context.roots.map((root) => root.path),
    ...overlayRoots(),
    ...[...discovered.skills.values()].flatMap((skill) => [skill.directory, path.join(skill.directory, 'evals')]),
    ...corpora.sources.map((source) => path.dirname(source.path)),
  ];
  let ancestor = context.cwd;
  const boundary = context.repoRoot || path.parse(context.cwd).root;
  while (true) {
    watchPaths.push(path.join(ancestor, '.agents', 'skills'));
    if (ancestor === boundary) break;
    const parent = path.dirname(ancestor);
    if (parent === ancestor) break;
    ancestor = parent;
  }
  const statFingerprint = fingerprintStats([...sourceFiles, ...watchPaths]);
  const scenarios = tokenizeScenarios(corpora.sources);
  const index = buildIndex(scenarios);
  const thresholds = calibrateThresholds(scenarios, index);
  const overlaySkills = new Set(corpora.sources.filter((source) => source.kind === 'overlay').map((source) => source.skill));
  const quality = selectEligibleSkills(scenarios, index, thresholds, overlaySkills);
  const hash = buildHash(scenarios, index);
  const coveredSkills = new Set(corpora.sources.map((source) => source.skill));
  const coverage = {
    active: discovered.skills.size,
    covered: coveredSkills.size,
    uncovered: discovered.skills.size - coveredSkills.size,
    eligible: quality.eligible.length,
    uncovered_skills: [...discovered.skills.keys()].filter((name) => !coveredSkills.has(name)).sort(),
  };
  const result = {
    context,
    index: {
      version: 2,
      algorithm_version: ALGORITHM_VERSION,
      build_hash: hash,
      K1: index.K1,
      B: index.B,
      avgdl: index.avgdl,
      idf: index.idf,
      scenarios,
    },
    thresholds,
    metrics: quality,
    manifest: {
      version: 2,
      algorithm_version: ALGORITHM_VERSION,
      build_hash: hash,
      source_fingerprint: sourceFingerprint,
      stat_fingerprint: statFingerprint,
      source_files: [...new Set(sourceFiles)].sort(),
      watch_paths: [...new Set(watchPaths)].sort(),
      scope_key: context.scopeKey,
      cwd: context.cwd,
      repo_root: context.repoRoot,
      roots: context.roots,
      active_skills: serializableSkills(discovered.skills, thresholds, coveredSkills),
      coverage,
      scenarios_count: scenarios.length,
      positive_count: scenarios.filter((scenario) => scenario.polarity === 'pos').length,
      negative_count: scenarios.filter((scenario) => scenario.polarity === 'neg').length,
      problems: [...discovered.problems, ...corpora.problems],
      built_at: new Date().toISOString(),
    },
  };
  if (dryRun) return result;

  const lock = acquireBuildLock(path.join(context.cacheDir, 'build.lock'));
  if (!lock.acquired) return { ...result, skipped: 'locked' };
  try {
    let current;
    try { current = JSON.parse(fs.readFileSync(path.join(context.cacheDir, 'manifest.json'), 'utf8')); } catch { current = null; }
    if (current && current.source_fingerprint === sourceFingerprint && current.algorithm_version === ALGORITHM_VERSION) {
      writeJsonAtomic(path.join(context.cacheDir, 'manifest.json'), {
        ...current,
        stat_fingerprint: statFingerprint,
        source_files: result.manifest.source_files,
        watch_paths: result.manifest.watch_paths,
      });
      writeJsonAtomic(path.join(context.cacheDir, 'verified.json'), { checked_at: new Date().toISOString() });
      return { ...result, skipped: 'cache-hit' };
    }
    writeJsonAtomic(path.join(context.cacheDir, 'index.json'), result.index);
    writeJsonAtomic(path.join(context.cacheDir, 'thresholds.json'), thresholds);
    writeJsonAtomic(path.join(context.cacheDir, 'manifest.json'), result.manifest);
    writeJsonAtomic(path.join(context.cacheDir, 'coverage.json'), coverage);
    writeJsonAtomic(path.join(context.cacheDir, 'metrics.json'), quality);
    writeJsonAtomic(path.join(context.cacheDir, 'verified.json'), { checked_at: new Date().toISOString() });
  } finally {
    lock.release();
  }
  return result;
}

function main() {
  try {
    const result = build();
    const summary = {
      scope: result.context.scopeKey,
      scenarios: result.manifest.scenarios_count,
      skills: result.manifest.coverage.active,
      covered: result.manifest.coverage.covered,
      eligible: result.manifest.coverage.eligible,
      conflicts: Object.values(result.thresholds).filter((threshold) => threshold.status === 'conflict').length,
      excluded: Object.values(result.thresholds).filter((threshold) => threshold.status === 'excluded').length,
      skipped: result.skipped || null,
    };
    process.stdout.write(`${JSON.stringify(summary)}\n`);
  } finally {
    if (process.env.SKILL_ROUTER_REQUEST_FILE) {
      try { fs.unlinkSync(process.env.SKILL_ROUTER_REQUEST_FILE); } catch { /* request expired or already cleared */ }
    }
  }
}

if (require.main === module) {
  try { main(); } catch (error) {
    process.stderr.write(`[build-index] ${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = {
  build,
  calibrateThresholds,
  crossSkillEvaluation,
  metricsAt,
  selectEligibleSkills,
  tokenizeScenarios,
};
