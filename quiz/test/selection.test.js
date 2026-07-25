import assert from 'node:assert/strict';
import test from 'node:test';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { loadQuestions, selectQuestions } from '../src/questions.js';
import { TOPIC_IDS, parseTopicIds } from '../src/topics.js';

const testDirectory = dirname(fileURLToPath(import.meta.url));
const questions = await loadQuestions(join(testDirectory, '..', 'questions'));

test('every bundled category is selectable', () => {
  const categories = [...new Set(questions.map(question => question.category_id))].sort((a, b) => a - b);

  assert.deepEqual(TOPIC_IDS, categories);
  assert.deepEqual(parseTopicIds('11,17'), [11, 17]);
});

test('PM profile can supply its advertised ten-question quiz', () => {
  const selected = selectQuestions(questions, {
    profile: 'pm',
    topics: [1, 2, 3, 16, 17],
    count: 10,
    difficultyWeight: { junior: 1, senior: 0, power: 0 }
  });

  assert.equal(selected.length, 10);
});

test('a new quiz avoids the immediately previous set when enough questions exist', () => {
  const pool = Array.from({ length: 12 }, (_, index) => ({
    id: `question-${index}`,
    category_id: 17,
    difficulty: 'junior',
    profiles: ['pm']
  }));
  const options = {
    profile: 'pm',
    topics: [17],
    count: 6,
    difficultyWeight: { junior: 1, senior: 0, power: 0 }
  };
  const firstSet = selectQuestions(pool, options);
  const nextSet = selectQuestions(pool, options, new Set(firstSet.map(question => question.id)));

  assert.equal(nextSet.length, options.count);
  assert.equal(nextSet.some(question => firstSet.some(previous => previous.id === question.id)), false);
});
