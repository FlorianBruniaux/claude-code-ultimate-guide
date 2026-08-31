import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

/** Collect only the public MCP list contract and always close its child process. */
export async function collectRuntimeSnapshot({ command, args, cwd }) {
  const transport = new StdioClientTransport({ command, args, cwd, stderr: 'pipe' })
  const client = new Client({ name: 'claude-code-guide-manifest', version: '1' })
  try {
    await client.connect(transport)
    const serverInfo = client.getServerVersion()
    if (serverInfo === undefined) throw new Error('MCP server did not return serverInfo')
    const [toolResult, resourceResult, promptResult] = await Promise.all([
      client.listTools(), client.listResources(), client.listPrompts(),
    ])
    return { serverInfo, tools: toolResult.tools, resources: resourceResult.resources, prompts: promptResult.prompts }
  } finally {
    await client.close()
  }
}
