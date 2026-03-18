import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import { loadThreatDb } from '../lib/content.js';
import { githubUrl } from '../lib/urls.js';

const THREAT_DB_GITHUB = githubUrl('examples/commands/resources/threat-db.yaml');

interface CveEntry {
  id: string;
  component: string;
  severity: string;
  cvss?: number;
  description: string;
  source: string;
  fixed_in?: string;
  mitigation?: string;
  notes?: string;
}

interface TechniqueEntry {
  id: string;
  name: string;
  description: string;
  examples?: string[];
  campaigns?: string[];
  cves?: string[];
  mitigation?: string;
}

const CATEGORY_LABELS: Record<string, string> = {
  cves: 'CVE Database',
  authors: 'Malicious Authors',
  skills: 'Malicious Skills',
  techniques: 'Attack Techniques',
  mitigations: 'Minimum Safe Versions',
  sources: 'Research Sources',
};

export function registerGetThreat(server: McpServer): void {
  server.tool(
    'get_threat',
    'Look up a specific threat by ID from the security threat database. Supports CVE IDs (e.g. "CVE-2025-53109") and technique IDs (e.g. "T001").',
    {
      id: z.string().describe('Threat ID: a CVE identifier (e.g. "CVE-2025-53109") or attack technique ID (e.g. "T001")'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ id }) => {
      const db = await loadThreatDb();
      const idUpper = id.toUpperCase();

      // Search CVE database
      const cve = (db.cve_database as CveEntry[]).find(
        (c) => c.id.toUpperCase() === idUpper,
      );
      if (cve) {
        const lines = [
          `# ${cve.id} — ${cve.component}`,
          THREAT_DB_GITHUB,
          '',
          `**Severity**: ${cve.severity.toUpperCase()}${cve.cvss ? ` (CVSS ${cve.cvss})` : ''}`,
          `**Component**: ${cve.component}`,
          `**Source**: ${cve.source}`,
          '',
          `## Description`,
          cve.description,
        ];

        if (cve.fixed_in) {
          lines.push('', `**Fixed in**: ${cve.fixed_in}`);
        }
        if (cve.mitigation) {
          lines.push('', `## Mitigation`, cve.mitigation);
        }
        if (cve.notes) {
          lines.push('', `## Notes`, cve.notes);
        }

        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      // Search attack techniques
      const technique = (db.attack_techniques as TechniqueEntry[]).find(
        (t) => t.id.toUpperCase() === idUpper,
      );
      if (technique) {
        const lines = [
          `# ${technique.id} — ${technique.name}`,
          THREAT_DB_GITHUB,
          '',
          `## Description`,
          technique.description,
        ];

        if (technique.examples?.length) {
          lines.push('', '## Examples');
          for (const ex of technique.examples) lines.push(`- ${ex}`);
        }
        if (technique.campaigns?.length) {
          lines.push('', `**Campaigns**: ${technique.campaigns.join(', ')}`);
        }
        if (technique.cves?.length) {
          lines.push(`**Related CVEs**: ${technique.cves.join(', ')}`);
        }
        if (technique.mitigation) {
          lines.push('', `## Mitigation`, technique.mitigation);
        }

        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      return {
        content: [{
          type: 'text',
          text: [
            `Threat ID "${id}" not found in the database.`,
            '',
            'Supported formats:',
            '  • CVE IDs: CVE-2025-53109, CVE-2026-24052, ...',
            '  • Technique IDs: T001, T002, ...',
            '',
            `Use list_threats("cves") or list_threats("techniques") to browse all entries.`,
            `Full database: ${THREAT_DB_GITHUB}`,
          ].join('\n'),
        }],
      };
    },
  );
}

export function registerListThreats(server: McpServer): void {
  server.tool(
    'list_threats',
    'Browse the security threat database. Without a category, returns a summary with counts. With a category, returns the full list for that section.',
    {
      category: z.enum(['cves', 'authors', 'skills', 'techniques', 'mitigations', 'sources'])
        .optional()
        .describe('Section to list: cves | authors | skills | techniques | mitigations | sources. Omit for a global summary.'),
    },
    { readOnlyHint: true, destructiveHint: false, openWorldHint: false },
    async ({ category }) => {
      const db = await loadThreatDb();

      if (!category) {
        // Global summary
        const lines = [
          `# Threat Database Summary`,
          `Version ${db.version} — updated ${db.updated}`,
          THREAT_DB_GITHUB,
          '',
          '| Category | Count |',
          '|----------|-------|',
          `| CVEs | ${db.cve_database.length} |`,
          `| Malicious Authors | ${db.malicious_authors.length} |`,
          `| Malicious Skills | ${db.malicious_skills.length} |`,
          `| Attack Techniques | ${db.attack_techniques.length} |`,
          `| Minimum Safe Versions | ${Object.keys(db.minimum_safe_versions).length} |`,
          `| Research Sources | ${db.sources.length} |`,
          '',
          'Use list_threats(category) to browse a section, or get_threat(id) for details.',
          'Categories: cves | authors | skills | techniques | mitigations | sources',
        ];
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      const label = CATEGORY_LABELS[category] ?? category;

      if (category === 'cves') {
        const cves = db.cve_database as CveEntry[];
        const lines = [
          `# ${label} (${cves.length} entries)`,
          THREAT_DB_GITHUB,
          '',
        ];
        for (const c of cves) {
          lines.push(`## ${c.id} — ${c.component}`);
          lines.push(`**Severity**: ${c.severity.toUpperCase()}${c.cvss ? ` (CVSS ${c.cvss})` : ''} | **Source**: ${c.source}`);
          lines.push(c.description);
          if (c.fixed_in) lines.push(`Fixed in: ${c.fixed_in}`);
          if (c.mitigation) lines.push(`Mitigation: ${c.mitigation}`);
          lines.push('');
        }
        lines.push(`---\nUse get_threat("CVE-XXXX-XXXXX") for full details on any CVE.`);
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      if (category === 'techniques') {
        const techniques = db.attack_techniques as TechniqueEntry[];
        const lines = [
          `# ${label} (${techniques.length} entries)`,
          THREAT_DB_GITHUB,
          '',
        ];
        for (const t of techniques) {
          lines.push(`## ${t.id} — ${t.name}`);
          lines.push(t.description);
          if (t.mitigation) lines.push(`Mitigation: ${t.mitigation}`);
          lines.push('');
        }
        lines.push(`---\nUse get_threat("T001") for full details including examples and CVE links.`);
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      if (category === 'authors') {
        const authors = db.malicious_authors as Array<{ name: string; source?: string; notes?: string }>;
        const lines = [
          `# ${label} (${authors.length} confirmed)`,
          THREAT_DB_GITHUB,
          '',
          'Block ALL skills from these authors — confirmed malicious by security researchers.',
          '',
        ];
        for (const a of authors) {
          lines.push(`- **${a.name}**${a.source ? ` — ${a.source}` : ''}${a.notes ? ` (${a.notes})` : ''}`);
        }
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      if (category === 'skills') {
        const skills = db.malicious_skills as Array<{ name: string; type?: string; source?: string; risk?: string; notes?: string }>;
        const lines = [
          `# ${label} (${skills.length} entries)`,
          THREAT_DB_GITHUB,
          '',
        ];
        for (const s of skills) {
          const tags = [s.type, s.risk ? `risk:${s.risk}` : undefined].filter(Boolean).join(', ');
          lines.push(`- **${s.name}**${tags ? ` [${tags}]` : ''}${s.source ? ` — ${s.source}` : ''}${s.notes ? ` (${s.notes})` : ''}`);
        }
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      if (category === 'mitigations') {
        const versions = db.minimum_safe_versions;
        const entries = Object.entries(versions);
        const lines = [
          `# ${label} (${entries.length} entries)`,
          THREAT_DB_GITHUB,
          '',
        ];
        for (const [component, minVersion] of entries) {
          lines.push(`- **${component}**: >= ${minVersion}`);
        }
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      if (category === 'sources') {
        const sources = db.sources as Array<{ name: string; url?: string; date?: string }>;
        const lines = [
          `# ${label} (${sources.length} entries)`,
          THREAT_DB_GITHUB,
          '',
        ];
        for (const s of sources) {
          lines.push(`- **${s.name}**${s.date ? ` (${s.date})` : ''}${s.url ? `\n  ${s.url}` : ''}`);
        }
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      return {
        content: [{ type: 'text', text: `Unknown category: "${category}". Use: cves | authors | skills | techniques | mitigations | sources` }],
      };
    },
  );
}
