<!-- Package: 00_skills/(architecture)/decomposition-planning-roadmap; relative command/resource examples resolve from that package or workspace root. -->

## Output Format

### Decomposition Roadmap

```markdown
# Decomposition Roadmap

## Current State Assessment

**Completed Patterns**:

- ✅ Pattern 1: Identify and Size Components
- ✅ Pattern 2: Gather Common Domain Components
- ⚠️ Pattern 3: Flatten Components (in progress)
- ❌ Pattern 4: Determine Component Dependencies (not started)
- ❌ Pattern 5: Create Component Domains (not started)
- ❌ Pattern 6: Create Domain Services (not started)

**Key Findings**:

- 75 components identified
- 3 common domain components found
- 2 oversized components need splitting
- High database coupling detected

## Phased Roadmap

### Phase 1: Analysis & Preparation (Weeks 1-4)

**Goal**: Complete component analysis and refactoring

**Patterns**:

1. Complete Pattern 3: Flatten Components
2. Apply Pattern 4: Determine Component Dependencies
3. Refactor oversized components

**Milestones**:

- Week 2: Component flattening complete
- Week 4: Dependency analysis complete

**Deliverables**:

- Flattened component structure
- Dependency diagram
- Feasibility assessment

### Phase 2: Domain Organization (Weeks 5-8)

**Goal**: Organize components into domains

**Patterns**:

1. Apply Pattern 5: Create Component Domains
2. Refactor namespaces for domain alignment

**Milestones**:

- Week 6: Domains identified
- Week 8: Namespace refactoring complete

**Deliverables**:

- Domain map
- Refactored component namespaces
- Domain documentation

### Phase 3: Service Extraction (Weeks 9-16)

**Goal**: Extract domains to domain services

**Patterns**:

1. Apply Pattern 6: Create Domain Services
2. Extract services incrementally

**Milestones**:

- Week 12: First domain service extracted
- Week 16: All domain services extracted

**Deliverables**:

- Domain services deployed
- API boundaries defined
- Service documentation
```

### Prioritized Work Plan

```markdown
## Prioritized Work Plan

### High Priority (Do First)

1. **Complete Component Flattening** (Priority: 9/10)
   - Risk: Low
   - Value: High (enables domain grouping)
   - Dependencies: None
   - Effort: 2 weeks

2. **Dependency Analysis** (Priority: 8/10)
   - Risk: Low
   - Value: High (validates feasibility)
   - Dependencies: Component flattening
   - Effort: 1 week

### Medium Priority (Do Next)

3. **Domain Identification** (Priority: 7/10)
   - Risk: Medium
   - Value: High (enables service extraction)
   - Dependencies: Dependency analysis
   - Effort: 2 weeks

### Low Priority (Do Later)

4. **Service Extraction** (Priority: 5/10)
   - Risk: High
   - Value: High (final goal)
   - Dependencies: Domain identification
   - Effort: 8 weeks
```

### Architecture Stories

```markdown
## Architecture Stories

### Story 1: Flatten Ticket Components

**As an architect**, I need to flatten the Ticket component hierarchy
to support better component organization
so that components exist only as leaf nodes.

**Acceptance Criteria**:

- [ ] No orphaned classes in root namespaces
- [ ] All components are leaf nodes
- [ ] Component structure validated

**Estimate**: 5 story points
**Priority**: High
**Dependencies**: None

### Story 2: Identify Component Domains

**As an architect**, I need to group components into logical domains
to support service-based architecture
so that components can be extracted to domain services.

**Acceptance Criteria**:

- [ ] All components assigned to domains
- [ ] Domain boundaries validated with stakeholders
- [ ] Domain map created

**Estimate**: 8 story points
**Priority**: High
**Dependencies**: Component flattening complete
```

### Progress Dashboard

```markdown
## Decomposition Progress Dashboard

### Pattern Completion Status

| Pattern                    | Status         | Progress | Blocker                 |
| -------------------------- | -------------- | -------- | ----------------------- |
| Identify & Size Components | ✅ Complete    | 100%     | None                    |
| Gather Common Components   | ✅ Complete    | 100%     | None                    |
| Flatten Components         | ⚠️ In Progress | 60%      | None                    |
| Determine Dependencies     | ❌ Not Started | 0%       | Waiting on flattening   |
| Create Domains             | ❌ Not Started | 0%       | Waiting on dependencies |
| Create Domain Services     | ❌ Not Started | 0%       | Waiting on domains      |

### Story Completion Status

**Completed**: 5 stories (25%)
**In Progress**: 3 stories (15%)
**Not Started**: 12 stories (60%)

### Key Metrics

- Components Identified: 75
- Components Refactored: 45 (60%)
- Domains Created: 0
- Services Extracted: 0
```
