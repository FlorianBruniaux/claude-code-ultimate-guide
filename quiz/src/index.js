#!/usr/bin/env node
/**
 * Claude Code Knowledge Quiz
 * Test your understanding of Claude Code with interactive MCQs
 *
 * Part of: claude-code-ultimate-guide
 * Author: Florian BRUNIAUX
 */

import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { parseArgs } from 'util';

import { displayHeader, displayHelp } from './ui.js';
import { selectProfile, selectTopics } from './prompts.js';
import { loadQuestions, selectQuestions } from './questions.js';
import { runQuiz } from './quiz.js';
import { displayFinalScore, offerRetry } from './score.js';
import { loadSession, saveSession } from './session.js';
import { TOPICS, TOPIC_IDS, parseTopicIds } from './topics.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// CLI argument parsing
const { values: args } = parseArgs({
  options: {
    profile: { type: 'string', short: 'p' },
    topics: { type: 'string', short: 't' },
    count: { type: 'string', short: 'c' },
    dynamic: { type: 'boolean', short: 'd', default: false },
    help: { type: 'boolean', short: 'h', default: false },
    version: { type: 'boolean', short: 'v', default: false }
  },
  strict: false
});

// Profile configurations
const PROFILES = {
  junior: {
    name: 'Junior Developer',
    description: '45 min to productivity',
    questionCount: 15,
    focusTopics: [1, 2, 3, 6],
    difficultyWeight: { junior: 0.8, senior: 0.2, power: 0 }
  },
  senior: {
    name: 'Senior Developer',
    description: '40 min to mastery',
    questionCount: 20,
    focusTopics: [2, 3, 4, 7, 9],
    difficultyWeight: { junior: 0.3, senior: 0.5, power: 0.2 }
  },
  power: {
    name: 'Power User',
    description: '2 hours for full mastery',
    questionCount: 25,
    focusTopics: TOPIC_IDS,
    difficultyWeight: { junior: 0.2, senior: 0.4, power: 0.4 }
  },
  pm: {
    name: 'Product Manager',
    description: '20 min overview',
    questionCount: 10,
    focusTopics: [1, 2, 3, 16, 17],
    difficultyWeight: { junior: 1, senior: 0, power: 0 }
  }
};

async function main() {
  // Handle help/version
  if (args.help) {
    displayHelp();
    process.exit(0);
  }

  if (args.version) {
    console.log('claude-code-quiz v1.0.0');
    process.exit(0);
  }

  // Display header
  displayHeader();

  // Profile selection
  let profile;
  if (args.profile && PROFILES[args.profile]) {
    profile = args.profile;
  } else {
    profile = await selectProfile(PROFILES);
  }

  // Topic selection
  let selectedTopics;
  if (args.topics) {
    selectedTopics = parseTopicIds(args.topics);
    if (selectedTopics.length === 0) selectedTopics = PROFILES[profile].focusTopics;
  } else {
    selectedTopics = await selectTopics(TOPICS, PROFILES[profile].focusTopics);
  }

  // Question count
  let questionCount = PROFILES[profile].questionCount;
  if (args.count) {
    const parsed = parseInt(args.count);
    if (parsed > 0 && parsed <= 50) questionCount = parsed;
  }

  // Load and filter questions
  const questionsDir = join(__dirname, '..', 'questions');
  const allQuestions = await loadQuestions(questionsDir);
  const questionOptions = {
    profile,
    topics: selectedTopics,
    count: questionCount,
    difficultyWeight: PROFILES[profile].difficultyWeight
  };

  const quizQuestions = selectQuestions(allQuestions, questionOptions);

  if (quizQuestions.length === 0) {
    console.log('\nNo questions available for selected criteria. Try different topics.');
    process.exit(1);
  }

  // Run quiz
  const results = await runQuiz(quizQuestions, {
    profile,
    topics: selectedTopics,
    dynamicEnabled: args.dynamic
  });

  // Display final score
  displayFinalScore(results, TOPICS);

  // Save session
  await saveSession(results);

  // Offer retry
  const retryChoice = await offerRetry(results);

  if (retryChoice === 'retry-wrong') {
    // Filter to only wrong questions and run again
    const wrongQuestions = results.questions.filter(q => !q.correct);
    if (wrongQuestions.length > 0) {
      const retryResults = await runQuiz(wrongQuestions.map(q => q.question), {
        profile,
        topics: selectedTopics,
        dynamicEnabled: args.dynamic,
        isRetry: true
      });
      displayFinalScore(retryResults, TOPICS);
      await saveSession(retryResults);
    }
  } else if (retryChoice === 'new-quiz') {
    // Restart with different questions
    const previousQuestionIds = new Set(quizQuestions.map(question => question.id));
    const newQuestions = selectQuestions(allQuestions, questionOptions, previousQuestionIds);
    const newResults = await runQuiz(newQuestions, {
      profile,
      topics: selectedTopics,
      dynamicEnabled: args.dynamic
    });
    displayFinalScore(newResults, TOPICS);
    await saveSession(newResults);
  }
  // else 'exit' - do nothing
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
