<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Map Component Structure

Scan directory/namespace structure to identify hierarchy:

1. **Map Namespace Tree**
   - Build tree of all namespaces
   - Identify parent-child relationships
   - Mark leaf nodes (components)

2. **Identify Root Namespaces**
   - Find namespaces that have been extended
   - Mark as root namespaces (subdomains)
   - Note which namespaces extend them

3. **Locate Source Files**
   - Find all source files in each namespace
   - Map files to their namespace location
   - Identify files in root namespaces

**Example Structure Mapping**:

```markdown
## Component Structure Map
```

ss.survey/ ← Root namespace (extended)
├── Survey.js ← Orphaned class
├── SurveyProcessor.js ← Orphaned class
└── templates/ ← Component (leaf node)
├── EmailTemplate.js
└── SMSTemplate.js

ss.ticket/ ← Root namespace (extended)
├── Ticket.js ← Orphaned class
├── assign/ ← Component (leaf node)
│ └── TicketAssign.js
└── route/ ← Component (leaf node)
└── TicketRoute.js

```

```

### Phase 2: Identify Orphaned Classes

Find source files in root namespaces:

1. **Scan Root Namespaces**
   - Check each root namespace for source files
   - Identify files that are orphaned
   - Count orphaned files per root namespace

2. **Classify Orphaned Classes**
   - **Shared Code**: Common utilities, interfaces, abstract classes
   - **Domain Code**: Business logic that should be in component
   - **Mixed**: Combination of shared and domain code

3. **Assess Impact**
   - How many files are orphaned?
   - What functionality do they contain?
   - What components depend on them?

**Example Orphaned Class Detection**:

```markdown
## Orphaned Classes Found

### Root Namespace: ss.survey

**Orphaned Files** (5 files):

- Survey.js (domain code - survey creation)
- SurveyProcessor.js (domain code - survey processing)
- SurveyValidator.js (shared code - validation)
- SurveyFormatter.js (shared code - formatting)
- SurveyConstants.js (shared code - constants)

**Classification**:

- Domain Code: 2 files (should be in components)
- Shared Code: 3 files (should be in .shared component)

**Dependencies**: Used by ss.survey.templates component
```

### Phase 3: Analyze Flattening Options

Determine best flattening strategy for each root namespace:

1. **Option 1: Consolidate Down**
   - Move leaf node code into root namespace
   - Makes root namespace the component
   - **Use when**: Leaf nodes are small, related functionality

2. **Option 2: Split Up**
   - Move root namespace code into new leaf nodes
   - Creates multiple components from root
   - **Use when**: Root namespace has distinct functional areas

3. **Option 3: Move Shared Code**
   - Extract shared code to `.shared` component
   - Keep domain code in root or split
   - **Use when**: Root namespace has shared utilities

**Example Flattening Analysis**:

```markdown
## Flattening Options Analysis

### Root Namespace: ss.survey

**Current State**:

- Root namespace: 5 orphaned files
- Leaf component: ss.survey.templates (7 files)

**Option 1: Consolidate Down** ✅ Recommended

- Move templates code into ss.survey
- Result: Single component ss.survey
- Effort: Low (7 files to move)
- Rationale: Templates are small, related to survey functionality

**Option 2: Split Up**

- Create ss.survey.create (2 files)
- Create ss.survey.process (1 file)
- Create ss.survey.shared (3 files)
- Keep ss.survey.templates (7 files)
- Effort: High (multiple components to create)
- Rationale: More granular, but may be over-engineering

**Option 3: Move Shared Code**

- Create ss.survey.shared (3 shared files)
- Keep domain code in root (2 files)
- Keep ss.survey.templates (7 files)
- Effort: Medium
- Rationale: Separates shared from domain, but still has hierarchy
```

### Phase 4: Create Flattening Plan

Generate refactoring plan for each root namespace:

1. **Select Strategy**
   - Choose best flattening option
   - Consider effort, complexity, maintainability

2. **Plan Refactoring Steps**
   - List files to move
   - Identify target namespaces
   - Note dependencies to update

3. **Estimate Effort**
   - Time to refactor
   - Risk assessment
   - Testing requirements

**Example Flattening Plan**:

```markdown
## Flattening Plan

### Priority: High

**Root Namespace: ss.survey**

**Strategy**: Consolidate Down

**Steps**:

1. Move files from ss.survey.templates/ to ss.survey/
   - EmailTemplate.js
   - SMSTemplate.js
   - [5 more files]

2. Update imports in dependent components
   - Update references from ss.survey.templates._ to ss.survey._

3. Remove ss.survey.templates/ directory

4. Update namespace declarations
   - Change namespace from ss.survey.templates to ss.survey

5. Run tests to verify changes

**Effort**: 2-3 days
**Risk**: Low (templates are self-contained)
**Dependencies**: None
```

### Phase 5: Execute Flattening

Perform the refactoring:

1. **Move Files**
   - Move source files to target namespace
   - Update file paths and imports

2. **Update References**
   - Update imports in dependent components
   - Update namespace declarations
   - Update directory structure

3. **Verify Changes**
   - Run tests
   - Check for broken references
   - Validate component structure
