<!-- Package: 00_skills/(gtm)/lead-enrichment; relative command/resource examples resolve from that package or workspace root. -->

## Section 2: Enrichment Waterfall Architecture

### What a Waterfall Does

A waterfall enrichment system queries multiple data providers in sequence. Each provider gets a chance to fill missing fields. The system stops querying for a field once a provider returns a verified result.

Single-provider enrichment typically yields 55-65% coverage. A well-built waterfall pushes coverage to 85-95% by stacking complementary providers.

### Waterfall Flow

```
Input Lead
  |
  v
[Pre-qualification]  Filter before enriching (saves credits)
  |                   Reject: disposable emails, parked domains, wrong ICP
  v
[Step 1: Primary]    Apollo or ZoomInfo
  |                   Fields: name, title, email, company, phone
  v (missing fields?)
[Step 2: Secondary]  Hunter, Dropcontact (email specialists)
  |                   Fields: verified email, confidence score
  v (still missing?)
[Step 3: Tertiary]   FindyMail, Snov.io (deep search + verify)
  |                   Fields: email, phone, LinkedIn URL
  v (still missing?)
[Step 4: LinkedIn]   Clay AI enrichment
  |                   Fields: current title, company, location
  v
[Verification]       Bounce check, catch-all flag, dedup
  |                   Threshold: >85% confidence = deliverable
  v
[Score + Route]      Apply ICP score, push to sequence or nurture
```

### Provider Selection by Use Case

Not every waterfall needs the same providers. Match your stack to your market and budget.

**High-volume outbound (1000+ leads/month):**

| Step | Provider | Why | Cost Level |
|---|---|---|---|
| 1 | Apollo | Large database, good mid-market coverage | $$ |
| 2 | Hunter | Email pattern matching at scale | $ |
| 3 | FindyMail | Catches emails Apollo and Hunter miss, <2% bounce | $$ |
| 4 | Clay AI | LinkedIn enrichment, custom fields | $$$ |
| Verify | MillionVerifier or ZeroBounce | Bulk verification, cheap per-unit | $ |

**Enterprise targeting (under 500 leads/month):**

| Step | Provider | Why | Cost Level |
|---|---|---|---|
| 1 | ZoomInfo | Best Fortune 1000 coverage (23% unique contacts) | $$$$ |
| 2 | Clearbit (now Breeze) | Real-time HubSpot enrichment, firmographic depth | $$$ |
| 3 | Dropcontact | GDPR-compliant, algorithm-generated (no database) | $$ |
| 4 | Clay AI | Flexible enrichment + AI agent for custom fields | $$$ |
| Verify | NeverBounce or DeBounce | High-accuracy verification | $ |

**Startup / budget-conscious (under 200 leads/month):**

| Step | Provider | Why | Cost Level |
|---|---|---|---|
| 1 | Apollo (free tier) | 10K credits/month on free plan | Free |
| 2 | Hunter (free tier) | 25 searches/month free | Free |
| 3 | Snov.io | Affordable at $39/month for 1,000 credits | $ |
| Verify | MillionVerifier | $0.0005/email bulk pricing | $ |

### Provider Comparison Matrix

| Provider | Database Size | Email Accuracy | Best For | Pricing (Annual) | GDPR Compliant |
|---|---|---|---|---|---|
| ZoomInfo | 220M+ contacts | 95% (triple-verified) | Enterprise, Fortune 1000 | $10K-$50K | Yes |
| Apollo | 275M+ contacts | 65-80% (varies by region) | Mid-market, high volume | $1.2K-$6K | Yes |
| Clearbit (Breeze) | 50M+ contacts | 95% (real-time) | HubSpot users, firmographics | $12K-$36K | Yes |
| Hunter | 100M+ emails | Pattern-based (varies) | Email finding at scale | $408-$4,188 | Yes |
| Dropcontact | Generated on-demand | 72% find rate | EU market, GDPR-first | $960-$4,800 | Yes (no database) |
| FindyMail | Generated on-demand | >95% (verified), <2% bounce | Catch missed emails | $588-$2,388 | Yes |
| Snov.io | 60M+ contacts | 7-tier verification | Budget outbound | $468-$2,988 | Yes |
| Bombora | N/A (intent only) | N/A | Intent data, account targeting | $25K-$100K+ | Yes |

### Incremental Coverage by Waterfall Step

Typical coverage gains when adding each provider in sequence:

```
Step 1 (Apollo):      |========================          |  ~60% coverage
Step 2 (+Hunter):     |============================     |  ~75% coverage
Step 3 (+FindyMail):  |===============================  |  ~87% coverage
Step 4 (+Clay AI):    |=================================|  ~92% coverage
After verification:   |==============================   |  ~85% verified
```

The drop after verification is expected. Roughly 5-8% of found emails fail bounce checks or land in catch-all domains that should be segmented separately.

---
