import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { readSection } from '../lib/section-reader.js';
import { resolveContentPath } from '../lib/content.js';
import { formatLinks } from '../lib/urls.js';

export function registerReadSection(server: McpServer): void {
  server.tool(
    'read_section',
    'Read a section from a guide file (markdown, YAML, examples). Supports pagination via offset. Use after search_guide() to fetch the full content at a specific location.',
    {
      path: z.string().describe('Relative path from repo root (e.g. "guide/ultimate-guide.md", "examples/agents/code-reviewer.md")'),
      offset: z.number().min(1).optional().default(1).describe('Line number to start reading from (1-based, default 1)'),
      limit: z.number().min(1).max(500).optional().default(500).describe('Max lines to return (default 500, max 500)'),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
    async ({ path: filePath, offset, limit }) => {
      // Security: validate path before attempting read
      const resolved = resolveContentPath(filePath);
      if (resolved === null) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: Invalid path "${filePath}". Only paths within the guide repo with allowed extensions (.md, .yaml, .yml, .sh, .ts, .js, .json, .py, .txt) are permitted.`,
            },
          ],
          isError: true,
        };
      }

      const result = await readSection(filePath, offset ?? 1, limit ?? 500);

      if (result === null) {
        return {
          content: [
            {
              type: 'text',
              text: [
                `File not found or unavailable: "${filePath}"`,
                '',
                'This may be because:',
                '  • The file does not exist in the guide repo',
                '  • Network unavailable (running offline without cache)',
                '',
                'Fallback: read the resource claude-code-guide://reference for inline summaries.',
              ].join('\n'),
            },
          ],
          isError: true,
        };
      }

      const header = [
        `File: ${filePath}`,
        `Lines: ${result.startLine}-${result.endLine} of ${result.totalLines}`,
        result.hasMore
          ? `Has more: yes — use offset=${result.nextOffset} for next section`
          : 'Has more: no',
        formatLinks(filePath, result.startLine),
        '---',
        '',
      ].join('\n');

      return {
        content: [
          {
            type: 'text',
            text: header + result.content,
          },
        ],
      };
    },
  );
}
