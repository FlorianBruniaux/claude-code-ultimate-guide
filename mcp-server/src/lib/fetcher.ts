import { existsSync, mkdirSync, readFileSync, writeFileSync, statSync } from 'fs';
import { resolve, dirname } from 'path';
import { homedir } from 'os';
import { createHash } from 'crypto';

const PACKAGE_VERSION = '1.0.0';
const GITHUB_RAW_BASE =
  'https://raw.githubusercontent.com/FlorianBruniaux/claude-code-ultimate-guide/main';
const CACHE_DIR = resolve(homedir(), '.cache', 'claude-code-guide', PACKAGE_VERSION);
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24h

function getCachePath(filePath: string): string {
  // Use hash to avoid path issues, but keep extension for readability
  const hash = createHash('md5').update(filePath).digest('hex').slice(0, 8);
  const safe = filePath.replace(/[^a-zA-Z0-9._-]/g, '_');
  return resolve(CACHE_DIR, `${hash}_${safe}`);
}

function isCacheValid(cachePath: string): boolean {
  if (!existsSync(cachePath)) return false;
  const stat = statSync(cachePath);
  return Date.now() - stat.mtimeMs < CACHE_TTL_MS;
}

export async function fetchFile(filePath: string): Promise<string | null> {
  // Normalize path separators
  const normalizedPath = filePath.replace(/\\/g, '/');
  const cachePath = getCachePath(normalizedPath);

  // Return cache if valid
  if (isCacheValid(cachePath)) {
    return readFileSync(cachePath, 'utf8');
  }

  // Fetch from GitHub
  const url = `${GITHUB_RAW_BASE}/${normalizedPath}`;
  try {
    const response = await fetch(url, {
      headers: { 'User-Agent': 'claude-code-ultimate-guide-mcp/1.0.0' },
      signal: AbortSignal.timeout(10_000),
    });

    if (!response.ok) {
      // Return stale cache if available (offline fallback)
      if (existsSync(cachePath)) {
        return readFileSync(cachePath, 'utf8');
      }
      return null;
    }

    const content = await response.text();

    // Write to cache
    mkdirSync(dirname(cachePath), { recursive: true });
    writeFileSync(cachePath, content, 'utf8');

    return content;
  } catch {
    // Offline fallback: return stale cache
    if (existsSync(cachePath)) {
      return readFileSync(cachePath, 'utf8');
    }
    return null;
  }
}

export function getCacheDir(): string {
  return CACHE_DIR;
}
