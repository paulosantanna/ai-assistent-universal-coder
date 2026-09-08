# Skill: web-modernization-performance

## Mission
Restyle, modernize and improve the performance, accessibility, maintainability and security of KingHost-hosted web applications without trading correctness for benchmark scores.

## Technology Scope
HTML, CSS, JavaScript, TypeScript, Node.js, React, Angular, PHP, WordPress/CMS frontends, static assets, SQL-backed applications and supported KingHost runtimes.

## Allowed Actions
- Inventory framework/runtime versions and dependency constraints.
- Establish baseline Core Web Vitals, backend latency, error rate, query latency, CPU/memory pressure and asset budgets.
- Plan CSS/design-system refactoring, responsive layouts, accessibility and semantic HTML improvements.
- Plan code splitting, lazy loading, image/font optimization, caching, compression and static-asset strategies.
- Analyze N+1 queries, indexes, connection usage, payload size, API waterfalls and server-side bottlenecks.
- Propose framework/runtime upgrades only after compatibility and hosting constraints are verified.
- Define before/after benchmarks and regression gates.

## Forbidden Actions
- Claim performance gains without reproducible evidence.
- Remove security, accessibility, observability or correctness checks to improve scores.
- Rewrite a stable application solely because a newer framework exists.
- Assume SSR, containers, persistent processes or specific Node/PHP versions are supported by the hosting plan.

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","baseline":{},"bottlenecks":[],"changes":[],"budgets":{},"validation":[],"rollback":[],"evidence_refs":[]}
```

## Quality Gates
- Baseline exists before optimization.
- Each proposed change maps to a measured bottleneck or explicit maintainability/accessibility objective.
- Hosting constraints are verified.
- Core Web Vitals and server-side budgets are both considered.
- Security headers, CSP strategy, dependency risk and secret handling are preserved or improved.
- Rollback and regression checks exist.
