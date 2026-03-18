import type { IndexFile } from './docs-cache.js';

// ── Types ──────────────────────────────────────────────────────────────────

export interface SectionDiff {
  slug: string;
  title: string;
  sourceUrl: string;
  kind: 'added' | 'removed' | 'modified';
  // Only for 'modified'
  linesBefore?: number;
  linesAfter?: number;
  charsBefore?: number;
  charsAfter?: number;
  lineDelta?: number;
  firstChangedLine?: string;
}

export interface DiffResult {
  unchanged: number;
  added: SectionDiff[];
  removed: SectionDiff[];
  modified: SectionDiff[];
  baselineDate: string;
  currentDate: string;
}

// ── Diff engine (pure — no I/O, no network) ────────────────────────────────

export function diffSnapshots(baseline: IndexFile, current: IndexFile): DiffResult {
  const baselineSlugs = new Set(Object.keys(baseline.sections));
  const currentSlugs = new Set(Object.keys(current.sections));

  const added: SectionDiff[] = [];
  const removed: SectionDiff[] = [];
  const modified: SectionDiff[] = [];
  let unchanged = 0;

  for (const slug of currentSlugs) {
    if (!baselineSlugs.has(slug)) {
      const s = current.sections[slug];
      added.push({ slug, title: s.title, sourceUrl: s.sourceUrl, kind: 'added' });
    }
  }

  for (const slug of baselineSlugs) {
    if (!currentSlugs.has(slug)) {
      const s = baseline.sections[slug];
      removed.push({ slug, title: s.title, sourceUrl: s.sourceUrl, kind: 'removed' });
    }
  }

  for (const slug of baselineSlugs) {
    if (!currentSlugs.has(slug)) continue;
    const base = baseline.sections[slug];
    const curr = current.sections[slug];

    if (base.hash === curr.hash) {
      unchanged++;
      continue;
    }

    modified.push({
      slug,
      title: curr.title,
      sourceUrl: curr.sourceUrl,
      kind: 'modified',
      linesBefore: base.lineCount,
      linesAfter: curr.lineCount,
      charsBefore: base.charCount,
      charsAfter: curr.charCount,
      lineDelta: curr.lineCount - base.lineCount,
      // firstChangedLine is enriched by the tool layer after loading content
    });
  }

  return {
    unchanged,
    added,
    removed,
    modified,
    baselineDate: baseline.fetchedAt,
    currentDate: current.fetchedAt,
  };
}

/** Find the first line that differs between two content strings. Returns truncated to 120 chars. */
export function findFirstChangedLine(baseContent: string, currentContent: string): string {
  const baseLines = baseContent.split('\n');
  const currLines = currentContent.split('\n');
  const len = Math.min(baseLines.length, currLines.length);

  for (let i = 0; i < len; i++) {
    if (baseLines[i] !== currLines[i]) {
      return currLines[i].slice(0, 120);
    }
  }

  // One side is longer — the first extra line is the change
  if (currLines.length > baseLines.length) {
    return (currLines[baseLines.length] ?? '').slice(0, 120);
  }

  return '';
}
