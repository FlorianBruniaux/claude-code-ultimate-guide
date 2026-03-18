import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { loadReference, resolveDeepDive } from '../lib/content.js';
import { tokenizeQuery } from '../lib/search.js';
import { githubUrl } from '../lib/urls.js';

interface ExampleResult {
  path: string;
  key: string;
  score: number;
  description: string;
  githubUrl: string;
}

export function registerSearchExamples(server: McpServer): void {
  server.tool(
    'search_examples',
    'Semantic search across all production-ready templates by intent (e.g. "hook lint", "agent code review"). Different from get_example (exact name) and list_examples (category browse).',
    {
      query: z.string().describe('Search query describing the template you need, e.g. "hook lint", "agent code review", "pre-commit typescript"'),
      limit: z.number().min(1).max(20).optional().default(10).describe('Max results to return (default 10, max 20)'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ query, limit }) => {
      const ref = loadReference();
      const tokens = tokenizeQuery(query);
      const queryLower = query.toLowerCase();

      if (tokens.length === 0) {
        return {
          content: [{
            type: 'text',
            text: 'Query too short or contained only stop words. Try: "hook lint", "agent security", "pre-commit".',
          }],
        };
      }

      // Collect and score entries pointing to examples/
      const results: ExampleResult[] = [];
      const seen = new Set<string>();

      for (const entry of ref.entries) {
        const target = entry.target ?? resolveDeepDive(entry.value);
        if (!target || target.type !== 'file') continue;
        if (!target.path.startsWith('examples/')) continue;

        // Deduplicate by path
        if (seen.has(target.path)) continue;

        const pathLower = target.path.toLowerCase();
        const keyLower = entry.key.toLowerCase();
        const textLower = entry.searchableText.toLowerCase();

        let score = 0;

        // Exact substring match on full query (highest signal)
        if (pathLower.includes(queryLower)) score += 15;

        for (const token of tokens) {
          if (token.length < 2) continue;
          if (pathLower.includes(token)) score += 10;
          else if (keyLower.includes(token)) score += 7;
          else if (textLower.includes(token)) score += 5;
          else {
            // Fuzzy: token length >= 5, levenshtein-like (segment starts with token)
            if (token.length >= 5) {
              const pathSegments = pathLower.replace(/[/_.-]/g, ' ').split(' ');
              for (const seg of pathSegments) {
                if (seg.length >= 4 && (seg.startsWith(token.slice(0, -1)) || token.startsWith(seg.slice(0, -1)))) {
                  score += 2;
                  break;
                }
              }
            }
          }
        }

        if (score > 0) {
          // Build human-readable description from key
          const description = entry.searchableText.slice(0, 120).replace(/\s+/g, ' ').trim();

          seen.add(target.path);
          results.push({
            path: target.path,
            key: entry.key,
            score,
            description,
            githubUrl: githubUrl(target.path),
          });
        }
      }

      results.sort((a, b) => b.score - a.score);
      const topResults = results.slice(0, limit ?? 10);

      if (topResults.length === 0) {
        return {
          content: [{
            type: 'text',
            text: [
              `No examples found for: "${query}"`,
              '',
              'Try broader terms or browse by category:',
              '  • list_examples("agents")   — custom agent templates',
              '  • list_examples("hooks")    — event hook examples',
              '  • list_examples("commands") — slash command templates',
              '  • list_examples("skills")   — skill module templates',
              '  • list_examples("scripts")  — utility scripts',
            ].join('\n'),
          }],
        };
      }

      const lines = [
        `# Examples matching "${query}"`,
        `Found ${topResults.length} result${topResults.length !== 1 ? 's' : ''} (of ${results.length} scored)`,
        '',
      ];

      for (const r of topResults) {
        const name = r.path.split('/').pop()?.replace(/\.(md|yaml|sh|ts|js|py)$/, '') ?? r.key;
        lines.push(`## ${r.path}`);
        lines.push(`Score: ${r.score} | Key: ${r.key}`);
        lines.push(r.description);
        lines.push(`GitHub: ${r.githubUrl}`);
        lines.push(`→ get_example("${name}")`);
        lines.push('');
      }

      return { content: [{ type: 'text', text: lines.join('\n') }] };
    },
  );
}
