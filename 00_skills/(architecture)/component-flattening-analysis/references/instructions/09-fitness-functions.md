<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Fitness Functions

After flattening components, create automated checks:

### No Source Code in Root Namespaces

```javascript
// Alert if source code exists in root namespace
function checkRootNamespaceCode(namespaces, sourceFiles) {
  const violations = []

  namespaces.forEach((ns) => {
    // Check if namespace has been extended
    const hasChildren = namespaces.some((n) => n.startsWith(ns + '.') || n.startsWith(ns + '/'))

    if (hasChildren) {
      // Check if namespace contains source files
      const files = sourceFiles.filter((f) => f.namespace === ns)

      if (files.length > 0) {
        violations.push({
          namespace: ns,
          files: files.map((f) => f.name),
          issue: 'Root namespace contains source files (orphaned classes)',
        })
      }
    }
  })

  return violations
}
```

### Components Only as Leaf Nodes

```javascript
// Ensure components exist only as leaf nodes
function validateComponentStructure(namespaces, sourceFiles) {
  const violations = []

  // Find all leaf nodes (components)
  const leafNodes = namespaces.filter((ns) => {
    return !namespaces.some((n) => n.startsWith(ns + '.') || n.startsWith(ns + '/'))
  })

  // Check that all source files are in leaf nodes
  sourceFiles.forEach((file) => {
    if (!leafNodes.includes(file.namespace)) {
      violations.push({
        file: file.name,
        namespace: file.namespace,
        issue: 'Source file not in leaf node (component)',
      })
    }
  })

  return violations
}
```
