<!-- Package: 00_skills/(gtm)/lead-enrichment; relative command/resource examples resolve from that package or workspace root. -->

## Section 1: ICP Scoring Framework

### The Three Signal Layers

Every ICP score pulls from three distinct signal categories. Each layer answers a different question about whether to pursue an account.

| Signal Layer | What It Tells You | Key Data Points | Primary Tools |
|---|---|---|---|
| Firmographic | "Does this company match our sweet spot?" | Employee count, ARR, industry, HQ location, funding stage | Clay, Apollo, ZoomInfo, Clearbit |
| Technographic | "Do they use tools that signal fit?" | Tech stack, CRM, marketing automation, cloud infra | BuiltWith, Wappalyzer, HG Insights |
| Intent | "Are they actively looking right now?" | Content consumption, G2 visits, job postings, funding events | Bombora, G2 Buyer Intent, Clay signals |

### ICP Scoring Formula

```
ICP Score = (Firmographic Fit x 0.30) + (Technographic Fit x 0.30) + (Intent Score x 0.40)
```

Weight intent highest because timing beats targeting. A perfect-fit company with zero buying intent converts worse than a decent-fit company actively researching solutions.

### Firmographic Fit Scoring (0-100)

Score each firmographic dimension, then average:

| Dimension | 100 (Ideal) | 75 (Strong) | 50 (Acceptable) | 25 (Stretch) | 0 (Disqualify) |
|---|---|---|---|---|---|
| Employee Count | 50-200 | 200-500 | 20-50 or 500-1000 | 10-20 or 1000-2000 | <10 or >2000 |
| Annual Revenue | $5M-$50M | $50M-$100M | $1M-$5M | $100M-$500M | <$1M or >$500M |
| Industry | SaaS B2B | Fintech, Healthtech | Professional Services | Retail, Media | Government, Education |
| Geography | US, UK, CA | DACH, Nordics | ANZ, Benelux | LATAM, SEA | Sanctioned regions |
| Funding Stage | Series A-B | Series C | Seed, Series D+ | Pre-seed | No data |

Adjust the ranges to your actual closed-won customer profile. Pull ranges from your CRM data, not assumptions.

### Technographic Fit Scoring (0-100)

Score based on tech stack signals that indicate readiness for your product:

```
Tech_Score = (Stack_Match x 0.50) + (Complexity_Signal x 0.30) + (Migration_Signal x 0.20)
```

**Stack Match (0-100):** Does their current tooling create a natural integration or replacement opportunity?

| Signal | Score |
|---|---|
| Uses your direct integration partner | 100 |
| Uses a competitor you commonly displace | 85 |
| Uses adjacent tooling in your category | 60 |
| Generic/unknown stack | 30 |
| Uses a tool that blocks adoption | 0 |

**Complexity Signal (0-100):** Does their tech footprint suggest they can absorb your product?

| Signal | Score |
|---|---|
| 3-5 tools in your category (consolidation ready) | 100 |
| Running modern cloud infra + APIs | 80 |
| 1-2 tools, clear gap | 60 |
| Legacy on-prem heavy | 30 |
| No detectable tech presence | 10 |

**Migration Signal (0-100):** Are they showing signs of switching?

| Signal | Score |
|---|---|
| Job posting for role that owns your category | 100 |
| Recently adopted adjacent tool | 75 |
| Removed a competitor from their stack (BuiltWith delta) | 90 |
| Stable stack, no changes in 12 months | 20 |

### Intent Score Calculation (0-100)

Intent scoring requires combining multiple signal sources. No single provider captures the full picture.

```
Intent_Score = max(Bombora_Surge, G2_Intent, First_Party) x 0.60
             + Hiring_Signal x 0.20
             + Funding_Signal x 0.20
```

**Bombora Company Surge scoring:**

| Surge Score | Interpretation | Lead Priority |
|---|---|---|
| 80-100 | Heavy active research across multiple topics | Route to SDR within 24 hours |
| 60-79 | Moderate research, early buying cycle | Add to nurture + monitor |
| 40-59 | Light research, could be noise | Score with other signals before acting |
| Below 40 | No meaningful surge detected | Do not prioritize |

**G2 Buyer Intent signals:**

| Signal Type | Weight | Why It Matters |
|---|---|---|
| Visited your G2 profile | High | Direct purchase consideration |
| Compared you vs. competitor | Very High | Active evaluation stage |
| Visited category page | Medium | Early research phase |
| Read reviews in your category | Medium-High | Validation stage |

**First-party intent signals (your own data):**

| Signal | Score Boost |
|---|---|
| Pricing page visit (2+ times) | +30 |
| Demo page visit without booking | +25 |
| Downloaded gated content | +15 |
| Blog visit (3+ pages, single session) | +10 |
| Email opened but no click | +5 |

### Composite Score Interpretation

| ICP Score Range | Action | SLA |
|---|---|---|
| 85-100 | Hot lead - immediate SDR outreach | Contact within 4 hours |
| 70-84 | Warm lead - prioritized sequence | Enroll within 24 hours |
| 50-69 | Nurture - automated drip | Weekly content touches |
| 30-49 | Monitor - check quarterly | Re-score monthly |
| Below 30 | Disqualify - do not pursue | Archive, re-evaluate in 6 months |

---
