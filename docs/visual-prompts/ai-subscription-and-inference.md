# AI Subscription and Inference Visual Prompts

These prompts cover the multi-provider subscription strategy, Mistral deployment paths, gateway visibility, and agentic-tool selection. Generate one image per prompt. Review every rendered label before publication, resize the selected source to 1600 x 900, and convert it to WebP.

## Selection record

| Published asset | Gemini source | Status |
|---|---|---|
| `subscription-provider-portfolio.webp` | `Gemini_Generated_Image_m1miyom1miyom1mi.jpeg` | Selected and published |
| `mistral-deployment-paths.webp` | `Gemini_Generated_Image_xxlnb4xxlnb4xxln.jpeg` | Selected and published |
| `gateway-visibility-boundary.webp` | `Gemini_Generated_Image_x9ycs7x9ycs7x9yc.jpeg` | Selected and published |
| `agentic-tool-selection-map.webp` | `Gemini_Generated_Image_sfqljesfqljesfql.jpeg` | Rejected: the unrequested pretitle misspells `EDITORIAL` as `EDTORIAL` |

## Shared art direction

Use a warm cream graph-paper background (`#f5f1e8`), a subtle grid (`#d4cfb8`), precise dark ink lines (`#1a1a1a`), and restrained orange (`#d97706`), green (`#16a34a`), and yellow (`#fbbf24`) accents. Reserve red for failed control gates. Do not use photos, 3D, mascots, decorative doodles, company logos, page numbers, or an extra pretitle. All visible text is English. Do not use em dashes. Target 1600 x 900 pixels.

## 1. Provider portfolio for 300 engineers

Output: `guide/images/subscription-provider-portfolio.webp`

Alt text: A 300-engineer organization split into managed interactive workforce subscriptions, governed service automation, and private inference, each with separate cost and acceptance measures.

```text
Create a clean editorial infographic for a technical documentation guide, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no decorative doodles, no company logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “ONE FLEET, THREE CONTROL PLANES”

At the top center, show one group labeled “300 ENGINEERS”. Split it into three clearly separated paths.

Path 1: “INTERACTIVE WORKFORCE”. Subtitle: “Managed user identities”. Show six compact labels: “Claude”, “Codex”, “Copilot”, “Gemini”, “Cursor”, “Mistral Vibe”. Below them show “Active users”, “Accepted tasks”, and “Seat and overage cost”.

Path 2: “AUTOMATION”. Subtitle: “Service identities through a gateway”. Show “CI”, “Shared agents”, and “Scheduled workflows” connected to one box titled “Gateway”. Inside it show “Budgets”, “Attribution”, “Routing”, and “Fallback”.

Path 3: “SENSITIVE WORKLOADS”. Subtitle: “Private or self-hosted inference”. Show one “Private inference cluster” with “Quality gate”, “Latency gate”, “Capacity gate”, and “Loaded cost”.

Footer: “ASSIGN BY POPULATION. MEASURE ACCEPTED OUTCOMES.”

Make the three control planes unmistakably different. Do not imply that one provider should serve every workload.
```

## 2. Mistral deployment paths

Output: `guide/images/mistral-deployment-paths.webp`

Alt text: Mistral Vibe, the Devstral API, and open-weight Devstral compared as managed workforce, metered service, and private inference paths behind shared quality, sovereignty, concurrency, latency, and loaded-cost gates.

```text
Create a clean technical decision infographic, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “THREE MISTRAL PATHS, THREE OPERATING MODELS”

Create three large vertical lanes.

Lane 1: “MISTRAL VIBE”. Subtitle: “Managed workforce”. Show “User seats”, “Organization controls”, “Included usage + PAYG”, and “Managed operations”.

Lane 2: “DEVSTRAL API”. Subtitle: “Metered service”. Show “Service identity”, “Token usage”, “Gateway budgets”, and “Provider operations”.

Lane 3: “OPEN-WEIGHT DEVSTRAL”. Subtitle: “Private inference”. Show “GPU capacity”, “Queue depth”, “TTFT + TPOT”, “Availability”, and “Operator time”.

Under the lanes, create five connected decision gates: “TASK QUALITY” → “DATA BOUNDARY” → “CONCURRENCY” → “LATENCY” → “LOADED COST”. End with three result cards: “Choose managed”, “Choose API”, and “Choose private”.

Red rejection note: “Hardware fit is not production capacity.”

Footer: “Provider nationality does not prove workload sovereignty.”
```

