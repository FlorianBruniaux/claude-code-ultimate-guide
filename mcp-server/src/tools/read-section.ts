import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { readSection, splitAnchor, AnchorNotFoundError } from '../lib/section-reader.js';
import { resolveContentPath } from '../lib/content.js';
import { formatLinks } from '../lib/urls.js';

export function registerReadSection(server: McpServer): void {
  server.tool(
    'read_section',
    'Read a section from a guide file (markdown, YAML, examples). Supports pagination via offset, or a "#heading-slug" anchor to jump straight to a section (as returned by search_guide()). Use after search_guide() to fetch the full content at a specific location.',
    {
      path: z.string().describe('Relative path from repo root, optionally with a "#heading-slug" anchor (e.g. "guide/ultimate-guide.md", "guide/core/memory-systems.md#1-tldr-three-track-model")'),
      offset: z.number().min(1).optional().default(1).describe('Line number to start reading from (1-based, default 1). Ignored when path has a "#" anchor.'),
      limit: z.number().min(1).max(500).optional().default(500).describe('Max lines to return (default 500, max 500)'),
    },
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
    async ({ path: rawPath, offset, limit }) => {
      // Security: validate the FILE part before attempting read. Anchors
      // ("#slug") are stripped first so the extension check doesn't see
      // trailing anchor text and traversal checks still run on the file path.
      const { file: filePath } = splitAnchor(rawPath);
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

      let result;
      try {
        result = await readSection(rawPath, offset ?? 1, limit ?? 500);
      } catch (err) {
        if (err instanceof AnchorNotFoundError) {
          return {
            content: [
              {
                type: 'text',
                text: [
                  `Error: ${err.message}`,
                  '',
                  err.nearMisses.length > 0
                    ? ['Closest headings in this file:', ...err.nearMisses.map((m) => `  • ${m}`)].join('\n')
                    : 'No headings found in this file to suggest.',
                ].join('\n'),
              },
            ],
            isError: true,
          };
        }
        throw err;
      }

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
        'Share the Guide URL with the user for further reading.',
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
