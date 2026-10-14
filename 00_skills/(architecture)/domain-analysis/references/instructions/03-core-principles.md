<!-- Package: 00_skills/(architecture)/domain-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Core Principles

### Subdomain Classification

**Core Domain**: Competitive advantage, highest business value, requires best developers

- Indicators: Complex business logic, frequent changes, domain experts needed

**Supporting Subdomain**: Essential but not differentiating, business-specific

- Indicators: Supports Core Domain, moderate complexity, business-specific rules

**Generic Subdomain**: Common functionality, could be outsourced

- Indicators: Well-understood problem, low differentiation, standard functionality

### Bounded Context

An explicit linguistic boundary where domain terms have specific, unambiguous meanings.

- Primary nature: Linguistic boundary, not technical
- Key rule: Inside boundary, all Ubiquitous Language terms are unambiguous
- Goal: Align 1 subdomain to 1 bounded context (ideal)
