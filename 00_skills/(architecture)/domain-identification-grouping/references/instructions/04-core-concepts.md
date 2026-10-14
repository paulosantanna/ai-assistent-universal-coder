<!-- Package: 00_skills/(architecture)/domain-identification-grouping; relative command/resource examples resolve from that package or workspace root. -->

## Core Concepts

### Domain Definition

A **domain** is a logical grouping of components that:

- Represents a distinct business capability or area
- Contains related components that work together
- Has clear boundaries and responsibilities
- Can become a domain service in service-based architecture

**Examples**:

- **Customer Domain**: Customer profile, billing, support contracts
- **Ticketing Domain**: Ticket creation, assignment, routing, completion
- **Reporting Domain**: Ticket reports, expert reports, financial reports

### Component Domain Relationship

**One-to-Many**: A single domain contains multiple components

```
Domain: Customer
├── Component: Customer Profile
├── Component: Billing Payment
├── Component: Billing History
└── Component: Support Contract
```

### Domain Manifestation

Domains are physically manifested through **namespace structure**:

**Before Domain Alignment**:

```
services/billing/payment
services/billing/history
services/customer/profile
services/supportcontract
```

**After Domain Alignment**:

```
services/customer/billing/payment
services/customer/billing/history
services/customer/profile
services/customer/supportcontract
```

Notice how all customer-related functionality is grouped under `.customer` domain.
