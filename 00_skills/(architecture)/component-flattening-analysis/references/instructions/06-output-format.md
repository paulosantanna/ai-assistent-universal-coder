<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Output Format

### Orphaned Classes Report

```markdown
## Orphaned Classes Analysis

### Root Namespace: ss.survey

**Status**: ⚠️ Has Orphaned Classes

**Orphaned Files** (5 files):

- Survey.js (domain code)
- SurveyProcessor.js (domain code)
- SurveyValidator.js (shared code)
- SurveyFormatter.js (shared code)
- SurveyConstants.js (shared code)

**Leaf Components**:

- ss.survey.templates (7 files)

**Issue**: Root namespace contains code but is extended by leaf component

**Recommendation**: Consolidate templates into root namespace
```

### Component Hierarchy Issues

```markdown
## Component Hierarchy Issues

| Root Namespace | Orphaned Files | Leaf Components                 | Issue                | Recommendation   |
| -------------- | -------------- | ------------------------------- | -------------------- | ---------------- |
| ss.survey      | 5              | 1 (templates)                   | Has orphaned classes | Consolidate down |
| ss.ticket      | 45             | 2 (assign, route)               | Large orphaned code  | Split up         |
| ss.reporting   | 0              | 3 (tickets, experts, financial) | No issue             | ✅ OK            |
```

### Flattening Plan

```markdown
## Flattening Plan

### Priority: High

**ss.survey** → Consolidate Down

- Move 7 files from templates to root
- Effort: 2-3 days
- Risk: Low

### Priority: Medium

**ss.ticket** → Split Up

- Create ss.ticket.maintenance (30 files)
- Create ss.ticket.completion (10 files)
- Create ss.ticket.shared (5 files)
- Effort: 1 week
- Risk: Medium
```
