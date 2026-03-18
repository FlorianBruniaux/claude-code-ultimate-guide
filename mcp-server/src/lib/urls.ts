const GITHUB_BASE = 'https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main';
const GUIDE_SITE_BASE = 'https://cc.bruniaux.com/guide/ultimate-guide';

// Chapter slugs for guide/ultimate-guide.md (line ranges → chapter slug)
// Pattern: https://cc.bruniaux.com/guide/ultimate-guide/{chapter-slug}/#{section-anchor}
const CHAPTER_RANGES: Array<{ from: number; to: number; slug: string }> = [
  { from: 1,     to: 220,   slug: '00-introduction' },
  { from: 221,   to: 1378,  slug: '01-quick-start' },
  { from: 1379,  to: 4231,  slug: '02-core-workflow' },
  { from: 4232,  to: 5648,  slug: '03-memory-files' },
  { from: 5649,  to: 6361,  slug: '04-agents' },
  { from: 6362,  to: 7470,  slug: '05-skills' },
  { from: 7471,  to: 8106,  slug: '06-commands' },
  { from: 8107,  to: 9482,  slug: '07-hooks' },
  { from: 9483,  to: 12118, slug: '08-mcp' },
  { from: 12119, to: 19831, slug: '09-advanced-patterns' },
  { from: 19832, to: 20760, slug: '10-reference' },
  { from: 20761, to: 21384, slug: '11-ai-ecosystem' },
  { from: 21385, to: Infinity, slug: '12-appendices' },
];

function lineToChapterSlug(line: number): string {
  for (const range of CHAPTER_RANGES) {
    if (line >= range.from && line <= range.to) return range.slug;
  }
  return '12-appendices';
}

export function githubUrl(filePath: string, line?: number): string {
  const base = `${GITHUB_BASE}/${filePath}`;
  return line ? `${base}#L${line}` : base;
}

// Only ultimate-guide.md is rendered as multi-chapter on the guide site
export function guideSiteUrl(filePath: string, line?: number): string | null {
  if (filePath !== 'guide/ultimate-guide.md') return null;
  if (!line) return `${GUIDE_SITE_BASE}/`;
  const chapterSlug = lineToChapterSlug(line);
  return `${GUIDE_SITE_BASE}/${chapterSlug}/`;
}

export function formatLinks(filePath: string, line?: number): string {
  const gh = githubUrl(filePath, line);
  const site = guideSiteUrl(filePath, line);
  const parts = [`GitHub: ${gh}`];
  if (site) parts.push(`Guide: ${site}`);
  return parts.join(' | ');
}
