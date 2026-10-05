import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import chapterMap from './chapter-ranges.generated.json';

const GITHUB_BASE = 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main';
const GUIDE_SITE_BASE = 'https://cc.bruniaux.com/guide/ultimate-guide';

// The bundle routes its own reference snapshot without accessing a guide repository.
// GUIDE_ROOT is checked once at module initialization. If local files diverge,
// callers retain the guide-root link instead of receiving a guessed chapter.
let matchesSnapshot = true;
if (process.env.GUIDE_ROOT) {
  try {
    const root = resolve(process.env.GUIDE_ROOT);
    const hashFile = (path: string) => createHash('sha256').update(readFileSync(path)).digest('hex');
    matchesSnapshot = hashFile(resolve(root, 'guide/ultimate-guide.md')) === chapterMap.sourceSha256
      && hashFile(resolve(root, 'machine-readable/reference.yaml')) === chapterMap.referenceSha256;
  } catch { matchesSnapshot = false; }
}

function lineToChapterSlug(line: number): string | null {
  if (!matchesSnapshot || !Number.isInteger(line) || line < 1 || line > chapterMap.lineCount) return null;
  return chapterMap.ranges.find(range => line >= range.from && line <= range.to)?.slug ?? null;
}

export function githubUrl(filePath: string, line?: number): string {
  const base = `${GITHUB_BASE}/${filePath}`;
  return line ? `${base}#L${line}` : base;
}

// Only ultimate-guide.md is rendered as multi-chapter on the guide site
export function guideSiteUrl(filePath: string, line?: number): string | null {
  if (filePath !== 'guide/ultimate-guide.md') return null;
  if (!line) return `${GUIDE_SITE_BASE}/`;
  const chapterSlug = lineToChapterSlug(line);
  return chapterSlug ? `${GUIDE_SITE_BASE}/${chapterSlug}/` : `${GUIDE_SITE_BASE}/`;
}

export function formatLinks(filePath: string, line?: number): string {
  const gh = githubUrl(filePath, line);
  const site = guideSiteUrl(filePath, line);
  const parts = [`GitHub: ${gh}`];
  if (site) parts.push(`Guide: ${site}`);
  return parts.join(' | ');
}
