<!-- Package: 00_skills/(architecture)/frontend-blueprint; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

Every project follows this sequence. Do NOT skip phases. If the user tries
to jump ahead, explain briefly why the current phase matters and proceed.

```
BRIEFING → REFERENCES → DESIGN DIRECTION → [STITCH PROTOTYPING] → EXECUTION PLAN → ATOMIC BUILD → REVIEW
```

The Stitch Prototyping phase (in brackets) is conditional — triggered when
the user has no existing mockups or needs visual validation before code.
See Phase 4 for details.

### Phase 1: Briefing

Goal: Understand WHAT the user needs and WHY.

Ask conversationally (not as a checklist dump). Adapt based on project
complexity — a simple button needs 2 questions, a full app needs more.

Key areas to cover:

- **What** are you building? (page, component, app, redesign, etc.)
- **Who** is the end user? (audience, demographics, context of use)
- **What problem** does this solve? (not just "looks nice" — the actual goal)
- **Technical constraints?** (framework, existing design system, browser support, responsive requirements)
- **Existing assets?** (brand guidelines, color palette, logos, fonts already in use)
- **Deadline or scope?** (MVP vs polished, how much time to invest)

IMPORTANT: For simple requests (a single component, a small tweak), compress
this to 1-2 targeted questions. Don't over-process small tasks. Scale your
discovery to the project size.

### Phase 2: Reference Collection

Goal: Build a concrete visual vocabulary BEFORE any design decisions.

This is the most critical phase. Request references across these dimensions:

**Must collect (always ask):**

- Visual references: "Share 2-3 screenshots, URLs, or images of designs you
  like. They don't need to be the same type of project — if you like the
  typography of site A and the layout of site B, share both and tell me what
  you like about each."
- What specifically they like in each reference: colors? layout? typography?
  spacing? animations? overall mood?

**Collect when relevant (ask based on project scope):**

- Typography preferences: serif vs sans-serif, bold vs light, specific font
  names if they have preferences
- Icon style: outlined, filled, duotone, hand-drawn, geometric, a specific
  library (Lucide, Phosphor, Heroicons, etc.)
- Color direction: dark/light theme, warm/cool tones, specific brand colors,
  accent color preferences
- Imagery style: photography, illustrations, gradients, abstract, minimal
- Motion/animation: subtle micro-interactions, dramatic transitions, none
- Layout preferences: dense/spacious, symmetric/asymmetric, grid-based/organic

**How to handle "I don't know" responses:**
When the user can't provide references or is unsure, DON'T proceed blindly.
Instead:

1. Offer 2-3 contrasting directions with concrete descriptions
2. Use well-known sites as anchors: "More like Stripe (clean, spacious) or
   more like Bloomberg (dense, data-rich)?"
3. Ask elimination questions: "What do you definitely NOT want?"
4. If building for a known brand, research their existing visual identity

CRITICAL: Do not proceed to Phase 3 until you have at least ONE concrete
visual reference or a clearly articulated direction confirmed by the user.

**Stitch as a discovery tool:** If the user has no visual references AND
is not using Figma/Sketch/Adobe XD or similar design tools, suggest Google
Stitch (stitch.withgoogle.com) as a rapid prototyping tool. Frame it as a
time-saver: "Before we write code, I can generate prompts for Google Stitch
to quickly visualize what we're building. You'll see the actual design in
seconds and we avoid rework. Want to try it?" If the user is interested,
read `references/stitch-integration.md` and proceed to Phase 4 (Stitch
Prototyping) after Phase 3. If the user has Stitch MCP connected, you can
generate designs directly.

### Phase 3: Design Direction

Goal: Synthesize references into a clear, agreed-upon direction.

Before writing code, present a **Design Direction Summary**:

```
## Design Direction

**Mood:** [describe in 2-3 words — e.g., "clean and editorial"]
**Color palette:** [primary, secondary, accent, neutrals — hex codes]
**Typography:**
  - Headings: [font name, weight, style rationale]
  - Body: [font name, weight, style rationale]
**Layout approach:** [describe — e.g., "generous whitespace, card-based, 12-col grid"]
**Icon style:** [library + style]
**Key references applied:**
  - From [ref A]: [what you're taking — e.g., "the spacing rhythm and card design"]
  - From [ref B]: [what you're taking — e.g., "the color temperature and typography pairing"]
**Intentional departures:**
  - [anything you're suggesting differently from refs, and WHY]
```

Wait for explicit approval or adjustments before proceeding.

This is also where you provide **expert opinions**: if the user's references
conflict, if their color choices have accessibility issues, if their font
pairing doesn't work — say so now. Suggest improvements with clear reasoning.

### Phase 4: Stitch Prototyping (Conditional)

Goal: Visualize the design BEFORE writing any code.

This phase activates when:

- The user has no existing mockups (Figma, Sketch, etc.)
- The user is uncertain about direction and wants to see options
- The project has multiple screens or complex layouts
- The user explicitly wants to prototype first

Read `references/stitch-integration.md` before executing this phase.

**If Stitch MCP is connected (agent has access to Stitch tools):**

