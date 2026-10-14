# Evidence, local conventions and report format

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2739–IMG_2748.

The photo's corporate flow mounts secrets at /etc/credentials, materializes runtime properties and refers to keys in configuration. A path/key placeholder is not a hardcoded secret. Verify this flow in the actual repo; record secret names/locations only. Do not read credentials to prove configuration wiring.
Gateway authorization is acceptable only with actual trust-boundary/route-policy evidence; inspect bypass paths and object/tenant authorization. Absence of @PreAuthorize does not by itself prove absence of authorization, and a gateway assumption does not prove protection. Missing runtime evidence is unknown.
Contract-first Resource/delegate code begins validation in its real OpenAPI contract. Preserve contract generation patterns; do not add hand-written duplicate controllers because a generic guide uses them.
Do not classify HTTP localhost or non-Secure local development cookies as production findings. Prove production environment and access path; inspect CSP/frame policies at the edge before asserting they do not exist. HSTS changes require domain/TLS readiness and authorization.
SSRF: show untrusted control of the resolved host and missing restrictions, not just new URL or Camel toD. Crypto/deserialization: verify the unsafe algorithm/input path, never assert prevalence from a photo. A structured security control in code may still need runtime proof.
Reports: executive summary in PT-BR, critical/high/medium/low sections, numeric ID, file:line, risk class, impact, source→sink and confidence, verification and unavailable evidence. Mask secret values completely. Corrections: source scope, behavioral compatibility, smallest useful check and project exceptions; no unconditional commit/push/publication.
Examples: filter-query endpoint → inspect contract validation and parameterized query; chat component → inspect interpolation, sanitizer and trust bypass before calling XSS; concrete PR security review → revisar-seguranca-pr; known package CVE → cve-remediation.
