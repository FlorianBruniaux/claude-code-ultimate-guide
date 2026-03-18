/**
 * Prompt Caching Test — Anthropic API
 *
 * Verifies that prompt caching is active on your Anthropic API key.
 * Runs 3 identical calls and checks that calls 2-3 read from cache.
 *
 * Usage:
 *   ANTHROPIC_API_KEY=sk-ant-... npx tsx test-prompt-caching.ts
 *
 * Requirements:
 *   - Node 18+ (native fetch)
 *   - No dependencies required
 *
 * Gotchas discovered in production (not in official docs):
 *   1. The `anthropic-beta: prompt-caching-2024-07-31` header is required
 *      even for Claude 4.x models — omitting it silently disables caching.
 *   2. The effective token threshold for Claude 4.x is ~2048+, not the
 *      documented 1024. Blocks below this threshold return write=0 with no warning.
 *   3. Cached tokens are excluded from `input_tokens` in the response.
 *      Track `cache_creation_input_tokens` and `cache_read_input_tokens` instead.
 *   4. The new API format exposes a nested `cache_creation` object with
 *      `ephemeral_5m_input_tokens` (5-min TTL) and `ephemeral_1h_input_tokens` (1-hour TTL).
 */

const API_KEY = process.env.ANTHROPIC_API_KEY;
if (!API_KEY) {
  console.error("Error: ANTHROPIC_API_KEY environment variable is not set.");
  process.exit(1);
}

// Stable system prompt — must exceed the effective cache threshold (~2048 tokens for Claude 4.x).
// In real usage: consolidate agent rules, platform context, and static instructions into one block.
const STABLE_SYSTEM_PROMPT = `
You are a helpful assistant.

Core rules:
- Be concise and accurate
- Cite sources when referencing external content
- Match the language of the user

Extended context (padding to exceed cache threshold):
${Array(200).fill("This platform helps users collaborate on tasks, track progress, and organize their workflow efficiently.").join(" ")}
`.trim();

type Usage = {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens?: number;
  cache_read_input_tokens?: number;
  cache_creation?: {
    ephemeral_5m_input_tokens?: number;
    ephemeral_1h_input_tokens?: number;
  };
};

async function callAPI(callIndex: number): Promise<Usage> {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": API_KEY!,
      "anthropic-version": "2023-06-01",
      // Required for all models, including Claude 4.x
      "anthropic-beta": "prompt-caching-2024-07-31",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 50,
      system: [
        {
          type: "text",
          text: STABLE_SYSTEM_PROMPT,
          // Mark this block for caching — must be the last or only system block
          cache_control: { type: "ephemeral" },
        },
      ],
      messages: [
        { role: "user", content: `Test call ${callIndex} — reply OK` },
      ],
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`API ${response.status}: ${body}`);
  }

  const data = (await response.json()) as { usage: Usage };
  return data.usage;
}

async function main() {
  console.log("Prompt Caching Test\n");

  let passed = true;

  for (let i = 1; i <= 3; i++) {
    const usage = await callAPI(i);

    const write = usage.cache_creation_input_tokens ?? 0;
    const read = usage.cache_read_input_tokens ?? 0;

    let status: string;
    if (i === 1) {
      status = write > 0 ? "cache written" : "❌ write failed (check token threshold)";
      if (write === 0) passed = false;
    } else {
      status = read > 0 ? "✅ cache hit" : "❌ cache miss";
      if (read === 0) passed = false;
    }

    console.log(
      `Call ${i}:  write=${String(write).padStart(5)}  read=${String(read).padStart(5)}  input=${String(usage.input_tokens).padStart(4)}  — ${status}`
    );
  }

  console.log();
  if (passed) {
    console.log("Result: caching is working correctly.");
  } else {
    console.log("Result: caching is NOT working. Common causes:");
    console.log("  - Token threshold not met (try increasing STABLE_SYSTEM_PROMPT)");
    console.log("  - Missing beta header (anthropic-beta: prompt-caching-2024-07-31)");
    console.log("  - Account tier does not support caching");
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
