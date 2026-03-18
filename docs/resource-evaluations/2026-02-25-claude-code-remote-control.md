# Resource Evaluation: Claude Code Remote Control

**Date**: 2026-02-25
**Evaluator**: Claude (claude-sonnet-4-6)
**Status**: Completed

---

## Metadata

| Field | Value |
|-------|-------|
| **URL** | https://code.claude.com/docs/en/remote-control |
| **Type** | Official Anthropic documentation + feature announcement |
| **Date** | 2026-02-25 |
| **Score** | 4/5 |
| **Decision** | Integrate this week |

---

## 1. Content Summary

Remote Control allows continuing a local Claude Code session from a phone, tablet, or web browser (claude.ai/code or Claude mobile app on iOS/Android).

**Two activation modes:**
- `claude remote-control` — new CLI subcommand
- `/remote-control` or `/rc` — slash command from an active session

**Key architecture:**
- Execution is 100% local — the terminal does all the work
- Mobile/web interface is a remote window onto the local session
- HTTPS outbound only, zero inbound ports, short-lived scoped credentials

**Availability:** Research Preview on Pro and Max plans. NOT available on Team, Enterprise, or API keys.

**Features:** QR code + session URL for fast connection, auto-enable via `/config`, `/mobile` command for app download links.

**Limitations:** 1 remote session at a time, terminal must stay open, ~10min network timeout.

---

## 2. Relevance Score

**Score: 4/5 — Very Relevant (significant improvement)**

| Score | Meaning |
|-------|---------|
| 5 | Essential — Major gap in the guide |
| **4** | **Very relevant — Significant improvement** |
| 3 | Relevant — Useful complement |
| 2 | Marginal — Secondary info |
| 1 | Out of scope — Not relevant |

**Justification:**
- Feature entirely new, zero coverage in ultimate-guide.md
- Partially tracked in releases tracker (v2.1.51 and v2.1.53)
- Introduces a new access paradigm (local execution + remote UI)
- HOWEVER: research preview (not GA), limited Pro/Max scope, potentially unstable API

---

## 3. Gap Analysis

| Aspect | Doc officielle Anthropic | Notre guide |
|--------|--------------------------|-------------|
| Remote Control feature | Complete detailed doc | Zero mention in ultimate-guide.md |
| `claude remote-control` command | Documented with flags | Missing from cheatsheet |
| `/rc` and `/remote-control` slash commands | Documented | Missing |
| Security model | Detailed (HTTPS outbound, credentials) | Not covered |
| Difference vs "Claude Code on the Web" | Clear comparison table | Not covered |
| QR code + session URL | Detailed workflow | Not covered |
| Config auto-enable | Via `/config` | Not covered |
| Releases tracker | v2.1.51 and v2.1.53 | Already up to date |
| `/mobile` command | Mentioned | Missing from guide |

---

## 4. Integration Recommendations

### Files to modify

| File | Action | Priority |
|------|--------|----------|
| `guide/ultimate-guide.md` | New section 9.22 "Remote Control" | High |
| `guide/cheatsheet.md` | Add `/remote-control`, `/rc`, `/mobile` to command table | High |
| `machine-readable/reference.yaml` | Add `remote-control` entry with target line | High |
| `guide/security-hardening.md` | Note on security implications of remote access | Medium |

### Content to document

1. **What is Remote Control** — definition, difference vs "Claude Code on the Web" and vs Teleportation
2. **Setup** — requirements (Pro/Max, /login, workspace trust)
3. **Two workflows** — `claude remote-control` (CLI) vs `/rc` (from session)
4. **Connection** — QR code, URL, mobile app, session list
5. **Config** — auto-enable via `/config`
6. **Security** — outbound-only model, scoped credentials
7. **Limitations** — 1 session, terminal open, 10min timeout, **slash commands don't work in remote UI**
8. **Disclaimer** — Research Preview clearly noted

---

## 5. Challenge (Technical Review)

**Score adjusted: 4/5** (down from 5)

**Reasons for downgrade:**
- Research preview, not GA → risk of documenting content that changes
- Restricted Pro/Max scope → majority of pro users (Team/Enterprise) don't have access
- Official Anthropic docs already accessible → guide isn't first source for early adopters

**Points missed in initial eval:**
- Distinction between CLI workflow (`claude remote-control` with `--verbose`, `--sandbox` flags) vs slash command (`/rc` without flags)
- Impact for enterprise environments with proxy/VPN/restrictive firewall
- `/mobile` command to download Claude app (mentioned in doc, not in our guide)
- Comparison with existing alternatives (SSH + mobile terminal, tmux, VS Code remote)

**Non-integration risks:**
- Short term (1-2 weeks): low, early adopters read Anthropic docs
- Medium term (1 month): moderate if feature goes GA
- Long term: high if remote-control becomes standard interaction mode

**Main risk: over-documenting an unstable preview** → solution: document with clear "Research Preview" disclaimer

