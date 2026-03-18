import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import {
  fetchOfficialDocs,
  parseIntoSections,
  saveSnapshot,
  loadIndex,
  loadSections,
  snapshotAgeDays,
  getSnapshotDir,
} from '../lib/docs-cache.js';
import { diffSnapshots, findFirstChangedLine } from '../lib/docs-diff.js';

const STALENESS_WARN_DAYS = 30;

// ── Helpers ────────────────────────────────────────────────────────────────

function formatDate(iso: string): string {
  return iso.slice(0, 10); // YYYY-MM-DD
}

function formatSize(bytes: number): string {
  if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(2)} MB`;
  return `${(bytes / 1024).toFixed(0)} KB`;
}

/** Extract a ~300-char excerpt from content around the first match of query. */
function extractExcerpt(content: string, query: string, maxLen = 300): string {
  const lowerContent = content.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const idx = lowerContent.indexOf(lowerQuery);

  if (idx === -1) {
    // No match in body — return opening
    const excerpt = content.slice(0, maxLen);
    return excerpt + (content.length > maxLen ? '…' : '');
  }

  const start = Math.max(0, idx - 100);
  const end = Math.min(content.length, idx + query.length + 200);
  const prefix = start > 0 ? '…' : '';
  const suffix = end < content.length ? '…' : '';
  return prefix + content.slice(start, end) + suffix;
}

/** Score a section for a query. Title matches count ×3, body match ×1. */
function scoreSection(title: string, content: string, query: string): number {
  const q = query.toLowerCase();
  const titleScore = title.toLowerCase().includes(q) ? 3 : 0;
  const bodyScore = content.toLowerCase().includes(q) ? 1 : 0;
  return titleScore + bodyScore;
}

// ── Tool registration ──────────────────────────────────────────────────────

export function registerOfficialDocs(server: McpServer): void {

  // ── init_official_docs ──────────────────────────────────────────────────
  server.tool(
    'init_official_docs',
    'Fetch the official Anthropic Claude Code docs (llms-full.txt) and store a local snapshot as the diff baseline. Run this first. Safe to re-run — overwrites previous baseline AND current. Takes ~5s (fetches ~1.2MB from Anthropic).',
    {},
    { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    async () => {
      let raw: string;
      try {
        raw = await fetchOfficialDocs();
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Failed to fetch official docs: ${err instanceof Error ? err.message : String(err)}\n\nCheck network connectivity and retry.`,
          }],
          isError: true,
        };
      }

      let parsed: ReturnType<typeof parseIntoSections>;
      try {
        parsed = parseIntoSections(raw);
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Parsing failed: ${err instanceof Error ? err.message : String(err)}`,
          }],
          isError: true,
        };
      }

      try {
        // init sets BOTH baseline and current
        saveSnapshot('baseline', parsed.index, parsed.content);
        saveSnapshot('current', parsed.index, parsed.content);
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Failed to save snapshot to disk: ${err instanceof Error ? err.message : String(err)}\n\nCheck that ${getSnapshotDir()} is writable.`,
          }],
          isError: true,
        };
      }

      const { index } = parsed;
      const totalChars = Object.values(index.sections).reduce((s, sec) => s + sec.charCount, 0);

      const lines = [
        '# Official Docs Snapshot Created',
        '',
        `Fetched: ${index.fetchedAt}`,
        `Sections: ${index.sectionCount}`,
        `Total size: ${formatSize(totalChars)}`,
        `Snapshot dir: ${getSnapshotDir()}`,
        '',
        'Both baseline and current snapshots have been set.',
        '',
        'Next steps:',
        '  - Run refresh_official_docs() to update current without touching the baseline',
        '  - Run diff_official_docs() to see changes between baseline and current',
        '  - Run search_official_docs(query) to search the official docs',
      ];

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );

  // ── refresh_official_docs ───────────────────────────────────────────────
  server.tool(
    'refresh_official_docs',
    'Re-fetch the official Anthropic Claude Code docs and update the "current" snapshot without touching the baseline. Run this to update the comparison target before diffing. Takes ~5s (fetches ~1.2MB from Anthropic).',
    {},
    { readOnlyHint: false, destructiveHint: false, openWorldHint: true },
    async () => {
      const baseline = loadIndex('baseline');
      if (!baseline) {
        return {
          content: [{
            type: 'text',
            text: 'No baseline snapshot found. Run init_official_docs() first to create both the baseline and the initial current snapshot.',
          }],
          isError: true,
        };
      }

      let raw: string;
      try {
        raw = await fetchOfficialDocs();
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Failed to fetch official docs: ${err instanceof Error ? err.message : String(err)}\n\nYour existing snapshots are intact.`,
          }],
          isError: true,
        };
      }

      let parsed: ReturnType<typeof parseIntoSections>;
      try {
        parsed = parseIntoSections(raw);
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Parsing failed: ${err instanceof Error ? err.message : String(err)}\n\nYour existing snapshots are intact.`,
          }],
          isError: true,
        };
      }

      try {
        saveSnapshot('current', parsed.index, parsed.content);
      } catch (err) {
        return {
          content: [{
            type: 'text',
            text: `Failed to save current snapshot: ${err instanceof Error ? err.message : String(err)}`,
          }],
          isError: true,
        };
      }

      // Quick preview: run the diff to show a summary
      const diff = diffSnapshots(baseline, parsed.index);
      const total = diff.added.length + diff.removed.length + diff.modified.length;

      const lines = [
        '# Official Docs — Current Snapshot Updated',
        '',
        `Fetched: ${parsed.index.fetchedAt}`,
        `Sections: ${parsed.index.sectionCount}`,
        '',
      ];

      if (total === 0) {
        lines.push(`No changes vs baseline (${formatDate(baseline.fetchedAt)}). All ${diff.unchanged} sections unchanged.`);
      } else {
        lines.push(`vs baseline (${formatDate(baseline.fetchedAt)}): ${diff.added.length} added, ${diff.removed.length} removed, ${diff.modified.length} modified, ${diff.unchanged} unchanged`);
        lines.push('');
        lines.push('Run diff_official_docs() for the full diff.');
      }

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );

  // ── diff_official_docs ──────────────────────────────────────────────────
  server.tool(
    'diff_official_docs',
    'Compare the baseline and current official Anthropic Claude Code docs snapshots. Shows added, removed, and modified pages. No network call — reads local files only. Run init_official_docs() first, then refresh_official_docs() when you want to update the current snapshot.',
    {},
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async () => {
      const baseline = loadIndex('baseline');
      if (!baseline) {
        return {
          content: [{
            type: 'text',
            text: 'No baseline found. Run init_official_docs() first to create a baseline snapshot.',
          }],
          isError: true,
        };
      }

      const current = loadIndex('current');
      if (!current) {
        return {
          content: [{
            type: 'text',
            text: 'No current snapshot found. Run refresh_official_docs() to fetch the latest docs.',
          }],
          isError: true,
        };
      }

      // Fast path: identical content hashes
      if (baseline.contentHash === current.contentHash) {
        const ageDays = snapshotAgeDays(current);
        const staleWarn = ageDays > STALENESS_WARN_DAYS
          ? `\n⚠️  Current snapshot is ${ageDays} days old — consider running refresh_official_docs()`
          : '';
        return {
          content: [{
            type: 'text',
            text: [
              '# Official Docs Diff',
              '',
              `Baseline: ${formatDate(baseline.fetchedAt)} | Current: ${formatDate(current.fetchedAt)}`,
              '',
              `No changes detected. All ${baseline.sectionCount} sections unchanged.${staleWarn}`,
              '',
              'Run refresh_official_docs() to fetch latest docs and update current.',
            ].join('\n'),
          }],
        };
      }

      const diff = diffSnapshots(baseline, current);

      // Enrich modified sections with firstChangedLine (load only modified slugs)
      if (diff.modified.length > 0) {
        const modifiedSlugs = diff.modified.map((m) => m.slug);
        const baselineContents = loadSections('baseline', modifiedSlugs);
        const currentContents = loadSections('current', modifiedSlugs);

        for (const entry of diff.modified) {
          const baseContent = baselineContents[entry.slug];
          const currContent = currentContents[entry.slug];
          if (baseContent && currContent) {
            const line = findFirstChangedLine(baseContent, currContent);
            if (line) entry.firstChangedLine = line;
          }
        }
      }

      const lines: string[] = [
        '# Official Docs Diff',
        '',
        `Baseline: ${formatDate(baseline.fetchedAt)} | Current: ${formatDate(current.fetchedAt)}`,
        '',
      ];

      const ageDays = snapshotAgeDays(current);
      if (ageDays > STALENESS_WARN_DAYS) {
        lines.push(`⚠️  Current snapshot is ${ageDays} days old — consider running refresh_official_docs()`);
        lines.push('');
      }

      if (diff.added.length > 0) {
        lines.push(`## Added (${diff.added.length})`);
        for (const s of diff.added) {
          lines.push(`+ ${s.slug} — "${s.title}"`);
          lines.push(`  ${s.sourceUrl}`);
        }
        lines.push('');
      }

      if (diff.removed.length > 0) {
        lines.push(`## Removed (${diff.removed.length})`);
        for (const s of diff.removed) {
          lines.push(`- ${s.slug} — "${s.title}"`);
          lines.push(`  ${s.sourceUrl}`);
        }
        lines.push('');
      }

      if (diff.modified.length > 0) {
        lines.push(`## Modified (${diff.modified.length})`);
        for (const s of diff.modified) {
          const delta = s.lineDelta !== undefined
            ? (s.lineDelta >= 0 ? `+${s.lineDelta}` : `${s.lineDelta}`)
            : '';
          const charDelta = s.charsAfter !== undefined && s.charsBefore !== undefined
            ? (s.charsAfter - s.charsBefore >= 0
              ? `+${s.charsAfter - s.charsBefore}`
              : `${s.charsAfter - s.charsBefore}`)
            : '';
          lines.push(`~ ${s.slug} (L${s.linesBefore} → L${s.linesAfter}, ${delta} lines, ${charDelta} chars)`);
          if (s.firstChangedLine) {
            lines.push(`  First change: "${s.firstChangedLine}"`);
          }
          lines.push(`  ${s.sourceUrl}`);
        }
        lines.push('');
      }

      const total = diff.added.length + diff.removed.length + diff.modified.length;
      lines.push('---');
      lines.push(`${diff.added.length} added, ${diff.removed.length} removed, ${diff.modified.length} modified, ${diff.unchanged} unchanged (${total} total changes)`);
      lines.push('Run refresh_official_docs() to update current to latest.');

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );

  // ── search_official_docs ────────────────────────────────────────────────
  server.tool(
    'search_official_docs',
    'Search the official Anthropic Claude Code documentation by keyword or topic. Uses the local current snapshot — no network call. Run init_official_docs() first.',
    {
      query: z.string().describe('Search term or topic (e.g. "hooks", "MCP authentication", "cost limits")'),
      limit: z.number().min(1).max(10).optional().default(5).describe('Max sections to return (default 5)'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ query, limit }) => {
      const current = loadIndex('current');
      if (!current) {
        return {
          content: [{
            type: 'text',
            text: 'No snapshot found. Run init_official_docs() first to create a local cache of the official docs.',
          }],
          isError: true,
        };
      }

      // Score all sections against the query (index only — no content loaded yet)
      const scored = Object.values(current.sections)
        .map((sec) => ({ meta: sec, titleScore: sec.title.toLowerCase().includes(query.toLowerCase()) ? 3 : 0 }))
        .filter((item) => item.titleScore > 0); // title-only pass first for speed

      // If fewer than limit title matches, also check content (load lazily)
      let finalSlugs: string[];
      if (scored.length >= (limit ?? 5)) {
        finalSlugs = scored
          .sort((a, b) => b.titleScore - a.titleScore)
          .slice(0, limit ?? 5)
          .map((item) => item.meta.slug);
      } else {
        // Load all content and score body matches too
        const allSlugs = Object.keys(current.sections);
        const allContents = loadSections('current', allSlugs);
        const fullScored = Object.values(current.sections)
          .map((sec) => ({
            meta: sec,
            score: scoreSection(sec.title, allContents[sec.slug] ?? '', query),
          }))
          .filter((item) => item.score > 0)
          .sort((a, b) => b.score - a.score)
          .slice(0, limit ?? 5);
        finalSlugs = fullScored.map((item) => item.meta.slug);
      }

      if (finalSlugs.length === 0) {
        return {
          content: [{
            type: 'text',
            text: `No results for "${query}" in ${current.sectionCount} sections (snapshot: ${formatDate(current.fetchedAt)}).\n\nTry broader terms or run refresh_official_docs() to update the cache.`,
          }],
        };
      }

      // Load only the matching sections
      const matchingContents = loadSections('current', finalSlugs);

      const lines: string[] = [
        `# Search: "${query}" — ${finalSlugs.length} result${finalSlugs.length !== 1 ? 's' : ''} (snapshot: ${formatDate(current.fetchedAt)})`,
        '',
      ];

      for (const slug of finalSlugs) {
        const meta = current.sections[slug];
        const content = matchingContents[slug] ?? '';
        const excerpt = extractExcerpt(content, query);
        lines.push(`## ${meta.title}`);
        lines.push(meta.sourceUrl);
        lines.push('');
        lines.push(excerpt);
        lines.push('');
      }

      lines.push('---');
      lines.push(`Showing ${finalSlugs.length} of ${current.sectionCount} sections. Run refresh_official_docs() to update the cache.`);

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
