<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Core Concepts

### Component Definition

A **component** is identified by a **leaf node** in directory/namespace structure:

- **Leaf Node**: The deepest directory containing source files
- **Component**: Source code files in leaf node namespace
- **Subdomain**: Parent namespace that has been extended

**Key Rule**: Components exist only as leaf nodes. If a namespace is extended, the parent becomes a subdomain, not a component.

### Root Namespace

A **root namespace** is a namespace node that has been extended:

- **Extended**: Another namespace node added below it
- **Example**: `ss.survey` extended to `ss.survey.templates`
- **Result**: `ss.survey` becomes a root namespace (subdomain)

### Orphaned Classes

**Orphaned classes** are source files in root namespaces:

- **Location**: Root namespace (non-leaf node)
- **Problem**: No definable component associated with them
- **Solution**: Move to leaf node namespace (component)

**Example**:

```
ss.survey/              ← Root namespace (extended by .templates)
├── Survey.js           ← Orphaned class (in root namespace)
└── templates/          ← Component (leaf node)
    └── Template.js
```

### Flattening Strategies

**Strategy 1: Consolidate Down**

- Move code from leaf nodes into root namespace
- Makes root namespace the component
- Example: Move `ss.survey.templates` → `ss.survey`

**Strategy 2: Split Up**

- Move code from root namespace into new leaf nodes
- Creates new components from root namespace
- Example: Split `ss.survey` → `ss.survey.create` + `ss.survey.process`

**Strategy 3: Move Shared Code**

- Move shared code to dedicated component
- Creates `.shared` component
- Example: `ss.survey` shared code → `ss.survey.shared`
