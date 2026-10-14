<!-- Package: 00_skills/(architecture)/decomposition-planning-roadmap; relative command/resource examples resolve from that package or workspace root. -->

## Core Concepts

### Decomposition Pattern Sequence

The six component-based decomposition patterns should be applied in sequence:

1. **Identify and Size Components** - Understand what you have
2. **Gather Common Domain Components** - Find duplicates
3. **Flatten Components** - Remove orphaned classes
4. **Determine Component Dependencies** - Assess coupling
5. **Create Component Domains** - Group into domains
6. **Create Domain Services** - Extract to services

### Phased Approach

Decomposition typically follows phases:

**Phase 1: Analysis & Preparation** (Patterns 1-4)

- Component identification and sizing
- Common component detection
- Component flattening
- Dependency analysis

**Phase 2: Domain Organization** (Pattern 5)

- Domain identification
- Component grouping
- Namespace refactoring

**Phase 3: Service Extraction** (Pattern 6)

- Domain service creation
- Service extraction
- API boundary definition

### Prioritization Factors

When prioritizing decomposition work, consider:

- **Risk**: Low risk = easier to extract, fewer dependencies
- **Value**: High value = business-critical, high impact
- **Dependencies**: Can this be done independently?
- **Complexity**: Simple = fewer components, clear boundaries
- **Coupling**: Low coupling = easier to extract
