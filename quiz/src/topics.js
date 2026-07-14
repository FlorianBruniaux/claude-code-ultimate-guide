export const TOPICS = Object.freeze({
  1: 'Quick Start & Installation',
  2: 'Core Concepts',
  3: 'Memory & Settings',
  4: 'Agents',
  5: 'Skills',
  6: 'Commands',
  7: 'Hooks',
  8: 'MCP Servers',
  9: 'Advanced Patterns',
  10: 'Reference & Troubleshooting',
  11: 'Learning with AI',
  12: 'Architecture Internals',
  13: 'Security Hardening',
  14: 'Privacy & Observability',
  15: 'AI Ecosystem',
  16: 'Agent Harness & Context',
  17: 'Team Metrics for AI-Augmented Engineering'
});

export const TOPIC_IDS = Object.freeze(Object.keys(TOPICS).map(Number));

export function parseTopicIds(value) {
  return value
    .split(',')
    .map(topic => parseInt(topic.trim(), 10))
    .filter(topic => TOPIC_IDS.includes(topic));
}
