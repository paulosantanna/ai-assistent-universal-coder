<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Best Practices

### Do's ✅

- Ensure components exist only as leaf nodes
- Remove orphaned classes from root namespaces
- Choose flattening strategy based on functionality
- Consolidate when functionality is related
- Split when functionality is distinct
- Extract shared code to `.shared` components
- Update all references after flattening
- Verify changes with tests

### Don'ts ❌

- Don't leave orphaned classes in root namespaces
- Don't create components on top of other components
- Don't skip updating imports after moving files
- Don't flatten without analyzing impact
- Don't mix flattening strategies inconsistently
- Don't ignore shared code when flattening
- Don't skip testing after refactoring
