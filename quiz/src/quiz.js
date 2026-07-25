/**
 * Quiz engine - handles the quiz flow
 */

import chalk from 'chalk';
import { displayQuestion, displayCorrect, displayIncorrect, displayProgress } from './ui.js';
import { promptAnswer, promptContinue } from './prompts.js';
import { generateDynamicQuestion } from './dynamic.js';
import { TOPICS } from './topics.js';

/**
 * Run the quiz with given questions
 */
export async function runQuiz(questions, options = {}) {
  const { profile, topics, dynamicEnabled, isRetry } = options;

  const results = {
    profile,
    topics,
    totalQuestions: questions.length,
    correctCount: 0,
    skippedCount: 0,
    startTime: Date.now(),
    endTime: null,
    questions: [],
    byCategory: {}
  };

  // Initialize category tracking
  for (const topicId of topics) {
    results.byCategory[topicId] = { correct: 0, total: 0, name: TOPICS[topicId] };
  }

  console.log(chalk.gray('\n' + '-'.repeat(60)));
  if (isRetry) {
    console.log(chalk.yellow(`Retrying ${questions.length} missed questions...`));
  } else {
    console.log(chalk.yellow(`Starting quiz: ${questions.length} questions for ${profile} profile`));
  }
  console.log(chalk.gray('-'.repeat(60)));

  // Quiz loop
  for (let i = 0; i < questions.length; i++) {
    const question = questions[i];
    const categoryName = question.category || TOPICS[question.category_id] || 'Unknown';

    // Display question
    displayQuestion(question, i, questions.length, categoryName);

    // Get answer
    const answer = await promptAnswer();

    // Handle special inputs
    if (answer === 'quit') {
      console.log(chalk.yellow('\nQuiz ended early.'));
      break;
    }

    if (answer === 'skip') {
      results.skippedCount++;
      results.questions.push({
        question,
        userAnswer: null,
        correct: false,
        skipped: true
      });
      if (results.byCategory[question.category_id]) {
        results.byCategory[question.category_id].total++;
      }
      continue;
    }

    // Validate answer
    const isCorrect = answer === question.correct.toLowerCase();

    // Update results
    if (isCorrect) {
      results.correctCount++;
      displayCorrect();
    } else {
      displayIncorrect(question, answer);
    }

    results.questions.push({
      question,
      userAnswer: answer,
      correct: isCorrect,
      skipped: false
    });

    // Update category stats
    if (results.byCategory[question.category_id]) {
      results.byCategory[question.category_id].total++;
      if (isCorrect) {
        results.byCategory[question.category_id].correct++;
      }
    }

    // Show progress
    displayProgress(i + 1, questions.length, results.correctCount);

    // Prompt to continue (only on wrong answers to give time to read)
    if (!isCorrect && i < questions.length - 1) {
      await promptContinue();
    }
  }

  results.endTime = Date.now();
  return results;
}
