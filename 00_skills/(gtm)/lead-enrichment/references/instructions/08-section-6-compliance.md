<!-- Package: 00_skills/(gtm)/lead-enrichment; relative command/resource examples resolve from that package or workspace root. -->

## Section 6: Compliance

### Compliance by Region

| Requirement | US (CAN-SPAM/CCPA) | EU (GDPR) | UK (UK GDPR) |
|---|---|---|---|
| B2B email consent | Opt-out model | Legitimate interest | Legitimate interest |
| Data source docs | Recommended | Required | Required |
| Right to erasure | CCPA: Yes | Required | Required |
| Data retention | Disclosure required | Define and enforce | Define and enforce |

### Provider Notes

- **Dropcontact** generates contacts algorithmically without a database (GDPR-native)
- **Apollo, ZoomInfo, Clearbit** are compliant as platforms; you own your usage basis
- **Clay** is compliant, but third-party providers accessed through Clay may not be. Verify each.
- **Bombora** cooperative data is compliant; downstream outreach must follow local regulations

### Safe Enrichment Practices

1. Document your legal basis (legitimate interest for B2B is standard)
2. Track which provider sourced each contact
3. Honor opt-out and erasure requests within 30 days
4. Do not enrich or contact individuals who have previously opted out
5. Review provider DPAs annually

---
