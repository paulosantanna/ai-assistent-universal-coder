<!-- Package: 00_skills/(architecture)/decomposition-planning-roadmap; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Assess Current State

Analyze what's already been done:

1. **Check Component Inventory**
   - Have components been identified and sized?
   - Is there a component inventory document?
   - Are oversized components identified?

2. **Check Common Component Analysis**
   - Have common domain components been identified?
   - Are consolidation opportunities documented?
   - Has coupling impact been analyzed?

3. **Check Component Structure**
   - Have components been flattened?
   - Are there orphaned classes?
   - Is component structure clean?

4. **Check Dependency Analysis**
   - Have component dependencies been mapped?
   - Is coupling analysis complete?
   - Is feasibility assessed?

5. **Check Domain Identification**
   - Have domains been identified?
   - Are components grouped into domains?
   - Are namespaces aligned with domains?

6. **Check Service Extraction**
   - Have any services been extracted?
   - Are domain services created?
   - Is service-based architecture in place?

**Output**: Current state assessment showing what's done and what's remaining

### Phase 2: Identify Patterns to Apply

Determine which decomposition patterns need to be applied:

1. **Review Pattern Prerequisites**
   - Pattern 1: Always needed (foundation)
   - Pattern 2: Needed if common components exist
   - Pattern 3: Needed if components have hierarchy
   - Pattern 4: Always needed (feasibility check)
   - Pattern 5: Needed before service extraction
   - Pattern 6: Final step (service extraction)

2. **Check Pattern Completion**
   - Which patterns are complete?
   - Which patterns are in progress?
   - Which patterns haven't started?

3. **Identify Missing Patterns**
   - What patterns still need to be applied?
   - What's blocking pattern application?
   - What dependencies exist?

**Output**: List of patterns to apply with status

### Phase 3: Prioritize Work

Prioritize decomposition patterns and work items:

1. **Assess Risk**
   - Low Risk: Infrastructure components, standalone functionality
   - Medium Risk: Domain components with some dependencies
   - High Risk: Core business logic, high coupling

2. **Assess Value**
   - High Value: Business-critical, high impact, frequent changes
   - Medium Value: Important but not critical
   - Low Value: Nice to have, low impact

3. **Assess Dependencies**
   - Independent: Can be done without other work
   - Dependent: Requires other patterns/work first
   - Blocking: Blocks other work from proceeding

4. **Calculate Priority Score**

   ```
   Priority = (Value × 3) - (Risk × 2) - (Dependencies × 1)

   Higher score = Higher priority
   ```

**Output**: Prioritized list of patterns and work items

### Phase 4: Create Phased Roadmap

Build a phased roadmap with milestones:

1. **Define Phases**
   - Phase 1: Analysis & Preparation
   - Phase 2: Domain Organization
   - Phase 3: Service Extraction
   - Phase 4: Optimization & Refinement

2. **Assign Patterns to Phases**
   - Which patterns belong in which phase?
   - What's the sequence within each phase?
   - What are the phase dependencies?

3. **Set Milestones**
   - What marks completion of each phase?
   - What are the success criteria?
   - What deliverables are expected?

4. **Estimate Timeline**
   - How long will each phase take?
   - What are the dependencies?
   - What's the critical path?

**Output**: Phased roadmap with timeline and milestones

### Phase 5: Generate Architecture Stories

Create architecture stories for tracking work:

1. **Create Story Template**

   ```
   As an architect, I need to [apply pattern/refactor component]
   to support [architectural characteristic/business need]
   so that [benefit/outcome]
   ```

2. **Break Down Work**
   - One story per pattern application
   - One story per major refactoring
   - One story per domain grouping

3. **Add Acceptance Criteria**
   - What defines "done"?
   - What metrics validate success?
   - What tests verify completion?

4. **Estimate Effort**
   - Story points or time estimates
   - Complexity assessment
   - Risk factors

**Output**: List of architecture stories with estimates

### Phase 6: Track Progress

Monitor progress through decomposition:

1. **Track Pattern Completion**
   - Which patterns are complete?
   - Which are in progress?
   - Which are blocked?

2. **Track Story Completion**
   - Stories completed
   - Stories in progress
   - Stories not started

3. **Track Metrics**
   - Components identified
   - Components refactored
   - Domains created
   - Services extracted

4. **Identify Blockers**
   - What's blocking progress?
   - What dependencies are missing?
   - What risks have emerged?

**Output**: Progress dashboard and status report
