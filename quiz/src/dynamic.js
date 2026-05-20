/**
 * Dynamic question generation using claude -p
 */

import { execFileSync } from 'child_process';
import YAML from 'yaml';

const TOPICS = {
  1: 'Quick Start & Installation',
  2: 'Core Concepts',
  3: 'Memory & Settings',
  4: 'Agents',
  5: 'Skills',
  6: 'Commands',
  7: 'Hooks',
  8: 'MCP Servers',
  9: 'Advanced Patterns',
  10: 'Reference & Troubleshooting'
};

const TOPIC_SECTIONS = {
  1: '1.1-1.6',
  2: '2.1-2.6',
  3: '3.1-3.4',
  4: '4.1-4.5',
  5: '5.1-5.4',
  6: '6.1-6.4',
  7: '7.1-7.5',
  8: '8.1-8.5',
  9: '9.1-9.5',
  10: '10.1-10.6'
};

/**
 * Generate a question dynamically using claude -p
 */
export async function generateDynamicQuestion(categoryId, difficulty = 'senior') {
  const categoryName = TOPICS[categoryId] || 'Claude Code';
  const sections = TOPIC_SECTIONS[categoryId] || '';

  const prompt = `Based on the Claude Code documentation section "${categoryName}" (sections ${sections}), generate a multiple-choice question at ${difficulty} difficulty level.

Output format (YAML only, no explanation):
\`\`\`yaml
id: "dyn-${Date.now()}"
difficulty: "${difficulty}"
profiles: ["junior", "senior", "power"]
question: "Your question here?"
options:
  a: "First option"
  b: "Second option"
  c: "Third option"
  d: "Fourth option"
correct: "a"
explanation: |
  Explanation of why this is correct and what the user should learn.
doc_reference:
  file: "guide/ultimate-guide.md"
  section: "${categoryName}"
  anchor: "#${categoryId}-${categoryName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}"
\`\`\`

Requirements:
- Test practical understanding, not trivia
- Include one clearly correct answer
- Make distractors plausible but distinguishable
- Explanation should teach, not just state the answer
- Question should be answerable from the documentation`;

  try {
    // Check if claude CLI is available
    const result = execFileSync('claude', ['-p', prompt, '--model', 'haiku'], {
      encoding: 'utf-8',
      timeout: 30000,
      maxBuffer: 1024 * 1024
    });

    // Extract YAML from response
    const yamlMatch = result.match(/```yaml\n([\s\S]*?)```/);
    if (!yamlMatch) {
      throw new Error('No YAML block found in response');
    }

    const question = YAML.parse(yamlMatch[1]);

    // Validate question structure
    if (!question.question || !question.options || !question.correct) {
      throw new Error('Invalid question structure');
    }

    // Add category info
    question.category = categoryName;
    question.category_id = categoryId;
    question.source_file = 'guide/ultimate-guide.md';
    question.generated = true;

    return question;
  } catch (err) {
    console.error('Dynamic generation failed:', err.message);
    return null;
  }
}

/**
 * Check if claude CLI is available
 */
export function isClaudeAvailable() {
  try {
    execSync('which claude', { encoding: 'utf-8' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Generate multiple questions for a category
 */
export async function generateQuestions(categoryId, count = 5, difficulty = 'senior') {
  const questions = [];

  for (let i = 0; i < count; i++) {
    const question = await generateDynamicQuestion(categoryId, difficulty);
    if (question) {
      questions.push(question);
    }
    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  return questions;
}
