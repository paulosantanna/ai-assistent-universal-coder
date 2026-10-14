<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Implementation Notes

### For Node.js/Express Applications

Components typically in `services/` directory:

```
services/
├── survey/              ← Root namespace (extended)
│   ├── Survey.js       ← Orphaned class
│   └── templates/      ← Component (leaf node)
│       └── Template.js
```

**Flattening**:

- Consolidate: Move `templates/` files to `survey/`
- Split: Create `survey/create/` and `survey/process/`
- Shared: Create `survey/shared/` for utilities

### For Java Applications

Components identified by package structure:

```
com.company.survey       ← Root package (extended)
├── Survey.java         ← Orphaned class
└── templates/          ← Component (leaf package)
    └── Template.java
```

**Flattening**:

- Consolidate: Move `templates` classes to `survey` package
- Split: Create `survey.create` and `survey.process` packages
- Shared: Create `survey.shared` package

### Detection Strategies

**Find Root Namespaces with Code**:

```javascript
// Find root namespaces containing source files
function findRootNamespacesWithCode(namespaces, sourceFiles) {
  const rootNamespaces = namespaces.filter((ns) => {
    // Check if namespace has been extended
    const hasChildren = namespaces.some((n) => n.startsWith(ns + '.') || n.startsWith(ns + '/'))

    // Check if namespace contains source files
    const hasFiles = sourceFiles.some((f) => f.namespace === ns)

    return hasChildren && hasFiles
  })

  return rootNamespaces
}
```

**Find Orphaned Classes**:

```javascript
// Find orphaned classes in root namespaces
function findOrphanedClasses(rootNamespaces, sourceFiles) {
  const orphaned = []

  rootNamespaces.forEach((rootNs) => {
    const files = sourceFiles.filter((f) => f.namespace === rootNs)
    orphaned.push({
      rootNamespace: rootNs,
      files: files,
      count: files.length,
    })
  })

  return orphaned
}
```
