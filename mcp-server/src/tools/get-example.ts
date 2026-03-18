import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { loadReference, resolveDeepDive } from '../lib/content.js';
import { readSection } from '../lib/section-reader.js';
import { tokenizeQuery } from '../lib/search.js';
import { githubUrl } from '../lib/urls.js';

export function registerGetExample(server: McpServer): void {
  server.tool(
    'get_example',
    'Fetch a production-ready template or example from the guide (agents, skills, commands, hooks, scripts). Pass a partial name to search for matching examples.',
    {
      name: z.string().describe('Example name or partial match (e.g. "code-reviewer", "pre-commit hook", "custom agent")'),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
    async ({ name }) => {
      const ref = loadReference();
      const nameLower = name.toLowerCase();
      const tokens = tokenizeQuery(name);

      // Collect entries pointing to examples/
      interface ExampleMatch {
        key: string;
        path: string;
        score: number;
      }
      const matches: ExampleMatch[] = [];

      for (const entry of ref.entries) {
        const target = entry.target ?? resolveDeepDive(entry.value);
        if (!target || target.type !== 'file') continue;
        if (!target.path.startsWith('examples/')) continue;

        const pathLower = target.path.toLowerCase();
        const keyLower = entry.key.toLowerCase();
        let score = 0;

        // Exact match in path
        if (pathLower.includes(nameLower)) score += 20;
        if (keyLower.includes(nameLower)) score += 15;

        // Token match
        for (const token of tokens) {
          if (pathLower.includes(token)) score += 5;
          if (keyLower.includes(token)) score += 3;
        }

        if (score > 0) {
          matches.push({ key: entry.key, path: target.path, score });
        }
      }

      matches.sort((a, b) => b.score - a.score);

      if (matches.length === 0) {
        return {
          content: [
            {
              type: 'text',
              text: [
                `No examples found matching: "${name}"`,
                '',
                'Available example categories:',
                '  • examples/agents/     — Custom agent templates',
                '  • examples/commands/   — Slash command templates',
                '  • examples/hooks/      — Event hook examples',
                '  • examples/skills/     — Skill module templates',
                '  • examples/scripts/    — Utility scripts',
                '',
                'Try: get_example("agent"), get_example("hook"), get_example("command")',
              ].join('\n'),
            },
          ],
        };
      }

      // Single match: fetch and return content
      if (matches.length === 1 || matches[0].score >= 20) {
        const match = matches[0];
        const section = await readSection(match.path, 1, 500);

        if (!section) {
          return {
            content: [
              {
                type: 'text',
                text: [
                  `Example found: ${match.path}`,
                  `Key: ${match.key}`,
                  '',
                  'Content unavailable (offline or file not found).',
                  `Try: read_section("${match.path}")`,
                ].join('\n'),
              },
            ],
          };
        }

        return {
          content: [
            {
              type: 'text',
              text: [
                `# ${match.path}`,
                `Key: ${match.key}`,
                `Lines: ${section.startLine}-${section.endLine} of ${section.totalLines}`,
                `GitHub: ${githubUrl(match.path)}`,
                '---',
                '',
                section.content,
                section.hasMore ? `\n\n[truncated — use read_section("${match.path}", ${section.nextOffset}) for more]` : '',
              ].join('\n'),
            },
          ],
        };
      }

      // Multiple matches: list them
      const lines = [
        `Found ${matches.length} examples matching "${name}":`,
        '',
      ];

      for (const match of matches.slice(0, 10)) {
        lines.push(`• ${match.path}`);
        lines.push(`  Key: ${match.key} | Score: ${match.score}`);
        lines.push(`  → get_example("${match.path.split('/').pop()?.replace(/\.(md|yaml|sh|ts)$/, '') ?? match.key}")`);
        lines.push('');
      }

      return {
        content: [{ type: 'text', text: lines.join('\n') }],
      };
    },
  );
}