## 3. Gateway visibility boundary

Output: `guide/images/gateway-visibility-boundary.webp`

Alt text: User subscriptions bypass gateway budgets and attribution while CI, shared agents, scheduled workflows, and internal services pass through centralized keys, quotas, model allowlists, fallback, and observability.

```text
Create a clean editorial architecture infographic, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no logos, no page number, and no pretitle. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “A GATEWAY SEES ONLY ROUTED TRAFFIC”

Build two horizontal traffic paths.

Top path in red: “USER SUBSCRIPTIONS”. Show “Claude”, “Codex”, “Cursor”, and “Mistral Vibe” connected directly to external provider boxes. Add “Outside gateway budgets”, “Outside gateway attribution”, and “Separate audit boundary”.

Bottom path in green: “GOVERNED SERVICE TRAFFIC”. Show “CI”, “Shared agents”, “Scheduled workflows”, and “Internal services” routed through one central box labeled “AI GATEWAY”. Inside it show “Central keys”, “Budgets”, “Quotas”, “Cost attribution”, “Model allowlist”, and “Fallback”. Connect the gateway to “Provider A”, “Provider B”, and “Private model”.

Add an orange observability panel containing “Logs”, “Latency”, “Errors”, and “Token usage”.

Footer: “CENTRALIZED CONTROL REQUIRES CENTRALIZED TRAFFIC.”
```

## 4. Agentic-tool selection map

Planned output: `guide/images/agentic-tool-selection-map.webp`

Status: not published. Regenerate from this clean prompt because the first output added a misspelled pretitle.

```text
Create a clean editorial selection infographic for an AI coding tools guide, landscape 16:9 at 1600x900. Use the shared warm cream graph-paper art direction. No photos, no 3D, no mascots, no company logos, no page number, and no pretitle above the headline. All visible text must be exactly in English and spelled correctly. Do not use em dashes.

Headline: “CHOOSE THE JOB BEFORE THE TOOL”

Create four large job cards connected to four tool categories.

1. “INTERACTIVE REPOSITORY WORK” connects to “Coding agent”, with “Claude Code, Codex, Gemini CLI”.
2. “IDE-CENTERED DEVELOPMENT” connects to “AI-native editor or extension”, with “Cursor, Copilot”.
3. “CI AND SHARED AUTOMATION” connects to “Agent runtime + governed API”, with “Service identity”, “Budget”, “Retry policy”, and “Audit trail”.
4. “PRIVATE INFERENCE” connects to “Open-weight model + serving engine”, with “Task quality”, “Concurrency”, “Latency”, and “Operations”.

Below the cards, add one measurement strip: “ACCEPTED TASKS”, “TOTAL WORKFLOW COST”, “REVIEW TIME”, and “FAILURES + RETRIES”.

Red warning: “Mismatch: Do not compare a seat, a gateway, a model, and a runtime as equivalent products.”

Footer: “THE RIGHT CATEGORY COMES BEFORE THE PROVIDER.”
```

## Verification record

| Asset | Dimensions | QA result |
|---|---:|---|
| `subscription-provider-portfolio.webp` | 1600 x 900 | Text and layout reviewed after conversion |
| `mistral-deployment-paths.webp` | 1600 x 900 | Text and layout reviewed after conversion |
| `gateway-visibility-boundary.webp` | 1600 x 900 | Text and layout reviewed after conversion |
| `agentic-tool-selection-map.webp` | Not published | Source rejected for misspelled pretitle |
