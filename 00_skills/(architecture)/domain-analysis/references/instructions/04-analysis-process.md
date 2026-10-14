<!-- Package: 00_skills/(architecture)/domain-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Extract Concepts

Scan codebase for business concepts (not infrastructure):

1. **Entities** (domain models with identity)
   - Patterns: `@Entity`, `class`, domain models
   - Focus: Business concepts, not technical classes

2. **Services** (business operations)
   - Patterns: `*Service`, `*Manager`, `*Handler`
   - Focus: Business logic, not technical utilities

3. **Use Cases** (business workflows)
   - Patterns: `*UseCase`, `*Command`, `*Handler`
   - Focus: Business processes, not CRUD

4. **Controllers/Resolvers** (entry points)
   - Patterns: `*Controller`, `*Resolver`, API endpoints
   - Focus: Business capabilities, not technical routes

### Phase 2: Group by Ubiquitous Language

For each concept, determine:

**Primary Language Context**

- What business vocabulary does this belong to?
- Examples:
  - `Subscription`, `Invoice`, `Payment` → Billing language
  - `Movie`, `Video`, `Episode` → Content language
  - `User`, `Authentication` → Identity language

**Linguistic Boundaries**

- Where do term meanings change?
- Same term, different meaning = different bounded context
- Example: "Customer" in Sales vs "Customer" in Support

**Concept Relationships**

- Which concepts naturally belong together?
- Which share business vocabulary?
- Which reference each other?

### Phase 3: Identify Subdomains

A subdomain has:

- Distinct business capability
- Independent business value
- Unique vocabulary
- Multiple related entities working together
- Cohesive set of business operations

**Common Domain Patterns**:

- Billing/Subscription: Payments, invoices, plans
- Content/Catalog: Media, products, inventory
- Identity/Access: Users, authentication, authorization
- Analytics: Metrics, dashboards, insights
- Notifications: Messages, alerts, communications

**Classify Each Subdomain**:

Use this decision tree:

```
Is it a competitive advantage?
  YES → Core Domain
  NO → Does it require business-specific knowledge?
        YES → Supporting Subdomain
        NO → Generic Subdomain
```

### Phase 4: Assess Cohesion

**High Cohesion Indicators** ✅

- Concepts share Ubiquitous Language
- Concepts frequently used together
- Direct business relationships
- Changes to one affect others in group
- Solve same business problem

**Low Cohesion Indicators** ❌

- Different business vocabularies mixed
- Concepts rarely used together
- No direct business relationship
- Changes don't affect others
- Solve different business problems

**Cohesion Score Formula**:

```
Score = (
  Linguistic Cohesion (0-3) +    // Shared vocabulary
  Usage Cohesion (0-3) +         // Used together
  Data Cohesion (0-2) +          // Entity relationships
  Change Cohesion (0-2)          // Change together
) / 10

8-10: High Cohesion ✅
5-7:  Medium Cohesion ⚠️
0-4:  Low Cohesion ❌
```

### Phase 5: Detect Low Cohesion Issues

**Rule 1: Linguistic Mismatch**

- Problem: Different business vocabularies mixed
- Example: `User` (identity) + `Subscription` (billing) in same service
- Action: Suggest separation into different bounded contexts

**Rule 2: Cross-Domain Dependencies**

- Problem: Tight coupling between domains
- Example: Service A directly instantiates entities from Domain B
- Action: Suggest interface-based integration

**Rule 3: Mixed Responsibilities**

- Problem: Single class handles multiple business concerns
- Example: Service handling both billing and content
- Action: Suggest splitting by subdomain

**Rule 4: Generic in Core**

- Problem: Generic functionality in core business logic
- Example: Email sending in billing service
- Action: Extract to Generic Subdomain

**Rule 5: Unclear Boundaries**

- Problem: Cannot determine which domain concept belongs to
- Example: Entity with relationships to multiple domains
- Action: Clarify boundaries, possibly split concept

### Phase 6: Map Bounded Contexts

For each subdomain identified, suggest bounded context:

**Bounded Context Characteristics**:

- Name reflects Ubiquitous Language
- Contains complete domain model
- Has explicit integration points
- Clear linguistic boundary

**Integration Patterns**:

- Shared Kernel: Shared model between contexts (use sparingly)
- Customer/Supplier: Downstream depends on upstream
- Conformist: Downstream conforms to upstream
- Anti-corruption Layer: Translation layer between contexts
- Open Host Service: Published interface for integration
- Published Language: Well-documented integration protocol
