<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Output Format

### Common Domain Components Report

```markdown
## Common Domain Components Found

### Notification Functionality

**Components**:

- services/customer/notification (2% - 1,433 statements)
- services/ticket/notification (2% - 1,765 statements)
- services/survey/notification (2% - 1,299 statements)

**Shared Classes**: SMTPConnection (used by all 3)

**Functionality Analysis**:

- All send emails to customers
- Differences: Content/templates, triggers
- Consolidation Feasibility: ✅ High

**Coupling Analysis**:

- Before: CA = 2 + 2 + 1 = 5
- After: CA = 5 (no increase)
- Verdict: ✅ Safe to consolidate

**Recommendation**: Consolidate into `services/notification`

- Approach: Shared Service
- Expected Size: ~4,500 statements (5% of codebase)
- Benefits: Reduced duplication, easier maintenance
```

### Consolidation Opportunities Table

```markdown
## Consolidation Opportunities

| Common Functionality | Components   | Current CA | After CA | Feasibility | Recommendation                |
| -------------------- | ------------ | ---------- | -------- | ----------- | ----------------------------- |
| Notification         | 3 components | 5          | 5        | ✅ High     | Consolidate to shared service |
| Audit                | 3 components | 8          | 12       | ⚠️ Medium   | Consolidate, monitor coupling |
| Validation           | 2 components | 3          | 3        | ✅ High     | Consolidate to shared library |
```

### Detailed Consolidation Plan

```markdown
## Consolidation Plan

### Priority: High

**Notification Components** → `services/notification`

**Steps**:

1. Create new `services/notification` component
2. Move common functionality from 3 components
3. Create abstraction for content/templates
4. Update dependent components to use new service
5. Remove old notification components

**Expected Impact**:

- Reduced code: ~4,500 statements consolidated
- Reduced duplication: 3 components → 1
- Coupling: No increase (CA stays at 5)
- Maintenance: Easier to maintain single component

### Priority: Medium

**Audit Components** → `services/audit`

**Steps**:
[Similar format]

**Expected Impact**:

- Coupling increase: CA 8 → 12 (monitor)
- Benefits: Reduced duplication
```
