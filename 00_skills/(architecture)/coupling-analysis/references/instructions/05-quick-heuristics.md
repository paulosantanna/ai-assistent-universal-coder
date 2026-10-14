<!-- Package: 00_skills/(architecture)/coupling-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Quick Heuristics

**For Integration Strength**:

- "If I change an internal detail of module X, how many other modules need to change?"
- "Was the integration contract designed to be public, or is it accidental?"
- "Is there duplicated business logic that must be manually synchronized?"

**For Distance**:

- "What's the cost of making a change that affects both modules?"
- "Do teams maintaining these modules need to coordinate deployments?"
- "If one module fails, does the other stop working?"

**For Volatility**:

- "Does this module encapsulate competitive business advantage?"
- "Does the business team frequently request changes in this area?"
- "Is there a history of many refactors in this area?"

**For Balance**:

- "Do components that need to change together live together in the code?"
- "Are independent components well separated?"
- "Where is there strong coupling with volatile and distant components?" (→ this is the main problem)
