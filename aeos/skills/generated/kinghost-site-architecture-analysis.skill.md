# Skill: kinghost-site-architecture-analysis

## Mission
Reverse-map and evaluate the deployed architecture of authorized KingHost sites from evidence rather than assumptions.

## Uses MCP
- kinghost-commerce

## Analysis Dimensions
- domain/DNS/TLS topology
- hosting/runtime/process model
- frontend/backend boundaries
- APIs and external integrations
- database/storage/cache topology
- authentication/session model
- background jobs/cron/event flows
- commerce/marketplace adapters and webhooks
- deployment/release topology
- observability/logging
- performance/scalability constraints
- security/trust boundaries
- availability, backup, disaster recovery and rollback

## Workflow
Inventory -> evidence graph -> dependency graph -> data-flow/trust-boundary map -> bottleneck/failure-domain analysis -> architecture fitness assessment -> prioritized recommendations.

## Required Outputs
- C4-like context/container/component map where evidence permits.
- Runtime/dependency graph.
- Data-flow and trust-boundary map.
- SPOF and failure-propagation analysis.
- Current-state vs target-state architecture.
- ADR candidates with trade-offs.
- Migration sequence that respects actual KingHost constraints.

## Forbidden Actions
Do not invent hidden components; do not infer cloud-native/container capabilities from application code; do not call an architecture scalable/secure/highly available without evidence; do not mutate the environment.

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","current_architecture":{},"dependencies":[],"data_flows":[],"trust_boundaries":[],"failure_domains":[],"fitness":{},"target_architecture":{},"adrs":[],"migration_plan":[],"evidence_refs":[]}
```

## Quality Gates
Every component marked observed|inferred|unknown; inferred components include confidence; failure propagation analyzed; target architecture constrained by business need and hosting capabilities.
