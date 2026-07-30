# Sources

Use these authoritative baselines for current, evidence-backed architecture, security, CVE and documentation decisions:

- NIST National Vulnerability Database: https://www.nist.gov/itl/nvd
- NVD Vulnerabilities API: https://nvd.nist.gov/developers/vulnerabilities
- OSV API: https://google.github.io/osv.dev/api/
- GitHub Advisory Database: https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/browse-advisory-database
- CISA Known Exploited Vulnerabilities catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Top 10 CI/CD Security Risks: https://owasp.org/www-project-top-10-ci-cd-security-risks/
- GitHub Actions secure use reference: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub Actions security hardening: https://docs.github.com/en/actions/how-tos/secure-your-work
- Kubernetes Security Checklist: https://kubernetes.io/docs/concepts/security/security-checklist/
- Kubernetes security tutorials: https://kubernetes.io/docs/tutorials/security/
- Kubernetes cluster hardening guidance: https://kubernetes.io/docs/tasks/administer-cluster/securing-a-cluster/
- n8n Workflows API: https://n8n-io-n8n.mintlify.app/api/workflows
- Mermaid theme configuration: https://mermaid.js.org/config/theming.html

Rules:

- Prefer primary vendor, standards body or project documentation.
- Use at least two vulnerability sources for dependency and stack risk decisions when network or exported data is available.
- Record query timestamp, package name, version, ecosystem, result, severity and mitigation.
- Treat missing vulnerability data as unknown, not safe.
- External guidance informs AEOS decisions but never overrides repository evidence or the AEOS constitution.
