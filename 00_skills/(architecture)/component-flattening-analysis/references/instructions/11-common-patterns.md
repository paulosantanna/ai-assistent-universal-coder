<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Common Patterns

### Pattern 1: Simple Consolidation

**Before**:

```
ss.survey/
├── Survey.js           ← Orphaned
└── templates/          ← Component
    └── Template.js
```

**After**:

```
ss.survey/              ← Component (leaf node)
├── Survey.js
└── Template.js
```

### Pattern 2: Functional Split

**Before**:

```
ss.ticket/              ← Root namespace
├── Ticket.js           ← Orphaned (45 files)
├── assign/             ← Component
└── route/              ← Component
```

**After**:

```
ss.ticket/              ← Subdomain
├── maintenance/        ← Component
│   └── Ticket.js
├── completion/        ← Component
│   └── TicketCompletion.js
├── assign/             ← Component
└── route/              ← Component
```

### Pattern 3: Shared Code Extraction

**Before**:

```
ss.survey/              ← Root namespace
├── Survey.js           ← Domain code
├── SurveyValidator.js  ← Shared code
└── templates/          ← Component
```

**After**:

```
ss.survey/              ← Component
├── Survey.js
└── shared/             ← Component
    └── SurveyValidator.js
```
