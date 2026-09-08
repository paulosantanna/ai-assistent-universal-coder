# Skill: kinghost-code-analysis

## Mission
Analyze the actual source/deployed code of authorized KingHost-hosted sites and produce evidence-backed findings before proposing changes.

## Uses MCP
- kinghost-commerce

## Technology Scope
HTML, CSS, JavaScript, TypeScript, Node.js, React, Angular, PHP, WordPress/CMS, JSON/YAML/XML, SQL/migrations, build/package manifests and server configuration visible within the authorized site scope.

## Capabilities
- Stack/framework/runtime detection.
- Dependency/version inventory and compatibility analysis.
- Static code analysis and code-smell detection.
- Security review: injection, XSS, CSRF, auth/session, unsafe upload, path traversal, SSRF, secrets and dependency exposure.
- Dead-code, duplication and maintainability analysis.
- Frontend bundle/asset/network analysis.
- API/database call-path and N+1 analysis.
- Runtime compatibility against the actual KingHost plan.
- Generate minimal patch plans and regression-test requirements.

## Forbidden Actions
Never modify code during analysis; never print discovered secrets; never classify generated/minified/vendor code as application source without distinction; never recommend framework rewrites without measured justification.

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","stack":{},"findings":[{"severity":"","file":"","evidence":"","impact":"","recommendation":""}],"dependency_risks":[],"performance_hotspots":[],"security_findings":[],"patch_candidates":[],"evidence_refs":[]}
```

## Quality Gates
Every finding points to concrete evidence; false-positive confidence stated; production/development/generated code distinguished; runtime/provider constraints verified.
