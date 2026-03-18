import { loadReference, type IndexEntry } from './content.js';

// ─── Stop words ───────────────────────────────────────────────────────────────

const STOP_WORDS = new Set([
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
  'do', 'does', 'did', 'have', 'has', 'had', 'will', 'would',
  'can', 'could', 'should', 'may', 'might', 'shall',
  'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
  'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
  'how', 'what', 'when', 'where', 'which', 'who', 'why',
  'not', 'no', 'up', 'out', 'if', 'about', 'into', 'that', 'this',
  'and', 'or', 'but', 'so', 'yet', 'nor', 'use', 'using', 'used',
  'get', 'set', 'add', 'run', 'make', 'see', 'all', 'new',
]);

// ─── Synonymes domaine ────────────────────────────────────────────────────────

const SYNONYMS: Record<string, string[]> = {
  env: ['environment', 'env_var', 'variable', 'envvar'],
  config: ['configuration', 'settings', 'configure', 'setup'],
  cmd: ['command', 'commands', 'slash'],
  auth: ['authentication', 'permission', 'permissions', 'authorize'],
  hook: ['hooks', 'event', 'pre_tool', 'post_tool', 'events'],
  agent: ['agents', 'subagent', 'teammate', 'subagents'],
  mcp: ['model_context_protocol', 'mcp_server', 'mcp_servers', 'protocol'],
  skill: ['skills', 'skill_module', 'modules'],
  debug: ['debugging', 'troubleshoot', 'troubleshooting', 'diagnose'],
  cost: ['token', 'tokens', 'pricing', 'budget', 'optimization', 'cost'],
  security: ['secure', 'hardening', 'vulnerability', 'cve', 'threat'],
  sandbox: ['isolation', 'container', 'docker', 'isolated'],
  slash: ['command', 'commands', 'custom_command'],
  install: ['installation', 'setup', 'installing'],
  memory: ['persistence', 'serena', 'context'],
  test: ['testing', 'tdd', 'bdd', 'spec', 'specs'],
  workflow: ['workflows', 'process', 'flow'],
  template: ['templates', 'example', 'examples', 'boilerplate'],
  model: ['claude', 'opus', 'sonnet', 'haiku', 'llm'],
  key: ['keyboard', 'shortcut', 'keybinding', 'keybindings'],
};

// ─── Levenshtein distance (inline, ~20 lines) ─────────────────────────────────

function levenshtein(a: string, b: string): number {
  if (Math.abs(a.length - b.length) > 3) return 99; // fast bail
  const m = a.length, n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)),
  );
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] =
        a[i - 1] === b[j - 1]
          ? dp[i - 1][j - 1]
          : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[m][n];
}

// ─── Query processing ─────────────────────────────────────────────────────────

export function tokenizeQuery(query: string): string[] {
  const tokens = query
    .toLowerCase()
    .replace(/[^a-z0-9_\s-]/g, ' ')
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t));

  // Expand synonyms
  const expanded = new Set(tokens);
  for (const token of tokens) {
    const syns = SYNONYMS[token];
    if (syns) {
      for (const syn of syns) expanded.add(syn);
    }
    // Also check partial matches on synonym keys
    for (const [key, syns2] of Object.entries(SYNONYMS)) {
      if (key.startsWith(token) || token.startsWith(key)) {
        expanded.add(key);
        for (const s of syns2) expanded.add(s);
      }
    }
  }

  return Array.from(expanded);
}

// ─── Scoring ──────────────────────────────────────────────────────────────────

export interface SearchResult {
  key: string;
  section: string;
  score: number;
  value: unknown;
  target: ReturnType<typeof import('./content.js').resolveDeepDive>;
  hint: string;
}

function scoreEntry(entry: IndexEntry, tokens: string[], originalTokens: string[]): number {
  let score = 0;
  const keyLower = entry.key.toLowerCase();
  const keySegments = keyLower.split('_');

  for (const token of tokens) {
    if (token.length < 2) continue;

    if (keyLower === token) {
      score += 20;
    } else if (keyLower.includes(token)) {
      score += 10;
    } else if (keySegments.some((seg) => seg.startsWith(token))) {
      score += 7;
    } else if (entry.searchableText.includes(token)) {
      score += 5;
    }
  }

  // Fuzzy only if no exact matches and token is long enough
  if (score === 0) {
    for (const token of originalTokens) {
      if (token.length <= 4) continue;
      for (const seg of keySegments) {
        if (seg.length > 4 && levenshtein(token, seg) <= 2) {
          score += 2;
          break;
        }
      }
    }
  }

  return score;
}

function buildHint(entry: IndexEntry): string {
  const { target } = entry;
  if (!target) return `Key: ${entry.key}`;

  switch (target.type) {
    case 'line':
      return `guide/ultimate-guide.md:${target.line}`;
    case 'file':
      return target.line ? `${target.path}:${target.line}` : target.path;
    case 'url':
      return target.url;
    case 'inline':
      return target.text.length > 100 ? target.text.slice(0, 100) + '…' : target.text;
    case 'structured':
      return `[structured data] — ${entry.key}`;
  }
}

// ─── Main search function ─────────────────────────────────────────────────────

export function searchGuide(query: string, limit = 10): SearchResult[] {
  const ref = loadReference();
  const tokens = tokenizeQuery(query);
  const originalTokens = query
    .toLowerCase()
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t));

  if (tokens.length === 0) return [];

  const results: SearchResult[] = [];

  for (const entry of ref.entries) {
    const score = scoreEntry(entry, tokens, originalTokens);
    if (score > 0) {
      results.push({
        key: entry.key,
        section: entry.section,
        score,
        value: entry.value,
        target: entry.target,
        hint: buildHint(entry),
      });
    }
  }

  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, Math.min(limit, 20));
}
