<!-- Package: 00_skills/(gtm)/lead-enrichment; relative command/resource examples resolve from that package or workspace root. -->

## Section 3: Clay Workflow Design

### Clay Architecture Basics

Clay operates on a table-based model. Each row is a lead. Each column is a data field. Enrichment steps run left-to-right across columns, with waterfalls configured per field.

**Core Clay concepts:**

| Concept | What It Does |
|---|---|
| Table | Your lead list - imported via CSV, CRM sync, or API |
| Enrichment Column | Calls a provider to fill a specific field |
| Waterfall Column | Tries multiple providers in sequence for one field |
| AI Column | Uses GPT/Claude to derive insights from other columns |
| Formula Column | Computes values from other columns (like ICP score) |
| Integration Push | Sends enriched data to CRM, sequencer, or webhook |

### Credit Consumption Guide

Clay charges credits per enrichment action. Budget carefully.

| Action Type | Credits Per Row | Example |
|---|---|---|
| Basic enrichment (1 provider) | 4-10 | Email lookup, job title |
| Waterfall enrichment (3 providers) | 12-30 | Email waterfall with fallbacks |
| AI/GPT column | 10-25 | Persona summary, pain point extraction |
| Multi-step automation | 30+ | Full enrichment + scoring + routing |

**Credit math:** 1,000 leads at 25 credits/lead = 25,000 credits. Starter plan handles that in 12.5 months, Explorer in 2.5 months, Pro in 0.5 months. Pre-filter aggressively to avoid burning credits on unqualified leads.

### Clay Pricing (2026)

| Plan | Price/Mo | Credits/Mo | Per Credit |
|---|---|---|---|
| Free | $0 | 100 | N/A |
| Starter | $149 | 2,000 | $0.075 |
| Explorer | $349 | 10,000 | $0.035 |
| Pro | $800 | 50,000 | $0.016 |
| Enterprise | Custom | Custom | Custom |

### Sample Clay Table Structure

Build your enrichment workflow in this column order:

```
Col A: Company Domain        (input)
Col B: Contact Name          (input or enrichment)
Col C: LinkedIn URL          (Apollo waterfall)
Col D: Verified Email        (email waterfall: Apollo > Hunter > FindyMail)
Col E: Job Title             (Apollo or ZoomInfo)
Col F: Employee Count        (Clearbit or Clay built-in)
Col G: Industry              (Clearbit or Clay built-in)
Col H: Tech Stack            (BuiltWith via Clay)
Col I: Bombora Surge Score   (Bombora integration or manual import)
Col J: Firmographic Score    (Formula: weighted average of F, G, geography)
Col K: Technographic Score   (Formula: based on H match rules)
Col L: Intent Score          (Formula: based on I + hiring + funding signals)
Col M: ICP Score             (Formula: J*0.30 + K*0.30 + L*0.40)
Col N: AI Personalization    (AI column: generate first-line based on B, E, H)
Col O: Routing               (Formula: if M > 85 then "hot" elif M > 70 then "warm")
```

### Credit Governance Rules

1. **Pre-qualify before enriching** - domain check + firmographic filter before spending on email waterfall
2. **Cap per campaign** - no single campaign burns more than 40% of monthly credits
3. **Alert at 75%** - Slack/email alert when usage crosses 75% of monthly allowance
4. **Audit weekly** - credits spent vs. leads enriched vs. leads qualified (target >60% qualification)
5. **90-day re-enrichment** - re-enrich stale contacts before including in new campaigns

---
