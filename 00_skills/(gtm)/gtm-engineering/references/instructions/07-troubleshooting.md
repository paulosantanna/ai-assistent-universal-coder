<!-- Package: 00_skills/(gtm)/gtm-engineering; relative command/resource examples resolve from that package or workspace root. -->

## Troubleshooting

- **Workflow success rate below 95%** → **Cause:** API rate limits, bad data, or timeouts. **Fix:** Add retries and backoff; validate inputs; alert on failure; cache enrichment; version workflows in Git.
- **Enrichment hit rate low** → **Cause:** Wrong provider order or stale cache. **Fix:** Reorder waterfall; set confidence threshold (0.85 accept, 0.50 flag, &lt;0.50 reject); re-enrich cadence 30–90d; track per-provider fill.
- **Lead response time too slow** → **Cause:** Manual steps or batch runs. **Fix:** Hot lead &lt;5 min (inbound), &lt;1 hr overall; warm &lt;4 hr; automate routing and first-touch; use real-time enrichment where possible.

---


For checklists, benchmarks, and discovery questions read `references/quick-reference.md` when you need detailed reference.

---
