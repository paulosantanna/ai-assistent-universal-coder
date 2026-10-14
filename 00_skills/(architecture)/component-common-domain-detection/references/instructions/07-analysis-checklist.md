<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Checklist

**Common Pattern Detection**:

- [ ] Scanned all component namespaces for common leaf nodes
- [ ] Identified components with same ending names
- [ ] Filtered out infrastructure patterns
- [ ] Grouped similar components

**Shared Class Detection**:

- [ ] Scanned imports/dependencies in each component
- [ ] Identified classes used by multiple components
- [ ] Classified as domain vs infrastructure
- [ ] Documented shared class usage

**Functionality Analysis**:

- [ ] Examined source code of common components
- [ ] Identified similarities and differences
- [ ] Assessed consolidation feasibility
- [ ] Determined if differences can be abstracted

**Coupling Assessment**:

- [ ] Calculated current coupling (CA) for each component
- [ ] Estimated consolidated coupling
- [ ] Compared total coupling levels
- [ ] Evaluated if coupling increase is acceptable

**Recommendations**:

- [ ] Suggested consolidation approach (service/library/merge)
- [ ] Prioritized recommendations by impact
- [ ] Created consolidation plan with steps
- [ ] Estimated expected benefits and risks
