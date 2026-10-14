<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Common Patterns to Look For

### High Consolidation Candidates

- **Notification**: `*.notification`, `*.notify`, `*.email`
- **Audit**: `*.audit`, `*.auditing`, `*.log`
- **Validation**: `*.validation`, `*.validate`, `*.validator`
- **Formatting**: `*.format`, `*.formatter`, `*.formatting`
- **Reporting**: `*.report`, `*.reporting` (if similar functionality)

### Low Consolidation Candidates

- **Infrastructure**: `*.util`, `*.helper`, `*.common` (usually infrastructure)
- **Different contexts**: Same name, different business meaning
- **High coupling risk**: Consolidation would create bottleneck
