<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Core Concepts

### Domain vs Infrastructure Functionality

**Domain Functionality** (candidates for consolidation):

- Business processing logic (notification, validation, auditing, formatting)
- Common to **some** processes, not all
- Examples: Customer notification, ticket auditing, data validation

**Infrastructure Functionality** (usually not consolidated here):

- Operational concerns (logging, metrics, security)
- Common to **all** processes
- Examples: Logging, authentication, database connections

### Common Domain Patterns

Common domain functionality often appears as:

1. **Namespace Patterns**: Components ending in same leaf node
   - `*.notification`, `*.audit`, `*.validation`, `*.formatting`
   - Example: `TicketNotification`, `BillingNotification`, `SurveyNotification`

2. **Shared Classes**: Same class used across multiple components
   - Example: `SMTPConnection` used by 5 different components
   - Example: `AuditLogger` used by multiple domain components

3. **Similar Functionality**: Different components doing similar things
   - Example: Multiple components sending emails with slight variations
   - Example: Multiple components writing audit logs

### Consolidation Approaches

**Shared Service**:

- Common functionality becomes a separate service
- Other components call this service
- Good for: Frequently changing logic, complex operations

**Shared Library**:

- Common code packaged as library (JAR, DLL, npm package)
- Components import and use the library
- Good for: Stable functionality, simple utilities

**Component Consolidation**:

- Merge multiple components into one
- Good for: Highly related functionality, low coupling impact
