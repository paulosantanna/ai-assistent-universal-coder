<!-- Package: 00_skills/(gtm)/gtm-metrics; relative command/resource examples resolve from that package or workspace root. -->

## 6. Dashboard Architecture

### Three-Tier Hierarchy

**Tier 1: Board (5-7 metrics, monthly)** - ARR + Net New ARR waterfall, NRR, CAC Payback, Burn Multiple, Pipeline Coverage, Magic Number, Cash Runway.

**Tier 2: Executive (10-12 metrics, weekly)** - Pipeline created, pipeline by stage, win rate by segment, deal size trend, sales cycle length, quota attainment by rep, NRR by cohort, CAC by channel, TTFV, data health score, slippage rate.

**Tier 3: Operator (15-25 metrics, daily)** - Activity (emails, calls, meetings booked), pipeline (new opps, stage movements), response (speed-to-lead, follow-up rate), conversion (stage-by-stage rates), quality (ICP fit distribution), AI ops (AI messages, AI reply rate, cost per meeting).

### Tool Selection

| Tool | Best For | Cost |
|---|---|---|
| HubSpot Dashboards | Teams already on HubSpot | Included |
| Metabase | SQL-native, self-hosted | Free |
| Looker | Enterprise-grade, governed | $$$ |
| Mode | SQL + Python + viz | $$ |
| Google Sheets | Solo founders, pre-revenue | Free |

### Dashboard Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| 50+ metrics on one screen | Limit to tier-appropriate count |
| Vanity metrics without context | Every metric needs benchmark, target, or trend line |
| Manual data entry | All metrics from system-of-record APIs |
| No dashboard owner | Named owner + review schedule required |
| Snapshot without trend | Always show trailing 4-week or 13-week trend |

---
