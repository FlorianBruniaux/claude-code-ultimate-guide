#!/usr/bin/env node
/**
 * generate-from-web.mjs
 *
 * One-way generator: canonical web quiz bank -> CLI YAML bundles.
 *
 * The web bank (Astro content collection, one Markdown file per question) is the
 * single source of truth. This script reads it and rewrites quiz/questions/*.yaml
 * so the CLI quiz holds the same questions in its native per-category YAML format.
 *
 * It never hand-merges. It replaces the `questions` array of each category and
 * preserves that category's existing header (category name + source_file), which
 * is CLI-side display metadata.
 *
 * Usage:
 *   node quiz/scripts/generate-from-web.mjs [--web <dir>] [--out <dir>] [--check]
 *
 *   --web <dir>   Path to the web questions dir.
 *                 Default: ../claude-code-ultimate-guide-landing/src/content/questions
 *                 (resolved relative to this repo root).
 *   --out <dir>   Where to write YAML. Default: quiz/questions (in place).
 *   --check       Dry run. Write nowhere, just report what would change and exit
 *                 non-zero if anything differs. Use in CI to detect drift.
 */

import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
import YAML from 'yaml';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..'); // claude-code-ultimate-guide/
const CLI_QUESTIONS_DIR = path.join(REPO_ROOT, 'quiz', 'questions');

function parseArgs(argv) {
  const args = { web: null, out: CLI_QUESTIONS_DIR, check: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--web') args.web = argv[++i];
    else if (argv[i] === '--out') args.out = argv[++i];
    else if (argv[i] === '--check') args.check = true;
  }
  if (!args.web) {
    args.web = path.resolve(REPO_ROOT, '..', 'claude-code-ultimate-guide-landing', 'src', 'content', 'questions');
  }
  return args;
}

// Read one web Markdown question: frontmatter + "question\n---\nexplanation" body.
function readWebQuestion(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) throw new Error(`No frontmatter: ${file}`);
  const fm = YAML.parse(m[1]);
  const parts = m[2].split(/\n---\n/);
  const question = parts[0].trim();
  const explanation = parts.slice(1).join('\n---\n').trim();
  return { fm, question, explanation, file };
}

// Load every web question, grouped by category_id.
function loadWeb(webDir) {
  const byCat = new Map();
  for (const cat of fs.readdirSync(webDir)) {
    const cdir = path.join(webDir, cat);
    if (!fs.statSync(cdir).isDirectory()) continue;
    for (const f of fs.readdirSync(cdir)) {
      if (!f.endsWith('.md') || /readme|index/i.test(f)) continue;
      const q = readWebQuestion(path.join(cdir, f));
      const cid = q.fm.category_id;
      if (!byCat.has(cid)) byCat.set(cid, []);
      byCat.get(cid).push(q);
    }
  }
  return byCat;
}

// Build the CLI-side shell (filename, category name, source_file) from existing YAML.
function loadCliShells(dir) {
  const shells = new Map(); // category_id -> { filename, category, source_file }
  for (const f of fs.readdirSync(dir)) {
    if (!/\.ya?ml$/.test(f)) continue;
    const doc = YAML.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    shells.set(doc.category_id, {
      filename: f,
      category: doc.category,
      source_file: doc.source_file,
    });
  }
  return shells;
}

// Convert one web question to the CLI question shape (native field order, no
// web-only fields like official_doc or roles).
function toCliQuestion(w) {
  const fm = w.fm;
  const out = {
    id: String(fm.id),
    difficulty: fm.difficulty,
    profiles: fm.profiles,
    question: w.question,
    options: {
      a: fm.options.a,
      b: fm.options.b,
      c: fm.options.c,
      d: fm.options.d,
    },
    correct: String(fm.correct),
    explanation: w.explanation,
  };
  if (fm.doc_reference) {
    const dr = fm.doc_reference;
    // Preserve whatever locator the web bank uses: anchor and/or line. Some
    // questions carry `anchor: "#..."`, others carry `line: 753-761`.
    out.doc_reference = { file: dr.file, section: dr.section };
    if (dr.anchor != null) out.doc_reference.anchor = dr.anchor;
    if (dr.line != null) out.doc_reference.line = dr.line;
  }
  return out;
}

function categorySourceFile(questions, fallback) {
  // Most common doc_reference.file among the category's questions.
  const counts = new Map();
  for (const q of questions) {
    const f = q.fm.doc_reference?.file;
    if (f) counts.set(f, (counts.get(f) || 0) + 1);
  }
  let best = fallback, bestN = 0;
  for (const [f, n] of counts) if (n > bestN) { best = f; bestN = n; }
  return best || fallback;
}

function stringifyCategory(shell, cliQuestions) {
  const doc = {
    category: shell.category,
    category_id: shell.category_id,
    source_file: shell.source_file,
    questions: cliQuestions,
  };
  // No line wrapping (stable diffs), block literal for multi-line explanations.
  // Let the lib pick scalar styles otherwise; it quotes numeric-looking strings
  // like "0" so options never collapse to numbers.
  return YAML.stringify(doc, {
    lineWidth: 0,
    blockQuote: 'literal',
  });
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(args.web)) {
    console.error(`Web questions dir not found: ${args.web}`);
    console.error('Pass --web <dir> pointing at the landing repo src/content/questions.');
    process.exit(2);
  }

  const byCat = loadWeb(args.web);
  const shells = loadCliShells(CLI_QUESTIONS_DIR);
  if (!args.check && args.out !== CLI_QUESTIONS_DIR) {
    fs.mkdirSync(args.out, { recursive: true });
  }

  const catIds = [...byCat.keys()].sort((a, b) => a - b);
  let changed = 0;
  const summary = [];

  for (const cid of catIds) {
    const questions = byCat.get(cid).sort((a, b) => String(a.fm.id).localeCompare(String(b.fm.id)));
    const shell = shells.get(cid);
    if (!shell) {
      console.error(`No CLI shell for category_id ${cid}. Add a header (category name + source_file) to a new quiz/questions/ file first.`);
      process.exit(3);
    }
    const resolved = {
      category_id: cid,
      category: shell.category,
      source_file: categorySourceFile(questions, shell.source_file),
    };
    const cliQuestions = questions.map(toCliQuestion);
    const yamlText = stringifyCategory(resolved, cliQuestions);

    const outPath = path.join(args.out, shell.filename);
    const prev = fs.existsSync(outPath) ? fs.readFileSync(outPath, 'utf8') : '';
    const isDiff = prev !== yamlText;
    if (isDiff) changed++;
    summary.push(`  cat ${String(cid).padStart(2, '0')} ${shell.filename}: ${cliQuestions.length} questions${isDiff ? ' (changed)' : ''}`);

    if (!args.check) fs.writeFileSync(outPath, yamlText);
  }

  console.log(`Generated ${catIds.length} categories from ${args.web}`);
  console.log(summary.join('\n'));

  if (args.check) {
    if (changed > 0) {
      console.error(`\n${changed} category file(s) would change. CLI YAML is out of sync with the web bank. Run without --check to regenerate.`);
      process.exit(1);
    }
    console.log('\nCLI YAML is in sync with the web bank.');
  } else {
    console.log(`\nWrote ${catIds.length} files to ${args.out} (${changed} changed).`);
  }
}

main();
