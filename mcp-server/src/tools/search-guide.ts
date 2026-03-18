import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { searchGuide } from '../lib/search.js';
import { formatLinks, githubUrl } from '../lib/urls.js';

export function registerSearchGuide(server: McpServer): void {
  server.tool(
    'search_guide',
    'Search the Claude Code Ultimate Guide by topic, keyword, or question. Returns ranked results with file locations and descriptions. Use this as the first step for any guide question.',
    {
      query: z.string().describe('Search query — topic, question, or keyword (e.g. "hooks", "custom agents", "cost optimization")'),
      limit: z.number().min(1).max(20).optional().default(10).describe('Max results to return (default 10, max 20)'),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
    async ({ query, limit }) => {
      const results = searchGuide(query, limit ?? 10);

      if (results.length === 0) {
        return {
          content: [
            {
              type: 'text',
              text: [
                `No results found for: "${query}"`,
                '',
                'Tips:',
                '  • Try shorter keywords: "hooks" instead of "how do I use hooks"',
                '  • Use the resource fallback: read claude-code-guide://reference for the full YAML index',
                '  • Try related terms: "commands", "agents", "mcp", "security", "cost"',
              ].join('\n'),
            },
          ],
        };
      }

      const lines: string[] = [
        `Found ${results.length} result(s) for: "${query}"`,
        '',
      ];

      for (const result of results) {
        lines.push(`## ${result.key} (score: ${result.score})`);
        lines.push(`Section: ${result.section}`);
        lines.push(`Location: ${result.hint}`);

        if (result.target) {
          switch (result.target.type) {
            case 'line':
              lines.push(`→ read_section("${result.target.file}", ${result.target.line})`);
              lines.push(`   ${formatLinks(result.target.file, result.target.line)}`);
              break;
            case 'file':
              lines.push(
                `→ read_section("${result.target.path}"${result.target.line ? `, ${result.target.line}` : ''})`,
              );
              lines.push(`   ${formatLinks(result.target.path, result.target.line)}`);
              break;
            case 'url':
              lines.push(`→ External: ${result.target.url}`);
              break;
            case 'inline':
              lines.push(`→ ${result.target.text.slice(0, 200)}${result.target.text.length > 200 ? '…' : ''}`);
              break;
            case 'structured':
              lines.push(`→ [structured data — use read_section or view resource]`);
              break;
          }
        }

        lines.push('');
      }

      lines.push('---');
      lines.push('Use read_section(path, line) to fetch the full content of any result.');
      lines.push('Use claude-code-guide://reference resource for the complete YAML index.');

      return {
        content: [{ type: 'text', text: lines.join('\n') }],
      };
    },
  );
}
