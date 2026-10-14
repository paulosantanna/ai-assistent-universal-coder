<!-- Package: 00_skills/(architecture)/component-identification-sizing; relative command/resource examples resolve from that package or workspace root. -->

## Core Concepts

### Component Definition

A **component** is an architectural building block that:

- Has a well-defined role and responsibility
- Is identified by a namespace, package structure, or directory path
- Contains source code files (classes, functions, modules) grouped together
- Performs specific business or infrastructure functionality

**Key Rule**: Components are identified by **leaf nodes** in directory/namespace structures. If a namespace is extended (e.g., `services/billing` extended to `services/billing/payment`), the parent becomes a **subdomain**, not a component.

### Size Metrics

**Statements** (not lines of code):

- Count executable statements terminated by semicolons or newlines
- More accurate than lines of code for size comparison
- Accounts for code complexity, not formatting

**Component Size Indicators**:

- **Percent of codebase**: Component statements / Total statements
- **File count**: Number of source files in component
- **Standard deviation**: Distance from mean component size
