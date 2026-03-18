import { readFileSync } from 'fs';
import { resolve, join, sep } from 'path';
import { parse as parseYaml } from 'yaml';
import { fileURLToPath } from 'url';
import { fetchFile } from './fetcher.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = resolve(__filename, '..');

// Dual mode: GUIDE_ROOT env var = local dev, else bundled content
const GUIDE_ROOT = process.env.GUIDE_ROOT
  ? resolve(process.env.GUIDE_ROOT)
  : null;

const CONTENT_DIR = GUIDE_ROOT
  ? resolve(GUIDE_ROOT, 'machine-readable')
  : resolve(__dirname, '../content');

const ALLOWED_EXTENSIONS = new Set([
  '.md', '.yaml', '.yml', '.sh', '.ts', '.js', '.json', '.py', '.txt',
]);

// ─── Types ───────────────────────────────────────────────────────────────────

export type DeepDiveTarget =
  | { type: 'line'; file: 'guide/ultimate-guide.md'; line: number }
  | { type: 'file'; path: string; line?: number }
  | { type: 'url'; url: string }
  | { type: 'inline'; text: string }
  | { type: 'structured'; data: unknown };

export interface IndexEntry {
  key: string;
  section: string;
  value: unknown;
  searchableText: string;
  target?: DeepDiveTarget;
}

export interface ReferenceData {
  version: string;
  entries: IndexEntry[];
  raw: Record<string, unknown>;
}

export interface ReleasesData {
  latest: string;
  updated: string;
  releases: unknown[];
  raw: Record<string, unknown>;
}

export interface ThreatDbData {
  version: string;
  updated: string;
  sources: unknown[];
  malicious_authors: unknown[];
  malicious_skills: unknown[];
  cve_database: unknown[];
  attack_techniques: unknown[];
  minimum_safe_versions: Record<string, string>;
  raw: Record<string, unknown>;
}

// ─── Path resolver ────────────────────────────────────────────────────────────

export function resolveContentPath(relativePath: string): string | null {
  const base = GUIDE_ROOT ?? resolve(__dirname, '../../..');

  // Layer 1: resolve and check starts with base
  const resolved = resolve(base, relativePath);
  if (!resolved.startsWith(base + sep)) return null;

  // Layer 2: extension whitelist
  const ext = relativePath.slice(relativePath.lastIndexOf('.'));
  if (!ALLOWED_EXTENSIONS.has(ext)) return null;

  return resolved;
}

export function isDevMode(): boolean {
  return GUIDE_ROOT !== null;
}

export function getGuideRoot(): string {
  return GUIDE_ROOT ?? resolve(__dirname, '../../..');
}

// ─── YAML cache ───────────────────────────────────────────────────────────────

let referenceCache: ReferenceData | null = null;
let releasesCache: ReleasesData | null = null;
let threatDbCache: ThreatDbData | null = null;

export function loadReference(): ReferenceData {
  if (referenceCache) return referenceCache;

  const filePath = join(CONTENT_DIR, 'reference.yaml');
  const raw = parseYaml(readFileSync(filePath, 'utf8')) as Record<string, unknown>;

  const entries: IndexEntry[] = [];
  flattenReference(raw, '', entries);

  referenceCache = {
    version: (raw.version as string) ?? 'unknown',
    entries,
    raw,
  };
  return referenceCache;
}

export function loadReleases(): ReleasesData {
  if (releasesCache) return releasesCache;

  const filePath = join(CONTENT_DIR, 'claude-code-releases.yaml');
  const raw = parseYaml(readFileSync(filePath, 'utf8')) as Record<string, unknown>;

  releasesCache = {
    latest: (raw.latest as string) ?? 'unknown',
    updated: (raw.updated as string) ?? 'unknown',
    releases: (raw.releases as unknown[]) ?? [],
    raw,
  };
  return releasesCache;
}

