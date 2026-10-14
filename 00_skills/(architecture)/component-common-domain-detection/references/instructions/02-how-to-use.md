<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## How to Use

### Quick Start

Request analysis of your codebase:

- **"Find common domain functionality across components"**
- **"Identify duplicate domain logic that should be consolidated"**
- **"Detect shared classes used across multiple components"**
- **"Analyze consolidation opportunities for common components"**

### Usage Examples

**Example 1: Find Common Functionality**

```
User: "Find common domain functionality across components"

The skill will:
1. Scan component namespaces for common patterns
2. Detect shared classes used across components
3. Identify duplicate domain logic
4. Analyze coupling impact of consolidation
5. Suggest consolidation opportunities
```

**Example 2: Detect Duplicate Notification Logic**

```
User: "Are there multiple notification components that should be consolidated?"

The skill will:
1. Find all components with notification-related names
2. Analyze their functionality and dependencies
3. Calculate coupling impact if consolidated
4. Recommend consolidation approach
```

**Example 3: Analyze Shared Classes**

```
User: "Find classes that are shared across multiple components"

The skill will:
1. Identify classes imported/used by multiple components
2. Classify as domain vs infrastructure functionality
3. Suggest consolidation or shared library approach
4. Assess impact on coupling
```

### Step-by-Step Process

1. **Scan Components**: Identify components with common namespace patterns
2. **Detect Shared Code**: Find classes/files used across components
3. **Analyze Functionality**: Determine if functionality is truly common
4. **Assess Coupling**: Calculate coupling impact before consolidation
5. **Recommend Actions**: Suggest consolidation or shared library approach
