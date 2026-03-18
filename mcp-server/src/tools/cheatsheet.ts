import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { readSection } from '../lib/section-reader.js';
import { formatLinks } from '../lib/urls.js';

const CHEATSHEET_PATH = 'guide/cheatsheet.md';

export function registerCheatsheet(server: McpServer): void {
  server.tool(
    'get_cheatsheet',
    'Return the Claude Code cheatsheet — a compact 1-page reference covering the most important commands, shortcuts, config options, and workflows.',
    {
      section: z.string().optional().describe('Optional: filter to a specific section (e.g. "installation", "hooks", "agents", "mcp")'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ section }) => {
      const result = await readSection(CHEATSHEET_PATH, 1, 500);
      if (!result) {
        return {
          content: [{ type: 'text', text: 'Cheatsheet unavailable (offline and no cache).' }],
          isError: true,
        };
      }

      let content = result.content;

      // Filter to section if requested
      if (section) {
        const sectionLower = section.toLowerCase();
        const lines = content.split('\n');
        const start = lines.findIndex(
          (l) => l.toLowerCase().includes(sectionLower) && l.startsWith('#'),
        );
        if (start !== -1) {
          // Find end of section (next heading of same or higher level)
          const startLevel = (lines[start].match(/^#+/) ?? [''])[0].length;
          let end = lines.length;
          for (let i = start + 1; i < lines.length; i++) {
            const m = lines[i].match(/^(#+)/);
            if (m && m[1].length <= startLevel) { end = i; break; }
          }
          content = lines.slice(start, end).join('\n');
        }
      }

      const header = [
        `# Claude Code Cheatsheet`,
        formatLinks(CHEATSHEET_PATH),
        section ? `Filtered: "${section}"` : `Lines: ${result.startLine}-${result.endLine} of ${result.totalLines}`,
        result.hasMore ? `Has more — use read_section("${CHEATSHEET_PATH}", ${result.nextOffset}) for rest` : '',
        '---',
        '',
      ].filter(Boolean).join('\n');

      return { content: [{ type: 'text', text: header + content }] };
    },
  );
}
