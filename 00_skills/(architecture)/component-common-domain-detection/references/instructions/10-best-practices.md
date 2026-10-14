<!-- Package: 00_skills/(architecture)/component-common-domain-detection; relative command/resource examples resolve from that package or workspace root. -->

## Best Practices

### Do's ✅

- Distinguish domain from infrastructure functionality
- Analyze coupling impact before consolidating
- Consider both shared service and shared library approaches
- Look for namespace patterns AND shared classes
- Verify functionality is truly similar before consolidating
- Calculate coupling metrics (CA) before and after

### Don'ts ❌

- Don't consolidate infrastructure functionality (handled separately)
- Don't consolidate without analyzing coupling impact
- Don't assume all common patterns should be consolidated
- Don't ignore differences in functionality
- Don't consolidate if coupling increase is too high
- Don't mix domain and infrastructure in same analysis
