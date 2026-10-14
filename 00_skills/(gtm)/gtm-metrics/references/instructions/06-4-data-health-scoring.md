<!-- Package: 00_skills/(gtm)/gtm-metrics; relative command/resource examples resolve from that package or workspace root. -->

## 4. Data Health Scoring

Bad CRM data makes every other metric unreliable. Quantify data trustworthiness before trusting pipeline reports.

### Data Health Score

```
Data Health Score = (Completeness * 0.35) + (Accuracy * 0.30) + (Recency * 0.20) + (Consistency * 0.15)
```

| Component | Weight | What It Measures |
|---|---|---|
| Completeness | 35% | % of required fields populated per record |
| Accuracy | 30% | % of data points verified against enrichment sources |
| Recency | 20% | % of records updated within 90 days |
| Consistency | 15% | % of records matching format standards |

### Health Score Targets

| Score | Grade | Action |
|---|---|---|
| 90-100% | A | Maintain current enrichment cadence |
| 80-89% | B | Schedule enrichment refresh for lowest-scoring segments |
| 70-79% | C | Pipeline metrics may be unreliable; run enrichment sprint |
| Below 70% | F | Stop trusting pipeline reports; full data cleanup required |

B2B data decays at 2.1% monthly on average. Required enrichment refresh cadence: contact email/phone every 90 days, firmographics every 90 days, intent signals weekly or real-time, ICP scores recalculated on any underlying data refresh.

---
