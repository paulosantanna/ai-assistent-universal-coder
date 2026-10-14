<!-- Package: 00_skills/(architecture)/domain-identification-grouping; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Identify Business Domains

Analyze the codebase to identify distinct business domains:

1. **Examine Component Responsibilities**
   - Read component names and descriptions
   - Understand what each component does
   - Identify business capabilities

2. **Look for Business Language**
   - Group components by business vocabulary
   - Example: "billing", "payment", "invoice" → Financial domain
   - Example: "customer", "profile", "contract" → Customer domain

3. **Identify Domain Boundaries**
   - Where do business concepts change?
   - What are the distinct business areas?
   - How do components relate to business capabilities?

4. **Collaborate with Business Stakeholders**
   - Validate domain identification with product owners
   - Ensure domains align with business understanding
   - Get feedback on domain boundaries

**Example Domain Identification**:

```markdown
## Identified Domains

1. **Ticketing Domain** (ss.ticket)
   - Ticket creation, assignment, routing, completion
   - Customer surveys
   - Knowledge base

2. **Customer Domain** (ss.customer)
   - Customer profile
   - Billing and payment
   - Support contracts

3. **Reporting Domain** (ss.reporting)
   - Ticket reports
   - Expert reports
   - Financial reports

4. **Admin Domain** (ss.admin)
   - User maintenance
   - Expert profile management

5. **Shared Domain** (ss.shared)
   - Login
   - Notification
```

### Phase 2: Group Components into Domains

Assign each component to an appropriate domain:

1. **Analyze Component Functionality**
   - What business capability does it support?
   - What domain vocabulary does it use?
   - What other components does it relate to?

2. **Check Component Relationships**
   - Which components are frequently used together?
   - What are the dependencies between components?
   - Do components share data or workflows?

3. **Assign to Domain**
   - Place component in domain that best fits its functionality
   - Ensure component aligns with domain's business language
   - Verify component relationships support domain grouping

4. **Handle Edge Cases**
   - Components that don't fit clearly: Analyze more deeply
   - Components that fit multiple domains: Choose primary domain
   - Shared components: May belong to Shared domain

**Example Component Grouping**:

```markdown
## Component Domain Assignment

### Ticketing Domain (ss.ticket)

- Ticket Shared (ss.ticket.shared)
- Ticket Maintenance (ss.ticket.maintenance)
- Ticket Completion (ss.ticket.completion)
- Ticket Assign (ss.ticket.assign)
- Ticket Route (ss.ticket.route)
- KB Maintenance (ss.ticket.kb.maintenance)
- KB Search (ss.ticket.kb.search)
- Survey (ss.ticket.survey)

### Customer Domain (ss.customer)

- Customer Profile (ss.customer.profile)
- Billing Payment (ss.customer.billing.payment)
- Billing History (ss.customer.billing.history)
- Support Contract (ss.customer.supportcontract)

### Reporting Domain (ss.reporting)

- Reporting Shared (ss.reporting.shared)
- Ticket Reports (ss.reporting.tickets)
- Expert Reports (ss.reporting.experts)
- Financial Reports (ss.reporting.financial)
```

### Phase 3: Validate Domain Groupings

Ensure components fit well in their assigned domains:

1. **Check Cohesion**
   - Do components in domain share business language?
   - Are components frequently used together?
   - Do components have direct relationships?

2. **Verify Boundaries**
   - Are domain boundaries clear?
   - Do components belong to only one domain?
   - Are there components that don't fit anywhere?

3. **Assess Completeness**
   - Are all components assigned to a domain?
   - Are domains cohesive and well-formed?
   - Do domains represent distinct business capabilities?

4. **Get Stakeholder Validation**
   - Review domain groupings with product owners
   - Ensure domains align with business understanding
   - Get feedback on domain boundaries

**Validation Checklist**:

- [ ] All components assigned to a domain
- [ ] Domains have clear boundaries
- [ ] Components fit well in their domains
- [ ] Domains represent distinct business capabilities
- [ ] Stakeholders validate domain groupings

### Phase 4: Refactor Namespaces for Domain Alignment

Align component namespaces with identified domains:

1. **Compare Current vs Target Namespaces**
   - Current: `services/billing/payment`
   - Target: `services/customer/billing/payment`
   - Change: Add `.customer` domain node

2. **Identify Refactoring Needed**
   - Which components need namespace changes?
   - What domain nodes need to be added?
   - Are there components already aligned?

3. **Create Refactoring Plan**
   - List components needing namespace changes
   - Specify target namespace for each
   - Prioritize refactoring work

4. **Execute Refactoring**
   - Update component namespaces
   - Update imports/references
   - Verify all references updated

**Example Namespace Refactoring**:

```markdown
## Namespace Refactoring Plan

### Customer Domain Alignment

| Component        | Current Namespace   | Target Namespace            | Action        |
| ---------------- | ------------------- | --------------------------- | ------------- |
| Billing Payment  | ss.billing.payment  | ss.customer.billing.payment | Add .customer |
| Billing History  | ss.billing.history  | ss.customer.billing.history | Add .customer |
| Customer Profile | ss.customer.profile | ss.customer.profile         | No change     |
| Support Contract | ss.supportcontract  | ss.customer.supportcontract | Add .customer |

### Ticketing Domain Alignment

| Component      | Current Namespace | Target Namespace         | Action      |
| -------------- | ----------------- | ------------------------ | ----------- |
| KB Maintenance | ss.kb.maintenance | ss.ticket.kb.maintenance | Add .ticket |
| KB Search      | ss.kb.search      | ss.ticket.kb.search      | Add .ticket |
| Survey         | ss.survey         | ss.ticket.survey         | Add .ticket |
```

### Phase 5: Create Domain Map

Visualize domain structure and component groupings:

1. **Create Domain Diagram**
   - Show domains as boxes
   - Show components within each domain
   - Show relationships between domains

2. **Document Domain Structure**
   - List domains and their components
   - Describe domain responsibilities
   - Note domain boundaries

3. **Create Domain Inventory**
   - Table of domains and components
   - Component counts per domain
   - Size metrics per domain

**Example Domain Map**:

```markdown
## Domain Map
```

┌─────────────────────────────────────┐
│ Ticketing Domain (ss.ticket) │
├─────────────────────────────────────┤
│ • Ticket Shared │
│ • Ticket Maintenance │
│ • Ticket Completion │
│ • Ticket Assign │
│ • Ticket Route │
│ • KB Maintenance │
│ • KB Search │
│ • Survey │
└─────────────────────────────────────┘
│
│ uses
▼
┌─────────────────────────────────────┐
│ Customer Domain (ss.customer) │
├─────────────────────────────────────┤
│ • Customer Profile │
│ • Billing Payment │
│ • Billing History │
│ • Support Contract │
└─────────────────────────────────────┘

````

## Output Format

### Domain Identification Report

```markdown
