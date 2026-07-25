/**
 * UI utilities for terminal display
 */

import chalk from 'chalk';
import { TOPICS } from './topics.js';

export function displayHeader() {
  console.log(chalk.cyan('\n' + '='.repeat(60)));
  console.log(chalk.cyan.bold('   CLAUDE CODE KNOWLEDGE QUIZ'));
  console.log(chalk.gray('   Master Claude Code: The Complete Guide'));
  console.log(chalk.cyan('='.repeat(60) + '\n'));
}

export function displayHelp() {
  console.log(`
${chalk.cyan.bold('Claude Code Knowledge Quiz')}
Test your understanding of Claude Code with interactive MCQs.

${chalk.yellow('Usage:')}
  npx claude-code-quiz [options]
  node quiz/src/index.js [options]

${chalk.yellow('Options:')}
  -p, --profile <type>   Pre-select profile (junior|senior|power|pm)
  -t, --topics <list>    Quiz specific sections (1-17, comma-separated)
  -c, --count <n>        Limit number of questions (1-50)
  -d, --dynamic          Enable dynamic question generation via claude -p
  -h, --help             Show this help message
  -v, --version          Show version

${chalk.yellow('Profiles:')}
  junior   Junior Developer (15 questions, sections 1-3, 6)
  senior   Senior Developer (20 questions, sections 2-4, 7, 9)
  power    Power User (25 questions, all sections)
  pm       Product Manager (10 questions, sections 1-3, 16-17)

${chalk.yellow('Topics:')}
${Object.entries(TOPICS).map(([id, name]) => `  ${id.padStart(2)} ${name}`).join('\n')}

${chalk.yellow('Examples:')}
  npx claude-code-quiz                      # Interactive mode
  npx claude-code-quiz -p senior            # Senior profile, default topics
  npx claude-code-quiz -p power -t 4,7,8    # Power user, specific topics
  npx claude-code-quiz -c 10                # Quick 10-question quiz

${chalk.gray('Part of: https://github.com/FlorianBruniaux/claude-code-ultimate-guide')}
`);
}

export function displayQuestion(question, index, total, categoryName) {
  console.log(chalk.gray('\n' + '-'.repeat(60)));
  console.log(chalk.yellow(`Question ${index + 1}/${total}`) + chalk.gray(` [${categoryName}]`));
  console.log();
  console.log(chalk.white.bold(question.question));
  console.log();

  const options = ['A', 'B', 'C', 'D'];
  Object.entries(question.options).forEach(([key, value], i) => {
    console.log(chalk.cyan(`  ${options[i]}) `) + value);
  });
  console.log();
}

export function displayCorrect() {
  console.log(chalk.green.bold('\n✓ CORRECT!\n'));
}

export function displayIncorrect(question, userAnswer) {
  const options = ['a', 'b', 'c', 'd'];
  const correctLetter = question.correct.toUpperCase();
  const correctText = question.options[question.correct];

  console.log(chalk.red.bold(`\n✗ INCORRECT.`) + chalk.white(` The correct answer is ${chalk.green(correctLetter)}) ${correctText}`));
  console.log();
  console.log(chalk.yellow('Explanation:'));
  console.log(chalk.gray(question.explanation.trim()));
  console.log();

  if (question.doc_reference) {
    const ref = question.doc_reference;
    const githubUrl = `https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/${ref.file}${ref.anchor || ''}`;
    console.log(chalk.blue('See: ') + chalk.underline(githubUrl));
    if (ref.line) {
      console.log(chalk.gray(`     (Line ${ref.line})`));
    }
  }
  console.log();
}

export function displayProgress(current, total, correct) {
  const percentage = Math.round((correct / current) * 100) || 0;
  const progressBar = createProgressBar(current, total, 20);
  console.log(chalk.gray(`Progress: ${progressBar} ${current}/${total} | Score: ${correct}/${current} (${percentage}%)`));
}

function createProgressBar(current, total, width) {
  const filled = Math.round((current / total) * width);
  const empty = width - filled;
  return chalk.green('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));
}

export function displayCategoryScore(categoryName, correct, total) {
  const percentage = Math.round((correct / total) * 100);
  const barWidth = 10;
  const filled = Math.round((percentage / 100) * barWidth);
  const bar = chalk.green('█'.repeat(filled)) + chalk.gray('░'.repeat(barWidth - filled));

  let color = chalk.green;
  if (percentage < 50) color = chalk.red;
  else if (percentage < 75) color = chalk.yellow;

  return `  ${categoryName.padEnd(30)} ${correct}/${total}  ${color(`(${percentage}%)`)}  [${bar}]`;
}
