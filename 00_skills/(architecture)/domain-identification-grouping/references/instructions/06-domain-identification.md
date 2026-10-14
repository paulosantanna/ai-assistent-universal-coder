<!-- Package: 00_skills/(architecture)/domain-identification-grouping; relative command/resource examples resolve from that package or workspace root. -->

## Domain Identification

### Domain: Customer (ss.customer)

**Business Capability**: Manages customer relationships, billing, and support contracts

**Components**:
- Customer Profile (ss.customer.profile)
- Billing Payment (ss.customer.billing.payment)
- Billing History (ss.customer.billing.history)
- Support Contract (ss.customer.supportcontract)

**Component Count**: 4
**Total Size**: ~15,000 statements (18% of codebase)

**Domain Cohesion**: ✅ High
- Components share customer-related vocabulary
- Components frequently used together
- Direct relationships between components

**Boundaries**:
- Clear separation from Ticketing domain
- Clear separation from Reporting domain
- Shared components (Notification) used by all domains
````

### Component Domain Assignment Table

```markdown
