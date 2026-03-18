import { readFileSync, existsSync } from 'fs';
import { resolveContentPath, isDevMode } from './content.js';
import { fetchFile } from './fetcher.js';

export interface SectionResult {
  content: string;
  startLine: number;
  endLine: number;
  totalLines: number;
  hasMore: boolean;
  nextOffset: number | null;
}

const MAX_LINES = 500;

// ─── Heading level detector ───────────────────────────────────────────────────

function getHeadingLevel(line: string): number | null {
  const match = line.match(/^(#{1,6})\s/);
  return match ? match[1].length : null;
}

// ─── Section extraction ───────────────────────────────────────────────────────

export function extractSection(
  lines: string[],
  offset: number,
  limit: number,
): SectionResult {
  const totalLines = lines.length;
  const startLine = Math.max(1, Math.min(offset, totalLines));
  const effectiveLimit = Math.min(limit, MAX_LINES);

  // Find heading level of starting section (for boundary detection)
  let sectionLevel: number | null = null;
  for (let i = startLine - 1; i < Math.min(startLine + 5, totalLines); i++) {
    const level = getHeadingLevel(lines[i]);
    if (level !== null) {
      sectionLevel = level;
      break;
    }
  }

  let inCodeFence = false;
  let endLine = startLine - 1;
  const collected: string[] = [];

  for (let i = startLine - 1; i < totalLines && collected.length < effectiveLimit; i++) {
    const line = lines[i];

    // Track code fences
    if (line.trimStart().startsWith('```')) {
      inCodeFence = !inCodeFence;
    }

    // Check heading boundary (only outside code fences, only same/higher level)
    if (!inCodeFence && i > startLine - 1 && sectionLevel !== null) {
      const level = getHeadingLevel(line);
      if (level !== null && level <= sectionLevel) {
        break; // Stop at same or higher heading
      }
    }

    collected.push(line);
    endLine = i + 1;
  }

  const hasMore = endLine < totalLines && collected.length >= effectiveLimit;

  return {
    content: collected.join('\n'),
    startLine,
    endLine,
    totalLines,
    hasMore,
    nextOffset: hasMore ? endLine + 1 : null,
  };
}

// ─── Public API ───────────────────────────────────────────────────────────────

export async function readSection(
  filePath: string,
  offset = 1,
  limit = MAX_LINES,
): Promise<SectionResult | null> {
  let content: string | null = null;

  if (isDevMode()) {
    // Dev mode: read from local filesystem
    const resolved = resolveContentPath(filePath);
    if (!resolved || !existsSync(resolved)) return null;
    content = readFileSync(resolved, 'utf8');
  } else {
    // Production: fetch from GitHub (with cache)
    content = await fetchFile(filePath);
  }

  if (content === null) return null;

  const lines = content.split('\n');
  return extractSection(lines, offset, limit);
}
