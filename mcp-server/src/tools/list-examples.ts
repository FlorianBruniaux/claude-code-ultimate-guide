import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { loadReference, resolveDeepDive } from '../lib/content.js';
import { githubUrl } from '../lib/urls.js';

const CATEGORIES = ['agents', 'commands', 'hooks', 'skills', 'scripts'] as const;
type Category = typeof CATEGORIES[number];

export function registerListExamples(server: McpServer): void {
  server.tool(
    'list_examples',
    'List all production-ready templates in the guide by category (agents, commands, hooks, skills, scripts). Use get_example(name) to fetch the content of any specific template.',
    {
      category: z
        .enum(CATEGORIES)
        .optional()
        .describe('Filter by category: agents | commands | hooks | skills | scripts. Omit for all.'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ category }) => {
      const ref = loadReference();

      // Collect all example paths from reference.yaml
      const byCategory = new Map<Category, Array<{ key: string; path: string; description: string }>>();
      for (const cat of CATEGORIES) byCategory.set(cat, []);

      for (const entry of ref.entries) {
        const target = entry.target ?? resolveDeepDive(entry.value);
        if (!target || target.type !== 'file') continue;
        if (!target.path.startsWith('examples/')) continue;

        const parts = target.path.split('/'); // ['examples', 'agents', 'file.md']
        const cat = parts[1] as Category;
        if (!CATEGORIES.includes(cat)) continue;
        if (category && cat !== category) continue;

        const list = byCategory.get(cat)!;
        // Deduplicate by path
        if (list.some((e) => e.path === target.path)) continue;

        // Build description from key
        const desc = entry.key
          .replace(/^deep_dive_/, '')
          .replace(/_/g, ' ')
          .replace(/\b\w/g, (c) => c.toUpperCase());

        list.push({ key: entry.key, path: target.path, description: desc });
      }

      const lines: string[] = [
        `# Claude Code Ultimate Guide — Templates`,
        `GitHub: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples`,
        '',
      ];

      let total = 0;
      for (const cat of CATEGORIES) {
        if (category && cat !== category) continue;
        const items = byCategory.get(cat)!;
        if (items.length === 0) continue;

        lines.push(`## ${cat.charAt(0).toUpperCase() + cat.slice(1)} (${items.length})`);
        for (const item of items) {
          const filename = item.path.split('/').pop() ?? item.path;
          const gh = githubUrl(item.path);
          lines.push(`- **${filename}** — ${item.description}`);
          lines.push(`  GitHub: ${gh}`);
          lines.push(`  → get_example("${filename.replace(/\.(md|yaml|sh|ts)$/, '')}")`);
        }
        lines.push('');
        total += items.length;
      }

      lines.push('---');
      lines.push(`${total} template(s) total. Use get_example(name) to fetch any template.`);

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
