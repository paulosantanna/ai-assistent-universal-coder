<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Identify Common Namespace Patterns

Scan component namespaces for common leaf node names:

1. **Extract leaf nodes** from all component namespaces
   - Example: `services/billing/notification` → `notification`
   - Example: `services/ticket/notification` → `notification`

2. **Group by common leaf nodes**
   - Find components with same leaf node name
   - Example: All components ending in `.notification`

3. **Filter out infrastructure patterns**
   - Exclude: `.util`, `.helper`, `.common` (usually infrastructure)
   - Focus on: `.notification`, `.audit`, `.validation`, `.formatting`

**Example Output**:

```markdown
## Common Namespace Patterns Found

**Notification Components**:

- services/customer/notification
- services/ticket/notification
- services/survey/notification

**Audit Components**:

- services/billing/audit
- services/ticket/audit
- services/survey/audit
```

### Phase 2: Detect Shared Classes

Find classes/files used across multiple components:

1. **Scan imports/dependencies** in each component
   - Track which classes are imported from where
   - Note classes used by multiple components

2. **Identify shared classes**
   - Classes imported by 2+ components
   - Exclude infrastructure classes (Logger, Config, etc.)

3. **Classify as domain vs infrastructure**
   - Domain: Business logic classes (SMTPConnection, AuditLogger)
   - Infrastructure: Technical utilities (Logger, DatabaseConnection)

**Example Output**:

```markdown
## Shared Classes Found

**Domain Classes**:

- `SMTPConnection` - Used by 5 components (notification-related)
- `AuditLogger` - Used by 8 components (audit-related)
- `DataFormatter` - Used by 3 components (formatting-related)

**Infrastructure Classes** (exclude from consolidation):

- `Logger` - Used by all components (infrastructure)
- `Config` - Used by all components (infrastructure)
```

### Phase 3: Analyze Functionality Similarity

For each group of common components:

1. **Examine functionality**
   - Read source code of each component
   - Identify what each component does
   - Note similarities and differences

2. **Assess consolidation feasibility**
   - Are differences minor (configurable)?
   - Can differences be abstracted?
   - Is functionality truly the same?

3. **Calculate coupling impact**
   - Count incoming dependencies (afferent coupling) before consolidation
   - Estimate incoming dependencies after consolidation
   - Compare total coupling levels

**Example Analysis**:

```markdown
## Functionality Analysis

**Notification Components**:

- CustomerNotification: Sends billing notifications
- TicketNotification: Sends ticket assignment notifications
- SurveyNotification: Sends survey emails

**Similarities**: All send emails to customers
**Differences**: Email content/templates, triggers

**Consolidation Feasibility**: ✅ High

- Differences are in content, not mechanism
- Can be abstracted with templates/context
```

### Phase 4: Assess Coupling Impact

Before recommending consolidation, analyze coupling:

1. **Calculate current coupling**
   - Count components using each notification component
   - Sum total incoming dependencies

2. **Estimate consolidated coupling**
   - Count components that would use consolidated component
   - Compare to current total

3. **Evaluate coupling increase**
   - Is consolidated component too coupled?
   - Does it create a bottleneck?
   - Is coupling increase acceptable?

**Example Coupling Analysis**:

```markdown
## Coupling Impact Analysis

**Before Consolidation**:

- CustomerNotification: Used by 2 components (CA = 2)
- TicketNotification: Used by 2 components (CA = 2)
- SurveyNotification: Used by 1 component (CA = 1)
- **Total CA**: 5

**After Consolidation**:

- Notification: Used by 5 components (CA = 5)
- **Total CA**: 5 (same!)

**Verdict**: ✅ No coupling increase, safe to consolidate
```

### Phase 5: Recommend Consolidation Approach

Based on analysis, recommend approach:

**Shared Service** (if):

- Functionality changes frequently
- Complex operations
- Needs independent scaling
- Multiple deployment units will use it

**Shared Library** (if):

- Stable functionality
- Simple utilities
- Compile-time dependency acceptable
- No need for independent deployment

**Component Consolidation** (if):

- Highly related functionality
- Low coupling impact
- Same deployment unit acceptable
