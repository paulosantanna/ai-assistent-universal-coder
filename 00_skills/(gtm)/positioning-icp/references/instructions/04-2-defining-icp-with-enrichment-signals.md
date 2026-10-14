<!-- Package: 00_skills/(gtm)/positioning-icp; relative command/resource examples resolve from that package or workspace root. -->

## 2. Defining ICP with Enrichment Signals

Build your ICP from three signal layers, not gut feel. Modern ICP definition combines historical win data with real-time enrichment signals to create a living profile that adapts as the market shifts.

### The Three Signal Layers

| Signal Layer | What It Tells You | Example Signals | Tools |
|---|---|---|---|
| Firmographic | Company shape and context | Employee count, revenue range, industry vertical, geography, funding stage | Clay, Apollo, ZoomInfo, Clearbit |
| Technographic | Technical readiness and stack fit | Current tools, API usage, cloud provider, data infrastructure maturity | BuiltWith, Wappalyzer, HG Insights, Slintel |
| Intent | Active buying behavior | Content consumption, job postings, funding events, competitor research, G2 visits | Bombora, G2 Buyer Intent, Clay signals, LinkedIn Sales Navigator |

### ICP Scoring Model

Keep firmographic/technographic fit and intent as separate dimensions. Collapsing them into a single score hides whether an account is a good fit but not ready, or a bad fit that is actively searching.

**Fit Score (0-100)**

```
Fit Score = (Firmographic Match * 0.4) + (Technographic Match * 0.35) + (Behavioral Fit * 0.25)
```

| Component | Weight | Scoring Criteria |
|---|---|---|
| Firmographic Match | 40% | Industry vertical (25pts), employee range (25pts), revenue range (25pts), geography (15pts), funding stage (10pts) |
| Technographic Match | 35% | Uses complementary tools (30pts), has API/integration infrastructure (25pts), cloud-native stack (25pts), data maturity (20pts) |
| Behavioral Fit | 25% | Historical deal velocity (30pts), expansion rate (30pts), retention rate (25pts), NPS/satisfaction (15pts) |

**Intent Score (0-100)**

```
Intent Score = (Third-Party Intent * 0.35) + (First-Party Signals * 0.40) + (Trigger Events * 0.25)
```

| Component | Weight | Scoring Criteria |
|---|---|---|
| Third-Party Intent | 35% | Bombora topic surges (30pts), G2 category research (30pts), competitor page visits (20pts), review site activity (20pts) |
| First-Party Signals | 40% | Website visits to pricing/demo pages (30pts), content downloads (20pts), email engagement (25pts), product signup/trial (25pts) |
| Trigger Events | 25% | New funding round (30pts), key hire in target dept (25pts), tech stack change (25pts), competitor churn signal (20pts) |

### ICP Prioritization Matrix

```
                    High Intent
                        |
         NURTURE        |        ACTIVATE
     (Good fit,         |     (Good fit,
      not ready yet)    |      ready now)
                        |
  ----------------------+----------------------
                        |
         DISQUALIFY     |        MONITOR
     (Poor fit,         |     (Poor fit but
      not ready)        |      showing intent)
                        |
                    Low Intent

         Low Fit                    High Fit
```

- **ACTIVATE (High Fit + High Intent)**: Route to sales immediately. These accounts match your ICP and are actively looking. Target response time: under 4 hours.
- **NURTURE (High Fit + Low Intent)**: Enroll in targeted content sequences. They will convert when a trigger event hits.
- **MONITOR (Low Fit + High Intent)**: Watch for ICP drift. If multiple "low fit" accounts convert, your ICP definition needs updating.
- **DISQUALIFY (Low Fit + Low Intent)**: Do not spend resources. Revisit only during quarterly ICP refresh.

### Enrichment Waterfall Architecture

Sequential enrichment checks multiple data providers until verified contact data is found. Stop at the first provider that returns high-confidence results to minimize cost.

```
Step 1: Clay (primary enrichment)
  |
  +--> Confidence >= 0.85? --> ACCEPT, stop
  |
  +--> Confidence < 0.85? --> Continue
  |
Step 2: Apollo (secondary)
  |
  +--> Confidence >= 0.85? --> ACCEPT, stop
  |
  +--> Confidence < 0.85? --> Continue
  |
Step 3: ZoomInfo (tertiary)
  |
  +--> Confidence >= 0.85? --> ACCEPT, stop
  |
  +--> Confidence < 0.85? --> Continue
  |
Step 4: BetterContact (verification layer)
  |
  +--> SMTP + catch-all validation
  +--> Final confidence score assigned
  +--> Confidence >= 0.50? --> ACCEPT with flag
  +--> Confidence < 0.50? --> REJECT
```

**Confidence Thresholds**

| Score Range | Action | Expected Deliverability |
|---|---|---|
| 0.85 - 1.00 | Accept, route to outreach | 95%+ deliverable |
| 0.70 - 0.84 | Accept with verification flag | 85-94% deliverable |
| 0.50 - 0.69 | Accept for nurture only, do not cold email | 70-84% deliverable |
| Below 0.50 | Reject, do not use | Below 70%, high bounce risk |

### ICP Definition Workflow

1. **Export your best 20-50 customers** by NRR, deal velocity, or LTV
2. **Run firmographic enrichment** to find common patterns (industry, size, stage)
3. **Run technographic enrichment** to find stack commonalities
4. **Analyze intent signals** that preceded closed-won deals
5. **Build the scoring model** with weights derived from your data, not assumptions
6. **Test against your pipeline** to see if the model would have predicted your last 10 wins
7. **Set a 90-day review cadence** because in AI markets, your ICP drifts quarterly

---
