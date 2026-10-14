<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Fitness Functions

After identifying common components, create automated checks:

### Common Namespace Pattern Detection

```javascript
// Alert if new components with common patterns are created
function checkCommonPatterns(components, exclusionList = []) {
  const leafNodes = {}
  components.forEach((comp) => {
    const leaf = extractLeafNode(comp.namespace)
    if (!exclusionList.includes(leaf)) {
      if (!leafNodes[leaf]) leafNodes[leaf] = []
      leafNodes[leaf].push(comp.name)
    }
  })

  return Object.entries(leafNodes)
    .filter(([leaf, comps]) => comps.length > 1)
    .map(([leaf, comps]) => ({
      pattern: leaf,
      components: comps,
      suggestion: 'Consider consolidating these components',
    }))
}
```

### Shared Class Usage Alert

```javascript
// Alert if class is used by multiple components
function checkSharedClasses(components, exclusionList = []) {
  const classUsage = {}
  components.forEach((comp) => {
    comp.imports.forEach((imp) => {
      if (!exclusionList.includes(imp)) {
        if (!classUsage[imp]) classUsage[imp] = []
        classUsage[imp].push(comp.name)
      }
    })
  })

  return Object.entries(classUsage)
    .filter(([cls, users]) => users.length > 1)
    .map(([cls, users]) => ({
      class: cls,
      usedBy: users,
      suggestion: 'Consider extracting to shared component or library',
    }))
}
```