export async function loadThreatDb(): Promise<ThreatDbData> {
  if (threatDbCache) return threatDbCache;

  const THREAT_DB_PATH = 'examples/commands/resources/threat-db.yaml';
  let content: string;

  if (GUIDE_ROOT) {
    content = readFileSync(join(GUIDE_ROOT, THREAT_DB_PATH), 'utf8');
  } else {
    const fetched = await fetchFile(THREAT_DB_PATH);
    if (!fetched) throw new Error('Failed to load threat-db.yaml');
    content = fetched;
  }

  const raw = parseYaml(content) as Record<string, unknown>;

  threatDbCache = {
    version: (raw.version as string) ?? 'unknown',
    updated: (raw.updated as string) ?? 'unknown',
    sources: (raw.sources as unknown[]) ?? [],
    malicious_authors: (raw.malicious_authors as unknown[]) ?? [],
    malicious_skills: (raw.malicious_skills as unknown[]) ?? [],
    cve_database: (raw.cve_database as unknown[]) ?? [],
    attack_techniques: (raw.attack_techniques as unknown[]) ?? [],
    minimum_safe_versions: (raw.minimum_safe_versions as Record<string, string>) ?? {},
    raw,
  };
  return threatDbCache;
}

export function loadLlmsTxt(): string {
  const filePath = join(CONTENT_DIR, 'llms.txt');
  return readFileSync(filePath, 'utf8');
}

export function getReferenceYamlRaw(): string {
  const filePath = join(CONTENT_DIR, 'reference.yaml');
  return readFileSync(filePath, 'utf8');
}

export function getReleasesYamlRaw(): string {
  const filePath = join(CONTENT_DIR, 'claude-code-releases.yaml');
  return readFileSync(filePath, 'utf8');
}

// ─── Deep dive resolver ───────────────────────────────────────────────────────

export function resolveDeepDive(value: unknown): DeepDiveTarget | undefined {
  if (value === null || value === undefined) return undefined;

  if (typeof value === 'number') {
    return { type: 'line', file: 'guide/ultimate-guide.md', line: value };
  }

  if (typeof value === 'string') {
    if (value.startsWith('http://') || value.startsWith('https://')) {
      return { type: 'url', url: value };
    }
    // File path with optional :line suffix
    const filePathMatch = value.match(/^(guide\/|examples\/|whitepapers\/|machine-readable\/)(.+?)(?::(\d+))?$/);
    if (filePathMatch) {
      return {
        type: 'file',
        path: filePathMatch[1] + filePathMatch[2],
        line: filePathMatch[3] ? parseInt(filePathMatch[3], 10) : undefined,
      };
    }
    return { type: 'inline', text: value };
  }

  if (typeof value === 'object') {
    return { type: 'structured', data: value };
  }

  return { type: 'inline', text: String(value) };
}

// ─── Reference flattener ──────────────────────────────────────────────────────

function flattenReference(
  obj: Record<string, unknown>,
  prefix: string,
  entries: IndexEntry[],
): void {
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}_${key}` : key;

    if (key === 'version' || key === 'generated' || key === 'description' || key === 'note') {
      continue;
    }

    if (value === null || value === undefined) continue;

    if (typeof value === 'object' && !Array.isArray(value)) {
      const obj2 = value as Record<string, unknown>;
      // Check if it's a leaf-like object (has deep_dive or simple scalar values)
      const hasDeepDive = 'deep_dive' in obj2;
      const hasNestedObjects = Object.values(obj2).some(
        (v) => typeof v === 'object' && v !== null && !Array.isArray(v) && !('deep_dive' in (v as Record<string, unknown>)),
      );

      if (hasDeepDive || !hasNestedObjects) {
        // Treat as leaf entry
        const searchableText = buildSearchableText(fullKey, value);
        const target = hasDeepDive
          ? resolveDeepDive((obj2 as Record<string, unknown>).deep_dive)
          : resolveDeepDive(value);

        entries.push({
          key: fullKey,
          section: prefix.split('_')[0] ?? fullKey,
          value,
          searchableText,
          target,
        });
      } else {
        flattenReference(obj2, fullKey, entries);
      }
    } else {
      const searchableText = buildSearchableText(fullKey, value);
      const target = resolveDeepDive(value);
      entries.push({
        key: fullKey,
        section: prefix.split('_')[0] ?? fullKey,
        value,
        searchableText,
        target,
      });
    }
  }
}

function buildSearchableText(key: string, value: unknown): string {
  const parts: string[] = [key.replace(/_/g, ' ')];

  if (typeof value === 'string') {
    parts.push(value);
  } else if (typeof value === 'number') {
    parts.push(String(value));
  } else if (Array.isArray(value)) {
    for (const item of value) {
      if (typeof item === 'string') parts.push(item);
      else if (typeof item === 'object' && item !== null) {
        parts.push(JSON.stringify(item));
      }
    }
  } else if (typeof value === 'object' && value !== null) {
    parts.push(JSON.stringify(value));
  }

  return parts.join(' ').toLowerCase();
}
