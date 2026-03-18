#!/bin/bash
# compile-questions.sh — Compile quiz YAML files into landing questions.json
# Usage: ./scripts/compile-questions.sh
#
# Reads all quiz/questions/*.yaml, merges into a single JSON with categories + questions.
# Output: $LANDING_DIR/questions.json
set -euo pipefail

GUIDE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LANDING_DIR="/Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing"
YAML_DIR="$GUIDE_DIR/quiz/questions"
NODE_PATH="$GUIDE_DIR/quiz/node_modules"
OUTPUT="$LANDING_DIR/questions.json"

if [ ! -d "$YAML_DIR" ]; then
  echo "ERROR: Quiz directory not found: $YAML_DIR" >&2
  exit 1
fi

if [ ! -d "$NODE_PATH/yaml" ]; then
  echo "ERROR: yaml module not found in $NODE_PATH" >&2
  echo "Run: cd quiz && npm install yaml" >&2
  exit 1
fi

NODE_PATH="$NODE_PATH" node -e "
const fs = require('fs');
const path = require('path');
const YAML = require('yaml');

const yamlDir = process.argv[1];
const files = fs.readdirSync(yamlDir)
  .filter(f => f.endsWith('.yaml'))
  .sort();

const categories = [];
const questions = [];

for (const file of files) {
  const content = fs.readFileSync(path.join(yamlDir, file), 'utf8');
  const data = YAML.parse(content);

  if (!data.category || !data.category_id || !data.questions) {
    console.error('Invalid YAML structure in ' + file);
    process.exit(1);
  }

  categories.push({ id: data.category_id, name: data.category });

  for (const q of data.questions) {
    questions.push({
      id: q.id,
      difficulty: q.difficulty,
      profiles: q.profiles,
      category_id: data.category_id,
      question: q.question,
      options: q.options,
      correct: q.correct,
      explanation: q.explanation,
      doc_reference: q.doc_reference
    });
  }
}

const output = JSON.stringify({ categories, questions }, null, 2);
fs.writeFileSync(process.argv[2], output + '\n');
console.log(questions.length + ' questions compiled (' + files.length + ' categories)');
" "$YAML_DIR" "$OUTPUT"
