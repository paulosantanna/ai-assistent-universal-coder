<!-- Package: 00_skills/(architecture)/frontend-blueprint; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: User with clear vision

User says: "Build me a pricing page. Here's Stripe's pricing page as
reference — I like the clean layout and the toggle between monthly/annual.
Our brand colors are #1a1a2e and #e94560. Use Inter for body, and something
bolder for headings."

Actions:

1. Briefing: Quick — they gave most context. Ask only: "How many tiers?
   Any specific features to highlight? Does the page need a FAQ section?"
2. References: Already provided. Ask: "Anything you DON'T like about
   Stripe's approach?"
3. Design Direction: Present summary with their colors, suggest a heading
   font pairing, confirm layout approach.
4. Execution Plan: [pricing toggle → tier cards → feature comparison → CTA]
5. Build each step, review each.

### Example 2: Vague request

User says: "I need a dashboard"

Actions:

1. Briefing: "What kind of dashboard? Analytics, admin panel, user-facing
   metrics? Who will use it? What data will it show?"
2. After answers, References: "Share 2-3 dashboards you like. Could be from
   any product — Notion, Linear, Vercel, or anything else. What specifically
   draws you to each?"
3. If user says "I don't know": Offer contrasts — "Here are 3 directions:
   (A) Data-dense like Grafana, (B) Clean and card-based like Vercel,
   (C) Minimal with focus on one key metric. Which resonates?"
4. Only proceed to Design Direction after concrete alignment.

### Example 3: Unsure user — Stitch prototyping flow

User says: "I need a dashboard but I'm not sure what I want"

Actions:

1. Briefing: Gather context — type of dashboard, audience, data to show
2. References: User can't provide any. Offer contrasts to narrow direction
3. Design Direction: Present summary based on alignment
4. Stitch Prototyping: "Since you don't have mockups, let's visualize
   this before coding. I'll generate Stitch prompts for 2-3 key screens."
   - Generate prompt: "A data analytics dashboard for SaaS metrics.
     Clean, minimal, light theme with blue accents. Sidebar navigation
     with Home, Analytics, Users, Settings. Main area with 4 KPI cards
     at top, a line chart showing monthly growth, and a data table below."
   - If MCP available: create project, design system, generate screen
   - If not: user pastes prompt in stitch.withgoogle.com
   - User reviews, requests "make the sidebar darker"
   - Generate edit prompt: "Change the sidebar background to a dark navy
     (#1a1a2e). Update sidebar text and icons to white."
   - Generate variants to compare layout options
   - User approves final version
5. Execution Plan: [design tokens → sidebar → KPI cards → chart → table]
6. Build each step using Stitch screenshot as reference

### Example 4: Redesign of existing UI

User says: "This component looks bad, make it better" [shares screenshot]

Actions:

1. Analyze current state: Identify specific issues (spacing, typography
   hierarchy, color contrast, layout problems)
2. Share analysis: "Here's what I see: [issues]. Before I fix it — what's
   the surrounding context? Are there brand guidelines to follow?"
3. Collect minimal references if none exist
4. Present 1-2 improvement directions, get alignment
5. Implement the chosen direction
