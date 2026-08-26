#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { performance } = require('node:perf_hooks');
const { build } = require('./build-index');
const { scoreSkills } = require('./bm25');
const { tokenize } = require('./tokenize');
const { filterEligible, shouldSkipPrompt } = require('../bm25-suggest');

function percentile(values, quantile) {
  if (!values.length) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * quantile))];
}

function evaluate(acceptance, built) {
  const active = built.manifest.active_skills;
  const decisions = [];
  const latencies = [];
  let expectedCount = 0;
  let truePositive = 0;
  let emitted = 0;
  let forbiddenHits = 0;
  for (const item of acceptance) {
    const start = performance.now();
    let matches = [];
    if (!shouldSkipPrompt(item.prompt, 'codex', Object.keys(active))) {
      const scored = scoreSkills(tokenize(item.prompt).tokens, built.index.scenarios, built.index);
      matches = filterEligible(scored, built.thresholds, active).slice(0, 3).map((match) => match.skill);
    }
    latencies.push(performance.now() - start);
    const expected = Array.isArray(item.expected) ? item.expected : [];
    const forbidden = Array.isArray(item.forbidden) ? item.forbidden : [];
    expectedCount += expected.length;
    truePositive += expected.filter((skill) => matches.includes(skill)).length;
    emitted += matches.length;
    forbiddenHits += forbidden.filter((skill) => matches.includes(skill)).length;
    decisions.push({ id: item.id || null, expected, forbidden, matches });
  }
  const falsePositive = Math.max(0, emitted - truePositive);
  const precision = emitted ? truePositive / emitted : 0;
  const recall = expectedCount ? truePositive / expectedCount : 1;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return {
    prompts: acceptance.length,
    expected: expectedCount,
    emitted,
    true_positive: truePositive,
    false_positive: falsePositive,
    forbidden_hits: forbiddenHits,
    precision,
    recall,
    f1,
    latency_ms: {
      p50: percentile(latencies, 0.50),
      p95: percentile(latencies, 0.95),
      max: Math.max(0, ...latencies),
    },
    decisions,
  };
}

function parseArg(name) {
  const index = process.argv.indexOf(name);
  return index === -1 ? null : process.argv[index + 1];
}

function main() {
  const file = path.resolve(parseArg('--acceptance') || path.join(__dirname, '..', 'test', 'acceptance-prompts.json'));
  const acceptance = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!Array.isArray(acceptance)) throw new Error('acceptance file must be an array');
  const result = evaluate(acceptance, build({ dryRun: true }));
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (process.argv.includes('--strict')) {
    if (result.precision < 0.80 || result.f1 < 0.70 || result.forbidden_hits > 0) process.exitCode = 1;
  }
}

if (require.main === module) {
  try { main(); } catch (error) {
    process.stderr.write(`[eval] ${error.message}\n`);
    process.exitCode = 1;
  }
}

module.exports = { evaluate, percentile };
