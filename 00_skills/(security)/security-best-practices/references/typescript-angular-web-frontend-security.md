# Angular and TypeScript browser security

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2740–IMG_2748. Read for Angular frontends and verify the target version.

- Prefer template interpolation/text binding for untrusted text. Trace innerHTML, direct DOM writes and bypassSecurityTrust* through the actual context; Angular's built-in sanitization means an innerHTML binding alone is not proof of XSS.
- A trust bypass does not sanitize. Verify input provenance and an appropriate trusted boundary; do not convert arbitrary server strings into trusted HTML/URL/resource values.
- Review HttpClient/XSRF behavior for actual origin, cookie and endpoint patterns. Client route guards are UX controls; authorization must exist at the trusted server/gateway boundary.
- Inspect token storage/session design and data exposed in bundles, logs and browser errors. Never embed secrets in frontend code or claim localStorage is a secret vault.
- CSP/Trusted Types help constrain browser execution; inspect deployed edge/runtime policies before reporting absence. Do not silently add unsafe-inline/eval to make an implementation work.
- Check dependency/version advisories separately from secure-code review and preserve a repository's declared Angular major.

Normative source: [Angular Security](https://angular.dev/best-practices/security). Test the actual unsafe flow before calling a finding; record unavailable runtime/edge evidence.
