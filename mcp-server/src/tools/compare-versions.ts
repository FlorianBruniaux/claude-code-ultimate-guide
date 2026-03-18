import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { loadReleases } from '../lib/content.js';
import { githubUrl } from '../lib/urls.js';

const RELEASES_GITHUB = githubUrl('guide/core/claude-code-releases.md');

interface ReleaseEntry {
  version: string;
  date: string;
  highlights: string[];
  breaking?: string[];
}

function parseSemver(v: string): [number, number, number] {
  const parts = v.replace(/^v/, '').split('.').map(Number);
  return [parts[0] ?? 0, parts[1] ?? 0, parts[2] ?? 0];
}

function semverCompare(a: string, b: string): number {
  const [am, an, ap] = parseSemver(a);
  const [bm, bn, bp] = parseSemver(b);
  if (am !== bm) return am - bm;
  if (an !== bn) return an - bn;
  return ap - bp;
}

export function registerCompareVersions(server: McpServer): void {
  server.tool(
    'compare_versions',
    'Show what changed between two Claude Code CLI versions. Lists all releases in range with aggregated highlights and breaking changes.',
    {
      from: z.string().describe('Starting version (older), e.g. "2.1.50"'),
      to: z.string().optional().describe('Ending version (newer). Omit to use the latest.'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ from, to }) => {
      const data = loadReleases();
      const releases = data.releases as ReleaseEntry[];

      const fromClean = from.replace(/^v/, '');
      const toClean = (to ?? data.latest).replace(/^v/, '');

      // Ensure from <= to (by semver)
      const fromVer = fromClean;
      const toVer = toClean;
      const ordered = semverCompare(fromVer, toVer) <= 0
        ? { older: fromVer, newer: toVer }
        : { older: toVer, newer: fromVer };

      // Validate both versions exist
      const fromFound = releases.find((r) => r.version === ordered.older);
      const toFound = releases.find((r) => r.version === ordered.newer);

      if (!fromFound) {
        const known = releases.slice(0, 10).map((r) => `v${r.version}`).join(', ');
        return {
          content: [{
            type: 'text',
            text: `Version v${ordered.older} not found.\n\nRecent versions: ${known}\n\nFull history: ${RELEASES_GITHUB}`,
          }],
        };
      }
      if (!toFound) {
        const known = releases.slice(0, 10).map((r) => `v${r.version}`).join(', ');
        return {
          content: [{
            type: 'text',
            text: `Version v${ordered.newer} not found.\n\nRecent versions: ${known}\n\nFull history: ${RELEASES_GITHUB}`,
          }],
        };
      }

      // Collect versions in range (releases are newest-first)
      const inRange = releases.filter(
        (r) => semverCompare(r.version, ordered.older) >= 0 &&
               semverCompare(r.version, ordered.newer) <= 0,
      );

      // Aggregate highlights and breaking changes
      const allHighlights: string[] = [];
      const allBreaking: string[] = [];

      for (const r of inRange) {
        for (const h of r.highlights ?? []) allHighlights.push(h);
        for (const b of r.breaking ?? []) allBreaking.push(b);
      }

      const versionList = inRange
        .slice()
        .sort((a, b) => semverCompare(b.version, a.version)) // newest first
        .map((r) => `v${r.version} (${r.date})`)
        .join(', ');

      const lines = [
        `# Claude Code: v${ordered.older} → v${ordered.newer}`,
        RELEASES_GITHUB,
        '',
        `**${inRange.length} release${inRange.length !== 1 ? 's' : ''} in range**: ${versionList}`,
        '',
        '## What changed',
        ...allHighlights.map((h) => `- ${h}`),
      ];

      if (allBreaking.length > 0) {
        lines.push('', '## Breaking changes');
        for (const b of allBreaking) lines.push(`- ⚠️ ${b}`);
      }

      lines.push('', `---`);
      lines.push(`${allHighlights.length} highlight${allHighlights.length !== 1 ? 's' : ''} | ${allBreaking.length} breaking change${allBreaking.length !== 1 ? 's' : ''} | Use get_release(version) for per-release details.`);

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
