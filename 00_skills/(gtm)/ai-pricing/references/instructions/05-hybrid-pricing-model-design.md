<!-- Package: 00_skills/(gtm)/ai-pricing; relative command/resource examples resolve from that package or workspace root. -->

## Hybrid Pricing Model Design

Pure pricing models have weaknesses. Consumption scares buyers. Per-seat misses expansion. Outcome puts all risk on you. Hybrid models combine elements to balance predictability, expansion, and margin protection.

**The hybrid formula:**

```
Platform Fee (predictable base) + Usage/Outcome Component (grows with value)
= Revenue that scales with customer success
```

**Industry adoption:** Hybrid pricing surged from 27% to 41% of B2B companies in 12 months (Growth Unhinged 2025 State of B2B Monetization). Pure per-seat dropped from 21% to 15% in the same period.

### Hybrid Model Patterns

| Pattern | Structure | Example | When to Use |
|---|---|---|---|
| Base + consumption | Platform fee + per-unit overage | $99/mo + $0.05/API call over 10K | API/platform products with variable usage |
| Base + credits | Platform fee + credit allocation | $199/mo includes 1,000 credits, $0.15/credit after | Multi-feature products with different cost profiles |
| Base + outcome | Platform fee + per-outcome | $499/mo + $0.99/resolved ticket | Agent products with measurable outcomes |
| Seat + consumption | Per-seat + usage cap/overage | $30/seat/mo + credits for AI actions | Copilots with heavy AI features |
| Commitment + burst | Annual commit + on-demand pricing | $50K/yr commit + pay-as-you-go above | Enterprise deals needing budget predictability |

### Designing Your Hybrid Model

```
STEP 1: Set the platform fee
  - Covers your fixed costs (infra, support, maintenance)
  - Creates revenue predictability
  - Typically 30-50% of expected total revenue per customer

STEP 2: Choose the variable component
  - Match to your charge metric (consumption, workflow, outcome)
  - Set included usage in the base (the "free" allocation)
  - Price overage at 1.2-2x your unit cost

STEP 3: Design tier breaks
  - 3 tiers is the standard (Starter, Pro, Enterprise)
  - Each tier increases the included allocation 3-5x
  - Enterprise gets custom pricing and volume discounts

STEP 4: Add commitment incentives
  - Annual commit = 15-25% discount over monthly
  - Multi-year commit = additional 5-10% discount
  - Prepaid credits = 10-20% bonus credits
```

### Hybrid Pricing Example (AI Support Agent)

| Component | Starter | Pro | Enterprise |
|---|---|---|---|
| Monthly platform fee | $199/mo | $599/mo | Custom |
| Included resolutions | 200/mo | 1,000/mo | Custom |
| Overage per resolution | $1.29 | $0.89 | $0.49-0.69 |
| Channels | Chat only | Chat + email | All channels |
| SLA | Best effort | 99.5% uptime | 99.9% + dedicated CSM |
| Annual discount | 15% | 20% | Negotiated |


For hybrid pricing, BYOK, margin management, tier design, GTM impact, migration, competitive analysis, anti-patterns, and experimentation read `references/implementation-guide.md`.
