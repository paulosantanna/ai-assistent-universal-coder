<!-- Package: 00_skills/(architecture)/component-flattening-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Checklist

**Structure Mapping**:

- [ ] Mapped all namespace hierarchies
- [ ] Identified root namespaces
- [ ] Located all source files
- [ ] Marked leaf nodes (components)

**Orphaned Class Detection**:

- [ ] Scanned root namespaces for source files
- [ ] Identified orphaned classes
- [ ] Classified orphaned classes (shared/domain/mixed)
- [ ] Assessed impact and dependencies

**Flattening Analysis**:

- [ ] Analyzed consolidation option
- [ ] Analyzed splitting option
- [ ] Analyzed shared code extraction option
- [ ] Selected best strategy for each root namespace

**Plan Creation**:

- [ ] Selected flattening strategy
- [ ] Created refactoring steps
- [ ] Estimated effort and risk
- [ ] Prioritized work

**Execution**:

- [ ] Moved files to target namespaces
- [ ] Updated imports and references
- [ ] Updated namespace declarations
- [ ] Verified changes with tests
