import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import {
  getAgentHarnessesJsonRaw,
  getDistributionChannelsYamlRaw,
  getReferenceYamlRaw,
  getReleasesYamlRaw,
  getTranslationsJsonRaw,
  loadLlmsTxt,
} from '../lib/content.js';

export function registerResources(server: McpServer): void {
  // Full reference YAML — the fallback when search isn't enough
  server.resource(
    'reference',
    'claude-code-guide://reference',
    {
      description: 'Complete structured index of the Claude Code Ultimate Guide. Use as fallback when search_guide() results are insufficient.',
      mimeType: 'text/yaml',
    },
    async () => {
      const content = getReferenceYamlRaw();
      return {
        contents: [
          {
            uri: 'claude-code-guide://reference',
            mimeType: 'text/yaml',
            text: content,
          },
        ],
      };
    },
  );

  // Releases history
  server.resource(
    'releases',
    'claude-code-guide://releases',
    {
      description: 'Claude Code official releases history — condensed highlights and breaking changes for each version.',
      mimeType: 'text/yaml',
    },
    async () => {
      const content = getReleasesYamlRaw();
      return {
        contents: [
          {
            uri: 'claude-code-guide://releases',
            mimeType: 'text/yaml',
            text: content,
          },
        ],
      };
    },
  );

  // Guide identity file
  server.resource(
    'llms',
    'claude-code-guide://llms',
    {
      description: 'llms.txt — machine-readable identity and navigation file for the Claude Code Ultimate Guide.',
      mimeType: 'text/plain',
    },
    async () => {
      const content = loadLlmsTxt();
      return {
        contents: [
          {
            uri: 'claude-code-guide://llms',
            mimeType: 'text/plain',
            text: content,
          },
        ],
      };
    },
  );

  // Normalized cross-harness catalog
  server.resource(
    'agent-harnesses',
    'claude-code-guide://agent-harnesses',
    {
      description: 'Evidence-backed Agent Harness Map dataset. Separates the broad source catalog, guide supplements, strict runtime map, and adjacent control planes. Unknown evidence is preserved as unknown.',
      mimeType: 'application/json',
    },
    async () => {
      const content = getAgentHarnessesJsonRaw();
      return {
        contents: [
          {
            uri: 'claude-code-guide://agent-harnesses',
            mimeType: 'application/json',
            text: content,
          },
        ],
      };
    },
  );

  server.resource(
    'translations',
    'claude-code-guide://translations',
    {
      description: 'Version, provenance, freshness, and coverage status for maintained and community translations of the guide.',
      mimeType: 'application/json',
    },
    async () => {
      const content = getTranslationsJsonRaw();
      return {
        contents: [
          {
            uri: 'claude-code-guide://translations',
            mimeType: 'application/json',
            text: content,
          },
        ],
      };
    },
  );

  server.resource(
    'distribution-channels',
    'claude-code-guide://distribution-channels',
    {
      description: 'Publication channels, attributed URLs, asset states, dates, and 30-day outcome fields for the guide.',
      mimeType: 'text/yaml',
    },
    async () => {
      const content = getDistributionChannelsYamlRaw();
      return {
        contents: [
          {
            uri: 'claude-code-guide://distribution-channels',
            mimeType: 'text/yaml',
            text: content,
          },
        ],
      };
    },
  );
}
