import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerSearchGuide } from './tools/search-guide.js';
import { registerReadSection } from './tools/read-section.js';
import { registerListTopics } from './tools/list-topics.js';
import { registerGetExample } from './tools/get-example.js';
import { registerChangelog } from './tools/changelog.js';
import { registerCheatsheet } from './tools/cheatsheet.js';
import { registerListExamples } from './tools/list-examples.js';
import { registerReleases } from './tools/releases.js';
import { registerCompareVersions } from './tools/compare-versions.js';
import { registerGetThreat, registerListThreats } from './tools/threats.js';
import { registerSearchExamples } from './tools/search-examples.js';
import { registerOfficialDocs } from './tools/official-docs.js';
import { registerResources } from './resources/index.js';
import { registerPrompts } from './prompts/index.js';
import { loadReference, loadReleases, isDevMode } from './lib/content.js';

export function createServer(): McpServer {
  const server = new McpServer({
    name: 'claude-code-ultimate-guide',
    version: '1.0.0',
  });

  // Pre-load YAML indexes into memory at startup
  try {
    const ref = loadReference();
    const releases = loadReleases();
    const mode = isDevMode() ? 'dev (local files)' : 'production (GitHub lazy fetch)';
    process.stderr.write(
      `[claude-code-guide] Loaded ${ref.entries.length} index entries | ${releases.releases.length} releases | mode: ${mode}\n`,
    );
  } catch (err) {
    process.stderr.write(`[claude-code-guide] Warning: Failed to pre-load indexes: ${err}\n`);
  }

  // Register all tools
  registerSearchGuide(server);
  registerReadSection(server);
  registerListTopics(server);
  registerGetExample(server);
  registerChangelog(server);
  registerCheatsheet(server);
  registerListExamples(server);
  registerReleases(server);
  registerCompareVersions(server);
  registerGetThreat(server);
  registerListThreats(server);
  registerSearchExamples(server);
  registerOfficialDocs(server);

  // Register resources
  registerResources(server);

  // Register prompts
  registerPrompts(server);

  return server;
}
