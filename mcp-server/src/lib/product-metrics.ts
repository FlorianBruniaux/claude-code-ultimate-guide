import { flattenReference, type IndexEntry } from './reference-flattener.js';

export function countReferenceEntries(raw: Record<string, unknown>): number {
  const entries: IndexEntry[] = [];
  flattenReference(raw, '', entries);
  return entries.length;
}
