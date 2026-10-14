<!-- Package: 00_skills/(architecture)/domain-identification-grouping; relative command/resource examples resolve from that package or workspace root. -->

## Domain Map

### Domain Structure
```

Customer Domain (ss.customer)
├── Customer Profile
├── Billing Payment
├── Billing History
└── Support Contract

Ticketing Domain (ss.ticket)
├── Ticket Shared
├── Ticket Maintenance
├── Ticket Completion
├── Ticket Assign
├── Ticket Route
├── KB Maintenance
├── KB Search
└── Survey

Reporting Domain (ss.reporting)
├── Reporting Shared
├── Ticket Reports
├── Expert Reports
└── Financial Reports

Admin Domain (ss.admin)
├── User Maintenance
└── Expert Profile

Shared Domain (ss.shared)
├── Login
└── Notification

```

### Domain Relationships

```

Ticketing Domain
│ uses
├─→ Shared Domain (Login, Notification)
└─→ Customer Domain (Customer Profile)

Customer Domain
│ uses
└─→ Shared Domain (Login, Notification)

Reporting Domain
│ uses
├─→ Ticketing Domain (Ticket data)
├─→ Customer Domain (Customer data)
└─→ Shared Domain (Login)

```

```

## Analysis Checklist

**Domain Identification**:

- [ ] Analyzed component responsibilities
- [ ] Identified business capabilities
- [ ] Identified distinct business domains
- [ ] Validated domains with stakeholders

**Component Grouping**:

- [ ] Assigned each component to a domain
- [ ] Analyzed component relationships
- [ ] Ensured components fit domain vocabulary
- [ ] Handled edge cases (shared components, unclear assignments)

**Domain Validation**:

- [ ] Checked cohesion within domains
- [ ] Verified domain boundaries are clear
- [ ] Ensured all components assigned
- [ ] Validated with stakeholders

**Namespace Refactoring**:

- [ ] Compared current vs target namespaces
- [ ] Identified components needing refactoring
- [ ] Created refactoring plan
- [ ] Prioritized refactoring work

**Domain Mapping**:

- [ ] Created domain diagram
- [ ] Documented domain structure
- [ ] Created domain inventory table
- [ ] Documented domain relationships

## Implementation Notes

### For Node.js/Express Applications

Domains typically organized in `services/` directory:

```
services/
├── customer/              ← Customer Domain
│   ├── profile/
│   ├── billing/
│   │   ├── payment/
│   │   └── history/
│   └── supportcontract/
├── ticket/                ← Ticketing Domain
│   ├── shared/
│   ├── maintenance/
│   ├── assign/
│   └── route/
└── reporting/             ← Reporting Domain
    ├── shared/
    ├── tickets/
    └── experts/
```

### For Java Applications

Domains identified by package structure:

```
com.company.customer       ← Customer Domain
├── profile
├── billing
│   ├── payment
│   └── history
└── supportcontract

com.company.ticket         ← Ticketing Domain
├── shared
├── maintenance
├── assign
└── route
```

### Domain Identification Strategies

**Strategy 1: Business Capability Analysis**

- Identify what business capabilities the system provides
- Group components by capability
- Example: "Customer Management" capability → Customer Domain

**Strategy 2: Vocabulary Analysis**

- Identify business vocabulary used by components
- Group components sharing same vocabulary
- Example: Components using "billing", "payment", "invoice" → Financial Domain

**Strategy 3: Relationship Analysis**

- Identify components frequently used together
- Group components with strong relationships
- Example: Components that share data/workflows → Same Domain

**Strategy 4: Stakeholder Collaboration**

- Work with product owners/business analysts
- Use their understanding of business areas
- Validate domain boundaries with them

## Fitness Functions

After creating domains, create automated checks:

### Domain Namespace Governance

```javascript
// Ensure components belong to correct domain
function validateDomainNamespaces(components, domainRules) {
  const violations = []

  components.forEach((comp) => {
    const domain = identifyDomain(comp.namespace)
    const expectedDomain = domainRules[comp.name]

    if (domain !== expectedDomain) {
      violations.push({
        component: comp.name,
        currentDomain: domain,
        expectedDomain: expectedDomain,
        namespace: comp.namespace,
      })
    }
  })

  return violations
}
```

### Domain Boundary Enforcement

```javascript
// Prevent components from accessing other domains directly
function enforceDomainBoundaries(components) {
  const violations = []

  components.forEach((comp) => {
    comp.imports.forEach((imp) => {
      const importedDomain = identifyDomain(imp)
      const componentDomain = identifyDomain(comp.namespace)

      if (importedDomain !== componentDomain && importedDomain !== 'shared') {
        violations.push({
          component: comp.name,
          domain: componentDomain,
          importsFrom: imp,
          importedDomain: importedDomain,
          issue: 'Cross-domain direct dependency',
        })
      }
    })
  })

  return violations
}
```

## Best Practices

### Do's ✅

- Collaborate with business stakeholders to identify domains
- Group components by business capability, not technical layers
- Ensure domains represent distinct business areas
- Validate domain boundaries with stakeholders
- Refactor namespaces to align with domains
- Create clear domain documentation
- Use business language in domain names

### Don'ts ❌

- Don't create domains based on technical layers (services, controllers, models)
- Don't force components into domains where they don't fit
- Don't skip stakeholder validation
- Don't create too many small domains (aim for 3-7 domains)
- Don't create domains that are too large (monolithic domains)
- Don't ignore components that don't fit (analyze why)
- Don't skip namespace refactoring (critical for clarity)

## Common Domain Patterns

### Typical Domains in Business Applications

- **Customer Domain**: Customer management, profiles, relationships
- **Product Domain**: Product catalog, inventory, pricing
- **Order Domain**: Order processing, fulfillment, shipping
- **Billing Domain**: Invoicing, payments, financial transactions
- **Reporting Domain**: Reports, analytics, dashboards
- **Admin Domain**: User management, system configuration
- **Shared Domain**: Common functionality (login, notification, utilities)

### Domain Size Guidelines

- **Small Domain**: 2-4 components
- **Medium Domain**: 5-8 components
- **Large Domain**: 9-15 components
- **Too Large**: >15 components (consider splitting)

## Next Steps

After creating component domains:

1. **Apply Create Domain Services Pattern** - Extract domains to separate services
2. **Plan Service Extraction** - Create migration plan for domain services
3. **Implement Domain Services** - Move domains to separately deployed services
4. **Monitor Domain Boundaries** - Use fitness functions to enforce boundaries

## Notes

- Domains should represent business capabilities, not technical layers
- Domain identification requires collaboration with business stakeholders
- Namespace refactoring is critical for domain clarity
- Domains prepare the codebase for service-based architecture
- Well-formed domains make service extraction easier
- Domain boundaries should be clear and well-documented
