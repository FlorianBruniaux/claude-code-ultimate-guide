/**
 * Question loading and filtering
 */

import { readdir, readFile } from 'fs/promises';
import { join } from 'path';
import YAML from 'yaml';

/**
 * Load all questions from YAML files in the questions directory
 */
export async function loadQuestions(questionsDir) {
  const allQuestions = [];

  try {
    const files = await readdir(questionsDir);
    const yamlFiles = files.filter(f => f.endsWith('.yaml') || f.endsWith('.yml'));

    for (const file of yamlFiles) {
      try {
        const content = await readFile(join(questionsDir, file), 'utf-8');
        const parsed = YAML.parse(content);

        if (parsed && parsed.questions && Array.isArray(parsed.questions)) {
          // Add category info to each question
          const questionsWithCategory = parsed.questions.map(q => ({
            ...q,
            category: parsed.category || 'Unknown',
            category_id: parsed.category_id || 0,
            source_file: parsed.source_file || 'guide/ultimate-guide.md'
          }));
          allQuestions.push(...questionsWithCategory);
        }
      } catch (err) {
        console.warn(`Warning: Could not parse ${file}: ${err.message}`);
      }
    }
  } catch (err) {
    console.error(`Error reading questions directory: ${err.message}`);
  }

  return allQuestions;
}

/**
 * Filter questions based on profile, topics, and difficulty
 */
export function filterQuestions(questions, options) {
  const { profile, topics, count, difficultyWeight } = options;

  // Filter by topics
  let filtered = questions.filter(q => topics.includes(q.category_id));

  // Filter by profile (if profiles array exists on question)
  filtered = filtered.filter(q => {
    if (!q.profiles || !Array.isArray(q.profiles)) return true;
    return q.profiles.includes(profile);
  });

  // Weight by difficulty
  if (difficultyWeight) {
    filtered = weightByDifficulty(filtered, difficultyWeight, count);
  }

  return filtered;
}

/**
 * Select a quiz set, preferring questions that were not in the previous set.
 */
export function selectQuestions(questions, options, excludedQuestionIds = new Set()) {
  const availableQuestions = excludedQuestionIds.size > 0
    ? questions.filter(question => !excludedQuestionIds.has(question.id))
    : questions;
  const selectedQuestions = filterQuestions(availableQuestions, options);

  if (selectedQuestions.length < options.count && excludedQuestionIds.size > 0) {
    return shuffleArray(filterQuestions(questions, options)).slice(0, options.count);
  }

  return shuffleArray(selectedQuestions).slice(0, options.count);
}

/**
 * Weight questions by difficulty distribution
 */
function weightByDifficulty(questions, weights, targetCount) {
  const byDifficulty = {
    junior: questions.filter(q => q.difficulty === 'junior'),
    senior: questions.filter(q => q.difficulty === 'senior'),
    power: questions.filter(q => q.difficulty === 'power'),
    all: questions.filter(q => q.difficulty === 'all' || !q.difficulty)
  };

  const result = [];

  // Add 'all' difficulty questions first
  result.push(...byDifficulty.all);

  // Calculate target counts for each difficulty
  const remaining = targetCount - result.length;
  const juniorCount = Math.floor(remaining * (weights.junior || 0));
  const seniorCount = Math.floor(remaining * (weights.senior || 0));
  const powerCount = Math.floor(remaining * (weights.power || 0));

  // Add questions by difficulty
  result.push(...shuffleArray(byDifficulty.junior).slice(0, juniorCount));
  result.push(...shuffleArray(byDifficulty.senior).slice(0, seniorCount));
  result.push(...shuffleArray(byDifficulty.power).slice(0, powerCount));

  // Fill remaining slots with any available questions
  const used = new Set(result.map(q => q.id));
  const unused = questions.filter(q => !used.has(q.id));
  const stillNeeded = targetCount - result.length;

  if (stillNeeded > 0) {
    result.push(...shuffleArray(unused).slice(0, stillNeeded));
  }

  return result;
}

/**
 * Shuffle array using Fisher-Yates algorithm
 */
export function shuffleArray(array) {
  const result = [...array];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Get category name from ID
 */
export function getCategoryName(categoryId, topics) {
  return topics[categoryId] || 'Unknown';
}
