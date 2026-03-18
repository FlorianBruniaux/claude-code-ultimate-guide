import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { loadReference } from '../lib/content.js';

export function registerListTopics(server: McpServer): void {
  server.tool(
    'list_topics',
    'List all top-level topics and categories in the Claude Code Ultimate Guide. Useful for exploring what the guide covers before searching.',
    {},
    {
      readOnlyHint: true,
      destructiveHint: false,
      openWorldHint: false,
    },
    async () => {
      const ref = loadReference();

      // Group entries by first key segment (before first underscore)
      const categories = new Map<string, { count: number; samples: string[] }>();

      for (const entry of ref.entries) {
        const category = entry.key.split('_')[0] ?? entry.key;
        if (!categories.has(category)) {
          categories.set(category, { count: 0, samples: [] });
        }
        const cat = categories.get(category)!;
        cat.count++;
        if (cat.samples.length < 5) {
          cat.samples.push(entry.key);
        }
      }

      const sorted = Array.from(categories.entries()).sort((a, b) => b[1].count - a[1].count);

      const lines: string[] = [
        `Claude Code Ultimate Guide — ${ref.entries.length} indexed entries across ${sorted.length} categories`,
        `Version: ${ref.version}`,
        '',
        '## Topics',
        '',
      ];

      for (const [category, { count, samples }] of sorted) {
        lines.push(`### ${category} (${count} entries)`);
        lines.push(`Examples: ${samples.join(', ')}`);
        lines.push('');
      }

      lines.push('---');
      lines.push('Use search_guide("topic") to search within any category.');
      lines.push('Use read_section("guide/ultimate-guide.md") to browse the full guide.');

      return {
        content: [{ type: 'text', text: lines.join('\n') }],
      };
    },
  );
}
