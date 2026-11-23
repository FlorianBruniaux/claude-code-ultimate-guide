# examples/commands

Custom commands were merged into skills. Every former command template now lives in [`examples/skills/`](../skills/) as `<name>/SKILL.md` and runs as `/<name>`.

This directory only keeps [`resources/threat-db.yaml`](resources/threat-db.yaml), the threat database read by the `security-check`, `security-audit` and `update-threat-db` skills. It stays at this path because published versions of the guide's MCP server fetch it from here.

Legacy `.claude/commands/*.md` files still load in Claude Code, with the same frontmatter as skills except `name` and `paths`. Write new ones as skills: see [§6 Commands](../../guide/ultimate-guide.md#6-commands-user-invocable-skills).
