#!/usr/bin/env node
'use strict';

const { performance } = require('node:perf_hooks');
const { routePayload } = require('../bm25-suggest');

function percentile(values, quantile) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * quantile))] || 0;
}

function main() {
  const iterationsArg = process.argv.indexOf('--iterations');
  const iterations = iterationsArg === -1 ? 1_000 : Number(process.argv[iterationsArg + 1]);
  if (!Number.isInteger(iterations) || iterations < 1) throw new Error('--iterations must be a positive integer');
  const cwdArg = process.argv.indexOf('--cwd');
  const cwd = cwdArg === -1 ? process.cwd() : process.argv[cwdArg + 1];
  const prompts = [
    'find repositories implementing shared agent memory',
    'analyse ce dépôt sans modifier les fichiers',
    'review this project for security issues',
    '$agentic-project-finder find projects',
    'ne suggère aucune skill pour ce prompt',
  ];
  routePayload({ prompt: prompts[0], cwd });
  const values = [];
  let emitted = 0;
  for (let index = 0; index < iterations; index += 1) {
    const start = performance.now();
    const output = routePayload({ prompt: prompts[index % prompts.length], cwd });
    values.push(performance.now() - start);
    if (output) emitted += 1;
  }
  process.stdout.write(`${JSON.stringify({
    iterations,
    emitted,
    latency_ms: {
      p50: percentile(values, 0.50),
      p95: percentile(values, 0.95),
      max: Math.max(...values),
    },
  }, null, 2)}\n`);
}

if (require.main === module) {
  try { main(); } catch (error) {
    process.stderr.write(`[benchmark] ${error.message}\n`);
    process.exitCode = 1;
  }
}

