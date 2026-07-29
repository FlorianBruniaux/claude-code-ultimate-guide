import { readFileSync, existsSync } from 'fs';
import { resolveContentPath, isDevMode } from './content.js';
import { fetchFile } from './fetcher.js';

export interface SectionResult {
  content: string;
  startLine: number;
  endLine: number;
  totalLines: number;
  hasMore: boolean;
  nextOffset: number | null;
}

// Thrown when a "#slug" anchor in a path does not match any heading in the
// target file. Carries a few near-miss headings so the caller can suggest
// alternatives instead of just failing.
export class AnchorNotFoundError extends Error {
  constructor(
    public readonly filePath: string,
    public readonly slug: string,
    public readonly nearMisses: string[],
  ) {
    super(`Anchor "#${slug}" not found in "${filePath}".`);
    this.name = 'AnchorNotFoundError';
  }
}

const MAX_LINES = 500;

// ─── Heading level detector ───────────────────────────────────────────────────

function getHeadingLevel(line: string): number | null {
  const match = line.match(/^(#{1,6})\s/);
  return match ? match[1].length : null;
}

// ─── Code fence tracking ───────────────────────────────────────────────────────

// A CommonMark-correct fence toggle, shared by extractSection's boundary
// detection and collectHeadings' scan. A line only OPENS a fence when we
// are not already inside one (info string like "```bash" allowed). Once
// inside a fence, only a line that is *nothing but* backticks closes it,
// a line like "```markdown" appearing inside an already-open fence (e.g. a
// doc illustrating fence syntax) is literal content, not a close. The naive
// "any ``` line toggles" version used before this function existed could
// desync on exactly that pattern and silently swallow the rest of the file
// as "inside a code fence", hiding real headings from both readers.
function isFenceMarker(line: string, currentlyInFence: boolean): boolean {
  const trimmed = line.trim();
  if (!currentlyInFence) return trimmed.startsWith('```');
  return /^`{3,}$/.test(trimmed);
}

// ─── Anchor helpers ────────────────────────────────────────────────────────────

// Splits a "path#slug" reference on the first '#'. Returns the anchor as
// null when the path has no '#'. Only the first '#' is treated as the
// separator; anchor text is not expected to contain '#' itself.
export function splitAnchor(path: string): { file: string; slug: string | null } {
  const i = path.indexOf('#');
  if (i === -1) return { file: path, slug: null };
  return { file: path.slice(0, i), slug: path.slice(i + 1) };
}

// Explicit heading id, Pandoc/kramdown-style: "### Some Heading {#custom-id}".
// When present it overrides the computed GitHub-style slug for that heading.
const EXPLICIT_ID_RE = /\s*\{#([a-z0-9-]+)\}\s*$/i;

// GitHub-style heading slug. Lowercases, strips any character that is not
// a letter (any script), digit, underscore, space, or hyphen, then converts
// each remaining space to a hyphen. Note this does NOT collapse consecutive
// spaces/hyphens: GitHub's own slugger doesn't either, so a heading like
// "Trinity: A + B" (with a stripped token between two spaces) legitimately
// slugs to "trinity--a--b". Letters/digits use Unicode properties (not
// a-z0-9 only) so accented headings ("Accès", "où") keep their characters
// instead of having them silently dropped. Underscores are kept as-is
// (GitHub preserves them, e.g. a heading naming "ANTHROPIC_API_KEY" or
// "max_turns" slugs with the underscore intact). A heading that opens with
// an emoji (stripped by the character filter, since it's neither a letter
// nor a digit) would otherwise leave a leading space that turns into a
// leading hyphen once spaces become hyphens, so the leading/trailing
// whitespace is trimmed first, and leading/trailing hyphens are trimmed
// from the result too, matching GitHub's own behavior.
function slugifyHeading(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\p{L}\p{N}_ -]/gu, '')
    .trim()
    .replace(/ /g, '-')
    .replace(/^-+|-+$/g, '');
}

interface HeadingRef {
  line: number; // 1-based
  level: number;
  text: string;
  slug: string;
}

// Collects headings outside of code fences, deduplicating slugs the way
// GitHub does (second+ occurrence gets a "-1", "-2", ... suffix).
function collectHeadings(lines: string[]): HeadingRef[] {
  const headings: HeadingRef[] = [];
  const seen = new Map<string, number>();
  let inCodeFence = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (isFenceMarker(line, inCodeFence)) {
      inCodeFence = !inCodeFence;
      continue;
    }
    if (inCodeFence) continue;

    const level = getHeadingLevel(line);
    if (level === null) continue;

    // getHeadingLevel only matches "^#{1,6}\s", so the heading marker is
    // always at the start of the line with no leading whitespace.
    let text = line.slice(level).trim();

    const explicitId = text.match(EXPLICIT_ID_RE);
    let slug: string;
    if (explicitId) {
      text = text.replace(EXPLICIT_ID_RE, '').trim();
      slug = explicitId[1].toLowerCase();
    } else {
      slug = slugifyHeading(text);
    }

    const priorCount = seen.get(slug) ?? 0;
    if (priorCount > 0) {
      seen.set(slug, priorCount + 1);
      slug = `${slug}-${priorCount}`;
    } else {
      seen.set(slug, 1);
    }

    headings.push({ line: i + 1, level, text, slug });
  }

  return headings;
}

// Resolves a slug to its heading's line number within the given lines.
// Throws AnchorNotFoundError (with near-miss headings) if nothing matches.
export function resolveAnchorLine(lines: string[], filePath: string, slug: string): number {
  const headings = collectHeadings(lines);
  const match = headings.find((h) => h.slug === slug);
  if (match) return match.line;

  const nearMisses = headings
    .map((h) => ({ h, dist: levenshtein(slug, h.slug) }))
    .sort((a, b) => a.dist - b.dist)
    .slice(0, 5)
    .map(({ h }) => `#${h.slug} ("${h.text}", line ${h.line})`);

  throw new AnchorNotFoundError(filePath, slug, nearMisses);
}

// Small Levenshtein distance, capped for very different lengths, used only
// to rank near-miss anchor suggestions (not for correctness).
function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
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

// ─── Section extraction ───────────────────────────────────────────────────────

export function extractSection(
  lines: string[],
  offset: number,
  limit: number,
): SectionResult {
  const totalLines = lines.length;
  const startLine = Math.max(1, Math.min(offset, totalLines));
  const effectiveLimit = Math.min(limit, MAX_LINES);

  // Find heading level of starting section (for boundary detection)
  let sectionLevel: number | null = null;
  for (let i = startLine - 1; i < Math.min(startLine + 5, totalLines); i++) {
    const level = getHeadingLevel(lines[i]);
    if (level !== null) {
      sectionLevel = level;
      break;
    }
  }

  let inCodeFence = false;
  let endLine = startLine - 1;
  const collected: string[] = [];

  for (let i = startLine - 1; i < totalLines && collected.length < effectiveLimit; i++) {
    const line = lines[i];

    // Track code fences
    if (isFenceMarker(line, inCodeFence)) {
      inCodeFence = !inCodeFence;
    }

    // Check heading boundary (only outside code fences, only same/higher level)
    if (!inCodeFence && i > startLine - 1 && sectionLevel !== null) {
      const level = getHeadingLevel(line);
      if (level !== null && level <= sectionLevel) {
        break; // Stop at same or higher heading
      }
    }

    collected.push(line);
    endLine = i + 1;
  }

  const hasMore = endLine < totalLines && collected.length >= effectiveLimit;

  return {
    content: collected.join('\n'),
    startLine,
    endLine,
    totalLines,
    hasMore,
    nextOffset: hasMore ? endLine + 1 : null,
  };
}

// ─── Public API ───────────────────────────────────────────────────────────────

// Accepts either a plain path ("guide/foo.md") or a path with a heading
// anchor ("guide/foo.md#some-slug"). For an anchor path, offset is ignored
// and the section starts at the resolved heading; limit still applies.
// Throws AnchorNotFoundError if the anchor doesn't match any heading.
export async function readSection(
  rawPath: string,
  offset = 1,
  limit = MAX_LINES,
): Promise<SectionResult | null> {
  const { file: filePath, slug } = splitAnchor(rawPath);
  let content: string | null = null;

  if (isDevMode()) {
    // Dev mode: read from local filesystem
    const resolved = resolveContentPath(filePath);
    if (!resolved || !existsSync(resolved)) return null;
    content = readFileSync(resolved, 'utf8');
  } else {
    // Production: fetch from GitHub (with cache)
    content = await fetchFile(filePath);
  }

  if (content === null) return null;

  const lines = content.split('\n');
  const startLine = slug === null ? offset : resolveAnchorLine(lines, filePath, slug);
  return extractSection(lines, startLine, limit);
}
