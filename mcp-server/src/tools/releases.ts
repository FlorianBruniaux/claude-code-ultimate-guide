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

export function registerReleases(server: McpServer): void {
  server.tool(
    'get_release',
    'Get details about Claude Code CLI official releases. Pass a version to get a specific release, or omit to get the latest and recent history.',
    {
      version: z.string().optional().describe('Specific version (e.g. "2.1.59"). Omit for latest + recent 5.'),
      count: z.number().min(1).max(30).optional().default(5).describe('Number of recent releases to show when no version specified (default 5)'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ version, count }) => {
      const data = loadReleases();
      const releases = data.releases as ReleaseEntry[];

      if (version) {
        const found = releases.find(
          (r) => r.version === version || r.version === version.replace(/^v/, ''),
        );
        if (!found) {
          const versions = releases.slice(0, 10).map((r) => `v${r.version}`).join(', ');
          return {
            content: [{
              type: 'text',
              text: `Release v${version} not found.\n\nRecent versions: ${versions}\n\nFull history: ${RELEASES_GITHUB}`,
            }],
          };
        }

        const lines = [
          `# Claude Code v${found.version} (${found.date})`,
          RELEASES_GITHUB,
          '',
          '## Highlights',
          ...(found.highlights ?? []).map((h) => `- ${h}`),
        ];

        if (found.breaking?.length) {
          lines.push('', '## Breaking changes');
          for (const b of found.breaking) lines.push(`- ⚠️ ${b}`);
        }

        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      // Latest + recent N
      const recent = releases.slice(0, count ?? 5);
      const lines = [
        `# Claude Code Releases`,
        `Latest: v${data.latest} (updated: ${data.updated})`,
        RELEASES_GITHUB,
        '',
      ];

      for (const r of recent) {
        lines.push(`## v${r.version} — ${r.date}`);
        for (const h of r.highlights ?? []) lines.push(`- ${h}`);
        if (r.breaking?.length) {
          for (const b of r.breaking) lines.push(`  ⚠️ ${b}`);
        }
        lines.push('');
      }

      lines.push(`---`);
      lines.push(`Showing ${recent.length} of ${releases.length} tracked releases. Use get_release(version) for details.`);

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