---

## 6. Fact-Check

| Claim | Verified | Source |
|-------|----------|--------|
| Available on Pro and Max | ✅ | Official doc + Perplexity (multiple sources) |
| Research preview | ✅ | Official doc ("research preview") |
| Not Team/Enterprise | ✅ | Official doc ("not available on Team or Enterprise") |
| HTTPS outbound only | ✅ | Official doc ("never opens inbound ports") |
| Timeout ~10 min | ✅ | Official doc ("more than roughly 10 minutes") |
| v2.1.51 first mention | ✅ | claude-code-releases.yaml line 47 |
| `/rc` alias for `/remote-control` | ✅ | Official doc |
| QR code via spacebar | ✅ | Official doc ("press spacebar to show a QR code") |
| Claude app iOS + Android | ✅ | Official doc (App Store + Play Store links) |
| "$2.5B annualized revenue" (Perplexity) | ❌ Not verifiable | MLQ.ai article claim, not in official doc. Ignored. |
| "29M daily VS Code installations" (Perplexity) | ❌ Not verifiable | Article claim, not in official doc. Ignored. |

---

## 7. Community Articles Found

| Source | Title | Date | Type |
|--------|-------|------|------|
| HelpNetSecurity | "Anthropic's Remote Control feature brings Claude Code to mobile" | 2026-02-25 | Press article |
| TechRadar | "Anthropic reveals Remote Control, a mobile version of Claude Code" | 2026-02-25 | Press article |
| MLQ.ai | "Anthropic Launches Remote Control Feature for Claude Code" | 2026-02-25 | Tech article |
| AwesomeAgents.ai | "Claude Code Gets Remote Control" | 2026-02-24 | Tech article |
| YouTube | "RIP OpenClaw!? This New Claude Code Feature is CRAZY!" | 2026-02-25 | Video |
| YouTube | "Claude Code Just Destroyed OpenClaw (new /remote-control)" | 2026-02-24 | Video |
| Binance Square | "Claude Code Introduces Remote Control Feature for Max Users" | 2026-02-25 | News |

**Observations:** Significant community buzz. Several articles compare to OpenClaw (open-source alternative that Remote Control may make obsolete). Significant press coverage for a preview feature.

---

## 8. Community Feedback (FR Slack, 2026-02-25)

Source: French-speaking developer Slack discussion (~15 messages, 7 participants)

### Field Insights (Not in Official Docs)

| Observation | Impact on guide |
|-------------|-----------------|
| Bash/AskUserQuestion permissions appear on the phone | Document: mobile serves as an approval terminal |
| Slash commands (`/new`, `/compact`) DON'T WORK in remote — treated as plain text | **Major limitation missing from official docs** |
| Skills ARE loaded on demand in remote | Positive: skills work |
| Works on remote VM (Clever Cloud) in tmux | Advanced use case to document |
| Multi-session workaround: multiple tmux tabs, each with own claude session | Pattern to document (bypasses single-session limit) |
| Server setup: 6-8 Claude sessions in tmux, no interruption while traveling | Advanced architecture to document |
| happy.engineering = main open-source alternative now "obsolete" | Mention in comparison |

### Security Concerns (Senior Devs)

| Concern | Analysis |
|---------|----------|
| "C'est une sacree RCE qu'ils introduisent là" (Frédéric C.) | True: session URL = live access key to local terminal. Real attack surface. |
| "Mon CISO va bientôt me challenger" (Mat F.) | Enterprise implication: even on personal plan, if used on corporate machine |
| Per-command permissions limit risk but "an attacker would say yes to everything" | Valid nuance: mobile approval guards against unintentional actions, not active attacker |
| Suggestion: use on "hardened trusted workstation à la Chromebook" | Best practice to document |

### Overall Sentiment

- **Strong enthusiasm**: "KILLER FEATURE", "finally", "here it is"
- **Immediate adoption**: several tested it within hours of announcement
- **Alternatives made obsolete**: happy.engineering, SSH/VPS hacks, OpenClaw
- **Perceived maturity**: "quite limited for now" (Hubert), single-session, no slash commands
- **Adoption score**: 8/10 (enthusiasm) but 5/10 (current maturity)

---

## 9. Final Decision

- **Final score**: 4/5
- **Action**: Integrate this week with "Research Preview" disclaimer
- **Confidence**: High (official doc verified, community feedback confirmed, multiple press sources)

### Added Value vs Official Doc

Thanks to community feedback, the guide can provide **original content** not in Anthropic docs:

1. **Slash commands limitation in remote** (`/new`, `/compact` treated as text) — undocumented
2. **tmux multi-session pattern** to bypass single-session limit
3. **Permanent server architecture**: tmux + remote VM + remote-control
4. **Community security analysis**: RCE surface, CISO implications, best practices (hardened workstation)
5. **Alternatives comparison**: happy.engineering, OpenClaw, SSH tunnels, VPS setups
