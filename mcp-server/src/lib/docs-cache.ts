import { createHash } from 'crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'fs';
import { homedir } from 'os';
import { resolve } from 'path';

const ANTHROPIC_DOCS_URL = 'https://code.claude.com/docs/llms-full.txt';
// Stable path — NOT versioned, survives package upgrades
const SNAPSHOT_DIR = resolve(homedir(), '.cache', 'claude-code-guide');

// ── Types ──────────────────────────────────────────────────────────────────

export interface SectionMeta {
  slug: string;
  title: string;
  sourceUrl: string;
  hash: string;
  lineCount: number;
  charCount: number;
}

export interface IndexFile {
  schemaVersion: 1;
  fetchedAt: string;
  contentHash: string;
  sectionCount: number;
  sections: Record<string, SectionMeta>;
}

export interface ContentFile {
  schemaVersion: 1;
  sections: Record<string, { content: string }>;
}

export type SnapshotType = 'baseline' | 'current';

// ── Paths ──────────────────────────────────────────────────────────────────

export function getSnapshotDir(): string {
  return SNAPSHOT_DIR;
}

function indexPath(type: SnapshotType): string {
  return resolve(SNAPSHOT_DIR, `anthropic-docs-${type}-index.json`);
}

function contentPath(type: SnapshotType): string {
  return resolve(SNAPSHOT_DIR, `anthropic-docs-${type}-content.json`);
}

// ── Fetch ──────────────────────────────────────────────────────────────────

export async function fetchOfficialDocs(): Promise<string> {
  const response = await fetch(ANTHROPIC_DOCS_URL, {
    headers: { 'User-Agent': 'claude-code-ultimate-guide-mcp/1.1.0' },
    signal: AbortSignal.timeout(15_000),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} fetching ${ANTHROPIC_DOCS_URL}`);
  }

  const text = await response.text();

  if (text.length < 500_000) {
    throw new Error(
      `Response looks malformed (got ${(text.length / 1024).toFixed(0)}KB, expected >500KB). The URL format may have changed.`,
    );
  }

  return text;
}

// ── Parsing ────────────────────────────────────────────────────────────────

export function parseIntoSections(raw: string): { index: IndexFile; content: ContentFile } {
  const lines = raw.split('\n');
  const sections: Record<string, SectionMeta> = {};
  const contents: Record<string, { content: string }> = {};

  // Tracking state for the current section being built
  let currentSlug: string | null = null;
  let currentTitle: string | null = null;
  let currentSourceUrl: string | null = null;
  let currentStartLine = 0;

  // Title candidate (# H1) waiting to be confirmed by a Source: line
  let titleCandidate: string | null = null;
  let titleCandidateLine = -1;

  const flushSection = (endLine: number) => {
    if (!currentSlug || !currentTitle || !currentSourceUrl) return;
    const sectionLines = lines.slice(currentStartLine, endLine);
    const content = sectionLines.join('\n').trimEnd();
    if (content.length === 0) return;
    const hash = createHash('sha256').update(content).digest('hex').slice(0, 16);
    sections[currentSlug] = {
      slug: currentSlug,
      title: currentTitle,
      sourceUrl: currentSourceUrl,
      hash,
      lineCount: sectionLines.length,
      charCount: content.length,
    };
    contents[currentSlug] = { content };
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detect H1 title (# Title, but not ##+ headings)
    if (line.startsWith('# ') && !line.startsWith('## ')) {
      titleCandidate = line;
      titleCandidateLine = i;
      continue;
    }

    // Detect Source: URL immediately after H1 (line N+1 rule)
    const sourceMatch = line.match(
      /^Source:\s+(https:\/\/code\.claude\.com\/docs\/(?:en\/)?([a-zA-Z0-9-]+))\s*$/,
    );
    if (sourceMatch && titleCandidate !== null && i === titleCandidateLine + 1) {
      const sourceUrl = sourceMatch[1];
      const slug = sourceMatch[2];

      // Flush the previous section up to the start of this new one
      flushSection(titleCandidateLine);

      currentSlug = slug;
      currentTitle = titleCandidate;
      currentSourceUrl = sourceUrl;
      currentStartLine = titleCandidateLine;
      titleCandidate = null;
      titleCandidateLine = -1;
      continue;
    }

    // Reset title candidate if not immediately followed by Source:
    if (titleCandidate !== null && i > titleCandidateLine + 1) {
      titleCandidate = null;
      titleCandidateLine = -1;
    }
  }

  // Flush the last section
  flushSection(lines.length);

  if (Object.keys(sections).length === 0) {
    throw new Error(
      'Section parser found 0 sections — llms-full.txt format may have changed. ' +
        'Please open an issue at https://github.com/FlorianBruniaux/claude-code-ultimate-guide',
    );
  }

  const contentHash = createHash('sha256').update(raw).digest('hex').slice(0, 16);

  const index: IndexFile = {
    schemaVersion: 1,
    fetchedAt: new Date().toISOString(),
    contentHash,
    sectionCount: Object.keys(sections).length,
    sections,
  };

  const content: ContentFile = {
    schemaVersion: 1,
    sections: contents,
  };

  return { index, content };
}

// ── Save / Load ────────────────────────────────────────────────────────────

export function saveSnapshot(type: SnapshotType, index: IndexFile, content: ContentFile): void {
  mkdirSync(SNAPSHOT_DIR, { recursive: true });

  // Atomic write: write to .tmp then rename to final path
  const iPath = indexPath(type);
  writeFileSync(`${iPath}.tmp`, JSON.stringify(index, null, 2), 'utf8');
  renameSync(`${iPath}.tmp`, iPath);

  const cPath = contentPath(type);
  writeFileSync(`${cPath}.tmp`, JSON.stringify(content, null, 2), 'utf8');
  renameSync(`${cPath}.tmp`, cPath);
}

export function loadIndex(type: SnapshotType): IndexFile | null {
  const path = indexPath(type);
  if (!existsSync(path)) return null;
  try {
    const data = JSON.parse(readFileSync(path, 'utf8')) as IndexFile;
    if (data.schemaVersion !== 1) return null;
    return data;
  } catch {
    return null;
  }
}

/** Load only the specified sections from the content file — never loads everything into memory */
export function loadSections(
  type: SnapshotType,
  slugs: string[],
): Record<string, string> {
  const path = contentPath(type);
  if (!existsSync(path)) return {};
  try {
    const data = JSON.parse(readFileSync(path, 'utf8')) as ContentFile;
    const result: Record<string, string> = {};
    for (const slug of slugs) {
      const section = data.sections[slug];
      if (section) result[slug] = section.content;
    }
    return result;
  } catch {
    return {};
  }
}

export function snapshotAgeDays(index: IndexFile): number {
  return Math.floor((Date.now() - new Date(index.fetchedAt).getTime()) / (1000 * 60 * 60 * 24));
}
