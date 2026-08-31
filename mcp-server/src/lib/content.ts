import { readFileSync } from 'fs';
import { resolve, join, sep } from 'path';
import { parse as parseYaml } from 'yaml';
import { fileURLToPath } from 'url';
import { fetchFile } from './fetcher.js';
import { flattenReference, type DeepDiveTarget, type IndexEntry } from './reference-flattener.js';

export type { DeepDiveTarget, IndexEntry } from './reference-flattener.js';
export { resolveDeepDive } from './reference-flattener.js';

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

export function getAgentHarnessesJsonRaw(): string {
  const filePath = join(CONTENT_DIR, 'agent-harnesses.json');
  return readFileSync(filePath, 'utf8');
}

export function getTranslationsJsonRaw(): string {
  const filePath = join(CONTENT_DIR, 'translations.json');
  return readFileSync(filePath, 'utf8');
}

// ─── Deep dive resolver ───────────────────────────────────────────────────────
