export interface ChangelogEntry {
  version: string;
  date: string;
  dateObj: Date;
  content: string;
}

export function parseChangelog(raw: string): ChangelogEntry[] {
  const entries: ChangelogEntry[] = [];
  // Match headers like: ## [3.27.0] - 2026-02-20  or  ## [Unreleased]
  const headerRe = /^## \[([^\]]+)\](?:\s*-\s*(\d{4}-\d{2}-\d{2}))?/m;
  const blocks = raw.split(/^(?=## \[)/m).filter((b) => b.trim());

  for (const block of blocks) {
    const match = block.match(headerRe);
    if (!match) continue;
    const version = match[1];
    const dateStr = match[2] ?? '';
    const dateObj = dateStr ? new Date(dateStr) : new Date(0);
    entries.push({ version, date: dateStr, dateObj, content: block.trim() });
  }

  return entries;
}

export function filterByPeriod(
  entries: ChangelogEntry[],
  period: 'day' | 'week' | 'month',
): ChangelogEntry[] {
  const MS = { day: 86_400_000, week: 7 * 86_400_000, month: 30 * 86_400_000 };
  const cutoff = Date.now() - MS[period];
  return entries.filter(
    // Include [Unreleased] (treat as today) + dated entries within the window
    (e) => e.version === 'Unreleased' || e.dateObj.getTime() >= cutoff,
  );
}
