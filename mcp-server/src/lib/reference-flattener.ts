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

export function resolveDeepDive(value: unknown): DeepDiveTarget | undefined {
  if (value === null || value === undefined) return undefined;
  if (typeof value === 'number') return { type: 'line', file: 'guide/ultimate-guide.md', line: value };
  if (typeof value === 'string') {
    if (value.startsWith('http://') || value.startsWith('https://')) return { type: 'url', url: value };
    const filePathMatch = value.match(/^(guide\/|examples\/|whitepapers\/|machine-readable\/)(.+?)(?::(\d+))?$/);
    if (filePathMatch) {
      return { type: 'file', path: filePathMatch[1] + filePathMatch[2], line: filePathMatch[3] ? parseInt(filePathMatch[3], 10) : undefined };
    }
    return { type: 'inline', text: value };
  }
  if (typeof value === 'object') return { type: 'structured', data: value };
  return { type: 'inline', text: String(value) };
}

export function buildSearchableText(key: string, value: unknown): string {
  const parts: string[] = [key.replace(/_/g, ' ')];
  if (typeof value === 'string') parts.push(value);
  else if (typeof value === 'number') parts.push(String(value));
  else if (Array.isArray(value)) {
    for (const item of value) {
      if (typeof item === 'string') parts.push(item);
      else if (typeof item === 'object' && item !== null) parts.push(JSON.stringify(item));
    }
  } else if (typeof value === 'object' && value !== null) {
    parts.push(JSON.stringify(value));
  }
  return parts.join(' ').toLowerCase();
}

export function flattenReference(obj: Record<string, unknown>, prefix: string, entries: IndexEntry[]): void {
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}_${key}` : key;
    if (key === 'version' || key === 'generated' || key === 'description' || key === 'note') continue;
    if (value === null || value === undefined) continue;
    if (typeof value === 'object' && !Array.isArray(value)) {
      const child = value as Record<string, unknown>;
      const hasDeepDive = 'deep_dive' in child;
      const hasNestedObjects = Object.values(child).some(
        (nested) => typeof nested === 'object' && nested !== null && !Array.isArray(nested) && !('deep_dive' in (nested as Record<string, unknown>)),
      );
      if (hasDeepDive || !hasNestedObjects) {
        entries.push({ key: fullKey, section: prefix.split('_')[0] ?? fullKey, value, searchableText: buildSearchableText(fullKey, value), target: hasDeepDive ? resolveDeepDive(child.deep_dive) : resolveDeepDive(value) });
      } else {
        flattenReference(child, fullKey, entries);
      }
    } else {
      entries.push({ key: fullKey, section: prefix.split('_')[0] ?? fullKey, value, searchableText: buildSearchableText(fullKey, value), target: resolveDeepDive(value) });
    }
  }
}
