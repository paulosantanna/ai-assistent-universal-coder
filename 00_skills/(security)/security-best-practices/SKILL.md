---
name: "security-best-practices"
description: "Write and review secure-by-default code by inspected language/framework: Java, Spring Boot 2/3, Apache Camel, Angular, Python, JavaScript/TypeScript and Go. Use for boas práticas de segurança, código Spring seguro, segurança do componente Angular or a prioritized secure-coding report. Do NOT use for a specific deep PR diff (revisar-seguranca-pr), CVE/EOL recon, dependency remediation or threat modeling."
license: "CC-BY-4.0"
metadata:
  author: "Tech Leads Club"
  version: "1.1.0"
  owner_agent: "codenavi-agent"
---

# security-best-practices

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.

## Workflow

1. Identify backend and frontend languages/frameworks from actual manifests, code and inherited parent/BOM. Corporate Arsenal names shown in photos are detection candidates, not proof of version.
2. Load every matching technology reference: [Java](references/java-general-backend-security.md), [Spring/Camel](references/java-spring-backend-security.md), [Angular](references/typescript-angular-web-frontend-security.md), and retained Python/JS/Go references only for matching scope.
3. Select the requested mode: secure generation/edits; passive high-impact detection in touched code; or an evidence-backed prioritized report. Do not expand passive detection into an unsolicited full audit.
4. Apply [project context and reporting](references/project-security-context.md). Prove source → dangerous sink, reachable attack path, existing defenses and impact. Do not infer exploitability from a keyword.
5. Trace secrets by runtime reference, authorization by actual gateway/service boundary, contract validation from real OpenAPI/delegate and environment-specific TLS/cookies. Corporate conventions apply only when evidenced; absent code-level annotation alone is not a finding.
6. Emit numeric IDs, severity, file:line, risk class, attacker impact, confidence, evidence and limitations; default output security_best_practices_report.md. “No findings in inspected scope” requires a list of checked controls, not a fabricated clean bill.
7. Perform only remediation already authorized by the request. Fix one root cause at a time, verify behavior/compatibility and honor documented safe project exceptions. Report-only requests do not authorize edits; update requests need no repeated local-edit approval.

## Inputs, output and stop

Input: authorized source and requested review/edit scope. Output: secure code or prioritized report with actual verification and gaps.
Never copy secret values into chat/reports/notebook. Read-only mirrors are reported, not patched. Remote publication, push/merge and deployment follow their own available authorized workflows.
If no reference covers the stack, inspect current official documentation and disclose the coverage gap; never invent a rule or finding. Retained original/source modules are historical where they conflict with this entry.
Source: IMG_2739–IMG_2748.

## Examples and failure handling

Example: “write this filter endpoint securely” → inspect Java/Spring/contract and use validation/parameterized queries; “check Angular chat rendering” → trace data/sanitizer/trust before alleging XSS. Error: absent edge policy evidence → report unknown, not missing protection.

## Retained resources

- Read [retained golang-general-backend-security](references/golang-general-backend-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-express-web-server-security](references/javascript-express-web-server-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-general-web-frontend-security](references/javascript-general-web-frontend-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-jquery-web-frontend-security](references/javascript-jquery-web-frontend-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-typescript-nextjs-web-server-security](references/javascript-typescript-nextjs-web-server-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-typescript-react-web-frontend-security](references/javascript-typescript-react-web-frontend-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained javascript-typescript-vue-web-frontend-security](references/javascript-typescript-vue-web-frontend-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained lenses](references/lenses) only for its matching mode; this entry and root governance take precedence.
- Read [retained ORIGINAL_SKILL](references/ORIGINAL_SKILL.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained package-notes](references/package-notes.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained provenance](references/provenance.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained python-django-web-server-security](references/python-django-web-server-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained python-fastapi-web-server-security](references/python-fastapi-web-server-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained python-flask-web-server-security](references/python-flask-web-server-security.md) only for its matching mode; this entry and root governance take precedence.
- Read [retained tlc](references/tlc) only for its matching mode; this entry and root governance take precedence.
- Read [retained usage-and-verification](references/usage-and-verification.md) only for its matching mode; this entry and root governance take precedence.
