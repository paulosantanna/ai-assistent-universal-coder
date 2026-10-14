<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Implementation Notes

### For Node.js/Express Applications

Common patterns to look for:

```
services/
├── CustomerService/
│   └── notification.js      ← Common pattern
├── TicketService/
│   └── notification.js     ← Common pattern
└── SurveyService/
    └── notification.js      ← Common pattern
```

**Shared Classes**:

- Check `require()` statements
- Look for classes imported from other components
- Example: `const SMTPConnection = require('../shared/SMTPConnection')`

### For Java Applications

Common patterns:

```
com.company.billing.audit     ← Common pattern
com.company.ticket.audit      ← Common pattern
com.company.survey.audit      ← Common pattern
```

**Shared Classes**:

- Check `import` statements
- Look for classes in common packages
- Example: `import com.company.shared.AuditLogger`

### Detection Strategies

**Namespace Pattern Detection**:

```javascript
// Extract leaf nodes from namespaces
function extractLeafNode(namespace) {
  const parts = namespace.split('/')
  return parts[parts.length - 1]
}

// Group by common leaf nodes
function groupByLeafNode(components) {
  const groups = {}
  components.forEach((comp) => {
    const leaf = extractLeafNode(comp.namespace)
    if (!groups[leaf]) groups[leaf] = []
    groups[leaf].push(comp)
  })
  return groups
}
```

**Shared Class Detection**:

```javascript
// Find classes used by multiple components
function findSharedClasses(components) {
  const classUsage = {}
  components.forEach((comp) => {
    comp.imports.forEach((imp) => {
      if (!classUsage[imp]) classUsage[imp] = []
      classUsage[imp].push(comp.name)
    })
  })

  return Object.entries(classUsage)
    .filter(([cls, users]) => users.length > 1)
    .map(([cls, users]) => ({ class: cls, usedBy: users }))
}
```