1. Create a Stitch project: `create_project(title: "Project Name")`
2. Create a Design System from the approved Design Direction (Phase 3),
   mapping color palette → `customColor`/`preset`, typography → `font`,
   dark/light → `colorMode`, border radius → `roundness`
3. Generate the first screen using `generate_screen_from_text` with a
   prompt built from the Design Direction. Use the prompt templates in
   `references/stitch-integration.md` Section 4.
4. Present the generated screenshot to the user for review
5. If the user wants alternatives: use `generate_variants` with
   appropriate `creativeRange` and `aspects`
6. If the user wants edits: use `edit_screens` with targeted, specific
   prompts (one change at a time)
7. Apply the design system to all screens for consistency
8. Once all screens are approved, extract HTML via `get_screen` to use
   as a reference in the Atomic Build phase

**If Stitch MCP is NOT connected (manual workflow):**

1. Ask if the user wants to set up MCP (offer setup guidance from
   `references/stitch-integration.md` Section 3 — it covers the generic
   config pattern and API Key method)
2. If they prefer manual: generate ready-to-paste prompts following the
   Stitch prompt formula: **Idea + Theme + Content + Image (optional)**
3. Guide the user through the Stitch workflow:
   - Paste the prompt at stitch.withgoogle.com
   - Choose device type (Mobile for apps, Web for websites/dashboards)
   - Generate, review, and share screenshots back
4. Generate targeted refinement prompts one at a time based on feedback
5. Suggest using **Variants** for comparison: "In Stitch, select the
   screen → Generate → Variants. Set Creative Range to Explore and
   generate 3 options."
6. Suggest using **Edit Theme** for quick adjustments: "Select the
   screen → Generate → Edit Theme to quickly tweak colors, font, dark
   mode, or corner radius."
7. Suggest creating a **Prototype** to test interactivity: "Select the
   screen → Generate → Prototype to see hover states and scroll behavior."
8. Once approved, user downloads HTML/images from Stitch for reference

**Prompt generation rules:**

- Follow the exact formula: Idea + Theme + Content
- Use UI/UX keywords: "navigation bar", "hero section", "card layout",
  "call-to-action button", "visual hierarchy", "drop shadow"
- Set the vibe with adjectives from the Design Direction mood
- Use the Style Word Bank for creative direction (Bento Grid, Editorial,
  Glassmorphism, Brutalist, Cyberpunk, etc.)
- If the user's chosen font is not in Stitch's 29 supported fonts,
  pick the closest match and note the substitution
- Keep prompts focused — one screen/section per generation
- Refinement prompts: one major change at a time, be specific about
  WHAT to change and HOW

**Exiting this phase:**
Proceed to Phase 5 when the user has approved visual designs for all
key screens. These become the source of truth for code generation.
If the user decides to skip Stitch at any point, proceed directly to
Phase 5.

### Phase 5: Execution Plan

Goal: Break the project into atomic, deliverable units.

Present a numbered list of components/sections to build, in dependency order:

```
## Execution Plan

I'll build this in [N] steps, each one reviewed before moving on:

1. **[Component/Section]** — [brief description, ~effort indicator]
2. **[Component/Section]** — [brief description]
3. **[Component/Section]** — [brief description]
...

Starting with #1. Ready?
```

Principles for the plan:

- Each step should produce something **visually reviewable**
- Dependencies first (design tokens/base styles → layout → components → details)
- Group logically but keep steps small enough that rework affects only one piece
- For large projects, suggest a phased approach (Phase A: core structure,
  Phase B: polish and animations, Phase C: responsive/edge cases)

### Phase 6: Atomic Build

Goal: Generate code one unit at a time, validated at each step.

If Stitch Prototyping (Phase 4) was completed, use the approved Stitch
screens as the primary visual reference. When Stitch MCP is available,
retrieve the HTML code via `get_screen` and use it as a structural
starting point — but always rewrite for the target framework, following
the agreed Design Direction tokens and the project's CSS architecture.
Stitch HTML is a reference, not copy-paste material.

For each unit in the execution plan:

1. **Generate the code** following the agreed design direction precisely
2. **Explain your choices** briefly — what you did and why (especially when
   you made subjective decisions)
3. **Highlight decision points** — anything that could go either way, present
   options: "I went with X here, but Y is also valid if you prefer Z"
4. **Proactive suggestions** — if you see an opportunity to improve beyond
   what was asked, suggest it: "This would look even better with a subtle
   hover animation — want me to add it?"

After presenting each unit, explicitly ask: "Does this match your vision?
Any adjustments before I move to the next step?"

CRITICAL: If the user requests changes, apply them to the CURRENT unit
before moving forward. Never accumulate "fix later" items.

### Phase 7: Review & Polish

Goal: Final quality pass on the complete deliverable.

Once all units are approved individually:

1. Present the **integrated result** (all components together)
2. Check for **visual consistency** across components (spacing rhythm,
   color usage, typography hierarchy)
3. Suggest **polish opportunities**: micro-interactions, transitions,
   responsive refinements, accessibility improvements
4. Provide a **final opinion** as a consultant: what's strong, what could
   be better in a future iteration, what to watch out for
