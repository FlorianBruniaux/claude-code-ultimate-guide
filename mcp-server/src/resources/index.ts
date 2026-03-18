import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { getReferenceYamlRaw, getReleasesYamlRaw, loadLlmsTxt } from '../lib/content.js';

export function registerResources(server: McpServer): void {
  // Full reference YAML — the fallback when search isn't enough
  server.resource(
    'reference',
    'claude-code-guide://reference',
    {
      description: 'Complete structured index of the Claude Code Ultimate Guide (94KB YAML, ~900 entries). Use as fallback when search_guide() results are insufficient.',
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
}
