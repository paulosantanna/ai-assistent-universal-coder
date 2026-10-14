<!-- Package: 00_skills/(architecture)/component-identification-sizing; relative command/resource examples resolve from that package or workspace root. -->

## Output Format

### Component Inventory Table

```markdown
## Component Inventory

| Component Name  | Namespace/Path               | Statements | Files | Percent | Status       |
| --------------- | ---------------------------- | ---------- | ----- | ------- | ------------ |
| Billing Payment | services/BillingService      | 4,312      | 23    | 5%      | ✅ OK        |
| Reporting       | services/ReportingService    | 27,765     | 162   | 33%     | ⚠️ Too Large |
| Notification    | services/NotificationService | 1,433      | 7     | 2%      | ✅ OK        |
```

**Status Legend**:

- ✅ OK: Well-sized (within 1-2 std dev from mean)
- ⚠️ Too Large: Exceeds size threshold or >2 std dev above mean
- 🔍 Too Small: <1% of codebase or <1 std dev below mean

### Size Analysis Summary

```markdown
## Size Analysis Summary

**Total Components**: 18
**Total Statements**: 82,931
**Mean Component Size**: 4,607 statements
**Standard Deviation**: 5,234 statements

**Oversized Components** (>2 std dev or >10%):

- Reporting (33% - 27,765 statements) - Consider splitting into:
  - Ticket Reports
  - Expert Reports
  - Financial Reports

**Well-Sized Components** (within 1-2 std dev):

- Billing Payment (5%)
- Customer Profile (5%)
- Ticket Assignment (9%)

**Undersized Components** (<1 std dev):

- Login (2% - 1,865 statements) - Consider consolidating with Authentication
```

### Component Size Distribution

```markdown
## Component Size Distribution
```

Component Size Distribution (by percent of codebase)

[Visual representation or histogram if possible]

Largest: ████████████████████████████████████ 33% (Reporting)
████████ 9% (Ticket Assign)
██████ 8% (Ticket)
██████ 6% (Expert Profile)
█████ 5% (Billing Payment)
████ 4% (Billing History)
...

````

### Recommendations

```markdown
