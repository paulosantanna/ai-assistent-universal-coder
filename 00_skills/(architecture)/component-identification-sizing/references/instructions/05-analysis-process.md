<!-- Package: 00_skills/(architecture)/component-identification-sizing; relative command/resource examples resolve from that package or workspace root. -->

## Analysis Process

### Phase 1: Identify Components

Scan the codebase directory structure:

1. **Map directory/namespace structure**
   - For Node.js: `services/`, `routes/`, `models/`, `utils/`
   - For Java: Package structure (e.g., `com.company.domain.service`)
   - For Python: Module paths (e.g., `app/billing/payment`)

2. **Identify leaf nodes**
   - Components are the deepest directories containing source files
   - Example: `services/BillingService/` is a component
   - Example: `services/BillingService/payment/` extends it, making `BillingService` a subdomain

3. **Create component inventory**
   - List each component with its namespace/path
   - Note any parent namespaces (subdomains)

### Phase 2: Calculate Size Metrics

For each component:

1. **Count statements**
   - Parse source files in component directory
   - Count executable statements (not comments, blank lines, or declarations alone)
   - Sum across all files in component

2. **Count files**
   - Total source files (`.js`, `.ts`, `.java`, `.py`, etc.)
   - Exclude test files, config files, documentation

3. **Calculate percentage**

   ```
   component_percent = (component_statements / total_statements) * 100
   ```

4. **Calculate statistics**
   - Mean component size: `total_statements / number_of_components`
   - Standard deviation: `sqrt(sum((size - mean)^2) / (n - 1))`
   - Component's deviation: `(component_size - mean) / std_dev`

### Phase 3: Identify Size Issues

**Oversized Components** (candidates for splitting):

- Exceeds 30% of total codebase (for small apps with <10 components)
- Exceeds 10% of total codebase (for large apps with >20 components)
- More than 2 standard deviations above mean
- Contains multiple distinct functional areas

**Undersized Components** (candidates for consolidation):

- Less than 1% of codebase (may be too granular)
- Less than 1 standard deviation below mean
- Contains only a few files with minimal functionality

**Well-Sized Components**:

- Between 1-2 standard deviations from mean
- Represents a single, cohesive functional area
- Appropriate percentage for application size
