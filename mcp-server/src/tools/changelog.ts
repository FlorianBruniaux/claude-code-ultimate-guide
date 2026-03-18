import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { readSection } from '../lib/section-reader.js';
import { parseChangelog, filterByPeriod } from '../lib/changelog-parser.js';
import { githubUrl, guideSiteUrl } from '../lib/urls.js';

const CHANGELOG_PATH = 'CHANGELOG.md';
const CHANGELOG_GITHUB = githubUrl(CHANGELOG_PATH);

// ─── File path extractor ──────────────────────────────────────────────────────

// Matches paths like: guide/ultimate-guide.md, docs/resource-evaluations/xxx.md,
// examples/agents/foo.md, machine-readable/reference.yaml, guide/cheatsheet.md
const FILE_PATH_RE =
  /\b((?:guide|docs|examples|machine-readable|whitepapers)\/[a-zA-Z0-9_./\-]+\.(?:md|yaml|yml|json|sh|ts|txt))/g;

interface ResourceLink {
  path: string;
  github: string;
  site: string | null;
}

function extractResourceLinks(text: string): ResourceLink[] {
  const seen = new Set<string>();
  const links: ResourceLink[] = [];
  for (const match of text.matchAll(FILE_PATH_RE)) {
    const path = match[1];
    if (seen.has(path)) continue;
    seen.add(path);
    links.push({
      path,
      github: githubUrl(path),
      site: guideSiteUrl(path),
    });
  }
  return links;
}

async function fetchChangelog(): Promise<string | null> {
  const result = await readSection(CHANGELOG_PATH, 1, 500);
  if (!result) return null;

  // If truncated, fetch more until we have everything (max 3000 lines)
  if (!result.hasMore) return result.content;

  let full = result.content;
  let offset = result.nextOffset!;
  for (let i = 0; i < 5 && offset; i++) {
    const next = await readSection(CHANGELOG_PATH, offset, 500);
    if (!next) break;
    full += '\n' + next.content;
    offset = next.nextOffset ?? 0;
    if (!next.hasMore) break;
  }
  return full;
}

export function registerChangelog(server: McpServer): void {
  // ── get_changelog ─────────────────────────────────────────────────────────
  server.tool(
    'get_changelog',
    'Return the last N entries from the Claude Code Ultimate Guide CHANGELOG. Shows what changed in the guide itself (not Claude Code CLI releases — use get_release() for that).',
    {
      count: z.number().min(1).max(20).optional().default(5).describe('Number of recent changelog entries to return (default 5)'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ count }) => {
      const raw = await fetchChangelog();
      if (!raw) {
        return {
          content: [{ type: 'text', text: 'CHANGELOG.md unavailable (offline and no cache).' }],
          isError: true,
        };
      }

      const entries = parseChangelog(raw);
      const slice = entries.slice(0, count ?? 5);

      if (slice.length === 0) {
        return { content: [{ type: 'text', text: 'No changelog entries found.' }] };
      }

      const combinedText = slice.map((e) => e.content).join('\n\n');
      const links = extractResourceLinks(combinedText);

      const lines = [
        `# Guide CHANGELOG — last ${slice.length} entries`,
        `GitHub: ${CHANGELOG_GITHUB}`,
        '',
        combinedText,
      ];

      if (links.length > 0) {
        lines.push('', '---', '## Resources mentioned', '');
        for (const l of links) {
          lines.push(`**${l.path}**`);
          lines.push(`  GitHub: ${l.github}`);
          if (l.site) lines.push(`  Guide: ${l.site}`);
        }
      }

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );

  // ── get_digest ─────────────────────────────────────────────────────────────
  server.tool(
    'get_digest',
    'Return a digest of guide and Claude Code CLI changes for a given period. Combines guide CHANGELOG entries + official Claude Code releases in the time window.',
    {
      period: z
        .enum(['day', 'week', 'month'])
        .describe('Time window: "day" (24h), "week" (7 days), "month" (30 days)'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ period }) => {
      const labels = { day: 'last 24h', week: 'last 7 days', month: 'last 30 days' };

      // Guide changelog
      const raw = await fetchChangelog();
      const guideEntries = raw ? filterByPeriod(parseChangelog(raw), period) : [];

      // Claude Code releases
      const { loadReleases } = await import('../lib/content.js');
      const relData = loadReleases();
      const MS = { day: 86_400_000, week: 7 * 86_400_000, month: 30 * 86_400_000 };
      const cutoff = Date.now() - MS[period];
      const ccReleases = (relData.releases as Array<{ version: string; date: string; highlights: string[] }>)
        .filter((r) => new Date(r.date).getTime() >= cutoff);

      const lines: string[] = [
        `# Digest — ${labels[period]}`,
        `Generated: ${new Date().toISOString().slice(0, 10)}`,
        '',
      ];

      // Guide section
      lines.push('## Guide changes');
      if (guideEntries.length === 0) {
        lines.push('No guide updates in this period.');
        lines.push('');
      } else {
        const guideText = guideEntries.map((e) => e.content).join('\n\n');
        lines.push(guideText);
        lines.push('');

        // Resource links extracted from guide entries
        const links = extractResourceLinks(guideText);
        if (links.length > 0) {
          lines.push('### Resources mentioned');
          for (const l of links) {
            const siteStr = l.site ? ` | Guide: ${l.site}` : '';
            lines.push(`- \`${l.path}\` — GitHub: ${l.github}${siteStr}`);
          }
          lines.push('');
        }
      }

      // CC releases section
      lines.push('## Claude Code CLI releases');
      if (ccReleases.length === 0) {
        lines.push('No Claude Code releases in this period.');
      } else {
        for (const r of ccReleases) {
          lines.push(`### v${r.version} (${r.date})`);
          for (const h of r.highlights ?? []) lines.push(`- ${h}`);
          // Link to the release tracking file
          lines.push(`GitHub: ${githubUrl('guide/core/claude-code-releases.md')}`);
          lines.push('');
        }
      }

      lines.push('---');
      lines.push(`Full changelog: ${CHANGELOG_GITHUB}`);

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
