<!-- Package: 00_skills/(gtm)/sales-motion-design; relative command/resource examples resolve from that package or workspace root. -->

## 2. Motion Archetypes in Detail

### 2A. Pure PLG

**When it works**: Low price, low complexity, user = buyer, fast TTFV.

**Examples**: Notion, Canva, Calendly, Loom, Figma early days.

**Conversion funnel**:
```
Visit -> Sign up -> Activate -> Engage -> Convert -> Expand
                                                      |
                                            (product handles all)
```

**Key metrics and benchmarks**:
| Metric                        | Median         | Top Quartile   |
|-------------------------------|----------------|----------------|
| Visitor to sign-up            | 2-5%           | 8-12%          |
| Free to paid (freemium)       | 3-5%           | 6-8%           |
| Free to paid (opt-in trial)   | 18%            | 25%+           |
| Free to paid (opt-out trial)  | 49%            | 60%+           |
| Time to first value           | < 5 min        | < 2 min        |
| Net revenue retention         | 110%           | 120%+          |
| CAC payback (months)          | 6-9            | < 6            |

**Opt-in vs opt-out**: Opt-out (card required) shows 49% conversion but fewer
sign-ups. Opt-in (no card) shows 18% but higher volume. Use opt-out only when
TTFV < 5 min and activation rate > 40%.

**Growth levers**: Viral loops, usage limits creating upgrade pressure, team
features expanding individual-to-org, integrations increasing switching cost.

**Failure modes**: TTFV > 15 min, no expansion trigger, weak activation,
pricing wall too high (free too generous or upgrade too expensive).

### 2B. PLG + Sales Hybrid

**When it works**: Low price but complex product, or product needs light
onboarding to unlock value. Most common motion in 2025-2026.

**Examples**: Slack, Datadog, Twilio, Vercel, Linear.

**Conversion funnel**:
```
Visit -> Sign up -> Activate -> PQL trigger -> Sales touch -> Close
                        |                          |
                   (product)              (human assists)
```

**What triggers the sales touch (PQL signals)**:
- Seats/usage exceeds free tier by 20%+
- Second team or department added
- Admin/billing page visited 3+ times
- Integration with production system connected
- API call volume crosses threshold
- Feature gate hit on enterprise capability

**PQL vs MQL performance comparison**:
| Lead Type | Avg Conversion to Paid | Relative Efficiency |
|-----------|----------------------|---------------------|
| MQL       | 5-10%                | Baseline            |
| PQL       | 25-30%               | 3-5x better         |
| PQL (ACV $1-5K)  | 30%          | 4x better           |
| PQL (ACV $5-10K) | 39%          | 5-6x better         |

**Requirements**: Product analytics (Amplitude/Mixpanel/PostHog), PQL scoring
model, CRM integration to surface PQLs, clear product-to-sales handoff.

**Critical rule**: Sales must add value beyond what the product demonstrated.
Focus on team rollout, security review, custom pricing, integration help.

### 2C. Sales-Assisted PLG

**When it works**: Higher price, simple enough for try-before-buy.
**Examples**: Figma Enterprise, GitHub Enterprise, Airtable Enterprise.

Bottom-up adoption triggers top-down sale. Free individual tier ($0-20/user/mo)
feeds adoption. Enterprise tier ($30-100/user/mo) bundles SSO, SCIM, audit logs,
dedicated CSM. The gap creates a natural sales conversation.

**Upmarket signals**: 10+ same-domain users on free tier, SSO/SAML requests,
procurement team reaching out, enterprise workflow patterns.

### 2D. Sales-Led

**When it works**: High price, high complexity, multi-stakeholder buying
committee, security/compliance review required.
**Examples**: Salesforce, Workday, Snowflake (enterprise), Palantir.

| Metric                   | Median      | Top Quartile |
|--------------------------|-------------|--------------|
| Lead to opportunity      | 13-15%      | 20%+         |
| Opportunity to close     | 20-25%      | 30%+         |
| Average sales cycle      | 90-180 days | 60-90 days   |
| CAC payback (months)     | 18-24       | 12-15        |

Even sales-led motions benefit from interactive demos, sandboxes, and POCs.
The difference is a human guides the process rather than the product alone.

### 2E. Agent-Led Discovery (Emerging, 2025-2026)

**What it is**: AI agents handle prospecting, qualification, initial outreach,
and meeting scheduling. Humans handle discovery calls, demos, negotiation, and
closing.

**Current reality check (2026 data)**:
| Metric                              | Current State        |
|-------------------------------------|----------------------|
| Pipeline growth (well-implemented)  | 3-8x                |
| CAC reduction (best case)           | 30-42% lower         |
| Failure rate within 6 months        | 85% of deployments   |
| AI outreach response rate           | 0.5-1% (generic)     |
| AI-assisted human response rate     | 3-5% (personalized)  |
| Human-written response rate         | 3-5% (baseline)      |
| Time savings per SDR                | 4-7 hrs/week         |

**Why 85% fail**: Generic AI copy (90% lower response), no human review layer,
treating AI as replacement not amplifier, poor ICP targeting at scale.

**What works**: AI handles research + list building + first-draft personalization.
Human reviews before sending. AI handles sequencing + scheduling. Human handles
all live conversations.

**Implementation tiers**:

| Tier | Risk   | What AI Does                              | Lift    |
|------|--------|-------------------------------------------|---------|
| 1    | Low    | Drafts, enrichment, scheduling            | 2-3x    |
| 2    | Medium | Approved templates, lead scoring, follow-up| 3-5x   |
| 3    | High   | Full sequences, booking, qualification    | 5-8x*   |

*Tier 3 has 85% failure rate. Only viable with tight ICP, simple product, low ACV.

**Recommendation**: Start Tier 1. Move to Tier 2 after 90+ days of positive
reply rates. Avoid Tier 3 unless ACV < $1K.

---
