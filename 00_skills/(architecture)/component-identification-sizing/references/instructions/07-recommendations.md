<!-- Package: 00_skills/(architecture)/component-identification-sizing; relative command/resource examples resolve from that package or workspace root. -->

## Recommendations

### High Priority: Split Large Components

**Reporting Component** (33% of codebase):
- **Current**: Single component with 27,765 statements
- **Issue**: Too large, contains multiple functional areas
- **Recommendation**: Split into:
  1. Reporting Shared (common utilities)
  2. Ticket Reports (ticket-related reports)
  3. Expert Reports (expert-related reports)
  4. Financial Reports (financial reports)
- **Expected Result**: Each component ~7-9% of codebase

### Medium Priority: Review Small Components

**Login Component** (2% of codebase):
- **Current**: 1,865 statements, 3 files
- **Consideration**: May be too granular if related to broader authentication
- **Recommendation**: Evaluate if should be consolidated with Authentication/User components

### Low Priority: Monitor Well-Sized Components

Most components are appropriately sized. Continue monitoring during decomposition.
````

## Analysis Checklist

**Component Identification**:

- [ ] Mapped all directory/namespace structures
- [ ] Identified leaf nodes (components) vs parent nodes (subdomains)
- [ ] Created complete component inventory
- [ ] Documented namespace/path for each component

**Size Calculation**:

- [ ] Counted statements (not lines) for each component
- [ ] Counted source files (excluding tests/configs)
- [ ] Calculated percentage of total codebase
- [ ] Calculated mean and standard deviation

**Size Assessment**:

- [ ] Identified oversized components (>threshold or >2 std dev)
- [ ] Identified undersized components (<1% or <1 std dev)
- [ ] Flagged components for splitting or consolidation
- [ ] Documented size distribution

**Recommendations**:

- [ ] Suggested splits for oversized components
- [ ] Suggested consolidations for undersized components
- [ ] Prioritized recommendations by impact
- [ ] Created architecture stories for refactoring

## Implementation Notes

### For Node.js/Express Applications

Components typically found in:

- `services/` - Business logic components
- `routes/` - API endpoint components
- `models/` - Data model components
- `utils/` - Utility components
- `middleware/` - Middleware components

**Example Component Identification**:

```
services/
├── BillingService/          ← Component (leaf node)
│   ├── index.js
│   └── BillingService.js
├── CustomerService/          ← Component (leaf node)
│   └── CustomerService.js
└── NotificationService/      ← Component (leaf node)
    └── NotificationService.js
```

### For Java Applications

Components identified by package structure:

- `com.company.domain.service` - Service components
- `com.company.domain.model` - Model components
- `com.company.domain.repository` - Repository components

**Example Component Identification**:

```
com.company.billing.payment   ← Component (leaf package)
com.company.billing.history   ← Component (leaf package)
com.company.billing           ← Subdomain (parent of payment/history)
```

### Statement Counting

**JavaScript/TypeScript**:

- Count statements terminated by `;` or newline
- Include: assignments, function calls, returns, conditionals, loops
- Exclude: comments, blank lines, declarations without assignment

**Java**:

- Count statements terminated by `;`
- Include: method calls, assignments, returns, conditionals
- Exclude: class/interface declarations, comments, blank lines

**Python**:

- Count executable statements (not comments or blank lines)
- Include: assignments, function calls, returns, conditionals
- Exclude: docstrings, comments, blank lines

## Fitness Functions

After identifying and sizing components, create automated checks:

### Component Size Threshold

```javascript
// Alert if any component exceeds 10% of codebase
function checkComponentSize(components, threshold = 0.1) {
  const totalStatements = components.reduce((sum, c) => sum + c.statements, 0)
  return components
    .filter((c) => c.statements / totalStatements > threshold)
    .map((c) => ({
      component: c.name,
      percent: ((c.statements / totalStatements) * 100).toFixed(1),
      issue: 'Exceeds size threshold',
    }))
}
```

### Standard Deviation Check

```javascript
// Alert if component is >2 standard deviations from mean
function checkStandardDeviation(components) {
  const sizes = components.map((c) => c.statements)
  const mean = sizes.reduce((a, b) => a + b, 0) / sizes.length
  const stdDev = Math.sqrt(sizes.reduce((sum, size) => sum + Math.pow(size - mean, 2), 0) / (sizes.length - 1))

  return components
    .filter((c) => Math.abs(c.statements - mean) > 2 * stdDev)
    .map((c) => ({
      component: c.name,
      deviation: ((c.statements - mean) / stdDev).toFixed(2),
      issue: 'More than 2 standard deviations from mean',
    }))
}
```

## Best Practices

### Do's ✅

- Use statements, not lines of code
- Identify components as leaf nodes only
- Calculate both percentage and standard deviation
- Consider application size when setting thresholds
- Document namespace/path for each component
- Create visual size distribution if possible

### Don'ts ❌

- Don't count test files in component size
- Don't treat parent directories as components
- Don't use fixed thresholds without considering app size
- Don't ignore small components (may need consolidation)
- Don't skip standard deviation calculation
- Don't mix infrastructure and domain components in same analysis

## Next Steps

After completing component identification and sizing:

1. **Apply Gather Common Domain Components Pattern** - Identify duplicate functionality
2. **Apply Flatten Components Pattern** - Remove orphaned classes from root namespaces
3. **Apply Determine Component Dependencies Pattern** - Analyze coupling between components
4. **Create Component Domains** - Group components into logical domains

## Notes

- Component size thresholds vary by application size
- Small apps (<10 components): 30% threshold may be appropriate
- Large apps (>20 components): 10% threshold is more appropriate
- Standard deviation is more reliable than fixed percentages
- Well-sized components are 1-2 standard deviations from mean
- Oversized components often contain multiple functional areas that can be split
