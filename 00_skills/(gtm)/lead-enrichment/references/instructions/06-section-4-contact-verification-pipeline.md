<!-- Package: 00_skills/(gtm)/lead-enrichment; relative command/resource examples resolve from that package or workspace root. -->

## Section 4: Contact Verification Pipeline

Unverified cold email lists carry 10-30% invalid addresses. Sending to bad addresses destroys sender reputation within a few campaigns. Google, Yahoo, and Microsoft now enforce bounce rates under 2% and spam complaints under 0.3%.

### Verification Pipeline Steps

| Step | Check | Action | Cost |
|---|---|---|---|
| 1 | Syntax validation | Remove malformed addresses (missing @, double dots) | Free |
| 2 | DNS/MX lookup | Verify domain has valid mail server | Free |
| 3 | SMTP verification | Confirm mailbox exists at provider | Provider-based |
| 4 | Catch-all detection | Flag domains that accept all addresses | Provider-based |
| 5 | Role account check | Flag info@, support@, admin@, sales@ | Provider-based |
| 6 | Confidence scoring | Assign final deliverability score | Computed |

### Confidence Score Thresholds

| Confidence | Classification | Action |
|---|---|---|
| >0.85 | Deliverable | Safe to send. Include in sequences. |
| 0.70-0.85 | Risky | Send in small batches. Monitor bounce rate per batch. |
| 0.50-0.69 | Catch-all/Unverifiable | Segment separately. Maximum 50 per day. Watch closely. |
| <0.50 | Invalid/High Risk | Reject. Do not send. Re-enrich with alternate provider. |

### Catch-All Domain Handling

Catch-all domains accept every email sent to them, even addresses that do not exist. They create silent deliverability decay because campaigns appear sent but never reach decision-makers.

**Rules for catch-all addresses:**

- Never mix catch-all addresses into your primary sending pool
- Send catch-all segments from a separate sending domain
- Limit to 20-50 catch-all sends per domain per day
- Track reply rates separately; if reply rate drops below 1%, stop sending to that domain
- Re-verify catch-all addresses every 30 days

### Verification Tool Comparison

| Tool | Verification Method | Catch-All Detection | Bulk Speed | Pricing |
|---|---|---|---|---|
| MillionVerifier | SMTP + proprietary | Yes | 1M/hour | $0.0005/email |
| ZeroBounce | SMTP + AI scoring | Yes | 100K/hour | $0.008/email |
| NeverBounce | SMTP + real-time API | Yes | 50K/hour | $0.008/email |
| DeBounce | SMTP + disposable detect | Yes | 500K/hour | $0.001/email |
| Bouncer | SMTP + toxicity check | Yes | 200K/hour | $0.005/email |

### Deliverability Protection Checklist

Before sending any enriched list to outreach:

- [ ] All emails verified within the last 7 days
- [ ] Bounce rate on verification under 2%
- [ ] Catch-all addresses segmented into separate pool
- [ ] Role accounts (info@, support@) removed or deprioritized
- [ ] Sending domain has SPF, DKIM, and DMARC configured
- [ ] Sending domain warmed for at least 14 days
- [ ] Daily send volume does not exceed 50 per inbox per day (cold)
- [ ] Spam complaint rate on prior campaigns under 0.3%

---
